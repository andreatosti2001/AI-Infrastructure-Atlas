# AI-Infrastructure-Atlas
Evidence-backed intelligence system mapping the infrastructure, supply chains, companies, technologies, and strategic dependencies underlying the global AI ecosystem.

## Status

**M1 — Domain + Evidence Foundation.** The repository contains governance documents, the
session system, a repository-integrity check, the S01 domain map, the accepted entity
schema (S03) and the accepted relationship schema (S04). It contains **no data records or UI yet**. See
[`docs/architecture/baseline.md`](docs/architecture/baseline.md) for what exists and what is
planned.

This is an independent repository. It shares no code, data or runtime with
`Eu-Digital-Policy` ([decision D-006](docs/architecture/decisions.md)).

## Layout

```text
CLAUDE.md, MASTER-ARCHITECTURE.md, ...   constitutional documents (see docs/README.md)
docs/            documentation map, baseline, decision log, entity and relationship taxonomies, research
schemas/         JSON Schema for entity records (accepted, S03) and relationship records (accepted, S04)
sessions/        session prompts, prompt registry and session reports
tools/           validators
tests/           unit tests for tools/ and schemas/, with fictional fixtures
.github/         CI
```

## Validate

Requires Python 3.11+. The tools use the standard library only. The tests also need
the pinned test dependencies (decision D-026).

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v   # unit tests
python tools/validate_repo.py             # Gate 0: repository integrity
```

CI runs both on every push and pull request.
