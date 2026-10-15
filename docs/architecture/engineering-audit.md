# Engineering audit (S22)

> **Records cited.** The session reports and prompts this audit cites are kept in the private development archive,
> not in this repository (D-151); the decisions, documents, commits and files it cites are here. The measurements can
> be re-run: [`../quality/audit-evidence/engineering-audit/`](../quality/audit-evidence/engineering-audit/).

**Status:** PROPOSED (S22, 2026-10-15), for the human's ruling item by item (S22 H-2).
**Required by:** `SESSION-ROADMAP.md` S22 (the twelve points of §3 below); `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §9
(code and engineering), §3 (maturity), §4 (the pre-release dual audit: this is its engineering half).
**Base read:** `claude/new-session-evm2a6` @ `5c492b2` (public `main` = `6c19501`, S21.5, plus S22's later-rule search
tool, D-211). Measures were taken on that tree on Python 3.11.17 and Chromium 141 unless a row says otherwise.
**Who audits:** Claude, as the Knowledge Architect (D-184: the Portfolio Reviewer is inactive until S24); the same model
wrote most of the code it audits. The audit therefore prefers what a script can recount (counts, coverage, rebuilds,
break runs, browser measures) to self-assessment, and shows the evidence beside each conclusion. Each finding is an
`INTERPRETATION` of that evidence; every number labelled *measured* comes from the evidence folder (L-04).

## 1. What the system is

A research product whose facts live in JSON records (`data/`, 25 files), checked by JSON Schemas and by a
standard-library test suite, analysed by four SQL queries run in an in-memory DuckDB (`tools/warehouse.py`, the only
third-party runtime import), and published as 18 static, script-free HTML pages written by four Python builds
(`build_page.py`, `build_insight.py`, `build_journeys.py`, `build_brief.py`). Every page states an input digest and is
rebuilt byte for byte by `--check`. A break harness plants faults in copies of the repository and requires the suite to
fail for the reason each fault names. Browser checks (four Playwright scripts) run by hand. Since S22 a standard-library
tool runs the later-rule search over the Federal Register (D-211).

| Measured (`measures.json`) | Files | Lines |
|---|---|---|
| `tools/*.py` | 11 | 5,190 |
| `tools/*.html` (templates) | 4 | 847 |
| `tests/test_*.py` (33 modules, 477 tests) | 33 | 10,662 |
| `tests/regression/*.py` (the harness: 189 breaks, 168 faults and 21 controls) | 8 | 1,589 |
| `tests/browser/*.js` | 4 | 517 |
| `sql/*.sql` | 4 | 481 |
| `site/` (generated) | 18 | 2.99 MB |

## 2. How findings are rated

- **Blocking** (for v1.0): a wrong value can reach a page; a build is not reproducible; or **a check can pass for the
  wrong reason**, so a failure would go unseen. Remediated in S22, checks first, once the human approves.
- **Debt:** a real weakness that cannot put a wrong value on a page or hide a failure. It gets an owner: S22 (when
  small and in scope), a named session, v1.5 or v2 (D-201).
- **Holds:** the indicator is met; the evidence is recorded so a later audit can see a regression.

## 3. The twelve points of the roadmap

| # | Point | Evidence (measured unless stated) | Reading | Findings |
|---|---|---|---|---|
| 1 | Modularity | Import graph of `tools/` is acyclic: the four builds share `build_page.Page` (50 methods, 1,188 lines); `Insight` and `Journey` subclass it and `Brief` subclasses `Journey` (two levels); the status rules (`policy_status.py`, `facility_status.py`), the navigation (`navigate.py`) and the trace (`trace.py`) are separate modules used by the builds and the CLI; the warehouse and the search tool import no other tool | holds, with one concentrated base class | F-8 |
| 2 | Test coverage | **92.0 % of the executable lines of `tools/` run in-process during the suite** (3,473 of 3,773; `coverage.json`, a standard-library tracer; lines run in a subprocess are not counted). Per file 61.9 % (`policy_status.py`) to 96.7 %; most missed lines are the command-line `main()` bodies. One branch of the policy status rule is never run (a published date whose month contains the as-of date). Every rule ID a test module's docstring declares has a test named after it, except RC-2 to RC-7, which one test checks together | holds; one rule branch untested | F-5 |
| 3 | Regression resistance | 189 breaks (168 faults, 21 controls), all setups applying; S21.5's full run caught 158 of 158 and passed 20 of 20; 28 run in CI (D-176). **Five check modules (70 tests) were failed by no break and hold no fault case of their own** (`test_claim_model.py` 21, `test_relationship_taxonomy.py` 25, `test_entity_taxonomy.py` 12, `test_facility_status.py` 9, `test_break_selection.py` 3; `break-modules.txt`). The four browser scripts **cannot fail**: none exits with a failure status, and two compute no overall verdict | **blocking** for the browser scripts; debt for the five modules | F-1, F-5 |
| 4 | Build reproducibility | Every build is byte-identical on rebuild (`--check`, PG-7, IN-8, JR-12, BR-12); the four page builds are also up to date when run on **Python 3.12 and 3.13** (`reproducibility.txt`); no clock or environment value enters a page (the only clock reads are the search tool's request times, which belong in its log, and `navigate.py`'s command-line default, which every build overrides with the as-of date); dependencies pinned exactly. CI runs Python 3.11 (D-004); all 57 tracked `.py` files compile on 3.11, but **5 of them** (the audit-evidence scripts) are compiled by nothing in CI | holds; the 3.11 guard has a hole | F-4 |
| 5 | Dependency hygiene | 7 exact pins: 6 test-only (`jsonschema` and its 5 transitive packages, D-026) and DuckDB (D-118); `pip check` clean; `jsonschema`/`referencing` imported only by tests, `duckdb` only by `tools/warehouse.py`; one audit-evidence script imports `pypdf` (documented as scratch-only, S13). Playwright and Chromium come from the environment (D-106). CI's actions are pinned to tags (`@v4`, `@v5`), not to commit hashes; the pins carry no hashes | holds; supply-chain pinning is by name, not by hash | F-12 |
| 6 | Accessibility | Static checks on every page: lang, one h1, landmarks, no skipped heading level, table header scope, named SVGs, palette contrast (PG-8, IN-7, JR-11, BR-11). Browser QA at S22's start (Chromium 141): minimum measured text contrast 6.21 to 6.42 (AA needs 4.5); every visible link reached by Tab with a focus ring (e.g. 380/380 on the export page, 513/513 on the brief at 375 px); **no horizontal overflow at 320 px on the six pages measured** (WCAG 1.4.10 reflow); smallest HTML text 10.2 px (research view) | holds; not measured: screen readers, zoom beyond reflow, forced colours | — |
| 7 | Performance | Builds 0.09 to 0.32 s, the warehouse 2.2 s, the suite 62 s, Gate 0 0.12 s; CI 48 s on `5c492b2`; the full harness about 43 minutes (S21.5, `--jobs 4`). Pages load nothing and run no script; the heaviest is the brief, **884 KB (82 KB gzipped), 11,637 elements, 79 printed A4 pages**, then the export page, 560 KB and 7,528 elements: the evidence panels are repeated on every page that shows a record (A-4) | holds on screen; print length is debt | F-13 |
| 8 | Security basics | 18 pages: 0 `<script>`, 0 inline event handlers, 0 resources loaded from the network, every external link `rel="noopener noreferrer"`; CI permission `contents: read`, no secrets; no `shell=True`, `eval`, `exec`, `pickle` or disabled TLS verification in any tracked Python. The search tool verifies TLS (urllib's default), follows no redirect, keeps one declared identity, writes its recording only outside the repository and its log only in its folder (LS-9), and parses XML with expat 2.6.1 (protected against entity expansion since 2.4.1) | holds | F-12 |
| 9 | Complexity | 294 functions in `tools/`, median 7 lines; 11 over 50 lines, 13 with a branch count over 15. The most complex is S22's own `later_rule_search.search` (104 lines, 56 branches), then `warehouse.load` (100, 41) and `build_journeys.render_company` (83, 35). Label sets: 531 strings across the four builds (PG-1's price: every word on a page has a home); `label_text` defined once per build; three `endpoint` signatures (`Brief` dispatches on an optional argument). Duplication is low: 23 six-line windows shared by two tools, 11 of them the input lists and template parsing shared by `build_journeys.py` and `build_brief.py` | appropriate where a check needs it; accidental in the base class, the labels' layout and one new function | F-8, F-9, F-14 |
| 10 | Visual regression and rendering consistency | Nothing compares pixels (A-7). **Two screenshots of each of six pages, in fresh browser contexts, were byte-identical** (`responsive.json`): a pixel baseline is stable inside one pinned environment. Pages use system fonts, so a baseline made here would not match CI's machine | debt | F-10 |
| 11 | Responsive behaviour of major infographics | At 320, 375, 768, 1024 and 1440 px no page overflows. **The export-control timeline scales to 0.29 at 320 px and 0.34 at 375 px: its labels render at 3.6 and 4.3 px**; it is legible from 768 px (9.2 px). The HBM figure renders its smallest label at 8.8 px at 320 px and 10.5 px at 375 px. Every timeline event is also listed in words beside the figure (`ol.timeline-words`, the SVG's description) | debt: the information reaches a phone, the graphic does not | F-6 |
| 12 | Chart and data binding correctness | Every text node of every page is a record value, a label, a derived value or marked framing, and every record value equals its home (PG-1, PG-2, IN-1, IN-2, JR-1, JR-2, BR-1, BR-2); derived values are recomputed (PG-2, IN-3, JR-3, BR-3); SQL cells equal their committed results (PG-11, IN-10). The only position-encoded visual, the timeline, is checked mark by mark against its declared scale (JR-5); the chain figure, the matrix and the unit squares are checked as structure (PG-5, JR-4, IN-4). The HBM page's journey specification names seven record IDs; resolving the recorded gap `cand-001` stops the HBM page and the brief with a named refusal (measured on a scratch copy); an out-of-vocabulary value crashes three builds with an unnamed `StopIteration` (measured) | holds for binding; two robustness gaps | F-2, F-3 |

## 4. PEF §9 indicators

| Indicator | Evidence | Reading |
|---|---|---|
| **Process:** commit coherence, change boundaries | 197 commits, 40 merged pull requests (one or more per session), 0 reverts; median 6 files per non-merge commit; one commit over 50 files (a page rebuild) | holds |
| regression testing before and after risky changes | checks written first and shown failing in every session since S03; a break for every new check; the full harness at each audit and on every check change (D-150, D-177) | holds |
| documented refactors | the harness rewrite (D-178, D-179: identical verdicts for 130 breaks); the templates' composition rule (D-204); D-188 | holds |
| dependency hygiene | every dependency has a decision (D-003, D-026, D-106, D-118) | holds |
| rollback and recovery | no revert was needed; CI went red three times in M6 (S20: f-strings only Python 3.12 parses; S21.5: a decision appended after the pages were rebuilt) and each was fixed forward in the same session; worker restarts were recovered from pushed commits | holds, with a recurring lesson (F-4, F-7) |
| decisions recorded | 211 decision records; each S22 change cites one | holds |
| **Outcome:** modularity; low accidental duplication; separation of data, logic and presentation | §3 points 1 and 9; text binding checked node by node; the HBM page's specification holds record IDs (F-3) | holds, with F-3 and F-8 |
| typing and validation | JSON Schemas for every record kind; type hints on the builds; the warehouse refuses unknown keys | holds |
| automated tests for critical paths | 92 % in-process line coverage of `tools/`; 168 planted faults | holds, with F-5 |
| accessible UI; acceptable performance; basic security; reproducible build | §3 points 6, 7, 8, 4 | holds; F-1 blocks the browser half |

## 5. Findings

### F-1 — The browser checks cannot fail (blocking)

- **Evidence.** `tests/browser/*.js` (measured at the start of S22): all four end with exit status 0 whatever they find;
  `journeys.qa.js` and `brief.qa.js` compute an `allOk` but only print it; `hbm-chain.qa.js` and `hbm-insight.qa.js`
  compute no overall verdict at all. A session reads the JSON to know whether they passed.
- **What it means.** The checks behind Gate 7 (overflow, keyboard path, contrast, console errors, print layout) pass for
  the wrong reason whenever nobody reads their output, and cannot run in CI as they are (H-0 chose CI).
- **Proposed disposition.** Remediate in S22, checks first: every script computes one verdict from all its measures
  and exits non-zero on any failure; each is shown failing on a planted page defect; then the CI job of H-0.

### F-2 — An out-of-vocabulary value crashes three builds without a reason (debt; E-2)

- **Evidence.** On a scratch copy, a citation `standing` outside its vocabulary makes `build_page.py`,
  `build_journeys.py` and `build_brief.py` stop with a bare `StopIteration` in `Page.value` (`next(...)` over the
  schema's `oneOf`). The record checks refuse the value first, so no wrong value reaches a page.
- **Proposed disposition.** Remediate in S22: `Page.value` raises a `BuildError` naming the record, the field and the
  value; one test written first.

### F-3 — The HBM page's specification names records, so the most plausible evidence change stops two builds (debt; E-1)

- **Evidence.** `build_page.py`'s journey specification holds seven record IDs (`walk_root`, `lane_edges`,
  `drawn_gaps` with `cand-001`, `candidates`). With `cand-001` resolved (removed on a scratch copy), the HBM page and the
  brief stop with "refused candidate cand-001 is not canonical"; the research view and the journeys build (measured).
  `sql_section` reads the committed result from the repository, not from the `data` argument (M4's "fixed path").
- **What it means.** The stop is named and safe; it is a specification a person must update with the evidence, which
  PG-10 already requires to have homes.
- **Proposed disposition.** Keep, owned by the session that resolves `cand-001` (it edits the specification with the
  record); S23 is told, since the H100's fabrication evidence is a content question.

### F-4 — Python 3.11 is guarded only for the files the suite loads (debt; A-1)

- **Evidence.** CI runs 3.11 (D-004); the four page builds pass `--check` on 3.12 and 3.13 too, so a local run on a
  newer interpreter cannot see 3.12-only syntax (S20's red CI). 57 tracked `.py` files compile on 3.11, but 5 (the
  audit-evidence scripts) are compiled by nothing in CI.
- **Proposed disposition.** Remediate in S22: a test compiles every tracked `.py` file with the running interpreter,
  so CI's 3.11 compiles all of them; `README.md` names the 3.11 virtualenv as the local command.

### F-5 — Five check modules have never been shown to fail (debt)

- **Evidence.** `break-modules.txt`: no break of S21.5's full run failed `test_claim_model.py` (21 tests),
  `test_relationship_taxonomy.py` (25), `test_entity_taxonomy.py` (12), `test_facility_status.py` (9) or
  `test_break_selection.py` (3), and none of them plants a fault of its own. They check that documents, vocabularies
  and the status rule agree. One branch of `policy_status.derive_status` is never run (coverage).
- **Proposed disposition.** S22 adds one break per module (five breaks, each failing for its named reason) and a
  fictional test of the untested status branch; no check changes.

### F-6 — The export-control timeline is illegible on a phone (debt)

- **Evidence.** `responsive.json`: labels at 3.6 px (320 px) and 4.3 px (375 px); legible from 768 px. The events are
  also in a list beside the figure. The HBM figure's smallest label is 8.8 px at 320 px.
- **Proposed disposition.** v1.5 (responsive infographics are its subject, D-201); until then the word list is the
  phone form. Alternative: a CSS-only change in S22 that keeps the figure at a readable width inside a horizontal
  scroller below 760 px (the template's style, Editorial; the browser scripts' overflow rule would need to accept the
  scroller).

### F-7 — The pre-commit sequence is seven commands (debt; S21.5's red CI)

- **Evidence.** The suite, Gate 0 and five `--check` commands; S21.5 committed after an edit to `decisions.md`, an
  input of every page, and CI went red. MA §15 asks for a documented `validate` equivalent.
- **Proposed disposition.** S22 adds `tools/check_all.py` (standard library): runs the suite, Gate 0 and every
  `--check` in order and exits non-zero on the first failure; `README.md` names it as the command run immediately
  before each commit. Alternative: keep the commands and the lesson as they are.

### F-8 — One large base class, two levels of subclassing and the label lists (debt; A-2)

- **Evidence.** `Page`: 50 methods in 1,188 lines; `Brief` → `Journey` → `Page`; 531 label strings; three `endpoint`
  signatures. Subclassing let S21 reuse the figure, panels and matrix with no change to older pages (S21 report).
- **What it means.** The complexity is paid for by reuse and by PG-1, but the base class mixes record access,
  rendering and composition, and the next page kind will deepen it.
- **Proposed disposition.** v1.5, which plans reusable visual components (D-201); no refactor before v1.0 (non-goal).

### F-9 — Two templates still compose differently (debt; A-3)

- **Evidence.** D-204 covers new templates; `page_template.html` and `insight_template.html` keep their own
  mechanism; the journeys and brief builds each carry the same template parsing and input lists (11 shared windows).
- **Proposed disposition.** v1.5, with F-8.

### F-10 — No visual regression check (debt; A-7)

- **Evidence.** Byte-identical screenshots inside one environment; system fonts make baselines machine-bound.
- **Proposed disposition.** v1.5: its opening session decides browser rules (D-201); a baseline made and compared in
  the CI job of H-0 is feasible on this evidence.

### F-11 — The research view's filter has never run in Firefox or Safari (debt; D-196, D-200)

- **Evidence.** Only Chromium is installed in the session environment; the filter relies on `:has()` with a CSS guard.
- **Proposed disposition.** The CI job of H-0 also installs Playwright's Firefox and WebKit (pinned with Playwright)
  and runs the research view's filter checks in them; the result is reported from CI. Alternative: v1.5.

### F-12 — Supply-chain pins are by name (debt, low)

- **Evidence.** `actions/checkout@v4`, `actions/setup-python@v5`; exact pip pins without hashes.
- **Proposed disposition.** Pin the actions to commit hashes in S22, since H-0 changes the workflow; pip hashes kept as
  they are (exact pins and a clean `pip check` suffice at this scale).

### F-13 — The brief prints 79 A4 pages (debt; A-4)

- **Evidence.** 884 KB and 11,637 elements; 66 of the printed pages are evidence appendices.
- **Proposed disposition.** D-210's compact printed evidence list (S22, H-0); the screen weight, a single home per
  claim's evidence, stays with a later UX session (v1.5).

### F-14 — The search tool's main function is the most complex in `tools/` (debt; S22's own code)

- **Evidence.** `later_rule_search.search`: 104 lines, 56 branches.
- **Proposed disposition.** S22 splits it into one function per step, with no change of behaviour (LS-1 to LS-11 and
  breaks S22-3 to S22-10 guard it).

## 6. The debt S22 owns, ruled

| Item | Proposed disposition | Finding |
|---|---|---|
| A-1, Python 3.11 syntax | remediate in S22 | F-4 |
| A-2, labels, subclassing, `endpoint` signatures | v1.5 | F-8 |
| A-3, the two older templates | v1.5 | F-9 |
| A-6, browser checks outside CI | remediated in S22 (H-0), after F-1 | F-1 |
| A-7, visual regression | v1.5 | F-10 |
| Cross-browser `:has()` filter | S22's CI job, or v1.5 | F-11 |
| E-1, a resolved gap stops two builds | kept; the session that resolves `cand-001` | F-3 |
| E-2, unnamed `StopIteration` | remediate in S22 | F-2 |
| C-8, two access dates for `src-043` | S23: which access date is canonical is a data question (no data changes in S22) | — |
| F-4 (agent audit), the Verifier's re-read is a private script | kept, owned by the next session that adds claims from a retrieval (the EAR's 1996 dates, D-210); a re-read tool needs PDF text, so that session's opening decides how (a pinned `pypdf`, or `pdftotext`) | — |
| M5 §6, a rule's country joins two texts; an official text's publisher is an edition's name | S23 (content and data, not code) | — |
| `not_researched`'s definition against ER-3's use; the ID rule's legal-form list lacks "Co., Ltd." | S23, as vocabulary wording; any schema change needs its own decision | — |
| Dark mode | v1.5 (it doubles the contrast surface; D-201) | — |
| D-210's search tool | **done** (D-211) | — |
| D-210's two page items | S22 (H-0) | F-13 |

## 7. Maturity (PEF §3): code and engineering

| Axis | Rating | Evidence |
|---|---|---|
| Process | **3, Controlled** | checks first and breaks every session; full harness on every check change; decisions for every dependency; CI red three times in M6, each fixed forward, two from the same lesson (run CI's checks, on CI's Python, immediately before committing) |
| Outcome | **2, Defined at this audit; 3, Controlled once F-1 and F-2 are remediated** | 92 % line coverage, 168 planted faults, builds identical across three interpreters, text binding checked node by node, clean security basics; but the browser checks could not fail (F-1) and a vocabulary error still crashes without a reason (F-2) |

## 8. What this audit does not cover

Research depth and content (S23); the portfolio and capability audit (S24); screen readers, forced colours and zoom
beyond 320 px reflow; browsers other than Chromium (F-11); performance on a slow network (the pages load nothing, but
their size was not timed on a device).
