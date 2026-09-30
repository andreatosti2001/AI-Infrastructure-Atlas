"""Behaviour tests for the source record in schemas/sources.schema.json (S06; D-050, D-026).

Valid fixtures must pass. Each invalid case is one JSON Pointer mutation of a valid base
record. It must fail, and some error must be reported at the mutated pointer, inside the
value it sets, or at its parent (S04 pattern), so a case cannot pass by failing somewhere
unrelated.

The source record takes claim-independent shapes (partial dates, company IDs, unresolved
states) from entities.schema.json by $ref, and the claim schema takes shared shapes from
both files. REGISTRY and check_mutations are shared with test_claim_schema.py.

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable

from test_entity_schema import mutate
from test_relationship_schema import error_paths, pointer_path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load(path: str):
    return json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))


ENTITY_SCHEMA = load("schemas/entities.schema.json")
SOURCE_SCHEMA = load("schemas/sources.schema.json")
CLAIM_SCHEMA = load("schemas/claims.schema.json")
FIXTURES = load("tests/fixtures/source_records.json")

REGISTRY = Registry().with_resources(
    (schema["$id"], Resource.from_contents(schema))
    for schema in (ENTITY_SCHEMA, SOURCE_SCHEMA, CLAIM_SCHEMA)
)


def validator(schema: dict) -> Draft202012Validator:
    return Draft202012Validator(schema, registry=REGISTRY)


def check_mutations(test: unittest.TestCase, check: Draft202012Validator, fixtures: dict) -> None:
    """Every invalid case is one mutation that fails at, under or beside its pointer."""
    names = [case["case"] for case in fixtures["invalid"]]
    test.assertEqual(len(names), len(set(names)), "invalid case names must be unique")
    for case in fixtures["invalid"]:
        with test.subTest(case=case["case"], why=case["why"]):
            base = fixtures["valid"][case["base"]]
            mutated = mutate(base, case)
            test.assertNotEqual(mutated, base, "mutation changed nothing")
            errors = list(check.iter_errors(mutated))
            test.assertNotEqual(errors, [], "mutated record was accepted")
            pointers = list(case.get("set", {})) + list(case.get("remove", []))
            test.assertEqual(len(pointers), 1, "one mutation per case")
            path = pointer_path(pointers[0])
            located = [p for p in error_paths(errors) if p[: len(path)] == path or p == path[:-1]]
            test.assertTrue(
                located, f"no error at, under or beside {pointers[0]}: {[e.message for e in errors]}"
            )


class SourceRecordSchemaTests(unittest.TestCase):
    check = validator(SOURCE_SCHEMA)

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(SOURCE_SCHEMA)

    def test_relative_refs_resolve_to_sibling_schemas(self) -> None:
        base = SOURCE_SCHEMA["$id"].rsplit("/", 1)[0]
        self.assertEqual(f"{base}/entities.schema.json", ENTITY_SCHEMA["$id"])
        self.assertEqual(f"{base}/claims.schema.json", CLAIM_SCHEMA["$id"])

    def test_cross_file_refs_are_really_used(self) -> None:
        with self.assertRaises(Unresolvable):
            list(Draft202012Validator(SOURCE_SCHEMA).iter_errors(FIXTURES["valid"]["technical_documentation"]))

    def test_valid_fixtures_pass(self) -> None:
        for name, record in FIXTURES["valid"].items():
            with self.subTest(fixture=name):
                self.assertEqual([e.message for e in self.check.iter_errors(record)], [])

    def test_valid_fixtures_cover_every_class_group_and_state(self) -> None:
        records = FIXTURES["valid"].values()
        classes = {r["source_class"] for r in records}
        self.assertTrue(any(c.startswith("company_") for c in classes))
        self.assertTrue(any(not c.startswith("company_") for c in classes))
        self.assertIn("company_filing", classes)
        methods = {r["retrieval"]["method"] for r in records}
        self.assertEqual(methods, {i["const"] for i in SOURCE_SCHEMA["$defs"]["vocab_retrieval_method"]["oneOf"]})
        self.assertIn({"state": "undated"}, [r["stated_dates"] for r in records])

    def test_invalid_mutations_fail_where_they_mutate(self) -> None:
        check_mutations(self, self.check, FIXTURES)

    def test_every_field_is_required_or_conditional(self) -> None:
        # D-025 discipline: a field may be left out only when its absence has one meaning.
        optional = set(SOURCE_SCHEMA["properties"]) - set(SOURCE_SCHEMA["required"])
        self.assertEqual(optional, {"migrated_from", "filing_copy"})


if __name__ == "__main__":
    unittest.main()
