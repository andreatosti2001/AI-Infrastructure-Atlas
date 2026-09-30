# SESSION-05 Report — Source hierarchy and evidence policy

- **Session:** S05 · **Type:** RESEARCH / ARCHITECTURE · **Milestone:** M1 — Domain + Evidence Foundation
- **Date:** 2026-09-30
- **Prompt:** [`sessions/prompts/S05-PROMPT.md`](../prompts/S05-PROMPT.md) (Part A human, Part B
  SPEC §2 detail written at the end of S04, with the human's answers H-1 and H-2 in §16)
- **Branch:** `claude/sleepy-bell-mv44c5`, at `main` @ `092c607` (the PR #5 merge, which
  brought the S05 prompt to `main`)
- **Base at start** (D-018 L-03):
  - `git branch -a` listed:
    - `claude/sleepy-bell-mv44c5` (local, at `092c607`);
    - `main`;
    - `remotes/origin/claude/sleepy-bell-mv44c5`;
    - `remotes/origin/main`.
  - `git ls-remote` showed `main` at `092c607` and four other branches, none carrying work
    missing from `main`:
    - `claude/atlas-architecture-baseline-jow618` (`26acdf9`), merged;
    - `claude/beautiful-albattani-gyg4nw` (`ace06f0`), merged by PR #5;
    - `claude/magical-galileo-vwn13j` (`ce5b881`), merged;
    - `claude/youthful-allen-rtfdu8` (`e23965c`): the S04 prompt commit, whose content S04
      cherry-picked onto `main`.
  - The S05 prompt was on `main` before the session started, so S04's Deviation 1 did not
    recur.

## Mission outcome

**Delivered for human review.**

| Deliverable | Where | Status |
|---|---|---|
| Source classes, each with a definition, neighbour test, what it is primary for and what it is never enough for | `schemas/sources.schema.json`; `docs/research/source-policy.md` §2–§3 | proposed (D-034) |
| Standing (party, originator, reporter), attribution chains, independence | policy §4 | proposed (D-035) |
| Preference matrix: one row per material claim type, read from both schemas | policy §7 | machine-checked; proposed (D-036) |
| MA §10 and D-015 reconciled; D-015 disposed | policy §9 | proposed (D-036) |
| The three S04 evidence rules as policy, with the `not_publicly_determinable` search rule | policy §6, ER-1 to ER-3 (and ER-4 to ER-10) | proposed (D-037) |
| Conflict policy, applied to CON-01 to CON-05 | policy §10 | machine-checked; proposed (D-038) |
| Retrieval, access and freshness rules; H-1 recorded; D-014 disposed | policy §11–§12 | proposed (D-039, D-040) |
| Class of every registered source and every blocked host; the CSET decision | policy §8 | machine-checked; proposed (D-041) |
| Five worked examples from registered sources | policy §13 | anchors machine-checked against the domain map |
| Weekly-gate explainer, "How the Atlas decides what to believe" | policy §14 | written; **the gate is the human's call** |
| Tests | `tests/test_source_policy.py`, `tests/test_source_schema.py`, `tests/fixtures/sources.json` | passing locally; CI: see the addendum |

**Registry gate, "source/evidence policy"** (roadmap gate: "Every material claim type has a
preferred source class"): **met for review, not approved.** Every row of the matrix names at
least one preferred class, and a test fails when either schema gains a type or field without
a row. D-034 to D-041 are `proposed`.

**Restated contract** (operating-contract step 6, given before any file was written):

- **Mission:** write the Atlas source policy: the classes; a preferred class for every
  material claim type; how conflicts are recorded and when they close. It must make three
  things impossible: marketing as a fact about the world; a secondary report standing in
  for the record it cites; a conflict settled by rank alone.
- **Scope:** the policy document; the class vocabulary schema (H-2 (b)); its tests and
  fixtures; the consistency tests; D-034 onward; the index, baseline and README state rows;
  this report.
- **Non-goals:** as Part B §08. No claim schema, evidence-status vocabulary, source record,
  register migration, agent contract, record, score, retrieval tool, freshness code,
  circumvention, change to an accepted schema, or edit to the root documents, domain map or
  register.
- **Acceptance:** Part B §15.
- **Plan:**
  1. classify the registered sources, grounding each class in the sources' own text;
  2. schema, fixtures, schema tests;
  3. policy document;
  4. consistency tests, fail-first;
  5. decisions;
  6. deliberate breakage;
  7. docs rows;
  8. report;
  9. commit and push.

  The plan held. One step was added inside step 1 (Deviation 2).

**No stop condition fired.** No preference needed a new entity field, relationship qualifier
or claim field (the claim fields the policy needs are handed to S06 without being added).
Every claim type has a publicly available preferred class. MA §10 reconciles without an edit.
No classification needed access D-014 forbids. The classes settled, so H-2's option (b)
applied, not the fallback.

## Files changed

Added:

- `docs/research/source-policy.md`: principles SP-1 to SP-7; the class table; the neighbour
  tests; standing, chains and independence; the separate axes; evidence rules ER-1 to ER-10;
  the preference matrix; the class of every registered source, every blocked host and the S05
  retrieval; the reconciliation of the tier orders; the conflict policy and its application;
  retrieval and access rules RA-1 to RA-7; freshness; five worked examples; the weekly-gate
  explainer; rejected candidates; handoffs.
- `schemas/sources.schema.json`: the `source_class` vocabulary only, one `const` with a
  description per class. Not a record schema (H-2).
- `tests/fixtures/sources.json`: every class as a valid value, and invalid values (tiers,
  ranks, "primary", "verified", near misses, null, two classes).
- `tests/test_source_schema.py`: behaviour tests (uses `jsonschema`). Each invalid value must
  be rejected at the root by the vocabulary itself.
- `tests/test_source_policy.py`: consistency tests (standard library). Imports `cells`,
  `section`, `decision_exists`, `CONCEPT` and `ENTITY_TYPES` from `test_entity_taxonomy.py`,
  as S04 did.
- `sessions/reports/SESSION-05-REPORT.md`: this report.

Modified:

- `docs/architecture/decisions.md`: D-034 to D-041 appended, all `proposed`.
- `docs/README.md`: the source-policy row (planned → proposed) and the schema rows.
- `docs/architecture/baseline.md`: dated state rows only: the status line, the §1 heading
  and "Source/evidence policy" row, a §4 sentence, the §5 Gate 1 row.
- `README.md`: the status sentence and two layout lines, which had become incomplete.

Not modified:

- the root constitutional documents, including MA §10;
- `domain-map.md`, `source-register.md`, `M0-audit.md`, both taxonomies;
- `entities.schema.json`, `relationships.schema.json`, `tools/`, `.github/`,
  `requirements-test.txt`, `PROMPT-REGISTRY.md`;
- anything in `Eu-Digital-Policy`, which was not opened.

## Data changed

- **Canonical or staging records:** none.
- **Schema:** the source-class vocabulary (proposed). The accepted S03 and S04 schemas are
  unchanged.
- **Measured at this commit** (by script over the committed tables, not typed; L-04):

  | Measure | Count |
  |---|---|
  | source classes | 11 |
  | matrix rows | 32 (11 relation types, 1 edge qualifier, 6 identity, 14 attribute) |
  | rows by freshness | 19 `stable`, 13 `time_sensitive` |
  | rows by standing | 15 `party`, 10 `party or originator`, 7 `originator` |
  | registered sources classed | 23: `company_marketing` 9, `company_technical_documentation` 5, `research_report` 3, `government_publication` 2, `policy_research_brief` 2, `industry_association` 1, `company_press_release` 1 |
  | classes with no registered source | `company_filing`, `standard_specification`, `market_research_consultancy`, `news_media` (filings and standards were blocked in S01) |
  | blocked-host rows classed | 9 |
  | neighbour-test pairs | 8 |
  | conflict kinds | 5 |
  | conflicts handled | 5 (all preserved) |
  | worked examples; distinct anchors checked | 5; 11 |
  | schema fixtures | 11 valid values, 12 invalid |
  | times each class is preferred | `company_filing` 16, `government_publication` 14, `company_technical_documentation` 13, `standard_specification` 7, `research_report` 5, `company_marketing` 4, `company_press_release` 1; the other four never |

## Tests run

Python 3.11.15. All commands ran locally from the repository root. "venv" means a fresh
virtualenv built from `requirements-test.txt` in the session scratchpad.

| Command / check | Result |
|---|---|
| `python -m unittest discover -s tests` at start, venv | OK (58 tests) |
| `python tools/validate_repo.py` at start | `Repository integrity: OK` |
| venv `pip freeze` vs the pins, sorted, at start and again in a second fresh venv at the end | installed set = pinned set, both times |
| Schema behaviour tests, first run | OK (3). Each invalid value's errors printed and read: all at the root, from `oneOf` (and `type` for non-strings) |
| **Fail-first**, consistency tests before D-034 to D-041 existed | 10 failures. 6 were "cited decision does not exist", as expected. **The other 4 came from 3 real defects, all fixed:** (1) ER-1 had copied eight-word runs of S04's §5 `fabricates` text (two failures; the one-home test caught it); (2) a neighbour test was not phrased as a question; (3) one matrix row pointed to another row instead of the schema field |
| Verifier re-read of the whole policy after tests passed | **three contradictions found by reading, not by tests, and fixed:** technical documentation and policy briefs sat in "acceptable" for class-level `requires`/`has_part`, though §2 says they are never enough for class-level necessity; policy briefs, research and government sat in "acceptable" for company roles, though §2 says briefs are never enough for company facts. Resolved toward the stricter reading. A test was added for the one prose claim that could be tested (§9: market research and news are never sufficient alone in any row) |
| L-04 scan of prose and decisions | hand-typed counts removed from D-034, D-036, D-038, D-040 and the policy, or labelled "as measured"; the remaining prose counts are tested |
| **Deliberate breakage**, 16 breaks, each in a fresh scratch copy | first run: 15 caught, **1 missed**: changing SRC-012's class to the class of the *other* side of CON-02 passed, because the test only looked for the class anywhere in the row. The test now pairs each source with its own class. Final run: **all 16 caught**: (1) a relation type added to the relationship schema; (2) an attribute field added to the entity schema; (3) a register row without a class; (4) an anchor changed by one word; (5) a class added to the vocabulary; (6) a class dropped from a matrix row; (7) a class in two columns; (8) a new CON in the domain map; (9) a conflict marked resolved; (10) S04 §5 text copied in; (11) a mapped class that disagrees with a conflict side; (12) a register tier cell changed; (13) a wrong prose count; (14) an undefined rule cited; (15) the vocabulary loosened to any string; (16) a required neighbour pair removed |
| `python -m unittest discover -s tests -v`, final, fresh venv | OK (85 tests) |
| The same, final, system Python | 74 tests run; the three `jsonschema` modules error on import (expected since D-026); the standard-library tests pass |
| `python tools/validate_repo.py`, final, with this report present | `Repository integrity: OK` |
| CI result | not observed when this report was committed; see the addendum (L-08) |

Not applicable: data validation (no records), browser, accessibility, performance.

## Evidence added/retired

- **Added (not to the register):**
  - **S05-R1**, NVIDIA's Form 10-K for fiscal 2026, company-hosted copy, retrieved with
    `curl` on 2026-09-30T16:57Z, SHA-256 prefix `a056b59e4170`. Retrieved under Part B §05
    to settle what the filing class contains, because no registered source is a filing.
    Recorded in policy §8.3 with locators and verbatim anchors, read by hand. Its identity
    with the copy at the SEC is **not verified** (EDGAR refused).
  - **S05-A1**, an access record, not a source: EDGAR's refusal page (HTTP 403,
    2026-09-30T16:56Z, SHA-256 prefix `14f247606881`), which cites a published access policy
    behind the same refusal.
  - Web search was used once, to discover the filing's URL. Aggregator copies in the results
    were not retrieved or cited. No snippet is used as evidence.
- **Re-read:** all 23 registered sources were re-retrieved on 2026-09-30 (as measured, not
  a tested count): 14 had the same bytes as in S01, 9 differed, and every domain-map anchor
  was found again in the 22 sources re-read. SRC-023's PDF is encrypted and was not re-read.
  New locators read in S05 (SRC-002 p.3; SRC-005 p.2; SRC-021 p.2, p.17–18, p.31, p.33) are
  cited in the policy.
- **Verifier pass:** every quoted anchor in policy §13–§14 is verbatim in the domain map
  (test). The S05-R1 anchors and the new register locators were checked by hand against the
  locally extracted text; they cannot be machine-checked, because full texts stay out of the
  repository (H-1).
- **Retired:** none. The register is unchanged.

## Decisions made

| ID | Subject | Status |
|---|---|---|
| D-034 | Source classes: document kinds, one per source, in a vocabulary schema (H-2 (b)) | proposed |
| D-035 | Standing (party, originator, reporter), attribution chains, independence; publisher as entity reference for S06 | proposed |
| D-036 | Preference matrix read from the schemas; no global ranking; MA §10 and D-015 reconciled; D-015's tiers superseded, its `verified` meaning to S06 | proposed |
| D-037 | Evidence rules ER-1 to ER-10, including the `not_publicly_determinable` search rule | proposed |
| D-038 | Conflict policy: kinds of conflict, never settled by rank; CON-01 to CON-05 applied | proposed |
| D-039 | Retrieval and access; manual retrieval by the human (H-1); supersedes D-014's retrieval clause | proposed |
| D-040 | Freshness: separate dates; byte changes trigger re-checks; a proposed 12-month horizon | proposed |
| D-041 | Where each source's class lives; register not annotated; CSET decision | proposed |

**Rejected alternatives** (each decision lists its own; the main ones):

- **A global ranking**, MA §10's or D-015's: it cannot express that marketing is preferred
  for product identity and insufficient for a definition.
- **Numeric scores** of any kind.
- **"Primary" and "secondary" as classes:** primacy is per claim (standing).
- **One company class** (D-015's T1).
- **Self-interest as a conflict kind:** it would invite deciding against the interested side.
- **A two-class value for joint reports; a tertiary class; an announcement class now.**
- **Conditional cells** ("acceptable only with an independent second publisher"): the
  partition model cannot check them, so the stricter column was chosen.
- **Annotating the register; the full source-record schema now; event rows now.**
- **Sending EDGAR a declared client identity** from memory of its policy.

## Deviations

1. **Part A and Part B, both followed.** Part A lists four claim labels; CLAUDE.md §6 adds
   `ATTRIBUTION`, and all five are used, as Part B §09 directs.
2. **All 23 registered sources were re-retrieved.** Part B tests the policy against the
   registered sources, and §06 q9 asks how dates and hashes work together. The re-read
   grounded the class tests in the sources' own words and measured whether byte hashes
   signal content change. It added no register row and edited no source record. It is
   recorded here because Part B did not list it as a task.
3. **The new filing came from the filer's site, not the regulator.** EDGAR refused plain
   requests. RA-6 allows a filer-hosted copy, classed as the filing, with the identity check
   recorded as not done.
4. **PDF text extraction** used `pypdf` in a scratch virtualenv, as S01 did (D-014). It is not
   a repository dependency, and the final test run used a second, clean venv built only from
   the pins.
5. **Schema fixtures are values, not records.** The S03/S04 pattern mutates a valid record.
   The S05 schema is a vocabulary, so each invalid case is one value. Each still must fail
   for its stated reason (at the root, in the vocabulary).
6. **Five worked examples** (Part B asked for at least four; SRC-005 was optional).

No part of Part A or Part B was skipped.

## Debt introduced/resolved

**Introduced:**

- **More Markdown parsing.** The consistency tests read seven tables in the policy, plus the
  register, domain map §5 and taxonomy §5. Each parse asserts the table width, and the
  register parse also asserts its row count.
- **The §2 class table and the matrix can disagree** without a test failing. Three such
  contradictions were found by reading and fixed. A machine check would need the class table
  in structured form. For now it is a Verifier read at each change.
- **S05-R1's anchors are verified by hand only** (full text outside the repository, H-1).
- **SRC-023 was not re-read** (encrypted PDF); its class rests on S01's description.
- **Blocked-host classes are `INTERPRETATION`**, because the hosts were not read.
- **The 12-month horizon is a proposal**, not an evidence-based figure.
- **No class for an announcement by a standards body or association** (S06 decides).
- **Cross-module test imports** continue (S04 Deviation 3, kept at the S04 review).

**Resolved:**

- D-014 and D-015 have dispositions (D-039, D-036), pending review.
- The tier-order conflict between MA §10 and D-015 is reconciled without editing MA.
- Register note 1 (CSET) is decided.
- `relationship-taxonomy.md` §15's S05 row (preferred class per §5 row and identity) is done.

## Unresolved issues

### Evidence gaps

- **Assumptions invalidated by the policy** (the domain map is not edited; later sessions
  act on them):
  - **DEP-02 and DEP-03 rest on one publisher.** S01 labelled them `FACT` from two and three
    SK hynix sources. Under ER-7 these are one voice, and a newsroom explainer or press
    release is never enough alone for `requires`. S08/S10 need a standard (JEDEC, blocked) or
    research before recording those edges as `FACT`.
  - **DEP-07 and DEP-09** (`requires`) cite CSET and company pages only. Both classes are now
    never sufficient alone for `requires`.
  - **D-015's T1–T6 do not survive:** T1 splits into four classes; SRC-021 and SRC-022 move
    from government to research; CSET moves from research to policy analysis (T4 → T5 in
    S01 terms).
  - **The register's byte hashes over-signal change:** 9 of 23 changed with no anchor lost
    (as measured on 2026-09-30).
- **HBM-06 is not closed by the filing.** S05-R1 names NVIDIA's memory suppliers at company
  level, which supports `supplies` candidates and never a product's `supplier` (ER-9).
- **EDGAR's access policy is unread** (behind the refusal). Filings via the SEC remain a gap.
- **ISO 3166-1** is still not in the register (jurisdiction identity).
- **SRC-023 has a 2026 successor** cited by SRC-021 (p.31); not retrieved.
- **Carried, unchanged:** the blocked primary sources (JEDEC, TSMC, Samsung, IEA and others);
  CON-01 to CON-05, preserved; the `not_researched` items in domain map §8.

### Human approvals required

1. **D-034 to D-041.** Approve or amend each. The consequential points:
   - no global ranking (D-036), and MA §10 read as guidance;
   - class-level `requires`/`has_part` edges need a standard, research or government source;
     company pages and policy briefs are never enough alone (D-036, the matrix);
   - CSET as `policy_research_brief` (D-041);
   - the `not_publicly_determinable` search rule (D-037, ER-3);
   - the 12-month horizon for `time_sensitive` rows (D-040).
2. **D-014 and D-015 status lines:** at acceptance they become "superseded in part by
   D-039" and "superseded in part by D-036".
3. **EDGAR:** whether the human reads `www.sec.gov/developer` in a browser (RA-4), and, if its
   rules require a declared identity, what identity to declare (RA-7).
4. **Still open from earlier sessions:** whether "external API dependency" becomes a v1.0
   non-goal; S01's weekly gate.
5. **The week-2 gate** ("the ontology and evidence policy are understandable before
   large-scale data collection begins"). Policy §14 is written for it. **S05 does not
   declare it passed.**
6. **Merging this branch:** no pull request has been opened.

## Process lessons

- **Grounding classes in the sources' own words settled the hard cases.** CSET's own aim
  ("To help policymakers…", SRC-002 p.3) and SIA's own role (SRC-005 p.2) made the neighbour
  tests answerable from the text. That is why H-2's option (b) applied, not the fallback.
- **The one-home test caught a copy the author did not notice** (ER-1 restating S04 §5). A
  shingle test over the source cells is cheap and catches paraphrase that stays too close.
- **A test that checks "present somewhere in the row" is weaker than it looks.** Break 11
  passed until the test paired each source with its own class. *Check what was read, and
  against what it belongs to.*
- **Reading found what tests could not.** The §2-versus-matrix contradictions were caught by
  the Verifier's re-read, not by any check. L-09 still applies after the tests are green.
- **A retrieved filing is a better lesson than a definition of one.** S05-R1 showed in one
  paragraph the difference between company-level and product-level evidence (ER-9), which
  no class definition would have made as clear.

## Implications for the next session

**Handoff: S06, Evidence/claim system (IMPLEMENTATION).**

- **Completed work:** the source classes (schema), the preference matrix, the evidence,
  conflict, retrieval and freshness rules, and their tests (proposed).
- **For S06** (policy §16 is the list):
  - **Source record:** class (this vocabulary); publisher as text, and as a company
    reference where the publisher is a company; authors; retrieval method (automated, or
    "manual, by the human"); access date; content hash; publication date as stated; the host
    of a copy.
  - **Claim record:** standing; the attribution chain (reporter, originator, locator); the
    as-of date; the search scope of a `not_publicly_determinable` claim (ER-3); the evidence
    status for disputed claims (§10).
  - **Migration:** each register row's class from policy §8.1; S05-R1 from §8.3.
  - **The meaning of `verified`** (D-015's second part): confirm or supersede.
  - **An announcement class**, if S06 retrieves one.
- **Open issues:** the human approvals above; `validate-freshness` (S06+); the `validate-data`
  rules V-1 to V-9 (S04).
- **Recommended next decision:** the human reviews D-034 to D-041 and declares the week-2
  gate before S06, because S06's claim model attaches standing and evidence status to claims
  whose sources S05 classifies.
- **Files for S06 to read first:**
  1. this report;
  2. `docs/research/source-policy.md` (§4, §5, §6, §7, §16);
  3. `schemas/sources.schema.json`;
  4. `docs/architecture/relationship-taxonomy.md` §5 and §9;
  5. `docs/architecture/entity-taxonomy.md` §7;
  6. `docs/research/source-register.md`;
  7. D-015, D-025, D-028, D-031 and D-034 to D-041.

**One next milestone:** S06 builds the claim and source records on top of this vocabulary,
so that the Atlas can answer "What exactly supports this relationship?"

## Addendum — CI

- At the commit that adds this report, CI had not been observed. Local results only
  (D-018 L-08).
