"""Consistency checks for the agent roles and contracts (S06; D-010, D-052, H-3).

- docs/agents/roles.md lists every role of CLAUDE.md §8 exactly once, parsed from CLAUDE.md;
- the roles marked active are exactly the roles with a contract in docs/agents/contracts.md,
  and every inactive role names the session that first activates it;
- every contract has the MA §12 fields, parsed from MA, in MA's order, each filled;
- every allowed write is a path that exists, or a file in a directory that exists;
- every validation gate names test files that exist, and CI runs them (L-02);
- no contract grants a write to canonical claims (data/claims.json) or allows a verdict:
  class C review is the human's (CLAUDE.md §9).

Standard library only.
"""

import re
import unittest
from pathlib import Path

from test_entity_taxonomy import cells, section

REPO_ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    target = REPO_ROOT / path
    return target.read_text(encoding="utf-8") if target.is_file() else ""


CLAUDE = read("CLAUDE.md")
MASTER = read("MASTER-ARCHITECTURE.md")
ROLES = read("docs/agents/roles.md")
CONTRACTS = read("docs/agents/contracts.md")
CI = read(".github/workflows/ci.yml")


def claude_roles() -> list[str]:
    body = section(CLAUDE, "Primary roles:", "### Orchestrator")
    return [line[2:].strip() for line in body.splitlines() if line.startswith("- ")]


def ma_fields() -> list[str]:
    body = section(MASTER, "## 12. Agent contract format", "Example:")
    block = body[body.index("```text") + len("```text") : body.rindex("```")]
    return [line.strip() for line in block.splitlines() if line.strip()]


def role_rows() -> list[list[str]]:
    result = []
    for line in ROLES.splitlines():
        row = cells(line)
        if row and row[0] not in {"Role", ""} and not set(row[0]) <= {"-", ":"}:
            assert len(row) == 5, f"roles.md row {row[0]!r} has {len(row)} cells"
            result.append(row)
    return result


def contracts() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    parts = re.split(r"^## ", CONTRACTS, flags=re.MULTILINE)[1:]
    for part in parts:
        title, _, body = part.partition("\n")
        fields = {}
        for line in body.splitlines():
            row = cells(line)
            if len(row) == 2 and re.fullmatch(r"[A-Z_]+", row[0]):
                assert row[0] not in fields, f"{title}: {row[0]} twice"
                fields[row[0]] = row[1]
        if fields:
            result[title.strip()] = fields
    return result


class RoleTests(unittest.TestCase):
    def test_every_claude_md_role_is_listed_once(self) -> None:
        names = [row[0] for row in role_rows()]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(claude_roles()))

    def test_active_roles_are_exactly_the_contracted_roles(self) -> None:
        active = {row[0] for row in role_rows() if row[1] == "active"}
        self.assertEqual(active, set(contracts()))
        # S11 (D-107; the human's ruling "Yes, both (Recommended)"): Editorial and QA join the five.
        self.assertEqual(active, {"Source Scout", "Extractor", "Verifier", "Knowledge Architect", "Data Auditor", "Editorial", "QA"})

    def test_inactive_roles_name_their_first_session(self) -> None:
        for row in role_rows():
            with self.subTest(role=row[0]):
                self.assertIn(row[1], {"active", "inactive"})
                if row[1] == "inactive":
                    self.assertRegex(row[4], r"\bS\d{2}\b")


class ContractTests(unittest.TestCase):
    def test_every_contract_has_the_ma_fields_in_order(self) -> None:
        fields = ma_fields()
        self.assertEqual(len(fields), 9)
        for role, contract in contracts().items():
            with self.subTest(role=role):
                self.assertEqual(list(contract), fields)
                for name, value in contract.items():
                    self.assertTrue(value.strip() and value.strip() != "—", f"{name} is empty")
                self.assertEqual(contract["ROLE"], role)

    def test_allowed_writes_exist(self) -> None:
        for role, contract in contracts().items():
            for path in re.findall(r"`([^`]+)`", contract["ALLOWED_WRITES"]):
                with self.subTest(role=role, path=path):
                    target = REPO_ROOT / path.rstrip("/")
                    self.assertTrue(target.exists() or target.parent.is_dir(), path)

    def test_validation_gates_are_tests_that_ci_runs(self) -> None:
        self.assertIn("unittest discover -s tests", CI)
        for role, contract in contracts().items():
            gates = re.findall(r"`(tests/test_[a-z_]+\.py)`", contract["VALIDATION_GATE"])
            with self.subTest(role=role):
                self.assertTrue(gates, "no CI-run test named")
                for gate in gates:
                    self.assertTrue((REPO_ROOT / gate).is_file(), gate)

    def test_no_contract_writes_canonical_claims_or_verdicts(self) -> None:
        for role, contract in contracts().items():
            with self.subTest(role=role):
                self.assertNotIn("data/claims.json", contract["ALLOWED_WRITES"])
                self.assertIn("review", contract["FORBIDDEN_WRITES"])


if __name__ == "__main__":
    unittest.main()
