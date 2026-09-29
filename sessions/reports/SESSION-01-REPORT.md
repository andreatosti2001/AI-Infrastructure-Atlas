# SESSION-01 Report — Domain map: the physical AI stack

- **Session:** S01 · **Type:** RESEARCH · **Milestone:** M0 — Project Constitution (`SESSION-ROADMAP.md` numbering; U-2 still open)
- **Date:** 2026-09-29
- **Prompt:** [`sessions/prompts/S01-PROMPT.md`](../prompts/S01-PROMPT.md) (Part A human, Part B Claude; sha256 `fbddd38e…0144369`)
- **Branch:** `claude/magical-galileo-vwn13j` (from `main` @ `6413a02`)

## Mission outcome

**Achieved as a draft, pending the human's terminology review.** The Part A weekly
gate ("explain the physical AI compute stack without relying on the website") is a
human judgement. This session supports it but cannot declare it passed.

| Acceptance criterion (Part B §15) | Result |
|---|---|
| 1. The map covers all seven Part A layers | met: layers 1–7, with "EDA/equipment" as 5a/5b (D-013) |
| 2. Every concept entry has a definition, layer, claim class, a source ID with locator or a status marker, and a scope call with justification | met: 46 entries, checked by script (see Tests run) |
| 3. Every cited source ID resolves to a register row | met: 23 cited, 23 rows, none unused |
| 4. Every register row has publisher, title, url, accessed_at and a provisional tier | met: checked by script |
| 5. No register row is a search page or snippet | met: every row was retrieved in full and read |
| 6. Plain-language chain overview and a terminology section with open questions | met: map §1 and §7 (12 questions) |
| 7. No entity-to-entity supply relationship stated as FACT without a primary source | met: the only entity-level statements are company-reported facts about the company's own products (NVIDIA on TSMC processes; Google/AWS on their own chips), labelled as attributed examples. They are not S10 edges. |
| 8. Unit tests and `tools/validate_repo.py` pass | met |
| 9. This report exists and satisfies Part B §14 | met: this file |

**Restated contract (Part A steps 6–7, done before any file was written):**

- **Mission:** a sourced, concept-level map of the seven Part A layers, with uncertainty
  markers and a source register.
- **Scope:** concepts, definitions and concept-level dependencies, each with evidence.
- **Non-goals:** canonical records, schemas, vocabularies, entity datasets, supply
  edges, metrics, EU/non-EU classification, policy analysis, networking, code.
- **Acceptance:** Part B §15.
- **Plan:**
  1. inspect the repository and run the validators;
  2. test source access;
  3. retrieve sources per layer and read them;
  4. write the register, then the map;
  5. check every anchor mechanically, and self-audit ≥10 entries by re-reading;
  6. append decisions, update the docs index, write this report;
  7. run tests and the validator;
  8. commit and push.

The plan held apart from the network stop described under Deviations.

## Files changed

Added:

- `docs/research/domain-map.md` — 46 concept entries in 7 layers. Also: a chain
  overview, an 18-row dependency table (structural/contingent, evidence type,
  non-public), a kinds/blurs matrix, 5 source conflicts, location-evidence pointers,
  12 terminology questions and a gaps list.
- `docs/research/source-register.md` — 23 sources (MA §5.3 fields + locators +
  content hash), a list of retrieved-but-uncited sources, and a list of sources that
  could not be retrieved.
- `sessions/reports/SESSION-01-REPORT.md` — this report.

Modified:

- `docs/README.md` — research-outputs row changed from `planned` to `draft`.
- `docs/architecture/decisions.md` — appended D-013, D-014 and D-015 (append-only).

Not modified: `tools/`, `tests/`, CI, the root constitutional documents, `sessions/prompts/`.

## Data changed

None. There are no canonical entities, relationships, claims or events, no schema and
no data files. The map and the register are research-staging artifacts (Part B §11).

## Tests run

All commands were run on Python 3.11.15 from the repository root.

| Command / check | Result |
|---|---|
| `python -m unittest discover -s tests` (session start, before any change) | 10 passed |
| `python tools/validate_repo.py` (session start) | `Repository integrity: OK` |
| `python -m unittest discover -s tests -v` (final) | 10 passed |
| `python tools/validate_repo.py` (final, with this report present) | `Repository integrity: OK` |
| Scratch evidence audit (session scratch area, **not** repository tooling, per Part B §12) | 46 entries have Kind / Definition-with-claim-class / Evidence / Status marker / Up-Downstream / Scope in {v1, future}; all 99 quoted anchors found in the retrieved text, and on the cited PDF page where a page is given; 23 register rows with 10 columns, `https` url, `accessed_at`, tier T1–T6; 0 dangling cross-references |
| Manual self-audit (14 sampled entries, below) | 11 pass; 3 wording problems found and fixed |

