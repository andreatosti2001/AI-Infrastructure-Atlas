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
    --json              print the answer as data (S11, D-101): the structure the page build reads

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

    # --- answers as data (S11, D-101): the text below and the page build both read these -------

    def entry(self, edge: dict, where: str) -> dict:
        """One edge as data: the record, where it lives, its level, its period and its claims."""
        level = VOCAB[edge["relation_type"]]["x-level"]
        period = None
        if "valid_from" in edge or "valid_to" in edge:
            period = {key: edge[key] for key in ("valid_from", "valid_to") if key in edge}
        claims = []
        for claim_id in edge["claim_ids"]:
            claim = self.claims.get(claim_id)
            if claim:
                claims.append({"id": claim_id, "claim_type": claim[0]["claim_type"], "evidence_status": claim[0]["evidence_status"], "where": claim[1]})
            else:
                claims.append({"id": claim_id, "missing": True})
        return {"edge": edge, "where": where, "level": level, "period": period, "claims": claims}

    def into(self, ref: str, types) -> list[tuple[dict, str]]:
        return [(e, w) for e, w in self.edges if e["target_entity"] == ref and e["relation_type"] in types]

    def depends_on_tree(self, ref: str) -> list[dict]:
        """The structural edges into ref, then into each dependent: a walk made now (RR-5)."""

        def walk(node: str, path: tuple[str, ...]) -> list[dict]:
            found = []
            for edge, where in self.into(node, STRUCTURAL):
                item = self.entry(edge, where)
                dependent = edge["source_entity"]
                item["cycle"] = dependent in path
                item["dependents"] = [] if item["cycle"] else walk(dependent, path + (dependent,))
                found.append(item)
            return found

        return walk(ref, (ref,))

    def supplier_rows(self, ref: str) -> dict:
        """A product's vendor field, the supplies edges whose item is ref, and the supplier of each
        incorporates edge into ref."""
        record = self.records.get(ref)
        vendor = record[0]["vendor"] if record and record[0].get("type") == "product" else None
        company_level = [self.entry(e, w) for e, w in self.edges if e["relation_type"] == "supplies" and e.get("item") == ref]
        product_level = []
        for edge, where in self.into(ref, ("incorporates",)):
            item = self.entry(edge, where)
            item["supplier"] = edge["supplier"]
            product_level.append(item)
        return {"vendor": vendor, "company_level": company_level, "product_level": product_level}

    def actors_list(self, ref: str) -> list[dict]:
        return [self.entry(e, w) for e, w in self.into(ref, ACTIVITY)]

    def edges_at(self, ref: str) -> list[dict]:
        found = []
        for edge, where in self.edges:
            reading = None
            if edge["source_entity"] == ref:
                reading = "forward"
            elif edge["target_entity"] == ref:
                reading = "inverse"
            elif edge.get("item") == ref:
                reading = "item"
            if reading:
                item = self.entry(edge, where)
                item["reading"] = reading
                found.append(item)
        return found

    # --- the text, rendered from the data -------------------------------------------------------

    def evidence_line(self, item: dict) -> str:
        parts = []
        for claim in item["claims"]:
            parts.append(f"{claim['id']} (MISSING)" if claim.get("missing") else f"{claim['id']} ({claim['claim_type']}, {claim['evidence_status']}, {claim['where']})")
        return "evidence: " + "; ".join(parts)

    def header(self, item: dict) -> str:
        period = ""
        if item["period"] is not None:
            period = f" · {item['period'].get('valid_from', '…')} to {item['period'].get('valid_to', '…')}"
        elif item["level"] == "instance":
            period = " · no period in the claims"
        return f"{item['edge']['id']} · {item['where']} · {item['level']}{period}"

    def show(self, lines: list[str], depth: int, item: dict, text: str | None = None) -> None:
        lines.append("  " * depth + (text or self.sentence(item["edge"])))
        lines.append("  " * (depth + 1) + self.header(item))
        lines.append("  " * (depth + 1) + self.evidence_line(item))

    # --- the questions ------------------------------------------------------------------------

    def depends_on(self, ref: str) -> list[str]:
        lines = [f"What depends on {self.name(ref)}? Structural edges into it, walked now (not stored, RR-5)."]

        def render(items: list[dict], depth: int) -> None:
            for item in items:
                self.show(lines, depth, item)
                if item["cycle"]:
                    lines.append("  " * (depth + 1) + f"(cycle at {item['edge']['source_entity']}; not walked again)")
                render(item["dependents"], depth + 1)

        tree = self.depends_on_tree(ref)
        render(tree, 1)
        if not tree:
            lines.append(f"  no recorded relationship: nothing recorded depends on {ref} (not 'nothing depends on it', RR-7)")
        return lines

    def suppliers(self, ref: str) -> list[str]:
        lines = [f"Who supplies {self.name(ref)}?"]
        rows = self.supplier_rows(ref)
        if rows["vendor"] is not None:
            lines.append(f"  vendor (an entity field, whose name the product carries; not a supply edge): {self.name(rows['vendor'])}")
        for item in rows["company_level"]:
            self.show(lines, 1, item, f"company level: {self.sentence(item['edge'])}")
        for item in rows["product_level"]:
            supplier = item["supplier"]
            if isinstance(supplier, list):
                text = "; ".join(f"{self.name(a['value'])} [{', '.join(a['claim_ids'])}]" for a in supplier)
            else:
                cited = f" [{', '.join(supplier['claim_ids'])}]" if "claim_ids" in supplier else ""
                text = f"{supplier['state']}{cited}"
            self.show(lines, 1, item, f"product level: in {self.name(item['edge']['source_entity'])}, supplier: {text}")
        if rows["vendor"] is None and not rows["company_level"] and not rows["product_level"]:
            lines.append(f"  no recorded relationship: no supplier of {ref} is recorded (not 'no supplier', RR-7)")
        return lines

    def actors(self, ref: str) -> list[str]:
        lines = [f"Who does what to {self.name(ref)}? Activity edges into it."]
        found = self.actors_list(ref)
        for item in found:
            self.show(lines, 1, item)
        if not found:
            lines.append(f"  no recorded relationship: no activity edge points to {ref} (RR-7)")
        return lines

    def all_edges(self, ref: str) -> list[str]:
        lines = [f"Edges at {self.name(ref)}."]
        found = self.edges_at(ref)
        for item in found:
            edge = item["edge"]
            if item["reading"] == "forward":
                self.show(lines, 1, item)
            elif item["reading"] == "inverse":
                reading = VOCAB[edge["relation_type"]]["x-inverse-reading"]
                self.show(lines, 1, item, f"{self.name(ref)} {reading} {self.name(edge['source_entity'])} (inverse reading, display only, RR-3)")
            else:
                self.show(lines, 1, item, f"item of: {self.sentence(edge)}")
        if not found:
            lines.append(f"  no recorded relationship at {ref} (RR-7)")
        return lines

    def evidence(self, ref: str) -> tuple[list[str], int]:
        return trace.trace(ref, trace.Store(self.data, []))


