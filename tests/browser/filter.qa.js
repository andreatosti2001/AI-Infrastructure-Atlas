// The research view's basis filter in each browser engine (S22, engineering audit F-11; D-196, D-200).
// Run from anywhere: node tests/browser/filter.qa.js OUTDIR. QA_BROWSERS lists the engines (default
// "chromium firefox webkit"; CI installs all three with the pinned Playwright, a session usually has Chromium only).
// Per engine at 1280 px: where the engine supports `:has()`, choosing each basis (by clicking its radio) shows exactly
// that basis's table rows and outlines exactly its marks, and "all links" shows every row again; where it does not,
// the filter is hidden (the @supports guard) and every row stays shown. An engine that cannot start is a failure, never
// a skip. Every failed condition is listed by name and exits non-zero (qa-lib.js).
const path = require('path');
const { playwright, verdict, finish } = require('./qa-lib');
const OUT = process.argv[2];
const URL = 'file://' + path.resolve(__dirname, '../../site/hbm-insight/index.html');
const ENGINES = (process.env.QA_BROWSERS || 'chromium firefox webkit').split(/\s+/).filter(Boolean);

(async () => {
  const pw = playwright();
  const report = { engines: {} };
  const { failures, check } = verdict();
  for (const name of ENGINES) {
    const r = {};
    report.engines[name] = r;
    let browser;
    try {
      browser = await pw[name].launch();
    } catch (e) {
      check(`${name}: the engine starts`, false, String(e).split('\n')[0]);
      continue;
    }
    r.version = browser.version();
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(URL, { waitUntil: 'load' });
    r.hasSupported = await page.evaluate(() => CSS.supports('selector(:has(*))'));
    r.filterShown = await page.evaluate(() => getComputedStyle(document.querySelector('fieldset.filter')).display !== 'none');
    const state = basis => page.evaluate(basis => {
      const rows = [...document.querySelectorAll('tr[data-basis]')];
      const shown = rows.filter(t => getComputedStyle(t).display !== 'none').map(t => t.dataset.basis);
      const marks = [...document.querySelectorAll('[data-mark][data-basis]')];
      const outlined = marks.filter(m => getComputedStyle(m).outlineStyle === 'solid').map(m => m.dataset.basis);
      return { rows: rows.length, shown: shown.length, shownMatch: basis === 'all' ? shown.length === rows.length : shown.every(b => b === basis) && shown.length === rows.filter(t => t.dataset.basis === basis).length,
               outlined: outlined.length, outlinedMatch: basis === 'all' ? outlined.length === 0 : outlined.every(b => b === basis) && outlined.length === marks.filter(m => m.dataset.basis === basis).length };
    }, basis);
    if (r.hasSupported) {
      check(`${name}: the filter is shown where :has() works`, r.filterShown);
      r.bases = {};
      for (const basis of ['stated', 'inferred', 'reported', 'gap', 'all']) {
        await page.check(`#f-${basis}`);
        const s = await state(basis);
        r.bases[basis] = s;
        check(`${name}: "${basis}" shows exactly its rows`, s.shownMatch, s);
        check(`${name}: "${basis}" outlines exactly its marks`, s.outlinedMatch, s);
      }
      await page.screenshot({ path: `${OUT}/${name}-filter-all.png` });
    } else {
      const s = await state('all');
      r.withoutHas = s;
      check(`${name}: the filter is hidden where :has() does not work`, !r.filterShown);
      check(`${name}: every row is shown where :has() does not work`, s.shownMatch, s);
    }
    check(`${name}: page errors`, !errors.length, errors);
    await browser.close();
  }
  const summary = Object.fromEntries(Object.entries(report.engines).map(([k, v]) => [k, v.version ? `${v.version}, :has() ${v.hasSupported ? 'supported' : 'unsupported'}` : 'did not start']));
  finish(OUT, report, failures, summary);
})();
