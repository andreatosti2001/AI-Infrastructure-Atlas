"""Consistency checks for the S03 entity taxonomy (standard library only).

They keep the schema, the taxonomy document and their inputs from drifting apart:

- the schema's own structure follows D-025 (every field required, one branch per type,
  every vocabulary value defined, every $ref resolvable);
- every v1 concept in M0 audit Part 4 is mapped exactly once, in its D-020 class
  unless a cited decision reclassifies it, to a target that exists in the schema;
- every entity type in MA §6.1 and §5.1 has exactly one disposition;
- every concept ID and decision cited by the schema or the mapping exists.
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((REPO_ROOT / "schemas/entities.schema.json").read_text(encoding="utf-8"))
TAXONOMY = (REPO_ROOT / "docs/architecture/entity-taxonomy.md").read_text(encoding="utf-8")
M0_AUDIT = (REPO_ROOT / "docs/architecture/milestone-audits/M0-audit.md").read_text(encoding="utf-8")
DOMAIN_MAP = (REPO_ROOT / "docs/research/domain-map.md").read_text(encoding="utf-8")
DECISIONS = (REPO_ROOT / "docs/architecture/decisions.md").read_text(encoding="utf-8")
BASELINE = (REPO_ROOT / "docs/architecture/baseline.md").read_text(encoding="utf-8")
MASTER = (REPO_ROOT / "MASTER-ARCHITECTURE.md").read_text(encoding="utf-8")

DEFS = SCHEMA["$defs"]
CONCEPT = r"(?:X|ACC|HBM|PKG|FAB|EDA|SME|DC|EN)-\d{2}"
RECORD_KINDS = {"source", "claim", "event", "relationship"}
RESERVED_TYPES = {"institution", "policy"}


def section(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    return text[begin : text.index(end, begin + len(start))]


def vocab(name: str) -> set[str]:
    return {item["const"] for item in DEFS[name]["oneOf"]}


ENTITY_TYPES = vocab("vocab_entity_type")


def resolve_target(target: str) -> bool:
    if target == "none":
        return True
    prefix, _, value = target.partition(":")
    if prefix == "type":
        return value in ENTITY_TYPES
    if prefix == "role":
        return value in vocab("vocab_actor_role")
    if prefix == "facility_kind":
        return value in vocab("vocab_facility_kind")
    if prefix == "attribute":
        entity, _, field = value.partition(".")
        return entity in ENTITY_TYPES and field in DEFS[entity]["properties"]
    if prefix == "kind":
        return value in RECORD_KINDS
    if prefix == "reserved":
        return value in RESERVED_TYPES and value not in ENTITY_TYPES
    return False


def decision_exists(ref: str) -> bool:
    if ref.startswith("D-"):
        return re.search(rf"^## {re.escape(ref)} ", DECISIONS, re.MULTILINE) is not None
    if ref.startswith("NG-"):
        return f"| {ref} |" in BASELINE
    return False


def cells(line: str) -> list[str]:
    """Cells of a Markdown table row, or [] if the line is not a row."""
    if not (line.startswith("|") and line.rstrip().endswith("|")):
        return []
    return [cell.strip() for cell in line.strip()[1:-1].split("|")]


def part4_classes() -> dict[str, str]:
    """Concept ID -> D-020 class, parsed from M0 audit Part 4."""
    part4 = M0_AUDIT[M0_AUDIT.index("## Part 4") :]
    result: dict[str, str] = {}
    for line in part4.splitlines():
        row = cells(line)
        if len(row) != 4 or not re.fullmatch(r"\*\*.+\*\*", row[0]):
            continue
        label, _, concepts, count = row[0].strip("*"), *row[1:]
        ids = re.findall(rf"\b{CONCEPT}\b", concepts)
        assert len(ids) == int(count), f"Part 4 row {label!r}: {len(ids)} IDs, n={count}"
        for concept_id in ids:
            assert concept_id not in result, f"{concept_id} listed twice in Part 4"
            result[concept_id] = label.lower()
    return result


def mapping_rows() -> list[tuple[str, str, str, list[str], str]]:
    """(concept, D-020 class, S03 class, targets, note) from taxonomy §5."""
    body = section(TAXONOMY, "## 5. ", "## 6. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 6 and re.fullmatch(CONCEPT, row[0]):
            concept, _, d020, s03, target_cell, note = row
            rows.append((concept, d020, s03, re.findall(r"`([^`]+)`", target_cell), note))
    return rows


def ma_entity_items() -> set[tuple[str, str]]:
    """(item, section) for every entity type listed in MA §6.1 and §5.1."""
    block = section(MASTER, "### 6.1 Core entities", "### 6.2")
    code = block[block.index("```text") + len("```text") : block.rindex("```")]
    items = {(line.strip(), "6.1") for line in code.splitlines() if line.strip()}
    core = section(MASTER, "### 5.1 Entity", "### 5.2")
    core = core[core.index("Core types:") :]
    items |= {(line[2:].strip(), "5.1") for line in core.splitlines() if line.startswith("- ")}
    return items


def disposition_rows() -> list[tuple[str, str, list[str], str]]:
    body = section(TAXONOMY, "## 6. ", "## 7. ")
    rows = []
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 5 and row[1] in {"6.1", "5.1"}:
            item, ma_section, _, target_cell, decision = row
            rows.append((item, ma_section, re.findall(r"`([^`]+)`", target_cell), decision))
    return rows


class SchemaStructureTests(unittest.TestCase):
    def test_each_type_has_one_branch_and_definition(self) -> None:
        branches = {
            b["if"]["properties"]["type"]["const"]: b["then"]["$ref"] for b in SCHEMA["allOf"]
        }
        self.assertEqual(set(branches), ENTITY_TYPES)
        for entity in ENTITY_TYPES:
            with self.subTest(type=entity):
                self.assertEqual(branches[entity], f"#/$defs/{entity}")
                definition = DEFS[entity]
                self.assertEqual(definition["properties"]["type"], {"const": entity})
                self.assertTrue(definition["properties"]["id"]["pattern"].startswith(f"^{entity}-"))
                self.assertIs(definition["additionalProperties"], False)

    def test_every_field_is_required(self) -> None:
        # D-025: a missing field is never accepted in place of an explicit state.
        for entity in ENTITY_TYPES:
            with self.subTest(type=entity):
                self.assertEqual(set(DEFS[entity]["required"]), set(DEFS[entity]["properties"]))

    def test_every_vocabulary_value_is_defined_once(self) -> None:
        for name in (n for n in DEFS if n.startswith("vocab_")):
            values = [item["const"] for item in DEFS[name]["oneOf"]]
            with self.subTest(vocabulary=name):
                self.assertEqual(len(values), len(set(values)))
                for item in DEFS[name]["oneOf"]:
                    self.assertTrue(item.get("description", "").strip(), item["const"])

    def test_reserved_and_record_kinds_are_not_instantiable(self) -> None:
        self.assertEqual(ENTITY_TYPES & (RESERVED_TYPES | RECORD_KINDS), set())

    def test_all_refs_resolve(self) -> None:
        refs: list[str] = []

        def walk(node) -> None:
            if isinstance(node, dict):
                if "$ref" in node:
                    refs.append(node["$ref"])
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(SCHEMA)
        for ref in refs:
            with self.subTest(ref=ref):
                self.assertTrue(ref.startswith("#/$defs/"))
                self.assertIn(ref[len("#/$defs/") :], DEFS)

    def test_concepts_cited_by_schema_exist_in_domain_map(self) -> None:
        for name in (n for n in DEFS if n.startswith("vocab_")):
            for item in DEFS[name]["oneOf"]:
                for concept in item.get("x-concepts", []):
                    with self.subTest(vocabulary=name, concept=concept):
                        self.assertIn(f"#### {concept} — ", DOMAIN_MAP)


class ConceptMappingTests(unittest.TestCase):
    def test_every_part4_concept_is_mapped_exactly_once(self) -> None:
        rows = mapping_rows()
        mapped = [row[0] for row in rows]
        self.assertEqual(len(mapped), len(set(mapped)), "a concept is mapped twice")
        self.assertEqual(set(mapped), set(part4_classes()))

    def test_d020_class_is_copied_from_part4(self) -> None:
        classes = part4_classes()
        for concept, d020, _, _, _ in mapping_rows():
            with self.subTest(concept=concept):
                self.assertEqual(d020, classes[concept])

    def test_reclassification_cites_an_existing_decision(self) -> None:
        for concept, d020, s03, _, note in mapping_rows():
            if d020 != s03:
                with self.subTest(concept=concept):
                    cited = re.findall(r"D-\d{3}", note)
                    self.assertTrue(cited, "reclassified without a decision")
                    for ref in cited:
                        self.assertTrue(decision_exists(ref), ref)

    def test_targets_resolve_in_schema(self) -> None:
        for concept, _, s03, targets, _ in mapping_rows():
            with self.subTest(concept=concept):
                self.assertTrue(targets, "no target")
                for target in targets:
                    self.assertTrue(resolve_target(target), target)
                if s03 in {"definitional", "energy, concept only"}:
                    self.assertEqual(targets, ["none"])


class MaDispositionTests(unittest.TestCase):
    def test_every_ma_entity_type_has_one_disposition(self) -> None:
        rows = [(item, ma_section) for item, ma_section, _, _ in disposition_rows()]
        self.assertEqual(len(rows), len(set(rows)), "an MA item has two dispositions")
        self.assertEqual(set(rows), ma_entity_items())

    def test_disposition_targets_and_decisions_resolve(self) -> None:
        for item, ma_section, targets, decision in disposition_rows():
            with self.subTest(item=item, section=ma_section):
                self.assertTrue(targets)
                for target in targets:
                    self.assertTrue(resolve_target(target), target)
                self.assertTrue(decision_exists(decision), decision)


if __name__ == "__main__":
    unittest.main()
