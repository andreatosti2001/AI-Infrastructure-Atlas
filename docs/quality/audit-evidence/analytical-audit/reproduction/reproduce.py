"""S16 independent reproduction of three page metrics from data/ and definitions.md only.

Run from the repository root:  python3 docs/quality/audit-evidence/analytical-audit/reproduction/reproduce.py
Standard library only. Deterministic output (sorted iteration, fixed reference date).

Every interpretive choice the plain definitions leave open is marked CHOICE-n below and
repeated in the output, together with the alternative's effect on the numbers where it has one.
"""
import json
import os
from datetime import date, timedelta

DATA = "data"
REF = date(2026, 10, 6)          # given: the page's printed reference date
HORIZON_MONTHS = 12               # given: the freshness horizon

ACCELERATORS = [                  # given: the page is about these two accelerators
    "product-amazon-com-trainium2",
    "product-nvidia-h100-tensor-core-gpu",
]

STATED_TYPES = {"FACT", "ATTRIBUTION"}                       # CHOICE-4
INFERRED_TYPES = {"DERIVATION", "INTERPRETATION", "IMPLICATION"}


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


claims = {c["id"]: c for c in load("claims.json")}
sources = {s["id"]: s for s in load("sources.json")}
rels = load("relationships.json")
refused = load("refused_candidates.json")
products = {p["id"]: p for p in load("products.json")}

names = {}
for f in ["products.json", "companies.json", "components.json", "technologies.json",
          "facilities.json", "jurisdictions.json"]:
    for r in load(f):
        names[r["id"]] = r["name"]


def nm(x):
    if isinstance(x, dict):
        return "%s [%s]" % (x.get("name", "?"), x.get("state"))
    return names.get(x, x)


def is_state(v):
    return isinstance(v, dict) and set(v) <= {"state", "name", "note"} and "state" in v


# ---------------------------------------------------------------- dates
def parse_date(s, partial_rule):
    """Return a date for 'YYYY-MM-DD', 'YYYY-MM', 'YYYY' or an ISO timestamp. CHOICE-9."""
    s = s[:10]
    parts = s.split("-")
    y = int(parts[0])
    if len(parts) == 3:
        return date(y, int(parts[1]), int(parts[2]))
    if len(parts) == 2:
        m = int(parts[1])
        if partial_rule == "start":
            return date(y, m, 1)
        nxt = date(y + (m == 12), m % 12 + 1, 1)
        return nxt - timedelta(days=1)
    return date(y, 1, 1) if partial_rule == "start" else date(y, 12, 31)


def evidence_of_claim(cid, seen=None):
    """Leaf evidence behind a claim: list of (kind, raw_date, origin).

    kind 'content' = a date the evidence itself carries (claim as_of, source stated_dates);
    kind 'access'  = when the Atlas read it (citation read.accessed_at, else source retrieval).
    Claims without citations are followed through input_claim_ids (CHOICE-6)."""
    seen = seen or set()
    if cid in seen or cid not in claims:
        return []
    seen = seen | {cid}
    c = claims[cid]
    out = []
    a = c.get("as_of")
    if isinstance(a, str):
        out.append(("content", a, "%s.as_of" % cid))
    for cit in c.get("citations", []):
        src = sources.get(cit["source_id"], {})
        sd = src.get("stated_dates")
        if isinstance(sd, list):
            for d in sd:
                out.append(("content", d["date"], "%s.stated_dates[%s]" % (src["id"], d["kind"])))
        rd = cit.get("read", {})
        if isinstance(rd, dict) and "accessed_at" in rd:
            out.append(("access", rd["accessed_at"], "%s citation read.accessed_at (%s)" % (cid, cit["source_id"])))
        elif "accessed_at" in src.get("retrieval", {}):
            out.append(("access", src["retrieval"]["accessed_at"], "%s.retrieval.accessed_at" % src["id"]))
    for ic in c.get("input_claim_ids", []) or []:
        out.extend(evidence_of_claim(ic, seen))
    return out


def evidence_of_considered(item):
    """Evidence behind a refused candidate's 'considered' entry."""
    if "claim_id" in item:
        return evidence_of_claim(item["claim_id"])
    out = []
    src = sources.get(item.get("source_id"), {})
    sd = src.get("stated_dates")
    if isinstance(sd, list):
        for d in sd:
            out.append(("content", d["date"], "%s.stated_dates[%s]" % (src["id"], d["kind"])))
    rd = item.get("read", {})
    if isinstance(rd, dict) and "accessed_at" in rd:
        out.append(("access", rd["accessed_at"], "candidate read.accessed_at (%s)" % item.get("source_id")))
    return out


