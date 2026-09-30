# SESSION-06 Report — Evidence/claim system

- **Session:** S06 · **Type:** IMPLEMENTATION · **Milestone:** M1 — Domain + Evidence Foundation
- **Date:** 2026-09-30
- **Prompt:** [`sessions/prompts/S06-PROMPT.md`](../prompts/S06-PROMPT.md) (Part A human, Part B
  SPEC §2 detail, with the human's answers H-1 to H-4 in §16). The uploaded copy was
  compared with the file on `main`: identical.
- **Branch:** `claude/new-session-o16fd6`, at `main` @ `11185a6` (the PR #9 merge, which
  brought the S06 prompt to `main`)
- **Base at start** (D-018 L-03):
  - `git branch -a` listed:
    - `claude/new-session-o16fd6` (local, at `11185a6`);
    - `main`;
    - `remotes/origin/claude/new-session-o16fd6`;
    - `remotes/origin/main`.
  - `git ls-remote` showed `main` at `11185a6` and five other branches, none carrying work
    missing from `main`:
    - `claude/sleepy-bell-mv44c5` (`11185a6`, the same commit);
    - `claude/atlas-architecture-baseline-jow618` (`26acdf9`), merged;
    - `claude/beautiful-albattani-gyg4nw` (`ace06f0`), merged;
    - `claude/magical-galileo-vwn13j` (`ce5b881`), merged;
    - `claude/youthful-allen-rtfdu8` (`e23965c`), the S04 prompt commit, whose content S04
      cherry-picked.
  - The S06 prompt was on `main` before the session started, so S04's Deviation 1 did not
    recur.

## Mission outcome

**Delivered for human review.** Claim-level provenance works on real sources, end to end:

- 24 canonical source records, migrated from the register and S05;
- 10 seed claims in staging, covering all five claim types and verified against the
  sources re-read in this session;
- `validate-data` in CI;
- a trace command that answers "what supports this?".

Nothing real is canonical except the source records.

| Deliverable | Where | Status |
|---|---|---|
| Claim model: MA §10 reconciled, type × status tables, citations, `verified`, staging and canonical, search record, migration, `validate-data`, trace, explainer, review sheet | `docs/architecture/claim-model.md` | proposed (D-044 to D-053) |
| Claim schema | `schemas/claims.schema.json` | proposed |
| Source record around the unchanged class vocabulary | `schemas/sources.schema.json` | proposed (D-050); every vocabulary line byte-identical |
| Migrated source records | `data/sources.json` | canonical by deterministic migration (class B); VD-9 proves it exact |
| Seed claims | `data/staging/claims.json` | verified by the S06 Verifier; **not reviewed by the human** |
| `validate-data` | `tests/test_data_schema.py`, `tests/test_data_integrity.py` | in CI (H-4) |
| Trace | `tools/trace.py`, `tests/test_trace.py` | in CI |
| Agent roles and contracts | `docs/agents/roles.md`, `docs/agents/contracts.md` | proposed (D-052) |

**Roadmap gate, "The system can answer: 'What exactly supports this relationship?'":**
**met for review, not approved.**

- The path relationship → claims → citations → sources works on a fictional relationship.
- The path claim → sources works on every real seed claim.
- No real relationship exists before S10, so the full real path cannot yet be shown
  (`claim-model.md` §12).

**Restated contract** (operating-contract step 6, given before any file was written):

- **Mission:** claim-level provenance, built from these parts:
  - claim and source records;
  - the register migrated into source records;
  - validation in CI;
  - a trace command;
  - agent contracts;
  - 5 to 10 seed claims in staging, for the human to test.
- **Scope:** the paths in Part B §12, with the human's answers. H-1: a staging seed. H-2:
  `data/sources.json` plus `data/staging/claims.json`. H-3: five full contracts. H-4:
  `validate-data` as CI tests.
- **Non-goals:** Part B §08. No entity, relationship or event record; no runtime; no score;
  no change to the S03 or S04 schemas or to the class values; no canonical claim.
- **Acceptance:** Part B §15.
- **Plan:**
  1. schemas, fixtures and behaviour tests;
  2. data, consistency and contract tests, fail-first;
  3. migration, seed claims, claim model, decisions and contracts;
  4. the trace and its tests;
  5. deliberate breaks;
  6. docs rows, report, commit and push.

  The plan held. The Verifier's re-read of the six seed sources ran before step 1, because
  the seed claims' wording depended on it (Deviation 1).

**Acceptance criteria** (Part B §15):

| # | Criterion | Result |
|---|---|---|
| 1 | Claim type and evidence status are separate required fields; values defined once; no numeric confidence | met: schema; `test_claim_model.py` VocabularyTests; `test_claim_schema.py` numeric test |
| 2 | Every MA §10 claim type has one disposition, machine-checked against MA | met: `claim-model.md` §2, parsed against MA's list. MA's evidence statuses too (§3) |
| 3 | Type × status rules as a table, enforced by tests | met: §4. The schema is probed for every type × status and compared with the table; the data checks read the status table (VD-6, VD-8) |
| 4 | A `FACT` without a citation, a `DERIVATION` without inputs, a citation without a locator or source fail | met: fixtures `fact_without_citations`, `derivation_without_inputs`, `citation_without_locator`, `citation_without_source`; breaks 2 and 3 |
| 5 | Every SRC-001 to SRC-023 and S05-R1 is one source record with the class from §8.1/§8.3, checked against the register | met: VD-9; breaks 4, 5 and 10 |
| 6 | Register marked frozen; one live home per class | met: register status line; §8.1 note; `test_source_policy.py` reads classes from the data |
| 7 | The `validate-data` checks run in CI | met in the existing unit-test step. CI: see the addendum (L-08) |
| 8 | The trace answers on a fixture relationship and on the seed claims, with source, class, locator, anchor, standing and dates; its limits are stated | met: `test_trace.py`; outputs below; limits in `claim-model.md` §12 |
| 9 | The meaning of `verified` in a decision; D-015's status line at review | decided in D-048; D-015's status line is left for the human's review, as Part B says |
| 10 | Contracts in MA §12 format for H-3's roles, each with a gate CI runs | met: `test_agent_contracts.py` |
| 11 | Seed claims cover the five types; every anchor verbatim at its source; none canonical before review; review sheet exists | met: coverage test; VD-11 against the domain map, plus the Verifier's re-read below; all `not_reviewed`; the sheet is below and in `claim-model.md` §14 |
| 12 | No change to accepted schemas or vocabulary values; no scores; no runtime | met: `entities.schema.json` and `relationships.schema.json` untouched; the class lines are byte-identical |
| 13 | Tests and Gate 0 pass in a fresh virtualenv; CI observed or reported | met locally in two fresh venvs; CI in the addendum |
| 14 | Report satisfies SPEC §5 and Part A; decisions appended as `proposed` | this report; D-044 to D-053 |

**No stop condition fired.**

- No claim or source field needed a change to an accepted vocabulary or to the
  `claim-<slug>` format.
- Every register row migrated without an invented value. Missing authors are
  `not_researched`, missing dates are `undated`, and company publishers are
  `not_researched`.
- Every seed anchor was found verbatim at its locator, and every source was re-read.
- MA §10 reconciles without an edit.

## Files changed

Added:

- `docs/architecture/claim-model.md`
- `docs/agents/roles.md`, `docs/agents/contracts.md`
- `schemas/claims.schema.json`
- `data/sources.json`, `data/staging/claims.json` (the first data directory, D-005, H-2)
- `tools/trace.py`
- `tests/test_claim_model.py`, `tests/test_claim_schema.py`,
  `tests/test_source_record_schema.py`, `tests/test_data_integrity.py`,
  `tests/test_data_schema.py`, `tests/test_trace.py`, `tests/test_agent_contracts.py`
- `tests/fixtures/claims.json`, `tests/fixtures/source_records.json` (fictional; source IDs
  `src-901` to `src-905`, claim IDs `claim-fixture-…`)
- `sessions/reports/SESSION-06-REPORT.md`

Modified:

- `schemas/sources.schema.json`: the root became the source record. The three header lines
  changed; the vocabulary lines are byte-identical (checked with `git diff`).
- `tests/test_source_schema.py`: validates class values against `$defs/vocab_source_class`,
  because the root is now the record. The migration requires this change.
- `tests/test_source_policy.py`: `mapped_class()` reads classes from `data/sources.json`,
  the live home. The migration requires this change.
- `docs/architecture/decisions.md`: D-044 to D-053 appended, all `proposed`.
- `docs/research/source-register.md`: the status line only (FROZEN).
- `docs/research/source-policy.md`: status notes on §8.1 and §16 only.
- `docs/README.md`, `docs/architecture/baseline.md` (dated state rows, §3, §4, §5),
  `README.md` (status, layout, commands).

Not modified:

- the root documents, including MA §10;
- `domain-map.md`, `M0-audit.md`, both taxonomies;
- `entities.schema.json`, `relationships.schema.json`;
- `.github/`, `requirements-test.txt`, `tools/validate_repo.py`, `PROMPT-REGISTRY.md`;
- anything in `Eu-Digital-Policy`, which was not opened.

## Data changed

The first data records in the repository. Counts were produced by script over the committed
files (L-04), as measured at this commit:

| Measure | Count |
|---|---|
| source records | 24: 23 register rows (`src-001` to `src-023`) and S05-R1 (`src-024`) |
| sources by class | `company_marketing` 9, `company_technical_documentation` 5, `research_report` 3, `government_publication` 2, `policy_research_brief` 2, `industry_association` 1, `company_press_release` 1, `company_filing` 1 |
| `publisher_entity` | `not_researched` 16 (company publishers, for S07), `not_applicable` 8 |
| stated dates | `published` 12, `undated` 5, `published` + `modified` 3, `last_updated` 2, `modified` 1, `signed` 1 |
| authors recorded as text | 7 (the rest `not_researched`) |
| migration overrides | 1 (SRC-005's publisher, per `source-policy.md` §2 and §8.1) |
| seed claims (staging) | 10: `ATTRIBUTION` 5, `FACT` 2, `DERIVATION` 1, `INTERPRETATION` 1, `IMPLICATION` 1; all `supported`, all `not_reviewed` |
| citations | 7: standing `party` 3, `originator` 3, `reporter` 1 |
| registered sources cited | 6: `src-001`, `src-003`, `src-006`, `src-017`, `src-020`, `src-021` |
| canonical claims | 0 (`data/claims.json` does not exist) |
| schema fixtures | claims: 15 valid, 67 invalid; source records: 5 valid, 32 invalid |

**Schema:**

- the claim record (new);
- the source record around the S05 vocabulary.

The accepted S03 and S04 schemas are unchanged. The class values are unchanged.

## Tests run

Python 3.11.15. All commands ran locally from the repository root. "venv" means a fresh
virtualenv built from `requirements-test.txt` in the session scratchpad.

| Command / check | Result |
|---|---|
| `python -m unittest discover -s tests` at start, venv | OK (85 tests) |
| `python tools/validate_repo.py` at start | `Repository integrity: OK` |
| venv `pip freeze` vs the pins, sorted, at start and in a second fresh venv at the end | installed set = pinned set, both times |
| Schema behaviour tests, first run | OK. Every invalid case's located error was printed and read: all 99 fail at, under or beside their pointer, for the reason named. Two cases (`interpretation_disputed`, `attribution_disputed`) showed first a secondary error (`disputed_with` required); both also fail on the type's status enum, which is their point |
| **Fail-first:** full suite before the data, `claim-model.md`, contracts and decisions existed | 147 tests: 14 failures, 41 errors. All traced to the missing files: cited decisions D-044 to D-053, the register status line, the §8.1 note, the §4 tables, `data/`, `docs/agents/`. The claim-schema fixture tests already passed |
| Tests caught while writing the document | the §9 table had two "not migrated" cells naming no field; three non-anchor phrases in §13 were in straight quotes, and the anchor test rejected them; `tests/test_trace.py` was named as a gate before it existed. All fixed |
| **Deliberate breakage**, 18 breaks, each in a fresh scratch copy | **first run: 18 caught**, but break 1 also failed a test it should not have: a trace defect (below). **Final run, after the fix: 18 of 18 caught** |
| Defect found by the breaks | `tools/trace.py` kept unresolved references across calls, so one failed trace made the next report failure. `trace()` now resets them. A new test fails without the fix and passes with it |
| `python -m unittest discover -s tests -v`, final, second fresh venv | OK (157 tests: 85 before, 72 new) |
| The same, final, system Python | OK (157). This container's system Python has `jsonschema` 4.26.0, the pinned version, unlike S05's container |
| `python -m unittest discover -s tests -p "test_data*.py"` (`validate-data`) | OK (19 tests) |
| `python tools/validate_repo.py`, final, with this report present | `Repository integrity: OK` |
| `python tools/trace.py <id>` on 2 fixture relationships and all 10 seed claims | exit 0 each; output below |
| CI result | not observed when this report was committed; see the addendum (L-08) |

**The 18 breaks:**

1. A claim cites a source ID that does not exist.
2. A `FACT` claim with no citation.
3. A `DERIVATION` that cites no input claim.
4. A register row missing from the migrated sources.
5. A migrated source whose class differs from §8.1.
6. A seed-claim anchor changed by one word.
7. A claim-type value added to the schema without a table row.
8. A staging claim presented as canonical.
9. An accepted verdict written on a staging claim.
10. A frozen register row edited.
11. An evidence status added without a table row.
12. MA §10 gains a claim type.
13. The §4 table allows disputed `ATTRIBUTION` while the schema does not.
14. A supported derivation over a `partial` input.
15. A `FACT` citation with `reporter` standing.
16. A company publisher marked `not_applicable`.
17. A contract gate naming a test that does not exist.
18. An input claim deleted.

Breaks 1 to 8 are Part B §07 task 11's.

Not applicable: browser, accessibility, performance.

## Evidence added/retired

- **No new source.** No web search was used. The register is frozen by this session, so a
  new source would have become a source record. None was needed.
- **Verifier re-read, 2026-09-30T21:29Z.** The six registered sources the seed claims cite
  were re-retrieved over HTTPS (RA-1) and their text was extracted locally. Each anchor was
  searched in the text and read in its sentence and paragraph:

  | Source | Bytes vs S01 register | Anchor | Locator |
  |---|---|---|---|
  | SRC-001 | same (`7b0c1a9fdfc6`) | found once, p.6 | as registered |
  | SRC-003 | same (`0f80b4fa1650`) | found once, p.4, footnote * | as registered |
  | SRC-006 | **changed** (S01 `ed8dc6f2a694`, now `fd13c05a1586`) | found once | the register's heading "H100 GPU hardware architecture in-depth" is not on the page; the sentence sits under "NVIDIA H100 GPU architecture in-depth" |
  | SRC-017 | same (`ec896b9cb6bc`) | found once, opening paragraph | as registered |
  | SRC-020 | same (`1f172d6e220c`) | found once, "Availability Zones" | as registered |
  | SRC-021 | same (`1108b5a0f829`) | p.16 and p.18, each found once | the sections are §3.1.2 "AI Accelerator Shipments"; p.31 reference list read |

- **Findings from the re-read** (recorded, not patched):
  - **SRC-006 names the GH100, not the H100.** The sentence reads "The full GH100 GPU that
    powers the H100 GPU is fabricated using the TSMC 4N process customized for NVIDIA".
    - FAB-05, `relationship-taxonomy.md` §12 and `source-policy.md` §13–§14 all
      paraphrase it as "the H100 is fabricated…", which is slightly more than the source
      says.
    - The seed claims name the GH100. The consequence for S04 is nil: `fabricates` is
      "wafer fabrication of the target product's dies", and the GH100 is the H100's die.
  - **SRC-021 p.18 is second-hand, as S01 and S05 recorded.** The sentence is in LBNL's
    own voice, but it sits in a paragraph that reports what "IDC analysts advised us" and closes "(IDC, 2026)".
    p.31 identifies "(IDC, 2026)" as a "Direct communication with … Executive Analyst …
    [Personal communication]". "The market" is the high-end GPU market of that paragraph.
  - **My own locator errors, caught in the Verifier pass.** I first wrote SRC-021's section
    as "§3.1 'Shipments'". It is "§3.1.2 AI Accelerator Shipments": I misread the end of
    that heading as a heading. Both locators were corrected before any review.
    A second re-read found that I had also described the p.18 paragraph as beginning "As a
    result, IDC analysts advised us"; it begins "As previously described". The locator now
    names the sentence itself.
  - **HBM-06 under ER-3** (`claim-model.md` §8): SRC-006 names HBM3 14 times (as measured)
    and no memory maker. Samsung's documentation was refused in S01, and no memory maker's
    documentation or filing was read. So the H100's HBM supplier is `not_researched`, not
    `not_publicly_determinable`.
- **Not re-read:** S05-R1 (no seed claim cites it) and the other 17 registered sources (no
  seed claim cites them). SRC-023 is still not re-read (S05 debt).
- **Retired:** none. The register is frozen, not deleted. "Retrieved but not cited",
  "Not retrievable" and S05-A1 stay as history (`claim-model.md` §9).

## Decisions made

| ID | Subject | Status |
|---|---|---|
| D-044 | The claim record: one proposition; records → claims; row derived; `claim-<slug>` kept | proposed |
| D-045 | Claim types: the CLAUDE.md labels; MA §10 reconciled | proposed |
| D-046 | Evidence status vocabulary; type × status rules; `disputed` for factual contradictions only | proposed |
| D-047 | Citations: locator, verbatim anchor, standing, chain, bytes read | proposed |
| D-048 | `verified` confirmed and extended; staging vs canonical; the human's review (H-1, H-2) | proposed |
| D-049 | The `not_publicly_determinable` search record; HBM-06 applied by hand | proposed |
| D-050 | The source record; `src-NNN`; the register migrated and frozen | proposed |
| D-051 | `validate-data` as CI tests (H-4); no `validate-freshness` code yet | proposed |
| D-052 | Agent roles and contracts (H-3) | proposed |
| D-053 | The trace command; the S06 gate met for review | proposed |

**MA §10 reconciliation** (`claim-model.md` §2–§3):

- **Claim types.** Fact, derived, attributed and interpretation map directly. Critique and
  forecast depend on the speaker. Law / normative text is reserved (S17).
- **Evidence statuses dropped or renamed:**
  - `derived` is dropped: it duplicates `DERIVATION`;
  - `direct` becomes `supported`: "direct" reads like standing, and cannot describe a
    derivation.
- **Kept:** `partial`, `context_only`, `unverified`, `disputed`, with `disputed` narrowed to
  factual contradictions.

**Main rejected alternatives** (each decision lists its own):

- a claim that lists the records it supports, or stores its matrix row;
- a numeric confidence;
- a `verified` field;
- one claims file with a staging flag;
- MA's `source-001` IDs, or keeping `SRC-001`;
- company IDs in `publisher_entity` before S07;
- `tools/validate_data.py` importing `jsonschema`;
- `validate-freshness` code now;
- full contracts for all roles.

## Deviations

1. **Verifier re-read before the schema work.**
   - Part B §05 expected no external research. §13 requires the Verifier to re-read every
     seed anchor at its locator.
   - The six registered sources were re-retrieved first, because what they say decided the
     claims' wording (GH100, the IDC chain).
   - No new source was added.
2. **PDF text extraction** used `pypdf` in a scratch virtualenv, as S01 and S05 did. It is
   not a repository dependency. The final runs used a second clean venv built only from
   the pins.
3. **Ten seed claims, not the prompt's full candidate list.**
   - Part B §06 q12's candidates, plus the input claims an interpretation and an
     implication need, came to eleven.
   - The SK hynix HBM4 plan (an intention, ER-8) was left out to stay within ten. ER-8 is
     illustrated in `source-policy.md` §13 example 3.
   - No seed claim cites S05-R1, so every anchor is machine-checked against the domain map
     and none rests on a hand check only.
4. **One claim type differs from the domain map's label.**
   `claim-nist-cloud-location-independence` is `ATTRIBUTION`, because a source's definition
   is that source's (`source-policy.md` §10.1). DC-04 labels the NIST material `FACT`. It
   is flagged for the human in the review sheet. The domain map is not edited.
5. **Test and fixture files.**
   - Seven new test modules, rather than a smaller set. Part B §12 allows tests and
     fixtures "for all of the above".
   - The migration function lives in `tests/test_data_integrity.py`, because §12 allows
     only one new command in `tools/`.
6. **The trace takes `--records FILE`** rather than a fixed path for entities and
   relationships. Their layout is S07's and S10's to design (D-005).
7. **Part A and Part B, both followed.** Part A lists four claim labels; CLAUDE.md §6 adds
   `ATTRIBUTION`, and all five are used, as Part B §09 directs.

No part of Part A or Part B was skipped.

## Debt introduced/resolved

**Introduced:**

- **VD-11 covers only anchors from S01 and S05 readings.** An anchor from a new retrieval,
  or from a manual one (RA-4), has no text in the repository to check against. VD-11 fails
  it until a decision says how such anchors are recorded (handed to S07).
- **The migration is frozen in a test.** A later correction to a migrated value, such as a
  title, needs a decision and a change to `migrated_records()`, by design.
- **The type table is enforced twice:** by the schema's `allOf` branches, and by the
  document's §4. A probe test keeps them equal, so it is one checked overlap, as in
  `relationship-taxonomy.md` §2.
- **More Markdown parsing:** the claim model's §2, §3, §4, §9 and §11 tables, MA's two
  lists, CLAUDE.md's role list, and MA §12's field block. Each parse asserts its width.
- **`publisher_entity`** is `not_researched` for 16 sources (as measured), pending S07.
- **V-10 and the search-completeness check** are defined but not built.
- **Cross-module test imports** continue (S04 Deviation 3), now with a shared
  `REGISTRY`/`check_mutations` in `test_source_record_schema.py`.

**Resolved:**

- D-010 (agent contracts), pending review.
- D-015's second part: confirmed and extended by D-048, pending review.
- The S05 handoff: the source record, the claim fields, the migration, and the meaning of
  `verified`.
- `baseline.md` §5: `validate-data` exists for sources and claims.
- The register is migrated and frozen; each source's class has one live home.

## Unresolved issues

### Evidence gaps

- **Assumptions invalidated** (the domain map is not edited; later sessions act on them):
  - **HBM-06 / DEP-01:** the HBM supplier per accelerator is `not_researched` under ER-3,
    not `not_publicly_determinable` as domain map §8 lists it (`claim-model.md` §8).
  - **FAB-05 and its S04/S05 restatements:** SRC-006 speaks of the GH100 die that powers
    the H100, not the H100 itself.
  - **SRC-006's locator** has changed with its bytes. Its current heading is recorded on
    the claim, and the register keeps S01's.
- **Carried, unchanged:**
  - S05-R1's anchors are hand-verified only;
  - SRC-023 is not re-read, with a 2026 successor to check;
  - the blocked primary sources (JEDEC, TSMC, Samsung, EDGAR and others);
  - CON-01 to CON-05, preserved;
  - ISO 3166-1 is not registered;
  - the §2 class table vs the §7 matrix has no machine check.

### Human approvals required

1. **D-044 to D-053.** Approve or amend each. The consequential points:
   - `direct` → `supported` and `derived` dropped (D-046);
   - `disputed` only for factual contradictions (D-046);
   - source IDs `src-NNN` (D-050);
   - `publisher_entity` left to S07 (D-050);
   - no `validate-freshness` code yet (D-051);
   - the gate "met for review" (D-053).
2. **D-015's status line:** at acceptance of D-048, "superseded by D-048" for its second
   part.
3. **The seed claims:** the human's manual test (Part A). **No verdict has been given yet.**
   The review sheet is below. Each verdict goes verbatim into an addendum here, then into
   the claim's `review`. An accepted claim moves to `data/claims.json`.
4. **The data layout under `data/`** follows H-2. The first canonical claims file appears
   only after your verdicts.
5. **Still open from earlier sessions:** S01's weekly gate.
6. **Merging this branch:** no pull request has been opened.

## Process lessons

- **Reading the source changed the claims.** Machine checks confirmed every anchor. Only
  reading the sentence showed that SRC-006 is about the GH100, and that the LBNL sentence
  sits in an IDC-cited paragraph. The check that the anchor exists and the judgement that
  the wording does not exceed it are different acts, which is why D-048 keeps both.
- **The Verifier needs to verify its own session's locators too.** The Extractor's locator
  for SRC-021 was wrong twice (a section number, then the paragraph's opening words). Each
  second look caught one. Both were caught before review, and neither was visible to a
  test, because locators are free text.
- **Breaks test the tests' side effects as well.** Break 1 failed the right test and one
  wrong one. The wrong one exposed state leaking between trace calls. *Read which tests
  fail, not only that something fails.*
- **One function for migration and proof works because the breaks attack both sides.**
  Editing the register (break 10) and editing the data (breaks 4, 5, 16) are each caught,
  so the shared function is not tautological.
- **A probe test beats a structural diff for schema-versus-table agreement.** Comparing
  `allOf` branches with a table would test the schema's text. Probing every type × status
  tests its behaviour.

## Implications for the next session

**Handoff: S07, Company dataset (RESEARCH / IMPLEMENTATION).**

- **Completed work:**
  - the claim and source records;
  - 24 migrated sources;
  - 10 seed claims, `not_reviewed`;
  - `validate-data` (VD-1 to VD-13);
  - the trace;
  - five agent contracts;
  - tests.
- **For S07** (gate: "Every canonical company record has identity evidence and stable
  IDs"):
  - **How to cite.** A company's `identity_claim_ids` and each attribute assertion's
    `claim_ids` point to claims in the S06 shape.
    - Identity and `legal_name` should be `FACT` claims citing a `company_filing` with
      `party` standing, from the filer's own copy (D-042), with `filing_copy` recorded.
    - These are the matrix rows `identity:company` and `attr:company.*`.
    - `roles` claims cite the filing's own words (e.g. S05-R1 p.8 "fabless").
  - **What to switch on:**
    - V-1 (references resolve, including `publisher_entity`);
    - V-9;
    - V-10 (the row's classes and standing, now that records exist);
    - `validate-freshness` for the `time_sensitive` company rows (D-040's 12 months).
  - **`publisher_entity`:** set it for the 16 company-published sources whose company S07
    creates. The migration test ignores that field, by design.
  - **Anchors from new retrievals:** decide how they are machine-checked, or accepted as
    hand-checked, before the first one (VD-11).
  - **Seed claims:** move accepted ones to `data/claims.json` on the human's verdicts.
- **Open issues:** the human approvals above; S01's weekly gate; S05 debt (the class table
  vs the matrix; S05-R1 hand-verified anchors; SRC-023 not re-read).
- **Recommended next decision:** the human reviews D-044 to D-053 and tests a few seed
  claims before S07, because S07's company records cite claims in this form.
- **Files for S07 to read first:**
  1. this report;
  2. `docs/architecture/claim-model.md`;
  3. `schemas/claims.schema.json`, `schemas/sources.schema.json`;
  4. `docs/research/source-policy.md` §7 (rows `identity:company`, `attr:company.*`) and
     §11;
  5. `docs/agents/contracts.md`;
  6. `docs/architecture/entity-taxonomy.md` §3.1 and §7;
  7. D-024, D-025, D-042 and D-044 to D-053.

**One next milestone:** S07 creates the first company records, each citing
first-hand identity claims in the S06 shape, with V-1 and V-10 switched on.

## Review sheet for the human's manual test

For each claim: open the URL, find the locator and the anchor, read the **whole sentence**,
and answer: **does it say this, and no more?** And: is the type right, that is, who is
speaking? `python tools/trace.py <claim ID>` prints the same fields. Snapshot as measured
at this commit:

| Claim | Type · proposed status | Evidence | Locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|---|
| `claim-h100-gh100-process-name` | `FACT` · `supported` | src-006 (SRC-006) · `company_technical_documentation` · standing `party` · <https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/> | section 'NVIDIA H100 GPU architecture in-depth' (the register's 'H100 GPU hardware architecture in-depth'), the sentence beginning 'The full GH100 GPU that powers the H100 GPU' | "fabricated using the TSMC 4N process customized for NVIDIA" | The sentence names the **GH100** die that powers the H100, not the H100. The domain map, S04 and S05 wrote "the H100 is fabricated…": slightly more than the source says. The page's bytes changed since S01, and its heading now reads "NVIDIA H100 GPU architecture in-depth" |
| `claim-tsmc-fabricates-h100-gh100` | `DERIVATION` · `supported` | input claims: `claim-h100-gh100-process-name` | — | — (see the reasoning in the trace) | Is ER-1 applied as written? Should it stay a `DERIVATION`? |
| `claim-asml-euv-unique-to-asml` | `ATTRIBUTION` · `supported` | src-017 (SRC-017) · `company_marketing` · standing `party` · <https://www.asml.com/en/products/euv-lithography-systems> | opening paragraph, the sentence beginning 'The technology, which is unique to ASML' | "The technology, which is unique to ASML, prints microchips using light with a wavelength of just 13.5 nm" | Is "unique to ASML" kept as ASML's claim, and not adopted? |
| `claim-lbnl-reports-idc-gpu-die-supply` | `ATTRIBUTION` · `supported` | src-021 (SRC-021) · `research_report` · standing `reporter` · <https://www.osti.gov/servlets/purl/3374245> | p.18, §3.1.2 'AI Accelerator Shipments', under 'Functional Unit for GPU Forecasts', the sentence beginning 'Because the market is currently constrained', in the paragraph that reports what 'IDC analysts advised us' and ends '(IDC, 2026)' | "the market is currently constrained by die supply" | The sentence reads in LBNL's voice. Its paragraph reports what "IDC analysts advised us" and closes with "(IDC, 2026)", which p.31 identifies as a personal communication. Is `reporter` right? And is "the market" the high-end GPU market of that paragraph? |
| `claim-cset-ai-chip-definition` | `ATTRIBUTION` · `supported` | src-003 (SRC-003) · `policy_research_brief` · standing `originator` · <https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf> | p.4, footnote * | "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)" | Footnote * on p.4: does it say "includes", and is "certain types of ASICs" kept? |
| `claim-lbnl-ai-accelerator-accounting` | `ATTRIBUTION` · `supported` | src-021 (SRC-021) · `research_report` · standing `originator` · <https://www.osti.gov/servlets/purl/3374245> | p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report' | "this update expands the accounting to all AI accelerators, namely ASICs" | Does p.16 support "the 2024 report covered GPU accelerators only"? |
| `claim-atlas-ai-accelerator-working-definition` | `INTERPRETATION` · `supported` | input claims: `claim-cset-ai-chip-definition`, `claim-lbnl-ai-accelerator-accounting` | — | — (see the reasoning in the trace) | Is it a choice, citing both sides of CON-01? |
| `claim-nist-cloud-location-independence` | `ATTRIBUTION` · `supported` | src-001 (SRC-001) · `government_publication` · standing `originator` · <https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf> | p.6, essential characteristic 'Resource pooling', the sentence beginning 'There is a sense of location independence' | "There is a sense of location independence" | The domain map labels DC-04 `FACT`; this claim treats NIST's definition as `ATTRIBUTION` (a source's definition, `source-policy.md` §10.1). Agree? |
| `claim-aws-availability-zone-data-centers` | `FACT` · `supported` | src-020 (SRC-020) · `company_technical_documentation` · standing `party` · <https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html> | section 'Availability Zones', the sentence beginning 'Each Availability Zone consists of' | "Each Availability Zone consists of one or more discrete data centers, each with redundant power, networking, and connectivity, and housed in separate facilities" | AWS on its own infrastructure: is `FACT` (party) right? |
| `claim-cloud-compute-facility-often-undisclosed` | `IMPLICATION` · `supported` | input claims: `claim-nist-cloud-location-independence`, `claim-aws-availability-zone-data-centers` | — | — (see the reasoning in the trace) | Does it stay a planning consequence, without claiming any site is `not_publicly_determinable`? |

**Where your verdicts go:** verbatim in an addendum to this report. Each claim's `review`
then gets the verdict, the date and this report's path (`claim-model.md` §7).

## Trace output (Part B §13)

On two fictional relationships, built from `tests/fixtures/` (the fixture relationships,
source records and claims):

```text
$ python tools/trace.py rel-example-foundry-fabricates-accelerator --data <fixtures> --records <fixture relationships>
rel-example-foundry-fabricates-accelerator · relationship record · <fixtures>/relationships.json
  company-example-foundry fabricates product-example-accelerator
  /claim_ids:
    claim-fixture-109 · DERIVATION · supported · verified 2026-09-30 · staging, not reviewed
      statement: Example Foundry performs the wafer fabrication of the example accelerator's die.
      reasoning: ER-1: the foundry is named only inside the vendor's process name, so fabrication by it is inferred.
      input:
        claim-fixture-201 · FACT · supported · verified 2026-09-30 · staging, not reviewed
          statement: The example accelerator is fabricated on the process its vendor names “Example 3X process”.
          as of: not_stated
          citation 1 · src-901 · standing party
            source: "Example Accelerator Architecture In-Depth" · Example Designer Inc. · https://example.com/accelerator-architecture
            class: company_technical_documentation · publisher record: company-example-designer
            stated dates: published 2025-03-01, modified 2026-01-15
            registered: automated 2026-09-29T09:00Z sha256 0123456789ab
            locator: section 'Architecture', the sentence beginning 'The example die'
            anchor: "fabricated using the Example 3X process"
            read by the Verifier: 2026-09-30T10:00Z sha256 0123456789ab (same bytes as registered)
(exit 0)

$ python tools/trace.py rel-example-accelerator-incorporates-stack --data <fixtures> --records <fixture relationships>
rel-example-accelerator-incorporates-stack · relationship record · <fixtures>/relationships.json
  product-example-accelerator incorporates component-example-memory-stack
  /claim_ids:
    claim-fixture-111 · FACT · supported · verified 2026-09-30 · staging, not reviewed
      statement: The example accelerator uses example stacked memory.
      as of: 2025-03
      citation 1 · src-901 · standing party
        source: "Example Accelerator Architecture In-Depth" · Example Designer Inc. · https://example.com/accelerator-architecture
        class: company_technical_documentation · publisher record: company-example-designer
        stated dates: published 2025-03-01, modified 2026-01-15
        registered: automated 2026-09-29T09:00Z sha256 0123456789ab
        locator: section 'Memory'
        anchor: "uses example stacked memory"
        read by the Verifier: 2026-09-30T10:00Z sha256 0123456789ab (same bytes as registered)
  /supplier/claim_ids:
    claim-fixture-112 · DERIVATION · supported · verified 2026-09-30 · staging, not reviewed
      statement: Which company supplies the example accelerator's stacked memory is not publicly determinable from the preferred classes searched.
      reasoning: ER-3: every preferred class was searched for this question and none states the answer.
      search: Which company supplies the stacked memory in the example accelerator? (2026-09-30) → not_publicly_determinable
        company_technical_documentation: no_answer · src-901
        company_filing: no_answer · src-904
(exit 0)
```

<details>
<summary>On every seed claim (real sources)</summary>

```text
$ python tools/trace.py claim-h100-gh100-process-name
claim-h100-gh100-process-name · FACT · supported · verified 2026-09-30 · staging, not reviewed
  statement: NVIDIA's GH100 GPU, which powers the H100 GPU, is fabricated on a process that NVIDIA names the “TSMC 4N process customized for NVIDIA”.
  as of: not_stated
  citation 1 · src-006 · standing party
    source: "NVIDIA Hopper Architecture In-Depth" · NVIDIA (NVIDIA Technical Blog) · https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
    class: company_technical_documentation · publisher record: not_researched
    stated dates: published 2022-03-22, modified 2025-07-22
    registered: automated 2026-09-29T13:26Z sha256 ed8dc6f2a694 · migrated from SRC-006
    locator: section 'NVIDIA H100 GPU architecture in-depth' (the register's 'H100 GPU hardware architecture in-depth'), the sentence beginning 'The full GH100 GPU that powers the H100 GPU'
    anchor: "fabricated using the TSMC 4N process customized for NVIDIA"
    read by the Verifier: 2026-09-30T21:29Z sha256 fd13c05a1586 (bytes changed since registration; anchor re-checked)
(exit 0)

$ python tools/trace.py claim-tsmc-fabricates-h100-gh100
claim-tsmc-fabricates-h100-gh100 · DERIVATION · supported · verified 2026-09-30 · staging, not reviewed
  statement: TSMC performs the wafer fabrication of the GH100 GPU die in NVIDIA's H100.
  reasoning: ER-1: TSMC is named only inside the process name NVIDIA gives for the GH100, so fabrication by TSMC is read out of that name. No retrieved source names the manufacturer directly. NVIDIA's 10-K names TSMC among its foundries at company level only (src-024 p.8, ER-9), so it does not make this a FACT.
  input:
    claim-h100-gh100-process-name · FACT · supported · verified 2026-09-30 · staging, not reviewed
      statement: NVIDIA's GH100 GPU, which powers the H100 GPU, is fabricated on a process that NVIDIA names the “TSMC 4N process customized for NVIDIA”.
      as of: not_stated
      citation 1 · src-006 · standing party
        source: "NVIDIA Hopper Architecture In-Depth" · NVIDIA (NVIDIA Technical Blog) · https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
        class: company_technical_documentation · publisher record: not_researched
        stated dates: published 2022-03-22, modified 2025-07-22
        registered: automated 2026-09-29T13:26Z sha256 ed8dc6f2a694 · migrated from SRC-006
        locator: section 'NVIDIA H100 GPU architecture in-depth' (the register's 'H100 GPU hardware architecture in-depth'), the sentence beginning 'The full GH100 GPU that powers the H100 GPU'
        anchor: "fabricated using the TSMC 4N process customized for NVIDIA"
        read by the Verifier: 2026-09-30T21:29Z sha256 fd13c05a1586 (bytes changed since registration; anchor re-checked)
(exit 0)

$ python tools/trace.py claim-asml-euv-unique-to-asml
claim-asml-euv-unique-to-asml · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
  statement: ASML describes EUV lithography as a technology “unique to ASML”.
  as of: not_stated
  citation 1 · src-017 · standing party
    source: "EUV lithography systems (product page)" · ASML · https://www.asml.com/en/products/euv-lithography-systems
    class: company_marketing · publisher record: not_researched
    stated dates: undated
    registered: automated 2026-09-29T13:27Z sha256 ec896b9cb6bc · migrated from SRC-017
    locator: opening paragraph, the sentence beginning 'The technology, which is unique to ASML'
    anchor: "The technology, which is unique to ASML, prints microchips using light with a wavelength of just 13.5 nm"
    read by the Verifier: 2026-09-30T21:29Z sha256 ec896b9cb6bc (same bytes as registered)
(exit 0)

$ python tools/trace.py claim-lbnl-reports-idc-gpu-die-supply
claim-lbnl-reports-idc-gpu-die-supply · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
  statement: LBNL's 2025 update reports IDC analysts' advice, in forecasting high-end GPU shipments, that the market “is currently constrained by die supply”.
  as of: not_stated
  citation 1 · src-021 · standing reporter
    source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
    class: research_report · publisher record: not_applicable
    stated dates: published 2026-06-18
    registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
    locator: p.18, §3.1.2 'AI Accelerator Shipments', under 'Functional Unit for GPU Forecasts', the sentence beginning 'Because the market is currently constrained', in the paragraph that reports what 'IDC analysts advised us' and ends '(IDC, 2026)'
    anchor: "the market is currently constrained by die supply"
    originator: IDC (International Data Corporation) analysts · market_research_consultancy · not retrieved · named at p.18, 'IDC analysts advised us' and the citation '(IDC, 2026)'; p.31, reference list: a direct communication with an IDC executive analyst
    read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
(exit 0)

$ python tools/trace.py claim-cset-ai-chip-definition
claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
  statement: CSET's definition of “AI chips” includes GPUs, FPGAs and certain types of ASICs.
  as of: not_stated
  citation 1 · src-003 · standing originator
    source: "AI Chips: What They Are and Why They Matter (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf
    class: policy_research_brief · publisher record: not_applicable
    stated dates: published 2020-04
    registered: automated 2026-09-29T13:25Z sha256 0f80b4fa1650 · migrated from SRC-003
    locator: p.4, footnote *
    anchor: "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"
    read by the Verifier: 2026-09-30T21:29Z sha256 0f80b4fa1650 (same bytes as registered)
(exit 0)

$ python tools/trace.py claim-lbnl-ai-accelerator-accounting
claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
  statement: LBNL's 2025 update says that the dataset of its 2024 report covered GPU accelerators only, and that the update “expands the accounting to all AI accelerators, namely ASICs”.
  as of: not_stated
  citation 1 · src-021 · standing originator
    source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
    class: research_report · publisher record: not_applicable
    stated dates: published 2026-06-18
    registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
    locator: p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report'
    anchor: "this update expands the accounting to all AI accelerators, namely ASICs"
    read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
(exit 0)

$ python tools/trace.py claim-atlas-ai-accelerator-working-definition
claim-atlas-ai-accelerator-working-definition · INTERPRETATION · supported · verified 2026-09-30 · staging, not reviewed
  statement: For the Atlas, an AI accelerator is a data-centre logic chip, a GPU or an AI ASIC, whose primary purpose is AI training or inference. FPGAs and CPUs are outside v1 scope.
  reasoning: CON-01 is a definitional conflict (source-policy.md §10.2): CSET's definition includes FPGAs; LBNL's accounting covers GPUs and ASICs. The working definition is a choice, not a resolution. The human chose it at TQ-01 (domain-map.md §7.1, D-016). Both source positions stay as ATTRIBUTION claims.
  input:
    claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
      statement: CSET's definition of “AI chips” includes GPUs, FPGAs and certain types of ASICs.
      as of: not_stated
      citation 1 · src-003 · standing originator
        source: "AI Chips: What They Are and Why They Matter (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf
        class: policy_research_brief · publisher record: not_applicable
        stated dates: published 2020-04
        registered: automated 2026-09-29T13:25Z sha256 0f80b4fa1650 · migrated from SRC-003
        locator: p.4, footnote *
        anchor: "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"
        read by the Verifier: 2026-09-30T21:29Z sha256 0f80b4fa1650 (same bytes as registered)
  input:
    claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
      statement: LBNL's 2025 update says that the dataset of its 2024 report covered GPU accelerators only, and that the update “expands the accounting to all AI accelerators, namely ASICs”.
      as of: not_stated
      citation 1 · src-021 · standing originator
        source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
        class: research_report · publisher record: not_applicable
        stated dates: published 2026-06-18
        registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
        locator: p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report'
        anchor: "this update expands the accounting to all AI accelerators, namely ASICs"
        read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
(exit 0)

$ python tools/trace.py claim-nist-cloud-location-independence
claim-nist-cloud-location-independence · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
  statement: NIST's definition of cloud computing says there is “a sense of location independence”: the customer generally has no control or knowledge over the exact location of the provided resources, but may be able to specify location at a higher level of abstraction, such as a country, state or datacenter.
  as of: not_stated
  citation 1 · src-001 · standing originator
    source: "The NIST Definition of Cloud Computing (Special Publication 800-145)" · National Institute of Standards and Technology (NIST) · https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf
    class: government_publication · publisher record: not_applicable
    stated dates: published 2011-09
    registered: automated 2026-09-29T13:25Z sha256 7b0c1a9fdfc6 · migrated from SRC-001
    locator: p.6, essential characteristic 'Resource pooling', the sentence beginning 'There is a sense of location independence'
    anchor: "There is a sense of location independence"
    read by the Verifier: 2026-09-30T21:29Z sha256 7b0c1a9fdfc6 (same bytes as registered)
(exit 0)

$ python tools/trace.py claim-aws-availability-zone-data-centers
claim-aws-availability-zone-data-centers · FACT · supported · verified 2026-09-30 · staging, not reviewed
  statement: Each AWS Availability Zone consists of one or more discrete data centers, each with redundant power, networking and connectivity, and housed in separate facilities.
  as of: not_stated
  citation 1 · src-020 · standing party
    source: "AWS Regions and Availability Zones (user guide)" · Amazon Web Services · https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html
    class: company_technical_documentation · publisher record: not_researched
    stated dates: undated
    registered: automated 2026-09-29T13:29Z sha256 1f172d6e220c · migrated from SRC-020
    locator: section 'Availability Zones', the sentence beginning 'Each Availability Zone consists of'
    anchor: "Each Availability Zone consists of one or more discrete data centers, each with redundant power, networking, and connectivity, and housed in separate facilities"
    read by the Verifier: 2026-09-30T21:29Z sha256 1f172d6e220c (same bytes as registered)
(exit 0)

$ python tools/trace.py claim-cloud-compute-facility-often-undisclosed
claim-cloud-compute-facility-often-undisclosed · IMPLICATION · supported · verified 2026-09-30 · staging, not reviewed
  statement: For cloud AI compute, the Atlas should expect the facility behind a service to be undisclosed: providers may let customers specify location only at a level above the site, and an Availability Zone groups one or more data centers. A facility is recorded only where a source names it, never read off a region or zone (D-022), and a missing site stays not_researched until an ER-3 search supports not_publicly_determinable.
  reasoning: Domain map §6 draws this implication from SRC-001 p.6 and SRC-020. It is restated here so that it does not pre-empt ER-3: expecting non-disclosure is a planning consequence, not a finding that any site is not_publicly_determinable.
  input:
    claim-nist-cloud-location-independence · ATTRIBUTION · supported · verified 2026-09-30 · staging, not reviewed
      statement: NIST's definition of cloud computing says there is “a sense of location independence”: the customer generally has no control or knowledge over the exact location of the provided resources, but may be able to specify location at a higher level of abstraction, such as a country, state or datacenter.
      as of: not_stated
      citation 1 · src-001 · standing originator
        source: "The NIST Definition of Cloud Computing (Special Publication 800-145)" · National Institute of Standards and Technology (NIST) · https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf
        class: government_publication · publisher record: not_applicable
        stated dates: published 2011-09
        registered: automated 2026-09-29T13:25Z sha256 7b0c1a9fdfc6 · migrated from SRC-001
        locator: p.6, essential characteristic 'Resource pooling', the sentence beginning 'There is a sense of location independence'
        anchor: "There is a sense of location independence"
        read by the Verifier: 2026-09-30T21:29Z sha256 7b0c1a9fdfc6 (same bytes as registered)
  input:
    claim-aws-availability-zone-data-centers · FACT · supported · verified 2026-09-30 · staging, not reviewed
      statement: Each AWS Availability Zone consists of one or more discrete data centers, each with redundant power, networking and connectivity, and housed in separate facilities.
      as of: not_stated
      citation 1 · src-020 · standing party
        source: "AWS Regions and Availability Zones (user guide)" · Amazon Web Services · https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html
        class: company_technical_documentation · publisher record: not_researched
        stated dates: undated
        registered: automated 2026-09-29T13:29Z sha256 1f172d6e220c · migrated from SRC-020
        locator: section 'Availability Zones', the sentence beginning 'Each Availability Zone consists of'
        anchor: "Each Availability Zone consists of one or more discrete data centers, each with redundant power, networking, and connectivity, and housed in separate facilities"
        read by the Verifier: 2026-09-30T21:29Z sha256 1f172d6e220c (same bytes as registered)
(exit 0)
```

</details>
