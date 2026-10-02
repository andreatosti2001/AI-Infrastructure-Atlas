# SESSION-10 Report — First supply-chain edges

- **Session:** S10 · **Type:** IMPLEMENTATION, with research · **Milestone:** M2 — Canonical Dataset (last session)
- **Date:** 2026-10-02
- **Prompt:** [`sessions/prompts/S10-PROMPT.md`](../prompts/S10-PROMPT.md) (Part A assembled by
  Claude at the end of S09 and confirmed by the human; Part B SPEC §2 detail; H-0 to H-7
  answered before the session). The prompt on `main` is byte-identical to the uploaded copy.
- **Branch:** `claude/new-session-15s0bd`, created from `main` @ `d2e319f` (the PR #16 merge,
  which carries the S10 prompt from PR #15 and a cross-cutting visual-intelligence addition).
- **Base** (D-018 L-03), at the start of the session:
  - `git branch -a`: `claude/new-session-15s0bd` and `main`, with their remotes.
  - `git ls-remote`: `main` and `HEAD` at `d2e319f`; `claude/vigilant-keller-320pbb` at
    `269a1fa` and `claude/new-session-mdyi2x` at `6f926b0` (both merged); `claude/s08-concept-dataset`
    at `41806c5` and `claude/s07-company-dataset` at `a5032ef` (merged); the six older `claude/*`
    branches at `26acdf9`, `ace06f0`, `ce5b881`, `d9d0a83`, `11185a6` and `e23965c`, as S09 listed
    them. The session branch did not yet exist on the remote.

## Mission outcome

**Delivered, smaller than H-1 foresaw; canonical after the human's review.** The Atlas has its
first five relationship records, each resting on claims that meet `relationship-taxonomy.md` §5
for its type, and each navigable from the JSON files:

| Edge | Type | Rests on |
|---|---|---|
| `rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory` | `incorporates` (supplier `not_researched`) | `FACT`, NVIDIA's own architecture page |
| `rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory` | `incorporates` (supplier `not_researched`) | `FACT`, AWS's own architecture page |
| `rel-company-amazon-com-designs-product-amazon-com-trainium2` | `designs` | `FACT`, Amazon's own release ("AWS-designed") |
| `rel-company-sk-hynix-operates-facility-kr-m16` | `operates` | `DERIVATION` from SK hynix's filing (flagged, approved) |
| `rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking` | `requires` (class) | `DERIVATION` from the ECP definition (flagged, approved) |

Together they form the first walkable chain: **3D die stacking ← HBM ← H100, Trainium2**
(`python tools/navigate.py depends-on technology-3d-die-stacking`), with who designs Trainium2,
who operates M16, and an explicit `not_researched` where the HBM maker of each product is not
known.

**Not edges** (each traced from its sentence in `edge-dataset.md` §1): every `supplies` candidate
from the filings (an item with no record, ER-9; a manufacturing service; co-mention), TSMC →
H100 `fabricates` (stale for a `time_sensitive` row; the human chose a gap), NVIDIA `designs`
H100 (ER-2), and every `owns` (no subsidiary record can meet D-057).

| Deliverable | Where | Status |
|---|---|---|
| Edge design: scope and refused candidates, edge ID rule, levels and kinds, time, unknown suppliers, company records, evidence guards and relation words, navigation, review, checks | `docs/architecture/edge-dataset.md` | accepted (D-089 to D-099) |
| Relationship records | `data/relationships.json` (canonical, 5); `data/staging/relationships.json` (empty) | canonical |
| New sources: the H100 page's new bytes; Amazon's 2023 chip release | `data/sources.json` (`src-051`, `src-052`) | source records |
| Claims: 6 new (`FACT` 3, `DERIVATION` 3) | `data/claims.json` | canonical, accepted |
| Edge checks: V-1 to V-10, CE-1, RI-1, PL-1, EP-1, PE-1, RV-1; V-7 and V-8 as warnings | `tests/test_data_relationships.py`, `tests/fixtures/edge_records.json` | in CI |
| VD-2 for edges; F-1 for edges; the trace reads the edge files | `tests/test_data_schema.py`, `tests/test_freshness.py`, `tools/trace.py`, `tests/test_trace.py` | in CI |
| Navigation (the gate, H-5) | `tools/navigate.py`, `tests/test_navigate.py` | tested |

**Roadmap gate, "Graph-like navigation is possible using relational data without introducing a
graph database": met.** `tools/navigate.py` (standard library) answers MA §18's "What depends on
this component?", "Who supplies this component?" and "What evidence supports the edge?", and
"who does what to X", from the JSON files; nothing it computes is stored (RR-5). The roadmap
rule "No relationship is published without evidence or an explicit non-published/unverified
state" holds: every edge cites claims, and an unknown supplier is an explicit state.

**Restated contract** (at the start of the session):

- **Mission:** the first canonical relationship records, each on claims meeting §5 for its type,
  navigable from relational files, so the human can follow at least 10 from source sentence to
  published edge.
- **Non-goals:** Part B §08: no metrics, `depends_on` or scores, no vocabulary or schema change,
  no graph database, DuckDB, UI or runtime, no promotion without the human's verdict.
- **Plan:** inspect and re-retrieve; research candidates against §5; ask the stop-condition
  rulings and RA-4; design document; checks and fixtures first; fail first; sources, claims and
  staging edges with a Verifier pass; navigation; breaks; review; promotion; documents; report.
  The plan held. The edge count did not (Deviation 1).

**Decisions the human took during the session** (verbatim):

| Question | Answer (verbatim) | Effect |
|---|---|---|
| RA-4: re-supply TSMC's 20-F? | "Re-supply it (Recommended)" | the file did not arrive (last row) |
| Stop condition: "HBM requires 3D die stacking" read out of a definition | "Allow, as DERIVATION (Recommended)" | D-091 |
| TSMC → H100 `fabricates` fails F-1 | "Gap until fresh evidence (Recommended)" | D-092: no edge; the derivation staged |
| Which endpoint for "AWS-designed"? | "company-amazon-com, as D-074 (Recommended)" | D-093 |
| Batch verdict (E1 to E3 and the TSMC claim) | "Accept all (Recommended)" | 4 claims and 3 edges promoted |
| Flagged rulings (unticked stay staging) | "E4: SK hynix operates M16 (D-099),E5: HBM requires 3D die stacking (D-091)" | both ticked: both edges and their claims promoted |
| D-089 to D-099 | "Approve all (Recommended)" | all accepted |
| TSMC's 20-F has not arrived | "Close as a gap (Recommended)" | a recorded gap |

One wording slip in a question: the E4 option's description read "在 이천" (a stray character)
where it meant "이천". The edge, the claim and the decision use the correct text.

## Files changed

| File | Change |
|---|---|
| `docs/architecture/edge-dataset.md` | new: the design, with the relation-word table RV-1 reads (§7) |
| `docs/architecture/decisions.md` | D-089 to D-099 appended, accepted at the review |
| `data/sources.json` | 2 new records (`src-051`, `src-052`) |
| `data/claims.json`, `data/staging/claims.json` | 6 claims staged, verified, accepted and moved; staging empty |
| `data/relationships.json`, `data/staging/relationships.json` | new files (H-2); 5 edges staged, then promoted; staging empty |
| `tests/test_data_relationships.py` | new: the edge checks, on real data and on fixtures with 18 planted faults and 2 planted warnings; a document-reference test for `edge-dataset.md` |
| `tests/fixtures/edge_records.json` | new: a fictional edge world over the entity fixtures |
| `tests/test_freshness.py` | F-1 for edges (`time_sensitive` rows and `supplier` assertions) |
| `tests/test_data_schema.py` | VD-2 for the relationship files and the edge fixtures |
| `tools/trace.py`, `tests/test_trace.py` | default files include the relationship files; every real edge traced in CI |
| `tools/navigate.py`, `tests/test_navigate.py` | new: navigation (H-5) |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md`, `docs/agents/contracts.md` | state rows and paths (Editorial) |
| `sessions/reports/SESSION-10-REPORT.md` | this report |

## Data changed

As measured at the final commit (produced by script, L-04):

| Measure | Count |
|---|---|
| source records | 52 (2 new: `company_technical_documentation` 1, `company_press_release` 1; both `automated`) |
| canonical claims | 120: `FACT` 55, `ATTRIBUTION` 30, `DERIVATION` 17, `INTERPRETATION` 17, `IMPLICATION` 1 |
| claims created and accepted in S10 | 6 (`FACT` 3, `DERIVATION` 3), with 5 citations |
| relationships | 5 canonical (`incorporates` 2, `designs` 1, `operates` 1, `requires` 1), 0 staging |
| staging | empty (claims, entities, events, relationships) |
| entity records | unchanged: 8 companies, 4 jurisdictions, 9 technologies, 7 components, 3 products, 2 facilities; 4 events |

**Data model:** no schema changed. The relationship schema accepted in S04 validates every edge.

## Tests run

Python 3.11.15. "Fresh venv" means a virtualenv built from `requirements-test.txt` in the session
scratchpad.

| Command / check | Result |
|---|---|
| **At start**, fresh venv; `pip freeze` sorted vs the pins | installed set = pinned set; OK (221 tests); `tools/validate_repo.py`: `Repository integrity: OK` |
| **Fail-first:** the suite with the S10 checks, fixtures, navigation and design written, before any S10 source, claim, edge or decision | 264 tests, 26 failures, all for missing S10 decisions, claims, sources, edges and edge files (output below). Every fixture test passed: each planted fault was caught on the fictional world |
| Suite with the staged data and the decisions written | OK (264) |
| **Deliberate breaks**, staging run (14 breaks + control) | 14 caught; the control passes |
| **Deliberate breaks**, final run on the canonical data (14 breaks + control) | 14 caught; the control passes. Output below |
| `python -m unittest discover -s tests`, final, fresh venv | OK (264 tests: 221 before, 43 new) |
| `validate-data` (`-p "test_data*.py"`) and `validate-freshness` (`-p "test_freshness.py"`), final | OK, OK |
| `python tools/validate_repo.py`, final | `Repository integrity: OK` |
| `python tools/trace.py` on the 5 canonical edges | exit 0 each; no `MISSING` (output below) |
| `python tools/navigate.py` on the real edges | output below |
| CI | observed on the checkpoint `5b42d20` (run 80): success. Not observed at the commit that adds this report (L-08) |

**What the checks cannot see.** A sentence that names the product and carries a relation word can
still state something else; a `DERIVATION` whose step does not hold passes every check
(`edge-dataset.md` §10). Break 1 shows how thin the guard is: a co-mention edge is caught only by
RV-1. The Verifier's reading and the human's review are the guard.

Not applicable: browser, accessibility, performance.

## Evidence added/retired

**Re-retrievals** (H-4, D-075), 2026-10-02T16:00Z: `src-024` to `src-030`, `src-040`, `src-043`
and `src-046` to `src-049` returned their registered bytes. `src-006`/`src-042` (NVIDIA's Hopper
architecture page) and `src-044` (Micron's HBM page) returned changed bytes; `src-031` (TSMC)
answered HTTP 403 (a Cloudflare challenge page).

**The H100 page is not byte-stable.** Two requests at 16:00Z returned the same new bytes; a third,
at 16:17Z, differed only by an injected monitoring script. The article text is the same. `src-051`
registers the 16:17Z bytes, which are the bytes the Verifier read.

**New sources** (retrieved automatically on 2026-10-02T16:17Z, full hashes registered; texts
outside the repository, RA-4(4)):

| Source | What | Class | Cited by |
|---|---|---|---|
| `src-051` | NVIDIA Hopper Architecture In-Depth, retrieval of 2026-10-02 (earlier bytes: `src-006`, `src-042`) | `company_technical_documentation` | `claim-h100-hbm-stacks` |
| `src-052` | Amazon US Press Center, "AWS Unveils Next Generation AWS-Designed Chips" (2023-11-28) | `company_press_release` | `claim-aws-designed-trainium2` |

**Verifier pass.** All 5 new citations: the anchor was found verbatim (whitespace normalised; HTML
tags and table-cell boundaries read as whitespace) in text extracted from the registered bytes,
the sentence around it was read, and each read's hash equals the registered full hash. The 3
`DERIVATION` claims: every input exists, is canonical and `supported`, and the step is the one its
ruling allows (ER-1 for TSMC; D-091; D-082/D-099). **Anchor re-check** (`source-policy.md` §12) of
the canonical claims on the changed page: `claim-h100-process-name`, `claim-h100-identity` and
`claim-h100-gh100-process-name` are still at their locators in `src-051`'s bytes.

**Access gaps** (SP-7; nothing bypassed, RA-2): `investor.tsmc.com` (HTTP 403 challenge). English
DART's report index did not return its section list, so SK hynix's report was not searched for
named customers in S10.

**Read, not registered:** NVIDIA's H100 product page and Hopper architecture page (TSMC 4N named
for the architecture only); the H100 PCIe product brief (2022; no foundry named); AWS's Trainium
page ("designed for one goal": a purpose, not a designer). Web search was used only to discover
the Amazon release and the H100 brief; the citations are to the company's own hosts.

**Retired:** nothing.

## Decisions made

All appended to `decisions.md` and accepted at the review ("Approve all (Recommended)").

| Decision | Subject | Status |
|---|---|---|
| D-089 | edge scope: five edges; the candidates that fail §5 (H-1) | accepted |
| D-090 | edge ID rule (RI-1) | accepted |
| D-091 | a class edge read out of a definition (the human's ruling) | accepted |
| D-092 | TSMC → H100 a gap until fresh evidence (the human's ruling) | accepted |
| D-093 | "AWS-designed" gives a `designs` edge from `company-amazon-com` (the human's ruling) | accepted |
| D-094 | unknown HBM suppliers are `not_researched` | accepted |
| D-095 | no new company records (H-3) | accepted |
| D-096 | validate-data and validate-freshness for edges | accepted |
| D-097 | navigation from the JSON files (H-5) | accepted |
| D-098 | layout, review and promotion for edges (H-2, H-6) | accepted |
| D-099 | SK hynix `operates` M16 as a `DERIVATION` (flagged) | accepted |

**Rejected alternatives** (in each decision and `edge-dataset.md` §8, §12). The main ones:

- **Edge IDs:** a counter (not recomputable); IDs without type prefixes (a technology and a
  component could collide).
- **Borderline rulings:** the Hopper architecture page as fresh evidence for TSMC → H100 (D-073
  logic); waiting for an AWS record before any `designs` edge; no class edge at all;
  `valid_from: 2021-02` on M16 (construction, not operation).
- **Items:** widening "memory" to HBM, or creating memory and optical-column component records.
- **Navigation:** DuckDB now (S14's, and a new dependency); extending the trace only; a stored
  adjacency list.

## Deviations

1. **Five edges, not 10–12.** H-1 expected about 10–12 and the human focus asked to inspect at
   least 10 "from source to published edge". The evidence supports five. The review covered the
   five edges, the staged TSMC derivation and nine refused candidates, each traced from its
   sentence, so the human inspected 15 relationship decisions end-to-end, but only 5 published
   edges. Acceptance criterion 7 is therefore met for decisions and not for published edges.
2. **No `supplies` edge.** H-1 put "`supplies` from filings" first. Every supplier sentence read is
   company-level with an item the Atlas has no record for ("memory", "semiconductor wafers",
   "optical columns"), or no item at all.
3. **No `fabricates` edge.** H-1 named TSMC → H100 as a `DERIVATION`. It meets §5 that way, but
   F-1, extended to edges as Part B §06 q4 asked, makes the only product-level evidence stale. The
   human chose a gap.
4. **Four rulings were asked at the start**, not at the review: the class edge (a §16 stop
   condition), the F-1 consequence, the AWS endpoint and RA-4. They shaped which records were
   built. The flagged edges were still asked separately at the review.
5. **New test and tool files beyond the prompt's "May modify" list:** `tests/test_navigate.py`,
   `tests/fixtures/edge_records.json` and `tools/navigate.py` are covered by "May create" (tests,
   fixtures, the navigation tool). `tests/test_data_schema.py` is a `test_data_*.py` file. No
   other file outside the lists was edited.
6. **The final run of break 9 first passed for the wrong reason.** On the canonical data, the
   break pointed an edge at a claim that had just been promoted, so CE-1 did not fail; RV-1 and
   PL-1 did. The break was corrected (the edge's own claim is moved back to staging) and re-run:
   CE-1 catches it. The corrected result is the one below.

**Invalidated assumptions.**

- S07's handoff expected `supplies` edges from NVIDIA's supplier paragraph (p.8). ER-9's "exactly
  as broad as the source" and the absence of a memory component make it give none.
- S07's handoff expected `owns` edges from subsidiary lists. D-057 makes a subsidiary record
  impossible from a parent's exhibit.
- The S04 worked example 1 treated TSMC → H100 as an S10 edge. It did not foresee F-1 on edges,
  which a 2025 page cannot pass in October 2026.

## Debt introduced/resolved

**Introduced:**

- TSMC → H100 `fabricates`: a gap until product-level evidence dated within 12 months (D-092).
- `supplies` items with no record (memory, wafers, optical columns): a concept decision is needed
  before any `supplies` edge from the filings read.
- `owns`: needs subsidiary company records with their own identity evidence (D-095).
- The HBM supplier of each product: `not_researched` until every preferred class is searched
  (ER-3).
- The H100 page serves varying bytes: future re-retrievals will register new records each time
  (D-075) unless a decision says how to treat injected scripts.
- The navigation tool prints text only; S11 will need a structured output for a page.
- RV-1 and PL-1 are word guards: they catch the plainest violations, not wrong readings.

**Resolved:**

- `relationship-taxonomy.md` §15: V-1 to V-9 for edges run in CI (V-7, V-8 as warnings), with V-10.
- `claim-model.md` §8 and §16: the search record's coverage of every preferred class is checked
  on the citing edge (fixtures; no real `not_publicly_determinable` yet).
- `company-dataset.md` §14 and `facility-dataset.md` §13: the S10 edge candidates, each ruled.
- D-082: the `operates` question for M16, ruled (D-099).

## Unresolved issues

- **TSMC's 20-F** (RA-4): closed as a gap at the human's request. It may name TSMC's equipment
  suppliers (an ASML → TSMC `supplies` edge).
- **The AWS legal entity:** `src-052` names "Amazon Web Services, Inc." as an Amazon.com, Inc.
  company; no record (D-093, D-095).
- **Inherited:** S01's weekly gate; S05 debt (the class table vs the matrix; SRC-023 not re-read).

## Process lessons

- **Run the freshness rule on candidates before promising them.** F-1 was known to extend to
  edges, but its effect on TSMC → H100 was found only during research. Checking each candidate's
  evidence date against its row first would have set H-1's expectation correctly.
- **Ask stop-condition rulings before building.** Asking the four rulings up front meant no record
  was built and then withdrawn.
- **A break must fail for the reason it names.** Break 9's first canonical run passed on other
  checks; listing the failing tests, not only "caught", exposed it.
- **A break script's helper can be the bug.** The first control run failed because the helper
  wrote a list of `None` over the entity files; the control is what showed it.

## Implications for the next session

S11 — First end-to-end vertical slice ("Build one complete user journey from source → entity →
relationship → visualization → evidence"; gate: "The journey is usable by a person who did not
build the dataset"):

- **Completed work S11 can build on:** 5 canonical edges, the edge checks, `tools/navigate.py`
  and the trace.
- **The journey's first question and the edges it walks:** "What does an AI accelerator's memory
  depend on, and who is known to make it?" It walks
  H100/Trainium2 → `incorporates` → HBM → `requires` → 3D die stacking, shows `supplier:
  not_researched` as a visible gap, and ends at each claim's sentence through the trace.
- **What a page would render:** `navigate.py depends-on technology-3d-die-stacking` (the chain),
  `navigate.py suppliers component-high-bandwidth-memory` (the gaps), and `trace.py <edge ID>`
  (the evidence). Navigation needs a structured (JSON) output for that, which is S11's to add.
- **Open issues:** TSMC (20-F gap; H100 fabrication gap, D-092); the AWS legal entity; `supplies`
  items; subsidiary records; S01's weekly gate; S05 debt.
- **Recommended next decision:** the user journey S11 builds first: the HBM chain above
  (recommended), or a company profile.
- **Files for S11 to read first:** this report; `edge-dataset.md`; `relationship-taxonomy.md` §2,
  §4; MA §19; `claim-model.md` §12.

**Next recommended milestone:** S11 — the HBM dependency chain as the first end-to-end journey,
from source sentence to an editorial visual.

**What M3's audits (S12, S13) should examine first** (H-7):

1. Whether RV-1 and PL-1 are worth keeping as guards, or give false comfort.
2. The edge ID rule's length, and whether the period-collision rule is enough.
3. F-1 on edges: whether a 12-month horizon suits `fabricates` for a product launched in 2022.
4. The ruling that reads necessity out of a definition (D-091), and whether it should become
   an evidence rule.
5. The alias endpoint for AWS (D-074, D-093): activity performed by a subsidiary, recorded on
   the parent.

## M2 completion

**M2 — Canonical Dataset (`SESSION-ROADMAP.md` S07 to S10; D-019 numbering): complete.** The
operational roadmap's week 4 ends "**Milestone M2 complete.**" after S10. Against each session's
gate:

| Session | Gate (`SESSION-ROADMAP.md`) | Met by |
|---|---|---|
| S07 | "Every canonical company record has identity evidence and stable IDs." | 8 companies; ID-1, V-10, CE-1 in CI |
| S08 | "Definitions are sourced and do not collapse technically distinct concepts." | 16 concept records; DEF-1, DEF-2, CI-1 in CI |
| S09 | "Do not conflate headquarters, company ownership, operating control and physical manufacturing location." | 2 facilities; HQ-1; owners and operators are never fields; events and derived status |
| S10 | "Graph-like navigation is possible using relational data without introducing a graph database." | 5 edges; `tools/navigate.py`; edge checks in CI |

**Against MA §22.** By D-019, MA §22's milestones are the portfolio's. The Atlas's M2 delivers
part of the portfolio's M1 ("entity schema, relationship schema, source/claim schema, 10–20
entities across the initial vertical chain"; 33 entity records exist, as measured: 8 companies, 4 jurisdictions, 9 technologies, 7 components, 3 products, 2 facilities) and the data it needs for a
"first dependency graph". It does not deliver MA §22's "working provenance UI" (S11) or the
portfolio M2's "EU AI compute dependency map with reproducible Python/SQL calculations" (S14 to
S15). M2 is complete as the Atlas defines it, and the MA §22 items not yet met are listed here,
not claimed.

**What M2 does not have:** a `supplies` edge, a `fabricates` edge, an `owns` edge, a data centre,
or a TSMC filing read since S07. Those are the gaps a dependency map will show first.

## Review sheet

The sheet as sent to the human (headings demoted one level). For each item: open the source at
the locator, read the whole sentence, and ask **does it state this relation, about this product,
and no more?** `python tools/trace.py <edge ID>` prints every edge with its claims, sources,
locators and anchors.

### Edges (5, staging at the review)

| # | Edge | Claim (type) | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|---|
| E1 | H100 `incorporates` HBM, supplier `not_researched` | `claim-h100-hbm-stacks` (FACT, party) | `src-051` · section 'H100 HBM3 and HBM2e DRAM subsystems', two sentences | "The H100 SXM5 GPU raises the bar considerably by supporting 80 GB (five stacks) of fast HBM3 memory" · "The PCIe H100 provides 80 GB of fast HBM2e" | Is "supporting … five stacks" containment? Both models cited because the record covers both. HBM3 and HBM2e as generations of HBM (taxonomy §12, example 2) |
| E2 | Trainium2 `incorporates` HBM, supplier `not_researched` | `claim-trainium2-hbm-capacity` (FACT, party) | `src-043` · 'Memory' table, header row and the row 'HBM Capacity (GiB)', cells in order | "Trainium Trainium2 Improvement factor HBM Capacity (GiB) 32 96 3x" | Does an HBM capacity state that the chip contains HBM? |
| E3 | Amazon `designs` Trainium2 | `claim-aws-designed-trainium2` (FACT, party, as of 2023-11-28) | `src-052` · first paragraph after 'LAS VEGAS--(BUSINESS WIRE)--' | "Amazon Web Services, Inc. (AWS), an Amazon.com, Inc. company (NASDAQ: AMZN), today announced the next generation of two AWS-designed chip families—AWS Graviton4 and AWS Trainium2" · "Graviton4 and Trainium2 mark the latest innovations in chip design from AWS" | Does "AWS-designed" state design by the firm (ER-2)? The endpoint is the AWS alias of Amazon (D-093) |
| E4 ⚑ | SK hynix `operates` M16 | `claim-sk-hynix-operates-m16` (DERIVATION) | inputs: "경기도 이천시와 충청북도 청주시에 생산공장을 설치ㆍ가동하고 있습니다"; "(3) 생산설비의 변동 2021. 02 이천 신규 공장 M16 준공"; "held a completion ceremony for its new fabrication plant M16" | — | Flagged (D-099): the filing does not list its 이천 plants one by one; no period |
| E5 ⚑ | HBM `requires` 3D die stacking | `claim-hbm-requires-3d-die-stacking` (DERIVATION) | inputs: "HBM is a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with through-silicon vias (TSVs)" with the 3D die stacking and HBM working definitions | — | Flagged (D-091): does the edge, as built, hold? |

### Staged claim with no edge

`claim-tsmc-fabricates-h100` (DERIVATION, ER-1, from "Using the TSMC 4N fabrication process
enables H100 to increase GPU core frequency"): held out of the edges by F-1 (D-092). Accepting it
makes the claim canonical, not an edge.

### Refused candidates (traced from their sentences, `edge-dataset.md` §1)

| Candidate | Sentence | Why not |
|---|---|---|
| SK hynix, Micron `supplies` NVIDIA | "We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung" (`src-024` p.8) | item "memory" has no record (ER-9) |
| TSMC `supplies` NVIDIA | "We utilize foundries, such as … TSMC … to produce our semiconductor wafers" (`src-024` p.8) | a manufacturing service, not supply; company-level |
| Carl Zeiss SMT `supplies` ASML | "Carl Zeiss SMT GmbH is our single supplier, and we are their single customer, of optical columns for lithography systems" (`src-029` p.322) | no item record; no Zeiss record |
| ASML `supplies` TSMC | "we were honored to receive the TSMC Supplier ‘Excellence in Green Manufacturing’ Award" (`src-029` p.173) | no item named |
| ASML `supplies` Micron | Micron in ASML's remuneration reference group (`src-029` p.118) | co-mention |
| NVIDIA `designs` H100 | "our ninth-generation data center GPU designed to deliver …" (`claim-h100-identity`) | a purpose, not a designer (ER-2) |
| Amkor `owns` its subsidiaries | Exhibit 21.1, "List of subsidiaries" (`src-026` p.117) | a subsidiary record would fail D-057 |
| Amazon `owns` AWS | "Amazon Web Services, Inc. (AWS), an Amazon.com, Inc. company" (`src-052`) | group text; stale for `rel:owns` |
| Micron `fabricates` HBM4 36GB 12H | "in high-volume production" (`claim-micron-hbm4-identity`) | production is not stated as wafer fabrication |

## Addendum — human review outcome (2026-10-02)

The review sheet above was sent after the checkpoint (`5b42d20`). The human's answers, verbatim:

- Batch: "Accept all (Recommended)"
- Flagged rulings: "E4: SK hynix operates M16 (D-099),E5: HBM requires 3D die stacking (D-091)"
- Decisions: "Approve all (Recommended)"
- TSMC: "Close as a gap (Recommended)"

**Applied:** the 6 S10 claims accepted and moved to `data/claims.json`, with `review` recording
this report; the 5 edges moved to `data/relationships.json`; D-089 to D-099 accepted;
`edge-dataset.md` accepted; TSMC's 20-F recorded as a gap. Staging is empty.

## Fail-first output

Sorted counts of the failing tests, with the S10 checks, fixtures, navigation and design written and no S10 source, claim, edge or decision:

```
      1 FAIL: test_cited_decisions_exist (decision='D-089')
      1 FAIL: test_cited_decisions_exist (decision='D-090')
      1 FAIL: test_cited_decisions_exist (decision='D-091')
      1 FAIL: test_cited_decisions_exist (decision='D-092')
      1 FAIL: test_cited_decisions_exist (decision='D-093')
      1 FAIL: test_cited_decisions_exist (decision='D-094')
      1 FAIL: test_cited_decisions_exist (decision='D-095')
      1 FAIL: test_cited_decisions_exist (decision='D-096')
      1 FAIL: test_cited_decisions_exist (decision='D-097')
      1 FAIL: test_cited_decisions_exist (decision='D-098')
      1 FAIL: test_cited_ids_exist (ref='claim-aws-designed-trainium2')
      1 FAIL: test_cited_ids_exist (ref='claim-h100-hbm-stacks')
      1 FAIL: test_cited_ids_exist (ref='claim-hbm-requires-3d-die-stacking')
      1 FAIL: test_cited_ids_exist (ref='claim-sk-hynix-operates-m16')
      1 FAIL: test_cited_ids_exist (ref='claim-trainium2-hbm-capacity')
      1 FAIL: test_cited_ids_exist (ref='claim-tsmc-fabricates-h100')
      1 FAIL: test_cited_ids_exist (ref='rel-company-amazon-com-designs-product-amazon-com-trainium2')
      1 FAIL: test_cited_ids_exist (ref='rel-company-sk-hynix-operates-facility-kr-m16')
      1 FAIL: test_cited_ids_exist (ref='rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking')
      1 FAIL: test_cited_ids_exist (ref='rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory')
      1 FAIL: test_cited_ids_exist (ref='rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory')
      1 FAIL: test_cited_ids_exist (ref='src-051')
      1 FAIL: test_cited_ids_exist (ref='src-052')
      2 FAIL: test_edge_files_exist (path='relationships.json')
      1 FAIL: test_s10_gate_edges_exist
      1 Ran 264 tests in 2.137s
      1 FAILED (failures=26)
```

## Deliberate breaks, final run

Run on the canonical data; each break edits a scratch copy of the repository and lists the tests that fail. Break 9 is the corrected run (Deviation 6).

### 1 an edge from co-mention (ASML supplies Micron, from the remuneration reference group): caught
   - test_data_relationships.EdgeDataTests.test_ce1_canonical_edges_rest_on_canonical_records
   - test_data_relationships.EdgeDataTests.test_rv1_relation_words
### 2 fabricates from a process name as a FACT (TSMC fabricates H100, citing claim-h100-process-name): caught
   - test_data_relationships.EdgeDataTests.test_ep1_no_fabricates_from_a_process_name
   - test_freshness.EdgeFreshnessTests.test_f1_real_edges_rest_on_fresh_evidence
### 3 a product edge from a company-level sentence (H100 incorporates HBM, from 'We purchase memory from …'): caught
   - test_data_relationships.EdgeDataTests.test_ce1_canonical_edges_rest_on_canonical_records
   - test_data_relationships.EdgeDataTests.test_pl1_product_edges_name_the_product
### 4 an edge from an announcement (SK hynix operates M16, citing the M15X plan): caught
   - test_freshness.EdgeFreshnessTests.test_f1_real_edges_rest_on_fresh_evidence
   - test_data_relationships.EdgeDataTests.test_pe1_no_edge_from_a_plan
   - test_data_relationships.EdgeDataTests.test_rv1_relation_words
### 5 a placeholder endpoint (H100 incorporates component-unknown-memory): caught
   - test_navigate.RealNavigationTests.test_every_edge_is_navigable
   - test_data_relationships.EdgeDataTests.test_ri1_edge_ids_follow_the_rule
   - test_data_relationships.EdgeDataTests.test_v1_references_resolve
   - test_data_relationships.EdgeDataTests.test_v9_no_placeholder_endpoints
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 6 a stored inverse (Trainium2 designed_by Amazon): caught
   - test_navigate.RealNavigationTests.test_every_edge_is_navigable
   - test_freshness.EdgeFreshnessTests.test_f1_real_edges_rest_on_fresh_evidence
   - test_data_relationships.EdgeDataTests.test_rv1_relation_words
   - test_data_relationships.EdgeDataTests.test_v10_edges_rest_on_allowed_classes_and_standing
   - test_data_relationships.EdgeDataTests.test_v6_no_broader_restated
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 7 a stored depends_on (H100 depends_on 3D die stacking): caught
   - test_navigate.RealNavigationTests.test_every_edge_is_navigable
   - test_freshness.EdgeFreshnessTests.test_f1_real_edges_rest_on_fresh_evidence
   - test_data_relationships.EdgeDataTests.test_pl1_product_edges_name_the_product
   - test_data_relationships.EdgeDataTests.test_rv1_relation_words
   - test_data_relationships.EdgeDataTests.test_v10_edges_rest_on_allowed_classes_and_standing
   - test_data_relationships.EdgeDataTests.test_v6_no_broader_restated
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 8 a class edge with a date (HBM requires 3D die stacking, valid_from 2018): caught
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 9 a canonical edge citing a staging claim: caught
   - test_data_relationships.EdgeDataTests.test_ce1_canonical_edges_rest_on_canonical_records
### 10 an endpoint of the wrong kind (production equipment requires EUV lithography): caught
   - test_data_relationships.EdgeDataTests.test_v2_kind_constraints
### 11 an endpoint of the wrong type (Amazon designs a component class): caught
   - test_data_relationships.EdgeDataTests.test_ri1_edge_ids_follow_the_rule
   - test_data_relationships.EdgeDataTests.test_v2_kind_constraints
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 12 an edge ID that does not follow the rule: caught
   - test_data_relationships.EdgeDocumentReferenceTests.test_cited_ids_exist
   - test_data_relationships.EdgeDataTests.test_ri1_edge_ids_follow_the_rule
### 13 a time-sensitive edge on stale evidence (SK hynix operates M16, from the 2021 release only): caught
   - test_freshness.EdgeFreshnessTests.test_f1_real_edges_rest_on_fresh_evidence
   - test_data_relationships.EdgeDataTests.test_rv1_relation_words
### 14 the same edge twice: caught
   - test_data_relationships.EdgeDataTests.test_ri1_edge_ids_follow_the_rule
   - test_data_relationships.EdgeDataTests.test_v5_no_duplicate_edges
### control CONTROL: every display name changed (must NOT fail): passes, as it must

## Traces of the canonical edges

`python tools/trace.py <edge ID>` for each of the 5 canonical edges, at the final commit.

```
rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory · relationship record · canonical relationships.json
  product-nvidia-h100-tensor-core-gpu incorporates component-high-bandwidth-memory
  /claim_ids:
    claim-h100-hbm-stacks · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-10-REPORT.md)
      statement: NVIDIA states that the H100 SXM5 GPU supports 80 GB (five stacks) of HBM3 memory, and that the PCIe H100 provides 80 GB of HBM2e.
      as of: not_stated
      citation 1 · src-051 · standing party
        source: "NVIDIA Hopper Architecture In-Depth (retrieval of 2026-10-02; earlier bytes: src-006, src-042)" · NVIDIA (NVIDIA Technical Blog) · https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
        class: company_technical_documentation · publisher record: not_researched
        stated dates: published 2022-03-22, modified 2025-07-22
        registered: automated 2026-10-02T16:17Z sha256 6d0f13b0975671d77b406913c54f076a7a26381fcc4c609b7ca93cde4916a347
        locator: section 'H100 HBM3 and HBM2e DRAM subsystems', the sentence beginning 'The H100 SXM5 GPU raises the bar'
        anchor: "The H100 SXM5 GPU raises the bar considerably by supporting 80 GB (five stacks) of fast HBM3 memory"
        read by the Verifier: 2026-10-02T16:17Z sha256 6d0f13b09756 (same bytes as registered)
      citation 2 · src-051 · standing party
        source: "NVIDIA Hopper Architecture In-Depth (retrieval of 2026-10-02; earlier bytes: src-006, src-042)" · NVIDIA (NVIDIA Technical Blog) · https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
        class: company_technical_documentation · publisher record: not_researched
        stated dates: published 2022-03-22, modified 2025-07-22
        registered: automated 2026-10-02T16:17Z sha256 6d0f13b0975671d77b406913c54f076a7a26381fcc4c609b7ca93cde4916a347
        locator: section 'H100 HBM3 and HBM2e DRAM subsystems', the sentence beginning 'The PCIe H100 provides'
        anchor: "The PCIe H100 provides 80 GB of fast HBM2e"
        read by the Verifier: 2026-10-02T16:17Z sha256 6d0f13b09756 (same bytes as registered)
  /supplier: not_researched
