/** Shared real-model list acceptance; legacy filename retained for QA callers. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';

const root = resolve(process.env.GALLERY_DIR || 'dist');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/shared-model-preview/browser');
const prefix = '/lowpoly-vault/';
const report = { status: 'running', commit: process.env.GITHUB_SHA || null, checks: [], screenshots: [], page_errors: [], measurements: {}, note: 'Chromium software WebGL and emulated touch. Resource bytes are estimates, not physical-device GPU/heap measurements.' };
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.webp': 'image/webp', '.png': 'image/png', '.glb': 'model/gltf-binary' };
const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (!url.pathname.startsWith(prefix)) throw Error();
    let file = resolve(root, decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html');
    if (file !== root && !file.startsWith(root + sep)) throw Error();
    if ((await stat(file)).isDirectory()) file = resolve(file, 'index.html');
    const data = await readFile(file);
    res.writeHead(200, { 'Content-Type': mime[extname(file)] || 'application/octet-stream', 'Content-Length': data.length });
    res.end(data);
  } catch { res.writeHead(404).end(); }
});
let browser, current, base;
const requests = [];
const check = text => report.checks.push(text);
const selector = id => `#grid .asset-card[data-id="${id}"]`;
const preview = page => page.evaluate(() => ({ ...window.__vaultPreview }));
const gpu = page => page.evaluate(() => ({ ...window.__vaultGPU }));
const glbs = from => requests.slice(from).filter(r => /\.glb(?:\?|$)/.test(r.url));
const angleDelta = (a, b) => Math.abs(((a - b + 540) % 360) - 180);
function noSequenceRequests(from = 0) { assert(!requests.slice(from).some(r => r.url.includes('/turntables/')), 'Real-model inspection must fetch no turntable manifest or frame'); }
function bounded(s) {
  assert.equal(s.rendererCreations, 1, 'All consumers share one renderer creation');
  assert(s.renderers <= 1 && s.liveScenes <= 1 && s.activeLeases <= 1 && s.activeParses <= 1);
  assert(s.cachedScenes <= 3 && s.cachedDecodedBytes <= 48 * 1024 * 1024);
  assert(s.decodedEntries <= 4 && s.uncachedActiveScenes <= 1);
  assert(s.cacheEntries <= 3 && s.cacheBytes <= 24 * 1024 * 1024);
  assert(s.peakRequests <= 1 && s.peakParses <= 1);
}
async function context(options = {}) {
  const c = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce', recordVideo: { dir: output, size: options.viewport || { width: 1440, height: 1000 } }, ...options });
  const page = await c.newPage(); current = page;
  page.on('pageerror', error => report.page_errors.push(error.message));
  page.on('request', request => requests.push({ page: page.url(), url: request.url(), time: Date.now() }));
  return { c, page };
}
async function catalog(page, lang = '') {
  await page.goto(base + prefix + lang + 'models/');
  await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');
  assert.equal(await page.locator('#grid .asset-card').count(), 10);
  assert.equal((await preview(page)).kind, 'shared-real-model');
}
async function ready(page, id, frame) {
  await page.waitForFunction(({ id, frame }) => {
    const card = document.querySelector(`#grid .asset-card[data-id="${id}"]`), host = card?.querySelector('.asset-image');
    const expected = frame === undefined ? null : ((42 + frame * 15) % 360 + 360) % 360;
    const actual = Number(host?.dataset.viewAzimuth);
    return card?.dataset.previewState === 'ready' && host?.dataset.modelState === 'ready' && Number(host.dataset.renderTriangles) > 0 &&
      host.querySelector('.model-canvas') && (expected === null || Math.abs(((actual - expected + 540) % 360) - 180) < 0.01);
  }, { id, frame }, { timeout: 30000 });
}
async function settled(page) { await page.waitForFunction(() => window.__vaultGPU?.activeRequests === 0 && window.__vaultGPU?.activeParses === 0 && window.__vaultGPU?.rafPending === 0); }
async function screenshot(page, name) { await page.screenshot({ path: resolve(output, name + '.png'), fullPage: false, animations: 'disabled' }); report.screenshots.push(name + '.png'); }
async function stopped(page) {
  await page.waitForFunction(() => window.__vaultPreview.activeId === null && (!window.__vaultGPU || (window.__vaultGPU.liveScenes === 0 && window.__vaultGPU.activeRequests === 0 && window.__vaultGPU.activeParses === 0 && window.__vaultGPU.rafPending === 0)));
  assert.equal(await page.locator('#grid .model-canvas').count(), 0);
  assert.equal(await page.locator('#grid .model-preview-snapshot').count(), 0);
  const s = await gpu(page); if (s.rendererCreations) bounded(s);
}
async function canonicalPoster(page, id) {
  await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open && !document.querySelector('.stage-flight') && window.__vaultPreview?.activeId === null && (!window.__vaultGPU || (window.__vaultGPU.liveScenes === 0 && window.__vaultGPU.rafPending === 0)));
  assert.equal(await page.locator('.model-canvas,.model-preview-snapshot').count(), 0, 'Completed close detaches 3D without retaining an inspected-angle bitmap');
  assert(await page.locator(selector(id)).locator('.asset-image').evaluate(host => {
    const image = host.querySelector('img');
    if (!image?.complete || !image.naturalWidth || host.querySelectorAll('img').length !== 1 || host.closest('[data-detail-origin]')) return false;
    for (let node = image; node; node = node.parentElement) { const css = getComputedStyle(node); if (css.display === 'none' || css.visibility === 'hidden' || Number(css.opacity) < .99) return false; }
    return true;
  }), 'The source card must visibly return to its single canonical transparent poster');
}
async function detail(page, id) {
  await page.waitForURL(url => url.pathname.endsWith(`/models/${id}/`));
  await page.waitForFunction(id => { const h = document.querySelector('#canvas-host'); return h?.dataset.modelState === 'ready' && h.dataset.presentedUrl?.endsWith('/' + id + '.glb') && Number(h.dataset.renderTriangles) > 0; }, id, { timeout: 30000 });
  assert.equal(await page.locator('#canvas-host .model-canvas').count(), 1);
  assert.equal(await page.locator('#grid .model-canvas').count(), 0);
  bounded(await gpu(page));
}
async function desktop() {
  const { c, page } = await context();
  try {
    const start = requests.length;
    await catalog(page); await page.waitForTimeout(250);
    assert.equal(glbs(start).length, 0, 'Unhovered catalog keeps static posters');
    assert(!requests.slice(start).some(r => /\/viewer-[^/]+\.js/.test(r.url)), 'The WebGL viewer remains lazy');
    noSequenceRequests(start);
    const arch = page.locator(selector('natural-arch'));
    await arch.hover(); await page.waitForTimeout(65); await page.mouse.move(1, 1); await page.waitForTimeout(230);
    assert.equal(glbs(start).length, 0, 'A brief pass over a card does not acquire a GLB');
    check('Unhovered cards and sub-180 ms hover retain static posters with no GLB, viewer or sequence work.');
    await arch.hover(); await ready(page, 'natural-arch'); await settled(page);
    assert.equal(await page.locator('#grid .model-canvas').count(), 1);
    assert(glbs(start).length > 0 && glbs(start).every(r => r.url.endsWith('/natural-arch.glb')), 'Only intentionally hovered model is requested');
    bounded(await gpu(page)); noSequenceRequests(start);
    const box = await arch.locator('.asset-image').boundingBox(), samples = [];
    // Pointer input is continuous; test actual camera angles rather than quantized frame indices.
    await page.mouse.move(box.x + box.width * 0.5, box.y + box.height / 2);
    const baseline = await preview(page);
    assert(Math.abs(baseline.frame) < 0.1, 'A tiny initial pointer move does not jump to the opposite view');
    for (const fraction of [.1, .9, .2, .8, .35, .65, .02, .98]) {
      const begin = Date.now(); await page.mouse.move(box.x + box.width * fraction, box.y + box.height / 2);
      await ready(page, 'natural-arch', (fraction - .5) * 24); samples.push(Date.now() - begin);
    }
    await settled(page); const idleBefore = await gpu(page), frame = (await preview(page)).frame;
    await page.waitForTimeout(400);
    assert.equal((await preview(page)).frame, frame); assert.equal((await gpu(page)).renderedFrames, idleBefore.renderedFrames, 'Idle reduced-motion inspection starts no animation loop');
    report.measurements.desktop_preview = { preview: await preview(page), gpu: await gpu(page), pointer_to_draw_ms: samples };
    await screenshot(page, 'desktop-active-arch');
    await page.mouse.move(1, 1); await stopped(page);
    await arch.focus(); await page.keyboard.press('End'); await ready(page, 'natural-arch', 23);
    await page.keyboard.press('ArrowRight'); await ready(page, 'natural-arch', 24);
    await page.keyboard.press('Home'); await ready(page, 'natural-arch', 0);
    await page.keyboard.press('Escape'); await stopped(page);
    check('Pointer, keyboard wrap/Home/End/Escape and reduced-motion inspection draw actual GLB triangles with bounded resources.');
    report.measurements.all_ten = [];
    for (const id of await page.locator('#grid .asset-card').evaluateAll(cards => cards.map(card => card.dataset.id))) {
      const boundary = requests.length;
      await page.locator(selector(id)).focus(); await page.keyboard.press('Home'); await ready(page, id, 0); await settled(page);
      const s = await gpu(page); bounded(s);
      assert.equal(await page.locator('#grid .model-canvas').count(), 1);
      assert(glbs(boundary).every(r => r.url.endsWith('/' + id + '.glb')), 'Each selected card requests only its own GLB');
      report.measurements.all_ten.push({ id, preview: await preview(page), gpu: s });
      await page.keyboard.press('Escape'); await stopped(page);
    }
    noSequenceRequests(start);
    check('All ten selected originals draw actual triangles independently using one canvas, one renderer and bounded encoded/decoded LRUs.');
    await arch.focus(); await page.keyboard.press('Home'); await ready(page, 'natural-arch', 0);
    for (let i = 0; i < 17; i++) await page.keyboard.press('ArrowRight');
    await ready(page, 'natural-arch', 17); await settled(page);
    const warm = await gpu(page);
    await page.evaluate(() => { window.__listModelCanvas = document.querySelector('#grid [data-id="natural-arch"] .model-canvas'); });
    await page.evaluate(() => {
      window.__handoffFrames = [];
      const sample = () => {
        const dialog = document.querySelector('#viewer-dialog'), host = document.querySelector('#canvas-host');
        if (dialog.open) {
          const visible = [...host.querySelectorAll('canvas,img'), ...document.querySelectorAll('.stage-flight')].some(el => {
            const css = getComputedStyle(el), parent = getComputedStyle(el.parentElement);
            return css.visibility !== 'hidden' && parent.visibility !== 'hidden' && css.opacity !== '0' && (el.tagName !== 'IMG' || el.naturalWidth > 0);
          });
          window.__handoffFrames.push({ visible, ready: host.dataset.modelState === 'ready', presented: host.dataset.presentedUrl || null });
        }
        window.__handoffRAF = requestAnimationFrame(sample);
      }; sample();
    });
    await page.keyboard.press('Enter'); await detail(page, 'natural-arch');
    assert(await page.evaluate(() => window.__listModelCanvas === document.querySelector('#canvas-host .model-canvas')), 'Card/detail share the exact WebGL canvas');
    const shown = await gpu(page);
    assert.equal(shown.parseCount, warm.parseCount, 'Warm detail acquires the same decoded model without parsing');
    assert.equal(shown.networkRequests, warm.networkRequests, 'Warm detail sends no new GLB request');
    const angle = Number(await page.locator('#canvas-host').getAttribute('data-view-azimuth'));
    assert(angleDelta(angle, 297) < .001, 'The actual 17/24 camera angle enters detail unchanged');
    assert(Math.abs(Number(await page.locator('#canvas-host').getAttribute('data-view-elevation')) - 23.3) < .001);
    await screenshot(page, 'detail-same-current-angle');
    await page.route('**/*.glb', async route => { await new Promise(r => setTimeout(r, 550)); await route.continue().catch(() => {}); });
    await page.locator('#next-model').click(); await page.waitForTimeout(70);
    assert(await page.locator('#canvas-host .model-handoff').isVisible() || await page.locator('#canvas-host[data-model-state="ready"] .model-canvas').isVisible(), 'Next model retains a draw or already-painted cached model');
    await page.locator('#previous-model').click(); await page.waitForTimeout(70);
    assert(await page.locator('#canvas-host .model-handoff').isVisible() || await page.locator('#canvas-host[data-model-state="ready"] .model-canvas').isVisible());
    await page.locator('#next-model').click();
    const finalId = await page.evaluate(() => location.pathname.split('/').filter(Boolean).at(-1)); await detail(page, finalId);
    await page.waitForTimeout(200);
    const frameLog = await page.evaluate(() => { cancelAnimationFrame(window.__handoffRAF); return window.__handoffFrames; });
    report.measurements.handoff = { frames_sampled: frameLog.length, blank_frames: frameLog.filter(f => !f.visible).length, initial_azimuth: angle };
    assert.equal(report.measurements.handoff.blank_frames, 0, 'No empty visual during delayed or cached next/previous handoff');
    await page.unroute('**/*.glb');
    await page.locator('#close').click(); await page.locator('#viewer-dialog').waitFor({ state: 'hidden' });
    await canonicalPoster(page, 'natural-arch');
    assert.equal((await gpu(page)).liveScenes, 0); assert.equal(await page.locator('.model-canvas').count(), 0);
    check('Warm card/detail reuses exact canvas and decoded resource with no network/parse; angle continuity and rapid next/previous stay painted.');
    noSequenceRequests(start);
  } finally { await c.close(); }
}
async function races() {
  const { c, page } = await context();
  try {
    await catalog(page); const start = requests.length;
    let sawFern; const requestedFern = new Promise(resolve => { sawFern = resolve; });
    await page.route('**/fern-cluster.glb', async route => { sawFern(); await new Promise(r => setTimeout(r, 550)); await route.continue().catch(() => {}); });
    await page.locator(selector('fern-cluster')).hover(); await requestedFern;
    await page.locator(selector('conifer-tree')).hover(); await ready(page, 'conifer-tree'); await settled(page);
    assert.equal(await page.locator(`${selector('fern-cluster')} .model-canvas`).count(), 0);
    assert.equal((await preview(page)).activeId, 'conifer-tree'); bounded(await gpu(page));
    await page.unroute('**/fern-cluster.glb'); await page.mouse.move(1, 1); await stopped(page);
    check('Rapid card changes abort the old GLB request and reject stale work, retaining one request/parse lane and one canvas.');
    let releaseDelayed, markDelayed;
    const delayed = new Promise(resolve => { releaseDelayed = resolve; });
    const requested = new Promise(resolve => { markDelayed = resolve; });
    await page.route('**/fern-cluster.glb', async route => { markDelayed(); await delayed; await route.continue().catch(() => {}); });
    await page.locator(selector('fern-cluster')).click(); await requested;
    await page.locator('#close').click(); await page.locator('#viewer-dialog').waitFor({ state: 'hidden' });
    assert.equal(await page.locator('.model-canvas').count(), 0);
    await page.locator(selector('cycad')).click(); releaseDelayed(); await detail(page, 'cycad'); await page.waitForTimeout(200);
    assert((await page.locator('#canvas-host').getAttribute('data-presented-url')).endsWith('/cycad.glb'));
    await page.unroute('**/fern-cluster.glb');
    check('Closing an outstanding cold GLB load and opening another model rejects the abandoned late result.');
    noSequenceRequests(start);
  } finally { await c.close(); }
}
async function failures() {
  const { c, page } = await context();
  try {
    await page.route('**/natural-arch.glb', route => route.fulfill({ status: 404, body: '' }));
    await catalog(page); const start = requests.length;
    await page.locator(selector('natural-arch')).hover();
    await page.waitForFunction(() => document.querySelector('#grid [data-id="natural-arch"]').dataset.previewState === 'fallback');
    assert(await page.locator(`${selector('natural-arch')} img`).isVisible());
    assert.equal(await page.locator('#grid .model-canvas:visible').count(), 0);
    const count = glbs(start).length; await page.waitForTimeout(300);
    assert.equal(glbs(start).length, count, 'A failed preview does not retry while idle');
    noSequenceRequests(start); await screenshot(page, 'failed-model-static');
    await page.unroute('**/natural-arch.glb');
    await page.locator(selector('natural-arch')).click(); await detail(page, 'natural-arch');
    check('A failed GLB keeps the static poster and usable detail link, with no retry loop; a later successful detail load recovers.');
  } finally { await c.close(); }
}
async function touch() {
  const { c, page } = await context({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  try {
    await catalog(page, 'zh-CN/'); const start = requests.length;
    const card = page.locator(selector('conifer-tree')); await card.scrollIntoViewIfNeeded();
    let box = await card.locator('.asset-image').boundingBox(); const session = await c.newCDPSession(page);
    const send = (type, x, y) => session.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1, radiusX: 2, radiusY: 2 }] });
    const x = box.x + box.width * .25, y = box.y + box.height * .5;
    await send('touchStart', x, y);
    for (let i = 1; i <= 6; i++) { await send('touchMove', x + 10 * i, y + 1); await page.waitForTimeout(30); }
    await send('touchEnd'); await ready(page, 'conifer-tree'); await settled(page);
    assert((await preview(page)).frame > 0, 'Horizontal touch changes the actual inspected angle');
    assert(new URL(page.url()).pathname.endsWith('/models/'));
    assert.equal(await page.locator('#grid .model-canvas').count(), 1); bounded(await gpu(page));
    assert(glbs(start).every(r => r.url.endsWith('/conifer-tree.glb'))); noSequenceRequests(start);
    report.measurements.touch = { preview: await preview(page), gpu: await gpu(page) }; await screenshot(page, 'touch-390-chinese-preview');
    check('390 px trusted browser touch: horizontal drag orbits one actual model and suppresses accidental navigation.');
    await card.scrollIntoViewIfNeeded(); box = await card.locator('.asset-image').boundingBox();
    const before = await page.evaluate(() => scrollY);
    await send('touchStart', box.x + box.width / 2, box.y + box.height * .7);
    for (let i = 1; i <= 6; i++) { await send('touchMove', box.x + box.width / 2, box.y + box.height * .7 - i * 20); await page.waitForTimeout(20); }
    await send('touchEnd'); await page.waitForTimeout(200);
    assert(await page.evaluate(() => scrollY) > before + 10, 'Vertical gestures retain native page scrolling');
    await card.scrollIntoViewIfNeeded(); await card.tap(); await detail(page, 'conifer-tree');
    check('Vertical touch retains native scrolling, and a subsequent normal tap opens the actual 3D detail.');
  } finally { await c.close(); }
}
try {
  await mkdir(output, { recursive: true }); await new Promise(r => server.listen(0, '127.0.0.1', r));
  base = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  report.chromium_version = browser.version();
  await desktop(); await races(); await failures(); await touch();
  assert.deepEqual(report.page_errors, []); report.status = 'pass';
  console.log(JSON.stringify({ status: report.status, checks: report.checks, measurements: report.measurements }, null, 2));
} catch (error) {
  report.status = 'fail'; report.error = error.stack; console.error(error);
  try { if (current && !current.isClosed()) await screenshot(current, 'failure'); } catch {}
  process.exitCode = 1;
} finally {
  report.requests = requests; await writeFile(resolve(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  await browser?.close(); if (server.listening) await new Promise(r => server.close(r));
}
