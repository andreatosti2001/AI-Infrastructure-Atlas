"""Agent audit, write boundaries (S19, point in time): which files changed since S06 lie in no active role's
ALLOWED_WRITES in docs/agents/contracts.md. Run from the repository root with the test virtualenv:
    python docs/quality/audit-evidence/agent-audit/write_boundaries.py
It reads the contracts as tests/test_agent_contracts.py parses them, and `git log --full-history --name-only`
from S06's first commit (bb47dfc, 2026-09-30, when the contracts were written) to HEAD. A file removed since is
skipped. Output: one line per file, with the number of commits that changed it and the first and last commit."""
import collections
import os
import re
import subprocess
import sys

sys.path.insert(0, "tests")
import test_agent_contracts as t  # noqa: E402

allowed = {}
for role, contract in t.contracts().items():
    for path in re.findall(r"`([^`]+)`", contract["ALLOWED_WRITES"]):
        allowed.setdefault(path, set()).add(role)


def owners(path: str) -> set[str]:
    return {r for p, roles in allowed.items() if path == p or (p.endswith("/") and path.startswith(p)) for r in roles}


log = subprocess.run(["git", "log", "--full-history", "--no-merges", "--format=@%h", "--name-only", "bb47dfc^..HEAD"],
                     capture_output=True, text=True, check=True).stdout
commit, orphan = None, collections.defaultdict(list)
for line in log.splitlines():
    if line.startswith("@"):
        commit = line[1:]
    elif line.strip() and os.path.exists(line) and not owners(line):
        orphan[line].append(commit)
for path in sorted(orphan):
    print(f"{len(orphan[path]):3} commits  {path}   first {orphan[path][-1]}  last {orphan[path][0]}")
print(f"{len(orphan)} files in no active role's ALLOWED_WRITES")
