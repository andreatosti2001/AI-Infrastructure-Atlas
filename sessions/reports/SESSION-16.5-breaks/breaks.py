"""S16.5: the merged break harness (S13 to S16) plus S16.5's breaks (D-141, D-142).

Loads S16's harness (`sessions/reports/SESSION-16-breaks/breaks.py`) and adds S16.5's breaks and a control. The
rules are S15's: each break copies the repository, makes one edit, runs its build steps (results -> HBM page ->
research view), runs the full suite, and counts only if the suite fails with every expected fragment in its
output. A control counts only if the suite passes.

Run with a virtualenv built from requirements-test.txt and requirements-analysis.txt:
    python sessions/reports/SESSION-16.5-breaks/breaks.py SCRATCH_DIR [ID ...]
    python sessions/reports/SESSION-16.5-breaks/breaks.py SCRATCH_DIR --setup-only
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("s16_breaks", REPO / "sessions/reports/SESSION-16-breaks/breaks.py")
s16 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s16)
s15 = s16.s15
edit, jedit, ALL = s15.edit, s15.jedit, s15.ALL
H100_HBM = "rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory"
CLAIM = "claim-sk-hynix-hbm3-for-h100-2022"


def name_sk_hynix_on_stale_evidence(edges):
    """The H100's HBM supplier set to SK hynix, resting on the 2022 claim (D-141 refused this)."""
    e = next(x for x in edges if x["id"] == H100_HBM)
    e["supplier"] = [{"value": "company-sk-hynix", "claim_ids": [CLAIM]}]


S165 = [
    ("S16.5-A1", "SK hynix named as the H100's HBM supplier on the stale 2022 statement (rebuilt)",
     jedit("data/relationships.json", name_sk_hynix_on_stale_evidence), ALL,
     ["supplier = company-sk-hynix: no accepted evidence within 12 months"]),
    ("S16.5-A2", "the new claim's review recorded in a malformed sub-session report",
     edit("data/claims.json", '"recorded_in": "sessions/reports/SESSION-16.5-REPORT.md"',
          '"recorded_in": "sessions/reports/SESSION-16.55-REPORT.md"'), ALL,
     ["test_vd2_every_record_is_valid"]),
    ("S16.5-A3", "the schema's sub-session suffix removed again (D-142)",
     edit("schemas/claims.schema.json", "SESSION-[0-9]{2}(\\\\.[0-9])?-REPORT", "SESSION-[0-9]{2}-REPORT"), ALL,
     ["test_review_may_be_recorded_in_a_sub_session_report", "test_vd2_every_record_is_valid"]),
    ("S16.5-C1", "control: the new claim's statement reworded, everything rebuilt",
     edit("data/claims.json", "and that it would provide HBM3 for NVIDIA systems",
          "and that it would supply HBM3 for NVIDIA systems"), ALL, []),
]

S16_BREAKS = s16.breaks


def breaks():
    return S16_BREAKS() + S165


if __name__ == "__main__":
    s15.breaks = breaks
    args = [a for a in sys.argv[2:] if a != "--setup-only"]
    sys.exit(1 if s15.run(Path(sys.argv[1]), set(args), "--setup-only" in sys.argv) else 0)
