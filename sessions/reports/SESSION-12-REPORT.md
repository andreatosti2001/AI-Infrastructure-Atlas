# SESSION-12 Report — Data architecture audit

- **Session:** S12 · **Type:** AUDIT · **Milestone:** M3 — Vertical Slice + Audit (second session)
- **Date:** 2026-10-02
- **Prompt:** [`sessions/prompts/S12-PROMPT.md`](../prompts/S12-PROMPT.md) (Part A confirmed by the human
  before the session; Part B SPEC §2 detail; H-1 answered at the end of S11; H-0, H-2, H-3 asked
  here).
- **Branch:** `claude/s12-data-architecture-audit`, created from `main` @ `3f17270` (the PR #21
  merge, which carries S11, PR #20, and the S12 prompt).
- **Base** (D-018 L-03), at the start of the session:
  - `git branch -a`: `main` and `remotes/origin/main`, both at `3f17270`.
  - `git ls-remote`: `main` and `HEAD` at `3f17270`; `claude/vigilant-planck-g998t3` at `aeec137`
    and `claude/new-session-djql6o` at `b741fb7` (both merged); `claude/new-session-15s0bd` at
    `c51cb60`, `claude/vigilant-keller-320pbb` at `269a1fa`, `claude/new-session-mdyi2x` at
    `6f926b0`, `claude/s08-concept-dataset` at `41806c5`, `claude/s07-company-dataset` at
    `a5032ef` (all merged); the six older `claude/*` branches at `26acdf9`, `ace06f0`, `ce5b881`,
    `d9d0a83`, `11185a6` and `e23965c`, as S11 listed them.
- **Commits:** `91f8342` (H-0), `7cf1b01` (the audit), `1f600de` (staging checkpoint), `9ce0929`
  (remediation complete), and the commit that adds this report.

## Mission outcome

**Delivered: the audit, its one blocking finding remediated with the human's rulings, and the
overdue M2 milestone audit.**

- [`docs/architecture/milestone-audits/M2-audit.md`](../../docs/architecture/milestone-audits/M2-audit.md)
  (proposed): Part 1 answers PEF §4's eight questions for S07 to S10, with process findings P-1 to
  P-7; Part 2 rates the roadmap's ten S12 items (normalization 3, duplicate concepts 3, stable IDs 3,
  relationship semantics 3, temporal correctness 2, provenance 3, queryability 2, migration risk 2,
  visual derived from canonical data 3, visual scope, units and time 3); Part 3 answers S10's five
  items, S11's handoff and Part B §06 q1, q2 and q6; Part 4 splits one blocking finding from eleven
  debt items with owners; Part 5 rates each PEF dimension.
- **Blocking finding B-1, remediated** (D-109): the twelve relations the Atlas considered and
  refused were a Markdown table that the page parsed twice and resolved to records by display name.
  They are now records in `data/refused_candidates.json`, with a schema, eight checks (RC-1 to
  RC-8), a scripted migration, a Verifier pass and the human's acceptance. The page reads them and
  shows four as cards grouped by reason, never in the diagram.
- **The principle that separates data from rules** (D-110): values about named records belong in
  `data/`; rules stay in their documents. The four other document tables holding per-record values
  are debt DT-1, due before S14.

**Two findings the human should know first:**

- **The word guards are floors.** A probe adding the refused `NVIDIA designs H100` edge, citing the
  sentence "… designed to deliver …", failed no data check. Only reading refused it (audit S10-1).
- **Every recorded human ruling in S07 to S11 followed Claude's recommendation** (audit P-3). This
  session's rulings did too (below).

**Restated contract** (at the start of the session):

- **Mission:** audit the canonical data model and the S11 page against the roadmap's S12 list, S10's
  five items and S11's handoff; design the candidate records before building; remediate only blocking
  findings, with the human's ruling.
- **Non-goals:** Part B §08: no new sources, claims, edges or entities; no metrics or DuckDB; no S13
  content depth; no new page or component system; no candidate drawn as a line.
