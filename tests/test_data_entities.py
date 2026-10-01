"""validate-data, part 3: entity records (S07; company-dataset.md §8).

Checks the company and jurisdiction records in data/ (canonical) and data/staging/
(staging) against each other, the claims and the sources. Standard library only; schema
validity of the records is part 2 (tests/test_data_schema.py). The checks, by ID:

- V-1  every reference resolves: identity_claim_ids and assertion claim_ids to claims,
       jurisdiction values to jurisdiction records, publisher_entity to a canonical company;
- V-4  valid_from <= valid_to on every assertion, at the coarser precision of the two;
- V-9  no placeholder slug in an entity ID (the relationship schema's `not_placeholder`
       pattern, read from its home);
- V-10 each field rests on at least one citation whose class is preferred or acceptable
       for the field's matrix row, with a standing the row allows (source-policy.md §7),
       following input claims down to their citations;
- CE-1 a canonical record cites only canonical claims and canonical jurisdictions, and no
       record ID is both staging and canonical (extends VD-8);
- ID-1 a company ID is `company-` plus the slug of one of its Latin-script legal names
       (company-dataset.md §3);
- J-1  a jurisdiction's code is on the ISO 3166-1 list: an identity claim of the record
       cites a standard_specification whose anchor carries the code.

The check functions take record lists, so the same checks run on the fictional fixtures.
"""

import copy
import json
import re
import unicodedata
import unittest
from pathlib import Path

