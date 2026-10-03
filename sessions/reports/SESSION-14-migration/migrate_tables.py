"""S14 DT-1 migration: four document tables of per-record values become data rows (D-110, D-117).

Run once, from the repository root, on the S14 base (the documents still holding their tables):

    python sessions/reports/SESSION-14-migration/migrate_tables.py

What it does, in order, stopping at the first failed assertion:

1. reads the four tables with the parsers the checks used before S14 (copied below unchanged in
   logic from tests/test_data_entities.py at main @ cc99f57): concept-dataset.md §3 (CI-1) and §7
   (PI-1, IO-1), facility-dataset.md §2 (FI-1) and §4 (FK-1);
2. writes the rows to data/identity_basis.json (one row per table row; a product's row becomes a
   product_term row and an instance_of_basis row) and an empty data/staging/identity_basis.json;
3. reads the JSON back with the post-S14 loaders in tests/test_data_entities.py and asserts that
   they return exactly the tuples the Markdown parsers returned (nothing gained, nothing lost);
4. only then rewrites the documents: each table of rows is replaced by a pointer to its rows, the
   rule text stays; the two tables that restated record values (company-dataset.md §2's legal
   entities, concept-dataset.md §5's broader values) lose the restated column and keep their
   rulings and reasons.

No value is typed by hand: every row comes from a parsed cell. Standard library only (D-003). Kept
with the session report (DT-8).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tests"))

from test_entity_taxonomy import CONCEPT, cells, section  # noqa: E402

CONCEPTS_MD = REPO / "docs/architecture/concept-dataset.md"
FACILITIES_MD = REPO / "docs/architecture/facility-dataset.md"
COMPANIES_MD = REPO / "docs/architecture/company-dataset.md"
OUT = REPO / "data/identity_basis.json"
OUT_STAGING = REPO / "data/staging/identity_basis.json"
POINTER = "S14, DT-1, D-117"


# --- 1. the pre-S14 parsers ----------------------------------------------------------------------


def old_concept_table(text):
    body = section(text, "\n## 3. ", "\n## 4. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 4 and re.fullmatch(CONCEPT, row[0]):
            ids = re.findall(r"`([^`]+)`", row[2])
            rows.append((row[0], row[1], ids[0] if ids else None, row[3]))
    assert rows
    return rows


def old_product_table(text):
    body = section(text, "\n## 7. ", "\n## 8. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 4 and re.fullmatch(r"`product-[a-z0-9-]+`", row[0]):
            rows.append((row[0].strip("`"), row[1], row[2].strip("`"), row[3].strip("`")))
    assert rows
    return rows


def old_facility_terms(text):
    body = section(text, "\n## 2. ", "\n## 3. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 4 and re.fullmatch(r"`facility-[a-z0-9-]+`", row[0]):
            assert row[2] in ("site name", "locality")
            rows.append((row[0].strip("`"), row[1], row[2], row[3]))  # the note cell kept for the row
    assert rows
    return rows


def old_kind_basis(text):
    body = section(text, "\n## 4. ", "\n## 5. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 4 and re.fullmatch(r"`facility-[a-z0-9-]+`", row[0]):
            rows.append((row[0].strip("`"), row[1].strip("`"), row[2].strip("`"), row[3]))
    assert rows
    return rows


# --- 2. rows -------------------------------------------------------------------------------------


def to_rows(concepts, products, facility_terms, kinds):
    rows = []
    for concept, term, record, note in concepts:
        row = {"kind": "concept_term", "concept": concept, "term": term, "record": record if record else {"state": "no_record"}}
        if note:
            row["note"] = note
        rows.append(row)
    seen = set()
    for pid, term, cls, claim in products:
        if pid not in seen:
            rows.append({"kind": "product_term", "record": pid, "term": term})
            seen.add(pid)
        rows.append({"kind": "instance_of_basis", "record": pid, "class": cls, "claim_id": claim})
    for fid, term, term_is, note in facility_terms:
        row = {"kind": "facility_term", "record": fid, "term": term, "term_is": term_is.replace(" ", "_")}
        if note:
            row["note"] = note
        rows.append(row)
    for fid, kind, claim, word in kinds:
        rows.append({"kind": "facility_kind_basis", "record": fid, "facility_kind": kind, "claim_id": claim, "word": word})
    return rows


def write_json(path: Path, rows) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --- 4. the documents ----------------------------------------------------------------------------


def drop_table(text: str, start: str, end: str, first_cell: re.Pattern, pointer: str) -> str:
    """Replace the table whose rows' first cell matches first_cell, inside one section, by a pointer."""
    begin = text.index(start)
    stop = text.index(end, begin + len(start))
    body = text[begin:stop]
    lines = body.split("\n")
    rows = [i for i, line in enumerate(lines) if cells(line) and first_cell.match(cells(line)[0])]
    assert rows, f"no table to drop in {start.strip()}"
    top, bottom = rows[0] - 2, rows[-1]  # the header and separator lines sit above the first row
    assert cells(lines[top]) and set(lines[top + 1].replace("|", "").strip()) <= {"-", " "}
    lines[top : bottom + 1] = [pointer]
    return text[:begin] + "\n".join(lines) + text[stop:]


def replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"expected one occurrence of {old[:60]!r}"
    return text.replace(old, new)


def rewrite_concepts(text: str) -> str:
    text = replace_once(
        text,
        "`tests/test_data_entities.py` reads this table. It checks",
        f"The rows (concept, term, record or gap, note) are data: `data/identity_basis.json`, kind\n"
        f"`concept_term` ({POINTER}). `tests/test_data_entities.py` reads them. It checks",
    )
    text = drop_table(
        text, "\n## 3. ", "\n## 4. ", re.compile(rf"^{CONCEPT}$"),
        "To list them: `python -m json.tool data/identity_basis.json`.",
    )
    text = replace_once(
        text,
        "The check recomputes the ID from the record's\n`vendor` and this table,",
        "The check recomputes the ID from the record's\n`vendor` and its `product_term` row in `data/identity_basis.json`,",
    )
    text = replace_once(
        text,
        "So each\nclass a product is an instance of has one row here, naming the claim that supports it.",
        "So each\nclass a product is an instance of has one `instance_of_basis` row in `data/identity_basis.json`\n"
        f"({POINTER}), naming the claim that supports it.",
    )
    text = drop_table(
        text, "\n## 7. ", "\n## 8. ", re.compile(r"^`product-[a-z0-9-]+`$"),
        "The three products' terms and basis claims are rows of `data/identity_basis.json`.",
    )
    # §5: the broader column restated record values; the reasons stay.
    old = (
        "| Record | `broader` | Why |\n|---|---|---|\n"
        "| `component-data-centre-gpu`, `component-ai-asic` | `component-ai-accelerator` | TQ-01: an AI accelerator is a GPU or an AI ASIC |\n"
        "| `component-assembly-packaging-and-wafer-level-packaging-tools` | `component-semiconductor-manufacturing-equipment` | CSET's SME definition includes tools to \"assemble, test, and package\" |\n"
        "| `technology-2-5d-packaging-with-an-interposer`, `technology-3d-die-stacking` | `technology-advanced-packaging` | TQ-03's narrow definition names both |\n"
    )
    new = (
        f"Each value is in its record's `broader` field ({POINTER}); this table keeps why it holds.\n\n"
        "| Record | Why it is a kind of its `broader` value |\n|---|---|\n"
        "| `component-data-centre-gpu`, `component-ai-asic` | TQ-01: an AI accelerator is a GPU or an AI ASIC |\n"
        "| `component-assembly-packaging-and-wafer-level-packaging-tools` | CSET's SME definition includes tools to \"assemble, test, and package\" |\n"
        "| `technology-2-5d-packaging-with-an-interposer`, `technology-3d-die-stacking` | TQ-03's narrow definition names both kinds of advanced packaging |\n"
    )
    return replace_once(text, old, new)


