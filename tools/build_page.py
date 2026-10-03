"""Build the S11 vertical-slice page from the Atlas's records (vertical-slice.md; D-102).

Writes site/hbm-chain/index.html: one self-contained file with inline CSS and SVG and no script,
generated from data/ (the refused candidates included, D-109), the schemas, the rule documents,
decisions.md, the first SQL query and its committed result (S14: sql/, read as files; DuckDB is never
imported here, D-118) and the template
tools/page_template.html. The page answers one question: "What does an AI accelerator's memory
depend on, and who is known to make it?"

Usage:
    python tools/build_page.py           write the page
    python tools/build_page.py --check   rebuild in memory; exit 1 if the committed page differs

Every value on the page is rendered from its home with the attributes the page checks read
(tests/test_page.py, PG-1 to PG-10): a record value carries data-ref and data-field, a fixed
label data-label, a derived value data-derived. The framing lives in the template. The output is
deterministic: the same inputs give the same bytes. Standard library only (D-003, D-026).
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import string
import sys
from pathlib import Path

import navigate
import trace

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
TEMPLATE = REPO_ROOT / "tools" / "page_template.html"
PAGE = REPO_ROOT / "site" / "hbm-chain" / "index.html"
TO_ROOT = "../../"  # from the page's directory to the repository root
INPUT_GLOBS = ("data/*.json", "data/staging/*.json", "schemas/*.json", "sql/*.sql", "sql/results/*.json")
INPUT_FILES = (
    "docs/architecture/company-dataset.md",
    "docs/architecture/decisions.md",
    "docs/architecture/relationship-taxonomy.md",
    "docs/research/source-policy.md",
    "tools/build_page.py",
    "tools/navigate.py",
    "tools/page_template.html",
    "tools/trace.py",
)

# The journey specification (vertical-slice.md §2): IDs and row keys only, never values.
JOURNEY = {
    # the deepest dependency the question reaches; the chain is walked into it
    "walk_root": "technology-3d-die-stacking",
    # recorded nearby, not linked to the chain (H-1; the human's lane rulings, D-100)
    "lane_edges": ["rel-company-sk-hynix-operates-facility-kr-m16"],
    # a recorded gap drawn on the diagram: a refused candidate and the canonical claim it opens (D-092, D-109)
    "drawn_gaps": [{"candidate": "cand-001", "claim": "claim-tsmc-fabricates-h100"}],
    # further refused candidates that answer "who makes it?" for records on the page (vertical-slice.md §5),
    # shown as cards grouped by reason, never in the diagram (D-109)
    # (the drawn gap's own candidate is shown with it, under "Recorded gaps")
    "candidates": ["cand-002", "cand-007", "cand-011"],
    # rulings the page states as limitations
    "decisions": ["D-091", "D-092", "D-093", "D-094", "D-099"],
}

# The first SQL result on the page and its tutorial (S14, H-3, D-115, D-121): the query file and the
# result tools/warehouse.py wrote from it. The page reads both as files.
SQL_QUERY = "accelerator_dependencies"
SQL_FLAGS = {"rests_on_atlas_interpretation": "rests on the Atlas’s own definitions", "publishers": "one publisher only"}

# Where each rule code the page quotes is defined (the new-user test, D-108): a code's one-line home.
RULE_HOMES = {
    "ER": "docs/research/source-policy.md",  # §6 table: the rule in bold
    "RR": "docs/architecture/relationship-taxonomy.md",  # §1 table: the rule in bold
    "F": "docs/architecture/company-dataset.md",  # the section titled with the code: its **Rule** paragraph
}
RULE_CODE = re.compile(r"\b(?:ER|RR|F)-\d+\b|\bD-\d{3}\b")

# Every fixed word on the page. A label names no record and holds no digit (PG-1).
LABELS = frozenset(
    {
        "Atlas framing", "Skip to the evidence", "AI Infrastructure Atlas", "Dependency journey",
        "What does an", "’s memory depend on, and who is known to make it?",
        "Short answer", "How to read this page", "Why it matters", "The chain", "The chain in words",
        "How to read the diagram", "Key context", "What each maker states about the memory",
        "Definitions the Atlas uses", "What the Atlas does not know", "Unknown values", "Recorded gaps",
        "Candidates that are not edges", "No recorded relationship", "Evidence", "Method and limitations",
        "Built from", "Dates", "Rulings this page depends on", "Reproduce", "Terms",
        "stated", "inferred", "gap: no edge", "supplier (who makes it)", "supplier (who makes this part)", "supplier", "class", "evidence",
        "named thing (instance level)", "vendor-neutral class (class level)",
        "stated: at least one cited claim is a FACT", "inferred: every cited claim is a DERIVATION",
        "gap: an unknown value or a recorded gap, never a zero", "recorded in the Atlas, not linked to the chain",
        "also recorded in the Atlas", "not linked to any accelerator on this chain", "instance of",
        "recorded as a kind of", "a property of its record,", "not a supply link", "a property of its record, not a supply link",
        "recorded gap", "a claim the Atlas holds, not an edge", "recorded gap: a claim the Atlas holds, not an edge",
        "ruling", "candidate", "type", "why not", "item", "no record in the Atlas", "the rule that refuses candidates:",
        "and", "each", "which", "Who makes that memory:", "in each", "Jump to", "Rules cited above", "defined in",
        "claim", "other claims in this record’s trace",
        "from the edge design record", "edge design record", "activity edges into this record:",
        "no recorded relationship", "input files", "input digest",
        "claims on this page verified from", "to", "sources accessed from",
        "back to the diagram", "ID", "level", "period", "no period in the claims", "basis", "name",
        "vendor", "working definition", "broader", "cited at", "verified", "review:", "by the", "on",
        "recorded in", "statement", "as of", "source", "publisher", "standing", "URL", "stated dates",
        "accessed", "locator", "anchor", "read by the Verifier", "same bytes as registered",
        "bytes changed since registration", "reasoning", "inputs to this inference", "shown above",
        "originator", "disputed with", "search", "outcome",
        "Relation types", "Claim types", "Evidence status", "Standing", "Unknown and unstated values", "Source classes",
        "python tools/navigate.py depends-on", "python tools/trace.py", "python tools/build_page.py --check",
        "the walk:", "the evidence for one edge:", "rebuild and compare:",
        "The chain as a table", "How this was computed", "Accelerator", "Link", "How the Atlas knows",
        "Evidence dated", "Published by", "Caveats", "Traced to", "gap", "IDs", "no source cited",
        "why it counts as an accelerator:", "edge or candidate:", "reached through:", "claims:", "sources:",
        "publisher not linked to a company record:", "The question", "The query, step by step",
        "How to read the result", "query file", "result file", "check the result:",
        "python tools/warehouse.py --check",
    }
)

# Fields whose claims say where or what a record is legally, not what the journey asks; their claims sit in a
# closed disclosure in the record's panel (the new-user test, D-108).
CONTEXT_FIELDS = ("legal_name", "incorporated_in", "headquartered_in", "located_in", "locality")

TERM_GROUPS = ("Relation types", "Claim types", "Evidence status", "Standing", "Unknown and unstated values", "Source classes")

PALETTE = {
    "surface-page": "#ffffff",
    "surface-panel": "#f6f7f9",
    "surface-class": "#e9eef4",
    "surface-gap": "#fff3df",
    "surface-framing": "#f3f1ec",
    "ink-strong": "#141d29",
    "ink-body": "#27313d",
    "ink-muted": "#4d5865",
    "ink-gap": "#713c00",
    "ink-link": "#174a86",
    "line-ink": "#2b4769",
    "line-gap": "#9c5800",
    "line-rule": "#6f7b88",
    "line-focus": "#0b57d0",
}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def load_json(path: Path) -> list:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


def input_digest(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.encode("utf-8") + b"\0" + hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest().encode("ascii") + b"\n")
    return digest.hexdigest()


def sql_tutorial(text: str) -> dict:
    """A query file read as its tutorial (sql-layer.md §6): the -- question: and -- reading: paragraphs,
    then each -- step: with its explanation lines and its SQL, exactly as the file has them."""
    lines = text.split("\n")
    header, steps, field, i = {}, [], None, 0
    while i < len(lines) and not lines[i].startswith("-- step:"):
        m = re.match(r"^-- (question|reading): (.*)$", lines[i])
        if m:
            field = m.group(1)
            header[field] = m.group(2).strip()
        elif lines[i].startswith("--   ") and field:
            header[field] += " " + lines[i][5:].strip()
        elif lines[i] in ("--", ""):
            field = None
        else:
            raise BuildError(f"sql/{SQL_QUERY}.sql line {i + 1} is not part of the tutorial header")
        i += 1
    while i < len(lines):
        title = lines[i].removeprefix("-- step:").strip()
        i += 1
        explanation, code = [], []
        while i < len(lines) and lines[i].startswith("-- ") and not lines[i].startswith("-- step:"):
            explanation.append(lines[i][3:].strip())
            i += 1
        while i < len(lines) and not lines[i].startswith("-- step:"):
            code.append(lines[i])
            i += 1
        steps.append({"title": title, "explanation": " ".join(explanation), "code": "\n".join(code).strip("\n")})
    if not header.get("question") or not header.get("reading") or not steps:
        raise BuildError(f"sql/{SQL_QUERY}.sql has no question, reading or steps for its tutorial")
    return {"header": header, "steps": steps}


class BuildError(Exception):
    """The journey cannot be drawn honestly from the records; the page is not written."""


class Page:
    def __init__(self, data: Path = DATA) -> None:
        self.atlas = navigate.Atlas(data, False)
        self.store = trace.Store(data, [])
        self.schemas = {p.name.split(".")[0]: json.loads(p.read_text(encoding="utf-8")) for p in sorted((REPO_ROOT / "schemas").glob("*.json"))}
        decisions = (REPO_ROOT / "docs/architecture/decisions.md").read_text(encoding="utf-8")
        self.decisions = {m.group(1): m.group(2).strip() for m in re.finditer(r"^## (D-\d{3}) — (.+)$", decisions, re.M)}
        self.rules: dict[str, str] = {}
        for prefix, path in RULE_HOMES.items():
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            for m in re.finditer(rf"^\| ({prefix}-\d+) \| \*\*(.+?)\*\*", text, re.M):
                self.rules[m.group(1)] = m.group(2)
            for m in re.finditer(rf"^## [^\n]*\(({prefix}-\d+)\)\n\n\*\*Rule\*\* \([^)]*\)\. (.+?)\n\n", text, re.M | re.S):
                self.rules[m.group(1)] = " ".join(m.group(2).split())
        self.homes: dict[str, dict] = {}
        for record, _ in self.atlas.records.values():
            self.homes[record["id"]] = record
        for edge, _ in self.atlas.edges:
            self.homes[edge["id"]] = edge
        for claim_id, claim in self.store.claims.items():
            if self.store.where[claim_id] == "canonical":
                self.homes[claim_id] = claim
        self.homes.update(self.store.sources)
        # refused candidates (D-109): canonical only; never read as edges or records by the walk
        self.candidates = {c["id"]: c for c in load_json(data / "refused_candidates.json")}
        self.homes.update(self.candidates)
        self.terms: dict[str, set[str]] = {}
        self.claims_shown: set[str] = set()
        self.sources_shown: set[str] = set()
        self.ids = 0

    # --- values ---------------------------------------------------------------------------------

    def value(self, ref: str, field: str):
        if ref.startswith("schema:"):
            stem, _, rest = ref[len("schema:") :].partition("#")
            name, _, const = rest.partition("/")
            node = self.schemas[stem]["$defs"][name]
            if const:
                node = next(item for item in node["oneOf"] if item.get("const") == const)
        elif ref.startswith("doc:decisions#"):
            key = ref[len("doc:decisions#") :]
            return key if field == "id" else self.decisions[key].replace("`", "")
        elif ref.startswith("doc:rules#"):
            key = ref[len("doc:rules#") :]
            return key if field == "code" else self.rules[key].replace("`", "")
        else:
            node = self.homes[ref]
        for part in [p for p in field.split("/") if p]:
            node = node[int(part)] if isinstance(node, list) else node[part]
        if not isinstance(node, (str, int, float)):
            raise BuildError(f"{ref} {field} is not a scalar")
        return node

    def attrs(self, extra: dict | None) -> str:
        return "".join(f' {k}="{esc(v)}"' if v is not None else f" {k}" for k, v in (extra or {}).items())

    def ref(self, ref: str, field: str, tag: str = "span", fmt: str | None = None, cls: str | None = None, **extra) -> str:
        """A record value: the text is the value at its home (PG-2)."""
        text = str(self.value(ref, field))
        if fmt == "state":
            text = text.replace("_", " ")
        attributes = {"class": cls, "data-ref": ref, "data-field": field, "data-format": fmt} | {k.replace("_", "-"): v for k, v in extra.items()}
        attributes = {k: v for k, v in attributes.items() if v is not None}
        return f"<{tag}{self.attrs(attributes)}>{esc(text)}</{tag}>"

    def absent(self, ref: str, field: str, text: str, tag: str = "span", cls: str | None = None) -> str:
        """A field the record does not hold, said in words (PG-2, data-absent)."""
        try:
            self.value(ref, field)
        except (KeyError, IndexError):
            return f'<{tag}{self.attrs({"class": cls})} data-ref="{esc(ref)}" data-field="{esc(field)}" data-absent>{esc(self.label_text(text))}</{tag}>'
        raise BuildError(f"{ref} {field} is present")

    @staticmethod
    def label_text(text: str) -> str:
        if text not in LABELS:
            raise BuildError(f"not a label: {text!r}")
        return text

    def label(self, text: str, tag: str = "span", cls: str | None = None, **extra) -> str:
        attributes = {"class": cls} | {k.replace("_", "-"): v for k, v in extra.items()}
        return f"<{tag}{self.attrs({k: v for k, v in attributes.items() if v is not None})} data-label>{esc(self.label_text(text))}</{tag}>"

    def derived(self, kind: str, text: str, tag: str = "span", cls: str | None = None, **extra) -> str:
        """A value the page computes; tests/test_page.py recomputes it (PG-2)."""
        attributes = {"class": cls} | {k.replace("_", "-"): v for k, v in extra.items()}
        return f'<{tag} data-derived="{esc(kind)}"{self.attrs({k: v for k, v in attributes.items() if v is not None})}>{esc(text)}</{tag}>'

    def term(self, group: str, ref: str) -> None:
        self.terms.setdefault(group, set()).add(ref)

    def new_id(self, prefix: str) -> str:
        self.ids += 1
        return f"{prefix}-{self.ids}"

    def name(self, record_id: str, tag: str = "span", **extra) -> str:
        return self.ref(record_id, "/name", tag=tag, **extra)

    def evidence_link(self, target: str) -> str:
        return f'<a class="ev-link" href="#ev-{esc(target)}">{self.label("evidence")}</a>'

    # --- the journey, computed ------------------------------------------------------------------

    def journey(self) -> dict:
        tree = self.atlas.depends_on_tree(JOURNEY["walk_root"])
        if len(tree) != 1:
            raise BuildError("the composition is drawn for one edge into the walk root")
        root_edge = tree[0]
        component = root_edge["edge"]["source_entity"]
        products = root_edge["dependents"]
        if not 1 <= len(products) <= 2 or any(p["edge"]["relation_type"] != "incorporates" or p["dependents"] for p in products):
            raise BuildError("the composition is drawn for one or two products incorporating the component")
        for item in (root_edge, *products):
            if item["where"] != "canonical" or any(c.get("missing") or c["where"] != "canonical" for c in item["claims"]):
                raise BuildError(f"{item['edge']['id']} rests on a record that is not canonical")
        for node in (JOURNEY["walk_root"], component):
            if self.atlas.actors_list(node):
                raise BuildError(f"an activity edge into {node} has no place in the composition")
        columns = []
        for item in products:
            product = item["edge"]["source_entity"]
            actors = self.atlas.actors_list(product)
            gaps = [g for g in JOURNEY["drawn_gaps"] if self.gap_ends(g)[1] == product]
            if len(actors) + len(gaps) > 1:
                raise BuildError(f"{product}: one actor slot")
            columns.append({"item": item, "product": product, "actor": actors[0] if actors else None, "gap": gaps[0] if gaps else None})
        product_ids = {c["product"] for c in columns}
        lane_edges = []
        for edge_id in JOURNEY["lane_edges"]:
            found = [(e, w) for e, w in self.atlas.edges if e["id"] == edge_id]
            if not found:
                raise BuildError(f"lane edge {edge_id} is not canonical")
            lane_edges.append(self.atlas.entry(*found[0]))
        chain_ids = {JOURNEY["walk_root"], component} | product_ids
        lane_products = [r["id"] for r, _ in self.atlas.records.values() if r.get("type") == "product" and component in r.get("instance_of", []) and r["id"] not in chain_ids]
        if len(lane_edges) > 1 or len(lane_products) > 1:
            raise BuildError("the lane is drawn for one edge and one product")
        lane_records = {r for e in lane_edges for r in (e["edge"]["source_entity"], e["edge"]["target_entity"])} | set(lane_products)
        for edge, _ in self.atlas.edges:
            ends = {edge["source_entity"], edge["target_entity"]}
            supplier = edge.get("supplier")
            named = {a["value"] for a in supplier} if isinstance(supplier, list) else set()
            if (ends & lane_records and ends & product_ids) or named & lane_records:
                raise BuildError(f"{edge['id']} links the lane to the chain: the lane's text would be false")
        return {"root": root_edge, "component": component, "columns": columns, "lane_edges": lane_edges, "lane_products": lane_products}

    def candidate(self, cand_id: str) -> dict:
        if cand_id not in self.candidates:
            raise BuildError(f"refused candidate {cand_id} is not canonical")
        return self.candidates[cand_id]

    def gap_ends(self, gap: dict) -> tuple[str, str]:
        """The drawn gap's two records: its candidate's endpoints, by ID (D-109), never by name."""
        cand = self.candidate(gap["candidate"])
        ends = cand["source_entities"] + cand["target_entities"]
        if len(ends) != 2 or len(cand["relation_types"]) != 1 or not all(isinstance(e, str) and e in self.homes for e in ends):
            raise BuildError(f"the drawn gap {gap['candidate']} needs one relation type between two records")
        return ends[0], ends[1]

    @staticmethod
    def basis(item: dict) -> str:
        """Stated when at least one cited claim is a FACT; otherwise inferred (D-103)."""
        return "stated" if any(c.get("claim_type") == "FACT" for c in item["claims"]) else "inferred"

    def claim_basis(self, claim_id: str) -> str:
        return "stated" if self.homes[claim_id]["claim_type"] == "FACT" else "inferred"

    # --- the diagram (vertical-slice.md §3) ------------------------------------------------------

    def box(self, record_id: str, x: int, y: int, w: int, h: int) -> str:
        record = self.homes[record_id]
        is_class = record["type"] in ("component", "technology")
        type_id, name_id = self.new_id("t"), self.new_id("t")
        parts = [f'<a class="mark node{" class-level" if is_class else ""}" href="#ev-{esc(record_id)}" data-mark="node" data-target="{esc(record_id)}" aria-labelledby="{name_id} {type_id}">']
        parts.append(f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        if is_class:
            parts.append(f'<rect class="class-rule" x="{x}" y="{y}" width="{w}" height="5" rx="2"/>')
            parts.append(self.label("class", tag="text", cls="pill-text", x=x + w - 10, y=y + 20, text_anchor="end"))
        parts.append(self.ref(record_id, "/type", tag="text", cls="node-type", id=type_id, x=x + 10, y=y + 20))
        parts.append(self.name_text(record_id, x + 10, y + 37, w, name_id))
        parts.append("</a>")
        return "".join(parts)

    def name_text(self, record_id: str, x: int, y: int, w: int, name_id: str) -> str:
        """A record's name in its box, on two lines when it is too long for one. The text element is
        the one data-ref; its two tspans hold the name's words, split at a space."""
        name = str(self.value(record_id, "/name"))
        capacity = int((w - 20) / 8.2)
        if len(name) <= capacity:
            return self.name(record_id, tag="text", cls="node-name", id=name_id, x=x, y=y)
        cut = name.rfind(" ", 0, capacity + 1)
        if cut <= 0 or len(name) - cut - 1 > capacity:
            raise BuildError(f"{record_id}: the name does not fit its box on two lines")
        return (
            f'<text class="node-name" id="{name_id}" x="{x}" y="{y}" data-ref="{esc(record_id)}" data-field="/name">'
            f'<tspan x="{x}" y="{y}">{esc(name[:cut])}</tspan> <tspan x="{x}" y="{y + 16}">{esc(name[cut + 1:])}</tspan></text>'
        )

    def arrow(self, item: dict, x: int, y1: int, y2: int, relation_ref: tuple[str, str] | None = None, kind: str = "edge", target: str | None = None, ends: tuple[str, str] | None = None) -> str:
        """A line from y1 down to y2 at x, with its relation type and basis to its right."""
        target = target or item["edge"]["id"]
        basis = self.claim_basis(target) if kind == "gap" else self.basis(item)
        rel_id, basis_id = self.new_id("t"), self.new_id("t")
        classes = f"mark {kind}{' inferred' if basis == 'inferred' else ''}"
        extra = f' data-from="{esc(ends[0])}" data-to="{esc(ends[1])}"' if ends else ""
        parts = [f'<a class="{classes}" href="#ev-{esc(target)}" data-mark="{kind}" data-target="{esc(target)}" data-basis="{basis}"{extra} aria-labelledby="{rel_id} {basis_id}">']
        parts.append(f'<rect class="hit" x="{x - 12}" y="{y1}" width="24" height="{y2 - y1}"/>')
        marker = "" if kind == "gap" else ' marker-end="url(#arrow)"'
        parts.append(f'<line class="line" x1="{x}" y1="{y1 + 1}" x2="{x}" y2="{y2 - 3}"{marker}/>')
        ref, field = relation_ref or (item["edge"]["id"], "/relation_type")
        parts.append(self.ref(ref, field, tag="text", cls="edge-type halo", id=rel_id, x=x, y=y1 + 20, text_anchor="middle"))
        parts.append(self.label(basis, tag="text", cls="edge-basis halo", id=basis_id, x=x, y=y1 + 34, text_anchor="middle"))
        if kind == "gap":
            pill_id = self.new_id("t")
            parts[0] = parts[0].replace(f'aria-labelledby="{rel_id} {basis_id}"', f'aria-labelledby="{rel_id} {basis_id} {pill_id}"')
            parts.append(f'<rect class="pill" x="{x - 50}" y="{y1 + 44}" width="100" height="24" rx="12"/>')
            parts.append(self.label("gap: no edge", tag="text", cls="pill-text", id=pill_id, x=x, y=y1 + 60, text_anchor="middle"))
        parts.append("</a>")
        return "".join(parts)

    def supplier_pill(self, item: dict, x: int, y: int) -> str:
        edge_id = item["edge"]["id"]
        supplier = item["edge"]["supplier"]
        if not isinstance(supplier, dict):
            raise BuildError("named suppliers need a design before they are drawn")
        self.term("Unknown and unstated values", f"schema:entities#vocab_unresolved_state/{supplier['state']}")
        head_id, state_id = self.new_id("t"), self.new_id("t")
        return (
            f'<a class="mark supplier-gap" href="#ev-{esc(edge_id)}" data-mark="supplier-gap" data-target="{esc(edge_id)}" aria-labelledby="{head_id} {state_id}">'
            f'<rect class="pill" x="{x - 74}" y="{y}" width="148" height="40" rx="10"/>'
            + self.label("supplier (who makes it)", tag="text", cls="pill-head", id=head_id, x=x, y=y + 16, text_anchor="middle")
            + self.ref(edge_id, "/supplier/state", tag="text", fmt="state", cls="pill-text", id=state_id, x=x, y=y + 32, text_anchor="middle")
            + "</a>"
        )

    def figure(self, j: dict) -> str:
        width, col_w = 360, 160
        n = len(j["columns"])
        centres = [180] if n == 1 else [90, 270]
        lefts = [100] if n == 1 else [10, 190]
        out = []
        actor_y, product_y, component_y, tech_y = 12, 150, 340, 470
        for col, cx, left in zip(j["columns"], centres, lefts):
            if col["actor"]:
                actor = col["actor"]
                out.append(self.box(actor["edge"]["source_entity"], left, actor_y, col_w, 46))
                out.append(self.arrow(actor, cx, actor_y + 46, product_y))
                self.term("Relation types", f"schema:relationships#vocab_relation_type/{actor['edge']['relation_type']}")
            elif col["gap"]:
                gap = col["gap"]
                source, target = self.gap_ends(gap)
                out.append(self.box(source, left, actor_y, col_w, 46))
                relation = self.candidate(gap["candidate"])["relation_types"][0]
                if relation not in navigate.VOCAB:
                    raise BuildError(f"the drawn gap's type {relation!r} is not a relation type")
                vocab_ref = f"schema:relationships#vocab_relation_type/{relation}"
                self.term("Relation types", vocab_ref)
                # the label is the vocabulary term, so no candidate reference sits in the diagram (D-109)
                out.append(self.arrow({}, cx, actor_y + 46, product_y, relation_ref=(vocab_ref, "/const"), kind="gap", target=gap["claim"], ends=(source, target)))
            out.append(self.box(col["product"], left, product_y, col_w, 52))
            item = col["item"]
            out.append(self.arrow(item, cx, product_y + 52, component_y))
            out.append(self.supplier_pill(item, cx, product_y + 52 + 50))
        out.append(self.box(j["component"], 10, component_y, 340, 52))
        out.append(self.arrow(j["root"], 180, component_y + 52, tech_y))
        out.append(self.box(JOURNEY["walk_root"], 10, tech_y, 340, 52))
        for item in (j["root"], *[c["item"] for c in j["columns"]]):
            self.term("Relation types", f"schema:relationships#vocab_relation_type/{item['edge']['relation_type']}")
        lane_y = tech_y + 52 + 34
        lane = [f'<g class="lane" data-lane>']
        lane.append(f'<rect class="lane-box" x="2" y="{lane_y}" width="356" height="236" rx="8"/>')
        lane.append(self.label("also recorded in the Atlas", tag="text", cls="lane-head", x=14, y=lane_y + 22))
        lane.append(self.derived("lane-unlinked", self.label_text("not linked to any accelerator on this chain"), tag="text", cls="lane-note", x=14, y=lane_y + 38))
        for item in j["lane_edges"]:
            edge = item["edge"]
            lane.append(self.box(edge["source_entity"], 10, lane_y + 54, col_w, 46))
            lane.append(self.arrow(item, 90, lane_y + 100, lane_y + 172))
            lane.append(self.box(edge["target_entity"], 10, lane_y + 172, col_w, 46))
            self.term("Relation types", f"schema:relationships#vocab_relation_type/{edge['relation_type']}")
        for product in j["lane_products"]:
            lane.append(self.box(product, 190, lane_y + 54, col_w, 64))
            lane.append(self.label("recorded as a kind of", tag="text", cls="edge-basis", x=200, y=lane_y + 138))
            lane.append(self.name(self.homes[product]["instance_of"][0], tag="text", cls="lane-ref", x=200, y=lane_y + 154))
            lane.append(self.label("a property of its record,", tag="text", cls="edge-basis", x=200, y=lane_y + 170))
            lane.append(self.label("not a supply link", tag="text", cls="edge-basis", x=200, y=lane_y + 184))
        lane.append("</g>")
        height = lane_y + 236 + 4
        defs = (
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker></defs>'
        )
        title = self.label("The chain", tag="title", id="chain-title")
        desc = self.label("The chain in words", tag="desc", id="chain-desc")
        return (
            f'<svg class="chain" data-figure viewBox="0 0 {width} {height}" role="group" aria-labelledby="chain-title" aria-describedby="chain-words">'
            f"{title}{desc}{defs}{''.join(out)}{''.join(lane)}</svg>"
        )

    def legend(self) -> str:
        swatches = [
            ('<rect class="box" x="2" y="4" width="32" height="18" rx="4"/>', "named thing (instance level)", ""),
            ('<rect class="box" x="2" y="4" width="32" height="18" rx="4"/><rect class="class-rule" x="2" y="4" width="32" height="4" rx="2"/>', "vendor-neutral class (class level)", " class-level"),
            ('<line class="line" x1="2" y1="13" x2="30" y2="13" marker-end="url(#arrow)"/>', "stated: at least one cited claim is a FACT", ""),
            ('<line class="line" x1="2" y1="13" x2="30" y2="13" marker-end="url(#arrow)"/>', "inferred: every cited claim is a DERIVATION", " inferred"),
            ('<rect class="pill" x="2" y="4" width="32" height="18" rx="9"/>', "gap: an unknown value or a recorded gap, never a zero", " gap"),
            ('<line class="line" x1="2" y1="13" x2="34" y2="13"/>', "recorded gap: a claim the Atlas holds, not an edge", " gap"),
            ('<rect class="lane-box" x="2" y="4" width="32" height="18" rx="4"/>', "recorded in the Atlas, not linked to the chain", ""),
        ]
        items = []
        for shape, text, cls in swatches:
            items.append(f'<li><svg class="swatch{cls}" viewBox="0 0 36 26" aria-hidden="true" focusable="false">{shape}</svg>{self.label(text)}</li>')
        return '<ul class="legend">' + "".join(items) + "</ul>"

    def words(self, j: dict) -> str:
        """The text equivalent of the diagram, top to bottom, each item linked to its panel."""
        items = []

        def sentence(item: dict) -> str:
            edge = item["edge"]
            basis = self.basis(item)
            return f"{self.name(edge['source_entity'])} {self.ref(edge['id'], '/relation_type', cls='rel')} {self.name(edge['target_entity'])} · {self.label(basis, cls='basis ' + basis)}"

        for col in j["columns"]:
            if col["actor"]:
                items.append(f"<li>{sentence(col['actor'])} {self.evidence_link(col['actor']['edge']['id'])}</li>")
            if col["gap"]:
                gap = col["gap"]
                source, target = self.gap_ends(gap)
                basis = self.claim_basis(gap["claim"])
                items.append(
                    f'<li>{self.name(source)} → {self.name(target)}: {self.ref(gap["candidate"], "/relation_types/0", cls="rel")} · '
                    f'{self.label("recorded gap: a claim the Atlas holds, not an edge", cls="basis gap")} · {self.label(basis, cls="basis " + basis)} {self.evidence_link(gap["claim"])}</li>'
                )
        for col in j["columns"]:
            item = col["item"]
            items.append(
                f"<li>{sentence(item)} · {self.label('supplier (who makes this part)')}: "
                f"{self.ref(item['edge']['id'], '/supplier/state', fmt='state', cls='basis gap')} {self.evidence_link(item['edge']['id'])}</li>"
            )
        items.append(f"<li>{sentence(j['root'])} {self.evidence_link(j['root']['edge']['id'])}</li>")
        lane = [f"<li>{sentence(item)} {self.evidence_link(item['edge']['id'])}</li>" for item in j["lane_edges"]]
        for product in j["lane_products"]:
            lane.append(
                f"<li>{self.name(product)}: {self.label('recorded as a kind of')} {self.name(self.homes[product]['instance_of'][0])} · "
                f"{self.label('a property of its record, not a supply link')} {self.evidence_link(product)}</li>"
            )
        return (
            f'<div id="chain-words"><ol class="words">{"".join(items)}</ol>'
            f'<p class="lane-words">{self.label("also recorded in the Atlas")} · '
            f'{self.derived("lane-unlinked", self.label_text("not linked to any accelerator on this chain"))}</p>'
            f'<ul class="words">{"".join(lane)}</ul></div>'
        )

    # --- the sections (vertical-slice.md §4) -----------------------------------------------------

    def lede(self, j: dict) -> str:
        """One sentence composed from the records: the products, their shared part, what it requires and
        who makes it. Omitted when the products do not share one relation type or one supplier state."""
        edges = [c["item"]["edge"] for c in j["columns"]]
        if len({e["relation_type"] for e in edges}) != 1 or not all(isinstance(e.get("supplier"), dict) for e in edges):
            return ""
        products = f" {self.label('and')} ".join(self.name(e["source_entity"]) for e in edges)
        each = f" {self.label('each')}" if len(edges) > 1 else ""
        first, root = j["columns"][0]["item"], j["root"]
        stated = all(self.basis(c["item"]) == "stated" for c in j["columns"])
        sentence = (
            f"{products}{each} {self.ref(edges[0]['id'], '/relation_type', cls='rel')} {self.name(edges[0]['target_entity'])} "
            f"({self.label('stated' if stated else 'inferred', cls='basis ' + ('stated' if stated else 'inferred'))}), "
            f"{self.label('which')} {self.ref(root['edge']['id'], '/relation_type', cls='rel')} {self.name(root['edge']['target_entity'])} "
            f"({self.label(self.basis(root), cls='basis ' + self.basis(root))})."
        )
        if len({e["supplier"]["state"] for e in edges}) == 1:
            sentence += (
                f" {self.label('Who makes that memory:')} {self.ref(edges[0]['id'], '/supplier/state', fmt='state', cls='basis gap')}"
                + (f" {self.label('in each')}" if len(edges) > 1 else "") + "."
            )
        return f'<p class="lede">{sentence}</p>'

    def short_answer(self, j: dict) -> str:
        items = []
        for col in j["columns"]:
            edge = col["item"]["edge"]
            items.append(
                f"<li>{self.name(edge['source_entity'])} {self.ref(edge['id'], '/relation_type', cls='rel')} {self.name(edge['target_entity'])} · "
                f"{self.label(self.basis(col['item']), cls='basis ' + self.basis(col['item']))} {self.evidence_link(edge['id'])}</li>"
            )
        root = j["root"]
        items.append(
            f"<li>{self.name(root['edge']['source_entity'])} {self.ref(root['edge']['id'], '/relation_type', cls='rel')} {self.name(root['edge']['target_entity'])} · "
            f"{self.label(self.basis(root), cls='basis ' + self.basis(root))} {self.evidence_link(root['edge']['id'])}</li>"
        )
        for col in j["columns"]:
            edge = col["item"]["edge"]
            items.append(
                f"<li>{self.name(edge['source_entity'])} → {self.name(edge['target_entity'])} · {self.label('supplier (who makes this part)')}: "
                f"{self.ref(edge['id'], '/supplier/state', fmt='state', cls='basis gap')} {self.evidence_link(edge['id'])}</li>"
            )
        for col in j["columns"]:
            if col["actor"]:
                edge = col["actor"]["edge"]
                items.append(
                    f"<li>{self.name(edge['source_entity'])} {self.ref(edge['id'], '/relation_type', cls='rel')} {self.name(edge['target_entity'])} · "
                    f"{self.label(self.basis(col['actor']), cls='basis ' + self.basis(col['actor']))} {self.evidence_link(edge['id'])}</li>"
                )
        return self.lede(j) + '<ul class="answer">' + "".join(items) + "</ul>"

    def context(self, j: dict) -> str:
        states = []
        for col in j["columns"]:
            edge = col["item"]["edge"]
            for claim_id in edge["claim_ids"]:
                states.append(
                    f'<li>{self.name(edge["source_entity"], cls="who")} {self.ref(claim_id, "/claim_type", cls="type-tag")} '
                    f'{self.ref(claim_id, "/statement", tag="q")} {self.evidence_link(edge["id"])}</li>'
                )
        definitions = []
        for record_id in (j["component"], JOURNEY["walk_root"]):
            record = self.homes[record_id]
            for index, definition in enumerate(record.get("definition", [])):
                claim_id = definition["claim_ids"][0]
                definitions.append(
                    f'<div class="def"><dt>{self.name(record_id)}</dt><dd>{self.ref(record_id, f"/definition/{index}/value")} '
                    f'<span class="cite">{self.label("working definition")} · {self.ref(record_id, f"/definition/{index}/claim_ids/0", tag="code")} · '
                    f'{self.ref(claim_id, "/claim_type", cls="type-tag")}</span> {self.evidence_link(record_id)}</dd></div>'
                )
        quotes = f'{self.label("What each maker states about the memory", tag="h3")}<ul class="quotes">{"".join(states)}</ul>'
        return quotes, f'{self.label("Definitions the Atlas uses", tag="h3")}<dl class="defs">{"".join(definitions)}</dl>'

    def gaps(self, j: dict) -> str:
        unknown = []
        states = set()
        for col in j["columns"]:
            edge = col["item"]["edge"]
            states.add(edge["supplier"]["state"])
            unknown.append(
                f"<li>{self.name(edge['source_entity'])} → {self.name(edge['target_entity'])} · {self.label('supplier (who makes this part)')}: "
                f"{self.ref(edge['id'], '/supplier/state', fmt='state', cls='basis gap')} {self.evidence_link(edge['id'])}</li>"
            )
        meaning = "".join(
            f'<p class="meaning">{self.ref(f"schema:entities#vocab_unresolved_state/{s}", "/const", fmt="state", tag="strong")}: '
            f'{self.ref(f"schema:entities#vocab_unresolved_state/{s}", "/description")}</p>'
            for s in sorted(states)
        )
        ruling = self.decision("D-094")
        drawn = []
        for gap in JOURNEY["drawn_gaps"]:
            cand_id = gap["candidate"]
            source, target = self.gap_ends(gap)
            drawn.append(
                f'<li><strong>{self.name(source)} → {self.name(target)}</strong> · {self.ref(cand_id, "/relation_types/0", cls="rel")} · '
                f'{self.label("a claim the Atlas holds, not an edge", cls="basis gap")} {self.evidence_link(gap["claim"])}<br>'
                f'{self.ref(cand_id, "/reasoning")}<br>{self.label("ruling")}: {self.decision(self.candidate(cand_id)["ruling"])}</li>'
            )
        table = (
            f'<p class="cite">{self.label("the rule that refuses candidates:")} '
            f'<a href="{TO_ROOT}docs/architecture/edge-dataset.md">{self.label("edge design record")}</a></p>{self.candidate_cards(j)}'
        )
        none_recorded = []
        for col in j["columns"]:
            if not self.atlas.actors_list(col["product"]):
                none_recorded.append(
                    f'<li>{self.name(col["product"])} · {self.label("activity edges into this record:")} '
                    f'{self.derived("no-activity-edge", self.label_text("no recorded relationship"), data_target=col["product"])}</li>'
                )
        return (
            f'{self.label("Unknown values", tag="h3")}<ul class="gaps">{"".join(unknown)}</ul>{meaning}<p class="meaning">{self.label("ruling")}: {ruling}</p>'
            f'{self.label("Recorded gaps", tag="h3")}<ul class="gaps">{"".join(drawn)}</ul>'
            f'{self.label("Candidates that are not edges", tag="h3")}{table}'
            f'{self.label("No recorded relationship", tag="h3")}<ul class="gaps">{"".join(none_recorded)}</ul>'
        )

    def endpoint(self, cand_id: str, pointer: str, value, panels: set[str]) -> str:
        """A candidate's party or item: a record's name (linked to its panel where the page has one),
        or the name the candidate records for a party with no record (D-109)."""
        if isinstance(value, str):
            name = self.name(value)
            return f'<a href="#ev-{esc(value)}">{name}</a>' if value in panels else name
        return f'{self.ref(cand_id, f"{pointer}/name")} <span class="cite">({self.label("no record in the Atlas")})</span>'

    def candidate_cards(self, j: dict) -> str:
        """The journey's refused candidates as cards, one group per reason, in the schema's order (D-109)."""
        panels = set(self.panel_nodes(j))
        cards = {cand_id: self.candidate(cand_id) for cand_id in JOURNEY["candidates"]}
        groups = []
        for reason in [item["const"] for item in self.schemas["refused_candidates"]["$defs"]["vocab_reason"]["oneOf"]]:
            members = [cid for cid, c in cards.items() if reason in c["reasons"]]
            if not members:
                continue
            vocab_ref = f"schema:refused_candidates#vocab_reason/{reason}"
            items = []
            for cid in members:
                cand = cards[cid]
                sources = ", ".join(self.endpoint(cid, f"/source_entities/{i}", v, panels) for i, v in enumerate(cand["source_entities"]))
                targets = ", ".join(self.endpoint(cid, f"/target_entities/{i}", v, panels) for i, v in enumerate(cand["target_entities"]))
                types = ", ".join(self.ref(cid, f"/relation_types/{i}", cls="rel") for i in range(len(cand["relation_types"])))
                for relation in cand["relation_types"]:
                    self.term("Relation types", f"schema:relationships#vocab_relation_type/{relation}")
                item = f' · {self.label("item")}: {self.endpoint(cid, "/item", cand["item"], panels)}' if "item" in cand else ""
                items.append(
                    f'<li class="card" data-candidate="{esc(cid)}"><p class="card-head">{sources} → {targets} · {types}{item}</p>'
                    f'<p>{self.ref(cid, "/reasoning")}</p><p class="cite">{self.label("ruling")}: {self.decision(cand["ruling"])}</p></li>'
                )
            groups.append(
                f'<section class="reason" data-reason="{esc(reason)}"><h4>{self.ref(vocab_ref, "/const", fmt="state")}</h4>'
                f'<p class="meaning">{self.ref(vocab_ref, "/description")}</p><ul class="cards">{"".join(items)}</ul></section>'
            )
        return "".join(groups)

    def rules_cited(self) -> str:
        """Each rule code quoted from the design record, with its one-line home (D-108)."""
        texts = [self.candidate(g["candidate"])["reasoning"] for g in JOURNEY["drawn_gaps"]]
        texts += [self.candidate(cand_id)["reasoning"] for cand_id in JOURNEY["candidates"]]
        codes = sorted({c for text in texts for c in RULE_CODE.findall(text)}, key=lambda c: (c.split("-")[0], int(c.split("-")[1])))
        items = []
        for code in codes:
            if code.startswith("D-"):
                items.append(f"<div><dt>{self.decision(code)}</dt></div>")
                continue
            if code not in self.rules:
                raise BuildError(f"rule {code} has no one-line home")
            home = RULE_HOMES[code.split("-")[0]]
            items.append(
                f'<div><dt>{self.ref(f"doc:rules#{code}", "code", tag="strong")}</dt><dd>{self.ref(f"doc:rules#{code}", "rule")} '
                f'<span class="cite">{self.label("defined in")} <a href="{TO_ROOT}{home}">{self.derived("rule-home", home, tag="code", data_target=code)}</a></span></dd></div>'
            )
        return f'{self.label("Rules cited above", tag="h3")}<dl class="terms rules">{"".join(items)}</dl>'

    def decision(self, key: str) -> str:
        if key not in self.decisions:
            raise BuildError(f"no decision {key}")
        return f'{self.ref(f"doc:decisions#{key}", "id", tag="strong")} {self.ref(f"doc:decisions#{key}", "title")}'

    # --- evidence panels (vertical-slice.md §6) --------------------------------------------------

    def claim_card(self, claim_id: str, panel: str, shown: set[str]) -> str:
        claim = self.store.claims[claim_id]
        if self.store.where[claim_id] != "canonical":
            raise BuildError(f"{claim_id} is a staging claim")
        anchor = f"cl-{panel}--{claim_id}"  # a claim card inside a panel; panels alone are "ev-"
        if claim_id in shown:
            return f'<p class="shown">{self.label("shown above")}: <a href="#{esc(anchor)}">{self.ref(claim_id, "/id", tag="code")}</a></p>'
        shown.add(claim_id)
        self.claims_shown.add(claim_id)
        self.term("Claim types", f"schema:claims#vocab_claim_type/{claim['claim_type']}")
        self.term("Evidence status", f"schema:claims#vocab_evidence_status/{claim['evidence_status']}")
        c = lambda field, **kw: self.ref(claim_id, field, **kw)  # noqa: E731
        out = [f'<div class="claim" id="{esc(anchor)}">']
        out.append(
            f'<p class="statement">{c("/claim_type", cls="type-tag type-" + claim["claim_type"].lower())} '
            f'{c("/evidence_status", cls="status")} {c("/statement")}</p>'
        )
        if "as_of" in claim:
            if isinstance(claim["as_of"], dict):
                self.term("Unknown and unstated values", "schema:claims#state_not_stated")
                out.append(f'<p class="meta">{self.label("as of", cls="k")} {c("/as_of/state", fmt="state")}</p>')
            else:
                out.append(f'<p class="meta">{self.label("as of", cls="k")} {c("/as_of")}</p>')
        if claim.get("citations"):
            out.append('<ol class="citations">')
            for index, citation in enumerate(claim["citations"]):
                out.append(self.citation(claim_id, index, citation))
            out.append("</ol>")
        if "reasoning" in claim:
            out.append(f'<p class="reasoning">{self.label("reasoning", cls="k")} {c("/reasoning")}</p>')
        if "search" in claim:
            out.append(f'<p class="meta">{self.label("search", cls="k")} {c("/search/question")} · {c("/search/conclusion", fmt="state")}</p>')
            for index, entry in enumerate(claim["search"]["classes"]):
                out.append(f'<p class="meta">{c(f"/search/classes/{index}/source_class")} · {self.label("outcome")} {c(f"/search/classes/{index}/outcome", fmt="state")}</p>')
        for index, _ in enumerate(claim.get("disputed_with", [])):
            out.append(f'<p class="meta">{self.label("disputed with", cls="k")} {c(f"/disputed_with/{index}", tag="code")}</p>')
        review = claim["review"]
        record = f'{self.label("claim", cls="k")} {c("/id", tag="code")} · {self.label("verified")} {c("/verified_on")}'
        if "verdict" in review:
            record += (
                f' · {self.label("review:")} {c("/review/verdict")} {self.label("by the")} {c("/review/reviewer")} '
                f'{self.label("on")} {c("/review/reviewed_on")} · {self.label("recorded in")} '
                f'{self.ref(claim_id, "/review/recorded_in", tag="a", href=TO_ROOT + review["recorded_in"])}'
            )
        out.append(f'<p class="meta claim-record">{record}</p>')
        inputs = claim.get("input_claim_ids", [])
        if inputs:
            cards = "".join(self.claim_card(input_id, panel, shown) for input_id in inputs)
            out.append(f'<details class="inputs"><summary>{self.label("inputs to this inference")}</summary>{cards}</details>')
        out.append("</div>")
        return "".join(out)

    def citation(self, claim_id: str, index: int, citation: dict) -> str:
        source_id = citation["source_id"]
        source = self.store.sources[source_id]
        self.sources_shown.add(source_id)
        self.term("Source classes", f"schema:sources#vocab_source_class/{source['source_class']}")
        self.term("Standing", f"schema:claims#vocab_standing/{citation['standing']}")
        s = lambda field, **kw: self.ref(source_id, field, **kw)  # noqa: E731
        k = lambda field, **kw: self.ref(claim_id, f"/citations/{index}/{field}", **kw)  # noqa: E731
        if isinstance(source["stated_dates"], dict):
            self.term("Unknown and unstated values", "schema:sources#state_undated")
            dates = s("/stated_dates/state", fmt="state")
        else:
            dates = "; ".join(f'{s(f"/stated_dates/{i}/kind")} {s(f"/stated_dates/{i}/date")}' for i in range(len(source["stated_dates"])))
        out = [
            f'<li class="citation"><blockquote class="anchor">{k("anchor")}</blockquote>',
            f'<p class="src">{self.label("source", cls="k")} {s("/title", tag="cite")} · {s("/publisher")}</p>',
            f'<p class="meta">{self.label("locator", cls="k")} {k("locator")}</p>',
            f'<p class="meta">{s("/source_class", cls="tag")} · {self.label("standing")} {k("standing", cls="tag")} · '
            f'{self.label("stated dates")} {dates} · {self.label("accessed")} {s("/retrieval/accessed_at")}</p>',
            f'<p class="meta url">{self.label("URL", cls="k")} {s("/url", tag="a", href=source["url"], rel="noopener noreferrer")}</p>',
        ]
        if "originator" in citation:
            out.append(f'<p class="meta">{self.label("originator", cls="k")} {k("originator/name")} · {k("originator/source_class", cls="tag")}</p>')
        if "read" in citation:
            registered = source["retrieval"]["sha256"]
            same = citation["read"]["sha256"].startswith(registered) or registered.startswith(citation["read"]["sha256"])
            note = "same bytes as registered" if same else "bytes changed since registration"
            out.append(
                f'<p class="meta">{self.label("read by the Verifier", cls="k")} {k("read/accessed_at")} · '
                f'{self.derived("bytes-match", self.label_text(note), data_target=claim_id, data_index=str(index))}</p>'
            )
        out.append("</li>")
        return "".join(out)

    def panel(self, record_id: str, heading: str, details: list[tuple[str, str]], intro: str = "") -> str:
        data, status = trace.trace_data(record_id, self.store)
        if status != 0:
            raise BuildError(f"the trace of {record_id} has missing references: {data.get('missing')}")
        shown: set[str] = set()
        out = [f'<article class="panel" id="ev-{esc(record_id)}"><h3>{heading}</h3>']
        if details:
            out.append('<dl class="facts">' + "".join(f"<div><dt>{self.label(k)}</dt><dd>{v}</dd></div>" for k, v in details) + "</dl>")
        out.append(intro)
        if data["kind"] == "claim":
            out.append(self.claim_card(record_id, record_id, shown))
        else:
            def cited(path: dict) -> str:
                return (
                    f'<p class="cited-at">{self.label("cited at")} '
                    f'{self.derived("pointer", path["pointer"], tag="code", data_target=record_id, data_claim=path["claim_id"])}</p>'
                    + self.claim_card(path["claim_id"], record_id, shown)
                )

            context = [p for p in data["paths"] if p["pointer"].split("/")[1] in CONTEXT_FIELDS]
            out += [cited(p) for p in data["paths"] if p not in context]
            if context:
                rest = "".join(cited(p) for p in context)
                out.append(f'<details class="inputs"><summary>{self.label("other claims in this record’s trace")}</summary>{rest}</details>')
        out.append(f'<p class="back"><a href="#chain">{self.label("back to the diagram")}</a></p></article>')
        return "".join(out)

    def edge_panel(self, item: dict) -> str:
        edge = item["edge"]
        edge_id = edge["id"]
        heading = f"{self.name(edge['source_entity'])} {self.ref(edge_id, '/relation_type', cls='rel')} {self.name(edge['target_entity'])}"
        details = [("ID", self.ref(edge_id, "/id", tag="code")), ("level", self.ref(f"schema:relationships#vocab_relation_type/{edge['relation_type']}", "/x-level"))]
        if item["level"] == "instance":
            if item["period"]:
                details.append(("period", " – ".join(self.ref(edge_id, f"/{k}") for k in ("valid_from", "valid_to") if k in edge)))
            else:
                details.append(("period", self.absent(edge_id, "/valid_from", "no period in the claims")))
        if isinstance(edge.get("supplier"), dict):
            details.append(("supplier", self.ref(edge_id, "/supplier/state", fmt="state", cls="basis gap")))
        basis = self.basis(item)
        details.append(("basis", self.label(basis, cls="basis " + basis)))
        return self.panel(edge_id, heading, details)

    def node_panel(self, record_id: str) -> str:
        record = self.homes[record_id]
        details = [("ID", self.ref(record_id, "/id", tag="code")), ("type", self.ref(record_id, "/type"))]
        if "vendor" in record:
            details.append(("vendor", f'{self.ref(record_id, "/vendor", tag="code")} · {self.name(record["vendor"])}'))
        for key, word in (("instance_of", "instance of"), ("broader", "broader")):
            for index, target in enumerate(record.get(key, [])):
                details.append((word, f'{self.ref(record_id, f"/{key}/{index}", tag="code")} · {self.name(target)}'))
        return self.panel(record_id, self.name(record_id), details)

    def gap_panel(self, gap: dict) -> str:
        cand_id = gap["candidate"]
        source, target = self.gap_ends(gap)
        heading = f'{self.name(source)} → {self.name(target)} · {self.label("recorded gap")}'
        details = [("type", self.ref(cand_id, "/relation_types/0")), ("why not", self.ref(cand_id, "/reasoning")), ("ruling", self.decision(self.candidate(cand_id)["ruling"]))]
        return self.panel(gap["claim"], heading, details)

    def panel_nodes(self, j: dict) -> list[str]:
        """The records that get a node panel, in panel order."""
        nodes: list[str] = []
        for col in j["columns"]:
            if col["actor"]:
                nodes.append(col["actor"]["edge"]["source_entity"])
            if col["gap"]:
                nodes.append(self.gap_ends(col["gap"])[0])
        nodes += [c["product"] for c in j["columns"]] + [j["component"], JOURNEY["walk_root"]]
        for item in j["lane_edges"]:
            nodes += [item["edge"]["source_entity"], item["edge"]["target_entity"]]
        nodes += j["lane_products"]
        return list(dict.fromkeys(nodes))

    def evidence(self, j: dict) -> str:
        panels = []
        for col in j["columns"]:
            if col["actor"]:
                panels.append(self.edge_panel(col["actor"]))
            if col["gap"]:
                panels.append(self.gap_panel(col["gap"]))
        for col in j["columns"]:
            panels.append(self.edge_panel(col["item"]))
        panels.append(self.edge_panel(j["root"]))
        for item in j["lane_edges"]:
            panels.append(self.edge_panel(item))
        for record_id in self.panel_nodes(j):
            panels.append(self.node_panel(record_id))
        return "".join(panels)

    # --- the chain as a table (S14) --------------------------------------------------------------

    def sql_cell(self, row: int, column: str, value, item: int | None = None, fmt: str | None = None, tag: str = "span", cls: str | None = None) -> str:
        """One value of the committed SQL result; tests/test_page.py PG-11 compares it with the result."""
        text = str(value).replace("_", " ") if fmt == "state" else str(value)
        extra = {"data_query": SQL_QUERY, "data_row": str(row), "data_column": column, "data_item": None if item is None else str(item), "data_format": fmt}
        return self.derived("sql-cell", text, tag=tag, cls=cls, **{k: v for k, v in extra.items() if v is not None})

    def sql_list(self, row: int, column: str, values: list, tag: str = "code", sep: str = ", ") -> str:
        return sep.join(self.sql_cell(row, column, v, item=i, tag=tag) for i, v in enumerate(values))

    def sql_section(self) -> str:
        query = REPO_ROOT / "sql" / f"{SQL_QUERY}.sql"
        result = json.loads((REPO_ROOT / "sql" / "results" / f"{SQL_QUERY}.json").read_text(encoding="utf-8"))
        if result["query_sha256"] != hashlib.sha256(query.read_bytes()).hexdigest():
            raise BuildError(f"sql/results/{SQL_QUERY}.json was computed from another version of its query (python tools/warehouse.py)")
        heads = ("Accelerator", "Link", "How the Atlas knows", "Evidence dated", "Published by", "Caveats", "Traced to")
        k = {h: self.label(h, cls="cell-k") for h in heads}
        body = []
        for i, r in enumerate(result["rows"]):
            state_end = r["from_id"] not in self.homes
            if r["relation"] not in self.atlas_relation_types():
                # a field of an edge (the supplier of a part): the part, then the field and its value or state
                link = (
                    f'{self.sql_cell(i, "to_name", r["to_name"])} · {self.sql_cell(i, "relation", r["relation"], cls="rel")}: '
                    f'{self.sql_cell(i, "from_name", r["from_name"], fmt="state" if state_end else None)}'
                )
            else:
                link = f'{self.sql_cell(i, "from_name", r["from_name"])} {self.sql_cell(i, "relation", r["relation"], cls="rel")} {self.sql_cell(i, "to_name", r["to_name"])}'
            basis = self.sql_cell(i, "basis", r["basis"], cls=f'basis {r["basis"]}')
            if r["basis"] == "gap":
                basis += f' · {self.sql_cell(i, "gap_reason", r["gap_reason"], fmt="state")}'
            dated = self.sql_cell(i, "evidence_dated_from", r["evidence_dated_from"], fmt="state" if r["evidence_dated_from"] == "not_applicable" else None)
            if r["evidence_dated_to"] != r["evidence_dated_from"]:
                dated += f' {self.label("to")} {self.sql_cell(i, "evidence_dated_to", r["evidence_dated_to"])}'
            published = self.sql_list(i, "publishers", r["publishers"], tag="span", sep="; ") if r["publishers"] else self.label("no source cited")
            caveats = []
            if r["rests_on_atlas_interpretation"]:
                caveats.append(self.derived("sql-flag", SQL_FLAGS["rests_on_atlas_interpretation"], data_row=str(i), data_column="rests_on_atlas_interpretation"))
            if len(r["publishers"]) == 1:
                caveats.append(self.derived("sql-flag", SQL_FLAGS["publishers"], data_row=str(i), data_column="publishers"))
            if r["party_standing_unchecked"]:
                caveats.append(f'{self.label("publisher not linked to a company record:")} {self.sql_list(i, "party_standing_unchecked", r["party_standing_unchecked"])}')
            ids = (
                f'<p>{self.label("edge or candidate:")} {self.sql_cell(i, "record_id", r["record_id"], tag="code")}</p>'
                f'<p>{self.label("reached through:")} {self.sql_cell(i, "reached_through", r["reached_through"], tag="code")}</p>'
                f'<p>{self.label("why it counts as an accelerator:")} {self.sql_cell(i, "accelerator_class_claim", r["accelerator_class_claim"], tag="code")}</p>'
                + (f'<p>{self.label("claims:")} {self.sql_list(i, "claim_ids", r["claim_ids"])}</p>' if r["claim_ids"] else "")
                + (f'<p>{self.label("sources:")} {self.sql_list(i, "source_ids", r["source_ids"])}</p>' if r["source_ids"] else "")
            )
            cells = (
                self.sql_cell(i, "accelerator", r["accelerator"], cls="who"), link, basis, dated, published,
                "<br>".join(f"<span>{c}</span>" for c in caveats),
                f'<details class="ids"><summary>{self.label("IDs")}</summary>{ids}</details>',
            )
            empty = ' class="empty"'  # a cell with nothing to show, hidden at phone width
            body.append("<tr>" + "".join(f"<td{'' if c else empty}>{k[h]}{c}</td>" for h, c in zip(heads, cells)) + "</tr>")
        head = "".join(f'<th scope="col">{self.label(h)}</th>' for h in heads)
        t = sql_tutorial(query.read_text(encoding="utf-8"))
        steps = "".join(
            f'<li>{self.derived("sql-step-title", s["title"], tag="h4")}{self.derived("sql-step-text", s["explanation"], tag="p")}'
            f'<pre><code data-derived="sql-step-code">{esc(s["code"])}</code></pre></li>'
            for s in t["steps"]
        )
        tutorial = (
            f'<details class="sql-tutorial"><summary>{self.label("How this was computed")}</summary><div class="tutorial">'
            f'{self.label("The question", tag="h3")}{self.derived("sql-question", t["header"]["question"], tag="p")}'
            f'{self.label("The query, step by step", tag="h3")}<ol class="steps">{steps}</ol>'
            f'{self.label("How to read the result", tag="h3")}{self.derived("sql-reading", t["header"]["reading"], tag="p")}'
            f'<p class="meta">{self.label("query file", cls="k")} {self.derived("sql-file", f"sql/{SQL_QUERY}.sql", tag="code")} · '
            f'{self.label("result file", cls="k")} {self.derived("sql-file", f"sql/results/{SQL_QUERY}.json", tag="code")} · '
            f'{self.label("input digest", cls="k")} {self.derived("sql-digest", result["input_digest"], tag="code", cls="digest")}</p>'
            f'<pre><code>{self.label("check the result:")}\n{self.label("python tools/warehouse.py --check")}</code></pre>'
            "</div></details>"
        )
        return f'<div class="table-wrap"><table class="sql"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>{tutorial}'

    def atlas_relation_types(self) -> set[str]:
        return {c["const"] for c in self.schemas["relationships"]["$defs"]["vocab_relation_type"]["oneOf"]}

    # --- method and terms ------------------------------------------------------------------------

    def method(self) -> str:
        paths = input_paths()
        files = "".join(f'<li><a href="{TO_ROOT}{esc(p)}">{self.derived("input-file", p, tag="code")}</a></li>' for p in paths)
        verified = sorted(self.store.claims[c]["verified_on"] for c in self.claims_shown)
        accessed = sorted(self.store.sources[s]["retrieval"]["accessed_at"] for s in self.sources_shown)
        rulings = "".join(f"<li>{self.decision(key)}</li>" for key in JOURNEY["decisions"])
        root = JOURNEY["walk_root"]
        first_edge = self.atlas.depends_on_tree(root)[0]["edge"]["id"]
        return (
            f'{self.label("Built from", tag="h3")}'
            f'<p>{self.label("input digest", cls="k")} {self.derived("input-digest", input_digest(paths), tag="code", cls="digest")}</p>'
            f'<details class="inputs"><summary>{self.label("input files")}</summary><ul class="files">{files}</ul></details>'
            f'{self.label("Dates", tag="h3")}'
            f'<p>{self.label("claims on this page verified from")} {self.derived("verified-first", verified[0])} {self.label("to")} {self.derived("verified-last", verified[-1])}.</p>'
            f'<p>{self.label("sources accessed from")} {self.derived("accessed-first", accessed[0])} {self.label("to")} {self.derived("accessed-last", accessed[-1])}.</p>'
            f'{self.label("Rulings this page depends on", tag="h3")}<ul class="rulings">{rulings}</ul>'
            f'{self.label("Reproduce", tag="h3")}'
            f'<pre><code>{self.label("the walk:")}\n{self.label("python tools/navigate.py depends-on")} {self.ref(root, "/id")}\n'
            f'{self.label("the evidence for one edge:")}\n{self.label("python tools/trace.py")} {self.ref(first_edge, "/id")}\n'
            f'{self.label("rebuild and compare:")}\n{self.label("python tools/build_page.py --check")}</code></pre>'
        )

    def glossary(self) -> str:
        groups = []
        for group in TERM_GROUPS:
            refs = sorted(self.terms.get(group, ()))
            if not refs:
                continue
            items = []
            for ref in refs:
                field = "/const" if "/" in ref.partition("#")[2] else "/properties/state/const"
                items.append(f'<div><dt>{self.ref(ref, field, tag="code", fmt="state")}</dt><dd>{self.ref(ref, "/description")}</dd></div>')
            groups.append(f'{self.label(group, tag="h3")}<dl class="terms">{"".join(items)}</dl>')
        return "".join(groups)

    # --- the page --------------------------------------------------------------------------------

    def render(self) -> str:
        j = self.journey()
        for gap in JOURNEY["drawn_gaps"]:
            cand = self.candidate(gap["candidate"])
            if gap["claim"] not in self.homes or cand["ruling"] not in self.decisions:
                raise BuildError(f"the drawn gap {gap['candidate']} has no canonical claim or ruling")
            if gap["claim"] not in [c.get("claim_id") for c in cand["considered"]]:
                raise BuildError(f"the drawn gap's claim {gap['claim']} is not one its candidate considered")
        for cand_id in JOURNEY["candidates"]:
            self.candidate(cand_id)
        figure = self.figure(j)
        quotes, definitions = self.context(j)
        parts = {
            "question": f'{self.label("What does an")} {self.name("component-ai-accelerator")}{self.label("’s memory depend on, and who is known to make it?")}',
            "short_answer": self.short_answer(j),
            "figure": figure,
            "legend": self.legend(),
            "words": self.words(j),
            "context_quotes": quotes,
            "context_definitions": definitions,
            "gaps": self.gaps(j),
            "rules": self.rules_cited(),
            "evidence": self.evidence(j),
            "sql_table": self.sql_section(),
        }
        parts["method"] = self.method()  # after the panels: its date ranges cover the claims they show
        parts["terms"] = self.glossary()
        parts["palette"] = " ".join(f"--{k}: {v};" for k, v in PALETTE.items())
        parts["title"] = esc(html.unescape(re.sub(r"<[^>]+>", "", parts["question"])))
        # substitute() fails on a slot with no value; values are not re-read, so a "$" in a record is safe
        return string.Template(TEMPLATE.read_text(encoding="utf-8")).substitute(parts)


def build(data: Path = DATA) -> bytes:
    return Page(data).render().encode("utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the S11 vertical-slice page from the Atlas's records.")
    parser.add_argument("--check", action="store_true", help="rebuild in memory and compare with the committed page")
    args = parser.parse_args(argv[1:])
    try:
        page = build()
    except BuildError as error:
        print(f"build refused: {error}")
        return 1
    if args.check:
        same = PAGE.exists() and PAGE.read_bytes() == page
        print("page: up to date" if same else f"page: differs from a rebuild ({PAGE.relative_to(REPO_ROOT)}); run python tools/build_page.py")
        return 0 if same else 1
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_bytes(page)
    print(f"wrote {PAGE.relative_to(REPO_ROOT)} ({len(page)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
