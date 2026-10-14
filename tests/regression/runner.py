"""The break harness's runner: parallel copies, one combined result, and selection by measured files (D-177, D-178).

Every break is (id, what, mutate(root), build steps, expected fragments); `breaks.py` builds the list. The runner
copies the repository (without .git) into SCRATCH/NNN-ID, one folder per break, numbered because some IDs name two
breaks. It plants the edit, runs the build steps in their order (results -> HBM page -> research view -> research journeys), runs the
whole suite, and counts the break only if the suite fails with every expected fragment in its output; a control
counts only if the suite passes. The method and the rule are those of the earlier runner (breaks_metrics.run);
only the scheduling changes: N breaks at a time, lines printed in the harness's order, then one summary.

Selection (D-177): a break's files are measured, never declared. Its setup is applied to a scratch copy and the
files whose bytes change, appear or disappear are its files. A break is selected when one of its files, or a tool
its build steps run, is among the changed files. A change to a check module, a schema, Gate 0 or the harness's
code selects every break: selection by setup files cannot see a check that was loosened. The harness's
documentation does not (D-188).

Standard library only (D-003).
"""

from __future__ import annotations

import fnmatch
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.png")
# A change to one of these selects the full harness (D-177): the checks, the schemas they apply, Gate 0, the harness's
# code. Not the harness's documentation (D-188): no check reads it, and Gate 0 checks its links on every push.
FULL_RUN_PATTERNS = ("tests/test_*.py", "schemas/*", "tools/validate_repo.py", "tests/regression/*.py")


def folder(index: int, bid: str) -> str:
    return f"{index:03d}-{re.sub(r'[^A-Za-z0-9.-]', '_', bid)}"


def run_one(index: int, brk, scratch: Path, setup_only: bool) -> tuple[str, bool | None]:
    """One break in its own copy. Returns (line, ok); ok is None for a setup that no longer applies."""
    bid, what, mutate, steps, expected = brk
    root = scratch / folder(index, bid)
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(REPO, root, ignore=IGNORE)
    try:
        try:
            mutate(root)
        except SystemExit as stale:
            return f"{bid:10} {'SETUP STALE':24} {what} | {stale}", None
        if setup_only:
            return f"{bid:10} {'setup applies':24} {what}", True
        py = sys.executable
        for tool in steps:
            subprocess.run([py, tool], cwd=root, capture_output=True, text=True)
        res = subprocess.run([py, "-m", "unittest", "discover", "-s", "tests"], cwd=root, capture_output=True, text=True)
        out = res.stdout + res.stderr
        if not expected:
            ok = res.returncode == 0
            verdict = "passes, as it must" if ok else "CONTROL FAILED"
        else:
            missing = [f for f in expected if f not in out]
            ok = res.returncode != 0 and not missing
            verdict = "caught" if ok else f"NOT CAUGHT as named (missing {missing})"
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", out, re.M)))
        return f"{bid:10} {verdict:24} {what} | failed: {', '.join(failed) or '-'}", ok
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run(breaks, scratch: Path, wanted: set[str], setup_only: bool = False, jobs: int = 1, out: Path | None = None) -> int:
    """Run the wanted breaks (all if none named), `jobs` at a time. Returns the number of breaks not as they must be."""
    chosen = [(i, b) for i, b in enumerate(breaks) if not wanted or b[0] in wanted]
    unknown = sorted(wanted - {b[0] for b in breaks})
    if unknown:
        raise SystemExit(f"no break with ID: {' '.join(unknown)}")
    scratch.mkdir(parents=True, exist_ok=True)
    lines, tally = [], {"fault": [0, 0], "control": [0, 0], "stale": 0}
    sink = out.open("w", encoding="utf-8") if out else None
    try:
        with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
            futures = [(b, pool.submit(run_one, i, b, scratch, setup_only)) for i, b in chosen]
            for brk, fut in futures:  # in the harness's order, each printed as soon as it and those before it are done
                line, ok = fut.result()
                print(line, flush=True)
                lines.append(line)
                if sink:
                    sink.write(line + "\n")
                    sink.flush()
                if ok is None:
                    tally["stale"] += 1
                else:
                    kind = "control" if not brk[4] else "fault"
                    tally[kind][0] += bool(ok)
                    tally[kind][1] += 1
        bad = tally["stale"] + (tally["fault"][1] - tally["fault"][0]) + (tally["control"][1] - tally["control"][0])
        if setup_only:
            summary = f"setups applying: {len(chosen) - tally['stale']} of {len(chosen)}; stale setups: {tally['stale']}"
        else:
            summary = (f"faults caught as named: {tally['fault'][0]} of {tally['fault'][1]}; "
                       f"controls passing: {tally['control'][0]} of {tally['control'][1]}; stale setups: {tally['stale']}")
        print(summary, flush=True)
        if sink:
            sink.write(summary + "\n")
        return bad
    finally:
        if sink:
            sink.close()


def digest(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts}


def touched(breaks) -> list[tuple[str, str, list[str], list[str]]]:
    """(id, what, measured files, build steps) for every break: its setup applied to a copy, its files measured."""
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "base"
        shutil.copytree(REPO, base, ignore=IGNORE)
        before = digest(base)
        for i, (bid, what, mutate, steps, _) in enumerate(breaks):
            root = Path(tmp) / folder(i, bid)
            shutil.copytree(base, root)
            try:
                mutate(root)
            except SystemExit as stale:
                raise SystemExit(f"{bid}: setup stale, files cannot be measured ({stale})")
            after = digest(root)
            files = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
            rows.append((bid, what, files, list(steps)))
            shutil.rmtree(root)
    return rows


def changed_since(rev: str) -> list[str]:
    """The files changed since REV, committed or not, plus untracked files."""
    diff = subprocess.run(["git", "diff", "--name-only", rev], cwd=REPO, capture_output=True, text=True, check=True)
    new = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=REPO, capture_output=True, text=True, check=True)
    return sorted(set(diff.stdout.split()) | set(new.stdout.split()))


def full_run_trigger(changed: list[str]) -> list[str]:
    """The changed files that select the full harness (D-177, D-188): a check, a schema, Gate 0 or the harness's code."""
    return [c for c in changed if any(fnmatch.fnmatch(c, p) for p in FULL_RUN_PATTERNS)]


def select(breaks, changed: list[str]) -> tuple[list[str], list[str]]:
    """(selected IDs in the harness's order, the reasons printed). D-177."""
    full = full_run_trigger(changed)
    if full:
        return list(dict.fromkeys(b[0] for b in breaks)), [f"full harness: a check, schema, Gate 0 or harness file changed ({', '.join(full)})"]
    wanted, reasons = {}, []
    changed_set = set(changed)
    for bid, what, files, steps in touched(breaks):
        hit = sorted((set(files) | set(steps)) & changed_set)
        if hit:
            wanted.setdefault(bid, None)
            reasons.append(f"{bid:10} {', '.join(hit)} | {what}")
    return list(wanted), reasons
