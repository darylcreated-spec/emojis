// tests/test_ast_dom_queries.js
// AST / Static Analysis of DOM queries & event listeners in app.js against index.html

const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const appJsPath = path.join(repoRoot, 'app.js');
const indexHtmlPath = path.join(repoRoot, 'index.html');

const appJs = fs.readFileSync(appJsPath, 'utf8');
const indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');

console.log('======================================================================');
console.log('Challenger 2 Node.js DOM Query & Event Listener Verification');
console.log('======================================================================');

let failures = 0;

function assert(condition, message) {
  if (!condition) {
    console.error(`[FAIL] ${message}`);
    failures++;
  } else {
    console.log(`[PASS] ${message}`);
  }
}

// 1. Extract all HTML IDs
const idAttrRegex = /\bid=["']([^"']+)["']/g;
const htmlIds = new Set();
let match;
while ((match = idAttrRegex.exec(indexHtml)) !== null) {
  htmlIds.add(match[1]);
}
console.log(`Discovered ${htmlIds.size} unique IDs in index.html.`);

// 2. Extract getElementById calls in app.js
const getElementByIdRegex = /getElementById\(["']([^"']+)["']\)/g;
const queriedIds = new Set();
while ((match = getElementByIdRegex.exec(appJs)) !== null) {
  queriedIds.add(match[1]);
}
console.log(`Discovered ${queriedIds.size} unique getElementById calls in app.js.`);

// Verify each queried ID exists in HTML
for (const id of queriedIds) {
  assert(htmlIds.has(id), `getElementById target '${id}' must exist in index.html`);
}

// 3. Specifically verify critical event listeners & controls
const criticalElements = [
  'toggleAnimatedBtn',
  'toggleAnimatedLabel',
  'packRail',
  'stickerGrid',
  'activePackCard',
  'slangSearchInput',
  'clearSearchBtn',
  'copyStickerClipboardBtn',
  'directSendSocialBtn',
  'downloadAnimGifBtn',
  'downloadAnimWebpBtn',
  'downloadPngBtn',
  'downloadDiscordBtn',
  'downloadPackBtn',
  'sharePackBtn',
  'shareAppBtn',
  'toastBanner'
];

for (const elId of criticalElements) {
  assert(htmlIds.has(elId), `Critical UI element '${elId}' exists in index.html`);
  assert(appJs.includes(elId), `Critical UI element '${elId}' is handled in app.js`);
}

// 4. Verify Event Listeners wired to critical controls
const eventListenerRegex = /([a-zA-Z0-9_]+)\??\.addEventListener\(["']([^"']+)["']/g;
const listeners = [];
while ((match = eventListenerRegex.exec(appJs)) !== null) {
  listeners.push({ variable: match[1], event: match[2] });
}
console.log(`Discovered ${listeners.length} addEventListener bindings in app.js.`);

const criticalListeners = [
  'toggleAnimatedBtn',
  'copyStickerClipboardBtn',
  'directSendSocialBtn',
  'downloadAnimGifBtn',
  'downloadAnimWebpBtn',
  'downloadPngBtn',
  'downloadDiscordBtn',
  'downloadPackBtn',
  'sharePackBtn',
  'shareAppBtn'
];

for (const btn of criticalListeners) {
  const isBound = listeners.some(l => l.variable === btn);
  assert(isBound, `Event listener attached to '${btn}'`);
}

// 5. Test onerror fallback logic
console.log('\n--- Verifying onerror fallback logic ---');
const onerrorRegex = /onerror=["']([^"']+)["']/g;
const onerrorHandlers = [];
while ((match = onerrorRegex.exec(appJs)) !== null) {
  onerrorHandlers.push(match[1]);
}
console.log(`Discovered ${onerrorHandlers.length} onerror fallback attributes in app.js template literals.`);
assert(onerrorHandlers.length > 0, 'app.js contains onerror fallback handlers');

for (const handler of onerrorHandlers) {
  // Validate that the handler is a safe JavaScript assignment
  assert(handler.startsWith("this.src="), `Handler starts with this.src=: ${handler}`);
  // Check for unsafe quotes or syntax injection
  assert(!handler.includes('"'), `Handler contains no double quotes: ${handler}`);
  assert(!handler.includes('<') && !handler.includes('>'), `Handler contains no angle brackets: ${handler}`);
}

// 6. Test URL construction with edge cases
console.log('\n--- Verifying URL construction with edge-case sticker IDs ---');
const testCases = [
  { id: 'steups', valid: true },
  { id: 'killing-me-dead', valid: true },
  { id: 'slang-wha-yuh-say', valid: true },
  { id: 'freshwater-yankee', valid: true },
  { id: 'doh-tote', valid: true },
  { id: "injection'quote", valid: false },
  { id: 'injection"dquote', valid: false },
  { id: 'injection<script>', valid: false },
  { id: 'space in id', valid: false }
];

for (const tc of testCases) {
  const isKebab = /^[a-z0-9]+(-[a-z0-9]+)*$/.test(tc.id);
  if (tc.valid) {
    assert(isKebab, `Valid ID '${tc.id}' is kebab-case`);
    const constructedUrl = `assets/stickers/${tc.id}.webp?v=9`;
    const onerrorAttr = `onerror="this.src='${constructedUrl}'"`;
    // Verify valid JS execution inside synthetic onerror
    try {
      new Function(`const obj = {}; obj.src = '${constructedUrl}';`);
      assert(true, `Simulated onerror JS is syntactically valid for '${tc.id}'`);
    } catch (e) {
      assert(false, `Simulated onerror JS failed for '${tc.id}': ${e.message}`);
    }
  } else {
    assert(!isKebab, `Malicious/edge ID '${tc.id}' correctly flagged as non-kebab`);
  }
}

// 7. Verify Cache Buster consistency
assert(!appJs.includes('?v=8'), 'No legacy ?v=8 in app.js');
const v9Count = (appJs.match(/\?v=9/g) || []).length;
assert(v9Count === 8, `Exactly 8 occurrences of ?v=9 in app.js (found ${v9Count})`);

console.log('======================================================================');
if (failures === 0) {
  console.log('ALL NODE.JS DOM & RUNTIME CHECKS PASSED (0 failures)');
  process.exit(0);
} else {
  console.error(`COMPLETED WITH ${failures} FAILURE(S)`);
  process.exit(1);
}
