"""Two remediations of the engineering audit (S22, D-213; docs/architecture/engineering-audit.md).

EN-1 (F-4, A-1) every tracked Python file compiles with the interpreter running the suite. CI runs the suite on
     Python 3.11 (D-004), so a file that only Python 3.12 or later parses fails here in CI, including the files no test
     imports (the audit-evidence scripts); and the CI workflow keeps that version.
EN-2 (F-7) tools/check_all.py runs every check a commit needs, in order: the suite, Gate 0, then the `--check` of every
     tool that has one, in build order (results, HBM page, research view, journeys, brief).

Standard library only.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_all  # noqa: E402


def tracked_python() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "*.py"], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        out = []
    if not out:  # a copy without .git (the break harness)
        out = [p.relative_to(REPO_ROOT).as_posix() for p in REPO_ROOT.rglob("*.py") if ".git" not in p.parts and "__pycache__" not in p.parts]
    return sorted(out)


class EngineeringTests(unittest.TestCase):
    # EN-1
    def test_en1_every_tracked_python_file_compiles(self) -> None:
        files = tracked_python()
        self.assertGreater(len(files), 50)
        failed = []
        for f in files:
            try:
                compile((REPO_ROOT / f).read_text(encoding="utf-8"), f, "exec")
            except SyntaxError as error:
                failed.append(f"{f}:{error.lineno}: {error.msg}")
        self.assertEqual(failed, [], f"files Python {sys.version.split()[0]} cannot parse (CI runs 3.11, D-004)")

    def test_en1_ci_runs_python_3_11(self) -> None:
        ci = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'python-version:\s*"([^"]+)"', ci), ["3.11"])

    # EN-2
    def test_en2_check_all_runs_every_check_in_order(self) -> None:
        commands = [" ".join(step[1:]) for step in check_all.STEPS]
        self.assertEqual(commands[:2], ["-m unittest discover -s tests", "tools/validate_repo.py"])
        with_check = sorted(p.relative_to(REPO_ROOT).as_posix() for p in (REPO_ROOT / "tools").glob("*.py")
                            if '"--check"' in p.read_text(encoding="utf-8") and p.name != "check_all.py")
        checked = [c.split()[0] for c in commands[2:]]
        self.assertEqual(sorted(checked), with_check, "a tool with --check that check_all.py does not run, or the reverse")
        self.assertTrue(all(c.endswith(" --check") for c in commands[2:]))
        order = ["tools/warehouse.py", "tools/build_page.py", "tools/build_insight.py", "tools/build_journeys.py", "tools/build_brief.py"]
        self.assertEqual([c for c in checked if c in order], order, "the checks run out of build order")


if __name__ == "__main__":
    unittest.main()
