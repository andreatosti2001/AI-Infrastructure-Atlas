// Browser QA for the research view, site/hbm-insight/index.html (visual-architecture.md §12; D-106, D-125, D-132).
// Run from anywhere: node tests/browser/hbm-insight.qa.js OUTDIR. Playwright comes from the pinned package or the
// environment (qa-lib.js, D-212); the screenshots and qa-result.json go to OUTDIR, outside the repository. Any failed
// condition is listed by name and exits non-zero (S22, F-1). QA_BROWSER=firefox or webkit runs the same checks in that
// engine (CI does, for the :has() filter, S22, F-11).
// Checks at 1280 and 375 px: console, page errors and network; document overflow and wide elements; the keyboard
// path to every mark (strip lines, the supplier slot, unit squares); Enter on a unit square lands on its table row;
// the basis filter driven from the keyboard and its effect on the table and the marks; every metric tutorial opened
// from the keyboard; measured contrast on every rendered text node, with the SQL tutorial open; screenshots.
const { engine, verdict, finish, onlyThePage } = require('./qa-lib');
const [ENGINE, browserType] = engine();
const OUT = process.argv[2];
const URL = 'file://' + require('path').resolve(__dirname, '../../site/hbm-insight/index.html');

function lum(rgb) {
  const c = rgb.map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
function ratio(a, b) { const [h, l] = [lum(a), lum(b)].sort((x, y) => y - x); return (h + 0.05) / (l + 0.05); }

(async () => {
  const browser = await browserType.launch();
  const report = {};
  for (const [name, width, height] of [['desktop', 1280, 900], ['mobile', 375, 812]]) {
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: name === 'mobile' ? 2 : 1 });
    const page = await ctx.newPage();
    const consoleMsgs = [], errors = [], requests = [];
    page.on('console', m => consoleMsgs.push(`${m.type()}: ${m.text()}`));
    page.on('pageerror', e => errors.push(String(e)));
    page.on('request', r => requests.push(r.url()));
    await page.goto(URL, { waitUntil: 'load' });
    const r = { console: consoleMsgs, pageErrors: errors, requests };
    r.overflow = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth }));
    r.wideElements = await page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'absolute' && !e.closest('.table-wrap') && !e.closest('pre'); }).slice(0, 10).map(e => e.tagName + '.' + e.className));
    await page.screenshot({ path: `${OUT}/${name}-01-top.png` });
    await (await page.$('#insight')).screenshot({ path: `${OUT}/${name}-02-insight.png` });
    await (await page.$('#visual')).screenshot({ path: `${OUT}/${name}-03-chains.png` });
    // keyboard path: Tab from the top until every mark has had focus
    const marks = await page.$$eval('a[data-mark]', as => as.map(a => a.getAttribute('data-mark') + ':' + a.getAttribute('data-row')));
    const seen = [];
    for (let i = 0; i < 300; i++) {
      await page.keyboard.press('Tab');
      const f = await page.evaluate(() => { const e = document.activeElement; return e && e.getAttribute('data-mark') ? e.getAttribute('data-mark') + ':' + e.getAttribute('data-row') : null; });
      if (f && !seen.includes(f)) seen.push(f);
      if (seen.length === marks.length) { r.tabsToReachAllMarks = i + 1; break; }
    }
    r.marks = marks.length; r.marksReachedByTab = seen.length;
    // a visible focus ring on a strip line
    await page.focus('a[data-mark="strip"]');
    r.focusRing = await page.evaluate(() => getComputedStyle(document.activeElement).outlineStyle + ' ' + getComputedStyle(document.activeElement).outlineWidth);
    // Enter on every unit square lands on its row, highlighted by :target
    r.unitEnter = [];
    for (const m of marks.filter(m => m.startsWith('unit:'))) {
      const row = m.split(':')[1];
      await page.focus(`a[data-mark="unit"][data-row="${row}"]`);
      await page.keyboard.press('Enter');
      await page.waitForTimeout(40);
      const res = await page.evaluate((row) => { const t = document.getElementById('row-' + row); const b = t.getBoundingClientRect(); return { hash: location.hash, inView: b.bottom > 0 && b.top < innerHeight, target: t.matches(':target') }; }, row);
      r.unitEnter.push({ row, ok: res.hash === '#row-' + row && res.inView && res.target });
      await page.evaluate(() => { history.replaceState(null, '', location.pathname); window.scrollTo(0, 0); });
    }
    // S15: every "How this was computed" opens from the keyboard, and each metric block's link lands on its tutorial
    r.tutorials = [];
    for (const id of await page.$$eval('details.sql-tutorial', ds => ds.map(d => d.getAttribute('data-query')))) {
      await page.focus(`details.sql-tutorial[data-query="${id}"] > summary`);
      await page.keyboard.press('Enter');
      r.tutorials.push({ query: id, opened: await page.$eval(`details.sql-tutorial[data-query="${id}"]`, d => d.open) });
    }
    r.howLinks = await page.$$eval('a.how-link', as => as.map(a => { const t = document.querySelector(a.getAttribute('href')); return !!t; }));
    r.wideWithTutorialsOpen = await page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'absolute' && !e.closest('.table-wrap'); }).slice(0, 10).map(e => e.tagName + '.' + e.className));
    await (await page.$('#method')).screenshot({ path: `${OUT}/${name}-06-method-tutorials-open.png` });
    await page.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = false; }));
    // the filter, from the keyboard: focus "all links", arrow right four times (stated, inferred, reported, gap)
    r.filter = [];
    await page.focus('#f-all');
    for (const basis of ['stated', 'inferred', 'reported', 'gap']) {
      await page.keyboard.press('ArrowRight');
      const res = await page.evaluate((basis) => {
        const rows = [...document.querySelectorAll('tr[data-basis]')];
        const shown = rows.filter(t => getComputedStyle(t).display !== 'none').map(t => t.dataset.basis);
        const marks = [...document.querySelectorAll('[data-mark][data-basis]')];
        const outlined = marks.filter(m => getComputedStyle(m).outlineStyle === 'solid').map(m => m.dataset.basis);
        return { checked: document.querySelector('input[name=basis]:checked').value, rowsShown: shown.length, rowsAllMatch: shown.every(b => b === basis), rowsExpected: rows.filter(t => t.dataset.basis === basis).length, marksOutlined: outlined.length, outlinedAllMatch: outlined.every(b => b === basis), marksExpected: marks.filter(m => m.dataset.basis === basis).length };
      }, basis);
      r.filter.push({ basis, ...res, ok: res.checked === basis && res.rowsAllMatch && res.rowsShown === res.rowsExpected && res.outlinedAllMatch && res.marksOutlined === res.marksExpected });
      if (basis === 'gap' || basis === 'reported') await (await page.$('#visual')).screenshot({ path: `${OUT}/${name}-04-filter-${basis}.png` });
    }
    await page.keyboard.press('ArrowRight'); // wraps to "all links"
    r.filterBackToAll = await page.evaluate(() => ({ checked: document.querySelector('input[name=basis]:checked').value, rowsHidden: [...document.querySelectorAll('tr[data-basis]')].filter(t => getComputedStyle(t).display === 'none').length }));
    // contrast on every rendered text node, with every disclosure open
    await page.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
    await (await page.$('#data')).screenshot({ path: `${OUT}/${name}-05-table-tutorial-open.png` });
    r.contrast = await page.evaluate(() => {
      const parse = s => (s.match(/\d+(\.\d+)?/g) || []).slice(0, 4).map(Number);
      function bg(el) { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c.length === 3 || (c.length === 4 && c[3] > 0)) return c.slice(0, 3); } return [255, 255, 255]; }
      const out = []; const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const n = walker.currentNode; if (!n.textContent.trim()) continue;
        const el = n.parentElement; const st = getComputedStyle(el);
        if (st.display === 'none' || st.visibility === 'hidden' || el.closest('.vh') || el.closest('style')) continue;
        out.push({ fg: parse(st.color).slice(0, 3), bg: bg(el), text: n.textContent.trim().slice(0, 30) });
      }
      return out;
    });
    const ratios = r.contrast.map(c => ({ ...c, ratio: ratio(c.fg, c.bg) }));
    r.contrastMin = Math.min(...ratios.map(c => c.ratio)).toFixed(2);
    r.contrastBelow45 = ratios.filter(c => c.ratio < 4.5).map(c => c.text);
    r.contrastTexts = ratios.length;
    delete r.contrast;
    r.wideElementsOpen = await page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'absolute' && !e.closest('.table-wrap'); }).slice(0, 10).map(e => e.tagName + '.' + e.className));
    report[name] = r;
    await ctx.close();
  }
  report.engine = `${ENGINE} ${browser.version()}`;
  await browser.close();
  const { failures, check } = verdict();
  for (const name of ['desktop', 'mobile']) {
    const r = report[name];
    check(`${name}: console messages`, !r.console.length, r.console);
    check(`${name}: page errors`, !r.pageErrors.length, r.pageErrors);
    check(`${name}: requests other than the page`, !onlyThePage(r.requests, URL).length, onlyThePage(r.requests, URL));
    check(`${name}: document overflow`, r.overflow.scrollWidth <= r.overflow.clientWidth, r.overflow);
    check(`${name}: wide elements`, !r.wideElements.length, r.wideElements);
    check(`${name}: marks reached by Tab`, r.marksReachedByTab === r.marks, `${r.marksReachedByTab} of ${r.marks}`);
    check(`${name}: a visible focus ring`, !/^none/.test(r.focusRing), r.focusRing);
    check(`${name}: Enter on a unit square lands on its row`, r.unitEnter.every(x => x.ok), r.unitEnter.filter(x => !x.ok));
    check(`${name}: every tutorial opens from the keyboard`, r.tutorials.every(x => x.opened), r.tutorials.filter(x => !x.opened));
    check(`${name}: every "how" link has its target`, r.howLinks.every(Boolean));
    check(`${name}: wide elements with the tutorials open`, !r.wideWithTutorialsOpen.length, r.wideWithTutorialsOpen);
    check(`${name}: the basis filter from the keyboard`, r.filter.every(f => f.ok), r.filter.filter(f => !f.ok));
    check(`${name}: the filter back to all links`, r.filterBackToAll.checked === 'all' && r.filterBackToAll.rowsHidden === 0, r.filterBackToAll);
    check(`${name}: text below 4.5:1 contrast`, !r.contrastBelow45.length, r.contrastBelow45);
    check(`${name}: wide elements with every disclosure open`, !r.wideElementsOpen.length, r.wideElementsOpen);
  }
  const summary = {};
  for (const k of ['desktop', 'mobile']) summary[k] = `marks ${report[k].marksReachedByTab}/${report[k].marks}, filter ${report[k].filter.filter(f => f.ok).length}/4, min contrast ${report[k].contrastMin}`;
  finish(OUT, report, failures, { engine: report.engine, ...summary });
})();
