# SESSION-11 Report — First end-to-end vertical slice

- **Session:** S11 · **Type:** IMPLEMENTATION · **Milestone:** M3 — Vertical Slice + Audit (first session)
- **Date:** 2026-10-02
- **Prompt:** [`sessions/prompts/S11-PROMPT.md`](../prompts/S11-PROMPT.md) (Part A confirmed by the human;
  Part B SPEC §2 detail; H-1 to H-5 answered before the session). The uploaded copy and the copy on
  `main` are byte-identical (sha256 `2c2f7af6…`). Its first heading reads "S10 Session Prompt"; the
  content is S11's. The prompt is immutable (D-011), so the slip is recorded here and not corrected.
- **Branch:** `claude/new-session-djql6o`, created from `main` @ `7433d98` (the PR #18 merge, which
  carries the S11 prompt).
- **Base** (D-018 L-03), at the start of the session:
  - `git branch -a`: `claude/new-session-djql6o` and `main`, with their remotes; both at `7433d98`.
  - `git ls-remote`: `main` and `HEAD` at `7433d98`; `claude/new-session-15s0bd` at `c51cb60` (merged);
    `claude/vigilant-keller-320pbb` at `269a1fa`, `claude/new-session-mdyi2x` at `6f926b0`,
    `claude/s08-concept-dataset` at `41806c5`, `claude/s07-company-dataset` at `a5032ef` (all merged);
    the six older `claude/*` branches at `26acdf9`, `ace06f0`, `ce5b881`, `d9d0a83`, `11185a6` and
    `e23965c`, as S10 listed them. The session branch existed on the remote at `7433d98`.

## Mission outcome

**Delivered: one journey, from source sentence to an editorial visual, generated and checked.**
The page [`site/hbm-chain/index.html`](../../site/hbm-chain/index.html) answers *"What does an AI
accelerator's memory depend on, and who is known to make it?"* from the five canonical edges:

