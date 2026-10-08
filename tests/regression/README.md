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
| `breaks.py` | the supplier-evidence rules and the reported supplier; the human review record and Gate 0's links; no session record in the public tree |

**Break IDs** are stable labels, kept so that audits can cite them; the prefix names the layer that added the
break (`S13-`, `S14-`, `S14.5-`, `S15-`, `S16-`, `S16.5-`, `S16.6-` after the roadmap phase, `D151-`, `D152-` after the
decision).