Not applicable (Part B §13): schema, browser, accessibility, performance.

### Self-audit — sampled entries (Part B §07 task 6; PROJECT-EVALUATION-FRAMEWORK §6)

For each entry, the cited source was re-opened. The surrounding passage (≈350
characters either side of the anchor) was re-read, and the map's wording was
compared with it.

| # | Entry | Source | Check | Result |
|---|---|---|---|---|
| 1 | ACC-01 | SRC-021 p.16 | Does LBNL exclude FPGAs? | It never mentions FPGAs (0 occurrences). Wording tightened from "FPGAs are absent" to "does not mention FPGAs". **Fixed** |
| 2 | ACC-05 | SRC-007 | two dies, chip-to-chip interconnect, "unified single GPU" | pass |
| 3 | HBM-03 | SRC-014 | base die, own technology to HBM3E, TSMC for HBM4 | pass; kept as a 2024 *plan* (time-bound) |
| 4 | HBM-06 | SRC-013, SRC-002 p.24 | HBM "semi-packaged", sent to a "system semiconductor manufacturer" | pass. Note: the recipient's actor type (foundry, OSAT or designer) is unspecified in the source; the map keeps it generic |
| 5 | PKG-03 | SRC-005 p.21 | breadth of "advanced packaging"; chiplets a "small but growing subset" | pass |
| 6 | PKG-07 | SRC-016 | Amkor does not form TSVs; does reveal/backside (MEOL) | pass |
| 7 | SME-03 | SRC-002 p.30 | CSET "necessary for mass-production" | **Exceeded evidence.** CSET says this of advanced photolithography equipment (EUV "especially", ArF immersion "secondarily"), not of EUV alone. **Fixed** |
| 8 | DC-04 | SRC-001 p.6 | location independence; location specified only at a higher level | pass |
| 9 | EN-02 | SRC-021 p.6, p.12 | interconnection definition; utilisation "not well documented" | pass; LBNL's ~50 % estimate deliberately not restated (no metrics) |
| 10 | DEP-11 | SRC-021 p.18 | "constrained by die supply" | **Exceeded evidence.** The map said "logic-die supply"; the source says "die supply" and names no stage. Changed to "die supply" with a note. **Fixed** |
| 11 | EDA-03 | SRC-002 p.50 | preferential access to process IP; process limits design options | pass; dated to CSET's 2019 data |
| 12 | DEP-01 | SRC-012 | training bandwidth "cannot be satisfied with conventional main memories" | pass as `ATTRIBUTION` (a 2019 statement by an HBM vendor, i.e. an interested party) |
| 13 | FAB-05 | SRC-002 p.23 | node names not comparable across firms | pass as `DERIVATION` (the source compares vendor node labels; it does not state the general rule) |
| 14 | DC-06 | SRC-021 p.27, SRC-007 | cooling dominates facility infrastructure energy; NVL72 liquid-cooled | pass |

Before the sampled audit, two wording problems were found and fixed during drafting.
The overview called rack-scale systems "increasingly" used; no source supports the
trend, so the word was removed. DC-01 said LBNL names "hyperscale" data centres; the
word does not appear in the report, so it was corrected. The earlier `Amkor` search
snippet claimed HBM-on-interposer content that the retrieved page does not contain;
Amkor is cited only for what the page says.

**Source-quality observation:** SRC-002 Table 6 lists "Samsung (U.S.)". It looks like a
typographical error. No claim in the map depends on that label.

## Evidence added/retired

**Added:** 23 register sources (SRC-001–SRC-023), all retrieved in full on
2026-09-29 and read from extracted text.

| Tier (provisional) | Count | Sources |
|---|---|---|
| T1 company documentation | 15 | SRC-006 – SRC-020 |
| T3 government | 4 | SRC-001, SRC-004 (NIST); SRC-021, SRC-022 (LBNL) |
| T4 research | 3 | SRC-002, SRC-003 (CSET); SRC-023 (EPRI) |
| T5 secondary analysis | 1 | SRC-005 (SIA/BCG) |

Claim classes of the entry definitions: 14 `FACT`, 29 `ATTRIBUTION`, 3 `DERIVATION`
(working definitions are marked `INTERPRETATION` inside entries). Status: 41
`verified`, 5 `disputed`. `not_researched` and `not_publicly_determinable` markers are
attached inside entries and dependencies (map §8).

**Retired:** none.

**Not retrievable** (register, last section): JEDEC, TSMC, Samsung, Intel, SEC EDGAR,
IEA, LBNL 2024 hosts, Applied Materials, KLA, Cadence, SEMI, ISO, OECD, Uptime, AMD,
Green Grid (member-only).

