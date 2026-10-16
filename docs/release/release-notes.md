# AI-Infrastructure-Atlas v1.0 — release notes

- **Status:** proposed (S25, 2026-10-16), for the human's acceptance with the release (S25 H-3). Written by the
  Editorial (D-229).
- **The release:** the commit tagged `v1.0` on `main`. Its pages are published at
  <https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/index.html>, built from that commit and checked
  there against it, byte for byte (D-226, D-227).
- **Dates:** the pages are read as of 15 October 2026, and the search for later export-control texts runs to the same
  day (D-228). Nothing published after it is in the Atlas.
- **Claim discipline:** a count names where it was measured. A sentence that judges is the release's reading
  (`INTERPRETATION`), and is marked as such.

## What v1.0 is

The Atlas is a small, checkable research database about the physical layer of AI. It answers one question end to
end:

> What does an AI accelerator's memory depend on, who is reported to supply it, and which recorded export-control
> texts name those parts?

It covers two accelerators, the NVIDIA H100 and AWS Trainium2, and the High Bandwidth Memory inside them. Every value
on its 18 pages opens the source sentence it rests on. Every gap is shown as a gap, never as a zero. Every page is
generated from the records by a tested build, and rebuilding it from the same records gives the same bytes.

It is deliberately narrow. It does not cover the global chain, give legal advice, or score anything. What it does
not do is listed in one place: [known limitations](../known-limitations.md).

## Where to start

| If you want to | Open |
|---|---|
| see the answer | [the client brief](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/briefs/accelerator-memory/index.html), or the [entry page](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/index.html) and its six questions |
| follow one value to its source | [the demonstration journey](demonstration.md) |
| see how the Atlas draws evidence | [the infographic set](infographic-set.md) |
| judge what the project shows | [the case study](../case-study.md) |
| check it yourself | `python tools/check_all.py` on Python 3.11 ([README, Validate](../../README.md#validate)); [CI runs](https://github.com/andreatosti2001/AI-Infrastructure-Atlas/actions/workflows/ci.yml) |

## The seven things to understand, and where each is explained

The roadmap's exit condition for v1.0 is that another person can understand these seven points. Each row says the
point in one sentence and links the document that explains it.

| Point | In one sentence | Explained in |
|---|---|---|
| 1. What the system does | It records which parts AI accelerators depend on and who makes them, each link resting on quoted sources, and answers questions about them on generated pages. | [README](../../README.md); [the entry page](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/index.html) |
| 2. How the data is structured | Canonical JSON records of thirteen kinds, each with one home and one schema. Typed relationships rest on claims, claims cite registered sources, and unknown values are named states. | [final architecture record](../architecture/final-architecture.md) §2; [`claim-model.md`](../architecture/claim-model.md); [`schemas/`](../../schemas/) |
| 3. How claims are verified | A Verifier re-reads each cited sentence in the source's bytes and sets its evidence status. The human then accepts or rejects every claim before it becomes canonical; drafts wait in staging. | [README, How evidence works](../../README.md#how-evidence-works); [human review record](../quality/human-reviews.md) |
| 4. How metrics are produced | SQL queries over an in-memory DuckDB rebuilt from the records. Each query states its question, population, denominator and what it does not prove, and its committed result carries the hash of every input. | [`sql-layer.md`](../architecture/sql-layer.md); [`metrics.md`](../architecture/metrics.md); the "How this was computed" tutorials on the pages |
| 5. How agents are governed | Twelve roles, eleven active, each a written contract of what Claude may read and write in a session. Every file has an owner, checked in CI. The human's verdicts are outside every contract. No program acts on its own. | [agent roles](../agents/roles.md); [contracts](../agents/contracts.md); [README, How this was built](../../README.md#how-this-was-built) |
| 6. How to reproduce the build | One command re-runs every check and rebuilds every result and page, failing if any differs from what is committed. CI does the same on every push, and the publication does it again before deploying. | [README, Validate](../../README.md#validate); [`.github/workflows/`](../../.github/workflows/) |
| 7. Why the product is useful | It shows exactly what is known about an AI-hardware dependency, how well, and what is not known. The reading behind that judgement is the case study's. | [the case study](../case-study.md); [the client brief](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/briefs/accelerator-memory/index.html) |

## What is in v1.0

- **The records** (`data/`): sources, claims, companies, places, technologies, components, products, facilities,
  export-control acts and their dated events, relationships, refused candidates and the basis of rule-made IDs. Every
  claim has been reviewed by the human. Current counts: [baseline §1](../architecture/baseline.md), measured by S24
  ([`measures.json`](../quality/audit-evidence/portfolio-audit/measures.json)).
- **The pages** (`site/`): the HBM dependency journey, the research view, the export-control comparison, nine company
  and four place profiles, the entry page, and the client brief.
- **The analysis** (`sql/`): four queries, each its own tutorial, with committed results.
- **The checks:** the test suite, Gate 0, five rebuild checks, the break harness of deliberate faults, the browser
  checks at 1280 and 375 px and in print, and the check of the published address. All of them are listed in the
  [README](../../README.md#how-quality-is-controlled).
- **The record of how it was built:** every decision with its context and, for nearly all, the alternatives it
  rejected ([decision log](../architecture/decisions.md)), and the audits ([audit history](../quality/audit-history.md)).

## What changed in S25, the release session

- **Published.** The pages and the files they link to are served from the release commit by
  `.github/workflows/pages.yml`. The workflow runs only on a tagged commit and only after every check passes, then
  checks the address with `tools/check_published.py` and the five browser scripts (D-227). The research view no
  longer says that it is not published. KL-15 keeps the half of its gap that remains: no person outside the project
  is recorded as having used the Atlas.
- **The release documents:** these notes, the [final architecture record](../architecture/final-architecture.md),
  the [final process and outcome audit](../architecture/final-audit.md), the
  [research backlog](../research/backlog.md), the [case study](../case-study.md), the
  [demonstration](demonstration.md), the [infographic set](infographic-set.md), and
  [M7's milestone audit](../architecture/milestone-audits/M7-audit.md).
- **No record, claim, source or status changed.** The as-of date did not move.

## What comes next

v1.5 (visual intelligence) and v2 (the global AI infrastructure chain) are planned in
[`VERSION-ROADMAP.md`](../../VERSION-ROADMAP.md). Each begins only when the human opens it. The research gaps that no
planned session closes yet are placed in the [research backlog](../research/backlog.md).