- **Plan:** inspect and baseline; ask H-0 and H-3; write the audit and the design; ask H-2 and the
  remediation rulings; checks and fixtures first; migrate to staging; Verifier; the human's review;
  promote; page; breaks; browser QA; documents; report. The plan held.

**Rulings the human took** (verbatim):

| Question (as asked) | Answer | Effect |
|---|---|---|
| Should the nine design rules used to build the HBM memory page become binding for all future pages, before this session audits the page against them? (H-0) | "Rules binding, page unchanged (Recommended)" | D-100 to D-108, `vertical-slice.md`, the Editorial and QA contracts accepted (`91f8342`) |
| … Should this session's audit also cover [the M2 phase]? (H-3) | "One audit covering both (Recommended)" | `M2-audit.md` |
| Where should the 12 relationships the Atlas considered and refused … be stored, now that they become data? (H-2) | "Own file, separate from real links (Recommended)" | D-109 |
| Four more design-document tables hold facts about individual records … Fix them in this session or later? | "Later, before the SQL layer (S14) (Recommended)" | D-110; DT-1 |
| The page quotes one-line rule texts … Should those rules stay in their documents? | "Rules stay in documents (Recommended)" | D-110 |
| Should these twelve refused candidates become official records, with the reasons I assigned? (the review sheet below) | "Approve all" | promotion (`9ce0929`) |

## Files changed

