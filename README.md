# AI-Infrastructure-Atlas

An evidence-backed research system for the physical layer of AI: the accelerators, memory, manufacturing,
packaging, equipment and data centres that AI compute depends on, the companies that make them, and the
evidence for each link between them.

The Atlas is deliberately narrow and deep. It answers one question end to end before it grows:

> **What does an AI accelerator's memory depend on, and who is known to make it?**

for two accelerators, the NVIDIA H100 and AWS Trainium2, and their High Bandwidth Memory (HBM). Every value
on its pages can be traced to a sentence in a registered source, and everything the Atlas does not know is
shown as a named gap, never as zero.

This is an independent repository. It shares no code, data or runtime with `Eu-Digital-Policy`
([D-006](docs/architecture/decisions.md)).

## What it contains

- **Canonical records** in `data/`: sources, claims, companies, jurisdictions, technologies, components,
  products, facilities, policy instruments, dated events, relationships, the relations the Atlas considered and refused, and the
  identity basis of rule-made IDs. Each kind has one home and one schema in `schemas/`. Current counts are in
  [`docs/architecture/baseline.md`](docs/architecture/baseline.md) §1.
- **A SQL layer** (`sql/`, `tools/warehouse.py`): the records are loaded into a DuckDB database rebuilt from
  `data/` on every run and never stored. Each query is also its own tutorial; its result is committed in
  `sql/results/` with the SHA-256 of every input, so a stale result is detected.
- **Two generated pages** (`site/`, never edited by hand):
  - [`site/hbm-chain/`](site/hbm-chain/index.html), the HBM journey: the chain from each accelerator to its
    memory, its maker and the technology it requires, with an evidence panel on every mark;
  - [`site/hbm-insight/`](site/hbm-insight/index.html), the research view: the same chain read in seven layers,
    question → insight → visual → explore → evidence → data → method, with the first metrics.

The pages are not published (NG-13): they are built and checked in the repository.

## How evidence works

- **A source** is registered when retrieved, with its URL, publisher, class (`docs/research/source-policy.md`),
  access time and the SHA-256 of the bytes read.
- **A claim** is one proposition, typed `FACT`, `ATTRIBUTION`, `DERIVATION`, `INTERPRETATION` or
  `IMPLICATION` (`CLAUDE.md` §6), citing its sources at a locator with a verbatim anchor. A Verifier reads the
  whole sentence and sets its evidence status: `supported`, `partial`, `context_only` or `disputed`. The
  Atlas's own inferences are `DERIVATION`s and are shown as inferred
  ([`claim-model.md`](docs/architecture/claim-model.md)).
- **The human reviews every real claim** before it becomes canonical; unreviewed claims stay in
  `data/staging/`. Each canonical claim names its verdict, its date and the entry of the
  [human review record](docs/quality/human-reviews.md) that holds the review.
- **A relationship** (for example, a product `incorporates` a component) is a typed edge resting on claims
  that meet its type's evidence expectation, including freshness
  ([`relationship-taxonomy.md`](docs/architecture/relationship-taxonomy.md),
  [`edge-dataset.md`](docs/architecture/edge-dataset.md)).
- **Unknown is never zero.** A missing value is an explicit state: `not_researched`,
  `not_publicly_determinable` (citing the claims that show it) or `not_applicable`. A value reported only by a
  third party is shown as **reported**, with the criteria it does or does not meet, never as stated.

`python tools/trace.py <record or claim ID>` prints what supports any record: its claims, sources, locators,
anchors and review.

## What it shows today

- Both accelerators incorporate HBM, and HBM requires 3D die stacking; both rest on the parties' own
  statements and a recorded inference.
- The HBM supplier is named only as **reported** by a third party: SK hynix for the H100 (historical, to
  2024-03, TrendForce) and Samsung Electronics for Trainium2 (SemiAnalysis, whose recognition criterion is not
  met). No current H100 supplier is established
  ([`hbm-supplier-research.md`](docs/research/hbm-supplier-research.md)).
- Two metrics are computed in SQL: evidence coverage per accelerator and source age as of a fixed reference
  date. The three supplier metrics (supplier count, geographic concentration, single-source relationships) are
  shown as "cannot be computed yet", because no source says a maker was the only one
  ([`metrics.md`](docs/architecture/metrics.md)).
