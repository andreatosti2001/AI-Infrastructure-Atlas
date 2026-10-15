"""S23 measures: the roadmap's seven points, counted from the canonical records (release content audit, Part 4).

Every number in measures.json is measured from data/ and the documents named below at the audit's base; the readings
of them are the audit's (INTERPRETATION). The output records the SHA-256 of every file read.

  1. conceptual coverage: the domain map's concept IDs (docs/research/domain-map.md §2) against the records that name
     them (concept_refs; identity_basis concept terms, including recorded gaps); the map's 18 concept-level
     dependencies against the Atlas's edges and drawn gaps (DEP_COVERAGE below: a reading by hand, listed so it can
     be checked);
  2. first-hand ratio: per citation, standing party or originator (first-hand, source-policy.md §4, SP-3) against
     reporter; by source class; by layer (the records that cite a claim, below); company-published share;
     corroboration (claims citing two or more publishers, ER-7);
  3. claim verification: from reread-result.json (the re-read of every citation);
  4. counterevidence: claims cited by a conflict CON-01 to CON-05; disputed or partial evidence statuses;
  5. temporal coverage: sources' stated dates by year; access dates; every value on a time_sensitive matrix row
     whose newest accepted evidence is more than 12 months before the reference date (the as-of date of
     sql/source_age.sql), using the freshness rule's own helpers (tests/test_freshness.py), with the reference date
     in place of the claim's verification date;
  6. analytical structure: claims with inputs, input depth, how many inputs each derivation or interpretation uses,
     and how many cite no source of their own;
  7. limitations: explicit states (not_researched, not_publicly_determinable, not_applicable, unknown) by field;
     refused candidates by reason.

Layers: a claim belongs to every layer whose records cite it, directly or as an input, transitively:
  chain (products, components, technologies, identity bases, refused candidates, the five chain edges), suppliers (the two supplier fields),
  companies and places (companies, jurisdictions, facilities, their events), policy (policies, the four restricts
  links, policy events, the Change Detector's later statements). A claim no record reaches is "unreached".

Standard library, plus the test helpers it imports read-only. Usage (from the repository root):
    python docs/quality/audit-evidence/release-content-audit/measure.py > docs/quality/audit-evidence/release-content-audit/measures.json
"""

from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "tests"))

from test_data_entities import fields, load_entities, matrix  # noqa: E402
from test_freshness import evidence_date, horizon_months, months_before  # noqa: E402

FILES = ["data/claims.json", "data/sources.json", "data/relationships.json", "data/events.json",
         "data/policies.json", "data/companies.json", "data/jurisdictions.json", "data/facilities.json",
         "data/products.json", "data/components.json", "data/technologies.json", "data/identity_basis.json",
         "data/refused_candidates.json", "docs/research/domain-map.md", "docs/research/source-policy.md",
         "docs/research/change-detection.md", "sql/source_age.sql"]
CLAIM_ID = re.compile(r"claim-[a-z0-9-]+")
STATES = ("not_researched", "not_publicly_determinable", "not_applicable", "unknown")

# The domain map's concept-level dependencies (§3) against the Atlas's edges and drawn gaps. A reading by hand: the
# edges carry no DEP reference, so which edge realises which dependency is the audit's judgement (INTERPRETATION).
DEP_COVERAGE = {
    "DEP-01": ("edge", "the H100 and Trainium2 incorporate HBM (two incorporates edges)"),
    "DEP-03": ("edge", "HBM requires 3D die stacking (D-091; restates the definition, S13 F-8)"),
    "DEP-05": ("gap", "TSMC fabricates H100 is a drawn gap, cand-001 (D-092)"),
    "DEP-15": ("edge", "Amazon designs Trainium2 (D-093)"),
}


def load(path: str):
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def ids_in(node) -> list[str]:
    if isinstance(node, dict):
        return [c for v in node.values() for c in ids_in(v)]
    if isinstance(node, list):
        return [c for v in node for c in ids_in(v)]
    return [node] if isinstance(node, str) and CLAIM_ID.fullmatch(node) else []