def newest(evidence, partial_rule="end", access_mode="fallback", source_access="citation"):
    """Newest evidence date. access_mode: 'fallback' (CHOICE-7: access date only when no content
    date exists), 'never' (access dates are not evidence dates), 'always' (all dates count)."""
    ev = evidence
    if source_access == "retrieval":   # CHOICE-8 alternative: use the source record's retrieval date
        ev2 = []
        for k, d, o in ev:
            if k == "access" and "citation read" in o:
                sid = o.split("(")[-1].rstrip(")")
                ev2.append((k, sources[sid]["retrieval"]["accessed_at"], "%s.retrieval.accessed_at" % sid))
            else:
                ev2.append((k, d, o))
        ev = ev2
    content = [(parse_date(d, partial_rule), o, "content") for k, d, o in ev if k == "content"]
    access = [(parse_date(d, partial_rule), o, "access") for k, d, o in ev if k == "access"]
    if access_mode == "never":
        pool = content
    elif access_mode == "always":
        pool = content + access
    else:
        pool = content or access
    if not pool:
        return None
    return max(pool, key=lambda t: (t[0], t[1]))


def horizon_cutoff():
    y, m = REF.year, REF.month - HORIZON_MONTHS
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, REF.day)


# ---------------------------------------------------------------- table of links
def touches(entity_list_or_id, target):
    if isinstance(entity_list_or_id, list):
        return target in entity_list_or_id
    return entity_list_or_id == target


def claim_class(claim_ids):
    types = {claims[c]["claim_type"] for c in claim_ids if c in claims}
    if types and types <= STATED_TYPES:
        return "stated"
    if types & INFERRED_TYPES:
        return "inferred"
    return "unclassified"


def build_rows(variant):
    """One row per accelerator and link. variant switches the alternatives of CHOICE-1/2/3/5."""
    rows = []
    for acc in ACCELERATORS:
        # Hop 1: canonical relationships with the accelerator as an endpoint (CHOICE-1)
        hop1 = [r for r in rels if acc in (r["source_entity"], r["target_entity"])]
        parts = sorted({r["target_entity"] for r in hop1
                        if r["relation_type"] == "incorporates" and r["source_entity"] == acc})
        linked = list(hop1)
        # Hop 2: links of the incorporated parts the page is about (CHOICE-2)
        if variant.get("hop2", True):
            for r in rels:
                if r in linked:
                    continue
                if r["source_entity"] in parts or (variant.get("hop2_inbound", False) and r["target_entity"] in parts):
                    linked.append(r)
        for r in sorted(linked, key=lambda r: r["id"]):
            rows.append({
                "acc": acc, "record": r["id"], "kind": claim_class(r["claim_ids"]),
                "link": "%s %s %s" % (nm(r["source_entity"]), r["relation_type"], nm(r["target_entity"])),
                "evidence": [e for c in r["claim_ids"] for e in evidence_of_claim(c)],
                "claims": list(r["claim_ids"]),
            })
            # The unknown supplier is a row of its own on the incorporates link (given)
            if r["relation_type"] == "incorporates" and is_state(r.get("supplier")):
                rows.append({
                    "acc": acc, "record": r["id"], "kind": "gap",
                    "link": "supplier of %s in %s: %s" % (nm(r["target_entity"]), nm(r["source_entity"]), r["supplier"]["state"]),
                    "evidence": [], "claims": [],
                })
        # Gaps: refused candidates with the accelerator as an endpoint (CHOICE-3)
        for c in refused:
            if touches(c["source_entities"], acc) or touches(c["target_entities"], acc):
                # CHOICE-5: a refusal of one piece of evidence for a link that IS recorded is not a gap
                dup = any(r["relation_type"] in c["relation_types"]
                          and r["source_entity"] in c["source_entities"]
                          and r["target_entity"] in c["target_entities"] for r in rels)
                if dup and not variant.get("count_refused_evidence_for_recorded_link", False):
                    continue
                rows.append({
                    "acc": acc, "record": c["id"], "kind": "gap",
                    "link": "%s %s %s (refused: %s)" % (", ".join(nm(x) for x in c["source_entities"]),
                                                          "/".join(c["relation_types"]),
                                                          ", ".join(nm(x) for x in c["target_entities"]),
                                                          ", ".join(c["reasons"])),
                    "evidence": [e for it in c["considered"] for e in evidence_of_considered(it)]
                    if variant.get("date_gaps", True) else [],
                    "claims": [it["claim_id"] for it in c["considered"] if "claim_id" in it],
                })
        # Optional: product-record reference fields as links (CHOICE-1 alternative)
        if variant.get("product_fields", False):
            p = products[acc]
            rows.append({"acc": acc, "record": acc, "kind": "stated",
                         "link": "%s vendor %s" % (p["name"], nm(p["vendor"])),
                         "evidence": [e for c in p["identity_claim_ids"] for e in evidence_of_claim(c)],
                         "claims": list(p["identity_claim_ids"])})
            for cls in p["instance_of"]:
                basis = [b["claim_id"] for b in load("identity_basis.json")
                         if b["kind"] == "instance_of_basis" and b["record"] == acc and b["class"] == cls]
                rows.append({"acc": acc, "record": acc, "kind": claim_class(basis),
                             "link": "%s instance_of %s" % (p["name"], nm(cls)),
                             "evidence": [e for c in basis for e in evidence_of_claim(c)], "claims": basis})
    return rows


