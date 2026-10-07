"""Consistency checks for the S05 source policy (standard library only).

They keep docs/research/source-policy.md, the source-class vocabulary and their inputs from
drifting apart:

- every class in schemas/sources.schema.json has a definition, exactly one row in the class
  table and at least one neighbour test, and the four pairs Part B §07 names are tested;
- the preference matrix has exactly one row per material claim type, read from the entity,
  relationship and (S09) event schemas at test time, and every row assigns all classes to exactly one
  column;
- the matrix points to relationship-taxonomy.md §5 and never copies its text (one home);
- every source in source-register.md has exactly one class, parsed from the register itself
  with width and row-count assertions; every "not retrievable" row is classed;
- every conflict in domain map §5 has one handling row, of a defined kind, preserved, and
  its sources' classes agree with the mapping;
- every decision, non-goal, rule, concept, DEP, SRC and CON cited exists; every quoted
  anchor in the worked examples and the explainer is verbatim in the domain map;
- every count written in prose matches the tables (L-04).

Markdown tables are parsed by splitting cells, with the width asserted (S03, S04 lessons).
"""

import json
import re
import unittest
from pathlib import Path

from test_entity_taxonomy import CONCEPT, ENTITY_TYPES, cells, decision_exists, section

REPO_ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


POLICY = read("docs/research/source-policy.md")
REGISTER = read("docs/research/source-register.md")
DOMAIN_MAP = read("docs/research/domain-map.md")
REL_TAXONOMY = read("docs/architecture/relationship-taxonomy.md")
SOURCE_SCHEMA = json.loads(read("schemas/sources.schema.json"))
ENTITY_DEFS = json.loads(read("schemas/entities.schema.json"))["$defs"]
REL_DEFS = json.loads(read("schemas/relationships.schema.json"))["$defs"]
EVENT_DEFS = json.loads(read("schemas/events.schema.json"))["$defs"]

CLASS_ITEMS = SOURCE_SCHEMA["$defs"]["vocab_source_class"]["oneOf"]
CLASSES = {item["const"] for item in CLASS_ITEMS}
THIRD_PARTY_STANDING = "party, or a third party under §7.1"
STANDINGS = {"party", "originator", "party or originator", THIRD_PARTY_STANDING}
FRESHNESS = {"stable", "time_sensitive"}
SRC = r"SRC-\d{3}"
REQUIRED_PAIRS = {
    frozenset({"company_filing", "company_press_release"}),
    frozenset({"company_technical_documentation", "company_marketing"}),
    frozenset({"research_report", "policy_research_brief"}),
    frozenset({"industry_association", "market_research_consultancy"}),
}


