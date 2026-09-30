# AI-Infrastructure-Atlas — S07 Session Prompt

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

Company dataset

Start a small, curated company seed set.

Human focus:
- manually inspect a sample of canonical entities and identity evidence.

**Milestone M1 complete.**

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
> - Everything above this line is **Part A**. For S05 and S06, the human uploaded Part A.
>   For S07, no upload was made: the human asked Claude to "write session 07 according to
>   the protocol of every session".
>   - Claude assembled Part A from the fixed template: the operating contract, report
>     list and headings are byte-identical in S05 and S06 Part A, and are copied here
>     unchanged.
>   - The session-specific mission is copied verbatim from the operational roadmap's
>     week-3 entry for S07 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`, "S07 —
>     Company dataset", including the line "**Milestone M1 complete.**").
>   - As with D-011, Part A was drafted by Claude. **The human confirmed it as
>     assembled** before S07 started ("Confirm as assembled (Recommended)", 2026-09-30).
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2. It was written after S06 was merged to `main` (PR #10,
>   `9424ebb`). It carries S06's findings forward: `SESSION-06-REPORT.md`,
>   `claim-model.md` §16, D-044 to D-053.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The
>   higher-level documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The prompt becomes immutable once S07 begins (D-011).
> - **Answered before S07 started (2026-09-30):** the human answered H-0 to H-6 in §16,
>   choosing Claude's recommendation each time, and confirmed Part A. H-0 (the S06
>   review) was applied before this prompt reached `main`.

## 01 — Session identity

- **Session:** S07
- **Title:** Company dataset
- **Type:** RESEARCH / IMPLEMENTATION (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`). It
  retrieves first-hand evidence for a small set of companies, and builds their records
  and the checks that make them canonical.
- **Milestone:** M2 — Canonical Dataset (`SESSION-ROADMAP.md` numbering, D-019). S07 is
  M2's first session.
- **Milestone label conflict:**
  - Part A copies the operational roadmap's line "**Milestone M1 complete.**", which the
    operational roadmap prints after S07.
  - In `SESSION-ROADMAP.md` numbering, which D-019 makes the meaning of a bare label, M1
    is S03–S06 and closed with S06.
  - So the line is read as the operational roadmap's own checkpoint: the end of its
    week 3, a human judgement after S07. It is not a claim that S07 belongs to M1.
  - M1's milestone audit is the question in §06 q12 and §16 (H-5).
- **Predecessor:** S06 — Evidence/claim system (merged to `main` at `9424ebb`, PR #10).
  D-044 to D-053 were accepted at the S06 review (§16, H-0; commit `5b22515`).
- **Expected successor:** S08 — Technology + component dataset (with the first product
  records, D-027).
- **Complexity class:** large. It creates:
  - the first entity records;
  - the first sources retrieved since the register was frozen;
  - the first claims that records cite;
  - the first record-level checks (V-1, V-9, V-10);
  - the first freshness check.

  §16 lets the human narrow it.
- **Weekly gate:** the operational roadmap's week-3 checkpoint follows S07 (human
  judgement, see above).

## 02 — Mission

Create a small, curated, evidence-backed seed set of company records, the first canonical
entities of the Atlas. Each has:

- a stable ID, chosen by a rule;
- identity claims that trace to the company's own first-hand documents;
- its attributes (`legal_name`, `incorporated_in`, `headquartered_in`, `roles`), each
  either claim-backed or an explicit state.

- **Records.** Companies, and the jurisdiction records their attributes point to (§16,
  H-4).
- **Evidence.** New source records, retrieved under the S05 rules, and claims in the S06
  shape.
- **Checks.** The record-level `validate-data` rules the records need: V-1, V-9, V-10.
  Also the first `validate-freshness` rule, for the `time_sensitive` company rows.
- **Human learning** (Part A): the human inspects a sample of canonical companies and
  their identity evidence by hand.

The result must make three things impossible:

- a canonical company record without identity evidence that traces to a first-hand
  source, or with an ID that could change when its display name changes;
- a company attribute whose value is inferred, such as a role read off relationships, a
  headquarters read off a facility, or a company read off a brand, instead of stated by a
  source or given as an explicit state;
- a canonical record resting on an unreviewed claim.

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S07: "Build the first curated company dataset
across the initial stack". Target: "A small, high-quality seed set rather than maximum
coverage". Coverage: "Accelerators, memory, packaging, foundries, equipment, selected
cloud/data-centre actors". Gate: "Every canonical company record has identity evidence
and stable IDs."

**Every later record needs companies.**

- Products need a `vendor` (S08, D-027).
- Facilities are owned and operated by companies (S09).
- Most S10 edge types have a company endpoint.
- The S06 source records wait for them: 16 company-published sources have
  `publisher_entity: not_researched` (as measured at `9424ebb`), so standing's party
  test cannot yet be automated (`source-policy.md` §4, D-050).

