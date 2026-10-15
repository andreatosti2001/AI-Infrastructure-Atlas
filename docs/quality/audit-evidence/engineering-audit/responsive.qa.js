// S22 audit: responsive behaviour of the major infographics, and rendering determinism (Chromium, Playwright from the
// environment). node responsive.qa.js REPO OUTDIR
// Per page and width (320, 375, 768, 1024, 1440): document overflow; elements wider than the viewport outside a
// scrolling container; every SVG's rendered width and its smallest text as rendered (font size x scale); the smallest
// rendered text of the page. Then each page at 1280 px is screenshotted twice in fresh contexts and the PNG hashes
// compared (is a pixel baseline stable in one environment?).
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'); const path = require('path'); const crypto = require('crypto');
const [REPO, OUT] = process.argv.slice(2);
const PAGES = ['site/hbm-chain/index.html', 'site/hbm-insight/index.html', 'site/questions/export-control-texts/index.html',
  'site/briefs/accelerator-memory/index.html', 'site/companies/company-sk-hynix/index.html', 'site/index.html'];
const WIDTHS = [320, 375, 768, 1024, 1440];
(async () => {
  const browser = await chromium.launch();
  const report = { chromium: browser.version(), pages: {} };
  for (const rel of PAGES) {
    const url = 'file://' + path.join(REPO, rel);
    report.pages[rel] = {};
    for (const w of WIDTHS) {
      const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
      const page = await ctx.newPage();
      await page.goto(url);
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
      const m = await page.evaluate(() => {
        const vw = document.documentElement.clientWidth;
        const scrollers = el => { for (let p = el.parentElement; p; p = p.parentElement) { const s = getComputedStyle(p); if (/(auto|scroll)/.test(s.overflowX)) return true; } return false; };
        const wide = [];
        for (const el of document.body.querySelectorAll('*')) {
          const r = el.getBoundingClientRect();
          if (r.width > vw + 1 && !scrollers(el) && !['HTML', 'BODY'].includes(el.tagName)) wide.push(el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''));
        }
        const svgs = [...document.querySelectorAll('svg')].filter(s => s.getBoundingClientRect().width > 0).map(s => {
          const r = s.getBoundingClientRect();
          const vb = s.viewBox && s.viewBox.baseVal && s.viewBox.baseVal.width ? s.viewBox.baseVal.width : r.width;
          const scale = r.width / vb;
          let minText = Infinity;
          s.querySelectorAll('text').forEach(t => { const fs = parseFloat(getComputedStyle(t).fontSize); if (fs) minText = Math.min(minText, fs * scale); });
          return { label: s.getAttribute('aria-labelledby') || s.getAttribute('aria-label') || s.id || 'svg', width: Math.round(r.width), scale: +scale.toFixed(2), minTextPx: minText === Infinity ? null : +minText.toFixed(1), inScroller: scrollers(s) };
        });
        let minHtml = Infinity;
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        while (walker.nextNode()) { const n = walker.currentNode; if (!n.textContent.trim()) continue; const p = n.parentElement; if (p.closest('svg')) continue; const r = p.getBoundingClientRect(); if (!r.width) continue; minHtml = Math.min(minHtml, parseFloat(getComputedStyle(p).fontSize)); }
        return { overflow: document.documentElement.scrollWidth - vw, wide: [...new Set(wide)].slice(0, 8), svgs, minHtmlTextPx: minHtml };
      });
      report.pages[rel][w] = m; console.error(rel, w, "measured");
      await ctx.close();
    }
    const hashes = [];
    for (let i = 0; i < 2; i++) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
      const page = await ctx.newPage(); await page.goto(url);
      const png = await page.screenshot({ fullPage: false });
      hashes.push(crypto.createHash('sha256').update(png).digest('hex'));
      if (i === 0) fs.writeFileSync(path.join(OUT, rel.replace(/\//g, '_') + '.png'), png);
      await ctx.close();
    }
    report.pages[rel].screenshotsIdentical = hashes[0] === hashes[1];
    report.pages[rel].screenshotSha = hashes[0];
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'responsive.json'), JSON.stringify(report, null, 1));
  for (const [rel, v] of Object.entries(report.pages)) {
    console.log(rel, 'identical screenshots:', v.screenshotsIdentical);
    for (const w of WIDTHS) console.log('  ', w, 'overflow', v[w].overflow, 'wide', JSON.stringify(v[w].wide), 'minHtml', v[w].minHtmlTextPx, 'svgs', JSON.stringify(v[w].svgs.map(s => [s.label.slice(0, 24), s.width, s.scale, s.minTextPx, s.inScroller])));
  }
})();
