"""validate-data, part 3: entity records (S07; company-dataset.md §8; S08: concept-dataset.md §9).

Checks the company, jurisdiction, technology, component and product records in data/
(canonical) and data/staging/ (staging) against each other, the claims and the sources. Standard library only; schema
validity of the records is part 2 (tests/test_data_schema.py). The checks, by ID:

- V-1  every reference resolves: identity_claim_ids and assertion claim_ids to claims,
       jurisdiction values to jurisdiction records, publisher_entity to a canonical company;
       (S08) `broader` to a record of the same type, `instance_of` to a technology or
       component, a product's `vendor` to a canonical company;
- V-4  valid_from <= valid_to on every assertion, at the coarser precision of the two;
- V-9  no placeholder slug in an entity ID (the relationship schema's `not_placeholder`
       pattern, read from its home);
- V-10 each field rests on at least one citation whose class is preferred or acceptable
       for the field's matrix row, with a standing the row allows (source-policy.md §7),
       following input claims down to their citations;
- CE-1 a canonical record cites only canonical claims and canonical jurisdictions, its
       `broader`, `instance_of` and `vendor` are canonical, and no record ID is both staging
       and canonical (extends VD-8);
- ID-1 a company ID is `company-` plus the slug of one of its Latin-script legal names
       (company-dataset.md §3);
- J-1  a jurisdiction's code is on the ISO 3166-1 list: an identity claim of the record
       cites a standard_specification whose anchor carries the code;
- DEF-1 a technology's or component's definition cites exactly one INTERPRETATION (the
       working definition), and every identity claim is an ATTRIBUTION among its inputs;
- DEF-2 no definition claim serves two records, and no concept is in two records unless
       the concept table lists it twice (a split);
- B-1  `broader` has no cycle;
- CI-1 concept-dataset.md §3: the concept table against entity-taxonomy.md §5, the schema's
       `x-concepts` and the records; IDs are the type plus the slug of the row's term;
- PI-1 a product ID is `product-`, the vendor's ID without `company-`, and the slug of the
       product's term in concept-dataset.md §7, found verbatim in an identity anchor;
- IO-1 every `instance_of` value has a basis row in concept-dataset.md §7, and every row a
       value.

The check functions take record lists, so the same checks run on the fictional fixtures.
"""

import copy
import json
import re
import unicodedata
import unittest
from pathlib import Path

