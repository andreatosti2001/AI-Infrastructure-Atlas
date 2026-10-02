# SESSION-09 Report — Facility dataset

- **Session:** S09 · **Type:** RESEARCH / IMPLEMENTATION · **Milestone:** M2 — Canonical Dataset (third session)
- **Date:** 2026-10-02
- **Prompt:** [`sessions/prompts/S09-PROMPT.md`](../prompts/S09-PROMPT.md) (Part A assembled by
  Claude from the template and confirmed by the human; Part B SPEC §2 detail; H-0 to H-6
  answered before the session). The prompt on `main` is byte-identical to the uploaded copy.
- **Branch:** `claude/new-session-mdyi2x`, created from `main` @ `c20faf4` (the PR #13 merge,
  which carries S08 and this prompt).
- **Base** (D-018 L-03), at the start of the session:
  - `git branch -a`: `claude/new-session-mdyi2x` and `main`, with their remotes.
  - `git ls-remote`: `main` and `claude/new-session-mdyi2x` at `c20faf4`;
    `claude/s08-concept-dataset` at `41806c5` and `claude/s07-company-dataset` at `a5032ef`
    (both merged); the six older `claude/*` branches at `26acdf9`, `ace06f0`, `ce5b881`,
    `d9d0a83`, `11185a6` and `e23965c`, as S08 listed them.

## Mission outcome

**Delivered, smaller than H-1 foresaw; canonical after the human's review.** The Atlas now
has its first physical sites and its first dated records:

- **Facilities:** 2 canonical records, Micron's fab in Manassas, Virginia
  (`facility-us-manassas-virginia`) and SK hynix's M16 (`facility-kr-m16`). Each is placed by a
  sentence about the site, never by a headquarters sentence, and each kind rests on a named
  word in an identity anchor.
- **Events:** a new event schema (accepted at the review) and 4 canonical events: M16's
  completion (`opened`, 2021-02) and three announcements of planned sites (Micron's second
  Idaho fab, SK hynix's M15X, Amkor's Arizona phase 2). A plan is never an occurrence, and a
  planned site gets no facility record.
- **Status:** derived by `tools/facility_status.py`, never stored. M16 reads `opened` from
  2021-02; Manassas reads `no_recorded_opening` (unknown, not "not operating").
- **Ownership and operation:** recorded as claims and marked against
  `relationship-taxonomy.md` §5 for S10. Only one candidate partly meets `operates`. None
  meets `owns`.
- **Not recorded:** ASML's sites (no facility kind fits: a stop condition, closed as a gap
  with a proposal, D-088), TSMC's sites (the 20-F was not re-supplied: closed as a gap), and
  any data centre (none named in the filings read).

| Deliverable | Where | Status |
|---|---|---|
| Facility-dataset design: scope, ID rule, location rule, kind words, ownership/operation evidence, events, status derivation, capacity, checks | `docs/architecture/facility-dataset.md` | proposed (D-078 to D-082, D-085 to D-088); D-083, D-084 accepted |
| Event schema | `schemas/events.schema.json` | accepted (D-083) |
| Event rows in the preference matrix | `docs/research/source-policy.md` §7 | accepted (D-084) |
| Status derivation | `tools/facility_status.py` | tested (ST-1) |
| New sources: three English DART sections of SK hynix's annual report, SK hynix's M16 release, Amkor's Arizona release | `data/sources.json` (`src-046` to `src-050`) | source records |
| Claims: 10 new | `data/claims.json` | canonical, accepted |
| Facilities: Manassas, M16 | `data/facilities.json` | canonical (2) |
| Events: 1 `opened`, 3 `announced` | `data/events.json` | canonical (4) |
| Checks: FI-1, HQ-1, FK-1, CAP-1; EV-1 to EV-4, EI-1; ST-1; VD-2 for events; matrix test reads the event rows | `tests/test_data_entities.py`, `tests/test_data_events.py`, `tests/test_facility_status.py`, `tests/test_data_schema.py`, `tests/test_source_policy.py`, `tests/fixtures/entity_records.json` | in CI |

**Roadmap gate, "temporal facility model": met for the records created.** Status is a
function of dated events (ST-1); a facility's location, kind and identity rest on
accepted claims; owners and operators are not fields (VD-2); a plan cannot be stored as an
occurrence (EV-2, schema); an event cannot be dated after its evidence (EV-3).

**Restated contract** (at the start of the session):

- **Mission:** the first facility records, each placed by a site sentence, and a minimal
  event schema so status is derived; ownership and operation evidence as claims for S10.
- **Non-goals:** Part B §08: no edges, metrics, schema changes to accepted files, runtime,
  or promotion without the human's verdict.
- **Plan:** access probe and re-retrieval; three start-of-session questions; design and
  event schema; checks first; sources, claims and staging records with a Verifier pass;
  breaks; review; promotion; documents; report. The plan held, except that TSMC never
  entered it (Deviation 2).

**Decisions the human took during the session** (verbatim):