## Decisions made

See `docs/architecture/decisions.md`. All three are **proposed**.

- **D-013:** map "EDA/equipment" as sub-layers 5a EDA and 5b SME (the human decides via TQ-05).
- **D-014:** raw retrieval only; sites that refuse ordinary requests are recorded as
  not retrievable, not worked around; search is used for discovery only.
- **D-015:** provisional tiers T1–T6; company superlatives are `ATTRIBUTION`; `verified`
  in research artifacts means a Verifier re-read, not human review.

Working definitions (TQ-01 to TQ-12) are **not** decisions. They are proposals in
`domain-map.md` §7, awaiting the human.

### Rejected alternatives

- **Writing the map from model knowledge while sources were blocked.** Part B §16 lists
  network restriction as a stop condition, and CLAUDE.md §5 says a plausible
  statement without evidence is a gap. S01 stopped and asked the human instead.
- **Citing search snippets** in place of blocked primary sources (JEDEC, TSMC):
  forbidden by Part A.
- **A headless browser to get past sites' bot filtering.** Attempted once and denied by
  the environment's permission check. It was not pursued further and would not have
  been adopted (D-014).
- **Using WebFetch (a model summary of a page) as evidence.** Rejected in favour of raw
  text, so every anchor can be re-checked verbatim.
- **Restating figures** (market shares, PUE values, electricity projections). Metrics
  are out of scope. Pointers only (map §6).
- **Separate entries for CoWoS, H100 and similar products.** These are entities (S07/S08).
  They appear only as attributed examples inside concept entries.
- **Committing the audit script to `tools/`.** Part B §12 prohibits tooling changes. It
  stays in the session scratch area. Promoting it is suggested as S06 debt.

## Deviations

1. **Network stop and resume** (SESSION-PROMPT-SPEC §1 classification: *evidence/research
   issue*). At the start, every primary-source host was blocked by the environment's
   egress policy. S01 stopped (Part B §16) and asked the human. The human changed the
   environment's network settings, and retrieval then worked for most hosts. Several
   hosts still refuse plain requests (D-014).
2. **Session-scratch tools.** `pypdf` (with `cffi`, `cryptography`, `fonttools`) was
   installed into the session scratch directory to extract PDF text. This is not a
   repository dependency: no file in the repository references it.
3. **"EDA/equipment" rendered as 5a/5b** rather than as one layer (D-013), pending the
   human's answer to TQ-05. Part A's layer list is unchanged.
4. **Number of v1 concepts.** 41 of 46 entries are proposed as v1. That is more than a
   "minimum set" might suggest. Most are definitional prerequisites of the joints in
   §3 (e.g. DRAM for HBM, fab for foundry). S02 should prune them when it freezes the
   v1 scope.

## Debt introduced/resolved

Introduced:

- The evidence audit (anchor/locator/field checks) exists only as a scratch script.
  S06 should implement an equivalent check in `tools/` for research/claim files.
- 5 live company pages have no publication date. Only `accessed_at` and a content hash
  anchor them (register note 3). A future freshness check (`validate-freshness`,
  baseline §5) should re-fetch and compare hashes.
- CSET market-structure statements are 2019 data. Where they are cited, it is for
  definitions only; any later use needs current sources.

Resolved: none.

## Unresolved issues

### Evidence gaps

- **Blocked primary sources:** JEDEC HBM standards; TSMC foundry and CoWoS pages; Samsung;
  Intel; SEC filings; IEA; PUE standards (Green Grid / ISO/IEC 30134-2).
- **`not_researched`:** EUV necessity threshold; data-centre sub-types and "hyperscaler";
  server-integration actors; alternatives to EUV patterning.
- **`not_publicly_determinable`** (on current evidence): HBM supplier per accelerator;
  accelerator deployments per site; die/wafer allocation; interconnection utilisation.

### Source conflicts

CON-01 to CON-05 (map §5): accelerator scope; on-chip vs in-package HBM; chiplet
definition; breadth of advanced packaging; "foundry" as facility or business model.

### Layers or concepts considered and excluded

FPGAs, CPUs and edge chips; 3DS DRAM modules and NAND; package substrates and
materials; flip-chip and fan-out as separate entries; wafers, photoresists and gases;
photomasks; test equipment; the SME industry's own suppliers; networking and
interconnect (NVLink, InfiniBand, TPU ICI); storage; data-centre sub-types; PaaS/SaaS;
generation mix, transmission and fuels; tariffs as policy (EN-06 kept as future).
Reasons are given per layer in the map.

### Open terminology questions

TQ-01 to TQ-12 in `domain-map.md` §7. The most consequential for S03/S04:

