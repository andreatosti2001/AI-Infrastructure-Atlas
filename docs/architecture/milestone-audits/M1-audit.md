# M1 Milestone Audit — Domain + Evidence Foundation (S03–S06)

> **Records cited.** This is a process audit (PEF §4). The session reports and prompts it cites are kept in the
> private development archive, not in this repository (D-151); the decisions, documents and files it cites are here.

**Status:** ACCEPTED (human review of S07, 2026-10-01). Written in S07 as its first task (human answer H-5, 2026-09-30). It is a document only, with no code change.
**Date:** 2026-10-01
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4 ("At every major milestone") and
§12 (the Portfolio Reviewer's outputs).
**Milestone label:** M1 in `SESSION-ROADMAP.md` numbering (D-019): S03–S06. It is not MA §22
"portfolio M1" (Part 1, question 3).
**Written by:** Claude, playing the Portfolio Reviewer role. `docs/agents/roles.md` marks
that role inactive until S24, and it has no contract. Writing this audit is a recorded
deviation from `roles.md`, which the S07 prompt anticipated.

**Bases read.**

- `main` @ `14890d2`, which includes S03–S06, their reviews (`5b22515` is the last) and the
  S07 prompt.
- The S03–S06 prompts and reports, including every addendum; `decisions.md` D-022 to
  D-053; the M0 audit; `baseline.md`; `git log`.
- Sizes and counts are labelled "as measured at `5b22515`" (the S06 review commit, the
  last commit of M1). They are not tested, so they follow D-018 L-04 by label.

**Claim labels** (CLAUDE.md §6), as in the M0 audit:

- `FACT`: a file, line, commit or command output in this repository;
- `ATTRIBUTION`: what a session report says about itself, not re-measured here;
- `DERIVATION`: a count or comparison computed here from `FACT`s;
- `INTERPRETATION`: this audit's own reading;
- `IMPLICATION`: what follows for M2.

---

## Part 1 — M1 audit (PEF §4, eight questions)

### 1. What was intended

`SESSION-ROADMAP.md` M1, with each session's gate (`FACT`, the roadmap text):

| Session | Mission | Gate or critical test |
|---|---|---|
| S03 | the minimum canonical entity vocabulary | "No entity should exist merely because it is convenient for the UI" |
| S04 | precise semantic relationships, preventing inference from co-occurrence | "Every relationship has a clear semantic definition and evidence expectation" |
| S05 | a source hierarchy for industrial technology research | "Every material claim type has a preferred source class" |
| S06 | claim-level provenance, verification state and temporal metadata, before dataset scale-up | "The system can answer: 'What exactly supports this relationship?'" |

The M0 audit (Part 2, question 8) carried four things into M1: the frozen non-goals, the
D-018 commitments L-01 to L-09, the v1 concept classification (M0 Part 4), and the blocked
sources and conflicts CON-01 to CON-05.

### 2. What was implemented

All `FACT`, as measured at `5b22515` unless a session report is cited:

| Session | Main artifacts | Decisions | Tests after the session (`ATTRIBUTION`, each report's final run) |
|---|---|---|---|
| S03 | `entity-taxonomy.md` (504 lines); `schemas/entities.schema.json` | D-022 to D-027 | 26 |
| S04 | `relationship-taxonomy.md` (637 lines); `schemas/relationships.schema.json` | D-028 to D-033 | 58 |
| S05 | `source-policy.md` (674 lines); the class vocabulary in `schemas/sources.schema.json`; one new source (S05-R1, NVIDIA's 10-K) | D-034 to D-043 | 85 |
| S06 | `claim-model.md` (551 lines); `schemas/claims.schema.json`; the source record; `data/sources.json` (24 records); `data/staging/claims.json` (10 claims); `tools/trace.py`; `docs/agents/` | D-044 to D-053 | 157 |

- **Decisions:** 32 (D-022 to D-053), all accepted at the human's reviews (`FACT`,
  `decisions.md` status lines).
- **Repository size by kind** (`FACT`, at `5b22515`): Python tests 2,812 lines; `tools/`
  355 lines; schemas 824 lines.
- **Canonical data at the end of M1** (`FACT`): 24 source records; 0 canonical claims;
  0 entity records; 0 relationship records.
- **Every gate was met "for review"** and then accepted by the human (`ATTRIBUTION`, each
  report's addendum). S06's gate is met on fictional fixtures for the relationship path,
  and on real claims for the claim path. No real relationship exists (D-053).

### 3. What changed, and why

| Change | From → to | Why | Record |
|---|---|---|---|
| FAB-03 "Foundry" | model concept → actor role `foundry_operator` | TQ-04 made the foundry a business model | D-024 |
| MA §5.1's `jurisdiction` field | one field → `incorporated_in`, `headquartered_in`, and `located_in` on facilities | three different facts | D-023, entity taxonomy §4.5 |
| MA §6.1's `CloudProvider`, `EquipmentSupplier`, `DataCentre`, `Fab`, `PackagingFacility` | types → roles or facility kinds | one identity test each (R-1, R-3) | D-023 |
| Composition | `part_of` (S03 prose) → `has_part` | the direction convention | D-029, S04 Deviation 4 |
| Source ranking | D-015's tiers T1–T6 and MA §10's order → a preference matrix per claim type, no global rank | no single order fits every claim type | D-036 |
| Evidence status | MA §10's `direct` → `supported`; `derived` dropped | `direct` read like standing; `derived` duplicated a claim type | D-046 |
| Filings | "regulator first" (implicit) → the filer's own copy | EDGAR refused plain requests | D-042 |
| Non-goals | 13 → 14 (NG-14, no external API) | a session non-goal made permanent through D-021's procedure | D-043 |
| Source register | live → frozen, migrated into source records | one live home per source class | D-050 |
| Prompts | the short human prompt (S03) → Part A plus an 18-section Part B (S04 onward) | S03's handoff; S04's report found that Part B removed design questions | S04 report, Process lessons |

### 4. Which assumptions failed

Each is `FACT` about what the session found, with its consequence recorded where it was
found. No accepted artifact was rewritten to hide it.

- **"Not publicly determinable" for HBM-06** (domain map §8). Under ER-3 the H100's HBM
  supplier is `not_researched`: one preferred class was refused, and no memory maker's filing
  was read (D-049; `claim-model.md` §8).
- **"The H100 is fabricated using the TSMC 4N process"** (FAB-05, repeated in S04 §12 and
  S05 §13–§14). The sentence names the GH100 die that powers the H100. This was found only
  by reading the sentence in S06.
- **That a registered locator stays valid.** SRC-006's bytes and heading changed between
  S01 and S06.
- **That primary sources and the regulator are reachable.** EDGAR refused (S05-A1). JEDEC,
  TSMC, Samsung and others had refused in S01 (`source-register.md`, "Not retrievable").
- **That "primary" is a class.** It is a relation between a source and a claim (SP-3,
  D-035).
- **That a prompt committed on a session branch reaches `main`.** The S04 prompt did not. From S05, each prompt is on `main` before the session starts.

### 5. Which shortcuts were taken

- PDF text extraction with `pypdf` in a scratch virtualenv (S05 Deviation 4, S06
  Deviation 2). It is not a repository dependency.
- S05-R1's anchors are verified by hand only. Its full text is outside the repository.
- The register migration is a function inside a test (`migrated_records()`), because S06
  allowed only one new command in `tools/`.
- Markdown tables in documents are parsed by the tests, with width assertions.
- Test helpers are imported across test modules (S04 Deviation 3, kept at the S04 review).
- The trace reads entities and relationships from `--records FILE`, because their layout
  was S07's and S10's to choose.

### 6. What technical and research debt was created

Open at the end of M1 (`FACT`, each report's debt section, checked against `main`):

| Debt | Created | Owner named |
|---|---|---|
| V-1 to V-10 not built; no record-level `validate-data` | S04, S06 | S07 (entities), S10 (relationships) |
| `validate-freshness` not built | S05, S06 | S07 |
| `publisher_entity` `not_researched` for 16 company sources | S06 | S07 |
| VD-11 covers only S01 and S05 anchors | S06 | S07, by decision |
| The ten seed claims have no human verdict | S06 | the human |
| The `source-policy.md` §2 class table and the §7 matrix can disagree with no test failing | S05 | none |
| SRC-023 not re-read; a newer edition to check | S05 | the first session that cites it |
| Kind constraints on relationship endpoints documented, not enforced | S04 | S10 (V-2) |
| The placeholder ban is a word list | S04 | V-9 |
| ISO 3166-1 not registered | S03, S05 | S07 |
| S01's weekly gate not declared | S01 | the human |
| M0 Part 4 shows FAB-03 under its old class (recorded in taxonomy §5) | S03 | none: accepted artifacts are not rewritten |

### 7. What was removed or rejected

The main rejections, each with its decision. Every decision also lists its own.

- **Types:** a separate Equipment type, a `hyperscaler` role, an Organisation supertype,
  brand and product-family records, a layer field (D-022 to D-024; taxonomy §8).
- **Inference:** roles derived from relationships (D-024); a taxonomic `is_a` edge (D-025);
  `depends_on` as a stored edge (D-029, D-030).
- **Evidence:** a global source ranking (D-036); numeric confidence anywhere (D-028, D-046);
  a `verified` field (D-048); a staging flag on one claims file (D-048); a separate
  search-record kind (D-049).
- **Engineering:** `tools/validate_data.py` importing `jsonschema` (D-051); full contracts
  for every role (D-052); a graph or database layer (D-053, NG-07); an external API (D-043).
- **Access:** declaring an identity to EDGAR (D-042); any circumvention (D-039, RA-2).

### 8. What should be carried into M2

- **The pipeline, as built:** source record → staged claim → verified claim → human review
  → canonical claim → record. M2 is the first milestone in which records rest on it.
- **The record-level checks** S06 defined and did not build (V-1 to V-10, freshness). Each
  arrives with the first records it checks (L-05, L-09).
- **The S06 reading lesson:** machine checks confirm that an anchor exists. Only reading the
  sentence judges the wording. M2 adds many new anchors with no machine-checkable home, so
  this matters more (H-6 of S07).
- **The open debt** in question 6, with its owners.
- **The access pattern:** many company and standards hosts refuse plain requests. M2 needs
  RA-4 manual retrievals by the human, planned per session, not discovered late.

---

## Part 2 — Process and outcome findings (PEF §12)

### 2.1 Process findings

| ID | Finding (`INTERPRETATION`) | Evidence |
|---|---|---|
| P-1 | **The D-018 commitments held through M1.** No agent runtime was built (L-01). Every check named a gate runs in CI (L-02). Every report from S03 records its base (L-03). Prose counts are tested or labelled (L-04). Claim type and evidence status are separate fields from the first claim schema (L-06) | `FACT`: no runtime code in `tools/`; `.github/workflows/ci.yml`; each report's header; `claims.schema.json` |
| P-2 | **Fail-first runs and deliberate breaks found real defects every session.** S03 found a parser that skipped rows. S04 found a dropped table column. S05 found a "present somewhere in the row" test that passed a wrong pairing. S06 found state leaking between trace calls | `ATTRIBUTION`: each report's Process lessons |
| P-3 | **Reading found what tests could not.** The GH100 wording, the IDC chain behind an LBNL sentence, three contradictions between the policy's class table and its matrix, and two wrong locators of S06's own were found by the Verifier reading, not by a test | `ATTRIBUTION`: S05 and S06 reports |
| P-4 | **One regression of an M0 anti-pattern.** A-6 (work stranded off `main`) recurred once: the S04 prompt sat on an unmerged commit. It was caught by Gate 0 and fixed by a rule (prompts on `main` before the session) | `FACT`: S04 Deviation 1; S05 to S07 prompts merged before their sessions |
| P-5 | **Review throughput is the bottleneck.** Four sessions and their reviews ran on one day (2026-09-30). Every design decision was accepted. The one content review asked of the human, the ten seed-claim verdicts, has not been given | `FACT`: `git log` dates; `decisions.md` status lines; S06 review addendum |
| P-6 | **Checks outgrew data in M1, by design, with a risk attached.** At the end of M1 there are 2,812 lines of tests (as measured at `5b22515`), 24 source records and no canonical claim or entity. Each check was tried on real sources (L-09), so this is not A-1. But in M2, records must now grow faster than checks | `DERIVATION`: the measures in question 2 |

### 2.2 Outcome findings

| ID | Finding (`INTERPRETATION`) | Evidence |
|---|---|---|
| O-1 | **The model is coherent and one-home.** Entity, relationship, source and claim shapes each have one home. Vocabularies are checked against the documents that explain them | `FACT`: the consistency tests in `tests/test_*_taxonomy.py`, `test_source_policy.py`, `test_claim_model.py` |
| O-2 | **Provenance works end to end on real sources, but only to the claim.** `tools/trace.py` prints every seed claim down to its source, class, locator, anchor, standing and the bytes read. No real record exists to trace from | `FACT`: `tests/test_trace.py`; D-053 |
| O-3 | **Unknown is explicit everywhere it can be recorded.** No null is accepted, and the HBM-06 case shows ER-3 downgrading a premature `not_publicly_determinable` | `FACT`: schemas; D-049 |
| O-4 | **The evidence base is thin and mostly company-published.** 16 of the 24 source records are company-published, and one is a filing (as measured at `5b22515`). M2's company records need the filing class most | `FACT`: `data/sources.json` |
| O-5 | **Maintainability cost is rising in the tests.** Markdown table parsing and cross-module test imports are each debts recorded by the sessions that created them | `ATTRIBUTION`: S03 to S06 debt sections |

### 2.3 Maturity per dimension (PEF §3; 0 Absent · 1 Ad hoc · 2 Defined · 3 Controlled · 4 Exemplary)

Compared with the M0 baseline (M0 audit Part 3). Each rating is `INTERPRETATION`, on the
evidence given.

| Dimension | M0 process / outcome | M1 process | M1 outcome | Evidence |
|---|---|---|---|---|
| Data architecture | 2 / 0 | 3 | 2 | Schemas, decisions and a tested migration (VD-9). No entity or relationship record, so the outcome is defined, not controlled |
| Content & review | 2 / 2 | 3 | 2 | Verifier re-reads; anchors machine-checked; deliberate breaks. No claim is human-reviewed, so nothing real is canonical except migrated sources |
| Agent architecture | 1 / 0 | 2 | 2 | Five MA §12 contracts, each with a CI gate; no runtime, by design (NG-08) |
| Analytical depth | 0 / 0 | 0 — not started | 0 — not started | S14–S16 |
| Code / engineering | 2 / 2 | 3 | 2 | Fail-first and breaks every session; 157 tests; but parsing and import coupling (O-5) |
| Product / user value | 2 / 0 | 2 | 1 | The trace answers "what supports this?" on real claims, from the command line only |
| Reproducibility | 2 / 1 | 3 | 2 | Deterministic migration; per-record dates and hashes. Full texts of filings and PDFs stay outside the repository |

**Regressions since M0:** none in the ratings. One process regression (P-4), fixed.

### 2.4 High-value improvements, and improvements rejected

- **High value for M2** (`IMPLICATION`):
  1. records that real users can trace from an entity, starting with S07's companies;
  2. the human's content review inside the session that produces the claims (S07's H-3),
     so verdicts do not pile up (P-5);
  3. RA-4 lists prepared at the start of each session that needs blocked hosts.
- **Rejected for now:**
  - extracting test helpers into a shared module. The cost is recorded (O-5), and no defect
    has come from the imports yet;
  - a structured form of the `source-policy.md` §2 class table. It would be a second home
    for the matrix's content unless the matrix is generated from it, which is a larger
    change than any session has needed.

### 2.5 Learning outcomes (PEF §10)

**What capability did M1 make demonstrably stronger?** (`INTERPRETATION`)

- **Evidence methodology:** a source policy that separates class, standing, claim type and
  evidence status, with worked examples from real sentences (`source-policy.md` §13–§14).
- **Data modelling:** entity, relationship and claim schemas, each with one home per fact
  and explicit unknowns.
- **Software engineering:** schema-behaviour tests with mutation fixtures, consistency tests
  against the governing documents, and deliberate breaks in every session.

M1 did not yet show industrial research depth: the domain facts are S01's, and the first
new company evidence arrives in S07.
