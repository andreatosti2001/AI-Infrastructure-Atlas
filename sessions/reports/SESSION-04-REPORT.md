# SESSION-04 Report — Relationship taxonomy

- **Session:** S04 · **Type:** ARCHITECTURE · **Milestone:** M1 — Domain + Evidence Foundation
- **Date:** 2026-09-30
- **Prompt:** [`sessions/prompts/S04-PROMPT.md`](../prompts/S04-PROMPT.md) (Part A human, Part B
  SPEC §2 detail written at the end of S03)
- **Branch:** `claude/beautiful-albattani-gyg4nw`, at `main` @ `1d0522c` (the S03 merge)
- **Base at start** (D-018 L-03):
  - `git branch -a` listed:
    - `claude/beautiful-albattani-gyg4nw` (local, at `1d0522c`);
    - `main`;
    - `remotes/origin/claude/beautiful-albattani-gyg4nw` (at `1d0522c`);
    - `remotes/origin/main`.
  - The local `origin/main` ref was stale (`6413a02`). A `git fetch origin main` moved it
    to `1d0522c`, which is `main` on the remote.
  - `git ls-remote` showed three other remote branches:
    - `claude/atlas-architecture-baseline-jow618` (`26acdf9`), merged;
    - `claude/magical-galileo-vwn13j` (`ce5b881`), merged;
    - `claude/youthful-allen-rtfdu8` (`e23965c`), **one commit not on `main`**: the S04
      prompt itself (Deviation 1).

## Mission outcome

**Delivered for human review.**

| Deliverable | Where | Status |
|---|---|---|
| Relationship vocabulary with levels, direction, endpoints, time and evidence expectations | [`docs/architecture/relationship-taxonomy.md`](../../docs/architecture/relationship-taxonomy.md) §1–§5 | proposed (D-028, D-029) |
| Record shape, vocabulary and endpoint types | [`schemas/relationships.schema.json`](../../schemas/relationships.schema.json) | proposed (D-028 to D-031) |
| One disposition for every verb in MA §6.2, the roadmap S04 list and domain map §3 | taxonomy §6 | machine-checked (D-030) |
| One-home rulings on the S03 fields; none moves | taxonomy §7 | machine-checked (D-030) |
| DEP-01 to DEP-18 mapped | taxonomy §8 | machine-checked |
| Unknown and non-public edges; CoWoS and constituent-level fabrication | taxonomy §9, §4.6–4.7 | proposed (D-031, D-032) |
| Role/edge warnings and `validate-data` rules handed on | taxonomy §11, §15 | proposed (D-033) |
| Three worked examples from S01 sentences (DEP-05, DEP-01, DEP-04) | taxonomy §12 | anchors machine-checked against the domain map |
| Evidence-expectation table for S05 | taxonomy §5 | one home; handoff below |
| Behaviour and consistency tests | `tests/test_relationship_schema.py`, `tests/test_relationship_taxonomy.py`, `tests/fixtures/relationships.json` | passing locally; CI not yet observed |

