# AI-Infrastructure-Atlas — S06 Session Prompt

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

Claim/evidence system

Implement claim-level provenance.

Human focus:
- understand FACT vs DERIVATION vs INTERPRETATION vs IMPLICATION;
- test a few claims manually.

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
> - Everything above this line is **Part A**, the human-authored S06 prompt. It is the
>   upload verbatim, with one repair: the upload showed `—` and `→` as `â€”` and `â†’`
>   (UTF-8 text read as Windows-1252). Part A restores those two characters. No other
>   character differs.
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2. It was written after the human's S05 review and the
>   week-2 gate. It carries S05's findings forward: `SESSION-05-REPORT.md` with its two
>   addenda; `source-policy.md` §4–§8, §12 and §16; D-034 to D-043.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The
>   higher-level documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The human may edit Part B before S06 starts. It becomes immutable once S06 begins
>   (D-011).
> - **Edited before S06 started (2026-09-30):** the human answered the four questions in
>   §16 (H-1 to H-4), choosing Claude's recommendation each time. The answers are recorded
>   in §16. §06 q11 to q13, §07 tasks 5 to 8 and §12 point to them.

## 01 — Session identity

- **Session:** S06
- **Title:** Evidence/claim system
- **Type:** IMPLEMENTATION (`SESSION-ROADMAP.md`). The dominant purpose is building the
  claim and source records and the checks that make provenance work. The design it needs
  is written first (§06), but the session is judged on working, tested records.
