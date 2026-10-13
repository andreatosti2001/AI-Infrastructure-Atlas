"""The policy layer's cross-cutting rules (S17; docs/architecture/policy-dataset.md; D-154 to D-164).

- PL-8 the source class `official_legal_text` exists; every policy row of source-policy.md §7 prefers it;
       only it may support a policy's dates and repeal (government publications such as press releases are
       never sufficient alone for them); every row that existed before S17 places it under "never
       sufficient alone", so no earlier check is loosened (P-6, D-158);
- the links S18 may record are defined once, in policy-dataset.md P-8, and the rejected verbs stay rejected;
- PK-1 a `restricts` link (policy-links.md K-1, K-3, K-4): its level is `policy`; it goes from a policy to a
       component or technology; it carries no dates, `item` or `supplier`;
- PK-2 a policy is an endpoint only as the source of `restricts` (replaces S17's PL-9, which refused every
       policy endpoint until S18); the data check of PK-2 (no link from a proposed rule) is in
       tests/test_data_relationships.py;
- PK-5 the row `rel:restricts` prefers only `official_legal_text`, accepts nothing else, and needs originator
       standing (K-6).

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


LINK_ROWS = {"rel:restricts"}  # S18 (K-6): the policy link's row also prefers the official text


def policy_row(key: str) -> bool:
    return key.startswith(("identity:policy", "attr:policy.")) or key in DATE_ROWS


def relationship_validator() -> Draft202012Validator:
    registry = Registry().with_resource(ENTITY_SCHEMA["$id"], Resource.from_contents(ENTITY_SCHEMA))
    return Draft202012Validator(REL_SCHEMA, registry=registry)


def link(**changes) -> dict:
    record = {
        "id": "rel-policy-us-fr-2024-28270-restricts-component-high-bandwidth-memory",
        "relation_type": "restricts",
        "source_entity": "policy-us-fr-2024-28270",
        "target_entity": "component-high-bandwidth-memory",
        "claim_ids": ["claim-test-attribution", "claim-test-derivation"],
    }
    record.update(changes)
    return record


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
            if not policy_row(key) and key not in LINK_ROWS:
                with self.subTest(row=key):
                    self.assertIn(LEGAL, column_classes(row[3]))


class LinkShapeTests(unittest.TestCase):
    """PK-1 and PK-2: what the schema admits."""

    def setUp(self) -> None:
        self.check = relationship_validator()

    def errors(self, record: dict) -> list:
        return list(self.check.iter_errors(record))

    def test_pk1_restricts_is_the_policy_level(self) -> None:
        vocab = {v["const"]: v for v in REL_SCHEMA["$defs"]["vocab_relation_type"]["oneOf"]}
        self.assertIn("restricts", vocab)
        self.assertEqual(vocab["restricts"]["x-level"], "policy")
        self.assertEqual([t for t, v in vocab.items() if v["x-level"] == "policy"], ["restricts"])
        self.assertEqual(vocab["restricts"]["x-inverse-reading"], "named among the items controlled by")

    def test_pk1_a_link_to_a_component_or_technology_is_admitted(self) -> None:
        self.assertEqual(self.errors(link()), [])
        self.assertEqual(self.errors(link(target_entity="technology-euv-lithography")), [])

    def test_pk1_a_product_or_company_target_is_refused_until_its_evidence_row_exists(self) -> None:
        for target in ("product-micron-technology-hbm4-36gb-12h", "company-micron-technology", "jurisdiction-us", "facility-kr-m16", "policy-us-15-cfr-730-774"):
            with self.subTest(target=target):
                self.assertNotEqual(self.errors(link(target_entity=target)), [])

    def test_pk1_a_link_carries_no_dates_item_or_supplier(self) -> None:
        for field, value in (("valid_from", "2024-12"), ("valid_to", "2025-01"), ("item", "component-ai-asic"), ("supplier", {"state": "not_researched"})):
            with self.subTest(field=field):
                self.assertNotEqual(self.errors(link(**{field: value})), [])

    def test_pk2_only_restricts_starts_from_a_policy(self) -> None:
        base = json.loads((REPO_ROOT / "data/relationships.json").read_text(encoding="utf-8"))[0]
        self.assertEqual(self.errors(base), [], "the base relationship must be valid")
        for end in ("source_entity", "target_entity"):
            with self.subTest(end=end):
                record = copy.deepcopy(base)
                record[end] = "policy-us-fr-2022-21658"
                self.assertNotEqual(self.errors(record), [])
        self.assertNotEqual(self.errors(link(source_entity="company-micron-technology")), [], "restricts from a company")
        self.assertNotEqual(self.errors(link(source_entity="component-ai-asic")), [], "restricts from a class")

    def test_pk2_supports_is_not_instantiable(self) -> None:
        self.assertNotEqual(self.errors(link(relation_type="supports", target_entity="company-micron-technology")), [])


class LinkRowTests(unittest.TestCase):
    """PK-5: the evidence row of the policy link (K-6)."""

    def test_pk5_restricts_rests_on_the_official_text_only(self) -> None:
        table = rows()
        self.assertIn("rel:restricts", table)
        row = table["rel:restricts"]
        self.assertEqual(column_classes(row[1]), [LEGAL])
        self.assertEqual(column_classes(row[2]), [])
        self.assertEqual(row[4], "originator")
        self.assertEqual(row[5], "stable")
        classes = {item["const"] for item in SOURCE_SCHEMA["$defs"]["vocab_source_class"]["oneOf"]}
        self.assertEqual(set(column_classes(row[3])), classes - {LEGAL})


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