exit 0

rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory · relationship record · canonical relationships.json
  product-amazon-com-trainium2 incorporates component-high-bandwidth-memory
  /claim_ids:
    claim-trainium2-hbm-capacity · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-10-REPORT.md)
      statement: AWS's Trainium2 architecture page gives Trainium2 an HBM capacity of 96 GiB, against 32 GiB for the first Trainium.
      as of: not_stated
      citation 1 · src-043 · standing party
        source: "Trainium2 Architecture (retrieval of 2026-10-01; earlier bytes: src-010)" · Amazon Web Services (AWS Neuron documentation) · https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html
        class: company_technical_documentation · publisher record: not_researched
        stated dates: undated
        registered: automated 2026-10-01T20:44Z sha256 746c25212873fd403894481c62b4cd1535b02ebf4f7439ae98b507fe47400cbf
        locator: section 'Trainium2 performance improvements', subsection 'Memory', the table's header row and its row 'HBM Capacity (GiB)'; cells read in order, table-cell boundaries as whitespace
        anchor: "Trainium Trainium2 Improvement factor HBM Capacity (GiB) 32 96 3x"
        read by the Verifier: 2026-10-02T16:00Z sha256 746c25212873 (same bytes as registered)
  /supplier: not_researched
exit 0

rel-company-amazon-com-designs-product-amazon-com-trainium2 · relationship record · canonical relationships.json
  company-amazon-com designs product-amazon-com-trainium2
  /claim_ids:
    claim-aws-designed-trainium2 · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-10-REPORT.md)
      statement: Amazon Web Services, Inc. (AWS), which the release calls an Amazon.com, Inc. company, announced Trainium2 on 2023-11-28 as one of two AWS-designed chip families, and calls Graviton4 and Trainium2 the latest innovations in chip design from AWS.
      as of: 2023-11-28
      citation 1 · src-052 · standing party
        source: "AWS Unveils Next Generation AWS-Designed Chips" · Amazon (US Press Center) · https://press.aboutamazon.com/2023/11/aws-unveils-next-generation-aws-designed-chips
        class: company_press_release · publisher record: not_researched
        stated dates: published 2023-11-28
        registered: automated 2026-10-02T16:17Z sha256 6a6c3fe30012dc67d0a3724e70d781e7021e8d32a3f585d6d946a6aa8e533ef3
        locator: first paragraph after the dateline 'LAS VEGAS--(BUSINESS WIRE)--'
        anchor: "Amazon Web Services, Inc. (AWS), an Amazon.com, Inc. company (NASDAQ: AMZN), today announced the next generation of two AWS-designed chip families—AWS Graviton4 and AWS Trainium2"
        read by the Verifier: 2026-10-02T16:17Z sha256 6a6c3fe30012 (same bytes as registered)
      citation 2 · src-052 · standing party
        source: "AWS Unveils Next Generation AWS-Designed Chips" · Amazon (US Press Center) · https://press.aboutamazon.com/2023/11/aws-unveils-next-generation-aws-designed-chips
        class: company_press_release · publisher record: not_researched
        stated dates: published 2023-11-28
        registered: automated 2026-10-02T16:17Z sha256 6a6c3fe30012dc67d0a3724e70d781e7021e8d32a3f585d6d946a6aa8e533ef3
        locator: first paragraph after the dateline, the sentence beginning 'Graviton4 and Trainium2 mark'
        anchor: "Graviton4 and Trainium2 mark the latest innovations in chip design from AWS"
        read by the Verifier: 2026-10-02T16:17Z sha256 6a6c3fe30012 (same bytes as registered)
