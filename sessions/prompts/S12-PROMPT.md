# AI-Infrastructure-Atlas — S12 Session Prompt

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

Data architecture audit

Do not build new features during this session unless needed for remediation.

Audit:
- normalization;
- stable IDs;
- temporal model;
- relationships;
- provenance;
- queryability;
- migration risk.

### Human focus

The operational roadmap's S12 entry names no human task. The human decides the remediation
(Part B §16).

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
> - Everything above this line is **Part A**. As for S07 to S11, no upload was made: Claude
>   assembled Part A at the end of S11, after the human chose the recommended answer to the S12
>   question ("Pick the recommended", 2026-10-02).
>   - The operating contract, report list and headings are S11's Part A, word for word. The title
>     line is corrected: S11's read "S10 Session Prompt" (a slip, recorded in `SESSION-11-REPORT.md`).
>   - The session-specific mission is copied verbatim from the operational roadmap's week-5 entry
>     for S12 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`, "S12 — Data architecture audit").
>     That entry names no human task, so the human focus says so.
> - Part B is Claude's elaboration of Part A into the 18 sections of `SESSION-PROMPT-SPEC.md` §2,
>   written after S11 (`SESSION-11-REPORT.md`, `vertical-slice.md`, D-100 to D-108).
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The higher-level
>   documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The prompt becomes immutable once S12 begins (D-011).
> - **Answered before S12:** H-1 and Part A (§16). The human confirmed Part A as assembled and asked
>   for the merge to `main` ("I confirm part A and tell u to pull to main", 2026-10-02).
>   **Not yet answered:** H-0, H-2, H-3. Ask them at the start of S12, before any audit finding is
>   acted on.

## 01 — Session identity

- **Session:** S12
- **Title:** Data architecture audit
- **Type:** AUDIT (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`: "data model passes audit").
- **Milestone:** M3 — Vertical Slice + Audit (D-019 numbering). M3 completes only after S13 and the
  remediation of blocking findings.
- **Predecessor:** S11 — First end-to-end vertical slice (the HBM journey page; D-100 to D-108,
  all `proposed`).
- **Expected successor:** S13 — Content/evidence depth audit.
- **Complexity class:** medium for the audit; large if H-1's remediation (a new record type) is built
  in this session.

## 02 — Mission

Independently challenge the canonical data model and the first vertical slice against
`SESSION-ROADMAP.md` S12's list, answer first whether the candidates that are not edges
(`edge-dataset.md` §1) become records, and leave an audit report whose every blocking finding has
a remediation decision the human has ruled on.

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S12 examines normalization, duplicate concepts, stable IDs,
relationship semantics, temporal correctness, provenance completeness, queryability, migration
risk, "whether visual outputs are derived from canonical/derived data rather than duplicated
presentation data" and "whether the visual model preserves scope, units and temporal semantics".
Required output: "Architecture Audit Report + remediation decisions".

**The evaluation framework.** PEF §5 (data architecture audit: process and outcome), §3 (maturity
0–4 per dimension, each rating citing evidence), §4 (milestone audit).

**What S11 hands over** (`SESSION-11-REPORT.md`, "Implications for the next session"): the page
reads two Markdown documents as data (the refused candidates of `edge-dataset.md` §1, and the rule
tables of `source-policy.md` §6, `relationship-taxonomy.md` §1 and `company-dataset.md` §9), each
with a parser in the build and another in the test; "who makes HBM?" has no edge path (entity
fields only); no edge has a period; the journey specification is a hand-chosen selection.

**What S10 hands over** for M3's audits (`SESSION-10-REPORT.md`): RV-1 and PL-1 as guards; the
edge ID rule's length and the period-collision rule; F-1's 12-month horizon for `fabricates`;
D-091 (necessity read out of a definition); the AWS alias endpoint (D-074, D-093).

## 04 — Current state

As of `main` after S11 is merged. **S11 (`claude/new-session-djql6o`, final commit `d7efb78`, with
this prompt) must be merged to `main` before S12 starts.** Verify at start, and record the base,
`git branch -a` and `git ls-remote` in the report (D-018 L-03).

