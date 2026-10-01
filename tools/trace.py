"""Trace what supports a record, a claim or a source (S06; D-053).

Answers the S06 gate question, "What exactly supports this relationship?", by printing the
chain record -> claims -> citations -> sources, and claim -> input claims, recursively.
For a source, it prints the source and the claims that cite it. Register labels such as
SRC-006 and S05-R1 resolve to their source records through `migrated_from`.

Usage:
    python tools/trace.py ID [--data DIR] [--records FILE ...]

    ID         a record ID (in a --records file), a claim ID, a source ID or a register label
    --data     directory holding sources.json, staging/claims.json and, once a claim is
               accepted, claims.json (default: the repository's data/)
    --records  a JSON array of records that cite claims (entities, relationships); repeatable.
               The entity files of --data (companies.json, jurisdictions.json and their
               staging copies, S07) are always read when they exist

Exit status: 0 when every reference resolves, 1 when one does not, 2 when ID is unknown.
Standard library only (D-003, D-026).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data"
# The entity data files (S07, H-2 layout), canonical then staging.
ENTITY_FILES = ("companies.json", "jurisdictions.json", "staging/companies.json", "staging/jurisdictions.json")


class Store:
    def __init__(self, data: Path, record_files: list[Path]) -> None:
        self.sources = {s["id"]: s for s in self._load(data / "sources.json")}
        self.labels = {s["migrated_from"]: s["id"] for s in self.sources.values() if "migrated_from" in s}
        self.claims: dict[str, dict] = {}
        self.where: dict[str, str] = {}
        for name, path in (("staging", data / "staging" / "claims.json"), ("canonical", data / "claims.json")):
            for claim in self._load(path):
                self.claims[claim["id"]] = claim
                self.where[claim["id"]] = name
        self.records: dict[str, tuple[dict, str]] = {}
        for path in [data / name for name in ENTITY_FILES]:
            for record in self._load(path):
                self.records[record["id"]] = (record, f"{'staging' if 'staging' in path.parts else 'canonical'} {path.name}")
        for path in record_files:
            for record in self._load(path, required=True):
                self.records[record["id"]] = (record, str(path))
        self.missing: list[str] = []

    @staticmethod
    def _load(path: Path, required: bool = False) -> list[dict]:
        if not path.exists():
            if required:
                raise SystemExit(f"no such file: {path}")
            return []
        records = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise SystemExit(f"{path} is not a JSON array of records")
        return records


def claim_paths(node, pointer: str = "") -> list[tuple[str, str, object]]:
    """Every (JSON pointer, claim ID, asserted value or None) in a record, in document order."""
    found = []
    if isinstance(node, dict):
        for key, value in node.items():
            path = f"{pointer}/{key}"
            if key in {"claim_ids", "identity_claim_ids"} and isinstance(value, list):
                found += [(path, claim_id, node.get("value", node.get("state"))) for claim_id in value]
            else:
                found += claim_paths(value, path)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found += claim_paths(value, f"{pointer}/{index}")
    return found


def stated(source: dict) -> str:
    dates = source["stated_dates"]
    if isinstance(dates, dict):
        return dates["state"]
    return ", ".join(f"{d['kind']} {d['date']}" for d in dates)


def state(value) -> str:
    return value["state"] if isinstance(value, dict) else value


class Printer:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.lines: list[str] = []
        self.shown: set[str] = set()

    def out(self, depth: int, text: str) -> None:
        self.lines.append("  " * depth + text)

    def missing(self, depth: int, what: str) -> None:
        self.store.missing.append(what)
        self.out(depth, f"MISSING: {what}")

    def source_lines(self, depth: int, source: dict) -> None:
        self.out(depth, f"source: \"{source['title']}\" · {source['publisher']} · {source['url']}")
        publisher = state(source["publisher_entity"])
        self.out(depth, f"class: {source['source_class']} · publisher record: {publisher}")
        self.out(depth, f"stated dates: {stated(source)}")
        retrieval = source["retrieval"]
        label = f" · migrated from {source['migrated_from']}" if "migrated_from" in source else ""
        self.out(depth, f"registered: {retrieval['method']} {retrieval['accessed_at']} sha256 {retrieval['sha256']}{label}")
        if "filing_copy" in source:
            self.out(depth, f"filing copy: {source['filing_copy']}")

    def review(self, claim: dict) -> str:
        review = claim["review"]
        if "verdict" in review:
            return f"{review['verdict']} by the {review['reviewer']} on {review['reviewed_on']} ({review['recorded_in']})"
        return review["state"].replace("_", " ")

    def claim(self, depth: int, claim_id: str, path: tuple[str, ...] = ()) -> None:
        store = self.store
        if claim_id in path:
            self.missing(depth, f"input cycle {' -> '.join(path + (claim_id,))}")
            return
        claim = store.claims.get(claim_id)
        if claim is None:
            self.missing(depth, f"claim {claim_id}")
            return
        verified = f"verified {claim['verified_on']}" if "verified_on" in claim else "not verified"
        self.out(depth, f"{claim_id} · {claim['claim_type']} · {claim['evidence_status']} · {verified} · {store.where[claim_id]}, {self.review(claim)}")
        if claim_id in self.shown:
            self.out(depth + 1, "(shown above)")
            return
        self.shown.add(claim_id)
        self.out(depth + 1, f"statement: {claim['statement']}")
        if "as_of" in claim:
            self.out(depth + 1, f"as of: {state(claim['as_of'])}")
        for number, citation in enumerate(claim.get("citations", []), start=1):
            self.citation(depth + 1, number, citation)
        if "reasoning" in claim:
            self.out(depth + 1, f"reasoning: {claim['reasoning']}")
        if "search" in claim:
            self.search(depth + 1, claim["search"])
        for other in claim.get("disputed_with", []):
            if other in store.claims:
                self.out(depth + 1, f"disputed with: {other} (a competing claim, kept)")
            else:
                self.missing(depth + 1, f"competing claim {other}")
        for input_id in claim.get("input_claim_ids", []):
            self.out(depth + 1, "input:")
            self.claim(depth + 2, input_id, path + (claim_id,))

    def citation(self, depth: int, number: int, citation: dict) -> None:
        self.out(depth, f"citation {number} · {citation['source_id']} · standing {citation['standing']}")
        source = self.store.sources.get(citation["source_id"])
        if source is None:
            self.missing(depth + 1, f"source {citation['source_id']}")
        else:
            self.source_lines(depth + 1, source)
        self.out(depth + 1, f"locator: {citation['locator']}")
        self.out(depth + 1, f"anchor: \"{citation['anchor']}\"")
        if "originator" in citation:
            origin = citation["originator"]
            self.out(depth + 1, f"originator: {origin['name']} · {origin['source_class']} · not retrieved · named at {origin['named_at']}")
        read = citation.get("read")
        if read:
            if source is None:
                note = ""
            elif read["sha256"].startswith(source["retrieval"]["sha256"]) or source["retrieval"]["sha256"].startswith(read["sha256"]):
                note = " (same bytes as registered)"
            else:
                note = " (bytes changed since registration; anchor re-checked)"
            self.out(depth + 1, f"read by the Verifier: {read['accessed_at']} sha256 {read['sha256'][:12]}{note}")

    def search(self, depth: int, search: dict) -> None:
        self.out(depth, f"search: {search['question']} ({search['searched_on']}) → {search['conclusion']}")
        for entry in search["classes"]:
            detail = ", ".join(entry.get("source_ids", [])) or entry.get("gap", "")
            self.out(depth + 1, f"{entry['source_class']}: {entry['outcome']} · {detail}")
            for source_id in entry.get("source_ids", []):
                if source_id not in self.store.sources:
                    self.missing(depth + 2, f"source {source_id}")

    def record(self, record: dict, origin: str) -> None:
        if "relation_type" in record:
            kind = "relationship record"
            summary = f"{record['source_entity']} {record['relation_type']} {record['target_entity']}"
            if "item" in record:
                summary += f" (item {record['item']})"
        else:
            kind = f"{record.get('type', 'entity')} record"
            summary = record.get("name", "")
        self.out(0, f"{record['id']} · {kind} · {origin}")
        self.out(1, summary)
        for pointer, claim_id, value in claim_paths(record):
            self.out(1, f"{pointer}:" + (f" {value}" if value is not None and pointer.endswith("/claim_ids") else ""))
            self.claim(2, claim_id)
        for key, value in record.items():
            if isinstance(value, dict) and "state" in value and "claim_ids" not in value:
                self.out(1, f"/{key}: {value['state']}")

    def source(self, source: dict) -> None:
        self.out(0, f"{source['id']} · source record")
        self.source_lines(1, source)
        citing = []
        for claim in self.store.claims.values():
            ids = [c["source_id"] for c in claim.get("citations", [])]
            ids += [s for e in claim.get("search", {}).get("classes", []) for s in e.get("source_ids", [])]
            if source["id"] in ids:
                citing.append(claim["id"])
        self.out(1, "cited by: " + (", ".join(sorted(citing)) if citing else "no claim"))


def trace(identifier: str, store: Store) -> tuple[list[str], int]:
    store.missing = []  # each trace reports only its own unresolved references
    printer = Printer(store)
    source_id = store.labels.get(identifier, identifier)
    if identifier in store.records:
        printer.record(*store.records[identifier])
    elif identifier in store.claims:
        printer.claim(0, identifier)
    elif source_id in store.sources:
        printer.source(store.sources[source_id])
    else:
        return [f"unknown ID: {identifier}"], 2
    return printer.lines, 1 if store.missing else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Trace what supports a record, a claim or a source.")
    parser.add_argument("id")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--records", type=Path, action="append", default=[])
    args = parser.parse_args(argv[1:])
    lines, status = trace(args.id, Store(args.data, args.records))
    print("\n".join(lines))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