def rewrite_facilities(text: str) -> str:
    text = replace_once(
        text,
        "`tests/test_data_entities.py` reads this table. It recomputes",
        f"The rows (facility, term, what the term is) are data: `data/identity_basis.json`, kind\n"
        f"`facility_term` ({POINTER}). `tests/test_data_entities.py` reads them. It recomputes",
    )
    text = drop_table(
        text, "\n## 2. ", "\n## 3. ", re.compile(r"^`facility-[a-z0-9-]+`$"),
        "To list them: `python -m json.tool data/identity_basis.json`.",
    )
    text = drop_table(
        text, "\n## 4. ", "\n## 5. ", re.compile(r"^`facility-[a-z0-9-]+`$"),
        f"Each record's basis rows are data: `data/identity_basis.json`, kind `facility_kind_basis`\n({POINTER}).",
    )
    return text


def rewrite_companies(text: str, legal_names: dict[str, str]) -> str:
    begin = text.index("\n## 2. ")
    stop = text.index("\n## 3. ", begin)
    lines = text[begin:stop].split("\n")
    out = []
    for line in lines:
        row = cells(line)
        if row == ["Record", "Legal entity (as the filing names it)", "Ruling"]:
            out.append("| Record | Ruling |")
        elif row == ["---", "---", "---"]:
            out.append("|---|---|")
        elif len(row) == 3 and row[0].startswith("`company-"):
            assert row[1] == legal_names[row[0].strip("`")], f"{row[0]}: restated name {row[1]!r} differs"
            out.append(f"| {row[0]} | {row[2]} |")
        else:
            out.append(line)
    body = "\n".join(out)
    body = replace_once(
        body,
        "| Record | Ruling |",
        f"The legal entity's name is the record's `legal_name` value, with its claims ({POINTER}); this table\nkeeps the ruling.\n\n| Record | Ruling |",
    )
    return text[:begin] + body + text[stop:]


def main() -> int:
    concepts_md = CONCEPTS_MD.read_text(encoding="utf-8")
    facilities_md = FACILITIES_MD.read_text(encoding="utf-8")
    companies_md = COMPANIES_MD.read_text(encoding="utf-8")
    old = {
        "concepts": old_concept_table(concepts_md),
        "products": old_product_table(concepts_md),
        "facility_terms": old_facility_terms(facilities_md),
        "kinds": old_kind_basis(facilities_md),
    }
    rows = to_rows(old["concepts"], old["products"], old["facility_terms"], old["kinds"])
    write_json(OUT, rows)
    write_json(OUT_STAGING, [])

    import test_data_entities as new  # the post-S14 loaders, reading the JSON just written

    assert new.concept_table() == old["concepts"], "concept rows differ"
    assert new.product_table() == old["products"], "product rows differ"
    assert new.facility_terms() == [(f, t, k.replace(" ", "_")) for f, t, k, _ in old["facility_terms"]], "facility terms differ"
    assert new.kind_basis() == old["kinds"], "kind-basis rows differ"

    companies = json.loads((REPO / "data/companies.json").read_text(encoding="utf-8"))
    # the restated cell gives one legal name, or a native name and its English form (SK hynix, TSMC)
    legal = {}
    for c in companies:
        names = [a["value"] for a in c["legal_name"]]
        legal[c["id"]] = names[0] if len(names) == 1 else f"{names[0]}, in English {names[1]}"
    CONCEPTS_MD.write_text(rewrite_concepts(concepts_md), encoding="utf-8")
    FACILITIES_MD.write_text(rewrite_facilities(facilities_md), encoding="utf-8")
    COMPANIES_MD.write_text(rewrite_companies(companies_md, legal), encoding="utf-8")
    counts = {k: sum(1 for r in rows if r["kind"] == k) for k in dict.fromkeys(r["kind"] for r in rows)}
    print(f"identity_basis: {len(rows)} rows {counts}; staging empty; documents rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
