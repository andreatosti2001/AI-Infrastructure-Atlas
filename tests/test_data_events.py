"""validate-data, part 4: facility event records (S09; facility-dataset.md §6, §11; D-083).

Checks the events in data/events.json (canonical) and data/staging/events.json (staging)
against the entity records, the claims and the sources. Standard library only; schema
validity of the events is part 2 (tests/test_data_schema.py). The checks, by ID:

- EV-1 the subject resolves to a facility, company or (S17) policy record and every claim resolves; a
       canonical event cites only canonical claims and has a canonical subject; event IDs
       are unique, and none is both staging and canonical;
- EV-2 a plan is never an occurrence: an occurrence (the schema's `x-occurrence` types) has
       the subject its type names (`x-subject`: a facility, or from S17 a policy) and rests on
       at least one FACT or DERIVATION; an announced event cites ATTRIBUTION claims only (ER-8);
- EV-3 no event is dated after a source that states it: its date is no later than each
       cited source's latest stated date (or, undated, its access date), at the coarser
       precision. One exception (D-164): an `effective` event may be dated after a citation
       whose source is the act's own official text (an `official_legal_text` cited by the
       subject policy's identity claims), because an act fixes its own effective date;
- PL-6 (S17) a `proposed_rule` has no `effective` or `repealed` event: a proposal never takes
       effect (policy-dataset.md P-4, D-156);
- EV-4 V-10 for events: the claims rest on at least one citation whose class and standing
       the `event:<type>` row of source-policy.md §7 allows;
- EI-1 an event ID is `event-`, the subject's ID without its type prefix, the event type
       and the date as recorded.

The check functions take record lists, so the same checks run on the fictional fixtures.
"""

import copy
import json
import unittest
from pathlib import Path

from test_data_entities import FIXTURES, all_records, coarse, fixture_world, leaf_citations, load_entities, matrix
from test_data_integrity import DATA, load_data, load_records

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENT_SCHEMA = json.loads((REPO_ROOT / "schemas/events.schema.json").read_text(encoding="utf-8"))
EVENT_TYPES = EVENT_SCHEMA["$defs"]["vocab_event_type"]["oneOf"]
OCCURRENCES = {item["const"] for item in EVENT_TYPES if item["x-occurrence"]}
SUBJECT = {item["const"]: item["x-subject"] for item in EVENT_TYPES if item["x-occurrence"]}
NEVER_FOR_PROPOSALS = ("effective", "repealed")


def event_files() -> tuple[Path, Path]:
    """(canonical, staging) paths of the event files (H-5 layout)."""
    return DATA / "events.json", DATA / "staging" / "events.json"


def load_events() -> dict:
    canonical, staging = event_files()
    return {
        "canonical": load_records(canonical) if canonical.exists() else [],
        "staging": load_records(staging) if staging.exists() else [],
    }


def all_events(events) -> list[tuple[str, dict]]:
    return [(where, e) for where in ("canonical", "staging") for e in events[where]]


def source_date(source: dict) -> str:
    dates = source["stated_dates"]
    if isinstance(dates, list):
        return max(d["date"] for d in dates)
    return source["retrieval"]["accessed_at"][:10]


def check_event_references(events, entities, staging_claims, canonical_claims) -> list[str]:
    """EV-1."""
    canonical_claim_ids = {c["id"] for c in canonical_claims}
    claim_ids = canonical_claim_ids | {c["id"] for c in staging_claims}
    subjects = {r["id"]: where for where, r in all_records(entities) if r["type"] in ("facility", "company", "policy")}
    errors = []
    seen = {}
    for where, event in all_events(events):
        if event["id"] in seen:
            errors.append(f"{event['id']} is defined twice ({seen[event['id']]} and {where})")
        seen[event["id"]] = where
        if event["subject"] not in subjects:
            errors.append(f"{event['id']}: subject {event['subject']} does not exist")
        elif where == "canonical" and subjects[event["subject"]] != "canonical":
            errors.append(f"canonical {event['id']} has non-canonical subject {event['subject']}")
        for claim_id in event["claim_ids"]:
            if claim_id not in claim_ids:
                errors.append(f"{event['id']} cites missing claim {claim_id}")
            elif where == "canonical" and claim_id not in canonical_claim_ids:
                errors.append(f"canonical {event['id']} cites staging claim {claim_id}")
    return errors


