// SPDX-License-Identifier: MIT
// Independent exact-GLB QA. The reviewer labels SwiftShader as software rendering.
import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ids = ['gryphaea', 'folded-strata-outcrop', 'volcanic-bomb', 'teredolites-wood-boring-cast'];
const root = process.cwd();
const handoff = JSON.parse(fs.readFileSync('production/continuous-small-life-round12-20261018/work/batch-36/HANDOFF.json', 'utf8'));
const attempts = Object.fromEntries(handoff.assets.map(x => [x.asset_id, x.selected_attempt]));
const expected = Object.fromEntries(handoff.assets.map(x => [x.asset_id, x.glb.sha256]));
const outputRoot = 'qa/continuous-small-life-round12-20261018/batch-36/independent-review/evidence/runtime';
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

const browser = await chromium.launch({
  executablePath: '/usr/bin/chromium',
  headless: true,
  args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
});

for (const asset of ids) {
  const base = `assets/candidates/continuous-small-life-round12-20261018/batch-36/${asset}/r001/${attempts[asset]}/${asset}`;
  const glbPath = path.join(root, base, `${asset}.glb`);
  const actualHash = hash(glbPath);
  if (actualHash !== expected[asset]) throw new Error(`${asset} GLB hash differs from frozen scope`);
  const dir = path.join(root, outputRoot, asset);
  fs.mkdirSync(dir, {recursive: true});

  for (const mode of ['single', 'scene']) {
    const page = await browser.newPage({viewport: {width: 640, height: 640}});
    const errors = [];
    const failed = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('requestfailed', r => failed.push({url: r.url(), failure: r.failure()}));
    const url = `http://127.0.0.1:8796/production/continuous-small-life-round12-20261018/work/batch-36/viewer.html?asset=${asset}&mode=${mode}&attempt=${attempts[asset]}`;
    await page.goto(url);
    await page.waitForFunction(() => window.ready, {timeout: 60000});
    const metrics = await page.evaluate(() => window.inspect);
    const views = [];
    const names = mode === 'scene' ? ['hero', 'top'] : ['hero', 'reversehero', 'front', 'side', 'rear', 'top', 'bottom'];
    for (const view of names) {
      const result = await page.evaluate(v => window.setView(v), view);
      const filename = `${mode}-${view}.png`;
      const target = path.join(dir, filename);
      await page.locator('canvas').screenshot({path: target});
      const glError = await page.evaluate(() => {
        const gl = document.querySelector('canvas').getContext('webgl2');
        return gl ? gl.getError() : null;
      });
      views.push({...result, gl_error: glError, path: filename, sha256: hash(target), bytes: fs.statSync(target).size});
    }
    if (mode === 'single') {
      for (const extent of [80, 160, 240]) {
        const result = await page.evaluate(n => window.setView('hero', n), extent);
        const filename = `single-${extent}px.png`;
        const target = path.join(dir, filename);
        await page.locator('canvas').screenshot({path: target});
        const glError = await page.evaluate(() => document.querySelector('canvas').getContext('webgl2').getError());
        views.push({...result, gl_error: glError, path: filename, sha256: hash(target), bytes: fs.statSync(target).size});
      }
    }
    const result = {
      schema_version: 1,
      kind: 'independent_exact_glb_browser_qa',
      asset_id: asset,
      mode,
      glb_path: base + `/${asset}.glb`,
      glb_sha256: actualHash,
      expected_glb_sha256: expected[asset],
      ...metrics,
      views,
      errors,
      failed_requests: failed,
      status: errors.length || failed.length || !metrics.webgl2 || views.some(v => v.gl_error !== 0 || v.triangles <= 0) ? 'fail' : 'pass',
      scope: 'Exact shipped GLB through Three.js GLTFLoader in Chromium WebGL2 using ANGLE SwiftShader software rendering; functional render evidence only, no physical-GPU or device-performance claim.',
    };
    const reportPath = path.join(dir, `${mode}.json`);
    fs.writeFileSync(reportPath, JSON.stringify(result, null, 2) + '\n');
    console.log(asset, mode, result.status, metrics.renderer, 'instances=', metrics.instances,
      'calls=', views.map(x => x.calls).join(','), 'triangles=', views.map(x => x.triangles).join(','));
    await page.close();
    if (result.status !== 'pass') throw new Error(`${asset} ${mode}: ${JSON.stringify(result)}`);
    if (!String(metrics.renderer).includes('SwiftShader')) throw new Error(`${asset} renderer was not identified as SwiftShader software`);
  }
}
await browser.close();
