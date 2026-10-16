# Regression breaks

The break harness tests the checks themselves. Each break copies the repository (without `.git`) into a scratch
folder, plants one fault, runs its build steps (results -> HBM page -> research view -> research journeys -> client brief), runs the full suite, and
counts only if the suite fails **with every expected fragment in its output**: the fault is caught, and caught
for the reason the break names. A control makes a harmless edit and counts only if the suite passes.

```bash
python -m pip install -r requirements-test.txt -r requirements-analysis.txt
python tests/regression/breaks.py SCRATCH_DIR                   # every break, one per processor at a time
python tests/regression/breaks.py SCRATCH_DIR --since main      # the breaks a change selects (D-177)
python tests/regression/breaks.py --changed PATH ... --select-only   # print a selection and its reasons
python tests/regression/breaks.py SCRATCH_DIR S16.6-A1 D151-2   # chosen breaks
python tests/regression/breaks.py SCRATCH_DIR --setup-only      # check that every edit still applies
python tests/regression/breaks.py --touched                     # every break's measured files and build steps
```

`SCRATCH_DIR` must be outside the repository. `--jobs N` sets how many breaks run at once (default: the number of
processors); `--out FILE` also writes the lines and the summary to a file. Each break runs in its own numbered
copy, `SCRATCH_DIR/NNN-ID`. Lines are printed in the harness's order, then one summary: faults caught as named,
controls passing, stale setups. The exit status is 0 only if every break is caught as named and every control
passes. Measured in S19 on 4 processors: the full run took 34.5 minutes with `--jobs 4` (36 minutes as four processes
split by hand, about 87 minutes one after another).

**When to run what** (D-150, D-177):
- the full harness at a milestone audit;
- in between, a change runs the breaks it selects (`--since` the base, or `--changed`), plus the new breaks for
  its own checks. A break is selected when a file its setup changes, or a tool its build steps run, is among the
  changed files. The files are **measured** (the setup applied to a scratch copy), never declared, so they cannot
  drift from what the setup edits;
- a change to a check module (`tests/test_*.py`), a schema, Gate 0 (`tools/validate_repo.py`) or the harness's
  code (`tests/regression/*.py`) selects the full harness: selection by setup files cannot see a check that was
  loosened. A change to this README does not (D-188): no check reads it, and Gate 0 checks its links on every
  push. `tests/test_break_selection.py` checks the trigger.

A break whose setup text a change removes is replaced by the same fault on the new text (the layer files show
how), never dropped.

**Permanent breaks** (D-176). 28 breaks also run on every commit, inside the suite, as
`tests/test_planted_faults.py`: each break's own setup is applied to a temporary copy of `data/`, the record
checks run in memory, and every expected fragment must be among the errors. A break is permanent when it plants a
fault in the records (a loosened check would leave CI green), its setup edits `data/` only and its fault is named
by a check's message (no copy, rebuild or subprocess), and its setup finds the records by ID. The 28: S13-2, S13-3,
S13-4 (the data break of each ID), S13-22 to S13-26; S16.5-A1; S16.6-A9 to A11; D151-4; S17-1 to S17-8, S17-11;
S18-1 to S18-5, S18-10. They stay in the harness. A new break that meets the criterion is added to the list in
`tests/test_planted_faults.py`.

**Layers.** Each file loads the one before it and replaces the inherited breaks whose setup text later changes
removed; `breaks.py` is the complete harness and the only entry point.

| File | Adds breaks for |
|---|---|
| `breaks_records_and_page.py` | the records, the refused candidates and the HBM page's checks |
| `breaks_sql.py` | the SQL layer and the HBM page's SQL section |
| `breaks_research_view.py` | the research view |
| `breaks_metrics.py` | the metrics; it also merges the three files above into one shape and holds the runner |
| `breaks_metric_audit.py` | the remediations of the metric audit |
| `breaks_supplier_freshness.py` | stale supplier evidence; the human review record's form |
| `runner.py` | not a layer: the runner `breaks.py` uses (parallel copies, the summary, measured selection) |
| `breaks.py` | the supplier-evidence rules and the reported supplier; the human review record and Gate 0's links; no session record in the public tree; the policy layer (S17: PL-1 to PL-9, D-164); the policy links (S18); the research journeys (S20: C-2, C-5, JR-1 to JR-12); the research view's filter guard (S20.5: IN-14, D-200); the client brief (S21: BR-1 to BR-12, JR-8's link to it, the Client Output's role, D-202 to D-206); the later-rule search window and tool (S21.5, S22); the engineering audit's remediations (S22: EN-1, EN-2, the printed list; S22.5: the named build error, the drawn gap's refusal, a break for each check module never shown failing, hash-pinned actions, D-216); v1.0's known limitations against the pages and the Portfolio Reviewer's activation (S24: KL-1 to KL-8, D-222, D-223); the publication (S25: the published-address check PA-1 to PA-3, the workflow PW-1 and its pins, KL-15 after the publication wording, D-227; S14.5-F1 replaced, its sentence gone). A break that rebuilds the results or the HBM page also rebuilds the journey pages, which read both (`with_journeys`, D-190); a break that rebuilds the results, the HBM page or the journeys also rebuilds the client brief, which reads all three (`with_brief`, D-203) |

**Break IDs** are stable labels, kept so that audits can cite them; the prefix names the layer that added the
break (`S13-`, `S14-`, `S14.5-`, `S15-`, `S16-`, `S16.5-`, `S16.6-`, `S17-` after the roadmap phase, `D151-`, `D152-` after the
decision).
