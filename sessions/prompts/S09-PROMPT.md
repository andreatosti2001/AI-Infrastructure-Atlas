# AI-Infrastructure-Atlas — S09 Session Prompt

## Operating contract

This is a governed Opus 5.5 session. Before changing anything:

1. Read `CLAUDE.md`.
2. Read the relevant sections of `MASTER-ARCHITECTURE.md`.
3. Read `SESSION-PROMPT-SPEC.md` and `PROJECT-EVALUATION-FRAMEWORK.md`.
4. Read the immediately previous session report if it exists.
5. Inspect the actual repository state; do not assume the roadmap matches reality.
6. Restate mission, scope, non-goals and acceptance criteria.
7. Propose the smallest safe execution plan before implementation.

Follow:
`inspect → reason → propose → implement → validate → report`

### Evidence rules
- Use authoritative/current sources when current information matters.
- Do not use search snippets as evidence.
- Do not invent facts or silently infer supply-chain relationships.
- Separate FACT, DERIVATION, INTERPRETATION and IMPLICATION.
- Preserve uncertainty and source conflicts explicitly.

### Engineering rules
- Prefer the simplest architecture that satisfies the requirement.
- Do not introduce infrastructure merely for appearance.
- Do not perform broad refactors outside this session's scope.
- Never overwrite canonical data from unverified text.
- Run relevant tests/validators before declaring completion.

### Autonomy boundary
If a required decision crosses an approval boundary, stop and report it rather than improvising.

## Session-specific mission

### Mission

Facility dataset

Add physical locations and distinguish ownership, operation and production.

## Required end-of-session report

Record:
- files/components changed;
- data/evidence changes;
- commands/tests and results;
- decisions and rejected alternatives;
- deviations from this prompt;
- unresolved debt and evidence gaps;
- human approvals required;
- one concrete next-session handoff.

Commit only verified work.

---

# Part B — Session contract detail (SESSION-PROMPT-SPEC §2)

> **Provenance and precedence (D-012 pattern).**
> - Everything above this line is **Part A**. As for S07 and S08, no upload was made: the
>   human asked Claude to "write session 9's prompt".
>   - Claude assembled Part A from the fixed template: the operating contract, report list
>     and headings are byte-identical to S08's Part A, and are copied unchanged.
>   - The session-specific mission is copied verbatim from the operational roadmap's week-4
>     entry for S09 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`, "S09 — Facility
>     dataset"). That entry lists no human focus, and none is added.
>   - **The human confirmed Part A as assembled** before S09 started ("Confirm as assembled
>     (Recommended)", 2026-10-02).
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2. It was written after S08 (`SESSION-08-REPORT.md`,
>   `concept-dataset.md`, D-067 to D-077) and before the merge that brings S08 to `main`.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The higher-level
>   documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The prompt becomes immutable once S09 begins (D-011).
> - **Answered before S09 started (2026-10-02):** the human answered H-0 to H-6 in §16,
>   choosing Claude's recommendation each time, and confirmed Part A. H-0 (the S08 review)
>   was applied before this prompt reached `main`.

## 01 — Session identity

- **Session:** S09
- **Title:** Facility dataset (operational roadmap: "Facility dataset")
- **Type:** RESEARCH / IMPLEMENTATION (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`).
- **Milestone:** M2 — Canonical Dataset (`SESSION-ROADMAP.md` numbering, D-019). S09 is M2's
  third session.
- **Predecessor:** S08 — Technology, component and product dataset (14 canonical records;
  D-067 to D-077, D-074 accepted at the S08 review).
- **Expected successor:** S10 — First supply-chain edges (M2's last session).
- **Complexity class:** large. It creates the first facility records, the first dated
  records (events, D-022), and the checks for both. The human can narrow it in §16.

## 02 — Mission

Create the first canonical facility records, each located by evidence, and the first event
records that date what happens to them, so that a facility's status is derived, never
stored (MA §5.6).

- **Records:** facilities of the kinds the schema allows (`wafer_fab`,
  `packaging_facility`, `data_centre`), named in first-hand sources (H-1).
- **Time:** an event schema and the first events (opened, announced, expanded, closed), as
  D-022 assigns to S09 (H-2).
- **Ownership and operation:** the evidence that a company owns or operates a site,
  recorded so that S10 can create the `owns` and `operates` edges (H-3).
- **Checks:** the record checks extended to facilities and events.

The result must make four things impossible:

- a facility located by a company's headquarters, listing address or incorporation (R-5;
  `source-policy.md` §7 row `attr:facility.located_in`);
