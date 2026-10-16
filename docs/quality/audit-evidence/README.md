# Audit evidence

The material that accepted audits cite for their measured findings. Each item records what the audit read or
ran **at its base commit**; it is evidence for that audit, not a live check, so a re-run on today's data may
differ (the scripts record the hashes of their inputs to show this). Live checks are in `tests/`.

| Folder | Audit | Holds |
|---|---|---|
| [`content-audit/`](content-audit/) | [content and evidence depth audit](../../research/content-audit.md) | the sampling script and the drawn sample; the re-read script and the result per citation, with the SHA-256 of the bytes read |
| [`analytical-audit/`](analytical-audit/) | [analytical depth audit](../../architecture/analytical-audit.md) | `cold-reading/`: the form, the visible text the readers were given and both readers' answers; `reproduction/`: the plain definitions, the independent script and its output; `probes/`: the sensitivity probes and their output |
| [`engineering-audit/`](engineering-audit/) | [engineering audit](../../architecture/engineering-audit.md) | the measurement script (sizes, functions, imports, record IDs in code, labels, duplication, rule-to-test names, breaks, determinism, pages, security, Git) and its output; the standard-library coverage tracer and its output; the browser measurement of six pages at five widths and of screenshot stability, and its output; the break-to-module map; the reproducibility record (compile on 3.11, builds on 3.12 and 3.13, pins) |
| [`release-content-audit/`](release-content-audit/) | [release content audit](../../research/release-content-audit.md) (S23) | the sampling script and the sample; the retrieval script and log (host, time, status, hash per request); the re-read script (PDF text by the machine's `pdftotext`, H-1) and its result per citation, with the hashes of the bytes and of the extracted text; the verdict per sampled claim; the measurement script and its output for the roadmap's seven points |
| [`portfolio-audit/`](portfolio-audit/) | [portfolio and capability audit](../../architecture/portfolio-audit.md) (S24) | the measurement script (the eight capability points from the records, checks and pages; PEF §4's retrospective from the Git history; counts only from the private archive) and its output, with the commits and the SHA-256 of every file read; the repository's merged pull requests (opening and merge times, reviews and comments); `cold-reading/`: the form, the four artifacts the two fresh readers were given, and their answers as given |
