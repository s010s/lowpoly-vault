// SPDX-License-Identifier: MIT
// Re-render the pinned batch31 GLBs through the repository's Three.js viewer.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const repo = process.cwd();
const outputRoot = path.resolve('qa/continuous-small-life-round11-20261018/batch-31/independent-review/evidence/runtime');
const assets = ['asaphus', 'hazelia', 'sea-cave', 'cruziana-crawling-furrow'];
const hashFile = filename => crypto.createHash('sha256').update(fs.readFileSync(filename)).digest('hex');
const browser = await chromium.launch({
  executablePath: '/usr/bin/chromium',
  headless: true,
  args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
});
const overall = { schema_version: 1, threejs: '0.180.0', chromium_executable: '/usr/bin/chromium', renderer_profile: 'ANGLE SwiftShader software WebGL2', assets: {} };

for (const asset of assets) {
  const configPath = path.join(repo, 'production/continuous-small-life-round11-20261018/work/batch-31', asset, 'r001/config.json');
  const attempt = JSON.parse(fs.readFileSync(configPath, 'utf8')).selected_attempt || 'attempt-01';
  const glbPath = path.join(repo, 'assets/candidates/continuous-small-life-round11-20261018/batch-31', asset, 'r001', attempt, asset, `${asset}.glb`);
  const assetOut = path.join(outputRoot, asset);
  fs.mkdirSync(assetOut, { recursive: true });
  const glbSha256 = hashFile(glbPath);
  overall.assets[asset] = { attempt, glb_path: path.relative(repo, glbPath), glb_sha256: glbSha256, modes: {} };

  for (const mode of ['single', 'scene']) {
    const page = await browser.newPage({ viewport: { width: 640, height: 640 } });
    const errors = [];
    const failed = [];
    page.on('pageerror', error => errors.push(String(error)));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    page.on('requestfailed', request => failed.push({ url: request.url(), failure: request.failure() }));
    const url = `http://127.0.0.1:8791/production/continuous-small-life-round11-20261018/work/batch-31/viewer.html?asset=${asset}&mode=${mode}&attempt=${attempt}`;
    await page.goto(url);
    await page.waitForFunction(() => window.ready, { timeout: 60000 });
    const runtime = await page.evaluate(() => window.inspect);
    const views = [];
    const viewNames = mode === 'scene' ? ['hero', 'top'] : ['hero', 'reversehero', 'front', 'side', 'rear', 'top', 'bottom'];
    for (const view of viewNames) {
      const metrics = await page.evaluate(name => window.setView(name), view);
      const name = `${mode}-${view}.png`;
      const screenshotPath = path.join(assetOut, name);
      await page.locator('canvas').screenshot({ path: screenshotPath });
      views.push({ ...metrics, path: name, sha256: hashFile(screenshotPath) });
    }
    if (mode === 'single') {
      for (const extent of [80, 160, 240]) {
        const metrics = await page.evaluate(size => window.setView('hero', size), extent);
        const name = `single-${extent}px.png`;
        const screenshotPath = path.join(assetOut, name);
        await page.locator('canvas').screenshot({ path: screenshotPath });
        views.push({ ...metrics, path: name, sha256: hashFile(screenshotPath) });
      }
    }
    const result = {
      schema_version: 1,
      asset,
      mode,
      status: errors.length || failed.length ? 'fail' : 'pass',
      glb_path: path.relative(repo, glbPath),
      glb_sha256: glbSha256,
      runtime,
      views,
      errors,
      failed,
      limitation: 'Actual GLTFLoader and browser render on Chromium ANGLE SwiftShader software WebGL2; this does not certify a hardware GPU or device performance.',
    };
    const reportPath = path.join(assetOut, `${mode}.json`);
    fs.writeFileSync(reportPath, JSON.stringify(result, null, 2) + '\n');
    overall.assets[asset].modes[mode] = { report: path.relative(repo, reportPath), status: result.status, view_count: views.length, renderer: runtime.renderer, webgl2: runtime.webgl2, instances: runtime.instances, errors, failed };
    await page.close();
    if (result.status !== 'pass') throw new Error(`${asset}/${mode} failed; see ${reportPath}`);
    console.log(`${asset}/${mode}: pass, ${views.length} views, ${runtime.renderer}`);
  }
}

await browser.close();
const summaryPath = path.join(outputRoot, 'summary.json');
fs.writeFileSync(summaryPath, JSON.stringify(overall, null, 2) + '\n');
console.log(`Runtime summary: ${path.relative(repo, summaryPath)}`);