| Question | Answer (verbatim) | Effect |
|---|---|---|
| RA-4: re-supply TSMC's 20-F? | "I'll re-supply it (Recommended)" | the file did not arrive during the session (see the last row) |
| May event rows be added to `source-policy.md` §7 (not in the prompt's file list)? | "Add the rows (Recommended)" | four `event:*` rows; the matrix test reads them (D-084) |
| ASML's sites fit no facility kind (§16 stop) | "Gap + proposal (Recommended)" | no ASML facility; the sentence kept as a claim; D-088 proposes a kind |
| Batch A (10 claims) | "Accept all (Recommended)" | all 10 accepted and promoted |
| Which flagged rulings do you approve? (unticked stay open) | "pick your recommendations" | Claude's recommendation was all four: "fab" = `wafer_fab` (D-081); 준공 recorded as `opened` (D-083); a planned site's announcement has the company as subject (D-083); clause-only anchors (D-080). All four approved by that delegation |
| Event schema and event rows | "Approve both (Recommended)" | D-083 and D-084 accepted |
| TSMC's 20-F has not arrived | "Close as a gap (Recommended)" | TSMC's sites are a recorded gap |

## Files changed

| File | Change |
|---|---|
| `docs/architecture/facility-dataset.md` | new: the design, with the tables the tests read (§2 facility terms, §3 excluded words, §4 kind words and basis, §8 capacity markers) |
| `schemas/events.schema.json` | new: the event shape and the four event types (D-083) |
| `docs/research/source-policy.md` | §7: four event rows, the definition of material claim types, the row count; a status line; the "not covered" note and the §16 handoff row (D-084, approved first by the human) |
| `docs/architecture/decisions.md` | D-078 to D-088 appended |
| `data/sources.json` | 5 new records (`src-046` to `src-050`) |
| `data/claims.json` | 10 accepted claims |
| `data/facilities.json`, `data/events.json` and their `data/staging/` copies | new files (H-5); the staging copies are empty after promotion |
| `tools/facility_status.py` | new: the status derivation (D-085) |
| `tools/trace.py` | default files only: reads the facility and event files |
| `tests/test_data_entities.py` | `ENTITY_KINDS` gains facilities; FI-1, HQ-1, FK-1, CAP-1 and their real-data and fixture tests; the document-reference test covers `facility-dataset.md`, facilities and events |
| `tests/test_data_events.py` | new: EV-1 to EV-4, EI-1, on the real events and on fixtures with planted faults |
| `tests/test_facility_status.py` | new: ST-1 |
| `tests/test_data_schema.py` | VD-2 for events; shape tests (no owner, operator or status field; occurrence subjects) |
| `tests/test_source_policy.py` | the matrix test reads event rows from the event schema |
| `tests/fixtures/entity_records.json` | fictional facilities, events, a press release and their tables; 9 entity faults and 9 event faults |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md`, `docs/agents/contracts.md` | state rows and paths (Editorial) |
| `sessions/reports/SESSION-09-REPORT.md` | this report |

`tests/test_freshness.py` needed no edit: it reads `ENTITY_KINDS`, and the only
`time_sensitive` facility row (capacity) has no value in S09.

## Data changed

As measured at the final commit (produced by script, L-04):

| Measure | Count |
|---|---|
| source records | 50 (5 new: `company_filing` 3, `company_press_release` 2; all `automated`) |
| canonical claims | 105: `FACT` 52, `ATTRIBUTION` 26, `DERIVATION` 14, `INTERPRETATION` 12, `IMPLICATION` 1 |
| claims created and accepted in S09 | 10 (`FACT` 5, `ATTRIBUTION` 3, `DERIVATION` 2), with 8 citations |
| staging claims | 9 (unchanged: the S08 claims waiting on D-070 and D-076) |
| facilities | 2 canonical (`wafer_fab` 2), 0 staging |
| events | 4 canonical (`opened` 1, `announced` 3), 0 staging |
| other entity records | unchanged: 8 companies, 4 jurisdictions, 7 components, 4 technologies (5 staging), 3 products |

**Data model:** the entity schema is unchanged. One new schema (events) and four new matrix
rows, both approved by the human.

## Tests run

Python 3.11.15. "Fresh venv" means a virtualenv built from `requirements-test.txt` in the
session scratchpad.

| Command / check | Result |
|---|---|
| **At start**, fresh venv; `pip freeze` sorted vs the pins | installed set = pinned set; OK (190 tests); `tools/validate_repo.py`: `Repository integrity: OK`. System Python: OK (190) |
| **Fail-first:** the suite with the S09 checks, design and event rows written, before any S09 source, claim, record or decision | 221 tests, 36 failures, all for missing S09 decisions, records, files and sources (output below). Every fixture test passed: each planted fault was caught on the fictional world |
| Suite with the staging data written | 12 failures, all for decisions not yet written; then OK (221) |
| **Deliberate breaks**, staging run (13 breaks + control) | 13 caught; the display-name control passes |
| **Deliberate breaks**, final run on the promoted data (13 breaks + control) | 13 caught; the control passes. Output below |
| `python -m unittest discover -s tests`, final, system Python and fresh venv | OK (221 tests: 190 before, 31 new); installed set = pinned set |
| `validate-data` (`-p "test_data*.py"`) and `validate-freshness` (`-p "test_freshness.py"`), final | OK, OK |
| `python tools/validate_repo.py`, final | `Repository integrity: OK` |
| `python tools/trace.py` on the 6 canonical S09 records | exit 0 each; no `MISSING` |
| `python tools/facility_status.py` | M16: `not_yet_opened` on 2020-12-31, `indeterminate` on 2021-02-10, `opened` on 2026-10-02; Manassas: `no_recorded_opening` |
| CI | observed on the checkpoint `21c2ed4` (run 69): success. Not observed at the commit that adds this report (L-08) |

**What the checks cannot see.** A site sentence that silently copies the head-office town
passes HQ-1. A kind word used loosely by a source passes FK-1. The Verifier's reading and
the human's review are the guard (`facility-dataset.md` §3, §4, §10).

Not applicable: browser, accessibility, performance.

## Evidence added/retired

**Re-retrievals** (H-4, D-075), 2026-10-02: `src-024` to `src-030` returned their registered
bytes. `src-031` (TSMC) answered HTTP 403 (a challenge page). No new record was needed for a
changed source.

**New sources** (retrieved automatically on 2026-10-02T12:23Z, full hashes registered; texts
outside the repository, RA-4(4)):

| Source | What | Class | Cited by |
|---|---|---|---|
| `src-046` | SK hynix annual report 2025, I.2 "Company history" (English DART) | `company_filing`, `regulator_hosted` | M16 identity, locality, opened event |
| `src-047` | the same, separate statements note 1 "Company overview" | `company_filing`, `regulator_hosted` | production plants in 이천 and 청주 (location bridge; S10 `operates` candidate) |
| `src-048` | the same, XI.1 "Progress and changes of disclosure information" | `company_filing`, `regulator_hosted` | M15X announcement |
| `src-049` | SK hynix Newsroom press release, M16 completion (2021-02-01) | `company_press_release` | M16 kind ("fabrication plant") |
| `src-050` | Amkor IR press release, Arizona phase 2 (2026-09-08) | `company_press_release` | Amkor announcement |

**Verifier pass.** All 8 new citations: the anchor was found verbatim (whitespace normalised;
HTML tags and table-cell boundaries read as whitespace) in text extracted from the
registered bytes, the sentence around it was read, and each read's hash equals the
registered full hash. Repeat requests to each new URL returned the same bytes.

**Access gaps** (SP-7; nothing bypassed, RA-2): `investor.tsmc.com` and `www.tsmc.com`
(HTTP 403 challenge). English DART dropped many connections (TLS errors, empty replies)
during a scan of all 134 report sections; slower retries read every section.

**Sentences read and not used** (candidates, not records): Micron's properties table
(countries only); Micron's Boise ground-breaking and construction start (no event type),
New York plan, Hiroshima and Taiwan facilities (no JP record; no named Taiwan site); Amkor's
country table, Vietnam Facility (no VN record) and Arizona construction start; SK hynix's
Dalian acquisition (CN, no `acquired` type); ASML's facility paragraphs (p.69 and the
property section).

**Retired:** nothing.

## Decisions made

All appended to `decisions.md`. D-083 and D-084 were accepted at the review; the flagged
rulings inside D-080, D-081 and D-083 were approved; the rest stay `proposed`.

| Decision | Subject | Status |
|---|---|---|
| D-078 | facility scope (H-1): records, plans as events, gaps | proposed |
| D-079 | facility ID rule (FI-1) | proposed |
| D-080 | location from site sentences only (HQ-1) | proposed; clause-only anchors approved |
| D-081 | facility kinds from basis rows and listed words (FK-1) | proposed; "fab" = `wafer_fab` approved |
| D-082 | ownership, operation and production evidence for S10 (H-3) | proposed |
| D-083 | the event schema (H-2) | **accepted** |
| D-084 | event rows in the preference matrix | **accepted** |
| D-085 | status derived by `tools/facility_status.py` | proposed |
| D-086 | capacity and data centres (CAP-1) | proposed |
| D-087 | layout, review and validate-data for facilities and events (H-5, H-6) | proposed |
| D-088 | proposal: a facility kind for equipment manufacturing (not applied) | proposed |

**Rejected alternatives** (in each decision and `facility-dataset.md` §12). The main ones:

- IDs carrying an owner's slug (wrong after a sale) or built from the display name;
- a facility record for a site under construction or announced;
- M16's location from the release's "at headquarter located in Icheon" phrase, or the
  head-office address as the bridge from 이천 to 경기도;
- a stored status, planned date or `announces` field;
- a kind read from a company's role;
- forcing ASML's sites into `wafer_fab`, or changing the schema in S09.

## Deviations

1. **`source-policy.md` and `tests/test_source_policy.py` were modified**, though the
   prompt's file list did not include them. `source-policy.md` §7 and §16 assign the event
   rows to S09; the human approved adding them before any edit (D-084).
2. **No TSMC facility.** H-1 named TSMC's Hsinchu fabs. The human agreed to re-supply the
   20-F, but it did not arrive, and the human closed TSMC as a gap.
3. **No ASML facility.** H-1 named ASML Veldhoven, but no facility kind fits an
   equipment-manufacturing site: a Part B §16 stop condition, answered by the human.
4. **No packaging facility.** H-1 asked for fabs and packaging sites. The packaging
   candidates were Amkor's, and its filing names no site in a recorded jurisdiction; Arizona
   is still under construction (an event).
5. **An `announced` event may have a company subject**, though H-2 said "facility events
   only". It is still about a facility, a planned one, which has no record (ER-8). The human
   approved this ruling.
6. **A new tool file**, `tools/facility_status.py`, beyond the prompt's "May create" list.
   The status derivation needed a home; `tools/` is the Data Auditor's allowed write.
7. **The flagged rulings were approved by delegation.** The human answered "pick your
   recommendations"; Claude's recommendation (all four) is recorded as the outcome.

**Invalidated assumptions.** The prompt (§03, §05) expected the filings' properties sections
to name sites. Micron's and Amkor's give country totals, ASML's sites are equipment
factories, and only one Micron site sentence exists. Several "sites" in the S07 handoff are
plans that have not become sites: Amkor Arizona, Micron Boise and Clay, SK hynix M15X.

## Debt introduced/resolved

**Introduced:**

- TSMC's sites: a gap until the 20-F is supplied (RA-4).
- ASML's sites: a gap until a facility kind is approved (D-088).
- SK hynix's Cheongju plants and M15: need an ISO 3166-2 claim for 충청북도 and a kind
  sentence. Micron's Japan sites need a JP jurisdiction record.
- No `owns` evidence for any facility; `operates` only partly for M16.
- The trace prints events like other records, but not an event's subject or a facility's
  derived status (the prompt allowed only default-file changes).
- D-078 to D-082 and D-085 to D-088 are proposed.

**Resolved:**

- D-022: the event schema exists and is accepted.
- `source-policy.md` §16: the event rows.
- The S07 handoff on facilities and Amkor's Arizona plan (as an event).

## Unresolved issues

- **The human's approval of D-078 to D-082 and D-085 to D-088**, above all D-079 (facility
  IDs), because S10's edges will point to facilities.
- **D-070 and D-076** (from S08) with their 5 staging technology records and 9 claims.
- **The AWS legal entity** (`company-dataset.md` §14), for S10.
- **Inherited:** S01's weekly gate; S05 debt (the class table vs the matrix; SRC-023 not
  re-read).

## Process lessons

- **Ask the file-list question before editing.** The source policy assigned the event rows
  to S09, but the prompt did not list the file. Asking at the start kept the edit inside an
  approval.
- **Locate plans before modelling events.** Three of the four events are announcements of
  sites that do not yet exist. The subject rule for them had to be designed, not assumed.
- **A combined command must not push on failure.** A checkpoint command ran `git push` after
  a failed Gate 0. The gate had already stopped the commit, so only the unchanged branch was
  pushed, but the push belonged inside the chain.
- **Delegated verdicts need the recommendation written down.** "pick your
  recommendations" is only auditable because the recommendation is recorded beside it.

## Implications for the next session

S10 — First supply-chain edges ("Create the first auditable relationships"; human focus:
"inspect at least 10 relationships end-to-end from source to published edge"):

- **Completed work S10 can build on:** 2 canonical facilities and 4 events; the facility,
  event and status checks; the ownership and operation claims, each marked against
  `relationship-taxonomy.md` §5 (`facility-dataset.md` §5).
- **Edge candidates:**
  - `operates`: SK hynix → M16, only as a `DERIVATION` from
    `claim-sk-hynix-production-plants-icheon-cheongju` and `claim-sk-hynix-m16-completed-icheon`;
    S10 decides whether it meets §5. Micron → Manassas fails both `owns` and `operates`.
  - `fabricates`, `packages`, `designs`, `supplies` from the S07 filings and S08 products;
    the S08 "requires"/"part of" statements (HBM and TSVs; 2.5D and the interposer).
  - the relationship rules V-2, V-3 and V-5 to V-8, which arrive with edges.
- **Open issues:** the approvals above; D-070 and D-076; the AWS legal entity; TSMC's 20-F
  (RA-4); S01's weekly gate; S05 debt.
- **Recommended next decision:** the human confirms the facility ID rule (D-079) and the
  remaining S09 decisions before S10, because edges will point to facilities.
- **Files for S10 to read first:** this report; `facility-dataset.md`; `relationship-taxonomy.md`
  §4, §5, §10, §15; `concept-dataset.md`; `company-dataset.md`; D-028 to D-033 and D-078 to
  D-088.

**Next recommended milestone:** S10 — the first auditable `owns`, `operates` and product
edges, each traced from source to edge.

## Addendum — human review outcome (2026-10-02)

The review sheet below was sent as part of the checkpoint report (`21c2ed4`), before the
questions. The human's answers, verbatim:

- Batch A: "Accept all (Recommended)"
- Rulings: "pick your recommendations" (Claude's recommendation: approve all four)
- Event model: "Approve both (Recommended)"
- TSMC: "Close as a gap (Recommended)"

**Applied:** 10 claims accepted and moved to `data/claims.json`, with `review` recording this
report; 2 facilities and 4 events promoted; D-083 and D-084 accepted; the rulings of D-080,
D-081 and D-083 recorded as approved; TSMC recorded as a gap.

## Review sheet

The sheet as sent to the human (headings demoted one level).

### S09 review sheet — batch A (10 staging claims, 2 facilities, 4 events)

For each claim: open the source at the locator, read the whole sentence, and answer **does it
say this, and no more?** Verdict per claim: **accept**, **reject**, or **wording too
strong**. `python tools/trace.py <record or claim ID>` prints any record with its claims,
sources, locators and anchors.

#### `facility-us-manassas-virginia` — Micron Manassas fab · wafer_fab · located_in `jurisdiction-us` · locality “Manassas, Virginia”

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-micron-manassas-fab` | FACT | Micron has a fab in Manassas, Virginia: its 10-K calls it “our fab in Manassas, Virginia”. | src-025 (company_filing) · p.48, Item 2 'Properties', the sentence beginning 'On June 11, 2025, we also entered into a direct funding agreement' | “to expand and modernize our fab in Manassas, Virginia” | The sentence is about a CHIPS funding agreement; only 'our fab in Manassas, Virginia' is used (identity, locality, kind word 'fab'). Ruling: 'fab' gives wafer_fab (asked separately). |
| `claim-micron-manassas-fab-in-us` | DERIVATION | Micron's fab in Manassas, Virginia is in the country with ISO 3166 code US (Virginia, which ISO 3166-2 lists as US-VA). | — | inputs: `claim-micron-manassas-fab`, `claim-iso-3166-2-us-va` (canonical), `claim-iso-3166-1-us` (canonical)<br>reasoning: The site sentence names a US state, not the country (claim-micron-manassas-fab). ISO 3166-2 lists Virginia as US-VA (claim-iso-3166-2-us-va), and an ISO 3166-2 code begins with the alpha-2 code of the country it subdivides (claim-iso-3166-1-us). So the site is in the country coded US. The step is the Atlas's (D-057, D-080); no headquarters or incorporation sentence is an input. | Does the US-VA step hold? No headquarters claim is an input. |

#### `facility-kr-m16` — SK hynix M16 · wafer_fab · located_in `jurisdiction-kr` · locality “이천”

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-sk-hynix-m16-completed-icheon` | FACT | SK hynix's annual report lists, among the changes in its production facilities, the completion (준공) of its new plant M16 in 이천 (Icheon) in February 2021 (the Atlas's translation). | src-046 (company_filing) · I.2 'Company history', item (3) 생산설비의 변동 (changes in production facilities), the row dated 2021. 02 | “(3) 생산설비의 변동 2021. 02 이천 신규 공장 M16 준공” | Korean, a table row under '(3) changes in production facilities'. Is the translation faithful? 준공 = completion of construction; recorded as an opened event (asked separately). |
| `claim-sk-hynix-m16-fabrication-plant` | FACT | SK hynix describes M16 as its new fabrication plant, for which it held a completion ceremony. | src-049 (company_press_release) · body, first paragraph, the sentence beginning 'SK hynix Inc. (or ‘the Company’' (its last words, a head-office phrase, are not used) | “held a completion ceremony for its new fabrication plant M16” | The sentence ends 'at headquarter located in Icheon, Gyeonggi-do, South Korea'; that phrase is not used (R-5). Used for the kind word 'fabrication plant' only. |
| `claim-sk-hynix-m16-in-kr` | DERIVATION | SK hynix's M16 plant is in the country with ISO 3166 code KR (in 이천, which SK hynix places in 경기도, which ISO 3166-2 lists as Gyeonggi-do, KR-41). | — | inputs: `claim-sk-hynix-m16-completed-icheon`, `claim-sk-hynix-production-plants-icheon-cheongju`, `claim-iso-3166-2-kr-41` (canonical), `claim-iso-3166-1-kr` (canonical)<br>reasoning: The filing places M16 in 이천 (claim-sk-hynix-m16-completed-icheon) and the company's production plants in 경기도 이천시 (claim-sk-hynix-production-plants-icheon-cheongju), so the 이천 of the M16 row is 경기도 이천시. ISO 3166-2 lists 경기도 as Gyeonggi-do, KR-41 (claim-iso-3166-2-kr-41); the romanisation is part of this step, as in D-057. An ISO 3166-2 code begins with the alpha-2 code of its country (claim-iso-3166-1-kr). No head-office sentence is an input (D-080). | Does the 이천 → 경기도 이천시 → KR-41 → KR step hold? No head-office claim is an input. |

#### Events

| Event | Type | Subject | Date | Claim |
|---|---|---|---|---|
| `event-kr-m16-opened-2021-02` | opened | `facility-kr-m16` | 2021-02 | `claim-sk-hynix-m16-completed-icheon` |
| `event-sk-hynix-announced-2022-09-06` | announced | `company-sk-hynix` | 2022-09-06 | `claim-sk-hynix-m15x-plan-disclosed` |
| `event-micron-technology-announced-2025-06` | announced | `company-micron-technology` | 2025-06 | `claim-micron-second-idaho-fab-announced` |
| `event-amkor-technology-announced-2026-09-08` | announced | `company-amkor-technology` | 2026-09-08 | `claim-amkor-arizona-phase-2-announced` |

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-sk-hynix-m15x-plan-disclosed` | ATTRIBUTION | SK hynix disclosed on 2022-09-06 its plan to build M15X, an extension fab of M15, from October 2022 on land it had already secured in the Cheongju Technopolis industrial complex (the Atlas's translation). | src-048 (company_filing) · XI.1 'Progress and changes of disclosure information', table 가, the row whose 신고일자 (filing date) is 2022.09.06; cells read in order, table-cell boundaries as whitespace | “2022.09.06 장래사업ㆍ경영 계획 (공정공시) 1. 제목: 생산기반 확충을 위한 투자계획 2. 내용: 2022년 10월부터 청주 테크노폴리스 산업단지 내 기존 확보된 부지에 M15의 확장 팹인 M15X(eXtension)를 건설할 계획입니다” | Korean, a table row (cells read in order). A plan (ER-8): an announced event dated by the disclosure, 2022-09-06. |
| `claim-micron-second-idaho-fab-announced` | ATTRIBUTION | Micron states that in June 2025 it announced plans for a second leading-edge memory manufacturing fab in Idaho. | src-025 (company_filing) · p.47, Item 2 'Properties', the sentence beginning 'In June 2025, in connection with certain amendments' | “In June 2025, in connection with certain amendments to our CHIPS Act agreements, we announced plans for a second leading-edge memory manufacturing fab in Idaho” | A plan (ER-8): an announced event only, never a facility or a state. |
| `claim-amkor-arizona-phase-2-announced` | ATTRIBUTION | Amkor announced on 2026-09-08 phase 2 of its Arizona advanced packaging and test campus. | src-050 (company_press_release) · first paragraph after the dateline 'TEMPE, Ariz.--(BUSINESS WIRE)--Sep. 8, 2026--' | “today announced phase 2 of its Arizona Advanced packaging and test campus” | A plan (ER-8). The release's 'leading provider' and 'first OSAT production site' (ER-5) are not used. |

#### Other staging claims

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-sk-hynix-production-plants-icheon-cheongju` | FACT | SK hynix Inc. states that it has installed and operates production plants in 경기도 이천시 (Icheon-si, Gyeonggi-do) and 충청북도 청주시 (Cheongju-si, Chungcheongbuk-do) (the Atlas's translation). | src-047 (company_filing) · notes to the separate financial statements, note 1 'Company overview', the first sentence, its last clause (the clause before it names the head office, and is not used) | “경기도 이천시와 충청북도 청주시에 생산공장을 설치ㆍ가동하고 있습니다” | Korean. The same sentence names the head office in its first clause; the anchor is only the production-plant clause. Is that a fair extract? Also the S10 operates candidate (partly meets §5). |
| `claim-asml-manufacturing-sites` | FACT | ASML states that all of its manufacturing activities, including subassembly, final assembly and system testing, take place in cleanroom facilities in Veldhoven, Eindhoven, Oirschot (the Netherlands), Berlin (Germany), Wilton, San Diego (US), Pyeongtaek (South Korea), and Linkou and Tainan (Taiwan). | src-029 (company_filing) · p.69, the paragraph on manufacturing, the sentence beginning 'All of our manufacturing activities' | “All of our manufacturing activities, including subassembly, final assembly and system testing, take place in (cleanroom) facilities in Veldhoven, Eindhoven, Oirschot (the Netherlands), Berlin (Germany), Wilton, San Diego (US), Pyeongtaek (South Korea) and Linkou and Tainan (Taiwan)” | Supports no record: ASML's sites have no facility kind (D-088, your 'Gap + proposal'). Kept as evidence for the later session. |

## Fail-first output

Sorted counts of the failing tests, with the S09 checks written and no S09 data, decision or record:

```
      1 FAIL: test_cited_decisions_and_non_goals_exist (test_source_policy.CitationTests.test_cited_decisions_and_non_goals_exist) (ref='D-084')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-078')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-079')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-080')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-081')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-082')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-083')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-084')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-085')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-086')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-087')
      1 FAIL: test_cited_decisions_exist (test_data_entities.DocumentReferenceTests.test_cited_decisions_exist) (decision='D-088')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='claim-asml-manufacturing-sites')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='claim-micron-manassas-fab')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='claim-sk-hynix-m16-completed-icheon')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='claim-sk-hynix-m16-fabrication-plant')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='claim-sk-hynix-production-plants-icheon-cheongju')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='event-amkor-technology-announced-2026-09-08')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='event-kr-m16-opened-2021-02')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='event-micron-technology-announced-2025-06')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='event-sk-hynix-announced-2022-09-06')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='facility-kr-m16')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='facility-us-manassas-virginia')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='src-046')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='src-047')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='src-048')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='src-049')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist) (ref='src-050')
      1 FAIL: test_display_name_does_not_move_a_facility_id (test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_facility_id)
      1 FAIL: test_entity_files_exist (test_data_entities.EntityDataTests.test_entity_files_exist) (kind='facilities')
      2 FAIL: test_event_files_exist (test_data_events.EventDataTests.test_event_files_exist) (path='events.json')
      1 FAIL: test_fi1_facility_ids_follow_the_rule (test_data_entities.EntityDataTests.test_fi1_facility_ids_follow_the_rule)
      1 FAIL: test_fk1_facility_kinds_have_a_basis (test_data_entities.EntityDataTests.test_fk1_facility_kinds_have_a_basis)
      1 FAIL: test_s09_gate_events_exist (test_data_events.EventDataTests.test_s09_gate_events_exist)
      1 FAIL: test_s09_gate_facility_records_exist (test_data_entities.EntityDataTests.test_s09_gate_facility_records_exist)
      1 FAILED (failures=36)
      1 Ran 221 tests in 2.550s
