"""Tests for tools/trace.py (S06; D-053). Standard library only.

The trace must answer "what supports this record?" (the S06 gate):

- on a fictional relationship, built from the relationship, source and claim fixtures, down
  to each source's class, locator, anchor, standing and dates;
- on every real seed claim and every real source record;
- for every register label, which must resolve to its source record (D-050);

and it must fail (exit 1) when a reference does not resolve, including an input cycle.

S11 (D-101): `trace_data` is the same trace as data. For every ID the text can trace, the data
names the same claims and sources, reports the same unresolved references and has the same status.
"""

import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from test_data_integrity import fixture_set, load_data
from test_source_policy import register_rows

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import trace  # noqa: E402

RELATIONSHIPS = json.loads((REPO_ROOT / "tests/fixtures/relationships.json").read_text(encoding="utf-8"))["valid"]


def write_data(root: Path, sources: list, staging: list, canonical: list) -> None:
    (root / "staging").mkdir(parents=True, exist_ok=True)
    (root / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    (root / "staging" / "claims.json").write_text(json.dumps(staging), encoding="utf-8")
    if canonical:
        (root / "claims.json").write_text(json.dumps(canonical), encoding="utf-8")


class FixtureTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_data(self.root, *fixture_set())
        self.records = self.root / "relationships.json"
        self.records.write_text(json.dumps(list(RELATIONSHIPS.values())), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_trace(self, identifier: str) -> tuple[str, int]:
        lines, status = trace.trace(identifier, trace.Store(self.root, [self.records]))
        return "\n".join(lines), status

    def test_relationship_traces_to_its_sources(self) -> None:
        text, status = self.run_trace("rel-example-foundry-fabricates-accelerator")
        self.assertEqual(status, 0, text)
        for expected in (
            "relationship record",
            "company-example-foundry fabricates product-example-accelerator",
            "/claim_ids:",
            "claim-fixture-109 · DERIVATION · supported · verified 2026-09-30 · staging, not reviewed",
            "reasoning: ER-1",
            "claim-fixture-201 · FACT",
            "citation 1 · src-901 · standing party",
            "class: company_technical_documentation",
            "stated dates: published 2025-03-01, modified 2026-01-15",
            "registered: automated 2026-09-29T09:00Z sha256 0123456789ab",
            "locator: section 'Architecture'",
            'anchor: "fabricated using the Example 3X process"',
            "read by the Verifier: 2026-09-30T10:00Z sha256 0123456789ab (same bytes as registered)",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_qualifier_claims_and_search_records_are_traced(self) -> None:
        text, status = self.run_trace("rel-example-accelerator-incorporates-stack")
        self.assertEqual(status, 0, text)
        self.assertIn("/supplier/claim_ids:", text)
        self.assertIn("→ not_publicly_determinable", text)
        self.assertIn("company_filing: no_answer · src-904", text)

    def test_chain_dispute_and_review_are_shown(self) -> None:
        text, _ = self.run_trace("claim-fixture-202")
        self.assertIn("originator: Example Analytics analysts · market_research_consultancy · not retrieved", text)
        text, _ = self.run_trace("claim-fixture-207")
        self.assertIn("disputed with: claim-fixture-208", text)
        text, _ = self.run_trace("claim-fixture-209")
        self.assertIn("canonical, accepted by the human on 2026-10-01", text)

    def test_unresolved_claims_fail(self) -> None:
        # The requires fixture cites claim-fixture-101 and -102, which have no claim record.
        text, status = self.run_trace("rel-example-stack-requires-via")
        self.assertEqual(status, 1)
        self.assertIn("MISSING: claim claim-fixture-101", text)

    def test_input_cycle_fails(self) -> None:
        sources, staging, canonical = fixture_set()
        for claim in staging:
            if claim["id"] == "claim-fixture-204":
                claim["input_claim_ids"] = ["claim-fixture-206"]
        write_data(self.root, sources, staging, canonical)
        text, status = self.run_trace("claim-fixture-206")
        self.assertEqual(status, 1)
        self.assertIn("MISSING: input cycle claim-fixture-206 -> claim-fixture-204 -> claim-fixture-206", text)

    def test_unknown_id(self) -> None:
        self.assertEqual(self.run_trace("rel-example-nothing")[1], 2)

    def test_a_failed_trace_does_not_leak_into_the_next(self) -> None:
        store = trace.Store(self.root, [self.records])
        self.assertEqual(trace.trace("rel-example-stack-requires-via", store)[1], 1)
        self.assertEqual(trace.trace("rel-example-foundry-fabricates-accelerator", store)[1], 0)


class RealDataTraceTests(unittest.TestCase):
    store = trace.Store(REPO_ROOT / "data", [])

    def test_every_claim_traces_to_its_evidence(self) -> None:
        sources, staging, canonical = load_data()
        classes = {s["id"]: s["source_class"] for s in sources}
        for claim in staging + canonical:
            with self.subTest(claim=claim["id"]):
                lines, status = trace.trace(claim["id"], self.store)
                text = "\n".join(lines)
                self.assertEqual(status, 0, text)
                self.assertIn(f"{claim['id']} · {claim['claim_type']} · {claim['evidence_status']}", text)
                for citation in claim.get("citations", []):
                    self.assertIn(f"{citation['source_id']} · standing {citation['standing']}", text)
                    self.assertIn(f"class: {classes[citation['source_id']]}", text)
                    self.assertIn(f"anchor: \"{citation['anchor']}\"", text)
                    self.assertIn(f"locator: {citation['locator']}", text)
                for input_id in claim.get("input_claim_ids", []):
                    self.assertIn(f"{input_id} · ", text)

    def test_every_edge_traces_to_its_evidence(self) -> None:
        # S10 (edge-dataset.md §8): "What evidence supports the edge?" for every real edge.
        edges = [e for name in ("relationships.json", "staging/relationships.json") if (REPO_ROOT / "data" / name).exists() for e in json.loads((REPO_ROOT / "data" / name).read_text(encoding="utf-8"))]
        for edge in edges:
            with self.subTest(edge=edge["id"]):
                lines, status = trace.trace(edge["id"], self.store)
                text = "\n".join(lines)
                self.assertEqual(status, 0, text)
                self.assertIn("relationship record", lines[0])
                self.assertIn(f"{edge['source_entity']} {edge['relation_type']} {edge['target_entity']}", text)
                for claim_id in edge["claim_ids"]:
                    self.assertIn(f"{claim_id} · ", text)

    def test_every_source_and_register_label_resolves(self) -> None:
        sources, _, _ = load_data()
        for identifier in [s["id"] for s in sources] + [row[0] for row in register_rows()] + ["S05-R1"]:
            with self.subTest(id=identifier):
                lines, status = trace.trace(identifier, self.store)
                self.assertEqual(status, 0)
                self.assertIn("· source record", lines[0])


CLAIM_LINE = re.compile(r"^\s*(claim-[A-Za-z0-9-]+) · ")
SOURCE_LINE = re.compile(r"^\s*(?:citation \d+ · (src-\d+)|(src-\d+) · source record)")


def text_and_data(identifier: str, store) -> tuple[list[str], int, dict, int, list[str]]:
    lines, status = trace.trace(identifier, store)
    text_missing = list(store.missing)
    data, data_status = trace.trace_data(identifier, store)
    return lines, status, data, data_status, text_missing


class TraceDataTests(unittest.TestCase):
    def check(self, identifier: str, store) -> None:
        lines, status, data, data_status, text_missing = text_and_data(identifier, store)
        self.assertEqual(status, data_status)
        if status == 2:
            return
        json.dumps(data)
        claims = {m.group(1) for m in map(CLAIM_LINE.match, lines) if m}
        self.assertEqual(claims, set(data["claims"]))
        sources = {m.group(1) or m.group(2) for m in map(SOURCE_LINE.match, lines) if m}
        searched = {s for c in data["claims"].values() for e in c["claim"].get("search", {}).get("classes", []) for s in e.get("source_ids", [])}
        self.assertEqual(sources | (searched & set(store.sources)), set(data["sources"]))
        self.assertEqual(sorted(text_missing), sorted(data["missing"]))

    def test_every_real_id(self) -> None:
        store = trace.Store(REPO_ROOT / "data", [])
        for identifier in sorted(store.records) + sorted(store.claims) + sorted(store.sources):
            with self.subTest(id=identifier):
                self.check(identifier, store)

    def test_fixture_ids_including_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_data(root, *fixture_set())
            records = root / "relationships.json"
            records.write_text(json.dumps(list(RELATIONSHIPS.values())), encoding="utf-8")
            store = trace.Store(root, [records])
            for identifier in sorted(store.records) + sorted(store.claims) + ["rel-example-nothing"]:
                with self.subTest(id=identifier):
                    self.check(identifier, store)
            # the cycle of test_input_cycle_fails, as data
            sources, staging, canonical = fixture_set()
            for claim in staging:
                if claim["id"] == "claim-fixture-204":
                    claim["input_claim_ids"] = ["claim-fixture-206"]
            write_data(root, sources, staging, canonical)
            data, status = trace.trace_data("claim-fixture-206", trace.Store(root, []))
            self.assertEqual(status, 1)
            self.assertIn("input cycle claim-fixture-206 -> claim-fixture-204 -> claim-fixture-206", data["missing"])

    def test_json_flag(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = trace.main(["trace.py", "rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking", "--json"])
        self.assertEqual(status, 0)
        data = json.loads(out.getvalue())
        self.assertEqual(data["kind"], "record")
        self.assertIn("claim-ecp-hbm-definition", data["claims"])


if __name__ == "__main__":
    unittest.main()
