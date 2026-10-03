"""S14 deliberate breaks for the SQL layer and the page's SQL section (sql-layer.md; D-118 to D-121).

Each break copies the repository (without .git) into a scratch folder, makes one edit, optionally
rebuilds the results (tools/warehouse.py) and then the page (tools/build_page.py), runs the full suite,
and counts only if the suite fails AND every expected fragment is in its output. A control passes only
if the suite passes. Run with a virtualenv built from requirements-test.txt and requirements-analysis.txt:
    python sessions/reports/SESSION-14-breaks/sql_breaks.py SCRATCH_DIR [ID ...]
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
QUERY = "sql/accelerator_dependencies.sql"
RESULT = "sql/results/accelerator_dependencies.json"
PAGE = "site/hbm-chain/index.html"


def edit(rel, old, new, count=1):
    def apply(root):
        p = root / rel
        t = p.read_text(encoding="utf-8")
        if old not in t:
            raise SystemExit(f"break setup: {old[:60]!r} not in {rel}")
        p.write_text(t.replace(old, new, count), encoding="utf-8")
    return apply


def jedit(rel, fn):
    def apply(root):
        p = root / rel
        d = json.loads(p.read_text(encoding="utf-8"))
        fn(d)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return apply


def rename_hbm(components):
    """A valid editorial change to the data: a display name (entity-taxonomy.md §7)."""
    next(c for c in components if c["id"] == "component-high-bandwidth-memory").update(name="High-Bandwidth Memory (HBM)")


# (id, what, edit, rebuild: "" | "results" | "both", expected fragments; [] for a control)
BREAKS = [
    ("Q1", "the query file changed, nothing rebuilt", edit(QUERY, "-- step: Find the accelerators", "-- step: Find every accelerator"), "",
     ["is not a fresh run of the current inputs", "the result was computed from another version of the query file"]),
    ("Q2", "the query file changed, results rebuilt, page not", edit(QUERY, "-- step: Find the accelerators", "-- step: Find every accelerator"), "results",
     ["test_pg7_rebuild_is_byte_identical", "test_pg11_the_tutorial_is_its_query_file"]),
    ("Q3", "the final ORDER BY removed (rebuilt)", edit(QUERY, "ORDER BY a.accelerator, r.position, r.record_id, r.gap_reason, r.from_id", ""), "both",
     ["the final SELECT has no ORDER BY"]),
    ("Q4", "a tutorial explanation names a record (rebuilt)", edit(QUERY, "-- what it incorporates.", "-- what it incorporates, such as rel-product-x."), "both",
     ["an explanation names a record"]),
    ("Q5", "the evidence date takes the oldest source date instead of the newest (rebuilt)",
     edit(QUERY, "THEN (SELECT max(d.date) FROM source_dates", "THEN (SELECT min(d.date) FROM source_dates"), "both",
     ["test_wh10_the_first_result_equals_an_independent_computation"]),
    ("Q6", "recorded gaps admitted for any reason (rebuilt)", edit(QUERY, "= ['evidence_not_fresh']", "IS NOT NULL"), "both",
     ["test_wh10_the_first_result_equals_an_independent_computation"]),
    ("R1", "a result cell hand-edited: inferred -> stated", edit(RESULT, '"basis": "inferred"', '"basis": "stated"'), "",
     ["is not a fresh run of the current inputs", "test_pg11_the_sql_table_equals_its_result"]),
    ("R2", "data changed (a display name), results not rebuilt", jedit("data/components.json", rename_hbm), "",
     ["is not a fresh run of the current inputs"]),
    ("P1", "a table cell on the page hand-edited (stated -> inferred)", edit(PAGE, 'data-column="basis">stated<', 'data-column="basis">inferred<'), "",
     ["test_pg11_the_sql_table_equals_its_result", "test_pg7_rebuild_is_byte_identical"]),
    ("P2", "the code shown in the tutorial hand-edited", edit(PAGE, "WHERE w.depth &lt; 10", "WHERE w.depth &lt; 100"), "",
     ["the code shown is not the query file"]),
    ("P3", "a caveat flag removed from the page", edit(PAGE, "rests on the Atlas’s own definitions</span>", "</span>"), "",
     ["a caveat flag missing"]),
    ("L1", "the loader turns every explicit state into 'value' (rebuilt)", edit("tools/warehouse.py", 'return None, value["state"]', 'return None, "value"'), "both",
     ["is NULL exactly when"]),
    ("C1", "control: a tutorial sentence reworded, results and page rebuilt",
     edit(QUERY, "Such a row is reached directly, and its depth is one.", "Such a row is reached directly; its depth is one."), "both", []),
    # A first C2 planted the H100 supplier as not_publicly_determinable and rebuilt: the schema and ER-3 rightly
    # refused it (that state needs a search record), so it was invalid data, not a control. WH-5 plants that state
    # below the data checks. This C2 makes a valid editorial change instead: a display name (entity-taxonomy §7).
    ("C2", "control: High Bandwidth Memory's display name edited, results and page rebuilt",
     jedit("data/components.json", rename_hbm), "both", []),
]


def run(scratch: Path, wanted: set[str]) -> int:
    py, bad = sys.executable, 0
    for bid, what, mutate, rebuild, expected in BREAKS:
        if wanted and bid not in wanted:
            continue
        root = scratch / f"sqlbreak-{bid}"
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.png"))
        mutate(root)
        steps = {"": [], "results": ["tools/warehouse.py"], "both": ["tools/warehouse.py", "tools/build_page.py"]}[rebuild]
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
        bad += not ok
        print(f"{bid:4} {verdict:24} {what} | {out.strip().splitlines()[-1]}")
        shutil.rmtree(root)
    return bad


if __name__ == "__main__":
    sys.exit(1 if run(Path(sys.argv[1]), set(sys.argv[2:])) else 0)
