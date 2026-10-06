"""The SQL layer: load the canonical records into DuckDB, run the queries, write their results (S14).

docs/architecture/sql-layer.md is the design; D-118 to D-121 the decisions.

    python tools/warehouse.py                 load data/ into a fresh in-memory database, run every
                                              query in sql/, write sql/results/<query>.json
    python tools/warehouse.py --check         the same in memory; exit 1 if a committed result differs
    python tools/warehouse.py --db PATH       also save the database to PATH, to explore it with the
                                              DuckDB command line; PATH must be outside the repository

The JSON files in data/ are the only home of the facts. The database is rebuilt from them on every
run, is never committed, and nothing is ever written from it back into data/. Only canonical files
are loaded; data/staging/ is never read.

Explicit states (sql-layer.md §3): a field that holds a value or a state becomes two columns,
<field>_value and <field>_state. The state is 'value' when a value is present, the record's own state
word otherwise (not_researched, not_applicable, ...), or 'absent' when the record has no such key.
NULL appears only in a _value column whose _state is not 'value'. Every key of every record kind is
listed below; an unknown key stops the load, so nothing is dropped silently.

Needs the pinned DuckDB (requirements-analysis.txt, D-118). The page build never imports this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
SQL = REPO_ROOT / "sql"
THIS = Path(__file__).resolve()

ENTITY_FILES = ("companies", "jurisdictions", "technologies", "components", "products", "facilities")
# Entity fields by shape. Everything not named here is an attribute: assertions ([{"value", "claim_ids"}])
# or a state ({"state": ...}), loaded into field_values.
ENTITY_CORE = ("id", "type", "name")
ENTITY_LISTS = ("aliases", "identity_claim_ids", "concept_refs", "broader", "instance_of", "facility_kinds")
ENTITY_SCALARS = ("vendor", "product_kind", "use_class", "technology_kind", "jurisdiction_kind")
ENTITY_ATTRIBUTES = (
    "legal_name", "incorporated_in", "headquartered_in", "roles",  # company
    "definition",  # technology, component
    "vendor_process_name", "tdp_w", "rated_power_w", "rack_scale", "cooling_method",  # product
    "locality", "located_in", "nameplate_it_capacity_mw",  # facility
)
KNOWN_KEYS = {
    "sources.json": {"id", "migrated_from", "source_class", "title", "publisher", "publisher_entity", "authors", "url", "stated_dates", "retrieval", "filing_copy"},
    "claims.json": {"id", "claim_type", "statement", "evidence_status", "citations", "as_of", "review", "verified_on", "input_claim_ids", "reasoning", "disputed_with", "search"},
    "citation": {"source_id", "locator", "anchor", "standing", "read", "originator"},
    "relationships.json": {"id", "relation_type", "source_entity", "target_entity", "claim_ids", "supplier", "item", "valid_from", "valid_to"},
    "events.json": {"id", "event_type", "subject", "date", "claim_ids"},
    "refused_candidates.json": {"id", "relation_types", "source_entities", "target_entities", "item", "considered", "reasons", "ruling", "reasoning"},
    "considered": {"claim_id", "source_id", "locator", "anchor", "read"},
    "identity_basis.json": {"kind", "concept", "term", "record", "note", "term_is", "class", "claim_id", "facility_kind", "word"},
    "entity": set(ENTITY_CORE) | set(ENTITY_LISTS) | set(ENTITY_SCALARS) | set(ENTITY_ATTRIBUTES),
}

# Column names ending in _value always have a _state partner (WH-4).
TABLES = {
    "load_manifest": "path VARCHAR, sha256 VARCHAR",
    "sources": (
        "id VARCHAR, migrated_from_value VARCHAR, migrated_from_state VARCHAR, source_class VARCHAR, title VARCHAR, "
        "publisher VARCHAR, publisher_entity_value VARCHAR, publisher_entity_state VARCHAR, authors_value VARCHAR, "
        "authors_state VARCHAR, url VARCHAR, stated_dates_state VARCHAR, retrieval_method VARCHAR, accessed_at VARCHAR, "
        "sha256 VARCHAR, filing_copy_value VARCHAR, filing_copy_state VARCHAR"
    ),
    "source_dates": "source_id VARCHAR, ordinal INTEGER, kind VARCHAR, date VARCHAR",
    "claims": (
        "id VARCHAR, claim_type VARCHAR, statement VARCHAR, evidence_status VARCHAR, as_of_value VARCHAR, as_of_state VARCHAR, "
        "verified_on VARCHAR, review_verdict VARCHAR, review_reviewer VARCHAR, review_reviewed_on VARCHAR, "
        "review_recorded_in VARCHAR, reasoning_value VARCHAR, reasoning_state VARCHAR, search_value VARCHAR, search_state VARCHAR"
    ),
    "citations": (
        "claim_id VARCHAR, ordinal INTEGER, source_id VARCHAR, locator VARCHAR, anchor VARCHAR, standing VARCHAR, "
        "read_accessed_at VARCHAR, read_sha256 VARCHAR, originator_value VARCHAR, originator_state VARCHAR"
    ),
    "claim_inputs": "claim_id VARCHAR, ordinal INTEGER, input_claim_id VARCHAR",
    "claim_disputes": "claim_id VARCHAR, ordinal INTEGER, disputed_claim_id VARCHAR",
    "entities": "id VARCHAR, type VARCHAR, name VARCHAR",
    "entity_lists": "entity_id VARCHAR, field VARCHAR, ordinal INTEGER, value VARCHAR",
    "entity_scalars": "entity_id VARCHAR, field VARCHAR, value VARCHAR",
    "field_values": (
        "record_id VARCHAR, field VARCHAR, ordinal INTEGER, assertion_value VARCHAR, assertion_state VARCHAR, "
        "valid_from_value VARCHAR, valid_from_state VARCHAR, valid_to_value VARCHAR, valid_to_state VARCHAR"
    ),
    "field_value_claims": "record_id VARCHAR, field VARCHAR, ordinal INTEGER, claim_ordinal INTEGER, claim_id VARCHAR",
    "relationships": (
        "id VARCHAR, relation_type VARCHAR, source_entity VARCHAR, target_entity VARCHAR, item_value VARCHAR, item_state VARCHAR, "
        "valid_from_value VARCHAR, valid_from_state VARCHAR, valid_to_value VARCHAR, valid_to_state VARCHAR"
    ),
    "relationship_claims": "relationship_id VARCHAR, ordinal INTEGER, claim_id VARCHAR",
    "events": "id VARCHAR, event_type VARCHAR, subject VARCHAR, date VARCHAR",
    "event_claims": "event_id VARCHAR, ordinal INTEGER, claim_id VARCHAR",
    "refused_candidates": "id VARCHAR, ruling VARCHAR, reasoning VARCHAR",
    "candidate_relation_types": "candidate_id VARCHAR, ordinal INTEGER, relation_type VARCHAR",
    "candidate_endpoints": (
        "candidate_id VARCHAR, side VARCHAR, ordinal INTEGER, entity_value VARCHAR, entity_state VARCHAR, "
        "name_value VARCHAR, name_state VARCHAR"
    ),
    "candidate_reasons": "candidate_id VARCHAR, ordinal INTEGER, reason VARCHAR",
    "candidate_considered": (
        "candidate_id VARCHAR, ordinal INTEGER, claim_id_value VARCHAR, claim_id_state VARCHAR, source_id_value VARCHAR, "
        "source_id_state VARCHAR, locator_value VARCHAR, locator_state VARCHAR, anchor_value VARCHAR, anchor_state VARCHAR, "
        "read_accessed_at_value VARCHAR, read_accessed_at_state VARCHAR, read_sha256_value VARCHAR, read_sha256_state VARCHAR"
    ),
    "identity_basis": (
        "kind VARCHAR, ordinal INTEGER, record_value VARCHAR, record_state VARCHAR, concept_value VARCHAR, concept_state VARCHAR, "
        "term_value VARCHAR, term_state VARCHAR, term_is_value VARCHAR, term_is_state VARCHAR, class_value VARCHAR, "
        "class_state VARCHAR, claim_id_value VARCHAR, claim_id_state VARCHAR, facility_kind_value VARCHAR, "
        "facility_kind_state VARCHAR, word_value VARCHAR, word_state VARCHAR, note_value VARCHAR, note_state VARCHAR"
    ),
}


class UnknownKey(ValueError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> list[dict]:
    records = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(records, list), f"{path.name} is not a JSON array"
    return records


def known(where: str, record: dict, contract: str) -> None:
    unknown = sorted(set(record) - KNOWN_KEYS[contract])
    if unknown:
        raise UnknownKey(f"{where}: key(s) {unknown} are not in the loader's contract (tools/warehouse.py KNOWN_KEYS)")


def text(value) -> str:
    """A value as text: a string as itself, anything else (a number, a list, an object) as compact JSON."""
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def vs(record: dict, key: str) -> tuple[str | None, str]:
    """(value, state) of a field that may hold a value, an explicit state, or be absent."""
    if key not in record:
        return None, "absent"
    value = record[key]
    if isinstance(value, dict) and set(value) <= {"state", "name"} and "state" in value:
        return None, value["state"]
    if value is None:
        raise ValueError(f"JSON null in key {key!r}: the records never use null (sql-layer.md §3)")
    return text(value), "value"


def load(data: Path = DATA, db: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """A fresh database holding the canonical records of data/ (never data/staging/)."""
    con = duckdb.connect(db)
    con.execute("SET threads = 1")
    for table, columns in TABLES.items():
        con.execute(f"CREATE TABLE {table} ({columns})")
    rows: dict[str, list[tuple]] = {table: [] for table in TABLES}
    files = sorted(p for p in data.glob("*.json"))
    for path in files:
        rows["load_manifest"].append((path.relative_to(data.parent).as_posix(), sha256(path)))

    for s in read(data / "sources.json"):
        known(f"sources.json {s.get('id')}", s, "sources.json")
        dates_state = "value" if isinstance(s["stated_dates"], list) else s["stated_dates"]["state"]
        rows["sources"].append((
            s["id"], *vs(s, "migrated_from"), s["source_class"], s["title"], s["publisher"], *vs(s, "publisher_entity"),
            *vs(s, "authors"), s["url"], dates_state, s["retrieval"]["method"], s["retrieval"]["accessed_at"],
            s["retrieval"]["sha256"], *vs(s, "filing_copy"),
        ))
        if dates_state == "value":
            rows["source_dates"] += [(s["id"], i, d["kind"], d["date"]) for i, d in enumerate(s["stated_dates"])]

    for c in read(data / "claims.json"):
        known(f"claims.json {c.get('id')}", c, "claims.json")
        review = c["review"]
        rows["claims"].append((
            c["id"], c["claim_type"], c["statement"], c["evidence_status"], *vs(c, "as_of"), c["verified_on"],
            review["verdict"], review["reviewer"], review["reviewed_on"], review["recorded_in"], *vs(c, "reasoning"), *vs(c, "search"),
        ))
        for i, cit in enumerate(c.get("citations", [])):
            known(f"claims.json {c['id']} citation {i}", cit, "citation")
            rows["citations"].append((
                c["id"], i, cit["source_id"], cit["locator"], cit["anchor"], cit["standing"],
                cit["read"]["accessed_at"], cit["read"]["sha256"], *vs(cit, "originator"),
            ))
        rows["claim_inputs"] += [(c["id"], i, x) for i, x in enumerate(c.get("input_claim_ids", []))]
        rows["claim_disputes"] += [(c["id"], i, x) for i, x in enumerate(c.get("disputed_with", []))]

    for kind in ENTITY_FILES:
        for e in read(data / f"{kind}.json"):
            known(f"{kind}.json {e.get('id')}", e, "entity")
            rows["entities"].append((e["id"], e["type"], e["name"]))
            for field in ENTITY_LISTS:
                rows["entity_lists"] += [(e["id"], field, i, v) for i, v in enumerate(e.get(field, []))]
            rows["entity_scalars"] += [(e["id"], f, e[f]) for f in ENTITY_SCALARS if f in e]
            for field in ENTITY_ATTRIBUTES:
                if field in e:
                    attribute(rows, e["id"], field, e[field])

    for r in read(data / "relationships.json"):
        known(f"relationships.json {r.get('id')}", r, "relationships.json")
        rows["relationships"].append((
            r["id"], r["relation_type"], r["source_entity"], r["target_entity"], *vs(r, "item"), *vs(r, "valid_from"), *vs(r, "valid_to"),
        ))
        rows["relationship_claims"] += [(r["id"], i, cid) for i, cid in enumerate(r["claim_ids"])]
        if "supplier" in r:
            attribute(rows, r["id"], "supplier", r["supplier"])

    for ev in read(data / "events.json"):
        known(f"events.json {ev.get('id')}", ev, "events.json")
        rows["events"].append((ev["id"], ev["event_type"], ev["subject"], ev["date"]))
        rows["event_claims"] += [(ev["id"], i, cid) for i, cid in enumerate(ev["claim_ids"])]

    for cand in read(data / "refused_candidates.json"):
        known(f"refused_candidates.json {cand.get('id')}", cand, "refused_candidates.json")
        rows["refused_candidates"].append((cand["id"], cand["ruling"], cand["reasoning"]))
        rows["candidate_relation_types"] += [(cand["id"], i, t) for i, t in enumerate(cand["relation_types"])]
        rows["candidate_reasons"] += [(cand["id"], i, t) for i, t in enumerate(cand["reasons"])]
        ends = [("source", cand["source_entities"]), ("target", cand["target_entities"])] + ([("item", [cand["item"]])] if "item" in cand else [])
        for side, endpoints in ends:
            for i, end in enumerate(endpoints):
                if isinstance(end, str):
                    rows["candidate_endpoints"].append((cand["id"], side, i, end, "value", None, "absent"))
                else:
                    rows["candidate_endpoints"].append((cand["id"], side, i, None, end["state"], *vs(end, "name")))
        for i, k in enumerate(cand["considered"]):
            known(f"refused_candidates.json {cand['id']} considered {i}", k, "considered")
            read_ = k.get("read")
            if isinstance(read_, dict) and "state" in read_:
                read_cols = (None, read_["state"], None, read_["state"])
            elif read_ is None:
                read_cols = (None, "absent", None, "absent")
            else:
                read_cols = (read_["accessed_at"], "value", read_["sha256"], "value")
            rows["candidate_considered"].append((cand["id"], i, *vs(k, "claim_id"), *vs(k, "source_id"), *vs(k, "locator"), *vs(k, "anchor"), *read_cols))

    for i, b in enumerate(read(data / "identity_basis.json")):
        known(f"identity_basis.json row {i}", b, "identity_basis.json")
        rows["identity_basis"].append((
            b["kind"], i, *vs(b, "record"), *vs(b, "concept"), *vs(b, "term"), *vs(b, "term_is"), *vs(b, "class"),
            *vs(b, "claim_id"), *vs(b, "facility_kind"), *vs(b, "word"), *vs(b, "note"),
        ))

    for table, values in rows.items():
        if values:
            marks = ", ".join("?" for _ in values[0])
            con.executemany(f"INSERT INTO {table} VALUES ({marks})", values)
    return con


def attribute(rows: dict, record_id: str, field: str, value) -> None:
    """An attribute held as assertions or as a state becomes field_values rows (sql-layer.md §3)."""
    if isinstance(value, dict):
        assert set(value) == {"state"}, f"{record_id}.{field}: an object that is not a state"
        rows["field_values"].append((record_id, field, 0, None, value["state"], None, "absent", None, "absent"))
        return
    for i, assertion in enumerate(value):
        rows["field_values"].append((record_id, field, i, text(assertion["value"]), "value", *vs(assertion, "valid_from"), *vs(assertion, "valid_to")))
        rows["field_value_claims"] += [(record_id, field, i, j, cid) for j, cid in enumerate(assertion["claim_ids"])]
        extra = sorted(set(assertion) - {"value", "claim_ids", "valid_from", "valid_to"})
        if extra:
            raise UnknownKey(f"{record_id}.{field}[{i}]: key(s) {extra} are not in the loader's contract")


def run(con: duckdb.DuckDBPyConnection, query: Path) -> tuple[list[str], list[dict]]:
    """Run one query file; return its column names and rows, with DuckDB lists as Python lists."""
    cursor = con.execute(query.read_text(encoding="utf-8"))
    columns = [d[0] for d in cursor.description]
    return columns, [dict(zip(columns, row)) for row in cursor.fetchall()]


def result_document(con, query: Path, upstream: tuple[Path, ...] = ()) -> bytes:
    columns, rows = run(con, query)
    manifest = [(p, h) for p, h in con.execute("SELECT path, sha256 FROM load_manifest ORDER BY path").fetchall()]
    queries = [(f"sql/{q.name}", sha256(q)) for q in (*upstream, query)]
    inputs = sorted(manifest + [("tools/warehouse.py", sha256(THIS))] + queries)
    digest = hashlib.sha256("".join(f"{p}\0{h}\n" for p, h in inputs).encode()).hexdigest()
    document = {
        "about": "Generated by tools/warehouse.py from the canonical records; never edited by hand (docs/architecture/sql-layer.md).",
        "query": f"sql/{query.name}",
        "query_sha256": sha256(query),
        "engine": f"duckdb {duckdb.__version__}",
        "input_digest": digest,
        "inputs": [{"path": p, "sha256": h} for p, h in inputs],
        "columns": columns,
        "rows": rows,
    }
    return (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def query_order(queries: list[Path]) -> list[tuple[Path, tuple[Path, ...]]]:
    """Each query with every query it reads, upstream first (S15, D-131).

    A query reads another when its code (comments aside) names that query's file stem as a table. Each
    query becomes a view once it has run, so a later query builds on an earlier result instead of
    repeating its definitions. The order is the sorted order, with each query moved after the queries it
    reads; a cycle stops the run.
    """
    stems = {q.stem: q for q in queries}
    reads = {}
    for q in queries:
        code = "\n".join(line for line in q.read_text(encoding="utf-8").splitlines() if not line.lstrip().startswith("--"))
        reads[q.stem] = sorted(s for s in stems if s != q.stem and re.search(rf"\b{re.escape(s)}\b", code))
    ordered: list[str] = []
    visiting: set[str] = set()

    def visit(stem: str) -> None:
        if stem in ordered:
            return
        if stem in visiting:
            raise ValueError(f"sql/{stem}.sql: queries read each other in a cycle")
        visiting.add(stem)
        for upstream in reads[stem]:
            visit(upstream)
        visiting.discard(stem)
        ordered.append(stem)

    for stem in sorted(stems):
        visit(stem)

    def closure(stem: str) -> list[str]:
        out: list[str] = []
        for upstream in reads[stem]:
            for s in closure(upstream) + [upstream]:
                if s not in out:
                    out.append(s)
        return out

    return [(stems[s], tuple(stems[u] for u in sorted(closure(s)))) for s in ordered]


def build_results(data: Path = DATA, sql: Path = SQL) -> dict[str, bytes]:
    """Every query's result, as the bytes tools/warehouse.py writes, keyed by its repository path."""
    con = load(data)
    try:
        results = {}
        for query, upstream in query_order(sorted(sql.glob("*.sql"))):
            results[f"sql/results/{query.stem}.json"] = result_document(con, query, upstream)
            # the query becomes a view, so a later query can read its result as a table (D-131)
            con.execute(f'CREATE VIEW "{query.stem}" AS ' + query.read_text(encoding="utf-8").strip().rstrip(";"))
        return dict(sorted(results.items()))
    finally:
        con.close()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if a committed result differs from a fresh run")
    parser.add_argument("--db", help="also save the database here (outside the repository) to explore it")
    args = parser.parse_args(argv)
    if args.db:
        target = Path(args.db).resolve()
        if target == REPO_ROOT or REPO_ROOT in target.parents:
            raise ValueError(f"--db {args.db}: the database is never kept inside the repository; choose a path outside the repository")
    results = build_results()
    if args.check:
        stale = [p for p, content in sorted(results.items()) if not (REPO_ROOT / p).exists() or (REPO_ROOT / p).read_bytes() != content]
        extra = sorted(p.relative_to(REPO_ROOT).as_posix() for p in (SQL / "results").glob("*.json") if p.relative_to(REPO_ROOT).as_posix() not in results)
        for p in stale:
            print(f"results: {p} differs from a fresh run (python tools/warehouse.py)")
        for p in extra:
            print(f"results: {p} has no query in sql/")
        if stale or extra:
            return 1
        print("results: up to date")
        return 0
    (SQL / "results").mkdir(exist_ok=True)
    for path, content in sorted(results.items()):
        (REPO_ROOT / path).write_bytes(content)
        print(f"wrote {path} ({len(json.loads(content)['rows'])} rows)")
    if args.db:
        target.unlink(missing_ok=True)
        load(DATA, str(target)).close()
        print(f"saved the database to {target} (a disposable copy; data/ stays the only home of the facts)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except ValueError as error:
        print(f"warehouse: {error}", file=sys.stderr)
        raise SystemExit(2)
