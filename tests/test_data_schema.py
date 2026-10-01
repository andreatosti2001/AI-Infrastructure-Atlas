"""validate-data, part 2: schema validity of every record in data/ (S06; D-051).

VD-2: every source record is valid against schemas/sources.schema.json, every claim
(staging and canonical) against schemas/claims.schema.json, and, from S07, every company
and jurisdiction record (staging and canonical) against schemas/entities.schema.json, with
cross-file references resolved. Uses the pinned jsonschema (D-026); tools/ stays standard library (H-4).

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import unittest

from test_data_entities import FIXTURES as ENTITY_FIXTURES, ENTITY_KINDS, entity_files
from test_data_integrity import CANONICAL_FILE, SOURCES_FILE, STAGING_FILE, load_records
from test_source_record_schema import CLAIM_SCHEMA, ENTITY_SCHEMA, SOURCE_SCHEMA, validator


class DataSchemaTests(unittest.TestCase):
    def test_vd2_every_record_is_valid(self) -> None:
        files = [(SOURCES_FILE, SOURCE_SCHEMA), (STAGING_FILE, CLAIM_SCHEMA)]
        if CANONICAL_FILE.exists():
            files.append((CANONICAL_FILE, CLAIM_SCHEMA))
        for kind in ENTITY_KINDS:  # S07: company and jurisdiction records (L-05)
            files += [(path, ENTITY_SCHEMA) for path in entity_files(kind) if path.exists()]
        for path, schema in files:
            check = validator(schema)
            for record in load_records(path):
                with self.subTest(file=path.name, record=record.get("id")):
                    self.assertEqual([f"{list(e.absolute_path)}: {e.message}" for e in check.iter_errors(record)], [])

    def test_entity_fixture_world_is_valid(self) -> None:
        # The fictional world the S07 checks run on must itself be valid records.
        world = ENTITY_FIXTURES["valid"]
        groups = [("sources", SOURCE_SCHEMA, world["sources"]), ("claims", CLAIM_SCHEMA, world["staging_claims"] + world["canonical_claims"])]
        groups += [(f"{where} {kind}", ENTITY_SCHEMA, world["entities"][where][kind]) for where in ("canonical", "staging") for kind in ENTITY_KINDS]
        for name, schema, records in groups:
            check = validator(schema)
            for record in records:
                with self.subTest(group=name, record=record.get("id")):
                    self.assertEqual([f"{list(e.absolute_path)}: {e.message}" for e in check.iter_errors(record)], [])


if __name__ == "__main__":
    unittest.main()
