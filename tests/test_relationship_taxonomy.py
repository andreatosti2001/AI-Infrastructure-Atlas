"""Consistency checks for the S04 relationship taxonomy (standard library only).

They keep the relationship schema, the taxonomy document and their inputs from drifting
apart:

- the schema's own structure follows D-028/D-029 (one branch per type, typed endpoints on
  instantiable entity types only, qualifiers required or forbidden, class-level types
  without dates, every vocabulary value defined, every $ref resolvable, cross-file refs
  included);
- every verb in MA §6.2, the roadmap's S04 list and domain map §3 has exactly one
  disposition, and the "In" column matches the lists as parsed from their documents;
- every S03 field listed in the S04 prompt has a one-home ruling, and none moves;
- every DEP in domain map §3 is mapped, and the schema's x-deps agree with the mapping;
- the §2 summary table agrees with the schema, every type has a definition section and an
  evidence-expectation row;
- every decision, non-goal, concept and DEP cited exists, and every anchor quoted in the
  worked examples appears verbatim in the domain map.

Markdown tables are parsed by splitting cells (S03 lesson), never with one regex per row.
"""

import json
import re
import unittest
from pathlib import Path

from test_entity_taxonomy import (
    CONCEPT,
    ENTITY_TYPES,
    RECORD_KINDS,
    RESERVED_TYPES,
    cells,
    decision_exists,
    resolve_target,
    section,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((REPO_ROOT / "schemas/relationships.schema.json").read_text(encoding="utf-8"))
ENTITY_SCHEMA = json.loads((REPO_ROOT / "schemas/entities.schema.json").read_text(encoding="utf-8"))
TAXONOMY = (REPO_ROOT / "docs/architecture/relationship-taxonomy.md").read_text(encoding="utf-8")
DOMAIN_MAP = (REPO_ROOT / "docs/research/domain-map.md").read_text(encoding="utf-8")
MASTER = (REPO_ROOT / "MASTER-ARCHITECTURE.md").read_text(encoding="utf-8")
ROADMAP = (REPO_ROOT / "SESSION-ROADMAP.md").read_text(encoding="utf-8")

DEFS = SCHEMA["$defs"]
VOCAB = {item["const"]: item for item in DEFS["vocab_relation_type"]["oneOf"]}
QUALIFIERS = ("item", "supplier")
DATES = ("valid_from", "valid_to")
INSTANCE_TYPES = {"company", "facility", "product"}
CLASS_TYPES = {"technology", "component"}
DISPOSITIONS = {
    "adopt",
    "merge into another verb",
    "already an entity field",
    "an event",
    "a derivation",
    "reserved for S17",
    "excluded by a non-goal",
    "rejected as vague",
}
# Part B §04: the accepted S03 fields a relationship could duplicate.
S03_FIELDS = {
    "facility.located_in",
    "company.incorporated_in",
    "company.headquartered_in",
    "product.vendor",
    "technology.broader",
    "component.broader",
    "product.instance_of",
    "product.vendor_process_name",
    "company.roles",
}
DEP = r"DEP-\d{2}"


def backticked(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def listed(cell: str) -> set[str]:
    return {item.strip() for item in cell.split(",") if item.strip() not in {"", "—"}}


# --- the three verb lists, parsed from their own documents -------------------------------


def ma_verbs() -> set[str]:
    block = section(MASTER, "### 6.2 Relationship vocabulary", "### 6.3")
    code = block[block.index("```text") + len("```text") : block.rindex("```")]
    return {line.strip() for line in code.splitlines() if line.strip()}


def roadmap_verbs() -> set[str]:
    s04 = section(ROADMAP, "## S04 — Relationship taxonomy", "## S05")
    return set(backticked(section(s04, "### Focus", "### Gate")))


def domain_map_verbs() -> set[str]:
    body = section(DOMAIN_MAP, "## 3. Concept-level dependencies", "## 4. ")
    verbs: set[str] = set()
    dep_rows_read = 0
    for line in body.splitlines():
        row = cells(line)
        if row and re.fullmatch(DEP, row[0]):
            assert len(row) == 7, f"domain map §3 row {row[0]} has {len(row)} cells, expected 7"
            verbs |= set(backticked(row[2]))
            dep_rows_read += 1
    assert dep_rows_read == len(dm_dependencies()), "a DEP row was skipped"
    proposed = section(body, "**Verbs for S04**", "roadmap's S04 list already has")
    verbs |= set(backticked(proposed.replace("**Verbs for S04**", "")))
    return {v for v in verbs if re.fullmatch(r"[a-z_]+", v)}


def dm_dependencies() -> set[str]:
    body = section(DOMAIN_MAP, "## 3. Concept-level dependencies", "## 4. ")
    return {row[0] for row in map(cells, body.splitlines()) if row and re.fullmatch(DEP, row[0])}


# --- tables in the taxonomy document ------------------------------------------------------


def rows(start: str, end: str, width: int) -> list[list[str]]:
    body = section(TAXONOMY, start, end)
    return [row for row in map(cells, body.splitlines()) if len(row) == width and not set(row[0]) <= {"-"}]


def summary_rows() -> dict[str, list[str]]:
    table = rows("## 2. ", "**The record**", 7)
    return {backticked(r[0])[0]: r for r in table if backticked(r[0])}


def reconciliation_rows() -> list[list[str]]:
    return [r for r in rows("## 6. ", "**Introduced by S04**", 6) if backticked(r[0])]


def field_rows() -> list[list[str]]:
    return [r for r in rows("## 7. ", "## 8. ", 4) if backticked(r[0])]


def dep_rows() -> list[list[str]]:
    return [r for r in rows("## 8. ", "## 9. ", 5) if re.fullmatch(DEP, r[0])]


def evidence_rows() -> dict[str, list[str]]:
    table = rows("## 5. ", "## 6. ", 4)
    return {backticked(r[0])[0]: r for r in table if backticked(r[0])}


# --- schema helpers -----------------------------------------------------------------------


def endpoint_types(node: dict) -> set[str]:
    refs = [node["$ref"]] if "$ref" in node else [alt["$ref"] for alt in node["anyOf"]]
    result = set()
    for ref in refs:
        assert ref.startswith("#/$defs/endpoint_"), ref
        result.add(ref[len("#/$defs/endpoint_") :])
    return result


def branch(relation_type: str) -> dict:
    return DEFS[f"rel_{relation_type}"]


def resolve_pointer(document: dict, pointer: str):
    node = document
    for token in pointer.lstrip("/").split("/"):
        node = node[token]
    return node


def all_refs(node) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        if "$ref" in node:
            found.append(node["$ref"])
        for value in node.values():
            found += all_refs(value)
    elif isinstance(node, list):
        for value in node:
            found += all_refs(value)
    return found


def resolve(target: str) -> bool:
    if target.startswith("rel:"):
        return target[len("rel:") :] in VOCAB
    return resolve_target(target)


class SchemaStructureTests(unittest.TestCase):
    def test_one_branch_per_type(self) -> None:
        branches = {
            b["if"]["properties"]["relation_type"]["const"]: b["then"]["$ref"] for b in SCHEMA["allOf"]
        }
        self.assertEqual(set(branches), set(VOCAB))
        for relation_type, ref in branches.items():
            self.assertEqual(ref, f"#/$defs/rel_{relation_type}")
        self.assertEqual({n for n in DEFS if n.startswith("rel_")}, {f"rel_{t}" for t in VOCAB})

    def test_every_vocabulary_value_is_defined(self) -> None:
        values = [item["const"] for item in DEFS["vocab_relation_type"]["oneOf"]]
        self.assertEqual(len(values), len(set(values)))
        for relation_type, item in VOCAB.items():
            with self.subTest(type=relation_type):
                self.assertTrue(item.get("description", "").strip())
                self.assertIn(item.get("x-level"), {"class", "instance"})
                self.assertIsInstance(item.get("x-deps"), list)
                self.assertTrue(item.get("x-inverse-reading", "").strip())

    def test_inverse_readings_are_never_stored_types(self) -> None:
        for relation_type, item in VOCAB.items():
            with self.subTest(type=relation_type):
                inverse = item["x-inverse-reading"].replace(" ", "_")
                self.assertNotIn(inverse, VOCAB)

    def test_endpoints_are_instantiable_entity_types(self) -> None:
        used: set[str] = set()
        for relation_type in VOCAB:
            for end in ("source_entity", "target_entity"):
                with self.subTest(type=relation_type, end=end):
                    types = endpoint_types(branch(relation_type)["properties"][end])
                    self.assertTrue(types <= ENTITY_TYPES, types - ENTITY_TYPES)
                    self.assertEqual(types & (RESERVED_TYPES | RECORD_KINDS), set())
                    used |= types
        self.assertNotIn("jurisdiction", used, "location is a field, not an edge (D-030)")
        self.assertEqual(endpoint_types(DEFS["endpoint_any"]), used)

    def test_endpoint_patterns_come_from_the_entity_schema(self) -> None:
        for name in (n for n in DEFS if n.startswith("endpoint_") and n != "endpoint_any"):
            entity_type = name[len("endpoint_") :]
            with self.subTest(endpoint=name):
                refs = [part["$ref"] for part in DEFS[name]["allOf"]]
                self.assertIn("#/$defs/not_placeholder", refs)
                external = [r for r in refs if r.startswith("entities.schema.json#")]
                self.assertEqual(len(external), 1)
                target = resolve_pointer(ENTITY_SCHEMA, external[0].split("#", 1)[1])
                self.assertTrue(target["pattern"].startswith(f"^{entity_type}-"))

    def test_levels_constrain_endpoints_and_dates(self) -> None:
        for relation_type, item in VOCAB.items():
            props = branch(relation_type)["properties"]
            ends = endpoint_types(props["source_entity"]) | endpoint_types(props["target_entity"])
            with self.subTest(type=relation_type, level=item["x-level"]):
                if item["x-level"] == "class":
                    self.assertTrue(ends <= CLASS_TYPES)
                    for field in DATES:
                        self.assertIs(props.get(field), False)
                else:
                    self.assertTrue(ends & INSTANCE_TYPES)
                    for field in DATES:
                        self.assertNotIn(field, props)

    def test_qualifiers_are_required_or_forbidden(self) -> None:
        # D-025 carried to edges: no optional qualifier whose absence could hide a gap.
        for relation_type in VOCAB:
            definition = branch(relation_type)
            for field in QUALIFIERS:
                with self.subTest(type=relation_type, qualifier=field):
                    forbidden = definition["properties"].get(field) is False
                    required = field in definition.get("required", [])
                    self.assertTrue(forbidden != required)

    def test_record_contract(self) -> None:
        # D-028: claim-level provenance, no record-level sources, notes, status or score.
        self.assertIs(SCHEMA["additionalProperties"], False)
        self.assertIn("claim_ids", SCHEMA["required"])
        self.assertEqual(SCHEMA["properties"]["claim_ids"]["$ref"], "entities.schema.json#/$defs/claim_ids")
        for forbidden in ("source_ids", "notes", "status", "confidence", "evidence_status", "layer"):
            self.assertNotIn(forbidden, SCHEMA["properties"])
        self.assertTrue(SCHEMA["properties"]["id"]["pattern"].startswith("^rel-"))

    def test_all_refs_resolve(self) -> None:
        for ref in all_refs(SCHEMA):
            with self.subTest(ref=ref):
                if ref.startswith("#/$defs/"):
                    self.assertIn(ref[len("#/$defs/") :], DEFS)
                else:
                    self.assertTrue(ref.startswith("entities.schema.json#/$defs/"))
                    resolve_pointer(ENTITY_SCHEMA, ref.split("#", 1)[1])

    def test_no_energy_or_network_type(self) -> None:
        for relation_type in VOCAB:
            self.assertIsNone(re.search(r"power|energy|grid|network|interconnect", relation_type))


class TaxonomyTableTests(unittest.TestCase):
    def test_summary_table_matches_schema(self) -> None:
        table = summary_rows()
        self.assertEqual(set(table), set(VOCAB))
        for relation_type, (_, level, source, target, qualifier, inverse, deps) in table.items():
            props = branch(relation_type)["properties"]
            with self.subTest(type=relation_type):
                self.assertEqual(level, VOCAB[relation_type]["x-level"])
                self.assertEqual(listed(source), endpoint_types(props["source_entity"]))
                self.assertEqual(listed(target), endpoint_types(props["target_entity"]))
                required = set(branch(relation_type).get("required", []))
                self.assertEqual(set(backticked(qualifier)), required & set(QUALIFIERS))
                self.assertEqual(inverse, VOCAB[relation_type]["x-inverse-reading"])
                self.assertEqual(listed(deps), set(VOCAB[relation_type]["x-deps"]))

    def test_every_type_has_a_definition_section(self) -> None:
        body = section(TAXONOMY, "## 4. ", "## 5. ")
        parts = re.split(r"^### 4\.\d+ ", body, flags=re.MULTILINE)[1:]
        by_type = {backticked(part.splitlines()[0])[0]: part for part in parts}
        self.assertEqual(set(by_type), set(VOCAB))
        labels = ("**Definition:**", "**Direction:**", "**Endpoints:**", "**Level:**", "**Time:**",
                  "**Not to be confused with:**")
        for relation_type, text in by_type.items():
            for label in labels:
                with self.subTest(type=relation_type, label=label):
                    self.assertIn(label, text)

    def test_every_type_has_an_evidence_expectation(self) -> None:
        table = evidence_rows()
        self.assertEqual(set(table), set(VOCAB))
        for relation_type, row in table.items():
            with self.subTest(type=relation_type):
                self.assertTrue(all(cell for cell in row), "empty evidence cell")


class CountTests(unittest.TestCase):
    """L-04: a count written in prose is checked against the schema, never trusted."""

    WORDS = {w: n for n, w in enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve".split())}

    def number(self, word: str) -> int:
        return self.WORDS[word.lower()]

    def test_type_counts_in_prose_match_the_schema(self) -> None:
        levels = [item["x-level"] for item in VOCAB.values()]
        match = re.search(r"^(\w+) types: (\w+) at class level, (\w+) at instance level", TAXONOMY, re.M)
        self.assertIsNotNone(match, "taxonomy §2 count sentence not found")
        total, at_class, at_instance = map(self.number, match.groups())
        self.assertEqual((total, at_class, at_instance),
                         (len(VOCAB), levels.count("class"), levels.count("instance")))
        decisions = (REPO_ROOT / "docs/architecture/decisions.md").read_text(encoding="utf-8")
        title = re.search(r"^## D-029 — Relationship vocabulary v1: (\w+) types", decisions, re.M)
        self.assertEqual(self.number(title.group(1)), len(VOCAB))


class ReconciliationTests(unittest.TestCase):
    def test_every_verb_has_exactly_one_disposition(self) -> None:
        verbs = [backticked(r[0])[0] for r in reconciliation_rows()]
        self.assertEqual(len(verbs), len(set(verbs)), "a verb has two dispositions")
        self.assertEqual(set(verbs), ma_verbs() | roadmap_verbs() | domain_map_verbs())

    def test_in_column_matches_the_lists(self) -> None:
        lists = {"MA": ma_verbs(), "RM": roadmap_verbs(), "DM": domain_map_verbs()}
        for row in reconciliation_rows():
            verb = backticked(row[0])[0]
            with self.subTest(verb=verb):
                self.assertEqual(listed(row[1]), {name for name, verbs in lists.items() if verb in verbs})

    def test_dispositions_and_targets_agree(self) -> None:
        for row in reconciliation_rows():
            verb, disposition, targets, decision = backticked(row[0])[0], row[2], backticked(row[3]), row[5]
            with self.subTest(verb=verb, disposition=disposition):
                self.assertIn(disposition, DISPOSITIONS)
                self.assertTrue(targets)
                for target in targets:
                    self.assertTrue(resolve(target), target)
                if disposition == "adopt":
                    self.assertEqual(targets, [f"rel:{verb}"])
                elif disposition == "merge into another verb":
                    self.assertEqual(len(targets), 1)
                    self.assertTrue(targets[0].startswith("rel:"))
                    self.assertNotEqual(targets[0], f"rel:{verb}")
                elif disposition == "already an entity field":
                    self.assertTrue(all(t.startswith("attribute:") for t in targets))
                elif disposition == "an event":
                    self.assertEqual(targets, ["kind:event"])
                elif disposition == "reserved for S17":
                    self.assertEqual(targets, ["reserved:policy"])
                else:
                    self.assertEqual(targets, ["none"])
                if disposition == "excluded by a non-goal":
                    self.assertTrue(decision.startswith("NG-"))
                self.assertEqual(verb in VOCAB, disposition == "adopt", "only adopted verbs are types")
                self.assertTrue(decision_exists(decision), decision)

    def test_introduced_types_are_exactly_the_new_names(self) -> None:
        # A type either keeps a listed verb's name (adopt) or is a new name, listed under
        # "Introduced by S04" with its reason. Merged verbs may point at either.
        listed_verbs = ma_verbs() | roadmap_verbs() | domain_map_verbs()
        introduced = set(backticked(section(TAXONOMY, "**Introduced by S04**", "**Conflicts with MA")))
        self.assertEqual(introduced & set(VOCAB), set(VOCAB) - listed_verbs)


class OneHomeTests(unittest.TestCase):
    def test_every_listed_s03_field_has_a_ruling_and_stays_a_field(self) -> None:
        fields = [backticked(r[0])[0] for r in field_rows()]
        self.assertEqual(len(fields), len(set(fields)))
        self.assertEqual({f[len("attribute:") :] for f in fields}, S03_FIELDS)
        for row in field_rows():
            with self.subTest(field=row[0]):
                self.assertTrue(resolve_target(backticked(row[0])[0]))
                self.assertEqual(row[2], "field", "moving a fact to an edge needs prior human approval")


class DependencyMappingTests(unittest.TestCase):
    def test_every_dep_is_mapped_once(self) -> None:
        mapped = [r[0] for r in dep_rows()]
        self.assertEqual(len(mapped), len(set(mapped)))
        self.assertEqual(set(mapped), dm_dependencies())

    def test_mapping_targets_resolve(self) -> None:
        kinds = {"relationship": "rel:", "event": "kind:event", "derivation": "none", "exclusion": "none"}
        for dep, _, maps_to, target_cell, note in dep_rows():
            targets = backticked(target_cell)
            with self.subTest(dep=dep, maps_to=maps_to):
                self.assertIn(maps_to, kinds)
                self.assertTrue(targets)
                for target in targets:
                    self.assertTrue(resolve(target), target)
                    self.assertTrue(target.startswith(kinds[maps_to]))
                if maps_to == "exclusion":
                    cited = re.findall(r"\b(?:D-\d{3}|NG-\d{2})\b", note)
                    self.assertTrue(cited, "an exclusion must cite its decision or non-goal")
                    for ref in cited:
                        self.assertTrue(decision_exists(ref), ref)

    def test_schema_x_deps_agree_with_the_mapping(self) -> None:
        expected: dict[str, set[str]] = {t: set() for t in VOCAB}
        for dep, _, maps_to, target_cell, _ in dep_rows():
            for target in backticked(target_cell):
                if target.startswith("rel:"):
                    expected[target[len("rel:") :]].add(dep)
        for relation_type, item in VOCAB.items():
            with self.subTest(type=relation_type):
                self.assertEqual(set(item["x-deps"]), expected[relation_type])


class CitationTests(unittest.TestCase):
    def test_cited_decisions_and_non_goals_exist(self) -> None:
        for ref in sorted(set(re.findall(r"\b(?:D-\d{3}|NG-\d{2})\b", TAXONOMY))):
            with self.subTest(ref=ref):
                self.assertTrue(decision_exists(ref), ref)

    def test_cited_concepts_and_dependencies_exist(self) -> None:
        for concept in sorted(set(re.findall(rf"\b{CONCEPT}\b", TAXONOMY))):
            with self.subTest(concept=concept):
                self.assertIn(f"#### {concept} — ", DOMAIN_MAP)
        for dep in sorted(set(re.findall(rf"\b{DEP}\b", TAXONOMY))):
            with self.subTest(dep=dep):
                self.assertIn(dep, dm_dependencies())

    def test_worked_example_anchors_are_verbatim_in_the_domain_map(self) -> None:
        examples = section(TAXONOMY, "## 12. ", "## 13. ")
        anchors = [q for q in re.findall(r'"([^"]+)"', examples) if len(q.split()) >= 3]
        self.assertGreaterEqual(len(anchors), 3)
        for anchor in anchors:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, DOMAIN_MAP)


if __name__ == "__main__":
    unittest.main()