```

## Deliberate breaks, final run

Run on the promoted data; each break edits a scratch copy of the repository and lists the tests that fail.

### 1 a facility located from a headquarters sentence (M16 located_in rests on SK hynix's head-office derivation): caught
   - test_data_entities.EntityDataTests.test_hq1_locations_never_rest_on_headquarters_evidence
### 2 a locality taken from a headquarters sentence (Manassas locality cites Micron's Boise headquarters claim): caught
   - test_data_entities.EntityDataTests.test_hq1_locations_never_rest_on_headquarters_evidence
### 3 an owner stored as a field (M16 owner = company-sk-hynix): caught
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 4 a stored status (Manassas status = operating): caught
   - test_facility_status.RealEventTests.test_no_record_stores_a_status
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 5 a plan recorded as an opened event (Micron's Idaho announcement as opened): caught
   - test_data_events.EventDataTests.test_ei1_event_ids_follow_the_rule
   - test_data_events.EventDataTests.test_ev2_a_plan_is_never_an_occurrence
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid
### 6 a plan recorded as an occurrence of an existing facility (M15X plan as M16 expanded): caught
   - test_data_events.EventDataTests.test_ei1_event_ids_follow_the_rule
   - test_data_events.EventDataTests.test_ev2_a_plan_is_never_an_occurrence
### 7 an event dated after its source's own date (M16 opened 2026-04; src-046 is dated 2026-03-17): caught
   - test_data_events.EventDataTests.test_ei1_event_ids_follow_the_rule
   - test_data_events.EventDataTests.test_ev3_no_event_after_its_source
### 8 a facility ID that changes with a display name (M16 ID rebuilt from 'SK hynix M16'): caught
   - test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_facility_id
   - test_data_events.EventDataTests.test_ev1_references_resolve_and_canonical_rests_on_canonical
   - test_data_entities.EntityDataTests.test_fi1_facility_ids_follow_the_rule
   - test_data_entities.EntityDataTests.test_fk1_facility_kinds_have_a_basis
### 9 a data-centre capacity that is not nameplate IT capacity (Manassas as a data centre, 100 MW from the fab sentence): caught
   - test_data_entities.EntityDataTests.test_cap1_capacity_only_as_nameplate_it_capacity
   - test_data_entities.EntityDataTests.test_fk1_facility_kinds_have_a_basis
### 10 a canonical event citing a staging claim: caught
   - test_data_events.EventDataTests.test_ev1_references_resolve_and_canonical_rests_on_canonical
### 11 an event whose subject is missing (M16 opened, subject facility-kr-m15): caught
   - test_data_events.EventDataTests.test_ei1_event_ids_follow_the_rule
   - test_data_events.EventDataTests.test_ev1_references_resolve_and_canonical_rests_on_canonical
### 12 an announced event citing a FACT (Amkor's announcement cites the M16 completion): caught
   - test_data_events.EventDataTests.test_ev2_a_plan_is_never_an_occurrence
   - test_data_events.EventDataTests.test_ev3_no_event_after_its_source
### 13 a facility kind with no basis (M16 also a packaging facility): caught
   - test_data_entities.EntityDataTests.test_fk1_facility_kinds_have_a_basis
### control CONTROL: every facility display name changed (must NOT fail): passes, as it must

## Traces of the canonical S09 records

`python tools/trace.py <ID>` for each of the 6 canonical records, at the final commit.

```
facility-us-manassas-virginia · facility record · canonical facilities.json
  Micron Manassas fab
  /identity_claim_ids:
    claim-micron-manassas-fab · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      statement: Micron has a fab in Manassas, Virginia: its 10-K calls it “our fab in Manassas, Virginia”.
      as of: not_stated
      citation 1 · src-025 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended August 28, 2025" · Micron Technology, Inc. · https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf
        class: company_filing · publisher record: company-micron-technology
        stated dates: signed 2025-10-03
        registered: automated 2026-10-01T05:33Z sha256 4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9
        filing copy: filer_hosted_not_checked
        locator: p.48, Item 2 'Properties', the sentence beginning 'On June 11, 2025, we also entered into a direct funding agreement'
        anchor: "to expand and modernize our fab in Manassas, Virginia"
        read by the Verifier: 2026-10-02T11:12Z sha256 4b50d54e91da (same bytes as registered)
  /located_in/0/claim_ids: jurisdiction-us
    claim-micron-manassas-fab-in-us · DERIVATION · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      statement: Micron's fab in Manassas, Virginia is in the country with ISO 3166 code US (Virginia, which ISO 3166-2 lists as US-VA).
      reasoning: The site sentence names a US state, not the country (claim-micron-manassas-fab). ISO 3166-2 lists Virginia as US-VA (claim-iso-3166-2-us-va), and an ISO 3166-2 code begins with the alpha-2 code of the country it subdivides (claim-iso-3166-1-us). So the site is in the country coded US. The step is the Atlas's (D-057, D-080); no headquarters or incorporation sentence is an input.
      input:
        claim-micron-manassas-fab · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
          (shown above)
      input:
        claim-iso-3166-2-us-va · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Virginia, of subdivision category 'state', with the code US-VA.
          as of: not_stated
          citation 1 · src-034 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, North Carolina to Wyoming (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 6825089a17a0758f864082577ffe219557c0991199c759f3b02bb1e96731f5b7
            locator: screenshot of the subdivision table, the row for US-VA
            anchor: "state US-VA Virginia"
            read by the Verifier: 2026-10-01T14:26Z sha256 6825089a17a0 (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-032 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 d02a4287f81268386a9f61a3b8d64b96460ca1cdb4b8f4d5e0a61ac4362ecda0
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code US Short name UNITED STATES OF AMERICA"
            read by the Verifier: 2026-10-01T14:30Z sha256 d02a4287f812 (same bytes as registered)
  /locality/0/claim_ids: Manassas, Virginia
    claim-micron-manassas-fab · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      (shown above)
  /nameplate_it_capacity_mw: not_applicable
exit 0

facility-kr-m16 · facility record · canonical facilities.json
  SK hynix M16
  /identity_claim_ids:
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
  /identity_claim_ids:
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
  /located_in/0/claim_ids: jurisdiction-kr
    claim-sk-hynix-m16-in-kr · DERIVATION · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      statement: SK hynix's M16 plant is in the country with ISO 3166 code KR (in 이천, which SK hynix places in 경기도, which ISO 3166-2 lists as Gyeonggi-do, KR-41).
      reasoning: The filing places M16 in 이천 (claim-sk-hynix-m16-completed-icheon) and the company's production plants in 경기도 이천시 (claim-sk-hynix-production-plants-icheon-cheongju), so the 이천 of the M16 row is 경기도 이천시. ISO 3166-2 lists 경기도 as Gyeonggi-do, KR-41 (claim-iso-3166-2-kr-41); the romanisation is part of this step, as in D-057. An ISO 3166-2 code begins with the alpha-2 code of its country (claim-iso-3166-1-kr). No head-office sentence is an input (D-080).
      input:
        claim-sk-hynix-m16-completed-icheon · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
          (shown above)
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
        claim-iso-3166-2-kr-41 · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Gyeonggi-do, of subdivision category 'province', with the code KR-41.
          as of: not_stated
          citation 1 · src-037 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for KR, subdivision table (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:KR
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 e81ab0ff68a4abb36414a2be4381d9e23836651e58a893abe37afd2aeca97fa8
            locator: screenshot of the subdivision table, the row for KR-41
            anchor: "province KR-41 Gyeonggi-do Gyeonggi"
            read by the Verifier: 2026-10-01T14:26Z sha256 e81ab0ff68a4 (same bytes as registered)
      input:
        claim-iso-3166-1-kr · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code KR to the entry with the short name “KOREA, REPUBLIC OF” (full name “the Republic of Korea”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-036 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for KR, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:KR
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 639a2393887f70a7b4f73aa146d0fd909420441eccf87933ad8433cc7567cb21
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code KR Short name KOREA, REPUBLIC OF"
            read by the Verifier: 2026-10-01T14:30Z sha256 639a2393887f (same bytes as registered)
  /locality/0/claim_ids: 이천
    claim-sk-hynix-m16-completed-icheon · FACT · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      (shown above)
  /nameplate_it_capacity_mw: not_applicable
exit 0

event-kr-m16-opened-2021-02 · entity record · canonical events.json
  
  /claim_ids:
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
exit 0

event-sk-hynix-announced-2022-09-06 · entity record · canonical events.json
  
  /claim_ids:
    claim-sk-hynix-m15x-plan-disclosed · ATTRIBUTION · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      statement: SK hynix disclosed on 2022-09-06 its plan to build M15X, an extension fab of M15, from October 2022 on land it had already secured in the Cheongju Technopolis industrial complex (the Atlas's translation).
      as of: 2022-09-06
      citation 1 · src-048 · standing party
        source: "Annual Report for fiscal year 2025 (제78기), section XI.1 'Progress and changes of disclosure information' (English DART)" · SK hynix Inc. · https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=126&offset=7831228&length=4080&dtd=dart4.xsd
        class: company_filing · publisher record: company-sk-hynix
        stated dates: published 2026-03-17
        registered: automated 2026-10-02T12:23Z sha256 9471557596770c666a7715c5d62e205cb910bb27fc38adbd6d83596490ddaadd
        filing copy: regulator_hosted
        locator: XI.1 'Progress and changes of disclosure information', table 가, the row whose 신고일자 (filing date) is 2022.09.06; cells read in order, table-cell boundaries as whitespace
        anchor: "2022.09.06 장래사업ㆍ경영 계획 (공정공시) 1. 제목: 생산기반 확충을 위한 투자계획 2. 내용: 2022년 10월부터 청주 테크노폴리스 산업단지 내 기존 확보된 부지에 M15의 확장 팹인 M15X(eXtension)를 건설할 계획입니다"
        read by the Verifier: 2026-10-02T12:23Z sha256 947155759677 (same bytes as registered)
exit 0

event-micron-technology-announced-2025-06 · entity record · canonical events.json
  
  /claim_ids:
    claim-micron-second-idaho-fab-announced · ATTRIBUTION · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      statement: Micron states that in June 2025 it announced plans for a second leading-edge memory manufacturing fab in Idaho.
      as of: 2025-06
      citation 1 · src-025 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended August 28, 2025" · Micron Technology, Inc. · https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf
        class: company_filing · publisher record: company-micron-technology
        stated dates: signed 2025-10-03
        registered: automated 2026-10-01T05:33Z sha256 4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9
        filing copy: filer_hosted_not_checked
        locator: p.47, Item 2 'Properties', the sentence beginning 'In June 2025, in connection with certain amendments'
        anchor: "In June 2025, in connection with certain amendments to our CHIPS Act agreements, we announced plans for a second leading-edge memory manufacturing fab in Idaho"
        read by the Verifier: 2026-10-02T11:12Z sha256 4b50d54e91da (same bytes as registered)
exit 0

event-amkor-technology-announced-2026-09-08 · entity record · canonical events.json
  
  /claim_ids:
    claim-amkor-arizona-phase-2-announced · ATTRIBUTION · supported · verified 2026-10-02 · canonical, accepted by the human on 2026-10-02 (sessions/reports/SESSION-09-REPORT.md)
      statement: Amkor announced on 2026-09-08 phase 2 of its Arizona advanced packaging and test campus.
      as of: 2026-09-08
      citation 1 · src-050 · standing party
        source: "Amkor Technology Announces Phase 2 of Arizona Advanced Packaging and Test Campus; Expands Investment to $12 Billion" · Amkor Technology (investor relations site) · https://ir.amkor.com/news-releases/news-release-details/amkor-technology-announces-phase-2-arizona-advanced-packaging
        class: company_press_release · publisher record: not_researched
        stated dates: published 2026-09-08
        registered: automated 2026-10-02T12:23Z sha256 2b1d929edb4fa3e170fab7b2bfc8f198c551ec92049093adb58bec9fc35dc365
        locator: first paragraph after the dateline 'TEMPE, Ariz.--(BUSINESS WIRE)--Sep. 8, 2026--'
        anchor: "today announced phase 2 of its Arizona Advanced packaging and test campus"
        read by the Verifier: 2026-10-02T12:23Z sha256 2b1d929edb4f (same bytes as registered)
exit 0

```