exit 0

rel-company-sk-hynix-operates-facility-kr-m16 · relationship record · canonical relationships.json
  company-sk-hynix operates facility-kr-m16
  /claim_ids:
    claim-sk-hynix-operates-m16 · DERIVATION · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-10-REPORT.md)
      statement: SK hynix Inc. operates its plant M16 in 이천 (Icheon).
      reasoning: SK hynix Inc., the entity of its separate financial statements, states that it has installed and operates (설치ㆍ가동) production plants in 경기도 이천시 (claim-sk-hynix-production-plants-icheon-cheongju). Its annual report lists M16 among the changes in its own production facilities, as a new plant (공장) in 이천 completed in 2021-02 (claim-sk-hynix-m16-completed-icheon), and its release calls M16 its new fabrication plant (claim-sk-hynix-m16-fabrication-plant). So M16 is one of SK hynix's production plants in 이천, which SK hynix Inc. states it operates. The step is the Atlas's (D-082, D-099): the filing does not list the 이천 plants one by one, and neither source names an operator other than SK hynix. Ownership is not read from it (설치 is not ownership), and no period is: the 2021-02 completion dates construction, not the start of operation.
      input:
        claim-sk-hynix-production-plants-icheon-cheongju · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
          statement: SK hynix Inc. states that it has installed and operates production plants in 경기도 이천시 (Icheon-si, Gyeonggi-do) and 충청북도 청주시 (Cheongju-si, Chungcheongbuk-do) (the Atlas's translation).
          as of: not_stated
          citation 1 · src-047 · standing party
            source: "Annual Report for fiscal year 2025 (제78기), notes to the separate financial statements, note 1 'Company overview' (English DART)" · SK hynix Inc. · https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=66&offset=3650620&length=2897&dtd=dart4.xsd
            class: company_filing · publisher record: company-sk-hynix
            stated dates: published 2026-03-17
            registered: automated 2026-10-02T12:23Z sha256 5d9519c006af94430a23b38451251cc351987c6d449e7ba55d8de3d27e472c42
            filing copy: regulator_hosted
            locator: notes to the separate financial statements, note 1 'Company overview', the first sentence, its last clause (the clause before it names the head office, and is not used)
            anchor: "경기도 이천시와 충청북도 청주시에 생산공장을 설치ㆍ가동하고 있습니다"
            read by the Verifier: 2026-10-02T12:23Z sha256 5d9519c006af (same bytes as registered)
      input:
        claim-sk-hynix-m16-completed-icheon · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
          statement: SK hynix's annual report lists, among the changes in its production facilities, the completion (준공) of its new plant M16 in 이천 (Icheon) in February 2021 (the Atlas's translation).
          as of: 2021-02
          citation 1 · src-046 · standing party
            source: "Annual Report for fiscal year 2025 (제78기), section I.2 'Company history' (English DART)" · SK hynix Inc. · https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=5&offset=72814&length=24617&dtd=dart4.xsd
            class: company_filing · publisher record: company-sk-hynix
            stated dates: published 2026-03-17
            registered: automated 2026-10-02T12:23Z sha256 da06078ebf59de1cbda03b62a98c05ef35b6bf4b175965cd46d53c74ca8ec2cb
            filing copy: regulator_hosted
            locator: I.2 'Company history', item (3) 생산설비의 변동 (changes in production facilities), the row dated 2021. 02
            anchor: "(3) 생산설비의 변동 2021. 02 이천 신규 공장 M16 준공"
            read by the Verifier: 2026-10-02T12:23Z sha256 da06078ebf59 (same bytes as registered)
      input:
        claim-sk-hynix-m16-fabrication-plant · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
          statement: SK hynix describes M16 as its new fabrication plant, for which it held a completion ceremony.
          as of: not_stated
          citation 1 · src-049 · standing party
            source: "SK hynix Announces the Completion of M16 Plant Construction" · SK hynix Newsroom · https://news.skhynix.com/en/sk-hynix-announces-the-completion-of-m16-plant-construction/
            class: company_press_release · publisher record: not_researched
            stated dates: published 2021-02-01
            registered: automated 2026-10-02T12:23Z sha256 c9eb052b836cb62eafc3487ac4829ea90548300913b5358c235bd8d4ec1b3881
            locator: body, first paragraph, the sentence beginning 'SK hynix Inc. (or ‘the Company’' (its last words, a head-office phrase, are not used)
            anchor: "held a completion ceremony for its new fabrication plant M16"
            read by the Verifier: 2026-10-02T12:23Z sha256 c9eb052b836c (same bytes as registered)
