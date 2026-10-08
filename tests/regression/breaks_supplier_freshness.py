"""The supplier-freshness layer: the metric-audit layer plus the breaks of D-141 and of the review record (D-151).

Loads `tests/regression/breaks_metric_audit.py` and adds its breaks and a control, under the same rules.

A layer of the full harness: run it through `tests/regression/breaks.py`, which replaces the breaks whose
setup text later changes removed. Run alone, some of this layer's breaks no longer apply.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("s16_breaks", REPO / "tests/regression/breaks_metric_audit.py")
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
    # A2 and A3 tested D-142's sub-session report names; D-151 superseded them, so each is the same fault on the
    # human review record: a review that names no entry, and the schema's form check loosened.
    ("S16.5-A2", "the new claim's review names an entry the human review record does not hold",
     edit("data/claims.json", '"recorded_in": "docs/quality/human-reviews.md#sk-hynix-hbm3-statement-2026-10-07"',
          '"recorded_in": "docs/quality/human-reviews.md#sk-hynix-hbm3-statement-2026-10-08"'), ALL,
     ["test_hr1_hr2_every_review_resolves_to_its_dated_entry", "names no entry of docs/quality/human-reviews.md"]),
    ("S16.5-A3", "the schema's review form loosened to any path (D-151)",
     edit("schemas/claims.schema.json", '"pattern": "^docs/quality/human-reviews\\\\.md#', '"pattern": "^.*'), ALL,
     ["test_review_is_recorded_in_the_human_review_record"]),
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
