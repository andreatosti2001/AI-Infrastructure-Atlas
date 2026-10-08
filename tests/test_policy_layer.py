"""The policy layer's cross-cutting rules (S17; docs/architecture/policy-dataset.md; D-154 to D-164).

- PL-8 the source class `official_legal_text` exists; every policy row of source-policy.md §7 prefers it;
       only it may support a policy's dates and repeal (government publications such as press releases are
       never sufficient alone for them); every row that existed before S17 places it under "never
       sufficient alone", so no earlier check is loosened (P-6, D-158);
- PL-9 no relationship has a policy endpoint before S18 (P-8, D-160): the relationship schema refuses it;
- the links S18 may record are defined once, in policy-dataset.md P-8, and the rejected verbs stay rejected.

Requires the pinned test dependencies (jsonschema).
"""

import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from test_source_policy import column_classes, matrix_rows

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_SCHEMA = json.loads((REPO_ROOT / "schemas/sources.schema.json").read_text(encoding="utf-8"))
REL_SCHEMA = json.loads((REPO_ROOT / "schemas/relationships.schema.json").read_text(encoding="utf-8"))
ENTITY_SCHEMA = json.loads((REPO_ROOT / "schemas/entities.schema.json").read_text(encoding="utf-8"))
POLICY_DATASET = (REPO_ROOT / "docs/architecture/policy-dataset.md").read_text(encoding="utf-8")

LEGAL = "official_legal_text"
DATE_ROWS = {"event:published", "event:effective", "event:repealed"}


def rows() -> dict[str, list[str]]:
    return {re.findall(r"`([^`]+)`", row[0])[0]: row for row in matrix_rows()}


def policy_row(key: str) -> bool:
    return key.startswith(("identity:policy", "attr:policy.")) or key in DATE_ROWS


class SourceClassTests(unittest.TestCase):
    def test_pl8_official_legal_text_is_a_class(self) -> None:
        self.assertIn(LEGAL, {item["const"] for item in SOURCE_SCHEMA["$defs"]["vocab_source_class"]["oneOf"]})

    def test_pl8_every_policy_row_prefers_the_official_text(self) -> None:
        table = rows()
        policy_keys = {k for k in table if policy_row(k)}
        fields = {f for f in ENTITY_SCHEMA["$defs"]["policy"]["properties"] if ENTITY_SCHEMA["$defs"]["policy"]["properties"][f].get("$ref", "").startswith("#/$defs/attr_")}
        self.assertEqual(policy_keys, {"identity:policy"} | {f"attr:policy.{f}" for f in fields} | DATE_ROWS)
        for key in sorted(policy_keys):
            with self.subTest(row=key):
                self.assertEqual(column_classes(table[key][1]), [LEGAL])

    def test_pl8_only_the_official_text_dates_or_repeals_an_act(self) -> None:
        table = rows()
        for key in sorted(DATE_ROWS):
            with self.subTest(row=key):
                self.assertIn("government_publication", column_classes(table[key][3]))

    def test_pl8_rows_before_s17_never_rest_on_legal_text_alone(self) -> None:
        for key, row in rows().items():
            if not policy_row(key):
                with self.subTest(row=key):
                    self.assertIn(LEGAL, column_classes(row[3]))


class EndpointTests(unittest.TestCase):
    def test_pl9_no_relationship_has_a_policy_endpoint(self) -> None:
        registry = Registry().with_resource(ENTITY_SCHEMA["$id"], Resource.from_contents(ENTITY_SCHEMA))
        validator = Draft202012Validator(REL_SCHEMA, registry=registry)
        base = json.loads((REPO_ROOT / "data/relationships.json").read_text(encoding="utf-8"))[0]
        self.assertEqual(list(validator.iter_errors(base)), [], "the base relationship must be valid")
        for end in ("source_entity", "target_entity"):
            with self.subTest(end=end):
                record = copy.deepcopy(base)
                record[end] = "policy-us-fr-2022-21658"
                self.assertNotEqual(list(validator.iter_errors(record)), [])


class LinkDefinitionTests(unittest.TestCase):
    def test_s18_links_are_defined_once_and_the_vague_verbs_rejected(self) -> None:
        body = POLICY_DATASET[POLICY_DATASET.index("## P-8") : POLICY_DATASET.index("## P-9")]
        verdicts = {}
        for line in body.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
            if len(cells) >= 2 and re.fullmatch(r"`[a-z_]+`", cells[0]):
                verdicts[cells[0].strip("`")] = cells[1]
        self.assertEqual(set(verdicts), {"restricts", "supports", "regulated_by", "constrained_by"})
        self.assertIn("define", verdicts["restricts"])
        self.assertIn("define", verdicts["supports"])
        self.assertIn("reject", verdicts["regulated_by"])
        self.assertIn("reject", verdicts["constrained_by"])


if __name__ == "__main__":
    unittest.main()
