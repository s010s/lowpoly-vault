/** Local integration regression, not whole-model artistic or full-site acceptance.
 * Start the actual build separately. Requires Playwright and a sandbox-capable browser.
 * QA_BASE_URL=http://127.0.0.1:PORT[/base] QA_OUTPUT_DIR=/path/to/evidence node <this file>
 * Optional QA_MODEL_IDS=id,id. The catalog must also contain the anchor models below.
 */
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const base = process.env.QA_BASE_URL?.replace(/\/$/, '');
const output = process.env.QA_OUTPUT_DIR;
assert(base && output, 'Set QA_BASE_URL and QA_OUTPUT_DIR');
const url = new URL(base);
assert(['127.0.0.1', 'localhost', '[::1]'].includes(url.hostname), 'Use a local review build');
const origin = url.origin;
const response = await fetch(`${base}/assets/gallery.json`);
assert(response.ok, 'Current built gallery catalog must be readable');
const catalog = await response.json();
const ids = (process.env.QA_MODEL_IDS || 'confuciusornis,diplomystus,archaeopteryx').split(',');
const modes = ['rapid-reselect', 'late-response', 'retry', 'rotate-reset'];
await fs.mkdir(output, {recursive:true});
const browser = await chromium.launch({headless:true, chromiumSandbox:true});
const results = [];
const bounded = async promise => {
  let timer;
  try { return await Promise.race([promise, new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error('Controlled GLB request was not observed')), 20000);
  })]); } finally { clearTimeout(timer); }
};
try {
  for (const id of ids) for (const width of [1440, 390]) for (const mode of modes) {
    const asset = catalog.assets.find(a => a.id === id);
    const anchor = id === 'confuciusornis' ? 'diplomystus' : 'confuciusornis';
    assert(asset && catalog.assets.some(a => a.id === anchor), 'Target and anchor must be in the real catalog');
    const page = await browser.newPage({viewport:{width, height:width === 390 ? 844 : 1000},
      isMobile:width === 390, hasTouch:width === 390});
    const errors = [];
    let armed = false, requests = 0, release, seen;
    const gate = new Promise(resolve => { release = resolve; });
    const requested = new Promise(resolve => { seen = resolve; });
    page.on('pageerror', error => errors.push(String(error)));
    await page.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
    await page.route(`${base}/${asset.glb}`, async route => {
      if (armed) {
        requests++; seen();
        if (mode === 'retry' && requests === 1) return route.abort('failed');
        if (mode === 'late-response') await gate;
      }
      return route.continue().catch(() => {}); // A newer selection may have cancelled this request.
    });
    const choose = target => page.evaluate(target => {
      void __preview.choose(target, {activateMobile:true});
    }, target);
    const ready = target => page.waitForFunction(target =>
      __preview.renderer.detail.asset?.id === target && __preview.renderer.stats.detailStatus === 'ready',
    target, {timeout:45000});
    const read = () => page.evaluate(() => {
      const renderer = __preview.renderer;
      return {selected:__preview.state.selected, id:renderer.detail.asset?.id,
        sha:renderer.detail.asset?.sha256?.glb, status:renderer.stats.detailStatus,
        model:!!renderer.detail.model, posterId:document.querySelector('#detail-poster').dataset.modelId,
        bridgeCount:document.querySelectorAll('.continuity-poster').length,
        transition:renderer.stats.cameraTransition, quaternion:renderer.detail.orientation.quaternion.toArray(),
        camera:renderer.detail.camera.position.toArray(), target:renderer.controls.target.toArray()};
    });
    try {
      await page.goto(`${base}/zh-CN/models/`);
      // Wait for actual initial poster readiness, not just the early renderer export.
      await page.waitForFunction(() => {
        const poster = document.querySelector('#detail-poster');
        return window.__preview?.renderer && poster?.dataset.modelId === __preview.state.selected && poster.dataset.state === 'ready';
      });
      await choose(anchor); await ready(anchor);
      armed = true; await choose(id);
      let before, rotated;
      if (mode === 'late-response') {
        await bounded(requested); await choose(anchor); await ready(anchor);
        release(); await page.waitForTimeout(500);
      } else if (mode === 'retry') {
        await page.locator('#retry').waitFor({state:'visible'});
        await page.locator('#retry').click(); await ready(id);
      } else {
        await ready(id);
        if (mode === 'rapid-reselect') {
          await page.evaluate(target => {
            for (let n = 0; n < 3; n++) void __preview.choose(target, {activateMobile:true});
          }, id);
          await ready(id); await page.waitForTimeout(250);
        } else {
          before = await read();
          const box = await page.locator('#detail').boundingBox();
          await page.mouse.move(box.x + box.width * .45, box.y + box.height * .5);
          await page.mouse.down();
          await page.mouse.move(box.x + box.width * .65, box.y + box.height * .55, {steps:12});
          await page.mouse.up(); rotated = await read();
          await page.locator('#reset').click();
          // Fixed 900 ms cannot guarantee a presented final RAF under load.
          await page.waitForFunction(() => !__preview.renderer.stats.cameraTransition &&
            !__preview.renderer.viewMotion.active, {}, {timeout:15000});
        }
      }
      const state = await read(), expected = mode === 'late-response' ? anchor : id;
      assert.equal(state.id, expected); assert.equal(state.selected, expected);
      assert.equal(state.sha, catalog.assets.find(a => a.id === expected).sha256.glb);
      assert.equal(state.status, 'ready'); assert(state.model); assert.equal(state.posterId, expected);
      assert.equal(errors.length, 0);
      if (mode === 'retry') assert(requests >= 2, 'Retry must issue a second GLB request');
      if (mode === 'rapid-reselect') assert.equal(state.bridgeCount, 0);
      if (mode === 'rotate-reset') {
        assert(before.camera.some((v, i) => Math.abs(v - rotated.camera[i]) > 1e-5) ||
          JSON.stringify(before.target) !== JSON.stringify(rotated.target), 'Drag must alter the view');
        assert(state.quaternion.every((v, i) => Math.abs(v - before.quaternion[i]) < 1e-7), 'Reset restores orientation');
        assert(state.target.every((v, i) => Math.abs(v - before.target[i]) < 1e-4), 'Reset restores target');
        assert(state.camera.every((v, i) => Math.abs(v - before.camera[i]) < 1e-4), 'Reset restores camera');
      }
      results.push({id, width, mode, state, before, rotated, requests, errors, pass:true});
      await fs.writeFile(`${output}/REGRESSION.json`, JSON.stringify({base, catalogTotal:catalog.total, results}, null, 2));
      console.log(id, width, mode, 'PASS');
    } catch (error) {
      await fs.writeFile(`${output}/FAILURE.json`, JSON.stringify({id, width, mode, requests, errors, error:String(error)}, null, 2));
      throw error;
    } finally { release(); await page.close(); }
  }
} finally { await browser.close(); }
