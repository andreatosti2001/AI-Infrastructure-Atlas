"""Behaviour tests for the source_class vocabulary in schemas/sources.schema.json (S05; D-034).

Since S06 the schema's root is the source record (D-050), tested in
test_source_record_schema.py; the vocabulary is unchanged in $defs and is tested here on
its own. Every class must be accepted, and each invalid value must be rejected. The error
must come from the vocabulary itself, so a value cannot fail for an unrelated reason.

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((REPO_ROOT / "schemas/sources.schema.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((REPO_ROOT / "tests/fixtures/sources.json").read_text(encoding="utf-8"))
CLASSES = [item["const"] for item in SCHEMA["$defs"]["vocab_source_class"]["oneOf"]]


class SourceClassSchemaTests(unittest.TestCase):
    validator = Draft202012Validator(SCHEMA["$defs"]["vocab_source_class"])

    def errors(self, value) -> list:
        return list(self.validator.iter_errors(value))

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(SCHEMA)

    def test_valid_fixtures_are_exactly_the_classes(self) -> None:
        self.assertEqual(len(FIXTURES["valid"]), len(set(FIXTURES["valid"])))
        self.assertEqual(set(FIXTURES["valid"]), set(CLASSES))
        for value in FIXTURES["valid"]:
            with self.subTest(value=value):
                self.assertEqual(self.errors(value), [])

    def test_invalid_values_fail_in_the_vocabulary(self) -> None:
        names = [case["case"] for case in FIXTURES["invalid"]]
        self.assertEqual(len(names), len(set(names)), "invalid case names must be unique")
        for case in FIXTURES["invalid"]:
            with self.subTest(case=case["case"], why=case["why"]):
                self.assertNotIn(case["value"], CLASSES)
                errors = self.errors(case["value"])
                self.assertNotEqual(errors, [], "invalid value was accepted")
                # Every error is about the value itself, and the class list rejects it.
                self.assertEqual({tuple(error.absolute_path) for error in errors}, {()})
                self.assertLessEqual({error.validator for error in errors}, {"oneOf", "type"})
                self.assertIn("oneOf", {error.validator for error in errors})


if __name__ == "__main__":
    unittest.main()