**S06 handed S07 a list** (`SESSION-06-REPORT.md`, Implications; `claim-model.md` §16):

- **How to cite:**
  - `identity_claim_ids` and attribute `claim_ids` point to claims in the S06 shape;
  - the matrix rows `identity:company` and `attr:company.*` prefer `company_filing` and
    `government_publication`, with `party` or `originator` standing
    (`source-policy.md` §7);
  - filings come from the filer's own copy (D-042), recording `filing_copy`.
- **Switch on:**
  - V-1, references resolve, including `publisher_entity`;
  - V-9, no placeholder slugs;
  - V-10, a record rests on classes and standing its matrix row allows;
  - `validate-freshness` for the `time_sensitive` company rows (D-040's 12 months).
- **Decide** how anchors from new retrievals are machine-checked, or accepted as
  hand-checked, before the first one (VD-11).
- **Move** accepted S06 seed claims to `data/claims.json`, on the human's verdicts only.

**Earlier handoffs that land here:**

- `entity-taxonomy.md` §9: "Registering the ISO 3166-1 standard as a source | S07, with
  the first jurisdiction records"; `validate-data` rules for entities (IDs unique,
  references resolve, jurisdiction IDs on the ISO list).
- `source-policy.md` §7, row `identity:jurisdiction`: "ISO 3166-1 is not yet in the
  register (gap)"; §16: "ISO 3166-1 as a registered source … S07 or the first session
  that creates a jurisdiction record".
- `relationship-taxonomy.md` §15: V-1 and V-9 "S06/S07, with the first records".

**A process obligation with no session assigned** (§06 q12): PEF §4 requires a milestone
audit "At every major milestone". M0's is `milestone-audits/M0-audit.md` (S02). M1
(S03–S06) closed with S06, and no M1 audit exists or is scheduled.

## 04 — Current state

