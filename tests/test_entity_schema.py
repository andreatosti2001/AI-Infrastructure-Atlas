"""Behaviour tests for schemas/entities.schema.json (S03; D-025, D-026).

Valid fixtures must pass. Each invalid case is one JSON Pointer mutation of a valid
base record and must fail, so a case can only fail for the reason it names.

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((REPO_ROOT / "schemas/entities.schema.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((REPO_ROOT / "tests/fixtures/entities.json").read_text(encoding="utf-8"))


def _tokens(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"not a JSON Pointer: {pointer!r}")
    return [t.replace("~1", "/").replace("~0", "~") for t in pointer[1:].split("/")]


def _parent(doc, pointer: str):
    *path, last = _tokens(pointer)
    node = doc
    for token in path:
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node, (int(last) if isinstance(node, list) else last)


def mutate(record: dict, case: dict) -> dict:
    result = copy.deepcopy(record)
    for pointer, value in case.get("set", {}).items():
        node, key = _parent(result, pointer)
        node[key] = value
    for pointer in case.get("remove", []):
        node, key = _parent(result, pointer)
        del node[key]
    return result


class EntitySchemaTests(unittest.TestCase):
    validator = Draft202012Validator(SCHEMA)

    def errors(self, record: dict) -> list[str]:
        return [e.message for e in self.validator.iter_errors(record)]

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(SCHEMA)

    def test_valid_fixtures_pass(self) -> None:
        for name, record in FIXTURES["valid"].items():
            with self.subTest(fixture=name):
                self.assertEqual(self.errors(record), [])

    def test_every_instantiable_type_has_a_valid_fixture(self) -> None:
        types = {item["const"] for item in SCHEMA["$defs"]["vocab_entity_type"]["oneOf"]}
        covered = {record["type"] for record in FIXTURES["valid"].values()}
        self.assertEqual(types - covered, set())

    def test_invalid_mutations_fail(self) -> None:
        names = [case["case"] for case in FIXTURES["invalid"]]
        self.assertEqual(len(names), len(set(names)), "invalid case names must be unique")
        for case in FIXTURES["invalid"]:
            with self.subTest(case=case["case"], why=case["why"]):
                base = FIXTURES["valid"][case["base"]]
                mutated = mutate(base, case)
                self.assertNotEqual(mutated, base, "mutation changed nothing")
                self.assertNotEqual(self.errors(mutated), [], "mutated record was accepted")


if __name__ == "__main__":
    unittest.main()