def coverage(rows):
    out = {}
    for acc in ACCELERATORS:
        mine = [r for r in rows if r["acc"] == acc]
        other = {r["record"] for r in rows if r["acc"] != acc}
        recs = {r["record"] for r in mine}
        out[acc] = {
            "links": len(mine),
            "stated": sum(r["kind"] == "stated" for r in mine),
            "inferred": sum(r["kind"] == "inferred" for r in mine),
            "gap": sum(r["kind"] == "gap" for r in mine),
            "unclassified": sum(r["kind"] == "unclassified" for r in mine),
            "records": len(recs),
            "shared_records": len(recs & other),
        }
    return out


def age_table(rows, **kw):
    cut = horizon_cutoff()
    per = []
    for r in rows:
        n = newest(r["evidence"], **kw)
        if n is None:
            per.append((r, None, None, None, None, None))
        else:
            d, origin, kind = n
            age = (REF - d).days
            per.append((r, d, origin, kind, age, d < cut))
    summary = {}
    for acc in ACCELERATORS:
        mine = [p for p in per if p[0]["acc"] == acc]
        dated = [p for p in mine if p[1] is not None]
        summary[acc] = {
            "dated": len(dated),
            "beyond_horizon": sum(1 for p in dated if p[5]),
            "beyond_365d": sum(1 for p in dated if p[4] > 365),
            "access_date_only": sum(1 for p in dated if p[3] == "access"),
            "nothing_to_date": len(mine) - len(dated),
        }
    return per, summary


def supplier_metrics():
    out = {}
    for acc in ACCELERATORS:
        inc = [r for r in rels if r["relation_type"] == "incorporates" and r["source_entity"] == acc]
        named = [r for r in inc if not is_state(r.get("supplier")) and r.get("supplier") is not None]
        unknown = [r for r in inc if is_state(r.get("supplier"))]
        parts = {r["target_entity"] for r in inc}
        # company-to-company supply links recorded for those parts: canonical 'supplies' relationships (CHOICE-11)
        supply = [r for r in rels if r["relation_type"] == "supplies"
                  and (r.get("item") in parts or r["target_entity"] in parts)]
        supply_any = [r for r in rels if r["relation_type"] == "supplies"]
        refused_supply = [c for c in refused if "supplies" in c["relation_types"]
                          and ((isinstance(c.get("item"), str) and c["item"] in parts)
                               or any(isinstance(t, str) and t in parts for t in c["target_entities"]))]
        out[acc] = {
            "incorporated_parts": len(inc),
            "parts": sorted(nm(p) for p in parts),
            "named_supplier": len(named),
            "unknown": len(unknown),
            "unknown_state_words": sorted({r["supplier"]["state"] for r in unknown}),
            "supply_links_for_parts": len(supply),
            "supply_links_any_in_atlas": len(supply_any),
            "refused_supply_candidates_for_parts": len(refused_supply),
        }
    return out


