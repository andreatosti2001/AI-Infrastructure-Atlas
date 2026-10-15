"""The full break harness: every deliberate fault the Atlas's checks must catch, and the controls they must pass.

Each break copies the repository (without .git) into SCRATCH_DIR, makes one edit, runs its build steps in the
order results -> HBM page -> research view -> research journeys, runs the full suite, and counts only if the suite fails with every
expected fragment in its output (the fault is caught for the reason it names). A control counts only if the
suite passes. The harness tests the checks, not the evidence (D-150): its full run is for milestone audits; a
change runs the breaks that touch the files it changes, plus its own new breaks.

The harness is built in layers, each loading the one before it and replacing the inherited breaks whose setup
text its own changes removed (see tests/regression/README.md):
    breaks_records_and_page.py, breaks_sql.py, breaks_research_view.py  ->  breaks_metrics.py
    -> breaks_metric_audit.py -> breaks_supplier_freshness.py -> this file (supplier evidence; review records;
    S17's policy layer; S18's policy links; S20's research journeys; S20.5's filter guard; S21's client brief; S21.5's search window; S22's search tool).

Run with a virtualenv built from requirements-test.txt and requirements-analysis.txt, from the repository root
(the runner is tests/regression/runner.py: parallel copies, one summary, selection by measured files, D-177,
D-178):
    python tests/regression/breaks.py SCRATCH_DIR [ID ...] [--jobs N] [--out FILE]
    python tests/regression/breaks.py SCRATCH_DIR --since main        # the breaks a change selects (D-177)
    python tests/regression/breaks.py --changed PATH ... --select-only
    python tests/regression/breaks.py SCRATCH_DIR --setup-only
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("s165_breaks", REPO / "tests/regression/breaks_supplier_freshness.py")
s165 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s165)
s15 = s165.s15
s13 = s15.module("tests/regression/breaks_records_and_page.py")
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
    # S20 (D-195): the H100's tally is 3 of 3 once its recorded gap is left out; the hand edit moves it to 2 of 3
    "S14.5-T1": ("S14.5-T1", "a tally hand-edited on the page (H100: 3 of 3 dated links older -> 2 of 3)",
                 edit(INSIGHT, f'data-derived="age-beyond" data-accelerator="{H100}">3<', f'data-derived="age-beyond" data-accelerator="{H100}">2<'), [],
                 ["test_in3_derived_values_are_recomputed", "test_in8_rebuild_is_byte_identical"]),
    # S20 (D-195): the H100's age tally leaves its recorded gap out, so its denominator is 3, not 4
    "S14.5-T2": ("S14.5-T2", "a tally's denominator removed from its block (the age block)",
                 edit(INSIGHT, f' <span data-label>of</span> <span data-derived="age-dated" data-accelerator="{H100}">3</span></span>', "</span>"), [],
                 ["a tally whose denominator is not in the same block"]),
    "S14.5-L1": ("S14.5-L1", "a label in the headline hand-edited ('What does an' -> 'What does every')",
                 edit(INSIGHT, "<span data-label>What does an</span>", "<span data-label>What does every</span>"), [],
                 ["a label that is not one of the build's labels"]),
    "S15-M8": ("S15-M8", "the page shows a zero supplier kind beside a supplier metric (rebuilt)",
               edit(INSIGHT_BUILD, '("parts_supplier_reported", "with a supplier reported by a third party;"))\n                    if r[column]',
                    '("parts_supplier_reported", "with a supplier reported by a third party;"))\n                    if True'), [INSIGHT_BUILD],
               ["a zero beside a supplier metric reads as 'no suppliers'"]),
    # S17, S18, S20 and S21.5 (D-137): the reference date moved to 2026-10-08, 2026-10-13, 2026-10-14, then 2026-10-15,
    # so the two breaks that move the literal date move it from the current value: the same fault and the same control.
    # From S21.5 (D-208, JR-13) a session that moves the date also runs the later-rule search again: the control moves
    # the "Searched to" date and the search log's window end with it.
    "S15-M3": ("S15-M3", "the reference date moved, results not rebuilt",
               edit("sql/source_age.sql", "DATE '2026-10-15' AS reference_date", "DATE '2027-10-15' AS reference_date"), [],
               ["is not a fresh run of the current inputs"]),
    "S16-C1": ("S16-C1", "control: the reference date moved one day with the later-rule search, everything rebuilt (D-137, D-208)",
               both(edit("sql/source_age.sql", "DATE '2026-10-15' AS reference_date", "DATE '2026-10-16' AS reference_date"),
                    edit("docs/research/change-detection.md", "**Searched to:** 2026-10-15", "**Searched to:** 2026-10-16"),
                    edit("docs/research/search-logs/later-rules/search-log.md", "**Window searched: 2024-12-06 to 2026-10-15**",
                         "**Window searched: 2024-12-06 to 2026-10-16**")), ALL, []),
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

# D-151: the human review record and Gate 0's link check.
REVIEWS = "docs/quality/human-reviews.md"
D151 = [
    ("D151-1", "a review entry's stated claim count changed (62 -> 61)",
     edit(REVIEWS, "- **Reviewer:** the human. **Claims:** 62.", "- **Reviewer:** the human. **Claims:** 61."), [],
     ["states 61 claims; 62 name it"]),
    ("D151-2", "a review entry renamed under the claims that name it",
     edit(REVIEWS, "## First relationships, 2026-10-02", "## First edges, 2026-10-02"), [],
     ["names no entry of docs/quality/human-reviews.md", "link to a missing heading"]),
    ("D151-3", "the review record links to a removed session report",
     edit(REVIEWS, "(`SESSION-PROMPT-SPEC.md` §9)", "([the report](../../sessions/reports/SESSION-07-REPORT.md))"), [],
     ["link to a missing file: ../../sessions/reports/SESSION-07-REPORT.md"]),
    ("D151-4", "a claim's review date no longer the date of its entry (rebuilt)",
     jedit("data/claims.json", lambda d: claim(d, TRENDFORCE)["review"].update(reviewed_on="2026-10-08")), ALL,
     ["is not the date of entry 'third-party-supplier-reports-and-samsung-electronics-2026-10-07'"]),
    ("D151-C1", "control: the review record's review question reworded",
     edit(REVIEWS, "finds the anchor, reads the whole sentence", "finds the anchor, reads the full sentence"), [], []),
]

# D-152: session records never in the public repository.
D152 = [
    ("D152-1", "a session report committed to the public repository",
     lambda root: (root / "sessions/reports").mkdir(parents=True) or (root / "sessions/reports/SESSION-17-REPORT.md").write_text("# S17\n", encoding="utf-8"),
     [], ["session record in the public repository (D-152): sessions/"]),
    ("D152-2", "a session prompt committed beside the documents",
     lambda root: (root / "docs/S17-PROMPT.md").write_text("# S17\n", encoding="utf-8"),
     [], ["session record in the public repository (D-152): docs/S17-PROMPT.md"]),
]

# S17: the policy layer (D-154 to D-164; checks PL-1 to PL-9 in docs/architecture/policy-dataset.md P-10).
POLICIES, EVENTS, POLICY_ROWS = "data/policies.json", "data/events.json", "docs/research/source-policy.md"
RULE_2022, RULE_2023_AC, RULE_2023_SME, RULE_2024 = (f"policy-us-fr-{n}" for n in ("2022-21658", "2023-23055", "2023-23049", "2024-28270"))


def policy(d, pid):
    return next(p for p in d if p["id"] == pid)


def src(d, sid):
    return next(s for s in d if s["id"] == sid)


EFFECTIVE_ROW = ("| `event:effective` | `official_legal_text` | none | `company_filing`, `company_technical_documentation`, "
                 "`company_press_release`, `company_marketing`, `standard_specification`, `government_publication`, ")
S17 = [
    ("S17-1", "a policy record stores a status (PL-1) (rebuilt)",
     jedit(POLICIES, lambda d: policy(d, RULE_2024).update(status="in_force")), ALL,
     ["Additional properties are not allowed ('status' was unexpected)"]),
    ("S17-2", "a policy ID whose code is not its issuing country's (PL-2) (rebuilt)",
     jedit(POLICIES, lambda d: policy(d, RULE_2024).update(id="policy-nl-fr-2024-28270")), ALL,
     ["policy-nl-fr-2024-28270: not policy- plus the code of its issued_in value"]),
    ("S17-3", "a policy issued by a jurisdiction that is not a country record (PL-3, D-154) (rebuilt)",
     jedit(POLICIES, lambda d: policy(d, RULE_2024)["issued_in"][0].update(value="jurisdiction-eu")), ALL,
     ["issued_in jurisdiction-eu is not an existing country jurisdiction"]),
    ("S17-4", "an act that amends itself (PL-4) (rebuilt)",
     jedit(POLICIES, lambda d: policy(d, RULE_2024)["amends"][0].update(value=RULE_2024)), ALL,
     [f"{RULE_2024} amends itself"]),
    ("S17-5", "a policy field resting on the Atlas's own interpretation (PL-5, LA-1) (rebuilt)",
     jedit(POLICIES, lambda d: policy(d, RULE_2024)["measure_kinds"][0].update(claim_ids=["claim-atlas-ai-accelerator-working-definition"])), ALL,
     ["which is not FACT or ATTRIBUTION"]),
    ("S17-6", "a rule relabelled a proposal while its effective dates stay (PL-6) (rebuilt)",
     jedit(POLICIES, lambda d: policy(d, RULE_2022)["instrument_form"][0].update(value="proposed_rule")), ALL,
     ["a proposed rule never takes effect or is repealed"]),
    ("S17-7", "a later effective date resting on a text that is not the act's official text (D-164) (rebuilt)",
     jedit("data/sources.json", lambda d: src(d, "src-059").update(source_class="government_publication")), ALL,
     ["dated 2023-11-17, after src-059", "event-us-fr-2023-23055-effective-2023-11-17: no citation with a class and"]),
    ("S17-8", "a publication date moved after the text that states it (EV-3) (rebuilt)",
     jedit(EVENTS, lambda d: next(e for e in d if e["id"] == "event-us-fr-2023-23049-published-2023-10-25").update(date="2023-10-26")), ALL,
     ["dated 2023-10-26, after src-060"]),
    ("S17-9", "the status tool ignores a repeal (PL-7)",
     edit("tools/policy_status.py", "    if repealed:\n", "    if False:\n"), [],
     ["test_repeal"]),
    ("S17-10", "a press release allowed to date an act (PL-8, D-158)",
     edit(POLICY_ROWS, EFFECTIVE_ROW, EFFECTIVE_ROW.replace("| none | ", "| `government_publication` | ").replace("`government_publication`, ", "", 1)), [],
     ["test_pl8_only_the_official_text_dates_or_repeals_an_act"]),
    ("S17-11", "a relationship with a policy endpoint before S18 (PL-9) (rebuilt)",
     jedit("data/relationships.json", lambda d: edge(d, "rel-company-amazon-com-designs-product-amazon-com-trainium2").update(source_entity=RULE_2024)), ALL,
     ["policy-us-fr-2024-28270"]),
    ("S17-C1", "control: a policy claim's statement reworded, everything rebuilt",
     edit("data/claims.json", "The Code of Federal Regulations states that the EAR are issued by the United States",
          "The Code of Federal Regulations says that the EAR are issued by the United States"), ALL, []),
]

# S18: the policy links (D-165 to D-174; checks PK-1 to PK-7 in docs/architecture/policy-links.md K-9).
HBM_LINK = "rel-policy-us-fr-2024-28270-restricts-component-high-bandwidth-memory"
SME_2022_LINK = "rel-policy-us-fr-2022-21658-restricts-component-semiconductor-manufacturing-equipment"
HBM_ATTR, HBM_MATCH = "claim-bis-rule-2024-28270-controls-hbm-stacks", "claim-bis-rule-2024-28270-hbm-term-match"
RESTRICTS_ROW = "| `rel:restricts` | `official_legal_text` | none | `company_filing`, "


S18 = [
    ("S18-1", "a policy link carrying a date (PK-1, K-4) (rebuilt)",
     jedit("data/relationships.json", lambda d: edge(d, HBM_LINK).update(valid_to="2025-01")), ALL,
     ["False schema does not allow '2025-01'"]),
    ("S18-2", "a policy link from an act relabelled a proposed rule (PK-2) (rebuilt)",
     jedit(POLICIES, lambda d: policy(d, RULE_2024)["instrument_form"][0].update(value="proposed_rule")), ALL,
     [f"{HBM_LINK}: a link from a proposed rule"]),
    ("S18-3", "a policy link's own quote moved to another act's text (PK-3) (rebuilt)",
     jedit("data/claims.json", lambda d: claim(d, HBM_ATTR)["citations"][0].update(source_id="src-060")), ALL,
     [f"{HBM_LINK}: no ATTRIBUTION resting only on its own act's official text"]),
    ("S18-4", "a term match without the record's working definition (PK-3) (rebuilt)",
     jedit("data/claims.json", lambda d: claim(d, HBM_MATCH).update(input_claim_ids=[HBM_ATTR])), ALL,
     [f"{HBM_LINK}: no DERIVATION matching its own act's words"]),
    ("S18-5", "an act's quote that never names the class (PK-4) (rebuilt)",
     jedit("data/claims.json", lambda d: claim(d, HBM_ATTR)["citations"][0].update(anchor="BIS is adding a new ECCN control on memory stacks with a specific memory bandwidth density to ECCN 3A090.c.")), ALL,
     [f"{HBM_LINK}: its own act's anchors never carry component-high-bandwidth-memory's name or an alias"]),
    ("S18-6", "a press release allowed to support a policy link (PK-5)",
     edit(POLICY_ROWS, RESTRICTS_ROW, "| `rel:restricts` | `official_legal_text` | `government_publication` | `company_filing`, "), [],
     ["test_pk5_restricts_rests_on_the_official_text_only"]),
    ("S18-7", "navigation reads a policy link as a dependency (PK-6)",
     edit("tools/navigate.py", 'STRUCTURAL = ("requires", "has_part", "incorporates")', 'STRUCTURAL = ("requires", "has_part", "incorporates", "restricts")'), ALL,
     ["test_pk6_a_policy_link_is_neither_a_dependency_nor_an_activity"]),
    ("S18-8", "navigation drops the no-advice line (PK-6, LA-5)",
     edit("tools/navigate.py", 'NO_ADVICE = "describes the text; does not advise (LA-5)"', 'NO_ADVICE = ""'), ALL,
     ["test_pk6_edges_shows_a_policy_link_with_its_status_text_and_no_advice_line"]),
    ("S18-9", "a policy ID written into the HBM page (PK-6) (rebuilt)",
     edit("tools/page_template.html", "</main>", "<p>policy-us-fr-2024-28270</p></main>"), ALL,
     ["test_pk6_the_page_shows_no_policy_link_or_policy"]),
    ("S18-10", "a threshold refusal pointed at a class (PK-7) (rebuilt)",
     jedit("data/refused_candidates.json", lambda d: cand(d, "cand-021").update(target_entities=["component-high-bandwidth-memory"])), ALL,
     ["cand-021: applies_a_threshold needs a product or company target"]),
    ("S18-C1", "control: a term match's reasoning reworded, everything rebuilt",
     edit("data/claims.json", "The rule's word is the record's alias HBM, applied to stacks.", "The rule's word is the record's alias HBM, used of stacks."), ALL, []),
]

# S20: the research journeys (D-189 to D-197; checks IN-3, IN-12 for C-2 and C-5; JR-1 to JR-12 in tests/test_journeys.py).
S20 = [
    ("S20-1", "the coverage block's gap count loses its reason (C-2, D-194) (rebuilt)",
     edit(INSIGHT_BUILD, "f'{self.gap_reasons(c[\"accelerator_id\"])}</span>'", "'</span>'"), [INSIGHT_BUILD],
     ["a gap counted without its reason"]),
    ("S20-2", "the age tally counts a recorded gap as a dated link again (C-5, D-195) (rebuilt)",
     edit(INSIGHT_BUILD, 'dated = [r for r in aged if r["basis"] != "gap"]', "dated = aged"), [INSIGHT_BUILD],
     ["test_in3_derived_values_are_recomputed"]),
]

JOURNEYS = "tools/build_journeys.py"
JT = "tools/journey_template.html"
NVIDIA_PAGE = "site/companies/company-nvidia/index.html"


def stray_page(root):
    """A page in a journey folder that no record calls for."""
    (root / "site" / "companies" / "company-nobody").mkdir(parents=True)
    (root / "site" / "companies" / "company-nobody" / "index.html").write_text("<!doctype html>", encoding="utf-8")


S20 += [
    ("S20-J1", "a sentence typed into the journey template outside a framing block (JR-1) (rebuilt)",
     edit(JT, "<main>\n${main}", "<main>\n<p>The memory market is concentrated.</p>\n${main}"), [JOURNEYS],
     ["text with no record, label, derived value or framing behind it"]),
    ("S20-J2", "a company's name hand-edited on its page (JR-2)",
     edit(NVIDIA_PAGE, 'data-field="/name">NVIDIA<', 'data-field="/name">Nvidia Corp<'), [],
     ["test_jr2_every_record_value_equals_its_home"]),
    ("S20-J3", "the export page counts one link too many (JR-3) (rebuilt)",
     edit(JOURNEYS, 'self.count(len(self.links), "links")', 'self.count(len(self.links) + 1, "links")'), [JOURNEYS],
     ["a count that differs from the records"]),
    ("S20-J4", "a zero shown as a count on a profile (JR-3) (rebuilt)",
     edit(JOURNEYS, "    def tally(self, n: int, what: str, words: tuple[str, str], none: str, title: str) -> str:\n        if n:", "    def tally(self, n: int, what: str, words: tuple[str, str], none: str, title: str) -> str:\n        if True:"), [JOURNEYS],
     ["a zero shown as a count"]),
    ("S20-J5", "a refusal drawn as 'no recorded relationship' in the matrix (JR-4) (rebuilt)",
     edit(JOURNEYS, 'return ("refused", cand) if cand else ("none", None)', 'return ("none", None)'), [JOURNEYS],
     ["test_jr4_the_matrix_equals_the_records"]),
    ("S20-J6", "a timeline dot drawn twelve units off its date (JR-5) (rebuilt)",
     edit(JOURNEYS, 'cx="{x(first):.2f}"', 'cx="{x(first) + 12:.2f}"'), [JOURNEYS],
     ["test_jr5_the_timeline_draws_every_dated_event_at_its_date"]),
    ("S20-J7", "the no-advice line dropped from the act blocks (JR-6, LA-5) (rebuilt)",
     edit(JOURNEYS, '{self.label(NO_ADVICE, tag="p", cls="no-advice")}</div>', "</div>"), [JOURNEYS],
     ["no no-advice line (LA-5)"]),
    ("S20-J8", "a policy ID written into a company page (JR-6, PK-6)",
     edit(NVIDIA_PAGE, "</main>", "<p>policy-us-fr-2024-28270</p></main>"), [],
     ["a policy ID on a page with no policy view (PK-6)"]),
    ("S20-J9", "statuses derived on another date than the as-of date (JR-7) (rebuilt)",
     edit(JOURNEYS, "self.atlas.on = self.on", 'self.atlas.on = "2023-11-01"'), [JOURNEYS],
     ["test_jr7_statuses_are_derived_on_the_as_of_date"]),
    ("S20-J10", "a refused candidate left off its company's page (JR-8) (rebuilt)",
     edit(JOURNEYS, "cands = [c for c in self.candidates.values() if cid in", "cands = [c for c in list(self.candidates.values())[1:] if cid in"), [JOURNEYS],
     ["candidate: the page and the records differ"]),
    ("S20-J11", "'restricted' in the export page's framing (JR-9) (rebuilt)",
     edit(JT, "It describes what the texts say.", "It describes which items are restricted."), [JOURNEYS],
     ["in the Atlas's own voice"]),
    ("S20-J12", "a script added to the journey template (JR-10) (rebuilt)",
     edit(JT, "</body>", "<script></script></body>"), [JOURNEYS],
     ["<script> on a self-contained page"]),
    ("S20-J13", "sections headed one level too deep (JR-11) (rebuilt)",
     edit(JOURNEYS, 'self.label(title, tag="h2", id=f"{sid}-h")', 'self.label(title, tag="h3", id=f"{sid}-h")'), [JOURNEYS],
     ["a skipped heading level"]),
    ("S20-J14", "a stray page in a journey folder (JR-12)",
     stray_page, [],
     ["a stray file in the journey folders"]),
    ("S20-J15", "the entry page's link dropped from the HBM page (JR-8, D-193) (rebuilt)",
     edit("tools/page_template.html", '<p class="crumbs"><a href="../index.html"><span data-label>All research pages</span></a></p>\n', ""), [PAGE_BUILD, JOURNEYS],
     ["a built page with no link to the entry page (D-193)"]),
    ("S20-JC1", "control: a framing sentence of the journey template reworded, journeys rebuilt",
     edit(JT, "Each item opens its evidence.", "Each item links to its evidence."), [JOURNEYS], []),
    ("S20-JC2", "control: a company identity claim reworded, everything rebuilt",
     edit("data/claims.json", "January 25, 2026 has the exact name", "January 25, 2026 bears the exact name"), ALL, []),
]

# S20.5: the script-free pages are kept; the research view's filter is hidden where :has() is unsupported (D-200; IN-14).
GUARD = "@supports not selector(:has(*)) { fieldset.filter { display: none; } }\n"
S205 = [
    ("S20.5-1", "the filter's guard dropped from the research view's template (IN-14) (rebuilt)",
     edit("tools/insight_template.html", GUARD, ""), [INSIGHT_BUILD],
     ["it must be hidden (D-200)"]),
    ("S20.5-2", "the guard hides another element than the filter (IN-14) (rebuilt)",
     edit("tools/insight_template.html", GUARD, GUARD.replace("fieldset.filter", "fieldset.basis")), [INSIGHT_BUILD],
     ["it must be hidden (D-200)"]),
    ("S20.5-C1", "control: the guard's last declaration written without its semicolon, research view rebuilt",
     edit("tools/insight_template.html", GUARD, GUARD.replace("display: none; }", "display: none }")), [INSIGHT_BUILD], []),
]

# S21: the client brief (client-brief.md; D-202 to D-206; BR-1 to BR-12 in tests/test_brief.py).
BRIEF = "tools/build_brief.py"
BT = "tools/brief_template.html"
BRIEF_PAGE = "site/briefs/accelerator-memory/index.html"


def stray_brief(root):
    """A page in site/briefs/ that the brief's build does not write."""
    (root / "site" / "briefs" / "other").mkdir(parents=True)
    (root / "site" / "briefs" / "other" / "index.html").write_text("<!doctype html>", encoding="utf-8")


