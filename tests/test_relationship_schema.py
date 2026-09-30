"""Behaviour tests for schemas/relationships.schema.json (S04; D-028 to D-031, D-026).

Valid fixtures must pass. Each invalid case is one JSON Pointer mutation of a valid
base record. It must fail, and some error must be reported at the mutated pointer,
inside the value it sets, or at its parent (for added or removed fields). So a case
cannot pass by failing somewhere unrelated.

The relationship schema takes claim IDs, dates, entity ID patterns, assertions and
explicit states from entities.schema.json by $ref (one home). These tests also prove
that jsonschema resolves those cross-file references, and that it cannot validate
without them.

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable

from test_entity_schema import _tokens, mutate

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTITY_SCHEMA = json.loads((REPO_ROOT / "schemas/entities.schema.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((REPO_ROOT / "schemas/relationships.schema.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((REPO_ROOT / "tests/fixtures/relationships.json").read_text(encoding="utf-8"))

REGISTRY = Registry().with_resource(ENTITY_SCHEMA["$id"], Resource.from_contents(ENTITY_SCHEMA))


def error_paths(errors) -> set[tuple]:
    """Instance paths of every error, including those nested in anyOf/oneOf context."""
    paths: set[tuple] = set()
    stack = list(errors)
    while stack:
        error = stack.pop()
        paths.add(tuple(error.absolute_path))
        stack.extend(error.context)
    return paths


def pointer_path(pointer: str) -> tuple:
    return tuple(int(t) if t.isdigit() else t for t in _tokens(pointer))


class RelationshipSchemaTests(unittest.TestCase):
    validator = Draft202012Validator(SCHEMA, registry=REGISTRY)

    def errors(self, record: dict) -> list:
        return list(self.validator.iter_errors(record))

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(SCHEMA)

    def test_relative_refs_resolve_to_the_entity_schema(self) -> None:
        base = SCHEMA["$id"].rsplit("/", 1)[0]
        self.assertEqual(f"{base}/entities.schema.json", ENTITY_SCHEMA["$id"])

    def test_cross_file_refs_are_really_used(self) -> None:
        # Without the entity schema in the registry, validation cannot proceed: the
        # shared definitions live only there.
        bare = Draft202012Validator(SCHEMA)
        with self.assertRaises(Unresolvable):
            list(bare.iter_errors(FIXTURES["valid"]["fabricates"]))

    def test_valid_fixtures_pass(self) -> None:
        for name, record in FIXTURES["valid"].items():
            with self.subTest(fixture=name):
                self.assertEqual([e.message for e in self.errors(record)], [])

    def test_every_relation_type_has_a_valid_fixture(self) -> None:
        types = {item["const"] for item in SCHEMA["$defs"]["vocab_relation_type"]["oneOf"]}
        covered = {record["relation_type"] for record in FIXTURES["valid"].values()}
        self.assertEqual(types - covered, set())

    def test_invalid_mutations_fail_where_they_mutate(self) -> None:
        names = [case["case"] for case in FIXTURES["invalid"]]
        self.assertEqual(len(names), len(set(names)), "invalid case names must be unique")
        for case in FIXTURES["invalid"]:
            with self.subTest(case=case["case"], why=case["why"]):
                base = FIXTURES["valid"][case["base"]]
                mutated = mutate(base, case)
                self.assertNotEqual(mutated, base, "mutation changed nothing")
                errors = self.errors(mutated)
                self.assertNotEqual(errors, [], "mutated record was accepted")
                pointers = list(case.get("set", {})) + list(case.get("remove", []))
                self.assertEqual(len(pointers), 1, "one mutation per case")
                path = pointer_path(pointers[0])
                located = [
                    p for p in error_paths(errors) if p[: len(path)] == path or p == path[:-1]
                ]
                self.assertTrue(
                    located,
                    f"no error at, under or beside {pointers[0]}: {[e.message for e in errors]}",
                )

    def test_required_generic_verbs_are_rejected(self) -> None:
        # Acceptance criterion 4 (Part B §15): associated_with and its generic synonyms.
        rejected = {
            case["set"]["/relation_type"]
            for case in FIXTURES["invalid"]
            if "/relation_type" in case.get("set", {})
        }
        for verb in ("associated_with", "related_to", "linked_to", "connected_to", "involved_with"):
            with self.subTest(verb=verb):
                self.assertIn(verb, rejected)


if __name__ == "__main__":
    unittest.main()
