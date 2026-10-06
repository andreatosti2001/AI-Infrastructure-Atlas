"""Checks for the SQL layer (S14; docs/architecture/sql-layer.md; D-118 to D-121).

The SQL layer loads the canonical JSON files into a DuckDB database held in memory, runs the queries
in sql/, and writes each result to sql/results/. These checks make five things impossible: a result
that is not a fresh run of the current inputs; a database that differs between two builds; an unknown
that reaches SQL or a result as NULL, zero or another state; a result row that does not lead back to
canonical records; a tutorial that shows a different query from the one that was run.

WH-1  two builds from the same inputs give byte-identical results
WH-2  every committed result equals a fresh run, and records the digests of its inputs and query
WH-3  the loader knows every key of every record kind and refuses an unknown one
WH-4  NULL appears only in a _value column whose _state says why; no result cell is NULL
WH-5  explicit states survive as themselves: a planted not_publicly_determinable reaches the result
      distinct from not_researched
WH-6  every ID in a result row resolves to a canonical record; each row's sources are recomputed
      without SQL and match
WH-7  staging records are never loaded
WH-8  every query ends in ORDER BY; no database file is written inside the repository
WH-9  each query file is a tutorial: a question, a reading guide and steps, and the steps rebuild the
      file exactly; a metric's file also answers the eight questions of PROJECT-EVALUATION-FRAMEWORK.md
      §8 in its header (S15, D-131)
WH-10 the first result equals an independent computation of the same definitions in plain Python,
      including where each evidence date comes from (S15, D-129)
WH-11 (S15) a query may read an earlier query's result as a view; a result records the query files it
      builds on, and a changed upstream query makes the dependent result stale
WH-12 (S15) evidence coverage equals an independent computation over the independent first result
WH-13 (S15) source age equals an independent computation; moving the reference date changes the ages
      and nothing else
WH-14 (S15) the supplier metrics equal an independent computation; with no supplier named, all three are
      "cannot be computed yet", and a planted unknown keeps its own word

Uses the pinned DuckDB (requirements-analysis.txt, D-118) through tools/warehouse.py.
Run alone: python -m unittest discover -s tests -p "test_warehouse.py" -v
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
SQL = REPO_ROOT / "sql"
RESULTS = SQL / "results"
FIRST = "accelerator_dependencies"
# S15: the metrics, each built on the first result, and the eight header fields every metric answers (PEF §8).
COVERAGE, AGE, SUPPLIERS = "evidence_coverage", "source_age", "supplier_metrics"
METRICS = (COVERAGE, AGE, SUPPLIERS)
PEF_FIELDS = ("question", "population", "denominator", "assumptions", "missing data", "reproduce", "sensitivity", "does not prove")
HEADER_FIELDS = PEF_FIELDS + ("reading",)
sys.path.insert(0, str(REPO_ROOT / "tools"))

STATE_WORDS = {"not_researched", "not_publicly_determinable", "not_applicable", "not_stated", "undated", "no_record", "not_re_read", "not_recorded", "absent"}


def warehouse():
    import warehouse as module  # noqa: PLC0415 (imported late: the checks are written before the loader)

    return module


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def query_files() -> list[Path]:
    return sorted(SQL.glob("*.sql"))


# --- the tutorial format, read independently of the page build (WH-9) ---------------------------


def tutorial(text: str) -> dict:
    """Split a query file into its header fields and its steps; every line lands in exactly one part."""
    lines = text.split("\n")
    header, steps, field = {}, [], None
    i = 0
    while i < len(lines) and not lines[i].startswith("-- step:"):
        line = lines[i]
        m = re.match(r"^-- (" + "|".join(HEADER_FIELDS) + r"): (.*)$", line)
        if m:
            field = m.group(1)
            header[field] = m.group(2).strip()
        elif line.startswith("--   ") and field:
            header[field] += " " + line[5:].strip()
        elif line in ("--", ""):
            field = None
        else:
            raise AssertionError(f"line {i + 1}: not part of the tutorial header: {line!r}")
        i += 1
    while i < len(lines):
        title = lines[i].removeprefix("-- step:").strip()
        i += 1
        explanation = []
        while i < len(lines) and lines[i].startswith("-- ") and not lines[i].startswith("-- step:"):
            explanation.append(lines[i][3:].strip())
            i += 1
        code = []
        while i < len(lines) and not lines[i].startswith("-- step:"):
            code.append(lines[i])
            i += 1
        steps.append({"title": title, "explanation": " ".join(explanation), "code": "\n".join(code).strip("\n")})
    return {"header": header, "steps": steps, "lines": lines}


# --- an independent computation of the first result (WH-10) -------------------------------------


class Records:
    def __init__(self, data: Path) -> None:
        self.claims = {c["id"]: c for c in load_json(data / "claims.json")}
        self.sources = {s["id"]: s for s in load_json(data / "sources.json")}
        self.entities = {}
        for kind in ("companies", "jurisdictions", "technologies", "components", "products", "facilities"):
            self.entities.update({r["id"]: r for r in load_json(data / f"{kind}.json")})
        self.edges = load_json(data / "relationships.json")
        self.candidates = load_json(data / "refused_candidates.json")
        self.basis = load_json(data / "identity_basis.json")

    def reached(self, claim_ids) -> list[str]:
        seen, todo = [], list(claim_ids)
        while todo:
            cid = todo.pop(0)
            if cid not in seen:
                seen.append(cid)
                todo += self.claims[cid].get("input_claim_ids", [])
        return seen

    def evidence_date(self, claim: dict, source: dict) -> str:
        """F-1 (company-dataset.md §9)."""
        return self.dated(claim, source)[0]

    @staticmethod
    def dated(claim: dict, source: dict) -> tuple[str, str]:
        """F-1's evidence date and where it comes from: as_of, stated or accessed (S15, D-129)."""
        if isinstance(claim.get("as_of"), str):
            return claim["as_of"], "as_of"
        if isinstance(source["stated_dates"], list):
            return max(d["date"] for d in source["stated_dates"]), "stated"
        return source["retrieval"]["accessed_at"][:10], "accessed"

    def evidence(self, claim_ids) -> dict:
        reached = self.reached(claim_ids)
        cites = [(self.claims[c], cit) for c in reached for cit in self.claims[c].get("citations", [])]
        dated = [self.dated(c, self.sources[cit["source_id"]]) for c, cit in cites]
        dates = sorted(d for d, _ in dated)
        weakest = ("accessed", "stated", "as_of")  # when kinds share a date, the weakest is reported

        def basis_of(date: str) -> str:
            kinds = {k for d, k in dated if d == date}
            return next(k for k in weakest if k in kinds)
        sources = sorted({cit["source_id"] for _, cit in cites})
        unchecked = sorted({cit["source_id"] for _, cit in cites if cit["standing"] == "party" and isinstance(self.sources[cit["source_id"]]["publisher_entity"], dict)})
        return {
            "source_ids": sources,
            "publishers": sorted({self.sources[s]["publisher"] for s in sources}),
            "evidence_dated_from": dates[0] if dates else "not_applicable",
            "evidence_dated_to": dates[-1] if dates else "not_applicable",
            "evidence_dated_from_basis": basis_of(dates[0]) if dates else "not_applicable",
            "evidence_dated_to_basis": basis_of(dates[-1]) if dates else "not_applicable",
            "party_standing_unchecked": unchecked,
            "rests_on_atlas_interpretation": any(self.claims[c]["claim_type"] == "INTERPRETATION" for c in reached),
        }

    def accelerators(self) -> dict[str, tuple[str, str]]:
        """product ID -> (class, the claim that supports it)."""
        result = {}
        for pid, record in self.entities.items():
            if record["type"] != "product":
                continue
            for cls in record["instance_of"]:
                if cls == "component-ai-accelerator" or "component-ai-accelerator" in self.entities[cls].get("broader", []):
                    claim = next(r["claim_id"] for r in self.basis if r["kind"] == "instance_of_basis" and r["record"] == pid and r["class"] == cls)
                    result[pid] = (cls, claim)
        return result

    def rows(self) -> set[tuple]:
        out = set()
        for acc, (cls, cls_claim) in self.accelerators().items():
            direct = [e for e in self.edges if acc in (e["source_entity"], e["target_entity"])]
            links = [(e, "direct") for e in direct]
            todo = [(e, e["id"]) for e in direct if e["source_entity"] == acc and e["relation_type"] == "incorporates"]
            while todo:
                edge, via = todo.pop(0)
                for nxt in self.edges:
                    if nxt["source_entity"] == edge["target_entity"] and nxt["relation_type"] in ("incorporates", "requires"):
                        links.append((nxt, via))
                        todo.append((nxt, via))
            for edge, via in links:
                stated = any(self.claims[c]["claim_type"] == "FACT" for c in edge["claim_ids"])
                ev = self.evidence(edge["claim_ids"])
                out.add((acc, cls, cls_claim, edge["id"], via, "stated" if stated else "inferred", "not_applicable", tuple(sorted(edge["claim_ids"])), tuple(ev["source_ids"]), ev["evidence_dated_from"], ev["evidence_dated_to"], ev["evidence_dated_from_basis"], ev["evidence_dated_to_basis"], tuple(ev["publishers"]), tuple(ev["party_standing_unchecked"]), ev["rests_on_atlas_interpretation"]))
                supplier = edge.get("supplier")
                if isinstance(supplier, dict):
                    out.add((acc, cls, cls_claim, edge["id"], via, "gap", supplier["state"], (), (), "not_applicable", "not_applicable", "not_applicable", "not_applicable", (), (), False))
                for assertion in supplier if isinstance(supplier, list) else []:
                    claims = tuple(sorted(assertion["claim_ids"]))
                    basis = "stated" if any(self.claims[c]["claim_type"] == "FACT" for c in claims) else "inferred"
                    ev = self.evidence(claims)
                    out.add((acc, cls, cls_claim, edge["id"], via, basis, "not_applicable", claims, tuple(ev["source_ids"]), ev["evidence_dated_from"], ev["evidence_dated_to"], ev["evidence_dated_from_basis"], ev["evidence_dated_to_basis"], tuple(ev["publishers"]), tuple(ev["party_standing_unchecked"]), ev["rests_on_atlas_interpretation"]))
            for cand in self.candidates:
                if acc in cand["target_entities"] and cand["reasons"] == ["evidence_not_fresh"]:
                    claims = sorted(k["claim_id"] for k in cand["considered"] if "claim_id" in k)
                    ev = self.evidence(claims)
                    out.add((acc, cls, cls_claim, cand["id"], "direct", "gap", "evidence_not_fresh", tuple(claims), tuple(ev["source_ids"]), ev["evidence_dated_from"], ev["evidence_dated_to"], ev["evidence_dated_from_basis"], ev["evidence_dated_to_basis"], tuple(ev["publishers"]), tuple(ev["party_standing_unchecked"]), ev["rests_on_atlas_interpretation"]))
        return out


