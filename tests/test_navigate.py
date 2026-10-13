"""Tests for tools/navigate.py (S10; edge-dataset.md §8; D-097). Standard library only.

The S10 gate: "Graph-like navigation is possible using relational data without introducing a
graph database." The tool must answer MA §18's questions from the JSON files:

- on the fictional edge world (tests/fixtures/edge_records.json), written to a temporary data
  directory, with known answers;
- on every real edge: each structural edge is found by `depends-on` from its target, each
  activity edge by `actors`, each edge by `edges` from both ends, and `evidence` traces it;

and it must never print "none" for a missing edge (RR-7).

S11 (D-101): every answer also exists as data (`navigate_data`, `--json`), and the data and the
text must name the same edges, with the same status.
"""

import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from test_data_relationships import edge_fixture_world, load_edges

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import navigate  # noqa: E402

KINDS = ("companies", "jurisdictions", "technologies", "components", "products", "facilities", "policies")
POLICY_LINK = "rel-policy-xa-example-code-1-9-restricts-component-example-gpu"


def write_world(root: Path) -> None:
    edges, entities, events, sources, staging, canonical, _ = edge_fixture_world()
    (root / "staging").mkdir(parents=True)
    (root / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    (root / "claims.json").write_text(json.dumps(canonical), encoding="utf-8")
    (root / "staging" / "claims.json").write_text(json.dumps(staging), encoding="utf-8")
    for where, folder in (("canonical", root), ("staging", root / "staging")):
        for kind in KINDS:
            (folder / f"{kind}.json").write_text(json.dumps(entities[where][kind]), encoding="utf-8")
        (folder / "relationships.json").write_text(json.dumps(edges[where]), encoding="utf-8")
        (folder / "events.json").write_text(json.dumps(events[where]), encoding="utf-8")


class FixtureNavigationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_world(self.root)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def ask(self, command: str, ref: str, staging: bool = False) -> tuple[str, int]:
        lines, status = navigate.navigate(command, ref, navigate.Atlas(self.root, staging, on="2026-10-13"))
        return "\n".join(lines), status

    def test_pk6_a_policy_link_is_neither_a_dependency_nor_an_activity(self) -> None:
        # policy-links.md K-8: restricts says what an act's text names; it is not something the class depends on,
        # and not something done to it
        for command in ("depends-on", "actors", "suppliers"):
            with self.subTest(command=command):
                text, status = self.ask(command, "component-example-gpu", staging=True)
                self.assertEqual(status, 0, text)
                self.assertNotIn(POLICY_LINK, text)

    def test_pk6_edges_shows_a_policy_link_with_its_status_text_and_no_advice_line(self) -> None:
        for ref in ("component-example-gpu", "policy-xa-example-code-1-9"):
            with self.subTest(ref=ref):
                text, status = self.ask("edges", ref, staging=True)
                self.assertEqual(status, 0, text)
                self.assertIn(POLICY_LINK, text)
                self.assertIn("· staging · policy", text)
                self.assertIn("status of policy-xa-example-code-1-9 on 2026-10-13: no_recorded_effect", text)
                self.assertIn("official text: https://example.com/src-918", text)
                self.assertIn("describes the text; does not advise (LA-5)", text)
        text, _ = self.ask("edges", "component-example-gpu", staging=True)
        self.assertIn("component-example-gpu (Example GPU) named among the items controlled by policy-xa-example-code-1-9", text)

    def test_pk6_the_status_follows_the_act_events(self) -> None:
        atlas = navigate.Atlas(self.root, True, on="2026-10-13")
        self.assertEqual(atlas.policy_status("policy-xa-ex-1-100")[0], "has_taken_effect")
        self.assertEqual(navigate.Atlas(self.root, True, on="2026-04-01").policy_status("policy-xa-ex-1-100")[0], "not_yet_published")

    def test_what_depends_on_a_technology(self) -> None:
        text, status = self.ask("depends-on", "technology-example-stacking")
        self.assertEqual(status, 0)
        self.assertIn("component-example-accelerator (Example accelerator) requires technology-example-stacking", text)
        self.assertIn("rel-component-example-accelerator-requires-technology-example-stacking · canonical · class", text)
        self.assertIn("claim-fixture-406 (FACT, supported, canonical)", text)

    def test_depends_on_walks_to_products(self) -> None:
        text, _ = self.ask("depends-on", "component-example-gpu", staging=True)
        self.assertIn("product-example-designer-chip-one (Chip One) incorporates component-example-gpu", text)
        self.assertIn("· staging · instance · no period in the claims", text)

    def test_canonical_only_by_default(self) -> None:
        text, status = self.ask("depends-on", "product-example-designer-chip-one")
        self.assertEqual(status, 0)
        self.assertIn("no recorded relationship", text)
        self.assertNotIn("staging", text.split("\n", 1)[1])

    def test_who_supplies_a_component(self) -> None:
        text, _ = self.ask("suppliers", "component-example-gpu", staging=True)
        self.assertIn("company level: company-example-foundry", text)
        self.assertIn("product level: in product-example-designer-chip-one (Chip One), supplier: not_publicly_determinable [claim-fixture-408]", text)

    def test_a_product_supplier_is_its_vendor_field(self) -> None:
        text, _ = self.ask("suppliers", "product-example-designer-chip-one")
        self.assertIn("vendor (an entity field", text)
        self.assertIn("company-example-designer", text)

    def test_who_does_what_to_a_product(self) -> None:
        text, _ = self.ask("actors", "product-example-designer-chip-one", staging=True)
        self.assertIn("company-example-designer (Example Designer) designs product-example-designer-chip-one", text)
        self.assertIn("company-example-foundry (Example Foundry) fabricates product-example-designer-chip-one", text)

    def test_inverse_reading_is_display_text(self) -> None:
        text, _ = self.ask("edges", "product-example-designer-chip-one")
        self.assertIn("designed by", text)

    def test_evidence_is_the_trace(self) -> None:
        text, status = self.ask("evidence", "rel-company-example-designer-designs-product-example-designer-chip-one")
        self.assertEqual(status, 0, text)
        self.assertIn("relationship record", text)
        self.assertIn('anchor: "We designed Chip One in our own design centres"', text)

    def test_unknown_id(self) -> None:
        self.assertEqual(self.ask("actors", "product-example-nothing")[1], 2)

    def test_never_none(self) -> None:
        # RR-7: a missing edge is "no recorded relationship", never "none".
        for command in ("depends-on", "suppliers", "actors", "edges"):
            for ref in ("facility-xa-example-fab-1", "technology-example-stacking", "company-example-designer"):
                with self.subTest(command=command, ref=ref):
                    text, _ = self.ask(command, ref)
                    self.assertNotRegex(text.lower(), r"\bnone\b")


class RealNavigationTests(unittest.TestCase):
    """Every real edge is reachable by the question it answers."""

    def ask(self, command: str, ref: str) -> tuple[str, int]:
        lines, status = navigate.navigate(command, ref, navigate.Atlas(REPO_ROOT / "data", True))
        return "\n".join(lines), status

    def test_every_edge_is_navigable(self) -> None:
        edges = load_edges()
        for where in ("canonical", "staging"):
            for edge in edges[where]:
                with self.subTest(edge=edge["id"]):
                    if edge["relation_type"] in navigate.STRUCTURAL:
                        text, status = self.ask("depends-on", edge["target_entity"])
                        self.assertEqual(status, 0)
                        self.assertIn(edge["id"], text)
                    if edge["relation_type"] in navigate.ACTIVITY:
                        self.assertIn(edge["id"], self.ask("actors", edge["target_entity"])[0])
                    for end in (edge["source_entity"], edge["target_entity"]):
                        self.assertIn(edge["id"], self.ask("edges", end)[0])
                    text, status = self.ask("evidence", edge["id"])
                    self.assertEqual(status, 0, text)
                    if edge["relation_type"] == "restricts":
                        # PK-6: never read as a dependency or an activity
                        for command in ("depends-on", "actors"):
                            self.assertNotIn(edge["id"], self.ask(command, edge["target_entity"])[0])


def edge_ids_in(node) -> set[str]:
    """Every edge ID in a navigate_data answer, at any depth."""
    if isinstance(node, dict):
        found = {node["edge"]["id"]} if isinstance(node.get("edge"), dict) else set()
        for value in node.values():
            found |= edge_ids_in(value)
        return found
    if isinstance(node, list):
        return set().union(*(edge_ids_in(value) for value in node)) if node else set()
    return set()


class StructuredOutputTests(unittest.TestCase):
    """D-101: the data and the text are one answer."""

    def check_world(self, root: Path, staging: bool) -> None:
        atlas = navigate.Atlas(root, staging)
        ids = sorted(set(atlas.records) | {e["id"] for e, _ in atlas.edges})
        edge_ids = {e["id"] for e, _ in atlas.edges}
        for command in ("depends-on", "suppliers", "actors", "edges"):
            for ref in ids:
                with self.subTest(command=command, ref=ref, staging=staging):
                    lines, status = navigate.navigate(command, ref, atlas)
                    data, data_status = navigate.navigate_data(command, ref, atlas)
                    self.assertEqual(status, data_status)
                    json.dumps(data)  # serialisable as it stands
                    named = {i for i in re.findall(r"\b(rel-[a-z0-9-]+)\b", "\n".join(lines[1:])) if i in edge_ids and i != ref}  # the question and "no recorded relationship" lines name ref itself
                    self.assertEqual(named, edge_ids_in(data["answer"]))

    def test_fixture_world(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_world(Path(tmp))
            for staging in (False, True):
                self.check_world(Path(tmp), staging)

    def test_real_data(self) -> None:
        for staging in (False, True):
            self.check_world(REPO_ROOT / "data", staging)

    def test_unknown_id_as_data(self) -> None:
        data, status = navigate.navigate_data("actors", "product-example-nothing", navigate.Atlas(REPO_ROOT / "data", False))
        self.assertEqual(status, 2)
        self.assertIn("error", data)

    def test_json_flag(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = navigate.main(["navigate.py", "depends-on", "technology-3d-die-stacking", "--json"])
        self.assertEqual(status, 0)
        data = json.loads(out.getvalue())
        self.assertEqual(data["command"], "depends-on")
        self.assertTrue(data["answer"])


if __name__ == "__main__":
    unittest.main()