from test_data_integrity import DATA, load_records, load_data
from test_entity_taxonomy import CONCEPT, TAXONOMY, cells, decision_exists, section
from test_source_policy import column_classes, matrix_rows

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET = (REPO_ROOT / "docs/architecture/company-dataset.md").read_text(encoding="utf-8")
CONCEPTS = (REPO_ROOT / "docs/architecture/concept-dataset.md").read_text(encoding="utf-8")
ENTITY_SCHEMA = json.loads((REPO_ROOT / "schemas/entities.schema.json").read_text(encoding="utf-8"))
REL_SCHEMA = json.loads((REPO_ROOT / "schemas/relationships.schema.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((REPO_ROOT / "tests/fixtures/entity_records.json").read_text(encoding="utf-8"))

ENTITY_KINDS = ("companies", "jurisdictions", "technologies", "components", "products")
REF_FIELDS = {"incorporated_in", "headquartered_in", "located_in"}
CONCEPT_TYPES = ("technology", "component")
KIND_FIELD = {"technology": ("technology_kind", "vocab_technology_kind"), "component": ("use_class", "vocab_component_use_class")}


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


def term_slug(term: str) -> str:
    """CI-1 and PI-1: lower-case ASCII words joined by '-'; no legal form is dropped."""
    ascii_text = unicodedata.normalize("NFKD", term).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def taxonomy_concepts() -> dict[str, tuple[str, list[str]]]:
    """entity-taxonomy.md §5: concept -> (name, targets)."""
    body = section(TAXONOMY, "## 5. ", "## 6. ")
    rows = {}
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 6 and re.fullmatch(CONCEPT, row[0]):
            rows[row[0]] = (row[1], re.findall(r"`([^`]+)`", row[4]))
    return rows


def concept_table() -> list[tuple[str, str, str | None, str]]:
    """concept-dataset.md §3: (concept, term, record ID or None for a gap, note)."""
    body = section(CONCEPTS, "\n## 3. ", "\n## 4. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 4 and re.fullmatch(CONCEPT, row[0]):
            ids = re.findall(r"`([^`]+)`", row[2])
            rows.append((row[0], row[1], ids[0] if ids else None, row[3]))
    assert rows, "no concept table in concept-dataset.md §3"
    return rows


def split_concepts() -> set[str]:
    """Concepts the concept table lists more than once (D-070)."""
    concepts = [row[0] for row in concept_table()]
    return {c for c in concepts if concepts.count(c) > 1}


def product_table() -> list[tuple[str, str, str, str]]:
    """concept-dataset.md §7: (product ID, term, class, basis claim)."""
    body = section(CONCEPTS, "\n## 7. ", "\n## 8. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 4 and re.fullmatch(r"`product-[a-z0-9-]+`", row[0]):
            rows.append((row[0].strip("`"), row[1], row[2].strip("`"), row[3].strip("`")))
    assert rows, "no product table in concept-dataset.md §7"
    return rows


def x_concepts(vocab: str) -> dict[str, set[str]]:
    """The schema's vocabulary value -> the concepts it serves (`x-concepts`)."""
    return {v["const"]: set(v.get("x-concepts", [])) for v in ENTITY_SCHEMA["$defs"][vocab]["oneOf"]}


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


def structural_refs(record: dict):
    """(field, target) for each reference that is not claim-backed (S08): broader, instance_of, vendor."""
    for target in record.get("broader", []):
        yield "broader", target
    for target in record.get("instance_of", []):
        yield "instance_of", target
    if "vendor" in record:
        yield "vendor", record["vendor"]


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
    types = {r["id"]: r["type"] for _, r in all_records(entities)}
    for _, record in all_records(entities):
        for field, target in structural_refs(record):
            if field == "vendor" and target not in companies:
                errors.append(f"{record['id']}.vendor points to {target}, which is not a canonical company")
            elif field == "broader" and types.get(target) != record["type"]:
                errors.append(f"{record['id']}.broader points to missing {record['type']} {target}")
            elif field == "instance_of" and types.get(target) not in CONCEPT_TYPES:
                errors.append(f"{record['id']}.instance_of points to missing class {target}")
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
    canonical_ids = {r["id"] for kind in ENTITY_KINDS for r in entities["canonical"][kind]}
    errors = []
    for kind in ENTITY_KINDS:
        staged = {r["id"] for r in entities["staging"][kind]}
        for record in entities["canonical"][kind]:
            if record["id"] in staged:
                errors.append(f"{record['id']} is both staging and canonical")
            for field, target in structural_refs(record):
                if target not in canonical_ids:
                    errors.append(f"canonical {record['id']}.{field} points to non-canonical {target}")
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


def concept_records(entities):
    return [r for _, r in all_records(entities) if r["type"] in CONCEPT_TYPES]


def definition_claims(record: dict) -> list[str]:
    value = record["definition"]
    return [c for a in value for c in a["claim_ids"]] if isinstance(value, list) else []


def check_definitions(entities, staging_claims, canonical_claims) -> list[str]:
    """DEF-1."""
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for record in concept_records(entities):
        ids = definition_claims(record)
        if len(ids) != 1 or claims.get(ids[0], {}).get("claim_type") != "INTERPRETATION":
            errors.append(f"{record['id']}.definition: not exactly one INTERPRETATION claim (a working definition)")
            continue
        inputs = set(claims[ids[0]].get("input_claim_ids", []))
        missing = [c for c in record["identity_claim_ids"] if c not in inputs]
        if missing:
            errors.append(f"{record['id']}: identity claims {missing} are not inputs of its working definition {ids[0]}")
        not_attributions = [c for c in record["identity_claim_ids"] if claims.get(c, {}).get("claim_type") != "ATTRIBUTION"]
        if not_attributions:
            errors.append(f"{record['id']}: identity claims {not_attributions} are not ATTRIBUTION claims")
    return errors


def check_distinct(entities, split: set[str]) -> list[str]:
    """DEF-2."""
    by_claim, by_concept = {}, {}
    for record in concept_records(entities):
        for claim_id in definition_claims(record):
            by_claim.setdefault(claim_id, set()).add(record["id"])
        for concept in record["concept_refs"]:
            by_concept.setdefault(concept, set()).add(record["id"])
    errors = [f"definition claim {c} serves several records: {sorted(ids)}" for c, ids in sorted(by_claim.items()) if len(ids) > 1]
    errors += [f"concept {c} is in several records: {sorted(ids)}" for c, ids in sorted(by_concept.items()) if len(ids) > 1 and c not in split]
    return errors


def check_broader_cycles(entities) -> list[str]:
    """B-1."""
    graph = {}
    for _, record in all_records(entities):
        graph.setdefault(record["id"], set()).update(record.get("broader", []))
    errors, done = [], set()

    def visit(node, path):
        if node in path:
            errors.append(f"broader cycle: {' -> '.join(path[path.index(node):] + [node])}")
            return
        if node in done:
            return
        for parent in sorted(graph.get(node, ())):
            visit(parent, path + [node])
        done.add(node)

    for node in sorted(graph):
        visit(node, [])
    return errors


def check_concept_table(entities, rows) -> list[str]:
    """CI-1."""
    taxonomy = taxonomy_concepts()
    records = {r["id"]: r for r in concept_records(entities)}
    listed = [row[0] for row in rows]
    errors = []
    for concept, (_, targets) in taxonomy.items():
        if any(t in ("type:technology", "type:component") for t in targets) and concept not in listed:
            errors.append(f"{concept}: mapped to a technology or component in entity-taxonomy §5 but not in the concept table")
    for concept, term, record_id, note in rows:
        name, targets = taxonomy.get(concept, ("", []))
        kinds = [t.removeprefix("type:") for t in targets if t in ("type:technology", "type:component")]
        if not kinds:
            errors.append(f"{concept}: not a technology or component concept in entity-taxonomy §5")
            continue
        if listed.count(concept) == 1 and term != name:
            errors.append(f"{concept}: term {term!r} is not the §5 name {name!r}")
        if listed.count(concept) > 1:
            words = set(re.findall(r"\w+", name.lower()))
            if not set(re.findall(r"\w+", term.lower())) <= words or not re.search(r"\bD-\d{3}\b", note):
                errors.append(f"{concept}: split term {term!r} must use words of {name!r} and cite a decision")
        if record_id is None:
            holders = sorted(r["id"] for r in records.values() if concept in r["concept_refs"])
            if holders:
                errors.append(f"{concept} is a gap in the concept table but has records {holders}")
            continue
        if record_id != f"{kinds[0]}-{term_slug(term)}":
            errors.append(f"{record_id}: not {kinds[0]}- plus the slug of its term {term!r}")
        record = records.get(record_id)
        if record is None:
            errors.append(f"{record_id}: in the concept table but no such record")
            continue
        if record["concept_refs"] != [concept]:
            errors.append(f"{record_id}: concept_refs {record['concept_refs']} is not [{concept!r}]")
        field, vocab = KIND_FIELD[record["type"]]
        if concept not in x_concepts(vocab).get(record[field], set()):
            errors.append(f"{record_id}: {field} {record[field]!r} does not serve {concept} (schema x-concepts)")
    tabled = {row[2] for row in rows}
    errors += [f"{rid}: a technology or component record not in the concept table" for rid in sorted(records) if rid not in tabled]
    return errors


def check_products(entities, staging_claims, canonical_claims, rows) -> list[str]:
    """PI-1 and IO-1."""
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    products = {r["id"]: r for where in ("canonical", "staging") for r in entities[where]["products"]}
    errors = [f"{pid}: in the product table but no such record" for pid in sorted({row[0] for row in rows}) if pid not in products]
    for pid, record in sorted(products.items()):
        mine = [row for row in rows if row[0] == pid]
        terms = {row[1] for row in mine}
        if len(terms) != 1:
            errors.append(f"{pid}: needs exactly one term in the product table, has {sorted(terms)}")
            continue
        (term,) = terms
        want = f"product-{record['vendor'].removeprefix('company-')}-{term_slug(term)}"
        if pid != want:
            errors.append(f"{pid}: not the vendor's ID plus the slug of its term (expected {want})")
        anchors = [c["anchor"] for cid in record["identity_claim_ids"] for c in claims.get(cid, {}).get("citations", [])]
        if not any(term in anchor for anchor in anchors):
            errors.append(f"{pid}: term {term!r} is not in any identity anchor")
        basis = {row[2] for row in mine}
        if basis != set(record["instance_of"]):
            errors.append(f"{pid}: instance_of {sorted(record['instance_of'])} has basis rows for {sorted(basis)}")
        errors += [f"{pid}: basis claim {row[3]} does not exist" for row in mine if row[3] not in claims]
    return errors


def entity_errors(entities, sources, staging_claims, canonical_claims) -> list[str]:
    errors = check_references(entities, sources, staging_claims, canonical_claims)
    errors += check_periods(entities)
    errors += check_placeholders(entities)
    errors += check_matrix_support(entities, sources, staging_claims, canonical_claims)
    errors += check_canonical_entities(entities, canonical_claims)
    errors += check_company_ids(entities)
    errors += check_jurisdiction_codes(entities, sources, staging_claims, canonical_claims)
    errors += check_definitions(entities, staging_claims, canonical_claims)
    errors += check_distinct(entities, split_concepts())
    errors += check_broader_cycles(entities)
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
        for kind in ENTITY_KINDS:
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

    def test_concept_and_product_tables_are_read(self) -> None:
        self.assertTrue(concept_table())
        self.assertTrue(product_table())
        self.assertTrue(taxonomy_concepts())

    def test_term_slug_examples(self) -> None:
        # concept-dataset.md §3 and §7: every run of other characters becomes one '-'.
        self.assertEqual(term_slug("2.5D packaging with an interposer"), "2-5d-packaging-with-an-interposer")
        self.assertEqual(term_slug("Assembly, packaging and wafer-level packaging tools"), "assembly-packaging-and-wafer-level-packaging-tools")
        self.assertEqual(term_slug("HBM4 36GB 12H"), "hbm4-36gb-12h")

    def test_display_name_does_not_move_a_concept_or_product_id(self) -> None:
        # CI-1 and PI-1 read the taxonomy name and the anchored term, never the display name.
        entities = load_entities()
        sources, staging, canonical = load_data()
        for _, record in all_records(entities):
            if record["type"] in ("technology", "component", "product"):
                record["name"] = "A Completely Different Display Name"
        self.assertEqual(check_concept_table(entities, concept_table()), [])
        self.assertEqual(check_products(entities, staging, canonical, product_table()), [])


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

    def test_s08_gate_concept_records_exist(self) -> None:
        # Roadmap S08 gate: "Definitions are sourced and do not collapse technically distinct
        # concepts". DEF-1, DEF-2, CI-1 and V-10 check the records; this checks there are some.
        self.assertTrue(concept_records(self.entities), "no technology or component record")
        self.assertTrue(self.entities["canonical"]["products"] + self.entities["staging"]["products"], "no product record")

    def test_def1_definitions_are_working_definitions(self) -> None:
        self.assertEqual(check_definitions(self.entities, self.staging, self.canonical), [])

    def test_def2_no_concept_or_definition_in_two_records(self) -> None:
        self.assertEqual(check_distinct(self.entities, split_concepts()), [])

    def test_b1_broader_is_acyclic(self) -> None:
        self.assertEqual(check_broader_cycles(self.entities), [])

    def test_ci1_concept_table_matches_taxonomy_schema_and_records(self) -> None:
        self.assertEqual(check_concept_table(self.entities, concept_table()), [])

    def test_pi1_io1_product_ids_and_instance_of_basis(self) -> None:
        self.assertEqual(check_products(self.entities, self.staging, self.canonical, product_table()), [])


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
            "set_record_field": lambda w, f: w[0][f["where"]][f["kind"]][f.get("index", 0)].__setitem__(f["field"], f["value"]),
        }
        self.assertTrue(faults)
        for fault in faults:
            with self.subTest(fault=fault["name"]):
                world = list(fixture_world())
                actions[fault["action"]](world, fault)
                errors = entity_errors(*world)
                self.assertTrue(any(fault["expect"] in e for e in errors), f"{fault['name']}: {errors}")


class DocumentReferenceTests(unittest.TestCase):
    """Every decision, source, claim and record cited in the S07 and S08 documents exists (S07
    Part B §07 task 11). Records and claims in either file count: the documents name staging
    ones too."""

    DOCS = ("docs/architecture/company-dataset.md", "docs/architecture/milestone-audits/M1-audit.md", "docs/architecture/concept-dataset.md")

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
        text = DATASET + CONCEPTS
        for span in re.findall(r"`src-(\d{3})` to `src-(\d{3})`", text):
            known_range = {f"src-{n:03d}" for n in range(int(span[0]), int(span[1]) + 1)}
            for ref in sorted(known_range):
                with self.subTest(ref=ref):
                    self.assertTrue(ref in known, f"{ref} is cited but does not exist")
        for ref in sorted(set(re.findall(r"`((?:src|claim|company|jurisdiction|technology|component|product)-[a-z0-9-]+)`", text))):
            with self.subTest(ref=ref):
                self.assertTrue(ref in known, f"{ref} is cited but does not exist")


if __name__ == "__main__":
    unittest.main()