def closure(seed: list[str], claims: dict) -> set[str]:
    seen: set[str] = set()
    queue = list(seed)
    while queue:
        cid = queue.pop()
        if cid in seen or cid not in claims:
            continue
        seen.add(cid)
        queue.extend(claims[cid].get("input_claim_ids", []))
    return seen


def later_statement_ids() -> list[str]:
    text = (REPO / "docs/research/change-detection.md").read_text(encoding="utf-8")
    body = text.partition("### Later statements about acts held")[2].split("\n#")[0]
    return re.findall(r"`(claim-[^`]+)`", body)


def layers(claims: dict) -> dict[str, set[str]]:
    rels = load("data/relationships.json")
    events = load("data/events.json")
    seeds = {
        "chain": ids_in([load(f"data/{f}.json") for f in ("products", "components", "technologies",
                                                          "identity_basis", "refused_candidates")])
                 + [c for r in rels if r["relation_type"] != "restricts" for c in r["claim_ids"]],
        "suppliers": [c for r in rels for s in r.get("supplier", []) for c in s["claim_ids"]],
        "companies_and_places": ids_in([load(f"data/{f}.json") for f in ("companies", "jurisdictions", "facilities")])
                                + ids_in([e for e in events if not e["subject"].startswith("policy-")]),
        "policy": ids_in(load("data/policies.json")) + [c for r in rels if r["relation_type"] == "restricts"
                                                        for c in r["claim_ids"]]
                  + ids_in([e for e in events if e["subject"].startswith("policy-")]) + later_statement_ids(),
    }
    out = {k: closure(v, claims) for k, v in seeds.items()}
    reached = set().union(*out.values())
    out["unreached"] = set(claims) - reached
    return out


def citation_stats(ids, claims, sources) -> dict:
    cits = [(cid, ci) for cid in ids for ci in claims[cid].get("citations", [])]
    standing = collections.Counter(ci["standing"] for _, ci in cits)
    classes = collections.Counter(sources[ci["source_id"]]["source_class"] for _, ci in cits)
    company = sum(n for k, n in classes.items() if k.startswith("company_"))
    publishers = {cid: {sources[ci["source_id"]]["publisher"] for ci in claims[cid].get("citations", [])} for cid in ids}
    return {
        "claims": len(ids),
        "claims_citing_a_source": sum(1 for cid in ids if claims[cid].get("citations")),
        "citations": len(cits),
        "standing": dict(standing),
        "first_hand_share": round((standing["party"] + standing["originator"]) / len(cits), 3) if cits else None,
        "by_class": dict(sorted(classes.items(), key=lambda kv: -kv[1])),
        "company_published_citations": company,
        "official_legal_text_citations": classes.get("official_legal_text", 0),
        "claims_citing_two_or_more_publishers": sum(1 for p in publishers.values() if len(p) >= 2),
        "by_type": dict(collections.Counter(claims[cid]["claim_type"] for cid in ids)),
    }


def conceptual_coverage(entities_all) -> dict:
    text = (REPO / "docs/research/domain-map.md").read_text(encoding="utf-8")
    body = text.partition("## 2. Concept entries by layer")[2].partition("## 3.")[0]
    concepts = sorted(set(re.findall(r"\b(?:ACC|HBM|PKG|FAB|EDA|SME|DC|EN)-\d{2}\b", body)))
    deps = sorted(set(re.findall(r"\bDEP-\d{2}\b", text)))
    with_record = {c for r in entities_all for c in (r.get("concept_refs") or [])}
    basis = load("data/identity_basis.json")
    gaps = {b["concept"] for b in basis if b.get("kind") == "concept_term" and isinstance(b["record"], dict)}
    by_layer = collections.defaultdict(lambda: [0, 0])
    for c in concepts:
        by_layer[c.split("-")[0]][0] += 1
        by_layer[c.split("-")[0]][1] += c in with_record
    return {
        "concepts": len(concepts),
        "concepts_with_a_record": len([c for c in concepts if c in with_record]),
        "concepts_recorded_as_gap": sorted(gaps),
        "by_layer_concepts_and_with_record": {k: v for k, v in sorted(by_layer.items())},
        "concepts_without_record": [c for c in concepts if c not in with_record],
        "dependencies": len(deps),
        "dependencies_with_an_edge": sorted(k for k, v in DEP_COVERAGE.items() if v[0] == "edge"),
        "dependencies_drawn_as_gap": sorted(k for k, v in DEP_COVERAGE.items() if v[0] == "gap"),
        "dependency_reading": {k: v[1] for k, v in DEP_COVERAGE.items()},
    }


