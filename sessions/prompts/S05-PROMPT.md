# AI-Infrastructure-Atlas — S05 Session Prompt

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

Source hierarchy and evidence policy

Build the industrial-technology source hierarchy.

Human focus:
- distinguish primary sources from company marketing and secondary reporting;
- examine how conflicts between sources will be handled.

**Weekly gate:** the ontology and evidence policy are understandable before large-scale data collection begins.

---

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
> - Everything above this line is **Part A**, the human-authored S05 prompt, reproduced
>   verbatim (byte-identical to the upload).
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2. It was written at the end of S04, after the human's S04
>   review. It carries S04's findings forward: `SESSION-04-REPORT.md` with its review
>   addendum; `relationship-taxonomy.md` §5, §9 and §12; D-028 to D-033.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The
>   higher-level documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The human may edit Part B before S05 starts. It becomes immutable once S05 begins
>   (D-011).

## 01 — Session identity

- **Session:** S05
- **Title:** Source hierarchy and evidence policy
- **Type:** RESEARCH / ARCHITECTURE (`SESSION-ROADMAP.md`). The dominant purpose is
  architecture: a policy and its checks. Research is limited to qualifying the sources
  already registered (§05).
- **Milestone:** M1 — Domain + Evidence Foundation (`SESSION-ROADMAP.md` numbering, D-019)
- **Predecessor:** S04 — Relationship taxonomy (merged to `main` at `60bb1ce`, PR #4;
  D-028 to D-033 accepted)
- **Expected successor:** S06 — Evidence/claim system
- **Complexity class:** medium (policy design, one reasoning document, consistency tests;
  possibly one small schema, depending on the §06 q10 answer)
- **Weekly gate:** week 2 closes with this session. Part A: "the ontology and evidence
  policy are understandable before large-scale data collection begins". The **human**
  declares it passed. S05 supplies what they need to judge it (§07 task 9).

## 02 — Mission

Write the Atlas source policy.

- **Source classes.** Define the classes of source the Atlas uses, and for each:
  - what it is **primary for**;
  - what it is **never enough for on its own**;
  - how it differs from company marketing and from secondary reporting.
- **Preferred class per claim type.** Assign a preferred source class to every material
  claim type the Atlas records:
  - each relationship type (S04);
  - entity identity;
  - each entity attribute (S03).
- **Conflicts.** State how conflicts between sources are recorded, and when, if ever,
  they are resolved.

The result must make three things impossible:
- treating a company's marketing claim as a fact about the world;
- treating a secondary report as if it were the primary record it cites;
- settling a conflict between sources by rank alone.

## 03 — Why this session exists

- **The roadmap.** `SESSION-ROADMAP.md` S05's mission is "Create a source hierarchy
  tailored to industrial technology research". Its gate is "Every material claim type
  has a preferred source class."
- **S04 handed S05 a table.** `relationship-taxonomy.md` §5 is the one home of evidence
  expectations. It has one row per relationship type: what a source must show, what is
  not enough, and what is typically non-public. Below it is the entity identity
  expectation (`identity_claim_ids`, D-025). S04 deliberately stated *what* the evidence
  must show and left *which class of source* to S05.
- **Preference depends on the claim type** (S04 finding, `INTERPRETATION`). The best
  source for "TSMC `fabricates` product P" is a party to that edge. The best source for
  "HBM `requires` TSV" is technical or standards literature. A single global ranking,
  such as MA §10's list or S01's provisional T1–T6, cannot express that. MA §10 itself
  says: "The source hierarchy is guidance, not a substitute for checking whether the
  source actually supports the claim."
- **S04 produced three evidence rules with no policy home yet** (taxonomy §12):
  - a process name that embeds a foundry's name supports "that foundry fabricates" only
    as `DERIVATION`;
  - a product's vendor is not established as its designer by the vendor field;
  - one page's silence supports `not_researched`, not `not_publicly_determinable`.

  S05 must turn these into policy.