- **Milestone:** M1 — Domain + Evidence Foundation (`SESSION-ROADMAP.md` numbering, D-019)
- **Predecessor:** S05 — Source hierarchy and evidence policy (merged to `main` at
  `e388777`, PR #7; D-034 to D-043 accepted; week-2 gate recorded as passed at `9bbf8c6`,
  PR #8)
- **Expected successor:** S07 — Company dataset (M1 completes with S07, operational
  roadmap week 3)
- **Complexity class:** large. It creates the repository's first data files, two record
  schemas, the first data validation, a trace tool and the agent contracts. §16 lets the
  human narrow it.
- **Weekly gate:** none closes in S06. Week 3 closes after S07.

## 02 — Mission

Implement claim-level provenance, so that every statement the Atlas records can be traced
to the exact words of a qualified source, or is openly labelled as the Atlas's own
derivation, interpretation or implication.

- **The claim record.** One home for what a statement says, what kind of statement it is
  (`FACT`, `ATTRIBUTION`, `DERIVATION`, `INTERPRETATION`, `IMPLICATION`), how well the
  evidence supports it, which sources it cites and exactly where, and when it was verified.
- **The source record.** The S05 class vocabulary extended into a full record, and the S01
  register migrated into it, so every citation points at a canonical source.
- **Tracing.** The roadmap S06 gate: the system can answer "What exactly supports this
  relationship?"
- **Human learning** (Part A): the human understands the five claim types through real
  claims, and tests a few by hand.

The result must make three things impossible:

- a statement recorded as `FACT` whose support cannot be followed to a source, a locator and
  a quoted anchor;
- a derivation, interpretation or implication that looks like a sourced fact;
- a real-world claim becoming canonical without the verification and review CLAUDE.md §9
  requires.

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S06: "Implement claim-level provenance, verification
state and temporal metadata before dataset scale-up." Its gate: "The system can answer:
'What exactly supports this relationship?'" S07 to S10 create records that must cite
claims, so the claim record has to exist first.

**Every accepted schema already points at claims that do not exist.**

- Entity records need `identity_claim_ids`, and every attribute assertion needs `claim_ids`
  (D-025).
- Relationship records need `claim_ids` (D-028), and the `supplier` qualifier needs its own
  claims (D-031).
- The claim ID format `claim-<slug>` was fixed by S03 "so that references have a checkable
  shape"; the claim record itself was left to S06 (`entity-taxonomy.md` §7).

**S05 handed S06 a list** (`source-policy.md` §16; `SESSION-05-REPORT.md`, Implications):

- **Source record:** class; publisher as text, and as a company reference where the
  publisher is a company (§4); authors; retrieval method (automated, or "manual, by the
  human"); access date; content hash; publication date as stated; the host of a copy
  (RA-6).
- **Claim record:** standing (`party`, `originator`, `reporter`); the attribution chain
  (reporter, originator, locator); the as-of date; the search scope of a
  `not_publicly_determinable` claim (ER-3); the evidence status for disputed claims (§10).
- **Migration:** each register row's class from `source-policy.md` §8.1; S05-R1 from §8.3.
  After the migration the register is frozen.
- **The meaning of `verified`:** D-015's second part is still in force "until S06's claim
  model confirms or replaces it" (D-036).

**Earlier handoffs also land here:**

- D-010: S06 writes `docs/agents/roles.md` and `docs/agents/contracts.md` in the MA §12
  format, "because that is when the staging → verification → canonical workflow first
  exists".
- `relationship-taxonomy.md` §15: the `validate-data` rules V-1 to V-9 go to "S06/S07, with
  the first records". S06 creates the first records (sources, and claims), so the part of
  `validate-data` that applies to them starts here.
- `baseline.md` §5: `validate-data` is "not built"; `validate-freshness` is "not built —
  needs sources with access dates (S06+)".

**Two claim-type lists disagree** (a one-home issue S06 must settle, §06 q2):

| Source | Claim types |
|---|---|
| CLAUDE.md §6 and the roadmap S06 | `FACT` · `ATTRIBUTION` · `DERIVATION` · `INTERPRETATION` · `IMPLICATION` |
| MA §10 | law / normative text · fact · derived · attributed · interpretation · critique · forecast |

MA §10 also lists evidence statuses (direct, partial, derived, context-only, unverified,
disputed), and MA §5.7 lists `verified` and `disputed` among null states. "Derived" appears
as both a claim type and an evidence status: a candidate second home (L-06).

**The human's learning** (Part A human focus):

- why "NVIDIA says the H100 uses a TSMC process" (`FACT` about what NVIDIA says),
  "TSMC fabricates the H100" (`DERIVATION`), "the Atlas counts only GPUs and ASICs as AI
  accelerators" (`INTERPRETATION`) and "facility-level location for cloud compute will often
  be undisclosed" (`IMPLICATION`) are different kinds of statement;
- what it takes to check a claim by hand: open the source, find the locator, read the
  anchor, judge whether the wording exceeds it.

## 04 — Current state

As of `main` @ `9bbf8c6` (PR #8), plus the commit that adds this prompt. Verify at start,
and record the base, the `git branch -a` result and `git ls-remote` in the report (D-018
L-03).

**This prompt must be on `main` before S06 starts.** S04's prompt reached `main` late (S04
Deviation 1). If S06 finds this file only on a branch, it records a deviation and brings in
the original commit.

**Accepted model:**

- entity types and fields: D-022 to D-025, `schemas/entities.schema.json`;
- relationship record and eleven types: D-028 to D-033, `schemas/relationships.schema.json`;
- source classes, standing, preference matrix, evidence rules, conflicts, retrieval,
  freshness, class homes: D-034 to D-041, `docs/research/source-policy.md`,
  `schemas/sources.schema.json` (vocabulary only);
- filings from the filer's own copy (D-042); no external API dependency (NG-14, D-043);
- D-026: `jsonschema`, pinned, for tests only; `tools/` stays standard library.

**Files S06 builds on:**

- `schemas/sources.schema.json`: the `source_class` vocabulary, whose root is a class value.
  S06 turns the root into the source record and keeps the vocabulary as a `$defs` entry.
- `docs/research/source-register.md`: SRC-001 to SRC-023 in a 10-column table, its notes,
  "Retrieved but not cited" and "Not retrievable".
- `docs/research/source-policy.md`:
  - §4 standing and attribution chains;
  - §5 the separate axes;
  - §6 ER-1 to ER-10;
  - §7 the matrix;
  - §8.1 the class of each registered source (the home until S06 migrates it, D-041);
  - §8.3 S05-R1 and the access record S05-A1;
  - §10 conflict kinds;
  - §12 the four dates;
  - §16 the handoff.
- `docs/research/domain-map.md`: S01's statements with claim labels and verbatim anchors.
  It is a research-staging artifact: S06 does not edit it and does not migrate it wholesale.
- `docs/architecture/entity-taxonomy.md` §7 and `relationship-taxonomy.md` §9, §15.
- Tests: 85, as measured at `9bbf8c6` in a fresh virtualenv (58 from S03/S04, 27 from S05).
  `tests/test_source_policy.py` parses the register and §8.1. The migration will change what
  it must parse (§06 q9).
- `tools/validate_repo.py` (Gate 0), `.github/workflows/ci.yml` (one job: pinned install,
  unit tests, Gate 0).

**No `data/` directory exists.** D-005: directories are not created until the session that needs
them, and their layout is that session's design decision (§16, H-2).

**Open items S06 inherits:**

- the S05 handoff list (§03);
- D-010 (agent contracts);
- V-1 to V-9 for the records S06 creates;
- the class for an announcement by a standards body or association, only if S06 retrieves
  one (it should not need to);
- S05 debt: the §2 class table and the §7 matrix can disagree without a test failing;
  S05-R1's anchors are verified by hand only; SRC-023 was not re-read.

**Not S06's:**

- entity records (S07 companies; S08 technologies, components and products, D-027; S09
  facilities);
- relationship records (S10);
- the event schema and event rows in the matrix (S09);
- metrics (S14–S15; NG-11);
- `validate-freshness` as code (§06 q10 decides whether any of it starts here).

**Next decision number:** D-044.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-05-REPORT.md`, including both addenda.
2. `docs/research/source-policy.md` §4, §5, §6, §7, §8, §10, §12, §14 and §16.
3. `schemas/sources.schema.json`, `schemas/entities.schema.json` (`claim_ids`, `assertion`,
   `unresolved`), `schemas/relationships.schema.json` (`claim_ids`, `attr_supplier`).
4. `docs/architecture/entity-taxonomy.md` §7; `relationship-taxonomy.md` §9, §12, §15.
5. `docs/research/source-register.md`: every row and every note.
6. `docs/research/domain-map.md`: "How to read this map" (claim classes and status
   markers), and the entries a seed claim would use (§06 q12).
7. MA §5.2 (claim), §5.3 (source), §5.6–5.7 (status and null semantics), §10 (claim types,
   evidence status, hierarchy), §11–§12 (agents and the contract format), §13 (autonomy),
   §14 Gate 2 (provenance), §15 (validation commands), §16 (pipeline).
8. PEF §6 (content audit: claim sampling, freshness exposure) and §7 (agent architecture
   audit).
9. `docs/architecture/decisions.md`: D-005, D-010, D-015, D-018 (L-01 to L-09), D-025,
   D-026, D-028, D-031, D-034 to D-043.
10. `SESSION-ROADMAP.md` S06, S07, S10, S11; the operational roadmap's week-3 entry.

**Repository paths to inspect:** `schemas/`, `tests/`, `tools/`, `docs/research/`,
`docs/architecture/`, `.github/`.

**External research: none expected.**

- The seed claims (§06 q12) use sources already registered and anchors already verbatim in
  the domain map, or in S05-R1's hand-verified anchors (`source-policy.md` §8.3).
- If a source must be retrieved, the S05 rules apply: RA-1 to RA-7, D-042, NG-14. A new
  source becomes a canonical source record, not a register row (the register is frozen by
  the migration).

**Audit findings to carry:**

- **A-1, L-01: machinery before a used loop.** No agent runtime, orchestrator or autonomous
  write path. Agents are contracts plus deterministic validators (NG-08). Every tool S06
  writes is exercised on real records in the same session.
- **L-02:** nothing is called a gate unless CI runs it.
- **L-04:** no hand-typed counts; prose counts are tested or labelled "as measured at
  `<commit>`".
- **L-05:** each new data file joins the validator's scope in the session that creates it.
- **L-06:** claim type and evidence status are separate fields from the first claim schema.
  Verification dates are per record, never a batch stamp.
- **L-09:** read before you automate. Every claim field is filled by hand on real claims
  before a check is written for it.
- **S05's process lessons:** check each value against what it belongs to, not only that it
  appears somewhere (break 11); reading finds contradictions that tests cannot; shingle
  tests catch text copied from another home.

## 06 — Required reasoning

Answer these before writing schemas or data. The answers go into the claim-model document
(§07 task 1) and the decision records.

1. **What a claim is.**
   - One proposition, stated once, with its evidence. Is a claim one sentence of one source,
     or one proposition that several sources may support? (S05 ER-7: several pages of one
     publisher are one voice; corroboration needs independent publishers.)
   - Where does the link between a record and its claims live? Entities and relationships
     already hold `claim_ids`. A claim that also lists the records it supports would be a
     second home. Decide the direction once.
   - Does a claim state its matrix row (`source-policy.md` §7), or is the row derived from
     the record and field that cite it? Choose the option that keeps one home.
2. **Claim types.** Reconcile CLAUDE.md §6 (five types, which the roadmap S06 requires) with
   MA §10's seven. Give each MA type a disposition, as S03/S04 did for MA's lists:
   - `attributed` and `fact` map directly;
   - `derived` is `DERIVATION`;
   - `forecast`: a third party's forecast is `ATTRIBUTION`, a plan is ER-8's intention, the
     Atlas's own forecast is out of scope before S15 (NG-11);
   - `critique`: whose, and is it `ATTRIBUTION` or `INTERPRETATION`?
   - law / normative text: reserved for the policy layer (S17).
   - Record the reconciliation; do not edit MA.
3. **Evidence status.** Define the vocabulary (S06 owns it, L-06; S05 defined none).
   - Start from MA §10 (direct, partial, derived, context-only, unverified, disputed).
   - Drop or rename any value that duplicates a claim type (`derived` vs `DERIVATION`) or an
     unresolved state (`not_researched`, `not_publicly_determinable` and `not_applicable`
     stay on attributes, D-025).
   - How does `disputed` work with S05's conflict kinds (§10.1)? A disputed status must point
     at the competing claims, never replace them.
   - Which statuses may a canonical record rest on, and which only in staging?
4. **Claim type × evidence status.** Which combinations are impossible? For example: an
   `INTERPRETATION` needs no source but must cite the claims it interprets; a `DERIVATION`
   must cite its input claims, and its status can be no stronger than its weakest input's; a
   `FACT` needs at least one citation of a preferred or acceptable class with the required
   standing (`source-policy.md` §5). Write the rules as a table the tests can read.
5. **Citations.** What each citation records: the source, the locator, the verbatim anchor,
   the standing, and for a `reporter` citation the originator and the locator where the
   reporter names it (the chain, ER-6).
   - Is the anchor required for every citation? For which source types can it not be
     (a figure, a table)?
   - How is an anchor from a manual retrieval verified when the full text stays outside the
     repository (H-1 of S05, RA-4)?
6. **The meaning of `verified`.** Confirm or replace D-015's second part ("the Verifier role
   re-read the retrieved source and found the quoted anchor at its locator"). Decide:
   - whether verification is a status value, a date, or both (L-06: per record);
   - who may verify (Verifier contract, §07 task 7) and what the human's class C review adds;
   - what "canonical" means for a real claim, and where the human's review is recorded.
7. **Staging and canonical.** MA §16: raw evidence → staging → verification → canonical.
   MA §5.6: no overloaded status field. How does a claim move from staging to canonical: a
   directory, a field, or a review record? Choose the simplest option that never lets an
   unreviewed real claim look canonical.
8. **`not_publicly_determinable` claims.** ER-3 needs the search recorded: the question,
   each class searched and the sources consulted, the date and the result. Is that a claim
   type, a field on the claim, or a separate search record? Apply it by hand to HBM-06's
   supplier question: under ER-3, can the current evidence support NPD at all, or only
   `not_researched`?
9. **The source record and the migration.**
   - Field list from `source-policy.md` §16 (§03 above). Which are required, which may be an
     explicit state (e.g. `undated (live page)`)?
   - Source IDs: the register uses `SRC-001`; MA §5.3 uses `source-001`; entity IDs are
     lower-case with a type prefix. Choose one format, keep the S01 numbers, and keep every
     `SRC-NNN` citation in existing documents resolvable.
   - Publisher as an entity reference: a `company-…` ID (checked by prefix; the record
     arrives in S07, V-1). `institution` stays reserved (D-022).
   - Where the class lives after migration: the source record (D-041). `source-policy.md`
     §8.1 becomes history. How do the tests move from "register ↔ §8.1" to "data ↔ §8.1",
     without two live homes?
   - What happens to the register's "Retrieved but not cited" and "Not retrievable" tables?
   - How the register is marked frozen (§12 below allows its status line to change).
10. **Freshness.** `baseline.md` §5 says `validate-freshness` needs sources with access
    dates, which the migration creates. Decide whether S06 implements any freshness check
    (for example: every source has an access date and hash; every `time_sensitive` claim has
    an as-of date), or leaves all of it to the first session with `time_sensitive` canonical
    records. L-09 applies.
11. **Validation.** Which checks S06 builds, and where they run (§16, H-4). At least:
    - schema validity of every source and claim record;
    - unique IDs; every citation's source exists; every claim a derivation or interpretation
      cites exists; no citation cycle;
    - type × status rules (q4);
    - the migration is complete and exact (every register row → one source record, same
      class as §8.1);
    - V-1 to V-9 stay with the entity and relationship records (S07, S10). Say which of them,
      if any, S06 can already run on the fictional fixtures.
    - Consider V-10: a record must not rest only on claims whose sources are "never
      sufficient alone" for its matrix row (S05 §7). Define it now; decide whether it runs
      yet.
12. **Seed claims** (§16, H-1). If real claims are created, pick them to cover all five
    types from registered sources. Candidates, each already evidenced in the domain map or
    S05-R1:
    - `FACT`: NVIDIA names the H100's process "TSMC 4N process customized for NVIDIA"
      (SRC-006, FAB-05);
    - `DERIVATION`: TSMC fabricates the H100 (ER-1), citing the claim above;
    - `ATTRIBUTION`: ASML calls EUV "unique to ASML" (SRC-017); LBNL reports IDC analysts on
      die supply (SRC-021 p.18, a chain); SK hynix plans TSMC's process for HBM4 base dies
      (SRC-014, an intention);
    - `INTERPRETATION`: the working definition of AI accelerator, GPUs and AI ASICs only
      (TQ-01, CON-01);
    - `IMPLICATION`: facility-level location for cloud AI compute will often be
      `not_publicly_determinable` (domain map §6).
    Each quoted anchor must be verbatim in the domain map (or in S05-R1, checked by hand).
13. **Agent contracts** (D-010; §16, H-3). Which roles get a full MA §12 contract now? For
    each: inputs, outputs, allowed and forbidden writes (paths that exist after S06), evidence
    requirements, handoff format, validation gate (a CI check that exists, L-02) and failure
    behaviour. No runtime (NG-08).
14. **The trace** (the roadmap gate). How does the system answer "What exactly supports this
    relationship?" before any real relationship exists (S10)? Candidate: a standard-library
    command that, given a record ID, prints record → claims → citations → sources (class,
    locator, anchor, standing, dates). It runs on the fictional fixtures for a relationship,
    and on the seed claims for real sources. Is that enough to call the gate "met for
    review"? Say what it cannot yet show.
15. **The human's manual test** (Part A). What does the human need to test a few claims by
    hand? A short review sheet: for each seed claim, the source link, the locator, the anchor,
    the type and status proposed, and a question ("does the anchor say this, and no more?").
    Where are the human's verdicts recorded, and what changes on the claim when they are?

## 07 — Tasks

**Design**

1. `docs/architecture/claim-model.md`: the answers to §06, with the claim-type
   reconciliation (MA §10), the evidence-status vocabulary, the type × status table, the
   citation and chain rules, the meaning of `verified`, staging vs canonical, the NPD search
   record, the source record and the migration mapping. It references `source-policy.md` by
   section and never restates it (A-5).
2. The explainer for the human (Part A focus): a section "Five kinds of claim", walking the
   seed claims (or, without seed claims, the §14 sentence of `source-policy.md`) through
   type, status, citation and display.

**Implementation**

3. `schemas/claims.schema.json`: the claim record. Vocabulary values are `const`s with one
   description each (S03–S05 pattern). Shared shapes (`claim_ids`, `partial_date`) are
   `$ref`s into `entities.schema.json`, never copied.
4. `schemas/sources.schema.json`: extended from vocabulary to source record. The class
   vocabulary stays in the same file, unchanged (D-034). Any change to a class value needs a
   human-approved decision first.
5. **Migration.** SRC-001 to SRC-023 and S05-R1 become canonical source records in `data/`
   (layout per H-2), each with the class from `source-policy.md` §8.1/§8.3. It is a
   deterministic transformation (CLAUDE.md §9, class B): a script or a test proves it is
   exact. The register gets a "frozen" status line. §8.1 is marked as history.
6. **Seed claims** (only under H-1's answer): 5 to 10 real claims in staging, covering all five
   types, with citations checked against the domain map by a test.
7. **Agent contracts** (D-010, scope per H-3): `docs/agents/roles.md` and
   `docs/agents/contracts.md` in the MA §12 format.
8. **Validation** (§06 q11, placement per H-4), in CI.
9. **Trace** (§06 q14): a standard-library command in `tools/`, with its own tests on the
   fixtures and on the seed claims.
10. **Tests:**
    - schema behaviour: valid fixtures pass; each invalid case is one JSON Pointer mutation of
      a valid base and fails at, under or beside the pointer it mutates (S04 pattern);
    - consistency: every claim-type and evidence-status value is defined once; the type ×
      status table matches the schema; every MA §10 claim type has one disposition, parsed
      from MA; every cited decision, section, SRC and anchor exists;
    - data: the validation checks of task 8, on the real files;
    - prose counts (L-04).

**Validation**

11. Fail first: the new tests fail before the decisions and the data exist. Then break things
    deliberately in scratch copies, at least eight ways, each caught. Include:
    - a claim citing a source ID that does not exist;
    - a `FACT` claim with no citation;
    - a `DERIVATION` that cites no input claim;
    - a register row missing from the migrated sources;
    - a migrated source whose class differs from §8.1;
    - a seed-claim anchor changed by one word;
    - a claim-type value added to the schema without a table row;
    - a staging claim presented as canonical (by whatever mechanism §06 q7 chooses).

**Documentation**

12. The review sheet for the human's manual test (§06 q15), in the claim-model document or
    the report.
13. Decisions from D-044, each `proposed`.
14. `docs/README.md` (claim model; source and claim schemas; agent contracts: planned →
    proposed), the baseline state rows that have become false (§1, §3, §4, §5), `README.md`
    (status and layout).
15. `sessions/reports/SESSION-06-REPORT.md`.

## 08 — Explicit non-goals

- Entity records of any type (S07 to S09), relationship records (S10), event records and the
  event schema (S09).
- Migrating the domain map's statements into claims, beyond the seed claims H-1 allows. The
  domain map stays S01's research artifact.
- Promoting any real claim to canonical without the human's review (CLAUDE.md §9, class C).
- Metrics, scores, numeric confidence or credibility values (NG-11; D-028).
- An agent runtime, orchestrator, dispatcher, queue, or any autonomous write path (NG-08;
  L-01). Contracts are documents; the checks are deterministic validators.
- A database server, graph database or frontend (NG-07); any UI.
- An external API dependency (NG-14); circumventing access controls (RA-2).
- Changing an accepted S03, S04 or S05 field, vocabulary value or decision without a decision
  the human approves first. The `claim_ids` format may change only through a decision, as
  `entity-taxonomy.md` §7 allows, and every schema that uses it must change with it.
- Editing the root documents, `domain-map.md`, `M0-audit.md` or the two taxonomies. The
  register changes only by its status line (§12).
- Anything in `Eu-Digital-Policy` (NG-01).

## 09 — Constraints

- **Evidence:**
  - Part A's evidence rules and `source-policy.md` apply to every claim S06 writes.
  - Every seed claim cites a canonical source record, a locator and a verbatim anchor
    (machine-checked against the domain map, or hand-checked for S05-R1).
  - Claim labels: `FACT | ATTRIBUTION | DERIVATION | INTERPRETATION | IMPLICATION`. Part A
    lists four; CLAUDE.md §6 adds `ATTRIBUTION` and takes precedence.
- **One home:**
  - claim type, evidence status and standing each have one home, on the claim or citation;
  - the link between a record and its claims has one direction (§06 q1);
  - each source's class has one home: the source record, after the migration (D-041);
  - vocabulary values live in the schemas; reasoning lives in the claim-model document.
- **Separate axes** (L-06; `source-policy.md` §5): class ≠ standing ≠ claim type ≠ evidence
  status. Verification dates are per record.
- **Unknown ≠ zero:** no default values for evidence status, claim type or standing; a
  missing value is invalid, never "unverified" by default.
- **Tooling:** `tools/` stays standard library (D-003, D-026). Tests may use the pinned
  `requirements-test.txt`. Any new dependency needs a decision the human approves first.
- **Process:** L-02, L-04, L-08 as in S05.
- **Portfolio:** demonstrate claim-level provenance on real sources, traceable end to end, not
  a schema with no data.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Knowledge Architect | `docs/architecture/claim-model.md`, `docs/architecture/decisions.md` (append), `schemas/claims.schema.json`, `schemas/sources.schema.json` | IDs, vocabularies, one-home rulings |
| Extractor | the data files for source records and staging claims (paths per H-2) | migration and seed claims; provenance on every candidate |
| Verifier | the report; the verification fields of staging claims | checks every anchor at its locator; may downgrade or reject; may not invent evidence |
| Data Auditor | `tests/`, `tests/fixtures/`, `tools/` (the trace, and validation if H-4 puts it there) | schema, reference, migration and type × status checks |
| Editorial | `docs/agents/`, `docs/README.md`, `baseline.md` state rows, `README.md`, the register's status line, `source-policy.md` (status notes on §8.1 only) | only to record the new state; never alters a canonical fact |

All other agents are inactive. No agent writes outside these paths and
`sessions/reports/`.

## 11 — Data and evidence rules

- **Canonical entities:** none created.
- **Allowed relationship types:** the eleven of D-029, unchanged. None is instantiated.
- **Required source tier:** the S05 policy: every citation's source has a class; a `FACT`
  cites at least one source of a preferred or acceptable class for its matrix row with the
  standing the row requires (`source-policy.md` §5, §7).
- **Provenance:** every citation records source, locator, anchor and standing; a `reporter`
  citation also records the originator (ER-6).
- **Temporal:** the source keeps its publication date as stated and its access date and hash;
  the claim keeps its as-of date and its verification date (`source-policy.md` §12).
- **Confidence:** no numeric values. Confidence is the claim type, the evidence status and the
  citations.
- **Unknown or unverified:**
  - a claim that has not been verified is visibly so;
  - `not_publicly_determinable` needs the ER-3 search record;
  - a source that could not be read supports nothing (SP-7).

## 12 — Implementation rules

- **Files S06 may create:**
  - `docs/architecture/claim-model.md`;
  - `schemas/claims.schema.json`;
  - the data directory and files H-2 chooses (source records; staging claims under H-1);
  - `docs/agents/roles.md`, `docs/agents/contracts.md`;
  - one trace command in `tools/`, and the validation command if H-4 puts it there;
  - tests and fixtures for all of the above;
  - `sessions/reports/SESSION-06-REPORT.md`.
- **Files S06 may modify:**
  - `schemas/sources.schema.json` (vocabulary → record, class values unchanged);
  - `docs/architecture/decisions.md` (append);
  - `tests/test_source_policy.py` and `tests/test_source_schema.py`, only as far as the
    migration requires (§06 q9);
  - `.github/workflows/ci.yml`, only if a new check cannot run under the existing unit-test
    step;
  - the register's status line; `source-policy.md` status notes on §8.1 and §16;
  - `docs/README.md`, `baseline.md` state rows, `README.md`.
- **Approach:** mirror S03 to S05. The document holds the reasoning; the schemas hold shapes
  and vocabularies; tests hold the checks. Tables are parsed by splitting cells with width
  and row-count assertions. Test helpers are imported from `tests/test_entity_taxonomy.py`
  (kept at the S04 review).
- **Migration:** deterministic, re-runnable, and proven exact by a test that reads the
  register itself.
- **Prohibited:** a runtime or scheduler; a hand-written JSON Schema validator (D-026
  rejected it); copying `source-policy.md` or taxonomy text; a hard-coded list of register
  rows or claim types in a test (read them from their homes).
- **Schema changes to accepted files** (`entities.schema.json`, `relationships.schema.json`):
  none. If §06 needs one, stop (§16).

## 13 — Verification plan

- **At start:** `python -m unittest discover -s tests` and `python tools/validate_repo.py`;
  record the base, `git branch -a` and `git ls-remote`.
- **Environment:** a fresh virtualenv from `requirements-test.txt`, with the installed set
  compared to the pins (sorted).
- **Fail first:** the new tests fail before the decisions, schemas and data exist.
- **Behaviour:** every invalid fixture is one mutation and fails where it targets. Read each
  error message.
- **Data:** the validation checks pass on the real files; each break in §07 task 11 is
  caught in a scratch copy.
- **Manual evidence check:** the Verifier re-reads every seed claim's anchor at its locator,
  records the date, and the human tests a few (Part A).
- **Trace:** run it on a fixture relationship and on each seed claim; paste the output into
  the report.
- **CI:** report it separately from local results, or say it was not observed (L-08).
- **Not applicable:** browser, accessibility, performance.

## 14 — Evaluation requirements

The report records:

- decisions and rejected alternatives, including the MA §10 reconciliation and the
  evidence-status values dropped;
- deviations from Part A or Part B;
- assumptions invalidated, in particular any register row that did not migrate cleanly, and
  any seed claim the Verifier or the human downgraded;
- new debt;
- unresolved questions;
- the human's verdicts on the claims they tested, verbatim.

## 15 — Acceptance criteria

1. A claim schema exists in which claim type and evidence status are separate required fields,
   with every value defined once and no numeric confidence.
2. Every MA §10 claim type has one disposition, machine-checked against MA.
3. The type × status rules are written as a table and enforced by tests.
4. A `FACT` claim without a citation, a `DERIVATION` without input claims, and a citation
   without a locator or source each fail validation.
5. Every register row SRC-001 to SRC-023 and S05-R1 is one canonical source record, with the
   class `source-policy.md` §8.1/§8.3 gives it. Machine-checked against the register.
6. The register is marked frozen, and each source's class has exactly one live home.
7. The `validate-data` checks S06 builds run in CI (L-02).
8. The trace answers "what supports this record?" on a fixture relationship and on the seed
   claims, with source, class, locator, anchor, standing and dates. The report says what it
   cannot yet show.
9. The meaning of `verified` is decided in a decision record, and D-015's status line records
   it at the human's review.
10. Agent contracts exist in the MA §12 format for the roles H-3 names, each with a validation
    gate that CI runs.
11. Under H-1: the seed claims cover all five types; every anchor is verbatim at its source;
    none is canonical before the human's review; the review sheet exists.
12. No change to accepted S03, S04 or S05 schemas or vocabulary values; no numeric scores; no
    runtime.
13. Tests and Gate 0 pass in a fresh virtualenv; the CI result is observed or reported as not
    observed.
14. The report satisfies SPEC §5 and Part A's list; new decisions are appended as `proposed`.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- a claim or source field would need a change to an accepted entity, relationship or source
  vocabulary (including the `claim-<slug>` format);
- a register row cannot be migrated without inventing a value (a missing date is an explicit
  state, never a guess);
- a seed claim's anchor is not verbatim at its locator, or the Verifier cannot re-read the
  source (the claim is dropped or downgraded, never patched);
- the evidence-status vocabulary cannot be reconciled with MA §10 without editing MA (record
  the conflict; do not edit MA);
- `validate-data` would need `jsonschema` inside `tools/` without H-4 allowing it;
- promoting any real claim to canonical would happen without the human's review;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions already taken** (2026-09-30, before S06 started; Claude's recommendation
first in each list). Do not ask them again. Record each in a decision (`proposed`, citing the
human's answer), and stop only if a condition cannot be met:

- **H-1 — real claims in S06** (§06 q12, q15):
  - *(recommended)* a seed of 5 to 10 real claims in staging, covering all five types, from
    registered sources, which the human tests by hand; none becomes canonical in S06 without
    the human's verdict;
  - fictional fixtures only (the human's manual test then uses the S05 §14 sentence);
  - seed claims promoted to canonical in S06 after the human's in-session review.
  - *Answer:* the recommended option ("Seed 5–10 in staging (Consigliato)").
- **H-2 — layout of the first data files** (D-005):
  - *(recommended)* one JSON file per record kind, as an array of records:
    `data/sources.json`, and `data/staging/claims.json` for unreviewed claims (a canonical
    `data/claims.json` appears when the first claim is accepted);
  - one JSON file per record (`data/sources/src-001.json` …);
  - JSON Lines.
  - *Answer:* the recommended option ("Un file JSON per tipo (Consigliato)").
- **H-3 — agent contracts in S06** (D-010):
  - *(recommended)* `roles.md` lists all twelve CLAUDE.md §8 roles; `contracts.md` gives full
    MA §12 contracts only to the roles active through S10 (Source Scout, Extractor, Verifier,
    Knowledge Architect, Data Auditor); the others say which session first activates them;
  - full contracts for all twelve roles now;
  - defer the contracts (needs a decision amending D-010).
  - *Answer:* the recommended option ("Pipeline fino a S10 (Consigliato)").
- **H-4 — where `validate-data` runs** (D-026):
  - *(recommended)* as CI tests over `data/` (schema checks with the pinned `jsonschema`,
    reference and migration checks with the standard library), documented as the Atlas's
    `validate-data`; `tools/` stays standard library;
  - a `tools/validate_data.py` that imports `jsonschema` (amends D-026: a runtime dependency
    in `tools/`);
  - a standard-library-only command that skips schema validation.
  - *Answer:* the recommended option ("Test in CI (Consigliato)").

## 17 — Deliverables

- `docs/architecture/claim-model.md`, including the "Five kinds of claim" explainer and the
  review sheet
- `schemas/claims.schema.json`; `schemas/sources.schema.json` as a source record
- the data files per H-2: migrated source records; seed claims in staging under H-1
- `docs/agents/roles.md`, `docs/agents/contracts.md` (scope per H-3)
- a trace command in `tools/`; validation per H-4; tests and fixtures
- `docs/architecture/decisions.md`: D-044 onward, `proposed`
- the register's status line; `source-policy.md` status notes; `docs/README.md`; baseline
  state rows; `README.md`
- `sessions/reports/SESSION-06-REPORT.md`

## 18 — Handoff

S06's report must hand S07 the following:

- **Completed work:** the claim and source records, the migrated sources, the seed claims and
  their review state, the validation, the trace, the agent contracts, and their tests.
- **For S07** (company dataset; gate: "Every canonical company record has identity evidence
  and stable IDs"):
  - how to write a company's `identity_claim_ids` and attribute claims, using the matrix rows
    `identity:company` and `attr:company.*` (filings preferred; D-042 for their copies);
  - which `validate-data` rules (V-1 onward, and V-10 if defined) S07 must switch on when the
    first entity records exist;
  - `publisher_entity` references that will resolve once company records exist (V-1);
  - `validate-freshness`, if not built in S06: the first `time_sensitive` canonical records
    arrive with S07.
- **Open issues:** the human approvals; any seed claim not yet reviewed; S01's weekly gate;
  S05 debt still open (the class table vs matrix check; S05-R1 hand-verified anchors; SRC-023
  not re-read).
- **Recommended next decision:** the human reviews the S06 decisions and the seed-claim
  verdicts before S07, because S07's company records cite claims in the form S06 defines.
- **Files for S07 to read first:**
  1. the S06 report;
  2. `docs/architecture/claim-model.md`;
  3. `schemas/claims.schema.json`, `schemas/sources.schema.json`;
  4. `docs/research/source-policy.md` §7 (rows `identity:company`, `attr:company.*`) and §11;
  5. `docs/agents/contracts.md`;
  6. `docs/architecture/entity-taxonomy.md` §3.1 and §7;
  7. D-024, D-025, D-042 and the S06 decisions.