exit 0

rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking · relationship record · canonical relationships.json
  component-high-bandwidth-memory requires technology-3d-die-stacking
  /claim_ids:
    claim-hbm-requires-3d-die-stacking · DERIVATION · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-10-REPORT.md)
      statement: Making any High Bandwidth Memory stack requires 3D die stacking.
      reasoning: The ECP report, a research report and the originator of its definition, defines HBM as a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with TSVs (claim-ecp-hbm-definition); the Atlas's HBM is that stack (claim-atlas-high-bandwidth-memory-working-definition). Stacking active dies and interconnecting them directly, not through the package, is what the Atlas calls 3D die stacking (claim-atlas-3d-die-stacking-working-definition). Since every HBM stack is stacked dies by definition, no HBM stack can be made without 3D die stacking: necessity read out of a definition, not stated in words. ER-1 does not cover this step; the human allowed it for S10 as a DERIVATION (D-091, 2026-10-02: "Allow, as DERIVATION (Recommended)"). The 3D die stacking record covers HBM stacking only in v1, so the edge says nothing about other stacked products.
      input:
        claim-ecp-hbm-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          statement: An ECP milestone report by Sandia describes HBM as a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with through-silicon vias (TSVs).
          as of: not_stated
          citation 1 · src-040 · standing originator
            source: "Milestone M1 Report: HBM2/3 Evaluation on Many-core CPU (ECP Milestone ECP-MT-1000; SAND2018-6370R)" · Sandia National Laboratories, for the DOE Exascale Computing Project (ECP), via OSTI · https://www.osti.gov/servlets/purl/1455354/
            class: research_report · publisher record: not_applicable
            stated dates: published 2018-06-08
            registered: automated 2026-10-01T20:51Z sha256 8a9e0dd19680df611754313dade196f95ca80c945fa3e0dc011c1c63801e8be8
            locator: p.5 (printed p.1), §1 'Introduction', second sentence
            anchor: "HBM is a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with through-silicon vias (TSVs)"
            read by the Verifier: 2026-10-01T20:51Z sha256 8a9e0dd19680 (same bytes as registered)
      input:
        claim-atlas-3d-die-stacking-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
          statement: For the Atlas, 3D die stacking is the process of stacking two or more active dies and interconnecting them directly, not through the package. In v1 it covers HBM stacking only.
          reasoning: HIR's 3D architecture gives the definition; the ECP report gives HBM as a case (DRAM dies stacked and connected by TSVs). The v1 scope (HBM only) is the taxonomy's (entity-taxonomy §5, PKG-05).
          input:
            claim-hir-3d-architecture-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
              statement: The IEEE EPS Heterogeneous Integration Roadmap defines a 3D architecture as two or more active silicon devices stacked and interconnected without the agency of the package.
              as of: not_stated
              citation 1 · src-039 · standing originator
                source: "Heterogeneous Integration Roadmap, 2020 Edition, Chapter 22: Interconnects for 2D and 3D Architectures" · IEEE Electronics Packaging Society (EPS) · https://eps.ieee.org/wp-content/uploads/2025/11/ch22_2D-3D-2020.pdf
                class: research_report · publisher record: not_applicable
                stated dates: published 2020-12
                registered: automated 2026-10-01T20:46Z sha256 80e8ea7385b21ce64c8b072051e67d695e4331c1ca44e0ab7be616d8aae12e16
                locator: p.4 (chapter page 2), §3, item b
                anchor: "A 3D architecture is defined as an architecture where two or more active silicon devices are stacked and interconnected without the agency of the package"
                read by the Verifier: 2026-10-01T20:46Z sha256 80e8ea7385b2 (same bytes as registered)
          input:
            claim-ecp-hbm-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
              (shown above)
      input:
        claim-atlas-high-bandwidth-memory-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          statement: For the Atlas, high Bandwidth Memory (HBM) is a memory component: a stack of DRAM dies, placed vertically and connected directly by through-silicon vias.
          reasoning: The ECP report describes HBM as a DRAM stacking technology. The Atlas records HBM as a component (entity-taxonomy §5, HBM-02), so the working definition names the stack the technology produces; the stacking process itself is the 3D die stacking record. Where the stack sits (TQ-02, in-package) is an S10 edge, not part of the definition.
          input:
            claim-ecp-hbm-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
              (shown above)
