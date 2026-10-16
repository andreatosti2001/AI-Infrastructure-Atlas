// Browser QA for the S21 client brief (docs/architecture/client-brief.md; D-106, D-202, D-203):
// site/briefs/accelerator-memory/index.html at 1280 and 375 px, and printed on A4 and Letter.
// Run from anywhere: node tests/browser/brief.qa.js OUTDIR. Playwright comes from the pinned package or the
// environment (qa-lib.js, D-212); the screenshots, the two PDFs and qa-result.json go to OUTDIR, outside the repository.
// Per width (as journeys.qa.js): console and page errors; network requests (only the page itself); document overflow
// and wide elements (outside scrolling tables and code); every link reached by Tab, with a visible focus ring; every
// in-page link's target exists; Enter on a diagram mark and on a matrix cell lands on its evidence; every disclosure
// opens from the keyboard; measured contrast on every rendered text node with every disclosure open; screenshots.
// In print (U-5): the boundary line, the scope section, the summary, the evidence (as one list of claims, S22, D-210;
// the panels hidden) and the sources are displayed; the
// first printed page carries the question, the boundary line, the as-of date and the input digest; the PDF's page
// count on A4 and Letter.
const { playwright, pageUrl, verdict, finish, widthChecks } = require('./qa-lib');
const { chromium } = playwright();
const fs = require('fs');
const OUT = process.argv[2];

