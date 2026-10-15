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
- **Generated research pages** (`site/`, never edited by hand), each answering one question; start at
  [`site/index.html`](site/index.html), "What are you trying to understand?":
  - [`site/hbm-chain/`](site/hbm-chain/index.html), the HBM journey: the chain from each accelerator to its
    memory, its maker and the technology it requires, with an evidence panel on every mark;
  - [`site/hbm-insight/`](site/hbm-insight/index.html), the research view: the same chain read in seven layers,
    question → insight → visual → explore → evidence → data → method, with the first metrics;
  - [`site/questions/export-control-texts/`](site/questions/export-control-texts/index.html) (S20): which
    classes each recorded export-control text names among the items it controls, refused pairs with their
    reasons, a timeline of the acts' dates, and each act's status on the as-of date;
  - a profile per company (`site/companies/<id>/`, 9) and per place (`site/places/<id>/`, 4): what the Atlas
    records about it, and on what evidence;
  - [`site/briefs/accelerator-memory/`](site/briefs/accelerator-memory/index.html) (S21), the first client brief:
    one printable page answering "What does an AI accelerator's memory depend on, who is reported to supply it,
    and which recorded export-control texts name those parts?", with its scope and limits, an executive summary
    composed from the records, the dependency map, the export-control comparison, the gaps, the method, and an
    evidence and source appendix ([`client-brief.md`](docs/architecture/client-brief.md)). It describes the
    records; it is not legal, investment or procurement advice.

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
  ([`policy-dataset.md`](docs/architecture/policy-dataset.md)).
- **The later-rule search** (S21.5): the Change Detector searched the official record from 6 December 2024 to
  15 October 2026 for later texts changing the entries the links rest on or repealing an act. It found two later BIS
  rules of January 2025 (the AI Diffusion rule and a due-diligence rule for advanced computing chips), now recorded
  as acts, whose changes to 3A090.c, 3B001 and 3B993 are quoted beside the links; no repeal; no official text
  rescinding the AI Diffusion rule ([`change-detection.md`](docs/research/change-detection.md), D-209). The pages
  state the date up to which the search ran, and a check keeps it at or after their as-of date (D-208).
  From S22 the search is a repository tool (`tools/later_rule_search.py`, D-211) that reads the Federal Register index
  and the official daily edition and writes a dated log; its first run (15 October 2026) found nothing new. A July 2026
  BIS statement about how the AI Diffusion rule is enforced is shown under that act, without changing its status
  (D-214).
- **The engineering audit** (S22): the repository audited as a software system, with measured evidence
  ([`engineering-audit.md`](docs/architecture/engineering-audit.md)); its blocking finding, browser checks that could
  not fail, is fixed and those checks now run in CI (D-212). S22.5 closed the findings left for v1.5's opening, checks
  first: a named build error for a value outside its vocabulary, a break for each check module never shown failing,
  CI's actions pinned to commit hashes, and the search tool's main function split by step (D-216, D-217).
- **The release content audit** (S23): every claim a page result rests on, plus a drawn sample, re-read against
  freshly retrieved sources, and every quoted passage searched for again
  ([`release-content-audit.md`](docs/research/release-content-audit.md), D-218): 178 of 178 readable passages found
  where their locators say, no claim saying more than its source; depth of method, narrow coverage, single-voice
  values. Remediated: BIS's own May 2025 announcement about the AI Diffusion rule is recorded and shown under the act,
  whose status is unchanged (D-220); company pages mark values whose newest evidence is past the freshness horizon on
  the as-of date (D-221); `not_researched` is reworded to cover a partial search (D-219).
- **The first policy links** (M5): four `restricts` links say that an act's own text names a class among the
  items it controls: the December 2024 rule names high-bandwidth memory, and the 2022, 2023 and 2024 rules
  name semiconductor manufacturing equipment. Each rests on the act's quoted sentence and a recorded match
  between its word and the Atlas's record; a later rule that changed the same entry is quoted beside it (the
  2023 rule removed the 2022 entry). Nine candidates were refused, among them GPUs, ASICs and accelerators
  (broader words than the records) and a named HBM product (only the Atlas applying the rule's threshold
  could link it). `python tools/navigate.py edges component-high-bandwidth-memory` shows each link with its
  act's status and "describes the text; does not advise"; since S20 the export-control page shows them too,
  each act with its official text and the same line ([`policy-links.md`](docs/architecture/policy-links.md),
  D-189, D-191).

## How quality is controlled

| Control | What it checks |
|---|---|
| `python -m unittest discover -s tests` | schemas, data integrity (every reference resolves, no unreviewed claim is canonical, freshness), the human review record, the SQL results, and every page (every text node has a home in the records or is marked framing, every count recomputed, rebuild byte-identical, accessibility basics; on the export-control page, every matrix cell, timeline mark and status against the records, and the no-advice line beside every act; on the client brief, every summary sentence recomputed from its rows, scope and limits in its first section and in print, and every cited source in its appendix); 28 planted data faults the record checks must name (D-176); every file has an owner role (D-180) |
| `python tools/validate_repo.py` | Gate 0: the governing documents exist, every relative link in the repository's Markdown resolves, and no session record is committed here |
| `--check` on `tools/warehouse.py`, `tools/build_page.py`, `tools/build_insight.py`, `tools/build_journeys.py`, `tools/build_brief.py` | every committed result and page equals a fresh rebuild from `data/` |
| [`tests/regression/`](tests/regression/README.md) | deliberate breaks (208): each plants one fault in its own copy and must be caught by the suite for the reason it names; run in parallel, selected by the files a change touches (D-177, D-178) |
| [`tests/browser/`](tests/browser/README.md) | browser QA at 1280 and 375 px: errors, overflow, keyboard path, measured contrast; the brief also printed on A4 and Letter |
| [Audits](docs/quality/audit-history.md) | milestone, content, analytical and process audits under `PROJECT-EVALUATION-FRAMEWORK.md` |

