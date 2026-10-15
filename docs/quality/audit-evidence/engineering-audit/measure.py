"""S22 engineering audit: recountable measurements of the repository (standard library only).

    python measure.py REPO OUT.json      # prints a readable summary and writes every number to OUT.json

Every number in docs/architecture/engineering-audit.md that is labelled "measured" comes from this script, run on
the commit the audit names. It reads the repository; it writes nothing in it.
"""

from __future__ import annotations

import ast
import collections
import gzip
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
R: dict = {}


def tracked() -> list[str]:
    return subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True).stdout.split()


FILES = tracked()
PY = [f for f in FILES if f.endswith(".py")]


def code_lines(text: str) -> int:
    n = 0
    in_doc = False
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        n += 1
    return n


# ---- 1. size ---------------------------------------------------------------------------------------------------
size = {}
for group, pred in {
    "tools/*.py": lambda f: f.startswith("tools/") and f.endswith(".py"),
    "tools/*.html (templates)": lambda f: f.startswith("tools/") and f.endswith(".html"),
    "tests/test_*.py": lambda f: re.fullmatch(r"tests/test_\w+\.py", f),
    "tests/regression/*.py": lambda f: f.startswith("tests/regression/") and f.endswith(".py"),
    "tests/browser/*.js": lambda f: f.startswith("tests/browser/") and f.endswith(".js"),
    "sql/*.sql": lambda f: re.fullmatch(r"sql/\w+\.sql", f),
    "schemas/": lambda f: f.startswith("schemas/"),
    "data/*.json": lambda f: f.startswith("data/") and f.endswith(".json"),
    "site/ (generated)": lambda f: f.startswith("site/"),
    "docs/ (markdown)": lambda f: f.startswith("docs/") and f.endswith(".md"),
}.items():
    fs = [f for f in FILES if pred(f)]
    texts = [(REPO / f).read_text(encoding="utf-8", errors="replace") for f in fs]
    size[group] = {"files": len(fs), "lines": sum(t.count("\n") for t in texts), "bytes": sum(len(t.encode()) for t in texts)}
R["size"] = size
R["size_per_tool"] = {f: (REPO / f).read_text().count("\n") for f in FILES if f.startswith("tools/") and f.endswith(".py")}

