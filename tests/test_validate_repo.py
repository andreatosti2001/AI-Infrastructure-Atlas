import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import validate_repo  # noqa: E402


def make_valid_repo(root: Path) -> None:
    for rel in validate_repo.REQUIRED_FILES:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# placeholder\n", encoding="utf-8")


class ValidateRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_valid_repo(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_valid_repo_passes(self) -> None:
        self.assertEqual(validate_repo.validate(self.root), [])

    def test_missing_constitutional_doc_fails(self) -> None:
        (self.root / "MASTER-ARCHITECTURE.md").unlink()
        self.assertEqual(
            validate_repo.validate(self.root),
            ["missing required file: MASTER-ARCHITECTURE.md"],
        )

    def test_the_human_review_record_is_required(self) -> None:
        # D-151: canonical claims name it as the record of the human's verdicts
        self.assertIn("docs/quality/human-reviews.md", validate_repo.REQUIRED_FILES)

    def test_relative_links_resolve(self) -> None:
        self.write("docs/a.md", "# A\n\n## Second part\n\nSee [b](b.md), [the root](../README.md) and [here](#second-part).\n")
        self.write("docs/b.md", "# B\n\nBack to [a](./a.md#second-part); a folder: [docs](../docs/).\n")
        self.assertEqual(validate_repo.validate(self.root), [])

    def test_a_link_to_a_missing_file_fails(self) -> None:
        self.write("docs/a.md", "# A\n\nline two\n[gone](../sessions/reports/SESSION-07-REPORT.md)\n")
        self.assertEqual(
            validate_repo.validate(self.root),
            ["docs/a.md:4: link to a missing file: ../sessions/reports/SESSION-07-REPORT.md"],
        )

    def test_a_link_to_a_missing_heading_fails(self) -> None:
        self.write("docs/a.md", "# A\n\n## Kept\n")
        self.write("docs/b.md", "[x](a.md#gone) [y](#nowhere)\n")
        self.assertEqual(
            validate_repo.validate(self.root),
            ["docs/b.md:1: link to a missing heading: a.md#gone", "docs/b.md:1: link to a missing heading: #nowhere"],
        )

    def test_external_links_code_and_fenced_blocks_are_not_checked(self) -> None:
        self.write("docs/a.md", "# A\n\n[web](https://example.org/x) [mail](mailto:a@b.c) `[code](gone.md)`\n\n"
                                "```text\n[fenced](gone.md)\n```\n")
        self.assertEqual(validate_repo.validate(self.root), [])

    def test_git_and_scratch_folders_are_not_walked(self) -> None:
        self.write(".git/x.md", "[gone](gone.md)\n")
        self.write("node_modules/x.md", "[gone](gone.md)\n")
        self.assertEqual(validate_repo.validate(self.root), [])

    def test_session_records_are_refused_in_the_public_tree(self) -> None:
        # D-152: session prompts, reports and their working folders belong in the private archive repository
        cases = (("sessions/reports/SESSION-17-REPORT.md", "sessions/"), ("sessions/prompts/S17-PROMPT.md", "sessions/"),
                 ("sessions/reports/SESSION-17-qa/x.md", "sessions/"), ("PROMPT-REGISTRY.md", "PROMPT-REGISTRY.md"),
                 ("docs/SESSION-17.5-REPORT.md", "docs/SESSION-17.5-REPORT.md"), ("notes/S18-PROMPT.md", "notes/S18-PROMPT.md"))
        for rel, reported in cases:
            with self.subTest(path=rel):
                self.write(rel, "# x\n")
                self.assertEqual(
                    validate_repo.validate(self.root),
                    [f"session record in the public repository (D-152): {reported}"],
                )
                path = self.root / rel
                path.unlink()
                for parent in path.relative_to(self.root).parents:
                    folder = self.root / parent
                    if folder != self.root and not any(folder.iterdir()):
                        folder.rmdir()

    def test_documents_about_sessions_are_not_session_records(self) -> None:
        self.write("SESSION-PROMPT-SPEC.md", "# spec\n")
        self.write("docs/session-notes.md", "# not a record\n")
        self.assertEqual(validate_repo.validate(self.root), [])

    def test_heading_anchors_follow_githubs_rule(self) -> None:
        text = ("# Human review record\n## Companies and jurisdictions, 2026-10-01\n## SK hynix HBM3 statement, 2026-10-07\n"
                "### 4. Build/Audit cadence\n## `recorded_in` and D-151 — the rule\n## Twice\n## Twice\n")
        self.assertEqual(
            validate_repo.markdown_anchors(text),
            {"human-review-record", "companies-and-jurisdictions-2026-10-01", "sk-hynix-hbm3-statement-2026-10-07",
             "4-buildaudit-cadence", "recorded_in-and-d-151--the-rule", "twice", "twice-1"},
        )

    def test_the_repository_itself_passes(self) -> None:
        self.assertEqual(validate_repo.validate(REPO_ROOT), [])

    def test_main_reports_status(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = validate_repo.main(["validate_repo.py", str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("Repository integrity: OK", buffer.getvalue())

        (self.root / "CLAUDE.md").unlink()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = validate_repo.main(["validate_repo.py", str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn("FAILED", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
