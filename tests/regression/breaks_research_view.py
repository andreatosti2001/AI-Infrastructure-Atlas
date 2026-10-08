"""Breaks for the research view (visual-architecture.md §10, §12; D-124, D-125).

Each break copies the repository (without .git) into a scratch folder, makes one edit, optionally rebuilds (the
results, the HBM page, the research view, in that order), runs the full suite, and counts only if the suite
fails AND every expected fragment is in its output. A control passes only if the suite passes.

A layer of the full harness: run it through `tests/regression/breaks.py`, which replaces the breaks whose
setup text later changes removed. Run alone, some of this layer's breaks no longer apply.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PAGE = "site/hbm-insight/index.html"
BUILD = "tools/build_insight.py"
TEMPLATE = "tools/insight_template.html"


def edit(rel, old, new, count=1):
    def apply(root):
        p = root / rel
        t = p.read_text(encoding="utf-8")
        if old not in t:
            raise SystemExit(f"break setup: {old[:60]!r} not in {rel}")
        p.write_text(t.replace(old, new, count), encoding="utf-8")
    return apply


def resub(rel, pattern, new):
    def apply(root):
        p = root / rel
        t = p.read_text(encoding="utf-8")
        t2, n = re.subn(pattern, new, t, count=1, flags=re.S)
        if not n:
            raise SystemExit(f"break setup: {pattern[:60]!r} not in {rel}")
        p.write_text(t2, encoding="utf-8")
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


H100 = "product-nvidia-h100-tensor-core-gpu"
ALL = ["tools/warehouse.py", "tools/build_page.py", BUILD]
# (id, what, edit, rebuild steps, expected fragments; [] for a control)
BREAKS = [
    ("T1", "a tally hand-edited on the page (H100: 1 of 4 stated -> 2 of 4)",
     edit(PAGE, f'data-derived="stated-count" data-accelerator="{H100}">1<', f'data-derived="stated-count" data-accelerator="{H100}">2<'), [],
     ["test_in3_derived_values_are_recomputed", "test_in8_rebuild_is_byte_identical"]),
    ("T2", "a tally's denominator removed from its block",
     edit(PAGE, f' <span data-label>of</span> <span data-derived="acc-rows" data-accelerator="{H100}">4</span>', ""), [],
     ["a tally whose denominator is not in the same block"]),
    ("T3", "the build computes a share (a metric) beside a tally, rebuilt",
     edit(BUILD, '{self.label("links")}</span>', '{self.label("links")}</span>{self.derived("share", "50%")}'), [BUILD],
     ["a derived value the checks do not recompute"]),
    ("V1", "a strip line drawn as stated when its row is inferred",
     edit(PAGE, 'class="link inferred s-process"', 'class="link stated s-process"'), [],
     ["the line style does not follow the basis"]),
    ("V2", "a gap's reason dropped from the marks, rebuilt",
     # first run: the line was deleted, which left an empty `if` block, so the build died of a syntax error and the
     # break failed for the wrong reason (recorded in the report); the reason is now replaced by nothing instead
     edit(BUILD, "            words += f\" · {self.cell(i, 'gap_reason', fmt='state')}\"\n", "            words += \"\"\n"), [BUILD],
     ["a gap without its reason in words"]),
    ("V3", "a unit square opens the wrong row",
     edit(PAGE, 'data-row="0" data-basis="stated" href="#row-0"', 'data-row="0" data-basis="stated" href="#row-1"'), [],
     ["a unit square that does not open its row"]),
    ("E1", "an evidence link to a panel the HBM page does not have",
     edit(PAGE, 'index.html#ev-rel-company-amazon-com-designs-product-amazon-com-trainium2"', 'index.html#ev-rel-company-amazon-com-designs"'), [],
     ["an evidence link to a panel the HBM page does not have"]),
    ("F1", "framing names a record, rebuilt",
     edit(TEMPLATE, "It is not published.</p>", "It is not published, and it covers NVIDIA.</p>"), [BUILD],
     ["framing names a record (NVIDIA)"]),
    ("S1", "a colour outside the palette, rebuilt",
     edit(TEMPLATE, ".qline { margin: 0 0 8px;", ".qline { color: #ff0000; margin: 0 0 8px;"), [BUILD],
     ["a colour outside the palette"]),
    ("S2", "the filter fades instead of outlining, rebuilt",
     edit(TEMPLATE, "body:has(#f-stated:checked) tr[data-basis]", "a.link { opacity: 0.3; }\nbody:has(#f-stated:checked) tr[data-basis]"), [BUILD],
     ["fading lowers contrast"]),
    ("L1", "a label in the headline hand-edited ('each' -> 'both')",
     edit(PAGE, "<span data-label>each</span>", "<span data-label>both</span>"), [],
     ["a label that is not one of the build's labels"]),
    ("D1", "data changed (a display name), results and HBM page rebuilt, prototype not",
     jedit("data/components.json", rename_hbm), ["tools/warehouse.py", "tools/build_page.py"],
     ["test_in2_sql_cells_equal_the_result", "test_in8_rebuild_is_byte_identical"]),
    ("D2", "a decision appended, the HBM page rebuilt, the prototype not",
     edit("docs/architecture/decisions.md", "## D-126 — Sub-session numbering: S14.5", "## D-126 — Sub-session numbering: S14.5 (break)"), ["tools/build_page.py"],
     ["test_in8_rebuild_is_byte_identical"]),
    ("C1", "control: a framing sentence reworded, prototype rebuilt",
     edit(TEMPLATE, "Every line opens its evidence.</p>", "Each line opens its evidence.</p>"), [BUILD], []),
    ("C2", "control: High Bandwidth Memory's display name edited, everything rebuilt in order",
     jedit("data/components.json", rename_hbm), ALL, []),
]


def run(scratch: Path, wanted: set[str]) -> int:
    py, bad = sys.executable, 0
    for bid, what, mutate, steps, expected in BREAKS:
        if wanted and bid not in wanted:
            continue
        root = scratch / f"insightbreak-{bid}"
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.png"))
        mutate(root)
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
        print(f"{bid:3} {verdict:24} {what} | {out.strip().splitlines()[-1]}")
        shutil.rmtree(root)
    return bad


if __name__ == "__main__":
    sys.exit(1 if run(Path(sys.argv[1]), set(sys.argv[2:])) else 0)
