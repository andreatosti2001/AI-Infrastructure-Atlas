const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 900 } });
  await p.goto('file://' + __dirname + '/supplier-mockup.html'); await p.screenshot({ path: __dirname + '/supplier-mockup.png', fullPage: true }); await b.close(); })();
