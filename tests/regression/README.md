# Regression breaks

The break harness tests the checks themselves. Each break copies the repository (without `.git`) into a scratch
folder, plants one fault, runs its build steps (results -> HBM page -> research view), runs the full suite, and
counts only if the suite fails **with every expected fragment in its output**: the fault is caught, and caught
for the reason the break names. A control makes a harmless edit and counts only if the suite passes.

```bash
python -m pip install -r requirements-test.txt -r requirements-analysis.txt
python tests/regression/breaks.py SCRATCH_DIR                 # every break (milestone audits, D-150)
python tests/regression/breaks.py SCRATCH_DIR S16.6-A1 D151-2 # chosen breaks
python tests/regression/breaks.py SCRATCH_DIR --setup-only    # check that every edit still applies
```

`SCRATCH_DIR` must be outside the repository. A full run copies the repository once per break and runs the suite
each time, so it takes hours; IDs can be split across several processes, each with its own scratch folder.
The exit status is 0 only if every break is caught as named and every control passes.

**When to run what** (D-150): the full harness at a milestone audit; in between, a change runs the breaks that
touch the files it changes, plus the new breaks for its own checks. A break whose setup text a change removes is
replaced by the same fault on the new text (the layer files show how), never dropped.

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
| `breaks.py` | the supplier-evidence rules and the reported supplier; the human review record and Gate 0's links; no session record in the public tree; the policy layer (S17: PL-1 to PL-9, D-164) |

**Break IDs** are stable labels, kept so that audits can cite them; the prefix names the layer that added the
break (`S13-`, `S14-`, `S14.5-`, `S15-`, `S16-`, `S16.5-`, `S16.6-`, `S17-` after the roadmap phase, `D151-`, `D152-` after the
decision).

## Proposal: the three harness improvements (S19, D-153) — awaiting the human's decision (H-1)

Measured on 2026-10-13 on `main` = `f6e6357`, in a 4-core container: the suite takes 38 s; one break takes about
40 s (copy, rebuild, suite); the 130 breaks take about 87 minutes one after another. Nothing below is built yet.

### H1-1. Permanent tests: 28 breaks checked on every commit

- **What changes.** A new test module, `tests/test_planted_faults.py`, run by the suite on every push and in CI
  (the workflow already runs the suite; it does not change). For each of 28 breaks it takes **the break's own
  setup** from the harness, applies it to a temporary copy of `data/` only, runs every record check (the schema
  of the changed records, VD, V, EV, PL, PK, RC, F-1, HR-1, HR-2) on the planted records in memory, and passes
  only if **every fragment the break expects** is among the errors. It also checks that the real data gives no
  error. The harness keeps the 28 breaks: nothing is dropped, and the milestone run still runs them.
- **Criterion.** A break becomes a permanent test when all three hold:
  1. *unnoticed otherwise*: it plants a fault in the records. If a later change loosened the check, the real
     data would still pass and CI would stay green, so the loss would show only at the next milestone audit;
  2. *cheap*: its setup edits files in `data/` only, and its fault is named by a check's message (not by a test
     name or a rebuild), so no repository copy, rebuild or subprocess is needed;
  3. *stable*: its setup finds the records by ID, so a page or tool change cannot make it stale.
- **The 28:** S13-2, S13-3, S13-4 (the data break of each ID), S13-22 to S13-26; S16.5-A1; S16.6-A9 to A11;
  D151-4; S17-1 to S17-8, S17-11; S18-1 to S18-5, S18-10.
- **Left in the harness only, with the reason:** the 14 controls (a false alarm is noticed at once, so a
  control fails criterion 1); every break that edits a page, a tool, a query, a schema or a document (it needs a
  copy and a rebuild); and the 7 data breaks named by a test name or a rebuild check (S13-5 twice, S13-7,
  S13-21, S13-27, S14-R2, S14.5-D1, S16.5-A2).
- **CI time.** About 0.05 s per break once only the changed records are re-validated against the schemas: about
  2 to 4 s more on a 38 s suite. Measured and reported when built.

### H1-2. Selection by the files a break actually touches

- **What changes.** `tests/regression/breaks.py` gains `--changed PATH ...` and `--since REV` (the files changed
  since a commit, read with `git diff --name-only`). For each break the runner applies its setup to a scratch
  copy and **measures** the files whose bytes change, appear or disappear (5.7 s for all 130). A break is
  selected when a measured file, or a tool its build steps run, is among the changed files. `--touched` prints
  every break with its measured files.
- **No declaration to keep in sync.** A break does not declare its files: the measurement is the declaration, so
  it cannot drift from what the setup edits, and setups of any form (lambdas, multi-file edits, new files) are
  read. The private selection scripts of S17 and S18 are no longer needed.
- **Evidence.** Given S18's list of changed files, the measured selection picks 59 breaks: the 56 that S18's
  script picked, plus S13-18, S13-20 and S13-21, the three S18 had to add by hand because the script could not
  read their setups. It misses none.
- **A remaining gap, and the proposed rule.** Selection by setup files does not see a change to a check itself
  (a `tests/test_*.py` module): a loosened check is caught only by the breaks whose setup happens to touch the
  changed files. Proposed: a session that changes a check module, a schema or the harness runs the **full**
  harness, in parallel (about 25 minutes, H1-3). This amends D-150, which keeps the full run for milestone audits.

### H1-3. Parallel copies with one combined result

- **What changes.** A runner in `tests/regression/runner.py` (standard library only, D-003), used by `breaks.py`:
  `--jobs N` (default: the number of processors) runs N breaks at a time, each in its own copy
  `SCRATCH/NNN-ID` (numbered, because four S13 IDs name two breaks each and the current folder name, the ID
  alone, would let two copies collide). Lines are printed in the harness's order, followed by one summary:
  faults caught as named, controls passing, stale setups. `--out FILE` writes the same lines. The exit status is
  0 only if every fault is caught as named and every control passes, as today.
- **Time.** Estimated at about 25 minutes for the 130 breaks on 4 processors, instead of about 87; measured at the
  full run.
- **What stays.** Each break still copies the repository, plants its edit, runs its build steps in order and the
  whole suite, and counts only if the suite fails with every expected fragment (a control: only if it passes).

### H1-4. Equivalence: the same verdict for every break

- The old runner (as it is, split by hand into four processes as S17 and S18 did) and the new runner
  (`--jobs 4`) run all 130 breaks on the same tree. For every break, the verdict and the set of failing tests must
  be identical. Any difference stops the session (prompt §16). The new runner's run is also the M5 full run.
- Each permanent test is shown failing before the checks are connected (every one of the 28 fails), and against
  a check loosened on purpose; and each is caught as named by the harness in the full run.
- The selection is shown to pick a superset of S18's script on S18's changed files (above).
