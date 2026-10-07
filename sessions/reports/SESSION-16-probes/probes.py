"""S16 sensitivity probes (Part B §06 q5, §07 task 4).

Run: python sessions/reports/SESSION-16-probes/probes.py SCRATCH_DIR > sessions/reports/SESSION-16-probes/probes-output.txt

Each probe copies the repository (without .git and sessions/) into SCRATCH_DIR, makes one planted change,
rebuilds in the order results -> HBM page -> research view, and prints the text of the research view's
indicator blocks, or the error that stopped the build. Nothing in the repository is changed.

Every planted value is HYPOTHETICAL. It tests how the page moves, never what is true: the planted supplier
is a placeholder id that names no company, the planted publication dates are marked as planted, and the
planted FACT re-types reuse claims already held. No probe output is evidence about the world.
"""
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRATCH = Path(sys.argv[1]).resolve()
PY = sys.executable


def edit_json(root: Path, name: str, fn) -> None:
    p = root / "data" / name
    d = json.loads(p.read_text(encoding="utf-8"))
    d = fn(d) or d
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def by_id(items, i):
    return next(x for x in items if x["id"] == i)


def p1_shared_link_stated(root):
    """One more link stated (shared): the claim behind 'HBM requires 3D die stacking' re-typed DERIVATION -> FACT,
    with a planted citation of a source it already rests on (src-039)."""
    def f(claims):
        c = by_id(claims, "claim-hbm-requires-3d-die-stacking")
        c["claim_type"] = "FACT"
        c["citations"] = [{"source_id": "src-039", "standing": "originator", "locator": "PLANTED BY S16 PROBE",
                           "anchor": "PLANTED BY S16 PROBE", "read": {"accessed_at": "2026-10-01T00:00Z", "sha256": "0" * 64}}]
        c.pop("input_claim_ids", None)
        c.pop("reasoning", None)
    edit_json(root, "claims.json", f)


def p2_h100_gap_resolved(root):
    """One more link stated (one accelerator): the H100's recorded gap 'TSMC fabricates' (refused as not fresh)
    replaced by a recorded fabricates edge citing the FACT claim the candidate already considered."""
    edit_json(root, "refused_candidates.json", lambda d: [x for x in d if x["id"] != "cand-001"])
    edit_json(root, "relationships.json", lambda d: d + [{
        "id": "rel-probe-s16-tsmc-fabricates-h100", "relation_type": "fabricates",
        "source_entity": "company-taiwan-semiconductor-manufacturing-company",
        "target_entity": "product-nvidia-h100-tensor-core-gpu", "claim_ids": ["claim-h100-process-name"]}])


def p3_undated_source_old_date(root):
    """One undated source given a publication date: src-043 (Trainium2's only recent date, an access date)
    given a PLANTED stated date 2024-12-03, older than the horizon."""
    edit_json(root, "sources.json", lambda d: by_id(d, "src-043").update(stated_dates=[{"kind": "published", "date": "2024-12-03"}]))


def p4_undated_source_recent_date(root):
    """The same source given a PLANTED stated date 2026-06-15, within the horizon."""
    edit_json(root, "sources.json", lambda d: by_id(d, "src-043").update(stated_dates=[{"kind": "published", "date": "2026-06-15"}]))


def set_reference(root, day):
    p = root / "sql" / "source_age.sql"
    t = p.read_text(encoding="utf-8")
    assert t.count("DATE '2026-10-06'") == 1
    p.write_text(t.replace("DATE '2026-10-06'", f"DATE '{day}'"), encoding="utf-8")


def p5_reference_s16_opening(root):
    """The reference date moved to the day S16 opened, 2026-10-07."""
    set_reference(root, "2026-10-07")


def p6_reference_one_year(root):
    """The reference date moved one year, to 2027-10-06 (where the next horizon crossing falls)."""
    set_reference(root, "2027-10-06")


def p7_supplier_named(root):
    """One supplier named: the H100's HBM supplier set to a PLACEHOLDER id (no company), on a claim already held."""
    def f(rels):
        by_id(rels, "rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory")["supplier"] = [
            {"value": "company-placeholder-s16-probe", "claim_ids": ["claim-h100-hbm-stacks"]}]
    edit_json(root, "relationships.json", f)


PROBES = [("P0 control: no change", None), ("P1", p1_shared_link_stated), ("P2", p2_h100_gap_resolved),
          ("P3", p3_undated_source_old_date), ("P4", p4_undated_source_recent_date),
          ("P5", p5_reference_s16_opening), ("P6", p6_reference_one_year), ("P7", p7_supplier_named)]


def indicator_text(page: Path) -> str:
    t = page.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    i, j = t.index('class="indicators-h"'), t.index('id="visual"')
    s = html.unescape(re.sub(r"<[^>]+>", " ", t[i - 4:j]))
    s = re.sub(r"\s+", " ", s).replace(" see how this was computed", "").strip()
    s = s.lstrip('h3 ="').strip()
    for k in ("Evidence age", "Publishers behind", "Cannot be computed yet", "geographic concentration", "single-source"):
        s = s.replace(" " + k, "\n  " + k)
    s = s.split(" <section")[0]
    return "  " + s[s.index("Evidence coverage"):] if "Evidence coverage" in s else s


def main() -> int:
    print(__doc__.strip().splitlines()[0])
    print(f"base: {subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()}\n")
    for name, fn in PROBES:
        root = SCRATCH / name.split()[0]
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", "sessions", "__pycache__"))
        if fn:
            fn(root)
        print(f"=== {name}" + (f": {fn.__doc__.strip()}" if fn else ""))
        # every step runs, so a stop in one build is reported without hiding what the next one does
        ok = {}
        for step in ("tools/warehouse.py", "tools/build_page.py", "tools/build_insight.py"):
            r = subprocess.run([PY, step], cwd=root, capture_output=True, text=True)
            ok[step] = not r.returncode
            print(f"  {step}: " + ("built" if ok[step] else "STOPPED: " + (r.stderr or r.stdout).strip().splitlines()[-1]))
            if step == "tools/warehouse.py" and not ok[step]:
                break
        if ok.get("tools/build_insight.py"):
            print(indicator_text(root / "site" / "hbm-insight" / "index.html"))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
