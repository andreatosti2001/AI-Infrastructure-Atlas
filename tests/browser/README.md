# Browser QA

One script per generated page. Each opens the page at 1280 and 375 px and measures what the static checks in
`tests/test_page.py` and `tests/test_insight.py` cannot: console and page errors, network requests, document
overflow and wide elements, the keyboard path to every evidence panel, and the contrast of every rendered text
node. It writes screenshots and `qa-result.json` (or prints the result) to `OUTDIR`.

```bash
node tests/browser/hbm-chain.qa.js   OUTDIR   # site/hbm-chain/index.html
node tests/browser/hbm-insight.qa.js OUTDIR   # site/hbm-insight/index.html
```

Playwright and Chromium come from the environment, never from the repository (D-106), so these scripts run
outside CI; `OUTDIR` must be outside the repository. A change that alters a page runs its script and reports the
result; screenshots are not committed.