def backticked(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def table(text: str, width: int, key: str) -> list[list[str]]:
    """Rows of the tables in `text` whose first cell matches `key`, each exactly `width` wide."""
    rows = []
    for line in text.splitlines():
        row = cells(line)
        if row and re.fullmatch(key, row[0]):
            assert len(row) == width, f"row {row[0]!r} has {len(row)} cells, expected {width}"
            rows.append(row)
    return rows


def policy_section(number: str, next_number: str) -> str:
    return section(POLICY, f"\n## {number}. ", f"\n## {next_number}. ")


# --- tables in the policy -----------------------------------------------------------------


def class_rows() -> list[list[str]]:
    return table(policy_section("2", "3"), 3, r"`[a-z_]+`")


def pair_rows() -> list[list[str]]:
    return table(policy_section("3", "4"), 3, r"`[a-z_]+` vs `[a-z_]+`")


def matrix_rows() -> list[list[str]]:
    return table(policy_section("7", "8"), 7, r"`(?:rel|identity|attr|event):[a-z_.]+`")


def mapping_rows() -> list[list[str]]:
    return table(section(POLICY, "### 8.1 ", "### 8.2 "), 5, SRC)


def blocked_rows() -> list[list[str]]:
    body = section(POLICY, "### 8.2 ", "### 8.3 ")
    rows = [cells(line) for line in body.splitlines()]
    rows = [r for r in rows if r and r[0] not in {"Host row", ""} and not set(r[0]) <= {"-"}]
    for row in rows:
        assert len(row) == 2, f"blocked-host row {row[0]!r} has {len(row)} cells"
    return rows


def kind_rows() -> list[list[str]]:
    return table(section(POLICY, "### 10.1 ", "### 10.2 "), 4, r"`[a-z_]+`")


def conflict_rows() -> list[list[str]]:
    return table(section(POLICY, "### 10.2 ", "\n## 11. "), 6, r"CON-\d{2}")


def column_classes(cell: str) -> list[str]:
    return [] if cell.strip() == "none" else backticked(cell)


# --- the inputs, parsed from their own documents ------------------------------------------


def register_rows() -> list[list[str]]:
    body = section(REGISTER, "## Register", "### Notes")
    rows = table(body, 10, SRC)
    expected = sum(1 for line in body.splitlines() if line.startswith("| SRC-"))
    assert len(rows) == expected, "a register row was skipped"
    return rows


def register_blocked() -> list[str]:
    """First cells of the register's "Not retrievable" table (the last section of the file)."""
    body = REGISTER[REGISTER.index("## Not retrievable") :]
    firsts = []
    for line in body.splitlines():
        row = cells(line)
        if not row or row[0] == "source (host)" or set(row[0]) <= {"-"}:
            continue
        assert len(row) == 3, f"register 'Not retrievable' row {row[0]!r} has {len(row)} cells"
        firsts.append(row[0])
    return firsts


def dm_conflicts() -> list[str]:
    return [row[0] for row in table(section(DOMAIN_MAP, "## 5. ", "## 6. "), 5, r"CON-\d{2}")]


def material_claim_types() -> set[str]:
    """Row keys the matrix must have, read from the schemas (§7 definition)."""
    keys = {f"rel:{item['const']}" for item in REL_DEFS["vocab_relation_type"]["oneOf"]}
    for name, definition in REL_DEFS.items():
        if name.startswith("rel_"):
            for prop, shape in definition.get("properties", {}).items():
                if isinstance(shape, dict) and shape.get("$ref", "").startswith("#/$defs/attr_"):
                    keys.add(f"rel:{name[len('rel_'):]}.{prop}")
    for entity in ENTITY_TYPES:
        properties = ENTITY_DEFS[entity]["properties"]
        if "identity_claim_ids" in properties:
            keys.add(f"identity:{entity}")
        for field, shape in properties.items():
            if shape.get("$ref", "").startswith("#/$defs/attr_"):
                keys.add(f"attr:{entity}.{field}")
    keys |= {f"event:{item['const']}" for item in EVENT_DEFS["vocab_event_type"]["oneOf"]}  # S09, D-084
    return keys


def mapped_class() -> dict[str, str]:
    """Register label -> class, from the live home: the source records (S06; D-041, D-050).

    §8.1 is history since the migration; VD-9 (test_data_integrity.py) checks it once."""
    records = json.loads(read("data/sources.json"))
    return {r["migrated_from"]: r["source_class"] for r in records if "migrated_from" in r}


# --- tests ----------------------------------------------------------------------------------


class ClassTests(unittest.TestCase):
    def test_every_class_has_a_definition_in_the_schema(self) -> None:
        values = [item["const"] for item in CLASS_ITEMS]
        self.assertEqual(len(values), len(set(values)), "a class is defined twice")
        for item in CLASS_ITEMS:
            with self.subTest(source_class=item["const"]):
                self.assertTrue(item.get("description", "").strip())

    def test_every_class_has_exactly_one_row(self) -> None:
        names = [backticked(row[0])[0] for row in class_rows()]
        self.assertEqual(len(names), len(set(names)), "a class has two rows")
        self.assertEqual(set(names), CLASSES)
        for row in class_rows():
            with self.subTest(source_class=row[0]):
                self.assertTrue(row[1] and row[2], "primary-for and never-enough cells are required")

    def test_every_class_has_a_neighbour_test(self) -> None:
        pairs = []
        for row in pair_rows():
            pair = backticked(row[0])
            self.assertEqual(len(pair), 2)
            self.assertLessEqual(set(pair), CLASSES, row[0])
            self.assertTrue(row[1].endswith("?"), f"{row[0]}: the test is a question")
            pairs.append(frozenset(pair))
        self.assertEqual(len(pairs), len(set(pairs)), "a pair is tested twice")
        self.assertLessEqual(REQUIRED_PAIRS, set(pairs))
        self.assertEqual(set().union(*pairs), CLASSES, "a class has no neighbour test")


class MatrixTests(unittest.TestCase):
    def test_one_row_per_material_claim_type(self) -> None:
        keys = [backticked(row[0])[0] for row in matrix_rows()]
        self.assertEqual(len(keys), len(set(keys)), "a claim type has two rows")
        self.assertEqual(set(keys), material_claim_types())

    def test_every_row_assigns_every_class_once(self) -> None:
        for row in matrix_rows():
            with self.subTest(row=row[0]):
                preferred, acceptable, never = (column_classes(c) for c in row[1:4])
                cited = preferred + acceptable + never
                self.assertLessEqual(set(cited), CLASSES, "a cited class is not defined")
                self.assertEqual(len(cited), len(set(cited)), "a class is in two columns")
                self.assertEqual(set(cited), CLASSES, "a class is left to a default")
                self.assertTrue(preferred or row[1].startswith("none —"), "no preferred class, no reason")

    def test_secondary_classes_are_never_sufficient_alone_anywhere(self) -> None:
        # §9 states this in prose; it must stay true of every row but one. S16.6 (R-5, D-147): the supplier of a
        # product may rest on a third party under §7.1's criteria, and only that row says so.
        for row in matrix_rows():
            with self.subTest(row=row[0]):
                if row[0] == "`rel:incorporates.supplier`":
                    self.assertEqual(row[4], THIRD_PARTY_STANDING, "the supplier row must name §7.1's standing")
                    self.assertLessEqual({"research_report", "market_research_consultancy", "news_media"}, set(column_classes(row[2])))
                    self.assertIn("§7.1", row[6])
                else:
                    self.assertLessEqual({"market_research_consultancy", "news_media"}, set(column_classes(row[3])))
                    self.assertNotEqual(row[4], THIRD_PARTY_STANDING, "only the supplier row admits third parties")

    def test_third_party_criteria_are_stated(self) -> None:
        # S16.6 (R-5): the human's four criteria, in §7.1, and R-1's historical values in §12.
        body = policy_section("7", "8")
        for phrase in ("### 7.1", "no older than 12 months", "internationally recognised as reliable",
                       "no conflict of interest", "stated explicitly"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, body)
        self.assertIn("Historical values of a `time_sensitive` row", policy_section("12", "13"))

    def test_standing_and_freshness_values(self) -> None:
        for row in matrix_rows():
            with self.subTest(row=row[0]):
                self.assertIn(row[4], STANDINGS)
                self.assertIn(row[5], FRESHNESS)

    def test_rows_point_to_the_home_of_their_expectation(self) -> None:
        for row in matrix_rows():
            key = backticked(row[0])[0]
            kind, _, name = key.partition(":")
            with self.subTest(row=key):
                if kind == "rel":
                    self.assertIn(f"taxonomy §5 `{name.split('.')[0]}`", row[6])
                elif kind == "attr":
                    self.assertIn(f"`entities.schema.json` `{name.split('.')[1]}`", row[6])
                elif kind == "event":
                    self.assertIn(f"`events.schema.json` `{name}`", row[6])
                elif name not in {"jurisdiction"}:
                    self.assertIn("§7", row[6])

    def test_taxonomy_section_5_is_referenced_not_copied(self) -> None:
        # A-5: no run of eight words from the S04 evidence-expectation cells appears here.
        body = section(REL_TAXONOMY, "## 5. ", "## 6. ")
        policy = flat(POLICY).lower()
        rows = table(body, 4, r"`[a-z_]+`")
        self.assertEqual(len(rows), len(REL_DEFS["vocab_relation_type"]["oneOf"]))
        for row in rows:
            for cell in row[1:]:
                words = flat(cell).lower().split()
                for i in range(len(words) - 7):
                    shingle = " ".join(words[i : i + 8])
                    with self.subTest(type=row[0], shingle=shingle):
                        self.assertFalse(shingle in policy, "copied from taxonomy §5")

    def test_row_counts_in_prose_match_the_table(self) -> None:
        match = re.search(
            r"The matrix has (\d+) rows: (\d+) relation types, (\d+) edge qualifiers?, "
            r"(\d+) identity rows, (\d+)\s+attribute rows and (\d+) event rows",
            POLICY,
        )
        self.assertIsNotNone(match, "matrix count sentence not found")
        kinds = [backticked(row[0])[0] for row in matrix_rows()]
        rel = [k for k in kinds if k.startswith("rel:")]
        expected = (
            len(kinds),
            sum("." not in k for k in rel),
            sum("." in k for k in rel),
            sum(k.startswith("identity:") for k in kinds),
            sum(k.startswith("attr:") for k in kinds),
            sum(k.startswith("event:") for k in kinds),
        )
        self.assertEqual(tuple(map(int, match.groups())), expected)

    def test_class_count_in_prose_matches_the_schema(self) -> None:
        match = re.search(r"The vocabulary has (\d+) classes", POLICY)
        self.assertIsNotNone(match)
        self.assertEqual(int(match.group(1)), len(CLASSES))
        match = re.search(r"assigns all (\d+) classes", POLICY)
        self.assertIsNotNone(match)
        self.assertEqual(int(match.group(1)), len(CLASSES))


class RegisterMappingTests(unittest.TestCase):
    def test_every_registered_source_has_exactly_one_class(self) -> None:
        register = {row[0] for row in register_rows()}
        mapped = [row[0] for row in mapping_rows()]
        self.assertEqual(len(mapped), len(set(mapped)), "a source is mapped twice")
        self.assertEqual(set(mapped), register)
        for row in mapping_rows():
            with self.subTest(source=row[0]):
                classes = backticked(row[1])
                self.assertEqual(len(classes), 1, "one class per source")
                self.assertIn(classes[0], CLASSES)

    def test_s01_tier_column_is_read_from_the_register(self) -> None:
        tiers = {row[0]: row[6].split()[0] for row in register_rows()}
        for row in mapping_rows():
            with self.subTest(source=row[0]):
                self.assertEqual(row[2], tiers[row[0]])

    def test_source_count_in_prose_matches_the_register(self) -> None:
        match = re.search(r"All (\d+) registered sources have one class each", POLICY)
        self.assertIsNotNone(match)
        self.assertEqual(int(match.group(1)), len(register_rows()))

    def test_every_blocked_host_row_is_classed(self) -> None:
        firsts = register_blocked()
        labels = [row[0] for row in blocked_rows()]
        self.assertEqual(len(labels), len(set(labels)))
        for label in labels:
            with self.subTest(label=label):
                self.assertEqual(sum(f.startswith(label) for f in firsts), 1, "must match one register row")
        for first in firsts:
            with self.subTest(register_row=first):
                self.assertEqual(sum(first.startswith(label) for label in labels), 1, "register row unclassed")
        for row in blocked_rows():
            with self.subTest(label=row[0]):
                classes = backticked(row[1])
                self.assertTrue(classes)
                self.assertLessEqual(set(classes), CLASSES)

    def test_s05_retrievals_have_a_class_or_none(self) -> None:
        rows = table(section(POLICY, "### 8.3 ", "**Why S05-R1"), 4, r"S05-[RA]\d+")
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(source=row[0]):
                if row[0].startswith("S05-R"):
                    self.assertEqual(len(backticked(row[3])), 1)
                    self.assertIn(backticked(row[3])[0], CLASSES)
                else:
                    self.assertEqual(row[3], "none", "an access record is not a source")


class ConflictTests(unittest.TestCase):
    def test_every_domain_map_conflict_has_one_handling_row(self) -> None:
        handled = [row[0] for row in conflict_rows()]
        self.assertEqual(len(handled), len(set(handled)))
        self.assertEqual(set(handled), set(dm_conflicts()))

    def test_kinds_are_defined_and_no_conflict_is_closed(self) -> None:
        kinds = {backticked(row[0])[0] for row in kind_rows()}
        self.assertTrue(kinds)
        for row in conflict_rows():
            with self.subTest(conflict=row[0]):
                self.assertEqual(len(backticked(row[1])), 1)
                self.assertIn(backticked(row[1])[0], kinds)
                self.assertEqual(row[4], "preserved", "a conflict is closed only by a human decision")

    def test_sides_use_each_source_s_mapped_class(self) -> None:
        classes = mapped_class()
        for row in conflict_rows():
            with self.subTest(conflict=row[0]):
                # Each side is "SRC-NNN [locators] · `class`"; the class must be that source's.
                sides = [side.strip() for side in row[2].split(";")]
                self.assertGreaterEqual(len(sides), 2, "a conflict has at least two sides")
                for side in sides:
                    source_part, _, class_part = side.partition(" · ")
                    (source,) = re.findall(SRC, source_part)
                    self.assertEqual(backticked(class_part), [classes[source]], side)


class CitationTests(unittest.TestCase):
    def test_cited_decisions_and_non_goals_exist(self) -> None:
        text = POLICY + json.dumps(SOURCE_SCHEMA)
        for ref in sorted(set(re.findall(r"\b(?:D-\d{3}|NG-\d{2})\b", text))):
            with self.subTest(ref=ref):
                self.assertTrue(decision_exists(ref), ref)

    def test_cited_rules_are_defined_here(self) -> None:
        homes = {"SP": (("1", "2"), 3), "ER": (("6", "7"), 3), "RA": (("11", "12"), 2)}
        for prefix, (numbers, width) in homes.items():
            defined = {row[0] for row in table(policy_section(*numbers), width, rf"{prefix}-\d+")}
            with self.subTest(prefix=prefix):
                self.assertTrue(defined)
                self.assertLessEqual(set(re.findall(rf"\b{prefix}-\d+\b", POLICY)), defined)

    def test_cited_sources_conflicts_concepts_and_deps_exist(self) -> None:
        register = {row[0] for row in register_rows()}
        for ref in sorted(set(re.findall(rf"\b{SRC}\b", POLICY))):
            with self.subTest(source=ref):
                self.assertIn(ref, register)
        for ref in sorted(set(re.findall(r"\bCON-\d{2}\b", POLICY))):
            with self.subTest(conflict=ref):
                self.assertIn(ref, dm_conflicts())
        for ref in sorted(set(re.findall(rf"\b{CONCEPT}\b", POLICY))):
            with self.subTest(concept=ref):
                self.assertIn(f"#### {ref} — ", DOMAIN_MAP)
        for ref in sorted(set(re.findall(r"\bDEP-\d{2}\b", POLICY))):
            with self.subTest(dep=ref):
                self.assertIn(f"| {ref} |", DOMAIN_MAP)

    def test_worked_examples_cover_the_required_sources(self) -> None:
        headings = re.findall(r"^### Example \d+ — (SRC-\d{3})", policy_section("13", "14"), re.MULTILINE)
        self.assertGreaterEqual(len(headings), 4)
        self.assertLessEqual({"SRC-006", "SRC-017", "SRC-014", "SRC-021"}, set(headings))

    def test_quoted_anchors_are_verbatim_in_the_domain_map(self) -> None:
        text = section(POLICY, "\n## 13. ", "\n## 15. ")
        anchors = [flat(q) for q in re.findall(r'"([^"]+)"', text) if len(q.split()) >= 3]
        self.assertGreaterEqual(len(set(anchors)), 4)
        domain_map = flat(DOMAIN_MAP)
        for anchor in anchors:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, domain_map)


if __name__ == "__main__":
    unittest.main()