S21 = [
    ("S21-1", "a sentence typed into the brief template outside a framing block (BR-1) (rebuilt)",
     edit(BT, "<main>\n${main}", "<main>\n<p>The memory market is concentrated.</p>\n${main}"), [BRIEF],
     ["test_br1_every_text_node_has_a_home", "text with no record, label, derived value or framing behind it"]),
    ("S21-2", "a supplier's name hand-edited in the brief (BR-2)",
     edit(BRIEF_PAGE, 'data-field="/name">SK hynix<', 'data-field="/name">SK Hynix Inc<'), [],
     ["test_br2_every_record_value_equals_its_home"]),
    ("S21-3", "the brief counts one accelerator too many (BR-3) (rebuilt)",
     edit(BRIEF, 'self.count(len(accs), "accelerators")', 'self.count(len(accs) + 1, "accelerators")'), [BRIEF],
     ["a count that differs from the records"]),
    ("S21-4", "a mark of the brief's map hand-edited from stated to inferred (BR-4)",
     edit(BRIEF_PAGE, 'data-target="rel-company-amazon-com-designs-product-amazon-com-trainium2" data-basis="stated"',
          'data-target="rel-company-amazon-com-designs-product-amazon-com-trainium2" data-basis="inferred"'), [],
     ["the brief's map differs from the HBM page's figure"]),
    ("S21-5", "the summary phrases the recorded gap as a link (BR-5) (rebuilt)",
     edit(BRIEF, '            if r["basis"] == "gap":\n                parts.append(', '            if False:\n                parts.append('), [BRIEF],
     ["a gap without its reason"]),
    ("S21-6", "the summary drops a reported supplier's period (BR-5) (rebuilt)",
     edit(BRIEF, 'if r["period_to"] != "not_applicable":', "if False:"), [BRIEF],
     ["a period shown exactly when the row has one"]),
    ("S21-7", "a policy cell hand-edited from named to no record (BR-6)",
     edit(BRIEF_PAGE, 'data-cell="named" data-link="rel-policy', 'data-cell="none" data-link="rel-policy'), [],
     ["test_br6_the_matrix_equals_the_records"]),
    ("S21-8", "statuses derived on another date than the as-of date (BR-6) (rebuilt)",
     edit(BRIEF, 'super().__init__(PAGE, "brief", None, data)', 'super().__init__(PAGE, "brief", None, data)\n        self.atlas.on = "2023-11-01"'), [BRIEF],
     ["test_br6_statuses_are_derived_on_the_as_of_date"]),
    ("S21-9", "the boundary line dropped from the brief's header (BR-7, the Boundary) (rebuilt)",
     edit(BRIEF, """"boundary": f'<p class="boundary" data-boundary data-label>{esc(self.label_text(BOUNDARY))}</p>',""", '"boundary": "",'), [BRIEF],
     ["the boundary line is not in the brief's header"]),
    ("S21-10", "the as-of date and digest moved after the limits, off the first printed page (BR-7, U-5) (rebuilt)",
     edit(BRIEF, "return f'{identity}{self.framing(\"brief-scope\")}{line}{limits}'", "return f'{self.framing(\"brief-scope\")}{line}{limits}{identity}'"), [BRIEF],
     ["they would print after the first page"]),
    ("S21-11", "print hides the out-of-scope list (BR-7, U-5) (rebuilt)",
     edit(BT, "  nav.jump, .crumbs, p.back { display: none; }", "  nav.jump, .crumbs, p.back, .limits { display: none; }"), [BRIEF],
     ["print hides what must travel with the brief"]),
    ("S21-12", "a source dropped from the source appendix (BR-8) (rebuilt)",
     edit(BRIEF, "for sid in sorted(self.sources_shown):", "for sid in sorted(self.sources_shown)[1:]:"), [BRIEF],
     ["the source appendix does not list exactly the sources the shown claims cite"]),
    ("S21-13", "'should' in the brief's framing (BR-9, NG-12) (rebuilt)",
     edit(BT, "It is not a list of things to watch.", "A reader should watch each of these."), [BRIEF],
     ["test_br9_no_forbidden_word_in_the_atlas_voice", "in the Atlas's own voice"]),
    ("S21-14", "a script added to the brief template (BR-10) (rebuilt)",
     edit(BT, "</body>", "<script></script></body>"), [BRIEF],
     ["test_br10_links_resolve_and_nothing_loads", "<script> on a self-contained page"]),
    ("S21-15", "a subsection headed one level too deep (BR-11) (rebuilt)",
     edit(BRIEF, 'self.label("The classes against the acts", tag="h3")', 'self.label("The classes against the acts", tag="h4")'), [BRIEF],
     ["test_br11_document_structure", "a skipped heading level"]),
    ("S21-16", "a stray page in site/briefs/ (BR-12)",
     stray_brief, [],
     ["a stray file in site/briefs/"]),
    ("S21-17", "the entry page's card for the brief loses its link (JR-8, D-206) (rebuilt)",
     edit(JOURNEYS, 'button(BRIEF, "Open the brief")', '""'), [JOURNEYS],
     ["test_jr8_the_entry_page_links_every_page_and_names_the_chainless_classes"]),
    ("S21-18", "the Client Output marked inactive again (D-205)",
     edit("docs/agents/roles.md", "| Client Output | active |", "| Client Output | inactive |"), [],
     ["test_active_roles_are_exactly_the_contracted_roles"]),
    ("S21-C1", "control: a framing sentence of the brief template reworded, brief rebuilt",
     edit(BT, "A printed copy keeps each address in full.", "A printed copy keeps every address in full."), [BRIEF], []),
    ("S21-C2", "control: a working-definition claim reworded, everything rebuilt",
     edit("data/claims.json", "Making any High Bandwidth Memory stack requires 3D die stacking.",
          "Making any High Bandwidth Memory stack needs 3D die stacking."), ALL, []),
]

