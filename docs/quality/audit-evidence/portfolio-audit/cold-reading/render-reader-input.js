// Run: node render-reader-input.js REPO DIR (Playwright from the environment, D-106).
// S24 cold reading (H-0): renders the client brief at 1280 and 375 px for the fresh readers: the brief's visible text
// with every disclosure closed, its first screen at both widths, and its SQL tutorial ("How this was computed")
// opened, as text (a screenshot of the opened tutorial hung in this container, so none is taken). Copies README.md and decision D-118 as they stand.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const [REPO, DIR] = process.argv.slice(2);
const URL = 'file://' + path.resolve(REPO, 'site/briefs/accelerator-memory/index.html');
(async () => {
  fs.copyFileSync(path.join(REPO, 'README.md'), path.join(DIR, '1-README.md'));
  const decisions = fs.readFileSync(path.join(REPO, 'docs/architecture/decisions.md'), 'utf8');
  const start = decisions.indexOf('## D-118 ');
  const end = decisions.indexOf('## D-119 ');
  fs.writeFileSync(path.join(DIR, '4-decision-D-118.md'), decisions.slice(start, end).trimEnd() + '\n');
  const browser = await chromium.launch();
  for (const [name, width, height] of [['desktop', 1280, 900], ['mobile', 375, 812]]) {
    const ctx = await browser.newContext({ viewport: { width, height } });
    const page = await ctx.newPage();
    await page.goto(URL, { waitUntil: 'load' });
    await page.screenshot({ path: `${DIR}/2-brief-${name}-first-screen.png` });
    if (name === 'desktop') {
      fs.writeFileSync(`${DIR}/2-brief-visible-text.txt`, await page.evaluate(() => document.body.innerText));
      const tut = await page.$('details.sql-tutorial');
      await tut.evaluate(d => { d.open = true; });
      fs.writeFileSync(`${DIR}/3-sql-tutorial-text.txt`, await tut.evaluate(d => d.innerText));
    }
    await ctx.close();
  }
  await browser.close();
})();