def check_plans(events, staging_claims, canonical_claims) -> list[str]:
    """EV-2."""
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for _, event in all_events(events):
        types = {cid: claims.get(cid, {}).get("claim_type") for cid in event["claim_ids"]}
        if event["event_type"] in OCCURRENCES:
            kind = SUBJECT[event["event_type"]]
            if not event["subject"].startswith(f"{kind}-"):
                errors.append(f"{event['id']}: an occurrence needs a {kind} subject, not {event['subject']}")
            if not any(t in ("FACT", "DERIVATION") for t in types.values()):
                errors.append(f"{event['id']}: a {event['event_type']} event rests on no FACT or DERIVATION (a plan is not an occurrence, ER-8)")
        else:
            errors += [f"{event['id']}: announced event cites {cid}, which is not an ATTRIBUTION" for cid, t in types.items() if t != "ATTRIBUTION"]
    return errors


def own_texts(entities, claims: dict, sources_by_id: dict) -> dict[str, set[str]]:
    """policy ID -> its own official texts: the official_legal_text sources its identity claims cite (D-164)."""
    result = {}
    for _, record in all_records(entities):
        if record["type"] == "policy":
            cited = {c["source_id"] for cid in record["identity_claim_ids"] for _, c in leaf_citations(cid, claims)}
            result[record["id"]] = {s for s in cited if sources_by_id.get(s, {}).get("source_class") == "official_legal_text"}
    return result


def check_event_dates(events, sources, staging_claims, canonical_claims, entities=None) -> list[str]:
    """EV-3."""
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    by_id = {s["id"]: s for s in sources}
    own = own_texts(entities if entities is not None else load_entities(), claims, by_id)
    errors = []
    for _, event in all_events(events):
        for claim_id in event["claim_ids"]:
            for _, citation in leaf_citations(claim_id, claims):
                source = by_id.get(citation["source_id"])
                if source is None:
                    continue
                if event["event_type"] == "effective" and source["id"] in own.get(event["subject"], set()):
                    continue  # D-164: the act fixes its own effective date
                stated = source_date(source)
                if coarse(event["date"], stated) > coarse(stated, event["date"]):
                    errors.append(f"{event['id']}: dated {event['date']}, after {source['id']}, which states it on {stated}")
    return errors


def check_event_matrix(events, sources, staging_claims, canonical_claims) -> list[str]:
    """EV-4."""
    rows = matrix()
    classes = {s["id"]: s["source_class"] for s in sources}
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for _, event in all_events(events):
        row_key = f"event:{event['event_type']}"
        row = rows[row_key]
        leaves = [c for cid in event["claim_ids"] for _, c in leaf_citations(cid, claims)]
        if not any(classes.get(c["source_id"]) in row["sufficient"] and c["standing"] in row["standings"] for c in leaves):
            errors.append(f"{event['id']}: no citation with a class and standing that {row_key} allows")
    return errors


def check_proposals(events, entities) -> list[str]:
    """PL-6."""
    forms = {r["id"]: {a["value"] for a in r["instrument_form"]} if isinstance(r["instrument_form"], list) else set()
             for _, r in all_records(entities) if r["type"] == "policy"}
    errors = []
    for _, event in all_events(events):
        if event["event_type"] in NEVER_FOR_PROPOSALS and "proposed_rule" in forms.get(event["subject"], set()):
            errors.append(f"{event['id']}: {event['subject']} is a proposed rule, and a proposed rule never takes effect or is repealed")
    return errors


def check_event_ids(events) -> list[str]:
    """EI-1."""
    errors = []
    for _, event in all_events(events):
        want = f"event-{event['subject'].split('-', 1)[1]}-{event['event_type']}-{event['date']}"
        if event["id"] != want:
            errors.append(f"{event['id']}: not event- plus the subject, type and date (expected {want})")
    return errors


