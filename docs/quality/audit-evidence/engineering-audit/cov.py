"""In-process line coverage of tools/*.py by the unit suite, standard library only (sys.settrace).

    python cov.py REPO OUT.json

Counts the lines of tools/ executed while `unittest discover -s tests` runs in this process. Lines run in a subprocess
(a test that runs a tool as a command) are not counted, so the figures are a lower bound.
"""

import json
import sys
import threading
import types
import unittest
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
TOOLS = str(REPO / "tools") + "/"
hit: dict[str, set[int]] = {}


def tracer(frame, event, arg):
    f = frame.f_code.co_filename
    if not f.startswith(TOOLS):
        return None
    lines = hit.setdefault(f, set())

    def local(frame, event, arg):
        if event == "line":
            lines.add(frame.f_lineno)
        return local
    lines.add(frame.f_lineno)
    return local


def executable(path: Path) -> set[int]:
    code = compile(path.read_text(encoding="utf-8"), str(path), "exec")
    lines = set()
    stack = [code]
    while stack:
        c = stack.pop()
        lines |= {l for _, _, l in c.co_lines() if l is not None}
        stack += [k for k in c.co_consts if isinstance(k, types.CodeType)]
    return lines


sys.path.insert(0, str(REPO / "tests"))
sys.path.insert(0, str(REPO / "tools"))
import os  # noqa: E402
os.chdir(REPO)
sys.settrace(tracer)
threading.settrace(tracer)
suite = unittest.defaultTestLoader.discover(str(REPO / "tests"))
result = unittest.TextTestRunner(stream=open(os.devnull, "w"), verbosity=0).run(suite)
sys.settrace(None)
threading.settrace(None)
report = {"tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "files": {}}
total_e = total_h = 0
for p in sorted((REPO / "tools").glob("*.py")):
    e = executable(p)
    h = hit.get(str(p), set()) & e
    total_e += len(e)
    total_h += len(h)
    missed = sorted(e - h)
    report["files"][p.name] = {"executable": len(e), "run": len(h), "percent": round(100 * len(h) / len(e), 1), "missed_lines": missed}
report["total"] = {"executable": total_e, "run": total_h, "percent": round(100 * total_h / total_e, 1)}
OUT.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
print(json.dumps({k: (v if k != "files" else {f: (x["run"], x["executable"], x["percent"]) for f, x in v.items()}) for k, v in report.items()}, indent=1))
