"""S13 sample: the claims the content audit re-reads (H-1, answered at the S13 opening).

Approved by the human on 2026-10-02: the page's 14 weight-bearing claims plus 20 drawn by type.

The rule, so a second run draws the same list:

1. The weight-bearing set. The six claims S12 handed over (SESSION-12-REPORT.md, "Implications for
   the next session"): the five that the five canonical edges cite, and the drawn gap's DERIVATION
   (claim-tsmc-fabricates-h100, D-092). The script asserts that the edges cite exactly the five, so
   an edge added or re-pointed fails here instead of silently changing the set. Then every input
   claim of a DERIVATION in the set, transitively (input_claim_ids), in discovery order.
2. The drawn set. Of the canonical claims not in step 1, 20 are drawn in proportion to claim_type,
   by largest remainder (ties: the order of TYPES below). Within each type, claims are ordered by
   SHA-256 of SEED + ":" + claim ID, and the first k are taken. The seed is fixed; no clock and no
   random state are read.
3. The edges: the five canonical relationships, and the drawn gap (the DERIVATION of step 1 that no
   edge cites).

The output records the SHA-256 of the inputs, so a re-run on different data is visible as such.

Standard library only. Usage (from the repository root):
    python sessions/reports/SESSION-13-sample/draw_sample.py            # print the sample
    python sessions/reports/SESSION-13-sample/draw_sample.py --write    # also write sample.json
    python sessions/reports/SESSION-13-sample/draw_sample.py --check    # sample.json equals a re-draw
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "sample.json"
SEED = "S13-content-audit"
DRAWN = 20
TYPES = ["FACT", "ATTRIBUTION", "DERIVATION", "INTERPRETATION", "IMPLICATION"]
HANDED_OVER = [
    "claim-h100-hbm-stacks",
    "claim-trainium2-hbm-capacity",
    "claim-hbm-requires-3d-die-stacking",
    "claim-tsmc-fabricates-h100",
    "claim-aws-designed-trainium2",
    "claim-sk-hynix-operates-m16",
]
DRAWN_GAP = "claim-tsmc-fabricates-h100"
INPUTS = ["data/claims.json", "data/relationships.json"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def order_key(claim_id: str) -> str:
    return hashlib.sha256(f"{SEED}:{claim_id}".encode("utf-8")).hexdigest()


def quotas(counts: dict[str, int], n: int) -> dict[str, int]:
    total = sum(counts.values())
    exact = {t: counts.get(t, 0) * n / total for t in TYPES}
    out = {t: int(exact[t]) for t in TYPES}
    rest = n - sum(out.values())
    by_remainder = sorted(TYPES, key=lambda t: (-(exact[t] - out[t]), TYPES.index(t)))
    for t in by_remainder[:rest]:
        out[t] += 1
    return out


def draw() -> dict:
    claims = json.loads((REPO / "data/claims.json").read_text(encoding="utf-8"))
    edges = json.loads((REPO / "data/relationships.json").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in claims}

    edge_claims = [cid for e in edges for cid in e["claim_ids"]]
    expected = [c for c in HANDED_OVER if c != DRAWN_GAP]
    if sorted(edge_claims) != sorted(expected):
        sys.exit(f"the edges cite {sorted(edge_claims)}, not the handed-over five {sorted(expected)}")

    weight = []
    queue = list(HANDED_OVER)
    while queue:
        cid = queue.pop(0)
        if cid in weight:
            continue
        if cid not in by_id:
            sys.exit(f"{cid} is not a canonical claim")
        weight.append(cid)
        queue.extend(by_id[cid].get("input_claim_ids", []))

    rest = [c for c in claims if c["id"] not in weight]
    counts = {t: sum(1 for c in rest if c["claim_type"] == t) for t in TYPES}
    if sum(counts.values()) != len(rest):
        sys.exit("a claim_type outside TYPES")
    q = quotas(counts, DRAWN)
    drawn = []
    for t in TYPES:
        pool = sorted((c["id"] for c in rest if c["claim_type"] == t), key=order_key)
        drawn.extend({"id": cid, "claim_type": t} for cid in pool[: q[t]])

    return {
        "rule": "draw_sample.py docstring; seed " + SEED,
        "inputs": {p: sha256(REPO / p) for p in INPUTS},
        "canonical_claims": len(claims),
        "weight_bearing": [{"id": cid, "claim_type": by_id[cid]["claim_type"]} for cid in weight],
        "drawn_pool_by_type": counts,
        "drawn_quota_by_type": q,
        "drawn": drawn,
        "edges": [{"id": e["id"], "claim_ids": e["claim_ids"]} for e in edges],
        "drawn_gap": DRAWN_GAP,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    text = json.dumps(draw(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if OUT.read_text(encoding="utf-8") != text:
            sys.exit("sample.json differs from a re-draw")
        print("sample: equals a re-draw")
        return
    if args.write:
        OUT.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
