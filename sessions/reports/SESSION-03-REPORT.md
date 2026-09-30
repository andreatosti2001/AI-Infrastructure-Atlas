# SESSION-03 Report — Entity taxonomy

- **Session:** S03 · **Type:** ARCHITECTURE · **Milestone:** M1 — Domain + Evidence Foundation
- **Date:** 2026-09-30
- **Prompt:** [`sessions/prompts/S03-PROMPT.md`](../prompts/S03-PROMPT.md)
- **Branch:** `claude/youthful-allen-rtfdu8`, created locally from `main` @ `f1948a1`
  (the S02 merge)
- **Base at start** (D-018 L-03):
  - `git branch -a` listed:
    - `claude/youthful-allen-rtfdu8` (local, at `f1948a1`);
    - `main`;
    - `remotes/origin/main`;
    - `remotes/origin/claude/youthful-allen-rtfdu8`.
  - The local `origin/main` ref was stale (`6413a02`). A `git fetch origin main` moved it
    to `f1948a1`, which is also `main` on the remote.
  - `git ls-remote` showed two other remote branches. Both are already merged into `main`:
    - `claude/atlas-architecture-baseline-jow618` (`26acdf9`);
    - `claude/magical-galileo-vwn13j` (`ce5b881`).
  - The designated branch did not exist on the remote. `git ls-remote` did not list it,
    and fetching it failed with "couldn't find remote ref". Its remote-tracking ref,
    listed above, was local only.

## Mission outcome

**Delivered for human review.**

| Deliverable | Where | Status |
|---|---|---|
| Canonical entity types, with the human-focus explanation of why the ten are distinct | [`docs/architecture/entity-taxonomy.md`](../../docs/architecture/entity-taxonomy.md) §1–§4 | proposed (D-022) |
| Machine-readable entity schema and controlled vocabularies | [`schemas/entities.schema.json`](../../schemas/entities.schema.json) | proposed (D-022 to D-025) |
| A home for every v1 concept in M0 Part 4 | taxonomy §5 | machine-checked |
| A disposition for every MA §6.1 and §5.1 entity type | taxonomy §6 | machine-checked |
| Schema behaviour tests and consistency checks, run in CI | `tests/test_entity_schema.py`, `tests/test_entity_taxonomy.py` | passing locally; CI not yet observed |

**Registry gate, "stable entity schema":** met for review, not approved. The schema is
tested, but D-022 to D-025 are `proposed`. "Stable" is the human's call.

**Restated contract** (operating-contract step 6, given to the human before any file was
written):

- **Mission:** define the minimum canonical entity vocabulary for the first vertical, with
  a clear test for why the ten named kinds are distinct.
- **Scope:**
  - entity types;
  - identity tests;
  - fields and vocabularies;
  - the mapping of the v1 concepts and the MA types;
  - tests.
- **Non-goals:**
  - relationship vocabulary (S04);
  - source policy (S05);
  - claim, source and event schemas;
  - any data records;
  - Policy and Institution schemas;
  - energy and networking;
  - edits to the root documents.
- **Acceptance:**
  - every v1 model and actor-role concept has exactly one home;
  - every MA §6.1 type has a disposition;
  - each type has a definition, an identity test and a "not" test;
  - any reclassification of a D-020 concept goes through a decision record;
  - the tests and Gate 0 pass.
- **Plan:**
  1. inspect;
  2. propose the design and ask the one blocking question;
  3. write the schema, the taxonomy, the fixtures and the tests;
  4. write the decisions;
  5. update the index, the baseline state rows and the README;
  6. validate;
  7. write this report;
  8. commit and push.

  The plan held, with one test-parser bug fixed along the way (Process lessons).

**Human decision taken during the session:**
- **Question:** "How far should S03 go in making the entity schema machine-checked?"
- **Answer:** "Schema + jsonschema tests (Recommended)". Recorded as D-026, accepted.

## Files changed

Added:

- `sessions/prompts/S03-PROMPT.md`: the human prompt (see Deviation 1).
- `docs/architecture/entity-taxonomy.md`:
  - design rules R-1 to R-8;
  - the record kinds at a glance;
  - the six instantiable types and two reserved types;
  - the human-focus explainer (§4: a decision guide, the confusable pairs, two worked
    examples drawn from S01 evidence, and the changes from MA §5.1);
  - the v1 concept mapping;
  - the MA dispositions;
  - the attribute contract;
  - the rejected candidates;
  - the handoffs.
