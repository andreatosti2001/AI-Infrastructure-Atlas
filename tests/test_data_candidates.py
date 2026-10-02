"""validate-data for refused candidates (S12; D-109; milestone-audits/M2-audit.md Part 3 q1).

A refused candidate is a relation the Atlas considered and refused. It is a design ruling, never a
fact and never an edge. The checks run on the real files (data/refused_candidates.json and its
staging copy) and on a fictional world (tests/fixtures/candidate_records.json, inside the edge
fixture world), where each planted fault must fail its check for the reason it names:

RC-1  every record is valid against schemas/refused_candidates.schema.json (no status, no edge field)
RC-2  entity, claim and source IDs resolve (an entity to a record of its prefix's type); the ruling
      is a decision in decisions.md
RC-3  a canonical candidate points only to canonical claims and records; no ID is both staging and
      canonical; IDs are unique
RC-4  a no-record name is not the name or an alias of a record (then its ID must be used), and not a
      placeholder word (RR-7, V-9)
RC-5  the reasons agree with the structure: endpoint_has_no_record exactly when an endpoint has no
      record; item_has_no_record exactly when the item has none; evidence_not_fresh only on a type
      whose source-policy.md §7 row is time_sensitive
RC-6  no considered claim supports an edge of the same type between the same endpoints (a sentence
      is never both used and refused for one relation)
RC-7  every rule code (ER-, RR-, F-, D-) quoted in a reasoning has its home
RC-8  the navigation and the trace never read candidates as edges or records

Uses the pinned jsonschema for RC-1 (D-026); the rest is standard library.
Run alone: python -m unittest discover -s tests -p "test_data_candidates.py" -v
"""

from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from test_data_entities import all_records, load_entities, matrix
from test_data_integrity import DATA, load_data, load_records
from test_data_relationships import PREFIX_TYPE, REL_SCHEMA, edge_fixture_world, load_edges, records_by_id
from test_page import Homes
from test_source_record_schema import CLAIM_SCHEMA, ENTITY_SCHEMA, SOURCE_SCHEMA

