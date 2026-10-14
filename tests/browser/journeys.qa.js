// Browser QA for the S20 research journeys (visual-architecture.md §15; D-106, D-190 to D-193): the entry page, the
// export-control page, the 9 company pages and the 4 place pages, each at 1280 and 375 px.
// Run from anywhere: node tests/browser/journeys.qa.js OUTDIR. Playwright and Chromium come from the environment,
// not the repository (D-106); the screenshots and qa-result.json go to OUTDIR, outside the repository.
// Per page and width: console and page errors; network requests (only the page itself); document overflow and wide
// elements (outside scrolling tables and code); every link reached by Tab, and a visible focus ring; every in-page
// link's target exists; Enter on a timeline mark and on a matrix cell lands on its evidence; every disclosure opens
// from the keyboard; measured contrast on every rendered text node with every disclosure open; a top screenshot.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const OUT = process.argv[2];
const SITE = path.resolve(__dirname, '../../site');

function lum(rgb) {
  const c = rgb.map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
function ratio(a, b) { const [h, l] = [lum(a), lum(b)].sort((x, y) => y - x); return (h + 0.05) / (l + 0.05); }

function pages() {
  const out = [['index', 'index.html'], ['export', 'questions/export-control-texts/index.html']];
  for (const folder of ['companies', 'places']) {
    for (const id of fs.readdirSync(path.join(SITE, folder)).sort()) out.push([`${folder}-${id}`, `${folder}/${id}/index.html`]);
  }
  return out;
}

(async () => {
  const browser = await chromium.launch();
  const report = { chromium: browser.version(), pages: {} };
  for (const [key, rel] of pages()) {
    const url = 'file://' + path.join(SITE, rel);
    report.pages[key] = {};
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
      await page.screenshot({ path: `${OUT}/${key}-${name}-top.png` });
      // keyboard: every visible link (closed disclosures aside) receives focus by Tab, with a visible ring
      // each link is numbered once, so the measure counts distinct links, never repeated focus
      const links = await page.$$eval('a[href]', as => { let n = 0; for (const a of as) { if ((a.offsetParent !== null || a.closest('svg')) && !a.closest('details:not([open])')) a.dataset.qa = String(n++); } return n; });
      const seen = new Set(), ringless = [];
      for (let i = 0; i < links * 2 + 40 && seen.size < links; i++) {
        await page.keyboard.press('Tab');
        const f = await page.evaluate(() => { const e = document.activeElement; if (!e || !e.dataset || e.dataset.qa === undefined) return null; const s = getComputedStyle(e); return { qa: e.dataset.qa, ring: s.outlineStyle !== 'none' || !!e.closest('svg'), text: (e.textContent || '').trim().slice(0, 30) }; });
        if (f && !seen.has(f.qa)) { seen.add(f.qa); if (!f.ring) ringless.push(f.text); }
      }
      const reached = seen.size;
      r.links = links; r.linksReachedByTab = reached; r.focusRingMissing = ringless.slice(0, 5);
      // every in-page fragment has its target
      r.brokenFragments = await page.$$eval('a[href^="#"]', as => as.filter(a => !document.getElementById(a.getAttribute('href').slice(1))).map(a => a.getAttribute('href')));
      // Enter on a timeline mark and on a named matrix cell lands on the evidence panel
      if (key === 'export') {
        r.enter = [];
        for (const sel of ['a.tl-mark', 'a.cell-named', 'a.cell-refused']) {
          const href = await page.$eval(sel, a => a.getAttribute('href'));
          await page.focus(sel);
          await page.keyboard.press('Enter');
          await page.waitForTimeout(40);
          const res = await page.evaluate(h => { const t = document.getElementById(h.slice(1)); const b = t.getBoundingClientRect(); return { hash: location.hash, inView: b.bottom > 0 && b.top < innerHeight }; }, href);
          r.enter.push({ sel, ok: res.hash === href && res.inView });
          await page.evaluate(() => { history.replaceState(null, '', location.pathname); window.scrollTo(0, 0); });
        }
        await (await page.$('#matrix')).screenshot({ path: `${OUT}/${key}-${name}-matrix.png` });
        await (await page.$('#timeline')).screenshot({ path: `${OUT}/${key}-${name}-timeline.png` });
      }
      // every disclosure opens from the keyboard
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
        // SVG text: its fill against the page surface
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
        && r.disclosuresOpenedByKeyboard === r.disclosures && (!r.enter || r.enter.every(x => x.ok));
      report.pages[key][name] = r;
      await ctx.close();
    }
  }
  report.allOk = Object.values(report.pages).every(p => p.desktop.ok && p.mobile.ok);
  fs.writeFileSync(`${OUT}/qa-result.json`, JSON.stringify(report, null, 2) + '\n');
  await browser.close();
  const summary = Object.fromEntries(Object.entries(report.pages).map(([k, v]) => [k, `${v.desktop.ok ? 'ok' : 'FAIL'} / ${v.mobile.ok ? 'ok' : 'FAIL'} (min contrast ${v.desktop.contrastMin}, links ${v.desktop.linksReachedByTab}/${v.desktop.links})`]));
  console.log(JSON.stringify({ chromium: report.chromium, allOk: report.allOk, pages: summary }, null, 1));
})();