# ---------------------------------------------------------------- report
def main():
    P = print
    P("S16 reproduction  (reference date %s, horizon %d months -> evidence dated before %s is beyond it)"
      % (REF, HORIZON_MONTHS, horizon_cutoff()))
    P()
    base = build_rows({})
    P("TABLE OF LINKS (primary interpretation)")
    for r in base:
        P("  %-14s %-9s %-75s record=%s" % (nm(r["acc"]), r["kind"], r["link"][:75], r["record"]))
    P()
    P("1. EVIDENCE COVERAGE (primary)")
    cov = coverage(base)
    P("  %-14s %5s %6s %8s %4s %7s %6s" % ("accelerator", "links", "stated", "inferred", "gap", "records", "shared"))
    for acc in ACCELERATORS:
        c = cov[acc]
        P("  %-14s %5d %6d %8d %4d %7d %6d" % (nm(acc), c["links"], c["stated"], c["inferred"], c["gap"], c["records"], c["shared_records"]))
    P()
    P("  Alternatives (each changes one choice from primary):")
    alts = [
        ("CHOICE-2 alt: no hop-2 (only links touching the accelerator itself)", {"hop2": False}),
        ("CHOICE-2 alt: hop-2 also inbound to the part (the other accelerator's incorporates link + its supplier row)", {"hop2_inbound": True}),
        ("CHOICE-5 alt: cand-008 (refused extra evidence for Amazon-designs-Trainium2) counted as a gap row", {"count_refused_evidence_for_recorded_link": True}),
        ("CHOICE-1 alt: product-record fields vendor + instance_of counted as links", {"product_fields": True}),
    ]
    for label, v in alts:
        c2 = coverage(build_rows(v))
        P("   - " + label)
        for acc in ACCELERATORS:
            c = c2[acc]
            P("       %-14s links=%d stated=%d inferred=%d gap=%d records=%d shared=%d"
              % (nm(acc), c["links"], c["stated"], c["inferred"], c["gap"], c["records"], c["shared_records"]))
    P()

    P("2. SOURCE AGE (primary: content dates; access date only as fallback; partial date -> last day of period)")
    per, summ = age_table(base)
    for r, d, origin, kind, age, beyond in per:
        if d is None:
            P("  %-14s %-60s  no date (nothing to date)" % (nm(r["acc"]), r["link"][:60]))
        else:
            P("  %-14s %-60s  newest=%s age=%4dd beyond=%s  from %s [%s]"
              % (nm(r["acc"]), r["link"][:60], d, age, "yes" if beyond else "no", origin, kind))
    P()
    P("  %-14s %5s %14s %16s %15s" % ("accelerator", "dated", "beyond_horizon", "access_date_only", "nothing_to_date"))
    for acc in ACCELERATORS:
        s = summ[acc]
        P("  %-14s %5d %14d %16d %15d" % (nm(acc), s["dated"], s["beyond_horizon"], s["access_date_only"], s["nothing_to_date"]))
        if s["beyond_horizon"] != s["beyond_365d"]:
            P("     (365-day rule would give beyond=%d)" % s["beyond_365d"])
    P()
    P("  Alternatives:")
    for label, rows_v, kw in [
        ("CHOICE-7 alt 'never': access dates are not evidence dates", base, {"access_mode": "never"}),
        ("CHOICE-7 alt 'always': access dates compete with content dates", base, {"access_mode": "always"}),
        ("CHOICE-8 alt: source retrieval.accessed_at instead of the citation's read.accessed_at", base, {"source_access": "retrieval"}),
        ("CHOICE-9 alt: partial date -> first day of period", base, {"partial_rule": "start"}),
        ("CHOICE-10 alt: refused-candidate (gap) rows get no date", build_rows({"date_gaps": False}), {}),
        ("CHOICE-2 alt: no hop-2", build_rows({"hop2": False}), {}),
    ]:
        per2, s2 = age_table(rows_v, **kw)
        P("   - " + label)
        for acc in ACCELERATORS:
            s = s2[acc]
            P("       %-14s dated=%d beyond=%d access_only=%d nothing_to_date=%d"
              % (nm(acc), s["dated"], s["beyond_horizon"], s["access_date_only"], s["nothing_to_date"]))
        if kw.get("source_access") == "retrieval" or kw.get("partial_rule") == "start":
            for r, d, origin, kind, age, beyond in per2:
                if (kind == "access" and kw.get("source_access")) or (kw.get("partial_rule") and "src-039" in (origin or "")):
                    P("       %s / %s: %s age %dd" % (nm(r["acc"]), r["link"][:50], d, age))
    P()

    P("3. SUPPLIER METRICS")
    sm = supplier_metrics()
    for acc in ACCELERATORS:
        s = sm[acc]
        P("  %-14s parts=%d %s named=%d unknown=%d state=%s supply_links_for_parts=%d (supplies edges anywhere=%d; refused supply candidates for these parts=%d)"
          % (nm(acc), s["incorporated_parts"], s["parts"], s["named_supplier"], s["unknown"],
             ",".join(s["unknown_state_words"]), s["supply_links_for_parts"], s["supply_links_any_in_atlas"],
             s["refused_supply_candidates_for_parts"]))
    P("  Supplier count / concentration / single-source: not computed (no part has a named supplier).")


if __name__ == "__main__":
    main()
