"""validate-data, part 2: schema validity of every record in data/ (S06; D-051).

VD-2: every source record is valid against schemas/sources.schema.json and every claim
(staging and canonical) against schemas/claims.schema.json, with cross-file references
resolved. Uses the pinned jsonschema (D-026); tools/ stays standard library (H-4).

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import unittest

from test_data_integrity import CANONICAL_FILE, SOURCES_FILE, STAGING_FILE, load_records
from test_source_record_schema import CLAIM_SCHEMA, SOURCE_SCHEMA, validator


class DataSchemaTests(unittest.TestCase):
    def test_vd2_every_record_is_valid(self) -> None:
        files = [(SOURCES_FILE, SOURCE_SCHEMA), (STAGING_FILE, CLAIM_SCHEMA)]
        if CANONICAL_FILE.exists():
            files.append((CANONICAL_FILE, CLAIM_SCHEMA))
        for path, schema in files:
            check = validator(schema)
            for record in load_records(path):
                with self.subTest(file=path.name, record=record.get("id")):
                    self.assertEqual([f"{list(e.absolute_path)}: {e.message}" for e in check.iter_errors(record)], [])


if __name__ == "__main__":
    unittest.main()