QUESTIONS = {"depends-on": "depends_on_tree", "suppliers": "supplier_rows", "actors": "actors_list", "edges": "edges_at"}


def navigate(command: str, ref: str, atlas: Atlas) -> tuple[list[str], int]:
    if command == "evidence":
        return atlas.evidence(ref)
    known = set(atlas.records) | {e["id"] for e, _ in atlas.edges}
    if ref not in known:
        return [f"unknown ID: {ref} (or a staging record: try --include-staging)"], 2
    handler = {"depends-on": atlas.depends_on, "suppliers": atlas.suppliers, "actors": atlas.actors, "edges": atlas.all_edges}[command]
    return handler(ref), 0


def navigate_data(command: str, ref: str, atlas: Atlas) -> tuple[dict, int]:
    """The same answer as data (D-101): what `--json` prints and what the page build reads."""
    if command == "evidence":
        data, status = trace.trace_data(ref, trace.Store(atlas.data, []))
        return {"command": command, "id": ref, "answer": data}, status
    known = set(atlas.records) | {e["id"] for e, _ in atlas.edges}
    if ref not in known:
        return {"command": command, "id": ref, "error": "unknown ID (or a staging record: try --include-staging)"}, 2
    record = atlas.records.get(ref)
    name = record[0].get("name") if record else None
    return {"command": command, "id": ref, "name": name, "answer": getattr(atlas, QUESTIONS[command])(ref)}, 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Navigate the Atlas's edges from the JSON files.")
    parser.add_argument("command", choices=("depends-on", "suppliers", "actors", "edges", "evidence"))
    parser.add_argument("id")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--include-staging", action="store_true")
    parser.add_argument("--json", action="store_true", help="print the answer as JSON (D-101)")
    args = parser.parse_args(argv[1:])
    atlas = Atlas(args.data, args.include_staging)
    if args.json:
        data, status = navigate_data(args.command, args.id, atlas)
        print(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True))
        return status
    lines, status = navigate(args.command, args.id, atlas)
    print("\n".join(lines))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
