"""validate-data, part 2: schema validity of every record in data/ (S06; D-051).

VD-2: every source record is valid against schemas/sources.schema.json, every claim
(staging and canonical) against schemas/claims.schema.json, and, from S07, every company
and jurisdiction record (staging and canonical) against schemas/entities.schema.json, with
cross-file references resolved. From S09, facility records against the same schema, and every
event (staging and canonical) against schemas/events.schema.json (proposed, D-083). From S10,
every edge (staging and canonical) against the unchanged schemas/relationships.schema.json. Uses the
pinned jsonschema (D-026); tools/ stays standard library (H-4).

Requires the pinned test dependencies: pip install -r requirements-test.txt
"""

import copy
import json
import unittest
from pathlib import Path

from test_data_entities import FIXTURES as ENTITY_FIXTURES, ENTITY_KINDS, entity_files
from test_data_integrity import CANONICAL_FILE, SOURCES_FILE, STAGING_FILE, load_records
from test_data_events import event_files
from test_data_relationships import EDGE_FIXTURES, edge_files
from test_source_record_schema import CLAIM_SCHEMA, ENTITY_SCHEMA, SOURCE_SCHEMA, validator

EVENT_SCHEMA = json.loads((Path(__file__).resolve().parent.parent / "schemas/events.schema.json").read_text(encoding="utf-8"))
REL_SCHEMA = json.loads((Path(__file__).resolve().parent.parent / "schemas/relationships.schema.json").read_text(encoding="utf-8"))


class DataSchemaTests(unittest.TestCase):
    def test_vd2_every_record_is_valid(self) -> None:
        files = [(SOURCES_FILE, SOURCE_SCHEMA), (STAGING_FILE, CLAIM_SCHEMA)]
        if CANONICAL_FILE.exists():
            files.append((CANONICAL_FILE, CLAIM_SCHEMA))
        for kind in ENTITY_KINDS:  # S07: company and jurisdiction records (L-05)
            files += [(path, ENTITY_SCHEMA) for path in entity_files(kind) if path.exists()]
        files += [(path, EVENT_SCHEMA) for path in event_files() if path.exists()]  # S09
        files += [(path, REL_SCHEMA) for path in edge_files() if path.exists()]  # S10
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
        groups += [(f"{where} events", EVENT_SCHEMA, world["events"][where]) for where in ("canonical", "staging")]
        for name, schema, records in groups:
            check = validator(schema)
            for record in records:
                with self.subTest(group=name, record=record.get("id")):
                    self.assertEqual([f"{list(e.absolute_path)}: {e.message}" for e in check.iter_errors(record)], [])

    def test_edge_fixture_world_is_valid(self) -> None:
        # The fictional edges, and the sources and claims they add, are valid records (S10).
        valid = EDGE_FIXTURES["valid"]
        groups = [("sources", SOURCE_SCHEMA, valid["sources"]), ("claims", CLAIM_SCHEMA, valid["staging_claims"] + valid["canonical_claims"])]
        groups += [(f"{where} edges", REL_SCHEMA, valid["relationships"][where]) for where in ("canonical", "staging")]
        groups += [(f"warning {case['name']}", REL_SCHEMA, [case["record"]]) for case in EDGE_FIXTURES["warnings"]]
        for name, schema, records in groups:
            check = validator(schema)
            for record in records:
                with self.subTest(group=name, record=record.get("id")):
                    self.assertEqual([f"{list(e.absolute_path)}: {e.message}" for e in check.iter_errors(record)], [])


class FacilityAndEventShapeTests(unittest.TestCase):
    """What the schemas themselves forbid (facility-dataset.md §5, §6, §7)."""

    def setUp(self) -> None:
        world = ENTITY_FIXTURES["valid"]
        self.facility = copy.deepcopy(world["entities"]["canonical"]["facilities"][0])
        self.plan = copy.deepcopy(world["events"]["staging"][1])
        self.opening = copy.deepcopy(world["events"]["canonical"][0])

    def test_an_owner_or_operator_is_never_a_facility_field(self) -> None:
        for field in ("owner", "operator", "owned_by", "status"):
            with self.subTest(field=field):
                record = dict(self.facility, **{field: "company-example-designer"})
                self.assertTrue(list(validator(ENTITY_SCHEMA).iter_errors(record)))

    def test_events_store_no_status_and_no_planned_date(self) -> None:
        for field in ("status", "planned_date", "owner"):
            with self.subTest(field=field):
                self.assertTrue(list(validator(EVENT_SCHEMA).iter_errors(dict(self.opening, **{field: "x"}))))

    def test_an_announced_event_may_have_a_company_subject_and_an_occurrence_may_not(self) -> None:
        check = validator(EVENT_SCHEMA)
        self.assertEqual(list(check.iter_errors(self.plan)), [])
        self.assertTrue(list(check.iter_errors(dict(self.plan, event_type="opened"))))
        self.assertTrue(list(check.iter_errors(dict(self.opening, event_type="planned"))))


if __name__ == "__main__":
    unittest.main()