- an owner or operator stored as a facility field, or ownership read as operation
  (`relationship-taxonomy.md` §4.3, §4.4);
- an announced plan recorded as an existing site or a state (ER-8);
- a stored operating status that events could contradict.

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S09: "Represent strategically relevant
production/data-centre facilities with location, operator/owner distinctions and
evidence." Critical distinction: "Do not conflate headquarters, company ownership,
operating control and physical manufacturing location." Primary gate (`PROMPT-REGISTRY.md`):
"temporal facility model".

**The governing question needs places.** Where AI compute's critical dependencies sit is
partly a question of where production happens, which can differ from where a firm is based
(`entity-taxonomy.md` §4.2, Company vs Facility). The later EU lens (D-008) needs facility
locations as their own facts.

**Earlier decisions that land here:**

- D-022: the event schema is S09's, because S09's gate is the temporal facility model.
- `entity-taxonomy.md` §3.2: a facility's operating status is derived from events, never
  stored; a cloud region or availability zone is not a facility.
- `relationship-taxonomy.md` §4.3, §4.4, §5: `owns` and `operates` are separate edges, with
  their evidence thresholds; S10 instantiates edges.
- S07's handoff (`company-dataset.md` §14): ASML's Veldhoven campus, TSMC's fabs, Micron's
  and SK hynix's production sites; Amkor's Arizona plan as an event.
- S08's handoff (`SESSION-08-REPORT.md`, Implications): extend `ENTITY_KINDS` and the trace;
  the re-retrieval rule (D-075).

## 04 — Current state

As of `main` after the S08 merge. Verify at start, and record the base, `git branch -a` and
`git ls-remote` in the report (D-018 L-03). **This prompt must be on `main` before S09
starts.**

**Accepted model:**

- entity types and fields (D-022 to D-027): `schemas/entities.schema.json` `facility`
  (`facility_kinds`, `located_in`, `locality`, `nameplate_it_capacity_mw`);
- relationships (D-028 to D-033): `owns`, `operates` in `schemas/relationships.schema.json`;
- source policy (D-034 to D-043), with the rows `identity:facility`, `attr:facility.*`;
- claim model (D-044 to D-053); company dataset (D-054 to D-066);
- concept dataset (D-067 to D-077): accepted, except D-070 and D-076, which stay proposed
  (H-0).

**No event schema exists.** MA §5.5 lists event types (opened, closed, announced, invested,
acquired and others); `entity-taxonomy.md` §3.2 and D-022 leave the schema to S09.

**Data at the start** (as measured at the S08 final commit, `4edf6d9`):

- 45 source records; 95 canonical claims, 9 staging claims;
- 8 companies, 4 jurisdictions, 7 components, 4 technologies (5 more in staging), 3
  products; no facility, relationship or event record.

**Checks at the start:** 190 tests; `validate-data` (VD-1 to VD-13; V-1, V-4, V-9, V-10,
CE-1, ID-1, J-1, CI-1, DEF-1, DEF-2, B-1, PI-1, IO-1) and `validate-freshness` (F-1) in CI.

**Open items S09 inherits:**

- D-070 and D-076 (not approved at the S08 review, left open at H-0) and the 5 staged
  technology records;
- the AWS legal entity (`company-dataset.md` §14); S01's weekly gate; S05 debt (the class
  table vs the matrix; SRC-023 not re-read).

**Not S09's:** relationship records (S10), metrics (S14–S15), policy (S17).