| File | Change |
|---|---|
| `docs/architecture/milestone-audits/M2-audit.md` | new: the M2 and S12 audit (proposed) |
| `docs/quality/audit-history.md` | one row |
| `docs/architecture/decisions.md` | D-100 to D-108 status `accepted` (H-0); D-109, D-110 appended, `proposed` |
| `schemas/refused_candidates.schema.json` | new: the record shape and the reason vocabulary (proposed, D-109) |
| `data/refused_candidates.json`, `data/staging/refused_candidates.json` | new: 12 canonical records; staging empty |
| `tests/test_data_candidates.py`, `tests/fixtures/candidate_records.json` | new: RC-1 to RC-8 on the real files and a fictional world with 15 planted faults and 8 schema faults |
| `tools/build_page.py` | reads the candidate records; the drawn gap and the journey's candidates named by ID; cards grouped by reason; `edge-dataset.md` out of the inputs; the Markdown row parser removed |
| `tools/page_template.html` | card styles; the closing framing sentence of the gaps section (Editorial) |
| `tests/test_page.py` | PG-2 resolves candidate records; PG-5 candidates never in the diagram, each card under each reason; PG-10 by candidate ID; a build refusal for a staging candidate; the Markdown row parser removed |
| `site/hbm-chain/index.html` | rebuilt (283,164 bytes) |
| `docs/architecture/edge-dataset.md` | §1: the twelve rows replaced by a pointer to the records and a note on section marks; the rule stays |
| `docs/architecture/vertical-slice.md` | status `accepted` (H-0); amended for D-109 (§2, §5, §8, the one-home list) |
| `docs/agents/contracts.md`, `docs/agents/roles.md` | Editorial and QA accepted (H-0); paths: the staging candidate file (Extractor; the Verifier's `read`), the audit report (Knowledge Architect) |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows |
| `sessions/reports/SESSION-12-migration/migrate_candidates.py` | the migration script, kept with the report (DT-8) |
| `sessions/reports/SESSION-12-qa/` | browser QA script, results, two screenshots |
| `sessions/reports/SESSION-12-REPORT.md` | this report |

## Data changed

- **New record kind:** 12 refused candidates, canonical (`cand-001` to `cand-012`), migrated from
  `edge-dataset.md` §1 with every value asserted equal to its cell. Each is the Atlas's ruling,
  never a fact about the world and never an edge.
- **No source, claim, entity, event or relationship record was created, edited or moved.**
- As measured at `9ce0929`: 52 source records; 120 canonical claims; 8 companies, 4 jurisdictions,
  9 technologies, 7 components, 3 products, 2 facilities, 4 events; 5 relationships; 12 refused
  candidates; staging empty.

**Review sheet** (as given to the human; the reason codes are the Extractor's reading of each row's
"why not" text):

| Record | Considered and refused | Reasons |
|---|---|---|
| cand-001 | TSMC makes the H100 chips | evidence too old for a time-sensitive link (ruling D-092) |
| cand-002 | SK hynix and Micron supply memory to NVIDIA | the item ("memory") has no record |
| cand-003 | TSMC supplies NVIDIA | wrong type of link (manufacturing, not supply); company-level sentence |
| cand-004 | Carl Zeiss SMT supplies optical columns to ASML | Zeiss has no record; the item has no record |
| cand-005 | ASML supplies TSMC (an award mention) | the sentence doesn't state the link |
| cand-006 | ASML supplies Micron (a pay-benchmark peer list) | the sentence doesn't state the link |
| cand-007 | NVIDIA designs the H100 | the sentence doesn't state the link (says what it is designed *for*) |
| cand-008 | Amazon designs Trainium2 (a second, "custom silicon" sentence) | the sentence doesn't state the link (the link exists from another sentence) |
| cand-009 | Amkor owns its subsidiaries | the subsidiaries have no records |
| cand-010 | Amazon owns Amazon Web Services, Inc. | the sentence doesn't state the link; evidence too old; AWS, Inc. has no record |
| cand-011 | Micron makes the HBM4 36GB 12H wafers | the sentence doesn't state the link; company-level sentence |
| cand-012 | Micron owns or operates the Manassas fab | the sentence doesn't state the link |

## Tests run

Python 3.11.15. "Fresh venv" is a virtualenv built from `requirements-test.txt` in the session
scratchpad; `pip freeze` equalled the pins.

| Command / check | Result |
|---|---|
| **At start** (`3f17270`), fresh venv | OK (291 tests); `Repository integrity: OK`; `build_page.py` rebuild byte-identical |
| After H-0 (`91f8342`) | the page's digest changed (decisions.md is an input; only the digest line differs); rebuilt; OK (291) |
| **Probe** (audit S10-1): the refused `NVIDIA designs H100` edge added in a scratch copy | no `validate-data` or `validate-freshness` test failed; only page tests (layout, PG-7) |
| RV-1 applied to the anchors of the 12 §1 rows (scratch script) | 6 of 12 would pass |
| New candidate checks on fixtures, before any real record | OK (8): clean world clean; each of 15 faults fails with its named message; each of 8 schema faults rejected at its own field |
| Migration fidelity (`migrate_candidates.py`), then 4 planted errors in scratch copies | "12 records; every value equals its §1 cell"; the 4 errors caught (wrong endpoint, changed quote, dropped type, a no-record name a record carries) |
| **Fail-first** for the page: `test_page.py` changed, build unchanged | 22 tests, 19 failures and 4 errors, each naming the Markdown rows or the missing candidate specification (output below) |
| Full suite with staging candidates | 299 tests; only PG-7 and the digest failed (page stale), as expected |
| Scratch copy with candidates promoted | OK (301) |
| **Final** (`9ce0929`), fresh venv | OK (301 tests: 291 before, 10 new); `Repository integrity: OK`; `page: up to date`; two builds byte-identical |
| Migration replayed on the pre-move document (`git show 1f600de:docs/architecture/edge-dataset.md`) | equals the canonical records, except the Verifier's `read` values |
| **Deliberate breaks** (S11's 18 re-run on the rebuilt page; 9 new; 3 controls) | 27 caught, each for its named reason; 3 controls pass (table below) |
| Rename control on the pre-S12 build (`91f8342`) | `build refused: 'TSMC' does not name one record` (now: passes) |
| Browser QA (below) | clean at 1280 px and 375 px |
| **CI** | run 102 on `7cf1b01`: success. Run 103 on `1f600de` (staging checkpoint): failure, as expected (Deviation 1). Run 104 on `9ce0929` (remediation complete): success. Not observed at the commit that adds this report (L-08) |

### Fail-first output (page checks, build unchanged)

```
     17 AssertionError: False is not true : no such home
      1 AssertionError: Lists differ: [... 'data/staging/relationships.json' ...] != [... 'data/staging/refused_candidates.json' ...]
      1 AssertionError: b'<!d[...]' != b'<!d[...]' : the committed page is not the build of the current inputs
      1 ERROR: test_a_journey_candidate_in_staging        (KeyError: 'candidates')
      1 ERROR: test_pg10_the_journey_specification_has_homes (KeyError: 'candidates')
      1 ERROR: test_pg5_candidates_are_cards_never_lines  (KeyError: 'candidates')
      1 ERROR: test_pg5_the_chain_and_its_gaps_are_drawn  (KeyError: 'candidate')
     17 FAIL: test_pg2_every_record_value_equals_its_home (ref='doc:edge-dataset#…', fields Candidate, Type, Why not)
      1 FAIL: test_pg2_derived_values
      1 FAIL: test_pg7_rebuild_is_byte_identical
Ran 22 tests; FAILED (failures=19, errors=4)
```

### Deliberate breaks, final run

Each break edits a fresh scratch copy of the repository; "(rebuilt)" means the page was rebuilt after
the edit. PG-7 also fails whenever the committed page is edited or an input changes without a rebuild.

| # | Break | Caught by (besides PG-7) | Reason given |
|---|---|---|---|
| 1 | a mark with no record behind it | PG-3 | `'company-example-nothing' not found` |
| 2 | a hand-edited label (NVIDIA H100 → H200) | PG-2 | `'NVIDIA H200' != 'NVIDIA H100'` |
| 3 | a supplier gap removed from the diagram | PG-5 | `('supplier-gap', 'rel-product-nvidia-…') not found` |
| 4 | a supplier gap drawn as zero | PG-2, PG-5 | `'0' != 'not researched'`; "a gap drawn as zero" |
| 5 | a staging edge on the page (not rebuilt) | PG-2 (three), PG-3, PG-4 | a staging ID; "no such home" |
| 6 | a DERIVATION drawn as a FACT | PG-4 | `'inferred' not found in {'gap: no edge', 'stated'}` |
| 7 | a changed claim statement, not rebuilt | PG-2, PG-2 derived | the statement differs from its home |
| 8 | an anchor that no longer matches | PG-2 | `'… lowers the bar …' != '… raises the bar …'` |
| 9 | a panel unreachable by keyboard | PG-8 | "a mark unreachable by keyboard" |
| 10 | an evidence panel removed | PG-3, PG-4, PG-9 | no such panel; a fragment with no target |
| 11 | a build that stamps the clock (rebuilt) | PG-7 only | two builds differ |
| 12 | framing that names a record (rebuilt) | PG-6 only | `'SK hynix' matches …` |
| 13 | "none" for a missing relationship | PG-2 derived, PG-5 | `RR-7: never 'none'` |
| 14 | a new edge links the lane to an accelerator (not rebuilt) | PG-5 lane, PG-2 derived, PL-1, the build refusals | "a lane record is linked to an accelerator"; the refusal test for a staging candidate meets the lane refusal first |
| 15 | a script fetched from the network | PG-9 | "<script> on a self-contained page" |
| 16 | a hover-only rule (rebuilt) | PG-8 only | "a hover rule without focus: li.card:hover" |
| 17 | a text colour below WCAG AA (rebuilt) | PG-8 only | `2.19 not greater than or equal to 4.5` |
| 18 | a quoted rule code whose definition is removed | PG-10 | "rule ER-9 is quoted with no definition on the page" |
| 19 | a refused candidate referenced in the diagram | PG-5 cards | "a refused candidate drawn in the diagram" |
| 20 | a card removed from one of its reason groups | PG-5 cards | `['relation_not_stated'] != ['company_level_only', 'relation_not_stated']` |
| 21 | a journey candidate moved to staging (not rebuilt) | PG-10, PG-2, PG-3, PG-5 cards, the staging refusal | `'cand-002' not found`; "not canonical" |
| 22 | a no-record name that is a record's name (ASML) | RC-4 | "no_record 'ASML' names a record (company-asml-holding); use its ID" |
| 23 | an item with no record, its reason dropped | RC-5, PG-5 cards | "the item has no record, but item_has_no_record is not a reason" |
| 24 | a sentence used by an edge and refused (Amazon designs Trainium2) | RC-6 | "claim-aws-designed-trainium2 supports rel-company-amazon-com-designs-…" |
| 25 | a stored status on a candidate (RR-6) | RC-1 | "Additional properties are not allowed ('status' was unexpected)" |
| 26 | a reasoning that quotes a rule with no home | RC-7 | "cand-005: rule ER-99 has no home" |
| 27 | a candidate given an edge's ID | RC-1, PG-10, PG-2, PG-3 | the ID breaks `^cand-[0-9]{3}$`; "refused candidate cand-001 is not canonical" |
| C | control: README edited | — | passes, as it must |
| D | control: `edge-dataset.md` prose edited (no longer a page input) | — | passes, as it must |
| E | control: every company's display name changed, page rebuilt | — | passes, as it must (before S12 the build refused) |

## Browser QA (D-106)

Scratch run: Playwright from the environment (`/opt/node-tools`; S11's `/opt/node22` path no longer
carries it) with the pre-installed Chromium, on the rebuilt page. Script and results:
[`SESSION-12-qa/qa.js`](./SESSION-12-qa/qa.js), [`qa-result.json`](./SESSION-12-qa/qa-result.json).

| Check | 1280 px | 375 px |
|---|---|---|
| Console messages, page errors | none | none |
| Network requests | the page file only (loaded twice by the script) | same |
| Horizontal overflow (`scrollWidth` / `clientWidth`); elements wider than the viewport | 1280 / 1280; none | 375 / 375; none |
| Diagram scale; smallest diagram text | 1.31; 14.4 px | 0.95; 10.5 px |
| Marks reached by Tab; Enter on each lands on its panel | 17 of 17; 17 of 17 | same |
| Disclosure by keyboard; skip link | yes; `#evidence` | same |
| Contrast on every rendered text node | 2,996 nodes; minimum 6.21:1; none below 4.5:1 | same |

**Screenshots:** [`desktop-03-gaps.png`](./SESSION-12-qa/desktop-03-gaps.png),
[`mobile-03-gaps.png`](./SESSION-12-qa/mobile-03-gaps.png): the gaps section with the cards.
**Found and fixed before the final build:** the closing framing still said the reasons were "quoted
from the Atlas's design record" and pointed to "the design record linked above the table"; there is
no table now. The framing was rewritten and a link to the edge design record added above the cards.

## Evidence added/retired

**None added, none retired.** No source was registered and no claim changed. External research:
none (Part B §05).

**The Verifier's pass on the candidates' sentences.** Six registered sources were re-retrieved on
2026-10-02 at 21:18Z to re-read the quoted sentences: `src-024`, `src-025`, `src-028`, `src-029` and
`src-052` returned their registered bytes (the full SHA-256 of `src-024` matches its 12-character
registered prefix). Every quote was found at its locator (PDF page text extracted with `pypdf` 6.19.0
in a separate scratch virtualenv, not a repository dependency); `src-029` p.118 names Micron in a
reference group, as `cand-006`'s locator says. Eight sentences carry the Verifier's `read`.
`src-026` (Amkor's filing): the host returned an empty reply twice; `cand-009` stays `not_re_read`
(SP-7: nothing bypassed).

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-100 to D-108 | the S11 page rules | accepted at the opening (H-0) |
| D-109 | the refused candidates become records (H-1, H-2) | proposed |
| D-110 | values about named records live in data; rules in their documents | proposed |

**Rejected alternatives** (in each decision and the audit): refusals inside `data/relationships.json`
(every edge reader would have to filter them; a stored status breaks RR-6); rule-made candidate IDs
(impossible with unrecorded or plural endpoints); the "why not" text left in §1 (the page would still
parse the table); two-source rows split (an improvement on the row); migrating the other document
tables now (the human chose S14); a rules data file (the human chose documents); showing all twelve
candidates on the page (beyond its question, D-104).

## Deviations

1. **A checkpoint with known failures was pushed** (`1f600de`): the environment's stop hook requires
   every commit to be pushed, and the page cannot build while its candidates are in staging. CI run
   103 failed (locally the same state failed PG-2's digest and PG-7: the page could not be rebuilt). Nothing went to `main`; the next commit restored green
   locally (as S07 Deviation 8).
2. **Files outside the prompt's "May modify" list:** `docs/architecture/vertical-slice.md` and
   `docs/agents/roles.md`. Their status lines were part of H-0's stated change. The content amendment
   to `vertical-slice.md` (§2, §5, §8) was not asked separately: without it the accepted design
   document would describe a Markdown table that no longer exists. It is listed for the human's
   review below.
3. **The migration script lives in `sessions/reports/SESSION-12-migration/`, not `tools/`:** after
   the move it has no input on `HEAD`; it replays from the pre-move commit (debt DT-8's remedy).
4. **Samsung is not an endpoint of `cand-002`,** though Part B §06 named it as an example: the §1
   row names SK hynix and Micron only, and the copy rule forbids improving it. Recorded for S13.
5. **The "why not" texts are stored without Markdown backticks,** as the page already displayed
   them; every other character is the cell's.
6. **Six registered sources were re-retrieved** for the Verifier's pass (Part B §10). No new source
   was registered, and nothing was read for new content.
7. **`tests/test_data_candidates.py` imports `Homes` from `tests/test_page.py`** to read the rule
   homes, rather than adding a fourth table parser (the cross-module import pattern M1 recorded).

**Invalidated assumptions.**

- The prompt expected the §1 candidates to have "endpoints and `item` as IDs where a record exists";
  two rows name two parties or a type pair, so endpoints and types are lists.
- S11's QA script path (`/opt/node22/...`) no longer resolves in this environment.

## Debt introduced/resolved

**Resolved:**

- B-1: the refused candidates live in records with checks; the page no longer parses Markdown
  rows; no record is found from a display name anywhere in the code.
- Two of the three Markdown table parsers (M-4) are gone (`build_page.py`, `test_page.py`).
- `edge-dataset.md` is no longer a page input: a prose edit to it no longer makes the page stale.
- PEF §4's missing M2 audit.

**Introduced:**

- A new record kind and schema to maintain (the cost H-2 named).
- `cand-NNN` IDs are a counter, not rule-made: a check cannot tell a renumbered candidate (DT-3
  covers ID stability).
- Candidate reason codes rest on the Extractor's reading and the human's review; RC-5 checks only
  the structural reasons (no record, freshness type).
- `cand-009`'s sentence is not re-read (access).

**Open, with owners:** the audit's DT-1 to DT-11 (`M2-audit.md` Part 4).

## Unresolved issues

**Human decision required: accept the S12 audit and the two decisions it produced**

- *What we are deciding:* whether the audit's findings, ratings and debt list, and the two new
  project rules, become accepted, or are changed first.
- *What will concretely change if accepted:* in `decisions.md`, D-109 and D-110 change from
  "proposed" to "accepted"; `M2-audit.md` and the candidate schema change from proposed to accepted;
  `audit-history.md` records the outcome. No data, code or page changes. What each fixes:
  - D-109: refused candidates are records in their own file with the eight checks, and the page
    shows them as cards, never as lines;
  - D-110: from now on, any value about a specific record goes into `data/`; rules stay in their
    design documents; the four remaining tables of per-record values must move before S14 (DT-1);
  - the debt list: eleven items, each with an owner and a deadline (for example: date the first
    relationship before relying on the freshness rule for past events, DT-2; an ID-stability check
    before the first export, DT-3);
  - the amendment to `vertical-slice.md` describing the cards (Deviation 2).
- *Why:* S13 starts from this audit; its debt owners and the S12 gate depend on it being accepted.
- *What stays the same:* the records, the page and the checks as they are now.
- *Options:*
  - **A — Accept as written (recommended):** the status lines change; S13 starts from the audit.
  - **B — Accept with named changes:** you name findings, ratings, owners or rules to change; Claude
    edits them before S13.
  - **C — Reject named items:** a rejected decision is reverted (for example, rejecting D-109 would
    return the candidates to a document table and the page to its S11 form).
- *Decision requested:* "Choose A, B or C", naming the items for B or C.
- *Technical reference:* D-109, D-110; `M2-audit.md` Parts 4 and 5; Deviation 2.

**Not asked now:** public deployment (NG-13).

**Inherited, unchanged:** TSMC → H100 `fabricates` (D-092); the HBM supplier of each product
(D-094); the AWS legal entity (D-093, DT-6); `supplies` items with no record; subsidiary records
(D-095); TSMC's 20-F; S01's weekly gate; S05 debt; the S11 new-user test as an independent walk.

## Process lessons

- **A probe beats an argument.** Whether RV-1 gives false comfort was S10's question; one scratch
  edge answered it in a minute.
- **Measure the human's rulings, then change how they are asked.** P-3 found every ruling followed
  the recommendation. This session asked the review with the records laid out and two named for the
  human's own reading; the answer was still "Approve all". S13, a content audit, is where the human's
  own sampling matters most.
- **A pop-up cannot carry a design.** The record design went into the audit and the message; the
  pop-ups asked only outcomes.
- **Checks written first caught a framing slip of Claude's own** in S11; here the screenshot did:
  a sentence pointing to a table that no longer existed.
- **Migrations kept with the report replay.** The script re-ran on the pre-move document from git
  and reproduced the records.

## Implications for the next session

S13 — Content/evidence depth audit ("No scaling until evidence weaknesses are corrected or explicitly
documented"):

- **Completed work:** the M2 and S12 audit; the refused-candidate records with checks; the page
  reading them.
- **Claims and edges that carry the most weight on the page:** `claim-h100-hbm-stacks`,
  `claim-trainium2-hbm-capacity` (the short answer); `claim-hbm-requires-3d-die-stacking` (D-091);
  `claim-tsmc-fabricates-h100` (D-092, the drawn gap); `claim-aws-designed-trainium2` (D-093);
  `claim-sk-hynix-operates-m16` (D-099).
- **Derivations whose steps S13 should challenge:** D-091, D-099, the TSMC claim.
- **Whether the page's annotations remove a caveat:** the short-answer sentence and the lane.
- **Open issues:** DT-1 to DT-11; Samsung (Deviation 4); `cand-009` not re-read; everything inherited.
- **Recommended next decision** (S13's first sampling question): *for each of the five edges and the
  drawn gap, does the quoted anchor, read in its source, state the relation as strongly as the page
  draws it?* Asked so that the human reads at least one before Claude's assessment.
- **Files for S13 to read first:** this report; `docs/architecture/milestone-audits/M2-audit.md`;
  `docs/architecture/vertical-slice.md`.

**Next recommended milestone:** S13 — the content and evidence depth audit, starting from the
question above.

**S12 gate** ("data model passes audit"): **met, subject to the human's acceptance of the audit.**
The one blocking finding is remediated and checked; every other finding is debt with an owner.

## Addendum — the S13 prompt and the merge (2026-10-02)

The human's message after the report, verbatim: "send me the .md file of prompt 13 and then merge
everything to main".

- Claude assembled [`S13-PROMPT.md`](../prompts/S13-PROMPT.md): Part A is S12's operating contract
  with the operational roadmap's week-5 entry for S13, verbatim; Part B elaborates it into SPEC §2's
  18 sections. It carries the unanswered acceptance of this audit as H-0, and asks H-1 (the sample)
  and H-2 (the human's own reading first) at the start of S13. Part A's confirmation is also open.
- The message did not answer the decision request above (accept the S12 audit), so D-109, D-110,
  `M2-audit.md` and the candidate schema stay `proposed` on `main`.
- S12 and the S13 prompt were merged to `main` through a pull request, as for S11 and S12.