- **Data:** 52 source records; 120 canonical claims; 8 companies, 4 jurisdictions, 9 technologies,
  7 components, 3 products, 2 facilities, 4 events; 5 relationships; staging empty (as measured at
  `d7efb78`).
- **Checks:** 291 tests, Gate 0, `validate-data`, `validate-freshness`, `validate-design`
  (`tests/test_page.py`, PG-1 to PG-10) in CI; browser QA scripted outside CI (D-106).
- **Page:** `site/hbm-chain/index.html`, generated by `tools/build_page.py` from 33 input files;
  stale whenever any input changes (PG-7).
- **Status:** D-100 to D-108, `vertical-slice.md` and the Editorial and QA contracts are
  `proposed` (H-0).

**Inherited open items:** TSMC → H100 `fabricates` (D-092); HBM suppliers `not_researched` (D-094);
the AWS legal entity (D-093); `supplies` items with no record; subsidiary records (D-095); TSMC's
20-F; S01's weekly gate; S05 debt; the S11 new-user test as an independent walk-through.

**Not S12's:** new sources, claims or edges; metrics and DuckDB (S14–S15); content depth, stale
claims and source quality (S13); public deployment (NG-13).

**Next decision number:** D-109.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-11-REPORT.md`; `docs/architecture/vertical-slice.md`.
2. `docs/architecture/edge-dataset.md` (§1 above all); `SESSION-10-REPORT.md` ("What M3's audits
   should examine first").
3. `PROJECT-EVALUATION-FRAMEWORK.md` §3, §5; `SESSION-ROADMAP.md` S12; MA §5 (shared data
   contract), §5.6–5.7 (status and null semantics), §18.
4. `entity-taxonomy.md`, `relationship-taxonomy.md`, `claim-model.md`, `company-dataset.md`,
   `concept-dataset.md`, `facility-dataset.md`; the five schemas.
5. `docs/architecture/milestone-audits/M1-audit.md` (the last audit's form and findings);
   `docs/quality/audit-history.md`.
6. `tools/build_page.py` (the journey specification, the resolver), `tests/test_page.py`.

**Repository paths to inspect:** `data/`, `schemas/`, `tools/`, `tests/`, `site/`.

**External research: none.** An audit finding that needs a fact is a gap in the report.

**Lessons to carry:** L-01, L-02, L-04, L-05, L-09; S07 to S11: write the checks before the data;
ask before editing a file the prompt does not list; ask stop-condition rulings before building; a
break must fail for the reason it names; measure before estimating; send the human the steps before
the suggestions; the human's principle of not overreaching (D-108).

## 06 — Required reasoning

Answer these in the audit report before any remediation is built.

1. **The refused candidates (H-1).** The human chose records. Design them before building:
   - what a record holds: endpoints and `item` as IDs where a record exists, the relation type,
     the reason as a code from a controlled list, the ruling; and what it must not hold (no stored
     status, RR-6; no inferred edge, RR-5);
   - how an endpoint with no record is held (Samsung, Carl Zeiss SMT, "memory") without a
     placeholder (RR-7, V-9);
   - how the source sentence is held when it is not a canonical claim (the memory-supplier sentence,
     `src-024` p.8): cited through a claim, or a source and locator with an explicit state. A
     candidate must never become evidence that skipped the Verifier;
   - its ID rule, its file and layout, its staging and review path (D-061 pattern), the checks;
   - what stays in `edge-dataset.md` §1 (the reasoning) and what moves (the values): one home each.
2. **The other Markdown-as-data:** the rule tables the page reads (D-108). Keep, move, or check
   in one place only?
3. **The roadmap's examine list,** each with a finding, evidence and a maturity rating (PEF §3):
   normalization; duplicate concepts; stable IDs; relationship semantics; temporal correctness;
   provenance completeness; queryability; migration risk; visual derived from canonical data; the
   visual's scope, units and time.
4. **S10's five items** (§03) and **S11's handoff** (entity-field paths for "who makes it", no periods,
   the hand-chosen journey specification).
5. **Blocking or not.** For each finding: blocking (fix before S13), or debt with an owner. Only
   blocking findings are remediated in S12, and only with the human's ruling.
6. **The page after remediation.** If the candidates become records, how the gaps section shows them
   (cards grouped by reason, never as lines on the chain), and which page checks change.

## 07 — Tasks

**Audit**

1. The audit report (path per H-3), with findings, evidence, maturity ratings and the
   blocking/debt split; a row in `docs/quality/audit-history.md`.
2. Remediation decisions from D-109, each `proposed`, asked of the human as a batch.

**Remediation (only what the human approves)**

3. For H-1: the record design (schema change through the Knowledge Architect), the checks and
   fixtures written first, the migration of the §1 rows as staging records, the Verifier's pass, the
   human's review, promotion.
4. The page reads the records, not the Markdown table; PG checks updated; the gaps section shows
   cards grouped by reason; rebuilt; byte-identical.

**Validation**

5. Fail first; deliberate breaks for every new check, each showing which test fails and why; the
   S11 breaks re-run on the rebuilt page.
6. Browser QA re-run on the gaps section (desktop and 375 px), as D-106.

**Documentation**

7. `docs/README.md`, the baseline rows, `README.md` (Editorial); `SESSION-12-REPORT.md`, with the
   audit's handoff to S13.

## 08 — Explicit non-goals

- New sources, claims, edges or entity records, except a correction the human approves.
- New features beyond approved remediation: no second journey, no new page, no component system.
- Metrics, shares, rankings, scores, DuckDB (S14–S15); content depth and source quality (S13).
- Plain-language rewrites of design reasons, or definitions of bare section marks (D-108).
- Drawing rejected candidates as lines on the chain.
- Public deployment (NG-13); editing the root documents or anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **Evidence:** Part A's rules. A candidate record is the Atlas's design ruling, never a fact about
  the world; a source sentence on it is not evidence until a claim carries it.
- **One home:** a value moved from a document to a record leaves the document; the reasoning stays.
- **Unknown ≠ zero:** an endpoint with no record is an explicit state, never a placeholder.
- **Tooling:** standard library for `tools/`; schemas validated with the pinned `jsonschema` in tests
  only; no new dependency without an approved decision.
- **Process:** L-02, L-04, L-08; gates run before any push; not overreaching (D-108).

## 10 — Agent responsibilities

As `docs/agents/contracts.md` (Editorial and QA as proposed in S11, H-0).

| Agent | May write | Notes |
|---|---|---|
| Knowledge Architect | the audit report, `decisions.md` (append), the schema for a new record type (approved first), its design section | ID rule, vocabulary of reasons, one-home rulings |
| Data Auditor | `tests/`, `tests/fixtures/`, `tools/` | checks for the new records; the build reads them; migration script |
| Extractor | staging records for the migrated candidates | values copied from `edge-dataset.md` §1, never improved |
| Verifier | the staging records' citations | anchors re-read where a candidate cites a source sentence |
| Editorial | the template's framing and style; state rows | the gaps section's cards |
| QA | the report (browser findings) | the gaps section at both widths |

## 11 — Data and evidence rules

- **Canonical records:** read only, except the approved migration.
- **The candidates:** twelve rows in `edge-dataset.md` §1 at S11's end; none is an edge, and none may
  become one in S12.
- **Provenance:** every migrated value traces to its §1 cell; every sentence to a claim or an
  explicit state.
- **Temporal:** the audit records each edge's missing period as a finding, and changes no record.
- **Confidence:** no numeric values.

## 12 — Implementation rules

**May create:** the audit report; a schema and data file for the candidate records (after H-2);
tests, fixtures and a standard-library migration script; `SESSION-12-REPORT.md`.

**May modify:** `edge-dataset.md` §1 (values moved out, after approval); `tools/build_page.py`,
`tools/page_template.html`, `tests/test_page.py`; `decisions.md` (append); `audit-history.md`;
`docs/README.md`, baseline rows, `README.md`; `contracts.md` paths.

**Prohibited:** a schema change before the human approves it; a candidate stored as an edge or with
a stored status; a placeholder endpoint; hand-typed values in templates or tests; loosening a check.

## 13 — Verification plan

- **At start:** the full suite and Gate 0, logged; base, `git branch -a`, `git ls-remote`; S11 merged
  and this prompt on `main`.
- **Environment:** a fresh virtualenv from the pins, installed set compared with the pins.
- **Fail first;** then breaks for every new check; the S11 breaks re-run.
- **Migration:** every migrated value equals its §1 cell (scripted, then deleted from the document).
- **Browser QA:** as D-106, on the rebuilt page.
- **CI:** reported separately from local results (L-08).

## 14 — Evaluation requirements

The report records: the findings and ratings with evidence; the blocking/debt split; decisions and
rejected alternatives; deviations; invalidated assumptions; new debt; unresolved questions; and
whether the S12 gate ("data model passes audit") is met.

## 15 — Acceptance criteria

1. An audit report covers every item of the roadmap's S12 list, S10's five items and S11's handoff,
   each with evidence and a maturity rating.
2. Every blocking finding has a remediation decision the human ruled on; every other finding is debt
   with an owner.
3. H-1 is designed in the report before anything is built; if built, the candidates live in records
   with checks, and the page reads them, not the Markdown table.
4. No new fact enters the data; no candidate becomes an edge.
5. Tests and Gate 0 pass in a fresh virtualenv; the page rebuilds byte-identically; CI observed or
   reported as not observed.
6. The report satisfies SPEC §5 and Part A; decisions appended as `proposed`; the handoff names what
   S13 examines first.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- a finding needs a fact the data does not hold;
- a remediation needs a schema change the human has not approved;
- moving a value would leave two homes, or none;
- a candidate's sentence would enter the data without the Verifier;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions.** Open questions follow `CLAUDE.md` §9A (merged to `main` during S11's close, PR #19):
each says what concretely changes under each answer. Answers taken are kept verbatim.

- **H-0 — Human decision required: keep the rules S11 used to build the page** (not yet answered;
  ask first).
  - *What we are deciding:* whether the design rules behind the S11 page become accepted project
    rules, or are changed first.
  - *What will concretely change:* if accepted, nine decision records in `decisions.md` and the page's
    design document (`vertical-slice.md`) change from "proposed" to "accepted", and the two new agent
    roles (Editorial: may write only the page's framing text and style, and documentation status rows;
    QA: may write only browser findings in reports) become accepted in `docs/agents/contracts.md`. No
    data, code or page content changes. Later sessions must then follow these rules: for example,
    every word on a page must come from a record, a fixed label, a computed value or a marked framing
    box, and the page must be rebuilt whenever its inputs change.
  - *Why:* S12 audits the data model and the page; auditing against rules that are still proposals
    would mean auditing a moving target.
  - *What stays the same:* the records, the page and its checks.
  - *Options:*
    - **A — Accept all (recommended).** The nine rules, the design document and the two roles become
      accepted as written; S12 audits against them.
    - **B — Accept with named changes.** Claude changes the named rules first, and the page and its
      checks if a change affects them, then S12 starts the audit.
    - **C — Reject named rules.** What was built on a rejected rule is removed or rebuilt first: for
      example, rejecting the separate-lane rule (D-104) removes SK hynix's M16 plant and Micron's HBM4
      from the page.
  - *Decision requested:* "Choose A, B or C", naming the rules for B or C.
  - *Technical reference:* D-100 to D-108; `vertical-slice.md`; `contracts.md`, `roles.md`.
- **H-1 — the refused candidates:**
  - *(recommended)* records with their own home and checks, decided in S12 on architecture grounds;
    the gaps section restyled as cards, grouped by reason, as remediation;
  - stay design text the page quotes.
  - *Answer:* "Pick the recommended" (2026-10-02, at the end of S11, to the recommendation above).
- **H-2 — Human decision required: where the rejected candidates are stored** (not yet answered;
  ask after S12 has designed the record and can show its fields, before anything is built).
  - *What we are deciding:* the file and format that hold the twelve relationships the Atlas
    considered and refused (for example "SK hynix and Micron supply memory to NVIDIA"), now that they
    become data (H-1).
  - *What will concretely change:* under A, a new data file (with a staging copy) and a new schema
    file are added, with new checks in `tests/`; `edge-dataset.md` §1 keeps only the reasoning; the
    page's build reads the new file instead of the Markdown table. Under B, the relationship schema
    gains fields for refused candidates, and `data/relationships.json` holds both real edges and
    refusals.
  - *Why:* H-1 moved the candidates out of a document; they need one home with checks.
  - *What stays the same:* under either option, no candidate becomes a relationship, and no new fact
    enters the data. The five existing edges are unchanged.
  - *Future consequences:* A adds one more file and schema to maintain, but no tool can mistake a
    refusal for an edge. B keeps one file, but every tool that reads edges (navigation, the trace, the
    checks, the page) must filter refusals out, and one that forgets would show a refused link as real;
    it also needs a stored "refused" status, which the relationship rules forbid (RR-6).
  - *Options:* **A — A separate file and schema (recommended)**; **B — Extra fields in the relationship
    file.**
  - *Decision requested:* "Choose A or B."
  - *Technical reference:* H-1; RR-6; D-098 (the review path A would reuse).
- **H-3 — Human decision required: whether S12's audit also counts as the overdue audit of the
  data-collection phase** (not yet answered).
  - *What we are deciding:* the project's evaluation framework asks for an audit at the end of every
    milestone. The phase that built the canonical data (sessions S07 to S10, "M2") ended without one.
    Should S12's audit cover it too?
  - *What will concretely change:* under A, S12 writes one file,
    `docs/architecture/milestone-audits/M2-audit.md`, covering both the data model (S12's own scope)
    and how S07 to S10 were run (process ratings, rework, shortcuts); `docs/quality/audit-history.md`
    gets one row. Under B, S12 writes a narrower file on the data model only, and the M2 audit stays
    owed, added to S13's work.
  - *Why:* the framework requires the milestone audit (PEF §4); S07 did the same for the previous
    phase (D-066).
  - *What stays the same:* the audit's findings, the remediation process and the human's rulings on
    them are the same either way; only the scope and the file differ.
  - *Future consequences:* A makes S12 larger but closes the gap now; B keeps S12 focused and makes
    S13 larger.
  - *Options:* **A — One audit covering both (recommended)**; **B — A data-model audit only, M2 audit
    in S13.**
  - *Decision requested:* "Choose A or B."
  - *Technical reference:* PEF §4; D-066; `M1-audit.md` (the previous milestone audit).
- **Part A:** confirm as assembled, or amend; and where S12 runs.
  - *Answer:* "I confirm part A and tell u to pull to main" (2026-10-02): Part A confirmed; S11 and
    this prompt merged to `main`; S12 starts from `main`.

## 17 — Deliverables

- the audit report and its row in `audit-history.md`;
- remediation decisions from D-109, `proposed`;
- if approved: the candidate schema, records, checks, migration script; the rebuilt page and
  updated page checks; browser QA findings;
- `docs/README.md`, baseline rows, `README.md`;
- `sessions/reports/SESSION-12-REPORT.md`.

## 18 — Handoff

S12's report must hand S13 (Content/evidence depth audit; "No scaling until evidence weaknesses
are corrected or explicitly documented"):

- **Completed work:** the audit, its remediation, the candidate records if built.
- **For S13:** which claims and edges carry the most weight on the page; the derivations (D-091,
  D-099, the TSMC claim) whose steps S13 should challenge; whether the page's annotations remove a
  caveat.
- **Open issues:** debt with owners; everything §04 inherits.
- **Recommended next decision:** the first sampling question S13 should answer.
- **Files for S13 to read first:** the S12 report; the audit report; `vertical-slice.md`.
