"""validate-data for identity-basis rows (S14; DT-1; D-110, D-117).

An identity-basis row is a value about a named record that the record has no field for: the term a
rule-made ID is built from (CI-1, PI-1, FI-1), or the claim and word behind one value of an identity
field with no claim field (IO-1, FK-1). Until S14 these rows sat in four design-document tables and
the checks parsed Markdown to read them; now they live in data/identity_basis.json (staging:
data/staging/identity_basis.json), and the documents keep the rules. What each row must agree with
(the record's ID, its instance_of, its facility kinds, the anchors) stays checked in
tests/test_data_entities.py. This module checks the rows themselves:

IB-1  every row is valid against schemas/identity_basis.schema.json
IB-2  one row per key: one term per concept-and-record, product and facility; one basis row per
      instance_of value and facility kind; a basis row's product or facility has a term row
IB-3  a row follows its record's layer: a canonical row names a canonical record, a staging row a
      staging record (a concept gap, no_record, is canonical only)
IB-4  one home: the four document sections hold no per-record row any more, and the two tables
      that restated record values (legal entities, broader) no longer do

Uses the pinned jsonschema for IB-1 (D-026); the rest is standard library.
Run alone: python -m unittest discover -s tests -p "test_data_identity_basis.py" -v
"""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from test_data_entities import CONCEPTS, DATASET, FACILITIES, load_entities
from test_data_integrity import DATA, load_records
from test_entity_taxonomy import CONCEPT, cells, section
from test_source_record_schema import ENTITY_SCHEMA

REPO_ROOT = Path(__file__).resolve().parent.parent
IB_SCHEMA = json.loads((REPO_ROOT / "schemas/identity_basis.schema.json").read_text(encoding="utf-8"))
REGISTRY = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in (ENTITY_SCHEMA, IB_SCHEMA))
CANONICAL_FILE = DATA / "identity_basis.json"
STAGING_FILE = DATA / "staging" / "identity_basis.json"

# The key that makes a row unique, per kind (IB-2).
KEYS = {
    "concept_term": ("concept", "record"),
    "product_term": ("record",),
    "instance_of_basis": ("record", "class"),
    "facility_term": ("record",),
    "facility_kind_basis": ("record", "facility_kind"),
}
TERM_OF = {"instance_of_basis": "product_term", "facility_kind_basis": "facility_term"}
# The document sections that held the rows (M2-audit.md N-2), and the row shape each held.
FORMER_TABLES = (
    ("concept-dataset.md §3", CONCEPTS, "\n## 3. ", "\n## 4. ", re.compile(rf"^{CONCEPT}$")),
    ("concept-dataset.md §7", CONCEPTS, "\n## 7. ", "\n## 8. ", re.compile(r"^`product-[a-z0-9-]+`$")),
    ("facility-dataset.md §2", FACILITIES, "\n## 2. ", "\n## 3. ", re.compile(r"^`facility-[a-z0-9-]+`$")),
    ("facility-dataset.md §4", FACILITIES, "\n## 4. ", "\n## 5. ", re.compile(r"^`facility-[a-z0-9-]+`$")),
)


def load_rows() -> tuple[list[dict], list[dict]]:
    """(canonical rows, staging rows); a missing file is an error for canonical, empty for staging."""
    staging = load_records(STAGING_FILE) if STAGING_FILE.exists() else []
    return load_records(CANONICAL_FILE), staging


def key(row: dict) -> tuple:
    return (row["kind"],) + tuple(json.dumps(row[k], sort_keys=True) for k in KEYS[row["kind"]])


def check_schema(rows: list[dict]) -> list[str]:
    """IB-1."""
    validator = Draft202012Validator(IB_SCHEMA, registry=REGISTRY)
    return [f"row {i} ({row.get('kind')}, {row.get('record')}): {e.message}" for i, row in enumerate(rows) for e in validator.iter_errors(row)]


def check_keys(rows: list[dict]) -> list[str]:
    """IB-2."""
    errors, seen = [], set()
    for row in rows:
        k = key(row)
        if k in seen:
            errors.append(f"{row['kind']} for {row.get('record')}: more than one row with key {k[1:]}")
        seen.add(k)
    terms = {(r["kind"], r["record"]) for r in rows if r["kind"] in TERM_OF.values()}
    for row in rows:
        if row["kind"] in TERM_OF and (TERM_OF[row["kind"]], row["record"]) not in terms:
            errors.append(f"{row['kind']} for {row['record']}: the record has no {TERM_OF[row['kind']]} row")
    return errors


def check_layers(canonical: list[dict], staging: list[dict], entities: dict) -> list[str]:
    """IB-3."""
    ids = {where: {r["id"] for kind in entities[where].values() for r in kind} for where in ("canonical", "staging")}
    errors = []
    for where, rows in (("canonical", canonical), ("staging", staging)):
        for row in rows:
            record = row["record"]
            if isinstance(record, dict):
                if where != "canonical":
                    errors.append(f"concept_term {row['concept']}: a gap (no_record) belongs in the canonical file")
                continue
            if record not in ids[where]:
                other = "staging" if where == "canonical" else "canonical"
                found = f"a {other} record" if record in ids[other] else "no record"
                errors.append(f"{row['kind']} in the {where} file names {record}, which is {found}")
    return errors


