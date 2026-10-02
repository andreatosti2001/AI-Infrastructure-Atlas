// Run: node qa.js OUTDIR (Playwright from the environment, not the repository; H-3, D-106).
// S12 re-run of the S11 browser QA (D-106; only the Playwright path changed: /opt/node22 no longer carries it).
// S11 browser QA (H-3, D-106): scratch Playwright with the pre-installed Chromium; no repository dependency.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const OUT = process.argv[2];
const URL = 'file:///home/user/AI-Infrastructure-Atlas/site/hbm-chain/index.html';

function lum(rgb) {
  const c = rgb.map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
function ratio(a, b) { const [h, l] = [lum(a), lum(b)].sort((x, y) => y - x); return (h + 0.05) / (l + 0.05); }

(async () => {
  const browser = await chromium.launch();
  const report = {};
  for (const [name, width, height] of [['desktop', 1280, 900], ['mobile', 375, 812]]) {
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: name === 'mobile' ? 2 : 1 });
    const page = await ctx.newPage();
    const consoleMsgs = [], errors = [], requests = [];
    page.on('console', m => consoleMsgs.push(`${m.type()}: ${m.text()}`));
    page.on('pageerror', e => errors.push(String(e)));
    page.on('request', r => requests.push(r.url()));
    await page.goto(URL, { waitUntil: 'load' });
    const r = { console: consoleMsgs, pageErrors: errors };
    r.requests = requests;
    r.overflow = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth }));
    r.wideElements = await page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'absolute' && !e.closest('.table-wrap') && !e.closest('pre'); }).slice(0, 10).map(e => e.tagName + '.' + e.className));
    r.svgScale = await page.evaluate(() => { const s = document.querySelector('svg.chain'); return s.getBoundingClientRect().width / s.viewBox.baseVal.width; });
    r.minSvgFontPx = await page.evaluate(() => { const s = document.querySelector('svg.chain'); const k = s.getBoundingClientRect().width / s.viewBox.baseVal.width; return Math.min(...[...s.querySelectorAll('text')].map(t => parseFloat(getComputedStyle(t).fontSize) * k)); });
    // screenshots
    await page.screenshot({ path: `${OUT}/${name}-01-top.png` });
    await (await page.$('#chain')).screenshot({ path: `${OUT}/${name}-02-chain.png` });
    await (await page.$('#gaps')).screenshot({ path: `${OUT}/${name}-03-gaps.png` });
    // keyboard path: Tab from the top until every mark has had focus
    const marks = await page.$$eval('a[data-mark]', as => as.map(a => a.getAttribute('data-mark') + ' ' + a.getAttribute('data-target')));
    const seen = []; let first = null;
    for (let i = 0; i < 400; i++) {
      await page.keyboard.press('Tab');
      const f = await page.evaluate(() => { const e = document.activeElement; return e ? { tag: e.tagName, mark: e.getAttribute('data-mark') ? e.getAttribute('data-mark') + ' ' + e.getAttribute('data-target') : null, href: e.getAttribute('href') } : null; });
      if (i === 0) first = f;
      if (f && f.mark && !seen.includes(f.mark)) seen.push(f.mark);
      if (seen.length === marks.length) { r.tabsToReachAllMarks = i + 1; break; }
    }
    r.firstTabStop = first;
    r.marks = marks.length; r.marksReachedByTab = seen.length; r.tabOrder = seen;
    // Enter on every mark lands on its panel, in view, with the panel highlighted by :target
    r.enter = [];
    for (const m of marks) {
      const target = m.split(' ')[1];
      await page.focus(`a[data-mark][data-target="${target}"]`);
      await page.keyboard.press('Enter');
      await page.waitForTimeout(60);
      const res = await page.evaluate((t) => { const p = document.getElementById('ev-' + t); const b = p.getBoundingClientRect(); return { hash: location.hash, inView: b.top >= -2 && b.top < innerHeight, targetMatch: p.matches(':target') }; }, target);
      r.enter.push({ mark: m, ok: res.hash === '#ev-' + target && res.inView && res.targetMatch });
      if (target.startsWith('rel-component')) await page.screenshot({ path: `${OUT}/${name}-04-panel-after-enter.png` });
      await page.evaluate(() => { history.replaceState(null, '', location.pathname); window.scrollTo(0, 0); });
    }
    // a disclosure opens from the keyboard
    await page.focus('#ev-rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking details.inputs summary');
    await page.keyboard.press('Enter');
    r.disclosureOpensByKeyboard = await page.$eval('#ev-rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking details.inputs', d => d.open);
    // skip link
    await page.goto(URL); await page.keyboard.press('Tab'); await page.keyboard.press('Enter');
    r.skipLink = await page.evaluate(() => location.hash);
    // measured contrast of every rendered text node against its painted background
    const samples = await page.evaluate(() => {
      const parse = c => (c.match(/[\d.]+/g) || []).map(Number);
      const out = [];
      const bgOf = el => {
        for (let e = el; e; e = e.parentElement) {
          const bg = getComputedStyle(e).backgroundColor; const v = parse(bg);
          if (v.length >= 3 && (v.length === 3 || v[3] > 0)) return v.slice(0, 3);
        }
        return [255, 255, 255];
      };
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        if (!n.textContent.trim()) continue;
        const el = n.parentElement; if (!el || el.closest('style')) continue;
        const svgText = el.closest('text');
        let fg, bg;
        if (svgText) {
          fg = parse(getComputedStyle(svgText).fill).slice(0, 3);
          bg = bgOf(svgText.ownerSVGElement);
          const tb = svgText.getBBox();
          const a = svgText.closest('a, g');
          for (const rect of (a ? a.querySelectorAll('rect.box, rect.pill') : [])) {
            const rb = rect.getBBox();
            if (tb.x >= rb.x - 1 && tb.y >= rb.y - 1 && tb.x + tb.width <= rb.x + rb.width + 1 && tb.y + tb.height <= rb.y + rb.height + 1) {
              const f = parse(getComputedStyle(rect).fill); if (f.length >= 3) bg = f.slice(0, 3);
            }
          }
        } else {
          fg = parse(getComputedStyle(el).color).slice(0, 3); bg = bgOf(el);
        }
        out.push({ text: n.textContent.trim().slice(0, 40), fg, bg, size: parseFloat(getComputedStyle(svgText || el).fontSize), svg: !!svgText });
      }
      return out;
    });
    const measured = samples.map(s => ({ ...s, ratio: ratio(s.fg, s.bg) }));
    r.textNodesMeasured = measured.length;
    r.minContrast = measured.reduce((m, s) => s.ratio < m.ratio ? s : m);
    r.belowAA = measured.filter(s => s.ratio < 4.5).map(s => `${s.text} ${s.ratio.toFixed(2)}`);
    report[name] = r;
    await ctx.close();
  }
  await browser.close();
  const summary = JSON.parse(JSON.stringify(report));
  for (const k of Object.keys(summary)) { summary[k].enterAllOk = summary[k].enter.every(e => e.ok); summary[k].enterFailures = summary[k].enter.filter(e => !e.ok); delete summary[k].enter; }
  console.log(JSON.stringify(summary, null, 1));
})();
