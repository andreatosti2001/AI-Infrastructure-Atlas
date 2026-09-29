# Session system

Governed Opus sessions follow `SESSION-PROMPT-SPEC.md`. This file only records where
things live and what is checked automatically.

```text
sessions/
├── prompts/
│   ├── PROMPT-REGISTRY.md     # index of all session prompts
│   └── SNN-PROMPT.md          # verbatim session prompt, immutable once the session starts
└── reports/
    └── SESSION-NN-REPORT.md   # mandatory end-of-session report
```

## Lifecycle

1. The human adds `sessions/prompts/SNN-PROMPT.md` and lists it in `PROMPT-REGISTRY.md`.
2. The session reads the constitutional documents, the previous report and the prompt.
3. The session ends with `sessions/reports/SESSION-NN-REPORT.md`.
4. Deviations go in the report and in `docs/architecture/decisions.md`. Prompts are never
   edited after the session starts (`SESSION-PROMPT-SPEC.md` §6).

## Enforced by `tools/validate_repo.py`

- prompt and report filenames follow the patterns above;
- every prompt is listed in the registry;
- every report has a matching prompt;
- every report contains the `SESSION-PROMPT-SPEC.md` §5 minimum fields as `##` headings:
  Mission outcome · Files changed · Data changed · Tests run · Evidence added/retired ·
  Decisions made · Deviations · Debt introduced/resolved · Unresolved issues ·
  Process lessons · Implications for the next session.

The validator checks that these sections exist, not what they say. Whether the content is
good enough is a human review.