**Registry gate, "semantic relationship model"** (roadmap gate: "Every relationship has a
clear semantic definition and evidence expectation"): **met for review, not approved.**
Every type has both, and tests enforce it. D-028 to D-033 are `proposed`.

**Restated contract** (operating-contract step 6, given before any file was written):

- **Mission:** define the Atlas relationship vocabulary. Each type gets a definition,
  direction, typed endpoints, level, time handling and evidence expectation. The result
  must make co-occurrence edges and vague verbs impossible to record.
- **Scope:**
  - the reasoning document;
  - the relationship schema;
  - fictional fixtures;
  - two test files;
  - decisions D-028 onward;
  - the index, baseline and README state rows;
  - this report.
- **Non-goals:** as Part B §08. No records, no source classes, no claim or event schema,
  no policy/energy/network edges, no metrics or derived `depends_on`, no record
  validator, no graph library, no change to an accepted S03 field.
- **Acceptance:** Part B §15, items 1–10.
- **Plan:**
  1. schema;
  2. taxonomy;
  3. fixtures and tests;
  4. fail-first run;
  5. decisions;
  6. deliberate breakage;
  7. docs;
  8. report;
  9. commit and push.

  The plan held.

**No blocking question was put to the human.** No §06 answer required moving a fact out of
an accepted S03 field. No new dependency was needed. No policy, energy or networking
endpoint was needed. So no stop condition fired, and the design is delivered as
`proposed` decisions.

## Files changed

Added:

- `docs/architecture/relationship-taxonomy.md`:
  - design rules RR-1 to RR-10 and the direction convention;
  - the type table;
  - the two levels;
  - eleven type definitions;
  - the evidence-expectation table;
  - the verb reconciliation;
  - the S03 field rulings;
  - the DEP mapping;
  - unknown edges, time, and role/edge warnings;
  - three worked examples;
  - a human-focus explainer;
  - the rejected candidates;
  - the handoffs.
- `schemas/relationships.schema.json`: JSON Schema 2020-12.
  - One `if`/`then` branch per relation type.
  - Endpoints and shared shapes are `$ref`s into `entities.schema.json`.
  - Each vocabulary value is a `const` with `description`, `x-level`, `x-deps` and
    `x-inverse-reading`.
- `tests/fixtures/relationships.json`: fictional valid records, at least one per type, and
  invalid cases, each one JSON Pointer mutation of a valid base.
- `tests/test_relationship_schema.py`: behaviour tests (uses `jsonschema`). Each invalid
  case must fail *at, under or beside* the pointer it mutates. The cross-file `$ref`s
  must resolve, and must fail without the entity schema.
- `tests/test_relationship_taxonomy.py`: consistency tests (standard library). It parses
  the three verb lists from MA, the roadmap and the domain map. It also parses the DEP
  table and the taxonomy tables, and checks prose counts (L-04).
- `sessions/prompts/S04-PROMPT.md`: brought in by cherry-picking `e23965c` (Deviation 1).
- `sessions/reports/SESSION-04-REPORT.md`: this report.

Modified:

- `docs/architecture/decisions.md`: D-028 to D-033 appended, all `proposed`.
- `docs/README.md`: the "Relationship taxonomy" row (planned → proposed, with links).
- `docs/architecture/baseline.md`: dated state rows only, those that had become false:
  - the status line;
  - the §1 heading and the "Relationship schema" row;
  - the §4 sentence on reconciling the verb lists;
  - the §5 Gate 1 row.
- `README.md`: status sentence and layout lines, which no longer listed everything in
  `schemas/` and `docs/`.

Not modified:

- root constitutional documents;
- `domain-map.md`, `source-register.md`, `M0-audit.md`, `entity-taxonomy.md`;
- `schemas/entities.schema.json`, `tools/`, `.github/`, `requirements-test.txt`;
- `PROMPT-REGISTRY.md`, which already listed S04;
- anything in `Eu-Digital-Policy`, which was not opened.

## Data changed

- **Canonical or staging records:** none.
- **Schema:** the first relationship schema (proposed). The entity schema is unchanged.
- **Fixtures:** fictional (`…-example-…`, `claim-fixture-…`). They assert nothing about
  the world.
- **Measured at this commit** (by script, not typed; L-04):

  | Measure | Count |
  |---|---|
  | valid fixtures | 17 |
  | invalid cases | 71 |
  | relation types | 11 (class level 2, instance level 9) |
  | verbs parsed from MA / roadmap / domain map | 18 / 14 / 12 |
  | distinct verbs across the three lists | 28 |
  | dispositions: adopt | 8 |
  | dispositions: merge | 5 |
  | dispositions: rejected as vague | 5 |
  | dispositions: reserved for S17 | 4 |
  | dispositions: event | 2 |
  | dispositions: derivation | 2 |
  | dispositions: entity field | 1 |
  | dispositions: excluded by a non-goal | 1 |
  | DEP mappings: relationship | 13 |
  | DEP mappings: event | 1 |
  | DEP mappings: exclusion | 4 |

## Tests run

Python 3.11.15. All commands ran locally from the repository root. "venv" means a fresh
virtualenv built from `requirements-test.txt` in the session scratchpad.

| Command / check | Result |
|---|---|
| `python -m unittest discover -s tests` at start, system Python | 23 tests run, 1 error: `jsonschema` not installed there (expected since D-026) |
| The same at start, venv | OK (26 tests) |
| `python tools/validate_repo.py` at start | `Repository integrity: OK` |
| venv `pip freeze` compared with the pins | installed set = pinned set |
| First run of the schema test | Two problems, both fixed. Run by file path, the import of the S03 helpers failed, because it only works under `discover -s tests`, which is how CI runs. The error-location check was too strict: it rejected an error reported *inside* the mutated value (`/claim_ids/0`). Relaxed to "at, under or beside the pointer" |
| Every invalid case's error messages printed and read by hand | each fails for the reason its `why` states. Notes: `false`-schema errors are reported at the root, not at the field; `endpoint_list` also trips the placeholder rule |
| **Fail-first**, before D-028 to D-033 existed | 35 failures, every one "cited decision does not exist". The same runs exposed four real defects, all fixed: (1) the domain-map DEP table was parsed as 8 columns instead of 7, so its Verb column was silently skipped; the In-column test caught it, and the parser now asserts the width and the row count; (2) a line break before "roadmap's" hid the end marker; (3) two non-anchor phrases in straight quotes in §12; (4) a wrong "reached XOR introduced" rule in the test |
| **Deliberate breakage**, 14 breaks, each in a fresh scratch copy | all caught: (1) top-level `additionalProperties` removed; (2) `associated_with` added to the vocabulary; (3) the `stacks_on` reconciliation row deleted; (4) the DEP-11 mapping row deleted; (5) `designs` target changed to facility; (6) jurisdiction allowed as an `owns` target; (7) `supplier` made optional; (8) dates allowed on `requires`; (9) a new verb in the domain map (`houses` → `hosts`); (10) an anchor altered by one word; (11) DEP-12 removed from `houses` x-deps; (12) the cross-file `claim_ids` `$ref` mistyped; (13) the placeholder ban removed; (14) the `located_in` ruling changed to "edge" |
| `python -m unittest discover -s tests -v`, final, venv | OK (58 tests) |
| The same, final, system Python | the two `jsonschema` modules error on import; the standard-library tests pass |
| `python tools/validate_repo.py`, final, with this report present | `Repository integrity: OK` |
| CI result | **not yet observed.** Local results only (D-018 L-08) |

Not applicable: data validation (no records), browser, accessibility, performance.

## Evidence added/retired

- **External sources:** none retrieved or added. `source-register.md` is unchanged.
- **Evidence cited:** definitions and worked examples rest on S01 domain-map entries:
  - DEP-01 to DEP-18;
  - FAB-05, ACC-03, ACC-04, HBM-03, HBM-06, PKG-04, PKG-07;
  - DC-03, DC-04, SME-01, SME-03.
- **Verifier pass** (Part B §10):
  - Every quoted anchor in taxonomy §12 appears verbatim in the domain map. A test now
    enforces this.
  - The source characterisations were checked against `source-register.md`:
    - SRC-006 is an NVIDIA technical blog;
    - SRC-014 is an SK hynix press release dated 2024-04-19.
  - **One statement corrected before commit.** Example 2 first said the H100/HBM3
    statement had no locator. The register has one: SRC-006's section on the H100 HBM3
    and HBM2e DRAM subsystems. Only the verbatim anchor is missing.
  - **Two downgrades, recorded as rules rather than records:**
    - "TSMC fabricates H100" reads a fabricator out of a process name, so it is a
      `DERIVATION` unless a source names the manufacturer (§12, example 1);
    - a single page's silence supports `not_researched`, not `not_publicly_determinable`
      (§9, example 2). S01's HBM-06 wording is scoped to "the product documentation
      retrieved", and S04 keeps that scope.
- **Retired:** none.

## Decisions made

| ID | Subject | Status |
|---|---|---|
| D-028 | Relationship record contract: `rel-` IDs, MA field names, `claim_ids` ≥ 1, optional dates; no `source_ids`, notes, status or confidence; endpoints on instantiable types only; no placeholder endpoints; shared shapes by `$ref` | proposed |
| D-029 | Eleven types at two levels (`requires`, `has_part`; nine instance types); one verb, one level; direction convention; ownership is an edge, not derived from events; activity edges target products only | proposed |
| D-030 | Reconciliation of the three verb lists (taxonomy §6); one-home rulings keep every S03 field; DEP-10 and DEP-11 excluded | proposed |
| D-031 | `supplier` qualifier on `incorporates` using the D-025 contract; missing edge = not recorded; no general unknown-endpoint record in v1 | proposed |
| D-032 | No vendor-named packaging process and no constituent-level fabrication in v1; S10 must stop and propose | proposed |
| D-033 | Role/edge conflicts RW-1 to RW-3 are warnings, never corrections; `validate-data` rules V-1 to V-9 handed to S06/S07 | proposed |

### Rejected verbs and alternatives

Each decision record lists its own. The main ones:

- **Rejected as vague:**
  - `manufactures` and `produces`: umbrellas over fabrication and packaging (TQ-06);
  - `uses`: it covers inclusion, necessity and service use;
  - `partners_with`;
  - `affected_by`: no evidence expectation can be written for it.
- **Not stored:**
  - `depends_on` and `competes_with`: derivations;
  - `enables` and `part_of`: stored inverses;
  - `is_a`, `subclass_of` and `instance_of`: taxonomy is a field.
- **Other alternatives rejected:**
  - one verb for both levels;
  - company → class edges (they restate roles);
  - a `located_in` edge;
  - record-level `source_ids`;
  - a confidence score;
  - a process or packaging-process qualifier;
  - a `part` qualifier;
  - an unknown-endpoint record;
  - a service → facility edge;
  - symmetric types;
  - a graph library.

## Deviations

1. **The S04 prompt came from an unmerged commit.**
   - `sessions/prompts/S04-PROMPT.md` was committed as `e23965c` on the S03 branch after
     PR #3's head (`f719ffb`), so it never reached `main`.
   - Gate 0 requires a report to have a matching prompt. S04 therefore brought the file
     in by cherry-picking `e23965c`, which keeps its original commit message.
   - Before finding that commit, the session had transcribed the prompt from the session
     message into the working tree. That transcription was **byte-identical** to the
     committed file (`diff` empty). It was deleted and replaced by the cherry-pick, so
     the prompt the session worked from is the committed one.
   - Part B §12 does not list this file, and §10 draws the write boundary at
     `sessions/reports/`. This is recorded here rather than silently absorbed.
2. **Part A and Part B, both followed.** Part A lists four claim labels. CLAUDE.md §6
   adds `ATTRIBUTION`, and all five are used, as Part B §09 directs.
3. **Test helpers imported, not copied.**
   - `test_relationship_schema.py` imports `mutate` from `test_entity_schema.py`.
   - `test_relationship_taxonomy.py` imports `cells`, `section`, `decision_exists` and
     `resolve_target` from `test_entity_taxonomy.py`.
   - This keeps one home for each helper, but the imports only resolve under
     `unittest discover -s tests`, which is how CI and the README run them (Debt).
4. **Naming against S03 prose.**
   - `entity-taxonomy.md` §9 calls composition "`part_of`". S04 stores it as `has_part`
     (whole → part) and keeps "part of" as its display reading.
   - The reason is the direction convention (D-029). This is S04's own vocabulary call,
     not a change to an accepted field or decision.
5. **An error caught before commit.**
   - While drafting D-030, hand-typed counts ("adopted, 9", "merged, 6") were wrong: the
     table gives 8 and 5.
   - They were removed from the decision, and a test now checks the remaining prose
     counts against the schema (L-04).
   - No incorrect count was committed.

## Debt introduced/resolved

**Introduced:**

- **More Markdown parsing.** The consistency tests now read tables in MA §6.2, the roadmap,
  the domain map and the new taxonomy.
  - A reformatted table fails loudly.
  - The parser also asserts the width and row count of the domain-map DEP table, so it
    cannot skip rows silently.
- **Cross-module test imports** (Deviation 3). If they become a problem, move the helpers
  into a `tests/_helpers.py` module.
- **Kind constraints are documented, not enforced.** Use class, facility kind and product
  kind (taxonomy §2) need the endpoint records. They wait for `validate-data` (V-2).
- **The placeholder ban is a heuristic word list.** An unlisted word such as
  `company-mystery-supplier` would pass. V-9 in `validate-data` and identity evidence
  (`identity_claim_ids`) are the real guards.
- **§2 repeats endpoints and levels from the schema.** This is a checked overlap: a test
  fails on any disagreement.
- **Deliberately unrepresentable in v1** (each recorded, each with an owner):
  - which facility fabricates or packages a product;
  - a service → facility link;
  - constituent-level fabrication;
  - vendor-named packaging processes;
  - an unknown party with no edge to hang it on.

**Resolved:**

- `baseline.md` §4's open item: the verb lists are reconciled, and machine-checked.
- `entity-taxonomy.md` §9's S04 row: ownership, operation, composition, and design,
  fabrication and packaging now have homes. The CoWoS question has a ruling (D-032).

## Unresolved issues

### Evidence gaps

- **DEP-01.** The H100 → HBM3 statement has a register locator but no verbatim anchor in
  the domain map. S10 must quote it.
- **DEP-05.** No retrieved anchor names NVIDIA as the H100's *designer*. The vendor field
  does not establish it.
- **DEP-05.** "TSMC fabricates H100" rests on a process name (`DERIVATION`).
- **The scope of `not_publicly_determinable`.** HBM-06's finding is scoped to the
  product documentation retrieved. S06 must decide what an NPD claim records about the
  search.
- **Type definitions are `INTERPRETATION`.** Industry scope comes from S01 entries: TSV
  formation vs reveal (PKG-07); package test as future scope; `packages` covering HBM
  stacking. No new source was retrieved.
- **Carried from S01 to S03, unchanged:**
  - blocked primary sources (JEDEC, TSMC, SEC, IEA and others);
  - CON-01 to CON-05;
  - the `not_researched` items in domain map §8;
  - ISO 3166-1 not in the register.

### Human approvals required

1. **D-028 to D-033.** Approve or amend each. The consequential points:
   - `uses`, `manufactures`, `produces`, `partners_with` and `affected_by` are rejected
     as vague; the four policy verbs are reserved for S17 (D-030);
   - composition is `has_part` (whole → part), not `part_of` (D-029);
   - class-level edges carry no dates (D-029);
   - no v1 type has a jurisdiction endpoint, so EU membership is future work (D-030);
   - unknown suppliers use the `supplier` qualifier, and there is no unknown-endpoint
     record (D-031);
   - CoWoS and the HBM4 base-die case are not modelled in v1 (D-032).
2. **Deviation 1:** accept the cherry-pick of the S04 prompt from the S03 branch.
3. **Deviation 3:** keep the cross-module test imports, or move the helpers into a shared
   module.
4. **Still open from earlier sessions:**
   - D-014 and D-015 (S05);
   - whether "external API dependency" becomes a non-goal;
   - S01's weekly gate;
   - the week-2 gate ("ontology and evidence policy understandable"), after S05.
5. **Merging this branch:** no pull request has been opened.

## Process lessons

- **Part B made a difference.** S02 and S03 worked from short prompts. S04's Part B gave:
  - the exact field list for the one-home rulings;
  - the three verb sources to reconcile;
  - the minimum invalid cases;
  - the stop conditions.

  Each became a machine check. No time went on re-deriving the contract, and no design
  question had to be put to the human, because Part B had already located the approval
  boundaries.
- **The source-list test found a silent parser bug.**
  - A table width of 8 instead of 7 dropped the domain map's Verb column, so four verbs
    looked absent.
  - The "In" column cross-check (every verb's list membership, parsed from its own
    document) caught it, which a count check would not have.
  - The parser now asserts width and row count, and the S03 lesson is extended: *check
    what was read, not just what was expected.*
- **Deliberate breakage covered inputs outside the session's own files.** Break 9 changed
  a verb in the domain map. The reconciliation test failed, which shows the table tracks
  its source document and not a hard-coded list.
- **Hand-typed counts go wrong even in a decision record** (Deviation 5). L-04 is now
  enforced by a test for the counts that remain in prose.
- **Worked examples found rules again.** Taking SRC-006 apart showed three things:
  - a process name is not a fabricator statement;
  - a vendor is not a designer;
  - one page's silence is not "not publicly determinable".

  All three became evidence-expectation rules (§5, §9) before any edge exists.

## Implications for the next session

**Handoff: S05, Source hierarchy and evidence policy (RESEARCH / ARCHITECTURE).**

- **Completed work:** the relationship vocabulary, its schema and its tests (proposed),
  running in CI alongside the entity schema.
- **For S05:** taxonomy §5 is the evidence-expectation table.
  - It has one row per relation type: what the source must show, what is not enough on
    its own, and what is typically non-public.
  - Below it is the entity identity-evidence expectation (`identity_claim_ids`, D-025).
  - S05's gate assigns a preferred source class to each row. The table states *what* the
    evidence must show, never *which tier*.
- **Open issues:**
  - the human approvals above;
  - D-014 and D-015, which fall to S05;
  - the `validate-data` rules V-1 to V-9, which include references, endpoint records,
    kind constraints and role/edge warnings (for S06/S07);
  - what a `not_publicly_determinable` claim must record about the search (S06).
- **Recommended next decision:** the human reviews D-028 to D-033 before S05 starts,
  because S05's source classes attach to S04's relation types.
- **Files for S05 to read first:**
  1. this report;
  2. `docs/architecture/relationship-taxonomy.md` §5, §9 and §12;
  3. `docs/architecture/entity-taxonomy.md` §7;
  4. `docs/research/source-register.md`;
  5. `docs/architecture/decisions.md` D-014, D-015 and D-028 to D-033.
