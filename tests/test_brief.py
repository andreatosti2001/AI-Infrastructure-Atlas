"""Page checks for the S21 client brief: site/briefs/accelerator-memory/index.html.

S21 (docs/architecture/client-brief.md; D-202 to D-206). Standard library only. The brief is written by
tools/build_brief.py; these checks read the committed page and the data with their own loader (the DOM, homes and
contrast helpers of tests/test_page.py, the records of tests/test_journeys.py) and recompute every value the brief
shows. Three things come from tools, each the one home of its rule: the build's fixed words (as JR-1 reads them),
the policy status rule (tools/policy_status.py, D-156) and the HBM page's committed figure, which tests/test_page.py
checks against the records (PG-3, PG-5).

BR-1  every text node sits inside a record value, an absent value, a fixed label, a derived value or a framing
      block; no annotated value contains another; framing names no record and holds no digit;
BR-2  every record value equals its home; labels hold no digit and name no record; claims in panels are shown whole;
BR-3  every derived value (counts, result cells and flags, the as-of cell, statuses, the latest publication date,
      the evidence date range, the tutorial, inputs, the digest, pointers, byte matches, rule homes) equals an
      independent recomputation; every count names its unit and is never zero;
BR-4  the dependency map: the brief's figure draws the same marks, targets and bases as the HBM page's figure; every
      mark opens a panel on the brief; the result table shows every row of the result;
BR-5  the executive summary: each sentence cites exactly the rows or classes of its group, with their values, bases,
      periods, criteria, statuses and counts; a gap is never phrased as a link;
BR-6  the policy matrix: one row per class the chain reaches, one cell per act, each state equal to the records; every
      policy shown sits in, or links to, a block with its official text link and the no-advice line (LA-5); every
      status is derived on the as-of date;
BR-7  scope, limits, the boundary line, the as-of date and the input digest are in the first section, outside any
      disclosure and never hidden in print; rows shown equal rows in the result; the citation carries the same date
      and digest (U-5, P-18);
BR-8  every citation resolves: every source shown is a source record, and the source appendix lists exactly the
      sources the shown claims cite, each with its URL;
BR-9  no forbidden word in the Atlas's own voice: JR-9's list, plus advice and determination words;
BR-10 every link resolves; only source URLs point outside; nothing is loaded; no script;
BR-11 document structure (lang, one h1 equal to the title, landmarks, no skipped heading level, table headers with a
      scope, every SVG named), palette, contrast and a print stylesheet;
BR-12 the committed brief equals a rebuild; two builds are identical; no other file sits in site/briefs/.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_journeys as tj  # noqa: E402  (the records and the page reader; no test class is imported)
import test_page as tp  # noqa: E402  (the DOM, homes and contrast helpers)

BRIEF = "site/briefs/accelerator-memory/index.html"
HBM_PAGE = "site/hbm-chain/index.html"
DEP = "accelerator_dependencies"
DEP_RESULT = REPO_ROOT / "sql" / "results" / f"{DEP}.json"
AGE_RESULT = REPO_ROOT / "sql" / "results" / "source_age.json"
INPUT_GLOBS = tj.INPUT_GLOBS
INPUT_FILES = (
    "docs/architecture/company-dataset.md",
    "docs/architecture/decisions.md",
    "docs/architecture/relationship-taxonomy.md",
    "docs/research/source-policy.md",
    "tools/brief_template.html",
    "tools/build_brief.py",
    "tools/build_journeys.py",
    "tools/build_page.py",
    "tools/facility_status.py",
    "tools/journey_template.html",
    "tools/navigate.py",
    "tools/page_template.html",
    "tools/policy_status.py",
    "tools/trace.py",
)
NO_ADVICE = tj.NO_ADVICE
BOUNDARY = "This brief describes what the Atlas’s records hold. It is not legal, investment or procurement advice, and it makes no recommendation."
FORBIDDEN = tj.FORBIDDEN + ("should", "must", "recommend", "recommends", "recommended", "is controlled", "are controlled", "subject to the")
DERIVED_KINDS = {
    "count", "sql-cell", "sql-flag", "policy-status", "latest-published", "evidence-first", "evidence-last",
    "input-file", "input-digest", "pointer", "bytes-match", "rule-home", "no-activity-edge", "lane-unlinked",
    "sql-question", "sql-reading", "sql-step-title", "sql-step-text", "sql-step-code", "sql-file", "sql-digest", "sql-header",
}
SQL_FLAGS = tp.SQL_FLAGS
COUNT_UNITS = {
    # data-count -> the unit that must follow the number in its own line (V-4); the singular stem
    "accelerators": "accelerator", "rows-shown": "of", "rows-in-result": "row", "acts": "act", "chain-classes": "class",
    "classes-named": "of", "classes-refused": "of", "classes-none": "of", "unreached-named-by": "of",
}
SUMMARY_KINDS = ("depends", "made", "supplied", "texts-named", "texts-refused", "texts-none", "limits")


def dep() -> dict:
    return json.loads(DEP_RESULT.read_text(encoding="utf-8"))


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


def build_module():
    import build_brief  # noqa: PLC0415 (imported late: the checks are written before the build)

    return build_brief


class Records(tj.Records):
    """What the brief must show, read from data/ and the dependency result independently of the build."""

    def __init__(self) -> None:
        super().__init__()
        self.rows = dep()["rows"]
        self.by_id = {r["id"]: r for r in self.classes + self.products + self.companies}

    def chain_classes(self) -> list[str]:
        """Each accelerator's class with the classes it is narrower than, then every class at an end of a row
        (client-brief.md §3.4)."""
        found: list[str] = []
        for row in self.rows:
            cls = row["accelerator_class"]
            for c in self.by_id[cls].get("broader", []) + [cls]:
                if c not in found:
                    found.append(c)
        for row in self.rows:
            for end in (row["from_id"], row["to_id"]):
                if self.by_id.get(end, {}).get("type") in ("component", "technology") and end not in found:
                    found.append(end)
        return found

    def class_state(self, cid: str) -> str:
        if any(e["target_entity"] == cid for e in self.links):
            return "named"
        if any(cid in c["target_entities"] for c in self.policy_candidates):
            return "refused"
        return "none"

    def accelerators(self) -> list[str]:
        return list(dict.fromkeys(r["accelerator_id"] for r in self.rows))

    def latest_published(self) -> str:
        return max(e["date"] for e in self.events if e["event_type"] == "published" and e["subject"] in self.policy_ids)

    def key_entities(self) -> set[str]:
        """The companies at an end of a result row or named as a row's supplier, the vendors of the accelerators, and
        the accelerators themselves."""
        found = {r["from_id"] for r in self.rows if self.by_id.get(r["from_id"], {}).get("type") == "company"}
        found |= {self.by_id[a]["vendor"] for a in self.accelerators() if "vendor" in self.by_id[a]}
        return found | set(self.accelerators())

    def unreached(self) -> list[str]:
        """Classes a policy link names that the chain does not reach."""
        chain = set(self.chain_classes())
        return list(dict.fromkeys(e["target_entity"] for e in self.links if e["target_entity"] not in chain))


class BriefTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = Records()
        cls.homes = tp.Homes()
        cls.page = tj.Page(BRIEF)
        cls.on = tj.as_of()
        cls.rows = cls.records.rows

    def setUp(self) -> None:
        if not self.page.raw:
            self.fail(f"brief not built: {BRIEF} (python tools/build_brief.py)")

    def sections(self) -> dict:
        return {n.attrs["id"]: n for n in self.page.nodes if n.tag == "section" and "id" in n.attrs}

    # BR-1
    def test_br1_every_text_node_has_a_home(self) -> None:
        labels = set(build_module().LABELS)
        for text, parent in self.page.visible():
            if tp.BARE.match(text):
                continue
            owner = parent.annotated()
            with self.subTest(text=tp.norm(text)[:80]):
                self.assertIsNotNone(owner, "text with no record, label, derived value or framing behind it")
                if "data-label" in owner.attrs:
                    self.assertIn(owner.text(), labels, "a label that is not one of the build's labels")
        for node in self.page.nodes:
            if any(a in node.attrs for a in ("data-ref", "data-label", "data-derived")):
                inner = [n for n in node.walk() if n is not node and any(a in n.attrs for a in tp.ANNOTATIONS)]
                with self.subTest(leaf=node.attrs.get("data-ref") or node.text()[:40]):
                    self.assertEqual(inner, [], "an annotated value must not contain another")

    def test_br1_framing_is_marked_and_names_no_record(self) -> None:
        framing = self.page.has("data-framing")
        self.assertTrue(framing, "no framing block")
        for block in framing:
            with self.subTest(block=block.text()[:60]):
                marks = [n for n in block.walk() if "data-label" in n.attrs and n.text() == tp.FRAMING_MARK]
                self.assertEqual(len(marks), 1, "a framing block without its visible mark")
                own = " ".join(t for t, parent in block.texts() if parent.annotated() is block)
                self.assertNotRegex(own, r"\d", "framing holds a digit")
                for name in self.homes.names:
                    self.assertNotRegex(own, rf"(?<![\w-]){re.escape(name)}(?![\w-])", f"framing names a record ({name})")

    # BR-2
    def test_br2_labels_carry_no_fact(self) -> None:
        for label in build_module().LABELS:
            with self.subTest(label=label):
                self.assertNotRegex(label, r"\d", "a label holds a digit")
                self.assertNotRegex(label.lower(), r"\bnone\b")
                for name in self.homes.names:
                    self.assertNotRegex(label, rf"(?<![\w-]){re.escape(name)}(?![\w-])", f"a label names a record ({name})")

    def test_br2_every_record_value_equals_its_home(self) -> None:
        labels = set(build_module().LABELS)
        values = self.page.has("data-ref")
        self.assertTrue(values, "no record value on the brief")
        for node in values:
            ref, field = node.attrs["data-ref"], node.attrs.get("data-field")
            with self.subTest(ref=ref, field=field):
                self.assertIsNotNone(field, "data-ref without data-field")
                self.assertNotIn(ref, self.homes.staging, "a staging record shown")
                if "data-absent" in node.attrs:
                    self.assertFalse(self.homes.has(ref, field), "drawn as absent, but the field exists")
                    self.assertIn(node.text(), labels)
                    continue
                self.assertTrue(self.homes.has(ref, field), "no such home")
                value = self.homes.resolve(ref, field)
                self.assertIsInstance(value, (str, int, float), "a value must be a scalar")
                self.assertEqual(node.text(), tp.norm(tp.FORMATS[node.attrs.get("data-format")](str(value))))
                if node.tag == "a" and field == "/url":
                    self.assertEqual(node.attrs.get("href"), value)

    def test_br2_claims_in_panels_are_shown_whole(self) -> None:
        shown = {(n.attrs["data-ref"], n.attrs["data-field"]) for n in self.page.has("data-ref")}
        claims = sorted({ref for ref, field in shown if field == "/statement" and ref.startswith("claim-")})
        self.assertTrue(claims, "no claim shown")
        for claim_id in claims:
            claim = self.homes.canonical[claim_id]
            with self.subTest(claim=claim_id):
                for field in ("/claim_type", "/evidence_status", "/verified_on"):
                    self.assertIn((claim_id, field), shown)
                for index, citation in enumerate(claim.get("citations", [])):
                    self.assertIn((claim_id, f"/citations/{index}/anchor"), shown)
                    self.assertIn((citation["source_id"], "/url"), shown)
                if claim["claim_type"] in ("DERIVATION", "INTERPRETATION", "IMPLICATION"):
                    self.assertIn((claim_id, "/reasoning"), shown)

    # BR-3
    def expected_counts(self) -> dict:
        r = self.records
        classes = r.chain_classes()
        states = [r.class_state(c) for c in classes]
        out = {
            ("accelerators", None): len(r.accelerators()),
            ("rows-shown", None): len(self.rows),
            ("rows-in-result", None): len(self.rows),
            ("acts", None): len(r.policies),
            ("chain-classes", None): len(classes),
        }
        for state in ("named", "refused", "none"):
            if states.count(state):
                out[(f"classes-{state}", None)] = states.count(state)
        for target in r.unreached():
            out[("unreached-named-by", target)] = sum(e["target_entity"] == target for e in r.links)
        return out

    def test_br3_derived_values_are_recomputed(self) -> None:
        age = json.loads(AGE_RESULT.read_text(encoding="utf-8"))
        rows = self.rows
        derived = self.page.has("data-derived")
        self.assertLessEqual({n.attrs["data-derived"] for n in derived}, DERIVED_KINDS, "a derived value the checks do not recompute")
        dated_from = [r["evidence_dated_from"] for r in rows if r["evidence_dated_from"] != "not_applicable"]
        dated_to = [r["evidence_dated_to"] for r in rows if r["evidence_dated_to"] != "not_applicable"]
        counts: dict = {}
        for node in derived:
            kind = node.attrs["data-derived"]
            with self.subTest(kind=kind, at=node.attrs.get("data-count") or node.attrs.get("data-target") or node.attrs.get("data-row")):
                if kind == "count":
                    counts.setdefault((node.attrs["data-count"], node.attrs.get("data-key")), set()).add(node.text())
                elif kind == "sql-cell":
                    query = node.attrs.get("data-query")
                    self.assertIn(query, (DEP, "source_age"))
                    table = rows if query == DEP else age["rows"]
                    value = table[int(node.attrs["data-row"])][node.attrs["data-column"]]
                    if "data-item" in node.attrs:
                        value = value[int(node.attrs["data-item"])]
                    text = str(value).replace("_", " ") if node.attrs.get("data-format") == "state" else str(value)
                    self.assertEqual(node.text(), tp.norm(text))
                elif kind == "sql-flag":
                    row, column = rows[int(node.attrs["data-row"])], node.attrs["data-column"]
                    if column == "rests_on_atlas_interpretation":
                        self.assertTrue(row[column])
                    elif column == "publishers":
                        self.assertEqual(len(row[column]), 1)
                    else:
                        self.assertEqual(row[column], "accessed")
                    key = "accessed" if column.endswith("_basis") else column
                    self.assertEqual(node.text(), SQL_FLAGS[key])
                elif kind == "latest-published":
                    self.assertEqual(node.text(), self.records.latest_published())
                elif kind == "evidence-first":
                    self.assertEqual(node.text(), min(dated_from))
                elif kind == "evidence-last":
                    self.assertEqual(node.text(), max(dated_to))
                elif kind == "pointer":
                    record = self.homes.canonical[node.attrs["data-target"]]
                    self.assertIn(node.attrs["data-claim"], tp.Homes.pointer(record, node.text()))
                elif kind == "bytes-match":
                    claim = self.homes.canonical[node.attrs["data-target"]]
                    citation = claim["citations"][int(node.attrs["data-index"])]
                    registered = self.homes.canonical[citation["source_id"]]["retrieval"]["sha256"]
                    same = citation["read"]["sha256"].startswith(registered) or registered.startswith(citation["read"]["sha256"])
                    self.assertEqual(node.text(), "same bytes as registered" if same else "bytes changed since registration")
                elif kind == "rule-home":
                    home = (REPO_ROOT / node.text()).read_text(encoding="utf-8")
                    self.assertRegex(home, rf"(\| {re.escape(node.attrs['data-target'])} \||\({re.escape(node.attrs['data-target'])}\)\n)")
                elif kind == "no-activity-edge":
                    self.assertFalse([e for e in self.records.edges if e["target_entity"] == node.attrs["data-target"] and e["relation_type"] in ("owns", "operates", "designs", "fabricates", "packages", "supplies")])
                    self.assertEqual(node.text(), "no recorded relationship")
                elif kind == "lane-unlinked":
                    self.assertEqual(node.text(), "the facility and product here: not linked to this chain")
        with self.subTest(what="counts"):
            want = {k: {str(v)} for k, v in self.expected_counts().items()}
            self.assertEqual(counts, want, "a count that differs from the records, or a count shown where nothing is counted")
        with self.subTest(what="inputs"):
            self.assertEqual(sorted(n.text() for n in self.page.find(data_derived="input-file")), input_paths())
            digests = {n.text() for n in self.page.find(data_derived="input-digest")}
            self.assertEqual(digests, {tp.input_digest(input_paths())})

    def test_br3_every_count_names_its_unit(self) -> None:
        counts = self.page.find(data_derived="count")
        self.assertTrue(counts)
        for node in counts:
            line = node.parent
            with self.subTest(count=node.attrs["data-count"]):
                self.assertTrue(any(n is not node and "data-label" in n.attrs for n in line.walk()), "a bare number with no words beside it")
                self.assertIn(COUNT_UNITS[node.attrs["data-count"]], tp.norm(line.text()))
                self.assertNotEqual(node.text(), "0", "a zero shown as a count: the brief says 'no recorded …' instead")

    def test_br3_the_tutorial_is_its_query_file(self) -> None:
        from test_warehouse import tutorial  # noqa: PLC0415 (the format's reader)

        query = REPO_ROOT / "sql" / f"{DEP}.sql"
        result = dep()
        self.assertEqual(result["query_sha256"], hashlib.sha256(query.read_bytes()).hexdigest())
        t = tutorial(query.read_text(encoding="utf-8"))
        boxes = [n for n in self.page.nodes if n.tag == "details" and "sql-tutorial" in n.attrs.get("class", "").split()]
        self.assertEqual(len(boxes), 1, "one 'How this was computed' beside the result table")
        box = boxes[0]

        def of(kind: str, raw: bool = False) -> list[str]:
            nodes = [n for n in box.walk() if n.attrs.get("data-derived") == kind]
            return ["".join(text for text, _ in n.texts()) if raw else n.text() for n in nodes]

        self.assertEqual(of("sql-question"), [tp.norm(t["header"]["question"])])
        self.assertEqual(of("sql-reading"), [tp.norm(t["header"]["reading"])])
        self.assertEqual(of("sql-step-title"), [tp.norm(s["title"]) for s in t["steps"]])
        self.assertEqual(of("sql-step-code", raw=True), [s["code"] for s in t["steps"]])
        self.assertEqual(of("sql-digest"), [result["input_digest"]])

    # BR-4
    def figure_marks(self, page: tj.Page) -> list[tuple]:
        svgs = [n for n in page.nodes if n.tag == "svg" and "data-figure" in n.attrs]
        self.assertEqual(len(svgs), 1, "one dependency map")
        return sorted((n.attrs["data-mark"], n.attrs["data-target"], n.attrs.get("data-basis")) for n in svgs[0].walk() if "data-mark" in n.attrs)

    def test_br4_the_map_draws_the_hbm_page_figure(self) -> None:
        mine, theirs = self.figure_marks(self.page), self.figure_marks(tj.Page(HBM_PAGE))
        self.assertTrue(mine)
        self.assertEqual(mine, theirs, "the brief's map differs from the HBM page's figure, which PG-3 and PG-5 check")
        for _, target, _ in mine:
            with self.subTest(target=target):
                self.assertIn(f"ev-{target}", self.page.by_id, "a mark with no panel on the brief")
        self.assertIn("map", self.sections())
        self.assertTrue(any("data-figure" in n.attrs for n in self.sections()["map"].walk()), "the map is not in its section")

    def test_br4_the_result_table_shows_every_row(self) -> None:
        cells = [n for n in self.page.find(data_derived="sql-cell") if n.attrs.get("data-query") == DEP and any(a.tag == "table" for a in n.ancestors())]
        self.assertEqual({int(n.attrs["data-row"]) for n in cells}, set(range(len(self.rows))), "a result row missing from the table")
        for index, row in enumerate(self.rows):
            shown = {n.attrs["data-column"] for n in cells if int(n.attrs["data-row"]) == index}
            with self.subTest(row=index):
                for column in tp.SQL_SHOWN:
                    self.assertIn(column, shown)
                self.assertEqual("gap_reason" in shown, row["basis"] == "gap")

    # BR-5
    def summary(self) -> dict:
        section = self.sections().get("summary")
        self.assertIsNotNone(section, "no executive summary")
        items: dict = {}
        for n in section.walk():
            if "data-summary" in n.attrs:
                items.setdefault(n.attrs["data-summary"], []).append(n)
        return items

    @staticmethod
    def cells(node) -> set[tuple]:
        return {(int(n.attrs["data-row"]), n.attrs["data-column"]) for n in node.walk() if n.attrs.get("data-derived") == "sql-cell" and n.attrs.get("data-query") == DEP}

    def test_br5_the_summary_has_one_sentence_per_group(self) -> None:
        items = self.summary()
        r = self.records
        states = {r.class_state(c) for c in r.chain_classes()}
        want = {"depends", "made", "supplied", "limits"} | {f"texts-{s}" for s in states}
        self.assertEqual(set(items), want, "a summary sentence missing, or one the records do not call for")
        self.assertLessEqual(set(items), set(SUMMARY_KINDS))

    def test_br5_dependency_sentences_cite_their_rows(self) -> None:
        items = self.summary()
        rows = self.rows
        incorporates = [i for i, r in enumerate(rows) if r["relation"] == "incorporates"]
        requires = [i for i, r in enumerate(rows) if r["relation"] == "requires"]
        depends = items["depends"]
        targets = sorted({rows[i]["to_id"] for i in incorporates})
        self.assertEqual(len(depends), len(targets), "one sentence per part the accelerators incorporate")
        got_inc, got_req = set(), set()
        for node in depends:
            cells = self.cells(node)
            got_inc |= {i for i, c in cells if c == "accelerator" and i in incorporates}
            got_req |= {i for i, c in cells if i in requires}
            group = sorted({i for i, _ in cells if i in incorporates})
            for i in group:
                with self.subTest(row=i):
                    self.assertTrue({(i, "accelerator"), (i, "basis")} <= cells, "an accelerator without its basis")
            with self.subTest(group=group):
                self.assertEqual(len({(rows[i]["relation"], rows[i]["to_id"]) for i in group}), 1, "one sentence groups rows of one relation and part")
                self.assertTrue(any({(i, "relation"), (i, "to_name")} <= cells for i in group), "the part and its relation are not stated")
        self.assertEqual(got_inc, set(incorporates), "an accelerator's incorporates row left out of the summary")
        for target in targets:
            req = [i for i in requires if rows[i]["from_id"] == target]
            with self.subTest(part=target):
                self.assertEqual(len({rows[i]["record_id"] for i in req}), 1, "the requires rows of one part are one record")
                self.assertTrue(got_req & set(req), "what the part requires is left out")
        made = [i for i, r in enumerate(rows) if r["position"] == 1]
        got = set()
        for node in items["made"]:
            cells = self.cells(node)
            for i in made:
                if (i, "from_name") in cells:
                    got.add(i)
                    with self.subTest(row=i):
                        self.assertIn((i, "to_name"), cells)
                        self.assertIn((i, "relation"), cells)
                        if rows[i]["basis"] == "gap":
                            self.assertIn((i, "gap_reason"), cells, "a gap without its reason")
                            gap = [n for n in node.walk() if n.attrs.get("data-gap-row") == str(i)]
                            self.assertTrue(gap and "a recorded gap, not a link" in gap[0].text(), "a gap phrased as a link")
                        else:
                            self.assertIn((i, "basis"), cells)
        self.assertEqual(got, set(made), "a designs or fabricates row left out of the summary")

    def test_br5_supplier_sentence_cites_every_supplier_row(self) -> None:
        rows = self.rows
        suppliers = [i for i, r in enumerate(rows) if r["relation"] == "supplier"]
        cells = set().union(*(self.cells(n) for n in self.summary()["supplied"]))
        self.assertEqual({i for i, c in cells if c == "from_name"}, set(suppliers))
        for i in suppliers:
            row = rows[i]
            with self.subTest(row=i):
                self.assertTrue({(i, "from_name"), (i, "accelerator"), (i, "basis")} <= cells)
                self.assertEqual((i, "period_to") in cells, row["period_to"] != "not_applicable", "a period shown exactly when the row has one")
                self.assertEqual((i, "criteria_unmet") in cells, bool(row["criteria_unmet"]), "each unmet criterion shown exactly when the row has one")

    def test_br5_texts_sentences_group_the_classes_by_state(self) -> None:
        r = self.records
        items = self.summary()
        for cid in r.chain_classes():
            state = r.class_state(cid)
            node = items[f"texts-{state}"][0]
            named = [n for n in node.walk() if n.attrs.get("data-class") == cid]
            with self.subTest(cls=cid, state=state):
                self.assertEqual(len(named), 1, "a class not in its group's sentence, or in it twice")
                acts = {n.attrs["data-ref"] for n in named[0].walk() if n.attrs.get("data-ref") in r.policy_ids}
                if state == "named":
                    self.assertEqual(acts, {e["source_entity"] for e in r.links if e["target_entity"] == cid})
                    statuses = {n.attrs["data-policy"]: n.text() for n in named[0].walk() if n.attrs.get("data-derived") == "policy-status"}
                    self.assertEqual(statuses, {a: r.status(a, self.on).replace("_", " ") for a in acts})
                elif state == "refused":
                    cands = [c for c in r.policy_candidates if cid in c["target_entities"]]
                    self.assertEqual(acts, {s for c in cands for s in c["source_entities"] if isinstance(s, str)})
                    reasons = {n.attrs["data-ref"].rsplit("/", 1)[1] for n in named[0].walk() if n.attrs.get("data-ref", "").startswith("schema:refused_candidates#vocab_reason/")}
                    self.assertEqual(reasons, {x for c in cands for x in c["reasons"]})
                else:
                    self.assertEqual(acts, set())
        for kind in ("texts-named", "texts-refused", "texts-none"):
            for node in items.get(kind, []):
                with self.subTest(kind=kind):
                    counts = {n.attrs.get("data-count") for n in node.walk() if n.attrs.get("data-derived") == "count"}
                    self.assertEqual(counts, {kind.replace("texts-", "classes-"), "chain-classes"}, "a group without its count over the classes compared")
        limits = items["limits"][0]
        self.assertEqual([n.text() for n in limits.walk() if n.attrs.get("data-derived") == "latest-published"], [r.latest_published()])

    # BR-6
    def test_br6_the_matrix_equals_the_records(self) -> None:
        r = self.records
        section = self.sections().get("texts")
        self.assertIsNotNone(section, "no export-control section")
        rows = [n for n in section.walk() if n.tag == "tr" and "data-target" in n.attrs]
        self.assertEqual([n.attrs["data-target"] for n in rows], r.chain_classes(), "a class the chain reaches missing, added or out of order")
        for row in rows:
            target = row.attrs["data-target"]
            cells = [n for n in row.walk() if "data-cell" in n.attrs]
            self.assertEqual(sorted(c.attrs["data-act"] for c in cells), sorted(r.policy_ids), f"{target}: not one cell per act")
            for cell in cells:
                state, record = r.cell(cell.attrs["data-act"], target)
                with self.subTest(target=target, act=cell.attrs["data-act"]):
                    self.assertEqual(cell.attrs["data-cell"], state)
                    if state == "named":
                        self.assertEqual(cell.attrs.get("data-link"), record)
                        self.assertIn(f"ev-{record}", self.page.by_id, "a named cell whose link has no panel")
                    elif state == "refused":
                        self.assertEqual(cell.attrs.get("data-candidate"), record)
                        self.assertIn(f"cand-{record}", self.page.by_id, "a refused cell whose candidate has no card")
                    else:
                        self.assertIn("no recorded relationship", cell.text())

    def test_br6_every_policy_shown_has_its_official_text_and_the_no_advice_line(self) -> None:
        r = self.records
        page = self.page
        blocks = {n.attrs["data-act"]: n for n in page.nodes if "data-act" in n.attrs and n.tag in ("article", "li", "div")}
        shown = {n.attrs["data-ref"] for n in page.has("data-ref") if n.attrs["data-ref"] in r.policy_ids}
        self.assertEqual(shown, set(r.policy_ids), "every recorded act is shown, with its status")
        for policy in shown:
            block = blocks.get(policy)
            with self.subTest(policy=policy):
                self.assertIsNotNone(block, "a policy shown with no block for its text and the no-advice line")
                hrefs = {n.attrs.get("href") for n in block.walk() if n.tag == "a" and "official" in n.attrs.get("class", "").split()}
                self.assertTrue(hrefs and hrefs <= r.official_texts(policy), "no official text link, or one that is not the act's official text")
                self.assertIn(NO_ADVICE, [n.text() for n in block.walk() if "data-label" in n.attrs], "no no-advice line (LA-5)")
        for node in page.has("data-ref"):
            ref = node.attrs["data-ref"]
            if ref not in r.policy_ids:
                continue
            inside = any(a.attrs.get("data-act") == ref for a in node.ancestors())
            linked = any(a.tag == "a" and a.attrs.get("href", "").startswith("#") and page.by_id.get(a.attrs["href"][1:]) is not None and page.by_id[a.attrs["href"][1:]].attrs.get("data-act") == ref for a in node.ancestors())
            with self.subTest(policy=ref, field=node.attrs["data-field"]):
                self.assertTrue(inside or linked, "a policy value outside its block and not linked to it")

    def test_br6_statuses_are_derived_on_the_as_of_date(self) -> None:
        r = self.records
        statuses = self.page.find(data_derived="policy-status")
        self.assertEqual({n.attrs["data-policy"] for n in statuses}, set(r.policy_ids), "an act without its status")
        for node in statuses:
            with self.subTest(policy=node.attrs["data-policy"]):
                self.assertEqual(node.attrs["data-on"], self.on, "a status on another date than the as-of date")
                self.assertEqual(node.text(), r.status(node.attrs["data-policy"], self.on).replace("_", " "))

    # BR-7
    def test_br7_scope_and_limits_travel_with_the_brief(self) -> None:
        sections = self.sections()
        order = [n.attrs["id"] for n in self.page.nodes if n.tag == "section" and "id" in n.attrs]
        self.assertGreaterEqual(len(order), 2)
        self.assertEqual(order[:2], ["scope", "summary"], "the scope section must come first, then the summary")
        scope = sections["scope"]
        header = next(n for n in self.page.nodes if n.tag == "header")
        boundary = [n for n in header.walk() if "data-boundary" in n.attrs]
        self.assertTrue(boundary and boundary[0].text() == BOUNDARY, "the boundary line is not in the brief's header")
        must = {
            "the out-of-scope list": [n for n in scope.walk() if "data-limits" in n.attrs and any("data-framing" in x.attrs for x in n.walk())],
            "the as-of date": [n for n in scope.walk() if n.attrs.get("data-column") == "reference_date"],
            "the input digest": [n for n in scope.walk() if n.attrs.get("data-derived") == "input-digest"],
            "the unsearched period": [n for n in scope.walk() if n.attrs.get("data-derived") == "latest-published"],
            "the scope counts": [n for n in scope.walk() if n.attrs.get("data-count") in ("accelerators", "acts", "chain-classes")],
        }
        for what, nodes in must.items():
            with self.subTest(item=what):
                self.assertTrue(nodes, f"{what} missing from the first section")
                for node in nodes:
                    self.assertFalse([a for a in node.ancestors() if a.tag == "details"], f"{what} inside a disclosure: it would not print")
        for node in (scope, *boundary):
            self.assertFalse([a for a in node.ancestors() if a.tag == "details"])
        first = [n for n in scope.children if isinstance(n, tp.Node) and n.tag != "h2"]
        self.assertTrue(first and "data-identity" in first[0].attrs, "the as-of date and digest are not the first lines of the scope: they would print after the first page")
        shown = [n for n in self.page.nodes if n.attrs.get("data-count") == "rows-shown"]
        total = [n for n in self.page.nodes if n.attrs.get("data-count") == "rows-in-result"]
        self.assertTrue(shown and total and shown[0].parent is total[0].parent, "rows shown and rows in the result in one line")
        cite = [n for n in self.page.nodes if "data-citation" in n.attrs]
        self.assertEqual(len(cite), 1, "one ready-made citation")
        self.assertEqual([n.text() for n in cite[0].walk() if n.attrs.get("data-column") == "reference_date"], [self.on])
        self.assertEqual([n.text() for n in cite[0].walk() if n.attrs.get("data-derived") == "input-digest"], [tp.input_digest(input_paths())])

    def test_br7_print_never_hides_scope_evidence_or_sources(self) -> None:
        css = "".join("".join(t for t, _ in n.texts()) for n in self.page.nodes if n.tag == "style")
        self.assertRegex(css, r"@page\s*\{", "no page rule for print")
        start = css.find("@media print")
        self.assertNotEqual(start, -1, "no print stylesheet")
        depth, i = 0, css.index("{", start)
        for j in range(i, len(css)):
            depth += {"{": 1, "}": -1}.get(css[j], 0)
            if depth == 0:
                break
        block = css[i + 1 : j]
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", block):
            if re.search(r"display\s*:\s*none|visibility\s*:\s*hidden", body):
                for word in ("scope", "boundary", "summary", "limits", "citation", "evidence", "sources", "panel", "main", "section", "table", "svg", "framing"):
                    with self.subTest(selectors=selectors.strip(), word=word):
                        self.assertNotIn(word, selectors, "print hides what must travel with the brief")

    # BR-8
    def test_br8_every_citation_resolves_to_a_source_record(self) -> None:
        sources = self.records.sources
        page = self.page
        for node in page.has("data-ref"):
            ref = node.attrs["data-ref"]
            if ref.startswith("src-"):
                with self.subTest(source=ref):
                    self.assertIn(ref, sources, "a source shown that is not a source record")
        claims = {n.attrs["data-ref"] for n in page.has("data-ref") if n.attrs["data-field"] == "/statement" and n.attrs["data-ref"].startswith("claim-")}
        cited = {c["source_id"] for cid in claims for c in self.records.claims[cid].get("citations", [])}
        section = self.sections().get("sources")
        self.assertIsNotNone(section, "no source appendix")
        rows = {n.attrs["data-source"]: n for n in section.walk() if n.tag == "tr" and "data-source" in n.attrs}
        self.assertEqual(set(rows), cited, "the source appendix does not list exactly the sources the shown claims cite")
        for sid, row in rows.items():
            fields = {(n.attrs["data-ref"], n.attrs["data-field"]) for n in row.walk() if "data-ref" in n.attrs}
            with self.subTest(source=sid):
                for field in ("/title", "/publisher", "/source_class", "/url", "/retrieval/accessed_at"):
                    self.assertIn((sid, field), fields)
                url = [n for n in row.walk() if n.attrs.get("data-ref") == sid and n.attrs.get("data-field") == "/url"]
                self.assertEqual(url[0].text(), sources[sid]["url"], "the URL is not printed in full")

    # BR-9
    def test_br9_no_forbidden_word_in_the_atlas_voice(self) -> None:
        for text, parent in self.page.visible():
            owner = parent.annotated()
            if owner is None or "data-ref" in owner.attrs:
                continue  # a record value: quoted, the record's own words
            for word in FORBIDDEN:
                with self.subTest(word=word):
                    self.assertNotRegex(text.lower(), rf"\b{word}\b", f"'{word}' in the Atlas's own voice: {tp.norm(text)[:80]}")

    # BR-10
    def test_br10_links_resolve_and_nothing_loads(self) -> None:
        urls = {s["url"] for s in self.records.sources.values()}
        other: dict = {}
        page = self.page
        for node in page.nodes:
            self.assertNotIn(node.tag, ("script", "iframe", "object", "embed", "img", "link"), f"<{node.tag}> on a self-contained page")
            self.assertNotIn("src", node.attrs)
            for attr in ("onclick", "onmouseover", "onload", "onfocus"):
                self.assertNotIn(attr, node.attrs)
            href = node.attrs.get("href")
            if href is None:
                continue
            with self.subTest(href=href):
                if href.startswith("#"):
                    self.assertIn(href[1:], page.by_id, "a fragment with no target")
                elif re.match(r"https?://", href):
                    self.assertEqual(node.tag, "a")
                    self.assertIn(href, urls, "an outside link that is not a source's URL")
                else:
                    path, _, fragment = href.partition("#")
                    target = (page.path.parent / path).resolve()
                    self.assertTrue(target.exists(), "a link to a file that does not exist")
                    if fragment and target.suffix == ".html":
                        if target not in other:
                            other[target] = {n.attrs["id"] for n in tp.parse(target.read_text(encoding="utf-8")).walk() if "id" in n.attrs}
                        self.assertIn(fragment, other[target])
                    elif fragment:
                        self.assertTrue(path.endswith(".md"))
                        self.assertIn(fragment, tp.markdown_anchors(target.read_text(encoding="utf-8")))
        css = "".join("".join(t for t, _ in n.texts()) for n in page.nodes if n.tag == "style")
        self.assertNotRegex(css, r"@import|url\(", "the style loads a resource")
        self.assertTrue(any(n.tag == "a" and (page.path.parent / n.attrs.get("href", "#")).resolve() == (REPO_ROOT / tj.INDEX).resolve() for n in page.nodes), "no link to the entry page")

    # BR-11
    def test_br11_document_structure(self) -> None:
        page = self.page
        html = next(n for n in page.nodes if n.tag == "html")
        self.assertEqual(html.attrs.get("lang"), "en")
        titles = [n for n in page.nodes if n.tag == "title" and n.parent.tag == "head"]
        h1 = [n for n in page.nodes if n.tag == "h1"]
        self.assertEqual(len(titles), 1)
        self.assertEqual(len(h1), 1)
        self.assertEqual(titles[0].text(), h1[0].text())
        self.assertTrue(any(n.tag == "meta" and n.attrs.get("name") == "viewport" for n in page.nodes))
        self.assertEqual(len([n for n in page.nodes if n.tag == "main"]), 1)
        self.assertEqual(len([n for n in page.nodes if n.tag == "header"]), 1)
        levels = [int(n.tag[1]) for n in page.nodes if re.fullmatch(r"h[1-6]", n.tag)]
        for before, after in zip(levels, levels[1:]):
            self.assertLessEqual(after, before + 1, "a skipped heading level")
        for th in (n for n in page.nodes if n.tag == "th"):
            self.assertIn(th.attrs.get("scope"), ("col", "row"), "a table header with no scope")
        for svg in (n for n in page.nodes if n.tag == "svg" and n.attrs.get("aria-hidden") != "true"):
            self.assertTrue(svg.attrs.get("aria-labelledby") and all(i in page.by_id for i in svg.attrs["aria-labelledby"].split()), "an unnamed figure")
        for panel in (n for n in page.nodes if n.attrs.get("id", "").startswith("ev-")):
            self.assertFalse(any(a.tag == "details" for a in panel.ancestors() if a is not panel), "a panel hidden in a closed disclosure")
        for section in (n for n in page.nodes if n.tag == "section" and "id" in n.attrs):
            self.assertTrue(section.attrs.get("aria-labelledby") in page.by_id, "a brief section with no heading")

    def test_br11_palette_and_contrast(self) -> None:
        css = "".join("".join(t for t, _ in n.texts()) for n in self.page.nodes if n.tag == "style")
        root = re.search(r":root\s*\{([^}]*)\}", css)
        self.assertIsNotNone(root, "no palette")
        palette = dict(re.findall(r"--([a-z-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;", root.group(1)))
        for ink in (k for k in palette if k.startswith("ink")):
            for surface in (k for k in palette if k.startswith("surface")):
                self.assertGreaterEqual(tp.contrast(palette[ink], palette[surface]), 4.5, f"{ink} on {surface}")
        body = css[root.end():]
        self.assertNotRegex(body, r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", "a colour outside the palette")
        for rule in re.findall(r"([^{}]+)\{", body):
            if ":hover" in rule:
                self.assertIn(":focus-visible", rule, f"a hover rule without focus: {rule.strip()}")

    # BR-5 and BR-12 support: key entities
    def test_br5_key_entities_are_the_chain_records(self) -> None:
        section = self.sections().get("entities")
        self.assertIsNotNone(section, "no key-entities section")
        rows = {n.attrs["data-entity"] for n in section.walk() if n.tag == "tr" and "data-entity" in n.attrs}
        self.assertEqual(rows, self.records.key_entities(), "a company or product on the chain missing, or one that is not on it")
        unreached = [n.attrs["data-unreached"] for n in self.page.nodes if "data-unreached" in n.attrs]
        self.assertEqual(unreached, self.records.unreached(), "a class a recorded act names but the chain does not reach is not said")

    # BR-12
    def test_br12_rebuild_is_byte_identical(self) -> None:
        build = build_module()
        first, second = build.build(), build.build()
        self.assertEqual(first, second, "two builds differ")
        self.assertEqual(sorted(first), [BRIEF], "the build writes other pages than the brief")
        self.assertEqual(self.page.raw.encode("utf-8"), first[BRIEF], "the committed brief differs from a rebuild (python tools/build_brief.py)")
        folder = REPO_ROOT / "site" / "briefs"
        found = {p.relative_to(REPO_ROOT).as_posix() for p in folder.rglob("*") if p.is_file()} if folder.exists() else set()
        self.assertEqual(found, {BRIEF}, "a stray file in site/briefs/")


if __name__ == "__main__":
    unittest.main()
