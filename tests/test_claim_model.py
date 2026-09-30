"""Consistency checks for the S06 claim model (standard library only).

They keep docs/architecture/claim-model.md, schemas/claims.schema.json and their inputs
from drifting apart:

- every claim type and evidence status is defined once in the schema, with a description;
- every MA §10 claim type and evidence status has exactly one disposition, parsed from MA
  itself (acceptance criterion 2), and every disposition names defined values;
- the type × status tables (§4) have one row per claim type and per status, and name only
  defined values; test_claim_schema.py checks them against the schema's behaviour, and
  test_data_integrity.py applies them to the data;
- the standing values in the schema are the rows of source-policy.md §4 (D-035);
- the migration table (§9) has one row per register column;
- every validate-data check (§11) names a test file that exists and implements it;
- every cited decision, non-goal, rule, section, source, concept, conflict and DEP exists;
  every quoted anchor in the explainer (§13) is verbatim in the domain map;
- every count written in prose matches its table or schema (L-04).

Markdown tables are parsed by splitting cells, with the width asserted (S03 to S05).
"""

import json
import re
import unittest
from pathlib import Path

from test_entity_taxonomy import CONCEPT, cells, decision_exists, section

REPO_ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


MODEL_PATH = "docs/architecture/claim-model.md"
MODEL = read(MODEL_PATH) if (REPO_ROOT / MODEL_PATH).is_file() else ""
MASTER = read("MASTER-ARCHITECTURE.md")
POLICY = read("docs/research/source-policy.md")
REGISTER = read("docs/research/source-register.md")
DOMAIN_MAP = read("docs/research/domain-map.md")
CLAIM_SCHEMA = json.loads(read("schemas/claims.schema.json"))
DEFS = CLAIM_SCHEMA["$defs"]


def vocab(name: str) -> set[str]:
    return {item["const"] for item in DEFS[name]["oneOf"]}


TYPES = vocab("vocab_claim_type")
STATUSES = vocab("vocab_evidence_status")
STANDINGS = vocab("vocab_standing")


