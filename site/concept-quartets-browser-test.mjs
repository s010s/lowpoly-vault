/** Exercise the actual unified gallery with the bounded marine quartet in both locales. */
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { mkdir, readFile, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { createHash } from 'node:crypto';
import { CONCEPT_QUARTETS_IDS } from './concept-quartets-release.mjs';

const BASE_COUNT = 182;
const minimumCount = BASE_COUNT + CONCEPT_QUARTETS_IDS.length;
const expectedIds = ['burgessia', 'emeraldella', 'sanctacaris', 'tuzoia'];
const root = resolve(process.env.GALLERY_DIR || 'dist');
const out = resolve(process.env.QA_OUTPUT_DIR || 'qa/quartets-release-20261019/browser');
const prefix = process.env.SITE_BASE || '/lowpoly-vault/';
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const report = {
  status: 'running', source_commit: process.env.GITHUB_SHA || null,
  minimum_count: minimumCount, cases: [], errors: [],
  limitations: ['Chromium SwiftShader with emulated mobile; no physical-device or intended museum-scene performance claim.'],
};
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.webp': 'image/webp', '.glb': 'model/gltf-binary', '.blend': 'application/octet-stream' };
let browser, server, currentPage, currentCase;
await mkdir(out, { recursive: true });

try {
  assert.deepEqual(CONCEPT_QUARTETS_IDS, expectedIds);
  const manifest = JSON.parse(await readFile(resolve(root, 'assets/manifest.json'), 'utf8'));
  assert(!manifest.review_only, 'Use the published unified gallery, never an isolated review catalog');
  assert.deepEqual(manifest.publication.approved_concept_quartets_ids, CONCEPT_QUARTETS_IDS);
  const expectedCount = manifest.assets.length;
  assert(expectedCount >= minimumCount, 'Later independently accepted releases may extend the catalog');
  report.expected_count = expectedCount;
  assert.equal(new Set(manifest.assets.map(asset => asset.id)).size, expectedCount);
  assert.deepEqual(manifest.assets.slice(BASE_COUNT, minimumCount).map(asset => asset.id).sort(), expectedIds);
  assert(!manifest.assets.some(asset => asset.id === 'ctenoimbricata'));

  server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, 'http://localhost');
      assert(url.pathname.startsWith(prefix));
      let file = resolve(root, decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html');
      assert(file === root || file.startsWith(root + sep));
      if ((await stat(file)).isDirectory()) file = resolve(file, 'index.html');
      const bytes = await readFile(file);
      res.writeHead(200, { 'Content-Type': mime[extname(file)] || 'application/octet-stream', 'Content-Length': bytes.length }).end(bytes);
    } catch {
      res.writeHead(404).end();
    }
  });
  await new Promise((done, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', done); });
  const base = `http://127.0.0.1:${server.address().port}${prefix}`;
  report.base = base;
  report.published_count = manifest.assets.length;
  browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || undefined,
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
  });
  report.browser = browser.version();

  for (const mobile of [false, true]) {
    const label = mobile ? 'mobile-zh-CN' : 'desktop-en';
    const lang = mobile ? 'zh' : 'en';
    const context = await browser.newContext({
      viewport: mobile ? { width: 390, height: 844 } : { width: 1440, height: 1000 },
      isMobile: mobile, hasTouch: mobile, reducedMotion: 'reduce', acceptDownloads: true,
    });
    const page = currentPage = await context.newPage();
    page.setDefaultTimeout(45000);
    const recordError = (kind, message) => report.errors.push({ viewport: label, id: currentCase?.id || null, kind, message });
    page.on('pageerror', error => recordError('pageerror', error.message));
    page.on('response', response => { if (response.status() >= 400) recordError('http', `${response.status()} ${response.url()}`); });
    page.on('requestfailed', request => {
      // Browser-cancelled requests are expected when a selection supersedes an in-flight model.
      const error = request.failure()?.errorText || 'Unknown request failure';
      if (!/ERR_ABORTED|NS_BINDING_ABORTED/i.test(error)) recordError('request', `${error} ${request.url()}`);
    });
    page.on('console', message => { if (message.type() === 'error') recordError('console', message.text()); });

    try {
      await page.goto(new URL((mobile ? 'zh-CN/' : '') + 'models/?model=' + CONCEPT_QUARTETS_IDS[0], base).href);
      await page.waitForFunction(count => window.__gallery?.models.length === count, expectedCount);
      assert.equal(await page.locator('html').getAttribute('lang'), mobile ? 'zh-CN' : 'en');
      const catalog = await page.evaluate(() => ({
        ids: window.__gallery.models.map(asset => asset.id),
        result_count: window.__gallery.state.results.length,
        result_label: document.querySelector('#results').textContent,
        renderers: document.querySelectorAll('canvas.preview-renderer').length,
        legacy_grid: !!document.querySelector('#grid'),
      }));
      assert.deepEqual(catalog.ids, manifest.assets.map(asset => asset.id), 'The shared gallery serves the whole published catalog');
      assert.equal(catalog.result_count, expectedCount);
      assert(catalog.result_label.includes(String(expectedCount)));
      assert.equal(catalog.renderers, 1);
      assert.equal(catalog.legacy_grid, false);

      for (const id of CONCEPT_QUARTETS_IDS) {
        const asset = manifest.assets.find(item => item.id === id);
        currentCase = { id, viewport: label, locale: mobile ? 'zh-CN' : 'en', status: 'running' };
        report.cases.push(currentCase);
        if (mobile && await page.locator('#mobile-back').isVisible()) await page.locator('#mobile-back').tap();
        await page.locator('#search').fill(id);
        await page.locator('#search').press('Enter');
        await page.waitForFunction(id => window.__gallery.state.query === id && window.__gallery.state.results.some(asset => asset.id === id), id);
        const slot = page.locator(`#slots [data-id="${id}"]`);
        assert(await slot.isVisible(), `${id}: discoverable through ordinary gallery search`);
        if (mobile) {
          await slot.tap();
          await page.waitForFunction(id => document.body.classList.contains('mobile-detail') && document.querySelector('#detail').dataset.modelId === id, id);
          assert(await page.locator('#mobile-interact').isVisible());
          await page.locator('#mobile-interact').tap();
        } else {
          await slot.click();
        }
        await page.waitForFunction(id => {
          const detail = document.querySelector('#detail'), poster = document.querySelector('#detail-poster');
          return detail?.dataset.state === 'ready' && detail.dataset.modelId === id
            && poster?.dataset.modelId === id && poster.dataset.state === 'ready'
            && poster.complete && poster.naturalWidth > 0;
        }, id);

        const snapshot = await page.evaluate(() => {
          const gallery = window.__gallery, renderer = gallery.renderer;
          const gl = renderer.renderer.getContext(), poster = document.querySelector('#detail-poster');
          renderer.draw();
          const canvas = renderer.renderer.domElement;
          return {
            selected: gallery.state.selected, rendered_asset: renderer.detail.asset.id,
            first_frame: renderer.stats.detailFirstFrameId,
            triangles: renderer.renderer.info.render.triangles,
            gl_error: gl.getError(), context_lost: gl.isContextLost(),
            canvas_width: canvas.width, canvas_height: canvas.height,
            poster: poster.currentSrc, poster_width: poster.naturalWidth, poster_height: poster.naturalHeight,
            poster_source: poster.dataset.source, poster_state: poster.dataset.state,
            body_overflow: document.body.scrollWidth > innerWidth + 1,
            document_overflow: document.documentElement.scrollWidth > innerWidth + 1,
          };
        });
        assert.equal(snapshot.selected, id);
        assert.equal(snapshot.rendered_asset, id);
        assert.equal(snapshot.first_frame, id);
        assert(snapshot.triangles > 0);
        assert.equal(snapshot.gl_error, 0);
        assert.equal(snapshot.context_lost, false);
        assert(snapshot.canvas_width > 0 && snapshot.canvas_height > 0);
        assert.equal(snapshot.poster, new URL(`gallery/posters/${id}.png`, base).href);
        assert.equal(snapshot.poster_source, 'canonical', 'A missing gallery poster must not silently pass through preview fallback');
        assert.equal(snapshot.poster_state, 'ready');
        assert(snapshot.poster_width > 0 && snapshot.poster_height > 0);
        assert.equal(snapshot.body_overflow, false);
        assert.equal(snapshot.document_overflow, false);

        await page.locator('#info').click();
        const panel = page.locator('#info-panel');
        assert(await panel.isVisible(), 'Sources must appear in the visible model information panel');
        const content = await page.locator('#info-content').textContent();
        assert(content.includes(asset.name[lang]));
        assert(content.includes(asset.scientific_scope[lang]), 'The bounded scientific claims must remain visible in each language');
        assert(content.includes(asset.description[lang]));
        const sourceLinks = await page.locator('#info-content a').evaluateAll(nodes => nodes.map(anchor => ({ href: anchor.href, label: anchor.textContent.trim() })));
        assert(asset.sources.length > 0);
        for (const source of asset.sources) {
          const href = new URL(source.url).href;
          const title = source.title || source.id || source.url;
          assert(sourceLinks.some(link => link.href === href && link.label.includes(title)), 'Every frozen reference has its accessible source label');
          const link = page.locator('#info-content a').filter({ hasText: title }).first();
          await link.scrollIntoViewIfNeeded();
          assert(await link.isVisible(), `${id}: source label is reachable inside the visible panel`);
        }
        const panelBounds = await panel.boundingBox();
        const viewport = page.viewportSize();
        assert(panelBounds && panelBounds.x >= -1 && panelBounds.y >= -1
          && panelBounds.x + panelBounds.width <= viewport.width + 1
          && panelBounds.y + panelBounds.height <= viewport.height + 1, 'The information panel fits the viewport');
        assert(await page.evaluate(() => Math.max(document.body.scrollWidth, document.documentElement.scrollWidth) <= innerWidth + 1));
        await page.screenshot({ path: resolve(out, `${label}-${id}-sources.png`) });
        await page.keyboard.press('Escape');
        await panel.waitFor({ state: 'hidden' });

        const downloads = {};
        for (const [key, selector] of [['glb', '#download'], ['blend', '#blend']]) {
          const control = page.locator(selector);
          assert(await control.isVisible());
          assert((await control.textContent()).trim(), 'Download controls have visible labels');
          const href = await control.evaluate(anchor => anchor.href);
          assert.equal(href, new URL(asset[key], base).href);
          const downloadReady = page.waitForEvent('download');
          await control.click();
          const download = await downloadReady;
          assert.equal(download.url(), href);
          assert.equal(await download.failure(), null);
          const downloadedPath = await download.path();
          assert(downloadedPath, 'The browser must complete the actual download');
          const bytes = await readFile(downloadedPath);
          assert(bytes.length > 0);
          assert.equal(sha(bytes), asset.sha256[key], `${id}: downloaded ${key} matches the frozen artifact`);
          downloads[key] = { url: href, sha256: sha(bytes), bytes: bytes.length, filename: download.suggestedFilename() };
        }
        await page.screenshot({ path: resolve(out, `${label}-${id}.png`) });
        Object.assign(currentCase, { status: 'pass', ...snapshot, sources: sourceLinks, downloads });
      }
    } finally {
      if (currentCase?.status === 'running') {
        currentCase.status = 'fail';
        await page.screenshot({ path: resolve(out, `${label}-${currentCase.id}-failure.png`) }).catch(() => {});
      }
      await context.close();
      currentPage = null;
    }
  }
  assert.equal(report.cases.length, CONCEPT_QUARTETS_IDS.length * 2);
  assert(report.cases.every(test => test.status === 'pass'));
  assert.deepEqual(report.errors, []);
  report.status = 'pass';
} catch (error) {
  report.status = 'fail';
  report.error = error.stack;
  process.exitCode = 1;
} finally {
  await browser?.close();
  if (server?.listening) await new Promise(done => server.close(done));
  await writeFile(resolve(out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
}
