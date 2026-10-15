// Shared by the browser scripts (S22, D-212): where Playwright comes from, and how a script fails.
// Playwright comes from the repository's pinned package (package.json, package-lock.json: `npm ci`) where it is
// installed, as in CI; otherwise from the session environment's copy (/opt/node-tools), as before S22 (D-106).
// A script lists every failed condition by name; any failure sets a non-zero exit status, so CI and a session see it
// without reading the JSON (engineering audit F-1). A crash also exits non-zero (an unhandled rejection).
const fs = require('fs');

function playwright() {
  try {
    return require('playwright');
  } catch (e) {
    return require('/opt/node-tools/node_modules/playwright');
  }
}

// The engine a script runs on: chromium unless QA_BROWSER names firefox or webkit (the research view's filter, F-11).
function engine() {
  const name = process.env.QA_BROWSER || 'chromium';
  if (!['chromium', 'firefox', 'webkit'].includes(name)) throw new Error(`QA_BROWSER must be chromium, firefox or webkit, not ${name}`);
  return [name, playwright()[name]];
}

// Collects named failures: check(label, condition, detail).
function verdict() {
  const failures = [];
  const check = (label, ok, detail) => { if (!ok) failures.push(detail === undefined ? label : `${label}: ${JSON.stringify(detail)}`); return ok; };
  return { failures, check };
}

// Writes qa-result.json with allOk and failures, prints the summary, and fails the process if anything failed.
function finish(out, report, failures, summary) {
  report.allOk = failures.length === 0;
  report.failures = failures;
  fs.writeFileSync(`${out}/qa-result.json`, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ allOk: report.allOk, failures, ...summary }, null, 1));
  if (failures.length) {
    console.error(`FAIL: ${failures.length} browser check(s) failed:\n- ${failures.join('\n- ')}`);
    process.exitCode = 1;
  }
}

// Every request a page makes must be the page itself (it loads nothing).
function onlyThePage(requests, url) {
  return requests.filter(r => r.split('#')[0] !== url);
}

// The conditions journeys.qa.js and brief.qa.js measure on a page at one width, each a named failure.
function widthChecks(check, label, r) {
  check(`${label}: console messages`, !r.console.length, r.console);
  check(`${label}: page errors`, !r.pageErrors.length, r.pageErrors);
  check(`${label}: requests other than the page`, !r.foreignRequests.length, r.foreignRequests);
  check(`${label}: document overflow`, r.overflow <= 0, r.overflow);
  check(`${label}: wide elements`, !r.wideElements.length, r.wideElements);
  check(`${label}: wide elements with every disclosure open`, !r.wideElementsOpen.length, r.wideElementsOpen);
  check(`${label}: links reached by Tab`, r.linksReachedByTab >= r.links, `${r.linksReachedByTab} of ${r.links}`);
  check(`${label}: links without a focus ring`, !r.focusRingMissing.length, r.focusRingMissing);
  check(`${label}: broken in-page links`, !r.brokenFragments.length, r.brokenFragments);
  check(`${label}: text below 4.5:1 contrast`, !r.contrastBelow45.length, r.contrastBelow45);
  check(`${label}: disclosures opened from the keyboard`, r.disclosuresOpenedByKeyboard === r.disclosures, `${r.disclosuresOpenedByKeyboard} of ${r.disclosures}`);
  check(`${label}: Enter lands on the evidence`, !r.enter || r.enter.every(x => x.ok), (r.enter || []).filter(x => !x.ok));
}

module.exports = { playwright, engine, verdict, finish, onlyThePage, widthChecks };