- **Two provisional S01 decisions wait on S05:**
  - D-014: raw retrieval only; blocked sites are recorded, not worked around. S01 asked
    "whether manual retrieval by the human is acceptable";
  - D-015: provisional tiers T1–T6 and the S01 meaning of `verified`, "superseded by
    S05's source policy when written".
- **The human's learning** (Part A human focus):
  - why a company's datasheet, press release and marketing page are different kinds of
    evidence, even from the same company;
  - why a respected secondary report is still not the record it cites;
  - how disagreement is kept visible instead of averaged away.

## 04 — Current state

As of `main` @ `60bb1ce`, plus the commit that adds this prompt. Verify at start, and
record the base and the `git branch -a` result in the report (D-018 L-03).

- **This prompt must be on `main` before S05 starts.**
  - S04's prompt was committed on a branch after its PR merged, so it never reached
    `main` (S04 Deviation 1).
  - If S05 finds this file only on a branch, it records that as a deviation and brings
    in the original commit, as S04 did.
- **Accepted model:**
  - entity types and fields: D-022 to D-025;
  - relationship record and vocabulary, eleven types at two levels: D-028 to D-033;
  - D-026 (the pinned `jsonschema`, for tests only);
  - D-027 (S08 creates the first product records).
- **Files S05 builds on:**
  - `docs/architecture/relationship-taxonomy.md`: §5 is the evidence-expectation
    table; §9 covers unknown and non-public edges; §12 has the worked examples;
  - `docs/architecture/entity-taxonomy.md` §7: the attribute contract and
    `identity_claim_ids`;
  - `schemas/entities.schema.json` and `schemas/relationships.schema.json`: the
    authoritative lists of attribute fields and relationship types, which S05's matrix
    must cover;
  - `docs/research/source-register.md`: SRC-001 to SRC-023, with provisional tiers
    T1–T6. It includes:
    - notes on CSET (T4, pending S05's review), SIA/BCG (an advocacy association) and
      undated live pages;
    - the list of hosts that were not retrievable (JEDEC, TSMC, Samsung, SEC EDGAR,
      IEA, Intel, ISO and others);
  - `docs/research/domain-map.md` §5: the source conflicts CON-01 to CON-05, preserved,
    not resolved;
  - tests: `tests/test_entity_*.py`, `tests/test_relationship_*.py`, with fixtures. CI
    runs 58 tests plus Gate 0, as measured at `842a735`.
- **Conflict between two tier orders** (a one-home issue S05 must settle):

  | Source | Order |
  |---|---|
  | S01 provisional (`source-register.md`, D-015) | `T1` company documentation and filings · `T2` standards bodies · `T3` government and intergovernmental · `T4` academic and technical research · `T5` secondary analysis · `T6` news |
  | MA §10 | 1 primary legal and institutional · 2 official government and company filings · 3 intergovernmental and standards bodies · 4 peer-reviewed research · 5 secondary analysis · 6 news and media · 7 tertiary summaries |

  They rank government sources and standards bodies differently, and MA separates
  filings from other company documentation. Do not edit MA. Reconcile in the policy and
  record the reconciliation (§16).
- **Open items S05 inherits:**
  - D-014 and D-015 (above);
  - whether a source's publisher becomes a reference to a company or institution record
    (`entity-taxonomy.md` §3.7, "S05/S06");
  - what a `not_publicly_determinable` claim must record about the search
    (`relationship-taxonomy.md` §9, handed to S06). S05 owns the part that is policy:
    which source classes must have been checked;
  - whether "external API dependency" becomes a non-goal (baseline §6). It is not S05's
    to decide, but the retrieval policy touches it.
- **Not S05's:**
  - the claim schema, including claim type and evidence status (S06);
  - migrating the register into canonical source records (S06, after which the
    register is frozen);
  - agent contracts (S06, D-010).
- **Planned artifact:** `docs/research/source-policy.md` (`docs/README.md`; PEF §11).
- **Next decision number:** D-034.

## 05 — Inputs and evidence

Documents, in this order:

1. `sessions/reports/SESSION-04-REPORT.md`, including the review addendum.
2. `docs/architecture/relationship-taxonomy.md` §5 (evidence expectations), §9
   (unknowns), §11 (role and edge warnings), §12 (worked examples), §15 (handoffs).
3. `docs/research/source-register.md`: every row, the notes, "Retrieved but not
   cited", and "Not retrievable".
4. `docs/research/domain-map.md`:
   - "How to read this map" (claim classes, status markers);
   - §5 (CON-01 to CON-05);
   - §8 (gaps, dated evidence).
5. `docs/architecture/entity-taxonomy.md` §3.7 (publishers, institutions) and §7
   (attribute contract).
6. `MASTER-ARCHITECTURE.md` §5.2–5.3 (claim and source records), §5.7, §10 (claim
   types, evidence status, evidence hierarchy) and §16 (the pipeline stages "source
   discovery → raw evidence").
7. `PROJECT-EVALUATION-FRAMEWORK.md` §6 (content audit: source qualification,
   contradiction handling, stale-source replacement) and §11.
8. `docs/architecture/decisions.md`: D-014, D-015, D-022, D-025, D-028 and D-031.
9. `SESSION-ROADMAP.md` S05, S06, S07, S09 and S10; the operational roadmap's week-2
   entry.

Repository paths to inspect: `docs/research/`, `docs/architecture/`, `schemas/`,
`tests/`, `.github/`.

**External research: bounded.**

- The policy is a design choice (`INTERPRETATION`), and it is tested against the 23
  registered sources, not against new ones.
- Retrieve a new source only to settle what a source class *is* when no registered row
  shows it. Example: what a 20-F annual report contains, if the policy's filing class
  needs a real example.
- Follow D-014 until S05 replaces it: retrieve raw; never circumvent access controls;
  record a blocked site as a gap. A newly retrieved source is cited in the report and the
  policy, with URL, access time and a content hash. Whether it also enters
  `source-register.md` is a §06 decision (q11).

**Audit findings to carry:**

- A-5: second homes. The policy must not restate S04's §5 text; it references rows by
  relationship type.
- A-1: machinery before a used loop. There must be no numeric credibility scores and no
  source-scoring code.
- L-09: read before you automate. Every class is exercised on registered sources before
  any check is written.
- **S04's process lessons:**
  - Check what was *read*, not only what was expected. Parsers assert the table width
    and the row count, because S04's DEP parser once skipped a whole column silently.
  - Cross-check against the source document instead of a hard-coded list. S04's "In"
    column caught the parser bug.
  - Numbers written in prose are tested or labelled "as measured at `<commit>`" (L-04).
    S04 nearly committed wrong counts in a decision record.
  - Worked-example anchors are machine-checked against the domain map.
  - Fail first, then deliberate breakage in scratch copies.

## 06 — Required reasoning

Answer these before writing the policy's tables. The answers go into `source-policy.md`
and the decision records.

1. **Source classes.** Which classes does the Atlas need? Build them from the 23
   registered sources and the blocked hosts, not from a generic list. Candidates:
   - company filings (regulatory, audited or legally accountable);
   - company technical documentation (datasheets, architecture papers, developer docs);
   - company press releases;
   - company explanatory or marketing pages;
   - standards and specifications;
   - government and intergovernmental reports;
   - national-laboratory and academic research;
   - policy research centres (CSET);
   - industry associations (SIA);
   - consultancies (BCG);
   - news.

   For each class, give:
   - its definition;
   - a test that tells two neighbouring classes apart;
   - what it is primary for;
   - what it is never enough for on its own.
2. **Primary, marketing and secondary** (Part A human focus).
   - When is a company source primary? D-015 says: for its own products and processes.
     Refine that:
     - is a source primary for a relationship when its publisher is **a party to the
       edge** (the source or target company)?
     - what about statements a company makes about *another* firm (NVIDIA naming TSMC's
       process, SRC-006)?
   - Where does marketing start? D-015 already makes superlatives `ATTRIBUTION`
     ("unique to", "world's first", "leader"). Is a *class* of page marketing, or only
     certain statements within a page?
   - What makes a report secondary? Carry the SRC-021 example: LBNL reporting IDC
     analysts (DEP-11) is second-hand. How is an attribution chain recorded?
3. **Preference per claim type** (the roadmap gate). Build a matrix that covers every
   "material claim type":
   - each type in `relationships.schema.json`;
   - entity identity (`identity_claim_ids`);
   - each attribute field in `entities.schema.json`;
   - class definitions (the `definition` field of technology and component).

   Give each row a preferred class, acceptable alternatives, and classes that are never
   sufficient alone. Reference S04's §5 rows by relationship type; **do not copy their
   text** (one home). Also decide:
   - Do events (announcements and plans, owned by S09) need rows now, or when S09
     defines event types?
   - Is "material claim type" defined by the schemas (machine-checkable), or by a list
     S05 writes?
4. **Reconciling the tier orders.** MA §10 and S01's T1–T6 disagree (§04).
   - Does the Atlas keep any global ranking at all, or only per-row preferences?
   - If a ranking survives, which order, and why? Record the conflict with MA §10; do
     not edit MA.
   - What replaces the register's provisional `source_tier` column? Decide the one home
     of each registered source's class:
     - the register (an S01 staging artifact, frozen after S06);
     - the policy's mapping table;
     - or a future source record (S06).
5. **Tier is not verification.**
   - How does the policy stop a preferred class from standing in for checking that the
     source supports the claim (MA §10, last line)?
   - How does it relate to the claim's evidence status, which is S06's and separate from
     claim type (L-06)? S05 must not define the evidence-status vocabulary.
6. **The three S04 evidence rules.** Turn each into policy:
   - the process name as fabricator (`DERIVATION`);
   - the vendor as designer (not established);
   - silence and `not_publicly_determinable`: which preferred classes must have been
     searched before `not_publicly_determinable` may be claimed for a row, and what the
     claim must say about the search. S06 gets the fields; S05 gets the rule.
7. **Conflicts** (Part A human focus). Classify the kinds of conflict. Candidates:
   - definitional (CON-01, CON-03, CON-04, CON-05);
   - loose wording (CON-02: Google's "on-chip");
   - factual contradiction;
   - temporal supersession (a 2019 figure vs a later one);
   - scope difference;
   - self-interest (an advocacy association vs an independent body).

   For each kind, how is it recorded? Consider:
   - several assertions, each with its own claims (D-025);
   - a `disputed` evidence status on claims (S06);
   - a working definition marked `INTERPRETATION`.

   Also decide:
   - When, if ever, is a conflict resolved, and who decides (CLAUDE.md §9 class C/D:
     "publication of unresolved material disputes" is human-only)?
   - Apply the handling to CON-01 to CON-05, as illustrations, without editing the
     domain map.
8. **Blocked and non-retrievable sources (D-014).**
   - Is manual retrieval by the human acceptable? This is a human decision; see §16.
   - If it is, how is such a source recorded: retrieval method, who retrieved it, hash,
     and the access date as the human's?
   - How is a login-walled or paid standard (ISO, The Green Grid) treated?
   - Does "external API dependency" matter here? Record the question only.
9. **Freshness and dated evidence.**
   - How do the publication date, the access date and the content hash of undated live
     pages (register note 3) work together?
   - When does evidence count as stale for a given class? Examples: CSET's 2019 market
     data; SK hynix's 2024 plan.
   - The policy states the rule. `validate-freshness` implements it later (S06+). S05
     writes no freshness code.
10. **How much becomes machine-readable.** Options:
    - (a) the policy document only, with its tables machine-checked by a stdlib test;
    - (b) a `source_class` controlled vocabulary in a new `schemas/sources.schema.json`,
      which S06 extends into the full source record;
    - (c) the full source-record schema now.

    D-022 assigns sources to "S05/S06". The S03/S04 pattern keeps vocabulary values in a
    schema with one definition each. Against that, A-1 warns about machinery before a
    used loop. This is the one design choice to put to the human before any file is
    written (§16). Recommendation to test: (b) if the classes are stable after the §06
    reasoning, otherwise (a).
11. **The register's future.** S06 migrates `source-register.md` rows into canonical
    source records, and the register is then frozen.
    - Does S05 annotate the register's tier column, or leave it as S01 history and map it
      in the policy?
    - Where do sources retrieved in S05 (if any) live until S06?
12. **Publishers** (`entity-taxonomy.md` §3.7).
    - Does the policy need the publisher to be an entity reference (company or
      institution) to apply the party-to-the-edge rule (q2)?
    - If so, S05 states the requirement, and S06 builds it with the source record.
      Reserved `institution` stays reserved unless a decision the human approves says
      otherwise.

## 07 — Tasks

**Research**

1. Classify each of SRC-001 to SRC-023, and each blocked host, into the §06 q1 classes.
   Read each row's `source_type`, the register notes and the domain-map uses. Record the
   CSET decision (T4 or T5 in S01 terms; register note 1).

**Design**

2. Write the class definitions (§06 q1–q2), with a neighbour test for each pair that is
   easily confused. At minimum:
   - filing vs press release;
   - technical documentation vs marketing page;
   - national laboratory vs policy research centre;
   - industry association vs consultancy.
3. Write the preference matrix (§06 q3), keyed by relationship type and entity field, as
   they appear in the schemas.
4. Write the conflict policy (§06 q7), and apply it to CON-01 to CON-05.
5. Write the retrieval, access and freshness rules (§06 q8–q9). Any rule that needs the
   human's decision waits for it.
6. Work through at least four registered sources as examples. Each is an illustration,
   not a record, and its quoted anchors must be verbatim in the domain map:
   - SRC-006 (NVIDIA technical blog): primary for NVIDIA's product; what it supports
     about TSMC;
   - SRC-017 (ASML product page): "unique to ASML" as `ATTRIBUTION`;
   - SRC-014 (SK hynix press release): a plan, which is an event and an `ATTRIBUTION`;
     primary for SK hynix's own intention only;
   - SRC-021 (LBNL reporting IDC analysts, DEP-11): a second-hand attribution chain;
   - optionally, SRC-005 (SIA/BCG): an advocacy association plus a consultancy.

**Implementation**

7. `docs/research/source-policy.md`: the one home of:
   - the classes;
   - the preference matrix;
   - the conflict and retrieval rules;
   - the dispositions of D-014, D-015 and the tier orders.
8. Tests: `tests/test_source_policy.py` (standard library). It checks that:
   - every relationship type in `relationships.schema.json`, entity identity, and every
     attribute field in `entities.schema.json` has exactly one row in the matrix, with
     classes that exist;
   - every class is defined once, and every class the matrix cites is defined;
   - every SRC ID in the register has exactly one class, parsed from the register itself
     with width and row-count assertions;
   - every CON ID in domain map §5 has a handling row;
   - every decision, non-goal, concept, DEP, SRC and CON cited exists;
   - every quoted anchor in the worked examples appears verbatim in the domain map;
   - every count written in prose matches what the tables contain (L-04).

   If the human chooses §06 q10 (b), also write `schemas/sources.schema.json`,
   `tests/test_source_schema.py` and fixtures, following the S03/S04 pattern.

**Validation**

9. Run the new tests before the decisions exist, and confirm they fail. Then break the
   policy, the schemas and a source document deliberately in scratch copies, in at
   least five different ways, and confirm each break is caught. Include one break of
   `relationships.schema.json`, adding a relationship type: the matrix test must then
   fail for lack of a row.

**Documentation**

10. **Human learning artifact for the weekly gate.** Write a short section in
    `source-policy.md`: "How the Atlas decides what to believe". It walks one S01
    sentence from source through class, claim and edge to what may be displayed, using
    S03 (entity), S04 (relationship) and S05 (source). The human reads it to judge the
    weekly gate. S05 does not declare the gate passed.
11. Append decisions from D-034, each `proposed`. Include how D-014 and D-015 are
    superseded or decided; their status lines change only at the human's review.
12. Add or update rows in `docs/README.md` (source policy: planned → proposed).
13. Update the baseline's state rows (§1 table, §4, §5), but only those that have become
    false.
14. Write `sessions/reports/SESSION-05-REPORT.md`.

## 08 — Explicit non-goals

- The claim schema, claim types and the evidence-status vocabulary (S06; L-06).
- Migrating `source-register.md` into canonical source records (S06).
- Agent contracts or roles (S06, D-010).
- Any entity, relationship, claim, source or event **record** (S07 to S10).
- Numeric credibility, reliability or confidence scores for sources (D-028 rejects
  confidence scores; NG-11).
- A source-scoring, crawling or retrieval tool, or `validate-freshness` code (S06+;
  L-01, NG-08).
- Circumventing access controls or bot filtering, including headless-browser retrieval
  of blocked sites (D-014).
- Changing an accepted S03 or S04 decision, field or vocabulary without a decision record
  the human approved **first**. The matrix attaches to the schemas; it does not change
  them.
- Instantiating `institution` or `policy` (reserved, D-022), or any policy-layer sourcing
  rules for S17's instruments.
- Editing the root documents, `M0-audit.md`, `domain-map.md` or `source-register.md`,
  unless §06 q11 is decided by a human-approved decision.
- Anything in `Eu-Digital-Policy` (NG-01). Its source policy may be read as a
  methodological reference (CLAUDE.md §3); nothing is copied (MA §4.2, D-006).

## 09 — Constraints

- **Evidence:**
  - Part A's evidence rules apply. Model memory is not evidence about a source class.
  - Every class definition that asserts what a real source type contains (e.g. what a
    20-F includes) cites a registered or newly retrieved source, or is labelled
    `INTERPRETATION`.
- **Claim labels:** `FACT | ATTRIBUTION | DERIVATION | INTERPRETATION | IMPLICATION`.
  Part A lists four; CLAUDE.md §6 adds `ATTRIBUTION` and takes precedence.
- **One home:**
  - Source classes are defined in one place (the policy, or the schema if §06 q10 is
    (b)).
  - The matrix references S04's §5 by relationship type and S03's fields by name; it
    never copies their text.
  - Each registered source's class has one home (§06 q4, q11).
- **Separate axes:**
  - source class ≠ claim type ≠ evidence status;
  - a preferred class is never a verification result (MA §10).
- **Unknown ≠ zero:**
  - a missing source class for a row is a test failure, never a default;
  - "no preferred class exists" is stated explicitly, with a reason.
- **Tooling:**
  - `tools/` stays standard-library only.
  - Tests may use the pinned `requirements-test.txt` (D-026).
  - Adding any dependency needs a decision and the human's approval first.
- **Process:**
  - L-02: nothing is called a gate unless CI runs it.
  - L-04: no hand-typed counts; prose counts are tested.
  - L-08: "ran locally" is kept apart from "CI result".
- **Portfolio:** demonstrate evidence methodology and source criticism, with the rules
  checked against real registered sources, not a generic hierarchy copied from
  elsewhere.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Source Scout | the S05 report (any new source it retrieves) | discovers only; a search result is not evidence (CLAUDE.md §8) |
| Knowledge Architect | `docs/research/source-policy.md`, `docs/architecture/decisions.md` (append); `schemas/sources.schema.json` only if §06 q10 is (b) | classes, matrix, one-home rulings |
| Verifier | the S05 report | checks every quoted anchor and every source classification against the register; may downgrade, may not invent evidence |
| Data Auditor | `tests/`, `tests/fixtures/` | consistency tests; schema tests if a schema is written |
| Editorial | `docs/README.md`, `baseline.md` state rows, `README.md` | only to correct statements that have become false |

All other agents are inactive. No agent writes outside `docs/research/source-policy.md`,
`docs/architecture/decisions.md`, `schemas/` (only under q10 (b)), `tests/`,
`docs/README.md`, `baseline.md`, `README.md` and `sessions/reports/`.

## 11 — Data and evidence rules

- **Canonical entities:** none created.
- **Allowed relationship types:** the eleven accepted in D-029, unchanged. S05 attaches
  source preferences to them; it adds, renames or removes none.
- **Required source tier:** this session defines it. Until the S05 decisions are
  accepted, D-015's provisional order applies to any source S05 retrieves.
- **Provenance:** every example and every class characterisation cites a register ID,
  with a locator, or a newly retrieved source, with URL, access time and hash.
- **Temporal:**
  - publication date, access date and content hash are distinct (§06 q9);
  - dated evidence stays dated (CSET 2019; SK hynix 2024).
- **Confidence:** there are no numeric confidence or credibility values anywhere.
  Confidence is expressed through class, claim type and, later, evidence status.
- **Unknown or unverified:**
  - a source that could not be retrieved is a gap, never a snippet (D-014);
  - `not_publicly_determinable` requires the preferred classes for that row to have been
    searched (§06 q6).

## 12 — Implementation rules

- **Files S05 may create:**
  - `docs/research/source-policy.md`;
  - `tests/test_source_policy.py`;
  - `sessions/reports/SESSION-05-REPORT.md`;
  - only under §06 q10 (b): `schemas/sources.schema.json`,
    `tests/test_source_schema.py` and `tests/fixtures/sources.json`.
- **Files S05 may modify:**
  - `docs/architecture/decisions.md` (append only);
  - `docs/README.md`;
  - the `baseline.md` state rows;
  - `README.md`.
- **Approach:** mirror S03 and S04.
  - The document holds the reasoning, and the tests hold the checks.
  - Tables are parsed by splitting cells, with width and row-count assertions.
  - Test helpers are imported from `tests/test_entity_taxonomy.py` rather than copied.
    The human kept this pattern at the S04 review.
- **Cross-file consistency:** the matrix's row keys are read from the two schemas at test
  time, so adding a relationship type or an entity field in a later session fails the
  test until the policy gains a row.
- **Prohibited:**
  - a numeric scoring model;
  - a hard-coded list of relationship types or fields in the test (read them from the
    schemas);
  - copying S04's §5 text.
- **Schema changes to accepted files** (`entities.schema.json`,
  `relationships.schema.json`): none. If §06 reasoning requires one, stop (§16).

## 13 — Verification plan

- **At start:**
  - `python -m unittest discover -s tests` and `python tools/validate_repo.py`;
  - record the base commit, the `git branch -a` result and `git ls-remote` (to catch
    unmerged branches, as S04 had to).
- **Fail first:** the consistency tests fail until the decisions and the tables exist.
- **Behaviour:** if a schema is written (§06 q10 (b)), every invalid fixture is a single
  mutation, and each fails at the path it targets. Read each error message.
- **Deliberate breakage:** at least five distinct breaks in scratch copies, each caught.
  Include:
  - a relationship type added to the schema without a matrix row;
  - a register row added without a class;
  - an anchor altered by one word.
- **Environment:** a fresh virtualenv from `requirements-test.txt`, with the installed
  set compared to the pins (compare sorted: `pip freeze` order differs).
- **CI:** report its result separately from local results, or say it was not observed
  (L-08).
- **Not applicable:** data validation (no records), browser, accessibility,
  performance.

## 14 — Evaluation requirements

The report records:

- decisions and rejected alternatives, including the rejected global ranking if §06 q4
  drops it;
- deviations from Part A or Part B;
- assumptions invalidated. In particular, record whether the S01 classifications (T1 to
  T6) survive, and which registered sources change class;
- new debt;
- unresolved questions.

It also records whether the weekly-gate artifact (§07 task 10) was written, and states
that the gate itself is the human's call.

## 15 — Acceptance criteria

1. Every source class has:
   - a definition;
   - a neighbour test;
   - what it is primary for;
   - what it is never enough for alone.

   Classes are defined once.
2. Every relationship type in `relationships.schema.json`, entity identity, and every
   attribute field in `entities.schema.json` has exactly one row in the preference
   matrix, with at least one preferred class or an explicit "no preferred class" and its
   reason. Machine-checked against the schemas at test time.
3. The matrix references S04's §5 rows and S03's fields; it copies neither.
4. Every register source SRC-001 to SRC-023 has exactly one class, with a one-home ruling
   on where that class lives. Machine-checked against the register.
5. The conflict policy classifies conflict kinds, states how each is recorded and who
   may resolve it, and applies to every CON in domain map §5. Machine-checked. No
   conflict is resolved by rank alone.
6. The three S04 evidence rules are policy, including the search requirement for
   `not_publicly_determinable`.
7. MA §10 and D-015's T1–T6 are reconciled in a decision, with MA unedited. D-014 and
   D-015 have a disposition. Any rule that depends on the human's retrieval decision
   records that decision.
8. At least four worked examples from registered sources; every quoted anchor verbatim in
   the domain map (machine-checked).
9. No numeric scores; no change to accepted S03 or S04 schemas.
10. The tests and the Gate 0 validator pass in a fresh virtualenv. The CI result is
    observed, or reported as not observed.
11. The weekly-gate explainer exists. The report does not claim the gate is passed.
12. The report satisfies SPEC §5 and Part A's list. New decisions are appended as
    `proposed`.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- **human decisions needed before files are written** (ask both together, each with a
  recommendation):
  1. §06 q8: is manual retrieval of blocked primary sources by the human acceptable, and
     under what recording rules?
  2. §06 q10: policy only, a `source_class` vocabulary schema now, or the full source
     schema now?
- a preference would require a new entity field, a new relationship qualifier or a claim
  field. Record it for S06, S08 or S10; do not add it;
- a claim type has no publicly available preferred class. Record the pattern with
  `not_publicly_determinable` logic; do not invent a proxy source;
- MA §10 and the chosen policy cannot be reconciled without editing MA. Record the
  conflict; do not edit MA;
- classifying a source would need access that D-014 forbids;
- two canonical homes for a source's class appear (register vs policy vs schema) with no
  approved ruling;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

## 17 — Deliverables

- `docs/research/source-policy.md`, including the weekly-gate explainer
- `tests/test_source_policy.py` (plus `schemas/sources.schema.json`, its tests and
  fixtures, only under §06 q10 (b))
- `docs/architecture/decisions.md`: D-034 onward, `proposed`
- `docs/README.md` row; `baseline.md` state rows only where they have become false;
  `README.md` if its status becomes false
- `sessions/reports/SESSION-05-REPORT.md`

## 18 — Handoff

S05's report must hand S06 the following:

- **Completed work:**
  - the source classes;
  - the preference matrix;
  - the conflict, retrieval and freshness rules;
  - their tests.
- **For S06:**
  - **Source record fields** the policy needs: class; publisher (text or entity
    reference, per §06 q12); retrieval method; access date; content hash; publication
    date as stated.
  - **Claim record fields** the policy needs:
    - the attribution chain (for second-hand reports);
    - the search scope of a `not_publicly_determinable` claim;
    - the evidence status `disputed` for conflicts.
  - **Migration.** How the register's rows migrate, using the policy's class mapping.
  - **The meaning of `verified`.** D-015's S01 meaning is to be superseded or confirmed
    in the claim model.
- **Open issues:**
  - human approvals;
  - the weekly gate (the human's call);
  - whether "external API dependency" becomes a non-goal;
  - S01's weekly gate;
  - `validate-freshness` (S06+).
- **Recommended next decision:** the human reviews the S05 decisions and declares the
  week-2 gate before S06, because S06's claim model attaches evidence status to claims
  whose sources S05 classifies.
- **Files for S06 to read first:**
  1. the S05 report;
  2. `docs/research/source-policy.md`;
  3. `docs/architecture/relationship-taxonomy.md` §5 and §9;
  4. `docs/architecture/entity-taxonomy.md` §7;
  5. `docs/research/source-register.md`;
  6. D-015, D-025, D-028, D-031 and the S05 decisions.
