"""S15: the merged break harness (S13, S14 and S14.5 breaks, plus the S15 metric breaks).

S14 and S14.5 left three harnesses with three shapes (debt owned by "the next session that changes a
page"). This script loads the three, normalises every break to one shape, replaces the few whose setup no
longer applies after S15's changes (named below, with the reason), and adds S15's own breaks. Each break
copies the repository (without .git) into a scratch folder, makes one edit, runs its build steps, runs the
full suite, and counts only if the suite fails AND every expected fragment is in its output (the break
fails for the reason it names). A control counts only if the suite passes.

Build steps always follow the order data → results → HBM page → research view: a break that rebuilt the
HBM page in S13 now also rebuilds the research view, which reads the HBM page's anchors; otherwise a
control would fail for a stale second page rather than for its own edit.

Run with a virtualenv built from requirements-test.txt and requirements-analysis.txt:
    python sessions/reports/SESSION-15-breaks/breaks.py SCRATCH_DIR [ID ...]
    python sessions/reports/SESSION-15-breaks/breaks.py SCRATCH_DIR --setup-only   # apply edits only
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WH, PAGE_BUILD, INSIGHT_BUILD = "tools/warehouse.py", "tools/build_page.py", "tools/build_insight.py"
ALL = [WH, PAGE_BUILD, INSIGHT_BUILD]
INSIGHT = "site/hbm-insight/index.html"
CHAIN = "site/hbm-chain/index.html"


def module(rel: str):
    spec = importlib.util.spec_from_file_location(rel.replace("/", "_").replace("-", "_").replace(".", "_"), REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def edit(rel, old, new, count=1):
    def apply(root: Path):
        p = root / rel
        t = p.read_text(encoding="utf-8")
        if old not in t:
            raise SystemExit(f"break setup: {old[:70]!r} not in {rel}")
        p.write_text(t.replace(old, new, count), encoding="utf-8")
    return apply


def jedit(rel, fn):
    def apply(root: Path):
        p = root / rel
        d = json.loads(p.read_text(encoding="utf-8"))
        fn(d)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return apply


def both(*mutations):
    def apply(root: Path):
        for m in mutations:
            m(root)
    return apply


def plant_named_supplier(edges):
    """An HBM supplier named by assertion: valid in shape, so the status becomes computable."""
    e = next(x for x in edges if x["id"] == "rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory")
    e["supplier"] = [{"value": "company-sk-hynix", "claim_ids": ["claim-h100-hbm-stacks"]}]


# --- the earlier harnesses, normalised to (id, what, mutate(root), steps, expected) ------------------------

def s13():
    mod = module("sessions/reports/SESSION-13-breaks/breaks.py")
    out = []
    for bid, what, mutate, rebuild, expected in mod.BREAKS:
        steps = [PAGE_BUILD, INSIGHT_BUILD] if rebuild else []
        out.append((f"S13-{bid}" if not bid.startswith("S13") else bid, what, (lambda m: lambda root: m(root))(mutate), steps, expected))
    return out


def s14():
    mod = module("sessions/reports/SESSION-14-breaks/sql_breaks.py")
    steps = {"": [], "results": [WH], "both": ALL}
    return [(f"S14-{bid}", what, mutate, steps[rebuild], expected) for bid, what, mutate, rebuild, expected in mod.BREAKS]


def s145():
    mod = module("sessions/reports/SESSION-14.5-breaks/insight_breaks.py")
    return [(f"S14.5-{bid}", what, mutate, list(steps), expected) for bid, what, mutate, steps, expected in mod.BREAKS]


H100 = "product-nvidia-h100-tensor-core-gpu"
# S14.5 breaks whose setup text S15 removed, each replaced by the same fault on the S15 page (D-132):
# T1 and T2 edited the prototype's "links on stated evidence" tally, now an SQL metric; T3 hooked on its label.
REPLACED = {
    "S14.5-T1": ("S14.5-T1", "a tally hand-edited on the page (H100: 3 of 3 dated links older -> 2 of 3)",
                 edit(INSIGHT, f'data-derived="age-beyond" data-accelerator="{H100}">3<', f'data-derived="age-beyond" data-accelerator="{H100}">2<'), [],
                 ["test_in3_derived_values_are_recomputed", "test_in8_rebuild_is_byte_identical"]),
    "S14.5-T2": ("S14.5-T2", "a tally's denominator removed from its block (the age block)",
                 edit(INSIGHT, f' <span data-label>of</span> <span data-derived="age-dated" data-accelerator="{H100}">3</span></span>', "</span>"), [],
                 ["an age tally without its denominator"]),
    "S14.5-T3": ("S14.5-T3", "the build computes a share (a metric) beside a tally, rebuilt",
                 edit(INSIGHT_BUILD, '{self.label("links stated")}</span>', '{self.label("links stated")}</span>{self.derived("share", "50%")}'), [INSIGHT_BUILD],
                 ["a derived value the checks do not recompute"]),
}

# --- S15's own breaks (metrics.md; D-127 to D-132) -----------------------------------------------------------
COV, AGE, SUP = "sql/evidence_coverage.sql", "sql/source_age.sql", "sql/supplier_metrics.sql"
S15 = [
    ("S15-M1", "a coverage result hand-edited (Trainium2 stated 2 -> 3)",
     edit("sql/results/evidence_coverage.json", '"stated": 2,', '"stated": 3,'), [],
     ["is not a fresh run of the current inputs", "test_in2_sql_cells_equal_the_result"]),
    ("S15-M2", "a metric's header no longer says what it does not prove (rebuilt)",
     edit(COV, "-- does not prove: It does not measure", "-- limits: It does not measure"), ALL,
     ["not part of the tutorial header"]),
    ("S15-M3", "the reference date moved, results not rebuilt",
     edit(AGE, "DATE '2026-10-06' AS reference_date", "DATE '2027-10-06' AS reference_date"), [],
     ["is not a fresh run of the current inputs"]),
    ("S15-M4", "the access-date flag removed from the HBM page's table by hand",
     edit(CHAIN, 'dated by the day the page was read</span>', '</span>'), [],
     ["a caveat flag missing"]),
    ("S15-M5", "coverage counts gaps as stated (rebuilt)",
     edit(COV, "count(*) FILTER (WHERE l.basis = 'stated') AS stated", "count(*) FILTER (WHERE l.basis IN ('stated', 'gap')) AS stated"), ALL,
     ["test_wh12_evidence_coverage_equals_an_independent_computation", "the parts do not add up to the denominator"]),
    ("S15-M6", "source age measured from the oldest evidence instead of the newest (rebuilt)",
     edit(AGE, "d.evidence_dated_to AS newest_evidence,", "d.evidence_dated_from AS newest_evidence,"), ALL,
     ["test_wh13_source_age_equals_an_independent_computation"]),
    ("S15-M7", "the supplier metrics count part classes, hiding one unknown (rebuilt)",
     edit(SUP, "(SELECT count(DISTINCT record_id) FROM suppliers) AS parts", "(SELECT count(DISTINCT part_id) FROM suppliers) AS parts"), ALL,
     ["test_wh14_supplier_metrics_equal_an_independent_computation"]),
    ("S15-M8", "the page shows the named-supplier count (0) beside a supplier metric (rebuilt)",
     edit(INSIGHT_BUILD, '{m("parts_supplier_unknown")} {self.label("of")}', '{m("parts_supplier_named")} {m("parts_supplier_unknown")} {self.label("of")}'), [INSIGHT_BUILD],
     ["a zero beside a supplier metric reads as 'no suppliers'"]),
    ("S15-M9", "a supplier named in the data: the build stops instead of drawing an undesigned metric",
     jedit("data/relationships.json", plant_named_supplier), ALL,
     ["a supplier metric became computable"]),
    ("S15-M10", "a PEF answer hand-edited in a metric's tutorial on the page",
     edit(INSIGHT, "does not measure how dependent an accelerator is", "does not measure how dependent an accelerator might be"), [],
     ["is not the query file's answer"]),
    ("S15-M11", "two queries read each other (a cycle)",
     both(edit(COV, "    FROM accelerator_dependencies\n),", "    FROM accelerator_dependencies\n    WHERE NOT EXISTS (SELECT 1 FROM source_age)\n),"),
          edit(AGE, "    FROM accelerator_dependencies AS d\n)", "    FROM accelerator_dependencies AS d\n    WHERE NOT EXISTS (SELECT 1 FROM evidence_coverage)\n)")), [],
     ["queries read each other in a cycle"]),
    ("S15-M12", "the date basis reports the strongest kind instead of the weakest (rebuilt)",
     edit("sql/accelerator_dependencies.sql", "coalesce((SELECT CASE WHEN bool_or(e.date_basis = 'accessed') THEN 'accessed'\n                             WHEN bool_or(e.date_basis = 'stated') THEN 'stated'\n                             WHEN bool_or(e.date_basis = 'as_of') THEN 'as_of' END",
          "coalesce((SELECT CASE WHEN bool_or(e.date_basis = 'as_of') THEN 'as_of'\n                             WHEN bool_or(e.date_basis = 'stated') THEN 'stated'\n                             WHEN bool_or(e.date_basis = 'accessed') THEN 'accessed' END", count=2), ALL,
     ["test_wh10_the_first_result_equals_an_independent_computation"]),
    ("S15-C1", "control: a metric's sensitivity sentence reworded, everything rebuilt",
     edit(COV, "Small counts: read the numbers, not a proportion.", "Small counts: read the numbers rather than a proportion."), ALL, []),
]


def breaks():
    out = []
    for b in s13() + s14() + s145():
        out.append(REPLACED.get(b[0], b))
    return out + S15


def run(scratch: Path, wanted: set[str], setup_only: bool) -> int:
    py, bad = sys.executable, 0
    for bid, what, mutate, steps, expected in breaks():
        if wanted and bid not in wanted:
            continue
        root = scratch / f"merged-{bid}"
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.png"))
        try:
            mutate(root)
        except SystemExit as stale:
            print(f"{bid:10} {'SETUP STALE':24} {what} | {stale}")
            bad += 1
            shutil.rmtree(root)
            continue
        if setup_only:
            print(f"{bid:10} {'setup applies':24} {what}")
            shutil.rmtree(root)
            continue
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
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", out, re.M)))
        print(f"{bid:10} {verdict:24} {what} | failed: {', '.join(failed) or '-'}", flush=True)
        shutil.rmtree(root)
    return bad


if __name__ == "__main__":
    args = [a for a in sys.argv[2:] if a != "--setup-only"]
    sys.exit(1 if run(Path(sys.argv[1]), set(args), "--setup-only" in sys.argv) else 0)
