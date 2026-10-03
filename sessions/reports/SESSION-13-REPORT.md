# SESSION-13 Report — Content and evidence depth audit

- **Session:** S13 · **Type:** AUDIT · **Milestone:** M3 — Vertical Slice + Audit (third and last
  session)
- **Date:** 2026-10-02
- **Prompt:** [`sessions/prompts/S13-PROMPT.md`](../prompts/S13-PROMPT.md) (Part A confirmed by the
  human at the opening, unchanged; Part B SPEC §2 detail; H-0, H-1, H-2 asked at the opening, H-3
  after the findings).
- **Branch:** `claude/new-session-4kuwvw` (the environment's designated branch), created at `main` @
  `bb3a9a6` (the PR #22 merge, which carries S12 and this prompt).
- **Base** (D-018 L-03), at the start of the session:
  - `git branch -a`: `claude/new-session-4kuwvw` and `main`, with `remotes/origin/claude/new-session-4kuwvw`
    and `remotes/origin/main`, all at `bb3a9a6`.
  - `git ls-remote`: `HEAD` at `bb3a9a6`; the older `claude/*` branches as S12 listed them
    (`claude/atlas-architecture-baseline-jow618` `26acdf9`, `claude/beautiful-albattani-gyg4nw`
    `ace06f0`, `claude/magical-galileo-vwn13j` `ce5b881`, `claude/new-session-15s0bd` `c51cb60`,
    `claude/new-session-djql6o` `b741fb7`, `claude/new-session-mdyi2x` `6f926b0`,
    `claude/new-session-o16fd6` `d9d0a83`, `claude/s07-company-dataset` `a5032ef`,
    `claude/s08-concept-dataset` `41806c5`, …).
- **Commits:** `99f1c4e` (H-0), `ed9a8f4` (the sample), `8592838` (the audit), `cc0f665` (F-1
  remediated, rulings recorded), and the commit that adds this report.

## Mission outcome

**Delivered: the content audit, every finding ruled by the human, the one blocking finding
remediated. M3 is complete.**

- [`docs/research/content-audit-S13.md`](../../docs/research/content-audit-S13.md): a reproducible
  sample (the page's 14 weight-bearing claims and 20 drawn by type), each claim re-read in freshly
  retrieved bytes, the five edges and the drawn gap judged against the page's marks, source quality,
  coverage and freshness exposure measured, eleven findings, PEF §6 maturity ratings.
- **The content holds where it speaks.** Of 34 sampled claims, 32 could be re-read; in none does the
  statement exceed its sentence, none has the wrong claim type, and no two sources the Atlas holds
  contradict each other. 23 of 23 readable anchors were found at their locators (13 of 13 PDF pages
  exact).
- **The weaknesses are in what the page shows and in the system around the claims.** The blocking
  one: the page's card for NVIDIA's memory suppliers named two of the three firms NVIDIA names
  (F-1). Remediated (D-111): `cand-002` now names Samsung as a party with no record, and the card
  shows all three.
- **Ten findings are documented debt with owners** (D-112, D-113), among them: the H100 figures
  come from a launch blog that calls them preliminary (F-3); evidence ages past the 12-month horizon
  with no signal, Micron's four values on 2026-10-03 (F-5); "party" standing is unchecked on 14
  citations (F-2, DT-10 re-owned).

**Restated contract** (at the start of the session):

- **Mission:** sample the canonical claims and relationships, re-read each sampled claim's evidence
  in its source, judge it against the claim model and the source policy, and leave an audit whose
  every finding the human has ruled on; downgrade or remove only what the human decides.
- **Non-goals:** Part B §08: no new sources, claims, edges or entities; no data-model change; no
  SQL or DuckDB; no new page; no deployment.
- **Acceptance:** Part B §15.
- **Plan:** baseline; Part A, H-0, H-1, H-2; the sample; the human's reading; the re-reads; the
  audit and D-111 onward; H-3; only the approved remediation; checks, breaks, browser QA;
  documents; report. The plan held.

**Approved by the human** (2026-10-02; outcomes only, D-114):

| Decision point | Outcome | Effect |
|---|---|---|
| The session prompt (Part A) | followed as written | prompt unchanged |
| The S12 audit and its two rules (H-0) | accepted, no other change | D-109, D-110, `M2-audit.md`, the candidate schema accepted (`99f1c4e`) |
| The sample (H-1) | the page's 14 weight-bearing claims plus 20 drawn by type | the sample |
| An independent reading first (H-2) | three claims read by the human before Claude's assessment; each judged to hold | audit Part 2 |
| F-1, the card for NVIDIA's memory suppliers (H-3) | the card names all three firms | D-111; `cand-002`; page rebuilt |
| F-3, the H100 figures (H-3) | the claim stays; the caveat is recorded | D-112 |
| F-2, F-4 to F-11 (H-3) | recorded as debt with owners, no data change | D-113; audit Part 7 |

## Files changed

| File | Change |
|---|---|
| `docs/research/content-audit-S13.md` | new: the audit (findings ruled; ratings proposed) |
| `sessions/reports/SESSION-13-sample/draw_sample.py`, `sample.json` | new: the sampling script (standard library) and its output |
| `sessions/reports/SESSION-13-sample/reread.py`, `reread-result.json` | new: the Verifier's re-read script (`pypdf` in a scratch virtualenv) and its per-citation results |
| `sessions/reports/SESSION-13-breaks/breaks.py`, `breaks-result.txt` | new: S12's breaks scripted, plus five for D-111, and the run's output |
| `sessions/reports/SESSION-13-qa/` | browser QA script (S12's, one comment line added), results, two screenshots |
| `data/refused_candidates.json` | `cand-002`: Samsung as a no-record party; reason `endpoint_has_no_record`; one reasoning sentence (D-111) |
| `site/hbm-chain/index.html` | rebuilt (285,359 bytes) |
| `docs/architecture/decisions.md` | D-109, D-110 accepted (H-0); D-111 to D-113 appended and accepted (H-3) |
| `docs/architecture/milestone-audits/M2-audit.md`, `schemas/refused_candidates.schema.json` | status lines (H-0) |
| `docs/quality/audit-history.md` | the S12 row's outcome (H-0); the S13 row |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows |
| `sessions/reports/SESSION-13-REPORT.md` | this report |

## Data changed

- **One record changed:** refused candidate `cand-002` (D-111). Its quote, locator and `read` are
  unchanged; the sentence was re-read in S13 in bytes equal to the registered ones.
- **No source, claim, entity, event or relationship record was created, edited or moved.** No claim
  was downgraded or removed. No new fact entered the data: "Samsung" is the quoted sentence's own
  word, already in the record.
- As measured at `cc0f665`: 52 source records; 120 canonical claims; 33 entity records; 4 events;
  5 relationships; 12 refused candidates; staging empty.

## Tests run

Python 3.11.15. "Fresh venv" is a virtualenv built from `requirements-test.txt` in the session
scratchpad; `pip freeze`, sorted, equalled the pins.

| Command / check | Result |
|---|---|
| **At start** (`bb3a9a6`), fresh venv | OK (301 tests); `Repository integrity: OK`; `page: up to date` |
| After H-0 (`99f1c4e`) | the page's digest line changed (`decisions.md` is an input); rebuilt; OK (301) |
| `draw_sample.py` run twice; `--check` | identical output; "sample: equals a re-draw" (also at the end) |
| Re-retrieval of the 20 cited sources (2026-10-02T23:10Z, `curl`) | 17 of 18 automated: registered bytes; `src-042`/`src-051`: new bytes on every request; `src-031`, `src-038`: HTTP 403 challenge |
| `reread.py` | 28 citations: 23 anchors exact (13 of 13 PDF pages as located), 5 access gaps, 0 missing |
| **Fail-first** for D-111: `cand-002` changed, page not rebuilt | 4 failures: PG-2 (the card's `/reasoning`), PG-2 derived, PG-5 (`candidate='cand-002'`: the card missing from its new reason group), PG-7; the candidate checks pass |
| Page rebuilt twice | byte-identical |
| **Deliberate breaks** (`breaks.py`; table below) | 30 caught for their named reasons; 2 controls pass |
| Browser QA (below) | clean at 1280 px and 375 px |
| **Final** (`cc0f665`), fresh venv | OK (301 tests); `Repository integrity: OK`; rebuild byte-identical with the committed page |
| **CI** | runs 109 (`99f1c4e`), 110 (`ed9a8f4`), 111 (`8592838`), 112 (`cc0f665`): success. Not observed at the commit that adds this report (L-08) |

No test was added or changed (audit Part 7: the missing check, "a refused candidate names every
party its quote names", needs a reader).

### Deliberate breaks

Each break edits a fresh copy of the repository and runs the full suite; it counts only if the suite
fails and the named fragment is in the output. Full output:
[`breaks-result.txt`](./SESSION-13-breaks/breaks-result.txt). S12's numbers are kept.

| # | Break | Caught by (besides PG-7) |
|---|---|---|
| 1 | a mark with no record behind it | PG-2, PG-3 |
| 2 | a hand-edited label (H100 → H200) | PG-2 |
| 4 | a supplier gap drawn as zero | PG-2 |
| 5 | a staging edge on the page (not rebuilt) | PG-2 (three), PG-3 (two), PG-4 |
| 6 | a DERIVATION drawn as stated | PG-4 |
| 7 | a changed claim statement, not rebuilt | PG-2, PG-2 derived |
| 8 | an anchor that no longer matches | PG-2 |
| 9 | a mark unreachable by keyboard | PG-8 |
| 10 | an evidence panel removed | PG-3, PG-4, PG-9 |
| 11 | a build that stamps the clock (rebuilt) | PG-7 only |
| 12 | framing that names a record (rebuilt) | PG-6 only |
| 13 | "none" for a missing relationship | PG-2 derived, PG-5 |
| 15 | a script fetched from the network | PG-9 |
| 16 | a hover-only rule (rebuilt) | PG-8 only |
| 17 | a text colour below WCAG AA (rebuilt) | PG-8 only |
| 18 | a quoted rule code whose definition is removed | PG-10 |
| 19 | a refused candidate referenced in the diagram | PG-5 cards |
| 20 | a card removed from one of its reason groups | PG-5 cards |
| 21 | a journey candidate moved to staging | the staging refusal, PG-10, PG-2, PG-3, PG-5 cards |
| 22 | a no-record name that is a record's name (ASML) | RC-4 |
| 23 | an item with no record, its reason dropped | RC-5 |
| 24 | a sentence used by an edge and refused | RC-6 |
| 25 | a stored status on a candidate | RC-1 |
| 26 | a reasoning that quotes a rule with no home | RC-7 |
| 27 | a candidate given an edge's ID | RC-1, PG-10, PG-2, PG-3, the lane refusal |
| S13-1 | Samsung removed from the page's card by hand | PG-2 |
| S13-2 | Samsung kept, its reason dropped | RC-5, PG-5 cards |
| S13-3 | Samsung's name replaced by a record's name (SK hynix) | RC-4, PG-2 |
| S13-4 | Samsung's name replaced by a placeholder | RC-4, PG-2 |
| S13-5 | Samsung dropped from the data, page not rebuilt | PG-2, PG-5 cards (stale page only) |
| C | control: README edited | passes |
| D | control: `edge-dataset.md` prose edited | passes |

**Not re-run:** S12's #3 (a supplier gap removed from the diagram), #14 (a new edge linking the
lane) and control E (every company renamed, rebuilt): each needs a multi-site edit the script does
not yet make. **S13-5 shows the limit of D-111:** dropping Samsung from the data *and* rebuilding
would pass every check (audit Part 7).

## Browser QA (D-106)

Playwright from `/opt/node-tools` with the pre-installed Chromium, on the rebuilt page:
[`SESSION-13-qa/qa.js`](./SESSION-13-qa/qa.js), [`qa-result.json`](./SESSION-13-qa/qa-result.json).

| Check | 1280 px | 375 px |
|---|---|---|
| Console messages, page errors | none | none |
| Network requests | the page file only | same |
| Horizontal overflow; elements wider than the viewport | 1280 / 1280; none | 375 / 375; none |
| Diagram scale; smallest diagram text | 1.31; 14.4 px | 0.95; 10.5 px |
| Marks reached by Tab; Enter lands on each panel | 17 of 17; all | same |
| Contrast on every rendered text node | 3,029 nodes; minimum 6.21:1; none below 4.5:1 | same |

Screenshots: [`desktop-03-gaps.png`](./SESSION-13-qa/desktop-03-gaps.png),
[`mobile-03-gaps.png`](./SESSION-13-qa/mobile-03-gaps.png): the card reads "SK hynix, Micron
Technology, Samsung (no record in the Atlas) → NVIDIA · supplies · item: memory" under "endpoint
has no record" and "item has no record", and D-111 is among the rules cited.

## Evidence added/retired

**None added, none retired.** No source was registered; no claim changed. External access: the 20
registered sources the sample cites were re-retrieved once (and the NVIDIA blog twice more, to test
whether its bytes change per request); nothing was read for new content. `src-031` and `src-038`
refused plain requests (403 challenge pages) and were not bypassed (RA-2); RA-4 was not requested
(F-7, debt).

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-109, D-110 | S12's refused-candidate records; values in data, rules in documents | accepted at the opening (H-0) |
| D-111 | a refused candidate names every party its quoted sentence names (`cand-002`, Samsung) | accepted (H-3) |
| D-112 | the H100 memory figures keep their claim; the "preliminary" note is debt | accepted (H-3) |
| D-113 | the audit's debt and owners; DT-10 re-owned | accepted (H-3) |

**Rejected alternatives** (in each decision and the audit): a Samsung company record (no Samsung
filing read); removing the `cand-002` card; narrowing the H100 claim (a new ID and rebuilt page for
figures no record uses as values); a page note for the "preliminary" caveat or the AWS alias (each
needs a place in the data, a model change); linking ten sources' publishers in S13 (a value about
the world without a rule for web publishers); a freshness test that reads the clock (CI would turn
red on a date, not a change); a generic "parties in the quote" check (needs a reader).

## Deviations

1. **`data/refused_candidates.json` is outside Part B §12's "May modify" list**, which names
   `data/claims.json` and records resting on a downgraded or removed claim. F-1 is about a refused
   candidate, not a claim. The human's H-3 ruling named this change, so it was made on that ruling.
2. **The re-read script and the breaks script live in `sessions/reports/`**, not `tools/`: the first
   needs `pypdf` (not a repository dependency) and network bytes kept outside the repository; the
   second is a session harness (DT-8's pattern).
3. **"Any source whose bytes changed since registration"** (Part B §06 q5) was measured on the 20
   sampled sources only; the other 32 registered sources were not re-retrieved.
4. **S12's breaks #3 and #14 and control E were not re-run** (above).
5. **No check was added** for F-1: the prompt allows checks where a finding shows one missing, but
   telling which words of a sentence are firms needs a reader.

**Invalidated assumptions.**

- Part B §06 counted the weight-bearing set as "the six claims of §03, their input claims": it is
  14 claims, because one input (`claim-atlas-3d-die-stacking-working-definition`) has an input of
  its own.
- H-2 assumed a reading recorded question by question; the form recorded one judgment per claim.

## Debt introduced/resolved

**Resolved:** S12's handoff items on Samsung (`cand-002`), D-091, D-099 and the TSMC claim
(re-checked: they hold as ruled); DT-11 partly (the human read before Claude's assessment); the
missing content audit (PEF §6).

**Introduced or re-owned** (audit Part 7, D-112, D-113): DT-S13-1 (F-2, DT-10 re-owned) to
DT-S13-10 (F-11), each with an owner and a due point. Also: `breaks.py` replays 25 of S12's 27
breaks; the remaining three need scripting when the page next changes.

**Open, with owners:** S12's DT-1 to DT-9; everything Part B §04 inherits.

## Unresolved issues

**Maturity ratings.** The audit's PEF ratings (audit Part 8) stay proposed. Accepting them changes
only the audit's status line and its row in the audit history. They are: content-and-review
process 3, outcome 2, both unchanged from M2.

**Human decision required: the wording of three new project rules in the root documents**

- *What we are deciding:* whether the drafted sentences for D-114, D-115 and D-116 go into
  `CLAUDE.md` and `SESSION-PROMPT-SPEC.md` as written.
- *What will concretely change:* if approved, `SESSION-PROMPT-SPEC.md` §9's last paragraph is
  replaced (decisions recorded as outcomes and dates, not transcripts), and `CLAUDE.md` §12 and §17
  gain three sentences (the SQL tutorial next to every SQL result; meaning before mechanism;
  outcomes, not transcripts). The drafts are in each decision's "Root documents" line. No data, page
  or check changes.
- *Why:* every future session loads these two files first. Until they change, each new session prompt
  must restate the three rules by hand.
- *What stays the same:* the decisions themselves are already in force (accepted 2026-10-03).
- *Options:* **A, approve the drafts as written:** the two files are edited. **B, change named
  sentences first:** Claude redrafts them before any edit.
- *Decision requested:* "Approve A, or name the sentences to change."

**Maturity ratings.** The audit's ratings (Part 8) stay proposed. Accepting them changes only the
audit's status line and its audit-history row.

**Not asked now:** public deployment (NG-13); merging this branch to `main` (not requested this
session).

**Inherited, unchanged:**
- TSMC → H100 `fabricates` (D-092);
- the HBM supplier of each product (D-094);
- the AWS legal entity (D-093, DT-6);
- `supplies` items with no record;
- subsidiary records (D-095);
- TSMC's 20-F;
- S01's weekly gate;
- S05 debt;
- the S11 new-user test as an independent walk;
- `cand-009` not re-read.

## Process lessons

- **The claims were stronger than the records around them.** Every sampled claim held, but a
  refused-candidate record (not a claim, and so never re-read against the claim rules) had narrowed
  its own quote. Audits should sample every record kind that quotes a source, not only claims.
- **A byte hash is no signal on a dynamic page.** Three hashes in one evening, same text. Measure
  before trusting a "same bytes" line.
- **Give the reading a form shaped like the comparison.** One field per question, so the
  independent reading can be set against Claude's question by question.

## Implications for the next session

S14 — DuckDB / SQL analytical layer:

- **Completed work:** the content audit and its remediation. **M3 is complete:** S12's B-1 and
  S13's F-1, the milestone's blocking findings, are remediated with the human's rulings; every
  other finding is documented debt with an owner.
- **Safe to compute over:** the 120 canonical claims and 5 edges as stated, with each value's basis
  (stated, inferred, gap) and evidence date carried into every result.
- **Weaknesses a query must show:**
  - no value is corroborated by a second publisher (audit Part 5);
  - the H100 capacity figures are "preliminary" in their source and are not computed over
    (DT-S13-2);
  - "HBM requires 3D die stacking" restates a definition and is not independent evidence; "SK hynix
    operates M16" shows its evidence date (DT-S13-7);
  - "party" standing is unchecked on 14 citations (DT-S13-1);
  - `time_sensitive` values pass the horizon in place, Micron's from 2026-10-03, so a query
    presenting a value as current must compute its age (DT-S13-4).
- **Before S14 starts:** S12's DT-1 (the four document tables of per-record values move into
  `data/`) is due; DT-4 (flattening for SQL) is S14's.
- **Recommended next decision** (S14's first analytical question): *for each accelerator on the
  page, which dependencies does the Atlas record, with what basis (stated, inferred, gap) and what
  evidence date?* That is a lineage-carrying table that reproduces the page's chain from SQL before
  any metric is built.
- **Files for S14 to read first:**
  - this report;
  - [`docs/research/content-audit-S13.md`](../../docs/research/content-audit-S13.md) (Parts 5 to 7);
  - [`docs/architecture/milestone-audits/M2-audit.md`](../../docs/architecture/milestone-audits/M2-audit.md)
    Part 4.

**Next recommended milestone:** S14, starting with DT-1, then the lineage table above.

**S13 gate** ("No scaling until evidence weaknesses are corrected or explicitly documented"):
**met.**

## Addendum — three new project rules (2026-10-03)

After the report, the human set three standing rules, recorded as D-114 to D-116 (accepted):

- **D-114, outcomes, not transcripts.** Records of human decisions state the outcome and the date,
  never the question as asked or the human's words. S13's report, audit, decision statuses, audit
  history and sample script were rewritten that way the same day. This supersedes the S13
  prompt's requirement to keep answers verbatim (Part B §11, §14, §16; `SESSION-PROMPT-SPEC.md`
  §9) for S13 and after. Earlier sessions' files and the commit messages already pushed are
  unchanged.
- **D-115, a SQL tutorial next to every SQL result** on the Atlas pages: S14 builds the first.
- **D-116, meaning before mechanism.** Pages and documents read in plain language first, with
  technical detail behind it.

The root-document wording waits for the human's approval (Unresolved issues above). For S14, the
prompt carries all three rules, and the lineage table recommended above gets its SQL tutorial.