REPO_ROOT = Path(__file__).resolve().parent.parent
CAND_SCHEMA = json.loads((REPO_ROOT / "schemas/refused_candidates.schema.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((REPO_ROOT / "tests/fixtures/candidate_records.json").read_text(encoding="utf-8"))
REGISTRY = Registry().with_resources(
    (schema["$id"], Resource.from_contents(schema)) for schema in (ENTITY_SCHEMA, SOURCE_SCHEMA, CLAIM_SCHEMA, REL_SCHEMA, CAND_SCHEMA)
)
RULE_CODE = re.compile(r"\b(?:ER|RR|F)-\d+\b|\bD-\d{3}\b")
_HOMES = Homes()
RULES, DECISIONS = _HOMES.rules, _HOMES.decisions


def candidate_validator() -> Draft202012Validator:
    return Draft202012Validator(CAND_SCHEMA, registry=REGISTRY)


def candidate_files() -> tuple[Path, Path]:
    """(canonical, staging) paths of the candidate files (D-109)."""
    return DATA / "refused_candidates.json", DATA / "staging" / "refused_candidates.json"


def load_candidates() -> dict:
    canonical, staging = candidate_files()
    return {
        "canonical": load_records(canonical) if canonical.exists() else [],
        "staging": load_records(staging) if staging.exists() else [],
    }


def all_candidates(cands) -> list[tuple[str, dict]]:
    return [(where, c) for where in ("canonical", "staging") for c in cands[where]]


def endpoints(cand: dict) -> list[tuple[str, object]]:
    """(field, value) for every endpoint and the item."""
    found = [("source_entities", v) for v in cand["source_entities"]] + [("target_entities", v) for v in cand["target_entities"]]
    if "item" in cand:
        found.append(("item", cand["item"]))
    return found


def recorded(value) -> bool:
    return isinstance(value, str)


def considered_claims(cand: dict) -> list[str]:
    return [c["claim_id"] for c in cand["considered"] if "claim_id" in c]


# --- checks -----------------------------------------------------------------------------------


def check_references(cands, entities, sources, staging_claims, canonical_claims) -> list[str]:
    """RC-2."""
    records = records_by_id(entities)
    claims = {c["id"] for c in staging_claims + canonical_claims}
    source_ids = {s["id"] for s in sources}
    errors = []
    for _, cand in all_candidates(cands):
        for field, value in endpoints(cand):
            if not recorded(value):
                continue
            found = records.get(value)
            if found is None:
                errors.append(f"{cand['id']}.{field}: {value} does not exist")
            elif found[1]["type"] != PREFIX_TYPE.get(value.split("-", 1)[0]):
                errors.append(f"{cand['id']}.{field}: {value} is a {found[1]['type']} record")
        for item in cand["considered"]:
            if "claim_id" in item and item["claim_id"] not in claims:
                errors.append(f"{cand['id']}: claim {item['claim_id']} does not exist")
            if "source_id" in item and item["source_id"] not in source_ids:
                errors.append(f"{cand['id']}: source {item['source_id']} does not exist")
        if cand["ruling"] not in DECISIONS:
            errors.append(f"{cand['id']}: ruling {cand['ruling']} is not a decision in decisions.md")
    return errors


def check_canonical(cands, entities, canonical_claims) -> list[str]:
    """RC-3."""
    records = records_by_id(entities)
    canonical_ids = {c["id"] for c in canonical_claims}
    errors = []
    for cand in cands["canonical"]:
        for claim_id in considered_claims(cand):
            if claim_id not in canonical_ids:
                errors.append(f"canonical {cand['id']} cites staging {claim_id}")
        for _, value in endpoints(cand):
            if recorded(value) and value in records and records[value][0] != "canonical":
                errors.append(f"canonical {cand['id']} points to staging {value}")
    ids = [c["id"] for _, c in all_candidates(cands)]
    errors += [f"{i} is both staging and canonical" for i in sorted({c["id"] for c in cands["canonical"]} & {c["id"] for c in cands["staging"]})]
    errors += [f"{i} is not unique" for i in sorted({i for i in ids if ids.count(i) > 1}) if not (i in {c["id"] for c in cands["canonical"]} and i in {c["id"] for c in cands["staging"]})]
    return errors


def check_no_record_names(cands, entities) -> list[str]:
    """RC-4."""
    names: dict[str, str] = {}
    for _, record in all_records(entities):
        for name in [record.get("name"), *record.get("aliases", [])]:
            if name:
                names[name.casefold()] = record["id"]
    words = re.compile(r"^(unknown|unspecified|undisclosed|unidentified|anonymous|tbd|tba|placeholder|various|others?|none|null|generic|n/?a)$", re.I)
    errors = []
    for _, cand in all_candidates(cands):
        for field, value in endpoints(cand):
            if recorded(value):
                continue
            name = value["name"]
            if name.casefold() in names:
                errors.append(f"{cand['id']}.{field}: no_record {name!r} names a record ({names[name.casefold()]}); use its ID")
            if words.match(name.strip()):
                errors.append(f"{cand['id']}.{field}: no_record {name!r} is a placeholder (RR-7)")
    return errors


def check_reasons(cands, rows) -> list[str]:
    """RC-5."""
    errors = []
    for _, cand in all_candidates(cands):
        reasons = set(cand["reasons"])
        parties = cand["source_entities"] + cand["target_entities"]
        unrecorded = any(not recorded(v) for v in parties)
        if "endpoint_has_no_record" in reasons and not unrecorded:
            errors.append(f"{cand['id']}: endpoint_has_no_record, but every endpoint has a record")
        if unrecorded and "endpoint_has_no_record" not in reasons:
            errors.append(f"{cand['id']}: an endpoint has no record, but endpoint_has_no_record is not a reason")
        item_unrecorded = "item" in cand and not recorded(cand["item"])
        if "item_has_no_record" in reasons and not item_unrecorded:
            errors.append(f"{cand['id']}: item_has_no_record, but the item has a record or is absent")
        if item_unrecorded and "item_has_no_record" not in reasons:
            errors.append(f"{cand['id']}: the item has no record, but item_has_no_record is not a reason")
        if "evidence_not_fresh" in reasons and not any(rows.get(f"rel:{t}", {}).get("freshness") == "time_sensitive" for t in cand["relation_types"]):
            errors.append(f"{cand['id']}: evidence_not_fresh, but no type is time_sensitive ({', '.join(cand['relation_types'])})")
    return errors


def check_used_and_refused(cands, edges) -> list[str]:
    """RC-6."""
    errors = []
    for _, cand in all_candidates(cands):
        for where in ("canonical", "staging"):
            for edge in edges[where]:
                if (
                    edge["relation_type"] in cand["relation_types"]
                    and edge["source_entity"] in cand["source_entities"]
                    and edge["target_entity"] in cand["target_entities"]
                ):
                    errors += [f"{cand['id']}: {c} supports {edge['id']}; a sentence is never both used and refused" for c in considered_claims(cand) if c in edge["claim_ids"]]
    return errors


def check_rule_codes(cands) -> list[str]:
    """RC-7."""
    errors = []
    for _, cand in all_candidates(cands):
        for code in sorted(set(RULE_CODE.findall(cand["reasoning"]))):
            if code not in (DECISIONS if code.startswith("D-") else RULES):
                errors.append(f"{cand['id']}: rule {code} has no home")
    return errors


def candidate_errors(cands, edges, entities, sources, staging_claims, canonical_claims) -> list[str]:
    errors = check_references(cands, entities, sources, staging_claims, canonical_claims)
    errors += check_canonical(cands, entities, canonical_claims)
    errors += check_no_record_names(cands, entities)
    errors += check_reasons(cands, matrix())
    errors += check_used_and_refused(cands, edges)
    errors += check_rule_codes(cands)
    return errors


# --- the fictional world ----------------------------------------------------------------------


def fixture_world():
    edges, entities, _, sources, staging, canonical, _ = edge_fixture_world()
    return copy.deepcopy(FIXTURES["valid"]), edges, entities, sources, staging, canonical


def apply_fault(cands, fault) -> None:
    assert fault["action"] == "set", fault["action"]
    cands[fault["where"]][fault["index"]][fault["field"]] = copy.deepcopy(fault["value"])


# --- tests ------------------------------------------------------------------------------------


class CandidateSchemaTests(unittest.TestCase):
    """RC-1."""

    def test_rc1_every_record_is_valid(self) -> None:
        check = candidate_validator()
        groups = [(f"data {w}", c) for w, c in all_candidates(load_candidates())]
        groups += [(f"fixture {w}", c) for w, c in all_candidates(FIXTURES["valid"])]
        for name, record in groups:
            with self.subTest(group=name, record=record.get("id")):
                self.assertEqual([f"{list(e.absolute_path)}: {e.message}" for e in check.iter_errors(record)], [])

    def test_rc1_schema_faults_are_rejected(self) -> None:
        check = candidate_validator()
        for case in FIXTURES["schema_faults"]:
            with self.subTest(case=case["name"]):
                record = copy.deepcopy(FIXTURES["valid"]["canonical"][case["base"]])
                record.update(copy.deepcopy(case.get("set", {})))
                for field in case.get("remove", []):
                    record.pop(field)
                self.assertNotEqual(list(check.iter_errors(record)), [], "accepted")

    def test_the_relationship_schema_rejects_a_candidate(self) -> None:
        # Neither file can hold the other's records (D-109).
        from test_source_record_schema import validator  # noqa: PLC0415

        check = validator(REL_SCHEMA)
        self.assertNotEqual(list(check.iter_errors(FIXTURES["valid"]["canonical"][0])), [])

    def test_reason_codes_are_defined(self) -> None:
        for item in CAND_SCHEMA["$defs"]["vocab_reason"]["oneOf"]:
            with self.subTest(code=item["const"]):
                self.assertTrue(item.get("description"))


class CandidateDataTests(unittest.TestCase):
    """RC-2 to RC-7 on the real files."""

    def test_real_candidates_pass(self) -> None:
        sources, staging, canonical = load_data()
        self.assertEqual(candidate_errors(load_candidates(), load_edges(), load_entities(), sources, staging, canonical), [])


class CandidateFixtureTests(unittest.TestCase):
    """RC-2 to RC-7 on the fictional world: clean, then each fault fails for its reason."""

    def test_the_fictional_world_is_clean(self) -> None:
        self.assertEqual(candidate_errors(*fixture_world()), [])

    def test_each_fault_fails_its_check(self) -> None:
        for fault in FIXTURES["faults"]:
            with self.subTest(check=fault["check"], fault=fault["name"]):
                world = fixture_world()
                apply_fault(world[0], fault)
                errors = candidate_errors(*world)
                self.assertTrue(any(fault["expect"] in e for e in errors), f"{fault['expect']!r} not in {errors}")


class CandidateIsolationTests(unittest.TestCase):
    """RC-8: the navigation and the trace never read candidates (RR-5)."""

    def test_rc8_navigation_and_trace_do_not_read_candidates(self) -> None:
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        import navigate  # noqa: PLC0415
        import trace  # noqa: PLC0415

        atlas = navigate.Atlas(DATA, True)
        store = trace.Store(DATA, [])
        for _, cand in all_candidates(load_candidates()):
            with self.subTest(candidate=cand["id"]):
                self.assertNotIn(cand["id"], {e["id"] for e, _ in atlas.edges})
                self.assertNotIn(cand["id"], atlas.records)
                self.assertNotIn(cand["id"], store.records if hasattr(store, "records") else {})
        self.assertNotIn("refused_candidates.json", " ".join(trace.ENTITY_FILES))


if __name__ == "__main__":
    unittest.main()