COMPARED = ("accelerator_id", "accelerator_class", "accelerator_class_claim", "record_id", "reached_through", "basis", "gap_reason", "claim_ids", "source_ids", "evidence_dated_from", "evidence_dated_to", "evidence_dated_from_basis", "evidence_dated_to_basis", "publishers", "party_standing_unchecked", "rests_on_atlas_interpretation")


def comparable(rows: list[dict]) -> set[tuple]:
    return {tuple(tuple(r[k]) if isinstance(r[k], list) else r[k] for k in COMPARED) for r in rows}


# --- independent computations of the S15 metrics (WH-12 to WH-14), from Records.rows(), never from SQL ---

IDX = {k: i for i, k in enumerate(COMPARED)}


def independent_coverage(rows: set[tuple]) -> dict[str, tuple]:
    """accelerator_id -> (links, stated, inferred, gap, records, shared)."""
    by_record: dict[str, set[str]] = {}
    for r in rows:
        by_record.setdefault(r[IDX["record_id"]], set()).add(r[IDX["accelerator_id"]])
    out = {}
    for acc in sorted({r[IDX["accelerator_id"]] for r in rows}):
        mine = [r for r in rows if r[IDX["accelerator_id"]] == acc]
        records = {r[IDX["record_id"]] for r in mine}
        basis = [r[IDX["basis"]] for r in mine]
        out[acc] = (len(mine), basis.count("stated"), basis.count("inferred"), basis.count("gap"), len(records), sum(1 for rec in records if len(by_record[rec]) > 1))
    return out