- NVIDIA H100 and AWS Trainium2 each `incorporates` High Bandwidth Memory (stated: `FACT`s from
  each maker's own page); HBM `requires` 3D die stacking (inferred: a `DERIVATION`, D-091);
- who makes the memory: **not researched** for both, drawn as a named gap on each arrow (D-094);
- Amazon `designs` Trainium2 (stated); TSMC → H100 `fabricates` drawn as a recorded gap, with no
  arrowhead, opening the canonical `claim-tsmc-fabricates-h100` (D-092);
- in a separate lane, "not linked to any accelerator on this chain": SK hynix `operates` M16
  (inferred, D-099) and Micron's HBM4 36GB 12H, recorded as a kind of HBM by an entity field.

Every mark opens its evidence panel: the record, each claim (type, status, statement), each
citation (the quoted anchor, source, locator, class, standing, stated dates, access time, the
Verifier's read) and, for an inference, its reasoning and inputs.

**The five impossibilities of Part B §02, and what enforces each:**

| Must be impossible | Enforced by |
|---|---|
| a mark, label or sentence with no record behind it | PG-1 (every text node has a home), PG-2 (every value equals its home), PG-3 (every mark targets a canonical record) |
| presentation data typed by hand; a rebuild that differs | PG-2, PG-7 (committed page = rebuild; two builds identical); the build stamps an input digest |
| a gap drawn as absence or zero | PG-5 (every unknown supplier and recorded gap drawn with its state; never "none"; never "0") |
| a staging record shown as canonical | PG-3; the build refuses (`BuildRefusalTests`) |
| an inference without its label | PG-4 (dashed, "inferred", reasoning in the panel) |

| Deliverable | Where | Status |
|---|---|---|
| Design document with the visual specification | `docs/architecture/vertical-slice.md` | proposed (D-100 to D-108) |
| Structured walk and trace (H-4) | `tools/navigate.py`, `tools/trace.py` (`--json`; `navigate_data`, `trace_data`) | tested; text output unchanged |
| Build step and template (H-2) | `tools/build_page.py`, `tools/page_template.html` | tested |
| The page | `site/hbm-chain/index.html` (278,342 bytes, self-contained) | generated |
| Page checks (`validate-design`) | `tests/test_page.py`: PG-1 to PG-10, build refusals | in CI |
| Editorial and QA contracts (H-5) | `docs/agents/contracts.md`, `roles.md` | proposed (D-107) |
| Browser QA (H-3) | [`SESSION-11-qa/`](./SESSION-11-qa/): script, results, screenshots | run, outside CI |

**Restated contract** (at the start of the session):

- **Mission:** one journey, H100 and Trainium2 → HBM → 3D die stacking, generated from `data/` by a
  tested standard-library build; every mark opens its evidence; every unknown drawn as a named gap.
- **Non-goals:** Part B §08: no new sources, claims, edges or records; no metric, share, rank,
  score, "critical" or "concentrated"; no framework, library, DuckDB or deployment; no second
  journey or component system; no edit to schemas, taxonomies or root documents.
- **Plan:** inspect; ask the stop-condition rulings; design document and decisions; structured
  outputs; page checks before the page (fail first); build and page; breaks; browser QA;
  contracts and state rows; checkpoint; the human's new-user test; fixes; report. The plan held.

**Rulings the human took at the start of the session** (verbatim):

| Question | Answer (verbatim) | Effect |
|---|---|---|
| H-1 names "SK hynix's M16", but no record links SK hynix or M16 to HBM or to either accelerator | "Separate lane (Recommended)" | D-100, D-104 |
| Micron's HBM4 36GB 12H, the only named HBM product (`instance_of` HBM, an entity field) | "Yes, not-connected lane (Recommended)" | D-100, D-104 |
| "The data commit it was built from" cannot be stamped on a page committed with its data | "Input digest (Recommended)" | D-102 |
| `tests/test_agent_contracts.py` (hard-codes the active roles) and a new `tests/test_page.py` | "Yes, both (Recommended)" | D-107 |

## The human's new-user test (Part A)

The page was sent to the human after the checkpoint (`3917a14`), with four steps: answer the
question from the page alone; follow one mark to its source sentence and source; try to break the
chain; note every unclear term. The human's messages, verbatim:

1. "Gimme suggestions"
2. "I agree, follow the principle of “not overreachment”"

Between the two, Claude proposed seven changes. The human agreed to all seven, under the
principle of not overreaching:

| # | Proposal (Claude's, agreed by the human) | Blocking? | Done |
|---|---|---|---|
| 1 | The "why not" cells quote rule codes (§5, F-1, ER-9, D-073) as if a reader knew them: list each code with its home | yes | "Rules cited above": ER-2, ER-9, F-1, D-073, D-092, each with its one-line home; section marks get one framing sentence, not a guessed definition |
| 2 | The TSMC gap reads "fabricates · inferred · gap: no edge": say what it is | yes | "recorded gap: a claim the Atlas holds, not an edge", in the legend, the words and the gaps list |
| 3 | The short answer has no answer sentence | yes | one sentence composed from the records, checked like every value |
| 4 | Company panels carry every identity claim | no | legal name, incorporation, headquarters and location claims in a closed disclosure |
| 5 | Claim cards lead with the ID | no | type, status and statement first; a citation leads with its quoted anchor |
| 6 | "maker of this part", "an entity field, not an edge" are the Atlas's coinages | no | "supplier (who makes this part)"; "recorded as a kind of … a property of its record, not a supply link" |
| 7 | No way to jump through a long page | no | a "Jump to" bar |

**What "not overreaching" left out** (D-108): no plain-language rewrite of the design record's
reasons (they stay quoted, one home); no definition for a bare section mark; no further cut of the
evidence panels. Proposal 4 shortened the page by 6 % on desktop (23,896 → 22,547 px) and 8 % at
375 px (47,313 → 43,346 px), not "about half" as Claude estimated: the evidence section is
14,263 px because each of 15 panels shows its full citations, which "every mark opens its evidence"
requires.

**Acceptance criterion 8 is met in part.** The human reviewed the page and decided on every
proposed change, but the findings are Claude's proposals, agreed, not the human's own walk-through
recorded step by step. No independent new-user observation exists yet.

## Visual QA (the roadmap's four questions)

| Question | Answer | Evidence |
|---|---|---|
| **Truth:** does it faithfully encode the data? | Yes, as far as checks can see. Every mark, label and date equals its record (PG-1, PG-2); line style follows claim type (PG-4); gaps carry their state (PG-5); nothing encodes a magnitude, a confidence or time | 18 breaks caught (below); the capacities stay quoted text and are not compared |
| **Clarity:** is the relationship understood quickly? | The chain reads top to bottom in four rows; "stated", "inferred" and the gap pills are written, not colour-only. Weak point: the panels are long and the quoted reasons dense | `SESSION-11-qa/desktop-02-chain.png`, `mobile-02-chain.png`; the new-user proposals 1–3 |
| **Context:** are dates, scope, uncertainty and provenance visible? | Each edge shows its period or "no period in the claims"; each claim its `verified_on`; each source its stated dates and access time; the method section gives the ranges and the input digest; five rulings listed as limitations | `mobile-04-panel-after-enter.png`; PG-2 completeness checks |
| **Presentation:** polished, consistent, usable across sizes? | One palette, one type scale, no overflow at 375 px, smallest diagram text 10.5 px at 375 px; no organisation's branding | `qa-result.json`; `desktop-03-gaps.png` |

## Browser QA (H-3)

Scratch run: Playwright 1.56.1 with the pre-installed Chromium 141.0.7390.37, from the environment,
not the repository (D-106). Page input digest `2ca03de11036af6d34f633135f20376364455bc20e1c18b3e24d47ba65f4cdfc`.
Script and full results: [`SESSION-11-qa/qa.js`](./SESSION-11-qa/qa.js),
[`qa-result.json`](./SESSION-11-qa/qa-result.json) (the script reads the page at this session's
checkout path).

| Check | 1280 px | 375 px |
|---|---|---|
| Console messages, page errors | none | none |
| Network requests | the page file only | the page file only |
| Horizontal overflow (`scrollWidth` / `clientWidth`) | 1280 / 1280 | 375 / 375 |
| Diagram scale; smallest diagram text | 1.31; 14.4 px | 0.95; 10.5 px |
| First Tab stop | the skip link to the evidence | same |
| Marks reached by Tab | 17 of 17 (30 Tab presses) | 17 of 17 |
| Enter on each mark: hash, panel in view, `:target` highlight | 17 of 17 | 17 of 17 |
| Disclosure ("inputs to this inference") opens by keyboard | yes | yes |
| Contrast measured on every rendered text node | 2,946 nodes; minimum 6.21:1 ("class" on the class tint); none below 4.5:1 | same |

**Screenshots:** [`desktop-02-chain.png`](./SESSION-11-qa/desktop-02-chain.png) (the diagram,
legend and text equivalent), [`mobile-02-chain.png`](./SESSION-11-qa/mobile-02-chain.png) (the
diagram at 375 px), [`desktop-03-gaps.png`](./SESSION-11-qa/desktop-03-gaps.png) (what the Atlas
does not know, with the rules cited), [`mobile-04-panel-after-enter.png`](./SESSION-11-qa/mobile-04-panel-after-enter.png)
(the `requires` panel after Enter on its mark, at 375 px).

**Fixed during QA** (each found in a screenshot or a measurement): edge labels clipped at the right
edge (now centred on their line with a halo); Micron's product name overflowing its box (now wrapped
inside one record value); legend swatches drawn black and solid (CSS scoped to the diagram only);
smallest diagram text 9.5 px at 375 px (raised to 10.5 px); a double rule under the title.

## Files changed

| File | Change |
|---|---|
| `docs/architecture/vertical-slice.md` | new: the answers to Part B §06, the visual specification, the checks |
| `docs/architecture/decisions.md` | D-100 to D-108 appended, `proposed` |
| `tools/navigate.py` | answers computed as data (`entry`, `depends_on_tree`, `supplier_rows`, `actors_list`, `edges_at`, `navigate_data`), text rendered from them; `--json` |
| `tools/trace.py` | `Collector` and `trace_data`: the trace as data; `--json` |
| `tools/build_page.py` | new: the build step (journey specification, labels, palette, resolver, diagram, panels, refusals, `--check`) |
| `tools/page_template.html` | new: the framing and the style (the Editorial's file) |
| `site/hbm-chain/index.html` | new, generated |
| `tests/test_page.py` | new: PG-1 to PG-10 and two build refusals |
| `tests/test_navigate.py`, `tests/test_trace.py` | structured-output tests (the data and the text name the same edges, claims, sources and missing references) |
| `tests/test_agent_contracts.py` | the expected active set gains Editorial and QA (the human's ruling) |
| `docs/agents/contracts.md`, `docs/agents/roles.md` | Editorial and QA contracts (`proposed`); path updates for the Knowledge Architect and the Data Auditor |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows; Gate 6, Gate 7, `validate-design`, `qa-browser` |
| `sessions/reports/SESSION-11-REPORT.md`, `sessions/reports/SESSION-11-qa/` | this report; browser QA script, results and screenshots |

## Data changed

**None.** No source, claim, entity, event or relationship record was created, edited or moved; no
schema changed. As measured at the final commit: 52 source records; 120 canonical claims; 8
companies, 4 jurisdictions, 9 technologies, 7 components, 3 products, 2 facilities, 4 events; 5
relationships; staging empty.

## Tests run

Python 3.11.15. "Fresh venv" means a virtualenv built from `requirements-test.txt` in the session
scratchpad.

| Command / check | Result |
|---|---|
| **At start**, fresh venv; `pip freeze` sorted vs the pins | installed set = pinned set; OK (264 tests); `tools/validate_repo.py`: `Repository integrity: OK` |
| `navigate.py` and `trace.py` text output, every command on every real ID, before and after the refactor (9,906 lines) | byte-identical |
| **Fail-first:** the suite with `tests/test_page.py` written and no build step or page | 289 tests, 18 failures, every one "the page is not built: site/hbm-chain/index.html"; the 271 others passed |
| Suite at the checkpoint (`3917a14`) | OK (291) |
| **Deliberate breaks**, final page (18 breaks, 2 controls) | 18 caught, each for the reason it names; both controls pass. Output below |
| `python -m unittest discover -s tests`, final, fresh venv | OK (291 tests: 264 before, 27 new) |
| `python -m unittest discover -s tests -p "test_page.py"` (`validate-design`) | OK (20) |
| `python tools/build_page.py --check`, final | `page: up to date` |
| `python tools/validate_repo.py`, final | `Repository integrity: OK` |
| Browser QA (above) | clean at 1280 px and 375 px |
| CI | observed on the checkpoint `3917a14` (run 91): success. Not observed at the commit that adds this report (L-08) |

**What the checks cannot see.** Whether the framing reads well, whether a new user understands
the encoding, whether a quoted reason is right. A sentence composed from records can be grammatical
and still mislead if the records change shape; the build then omits it rather than guess (D-108),
but only for the two conditions it tests. The human's reading is the guard.

## Evidence added/retired

**None.** No source was retrieved or registered; no anchor was re-read (no source's bytes changed in
S11, so the Verifier had nothing to re-check). The page shows the evidence as recorded, including
the Verifier's reads from S07 to S10. External research: none (Part B §05).

## Decisions made

All appended to `decisions.md` as `proposed`, for the human's review.

| Decision | Subject |
|---|---|
| D-100 | the journey and its scope; M16 and Micron's HBM4 in a separate lane (H-1; the human's rulings) |
| D-101 | structured output for the walk and the trace (H-4) |
| D-102 | the build step, one self-contained file, and the input digest instead of a commit (H-2; the human's ruling) |
| D-103 | the visual form and its encoding |
| D-104 | gap encoding and the lane; the build refuses a linked lane |
| D-105 | the text provenance rule; `validate-design` = `tests/test_page.py` |
| D-106 | browser QA in a scratch environment (H-3) |
| D-107 | Editorial and QA contracts (H-5; the human's ruling on the two test files) |
| D-108 | the seven changes from the new-user test ("I agree, follow the principle of “not overreachment”") |

**Rejected alternatives** (in each decision and `vertical-slice.md` §10). The main ones:

- **Visual form:** a table as the primary visual (kept as the text equivalent); a force-directed
  network (position would carry no meaning, and the rebuild would not be stable).
- **Gap encoding:** omitting unknowns; a placeholder "unknown supplier" node (RR-7); M16 drawn next
  to HBM (would imply supply).
- **Build:** a page reading JSON at run time; a charting library; JavaScript; a commit stamp; a
  separate stylesheet.
- **Browser checks:** Playwright pinned and run in CI (H-3's alternative).
- **New-user changes:** rewriting the quoted reasons in plain words (a second home); collapsing
  claim cards (evidence two clicks away).

## Deviations

1. **No data commit on the page** (Part B §11). The page carries a SHA-256 over its 33 input files;
   the commit is recorded here. The human's ruling ("Input digest (Recommended)"), D-102.
2. **Files outside the prompt's lists:** `tests/test_agent_contracts.py` and `tests/test_page.py`,
   asked before the build ("Yes, both (Recommended)"). The Knowledge Architect's and Data Auditor's
   contract rows gained paths (`vertical-slice.md`; the page and `tests/test_page.py`), as S07 to S10
   updated paths. `sessions/reports/SESSION-11-qa/` holds the QA record (the QA role's write).
3. **The new-user findings are proposals the human agreed to,** not the human's own walk-through
   (above). Criterion 8 is met in part.
4. **The build reads three more documents** (`source-policy.md`, `relationship-taxonomy.md`,
   `company-dataset.md`) for the rule homes added by D-108, so they are inputs: a change to any of
   them requires a rebuild.
5. **The page-length estimate was wrong** (6–8 % shorter, not half).
6. **Screenshots are of sections,** not whole pages: the page is 22,547 px tall on desktop.

**Invalidated assumptions.**

- S10's handoff named three navigation outputs for the page (`depends-on`, `suppliers`, the
  trace). The journey also needed `actors` (Amazon) and a walk over `instance_of` (Micron's HBM4),
  which no navigation command answers; the build reads the field directly.
- H-1 listed "SK hynix's M16" as part of the HBM chain. No record links it to HBM; it became a lane.

## Debt introduced/resolved

**Introduced:**

- **The page is stale whenever an input changes.** Any new decision, claim or edit to the rule homes
  makes PG-7 fail until `python tools/build_page.py` is run. Every later session that appends a
  decision must rebuild the page.
- **The journey specification is hand-chosen** (the walk root, the lane edge, the drawn gap's row,
  three text rows, five rulings): IDs only, checked by PG-10, but a selection.
- **The layout is fixed** for one or two products, one actor or gap per product, one lane edge and one
  lane product; the build refuses anything else.
- **The quoted reasons stay dense** and bare section marks stay undefined (D-108).
- **`LABELS` is a fixed vocabulary** in the build; a second page will grow it.
- **Browser QA is outside CI;** its script reads the page at a local path.
- **The test re-implements the input list and the digest** on purpose (a spec check), so a new input
  needs both changed.

**Resolved:**

- S10: "The navigation tool prints text only; S11 will need a structured output for a page" (D-101).
- Baseline Gate 6, `validate-design` and `qa-browser`: from "not applicable" or "not built" to
  partial (D-105, D-106).
- `roles.md`: Editorial and QA have contracts (D-107).

## Unresolved issues

- **Human decision required: keep the rules S11 used to build the page** (`CLAUDE.md` §9A; asked
  as H-0 at the start of S12).
  - *What we are deciding:* whether S11's design rules become accepted project rules.
  - *What will concretely change:* if accepted, these records change from "proposed" to "accepted";
    no data, code or page content changes. What each rule fixes:
    - the page answers one question, about the memory of the H100 and Trainium2, and shows SK
      hynix's M16 plant and Micron's HBM4 apart, as not linked (D-100);
    - `tools/navigate.py` and `tools/trace.py` can print their answers as data, which the page build
      reads; their text output is unchanged (D-101);
    - the page is one generated file with no script; it states a fingerprint of its inputs instead of
      a commit, so any change to an input means rebuilding it, and CI fails until then (D-102);
    - the diagram's encoding: boxes for records, solid lines for stated relations, dashed for inferred
      ones, amber pills for unknowns; nothing encodes a quantity (D-103);
    - unknown suppliers and the TSMC gap are drawn and named, and the build refuses to draw the side
      lane if any record links it to the accelerators (D-104);
    - every word on the page comes from a record, a fixed label, a computed value or a marked framing
      box, enforced by `tests/test_page.py` in CI (D-105);
    - browser checks run by hand outside the repository, with results in the report, not in CI (D-106);
    - two new agent roles with written limits: Editorial writes only the page's framing and style and
      documentation status rows; QA writes only browser findings (D-107);
    - the seven readability changes from the new-user review (D-108).
  - *Why:* S12 audits against these rules; they should not be proposals while being audited.
  - *Options:* **A — Accept all (recommended)**; **B — Accept with named changes** (made before the
    audit); **C — Reject named rules** (what was built on them is removed or rebuilt first).
  - *Decision requested:* "Choose A, B or C", naming the rules for B or C.
  - *Technical reference:* D-100 to D-108; `vertical-slice.md`; `contracts.md`, `roles.md`.
- **Not asked now:** public deployment (NG-13). It needs this slice to pass its gates first; the page
  stays unpublished until the human decides.
- **Inherited, unchanged:** TSMC → H100 `fabricates` (D-092); the HBM supplier of each product
  (`not_researched`, D-094); the AWS legal entity (D-093); `supplies` items with no record; subsidiary
  records (D-095); TSMC's 20-F; S01's weekly gate; S05 debt.

## Process lessons

- **Ask for the new-user walk-through before offering suggestions.** Asked for suggestions, the human
  agreed to Claude's; the result is a reviewed page, not an independent new-user test. Next time,
  send the four steps first and the suggestions only after the human's own notes.
- **Checks written first catch the builder too.** PG-5 failed on Claude's own framing ("it never
  means that none exists"), and PG-1 on "SHA-256" in a label.
- **Measure before estimating.** The "about half" figure for the panel change was a guess; the
  measured gain was 6–8 %.
- **Record values can be split for layout without losing their home.** Micron's name wraps across two
  `tspan`s inside one `data-ref` element, and PG-2 still compares the whole name.
- **Write multi-line edit scripts to a file.** One heredoc with nested quotes failed before any edit
  applied; scripts with an assertion per replacement did not.

## Implications for the next session

S12 — Data architecture audit ("Do not build new features during this session unless needed for
remediation"):

- **Completed work:** the journey, the page, its checks (PG-1 to PG-10, 18 breaks), the structured
  outputs, the Editorial and QA contracts.
- **What the page revealed about the data model:**
  - **IDs:** stable and rule-made; edge IDs are long (up to 84 characters) and wrap in every panel.
  - **Relationship semantics:** "who makes HBM?" has no edge path. SK hynix's role claim names DRAM,
    NAND and MCP; Micron's HBM4 reaches HBM only through `instance_of`, and its maker only through
    `vendor`. The question's second half is answered by entity fields, not edges.
  - **Temporal correctness:** no edge has a period; every instance edge shows "no period in the
    claims". The page cannot say *when* any relation held.
  - **Provenance completeness:** every mark traces to sources; no missing reference in any trace.
  - **Queryability:** `navigate.py` needed data output (done), and still has no question for
    "instances of a class and their vendors".
  - **Derived or duplicated?** Every value is derived from canonical records or quoted from a
    document (PG-1, PG-2, PG-7). But the page reads two Markdown documents as data:
    `edge-dataset.md` §1 (the refused candidates) and the rule tables. A Markdown table is now a data
    source with a parser in two places (the build and the test).
- **Open issues:** everything §04 of the prompt inherits; the new-user test as an independent walk
  through.
- **Recommended next decision:** S12's first audit question: *should the refused candidates of
  `edge-dataset.md` §1, which the page now reads as data, become records with their own home and
  checks, or stay design text the page quotes?*
- **Files for S12 to read first:** this report; `docs/architecture/vertical-slice.md`;
  `docs/architecture/edge-dataset.md`; the S10 report's list of what M3's audits should examine
  first; `tools/build_page.py` (the journey specification and the resolver).

**Next recommended milestone:** S12 — the data architecture audit, starting from the question above.

**S11 gate** ("The journey is usable by a person who did not build the dataset"): **met in part.**
The page answers its question without other documents, every mark opens its evidence, and the
checks and browser QA pass. The person who used it did not build the dataset, but recorded no
independent findings, so usability by such a person is shown by review, not yet by observation.

## Fail-first output

The suite with `tests/test_page.py` written and no build step or page (sorted, de-duplicated):

```
      1 FAIL: test_pg10_the_journey_specification_has_homes
      1 FAIL: test_pg1_every_text_node_has_a_home
      1 FAIL: test_pg1_labels_carry_no_fact
      1 FAIL: test_pg2_claims_and_sources_are_shown_whole
      1 FAIL: test_pg2_derived_values
      1 FAIL: test_pg2_every_instance_edge_shows_its_period
      1 FAIL: test_pg2_every_record_value_equals_its_home
      1 FAIL: test_pg3_marks_target_canonical_records_and_open_their_panel
      1 FAIL: test_pg3_no_staging_record_and_every_id_canonical
      1 FAIL: test_pg4_inference_is_labelled_and_reasoned
      1 FAIL: test_pg5_the_chain_and_its_gaps_are_drawn
      1 FAIL: test_pg5_the_lane_is_not_linked
      1 FAIL: test_pg6_framing_is_marked_and_names_no_record
      1 FAIL: test_pg7_rebuild_is_byte_identical
      1 FAIL: test_pg8_document_structure
      1 FAIL: test_pg8_style_palette_and_contrast
      1 FAIL: test_pg8_the_diagram_has_a_text_equivalent_and_keyboard_marks
      1 FAIL: test_pg9_links_resolve_and_nothing_loads
     18 AssertionError: the page is not built: site/hbm-chain/index.html (python tools/build_page.py)
Ran 289 tests; FAILED (failures=18)
```

The first build then failed 12 checks, each for a real fault: decision IDs the test resolver did not
read, "SHA-256" in a label (a digit), "none" in Claude's framing, the lane's edge missing from the text
equivalent, and claim-card IDs read as panels. Each was fixed in the build, the template or the
resolver, never by loosening a check.

## Deliberate breaks, final run

Each break edits a scratch copy of the repository and lists the tests that fail (with the assertion
that names the reason). PG-7 also fails whenever the committed page is edited by hand.

| # | Break | Caught by (besides PG-7) | Reason given |
|---|---|---|---|
| 1 | a mark with no record behind it | PG-3 | `'company-example-nothing' not found` |
| 2 | a hand-edited label (NVIDIA H100 → H200) | PG-2 | `'NVIDIA H200' != 'NVIDIA H100'` |
| 3 | a supplier gap removed from the diagram | PG-5 | `('supplier-gap', 'rel-product-nvidia-…') not found` |
| 4 | a supplier gap drawn as zero | PG-2 | `'0' != 'not researched'` |
| 5 | a staging edge on the page (designs edge moved to staging, not rebuilt) | PG-2, PG-3 (both), PG-4, PG-2 period, PG-2 derived | a staging ID on the page; no such home |
| 6 | a DERIVATION drawn as a FACT | PG-4 | `'stated' != 'inferred'` |
| 7 | a changed claim statement, not rebuilt | PG-2, PG-2 derived (digest) | the statement differs from its home |
| 8 | an anchor that no longer matches | PG-2 | `'… lowers the bar …' != '… raises the bar …'` |
| 9 | an evidence panel unreachable by keyboard (`tabindex="-1"`) | PG-8 | `a mark unreachable by keyboard` |
| 10 | an evidence panel removed | PG-3, PG-4, PG-9 | the panel does not exist; a fragment with no target |
| 11 | a build that stamps the clock | PG-7 only | two builds differ |
| 12 | framing that names a record (rebuilt) | PG-6 only | `framing names a record (SK hynix)` |
| 13 | "none" for a missing relationship | PG-2 derived, PG-5 | `RR-7: never 'none'` |
| 14 | a new edge links the lane to an accelerator (not rebuilt) | PG-5 lane, PG-2 derived, PL-1 | `a lane record is linked to an accelerator`; a rebuild is refused |
| 15 | a script fetched from the network | PG-9 | `<script> on a self-contained page` |
| 16 | a hover-only rule (rebuilt) | PG-8 only | `a hover rule without focus` |
| 17 | a text colour below WCAG AA (rebuilt) | PG-8 only | `2.19 not greater than or equal to 4.5` |
| 18 | a quoted rule code whose definition is removed | PG-10 | `rule ER-9 is quoted with no definition on the page` |
| A | control: README edited | — | passes, as it must |
| B | control: an input rewritten and the page rebuilt | — | passes, as it must |

The prompt's nine required breaks are 1 (a mark with no record), 2 (a hand-edited label), 3 and 4 (a
gap removed or drawn as zero), 5 (a staging edge), 6 (a DERIVATION as a FACT), 7 (a changed
statement not rebuilt), 8 (an anchor), 9 and 10 (a panel unreachable by keyboard) and 11 (a page that
does not rebuild identically).

## Addendum — the S12 question and prompt (2026-10-02)

After the report, Claude recommended S12's first audit question: should the candidates of
`edge-dataset.md` §1, which the page reads as data, become records or stay design text the page
quotes? The human's messages, verbatim:

1. "What’s more graphically pleasant"
2. "Pick the recommended"

Claude answered the first: records give the better page (cards grouped by reason, names linked to
their records), but the choice belongs to S12 on architecture grounds (checkable endpoints, a
controlled list of reasons, one parser instead of two), and rejected candidates must never be drawn
as lines on the chain. The recommendation the human picked: **records, decided in S12 on
architecture grounds, with the gaps section restyled as remediation.**

Claude then assembled [`S12-PROMPT.md`](../prompts/S12-PROMPT.md): Part A is S11's operating contract
with S12's roadmap entry; Part B records this answer as H-1 and leaves H-0 (the S11 review), H-2 (the
schema for the candidate records), H-3 (where the audit lives) and Part A's confirmation to be asked
at the start of S12.

The human then confirmed Part A and asked for the merge, verbatim: "I confirm part A and tell u to
pull to main". The prompt records the answer, and S11 with the S12 prompt is merged to `main`.