# S21.5: the Change Detector and the date up to which later texts were searched (D-207, D-208; JR-13, BR-3, BR-7).
CD = "docs/research/change-detection.md"
S215 = [
    ("S21.5-1", "the 'Searched to' date moved past the search log's window, pages not rebuilt (JR-13)",
     edit(CD, "**Searched to:** 2026-10-15", "**Searched to:** 2026-10-16"), [],
     ["the search log's window does not end on the 'Searched to' date"]),
    ("S21.5-2", "the as-of date moved past the searched window, everything rebuilt (JR-13, D-208)",
     edit("sql/source_age.sql", "SELECT DATE '2026-10-15' AS reference_date", "SELECT DATE '2026-10-16' AS reference_date"), ALL,
     ["the as-of date is later than the searched window"]),
    ("S21.5-3", "the export-control page drops the searched-to line (JR-13) (rebuilt)",
     edit(JOURNEYS, """            + f'<p>{self.label("later texts searched for up to:")} {self.derived("searched-to", searched_to())}</p>'\n""", ""), [JOURNEYS],
     ["the export-control page does not show the date up to which later texts were searched"]),
    ("S21.5-4", "the brief's unsearched period reverts to the latest publication date (BR-7) (rebuilt)",
     edit(BRIEF, 'return self.derived("searched-to", build_journeys.searched_to())', "return self.latest()"), [BRIEF],
     ["the unsearched period missing from the first section"]),
    ("S21.5-5", "the Change Detector marked inactive again (D-207)",
     edit("docs/agents/roles.md", "| Change Detector | active |", "| Change Detector | inactive |"), [],
     ["test_active_roles_are_exactly_the_contracted_roles"]),
    ("S21.5-C1", "control: a framing sentence of the journey template reworded, journeys rebuilt",
     edit(JT, "texts published after the search date below were not searched.", "texts published after the search date below were not read."), [JOURNEYS], []),
]