def reference_date(query_text: str) -> str:
    found = re.findall(r"DATE '(\d{4}-\d{2}-\d{2})' AS reference_date", query_text)
    assert len(found) == 1, "the source-age query must hold exactly one reference date"
    return found[0]


def independent_ages(rows: set[tuple], reference: str) -> set[tuple]:
    """(accelerator_id, record_id, gap_reason, newest, newest_basis, age_days, beyond_horizon) per row."""
    import datetime  # noqa: PLC0415

    ref = datetime.date.fromisoformat(reference)
    cutoff = ref.replace(year=ref.year - 1)  # 12 months before the reference date
    out = set()
    for r in rows:
        newest, basis = r[IDX["evidence_dated_to"]], r[IDX["evidence_dated_to_basis"]]
        if newest == "not_applicable":
            age = beyond = "not_applicable"
        else:
            start = datetime.date.fromisoformat({4: newest + "-01-01", 7: newest + "-01"}.get(len(newest), newest))
            age, beyond = str((ref - start).days), "yes" if start < cutoff else "no"
        out.add((r[IDX["accelerator_id"]], r[IDX["record_id"]], r[IDX["gap_reason"]], newest, basis, age, beyond))
    return out


def independent_suppliers(records: "Records", rows: set[tuple]) -> tuple:
    """(parts, parts_supplier_named, parts_supplier_unknown, unknown_state, supplies_links, status)."""
    edges = {e["id"]: e for e in records.edges}
    chain_parts = {r[IDX["record_id"]] for r in rows if r[IDX["record_id"]] in edges and edges[r[IDX["record_id"]]]["relation_type"] == "incorporates" and edges[r[IDX["record_id"]]]["source_entity"] == r[IDX["accelerator_id"]]}
    named = {e for e in chain_parts if isinstance(edges[e].get("supplier"), list) and edges[e]["supplier"]}
    unknown = {e for e in chain_parts if isinstance(edges[e].get("supplier"), dict)}
    states = sorted({edges[e]["supplier"]["state"] for e in unknown})
    items = {edges[e]["target_entity"] for e in chain_parts}
    supplies = sum(1 for e in records.edges if e["relation_type"] == "supplies" and e.get("item") in items)
    return (len(named | unknown), len(named), len(unknown), ", ".join(states) if states else "not_applicable", supplies, "cannot_be_computed_yet" if not named else "computable_not_yet_defined")