**Next decision number:** D-078.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-08-REPORT.md`, with its addendum.
2. `docs/architecture/concept-dataset.md` and `company-dataset.md` (the patterns S09
   reuses: IDs, staging, attested anchors, re-retrievals, record checks, freshness).
3. `schemas/entities.schema.json` (`facility`) and `schemas/relationships.schema.json`
   (`owns`, `operates`).
4. `docs/architecture/entity-taxonomy.md` §3.2, §4.2, §4.4 (a plan is not an edge), §9.
5. `docs/architecture/relationship-taxonomy.md` §4.3, §4.4, §5 (evidence expectations), §10 (time).
6. `docs/research/source-policy.md` §6 (ER-8, ER-9), §7 (rows `identity:facility`,
   `attr:facility.*`), §11, §12 (`time_sensitive`: `nameplate_it_capacity_mw`).
7. `docs/architecture/claim-model.md` §2–§4, §13.
8. `MASTER-ARCHITECTURE.md` §5.5 (Event), §5.6 (status semantics), §5.7.
9. `docs/architecture/decisions.md`: D-022, D-024, D-029, D-030, D-031, D-040, D-054 to D-077.

**External research: expected.** Every retrieval follows `source-policy.md` §11 (RA-1 to
RA-7) and the S07/S08 practice: an access probe first, then one targeted RA-4 list for the
human. Web search only discovers URLs. Candidate sources (`INTERPRETATION`; the session
checks each):

- the filings already registered (`src-024` to `src-031`): their "Properties" and
  facilities sections (Micron p.47, ASML p.327, TSMC p.21);
- company pages and press releases naming a site (as `party`; plans as events, ER-8);
- government publications naming a facility (CHIPS awards, permits), as `originator`.

**Audit findings to carry:** L-01, L-02, L-04, L-05, L-09; S07's and S08's lessons: read the
sentence; plan RA-4 at the start; re-retrieve before citing (D-075); write the checks
before the data; ask flagged rulings separately, with a rule for what an unticked answer
means.

## 06 — Required reasoning

Answer these before writing records, in a document (§07 task 1) and decisions.

1. **Which facilities** (H-1)? For each candidate: which sentence names the site, which
   kind it is (`facility_kinds`, several allowed: B-3), and whether the sentence supports a
   state or only a plan (ER-8).
2. **Facility identity and IDs.** What makes one site one record (`entity-taxonomy.md`
   §3.2: one site at one location; the ID survives a change of owner)? What stable,
   non-editorial key gives the ID: the operator's own site name ("Fab 18"), the locality,
   or another rule? Machine-checkable where possible.
3. **Location.** `located_in` from a sentence that places the site, never from the owner's
   headquarters or incorporation (R-5). When the sentence names a city or park, how is the
   country reached (the S07 ISO 3166-2 `DERIVATION` pattern, D-057)? `locality` exactly as
   the source gives it.
4. **Ownership vs operation vs production** (H-3). For each facility: which sentence says
   who owns it, who operates it, and what is made there? Do these meet the evidence expectations of
   `relationship-taxonomy.md` §5? What S09 records now (claims) and what S10 turns into
   edges.
5. **Events** (H-2). The smallest event schema that dates a facility's life: which event
   types (from MA §5.5), which fields (date with precision, subject, claims), and how a
   plan differs from an occurrence. How is status derived from events, and where does the
   derivation live (a function, never a stored field)?
6. **Capacity.** `nameplate_it_capacity_mw` only where a source says the figure is
   nameplate IT capacity (TQ-10); it is `time_sensitive` (F-1).
7. **Data centres.** Cloud providers rarely name sites
   (`claim-cloud-compute-facility-often-undisclosed`). Which data centres, if any, have a
   first-hand sentence? A region or zone is never a facility.
8. **Staging and canonical:** as D-061; CE-1 extended to facilities and events.
9. **Checks:** extend `ENTITY_KINDS`, V-1 (`located_in`; event subjects), V-4, V-9, V-10
   (the facility rows), CE-1, F-1; the facility ID rule; schema validity of events; the
   status derivation as a tested function. Hand-apply each to real records first (L-09).
10. **The human's review:** review sheets as in S08, with the flagged rulings asked
    separately.

## 07 — Tasks

**Design**

1. `docs/architecture/facility-dataset.md` (or a name the session justifies): the answers to
   §06, referencing the taxonomies, policy and claim model by section, never restating them.
2. The event schema (`schemas/events.schema.json` or the name the design justifies), with
   fictional fixtures, as a decision for the human (H-2).

**Research**

3. Access probe of the candidate hosts; then one RA-4 list for the human, with exact pages
   and reasons. Record every refusal.
4. Register new sources (`src-046` onward); re-retrieve registered filings before citing
   them again (D-075).

**Implementation**

5. Facility, ownership/operation and event claims in `data/staging/claims.json`, verified
   at their locators.
6. Facility and event records, first in staging.
7. Checks (§06 q9) in CI, with fixtures and planted faults.
8. Promotion on the human's verdicts.

**Validation**

9. Fail first; then at least eight deliberate breaks, each showing which tests fail.
   Include: a facility located from a headquarters sentence; an owner stored as a field;
   a plan recorded as an opened event; an event dated after the source's own date; a
   facility ID that changes with a display name; a data-centre capacity that is not
   nameplate IT capacity; a canonical event citing a staging claim; an event whose subject
   is missing.

**Documentation**

10. Decisions from D-078, each `proposed`; `docs/README.md`, the baseline state rows,
    `README.md`, `contracts.md` paths if they change.
11. `sessions/reports/SESSION-09-REPORT.md`, with the review sheets and the trace of each
    canonical record.

## 08 — Explicit non-goals

- Relationship records, including `owns` and `operates` edges (S10). S09 records their
  evidence as claims only.
- Metrics, capacity shares or any score (S14–S15).
- Production lines, clean rooms or sub-site detail (`entity-taxonomy.md` §3.2).
- Cloud regions or availability zones as facilities (D-022).
- Coverage beyond H-1.
- Any change to an accepted schema, vocabulary value or decision without a decision the
  human approves first (§16 stop). The new event schema is a proposal for the human.
- An agent runtime, a database or graph server, a UI; an external API; circumvention.
- Promoting anything without the human's verdict.
- Editing the root documents, `domain-map.md`, the taxonomies, the frozen register or
  migrated values. Anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **Evidence:** Part A's rules, `source-policy.md` and `claim-model.md`. A facility's
  identity and location rest on `party` or `originator` sources of a preferred or
  acceptable class. ER-8 (plans), ER-9 (company-level is not site-level) apply.
- **One home:** a facility's location is its `located_in` field through claims; who owns or
  operates it will be S10 edges; its status is derived from events, never stored.
- **Unknown ≠ zero:** every field present; `not_researched` where no source was read;
  `not_applicable` only where the attribute cannot apply (capacity on a fab).
- **Tooling:** `tools/` standard library (D-003, D-026); PDF extraction in a scratch
  environment; no new dependency without an approved decision.
- **Process:** L-02, L-04, L-08.

## 10 — Agent responsibilities

As `docs/agents/contracts.md` (accepted, D-052; paths updated in S07 and S08). The
Extractor's allowed writes extend to the new staging files through the Editorial row,
recorded in the report. The Change Detector stays inactive.

| Agent | May write | Notes |
|---|---|---|
| Source Scout | the report | discovery only |
| Extractor | `data/sources.json` (new records), `data/staging/*.json` | provenance on every candidate |
| Verifier | verification fields of staging claims; the report | re-checks its own locators |
| Knowledge Architect | the design document, the event schema (proposed), `decisions.md` (append) | ID rules, one-home rulings |
| Data Auditor | `tests/`, `tests/fixtures/`, `tools/` | the checks of §06 q9 |
| Editorial | `docs/README.md`, baseline rows, `README.md`, `contracts.md` (paths only) | the new state only |

## 11 — Data and evidence rules

- **Canonical entities:** facilities; events as a new record kind; canonical only on the
  human's verdict.
- **Allowed relationship types:** none instantiated. Ownership and operation evidence stays
  in claims for S10.
- **Required source tier:** `source-policy.md` §7 rows `identity:facility`,
  `attr:facility.located_in`, `attr:facility.locality`,
  `attr:facility.nameplate_it_capacity_mw` (filings and government publications preferred).
- **Provenance:** every value cites claims in the S06 shape.
- **Temporal:** identity and location are `stable` rows; capacity is `time_sensitive`
  (F-1). Events carry their own dates.
- **Confidence:** no numeric values.
- **Unknown or unverified:** `not_researched`; access gaps support nothing (SP-7).

## 12 — Implementation rules

**May create:** the design document; the event schema with its fixtures (proposed);
`data/facilities.json`, the event data file(s) and their staging copies; tests and fixtures;
`sessions/reports/SESSION-09-REPORT.md`.

**May modify:** `data/sources.json` (new records); `data/staging/claims.json`,
`data/claims.json` (promotion on verdicts); `tests/test_data_entities.py`,
`tests/test_data_schema.py`, `tests/test_freshness.py` (scope); `tools/trace.py` (default
files only); `decisions.md` (append); `docs/README.md`, baseline rows, `README.md`,
`contracts.md` (paths).

**Approach:** mirror S07 and S08. Rules are read from their homes (the matrix from
`source-policy.md` §7, facility kinds from the schema), never copied.

**Prohibited:** a hard-coded list of facilities, rows or classes in a test; a stored status
field; a runtime; a hand-written JSON Schema validator; copying policy or taxonomy text.

**Schema changes to accepted files:** none. The event schema is new and proposed (H-2). If
§06 needs a change to an accepted schema, stop (§16).

## 13 — Verification plan

- **At start:** the full suite and Gate 0, logged in the report (S08 Deviation 6); base,
  `git branch -a`, `git ls-remote`; this prompt on `main`.
- **Environment:** a fresh virtualenv from the pins, installed set compared with the pins.
- **Fail first;** then the breaks of §07 task 9, each with the tests it fails.
- **Manual evidence check:** the Verifier reads every anchor's sentence and re-checks its
  own locators; the human reviews each batch.
- **Trace:** each canonical record, pasted in the report.
- **CI:** reported separately from local results (L-08).
- **Not applicable:** browser, accessibility, performance.

## 14 — Evaluation requirements

The report records decisions and rejected alternatives (the facility ID rule, the event
schema, the status derivation, the ownership/operation evidence); deviations; invalidated
assumptions (a facility no source locates, a plan that never became a site); new debt;
unresolved questions; the human's verdicts verbatim.

## 15 — Acceptance criteria

1. Every canonical facility validates against the unchanged entity schema; its
   `identity_claim_ids` and `located_in` rest on claims that V-10 accepts for their rows.
2. No `located_in` rests on a headquarters, incorporation or listing sentence.
3. No owner or operator is a facility field; the ownership and operation evidence is in
   claims, ready for S10, each meeting or explicitly failing `relationship-taxonomy.md` §5.
4. Every event validates against the event schema; a plan is never an occurrence; status is
   derived by a tested function and never stored.
5. Every facility ID follows a written rule, machine-checked where the rule allows.
6. Every new source has class, retrieval, hash and dates; access gaps are listed; RA-4
   files stay outside the repository.
7. The extended checks run in CI.
8. Nothing real is canonical without the human's recorded verdict.
9. No change to accepted schemas or vocabulary values; no relationship record; no scores;
   no runtime.
10. Tests and Gate 0 pass in a fresh virtualenv; CI observed or reported as not observed.
11. The report satisfies SPEC §5 and Part A; new decisions appended as `proposed`.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- a record would need a field, vocabulary value or kind the accepted entity schema lacks
  (e.g. a facility kind for a research site or an office);
- a facility's location is supported only by a headquarters or listing sentence;
- a source states ownership but not operation (or the reverse) and a record would need
  the other;
- a site is known only from an announcement (it is an event, not a facility, unless the
  human decides otherwise);
- a source is reachable only by circumvention, or an anchor cannot be re-read (SP-7);
- promoting anything would happen without the human's verdict;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions already taken** (2026-10-02, before S09 started; Claude's recommendation
first in each list). Do not ask them again. Record H-1 to H-6 in decisions (`proposed`,
citing the human's answer), and stop only if a condition cannot be met.

- **H-0 — the S08 review (D-067 to D-077; D-074 accepted at the S08 review):**
  - *(recommended)* approve the rest except D-070 and D-076, which stay open with the 5
    staged records;
  - approve all, including D-070 and D-076 (the 9 staged claims and 5 records become
    canonical);
  - leave them proposed.
  - *Answer:* "All except D-070, D-076 (Recommended)". Applied before S09: the status
    lines of D-067 to D-069, D-071 to D-073, D-075 and D-077, the design document and an
    addendum to the S08 report. D-070 and D-076 stay proposed; the 5 staged records stay
    staging.
- **H-1 — facility scope:**
  - *(recommended)* a few fabs and packaging sites named in the registered filings (ASML
    Veldhoven, TSMC Hsinchu Science Park fabs, Micron's and SK hynix's production sites,
    an Amkor site), plus a data centre only where a first-hand sentence names one;
  - fabs only;
  - fabs, packaging sites and data centres from any sufficient source.
  - *Answer:* "Filings' fabs + packaging (Recommended)".
- **H-2 — events:**
  - *(recommended)* a minimal event schema in S09 (facility events only: announced,
    opened, expanded, closed), proposed for the human, with status derived by a tested
    function;
  - no events in S09: facility status stays `not_researched` until a later session.
  - *Answer:* "Minimal event schema (Recommended)".
- **H-3 — ownership and operation:**
  - *(recommended)* S09 records the sentences as claims and lists them as S10 edge
    candidates; S10 creates the `owns` and `operates` edges;
  - S09 creates the first `owns` and `operates` edges itself.
  - *Answer:* "Claims now, edges in S10 (Recommended)".
- **H-4 — sources and RA-4:**
  - *(recommended)* re-retrieve the registered filings first; one RA-4 list for anything
    refused; paywalled sources stay gaps;
  - registered filings only, no new retrievals.
  - *Answer:* "Re-retrieve + RA-4 list (Recommended)".
- **H-5 — layout:**
  - *(recommended)* one file per kind, as D-055 and D-077: `data/facilities.json` and
    `data/events.json`, with staging copies;
  - one combined file.
  - *Answer:* "One file per kind (Recommended)".
- **H-6 — when records become canonical:**
  - *(recommended)* review inside S09, as S07 and S08;
  - after the session.
  - *Answer:* "Review inside S09 (Recommended)".
- **Part A:** confirm as assembled, or amend.
  - *Answer:* "Confirm as assembled (Recommended)".

## 17 — Deliverables

- the design document (§07 task 1) and the proposed event schema;
- new source records; facility, ownership/operation and event claims; facility and event
  records (staging and canonical);
- the extended checks, tests and fixtures;
- `decisions.md`: D-078 onward, `proposed`;
- `docs/README.md`, baseline rows, `README.md`, `contracts.md` paths if changed;
- `sessions/reports/SESSION-09-REPORT.md`.

## 18 — Handoff

S09's report must hand S10 (First supply-chain edges; "Create the first auditable
relationships"; human focus: "inspect at least 10 relationships end-to-end from source to
published edge"):

- **Completed work:** the canonical facilities and events; the ownership and operation
  claims, each marked against `relationship-taxonomy.md` §5; the extended checks.
- **For S10:**
  - the edge candidates: `owns` and `operates` from S09's claims; `fabricates`,
    `packages`, `designs`, `supplies` from the S07 filings and S08 products; the S08
    "requires"/"part of" statements;
  - the relationship rules V-2, V-3 and V-5 to V-8 that arrive with edges;
  - the human's review of at least 10 edges end-to-end.
- **Open issues:** the human approvals of the S09 decisions; D-070 and D-076 if still open;
  the AWS legal entity; S01's weekly gate; S05 debt.
- **Recommended next decision:** the human confirms the facility IDs and the event schema
  before S10, because edges will point to facilities.
- **Files for S10 to read first:** the S09 report; the S09 design document;
  `relationship-taxonomy.md` §4, §5, §10, §15; `concept-dataset.md`; `company-dataset.md`;
  D-028 to D-033 and the S09 decisions.