exit 0

```

## Navigation on the canonical edges (H-5)

```
$ python tools/navigate.py depends-on technology-3d-die-stacking
What depends on technology-3d-die-stacking (3D die stacking)? Structural edges into it, walked now (not stored, RR-5).
  component-high-bandwidth-memory (High Bandwidth Memory) requires technology-3d-die-stacking (3D die stacking)
    rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking · canonical · class
    evidence: claim-hbm-requires-3d-die-stacking (DERIVATION, supported, canonical)
    product-nvidia-h100-tensor-core-gpu (NVIDIA H100) incorporates component-high-bandwidth-memory (High Bandwidth Memory)
      rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory · canonical · instance · no period in the claims
      evidence: claim-h100-hbm-stacks (FACT, supported, canonical)
    product-amazon-com-trainium2 (AWS Trainium2) incorporates component-high-bandwidth-memory (High Bandwidth Memory)
      rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory · canonical · instance · no period in the claims
      evidence: claim-trainium2-hbm-capacity (FACT, supported, canonical)
exit 0

$ python tools/navigate.py suppliers component-high-bandwidth-memory
Who supplies component-high-bandwidth-memory (High Bandwidth Memory)?
  product level: in product-nvidia-h100-tensor-core-gpu (NVIDIA H100), supplier: not_researched
    rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory · canonical · instance · no period in the claims
    evidence: claim-h100-hbm-stacks (FACT, supported, canonical)
  product level: in product-amazon-com-trainium2 (AWS Trainium2), supplier: not_researched
    rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory · canonical · instance · no period in the claims
    evidence: claim-trainium2-hbm-capacity (FACT, supported, canonical)