# S22: the later-rule search tool and the widened JR-13 (D-210, D-211; tests/test_later_rule_search.py LS-1 to LS-11).
TOOL = "tools/later_rule_search.py"
LOGS = "docs/research/search-logs/later-rules"


def run_log(first, last, outcome):
    """A run log of the search tool (its window and outcome lines), with the 'Searched to' date moved to its end."""
    def apply(root):
        (root / LOGS / f"run-{first}-to-{last}.md").write_text(
            f"# Later-rule search run: {first} to {last}\n\n**Window searched: {first} to {last}**\n\n**Outcome:** {outcome}.\n",
            encoding="utf-8")
        edit(CD, "**Searched to:** 2026-10-15", f"**Searched to:** {last}")(root)
    return apply


S22 = [
    ("S22-1", "a gap between search windows: a later run starts two days after the last one, the date moved, pages rebuilt (JR-13)",
     run_log("2026-10-17", "2026-10-17", "none found in the searched window"), [JOURNEYS, BRIEF],
     ["a gap in the searched windows"]),
    ("S22-2", "the run ending on the 'Searched to' date is incomplete, the date moved, pages rebuilt (JR-13)",
     run_log("2026-10-16", "2026-10-16", "incomplete: an access gap"), [JOURNEYS, BRIEF],
     ["the only search logs ending on the 'Searched to' date are incomplete"]),
    ("S22-3", "the search tool reports an outcome without its access gaps (LS-3)",
     edit(TOOL, "    if result.gaps:\n", "    if False:\n"), [],
     ["test_ls3_a_refused_request_is_an_access_gap_never_none_found"]),
    ("S22-4", "the search tool ignores a heading naming 15 CFR part 774 (LS-2)",
     edit(TOOL, "        if d.part_774:\n", "        if False:\n"), [],
     ["test_ls2_a_candidate_is_listed_with_its_hash_and_stops_the_date"]),
    ("S22-5", "the search tool calls a changed registered text unchanged (LS-5, CD-5)",
     edit(TOOL, 'verdict = "unchanged" if now == registered_sha else', 'verdict = "unchanged" if True else'), [],
     ["test_ls5_a_changed_registered_text_is_reported"]),
    ("S22-6", "the search tool writes its log anywhere in the repository (LS-9)",
     edit(TOOL, "    if _inside(log, REPO_ROOT) and not _inside(log, LOG_DIR):\n", "    if False:\n"), [],
     ["test_ls9_the_command_line_writes_only_its_log"]),
    ("S22-7", "the search tool reads only the 3A entries of CD-3 (LS-8)",
     edit(TOOL, 'r"\\b3[AB]\\d{3}\\b"', 'r"\\b3A\\d{3}\\b"'), [],
     ["test_ls8_terms_come_from_their_homes"]),
    ("S22-8", "the search tool selects BIS notices by their repeal words (LS-11)",
     edit(TOOL, 'if d.is_bis and d.tag in ("RULE", "PRORULE") and d.bis_words:', "if d.is_bis and d.bis_words:"), [],
     ["test_ls11_repeal_words_select_bis_rules_not_notices"]),
    ("S22-9", "the search tool accepts fewer index results than the count (LS-10)",
     edit(TOOL, '            if len(found) != reply["count"]:\n', "            if False:\n"), [],
     ["test_ls10_fewer_results_than_the_count_is_an_access_gap"]),
    ("S22-10", "the search tool treats an issue the index lists as absent (LS-4)",
     edit(TOOL, "        elif listed == 0:\n", "        elif True:\n"), [],
     ["test_ls4_a_missing_issue_is_a_gap_only_when_the_index_lists_documents"]),
    ("S22-C1", "control: a framing sentence of the search log reworded",
     edit(TOOL, "Times are UTC.", "All times are UTC."), [], []),
]