- `schemas/entities.schema.json`: JSON Schema draft 2020-12, one branch per type. Every
  vocabulary value is a `const` with its own definition.
- `requirements-test.txt`: exact pins for `jsonschema` and its transitive dependencies
  (D-026).
- `tests/fixtures/entities.json`:
  - fictional valid records for every type;
  - invalid cases, each one JSON Pointer mutation of a valid base.
- `tests/test_entity_schema.py`: schema behaviour (uses `jsonschema`).
- `tests/test_entity_taxonomy.py`: consistency checks (standard library only).
- `sessions/reports/SESSION-03-REPORT.md`: this report.

Modified:

- `docs/architecture/decisions.md`:
  - D-022 to D-026 appended;
  - D-003's status line marked "amended by D-026".
- `.github/workflows/ci.yml`: a step installs `requirements-test.txt` before the tests.
- `docs/architecture/baseline.md`: dated state rows only (see Deviation 3):
  - the status note;
  - the §1 state table (the schema row split into entity and relationship);
  - the §4 sentence on the physical schema;
  - the §5 Gate 1 row and the `validate-data` row.
- `docs/README.md`: new "Data model" table.
- `README.md`: the status, layout and validate instructions, which were stale ("no
  schemas", "No third-party packages are needed").

Not modified:

- root constitutional documents;
- `tools/`;
- `docs/research/`;
- `milestone-audits/M0-audit.md`;
- `sessions/prompts/PROMPT-REGISTRY.md` (it already lists S03);
- anything in `Eu-Digital-Policy`, which was not opened.

## Data changed

- **Canonical or staging records:** none.
- **Schema:** the first physical schema, for six entity types (proposed).
- **Fixtures:** fictional (`Example …`, jurisdiction `ZZ`, `claim-fixture-…`). They assert
  nothing about the world.

## Tests run

Python 3.11.15. All commands ran locally from the repository root.

| Command / check | Result |
|---|---|
| `python -m unittest discover -s tests` (start, before changes) | OK (10 tests) |
| `python tools/validate_repo.py` (start) | `Repository integrity: OK` |
| First run of the new tests, before D-022 to D-026 existed | Failed as intended on the missing decisions. It also exposed a parser bug: rows with an empty cell were skipped, so 11 concepts looked unmapped. Fixed by splitting cells instead of using a regex |
| Fresh virtualenv, `pip install -r requirements-test.txt`, `pip freeze` compared with the pins | installed set = pinned set |
| `python -m unittest discover -s tests -v`, final, in that virtualenv | OK (26 tests) |
| `python tools/validate_repo.py`, final, with this report present | `Repository integrity: OK` |
| Error message printed for every invalid case, read by hand | each fails at the mutated path, for the stated reason |
| Deliberate breakage in scratch copies (the tests must fail) | all caught: (1) `additionalProperties` removed from company; (2) `locality` made optional; (3) PKG-07 mapping row deleted; (4) FAB-03 reclassification with its decision citation removed; (5) an MA disposition row dropped; (6) `osat` removed from the vocabulary |
| CI result | **not yet observed.** Local results only (D-018 L-08) |

Not applicable: data validation (no records), browser, accessibility, performance.

## Evidence added/retired

- **External sources:** none retrieved or added. `source-register.md` is unchanged.
- **Evidence cited:**
  - The taxonomy's worked examples and vocabulary definitions rest on S01 domain-map
    entries (FAB-05/SRC-006, HBM-03/SRC-014, DEP-04, DC-04/SRC-020, PKG-04/SRC-014, and
    others).
  - The quoted anchors were checked by hand against the domain map. They were not
    re-read against the sources in S03.
- **Retired:** none.

## Decisions made

| ID | Subject | Status |
|---|---|---|
| D-022 | Six instantiable types; `institution` and `policy` reserved; four record kinds owned elsewhere; Event schema proposed for S09 | proposed |
| D-023 | Dispositions of the MA §6.1/§5.1 entity-type lists; MA §5.1 example fields `jurisdiction`, `status`, `source_ids` not adopted | proposed |
| D-024 | Actor roles are claim-backed, time-bounded values on Company, never derived; FAB-03 reclassified from model to actor role; `equipment_maker` and `eda_vendor` added | proposed |
| D-025 | Attribute value contract: every field required; assertions with claims, or an explicit state; no null, zero-as-unknown, notes, status or layer | proposed |
| D-026 | Pinned test-only `jsonschema` dependency (amends D-003) | accepted (human, 2026-09-30) |

### Rejected alternatives

The main ones are listed here. Each decision record lists its own.

- **One type per MA §6.1 name** (`CloudProvider`, `Fab`, …). It would give one firm or site
  several records (R-1, R-3).
- **A single `Organisation` type** over Company and Institution. It would mix supply-chain
  actors with evidence and policy actors.
- **A separate `Equipment` type.** Its identity test is the same as Component's.
- **Optional or nullable attributes.** A missing field hides "not researched".
- **Record-level `source_ids`.** They cannot say which source supports which value.
- **Roles derived from relationships.** Incomplete data cannot establish an absence.
- **A stored `layer` field.** It is derivable from `concept_refs`.
- **A hand-written subset JSON Schema validator** (D-026).
- **Taxonomy document only, with the schema deferred.** Offered to the human and not
  chosen.

## Deviations

1. **Prompt encoding.** As in S02, the prompt arrived with UTF-8 punctuation mis-decoded
   ("â€”", "â†’"). `S03-PROMPT.md` records the decoded text. The wording is unchanged.
2. **No SESSION-PROMPT-SPEC §2 Part B.**
   - The S02 handoff recommended writing S03's prompt in §2 form before S03 started. The
     prompt received is the short human form.
   - The restated contract above stands in for it, as in S02.
3. **An approved record was edited.**
   - `baseline.md` was approved in S02. S03 changed only its dated state rows, which were
     now false: the rows saying no schema exists.
   - The approved sections (§2 boundaries, §6 non-goals, §8 approval record) are
     untouched.
   - The human may prefer the baseline to be a frozen start record. If so, these edits
     should be reverted and the state tracked in `docs/README.md` only.
4. **Plan approval (improves on S02 Deviation 4).**
   - The one choice that touched an accepted decision (D-003) was put to the human before
     any file was written.
   - The rest of the design was not held for approval. It is delivered as `proposed`
     decisions, so no approval boundary was crossed.
5. **Touches on other sessions' ground, each recorded:**
   - the claim ID format is fixed for referencing (D-025; S06 may change it);
   - S09 is proposed as the Event schema owner (D-022);
   - the relationship constraints S04 should respect are listed (taxonomy §9).

   None of these creates a claim, event or relationship schema.

## Debt introduced/resolved

**Introduced:**

- **Markdown tables parsed by tests.**
  - The consistency checks read the tables in the taxonomy, M0 Part 4 and MA §5.1/§6.1.
  - A reformatted table fails the tests loudly. It does not pass silently, but it is
    coupling to layout.
- **No record validator.** Several checks exist only as a plan (taxonomy §9), for
  `validate-data` in S06/S07:
  - references resolve;
  - IDs are unique;
  - `broader` is acyclic;
  - `valid_from` ≤ `valid_to`;
  - jurisdiction IDs appear on the ISO list.
- **M0 Part 4 now differs from the live classification by one concept** (FAB-03).
  - Taxonomy §5 records the move and cites D-024.
  - A reader of M0 Part 4 alone would not see it. This is the same pattern as S02's
    domain-map debt, and it is left for the same reason: accepted artifacts are not
    rewritten.
- **Local runs need `pip install -r requirements-test.txt`.** The README now says so.

**Resolved:**

- S02's "scratch cross-reference check" debt, **partly.**
  - Concept IDs, decision and NG references, and schema targets in the S03 artifacts are
    now checked in CI.
  - References across all the other documents are still unchecked.
- The stale "no schemas" statements in `README.md` and `baseline.md`.

## Unresolved issues

### Evidence gaps

- **ISO 3166-1** is the identifier basis for jurisdiction IDs, but the standard is not in
  the source register. To be added in S07 with the first jurisdiction records.
- **Terms with no S01 concept entry:** `equipment_maker`, `eda_vendor` and
  `packaging_facility`. Their definitions are `INTERPRETATION`, drawn from domain map
  §4's table. Each assignment to a record will need its own claim.
- **Vocabulary definitions** paraphrase S01's attributed definitions. S03 did not
  re-verify them against the sources.
- **Carried from S01/S02, unchanged:**
  - blocked primary sources (JEDEC, TSMC, SEC, IEA and others);
  - CON-01 to CON-05;
  - the `not_researched` items in domain map §8.

### Human approvals required

1. **D-022 to D-025.** Approve or amend each. The consequential points:
   - "Country" becomes the type `jurisdiction` (D-022);
   - MA's `CloudProvider`, `EquipmentSupplier`, `Fab`, `PackagingFacility`, `DataCentre`
     and `ChipDesign` are not types (D-023);
   - FAB-03 is reclassified (D-024);
   - every field is required, with explicit states (D-025).
2. **Event schema owner:** S09 is proposed (D-022). The roadmap names no owner.
3. **Which session creates product records:** S08 or S10. Unassigned, and needed before
   S08.
4. **Baseline edits** (Deviation 3): keep them, or revert and freeze the baseline as a
   start record.
5. **Still open from earlier sessions:**
   - D-014 and D-015;
   - whether "external API dependency" becomes a non-goal;
   - S01's weekly gate.
6. **Merging this branch:** no pull request has been opened.

## Process lessons

- **Fail-first confirmed the checks were real.**
  - The consistency tests failed until the decisions they cite existed.
  - Six deliberate breakages were each caught.
  - Without the breakage run, a parser that skips rows could have passed a table it
    never read. The first run showed exactly this before the parser was fixed.
- **Mutation-based negative fixtures** keep invalid cases honest. Each is one change to a
  record known to be valid, so it cannot fail for an unrelated reason. Reading the error
  message for each case confirmed this.
- **Worked examples found the rules.** Breaking one S01 sentence (SRC-006) into record
  kinds showed what the sentence does *not* support: no fab location and no event date.
  That became R-5 and the explicit-state rule, before any real record existed (L-09 in
  spirit).

## Implications for the next session

**Handoff: S04, Relationship taxonomy (ARCHITECTURE).**

- **Completed work:** entity types, schema and vocabularies (proposed), with tests in CI.
- **Open issues:**
  - the human approvals above;
  - no record validator yet.
- **S04 must respect** (taxonomy §9, D-025):
  - endpoints typed by entity type and `use_class`;
  - no taxonomic `is_a` or `subclass_of` relationship (taxonomy is `broader`);
  - ownership, operation, composition and design/fabrication/packaging are relationships,
    never entity fields;
  - a place to hold vendor-named processes on edges (the CoWoS case);
  - reconcile MA §6.2 with the roadmap's S04 list (baseline §4);
  - the verbs S01 proposed (domain map §3).
- **Recommended next decision:** the human reviews D-022 to D-025 before S04 starts,
  because S04's endpoint rules depend on the types.
- **Files to read first:**
  1. this report;
  2. `docs/architecture/entity-taxonomy.md` (§1, §3, §4.2, §9);
  3. `schemas/entities.schema.json`;
  4. `docs/research/domain-map.md` §3 (dependencies and proposed verbs);
  5. `docs/architecture/decisions.md` (D-022 to D-026).

## Addendum — human review outcome (2026-09-30)

Appended after the human's review of the S03 output. The sections above are unchanged.

- **CI:** run 15 on `4113e48` completed with `success`
  (<https://github.com/andreatosti2001/AI-Infrastructure-Atlas/actions/runs/36739053651>).
  This replaces "not yet observed" in Tests run.
- **Decisions accepted:** D-022, D-023, D-024 and D-025 ("Approve all four"). With D-026,
  every S03 decision is now accepted. The registry gate, "stable entity schema", is met.
- **Event schema owner:** S09 ("S09 (Recommended)"), noted on D-022's status line.
- **First product records:** S08 ("S08 (Recommended)"), recorded as **D-027**. The S08
  prompt must include them.
- **Baseline edits** (Deviation 3): kept ("Keep (Recommended)"). The baseline's dated
  state rows are updated when they become false; its approved sections are not.
- **Documents updated to match:** the taxonomy and schema status lines, taxonomy §2,
  §3.5, §6 and §9, `docs/README.md`, the baseline state rows and `README.md`.
- **Merge:** the human asked for this branch to be merged into `main`.
- **Still open, not covered by this review:**
  - D-014 and D-015;
  - whether "external API dependency" becomes a non-goal;
  - S01's weekly gate.
- **Updated handoff to S04:** S04 may start. Its endpoint rules can rely on the accepted
  types, and its prompt should list the constraints in taxonomy §9.
