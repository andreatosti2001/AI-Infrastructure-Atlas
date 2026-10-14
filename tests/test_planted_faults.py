"""Permanent breaks: 28 planted data faults the record checks must name, on every commit (D-175).

The break harness (tests/regression/) runs at milestone audits and copies the whole repository for each break.
Between audits, a check loosened by a later change would go unnoticed: the real data would still pass. These
tests take 28 of the harness's breaks and run them inside the suite, cheaply:

- the break's own setup (imported from tests/regression/breaks.py, its one home) is applied to a temporary copy
  of data/ only;
- the record checks run in memory on the planted records: the schemas (of the records the setup changed), the
  integrity checks (VD), the entity, policy, event, edge, policy-link and candidate checks, freshness (F-1) and
  the human review record (HR-1, HR-2), each through its own module's function;
- the test passes only if every fragment the break expects is among the errors, and none of them is among the
  errors of the real data.

The criterion (tests/regression/README.md): the break plants a fault in the records (a loosened check would leave
CI green), its setup edits data/ only and its fault is named by a check's message (no copy, rebuild or
subprocess), and its setup finds the records by ID (stable). The harness keeps the 28; nothing is dropped.
Where an ID names two breaks (S13-2, S13-4), the permanent one is the break whose setup edits data/ only.
"""

from __future__ import annotations

import functools
import importlib.util
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import test_data_candidates as candidates
import test_data_entities as entities
import test_data_events as events
import test_data_integrity as integrity
import test_data_relationships as relationships
import test_freshness as freshness
import test_human_reviews as reviews
from test_data_schema import EVENT_SCHEMA, REL_SCHEMA
from test_source_record_schema import CLAIM_SCHEMA, ENTITY_SCHEMA, SOURCE_SCHEMA, validator

REPO_ROOT = Path(__file__).resolve().parent.parent

PERMANENT = (
    "S13-2", "S13-3", "S13-4", "S13-22", "S13-23", "S13-24", "S13-25", "S13-26",
    "S16.5-A1", "S16.6-A9", "S16.6-A10", "S16.6-A11", "D151-4",
    "S17-1", "S17-2", "S17-3", "S17-4", "S17-5", "S17-6", "S17-7", "S17-8", "S17-11",
    "S18-1", "S18-2", "S18-3", "S18-4", "S18-5", "S18-10",
)

SCHEMAS = {"sources": SOURCE_SCHEMA, "claims": CLAIM_SCHEMA, "events": EVENT_SCHEMA, "relationships": REL_SCHEMA,
           **{kind: ENTITY_SCHEMA for kind in entities.ENTITY_KINDS}}


