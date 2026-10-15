"""Every check a commit needs, in one command (S22, D-213; engineering audit F-7; MA §15).

    python tools/check_all.py        run the suite, Gate 0 and every --check, in order; stop at the first failure

Run it on Python 3.11, the version CI uses (D-004), immediately before each commit: after the last edit, not before
it. Every page reads docs/architecture/decisions.md and its other inputs, so an edit made after a rebuild leaves a page
stale, and only a --check run after the edit sees it (S21.5's red CI). The browser checks are separate
(tests/browser/README.md; CI runs them). Standard library only (D-003).
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# (what it checks, arguments after the interpreter), in the order a commit needs them: the suite, Gate 0, then every
# build's --check in build order (results -> HBM page -> research view -> journeys -> brief).
STEPS = (
    ("the suite", "-m", "unittest", "discover", "-s", "tests"),
    ("Gate 0, repository integrity", "tools/validate_repo.py"),
    ("the SQL results", "tools/warehouse.py", "--check"),
    ("the HBM page", "tools/build_page.py", "--check"),
    ("the research view", "tools/build_insight.py", "--check"),
    ("the 15 journey pages", "tools/build_journeys.py", "--check"),
    ("the client brief", "tools/build_brief.py", "--check"),
)


def main() -> int:
    if sys.version_info[:2] != (3, 11):
        print(f"note: Python {sys.version.split()[0]}; CI runs 3.11 (D-004), so a pass here is not yet CI's pass", flush=True)
    for what, *args in STEPS:
        start = time.monotonic()
        done = subprocess.run([sys.executable, *args], cwd=REPO_ROOT, capture_output=True, text=True)
        took = time.monotonic() - start
        if done.returncode != 0:
            print(f"FAIL  {what} ({' '.join(args)}), {took:.1f} s\n{done.stdout[-4000:]}{done.stderr[-4000:]}", flush=True)
            return 1
        print(f"ok    {what}, {took:.1f} s", flush=True)
    print("every check passed: ready to commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
