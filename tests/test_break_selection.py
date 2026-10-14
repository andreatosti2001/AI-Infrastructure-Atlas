"""The break harness's full-run trigger (D-177, amended by D-188).

A change to a check module, a schema, Gate 0 or the harness's code selects the full harness: selection by the
files a setup touches cannot see a check that was loosened. A change to the harness's documentation does not:
no check reads it, and Gate 0 checks its links on every push. Standard library only.
"""

import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("break_runner", REPO_ROOT / "tests/regression/runner.py")
runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runner)


class FullRunTriggerTests(unittest.TestCase):
    def test_check_schema_gate0_and_harness_code_select_the_full_harness(self) -> None:
        for path in ("tests/test_data_relationships.py", "schemas/claims.schema.json", "tools/validate_repo.py",
                     "tests/regression/runner.py", "tests/regression/breaks.py", "tests/regression/breaks_sql.py"):
            with self.subTest(path=path):
                self.assertEqual(runner.full_run_trigger([path]), [path])

    def test_harness_documentation_does_not(self) -> None:
        self.assertEqual(runner.full_run_trigger(["tests/regression/README.md"]), [])

    def test_other_files_do_not(self) -> None:
        for path in ("README.md", "data/claims.json", "tools/build_page.py", "docs/architecture/decisions.md"):
            with self.subTest(path=path):
                self.assertEqual(runner.full_run_trigger([path]), [])


if __name__ == "__main__":
    unittest.main()