exit 0

$ python tools/navigate.py actors product-amazon-com-trainium2
Who does what to product-amazon-com-trainium2 (AWS Trainium2)? Activity edges into it.
  company-amazon-com (Amazon) designs product-amazon-com-trainium2 (AWS Trainium2)
    rel-company-amazon-com-designs-product-amazon-com-trainium2 · canonical · instance · no period in the claims
    evidence: claim-aws-designed-trainium2 (FACT, supported, canonical)
exit 0

$ python tools/navigate.py actors facility-kr-m16
Who does what to facility-kr-m16 (SK hynix M16)? Activity edges into it.
  company-sk-hynix (SK hynix) operates facility-kr-m16 (SK hynix M16)
    rel-company-sk-hynix-operates-facility-kr-m16 · canonical · instance · no period in the claims
    evidence: claim-sk-hynix-operates-m16 (DERIVATION, supported, canonical)
exit 0

$ python tools/navigate.py actors product-nvidia-h100-tensor-core-gpu
Who does what to product-nvidia-h100-tensor-core-gpu (NVIDIA H100)? Activity edges into it.
  no recorded relationship: no activity edge points to product-nvidia-h100-tensor-core-gpu (RR-7)
exit 0

$ python tools/navigate.py edges component-high-bandwidth-memory
Edges at component-high-bandwidth-memory (High Bandwidth Memory).
  component-high-bandwidth-memory (High Bandwidth Memory) incorporated in product-nvidia-h100-tensor-core-gpu (NVIDIA H100) (inverse reading, display only, RR-3)
    rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory · canonical · instance · no period in the claims
    evidence: claim-h100-hbm-stacks (FACT, supported, canonical)
  component-high-bandwidth-memory (High Bandwidth Memory) incorporated in product-amazon-com-trainium2 (AWS Trainium2) (inverse reading, display only, RR-3)
    rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory · canonical · instance · no period in the claims
    evidence: claim-trainium2-hbm-capacity (FACT, supported, canonical)
  component-high-bandwidth-memory (High Bandwidth Memory) requires technology-3d-die-stacking (3D die stacking)
    rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking · canonical · class
    evidence: claim-hbm-requires-3d-die-stacking (DERIVATION, supported, canonical)
exit 0

```
