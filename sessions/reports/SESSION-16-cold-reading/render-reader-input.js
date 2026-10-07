// Run: node render-reader-input.js DIR (Playwright from the environment, D-106).
// S16 cold reading: renders the research view copy with its tutorials removed, at 1280 and 375 px, for the fresh
// reader: the indicator section and the full page as screenshots, and the page's visible text.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const DIR = process.argv[2];
const URL = 'file://' + require('path').resolve(DIR, 'page-without-method.html');
(async () => {
  const browser = await chromium.launch();
  for (const [name, width, height] of [['desktop', 1280, 900], ['mobile', 375, 812]]) {
    const ctx = await browser.newContext({ viewport: { width, height } });
    const page = await ctx.newPage();
    await page.goto(URL, { waitUntil: 'load' });
    await page.screenshot({ path: `${DIR}/${name}-01-top.png` });
    await (await page.$('#insight')).screenshot({ path: `${DIR}/${name}-02-indicators.png` });
    await page.screenshot({ path: `${DIR}/${name}-00-full-page.png`, fullPage: true });
    if (name === 'desktop') fs.writeFileSync(`${DIR}/visible-text.txt`, await page.evaluate(() => document.body.innerText));
    await ctx.close();
  }
  await browser.close();
})();
