# AI-Infrastructure-Atlas
Evidence-backed intelligence system mapping the infrastructure, supply chains, companies, technologies, and strategic dependencies underlying the global AI ecosystem.

## Status

**M4 — Analytical Intelligence (S14 done: the SQL layer, accepted 2026-10-03; S14.5 done: the visual and research-experience architecture, accepted 2026-10-06; S15 next).** The repository contains governance documents, the
session system, a repository-integrity check, the S01 domain map, the accepted entity
schema (S03), the accepted relationship schema (S04), the accepted source policy with its
source-class vocabulary (S05), the accepted claim model (S06), and the first canonical
entities (S07, M2): 8 companies and 4 jurisdictions, each traceable to the companies' own
filings and to ISO 3166, with record-level `validate-data` and a first `validate-freshness`
rule; and (S08) 7 components, 9 technologies and 3 products, each concept defined by an
`INTERPRETATION` over government, research and policy-research sources (5 of the technologies
became canonical at the end of S09, when the human approved the last two S08 rulings); and (S09) 2
facilities, each placed by a site sentence and never by a headquarters one, with 4 dated
events in a new event schema, from which a facility's status is derived, never stored; and (S10) the first 5
relationship records, each resting on claims that meet the taxonomy's evidence expectation for
its type, navigable from the JSON files by `tools/navigate.py` without a graph database; and (S11) the first
page, [`site/hbm-chain/index.html`](site/hbm-chain/index.html): one journey, "What does an AI accelerator's
memory depend on, and who is known to make it?", generated from the records by a tested standard-library
build step, in which every mark opens its evidence and every unknown is drawn as a named gap. The page is
not published (NG-13). S12 audited the data model and the page (the overdue M2 audit,
[`docs/architecture/milestone-audits/M2-audit.md`](docs/architecture/milestone-audits/M2-audit.md)):
its one blocking finding is remediated, so the 12 relations the Atlas considered and refused are now
records with their own checks, which the page shows as cards grouped by reason. S13 audited the
content ([`docs/research/content-audit-S13.md`](docs/research/content-audit-S13.md)): 34 sampled claims
re-read in their sources, none overreaching; its one blocking finding is remediated, so the card for
NVIDIA's memory suppliers now names all three firms NVIDIA names, and ten weaknesses are recorded with
owners. S14 added the SQL layer ([`docs/architecture/sql-layer.md`](docs/architecture/sql-layer.md)): the records are
loaded into a DuckDB database rebuilt from `data/` on every run and never stored, and the first query lists, for
each accelerator on the page, every link the Atlas records with its basis and evidence dates. The page shows the
result as "The chain as a table", with a "How this was computed" tutorial generated from the query file. S14.5
studied five data-intensive research products ([`docs/research/visual-benchmark-S14.5.md`](docs/research/visual-benchmark-S14.5.md))
and set the Atlas's visual and research-experience architecture ([`docs/architecture/visual-architecture.md`](docs/architecture/visual-architecture.md)):
a page answers its question in seven layers, from the finding to the method, each rendered from a committed SQL result or
from the records. A generated prototype, [`site/hbm-insight/index.html`](site/hbm-insight/index.html), shows the HBM chain that
way: a headline composed from the result, indicator blocks whose counts carry their denominators, the two accelerators'
chains side by side, a basis filter, and evidence one click from every mark. See
[`docs/architecture/baseline.md`](docs/architecture/baseline.md) for what exists and what is
planned.

This is an independent repository. It shares no code, data or runtime with
`Eu-Digital-Policy` ([decision D-006](docs/architecture/decisions.md)).

## Layout

```text
CLAUDE.md, MASTER-ARCHITECTURE.md, ...   constitutional documents (see docs/README.md)
data/            source records, canonical claims, companies, jurisdictions, technologies, components, products, facilities, events, relationships, refused candidates and identity-basis rows; staging/ holds records awaiting the human's review
docs/            documentation map, baseline, decision log, entity and relationship taxonomies, claim model, company, concept, facility and edge datasets, milestone audits, agent roles and contracts, research, source policy
schemas/         JSON Schema for entity records (accepted, S03), relationship records (accepted, S04), refused candidates (S12), source records around the accepted source-class vocabulary (S05, S06), claims (S06) and facility events (S09)
sessions/        session prompts, prompt registry and session reports
tools/           Gate 0 validator, the trace command, the facility status derivation, edge navigation, the page build with its template, the SQL warehouse (S14), and the prototype build with its template (S14.5)
sql/             SQL queries, each also its own tutorial; results/ holds their generated results (never edited by hand)
site/            generated pages (never edited by hand): hbm-chain/index.html (S11); hbm-insight/index.html (S14.5 prototype)
tests/           unit tests for tools/, schemas/ and data/ (validate-data), with fictional fixtures
.github/         CI
```

## Validate

Requires Python 3.11+. The tools use the standard library only, except the SQL warehouse, which needs
the pinned DuckDB (decision D-118). The tests also need the pinned test dependencies (decision D-026).

```bash
python -m pip install -r requirements-test.txt -r requirements-analysis.txt
python -m unittest discover -s tests -v   # unit tests
python tools/validate_repo.py             # Gate 0: repository integrity
python -m unittest discover -s tests -p "test_data*.py" -v   # validate-data
python -m unittest discover -s tests -p "test_freshness.py" -v   # validate-freshness
python tools/trace.py company-nvidia                         # what supports a record or claim
python tools/facility_status.py facility-kr-m16 --on 2026-10-02   # a facility's derived status
python tools/navigate.py depends-on technology-3d-die-stacking   # what depends on a record (S10); --json for data (S11)
python tools/warehouse.py --check                                # every SQL result equals a fresh run from data/ (S14)
python tools/build_page.py --check                               # the S11 page equals a rebuild (validate-design: tests/test_page.py)
python tools/build_insight.py --check                            # the S14.5 prototype equals a rebuild (tests/test_insight.py); build it after the S11 page
```

CI runs the unit tests (including the page checks) and Gate 0 on every push and pull request.