As of `main` @ `9424ebb` (PR #10), plus the S06 review commit (`5b22515`) and the commit
that adds this prompt. Verify at start,
and record the base, the `git branch -a` result and `git ls-remote` in the report (D-018
L-03).

**This prompt must be on `main` before S07 starts** (the S04 Deviation 1 lesson).

**Accepted model:**

- entity types and fields (D-022 to D-025): `schemas/entities.schema.json`;
- relationship record (D-028 to D-033): `schemas/relationships.schema.json`;
- source classes, standing, the preference matrix and the evidence, conflict, retrieval
  and freshness rules (D-034 to D-043): `docs/research/source-policy.md`;
- filings from the filer's own copy (D-042); no external API (NG-14, D-043);
- D-026: `jsonschema` pinned for tests only; `tools/` stays standard library.

**Accepted at the S06 review** (D-044 to D-053; §16, H-0):

- `docs/architecture/claim-model.md` covers:
  - claim types and evidence status;
  - the §4 type × status tables;
  - citations, `verified`, and staging vs canonical;
  - the search record;
  - the migration;
  - `validate-data` VD-1 to VD-13;
  - the trace.
- `schemas/claims.schema.json`, and the source record in `schemas/sources.schema.json`.
- `data/sources.json`: `src-001` to `src-024`. The register is frozen.
- `data/staging/claims.json`: ten seed claims, all `supported`, all `not_reviewed` (as
  measured at `9424ebb`).
- `tools/trace.py`; `docs/agents/roles.md` and `docs/agents/contracts.md`.

**Tests:** 157, as measured at `9424ebb` in a fresh virtualenv. CI run 43 succeeded on
the S06 head.

**Files S07 builds on:**

- `schemas/entities.schema.json`: `company` (fields `name`, `aliases`,
  `identity_claim_ids`, `legal_name`, `incorporated_in`, `headquartered_in`, `roles`),
  `jurisdiction`, `vocab_actor_role`, the attribute contract;
- `docs/architecture/entity-taxonomy.md` §3.1 (company identity: "one record per legal
  entity as sources name it"; parent and subsidiary), §3.6 (jurisdiction), §7;
- `docs/research/source-policy.md` §4, §6 (ER-8, ER-9), §7 (rows `identity:company`,
  `identity:jurisdiction`, `attr:company.*`), §8.3 (S05-R1 anchors), §11 (RA-1 to RA-7),
  §12;
- `docs/architecture/claim-model.md` §1, §4, §5, §7, §9, §11, §16;
- `tests/test_data_integrity.py`, `tests/test_data_schema.py`, `tools/trace.py`.

**No entity records exist, and no entity data file exists.** The layout is S07's to
choose, within H-2 of S06 (§16, H-2).

**Open items S07 inherits:**

- the S06 seed-claim verdicts: none given, and the ten claims stay `not_reviewed`
  (S06 review addendum);
- S01's weekly gate;
- S05 debt: the §2 class table vs the §7 matrix; S05-R1's anchors hand-verified only;
  SRC-023 not re-read;
- S06 debt: VD-11's scope; `publisher_entity`; V-10; freshness;
- the M1 milestone audit (§06 q12).

**Not S07's:**

- technology, component and product records (S08, D-027);
- facilities and site locations (S09);
- relationship records, including `owns` from a filing's subsidiary list and `supplies`
  from its supplier paragraph (S10);
- events, such as an announced plan or an acquisition (S09);
- metrics (S14–S15, NG-11).

**Next decision number:** D-054.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-06-REPORT.md`, including any addenda.
2. `docs/architecture/claim-model.md`.
3. `schemas/entities.schema.json` (`company`, `jurisdiction`, the attribute contract),
   `schemas/claims.schema.json`, `schemas/sources.schema.json`.
4. `docs/architecture/entity-taxonomy.md` §3.1, §3.6, §7, §9.
5. `docs/research/source-policy.md` §4, §6, §7, §8.3, §11, §12.
6. `docs/research/domain-map.md`: the actor-type entries (ACC-04, HBM-06, PKG-07, FAB-03,
   FAB-04, DC-04) and §6.
7. MA §5.1, §5.7, §6.1, §11.6–11.7, §14 Gates 1–3, §15.
8. PEF §4 (milestone audit) and §5 (data architecture audit).
9. `docs/architecture/decisions.md`: D-005, D-018 (L-01 to L-09), D-022 to D-025, D-027,
   D-033, D-036, D-040, D-042 to D-053.
10. `SESSION-ROADMAP.md` S07 to S10; the operational roadmap's week-3 and week-4 entries.

**Repository paths to inspect:** `data/`, `schemas/`, `tests/`, `tools/`, `docs/`,
`.github/`.

**External research: expected.** This is the first S0x session since S01 that retrieves
new sources. Every retrieval follows `source-policy.md` §11:

- raw HTTPS (RA-1), no circumvention (RA-2);
- filer-hosted copies of filings (RA-6, D-042); no identity declared to any site (RA-7);
- no external API (NG-14);
- manual retrieval by the human only under RA-4, targeted, with a list the session gives
  the human.

Web search only discovers URLs. A snippet is never evidence. Every new source becomes a
record in `data/sources.json`, never a register row.

**Candidate companies** (`INTERPRETATION`; the human sets the seed in §16, H-1). Each is
named in a registered source or the domain map, so the seed stays inside the first
vertical:

| Layer | Candidate | Why it is a candidate | Evidence already registered |
|---|---|---|---|
| Accelerators | NVIDIA | ACC-04; the S06 seed claims | SRC-006, SRC-007; S05-R1 (`src-024`), its 10-K |
| Memory | SK hynix | HBM-06; four registered sources | SRC-011 to SRC-014 |
| Memory | Micron | HBM-06; named in S05-R1 p.8 | SRC-015 |
| Packaging | Amkor | PKG-07 (OSAT) | SRC-016 |
| Foundry | TSMC | FAB-03; named in S05-R1 p.8 and FAB-05 | none of its own (its hosts refused in S01) |
| Equipment | ASML | SME-03 | SRC-017 |
| EDA | Synopsys | EDA-01 | SRC-018 |
| Cloud | Amazon (AWS) | DC-04; the S06 seed claims | SRC-010, SRC-020 |

Other firms in the registered sources (Google, Lam Research, Samsung, Intel) are not
candidates in the recommended seed. Samsung's and Intel's hosts refused in S01.

**Audit findings to carry:**

- **A-1, L-01: machinery before a used loop.** Only checks that run on the S07 records;
  no runtime.
- **L-02:** a gate only if CI runs it.
- **L-04:** no hand-typed counts in prose; they are tested or labelled "as measured at
  `<commit>`".
- **L-05:** each new data file joins `validate-data` in the session that creates it.
- **L-06:** verification dates per record.
- **L-09:** every company field is filled by hand for at least one company, and each
  record-level check is hand-applied to real records, before it is automated.
- **S06's process lessons:**
  - reading the sentence changes the claim (the GH100 finding);
  - the Verifier must re-check the session's own locators, which are free text no test
    reads;
  - break tests must show which tests fail, not only that one does.

## 06 — Required reasoning

Answer these before writing records. The answers go into a company-dataset document (§07
task 1) and the decision records.

1. **The seed** (§16, H-1).
   - Which companies, by what rule: at least one per chain layer (MA §6.4), each named in
     a registered source or concept?
   - What makes the set "curated" rather than "complete"? Record what is left out and
     why (NG-03).

2. **Which legal entity** (`entity-taxonomy.md` §3.1: "one record per legal entity as
   sources name it"; a parent and a subsidiary are two records only when the evidence
   needs both).
   - For each candidate, which entity do the first-hand sources name?
     - "Amazon Web Services" vs Amazon.com, Inc.
     - "SK hynix Newsroom" vs SK hynix Inc.
     - the filer of a 20-F vs its operating subsidiary.
   - When does a brand stay an alias, and when does it need its own record?
   - Record parent/subsidiary questions as open. The `owns` edge is S10's.

3. **Stable IDs.**
   - A rule for `company-<slug>`:
     - from which name (legal name without its legal-form suffix? the common name?);
     - how collisions and renames are handled (a renamed company keeps its ID, §3.1);
     - whether the rule is machine-checked.
   - The rule must never make an ID depend on a value that can change.
   - Check each slug against V-9 (placeholder slugs) and the schema pattern.

4. **Identity claims.**
   - What does an identity claim state: that a legal entity with this name exists, and is
     a company?
   - Which sentence of a filing states it (e.g. S05-R1 p.1, "(Exact name of registrant as
     specified in its charter)")?
   - Can one `FACT` serve `identity_claim_ids` and `legal_name` at once? D-044 allows one
     claim to serve two fields.
   - Standing must be `party` (the filer about itself) or `originator` (a registry). The
     row is `identity:company`.
   - Apply V-10 by hand to each before writing the check (L-09).

5. **Attributes.** For each of `legal_name`, `incorporated_in`, `headquartered_in` and
   `roles`:
   - the sentence that states it;
   - its claim type;
   - `as_of` and `valid_from`/`valid_to`.
   - All four rows are `time_sensitive` (`source-policy.md` §7).
   - A role needs a sentence that states the business model ("fabless", "foundry",
     "OSAT", "cloud"); it is never derived from edges (D-024). No such sentence means
     `not_researched`.
   - A headquarters is never read off a facility or a stock listing (R-5).
   - ER-8 (forward-looking statements) applies inside filings too.

6. **Jurisdictions** (§16, H-4).
   - The attributes point to `jurisdiction-xx` records. Which are needed?
   - The row `identity:jurisdiction` prefers `standard_specification` with `originator`
     standing (ISO 3166-1) and accepts `government_publication`.
   - Can ISO's own publication of the codes be retrieved under RA-1 and RA-2? If not, what
     is recorded, without a secondary list standing in for the standard (RA-5)?
   - The code is an identifier, and states no position on sovereignty (§3.6).

7. **Staging and canonical for entities** (§16, H-3).
   - The accepted entity schema has no review field, and S07 must not add one without a
     decision the human approves first (§08). What makes an entity record canonical?
   - Candidate: its file (staging or canonical, as for claims), plus a rule that a
     canonical record cites only canonical claims (extends VD-8).
   - How the human's verdicts on identity claims are gathered and recorded, and when
     records move.
   - The S06 seed claims stay in staging unless the human's verdicts are recorded.

8. **New sources and their anchors** (§16, H-6).
   - Every retrieval records method, time and hash; filings record `filing_copy`.
   - VD-11 machine-checks anchors only for S01/S05 readings. For new sources, the full
     text stays outside the repository (RA-4(4)).
   - Decide how their anchors are checked: the Verifier's `read` hash, a human sample, or
     both. Record it in a decision before the first new claim.

9. **`validate-data` for records.**
   - V-1: every entity reference resolves, including `publisher_entity` and every
     `claim_ids`.
   - V-9: no placeholder slugs.
   - V-10: the classes and standing of each record field's claims suit its matrix row.
     This needs `source-policy.md` §7 parsed from its home, never copied.
   - V-2 to V-8 need relationships (S10). Say which, if any, applies to entities
     (e.g. jurisdiction IDs on the ISO list, from `entity-taxonomy.md` §9).
   - Each rule is hand-applied to the real records first, and caught in a deliberate
     break.

10. **Freshness.**
    - The first `validate-freshness` rule: for `time_sensitive` rows, evidence whose
      `as_of` (or publication date, when there is no `as_of`) is more than 12 months
      before the record's use must have been re-checked (D-040).
    - What is "use" for a record committed today?
    - Where the rule runs: a test, as H-4 of S06 placed `validate-data`.

11. **`publisher_entity`.** For each of the 16 company-published sources, is the
    publisher one of the seed companies, as a legal entity (q2)?
    - Set the reference only where the evidence shows it.
    - The newsroom and blog publishers ("SK hynix Newsroom", "NVIDIA Technical Blog") are
      the q2 question in miniature.

12. **The M1 milestone audit** (§16, H-5).
    - PEF §4's eight questions over S03–S06: intended, implemented, changed, failed
      assumptions, shortcuts, debt, rejected, carry-forward.
    - Where it is done, and whether it blocks the data work.
    - It is a document, not a code change (PEF §4; `milestone-audits/M0-audit.md` is the
      precedent).

13. **The S07 gate** ("Every canonical company record has identity evidence and stable
    IDs"). Which checks prove it in CI?
    - Every canonical company has at least one canonical `identity_claim_ids` claim whose
      class and standing suit `identity:company` (V-10).
    - IDs follow the q3 rule.
    - `tools/trace.py` prints each company's evidence, with `--records` pointing at the
      new files.

14. **The human's manual inspection** (Part A).
    - A review sheet for a sample of canonical companies: the record, each identity
      claim's source, locator and anchor, and a question per field ("does the filing say
      this, and no more?").
    - Where the human's findings are recorded, and what changes when they find a problem.

## 07 — Tasks

**Audit and design**

1. The M1 milestone audit, if §16 H-5 places it in S07:
   `docs/architecture/milestone-audits/M1-audit.md`, with a row in
   `docs/quality/audit-history.md`.
2. `docs/architecture/company-dataset.md`: the answers to §06. It covers the seed and
   what is left out, the legal-entity rulings, the ID rule, the claim pattern for
   identity and each attribute, jurisdictions, staging and canonical, new-anchor
   checking, the V-1/V-9/V-10 and freshness definitions, and the review sheet. It
   references `claim-model.md`, `source-policy.md` and `entity-taxonomy.md` by section and
   never restates them (A-5).

**Research**

3. Retrieve the first-hand identity sources for each seed company:
   - filer-hosted filings first;
   - `government_publication` registries where the filing is unavailable;
   - otherwise the acceptable classes of `identity:company`, with the gap recorded.
   - Record every refusal as an access gap. List any RA-4 manual retrievals the human
     should make, and stop for them (§16).
4. Register each new source in `data/sources.json` (`src-025` onward), with class,
   `filing_copy`, retrieval and stated dates.
5. ISO 3166-1, if §16 H-4 allows it: its source record, and the jurisdiction records the
   seed needs.

**Implementation**

6. **Claims.** Identity and attribute claims in `data/staging/claims.json`, verified by
   the Verifier against the bytes read, with `read` recorded. Anchors are checked as
   decided under §06 q8.
7. **Records.** Company and jurisdiction records in the layout §16 H-2 chooses, first in
   staging.
8. **`publisher_entity`** set where §06 q11 shows it. The migration test ignores this
   field (D-050).
9. **Checks.** V-1, V-9 and V-10 for entities, the freshness rule, and the canonical-entity
   rule (extending VD-8), in CI (L-02, L-05). A test enforcing the ID rule, if §06 q3
   makes it checkable.
10. **Promotion.** The human's verdicts on the identity claims (§16 H-3). Accepted claims
    and the records resting on them move to the canonical files. The S06 seed claims move
    only on their own verdicts.
11. **Tests:**
    - entity fixtures remain the S03 ones. New fixtures cover the new checks;
    - each check's planted fault is caught;
    - prose counts are tested or labelled (L-04);
    - every cited decision, section, source and concept exists.

**Validation**

12. **Fail first:** the new checks fail before the records exist. Then break things
    deliberately in scratch copies, at least eight ways, each caught. Include:
    - a company citing a claim that does not exist;
    - a company whose `incorporated_in` points to a missing jurisdiction;
    - an identity claim from a class the `identity:company` row never allows alone;
    - an identity claim with `reporter` standing;
    - a canonical company citing a staging claim;
    - a placeholder slug (`company-unknown`);
    - a role asserted with no claim;
    - a `time_sensitive` value older than 12 months, not re-checked;
    - a changed display name that would change an ID under a bad rule.

**Documentation**

13. Decisions from D-054, each `proposed`.
14. `docs/README.md` (company dataset; M1 audit), the baseline state rows (§1, §4, §5),
    `README.md`, `docs/agents/contracts.md` only if a contract's paths change (e.g. the
    new data files in the Extractor's allowed writes).
15. `sessions/reports/SESSION-07-REPORT.md`, with the review sheet and the trace of each
    canonical company.

## 08 — Explicit non-goals

- Technology, component and product records (S08, D-027), facility records (S09),
  relationship records (S10) and events (S09):
  - a filing's subsidiary list is an `owns` candidate for S10, not an S07 record;
  - its supplier paragraph is a `supplies` candidate for S10;
  - an announced plan is an event.
- Coverage beyond the seed the human sets (NG-03). Completeness is not a goal.
- Company attributes the schema does not have: revenue, market share, headcount, stock
  listing. No new field without a decision the human approves first (§16 stop).
- Metrics, scores or rankings (NG-11).
- An agent runtime (NG-08), a database server or graph database (NG-07), a UI.
- An external API (NG-14), circumventing access controls (RA-2), declaring an identity to
  a site (RA-7).
- Changing an accepted schema, vocabulary value or decision without a decision the human
  approves first. This includes adding a review field to entity records, a company field,
  or an actor role.
- Promoting any real claim or record to canonical without the human's verdict (CLAUDE.md
  §9, class C).
- Editing the root documents, `domain-map.md`, `M0-audit.md`, the two taxonomies, the
  frozen register, or migrated source values (VD-9).
- Anything in `Eu-Digital-Policy` (NG-01).

## 09 — Constraints

- **Evidence:**
  - Part A's evidence rules, `source-policy.md` and `claim-model.md` apply to every
    claim.
  - Identity rests on first-hand sources: `party` or `originator` standing, a class
    preferred or acceptable for `identity:company`.
  - A company's own marketing is acceptable for identity only when no filing or registry
    states it, and the claim shows the class.
  - Filings: the filer's copy, with `filing_copy` recorded; a forward-looking statement
    is ER-8.
  - Company-level is not product-level (ER-9). Nothing in S07 supports a product edge.
- **One home:**
  - the ID is the identifier, and the display `name` is editorial (§7);
  - the legal name is a claim-backed attribute;
  - a jurisdiction's code lives in its ID only (§3.6);
  - roles live on the company, never as edges (D-024);
  - the class of each source lives on its record (D-041, D-050).
- **Unknown ≠ zero:** every company field is present. An attribute nobody researched is
  `not_researched`. `not_publicly_determinable` needs an ER-3 search record (D-049).
- **Separate axes:** class ≠ standing ≠ claim type ≠ evidence status. Verification dates
  are per record.
- **Tooling:** `tools/` stays standard library (D-003, D-026). Tests may use the pinned
  `requirements-test.txt`. Any new dependency needs a decision the human approves first.
  PDF text extraction happens in a scratch environment, as in S01, S05 and S06.
- **Process:** L-02, L-04, L-08 as in S06.
- **Portfolio:** show a small set of company records that a stranger can trace to the
  companies' own filings, and checks that make an untraceable record impossible.

## 10 — Agent responsibilities

The contracts are `docs/agents/contracts.md` (D-052, accepted at the S06 review). This
session uses them as written. If a path must change, the Editorial row records it and the
report says so.

| Agent | May write | Notes |
|---|---|---|
| Source Scout | the report (candidate URLs, access gaps, the RA-4 list) | discovery only; no snippet is evidence |
| Extractor | `data/sources.json` (new records; `publisher_entity`), `data/staging/claims.json`, the staging entity files (per H-2) | provenance on every candidate; explicit states for gaps |
| Verifier | the verification fields of staging claims; the report | reads each sentence at its locator; re-checks the session's own locators |
| Knowledge Architect | `docs/architecture/company-dataset.md`, `docs/architecture/decisions.md` (append) | ID rule, legal-entity rulings, one-home checks; no schema change without the human |
| Data Auditor | `tests/`, `tests/fixtures/`, `tools/` | V-1, V-9, V-10, freshness, the canonical-entity rule; the M1 audit's measurements |
| Editorial | `docs/README.md`, the baseline state rows, `README.md`, `docs/agents/contracts.md` (paths only), `docs/quality/audit-history.md` | records the new state only |

**Moving accepted records** to the canonical files happens in the session, on the human's
recorded verdicts, and is reported (`docs/agents/contracts.md`, preamble). The M1 audit,
if in S07, is written by the Portfolio Reviewer role, played by Claude under PEF §12,
without a contract (inactive in `roles.md`). This is recorded as a deviation from
`roles.md`, or the human assigns it otherwise (H-5).

No agent writes outside these paths and `sessions/reports/`.

## 11 — Data and evidence rules

- **Canonical entities:** companies, and the jurisdictions they need (H-4). Canonical
  only on the human's verdict (H-3).
- **Allowed relationship types:** none instantiated (S10).
- **Required source tier:** the `source-policy.md` §7 rows:
  - `identity:company` and `attr:company.*`, which prefer `company_filing` and
    `government_publication`;
  - `identity:jurisdiction`, which prefers `standard_specification`.
- **Provenance:** every value cites claims in the S06 shape: source, locator, verbatim
  anchor, standing, and the bytes read.
- **Temporal:**
  - every attribute claim has `as_of`, or `not_stated`;
  - `valid_from`/`valid_to` only where the source gives a period;
  - the 12-month rule applies to `time_sensitive` rows.
- **Confidence:** no numeric values.
- **Unknown or unverified:**
  - `not_researched` for any field no source was read for;
  - an access gap is recorded and supports nothing (SP-7);
  - an unverified claim supports no canonical record.

## 12 — Implementation rules

**Files S07 may create:**

- `docs/architecture/company-dataset.md`;
- `docs/architecture/milestone-audits/M1-audit.md` (if H-5 places it here);
- the entity data files H-2 chooses, in `data/` and `data/staging/`;
- `data/claims.json`, only when the first claim is accepted;
- tests and fixtures for the new checks;
- `sessions/reports/SESSION-07-REPORT.md`.

**Files S07 may modify:**

- `data/sources.json`: new records, and `publisher_entity` only on migrated ones;
- `data/staging/claims.json`;
- `tests/test_data_integrity.py` and `tests/test_data_schema.py`, to bring the new files
  into scope (L-05);
- `tools/trace.py`, only to read the new files by default, if H-2's layout needs it;
- `docs/architecture/decisions.md` (append);
- `docs/README.md`, baseline state rows, `README.md`, `docs/quality/audit-history.md`;
- `docs/agents/contracts.md` (paths only);
- `docs/architecture/claim-model.md`: status notes only, e.g. VD-11's scope after the §06
  q8 decision.

**Approach:** mirror S03 to S06.

- The document holds the reasoning; the schemas hold shapes; the data holds records; the
  tests hold checks.
- Tables are parsed by splitting cells, with width assertions.
- The matrix is read from `source-policy.md` §7, never copied.
- Test helpers are imported from the existing test modules.

**Prohibited:**

- a hard-coded list of companies, rows or classes in a test (read them from their
  homes);
- a runtime or scheduler;
- a hand-written JSON Schema validator (D-026);
- copying `source-policy.md`, `claim-model.md` or taxonomy text.

**Schema changes to accepted files:** none. If §06 needs one (e.g. a review field on
entities), stop (§16).

## 13 — Verification plan

- **At start:**
  - `python -m unittest discover -s tests` and `python tools/validate_repo.py`;
  - record the base, `git branch -a` and `git ls-remote`;
  - confirm that `main` carries this prompt.
- **Environment:** a fresh virtualenv from `requirements-test.txt`, with the installed set
  compared to the pins (sorted).
- **Fail first:** the new checks fail before the records exist.
- **Behaviour:** every new fixture fails where it mutates, and each error message is
  read.
- **Data:**
  - `validate-data` passes on the real files;
  - each break in §07 task 12 is caught in a scratch copy;
  - the report says which tests each break fails.
- **Manual evidence check:**
  - the Verifier reads every new anchor's sentence at its locator, and re-checks every
    locator the session wrote;
  - the human inspects a sample of canonical companies (Part A).
- **Trace:** run it on each canonical company, and paste the output into the report.
- **CI:** report it separately from local results, or say it was not observed (L-08).
- **Not applicable:** browser, accessibility, performance.

## 14 — Evaluation requirements

The report records:

- decisions and rejected alternatives, in particular the legal-entity rulings, the ID
  rule and the anchor-checking rule for new sources;
- deviations from Part A or Part B, including the milestone-label reading in §01 if the
  human reads it differently;
- assumptions invalidated: a company the evidence would not identify, a filing that was
  not the filer's copy, a registered source whose publisher is not the company it seemed;
- new debt;
- unresolved questions (parent and subsidiary, brands);
- the human's findings on the sample they inspected, verbatim.

## 15 — Acceptance criteria

1. Every canonical company record validates against the accepted entity schema,
   unchanged, and has at least one canonical identity claim that V-10 accepts for
   `identity:company`.
2. Every company ID follows the rule in `company-dataset.md`, and a test fails when a
   record breaks it (if the rule is machine-checkable).
3. Every company field is claim-backed or an explicit state. No role is inferred; no
   headquarters is read off a facility or a listing.
4. Every jurisdiction a company points to exists, with its own identity evidence, or the
   attribute stays `not_researched` as H-4 allows.
5. Every new source is a record with class, retrieval, hash and stated dates. Every
   filing records `filing_copy`. Access gaps are listed.
6. V-1, V-9, V-10, the freshness rule and the canonical-entity rule run in CI (L-02).
7. Nothing real is canonical without the human's recorded verdict. The S06 seed claims
   move only on theirs.
8. The trace prints each canonical company's evidence, down to the source, class,
   locator, anchor, standing and dates.
9. The M1 milestone audit exists or is placed, as H-5 decides.
10. No change to accepted schemas or vocabulary values; no scores; no runtime; no
    relationship, product, facility or event record.
11. Tests and Gate 0 pass in a fresh virtualenv; the CI result is observed or reported as
    not observed.
12. The report satisfies SPEC §5 and Part A's list; new decisions are appended as
    `proposed`.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- a company record would need a field, role value or review field the accepted schema
  does not have;
- a seed company cannot be identified from a first-hand source of an allowed class, or
  the source names a different legal entity than expected. It is dropped or recorded as
  open, never patched;
- a filing is available only through a refusal-protected host, or only as an aggregator
  copy (RA-2, D-042);
- an anchor is not verbatim at its locator, or a source cannot be re-read (SP-7);
- ISO 3166-1, or any preferred source for jurisdiction identity, cannot be retrieved
  without circumvention, and H-4 gave no fallback;
- promoting any real claim or record would happen without the human's verdict;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions already taken** (2026-09-30, before S07 started; Claude's
recommendation first in each list). Do not ask them again. Record each of H-1 to H-6 in a
decision (`proposed`, citing the human's answer), and stop only if a condition cannot be
met.

- **H-0 — the S06 review** (not an S07 design question, but S07's claims take the S06
  shape):
  - *(recommended)* accept D-044 to D-053, and record D-015's second part as superseded
    by D-048;
  - accept with amendments;
  - leave them `proposed` (S07 then builds on proposed decisions, as a recorded risk).
  - *Answer:* the recommended option ("Approve all (Recommended)"). Applied before S07:
    D-044 to D-053 are accepted, D-015's status line records D-048, and the S06 report has
    a review addendum (commit `5b22515`).
- **H-1 — the seed:**
  - *(recommended)* eight companies, at least one per chain layer: NVIDIA, SK hynix,
    Micron, Amkor, TSMC, ASML, Synopsys, Amazon (AWS);
  - a minimal five: NVIDIA, TSMC, SK hynix, Amkor, ASML;
  - a broader twelve: the eight plus Google, Lam Research, Samsung, Intel. Two of these
    were refused in S01.
  - *Answer:* the recommended option ("8, one per layer (Recommended)").
- **H-2 — the entity data layout** (D-005):
  - *(recommended)* one JSON array file per entity type, as S06's H-2 did per record
    kind: `data/companies.json` and `data/jurisdictions.json`, with the staging copies
    under `data/staging/`;
  - one `data/entities.json` for every entity type.
  - *Answer:* the recommended option ("One file per entity type (Recommended)").
- **H-3 — when records become canonical:**
  - *(recommended)* build in staging. Near the end of S07, the human reviews the identity
    claims on a review sheet. Accepted claims, and the records resting only on accepted
    claims, move to the canonical files before the final commit. The rest stay in
    staging. This lets Part A's human focus inspect canonical records;
  - everything stays in staging, and promotion waits for the post-session review. The
    S07 gate is then met only after that review.
  - *Answer:* the recommended option ("Your review inside S07 (Recommended)").
- **H-4 — jurisdictions:**
  - *(recommended)* create only the jurisdiction records the seed's attributes need,
    citing ISO 3166-1 as registered from ISO's own publication. If that cannot be
    retrieved under RA-1/RA-2, stop and ask;
  - no jurisdiction records in S07: `incorporated_in` and `headquartered_in` stay
    `not_researched` until a later session.
  - *Answer:* the recommended option ("Create the needed ones (Recommended)").
- **H-5 — the M1 milestone audit** (PEF §4):
  - *(recommended)* S07 writes it first, as a document over S03–S06 (PEF §4's eight
    questions), before any data work;
  - defer it to S12 (the data architecture audit), recording the gap against PEF §4.
  - *Answer:* the recommended option ("First task of S07 (Recommended)").
- **H-6 — anchors from new retrievals** (VD-11):
  - *(recommended)* Verifier-attested. The citation's `read` hash is required, the
    Verifier re-reads every sentence, and the human spot-checks a sample, recorded in the
    report. VD-11's machine check stays for S01/S05 anchors;
  - the human checks every new anchor by hand, not a sample.
  - *Answer:* the recommended option ("Verifier + your sample (Recommended)").

## 17 — Deliverables

- `docs/architecture/company-dataset.md`, with the review sheet;
- `docs/architecture/milestone-audits/M1-audit.md` and its `audit-history.md` row (per
  H-5);
- new source records; company and jurisdiction records (staging and canonical, per H-2
  and H-3); identity and attribute claims;
- the checks: V-1, V-9, V-10, freshness, the canonical-entity rule; tests and fixtures;
- `docs/architecture/decisions.md`: D-054 onward, `proposed`;
- `docs/README.md`, baseline state rows, `README.md`, and `contracts.md` paths if changed;
- `sessions/reports/SESSION-07-REPORT.md`.

## 18 — Handoff

S07's report must hand S08 the following:

- **Completed work:**
  - the company and jurisdiction records, and which are canonical;
  - the new sources and their access gaps;
  - the checks;
  - the M1 audit (or its placement).
- **For S08** (technology, component and product dataset; gate: "Definitions are sourced
  and do not collapse technically distinct concepts"):
  - product records' `vendor` values point to the canonical companies (V-1);
  - the rows `identity:technology`, `identity:component` and `attr:*.definition` prefer
    standards, government and research sources. S08 retrieves them, and CON-01 to CON-05
    stay preserved;
  - the S06 seed claims that S08 can cite (the working definition, NIST, the GH100 FACT)
    and their review state;
  - which V-rules S08 must extend to technologies, components and products.
- **Open issues:**
  - the human approvals of the S07 decisions, and any seed-claim verdicts still missing;
  - parent/subsidiary questions left open for S10's `owns`;
  - S01's weekly gate;
  - S05 and S06 debt still open.
- **Recommended next decision:** the human confirms the canonical companies and the ID
  rule before S08, because product `vendor` references depend on them.
- **Files for S08 to read first:**
  1. the S07 report;
  2. `docs/architecture/company-dataset.md`;
  3. `docs/architecture/claim-model.md`;
  4. `schemas/entities.schema.json` (`technology`, `component`, `product`);
  5. `docs/architecture/entity-taxonomy.md` §3.3–§3.5, §5;
  6. `docs/research/source-policy.md` §7, §10;
  7. D-022, D-027 and the S07 decisions.