CI runs the unit tests and Gate 0, and in a second job the browser checks (Chromium; the research view's filter also in
Firefox and WebKit, D-212), on every push and pull request.

## Limitations

- Coverage is one chain for two accelerators, by design. The Atlas does not claim global coverage. The entry
  page lists the recorded classes no dependency link reaches yet. There is no search: it would need a script
  (D-190).
- Much of the evidence is more than twelve months old. The 12-month horizon applies to time-sensitive links
  (who fabricates a product, who supplies a part): there, stale evidence leaves a gap (TSMC → H100) or a value
  bounded in time (the H100's supplier). Some publishers refuse automated retrieval; these are recorded as
  access gaps.
- Policy records describe; they never advise. No record or link says what anyone must do, and no technical
  threshold is applied to a product (`policy-dataset.md` P-9). A policy link says only that an act's text
  names a class among the items it controls: never that every member, a product or a firm is controlled, for
  which destination, or that the control is in effect today; no exposure is shown. Products and companies
  are not linked to acts yet, and texts published after the search date (15 October 2026) were not searched for
  changes (D-208, D-209). The EAR record still has no dates. Only acts issued by a country can be recorded; EU instruments
  stay in `Eu-Digital-Policy`. A repeal the Atlas has not recorded would not show: the status says "no repeal
  recorded in the Atlas". The end of a single instruction's effect (one 2023 instruction ran to 2026-01-01) is
  stated in a claim, not as an event.
- The open debt, each item with an owner, is listed in the latest audits
  ([M5](docs/architecture/milestone-audits/M5-audit.md), [agent audit](docs/architecture/agent-audit.md),
  [M4](docs/architecture/milestone-audits/M4-audit.md), [analytical audit](docs/architecture/analytical-audit.md)).

## Next phase

M6, the client product, closes with S21.5 ([`SESSION-ROADMAP.md`](SESSION-ROADMAP.md)). S20 built the researcher and
analyst journeys ([`visual-architecture.md`](docs/architecture/visual-architecture.md) §15, D-189 to D-197); S20.5
kept the script-free generated pages (D-200) and set the plan after v1.0 ([`VERSION-ROADMAP.md`](VERSION-ROADMAP.md),
D-201); S21 built the first client brief and activated the Client Output role
([`client-brief.md`](docs/architecture/client-brief.md), D-202 to D-206). S21.5, added by the human (D-207), activates
the Change Detector and runs its first task, the dated search for later export-control texts after 5 December 2024
([`change-detection.md`](docs/research/change-detection.md)). M7, the final audits and the v1.0 release (S22 to
S25), opened with S22, the code and engineering audit, and S22.5, which closed its findings outside v1.5; S23, the
research depth and content audit, is done (D-218 to D-221); next is S24, the portfolio and capability audit.

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

Use Python 3.11, the version CI runs (D-004): a newer interpreter accepts syntax 3.11 rejects (EN-1 catches it in CI).
The tools use the standard library only, except the SQL warehouse, which needs the pinned DuckDB (D-118). The tests
also need the pinned test dependencies (D-026). **Run `python tools/check_all.py` immediately before each commit**,
after the last edit (D-213): it runs the suite, Gate 0 and every `--check` below, in order.

```bash
python3.11 -m venv .venv && . .venv/bin/activate                 # outside Git: .venv is not committed
python -m pip install -r requirements-test.txt -r requirements-analysis.txt
python tools/check_all.py                                        # every check below, in order; stops at the first failure
python -m unittest discover -s tests -v                          # unit tests
python tools/validate_repo.py                                    # Gate 0: repository integrity
python tools/warehouse.py --check                                # every SQL result equals a fresh run from data/
python tools/build_page.py --check                               # the HBM page equals a rebuild
python tools/build_insight.py --check                            # the research view equals a rebuild (build it after the HBM page)
python tools/build_journeys.py --check                           # the 15 journey pages equal a rebuild
python tools/build_brief.py --check                              # the client brief equals a rebuild (build it last)
python tools/trace.py company-nvidia                             # what supports a record or claim
python tools/facility_status.py facility-kr-m16 --on 2026-10-02  # a facility's derived status
python tools/navigate.py depends-on technology-3d-die-stacking   # what depends on a record; --json for data
python tools/later_rule_search.py --from YYYY-MM-DD --to YYYY-MM-DD   # the later-rule search for a window (D-211)
```

Browser checks (Node 22; CI runs them on every push, D-212): `npm ci`, then the scripts in
[`tests/browser/`](tests/browser/README.md).
