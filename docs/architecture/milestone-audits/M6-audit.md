# M6 Milestone Audit — Client Product (S20 to S21.5)

> **Records cited.** This is a process audit (PEF §4). The session reports and prompts it cites are kept in the
> private development archive, not in this repository (D-151); the decisions, documents and files it cites are here.

**Status:** ACCEPTED by the human on 2026-10-15 (S22 H-2, D-213); M6 closes with this audit. Written in S22 because M6
had closed without its audit (S22 H-1).
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4 (a milestone audit at every major milestone);
`SESSION-PROMPT-SPEC.md` §4 (mandatory "before client mode is considered stable": the client brief is S21's).
**Written by:** Claude, as the Knowledge Architect; the human's review stands in for the Portfolio Reviewer (D-184).
The same model did the work it audits; counts below are recounted from Git, the checks and the session reports.
**Base read:** `claude/new-session-evm2a6` @ `5c492b2`. M6's work reached `main` in PR #35 (S20, `4d84405`), #36 (S20.5,
`675dbac`), #37 (S21, `590a70f`) and #38 (S21.5, `6c19501`). The code and engineering side is audited in
[`../engineering-audit.md`](../engineering-audit.md); this audit is about the milestone's process and outcome.
**What this audit is:** an `INTERPRETATION` of the project's own record.

## Part 1 — The eight questions (PEF §4)

### 1. What was intended

The roadmap's M6, "Client Product":

- **S20, researcher and analyst UX:** "Turn the knowledge system into a product that answers concrete investigation
  questions efficiently", through six journeys (explore a dependency, a company, a country, inspect evidence, compare
  layers, a temporal relationship in an editorial visual). Gate: "Each major UI feature maps to a documented user
  question."
- **S21, client brief generator:** "a reproducible, evidence-backed technology dependency brief from a defined question
  and scope", with no autonomous legal, investment or procurement recommendation.

Two sessions were added by the human during the milestone: **S20.5** (D-199), a frontend architecture assessment and
framework decision; **S21.5** (D-207), the Change Detector's dated search for later rules.

### 2. What was implemented

| Session | Delivered | Record |
|---|---|---|
| S20 | the entry page, the export-control page (an acts × classes matrix, a timeline, statuses derived on the as-of date), 9 company and 4 place pages; the first page view of the policy links with the no-advice line; C-2 and C-5 resolved; a design pass after the human's review; checks JR-1 to JR-12 | `visual-architecture.md` §15; D-189 to D-198 |
| S20.5 | the frontend decision: static, script-free, Python-built pages kept, Vue.js assessed and not adopted; one CSS guard for the research view's filter; the version roadmap (v1.5 visual intelligence, v2 global coverage) | D-199 to D-201; `VERSION-ROADMAP.md` |
| S21 | the client brief (`site/briefs/accelerator-memory/`): twelve sections, every sentence composed from records and recomputed by CI, scope and limits on the first printed page; the Client Output active; one composition mechanism for new templates; checks BR-1 to BR-12 | `client-brief.md`; D-202 to D-206 |
| S21.5 | the Change Detector active; a dated, logged search of the Federal Register from 6 December 2024 to 15 October 2026; two later acts recorded with 22 claims; the pages say up to when later texts were searched (JR-13) | `change-detection.md`; D-207 to D-210 |

**Against the gates:**
- **S20's gate is met:** each page maps to a recorded question (`visual-architecture.md` §15.1), and what the records
  cannot answer is stated on each page.
- **S21's boundary is met and checked:** BR-9 refuses advice words in the Atlas's voice; no sentence says a product or
  firm is controlled.
- **S20.5's gate is met:** one outcome decided with its evidence; provenance stays checkable; nothing loads from the
  network.
- **S21.5's gate is met:** the search is logged and re-runnable (from S22 by a tool, D-211); every later act was
  recorded from its official text with the human's verdict.

**Counts** (recounted from the session reports): tests 418 → 438 (S20) → 439 (S20.5) → 465 (S21) → 466 (S21.5);
pages 2 → 17 → 17 → 18 → 18; breaks 130 → 149 → 152 → 172 → 178, every full run clean (133/133, 135/135, 153/153,
158/158 faults); sources 61 → 64, claims 174 → 196, policies 5 → 7, events 15 → 19 (S21.5). Decisions D-189 to D-210.

### 3. What changed, and why

- **A design pass inside S20** (D-198): every check passed on pages the human judged poor ("1 recorded links", the
  answer buried, a matrix of words). The pass kept the rules (no script, system fonts, every value traceable).
- **S20.5 was inserted** before the brief so that a later change of stack would not also touch it (D-199). It kept the
  stack: no recorded question needed state in the browser, and the provenance checks cannot see text a script draws
  (D-200).
- **The release plan grew a v1.5 and a v2** (D-201): the visual gap to the benchmarks comes chiefly from thin
  quantitative data and one covered path, so it is a version, not a pass.
- **The brief's question says "reported to supply"**, not "known to make" (D-202): both supplier namings rest on
  third-party reports. Five classes are compared, not three (D-203).
- **S21.5 was inserted** after the external audit of 2026-10-14 (D-207): every act said "no later change recorded"
  without a dated search behind it.