@functools.lru_cache(maxsize=None)
def harness_breaks() -> tuple:
    spec = importlib.util.spec_from_file_location("planted_breaks", REPO_ROOT / "tests/regression/breaks.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(module.breaks())


@functools.lru_cache(maxsize=None)
def schema_validator(name: str):
    if name == "refused_candidates":
        return candidates.candidate_validator()
    return validator(SCHEMAS[name]) if name in SCHEMAS else None


def load_world(root: Path) -> dict[str, list]:
    """Every data file under root/data, keyed by its repository path."""
    return {p.relative_to(root).as_posix(): json.loads(p.read_text(encoding="utf-8")) for p in sorted((root / "data").rglob("*.json"))}


def schema_errors(world: dict, clean: dict) -> list[str]:
    """VD-2 and RC-1 on the records that differ from the clean world (the planted ones)."""
    errors = []
    for path, records in world.items():
        check = schema_validator(Path(path).stem)
        if check is None:
            continue
        before = {json.dumps(r, sort_keys=True) for r in clean.get(path, [])}
        for record in records:
            if json.dumps(record, sort_keys=True) not in before:
                errors += [f"{path} {record.get('id')}: {list(e.absolute_path)}: {e.message}" for e in check.iter_errors(record)]
    return errors


@functools.lru_cache(maxsize=None)
def review_record() -> str:
    return (REPO_ROOT / reviews.RECORD).read_text(encoding="utf-8")


def record_errors(world: dict, clean: dict) -> list[str]:
    """Every record check, each through its own module's function, on one world of records."""
    get = lambda path: world.get(path, [])
    pair = lambda name: {"canonical": get(f"data/{name}.json"), "staging": get(f"data/staging/{name}.json")}
    sources, staging, canonical = get("data/sources.json"), get("data/staging/claims.json"), get("data/claims.json")
    ents = {"canonical": {k: get(f"data/{k}.json") for k in entities.ENTITY_KINDS},
            "staging": {k: get(f"data/staging/{k}.json") for k in entities.ENTITY_KINDS}}
    evs, edges, cands = pair("events"), pair("relationships"), pair("refused_candidates")
    errors = schema_errors(world, clean)
    errors += integrity.integrity_errors(sources, staging, canonical)
    errors += entities.entity_errors(ents, sources, staging, canonical)
    errors += events.event_errors(evs, ents, sources, staging, canonical)
    errors += relationships.edge_errors(edges, ents, evs, sources, staging, canonical, relationships.product_terms())
    errors += candidates.candidate_errors(cands, edges, ents, sources, staging, canonical)
    errors += freshness.check_edge_freshness(edges, sources, staging, canonical)
    errors += freshness.check_freshness(ents, sources, staging, canonical)
    errors += reviews.resolution_errors(staging + canonical, review_record())
    return errors


def plant(brk, tmp: Path) -> tuple[dict, list[str]]:
    """Apply the break's own setup to a copy of data/; return the planted world and the files the setup changed."""
    root = Path(tempfile.mkdtemp(prefix=re.sub(r"[^A-Za-z0-9.-]", "_", brk[0]) + "-", dir=tmp))
    shutil.copytree(REPO_ROOT / "data", root / "data")
    before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    brk[2](root)
    after = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    changed = sorted(p.relative_to(root).as_posix() for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    return load_world(root), changed


def data_only(brk, tmp: Path) -> bool:
    """True when the break's setup applies to a copy of data/ alone (it edits nothing else)."""
    try:
        _, changed = plant(brk, tmp)
    except (OSError, SystemExit, KeyError, StopIteration, ValueError):
        return False
    return bool(changed) and all(c.startswith("data/") for c in changed)


class PlantedFaultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = Path(tempfile.mkdtemp())
        cls.clean = load_world(REPO_ROOT)
        cls.clean_errors = "\n".join(record_errors(cls.clean, cls.clean))

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def permanent(self, bid: str):
        found = [b for b in harness_breaks() if b[0] == bid and data_only(b, self.tmp)]
        self.assertEqual(len(found), 1, f"{bid}: {len(found)} breaks of this ID plant data only (one expected)")
        return found[0]

    def test_each_permanent_break_meets_the_criterion(self) -> None:
        for bid in PERMANENT:
            with self.subTest(brk=bid):
                brk = self.permanent(bid)
                self.assertTrue(brk[4], f"{bid} is a control: a false alarm is noticed at once (criterion 1)")
                names = [f for f in brk[4] if re.fullmatch(r"test_\w+", f)]
                self.assertEqual(names, [], f"{bid} is named by a test, not by a check's message (criterion 2)")

    def test_each_permanent_break_is_caught_as_named(self) -> None:
        for bid in PERMANENT:
            with self.subTest(brk=bid):
                brk = self.permanent(bid)
                world, changed = plant(brk, self.tmp)
                errors = "\n".join(record_errors(world, self.clean))
                for fragment in brk[4]:
                    self.assertNotIn(fragment, self.clean_errors, f"{bid}: {fragment!r} is already reported on the real data")
                    self.assertIn(fragment, errors, f"{bid} ({brk[1]}): planted in {', '.join(changed)}, but no check names {fragment!r}")


if __name__ == "__main__":
    unittest.main()
