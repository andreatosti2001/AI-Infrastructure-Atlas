# AI-Infrastructure-Atlas
Evidence-backed intelligence system mapping the infrastructure, supply chains, companies, technologies, and strategic dependencies underlying the global AI ecosystem.

## Status

**M2 — Canonical Dataset (S07 to S09 complete; S10 to come).** The repository contains governance documents, the
session system, a repository-integrity check, the S01 domain map, the accepted entity
schema (S03), the accepted relationship schema (S04), the accepted source policy with its
source-class vocabulary (S05), the accepted claim model (S06), and the first canonical
entities (S07, M2): 8 companies and 4 jurisdictions, each traceable to the companies' own
filings and to ISO 3166, with record-level `validate-data` and a first `validate-freshness`
rule; and (S08) 7 components, 9 technologies and 3 products, each concept defined by an
`INTERPRETATION` over government, research and policy-research sources (5 of the technologies
became canonical at the end of S09, when the human approved the last two S08 rulings); and (S09) 2
facilities, each placed by a site sentence and never by a headquarters one, with 4 dated
events in a new event schema, from which a facility's status is derived, never stored. It contains **no relationship records and no UI yet**. See
[`docs/architecture/baseline.md`](docs/architecture/baseline.md) for what exists and what is
planned.

This is an independent repository. It shares no code, data or runtime with
`Eu-Digital-Policy` ([decision D-006](docs/architecture/decisions.md)).

## Layout

```text
CLAUDE.md, MASTER-ARCHITECTURE.md, ...   constitutional documents (see docs/README.md)
data/            source records, canonical claims, companies, jurisdictions, technologies, components, products, facilities and events; staging/ holds records awaiting the human's review
docs/            documentation map, baseline, decision log, entity and relationship taxonomies, claim model, company, concept and facility datasets, milestone audits, agent roles and contracts, research, source policy
schemas/         JSON Schema for entity records (accepted, S03), relationship records (accepted, S04), source records around the accepted source-class vocabulary (S05, S06), claims (S06) and facility events (S09)
sessions/        session prompts, prompt registry and session reports
tools/           Gate 0 validator, the trace command and the facility status derivation
tests/           unit tests for tools/, schemas/ and data/ (validate-data), with fictional fixtures
.github/         CI
```

## Validate

Requires Python 3.11+. The tools use the standard library only. The tests also need
the pinned test dependencies (decision D-026).

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v   # unit tests
python tools/validate_repo.py             # Gate 0: repository integrity
python -m unittest discover -s tests -p "test_data*.py" -v   # validate-data
python -m unittest discover -s tests -p "test_freshness.py" -v   # validate-freshness
python tools/trace.py company-nvidia                         # what supports a record or claim
python tools/facility_status.py facility-kr-m16 --on 2026-10-02   # a facility's derived status
```

CI runs both on every push and pull request.