function lum(rgb) {
  const c = rgb.map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
function ratio(a, b) { const [h, l] = [lum(a), lum(b)].sort((x, y) => y - x); return (h + 0.05) / (l + 0.05); }

(async () => {
  const browser = await chromium.launch();
  const url = pageUrl('briefs/accelerator-memory/index.html');
  const report = { chromium: browser.version(), widths: {}, print: {} };
  for (const [name, width, height] of [['desktop', 1280, 900], ['mobile', 375, 812]]) {
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: name === 'mobile' ? 2 : 1 });
    const page = await ctx.newPage();
    const consoleMsgs = [], errors = [], requests = [];
    page.on('console', m => consoleMsgs.push(`${m.type()}: ${m.text()}`));
    page.on('pageerror', e => errors.push(String(e)));
    page.on('request', r => requests.push(r.url()));
    await page.goto(url, { waitUntil: 'load' });
    const r = { console: consoleMsgs, pageErrors: errors };
    r.foreignRequests = requests.filter(u => u.split('#')[0] !== url);
    const wide = () => page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'absolute' && !e.closest('.table-wrap') && !e.closest('pre'); }).slice(0, 10).map(e => e.tagName + '.' + e.className));
    r.overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    r.wideElements = await wide();
    await page.screenshot({ path: `${OUT}/brief-${name}-top.png` });
    for (const id of ['summary', 'map', 'texts', 'gaps', 'sources']) {
      // the section's top in the viewport: a screenshot of the whole page or of a long section never settles
      await page.$eval('#' + id, e => window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY));
      await page.screenshot({ path: `${OUT}/brief-${name}-${id}.png` });
    }
    await page.evaluate(() => window.scrollTo(0, 0));
    const links = await page.$$eval('a[href]', as => { let n = 0; for (const a of as) { if ((a.offsetParent !== null || a.closest('svg')) && !a.closest('details:not([open])')) a.dataset.qa = String(n++); } return n; });
    const seen = new Set(), ringless = [];
    for (let i = 0; i < links * 2 + 40 && seen.size < links; i++) {
      await page.keyboard.press('Tab');
      const f = await page.evaluate(() => { const e = document.activeElement; if (!e || !e.dataset || e.dataset.qa === undefined) return null; const s = getComputedStyle(e); return { qa: e.dataset.qa, ring: s.outlineStyle !== 'none' || !!e.closest('svg'), text: (e.textContent || '').trim().slice(0, 30) }; });
      if (f && !seen.has(f.qa)) { seen.add(f.qa); if (!f.ring) ringless.push(f.text); }
    }
    r.links = links; r.linksReachedByTab = seen.size; r.focusRingMissing = ringless.slice(0, 5);
    r.brokenFragments = await page.$$eval('a[href^="#"]', as => as.filter(a => !document.getElementById(a.getAttribute('href').slice(1))).map(a => a.getAttribute('href')));
    r.enter = [];
    for (const sel of ['svg.chain a.mark', 'a.cell-named', 'a.cell-refused']) {
      const href = await page.$eval(sel, a => a.getAttribute('href'));
      await page.focus(sel);
      await page.keyboard.press('Enter');
      await page.waitForTimeout(40);
      const res = await page.evaluate(h => { const t = document.getElementById(h.slice(1)); const b = t.getBoundingClientRect(); return { hash: location.hash, inView: b.bottom > 0 && b.top < innerHeight }; }, href);
      r.enter.push({ sel, ok: res.hash === href && res.inView });
      await page.evaluate(() => { history.replaceState(null, '', location.pathname); window.scrollTo(0, 0); });
    }
    const summaries = await page.$$eval('details > summary', s => s.length);
    let opened = 0;
    for (let i = 0; i < summaries; i++) {
      const s = (await page.$$('details > summary'))[i];
      if (!(await s.isVisible())) continue;
      await s.focus();
      await page.keyboard.press('Enter');
      if (await s.evaluate(e => e.parentElement.open)) opened++;
    }
    r.disclosures = summaries; r.disclosuresOpenedByKeyboard = opened;
    await page.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
    const contrast = await page.evaluate(() => {
      const parse = s => (s.match(/\d+(\.\d+)?/g) || []).slice(0, 4).map(Number);
      function bg(el) { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c.length === 3 || (c.length === 4 && c[3] > 0)) return c.slice(0, 3); } return [255, 255, 255]; }
      const out = []; const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const n = walker.currentNode; if (!n.textContent.trim()) continue;
        const el = n.parentElement; const st = getComputedStyle(el);
        if (st.display === 'none' || st.visibility === 'hidden' || el.closest('style') || el.closest('svg')) continue;
        out.push({ fg: parse(st.color).slice(0, 3), bg: bg(el), text: n.textContent.trim().slice(0, 30) });
      }
      for (const t of document.querySelectorAll('svg text')) out.push({ fg: parse(getComputedStyle(t).fill).slice(0, 3), bg: bg(t.closest('svg')), text: t.textContent.trim().slice(0, 30) });
      return out;
    });
    const ratios = contrast.map(c => ({ ...c, ratio: ratio(c.fg, c.bg) }));
    r.contrastTexts = ratios.length;
    r.contrastMin = Math.min(...ratios.map(c => c.ratio)).toFixed(2);
    r.contrastBelow45 = ratios.filter(c => c.ratio < 4.5).map(c => c.text).slice(0, 10);
    r.wideElementsOpen = await wide();
    r.ok = !consoleMsgs.length && !errors.length && !r.foreignRequests.length && r.overflow <= 0 && !r.wideElements.length && !r.wideElementsOpen.length
      && r.linksReachedByTab >= r.links && !r.focusRingMissing.length && !r.brokenFragments.length && !r.contrastBelow45.length
      && r.disclosuresOpenedByKeyboard === r.disclosures && r.enter.every(x => x.ok);
    report.widths[name] = r;
    await ctx.close();
  }
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'load' });
    report.screenListHidden = await page.evaluate(() => getComputedStyle(document.querySelector('#evidence-print')).display === 'none');
    await ctx.close();
  }
  // print: what U-5 says must travel is displayed; the first page; the PDF on A4 and Letter
  for (const format of ['A4', 'Letter']) {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'load' });
    await page.emulateMedia({ media: 'print' });
    const p = {};
    p.displayed = await page.evaluate(() => Object.fromEntries(['[data-boundary]', '#scope', '[data-limits]', '[data-identity]', '#summary', '#map svg.chain', '#texts table', '#evidence-print', '#sources', '[data-citation]']
      .map(sel => { const e = document.querySelector(sel); return [sel, !!e && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0]; })));
    // S22 (D-210, BR-13): in print the appendix's panels give way to the list of claims, each once
    p.panelsHidden = await page.evaluate(() => getComputedStyle(document.querySelector('#evidence')).display === 'none');
    p.listItems = await page.$$eval('#evidence-print li[data-claim]', ls => ls.length);
    const file = `${OUT}/brief-${format}.pdf`;
    await page.pdf({ path: file, format, printBackground: true, preferCSSPageSize: false });
    const pdf = fs.readFileSync(file, 'latin1');
    p.pages = (pdf.match(/\/Type\s*\/Page[^s]/g) || []).length;
    p.bytes = fs.statSync(file).size;
    // the first printed page, as an image: the viewport set to the paper's width at 96 dpi
    const [w, h] = format === 'A4' ? [794, 1123] : [816, 1056];
    await page.setViewportSize({ width: w, height: h });
    await page.screenshot({ path: `${OUT}/brief-print-${format}-first.png` });
    p.firstPage = await page.evaluate(hgt => {
      const inFirst = sel => { const e = document.querySelector(sel); if (!e) return false; const b = e.getBoundingClientRect(); return b.top >= 0 && b.top < hgt; };
      return { h1: inFirst('h1'), boundary: inFirst('[data-boundary]'), asOf: inFirst('[data-identity]') || inFirst('[data-column="reference_date"]'), digest: inFirst('[data-identity] .digest') };
    }, h - 2 * 16 * 3.78);
    p.ok = Object.values(p.displayed).every(Boolean) && p.pages > 0 && Object.values(p.firstPage).every(Boolean);
    report.print[format] = p;
    await ctx.close();
  }
  await browser.close();
  const { failures, check } = verdict();
  for (const [name, r] of Object.entries(report.widths)) widthChecks(check, name, r);
  check('screen: the print-only evidence list shows on screen', report.screenListHidden);
  for (const [format, p] of Object.entries(report.print)) {
    check(`print ${format}: hidden in print`, Object.values(p.displayed).every(Boolean), Object.keys(p.displayed).filter(k => !p.displayed[k]));
    check(`print ${format}: no PDF pages`, p.pages > 0, p.pages);
    check(`print ${format}: the evidence panels print beside the list`, p.panelsHidden);
    check(`print ${format}: the printed evidence list is empty`, p.listItems > 0, p.listItems);
    check(`print ${format}: missing from the first printed page`, Object.values(p.firstPage).every(Boolean), Object.keys(p.firstPage).filter(k => !p.firstPage[k]));
  }
  const w = report.widths;
  finish(OUT, report, failures, {
    chromium: report.chromium,
    desktop: `${w.desktop.ok ? 'ok' : 'FAIL'} (min contrast ${w.desktop.contrastMin}, links ${w.desktop.linksReachedByTab}/${w.desktop.links}, overflow ${w.desktop.overflow})`,
    mobile: `${w.mobile.ok ? 'ok' : 'FAIL'} (min contrast ${w.mobile.contrastMin}, links ${w.mobile.linksReachedByTab}/${w.mobile.links}, overflow ${w.mobile.overflow}, wide ${w.mobile.wideElements.join(' ')})`,
    print: Object.fromEntries(Object.entries(report.print).map(([k, v]) => [k, `${v.ok ? 'ok' : 'FAIL'} ${v.pages} pages; first page ${JSON.stringify(v.firstPage)}`])),
  });
})();