- **The first policy records** (M5): five US export-control acts, each recorded from its own official text on
  govinfo.gov: the Export Administration Regulations and four rules of the Bureau of Industry and Security
  (October 2022, two of October 2023, December 2024). Each record holds what identifies the act; what the act
  provides stays in claims attributed to the authority; its dates are events, and its status on any day is
  computed by `tools/policy_status.py` ("has taken effect; no repeal recorded in the Atlas", never "in force").
  They are not yet linked to companies, parts or technologies
  ([`policy-dataset.md`](docs/architecture/policy-dataset.md)).

## How quality is controlled

| Control | What it checks |
|---|---|
| `python -m unittest discover -s tests` | schemas, data integrity (every reference resolves, no unreviewed claim is canonical, freshness), the human review record, the SQL results, and both pages (every text node has a home in the records or is marked framing, rebuild byte-identical, accessibility basics) |
| `python tools/validate_repo.py` | Gate 0: the governing documents exist, every relative link in the repository's Markdown resolves, and no session record is committed here |
| `--check` on `tools/warehouse.py`, `tools/build_page.py`, `tools/build_insight.py` | every committed result and page equals a fresh rebuild from `data/` |
| [`tests/regression/`](tests/regression/README.md) | deliberate breaks: each plants one fault and must be caught by the suite for the reason it names |
| [`tests/browser/`](tests/browser/README.md) | browser QA at 1280 and 375 px: errors, overflow, keyboard path, measured contrast |
| [Audits](docs/quality/audit-history.md) | milestone, content, analytical and process audits under `PROJECT-EVALUATION-FRAMEWORK.md` |

CI runs the unit tests and Gate 0 on every push and pull request.

## Limitations

- Coverage is one chain for two accelerators, by design. The Atlas does not claim global coverage.
- Much of the evidence is more than twelve months old. The 12-month horizon applies to time-sensitive links
  (who fabricates a product, who supplies a part): there, stale evidence leaves a gap (TSMC → H100) or a value
  bounded in time (the H100's supplier). Some publishers refuse automated retrieval; these are recorded as
  access gaps.
- Policy records describe; they never advise. No record or link says what anyone must do, and no technical
  threshold is applied to a product (`policy-dataset.md` P-9). The five export-control records are not yet
  linked to the chain, so no exposure is shown. Only acts issued by a country can be recorded; EU instruments
  stay in `Eu-Digital-Policy`. A repeal the Atlas has not recorded would not show: the status says "no repeal
  recorded in the Atlas". The end of a single instruction's effect (one 2023 instruction ran to 2026-01-01) is
  stated in a claim, not as an event.
- The open debt, each item with an owner, is listed in the latest audits
  ([M4](docs/architecture/milestone-audits/M4-audit.md), [analytical audit](docs/architecture/analytical-audit.md)).

## Next phase

M5 ([`SESSION-ROADMAP.md`](SESSION-ROADMAP.md)) is under way. S17 defined the policy record and recorded the
first export-control acts. S18 links them to the parts, products, technologies and companies their texts name
(`restricts`, defined in [`policy-dataset.md`](docs/architecture/policy-dataset.md) P-8), each link resting on
the text's own words or a party's statement. S19 audits the agent architecture and, first, improves the break
harness (D-153).

## Layout

```text
CLAUDE.md, MASTER-ARCHITECTURE.md, ...   constitutional documents (see docs/README.md)
data/            canonical records; staging/ holds records awaiting the human's review
schemas/         JSON Schema for every record kind, with their controlled vocabularies
sql/             SQL queries, each also its own tutorial; results/ holds their generated results
tools/           Gate 0, the trace command, facility and policy status, edge navigation, the SQL warehouse, the page builds
site/            generated pages (never edited by hand)
tests/           unit tests with fictional fixtures; regression/ (deliberate breaks); browser/ (browser QA)
docs/            documentation map, architecture, decisions, research, audits, agent contracts
.github/         CI
```

## Validate

Requires Python 3.11+. The tools use the standard library only, except the SQL warehouse, which needs the
pinned DuckDB (D-118). The tests also need the pinned test dependencies (D-026).

```bash
python -m pip install -r requirements-test.txt -r requirements-analysis.txt
python -m unittest discover -s tests -v                          # unit tests
python tools/validate_repo.py                                    # Gate 0: repository integrity
python tools/warehouse.py --check                                # every SQL result equals a fresh run from data/
python tools/build_page.py --check                               # the HBM page equals a rebuild
python tools/build_insight.py --check                            # the research view equals a rebuild (build it after the HBM page)
python tools/trace.py company-nvidia                             # what supports a record or claim
python tools/facility_status.py facility-kr-m16 --on 2026-10-02  # a facility's derived status
python tools/navigate.py depends-on technology-3d-die-stacking   # what depends on a record; --json for data
```