def copy_repo() -> Path:
    tmp = Path(tempfile.mkdtemp()) / "repo"
    for part in ("data", "sql", "tools", "schemas"):
        shutil.copytree(REPO_ROOT / part, tmp / part, ignore=shutil.ignore_patterns("__pycache__"))
    return tmp


# --- the checks -----------------------------------------------------------------------------------


class WarehouseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wh = warehouse()
        cls.fresh = cls.wh.build_results(DATA)

    def test_wh1_two_builds_are_identical(self) -> None:
        self.assertEqual(self.fresh, self.wh.build_results(DATA))

    def test_wh2_committed_results_equal_a_fresh_run(self) -> None:
        self.assertTrue(query_files(), "no query in sql/")
        self.assertEqual(sorted(self.fresh), sorted(f"sql/results/{q.stem}.json" for q in query_files()))
        for path, content in sorted(self.fresh.items()):
            with self.subTest(result=path):
                committed = REPO_ROOT / path
                self.assertTrue(committed.exists(), f"{path} is not committed (python tools/warehouse.py)")
                self.assertEqual(committed.read_bytes(), content, f"{path} is not a fresh run of the current inputs (python tools/warehouse.py)")

    def test_wh2_a_result_records_its_inputs_and_query(self) -> None:
        for query in query_files():
            result = load_json(RESULTS / f"{query.stem}.json")
            with self.subTest(query=query.name):
                self.assertEqual(result["query"], f"sql/{query.name}")
                self.assertEqual(result["query_sha256"], hashlib.sha256(query.read_bytes()).hexdigest())
                paths = [i["path"] for i in result["inputs"]]
                self.assertEqual(paths, sorted(paths))
                self.assertIn("tools/warehouse.py", paths)
                self.assertFalse(any(p.startswith("data/staging/") for p in paths))
                for item in result["inputs"]:
                    self.assertEqual(item["sha256"], hashlib.sha256((REPO_ROOT / item["path"]).read_bytes()).hexdigest(), item["path"])
                joined = "".join(f"{i['path']}\0{i['sha256']}\n" for i in result["inputs"])
                self.assertEqual(result["input_digest"], hashlib.sha256(joined.encode()).hexdigest())
                self.assertEqual(result["engine"], f"duckdb {self.wh.duckdb.__version__}")

    def test_wh3_an_unknown_key_is_refused(self) -> None:
        root = copy_repo()
        claims = load_json(root / "data/claims.json")
        claims[0]["confidence"] = "high"
        (root / "data/claims.json").write_text(json.dumps(claims), encoding="utf-8")
        with self.assertRaisesRegex(Exception, r"claims\.json.*confidence"):
            self.wh.load(root / "data")

    def test_wh4_null_only_beside_a_state(self) -> None:
        con = self.wh.load(DATA)
        for (table,) in con.execute("SELECT table_name FROM information_schema.tables ORDER BY table_name").fetchall():
            columns = [c for (c,) in con.execute("SELECT column_name FROM information_schema.columns WHERE table_name = ? ORDER BY ordinal_position", [table]).fetchall()]
            for column in columns:
                with self.subTest(table=table, column=column):
                    nulls = con.execute(f'SELECT count(*) FROM "{table}" WHERE "{column}" IS NULL').fetchone()[0]
                    if not column.endswith("_value"):
                        self.assertEqual(nulls, 0, "NULL outside a _value column")
                        continue
                    state = column.removesuffix("_value") + "_state"
                    self.assertIn(state, columns, f"{column} has no {state} beside it")
                    bad = con.execute(f'SELECT count(*) FROM "{table}" WHERE ("{column}" IS NULL) <> ("{state}" <> \'value\')').fetchone()[0]
                    self.assertEqual(bad, 0, f"{column} is NULL exactly when {state} is not 'value'")
                    states = {s for (s,) in con.execute(f'SELECT DISTINCT "{state}" FROM "{table}"').fetchall()}
                    self.assertLessEqual(states, STATE_WORDS | {"value"})
        for path, content in self.fresh.items():
            for row in json.loads(content)["rows"]:
                with self.subTest(result=path, row=row.get("record_id")):
                    self.assertNotIn(None, row.values())

    def test_wh5_planted_states_survive_as_themselves(self) -> None:
        root = copy_repo()
        edges = load_json(root / "data/relationships.json")
        h100 = next(e for e in edges if e["id"] == "rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory")
        h100["supplier"] = {"state": "not_publicly_determinable"}
        (root / "data/relationships.json").write_text(json.dumps(edges), encoding="utf-8")
        rows = json.loads(self.wh.build_results(root / "data")[f"sql/results/{FIRST}.json"])["rows"]
        reasons = {(r["accelerator_id"], r["gap_reason"]) for r in rows if r["basis"] == "gap" and r["record_id"].startswith("rel-")}
        self.assertIn(("product-nvidia-h100-tensor-core-gpu", "not_publicly_determinable"), reasons)
        self.assertIn(("product-amazon-com-trainium2", "not_researched"), reasons)
        con = self.wh.load(root / "data")
        tdp = con.execute("SELECT assertion_state, assertion_value FROM field_values WHERE record_id = 'product-nvidia-h100-tensor-core-gpu' AND field = 'tdp_w'").fetchall()
        self.assertEqual(tdp, [("not_researched", None)])

    def test_wh6_every_row_leads_back_to_canonical_records(self) -> None:
        records = Records(DATA)
        known = set(records.claims) | set(records.sources) | set(records.entities) | {e["id"] for e in records.edges} | {c["id"] for c in records.candidates}
        rows = json.loads(self.fresh[f"sql/results/{FIRST}.json"])["rows"]
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(row=row["record_id"]):
                for key in ("accelerator_id", "accelerator_class", "accelerator_class_claim", "record_id", "from_id", "to_id"):
                    self.assertIn(row[key], known | STATE_WORDS, key)
                self.assertIn(row["reached_through"], known | {"direct"})
                for key in ("claim_ids", "source_ids", "party_standing_unchecked"):
                    self.assertLessEqual(set(row[key]), known, key)
                self.assertEqual(row["source_ids"], records.evidence(row["claim_ids"])["source_ids"])

    def test_wh7_staging_is_never_loaded(self) -> None:
        root = copy_repo()
        edges = load_json(root / "data/relationships.json")
        planted = copy.deepcopy(edges[0])
        planted["id"] = "rel-product-nvidia-h100-tensor-core-gpu-incorporates-technology-3d-die-stacking"
        planted["target_entity"] = "technology-3d-die-stacking"
        (root / "data/staging/relationships.json").write_text(json.dumps([planted]), encoding="utf-8")
        result = json.loads(self.wh.build_results(root / "data")[f"sql/results/{FIRST}.json"])
        self.assertNotIn(planted["id"], {r["record_id"] for r in result["rows"]})
        con = self.wh.load(root / "data")
        self.assertEqual(con.execute("SELECT count(*) FROM relationships WHERE id = ?", [planted["id"]]).fetchone()[0], 0)

    def test_wh8_queries_end_in_order_by(self) -> None:
        for query in query_files():
            code = "\n".join(line for line in query.read_text(encoding="utf-8").splitlines() if not line.startswith("--"))
            with self.subTest(query=query.name):
                self.assertRegex(code.strip().rstrip(";"), r"(?is)\border\s+by\b[^()]*$", "the final SELECT has no ORDER BY")

    def test_wh8_no_database_file_inside_the_repository(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            self.wh.main(["--db", str(REPO_ROOT / "atlas.duckdb")])
        self.assertEqual(sorted(p for p in REPO_ROOT.rglob("*.duckdb") if ".git" not in p.parts), [])

    def test_wh9_each_query_file_is_a_tutorial(self) -> None:
        for query in query_files():
            text = query.read_text(encoding="utf-8")
            t = tutorial(text)
            with self.subTest(query=query.name):
                self.assertTrue(t["header"].get("question"), "no '-- question:' paragraph")
                self.assertTrue(t["header"].get("reading"), "no '-- reading:' paragraph")
                if query.stem in METRICS:
                    for field in PEF_FIELDS:
                        self.assertTrue(t["header"].get(field), f"a metric's header does not answer '{field}' (PEF §8)")
                self.assertGreaterEqual(len(t["steps"]), 2)
                for step in t["steps"]:
                    self.assertTrue(step["title"] and step["explanation"] and step["code"], f"step {step['title']!r} lacks a title, an explanation or code")
                    self.assertNotRegex(step["explanation"], r"\b(?:rel|claim|src|cand)-[a-z0-9]", "an explanation names a record; it explains the query, not the data")
                # nothing hides between the parts: header, titles, explanations and code rebuild the file
                code = "\n".join(s["code"] for s in t["steps"])
                stripped = "\n".join(line for line in text.splitlines() if not line.startswith("-- ") and line not in ("--",)).strip("\n")
                self.assertEqual(re.sub(r"\n+", "\n", code), re.sub(r"\n+", "\n", stripped))

    def test_wh10_the_first_result_equals_an_independent_computation(self) -> None:
        rows = json.loads(self.fresh[f"sql/results/{FIRST}.json"])["rows"]
        self.assertEqual(comparable(rows), Records(DATA).rows())
        keys = [(r["accelerator"], r["position"], r["record_id"], r["gap_reason"], r["from_id"]) for r in rows]
        self.assertEqual(keys, sorted(keys), "rows are not in the order the query states")
        self.assertEqual(len(keys), len(set(keys)), "two rows share a key")


    def test_wh10_a_tied_date_reports_its_weakest_kind(self) -> None:
        """The data has no tie today, so the rule is planted (S15 break M12 found it unexercised): one claim's
        as_of equals another source's stated date on the same row; the newest date must say 'stated'."""
        root = copy_repo()
        claims = load_json(root / "data/claims.json")
        next(c for c in claims if c["id"] == "claim-ecp-hbm-definition")["as_of"] = "2020-12"
        (root / "data/claims.json").write_text(json.dumps(claims), encoding="utf-8")
        rows = json.loads(self.wh.build_results(root / "data")[f"sql/results/{FIRST}.json"])["rows"]
        self.assertEqual(comparable(rows), Records(root / "data").rows())
        tied = [r for r in rows if r["relation"] == "requires"]
        self.assertTrue(tied)
        self.assertEqual({(r["evidence_dated_to"], r["evidence_dated_to_basis"]) for r in tied}, {("2020-12", "stated")}, "a tie between an as-of date and a stated date must report the weaker kind")

    # WH-11
    def test_wh11_a_query_reads_an_earlier_result_and_records_it(self) -> None:
        for stem in METRICS:
            with self.subTest(metric=stem):
                self.assertIn(f"sql/results/{stem}.json", self.fresh, f"no result for sql/{stem}.sql")
                result = json.loads(self.fresh[f"sql/results/{stem}.json"])
                self.assertIn(f"sql/{FIRST}.sql", [i["path"] for i in result["inputs"]], "a result does not record the query it builds on")
        root = copy_repo()
        first = root / "sql" / f"{FIRST}.sql"
        first.write_text(first.read_text(encoding="utf-8").replace("-- step:", "-- step: (edited)", 1), encoding="utf-8")
        fresh = self.wh.build_results(root / "data", sql=root / "sql")
        for stem in METRICS:
            with self.subTest(metric=stem):
                self.assertNotEqual(json.loads(fresh[f"sql/results/{stem}.json"])["input_digest"], json.loads(self.fresh[f"sql/results/{stem}.json"])["input_digest"], "a changed upstream query leaves the dependent result looking fresh")

    # WH-12
    def test_wh12_evidence_coverage_equals_an_independent_computation(self) -> None:
        rows = json.loads(self.fresh[f"sql/results/{COVERAGE}.json"])["rows"]
        for r in rows:  # first, so a wrong split reports this reason (S15 break M5)
            with self.subTest(accelerator=r["accelerator_id"]):
                self.assertEqual(r["stated"] + r["inferred"] + r["gap"], r["links"], "the parts do not add up to the denominator")
        got = {r["accelerator_id"]: (r["links"], r["stated"], r["inferred"], r["gap"], r["records"], r["shared"]) for r in rows}
        self.assertEqual(got, independent_coverage(Records(DATA).rows()))

    # WH-13
    def test_wh13_source_age_equals_an_independent_computation(self) -> None:
        text = (SQL / f"{AGE}.sql").read_text(encoding="utf-8")
        reference = reference_date(text)
        rows = json.loads(self.fresh[f"sql/results/{AGE}.json"])["rows"]
        got = {(r["accelerator_id"], r["record_id"], r["gap_reason"], r["newest_evidence"], r["newest_evidence_basis"], r["age_days"], r["beyond_horizon"]) for r in rows}
        self.assertEqual(got, independent_ages(Records(DATA).rows(), reference))
        self.assertEqual({r["reference_date"] for r in rows}, {reference})
        first = json.loads(self.fresh[f"sql/results/{FIRST}.json"])["rows"]
        self.assertEqual([(r["accelerator_id"], r["record_id"], r["gap_reason"], r["from_id"]) for r in rows], [(r["accelerator_id"], r["record_id"], r["gap_reason"], r["from_id"]) for r in first], "the ages are not the links of the table, in its order")

    def test_wh13_moving_the_reference_date_changes_the_ages_and_nothing_else(self) -> None:
        root = copy_repo()
        query = root / "sql" / f"{AGE}.sql"
        query.write_text(query.read_text(encoding="utf-8").replace("DATE '2026-10-06' AS reference_date", "DATE '2027-10-06' AS reference_date"), encoding="utf-8")
        before = json.loads(self.fresh[f"sql/results/{AGE}.json"])["rows"]
        after = json.loads(self.wh.build_results(root / "data", sql=root / "sql")[f"sql/results/{AGE}.json"])["rows"]
        moving = {"reference_date", "age_days", "beyond_horizon"}
        self.assertEqual(len(before), len(after))
        changed = set()
        for b, a in zip(before, after):
            changed |= {k for k in b if b[k] != a[k]}
            self.assertEqual({k: v for k, v in b.items() if k not in moving}, {k: v for k, v in a.items() if k not in moving})
        self.assertEqual(changed, moving, "moving the reference date must move the ages, and only the ages")
        self.assertEqual(independent_ages(Records(root / "data").rows(), "2027-10-06"), {(r["accelerator_id"], r["record_id"], r["gap_reason"], r["newest_evidence"], r["newest_evidence_basis"], r["age_days"], r["beyond_horizon"]) for r in after})

    # WH-14
    def test_wh14_supplier_metrics_equal_an_independent_computation(self) -> None:
        rows = json.loads(self.fresh[f"sql/results/{SUPPLIERS}.json"])["rows"]
        self.assertEqual([r["metric"] for r in rows], ["supplier count", "geographic concentration", "single-source relationships"])
        records = Records(DATA)
        want = independent_suppliers(records, records.rows())
        for r in rows:
            with self.subTest(metric=r["metric"]):
                self.assertEqual((r["parts"], r["parts_supplier_named"], r["parts_supplier_unknown"], r["unknown_state"], r["supplies_links"], r["status"]), want)
                self.assertTrue(r["needs"])
        self.assertEqual({r["status"] for r in rows}, {"cannot_be_computed_yet"}, "a supplier metric shows as computable while no supplier is named")

    def test_wh14_a_planted_unknown_keeps_its_word_in_every_metric(self) -> None:
        root = copy_repo()
        edges = load_json(root / "data/relationships.json")
        h100 = next(e for e in edges if e["id"] == "rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory")
        h100["supplier"] = {"state": "not_publicly_determinable"}
        (root / "data/relationships.json").write_text(json.dumps(edges), encoding="utf-8")
        fresh = self.wh.build_results(root / "data")
        suppliers = json.loads(fresh[f"sql/results/{SUPPLIERS}.json"])["rows"]
        self.assertEqual({r["unknown_state"] for r in suppliers}, {"not_publicly_determinable, not_researched"})
        self.assertEqual({r["parts_supplier_unknown"] for r in suppliers}, {2})
        coverage = {r["accelerator_id"]: r for r in json.loads(fresh[f"sql/results/{COVERAGE}.json"])["rows"]}
        self.assertEqual(coverage["product-nvidia-h100-tensor-core-gpu"]["gap"], 2, "an unknown left the gap count")
        ages = json.loads(fresh[f"sql/results/{AGE}.json"])["rows"]
        planted = [r for r in ages if r["gap_reason"] == "not_publicly_determinable"]
        self.assertEqual([(r["age_days"], r["beyond_horizon"]) for r in planted], [("not_applicable", "not_applicable")], "an unknown was given an age")


class WarehouseBreakTests(unittest.TestCase):
    """A changed input fails WH-2 for the reason it names, until the results are rebuilt."""

    def test_a_changed_query_file_makes_the_result_stale(self) -> None:
        wh = warehouse()
        root = copy_repo()
        query = root / "sql" / f"{FIRST}.sql"
        query.write_text(query.read_text(encoding="utf-8").replace("-- step:", "-- step: (edited)", 1), encoding="utf-8")
        fresh = wh.build_results(root / "data", sql=root / "sql")
        self.assertNotEqual(json.loads(fresh[f"sql/results/{FIRST}.json"])["query_sha256"], load_json(RESULTS / f"{FIRST}.json")["query_sha256"])


if __name__ == "__main__":
    unittest.main()
