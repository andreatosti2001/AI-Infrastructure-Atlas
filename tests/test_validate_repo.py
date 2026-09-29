import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import validate_repo  # noqa: E402

VALID_REPORT = "# Report\n\n" + "".join(
    f"## {section}\n\ncontent\n\n" for section in validate_repo.REPORT_SECTIONS
)


def make_valid_repo(root: Path) -> None:
    for rel in validate_repo.REQUIRED_FILES:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# placeholder\n", encoding="utf-8")
    (root / "sessions/prompts/PROMPT-REGISTRY.md").write_text(
        "| S00 | [`S00-PROMPT.md`](./S00-PROMPT.md) |\n", encoding="utf-8"
    )
    (root / "sessions/prompts/S00-PROMPT.md").write_text("# S00\n", encoding="utf-8")
    reports = root / "sessions/reports"
    reports.mkdir(parents=True)
    (reports / "SESSION-00-REPORT.md").write_text(VALID_REPORT, encoding="utf-8")


class ValidateRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_valid_repo(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_valid_repo_passes(self) -> None:
        self.assertEqual(validate_repo.validate(self.root), [])

    def test_missing_constitutional_doc_fails(self) -> None:
        (self.root / "MASTER-ARCHITECTURE.md").unlink()
        self.assertEqual(
            validate_repo.validate(self.root),
            ["missing required file: MASTER-ARCHITECTURE.md"],
        )

    def test_report_missing_section_fails(self) -> None:
        report = self.root / "sessions/reports/SESSION-00-REPORT.md"
        report.write_text(VALID_REPORT.replace("## Deviations", "## Other"), encoding="utf-8")
        self.assertEqual(
            validate_repo.validate(self.root),
            ["sessions/reports/SESSION-00-REPORT.md: missing section '## Deviations'"],
        )

    def test_section_heading_match_is_case_insensitive(self) -> None:
        report = self.root / "sessions/reports/SESSION-00-REPORT.md"
        report.write_text(VALID_REPORT.upper(), encoding="utf-8")
        self.assertEqual(validate_repo.validate(self.root), [])

    def test_section_must_be_level_two_heading(self) -> None:
        report = self.root / "sessions/reports/SESSION-00-REPORT.md"
        report.write_text(VALID_REPORT.replace("## Tests run", "### Tests run"), encoding="utf-8")
        self.assertEqual(
            validate_repo.validate(self.root),
            ["sessions/reports/SESSION-00-REPORT.md: missing section '## Tests run'"],
        )

    def test_report_without_prompt_fails(self) -> None:
        (self.root / "sessions/reports/SESSION-01-REPORT.md").write_text(VALID_REPORT, encoding="utf-8")
        self.assertEqual(
            validate_repo.validate(self.root),
            ["sessions/reports/SESSION-01-REPORT.md: no matching prompt sessions/prompts/S01-PROMPT.md"],
        )

    def test_unregistered_prompt_fails(self) -> None:
        (self.root / "sessions/prompts/S01-PROMPT.md").write_text("# S01\n", encoding="utf-8")
        self.assertEqual(
            validate_repo.validate(self.root),
            ["sessions/prompts/S01-PROMPT.md: not listed in PROMPT-REGISTRY.md"],
        )

    def test_misnamed_session_files_fail(self) -> None:
        (self.root / "sessions/prompts/s02-prompt.md").write_text("x", encoding="utf-8")
        (self.root / "sessions/reports/S00-REPORT.md").write_text("x", encoding="utf-8")
        self.assertEqual(
            validate_repo.validate(self.root),
            [
                "sessions/prompts/s02-prompt.md: name must match SNN-PROMPT.md",
                "sessions/reports/S00-REPORT.md: name must match SESSION-NN-REPORT.md",
            ],
        )

    def test_main_exit_status(self) -> None:
        with redirect_stdout(io.StringIO()):
            self.assertEqual(validate_repo.main(["validate_repo.py", str(self.root)]), 0)
            (self.root / "CLAUDE.md").unlink()
            self.assertEqual(validate_repo.main(["validate_repo.py", str(self.root)]), 1)


class RealRepositoryTest(unittest.TestCase):
    def test_repository_passes_its_own_integrity_check(self) -> None:
        self.assertEqual(validate_repo.validate(REPO_ROOT), [])


if __name__ == "__main__":
    unittest.main()