from test_data_integrity import DATA, load_records, load_data
from test_entity_taxonomy import cells, decision_exists, section
from test_source_policy import column_classes, matrix_rows

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET = (REPO_ROOT / "docs/architecture/company-dataset.md").read_text(encoding="utf-8")
REL_SCHEMA = json.loads((REPO_ROOT / "schemas/relationships.schema.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((REPO_ROOT / "tests/fixtures/entity_records.json").read_text(encoding="utf-8"))

ENTITY_KINDS = ("companies", "jurisdictions")
REF_FIELDS = {"incorporated_in", "headquartered_in", "located_in"}


def entity_files(kind: str) -> tuple[Path, Path]:
    """(canonical, staging) paths of one entity file pair (H-2 layout)."""
    return DATA / f"{kind}.json", DATA / "staging" / f"{kind}.json"


def load_entities() -> dict:
    """{"canonical": {kind: [records]}, "staging": {kind: [records]}}; a missing file is empty."""
    result = {"canonical": {}, "staging": {}}
    for kind in ENTITY_KINDS:
        canonical, staging = entity_files(kind)
        result["canonical"][kind] = load_records(canonical) if canonical.exists() else []
        result["staging"][kind] = load_records(staging) if staging.exists() else []
    return result


# --- the rules, read from their homes ---------------------------------------------------------


def legal_forms() -> list[str]:
    """company-dataset.md §3: the legal-form designations stripped from a legal name."""
    body = section(DATASET, "\n## 3. ", "\n## 4. ")
    rows = [cells(line) for line in body.splitlines()]
    rows = [r for r in rows if r and re.fullmatch(r"`[^`]+`", r[0])]
    for row in rows:
        assert len(row) == 3, f"legal-form row {row[0]!r} has {len(row)} cells, expected 3"
    assert rows, "no legal-form table in company-dataset.md §3"
    return [row[0].strip("`") for row in rows]


def placeholder_pattern() -> re.Pattern:
    return re.compile(REL_SCHEMA["$defs"]["not_placeholder"]["not"]["pattern"])


def matrix() -> dict[str, dict]:
    """source-policy.md §7: row -> {sufficient classes, standings, freshness}."""
    result = {}
    for row in matrix_rows():
        key = row[0].strip("`")
        standings = {"party or originator": {"party", "originator"}, "party": {"party"}, "originator": {"originator"}}[row[4]]
        result[key] = {
            "sufficient": set(column_classes(row[1])) | set(column_classes(row[2])),
            "standings": standings,
            "freshness": row[5],
        }
    return result


def slug(name: str) -> str:
    """ID-1: drop one trailing legal-form designation, then lower-case ASCII words joined by '-'."""
    text = name.strip()
    for form in sorted(legal_forms(), key=len, reverse=True):
        if text.lower().endswith(" " + form.lower()):
            text = text[: -len(form)].rstrip(" ,")
            break
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def is_latin(name: str) -> bool:
    return all(ord(ch) < 0x250 for ch in name)


# --- walking records --------------------------------------------------------------------------


def fields(record: dict):
    """(field, row suffix, list of (assertion or None, claim IDs)) for every claim-citing field."""
    yield "identity_claim_ids", f"identity:{record['type']}", [(None, record["identity_claim_ids"])]
    for name, value in record.items():
        if isinstance(value, list) and value and isinstance(value[0], dict) and "claim_ids" in value[0]:
            yield name, f"attr:{record['type']}.{name}", [(a, a["claim_ids"]) for a in value]
        elif isinstance(value, dict) and "claim_ids" in value:
            yield name, f"attr:{record['type']}.{name}", [(None, value["claim_ids"])]


def leaf_citations(claim_id: str, claims: dict, seen=None) -> list[tuple[dict, dict]]:
    """(claim, citation) for every citation reached from a claim through its inputs."""
    seen = set() if seen is None else seen
    if claim_id in seen or claim_id not in claims:
        return []
    seen.add(claim_id)
    claim = claims[claim_id]
    found = [(claim, c) for c in claim.get("citations", [])]
    for ref in claim.get("input_claim_ids", []):
        found += leaf_citations(ref, claims, seen)
    return found


def all_records(entities: dict) -> list[tuple[str, dict]]:
    return [(where, r) for where in ("canonical", "staging") for kind in ENTITY_KINDS for r in entities[where][kind]]


# --- checks -----------------------------------------------------------------------------------


def check_references(entities, sources, staging_claims, canonical_claims) -> list[str]:
    """V-1."""
    claims = {c["id"] for c in staging_claims + canonical_claims}
    jurisdictions = {r["id"] for where in entities for r in entities[where]["jurisdictions"]}
    errors = []
    for _, record in all_records(entities):
        for field, _, assertions in fields(record):
            for assertion, ids in assertions:
                errors += [f"{record['id']}.{field} cites missing claim {c}" for c in ids if c not in claims]
                if assertion is not None and field in REF_FIELDS and assertion["value"] not in jurisdictions:
                    errors.append(f"{record['id']}.{field} points to missing jurisdiction {assertion['value']}")
    companies = {r["id"] for r in entities["canonical"]["companies"]}
    for source in sources:
        ref = source["publisher_entity"]
        if isinstance(ref, str) and ref not in companies:
            errors.append(f"{source['id']}.publisher_entity points to {ref}, which is not a canonical company")
    return errors


def coarse(date: str, other: str) -> str:
    return date[: min(len(date), len(other))]


def check_periods(entities) -> list[str]:
    """V-4."""
    errors = []
    for _, record in all_records(entities):
        for field, _, assertions in fields(record):
            for assertion, _ in assertions:
                if assertion and "valid_from" in assertion and "valid_to" in assertion:
                    start, end = assertion["valid_from"], assertion["valid_to"]
                    if coarse(start, end) > coarse(end, start):
                        errors.append(f"{record['id']}.{field}: valid_from {start} is after valid_to {end}")
    return errors


def check_placeholders(entities) -> list[str]:
    """V-9."""
    pattern = placeholder_pattern()
    return [f"{record['id']} is a placeholder slug" for _, record in all_records(entities) if pattern.search(record["id"])]


def check_matrix_support(entities, sources, staging_claims, canonical_claims) -> list[str]:
    """V-10."""
    rows = matrix()
    classes = {s["id"]: s["source_class"] for s in sources}
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for _, record in all_records(entities):
        for field, row_key, assertions in fields(record):
            row = rows[row_key]
            for assertion, ids in assertions:
                leaves = [lc for cid in ids for lc in leaf_citations(cid, claims)]
                if not any(classes.get(c["source_id"]) in row["sufficient"] and c["standing"] in row["standings"] for _, c in leaves):
                    label = f" = {assertion['value']}" if assertion else ""
                    errors.append(f"{record['id']}.{field}{label}: no citation with a class and standing that {row_key} allows")
    return errors


def check_canonical_entities(entities, canonical_claims) -> list[str]:
    """CE-1."""
    claim_ids = {c["id"] for c in canonical_claims}
    jurisdictions = {r["id"] for r in entities["canonical"]["jurisdictions"]}
    errors = []
    for kind in ENTITY_KINDS:
        staged = {r["id"] for r in entities["staging"][kind]}
        for record in entities["canonical"][kind]:
            if record["id"] in staged:
                errors.append(f"{record['id']} is both staging and canonical")
            for field, _, assertions in fields(record):
                for assertion, ids in assertions:
                    errors += [f"canonical {record['id']}.{field} cites staging claim {c}" for c in ids if c not in claim_ids]
                    if assertion is not None and field in REF_FIELDS and assertion["value"] not in jurisdictions:
                        errors.append(f"canonical {record['id']}.{field} points to non-canonical {assertion['value']}")
    for where in ("canonical", "staging"):
        for kind in ENTITY_KINDS:
            seen = set()
            for record in entities[where][kind]:
                if record["id"] in seen:
                    errors.append(f"{record['id']} is defined twice in {where} {kind}")
                seen.add(record["id"])
    return errors


def check_company_ids(entities) -> list[str]:
    """ID-1."""
    errors = []
    for where in ("canonical", "staging"):
        for record in entities[where]["companies"]:
            names = record["legal_name"] if isinstance(record["legal_name"], list) else []
            slugs = {"company-" + slug(a["value"]) for a in names if is_latin(a["value"])}
            if record["id"] not in slugs:
                errors.append(f"{record['id']}: not the slug of a Latin-script legal name {sorted(slugs) or '(none recorded)'}")
    return errors


def check_jurisdiction_codes(entities, sources, staging_claims, canonical_claims) -> list[str]:
    """J-1."""
    classes = {s["id"]: s["source_class"] for s in sources}
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for where in ("canonical", "staging"):
        for record in entities[where]["jurisdictions"]:
            code = record["id"].removeprefix("jurisdiction-").upper()
            ok = any(
                classes.get(c["source_id"]) == "standard_specification" and re.search(rf"\b{code}\b", c["anchor"])
                for cid in record["identity_claim_ids"]
                for c in claims.get(cid, {}).get("citations", [])
            )
            if not ok:
                errors.append(f"{record['id']}: no ISO 3166-1 identity citation carries the code {code}")
    return errors


def entity_errors(entities, sources, staging_claims, canonical_claims) -> list[str]:
    errors = check_references(entities, sources, staging_claims, canonical_claims)
    errors += check_periods(entities)
    errors += check_placeholders(entities)
    errors += check_matrix_support(entities, sources, staging_claims, canonical_claims)
    errors += check_canonical_entities(entities, canonical_claims)
    errors += check_company_ids(entities)
    errors += check_jurisdiction_codes(entities, sources, staging_claims, canonical_claims)
    return errors


def fixture_world():
    """The fictional sources, claims and entity records of tests/fixtures/entity_records.json."""
    world = copy.deepcopy(FIXTURES["valid"])
    return world["entities"], world["sources"], world["staging_claims"], world["canonical_claims"]


# --- tests ------------------------------------------------------------------------------------


class RuleSourceTests(unittest.TestCase):
    def test_legal_forms_are_read(self) -> None:
        self.assertTrue(legal_forms())

    def test_every_entity_field_has_a_matrix_row(self) -> None:
        rows = matrix()
        for kind, type_name in (("companies", "company"), ("jurisdictions", "jurisdiction")):
            record = (FIXTURES["valid"]["entities"]["staging"][kind] + FIXTURES["valid"]["entities"]["canonical"][kind])[0]
            for _, row_key, _ in fields(record):
                with self.subTest(row=row_key):
                    self.assertIn(row_key, rows)

    def test_slug_rule_examples(self) -> None:
        # company-dataset.md §3: the slug ignores case, punctuation and the legal form.
        self.assertEqual(slug("EXAMPLE.COM, INC."), "example-com")
        self.assertEqual(slug("Example Designer Corporation"), "example-designer")
        self.assertEqual(slug("Example Holding N.V."), "example-holding")

    def test_display_name_does_not_move_an_id(self) -> None:
        # ID-1 reads the legal name, never the editorial display name (entity taxonomy §7).
        entities, sources, staging, canonical = fixture_world()
        entities["staging"]["companies"][0]["name"] = "A Completely Different Display Name"
        self.assertEqual(check_company_ids(entities), [])


class EntityDataTests(unittest.TestCase):
    """The checks on the real files in data/ and data/staging/."""

    def setUp(self) -> None:
        self.entities = load_entities()
        self.sources, self.staging, self.canonical = load_data()

    def test_entity_files_exist(self) -> None:
        # L-05: each data file this session creates is in the validator's scope.
        for kind in ENTITY_KINDS:
            canonical, staging = entity_files(kind)
            with self.subTest(kind=kind):
                self.assertTrue(canonical.exists() or staging.exists(), f"no {kind} file")

    def test_s07_gate_canonical_companies_exist(self) -> None:
        # Roadmap S07 gate: "Every canonical company record has identity evidence and stable
        # IDs". The schema requires identity_claim_ids; CE-1, V-10 and ID-1 check the rest.
        self.assertTrue(self.entities["canonical"]["companies"], "no canonical company")

    def test_v1_references_resolve(self) -> None:
        self.assertEqual(check_references(self.entities, self.sources, self.staging, self.canonical), [])

    def test_v4_periods_are_ordered(self) -> None:
        self.assertEqual(check_periods(self.entities), [])

    def test_v9_no_placeholder_ids(self) -> None:
        self.assertEqual(check_placeholders(self.entities), [])

    def test_v10_fields_rest_on_allowed_classes_and_standing(self) -> None:
        self.assertEqual(check_matrix_support(self.entities, self.sources, self.staging, self.canonical), [])

    def test_ce1_canonical_records_rest_on_canonical_claims(self) -> None:
        self.assertEqual(check_canonical_entities(self.entities, self.canonical), [])

    def test_id1_company_ids_follow_the_rule(self) -> None:
        self.assertEqual(check_company_ids(self.entities), [])

    def test_j1_jurisdiction_codes_are_on_the_iso_list(self) -> None:
        self.assertEqual(check_jurisdiction_codes(self.entities, self.sources, self.staging, self.canonical), [])


class EntityFixtureTests(unittest.TestCase):
    """The checks accept the fictional set and catch a planted fault of each kind."""

    def test_fixture_world_is_clean(self) -> None:
        self.assertEqual(entity_errors(*fixture_world()), [])

    def test_planted_faults_are_caught(self) -> None:
        def company(entities, where="staging"):
            return entities[where]["companies"][0]

        def claim(claims, claim_id):
            return next(c for c in claims if c["id"] == claim_id)

        faults = FIXTURES["faults"]
        actions = {
            "set_company_field": lambda w, f: company(w[0], f.get("where", "staging")).__setitem__(f["field"], f["value"]),
            "set_citation_field": lambda w, f: claim(w[2] + w[3], f["claim"])["citations"][0].__setitem__(f["field"], f["value"]),
            "set_source_field": lambda w, f: next(s for s in w[1] if s["id"] == f["source"]).__setitem__(f["field"], f["value"]),
            "move_company_to_canonical": lambda w, f: w[0]["canonical"]["companies"].append(copy.deepcopy(company(w[0]))),
            "drop_jurisdiction": lambda w, f: w[0][f["where"]]["jurisdictions"].clear(),
        }
        self.assertTrue(faults)
        for fault in faults:
            with self.subTest(fault=fault["name"]):
                world = list(fixture_world())
                actions[fault["action"]](world, fault)
                errors = entity_errors(*world)
                self.assertTrue(any(fault["expect"] in e for e in errors), f"{fault['name']}: {errors}")


class DocumentReferenceTests(unittest.TestCase):
    """Every decision, source, claim and record cited in the S07 documents exists (Part B §07
    task 11). Records and claims in either file count: the documents name staging ones too."""

    DOCS = ("docs/architecture/company-dataset.md", "docs/architecture/milestone-audits/M1-audit.md")

    def text(self) -> str:
        return "\n".join((REPO_ROOT / d).read_text(encoding="utf-8") for d in self.DOCS)

    def test_cited_decisions_exist(self) -> None:
        for ref in sorted(set(re.findall(r"\bD-\d{3}\b", self.text()))):
            with self.subTest(decision=ref):
                self.assertTrue(decision_exists(ref))

    def test_cited_sources_claims_and_records_exist(self) -> None:
        sources, staging, canonical = load_data()
        entities = load_entities()
        known = {s["id"] for s in sources} | {c["id"] for c in staging + canonical}
        known |= {r["id"] for _, r in all_records(entities)}
        text = DATASET
        for span in re.findall(r"`src-(\d{3})` to `src-(\d{3})`", text):
            known_range = {f"src-{n:03d}" for n in range(int(span[0]), int(span[1]) + 1)}
            for ref in sorted(known_range):
                with self.subTest(ref=ref):
                    self.assertTrue(ref in known, f"{ref} is cited but does not exist")
        for ref in sorted(set(re.findall(r"`((?:src|claim|company|jurisdiction)-[a-z0-9-]+)`", text))):
            with self.subTest(ref=ref):
                self.assertTrue(ref in known, f"{ref} is cited but does not exist")


if __name__ == "__main__":
    unittest.main()