def check_one_home(entities: dict) -> list[str]:
    """IB-4."""
    errors = []
    for label, text, start, end, first_cell in FORMER_TABLES:
        for line in section(text, start, end).splitlines():
            row = cells(line)
            if row and first_cell.match(row[0]):
                errors.append(f"{label} holds a per-record row again ({row[0]}); its home is data/identity_basis.json")
    companies = [r for where in ("canonical", "staging") for r in entities[where]["companies"]]
    legal = {a["value"] for r in companies if isinstance(r.get("legal_name"), list) for a in r["legal_name"]}
    for line in section(DATASET, "\n## 2. ", "\n## 3. ").splitlines():
        row = cells(line)
        for value in sorted(legal):
            if row and any(cell == value or cell.startswith(value + ",") for cell in row):
                errors.append(f"company-dataset.md §2 restates the legal name {value!r}; its home is the record")
    broader = {b for where in ("canonical", "staging") for kind in entities[where].values() for r in kind for b in r.get("broader", [])}
    for line in section(CONCEPTS, "\n## 5. ", "\n## 6. ").splitlines():
        row = cells(line)
        restated = [cell for cell in row[1:] if re.fullmatch(r"`[a-z0-9-]+`", cell) and cell.strip("`") in broader]
        if restated:
            errors.append(f"concept-dataset.md §5 restates the broader value {restated[0]}; its home is the record")
    return errors


class IdentityBasisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.canonical, self.staging = load_rows()
        self.entities = load_entities()

    def test_ib1_schema(self) -> None:
        self.assertEqual(check_schema(self.canonical + self.staging), [])

    def test_ib2_keys(self) -> None:
        self.assertEqual(check_keys(self.canonical + self.staging), [])

    def test_ib3_layers(self) -> None:
        self.assertEqual(check_layers(self.canonical, self.staging, self.entities), [])

    def test_ib4_one_home(self) -> None:
        self.assertEqual(check_one_home(self.entities), [])

    def test_every_kind_is_present(self) -> None:
        # DT-1 moved four tables; each kind has rows, so a check over an empty kind cannot pass vacuously.
        self.assertEqual({r["kind"] for r in self.canonical}, set(KEYS))


class IdentityBasisBreakTests(unittest.TestCase):
    """Each planted fault fails its check for the reason it names."""

    def setUp(self) -> None:
        self.canonical, self.staging = load_rows()
        self.entities = load_entities()

    def first(self, kind: str) -> dict:
        return next(r for r in self.canonical if r["kind"] == kind)

    def test_ib1_rejects_an_unknown_field(self) -> None:
        row = copy.deepcopy(self.first("product_term"))
        row["vendor"] = "company-nvidia"
        self.assertTrue(any("vendor" in e for e in check_schema([row])))

    def test_ib1_rejects_a_bad_facility_kind(self) -> None:
        row = copy.deepcopy(self.first("facility_kind_basis"))
        row["facility_kind"] = "fab"
        self.assertTrue(check_schema([row]))

    def test_ib2_rejects_a_second_term(self) -> None:
        row = copy.deepcopy(self.first("product_term"))
        row["term"] = "Another term"
        self.assertTrue(any("more than one row" in e for e in check_keys(self.canonical + [row])))

    def test_ib2_rejects_a_basis_row_without_a_term(self) -> None:
        rows = [r for r in self.canonical if not (r["kind"] == "product_term" and r["record"] == "product-nvidia-h100-tensor-core-gpu")]
        self.assertTrue(any("no product_term row" in e for e in check_keys(rows)))

    def test_ib3_rejects_a_canonical_row_for_no_record(self) -> None:
        row = copy.deepcopy(self.first("facility_term"))
        row["record"] = "facility-xa-nowhere"
        self.assertTrue(any("which is no record" in e for e in check_layers([row], [], self.entities)))

    def test_ib3_rejects_a_staged_gap(self) -> None:
        gap = next(r for r in self.canonical if r["kind"] == "concept_term" and isinstance(r["record"], dict))
        self.assertTrue(any("belongs in the canonical file" in e for e in check_layers([], [gap], self.entities)))

    def test_ib4_rejects_a_row_back_in_a_document(self) -> None:
        import test_data_identity_basis as module

        planted = CONCEPTS.replace("\n## 4. ", "\n| HBM-02 | High Bandwidth Memory | `component-high-bandwidth-memory` | |\n\n## 4. ", 1)
        saved = module.FORMER_TABLES
        try:
            module.FORMER_TABLES = ((saved[0][0], planted) + saved[0][2:],) + saved[1:]
            self.assertTrue(any("holds a per-record row again (HBM-02)" in e for e in check_one_home(self.entities)))
        finally:
            module.FORMER_TABLES = saved


if __name__ == "__main__":
    unittest.main()