def reference_date() -> str:
    (day,) = re.findall(r"DATE '(\d{4}-\d{2}-\d{2})' AS reference_date", (REPO / "sql/source_age.sql").read_text())
    return day


def leaf(cid, claims, seen=None):
    seen = seen or set()
    if cid in seen or cid not in claims:
        return []
    seen.add(cid)
    claim = claims[cid]
    out = [(claim, ci) for ci in claim.get("citations", [])]
    for i in claim.get("input_claim_ids", []):
        out += leaf(i, claims, seen)
    return out


def temporal(claims, sources, ref) -> dict:
    rows = matrix()
    months = horizon_months()
    limit = months_before(ref, months)
    exposed, fresh, values = [], 0, 0
    entities = load_entities()["canonical"]
    for kind in entities:
        for record in entities[kind]:
            for field, row_key, assertions in fields(record):
                row = rows[row_key]
                if row["freshness"] != "time_sensitive":
                    continue
                for assertion, ids in assertions:
                    if assertion and "valid_to" in assertion:
                        continue
                    values += 1
                    dates = [evidence_date(c, sources[ci["source_id"]]) for cid in ids for c, ci in leaf(cid, claims)
                             if sources[ci["source_id"]]["source_class"] in row["sufficient"]
                             and ci["standing"] in row["standings"]]
                    newest = max(dates) if dates else None
                    if newest and newest >= limit:
                        fresh += 1
                    else:
                        exposed.append({"record": record["id"], "field": field,
                                        "value": assertion.get("value") if assertion else None, "newest_evidence": newest})
    for edge in load("data/relationships.json"):
        for key, ids, hist in [(f"rel:{edge['relation_type']}", edge["claim_ids"], False)] + [
                (f"rel:{edge['relation_type']}.supplier", s["claim_ids"], "valid_to" in s) for s in edge.get("supplier", [])]:
            if key not in rows or rows[key]["freshness"] != "time_sensitive" or hist:
                continue
            values += 1
            dates = [evidence_date(c, sources[ci["source_id"]]) for cid in ids for c, ci in leaf(cid, claims)
                     if sources[ci["source_id"]]["source_class"] in rows[key]["sufficient"] and ci["standing"] in rows[key]["standings"]]
            newest = max(dates) if dates else None
            if newest and newest >= limit:
                fresh += 1
            else:
                exposed.append({"record": edge["id"], "field": key, "newest_evidence": newest})
    stated = collections.Counter()
    for s in sources.values():
        ds = s["stated_dates"]
        stated[max(d["date"] for d in ds)[:4] if isinstance(ds, list) else "undated"] += 1
    access = collections.Counter(s["retrieval"]["accessed_at"][:10] for s in sources.values())
    return {
        "reference_date": ref, "horizon_months": months, "limit": limit,
        "time_sensitive_current_values": values, "within_horizon": fresh,
        "beyond_horizon_at_reference_date": exposed,
        "sources_by_newest_stated_year": dict(sorted(stated.items())),
        "sources_by_access_day": dict(sorted(access.items())),
    }


def analytical(claims) -> dict:
    derived = [c for c in claims.values() if c.get("input_claim_ids")]

    def depth(cid, seen=()):
        c = claims[cid]
        if cid in seen or not c.get("input_claim_ids"):
            return 0
        return 1 + max(depth(i, seen + (cid,)) for i in c["input_claim_ids"])

    return {
        "claims_with_inputs": len(derived),
        "by_type": dict(collections.Counter(c["claim_type"] for c in derived)),
        "citing_no_source_of_their_own": sum(1 for c in derived if not c.get("citations")),
        "inputs_per_claim": dict(sorted(collections.Counter(len(c["input_claim_ids"]) for c in derived).items())),
        "max_input_depth": max(depth(c["id"]) for c in derived),
        "depth_distribution": dict(sorted(collections.Counter(depth(c["id"]) for c in derived).items())),
    }


