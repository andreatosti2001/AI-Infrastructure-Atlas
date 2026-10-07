"""Behaviour tests for schemas/claims.schema.json (S06; D-044 to D-049, D-026).

- Valid fixtures pass, and cover every claim type and evidence status.
- Each invalid case is one JSON Pointer mutation of a valid base record, and fails at,
  under or beside its pointer (S04 pattern).
- The type × status table in docs/architecture/claim-model.md §4 matches the schema's
  behaviour: for every claim type and every evidence status, a probe record is accepted
  exactly when the table allows the pair, and the "sources" and "input claims" columns
  hold (acceptance criterion 3).

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import copy
import unittest

from jsonschema import Draft202012Validator
from referencing.exceptions import Unresolvable

from test_claim_model import TYPES, STATUSES, rule_rows
from test_source_record_schema import CLAIM_SCHEMA, check_mutations, load, validator

FIXTURES = load("tests/fixtures/claims.json")
VALID = FIXTURES["valid"]


def probe(claim_type: str, status: str) -> dict:
    """A minimal record of the given type and status, built from the valid fixtures."""
    base = {
        "FACT": "fact",
        "ATTRIBUTION": "attribution_definition",
        "DERIVATION": "derivation",
        "INTERPRETATION": "interpretation",
        "IMPLICATION": "implication",
    }[claim_type]
    record = copy.deepcopy(VALID[base])
    record["evidence_status"] = status
    if status == "unverified":
        record.pop("verified_on", None)
        for citation in record.get("citations", []):
            citation.pop("read", None)
    if status == "disputed":
        record["disputed_with"] = ["claim-fixture-999"]
    return record


class ClaimSchemaTests(unittest.TestCase):
    check = validator(CLAIM_SCHEMA)

    def errors(self, record: dict) -> list[str]:
        return [e.message for e in self.check.iter_errors(record)]

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(CLAIM_SCHEMA)

    def test_cross_file_refs_are_really_used(self) -> None:
        with self.assertRaises(Unresolvable):
            list(Draft202012Validator(CLAIM_SCHEMA).iter_errors(VALID["fact"]))

    def test_valid_fixtures_pass(self) -> None:
        for name, record in VALID.items():
            with self.subTest(fixture=name):
                self.assertEqual(self.errors(record), [])

    def test_valid_fixtures_cover_every_type_and_status(self) -> None:
        self.assertEqual({r["claim_type"] for r in VALID.values()}, TYPES)
        self.assertEqual({r["evidence_status"] for r in VALID.values()}, STATUSES)
        standings = {c["standing"] for r in VALID.values() for c in r.get("citations", [])}
        self.assertEqual(standings, {"party", "originator", "reporter"})

    def test_invalid_mutations_fail_where_they_mutate(self) -> None:
        check_mutations(self, self.check, FIXTURES)

    def test_a_citation_may_record_its_third_party_criteria(self) -> None:
        # S16.6 (R-5, D-147): a third-party citation records whether its publisher is internationally recognised
        # as reliable and independent of the parties, each with a reason; a malformed record is refused.
        fact = copy.deepcopy(VALID["fact"])
        good = {"recognised": {"met": True, "reason": "an established teardown laboratory"},
                "independent": {"met": False, "reason": "commissioned by a party"}}
        fact["citations"][0]["third_party_criteria"] = good
        self.assertEqual(self.errors(fact), [])
        for bad in ({"recognised": {"met": True, "reason": "x"}},
                    {"recognised": {"met": "yes", "reason": "x"}, "independent": {"met": True, "reason": "x"}},
                    {"recognised": {"met": True}, "independent": {"met": True, "reason": "x"}},
                    dict(good, recent=True)):
            fact["citations"][0]["third_party_criteria"] = bad
            with self.subTest(criteria=bad):
                self.assertNotEqual(self.errors(fact), [])

    def test_review_may_be_recorded_in_a_sub_session_report(self) -> None:
        # S16.5 (D-142): a review is recorded in the report of the session that took it, sub-sessions
        # included, with D-126's one-digit suffix; anything else stays refused.
        accepted = next(r for r in VALID.values() if isinstance(r.get("review"), dict) and r["review"].get("verdict") == "accepted")
        for path, ok in (("sessions/reports/SESSION-16.5-REPORT.md", True), ("sessions/reports/SESSION-16-REPORT.md", True),
                         ("sessions/reports/SESSION-16.55-REPORT.md", False), ("sessions/reports/SESSION-16.x-REPORT.md", False)):
            record = copy.deepcopy(accepted)
            record["review"]["recorded_in"] = path
            with self.subTest(recorded_in=path):
                self.assertEqual(self.errors(record) == [], ok, self.errors(record))

    def test_type_by_status_table_matches_the_schema(self) -> None:
        rows = rule_rows()
        self.assertEqual(set(rows), TYPES)
        for claim_type, row in rows.items():
            for status in sorted(STATUSES):
                with self.subTest(type=claim_type, status=status):
                    accepted = self.errors(probe(claim_type, status)) == []
                    self.assertEqual(accepted, status in row["statuses"])

    def test_sources_and_inputs_columns_match_the_schema(self) -> None:
        cite = VALID["fact"]["citations"]
        for claim_type, row in rule_rows().items():
            with self.subTest(type=claim_type):
                record = probe(claim_type, "supported")
                with_sources = dict(record, citations=copy.deepcopy(cite))
                without_sources = {k: v for k, v in record.items() if k != "citations"}
                with_inputs = dict(record, input_claim_ids=["claim-fixture-205"])
                without_inputs = {k: v for k, v in record.items() if k != "input_claim_ids"}
                if row["sources"] == "required":
                    self.assertNotEqual(self.errors(without_sources), [])
                    self.assertEqual(self.errors(with_sources), [])
                else:
                    self.assertNotEqual(self.errors(with_sources), [])
                if row["inputs"] == "required":
                    self.assertNotEqual(self.errors(without_inputs), [])
                    self.assertEqual(self.errors(with_inputs), [])
                elif row["inputs"] == "forbidden":
                    self.assertNotEqual(self.errors(with_inputs), [])

    def test_standing_column_matches_the_schema(self) -> None:
        for claim_type, row in rule_rows().items():
            if row["sources"] != "required":
                continue
            for standing in ("party", "originator", "reporter"):
                with self.subTest(type=claim_type, standing=standing):
                    record = probe(claim_type, "supported")
                    citation = record["citations"][0]
                    citation["standing"] = standing
                    citation.pop("originator", None)
                    if standing == "reporter":
                        citation["originator"] = VALID["attribution_chain"]["citations"][0]["originator"]
                    self.assertEqual(self.errors(record) == [], standing in row["standing"])

    def test_no_numeric_value_anywhere_in_the_vocabularies(self) -> None:
        # NG-11: no score, rank or confidence value can be expressed.
        for name, definition in CLAIM_SCHEMA["$defs"].items():
            if name.startswith("vocab_"):
                for item in definition["oneOf"]:
                    with self.subTest(vocabulary=name, value=item["const"]):
                        self.assertIsInstance(item["const"], str)


if __name__ == "__main__":
    unittest.main()