def event_errors(events, entities, sources, staging_claims, canonical_claims) -> list[str]:
    errors = check_event_references(events, entities, staging_claims, canonical_claims)
    errors += check_plans(events, staging_claims, canonical_claims)
    errors += check_event_dates(events, sources, staging_claims, canonical_claims, entities)
    errors += check_event_matrix(events, sources, staging_claims, canonical_claims)
    errors += check_event_ids(events)
    errors += check_proposals(events, entities)
    return errors


def fixture_events() -> dict:
    return copy.deepcopy(FIXTURES["valid"]["events"])


class EventVocabularyTests(unittest.TestCase):
    def test_every_event_type_has_a_matrix_row(self) -> None:
        rows = matrix()
        for item in EVENT_TYPES:
            with self.subTest(event_type=item["const"]):
                self.assertIn(f"event:{item['const']}", rows)

    def test_announced_is_the_only_plan(self) -> None:
        # H-2: only announced is a plan (ER-8); S17 adds three policy occurrences (D-156).
        self.assertEqual({item["const"] for item in EVENT_TYPES} - OCCURRENCES, {"announced"})

    def test_policy_event_types_have_a_policy_subject(self) -> None:
        # P-4 (D-156): published, effective and repealed happen to a policy; the facility types to a facility.
        self.assertEqual({t for t, kind in SUBJECT.items() if kind == "policy"}, {"published", "effective", "repealed"})
        self.assertEqual({t for t, kind in SUBJECT.items() if kind == "facility"}, {"opened", "expanded", "closed"})


class EventDataTests(unittest.TestCase):
    """The checks on the real files."""

    def setUp(self) -> None:
        self.events = load_events()
        self.entities = load_entities()
        self.sources, self.staging, self.canonical = load_data()

    def test_event_files_exist(self) -> None:
        # L-05: each data file this session creates is in the validator's scope.
        for path in event_files():
            with self.subTest(path=path.name):
                self.assertTrue(path.exists())

    def test_s09_gate_events_exist(self) -> None:
        self.assertTrue(self.events["canonical"] + self.events["staging"], "no event record")

    def test_ev1_references_resolve_and_canonical_rests_on_canonical(self) -> None:
        self.assertEqual(check_event_references(self.events, self.entities, self.staging, self.canonical), [])

    def test_ev2_a_plan_is_never_an_occurrence(self) -> None:
        self.assertEqual(check_plans(self.events, self.staging, self.canonical), [])

    def test_ev3_no_event_after_its_source(self) -> None:
        self.assertEqual(check_event_dates(self.events, self.sources, self.staging, self.canonical, self.entities), [])

    def test_pl6_no_proposal_takes_effect(self) -> None:
        self.assertEqual(check_proposals(self.events, self.entities), [])

    def test_ev4_events_rest_on_allowed_classes_and_standing(self) -> None:
        self.assertEqual(check_event_matrix(self.events, self.sources, self.staging, self.canonical), [])

    def test_ei1_event_ids_follow_the_rule(self) -> None:
        self.assertEqual(check_event_ids(self.events), [])


class EventFixtureTests(unittest.TestCase):
    """The checks accept the fictional events and catch a planted fault of each kind."""

    def test_fixture_events_are_clean(self) -> None:
        entities, sources, staging, canonical = fixture_world()
        self.assertEqual(event_errors(fixture_events(), entities, sources, staging, canonical), [])

    def test_planted_faults_are_caught(self) -> None:
        faults = FIXTURES["event_faults"]
        self.assertTrue(faults)
        for fault in faults:
            with self.subTest(fault=fault["name"]):
                events = fixture_events()
                entities, sources, staging, canonical = fixture_world()
                if fault["where"] == "source":
                    next(s for s in sources if s["id"] == fault["source"])[fault["field"]] = fault["value"]
                elif fault["where"] == "entity":
                    entities["staging"][fault["kind"]][fault["index"]][fault["field"]] = fault["value"]
                else:
                    events[fault["where"]][fault["index"]][fault["field"]] = fault["value"]
                errors = event_errors(events, entities, sources, staging, canonical)
                self.assertTrue(any(fault["expect"] in e for e in errors), f"{fault['name']}: {errors}")


if __name__ == "__main__":
    unittest.main()
