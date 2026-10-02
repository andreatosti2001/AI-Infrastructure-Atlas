# AI-Infrastructure-Atlas — S13 Session Prompt

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

Content/evidence depth audit

Sample claims and relationships.

### Human focus

- inspect conflicts and weak sources;
- decide which claims must be downgraded or removed.

**Milestone M3 complete only after remediation of blocking audit findings.**

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
> - Everything above this line is **Part A**. As for S07 to S12, no upload was made: Claude
>   assembled Part A at the end of S12, when the human asked for "the .md file of prompt 13"
>   (2026-10-02).
>   - The operating contract, report list and headings are S12's Part A, word for word.
>   - The session-specific mission and human focus are copied verbatim from the operational
>     roadmap's week-5 entry for S13 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`,
>     "S13 — Content/evidence depth audit"), with the entry's closing milestone line.
> - Part B is Claude's elaboration of Part A into the 18 sections of `SESSION-PROMPT-SPEC.md` §2,
>   written after S12 (`SESSION-12-REPORT.md`, `milestone-audits/M2-audit.md`, D-109, D-110).
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The higher-level
>   documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The prompt becomes immutable once S13 begins (D-011).
> - **Not yet answered:** Part A's confirmation, H-0, H-1 and H-2. Ask them at the start of S13,
>   before any claim is sampled. H-3 is asked after the findings exist.

## 01 — Session identity