- TQ-03 (advanced-packaging breadth);
- TQ-04 ("foundry");
- TQ-05 (EDA/equipment split);
- TQ-11 (a missing server-integration layer).

### Assumptions invalidated

- **"HBM" is a memory-only layer.** Invalidated. From HBM4, SK hynix plans a foundry
  logic base die (SRC-014), and HBM needs 2.5D packaging to be usable (SRC-013).
- **"Advanced packaging" is a back-end activity done by packagers.** Invalidated. It
  needs fab-type wafer processes (SRC-004 p.5), is split between foundry and OSAT
  (SRC-016), and is also done in-house by foundries (SRC-002 p.23; SRC-014).
- **Part A's seven layers are exhaustive.** Partly invalidated. Server/system
  integration sits between accelerators and data centres (TQ-11). Networking is a real
  dependency deferred by the non-goals.
- **Primary sources are retrievable from this environment.** Invalidated at session
  start; partly fixed by the human (Deviation 1).

### Human approvals required

1. **Terminology review** (Part A "Human task"): answer or challenge TQ-01 to TQ-12.
2. **Accept or reject D-013, D-014 and D-015.**
3. **Weekly gate:** the human's own judgement of whether they can explain the stack
   without the website.
4. **Blocked sources:** decide whether the human will supply JEDEC/TSMC/IEA documents
   manually (to be recorded as human-supplied), or whether S05 accepts the gaps.
5. **U-2** (milestone label collision) is still open from S00.

## Process lessons

- Checking source access **before** drafting avoided a map written from memory. The
  first access test found a total block. The stop cost one question to the human.
- Keeping short verbatim anchors in every entry made the self-audit cheap and
  repeatable. The script checked all 99 anchors, which left the manual audit free to
  focus on meaning. Three of 14 sampled entries still overstated their source. Both
  layers of checking earned their keep.
- Search results overstate pages (the Amkor snippet). Reading the retrieved page
  itself is not optional.
- Company self-descriptions are excellent for structure ("HBM is semi-packaged", "does
  NOT provide TSV formation") and must be quarantined for standing ("unique to",
  "leader").

## Implications for the next session

**Handoff: S02 — Architecture baseline + process benchmark (AUDIT / SYNTHESIS).**

- **Completed work:** the domain map and source register (draft); D-013 to D-015 (proposed).
- **Open issues:** the human's answers to TQ-01 to TQ-12; the blocked-source gaps;
  CON-01 to CON-05; U-2.
- **Audit findings:** the self-audit table above (3 fixes); the scratch-only evidence
  checker (debt).
- **Recommended next decision:** freeze which of the 41 proposed v1 concepts S03/S04
  must model. Start from the joints in map §1 item 8 and the 18 dependencies in §3, and
  demote definitional prerequisites that do not need their own entity type.
- **Files to read first:**
  1. this report;
  2. `docs/research/domain-map.md` (§1, §3, §7);
  3. `docs/architecture/baseline.md`;
  4. `docs/architecture/decisions.md` D-013 to D-015.

## Addendum — human review outcome (2026-09-29)

Appended after the human's review of the S01 output. The sections above are unchanged.

- **Terminology (approval 1):** the human answered TQ-01 to TQ-12. The answers are
  recorded once in `domain-map.md` §7.1 and adopted as working terminology for
  S02–S04 by **D-016** (accepted). Every answer took the working choice proposed in the
  map, with one addition: TQ-04 extends "foundry operator" to IDMs for the foundry
  services they sell.
  Map changes that follow from the answers:
  - FAB-06 (leading-edge threshold) moves from v1 to **future** (TQ-07);
  - ACC-05 is labelled "multi-die" (TQ-09);
  - PKG-06 scope is narrowed to "multi-die package" (TQ-09).

  v1/future is now 40/6.
- **Decisions (approval 2):**
  - **D-013 accepted.**
  - **D-014 and D-015 deferred.** Both stay `proposed` and are carried to S02/S05. Until
    then, the map's `verified` markers and source tiers rest on a proposed definition,
    not an accepted one.
- **Weekly gate (approval 3):** **open.** The human is still reviewing and has not judged
  the gate.
- **Blocked sources (approval 4):** left to S05's source policy. No human-supplied
  documents were added.
- **U-2:** still open.
- **Validation after these changes:** see the commit that adds this addendum. The unit
  tests, `tools/validate_repo.py` and the scratch evidence audit were re-run before
  pushing.
- **Updated handoff to S02:** the terminology questions are answered, so the recommended
  next decision is unchanged: freeze the v1 concept set (now 40 proposed) for S03/S04.
  S02 should also decide D-014 and D-015.
