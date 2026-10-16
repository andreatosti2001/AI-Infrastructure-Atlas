"""Consistency checks for the agent roles and contracts (S06; D-010, D-052, H-3).

- docs/agents/roles.md lists every role of CLAUDE.md §8 exactly once, parsed from CLAUDE.md;
- the roles marked active are exactly the roles with a contract in docs/agents/contracts.md,
  and every inactive role names the session that first activates it;
- every contract has the MA §12 fields, parsed from MA, in MA's order, each filled;
- every allowed write is a path that exists, or a file in a directory that exists;
- every validation gate names test files that exist, and CI runs them (L-02);
- no contract grants a write to canonical claims (data/claims.json) or allows a verdict:
  class C review is the human's (CLAUDE.md §9);
- every tracked file has an owner: a role whose ALLOWED_WRITES names it, or the list of files written only on
  the human's decision ("Outside every contract"). A path ending in / owns the folder; * matches within a name
  (S19, agent audit F-2, D-180).

Standard library only.
"""

import re
import subprocess
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


def human_only() -> list[str]:
    """The paths of contracts.md's "Outside every contract" list: written only on the human's decision."""
    body = CONTRACTS.partition("## Outside every contract")[2].split("\n## ")[0]
    items = re.split(r"^- ", body, flags=re.M)[1:]  # one item: a bullet and its continuation lines
    return [p for item in items for p in re.findall(r"`([^`]+)`", item.split(": ", 1)[0])]


def owned(path: str, patterns: list[str]) -> bool:
    def match(p: str) -> bool:
        if p.endswith("/"):
            return path.startswith(p)
        return re.fullmatch(re.escape(p).replace(r"\*", "[^/]*"), path) is not None
    return any(match(p) for p in patterns)


def tracked_files() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        out = []
    if not out:  # a copy without .git (the break harness): every file in the tree
        out = [p.relative_to(REPO_ROOT).as_posix() for p in REPO_ROOT.rglob("*")
               if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.suffix != ".png"]
    return sorted(out)


class RoleTests(unittest.TestCase):
    def test_every_claude_md_role_is_listed_once(self) -> None:
        names = [row[0] for row in role_rows()]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(claude_roles()))

    def test_active_roles_are_exactly_the_contracted_roles(self) -> None:
        active = {row[0] for row in role_rows() if row[1] == "active"}
        self.assertEqual(active, set(contracts()))
        # S11 (D-107; the human's ruling "Yes, both (Recommended)"): Editorial and QA join the five.
        # S19 (D-181): the Analyst, whose work S14 to S16 did without a contract.
        # S21 (D-205; the human's ruling "Activate Client Output (Recommended)"): the Client Output, for the brief.
        # S21.5 (D-207; the human's instruction to run the later-rule search as a dedicated session): the Change Detector.
        # S24 (D-223; the human's ruling "Audit plus limitations list (Recommended)"): the Portfolio Reviewer.
        self.assertEqual(active, {"Source Scout", "Extractor", "Verifier", "Knowledge Architect", "Data Auditor", "Editorial", "QA", "Analyst", "Client Output", "Change Detector", "Portfolio Reviewer"})

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

    def test_every_tracked_file_has_an_owner(self) -> None:
        patterns = [p for c in contracts().values() for p in re.findall(r"`([^`]+)`", c["ALLOWED_WRITES"])] + human_only()
        self.assertTrue(human_only(), "contracts.md has no 'Outside every contract' list")
        orphans = [f for f in tracked_files() if not owned(f, patterns)]
        self.assertEqual(orphans, [], "files no role and no human-only entry owns (agent audit F-2)")

    def test_owner_patterns_resolve(self) -> None:
        files = tracked_files()
        for pattern in human_only():
            with self.subTest(pattern=pattern):
                self.assertTrue([f for f in files if owned(f, [pattern])], f"{pattern} owns no file")

    def test_no_contract_writes_canonical_claims_or_verdicts(self) -> None:
        for role, contract in contracts().items():
            with self.subTest(role=role):
                self.assertNotIn("data/claims.json", contract["ALLOWED_WRITES"])
                self.assertIn("review", contract["FORBIDDEN_WRITES"])


if __name__ == "__main__":
    unittest.main()
