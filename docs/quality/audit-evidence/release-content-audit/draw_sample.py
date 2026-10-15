"""S23 sample: the claims the release content audit reads in full (H-0, answered at the S23 opening).

Approved by the human on 2026-10-15: every weight-bearing claim plus 30 drawn by type, read in full; the anchors of
every canonical claim's citations searched by reread.py (all 203, not only the sample's).

The rule, so a second run draws the same list:

1. The weight-bearing set: every claim a page result rests on, found mechanically from the records the builds read,
   in this order (discovery order is kept):
   a. every claim ID anywhere in data/relationships.json (the five chain edges, their two supplier fields, the four
      `restricts` links);
   b. every claim ID in the rows of sql/results/accelerator_dependencies.json (the dependency table the HBM page, the
      research view, the journeys and the brief's summary read: its edges, supplier rows, recorded gaps and each
      accelerator's class claim);
   c. every claim ID in data/events.json (the events every derived status rests on: policy, facility, company);
   d. every claim in the Change Detector's table "Later statements about acts held"
      (docs/research/change-detection.md §1), which the export-control page and the brief show under their acts;
   e. then every input claim (input_claim_ids) of a claim already in the set, transitively.
2. The drawn set. Of the canonical claims not in step 1, 30 are drawn in proportion to claim_type by largest remainder
   (ties: the order of TYPES). Within each type, claims are ordered by SHA-256 of SEED + ":" + claim ID and the first
   k are taken. The seed is fixed; no clock and no random state are read.

The output records the SHA-256 of every file read, so a re-run on different data is visible as such.

Standard library only (D-003). Usage (from the repository root):
    python docs/quality/audit-evidence/release-content-audit/draw_sample.py            # print the sample
    python docs/quality/audit-evidence/release-content-audit/draw_sample.py --write    # also write sample.json
    python docs/quality/audit-evidence/release-content-audit/draw_sample.py --check    # sample.json equals a re-draw
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent / "sample.json"
SEED = "S23-release-content-audit"
DRAWN = 30
TYPES = ["FACT", "ATTRIBUTION", "DERIVATION", "INTERPRETATION", "IMPLICATION"]
CLAIMS = "data/claims.json"
RELATIONSHIPS = "data/relationships.json"
DEPENDENCIES = "sql/results/accelerator_dependencies.json"
EVENTS = "data/events.json"
CHANGE_DETECTION = "docs/research/change-detection.md"
LATER_HEAD = "### Later statements about acts held"
INPUTS = [CLAIMS, RELATIONSHIPS, DEPENDENCIES, EVENTS, CHANGE_DETECTION]
CLAIM_ID = re.compile(r"claim-[a-z0-9-]+")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def order_key(claim_id: str) -> str:
    return hashlib.sha256(f"{SEED}:{claim_id}".encode("utf-8")).hexdigest()


def claim_ids_in(node) -> list[str]:
    """Every string value under node that is a whole claim ID, in document order."""
    if isinstance(node, dict):
        return [c for v in node.values() for c in claim_ids_in(v)]
    if isinstance(node, list):
        return [c for v in node for c in claim_ids_in(v)]
    if isinstance(node, str) and CLAIM_ID.fullmatch(node):
        return [node]
    return []


def later_statement_claims(text: str) -> list[str]:
    if LATER_HEAD not in text:
        sys.exit(f"{CHANGE_DETECTION} has no table {LATER_HEAD[4:]!r}")
    found = []
    for line in text.partition(LATER_HEAD)[2].split("\n#")[0].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].startswith("`policy-"):
            found.extend(re.findall(r"`(claim-[^`]+)`", cells[1]))
    return found


def quotas(counts: dict[str, int], n: int) -> dict[str, int]:
    total = sum(counts.values())
    exact = {t: counts.get(t, 0) * n / total for t in TYPES}
    out = {t: int(exact[t]) for t in TYPES}
    rest = n - sum(out.values())
    for t in sorted(TYPES, key=lambda t: (-(exact[t] - out[t]), TYPES.index(t)))[:rest]:
        out[t] += 1
    return out


def load(path: str):
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def draw() -> dict:
    claims = load(CLAIMS)
    by_id = {c["id"]: c for c in claims}
    steps = {
        "a_relationships": claim_ids_in(load(RELATIONSHIPS)),
        "b_dependency_rows": claim_ids_in(load(DEPENDENCIES)["rows"]),
        "c_events": claim_ids_in(load(EVENTS)),
        "d_later_statements": later_statement_claims((REPO / CHANGE_DETECTION).read_text(encoding="utf-8")),
    }
    weight: list[str] = []
    reason: dict[str, str] = {}
    queue = [(cid, step) for step, ids in steps.items() for cid in ids]
    while queue:
        cid, why = queue.pop(0)
        if cid in weight:
            continue
        if cid not in by_id:
            sys.exit(f"{cid} ({why}) is not a canonical claim")
        weight.append(cid)
        reason[cid] = why
        queue.extend((i, f"e_input_of:{cid}") for i in by_id[cid].get("input_claim_ids", []))

    rest = [c for c in claims if c["id"] not in reason]
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
        "weight_bearing_count": len(weight),
        "weight_bearing": [{"id": c, "claim_type": by_id[c]["claim_type"], "why": reason[c]} for c in weight],
        "drawn_pool_by_type": counts,
        "drawn_quota_by_type": q,
        "drawn": drawn,
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
