# AI-Infrastructure-Atlas
Evidence-backed intelligence system mapping the infrastructure, supply chains, companies, technologies, and strategic dependencies underlying the global AI ecosystem.

## Status

**M0 — Project Constitution.** The repository contains governance documents, the session
system and a repository-integrity check. It contains **no data, schemas or UI yet**. See
[`docs/architecture/baseline.md`](docs/architecture/baseline.md) for what exists and what is
planned.

This is an independent repository. It shares no code, data or runtime with
`Eu-Digital-Policy` ([decision D-006](docs/architecture/decisions.md)).

## Layout

```text
CLAUDE.md, MASTER-ARCHITECTURE.md, ...   constitutional documents (see docs/README.md)
docs/            documentation map, baseline architecture record, decision log
sessions/        session prompts, prompt registry and session reports
tools/           validators
tests/           unit tests for tools/
.github/         CI
```

## Validate

Requires Python 3.11+. No third-party packages are needed.

```bash
python -m unittest discover -s tests -v   # unit tests
python tools/validate_repo.py             # Gate 0: repository integrity
```

CI runs both on every push and pull request.
