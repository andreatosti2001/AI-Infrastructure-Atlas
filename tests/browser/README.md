# Browser QA

One script per generated page. Each opens the page at 1280 and 375 px and measures what the static checks in
`tests/test_page.py` and `tests/test_insight.py` cannot: console and page errors, network requests, document
overflow and wide elements, the keyboard path to every evidence panel, and the contrast of every rendered text
node. It writes screenshots and `qa-result.json` to `OUTDIR`. **Every script lists each failed condition by name and
exits non-zero** (S22, engineering audit F-1, D-212); before S22 they always exited 0.

```bash
npm ci                                            # the pinned Playwright (package.json, package-lock.json; D-212)
npx playwright install chromium firefox webkit    # its browsers (CI); a session uses /opt/pw-browsers' Chromium instead
node tests/browser/hbm-chain.qa.js   OUTDIR   # site/hbm-chain/index.html
node tests/browser/hbm-insight.qa.js OUTDIR   # site/hbm-insight/index.html
node tests/browser/journeys.qa.js    OUTDIR   # the 15 S20 pages: site/index.html, site/questions/, site/companies/, site/places/
node tests/browser/brief.qa.js       OUTDIR   # the S21 client brief: site/briefs/accelerator-memory/index.html
QA_BROWSERS="chromium firefox webkit" node tests/browser/filter.qa.js OUTDIR   # the research view's filter per engine (F-11)
```

**At a published address** (S25, D-227): with `QA_BASE_URL` set to the address the repository is served at, each
script opens the same page under it (`site/<page>`) and runs the same measures; the publication workflow
(`.github/workflows/pages.yml`) does this after each deployment, beside `tools/check_published.py`, which compares every
page and every file the pages link to with the commit, byte for byte.

```bash
QA_BASE_URL=https://andreatosti2001.github.io/AI-Infrastructure-Atlas/ node tests/browser/brief.qa.js OUTDIR
```

`journeys.qa.js` (S20, D-190) also counts every visible link reached by Tab (distinct links, each with a focus ring),
checks every in-page fragment, presses Enter on a timeline mark and on a matrix cell, and opens every disclosure from
the keyboard. Its `qa-result.json` has `allOk` and one entry per page and width.

`brief.qa.js` (S21, D-203) runs the same measures on the client brief, presses Enter on a diagram mark and on two
matrix cells, and prints the brief on A4 and Letter: it checks that the boundary line, the scope and its limits, the
summary, the evidence and the sources are displayed in print, that the question, the boundary line, the as-of date and
the input digest sit on the first printed page, and it writes both PDFs with their page counts.

`filter.qa.js` (S22, F-11) checks the research view's basis filter in each engine listed in `QA_BROWSERS`: where
`:has()` works, each basis shows exactly its rows and outlines exactly its marks; where it does not, the filter is
hidden and every row stays shown (D-200). An engine that cannot start is a failure, never a skip.

**Where Playwright comes from** (`qa-lib.js`): the repository's pinned package when `npm ci` has installed it (CI), or
else the session environment's copy in `/opt/node-tools` (D-106 as amended by D-212). **CI** runs every script on every
push in the `browser` job of `.github/workflows/ci.yml`, with Chromium for the four page scripts and Chromium, Firefox
and WebKit for the filter. `OUTDIR` must be outside the repository; screenshots are not committed. A change that
alters a page also runs its script in the session and reports the result.