- **Session:** S13
- **Title:** Content/evidence depth audit
- **Type:** AUDIT (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`: "content passes audit").
- **Milestone:** M3 — Vertical Slice + Audit (D-019 numbering). M3 completes only when the blocking
  findings of S12 and S13 are remediated (Part A).
- **Predecessor:** S12 — Data architecture audit (`M2-audit.md`; D-109, D-110 `proposed`).
- **Expected successor:** S14 — DuckDB / SQL layer.
- **Complexity class:** medium; large if many claims must be narrowed and their records re-pointed.

## 02 — Mission

Test whether the content layer is stronger than the presentation layer: sample the canonical claims
and relationships, re-read each sampled claim's evidence in its source, judge it against the
claim model and the source policy, and leave an audit whose every finding the human has ruled on,
with the claims the human decides to downgrade or remove handled through the claim model's paths.

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S13 examines source quality, locator precision, evidence
overreach, stale claims, conflicting sources, the interpretation/fact boundary, "whether visual
annotations and takeaways remain supported by the underlying evidence" and "whether the visual
removes material caveats or uncertainty". Gate: "No scaling until evidence weaknesses are
corrected or explicitly documented."

**The evaluation framework.** PEF §6 (content and review audit: process and outcome); §3 (maturity
0–4, each rating citing evidence).

**What S12 hands over** (`SESSION-12-REPORT.md`, "Implications for the next session";
`M2-audit.md` Part 7):

- the claims that carry the most weight on the page: `claim-h100-hbm-stacks`,
  `claim-trainium2-hbm-capacity`, `claim-hbm-requires-3d-die-stacking` (D-091),
  `claim-tsmc-fabricates-h100` (D-092), `claim-aws-designed-trainium2` (D-093),
  `claim-sk-hynix-operates-m16` (D-099);
- the derivations to challenge: D-091, D-099, the TSMC claim;
- whether the short-answer sentence or the lane removes a caveat;
- the word guards are floors (S10-1: a refused edge passed every data check);
- every recorded human ruling followed Claude's recommendation (P-3, DT-11): the human's own reading
  should come first;
- Samsung, named in NVIDIA's memory-supplier sentence but not in `cand-002`;
- DT-10 (`publisher_entity` `not_researched` on 23 sources); `cand-009` not re-read (Amkor's host).

## 04 — Current state

As of `main` after S12 is merged. **S12 (`claude/s12-data-architecture-audit`, with this prompt) must
be merged to `main` before S13 starts.** Verify at start, and record the base, `git branch -a` and
`git ls-remote` in the report (D-018 L-03).

- **Data** (as measured at S12's final commit): 52 source records (company marketing 11, company
  filing 11, company technical documentation 8, standard specification 7, research report 5,
  company press release 4, government publication 3, policy research brief 2, industry association
  1); 120 canonical claims (55 `FACT`, 30 `ATTRIBUTION`, 17 `DERIVATION`, 17 `INTERPRETATION`,
  1 `IMPLICATION`; all `supported`), citing 38 sources; 33 entity records; 4 events;
  5 relationships; 12 refused candidates; staging empty.
- **Checks:** 301 tests and Gate 0 in CI; the page `site/hbm-chain/index.html` is rebuilt whenever an
  input changes (PG-7); browser QA by hand (D-106).
- **Status:** `M2-audit.md`, D-109 and D-110 are `proposed` (H-0 below).
- **The claim model's paths** (`claim-model.md` §3, §7): a claim's wording that exceeds its anchor is
  `partial` and must be narrowed into a new claim before any record rests on it; a claim whose
  locators do not state it is `context_only`; a factual contradiction is `disputed` with
  `disputed_with`; a canonical claim must be `supported` or `disputed` and accepted by the human
  (VD-8). A canonical record cannot rest on a staging claim (CE-1).

**Inherited open items:** TSMC → H100 (D-092); the HBM suppliers (D-094); the AWS legal entity
(D-093, DT-6); `supplies` items with no record; subsidiary records (D-095); TSMC's 20-F; S01's weekly
gate; S05 debt; the S11 new-user test as an independent walk-through; S12's DT-1 to DT-11.

**Not S13's:** the data model (S12's debt owners); SQL, metrics and DuckDB (S14–S15); new pages;
public deployment (NG-13).

**Next decision number:** D-111.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-12-REPORT.md`; `docs/architecture/milestone-audits/M2-audit.md` (Parts
   1b, 3, 4, 7).
2. `PROJECT-EVALUATION-FRAMEWORK.md` §3, §6; `SESSION-ROADMAP.md` S13.
3. `docs/architecture/claim-model.md` (§2 to §7, §10, §13); `docs/research/source-policy.md` (§4
   standing, §6 ER-1 to ER-10, §7 the matrix, §10 conflicts, §12 freshness).
4. `docs/architecture/edge-dataset.md` §1, §4, §7; `docs/architecture/vertical-slice.md` §4, §5.
5. The traces: `python tools/trace.py <ID>` for every sampled claim and edge.

**Repository paths to inspect:** `data/`, `site/hbm-chain/index.html`, `tools/trace.py`.

**External access:** re-retrieval of **registered** sources only, to re-read anchors (as S12's
Verifier pass); RA-4 (the human supplies a file) where a host refuses. No new source is registered,
and no new claim is extracted, unless the human approves it as a remediation. A finding that needs a
source the Atlas does not hold is a gap in the report.

**Lessons to carry:** L-01, L-02, L-04, L-05, L-09; S07 to S12: write the checks before the data;
ask before editing a file the prompt does not list; ask stop-condition rulings before building; a
break must fail for the reason it names; measure before estimating; send the human the steps before
the suggestions; not overreaching (D-108); a probe beats an argument (S12).

## 06 — Required reasoning

Answer these in the audit before any remediation is built.

1. **The sample.** How it is drawn (H-1), reproducibly: the rule, the seed or ordering, the list, so
   a second run draws the same claims.
2. **For each sampled claim:** does the anchor, re-read in its source at its locator, state the
   proposition; does the wording exceed it (overreach); is the locator precise enough to find it
   again; is the class and standing right for its matrix row; is the evidence fresh for its row; is
   its claim type right (a `FACT` that is an interpretation; a `DERIVATION` whose step does not
   follow); does another source contradict it.
3. **For each sampled edge and the drawn gap:** does the evidence state the relation as strongly as
   the page draws it (solid, dashed, gap)?
4. **The page:** do the short-answer sentence, the lane, the legend or any card remove a caveat the
   records carry (for example, a `not_researched` read as "no supplier", or a `DERIVATION` read as
   stated)?
5. **Source quality:** the share of evidence resting on company marketing; the 23 sources with
   `publisher_entity` `not_researched` (DT-10); any source whose bytes changed since registration.
6. **The S12 handoff:** D-091, D-099 and the TSMC claim, step by step; Samsung and `cand-002`.
7. **Blocking or not.** For each finding: blocking (fixed before S14, with the human's ruling), or
   documented debt with an owner. The gate allows either, but nothing undocumented.

## 07 — Tasks

**Audit**

1. The sample (H-1), drawn by a standard-library script kept with the report (S12 DT-8 pattern).
2. The human's own reading of the first items, before Claude's assessment of them (H-2).
3. The re-reads (Verifier role): each sampled claim's anchors in the registered bytes; re-retrieval
   results and access gaps recorded.
4. The audit report (`docs/research/content-audit-S13.md`, unless H-0 or the human names another
   path), with findings, evidence, PEF §6 maturity ratings and the blocking/debt split; a row in
   `docs/quality/audit-history.md`.
5. Remediation decisions from D-111, each `proposed`, asked of the human with the findings (H-3).

**Remediation (only what the human approves)**

6. For each claim the human downgrades: the claim model's path (`partial` → a narrowed claim with a
   new ID; `context_only`; `disputed`), and every record, edge or page element that rests on it
   re-pointed or removed, with the human's verdict recorded.
7. For each claim the human removes: it leaves `data/claims.json` with its verdict recorded (never
   deleted without trace; `claim-model.md` §7); anything resting on it follows.
8. The page rebuilt if any input changed; checks updated if a finding shows a check missing.

**Validation**

9. Fail first for any new check; deliberate breaks for each; S12's breaks re-run if the page changes.
10. Browser QA (D-106) if the page changes.

**Documentation**

11. `docs/README.md`, the baseline rows, `README.md` (Editorial); `SESSION-13-REPORT.md`, with the
    handoff to S14.

## 08 — Explicit non-goals

- New sources, claims, edges or entity records, except a correction or narrowed claim the human
  approves.
- Data-model changes (S12's debt owners: DT-1 to DT-9), unless a finding cannot be fixed otherwise
  and the human approves.
- SQL, metrics, shares, rankings, scores, DuckDB (S14–S15); a new page or component system.
- Rewriting accepted design documents beyond what an approved remediation needs.
- Public deployment (NG-13); editing the root documents or anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **Evidence:** Part A's rules. A finding is the Atlas's assessment (`INTERPRETATION`), never a new
  fact; a contradiction needs two sources the Atlas holds.
- **One home:** a narrowed claim replaces the old one in every record that cited it; nothing cites
  both.
- **Unknown ≠ zero:** a removed claim leaves an explicit state where a value depended on it, never an
  empty field read as "none".
- **Tooling:** standard library for `tools/` and the sampling script; `pypdf` only in a scratch
  virtualenv for reading PDFs (not a repository dependency); no new dependency without an approved
  decision.
- **Process:** L-02, L-04, L-08; gates run before any push; not overreaching (D-108).

## 10 — Agent responsibilities

As `docs/agents/contracts.md`.

| Agent | May write | Notes |
|---|---|---|
| Verifier | claims' `evidence_status`, `verified_on`, `disputed_with`, citations' `read`; reports | the re-reads; may downgrade, never replace evidence |
| Extractor | staging claims (a narrowed claim the human approves) | never improves a value the source does not state |
| Knowledge Architect | the audit report, `decisions.md` (append) | the blocking/debt split; the one-home ruling for re-pointed records |
| Data Auditor | `tests/`, `tools/`, the sampling script with the report | checks a finding shows to be missing |
| Editorial | the template's framing; state rows | only if a finding is about the page's wording |
| QA | the report (browser findings) | only if the page changes |

## 11 — Data and evidence rules

- **Canonical records:** read only, except the human-approved remediation.
- **Verdicts:** every downgrade or removal carries the human's words, verbatim, in the report.
- **Provenance:** every finding cites the claim, the source, the locator and the bytes read.
- **Temporal:** a stale claim is judged by F-1 as defined; a claim the model cannot date correctly
  is recorded against DT-2, not re-dated.
- **Confidence:** no numeric values.

## 12 — Implementation rules

**May create:** the audit report; the sampling script and its output with the report; narrowed
claims in staging (after the human's ruling); tests and fixtures for a missing check;
`SESSION-13-REPORT.md`.

**May modify:** `data/claims.json` and the records resting on a downgraded or removed claim (after
the human's ruling); `tools/build_page.py`, `tools/page_template.html`, `tests/` (only for an approved
remediation); `decisions.md` (append); `audit-history.md`; `docs/README.md`, baseline rows,
`README.md`; and, if H-0 is answered A, the status lines of `M2-audit.md`, D-109, D-110 and
`schemas/refused_candidates.schema.json`.

**Prohibited:** a downgrade or removal without the human's verdict; a claim narrowed by Claude's
judgement alone; a check loosened to pass; a new fact entering the data.

## 13 — Verification plan

- **At start:** the full suite and Gate 0, logged; base, `git branch -a`, `git ls-remote`; S12
  merged and this prompt on `main`.
- **Environment:** a fresh virtualenv from the pins, installed set compared with the pins.
- **Sampling:** the script run twice gives the same list.
- **Re-reads:** each sampled anchor found (or not) in bytes whose hash is recorded.
- **Remediation:** fail first; breaks; the page rebuilt byte-identically; browser QA if it changed.
- **CI:** reported separately from local results (L-08).

## 14 — Evaluation requirements

The report records: the sample and how it was drawn; the findings with evidence; PEF §6 ratings; the
blocking/debt split; decisions and rejected alternatives; the human's verdicts, verbatim; deviations;
invalidated assumptions; new debt; unresolved questions; and whether the S13 gate ("No scaling until
evidence weaknesses are corrected or explicitly documented") is met, and with it M3.

## 15 — Acceptance criteria

1. A reproducible sample covers every weight-bearing claim and edge of the page, plus the sample H-1
   sets.
2. Every sampled claim has a recorded re-read, or an access gap, and a finding.
3. The human read at least the items H-2 names before seeing Claude's assessment of them.
4. Every finding is blocking with a human-ruled remediation, or debt with an owner.
5. Every downgrade or removal follows the claim model's path, with the human's verdict verbatim; no
   record rests on a claim that is not canonical and `supported` or `disputed`.
6. No new fact enters the data.
7. Tests and Gate 0 pass in a fresh virtualenv; the page rebuilds byte-identically; CI observed or
   reported as not observed.
8. The report satisfies SPEC §5 and Part A; decisions appended as `proposed`; the handoff names what
   S14 needs from the content layer.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- a finding needs a source the Atlas does not hold;
- a downgrade would leave an edge, a record or the page resting on a claim that is not canonical;
- two sources the Atlas holds contradict each other on a value a record states;
- a remediation needs a schema change;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions.** Open questions follow `CLAUDE.md` §9A: each says what concretely changes under
each answer. Answers taken are kept verbatim.

- **Part A:** confirm as assembled, or amend; and where S13 runs (not yet answered).
- **H-0 — Human decision required: accept the S12 audit and its two new rules** (not yet answered;
  ask first; asked at the end of S12 and not answered there).
  - *What we are deciding:* whether S12's findings, ratings and debt list, and the two rules it
    produced, become accepted.
  - *What will concretely change:* if accepted, D-109 and D-110 in `decisions.md`, `M2-audit.md` and
    `schemas/refused_candidates.schema.json` change from "proposed" to "accepted", and
    `audit-history.md` records the outcome. No data, code or page changes. D-109 keeps the refused
    candidates in their own file with eight checks, shown on the page as cards and never as lines.
    D-110 sends every future value about a specific record into `data/` and keeps rules in their
    documents; four remaining tables of per-record values must move before S14.
  - *Why:* S13 audits the content on top of that model; its debt owners must be settled.
  - *What stays the same:* the records, the page and the checks.
  - *Options:* **A — Accept as written (recommended):** status lines only. **B — Accept with named
    changes:** Claude edits the named findings, owners or rules first. **C — Reject named items:** a
    rejected rule is reverted (rejecting D-109 returns the candidates to a document table and the
    page to its S11 form).
  - *Decision requested:* "Choose A, B or C", naming items for B or C.
  - *Technical reference:* D-109, D-110; `M2-audit.md` Parts 4, 5; S12 Deviation 2.
- **H-1 — Human decision required: how many claims the audit samples, and which** (not yet
  answered).
  - *What we are deciding:* the size and rule of the sample of the 120 canonical claims.
  - *What will concretely change:* under A, the audit re-reads the page's weight-bearing set (the six
    claims of §03, their input claims and the five edges) plus 20 other claims drawn by a fixed rule
    in proportion to claim type (about 9 `FACT`, 5 `ATTRIBUTION`, 3 `DERIVATION`, 3
    `INTERPRETATION`); under B, the weight-bearing set only; under C, every claim (120).
  - *Why:* the roadmap asks for a sample; the page's claims carry the most weight, and a drawn sample
    shows whether the rest of the data shares their weaknesses.
  - *What stays the same:* how each claim is judged, and the human's ruling on every finding.
  - *Future consequences:* A gives a measured rate for the whole dataset at moderate cost; B is
    fastest but says nothing about records off the page; C is complete but roughly triples the
    session and the human's review.
  - *Options:* **A — The page's claims plus 20 drawn by type (recommended)**; **B — The page's claims
    only**; **C — All 120 claims.**
  - *Decision requested:* "Choose A, B or C."
  - *Technical reference:* PEF §6; S12 handoff.
- **H-2 — Human decision required: does the human read some evidence before Claude's assessment**
  (not yet answered).
  - *What we are deciding:* whether the human re-reads a few sampled claims on their own, before
    seeing Claude's findings on them.
  - *What will concretely change:* under A, Claude sends three weight-bearing claims, each with its
    source link, locator and quoted anchor and the four questions of §06 q2, and records the human's
    answers verbatim before writing its own; the report compares the two. Under B, Claude assesses
    everything and the human reviews the findings.
  - *Why:* S12 found that every human ruling in S07 to S12 followed Claude's recommendation (P-3);
    an independent reading is the only check that does not start from Claude's view.
  - *What stays the same:* the findings, the remediation and the human's final rulings.
  - *Future consequences:* A costs the human about three source reads and gives the project its
    first independent content check; B is faster and leaves DT-11 open.
  - *Options:* **A — The human reads three claims first (recommended)**; **B — Claude assesses, the
    human reviews.**
  - *Decision requested:* "Choose A or B."
  - *Technical reference:* M2 audit P-3, DT-11; S11's process lesson.
- **H-3 — the remediation of each finding** (asked after the findings exist, not at the start): for
  each claim found weak, whether it is narrowed, marked `context_only` or `disputed`, removed, or kept
  with the weakness documented, and what happens to each record, edge or page element that rests on
  it. Each item is asked with its concrete consequence (CLAUDE.md §9A, "Approving several items at
  once").

## 17 — Deliverables

- the audit report and its row in `audit-history.md`;
- the sampling script and its output, with the report;
- remediation decisions from D-111, `proposed`;
- if approved: narrowed claims, re-pointed records, updated checks, the rebuilt page and browser QA;
- `docs/README.md`, baseline rows, `README.md`;
- `sessions/reports/SESSION-13-REPORT.md`.

## 18 — Handoff

S13's report must hand S14 (DuckDB / SQL layer):

- **Completed work:** the content audit and its remediation; whether M3 is complete.
- **For S14:** which claims and edges are safe to compute over, and which carry documented
  weaknesses a query must show; S12's DT-1 (the document tables that must move before S14) and DT-4
  (flattening for SQL).
- **Open issues:** debt with owners; everything §04 inherits.
- **Recommended next decision:** the first analytical question S14's SQL layer must answer.
- **Files for S14 to read first:** the S13 report; the content audit; `M2-audit.md` Part 4.