S165_BREAKS = s165.breaks


def with_journeys(brk):
    """S20 (D-190): a break that rebuilds the results or the HBM page also rebuilds the journey pages, which read
    both; declared in its steps, so selection by measured files still sees the build it runs (D-177)."""
    bid, what, mutate, steps, expected = brk
    if set(steps) & {WH, PAGE_BUILD} and JOURNEYS not in steps:
        steps = [*steps, JOURNEYS]
    return (bid, what, mutate, steps, expected)


def with_brief(brk):
    """S21 (D-203): a break that rebuilds the results, the HBM page or the journeys also rebuilds the brief, which reads
    all three (and their templates); declared in its steps, so selection by measured files still sees it (D-177)."""
    bid, what, mutate, steps, expected = brk
    if set(steps) & {WH, PAGE_BUILD, JOURNEYS} and BRIEF not in steps:
        steps = [*steps, BRIEF]
    return (bid, what, mutate, steps, expected)


def breaks():
    found = [REPLACED_BY_WHAT.get((b[0], b[1]), REPLACED.get(b[0], b)) for b in S165_BREAKS()] + S166 + D151 + D152 + S17 + S18 + S20 + S205 + S21 + S215 + S22
    return [with_brief(with_journeys(b)) for b in found]


def main(argv: list[str]) -> int:
    import argparse
    import os

    spec = importlib.util.spec_from_file_location("runner", REPO / "tests/regression/runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    p = argparse.ArgumentParser(description="The full break harness (tests/regression/README.md).")
    p.add_argument("scratch", nargs="?", type=Path, help="a scratch folder outside the repository")
    p.add_argument("ids", nargs="*", help="break IDs to run (default: every break)")
    p.add_argument("--setup-only", action="store_true", help="check that every edit still applies; run nothing")
    p.add_argument("--jobs", type=int, default=os.cpu_count() or 1, help="breaks run at a time (default: processors)")
    p.add_argument("--out", type=Path, help="also write the lines and the summary to this file")
    p.add_argument("--changed", nargs="+", metavar="PATH", help="run the breaks these changed files select (D-177)")
    p.add_argument("--since", metavar="REV", help="run the breaks the files changed since REV select (D-177)")
    p.add_argument("--select-only", action="store_true", help="with --changed or --since: print the selection, run nothing")
    p.add_argument("--touched", action="store_true", help="print every break's measured files and build steps")
    a = p.parse_args(argv)
    all_breaks = breaks()
    if a.touched:
        for bid, what, files, steps in runner.touched(all_breaks):
            print(f"{bid:10} {', '.join(files)} | steps: {', '.join(steps) or '-'} | {what}")
        return 0
    wanted = set(a.ids)
    if a.changed or a.since:
        changed = list(a.changed or []) + (runner.changed_since(a.since) if a.since else [])
        picked, reasons = runner.select(all_breaks, changed)
        print("\n".join(reasons) or "no break touches the changed files")
        print(f"selected: {len(picked)} IDs: {' '.join(picked)}", flush=True)
        if a.select_only or not picked:
            return 0
        wanted |= set(picked)
    if a.scratch is None:
        p.error("a scratch folder is needed to run breaks")
    if a.scratch.resolve().is_relative_to(REPO):
        p.error("the scratch folder must be outside the repository")
    return 1 if runner.run(all_breaks, a.scratch, wanted, a.setup_only, a.jobs, a.out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