### 4. Which assumptions failed

- "The suite passing locally means CI passes": false across Python versions (S20, three red commits).
- "The checks show the pages are good": they prove truth and traceability, not hierarchy or legibility (D-198).
- "The research view's `:has()` filter is a known problem": no failure was shown in Chromium; the real risk, other
  engines, is still unverified (D-200; engineering audit F-11).
- "The AI Diffusion rule's reported withdrawal has an official text": none in the window (D-209).
- "The prompt describes the base": S21.5's prompt described S20.5's state and named a decision number S21 had used.
- "S22 opens on a later day than S21.5" (S22's prompt): it opened the same day, so its search window was empty (D-211).

### 5. Which shortcuts were taken

- Browser and print QA by hand, outside CI, on Chromium only (A-6); the scripts could not even fail (engineering audit
  F-1).
- Visual quality checked by eye (A-7).
- The later-rule search scripted in the archive, not in a tool (resolved in S22, D-211).
- The brief reused the journeys' build by subclassing, two levels deep, rather than shared components (F-8).
- Print length accepted at 65, then 79 A4 pages (A-4; D-210's compact list is S22's).

### 6. What technical and research debt was created

| Item | Owner (as ruled or proposed) |
|---|---|
| A-1 to A-7 (engineering) | ruled in the engineering audit §6 |
| A-4, evidence panels repeated on every page (1.39 MB for the journeys; the brief 884 KB) | a later UX session (v1.5) |
| No search across records (needs a script) | v1.5 (its opening decides scripts, D-201) |
| The EAR's dates | the next policy research session (D-210) |
| The July 2026 enforcement statement on no page | S22 (D-210) |
| Texts after the "Searched to" date | every session that moves the as-of date (D-208), now by the tool (D-211) |

### 7. What was removed or rejected

Vue.js on the research view (D-200); a Markdown export and a PDF of the brief (D-202); a free-text summary and a SQL
query for it (D-203); "monitoring considerations" as advice, replaced by "what this brief does not track" (D-203);
folding the later-rule search into S22 (D-207); a repeal or end date from the July 2026 statement (D-209); the CFR
finding-aid PDFs as the tool's second register (D-211).

### 8. What should be carried into the next phase

- **Client mode is stable for v1.0 once two S22 items land:** the browser and print checks run in CI and can fail
  (engineering audit F-1, H-0), and the printed brief lists each claim once (D-210). The brief is otherwise
  reproducible, recomputed sentence by sentence in CI, and scoped on its first page.
- The as-of date moves only with a search run (D-208); the tool makes that a command (D-211).
- S23 inherits the content questions M6 met: the H100's fabrication evidence (E-1), `src-043`'s two access dates
  (C-8), the M5 data rows, the working definition of HBM.
- v1.5 inherits the visual debt (A-2, A-3, A-4, A-7, dark mode, mobile infographics).

## Part 2 — Process findings (PEF §4, §12)

| ID | Finding | Evidence | Disposition |
|---|---|---|---|
| M6-P1 | **The human's look at the pages found what no check could.** D-198 came from a screenshot review; every check had passed | S20 report, Deviation 8 | standing practice: show pages to the human before H-2 |
| M6-P2 | **The same lesson cost CI twice**: run CI's checks, on CI's Python, immediately before committing (S20: 3.12 syntax; S21.5: a decision appended after the rebuild) | S20 and S21.5 reports | engineering audit F-4 and F-7 |
| M6-P3 | **Prompts were written before their predecessor merged**, so two described an older base (S21.5) or a later day (S22) | S21.5 report, Deviations 1 and 2; D-211 | standing practice: §04 is re-measured at the start (S22's prompt already says so) |
| M6-P4 | **Asking after reading kept options concrete** (M5-P1 again): S21.5's H-3 changed with what the texts said | S21.5 report, Deviation 4 | standing practice |
| M6-P5 | **The milestone closed without its audit**, as M3 and M4 did (M4-P3) | `audit-history.md`; S22 H-1 | the last session of a milestone carries its audit in its prompt, or the next prompt says so |

## Part 3 — Maturity (PEF §3), where M6 produced new evidence

| Dimension | Rating | Evidence |
|---|---|---|
| Product / user value: outcome | **2, Defined** | five investigation questions and a client brief answered on pages, each value traced to its record and checked; but no reader beyond the human has used them, and the human judged the visual quality below the benchmark (D-198, D-201) |
| Product / user value: process | **3, Controlled** | each page from a recorded question (S20 gate); the framework question decided on evidence (D-200); limits stated on every page |
| Content & review: outcome (policy freshness) | **3, Controlled** | a dated, logged search over two registers; both sides of every change quoted; JR-13 keeps the pages' search date at or after the as-of date |
| Reproducibility: outcome | **3, Controlled** | 18 pages rebuilt byte for byte; the brief's every sentence recomputed; the search re-runnable by a tool (D-211) |
| Code / engineering | see the engineering audit §7 | |

## Part 4 — Findings and debt

No blocking finding is specific to M6's process; the engineering audit's F-1 (blocking) concerns M6's pages and is
remediated with H-0's CI job (D-212). The rest is debt with the owners above. **M6 is closed** with this audit (D-213).