# ---- 2. functions, complexity, classes -------------------------------------------------------------------------
BRANCH = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.IfExp, ast.ExceptHandler, ast.comprehension, ast.Match)
funcs, classes = [], []
for f in PY:
    if not (f.startswith("tools/") or f.startswith("tests/")):
        continue
    tree = ast.parse((REPO / f).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            branches = sum(isinstance(n, BRANCH) for n in ast.walk(node)) + sum(len(n.values) - 1 for n in ast.walk(node) if isinstance(n, ast.BoolOp))
            funcs.append({"file": f, "name": node.name, "line": node.lineno, "length": node.end_lineno - node.lineno + 1, "complexity": 1 + branches})
        if isinstance(node, ast.ClassDef):
            classes.append({"file": f, "name": node.name, "bases": [ast.unparse(b) for b in node.bases], "methods": sum(isinstance(n, ast.FunctionDef) for n in node.body)})
tools_funcs = [x for x in funcs if x["file"].startswith("tools/")]
lengths = sorted(x["length"] for x in tools_funcs)
R["functions"] = {
    "tools_count": len(tools_funcs),
    "tools_median_length": lengths[len(lengths) // 2],
    "tools_over_50_lines": sum(l > 50 for l in lengths),
    "tools_over_100_lines": sum(l > 100 for l in lengths),
    "tools_complexity_over_15": sum(x["complexity"] > 15 for x in tools_funcs),
    "longest_tools": sorted(tools_funcs, key=lambda x: -x["length"])[:12],
    "most_complex_tools": sorted(tools_funcs, key=lambda x: -x["complexity"])[:12],
}
R["classes_tools"] = [c for c in classes if c["file"].startswith("tools/")]

# ---- 3. imports: local graph and third-party -------------------------------------------------------------------
stdlib = set(sys.stdlib_module_names)
local_tools = {Path(f).stem for f in FILES if f.startswith("tools/") and f.endswith(".py")}
graph, third = {}, collections.defaultdict(list)
for f in PY:
    tree = ast.parse((REPO / f).read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            mods.add(node.module.split(".")[0])
    local = sorted(m for m in mods if m in local_tools)
    if f.startswith("tools/"):
        graph[f] = local
    for m in sorted(mods - stdlib - local_tools - {"__future__"}):
        if not (REPO / "tests" / f"{m}.py").exists() and not (REPO / "tests/regression" / f"{m}.py").exists():
            third[m].append(f)
R["imports_tools_graph"] = graph
R["third_party_imports"] = dict(third)

# ---- 4. record IDs typed into build code and templates ---------------------------------------------------------
ID = re.compile(r"\b(cand-\d{3}|claim-[a-z0-9-]+|rel-[a-z0-9-]+|(?:company|component|technology|product|facility|policy|jurisdiction)-[a-z0-9-]+|src-\d{3}|event-[a-z0-9-]+)\b")
ids = {}
for f in FILES:
    if f.startswith("tools/") and (f.endswith(".py") or f.endswith(".html")) and f != "tools/later_rule_search.py":
        text = (REPO / f).read_text(encoding="utf-8")
        tree_strings = []
        if f.endswith(".py"):
            tree = ast.parse(text)
            docs = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and ast.get_docstring(node, clean=False):
                    docs.add(id(node.body[0].value))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
                    tree_strings.append(node.value)
            hay = "\n".join(tree_strings)
        else:
            hay = text
        found = sorted(set(m.group(1) for m in ID.finditer(hay)))
        found = [x for x in found if not x.startswith(("policy-us-fr-", "rel-policy")) or True]
        if found:
            ids[f] = found
R["record_ids_in_code"] = {f: {"count": len(v), "ids": v} for f, v in ids.items()}

# ---- 5. labels (A-2) ---------------------------------------------------------------------------------------------
labels = {}
for f in ("tools/build_page.py", "tools/build_insight.py", "tools/build_journeys.py", "tools/build_brief.py"):
    tree = ast.parse((REPO / f).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [ast.unparse(t) for t in targets]
            if any(re.search(r"LABELS$", n) for n in names) and isinstance(node.value, (ast.Dict, ast.Set, ast.List, ast.Tuple, ast.Call, ast.BinOp)):
                elts = [n for n in ast.walk(node.value) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
                labels.setdefault(f, {})[" ".join(names)] = len(elts)
R["labels"] = labels
text_all = {f: (REPO / f).read_text(encoding="utf-8") for f in ("tools/build_page.py", "tools/build_insight.py", "tools/build_journeys.py", "tools/build_brief.py")}
R["label_text_definitions"] = {f: len(re.findall(r"def label_text\b", t)) for f, t in text_all.items()}
R["endpoint_signatures"] = {f: re.findall(r"def endpoint\(([^)]*)\)", t) for f, t in text_all.items() if "def endpoint" in t}

# ---- 6. duplication across tools ---------------------------------------------------------------------------------
W = 6
windows = collections.defaultdict(set)
for f in FILES:
    if f.startswith("tools/") and f.endswith(".py"):
        lines = [re.sub(r"\s+", " ", l.strip()) for l in (REPO / f).read_text(encoding="utf-8").splitlines()]
        lines = [l for l in lines if l and not l.startswith("#") and len(l) > 3]
        for i in range(len(lines) - W + 1):
            windows["\n".join(lines[i:i + W])].add(f)
dup = {k: v for k, v in windows.items() if len(v) > 1}
R["duplication"] = {"window_lines": W, "windows_in_two_or_more_tools": len(dup),
                    "pairs": collections.Counter(" + ".join(sorted(v)) for v in dup.values()).most_common(10),
                    "examples": [k.split("\n")[0][:120] for k in list(dup)[:8]]}

# ---- 7. tests: counts, rule IDs documented vs tested -------------------------------------------------------------
tests = {}
for f in FILES:
    if re.fullmatch(r"tests/test_\w+\.py", f):
        tree = ast.parse((REPO / f).read_text(encoding="utf-8"))
        names = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
        doc = ast.get_docstring(tree) or ""
        rules = sorted(set(re.findall(r"^\s*([A-Z]{2,3}-\d+)\b", doc, re.M)), key=lambda r: (r.split("-")[0], int(r.split("-")[1])))
        untested = [r for r in rules if not any(n.startswith("test_" + r.replace("-", "").lower() + "_") for n in names)]
        tests[f] = {"tests": len(names), "rules_in_docstring": len(rules), "rules_without_a_named_test": untested}
R["tests"] = tests
R["tests_total_methods"] = sum(v["tests"] for v in tests.values())

# ---- 8. break coverage per test module ---------------------------------------------------------------------------
sys.path.insert(0, str(REPO / "tests/regression"))
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("breaks_all", REPO / "tests/regression/breaks.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
breaks = mod.breaks()
name_to_module = {}
for f in tests:
    tree = ast.parse((REPO / f).read_text(encoding="utf-8"))
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name.startswith("test_"):
            name_to_module.setdefault(n.name, set()).add(f)
per_module = collections.Counter()
faults = [b for b in breaks if b[4]]
controls = [b for b in breaks if not b[4]]
unnamed = 0
for b in faults:
    mods = set()
    for frag in b[4]:
        mods |= name_to_module.get(frag, set())
    if not mods:
        unnamed += 1
    for m in mods:
        per_module[m] += 1
R["breaks"] = {"total": len(breaks), "faults": len(faults), "controls": len(controls),
               "faults_naming_only_a_message": unnamed,
               "faults_per_test_module": dict(sorted(per_module.items())),
               "test_modules_no_break_names": sorted(set(tests) - set(per_module))}
pf = (REPO / "tests/test_planted_faults.py").read_text(encoding="utf-8")
R["breaks"]["permanent_in_suite"] = len(set(re.findall(r'"((?:S\d+(?:\.\d+)?|D\d+)-[A-Z]?\d+)"', pf)))

# ---- 9. determinism: clocks and environment in tools -------------------------------------------------------------
det = {}
for f in FILES:
    if f.startswith("tools/") and f.endswith(".py"):
        t = (REPO / f).read_text(encoding="utf-8")
        hits = re.findall(r"datetime\.(?:datetime\.)?now|date\.today|time\.time\(|os\.environ|platform\.|random\.|uuid", t)
        if hits:
            det[f] = collections.Counter(hits)
R["clock_or_environment_in_tools"] = {k: dict(v) for k, v in det.items()}

# ---- 10. pages: weight and structure -----------------------------------------------------------------------------
pages = {}
for f in FILES:
    if f.startswith("site/") and f.endswith(".html"):
        b = (REPO / f).read_bytes()
        t = b.decode()
        pages[f] = {"bytes": len(b), "gzip": len(gzip.compress(b, 9, mtime=0)), "elements": len(re.findall(r"<[a-zA-Z]", t)),
                    "svg": t.count("<svg"), "data_ref": t.count("data-ref="), "data_derived": t.count("data-derived="),
                    "details": t.count("<details"), "script": t.count("<script"), "on_handlers": len(re.findall(r"\son[a-z]+=", t)),
                    "external_src": len(re.findall(r"\s(?:src|href)=\"https?://[^\"]+\"[^>]*>", t)) and len(re.findall(r"<(?:img|link|iframe|source|video|audio|embed|object)[^>]+(?:src|href)=\"https?://", t)),
                    "blank_targets_without_noopener": len(re.findall(r"target=\"_blank\"(?![^>]*noopener)", t))}
R["pages"] = pages
R["pages_total_bytes"] = sum(p["bytes"] for p in pages.values())

# ---- 11. security basics -----------------------------------------------------------------------------------------
ci = (REPO / ".github/workflows/ci.yml").read_text(encoding="utf-8")
sec = {"ci_permissions": re.findall(r"permissions:\s*\n\s*(\S.*)", ci), "actions": re.findall(r"uses:\s*(\S+)", ci),
       "actions_pinned_to_sha": all(re.search(r"@[0-9a-f]{40}$", a) for a in re.findall(r"uses:\s*(\S+)", ci))}
risky = collections.defaultdict(list)
for f in PY:
    t = (REPO / f).read_text(encoding="utf-8")
    for pat in (r"shell=True", r"\beval\(", r"\bexec\(", r"pickle", r"yaml\.load", r"verify=False", r"_create_unverified_context", r"os\.system"):
        if re.search(pat, t):
            risky[pat].append(f)
sec["risky_calls"] = dict(risky)
reqs = {f: (REPO / f).read_text().splitlines() for f in ("requirements-test.txt", "requirements-analysis.txt")}
sec["pins"] = {f: [l for l in v if l and not l.startswith("#")] for f, v in reqs.items()}
sec["pins_exact"] = all("==" in l for v in sec["pins"].values() for l in v)
sec["pins_with_hashes"] = any("--hash" in l for v in reqs.values() for l in v)
import pyexpat  # noqa: E402
sec["expat"] = pyexpat.EXPAT_VERSION
R["security"] = sec

# ---- 12. process: git history ------------------------------------------------------------------------------------
log = subprocess.run(["git", "log", "--format=%H%x09%s%x09%P", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True).stdout.splitlines()
commits = [l.split("\t") for l in log]
merges = [c for c in commits if len(c[2].split()) > 1]
reverts = [c for c in commits if c[1].lower().startswith("revert")]
shortstat = subprocess.run(["git", "log", "--no-merges", "--format=@%H", "--shortstat", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True).stdout
files_changed = [int(m) for m in re.findall(r"(\d+) files? changed", shortstat)]
R["git"] = {"commits": len(commits), "merges": len(merges), "reverts": len(reverts),
            "non_merge": len(commits) - len(merges),
            "median_files_per_commit": sorted(files_changed)[len(files_changed) // 2] if files_changed else 0,
            "commits_over_50_files": sum(n > 50 for n in files_changed),
            "decisions": len(re.findall(r"^## D-\d+", (REPO / "docs/architecture/decisions.md").read_text(), re.M))}

OUT.write_text(json.dumps(R, indent=1, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: R[k] for k in ("size", "functions", "breaks", "git", "security", "clock_or_environment_in_tools", "labels", "label_text_definitions", "endpoint_signatures", "duplication", "record_ids_in_code", "third_party_imports", "imports_tools_graph")}, indent=1, default=str)[:20000])