def limitations(entities_all) -> dict:
    states = collections.Counter()

    def walk(node, path):
        if isinstance(node, dict):
            if node.get("state") in STATES:
                states[(path, node["state"])] += 1
            for k, v in node.items():
                walk(v, k)
        elif isinstance(node, list):
            for v in node:
                walk(v, path)

    for r in entities_all + load("data/relationships.json"):
        walk(r, "")
    refused = collections.Counter(reason for c in load("data/refused_candidates.json") for reason in c["reasons"])
    pages = sorted((REPO / "site").rglob("*.html"))
    shown = {c for p in pages for c in CLAIM_ID.findall(p.read_text(encoding="utf-8"))}
    claims = [c["id"] for c in load("data/claims.json")]
    return {"pages": len(pages),
            "pages_digest": hashlib.sha256("".join(hashlib.sha256(p.read_bytes()).hexdigest() for p in pages).encode()).hexdigest(),
            "claims_on_no_page": sorted(c for c in claims if c not in shown),
            "explicit_states_by_field": {f"{k[0]}:{k[1]}": n for k, n in sorted(states.items())},
            "explicit_states_total": dict(collections.Counter(k[1] for k in states.elements())),
            "refused_candidates": len(load("data/refused_candidates.json")),
            "refusal_reasons": dict(refused.most_common())}


def verification() -> dict:
    path = HERE / "reread-result.json"
    if not path.exists():
        return {"note": "reread-result.json not present"}
    rows = json.loads(path.read_text(encoding="utf-8"))["citations"]
    return {"citations": len(rows), "anchor": dict(collections.Counter(r["anchor"] for r in rows)),
            "equals_registered": dict(collections.Counter(str(r.get("equals_registered")) for r in rows if r["anchor"] != "access_gap")),
            "sources_with_changed_bytes": sorted({r["source_id"] for r in rows if r.get("equals_registered") is False}),
            "access_gap_sources": sorted({r["source_id"] for r in rows if r["anchor"] == "access_gap"}),
            "locator_page_mismatch": [f"{r['claim']} #{r['citation']}" for r in rows if r.get("locator_page_matches") is False]}


def main() -> None:
    claims = {c["id"]: c for c in load("data/claims.json")}
    sources = {s["id"]: s for s in load("data/sources.json")}
    entities_all = [r for f in ("companies", "jurisdictions", "facilities", "products", "components", "technologies",
                                "policies") for r in load(f"data/{f}.json")]
    lay = layers(claims)
    policy_text = (REPO / "docs/research/source-policy.md").read_text(encoding="utf-8")
    con_rows = policy_text.partition("### 10.2 CON-01 to CON-05")[2].split("\n## ")[0]
    out = {
        "inputs": {p: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for p in FILES},
        "counts": {"claims": len(claims), "sources": len(sources),
                   "sources_cited": len({ci["source_id"] for c in claims.values() for ci in c.get("citations", [])}),
                   "claim_types": dict(collections.Counter(c["claim_type"] for c in claims.values())),
                   "evidence_status": dict(collections.Counter(c["evidence_status"] for c in claims.values())),
                   "source_classes": dict(collections.Counter(s["source_class"] for s in sources.values())),
                   "retrieval_method": dict(collections.Counter(s["retrieval"]["method"] for s in sources.values()))},
        "1_conceptual_coverage": conceptual_coverage(entities_all),
        "2_first_hand": {"all": citation_stats(list(claims), claims, sources),
                         **{k: citation_stats(sorted(v), claims, sources) for k, v in lay.items()}},
        "3_verification": verification(),
        "4_counterevidence": {"conflicts_recorded": sorted(set(re.findall(r"CON-0\d", con_rows))),
                              "evidence_status_other_than_supported": sum(1 for c in claims.values()
                                                                          if c["evidence_status"] != "supported")},
        "5_temporal": temporal(claims, sources, reference_date()),
        "6_analytical": analytical(claims),
        "7_limitations": limitations(entities_all),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
