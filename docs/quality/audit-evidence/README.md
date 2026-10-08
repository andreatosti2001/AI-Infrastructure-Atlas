# Audit evidence

The material that accepted audits cite for their measured findings. Each item records what the audit read or
ran **at its base commit**; it is evidence for that audit, not a live check, so a re-run on today's data may
differ (the scripts record the hashes of their inputs to show this). Live checks are in `tests/`.

| Folder | Audit | Holds |
|---|---|---|
| [`content-audit/`](content-audit/) | [content and evidence depth audit](../../research/content-audit.md) | the sampling script and the drawn sample; the re-read script and the result per citation, with the SHA-256 of the bytes read |
| [`analytical-audit/`](analytical-audit/) | [analytical depth audit](../../architecture/analytical-audit.md) | `cold-reading/`: the form, the visible text the readers were given and both readers' answers; `reproduction/`: the plain definitions, the independent script and its output; `probes/`: the sensitivity probes and their output |