def backticked(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def model_section(number: str) -> str:
    """Section `## N. ` of the claim model, up to the next `## ` heading."""
    start = MODEL.index(f"\n## {number}. ")
    end = MODEL.find("\n## ", start + 1)
    return MODEL[start : end if end >= 0 else len(MODEL)]


def rows(text: str, width: int, header: str) -> list[list[str]]:
    """Body rows of the one table in `text` whose first header cell is `header`."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if cells(line)[:1] == [header]]
    assert len(starts) == 1, f"expected one table headed {header!r}, found {len(starts)}"
    body = []
    for line in lines[starts[0] + 2 :]:
        row = cells(line)
        if not row:
            break
        assert len(row) == width, f"row {row[0]!r} has {len(row)} cells, expected {width}"
        body.append(row)
    return body


def ma_list(heading: str, next_heading: str) -> list[str]:
    body = section(MASTER, heading, next_heading)
    return [line[2:].strip() for line in body.splitlines() if line.startswith("- ")]


def ma_claim_types() -> list[str]:
    return ma_list("### Claim types", "### Evidence status")


def ma_statuses() -> list[str]:
    return ma_list("### Evidence status", "### Evidence hierarchy")


def values_in(cell: str, allowed: set[str]) -> set[str]:
    if cell.strip() in {"any"}:
        return set(allowed)
    return {v for v in backticked(cell) if v in allowed}


def rule_rows() -> dict[str, dict]:
    """Claim type -> {sources, inputs, standing, reasoning, as_of, statuses} from §4."""
    result = {}
    for row in rows(model_section("4"), 7, "Type"):
        (claim_type,) = backticked(row[0])
        assert claim_type not in result, f"{claim_type} has two rows"
        result[claim_type] = {
            "sources": row[1].split()[0],
            "inputs": row[2].split()[0],
            "standing": values_in(row[3], STANDINGS),
            "reasoning": row[4].split()[0],
            "as_of": row[5].split()[0],
            "statuses": values_in(row[6], STATUSES),
            "cells": row,
        }
    return result


def status_rows() -> dict[str, dict]:
    """Status -> {canonical, inputs} from §4: which statuses may be canonical, and which
    input statuses a claim with that status may rest on."""
    result = {}
    for row in rows(model_section("4"), 4, "Status"):
        (status,) = backticked(row[0])
        assert status not in result, f"{status} has two rows"
        assert row[1] in {"yes", "no"}, row
        result[status] = {"canonical": row[1] == "yes", "inputs": values_in(row[2], STATUSES), "cells": row}
    return result


class VocabularyTests(unittest.TestCase):
    def test_every_value_is_defined_once_with_a_description(self) -> None:
        for name in (n for n in DEFS if n.startswith("vocab_")):
            values = [item["const"] for item in DEFS[name]["oneOf"]]
            with self.subTest(vocabulary=name):
                self.assertEqual(len(values), len(set(values)), "a value is defined twice")
                for item in DEFS[name]["oneOf"]:
                    self.assertTrue(item.get("description", "").strip(), item["const"])

    def test_claim_types_are_the_claude_md_labels(self) -> None:
        claude = read("CLAUDE.md")
        labels = re.search(r"`(FACT \| ATTRIBUTION \| [A-Z |]+)`", claude).group(1)
        self.assertEqual(TYPES, {label.strip() for label in labels.split("|")})

    def test_type_and_status_are_separate_required_fields(self) -> None:
        # L-06, acceptance criterion 1.
        self.assertLessEqual({"claim_type", "evidence_status"}, set(CLAIM_SCHEMA["required"]))
        self.assertEqual(TYPES & STATUSES, set())

    def test_standing_values_are_the_policy_rows(self) -> None:
        body = section(POLICY, "\n## 4. ", "\n## 5. ")
        policy = {backticked(row[0])[0] for row in (cells(l) for l in body.splitlines()) if len(row) == 3 and row[0].startswith("`")}
        self.assertEqual(STANDINGS, policy)


class MaReconciliationTests(unittest.TestCase):
    def test_every_ma_claim_type_has_one_disposition(self) -> None:
        table = rows(model_section("2"), 3, "MA §10 claim type")
        items = [row[0] for row in table]
        self.assertEqual(len(items), len(set(items)), "an MA type has two rows")
        self.assertEqual(set(items), set(ma_claim_types()))
        for row in table:
            with self.subTest(ma_type=row[0]):
                named = set(backticked(row[1]))
                self.assertLessEqual(named, TYPES | {"NG-11"}, "disposition names an undefined type")
                self.assertTrue(named & TYPES or row[1].startswith("reserved"), "no disposition")
                self.assertTrue(row[2])

    def test_every_claim_type_is_explained(self) -> None:
        body = model_section("2")
        for claim_type in TYPES:
            with self.subTest(type=claim_type):
                self.assertIn(f"`{claim_type}`", body)

    def test_every_ma_status_has_one_disposition(self) -> None:
        table = rows(model_section("3"), 3, "MA §10 evidence status")
        items = [row[0] for row in table]
        self.assertEqual(len(items), len(set(items)))
        self.assertEqual(set(items), set(ma_statuses()))
        for row in table:
            with self.subTest(ma_status=row[0]):
                named = set(backticked(row[1])) & (STATUSES | TYPES)
                self.assertTrue(named, "a disposition names a defined value")
                self.assertLessEqual(set(backticked(row[1])), STATUSES | TYPES)

    def test_every_status_is_explained(self) -> None:
        body = model_section("3")
        for status in STATUSES:
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", body)


class RuleTableTests(unittest.TestCase):
    def test_one_type_row_per_claim_type(self) -> None:
        table = rule_rows()
        self.assertEqual(set(table), TYPES)
        for claim_type, row in table.items():
            with self.subTest(type=claim_type):
                self.assertIn(row["sources"], {"required", "forbidden"})
                self.assertIn(row["inputs"], {"required", "forbidden"})
                self.assertIn(row["reasoning"], {"required", "forbidden"})
                self.assertIn(row["as_of"], {"required", "forbidden"})
                self.assertTrue(row["statuses"], "a type allows no status")
                self.assertIn("unverified", row["statuses"], "every claim starts unverified")
                # A claim either cites sources or rests on inputs, never both.
                self.assertNotEqual(row["sources"], row["inputs"])
                self.assertEqual(bool(row["standing"]), row["sources"] == "required")
                self.assertEqual(row["as_of"], row["sources"])
                self.assertNotEqual(row["reasoning"], row["sources"])

    def test_first_hand_rule(self) -> None:
        # ER-4, ER-6: a FACT needs first-hand standing; a reporter supports at most ATTRIBUTION.
        table = rule_rows()
        self.assertEqual(table["FACT"]["standing"], {"party", "originator"})
        self.assertIn("reporter", table["ATTRIBUTION"]["standing"])

    def test_one_status_row_per_status(self) -> None:
        table = status_rows()
        self.assertEqual(set(table), STATUSES)
        canonical = {s for s, row in table.items() if row["canonical"]}
        self.assertEqual(canonical, {"supported", "disputed"})
        # A claim may never rest on inputs weaker than itself allows (§4).
        self.assertEqual(table["supported"]["inputs"], {"supported"})
        self.assertEqual(table["unverified"]["inputs"], STATUSES)
        for status, row in table.items():
            with self.subTest(status=status):
                self.assertNotIn("context_only", row["inputs"] - ({"context_only"} if status == "unverified" else set()))

    def test_schema_accepted_review_matches_canonical_statuses(self) -> None:
        (rule,) = [r for r in CLAIM_SCHEMA["allOf"] if "review" in r["if"]["properties"]]
        allowed = set(rule["then"]["properties"]["evidence_status"]["enum"])
        self.assertEqual(allowed, {s for s, row in status_rows().items() if row["canonical"]})


class MigrationTableTests(unittest.TestCase):
    def test_every_register_column_has_one_row(self) -> None:
        header = next(cells(l) for l in REGISTER.splitlines() if cells(l)[:1] == ["id"])
        table = rows(model_section("9"), 3, "Register column")
        columns = [backticked(row[0])[0] for row in table]
        self.assertEqual(len(columns), len(set(columns)))
        self.assertEqual(set(columns), set(header))
        properties = set(json.loads(read("schemas/sources.schema.json"))["properties"])
        for row in table:
            with self.subTest(column=row[0]):
                target = backticked(row[1])
                self.assertTrue(target, "target is a field or 'not migrated'")
                self.assertTrue(set(target) <= properties or row[1].startswith("not migrated"), row[1])


class ValidateDataTableTests(unittest.TestCase):
    def test_every_check_names_an_existing_test_that_implements_it(self) -> None:
        table = rows(model_section("11"), 4, "Check")
        ids = [row[0] for row in table]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(any(i.startswith("VD-") for i in ids))
        for row in table:
            if not row[0].startswith("VD-"):
                continue
            with self.subTest(check=row[0]):
                (path,) = backticked(row[2])
                self.assertTrue((REPO_ROOT / path).is_file(), path)
                self.assertRegex(read(path), rf"\b{re.escape(row[0])}\b", "the test does not name the check")


class CitationTests(unittest.TestCase):
    def test_cited_decisions_and_non_goals_exist(self) -> None:
        text = MODEL + json.dumps(CLAIM_SCHEMA)
        for ref in sorted(set(re.findall(r"\b(?:D-\d{3}|NG-\d{2})\b", text))):
            with self.subTest(ref=ref):
                self.assertTrue(decision_exists(ref), ref)

    def test_cited_policy_rules_exist(self) -> None:
        for prefix in ("ER", "SP", "RA"):
            for ref in sorted(set(re.findall(rf"\b{prefix}-\d+\b", MODEL))):
                with self.subTest(rule=ref):
                    self.assertRegex(POLICY, rf"\| {re.escape(ref)} \|")

    def test_cited_sections_exist(self) -> None:
        homes = {
            "source-policy.md": POLICY,
            "entity-taxonomy.md": read("docs/architecture/entity-taxonomy.md"),
            "relationship-taxonomy.md": read("docs/architecture/relationship-taxonomy.md"),
            "claim-model.md": MODEL,
        }
        text = MODEL + json.dumps(CLAIM_SCHEMA) + json.dumps(json.loads(read("schemas/sources.schema.json")))
        for name, home in homes.items():
            for number in sorted(set(re.findall(rf"{re.escape(name)} §(\d+(?:\.\d+)?)", text))):
                with self.subTest(doc=name, section=number):
                    self.assertRegex(home, rf"\n#+ {re.escape(number)}\.? ")

    def test_cited_register_labels_and_source_ids_exist(self) -> None:
        sources = json.loads(read("data/sources.json"))
        ids = {s["id"] for s in sources}
        labels = {s.get("migrated_from") for s in sources}
        for ref in sorted(set(re.findall(r"\b(?:SRC-\d{3}|S05-R\d+)\b", MODEL))):
            with self.subTest(label=ref):
                self.assertIn(ref, labels)
        for ref in sorted(set(re.findall(r"\bsrc-\d{3}\b", MODEL))):
            with self.subTest(source=ref):
                self.assertIn(ref, ids)

    def test_cited_concepts_conflicts_and_deps_exist(self) -> None:
        for ref in sorted(set(re.findall(rf"\b{CONCEPT}\b", MODEL))):
            with self.subTest(concept=ref):
                self.assertIn(f"#### {ref} — ", DOMAIN_MAP)
        for ref in sorted(set(re.findall(r"\b(?:CON|DEP|TQ)-\d{2}\b", MODEL))):
            with self.subTest(ref=ref):
                self.assertRegex(DOMAIN_MAP, rf"(\| {ref} \||\*\*{ref}\b|\| {ref} \|)")

    def test_explainer_anchors_are_verbatim_in_the_domain_map(self) -> None:
        text = model_section("13")
        anchors = [flat(q) for q in re.findall(r'"([^"]+)"', text) if len(q.split()) >= 3]
        self.assertGreaterEqual(len(set(anchors)), 3)
        domain_map = flat(DOMAIN_MAP)
        for anchor in anchors:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, domain_map)


class ProseCountTests(unittest.TestCase):
    def test_vocabulary_counts_in_prose(self) -> None:
        words = {"three": 3, "four": 4, "five": 5, "six": 6, "seven": 7}
        for pattern, expected in (
            (r"The schema has (\w+) claim types", len(TYPES)),
            (r"and (\w+) evidence statuses", len(STATUSES)),
            (r"MA §10 lists (\w+) claim types", len(ma_claim_types())),
            (r"MA §10 lists (\w+) evidence statuses", len(ma_statuses())),
        ):
            with self.subTest(pattern=pattern):
                match = re.search(pattern, MODEL)
                self.assertIsNotNone(match, pattern)
                self.assertEqual(words[match.group(1)], expected)


if __name__ == "__main__":
    unittest.main()
