// Hash-bound direct browser review of the four frozen GLBs (software WebGL only).
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ids = ['diplomoceras', 'nelumbo', 'marine-terrace', 'angular-unconformity-outcrop'];
const asset = process.argv[2];
const out = path.resolve(process.argv[3]);
if (!ids.includes(asset) || !process.argv[3]) throw Error('usage: browser_qa.mjs <asset-id> <empty-output-dir>');
if (fs.existsSync(out) && fs.readdirSync(out).length) throw Error(`Output directory must be empty: ${out}`);
fs.mkdirSync(out, { recursive: true });
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const attempt = JSON.parse(fs.readFileSync(`production/continuous-small-life-round13-20261018/work/batch-38/${asset}/r001/config.json`)).selected_attempt || 'attempt-01';
const base = `assets/candidates/continuous-small-life-round13-20261018/batch-38/${asset}/r001/${attempt}/${asset}`;
const glb = `${base}/${asset}.glb`;
const glbHash = hash(glb);
const scope = JSON.parse(fs.readFileSync('production/continuous-small-life-round13-20261018/work/batch-38/QA-HANDOFF-SCOPE.json'));
if (scope.expected_glb_sha256_by_asset[asset] !== glbHash) throw Error(`GLB pin mismatch for ${asset}`);
const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', headless: true,
  args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const summaries = [];
try {
  for (const mode of ['single', 'scene']) {
    const page = await browser.newPage({ viewport: { width: 640, height: 640 } });
    const errors = [], failed = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('requestfailed', r => failed.push({ url: r.url(), failure: r.failure() }));
    await page.goto(`http://127.0.0.1:8798/production/continuous-small-life-round13-20261018/work/batch-38/viewer.html?asset=${asset}&mode=${mode}&attempt=${attempt}`);
    await page.waitForFunction(() => window.ready, { timeout: 60000 });
    const metrics = await page.evaluate(() => window.inspect);
    const views = [];
    const requested = mode === 'scene' ? ['hero', 'top'] : ['hero', 'reversehero', 'front', 'side', 'rear', 'top', 'bottom'];
    for (const view of requested) {
      const result = await page.evaluate(v => window.setView(v), view);
      const name = `${mode}-${view}.png`;
      await page.locator('canvas').screenshot({ path: path.join(out, name) });
      views.push({ ...result, path: name, sha256: hash(path.join(out, name)) });
    }
    if (mode === 'single') for (const extent of [80, 160, 240]) {
      const result = await page.evaluate(n => window.setView('hero', n), extent);
      const name = `single-${extent}px.png`;
      await page.locator('canvas').screenshot({ path: path.join(out, name) });
      views.push({ ...result, path: name, sha256: hash(path.join(out, name)) });
    }
    const result = { asset_id: asset, mode, ...metrics, views, errors, failed,
      status: errors.length || failed.length ? 'fail' : 'pass', glb_sha256: glbHash,
      runtime_scope: 'Actual pinned Three.js GLTFLoader in Chromium WebGL2 ANGLE SwiftShader software renderer; no physical-device performance claim.' };
    fs.writeFileSync(path.join(out, `${mode}.json`), JSON.stringify(result, null, 2) + '\n');
    if (errors.length || failed.length) throw Error(JSON.stringify(result));
    summaries.push({ mode, status: result.status, three: result.three, renderer: result.renderer, views: views.length });
    await page.close();
  }
} finally { await browser.close(); }
fs.writeFileSync(path.join(out, 'summary.json'), JSON.stringify({ asset_id: asset, glb_sha256: glbHash, statuses: summaries }, null, 2) + '\n');
console.log(JSON.stringify({ asset_id: asset, glb_sha256: glbHash, statuses: summaries }, null, 2));
