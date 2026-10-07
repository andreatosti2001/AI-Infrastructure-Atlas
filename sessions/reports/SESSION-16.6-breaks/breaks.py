"""S16.6: the merged break harness (S13 to S16.5) plus S16.6's breaks (D-144 to D-148).

Loads S16.5's harness (`sessions/reports/SESSION-16.5-breaks/breaks.py`), replaces the inherited breaks whose
setup text or meaning S16.6 changed (named below, with the reason), and adds S16.6's breaks and a control. The
rules are S15's: each break copies the repository, makes one edit, runs its build steps (results -> HBM page ->
research view), runs the full suite, and counts only if the suite fails with every expected fragment in its
output. A control counts only if the suite passes.

Run with a virtualenv built from requirements-test.txt and requirements-analysis.txt:
    python sessions/reports/SESSION-16.6-breaks/breaks.py SCRATCH_DIR [ID ...]
    python sessions/reports/SESSION-16.6-breaks/breaks.py SCRATCH_DIR --setup-only
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("s165_breaks", REPO / "sessions/reports/SESSION-16.5-breaks/breaks.py")
s165 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s165)
s15 = s165.s15
s13 = s15.module("sessions/reports/SESSION-13-breaks/breaks.py")
edit, jedit, both, ALL = s15.edit, s15.jedit, s15.both, s15.ALL
INSIGHT, INSIGHT_BUILD, PAGE_BUILD, CHAIN = s15.INSIGHT, s15.INSIGHT_BUILD, s15.PAGE_BUILD, s15.CHAIN
WH, COV, SUP, DEP = s15.WH, s15.COV, s15.SUP, "sql/accelerator_dependencies.sql"
H100, H100_HBM = s15.H100, s165.H100_HBM
TRN2_HBM = "rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory"
TRENDFORCE = "claim-trendforce-h100-hbm3-primarily-sk-hynix-2024"
SEMIANALYSIS = "claim-semianalysis-trn2-hbm-samsung-2025"


def cand(d, cid):
    return next(c for c in (d["refused_candidates"] if isinstance(d, dict) else d) if c["id"] == cid)


def claim(d, cid):
    return next(c for c in (d["claims"] if isinstance(d, dict) else d) if c["id"] == cid)


def edge(d, eid):
    return next(e for e in (d["relationships"] if isinstance(d, dict) else d) if e["id"] == eid)


# Inherited breaks whose setup text or meaning S16.6 changed, each replaced by the same fault on the S16.6 tree:
# - S13's harness numbers its first breaks "1", "2", ... and its D-111 breaks "S13-1", "S13-2", ...; the merged
#   harness names both S13-n, so S13's replacements are keyed by their description (REPLACED_BY_WHAT):
#   - "a supplier gap drawn as zero": both suppliers are now named, so the page's one remaining gap mark
#     (TSMC -> H100, "gap: no edge") is drawn as 0;
# - S13-1 to S13-5 (D-111) edited Samsung as cand-002's firm with no record. D-149 links Samsung's new record, so
#   each fault moves to a no-record name that remains: cand-002's item ("memory", the only one the HBM page
#   draws) for S13-1 and S13-2, cand-004's firm (Carl Zeiss SMT GmbH) for S13-3 and S13-4; S13-5 drops
#   Samsung's linked record from the card instead;
# - S13-20 removed one of cand-002's two cards; with one reason left cand-002 has one card, so the page's card in
#   two groups is now cand-011's.
# - S14.5-T1 and T2 edited the H100's age tally "3 of 3"; the H100 now has four dated links ("4 of 4").
# - S14.5-L1 edited the headline's label "each"; the headline is now the question alone (V-2: the two chains no
#   longer share one supplier state), so a question label is edited.
# - S15-M8 showed the retired column parts_supplier_named; the same fault is now a zero kind shown.
# - S15-M9 planted a named supplier to make a metric computable; D-148 made the status depend on the "needs",
#   not on any supplier being named, so the fault is now the status rule loosened in SQL.
REPLACED_BY_WHAT = {
    ("S13-20", "a card removed from one of its reason groups"): (
        "S13-20", "a card removed from one of its reason groups (cand-011, the page's one card in two groups)",
        lambda root: s13.remove_last_card(root, "cand-011"), [],
        ["test_pg5_candidates_are_cards_never_lines"]),
    ("S13-5", "Samsung dropped from the data, page not rebuilt"): ("S13-5", "Samsung's linked record dropped from the card, page not rebuilt",
              jedit("data/refused_candidates.json", lambda d: cand(d, "cand-002")["source_entities"].pop()), [],
              ["test_pg7"]),
    ("S13-3", "Samsung's no-record name replaced by a record's name (SK hynix)"): ("S13-3", "a no-record name replaced by a record's name (cand-004's firm -> SK hynix)",
              jedit("data/refused_candidates.json", lambda d: cand(d, "cand-004")["source_entities"][0].update(name="SK hynix")), [],
              ["no_record 'SK hynix' names a record"]),
    ("S13-2", "Samsung kept, its reason dropped"): ("S13-2", "the no-record item kept, its reason dropped (cand-002)",
              jedit("data/refused_candidates.json", lambda d: cand(d, "cand-002")["reasons"].remove("item_has_no_record")), [],
              ["cand-002: the item has no record, but item_has_no_record is not a reason"]),
    ("S13-1", "Samsung removed from the page's card by hand (not rebuilt)"): ("S13-1", "the no-record item removed from the page's card by hand (cand-002's 'memory', not rebuilt)",
              edit(CHAIN, 'data-ref="cand-002" data-field="/item/name">memory</span>', 'data-ref="cand-002" data-field="/item/name"></span>'), [],
              ["test_pg2", "cand-002"]),
    ("S13-4", "a supplier gap drawn as zero"): (
        "S13-4", "a gap drawn as zero (the HBM page's remaining gap mark)",
        edit(CHAIN, 'text-anchor="middle" data-label>gap: no edge<', 'text-anchor="middle" data-label>0<'), [],
        ["a gap drawn as zero"]),
    ("S13-4", "Samsung's no-record name replaced by a placeholder"): (
        "S13-4", "a no-record name replaced by a placeholder (cand-004's firm)",
        jedit("data/refused_candidates.json", lambda d: cand(d, "cand-004")["source_entities"][0].update(name="unknown")), [],
        ["placeholder"]),
}

REPLACED = {
    "S14.5-T1": ("S14.5-T1", "a tally hand-edited on the page (H100: 4 of 4 dated links older -> 3 of 4)",
                 edit(INSIGHT, f'data-derived="age-beyond" data-accelerator="{H100}">4<', f'data-derived="age-beyond" data-accelerator="{H100}">3<'), [],
                 ["test_in3_derived_values_are_recomputed", "test_in8_rebuild_is_byte_identical"]),
    "S14.5-T2": ("S14.5-T2", "a tally's denominator removed from its block (the age block)",
                 edit(INSIGHT, f' <span data-label>of</span> <span data-derived="age-dated" data-accelerator="{H100}">4</span></span>', "</span>"), [],
                 ["a tally whose denominator is not in the same block"]),
    "S14.5-L1": ("S14.5-L1", "a label in the headline hand-edited ('What does an' -> 'What does every')",
                 edit(INSIGHT, "<span data-label>What does an</span>", "<span data-label>What does every</span>"), [],
                 ["a label that is not one of the build's labels"]),
    "S15-M8": ("S15-M8", "the page shows a zero supplier kind beside a supplier metric (rebuilt)",
               edit(INSIGHT_BUILD, '("parts_supplier_reported", "with a supplier reported by a third party;"))\n                    if r[column]',
                    '("parts_supplier_reported", "with a supplier reported by a third party;"))\n                    if True'), [INSIGHT_BUILD],
               ["a zero beside a supplier metric reads as 'no suppliers'"]),
    "S15-M9": ("S15-M9", "the supplier metrics' status loosened: computable once suppliers are named (rebuilt)",
               edit(SUP, "'cannot_be_computed_yet' AS status,", "'computable' AS status,"), ALL,
               ["a supplier metric became computable"]),
}

S166 = [
    ("S16.6-A1", "a reported supplier relabelled 'stated' in the first query (rebuilt)",
     edit(DEP, "cl.claim_type = 'ATTRIBUTION') THEN 'reported'", "cl.claim_type = 'ATTRIBUTION') THEN 'stated'"), ALL,
     ["test_wh10_the_first_result_equals_an_independent_computation"]),
    ("S16.6-A2", "coverage counts reported links as gaps (rebuilt)",
     edit(COV, "count(*) FILTER (WHERE l.basis = 'gap') AS gap,", "count(*) FILTER (WHERE l.basis IN ('gap', 'reported')) AS gap,"), ALL,
     ["test_wh12_evidence_coverage_equals_an_independent_computation", "the parts do not add up to the denominator"]),
    ("S16.6-A3", "the warehouse drops the third-party criteria (rebuilt)",
     edit(WH, '                rows["citation_criteria"].append((c["id"], i, criterion, verdict["met"], verdict["reason"]))',
          '                pass'), ALL,
     ["test_wh3_third_party_criteria_reach_sql_row_by_row"]),
    ("S16.6-A4", "the research view leaves out a historical value's period (rebuilt)",
     edit(INSIGHT_BUILD, "words += f\" · {self.label('historical, to')} {self.cell(i, 'period_to', cls='date')}\"", "pass"),
     [INSIGHT_BUILD], ["test_in13"]),
    ("S16.6-A5", "the research view leaves out an unmet criterion (rebuilt)",
     edit(INSIGHT_BUILD, "for k in range(len(r[\"criteria_unmet\"])):", "for k in range(0):"),
     [INSIGHT_BUILD], ["test_in13"]),
    ("S16.6-A6", "the HBM page draws a historical supplier without its period (rebuilt)",
     edit(PAGE_BUILD, '            if "valid_to" in assertion:\n                # the period gets its own line',
          '            if False:\n                # the period gets its own line'),
     [PAGE_BUILD, INSIGHT_BUILD], ["a historical supplier drawn without its period, or a period invented"]),
    ("S16.6-A7", "the HBM page's key loses its 'reported' line (rebuilt)",
     edit(PAGE_BUILD, """            ('<rect class="pill named" x="2" y="4" width="32" height="18" rx="9"/>', "reported: no cited claim is a FACT, and one reports what a third party says", " supplier reported"),\n""", ""),
     [PAGE_BUILD, INSIGHT_BUILD], ["a named supplier's basis is missing from the key"]),
    ("S16.6-A8", "the HBM page's evidence panel leaves out the recognition criterion (rebuilt)",
     edit(PAGE_BUILD, """f'{self.label("recognised as reliable:")} {k("third_party_criteria/recognised/met", fmt="met", cls="tag")} · {k("third_party_criteria/recognised/reason")} · '""", "f''"),
     [PAGE_BUILD, INSIGHT_BUILD], ["test_pg2"]),
    ("S16.6-A9", "a third-party citation recorded without its criteria (rebuilt)",
     jedit("data/claims.json", lambda d: claim(d, TRENDFORCE)["citations"][0].pop("third_party_criteria")), ALL,
     ["without its third-party criteria (R-5)"]),
    ("S16.6-A10", "the H100's supplier loses its end date: stale evidence presented as current (rebuilt)",
     jedit("data/relationships.json", lambda d: edge(d, H100_HBM)["supplier"][0].pop("valid_to")), ALL,
     ["supplier = company-sk-hynix: no accepted evidence within 12 months"]),
    ("S16.6-A11", "the H100's historical period moved before its evidence (rebuilt)",
     jedit("data/relationships.json", lambda d: edge(d, H100_HBM)["supplier"][0].update(valid_to="2024-04")), ALL,
     ["historical value whose evidence is not dated from valid_to 2024-04"]),
    ("S16.6-A12", "the source policy loses the criterion 'no conflict of interest' (§7.1)",
     edit("docs/research/source-policy.md", "no conflict of interest", "no obvious bias"), [],
     ["test_third_party_criteria_are_stated"]),
    ("S16.6-C1", "control: the TrendForce claim's statement reworded, everything rebuilt",
     edit("data/claims.json", "It is TrendForce's own assessment; the release names no source for it.",
          "It is TrendForce's own assessment; the release cites no source for it."), ALL, []),
]

S165_BREAKS = s165.breaks


def breaks():
    return [REPLACED_BY_WHAT.get((b[0], b[1]), REPLACED.get(b[0], b)) for b in S165_BREAKS()] + S166


if __name__ == "__main__":
    s15.breaks = breaks
    args = [a for a in sys.argv[2:] if a != "--setup-only"]
    sys.exit(1 if s15.run(Path(sys.argv[1]), set(args), "--setup-only" in sys.argv) else 0)
