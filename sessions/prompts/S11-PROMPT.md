# AI-Infrastructure-Atlas — S10 Session Prompt

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

First end-to-end vertical slice

Build one complete user journey:

`source → entity → relationship → dependency path → visualization → evidence`

### Human focus

- use it as if you were a new user;
- try to break the chain;
- note confusing terminology.

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
> - Everything above this line is **Part A**. As for S07 to S10, no upload was made: Claude
>   assembled Part A at the end of S10, after the human agreed to the next milestone Claude
>   recommended ("yes and merge into main", 2026-10-02, to "S11: build the HBM dependency chain
>   as the first end-to-end user journey, from source sentence to an editorial visual, with the
>   unknown HBM supplier shown as a visible gap").
>   - The operating contract, report list and headings are byte-identical to S10's Part A.
>   - The session-specific mission and the human focus are copied verbatim from the
>     operational roadmap's week-5 entry for S11 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`,
>     "S11 — First end-to-end vertical slice").
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2, written after S10 (`SESSION-10-REPORT.md`, `edge-dataset.md`,
>   D-089 to D-099).
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The higher-level
>   documents (`CLAUDE.md`, including §6A, and `MASTER-ARCHITECTURE.md`, including §16.1) govern
>   both.
> - The prompt becomes immutable once S11 begins (D-011).
> - **Answered before S11 started** (2026-10-02, end of S10): H-1 (the human's "yes"), H-4 with
>   it, and H-2, H-3, H-5 and Part A, each with Claude's recommendation (§16). The human confirmed
>   Part A as assembled ("Confirm; new session (Recommended)"). Do not ask them again; record them in decisions (`proposed`, citing
>   the answer).

## 01 — Session identity

- **Session:** S11
- **Title:** First end-to-end vertical slice
- **Type:** IMPLEMENTATION (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`).
- **Milestone:** M3 — Vertical Slice + Audit (`SESSION-ROADMAP.md` numbering, D-019). S11 is M3's
  first session; M3 completes only after S12 and S13 and the remediation of blocking findings.
- **Predecessor:** S10 — First supply-chain edges (5 canonical edges; D-089 to D-099, all
  accepted; M2 complete).
- **Expected successor:** S12 — Data architecture audit (including the visual/data-model
  integrity audit, `SESSION-ROADMAP.md` cross-cutting section).
- **Complexity class:** large: the first page, the first visual, the first Editorial and QA
  contracts, and the first browser checks.

## 02 — Mission

Build one journey that answers **"What does an AI accelerator's memory depend on, and who is
known to make it?"** by walking the canonical edges from the H100 and Trainium2 through HBM to
3D die stacking, rendered as one editorial-quality visual generated from the JSON files, in which
every mark opens the evidence behind it and every unknown is shown as a gap.

The result must make five things impossible:

- a mark, label or sentence on the page with no canonical record, edge or claim behind it;
- presentation data typed by hand: the page is generated from `data/` by a tested build step,
  and regenerating it from the same data gives the same bytes;
- a gap drawn as absence or zero: `not_researched` (the HBM supplier) and the recorded gaps
  (TSMC → H100, D-092) are visible and named;
- a staging record shown as canonical;
- an inference shown without its label: a `DERIVATION` edge (M16, the class edge) is marked as
  inferred, and its reasoning is one click away.

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S11: "Build one complete user journey from source → entity
→ relationship → visualization → evidence." Target journey: "Trace one AI compute dependency
chain upstream." Gate: "The journey is usable by a person who did not build the dataset."
Visual requirement: "at least one editorial-quality analytical visual, not only a raw chart or
graph. The visual must connect visibly to the evidence chain."

**The constitution.** `CLAUDE.md` §6A and MA §16.1 (added before S10, commit `269a1fa`): the
pipeline `validated data → derivation → insight → visual specification → editorial composition
→ presentation`; the visual quality gate; Gate 6 "UI and visual communication". MA §19: every
insight page gives the short answer, why it matters, the evidence, the entities and edges, the
method and limitations, the date last verified and deeper links.

**What S10 hands over.** The chain exists only as five edges and two text tools
(`tools/navigate.py`, `tools/trace.py`). S10's report names the journey and says navigation needs
a structured output for a page (`SESSION-10-REPORT.md`, "Implications for the next session").

**Roles that start here.** `docs/agents/roles.md`: Editorial and QA are "First active: S11", with
no contract yet.

## 04 — Current state

As of `main` after the S10 merge (`1e03337`, PR #17). Verify at start, and record the base,
`git branch -a` and `git ls-remote` in the report (D-018 L-03). **This prompt must be on `main`
before S11 starts.**

**Accepted model:** entity, relationship, source, claim and event schemas; source policy; claim
model; company, concept, facility and edge datasets (D-022 to D-099, all accepted).

**Data at the start** (as measured at the S10 final commit, `0b2bb0e`):

- 52 source records; 120 canonical claims; staging empty;
- 8 companies, 4 jurisdictions, 9 technologies, 7 components, 3 products, 2 facilities,
  4 events; **5 relationships** (`incorporates` 2, `designs` 1, `operates` 1, `requires` 1).

**Checks at the start:** 264 tests; `validate-data` (VD-1 to VD-13; entity checks; event checks;
edge checks V-1 to V-10, CE-1, RI-1, PL-1, EP-1, PE-1, RV-1), `validate-freshness` (F-1, entities
and edges), the trace and navigation tests, Gate 0, all in CI. `validate-design` and
`qa-browser` (MA §15) do not exist.

**Open items S11 inherits:** TSMC → H100 `fabricates` (D-092); the HBM suppliers
(`not_researched`, D-094); the AWS legal entity (D-093); `supplies` items with no record;
subsidiary records (D-095); TSMC's 20-F (a gap); S01's weekly gate; S05 debt.

**Not S11's:** new edges or sources (S11 shows the data; it does not extend it); metrics and
DuckDB (S14–S15); policy (S17); the audits (S12, S13); public deployment (NG-13, until this slice
passes its gates).

**Next decision number:** D-100.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-10-REPORT.md` (the handoff; the navigation outputs).
2. `CLAUDE.md` §6A, §12; MA §14 (Gate 6, Gate 7), §16.1, §19; `SESSION-ROADMAP.md` (the
   cross-cutting visual section and S11).
3. `docs/architecture/edge-dataset.md` §1, §8; `relationship-taxonomy.md` §1 (direction
   convention), §2, §4, §9 (unknowns); `claim-model.md` §12 (the trace), §13 (how claims are
   displayed: "A reader never sees a bare *TSMC makes the H100*").
4. `docs/agents/roles.md`, `contracts.md`; `docs/architecture/baseline.md` §5, §6 (NG-07, NG-09,
   NG-13).
5. `docs/architecture/decisions.md`: D-019, D-028 to D-033, D-073, D-089 to D-099.

**External research: none expected.** The page shows canonical data. If the journey cannot be
told without a new fact, that is a gap on the page, not a research task (§16).

**Audit findings and lessons to carry:** L-01, L-02, L-04, L-05, L-09; S07 to S10: write the
checks before the data; ask before editing a file the prompt does not list; never push after a
failed gate; ask stop-condition rulings before building; a break must fail for the reason it
names; run every rule on a candidate before promising it.

## 06 — Required reasoning

Answer these before building, in a document (§07 task 1) and decisions.

1. **The question and its scope.** The journey's question, what it covers (two products, one
   component class, one technology, the actors), and what it explicitly does not (other
   accelerators, market shares, "critical", "concentrated": NG-11).
2. **The derivation.** The path is computed from the edges (a walk, never stored, RR-5). Which
   function computes it, and how the page build reads it (H-4).
3. **The visual form** (MA §16.1 grammar). A dependency/flow diagram is the expected form; say why
   it answers the question better than a table or a network layout, and what each mark, line,
   label and colour encodes: level (class vs instance), relation type, `FACT` vs `DERIVATION`,
   canonical only, gaps.
4. **The editorial composition.** Headline (the question), short answer, why it matters, the
   visual, key context, the evidence panel, method and limitations, dates (each claim's
   `verified_on` and each source's stated dates). Every sentence of prose is either generated from
   a record or is the Atlas's own framing labelled as such; Editorial adds no fact.
5. **Gaps.** How `not_researched`, the TSMC → H100 gap and "no recorded relationship" are drawn so
   that a reader cannot read them as "none" (RR-7).
6. **Evidence on the page.** From each mark to the edge, its claims (type, status, statement), the
   citation (source, class, locator, anchor, standing, dates) and, for a `DERIVATION`, its
   reasoning and inputs: the trace, rendered.
7. **Accessibility and mobile.** Contrast, a text equivalent of the diagram, keyboard access to
   every evidence panel, nothing only on hover, readable at 375 px.
8. **Checks.** What `validate-design` means for this page (H-2), what the browser check covers
   (H-3), and which faults the tests must catch.
9. **The new-user test.** How the human uses it "as if a new user", tries to break the chain,
   and records confusing terms; where the findings go.

## 07 — Tasks

**Design**

1. `docs/architecture/vertical-slice.md` (or a name the session justifies): the answers to §06,
   including the visual specification, referencing the taxonomy, claim model and edge dataset by
   section, never restating them.
2. Editorial and QA contracts in `docs/agents/contracts.md`, and their rows in `roles.md` (H-5).

**Implementation**

3. A structured output of the walk and the trace (H-4), tested.
4. The build step (H-2): from `data/` to the page, deterministic, standard library.
5. The page itself: the composition of §06 q4, with the visual of q3 and the evidence of q6.
6. Checks in CI, written before the page: every mark resolves to a canonical record; every
   displayed statement, anchor and date equals its canonical home; gaps are present; no staging
   record; rebuilding gives the same bytes; accessibility basics that can be checked statically.

**Validation**

7. Fail first; then at least eight deliberate breaks, each showing which tests fail. Include: a
   mark with no record behind it; a hand-edited label that no longer matches its record; a gap
   removed or drawn as zero; a staging edge on the page; a `DERIVATION` drawn as a `FACT`; a
   changed claim statement not reflected after a rebuild; an anchor that no longer matches; an
   evidence panel unreachable by keyboard; a page that does not rebuild identically.
8. Browser QA (H-3): desktop and 375 px, keyboard path, no console errors; screenshots in the
   report.
9. The human's new-user test (Part A): findings recorded verbatim; blocking ones fixed or listed
   for S12.

**Documentation**

10. Decisions from D-100, each `proposed`; `docs/README.md`, the baseline state rows (including
    Gate 6 and `validate-design`), `README.md`, `contracts.md` and `roles.md` (H-5).
11. `sessions/reports/SESSION-11-REPORT.md`, with the new-user findings, the visual QA answers
    (truth, clarity, context, presentation), screenshots, and the handoff to S12.

## 08 — Explicit non-goals

- New sources, claims, edges or entity records, except a correction the human approves.
- Metrics, shares, rankings, "critical" or "concentrated" labels, or any score (NG-11; S14–S15).
- A frontend framework, a charting library, a graph database, a database server or DuckDB
  without a recorded requirement (NG-07; H-2).
- Public deployment (NG-13: not before this slice passes its gates and the human decides).
- A second journey, a reusable component system or a design system (MA §16.1: "prove 2-3
  high-quality end-to-end infographic compositions before turning recurring patterns into
  reusable components").
- A chatbot or any text not generated from records or labelled as the Atlas's framing (NG-09).
- Editing the root documents, the taxonomies, the source policy, the schemas, migrated values or
  anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **Evidence:** Part A's rules; `claim-model.md` §13: a reader never sees a bare inference; RR-7:
  never "none".
- **One home:** the page holds no fact; it is generated from `data/` and every value on it has a
  home there. A generated file is never edited by hand.
- **Unknown ≠ zero:** gaps are drawn, named and explained.
- **Tooling:** standard library for `tools/` (D-003, D-026); vanilla HTML, CSS and inline SVG
  (CLAUDE.md §11); no runtime network request from the page (self-contained); browser checks in a
  scratch environment unless H-3 says otherwise; no new pinned dependency without an approved
  decision.
- **Visual:** MA §16.1's quality gate and the roadmap's four checks (truth, clarity, context,
  presentation); no organisation's branding copied.
- **Process:** L-02, L-04, L-08; gates run before any push.

## 10 — Agent responsibilities

As `docs/agents/contracts.md`, with Editorial and QA added by this session (H-5). The Change
Detector, Analyst, Client Output and Orchestrator stay inactive (the walk is a derivation the
build step computes and tests; it is not a metric).

| Agent | May write | Notes |
|---|---|---|
| Knowledge Architect | the design document, `decisions.md` (append), `contracts.md` and `roles.md` (the two new contracts, H-5) | visual specification; one-home rulings for the page |
| Data Auditor | `tests/`, `tests/fixtures/`, `tools/` | structured walk output; build step; page checks |
| Editorial | the page's framing text (in the build step's template), `docs/README.md`, baseline rows, `README.md` | no fact; only framing labelled as the Atlas's |
| QA | the report (browser findings, screenshots) | desktop, 375 px, keyboard, console |
| Verifier | the report | re-reads any anchor the page shows whose source bytes changed |

## 11 — Data and evidence rules

- **Canonical records:** read only. None created, except a correction approved by the human.
- **Allowed relationship types:** the five canonical edges; the recorded gaps of
  `edge-dataset.md` §1 as text, never as edges.
- **Required source tier:** unchanged; the page shows each citation's class and standing.
- **Provenance:** every mark resolves to an edge or record; every claim shown with its type,
  status, `verified_on` and citation.
- **Temporal:** each edge shows "no period in the claims" where it has none; each source shows
  its stated dates and access date; the page states the data commit it was built from.
- **Confidence:** no numeric values; evidence status and claim type only.
- **Unknown or unverified:** `not_researched` and the recorded gaps visible, named and explained.

## 12 — Implementation rules

**May create:** the design document; the build step and any standard-library helper under
`tools/`; the generated page and its stylesheet under one directory (H-2); tests and fixtures;
`SESSION-11-REPORT.md`.

**May modify:** `tools/navigate.py`, `tools/trace.py` (structured output, H-4);
`tests/test_navigate.py`, `tests/test_trace.py`; `decisions.md` (append); `contracts.md` and
`roles.md` (H-5); `docs/README.md`, baseline rows, `README.md`; `.github/workflows/ci.yml` only to
run the page checks if they are not unit tests (ask first).

**Approach:** generate, never hand-write, every value; test the generator and the output; keep the
first composition specific to this journey.

**Prohibited:** a hard-coded copy of any record, claim text or date in a template or test; a
stored path or `depends_on`; a framework, charting library or bundler; external fonts, scripts or
images fetched at runtime; a hand-written JSON Schema validator.

**Schema changes to accepted files:** none. If §06 needs one, stop (§16).

## 13 — Verification plan

- **At start:** the full suite and Gate 0, logged; base, `git branch -a`, `git ls-remote`; this
  prompt on `main`.
- **Environment:** a fresh virtualenv from the pins, installed set compared with the pins.
- **Fail first;** then the breaks of §07 task 7.
- **Data:** the page checks prove every value comes from `data/`; the rebuild is byte-identical.
- **Browser QA (H-3):** desktop and 375 px screenshots; keyboard-only path to every evidence
  panel; console free of errors; contrast measured for text and marks.
- **Visual QA:** the four questions (truth, clarity, context, presentation) answered in the report
  with evidence.
- **Human:** the new-user test of Part A.
- **CI:** reported separately from local results (L-08).
- **Not applicable:** performance beyond a single static page.

## 14 — Evaluation requirements

The report records decisions and rejected alternatives (the visual form, the gap encoding, the
build design, the browser-check approach); deviations; invalidated assumptions; new debt;
unresolved questions; the human's new-user findings verbatim; and whether the S11 gate is met.

## 15 — Acceptance criteria

1. The page answers the journey's question for the H100 and Trainium2, from the five canonical
   edges, and shows the TSMC → H100 gap and the `not_researched` suppliers.
2. Every mark, label, statement, anchor and date on the page resolves to its home in `data/`,
   checked in CI.
3. The page is generated by a tested, standard-library build step, and a rebuild from the same data
   is byte-identical.
4. No staging record appears; every `DERIVATION` is labelled and its reasoning reachable.
5. Every evidence panel is reachable by keyboard and nothing is available only on hover; the page
   is readable at 375 px; text contrast meets WCAG AA.
6. The page needs no network request to render, and no new pinned dependency was added without an
   approved decision.
7. Editorial and QA have contracts, and their work is checked (H-5).
8. The human used the journey as a new user; findings are verbatim in the report.
9. Tests and Gate 0 pass in a fresh virtualenv; CI observed or reported as not observed.
10. The report satisfies SPEC §5 and Part A; new decisions appended as `proposed`; the handoff to
    S12 names what the audit should examine first.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- the journey cannot be told without a fact the canonical data does not hold (show the gap; never
  add the fact);
- a visual encoding would need a value the records lack (a share, a count, a rank);
- the page would need a framework, library or external resource the human has not approved;
- a canonical value looks wrong when rendered (report it; correcting it is a Verifier and human
  matter);
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions taken before S11** (2026-10-02, at the end of S10; Claude's recommendation first
in each list). Do not ask them again; stop only if a condition cannot be met.

- **H-0 — the S10 review:** nothing open. D-089 to D-099 were accepted in S10.
- **H-1 — the journey:**
  - *(recommended)* the HBM dependency chain: H100 and Trainium2 → HBM → 3D die stacking, with
    Amazon's design, SK hynix's M16, the `not_researched` suppliers and the TSMC gap;
  - a company profile.
  - *Answer:* "yes and merge into main" (2026-10-02, to Claude's recommended S11).
- **H-2 — page technology:**
  - *(recommended)* a static page generated by a standard-library Python build step, with inline
    SVG and CSS, no libraries, written under one directory and checked in CI;
  - a hand-written page that reads the JSON at run time;
  - a charting library (e.g. D3) from a CDN.
  - *Answer:* "Static, stdlib build, inline SVG (Recommended)".
- **H-3 — browser QA:**
  - *(recommended)* in a scratch environment with the pre-installed Chromium and a scratch
    Playwright install, no repository dependency; screenshots and findings in the report;
  - Playwright added to the pinned test dependencies and run in CI.
  - *Answer:* "Scratch Playwright, no repo dep (Recommended)".
- **H-4 — structured output:**
  - *(recommended)* `tools/navigate.py` and `tools/trace.py` gain a JSON output that the build
    step reads, with tests;
  - the build step walks the files itself.
  - *Answer:* Claude's recommendation, as part of H-1's journey (no separate question).
- **H-5 — Editorial and QA contracts:**
  - *(recommended)* written in S11 as `proposed`, reviewed with the session's decisions;
  - left inactive, with the work done under the Data Auditor's contract.
  - *Answer:* "Contracts in S11, proposed (Recommended)".
- **Part A:** confirm as assembled, or amend; and where S11 runs.
  - *Answer:* "Confirm; new session (Recommended)": the prompt is merged to `main`, and S11
    starts in a fresh session from `main`.

## 17 — Deliverables

- the design document with the visual specification;
- the structured walk and trace outputs; the build step; the generated page;
- the page checks, tests and fixtures; browser-QA screenshots;
- Editorial and QA contracts;
- `decisions.md`: D-100 onward, `proposed`;
- `docs/README.md`, baseline rows, `README.md`, `contracts.md`, `roles.md`;
- `sessions/reports/SESSION-11-REPORT.md`.

## 18 — Handoff

S11's report must hand S12 (Data architecture audit; "Do not build new features during this
session unless needed for remediation"):

- **Completed work:** the journey, the page, its checks, the contracts.
- **For S12:** what the page revealed about the data model (IDs, relationship semantics,
  temporal correctness, provenance completeness, queryability), and whether the visual is
  derived from canonical data rather than duplicated presentation data.
- **Open issues:** the human's new-user findings not fixed; everything §04 inherits.
- **Recommended next decision:** the first audit question S12 should answer.
- **Files for S12 to read first:** the S11 report; the S11 design document; `edge-dataset.md`;
  the S10 report's list of what M3's audits should examine first.
