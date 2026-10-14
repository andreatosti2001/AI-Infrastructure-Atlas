# Browser QA

One script per generated page. Each opens the page at 1280 and 375 px and measures what the static checks in
`tests/test_page.py` and `tests/test_insight.py` cannot: console and page errors, network requests, document
overflow and wide elements, the keyboard path to every evidence panel, and the contrast of every rendered text
node. It writes screenshots and `qa-result.json` (or prints the result) to `OUTDIR`.

```bash
node tests/browser/hbm-chain.qa.js   OUTDIR   # site/hbm-chain/index.html
node tests/browser/hbm-insight.qa.js OUTDIR   # site/hbm-insight/index.html
node tests/browser/journeys.qa.js    OUTDIR   # the 15 S20 pages: site/index.html, site/questions/, site/companies/, site/places/
node tests/browser/brief.qa.js       OUTDIR   # the S21 client brief: site/briefs/accelerator-memory/index.html
```

`journeys.qa.js` (S20, D-190) also counts every visible link reached by Tab (distinct links, each with a focus ring),
checks every in-page fragment, presses Enter on a timeline mark and on a matrix cell, and opens every disclosure from
the keyboard. Its `qa-result.json` has `allOk` and one entry per page and width.

`brief.qa.js` (S21, D-203) runs the same measures on the client brief, presses Enter on a diagram mark and on two
matrix cells, and prints the brief on A4 and Letter: it checks that the boundary line, the scope and its limits, the
summary, the evidence and the sources are displayed in print, that the question, the boundary line, the as-of date and
the input digest sit on the first printed page, and it writes both PDFs with their page counts.

Playwright and Chromium come from the environment, never from the repository (D-106), so these scripts run
outside CI; `OUTDIR` must be outside the repository. A change that alters a page runs its script and reports the
result; screenshots are not committed.
