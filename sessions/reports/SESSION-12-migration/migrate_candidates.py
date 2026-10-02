"""S12 migration: edge-dataset.md §1 "Candidates that are not edges" -> data/staging/refused_candidates.json.

D-109; milestone-audits/M2-audit.md Part 3 q1. Kept with the session report (debt DT-8): after the
migration the table's rows leave edge-dataset.md, so the script runs only on the commit before that
(git show <commit>:docs/architecture/edge-dataset.md), which `--doc` accepts.

The records are written out below by hand: the Extractor's reading of each row, including the
reason codes, which the human reviews. The script then asserts that every value equals its cell:

- endpoints: each name in the Candidate cell is a record's name or alias (then its ID is used), or,
  for "Manassas", a word of exactly one record's name whose identity claim the row cites, or a
  name no record carries (then a no_record state with that name);
- relation types: the backticked types of the Type cell;
- claims and sources: the backticked IDs of the Sentence cell, in order;
- quotes: every quoted string of the Sentence cell is an anchor here, or (with "…" read as a gap)
  part of a considered claim's anchor; locators are the cell's page marks;
- item: its name is quoted in the Why not cell;
- reasoning: the Why not cell with Markdown backticks removed;
- the row count and order.

Standard library only. Usage (from the repository root):
    python sessions/reports/SESSION-12-migration/migrate_candidates.py [--doc PATH] [--write]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
NOT_RE_READ = {"state": "not_re_read"}


def nr(name: str) -> dict:
    return {"state": "no_record", "name": name}


def claim(cid: str) -> dict:
    return {"claim_id": cid}


def sentence(source_id: str, locator, anchor: str | None = None) -> dict:
    item = {"source_id": source_id, "locator": locator}
    if anchor is not None:
        item["anchor"] = anchor
    item["read"] = dict(NOT_RE_READ)
    return item


TSMC = "company-taiwan-semiconductor-manufacturing-company"
H100 = "product-nvidia-h100-tensor-core-gpu"
NVIDIA = "company-nvidia"
MICRON = "company-micron-technology"
ASML = "company-asml-holding"
AMAZON = "company-amazon-com"

# (row key, record without id and reasoning); the order is the table's
ROWS = [
    ("TSMC → H100", dict(relation_types=["fabricates"], source_entities=[TSMC], target_entities=[H100],
        considered=[claim("claim-h100-process-name"), claim("claim-tsmc-fabricates-h100")],
        reasons=["evidence_not_fresh"], ruling="D-092")),
    ("SK hynix, Micron → NVIDIA", dict(relation_types=["supplies"], source_entities=["company-sk-hynix", MICRON], target_entities=[NVIDIA],
        item=nr("memory"),
        considered=[sentence("src-024", "p.8", "We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung")],
        reasons=["item_has_no_record"], ruling="D-089")),
    ("TSMC → NVIDIA", dict(relation_types=["supplies"], source_entities=[TSMC], target_entities=[NVIDIA],
        considered=[sentence("src-024", "p.8", "We utilize foundries, such as … TSMC … to produce our semiconductor wafers")],
        reasons=["wrong_relation_type", "company_level_only"], ruling="D-089")),
    ("Carl Zeiss SMT GmbH → ASML", dict(relation_types=["supplies"], source_entities=[nr("Carl Zeiss SMT GmbH")], target_entities=[ASML],
        item=nr("optical column"),
        considered=[sentence("src-029", "p.322", "Carl Zeiss SMT GmbH is our single supplier, and we are their single customer, of optical columns for lithography systems")],
        reasons=["endpoint_has_no_record", "item_has_no_record"], ruling="D-089")),
    ("ASML → TSMC", dict(relation_types=["supplies"], source_entities=[ASML], target_entities=[TSMC],
        considered=[sentence("src-029", "p.173", "we were honored to receive the TSMC Supplier ‘Excellence in Green Manufacturing’ Award")],
        reasons=["relation_not_stated"], ruling="D-089")),
    ("ASML → Micron", dict(relation_types=["supplies"], source_entities=[ASML], target_entities=[MICRON],
        considered=[sentence("src-029", "p.118, Micron Technology in ASML's remuneration reference group")],
        reasons=["relation_not_stated"], ruling="D-089")),
    ("NVIDIA → H100", dict(relation_types=["designs"], source_entities=[NVIDIA], target_entities=[H100],
        considered=[claim("claim-h100-identity")],
        reasons=["relation_not_stated"], ruling="D-089")),
    ("Amazon → Trainium2", dict(relation_types=["designs"], source_entities=[AMAZON], target_entities=["product-amazon-com-trainium2"],
        considered=[sentence("src-028", "p.5", "Our second version of our custom AI silicon (Trainium2)")],
        reasons=["relation_not_stated"], ruling="D-089")),
    ("Amkor → its subsidiaries", dict(relation_types=["owns"], source_entities=["company-amkor-technology"], target_entities=[nr("its subsidiaries")],
        considered=[sentence("src-026", "p.117, Exhibit 21.1", "List of subsidiaries")],
        reasons=["endpoint_has_no_record"], ruling="D-089")),
    ("Amazon → Amazon Web Services, Inc.", dict(relation_types=["owns"], source_entities=[AMAZON], target_entities=[nr("Amazon Web Services, Inc.")],
        considered=[sentence("src-052", {"state": "not_recorded"}, "Amazon Web Services, Inc. (AWS), an Amazon.com, Inc. company")],
        reasons=["relation_not_stated", "evidence_not_fresh", "endpoint_has_no_record"], ruling="D-089")),
    ("Micron → HBM4 36GB 12H", dict(relation_types=["fabricates"], source_entities=[MICRON], target_entities=["product-micron-technology-hbm4-36gb-12h"],
        considered=[claim("claim-micron-hbm4-identity"), sentence("src-025", "p.7", "We manufacture our products at wholly-owned facilities")],
        reasons=["relation_not_stated", "company_level_only"], ruling="D-089")),
    ("Micron → Manassas", dict(relation_types=["owns", "operates"], source_entities=[MICRON], target_entities=["facility-us-manassas-virginia"],
        considered=[claim("claim-micron-manassas-fab")],
        reasons=["relation_not_stated"], ruling="D-089")),
]


def cells(line: str) -> list[str]:
    if not (line.startswith("|") and line.rstrip().endswith("|")):
        return []
    return [c.strip() for c in line.strip()[1:-1].split("|")]


def table(doc: str) -> list[list[str]]:
    body = doc[doc.index("**Candidates that are not edges**") : doc.index("**Count.**")]
    rows = [cells(line) for line in body.splitlines() if cells(line)]
    assert rows[0] == ["Candidate", "Type", "Sentence", "Why not"], rows[0]
    return rows[2:]


def load(path: str) -> list:
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def migrate(doc: str) -> list[dict]:
    records = {r["id"]: r for kind in ("companies", "products", "facilities", "components", "technologies", "jurisdictions") for r in load(f"data/{kind}.json")}
    claims = {c["id"]: c for c in load("data/claims.json")}
    sources = {s["id"] for s in load("data/sources.json")}
    rows = table(doc)
    assert [r[0] for r in rows] == [k for k, _ in ROWS], "rows differ from the table, or their order"
    out = []
    for n, ((key, spec), (cand_cell, type_cell, sent_cell, why_cell)) in enumerate(zip(ROWS, rows), start=1):
        rec = {"id": f"cand-{n:03d}", **spec, "reasoning": why_cell.replace("`", "")}
        # endpoints
        left, right = (part.strip() for part in cand_cell.split("→"))
        names = [s.strip() for s in left.split(",")] if key.startswith("SK hynix, Micron") else [left]
        for written, value in zip(names + [right], rec["source_entities"] + rec["target_entities"], strict=True):
            if isinstance(value, dict):
                assert value["name"] == written, (key, value, written)
                assert not any(written in (r["name"], *r.get("aliases", [])) for r in records.values()), (key, written, "a record carries this name")
            else:
                r = records[value]
                if written not in (r["name"], *r.get("aliases", [])):
                    holders = [x for x in records.values() if written in x["name"].split()]
                    assert holders == [r] and set(r["identity_claim_ids"]) & set(c["claim_id"] for c in rec["considered"] if "claim_id" in c), (key, written)
        # types, IDs, quotes, locators
        assert rec["relation_types"] == re.findall(r"`([a-z_]+)`", type_cell), (key, type_cell)
        ids = re.findall(r"`((?:claim|src)-[a-z0-9-]+)`", sent_cell)
        mine = [c.get("claim_id") or c.get("source_id") for c in rec["considered"]]
        assert mine == ids, (key, mine, ids)
        assert all(i in claims or i in sources for i in ids), key
        anchors = [c["anchor"] for c in rec["considered"] if "anchor" in c]
        claim_anchors = [cit["anchor"] for c in rec["considered"] if "claim_id" in c for cit in claims[c["claim_id"]].get("citations", [])]
        for quote in re.findall(r'"([^"]+)"', sent_cell):
            if quote in anchors:
                continue
            parts = [p.strip() for p in quote.split("…") if p.strip()]
            assert any(all(p in a for p in parts) for a in claim_anchors), (key, quote, "neither an anchor here nor in a considered claim")
        assert len(anchors) == len([q for q in re.findall(r'"([^"]+)"', sent_cell) if q in anchors]), (key, "an anchor not quoted in the cell")
        for item in rec["considered"]:
            if isinstance(item.get("locator"), str):
                page = item["locator"].split(",")[0]
                assert f"`{item['source_id']}` {page}" in sent_cell, (key, item["locator"])
                if "," in item["locator"]:
                    assert item["locator"].split(", ", 1)[1] in sent_cell, (key, item["locator"])
        if "item" in rec:
            assert f'"{rec["item"]["name"]}"' in why_cell, (key, rec["item"])
        out.append(rec)
    assert len(out) == 12
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", default="docs/architecture/edge-dataset.md")
    parser.add_argument("--write", action="store_true", help="write data/staging/refused_candidates.json")
    args = parser.parse_args(argv[1:])
    out = migrate((REPO / args.doc).read_text(encoding="utf-8") if not Path(args.doc).is_absolute() else Path(args.doc).read_text(encoding="utf-8"))
    print(f"{len(out)} records; every value equals its §1 cell")
    if args.write:
        path = REPO / "data/staging/refused_candidates.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
