"""Navigate the Atlas's edges from the JSON files (S10; edge-dataset.md §8; D-097).

Answers MA §18's questions with relational files and no graph database. Nothing it computes
is stored (RR-5): every walk is made when asked.

Usage:
    python tools/navigate.py COMMAND ID [--data DIR] [--include-staging]

    depends-on ID   What depends on this component? The structural edges (requires, has_part,
                    incorporates) that point into ID, then into each dependent, with the path.
    suppliers ID    Who supplies this component? supplies edges whose item is ID; for each
                    incorporates edge into ID, its supplier values or state; a product's vendor.
    actors ID       Who does what to this record? The activity edges that point into ID.
    edges ID        Every recorded edge at ID, both directions; the inverse is display text.
    evidence REL    What evidence supports the edge? The trace (tools/trace.py).

    --data              directory holding the data files (default: the repository's data/)
    --include-staging   also read staging edges and records, each marked "staging"

Canonical records only by default. A missing edge is "no recorded relationship", never
"none" (RR-7). Exit status: 0, or 2 when ID is unknown. Standard library only (D-003, D-026).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import trace

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = REPO_ROOT / "data"
SCHEMA = json.loads((REPO_ROOT / "schemas/relationships.schema.json").read_text(encoding="utf-8"))
VOCAB = {v["const"]: v for v in SCHEMA["$defs"]["vocab_relation_type"]["oneOf"]}
ENTITY_KINDS = ("companies", "jurisdictions", "technologies", "components", "products", "facilities")
# relationship-taxonomy.md §1, direction convention: structural edges point from the dependent to
# its dependency, activity edges from the actor to what it acts on.
STRUCTURAL = ("requires", "has_part", "incorporates")
ACTIVITY = ("owns", "operates", "designs", "fabricates", "packages", "supplies")


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


class Atlas:
    def __init__(self, data: Path, include_staging: bool) -> None:
        self.data = data
        places = ["canonical"] + (["staging"] if include_staging else [])
        self.records: dict[str, tuple[dict, str]] = {}
        self.edges: list[tuple[dict, str]] = []
        self.claims: dict[str, tuple[dict, str]] = {}
        for where in places:
            folder = data if where == "canonical" else data / "staging"
            for kind in ENTITY_KINDS:
                for record in load(folder / f"{kind}.json"):
                    self.records[record["id"]] = (record, where)
            self.edges += [(edge, where) for edge in load(folder / "relationships.json")]
        for where, path in (("staging", data / "staging" / "claims.json"), ("canonical", data / "claims.json")):
            for claim in load(path):
                self.claims[claim["id"]] = (claim, where)

    def name(self, ref: str) -> str:
        found = self.records.get(ref)
        return f"{ref} ({found[0].get('name', '')})" if found else f"{ref} (no record read)"

    def sentence(self, edge: dict) -> str:
        text = f"{self.name(edge['source_entity'])} {edge['relation_type']} {self.name(edge['target_entity'])}"
        return text + (f", item {self.name(edge['item'])}" if "item" in edge else "")

    def evidence_line(self, edge: dict) -> str:
        parts = []
        for claim_id in edge["claim_ids"]:
            claim = self.claims.get(claim_id)
            parts.append(f"{claim_id} ({claim[0]['claim_type']}, {claim[0]['evidence_status']}, {claim[1]})" if claim else f"{claim_id} (MISSING)")
        return "evidence: " + "; ".join(parts)

    def header(self, edge: dict, where: str) -> str:
        period = ""
        if "valid_from" in edge or "valid_to" in edge:
            period = f" · {edge.get('valid_from', '…')} to {edge.get('valid_to', '…')}"
        else:
            period = " · no period in the claims" if VOCAB[edge["relation_type"]]["x-level"] == "instance" else ""
        return f"{edge['id']} · {where} · {VOCAB[edge['relation_type']]['x-level']}{period}"

    def show(self, lines: list[str], depth: int, edge: dict, where: str, text: str | None = None) -> None:
        lines.append("  " * depth + (text or self.sentence(edge)))
        lines.append("  " * (depth + 1) + self.header(edge, where))
        lines.append("  " * (depth + 1) + self.evidence_line(edge))

    def into(self, ref: str, types) -> list[tuple[dict, str]]:
        return [(e, w) for e, w in self.edges if e["target_entity"] == ref and e["relation_type"] in types]

    # --- the questions ------------------------------------------------------------------------

    def depends_on(self, ref: str) -> list[str]:
        lines = [f"What depends on {self.name(ref)}? Structural edges into it, walked now (not stored, RR-5)."]
        found = False

        def walk(node: str, depth: int, path: tuple[str, ...]) -> None:
            nonlocal found
            for edge, where in self.into(node, STRUCTURAL):
                found = True
                self.show(lines, depth, edge, where)
                dependent = edge["source_entity"]
                if dependent in path:
                    lines.append("  " * (depth + 1) + f"(cycle at {dependent}; not walked again)")
                else:
                    walk(dependent, depth + 1, path + (dependent,))

        walk(ref, 1, (ref,))
        if not found:
            lines.append(f"  no recorded relationship: nothing recorded depends on {ref} (not 'nothing depends on it', RR-7)")
        return lines

    def suppliers(self, ref: str) -> list[str]:
        lines = [f"Who supplies {self.name(ref)}?"]
        found = False
        record = self.records.get(ref)
        if record and record[0].get("type") == "product":
            found = True
            lines.append(f"  vendor (an entity field, whose name the product carries; not a supply edge): {self.name(record[0]['vendor'])}")
        for edge, where in self.edges:
            if edge["relation_type"] == "supplies" and edge.get("item") == ref:
                found = True
                self.show(lines, 1, edge, where, f"company level: {self.sentence(edge)}")
        for edge, where in self.into(ref, ("incorporates",)):
            found = True
            supplier = edge["supplier"]
            if isinstance(supplier, list):
                text = "; ".join(f"{self.name(a['value'])} [{', '.join(a['claim_ids'])}]" for a in supplier)
            else:
                cited = f" [{', '.join(supplier['claim_ids'])}]" if "claim_ids" in supplier else ""
                text = f"{supplier['state']}{cited}"
            self.show(lines, 1, edge, where, f"product level: in {self.name(edge['source_entity'])}, supplier: {text}")
        if not found:
            lines.append(f"  no recorded relationship: no supplier of {ref} is recorded (not 'no supplier', RR-7)")
        return lines

    def actors(self, ref: str) -> list[str]:
        lines = [f"Who does what to {self.name(ref)}? Activity edges into it."]
        found = self.into(ref, ACTIVITY)
        for edge, where in found:
            self.show(lines, 1, edge, where)
        if not found:
            lines.append(f"  no recorded relationship: no activity edge points to {ref} (RR-7)")
        return lines

    def all_edges(self, ref: str) -> list[str]:
        lines = [f"Edges at {self.name(ref)}."]
        found = False
        for edge, where in self.edges:
            if edge["source_entity"] == ref:
                found = True
                self.show(lines, 1, edge, where)
            elif edge["target_entity"] == ref:
                found = True
                reading = VOCAB[edge["relation_type"]]["x-inverse-reading"]
                self.show(lines, 1, edge, where, f"{self.name(ref)} {reading} {self.name(edge['source_entity'])} (inverse reading, display only, RR-3)")
            elif edge.get("item") == ref:
                found = True
                self.show(lines, 1, edge, where, f"item of: {self.sentence(edge)}")
        if not found:
            lines.append(f"  no recorded relationship at {ref} (RR-7)")
        return lines

    def evidence(self, ref: str) -> tuple[list[str], int]:
        return trace.trace(ref, trace.Store(self.data, []))


def navigate(command: str, ref: str, atlas: Atlas) -> tuple[list[str], int]:
    if command == "evidence":
        return atlas.evidence(ref)
    known = set(atlas.records) | {e["id"] for e, _ in atlas.edges}
    if ref not in known:
        return [f"unknown ID: {ref} (or a staging record: try --include-staging)"], 2
    handler = {"depends-on": atlas.depends_on, "suppliers": atlas.suppliers, "actors": atlas.actors, "edges": atlas.all_edges}[command]
    return handler(ref), 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Navigate the Atlas's edges from the JSON files.")
    parser.add_argument("command", choices=("depends-on", "suppliers", "actors", "edges", "evidence"))
    parser.add_argument("id")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--include-staging", action="store_true")
    args = parser.parse_args(argv[1:])
    lines, status = navigate(args.command, args.id, Atlas(args.data, args.include_staging))
    print("\n".join(lines))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
