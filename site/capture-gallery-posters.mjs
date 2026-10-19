/** Complete the published gallery using its actual approved browser renderer. */
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { cp, mkdir, mkdtemp, readFile, realpath, rename, rm, stat, writeFile } from 'node:fs/promises';
import { dirname, extname, resolve, sep } from 'node:path';
import { auditGalleryAssets } from './gallery-assets.mjs';
import { normalizeSiteBase } from './routes.js';
import { CAPTURE_POLICY, posterInputKey } from './gallery-poster-inputs.mjs';

const root = process.cwd(), outputRoot = resolve(process.env.GALLERY_OUTPUT_DIR || 'dist');
const manifest = JSON.parse(await readFile(resolve(outputRoot, 'assets/manifest.json'), 'utf8'));
const initial = await auditGalleryAssets(manifest, { root, outputRoot });
if (!initial.coverage.missing.length) {
  await auditGalleryAssets(manifest, { root, outputRoot, requireComplete: true });
  if (process.argv.includes('--source-output')) await persistSourceGallery();
  console.log(`Gallery capture complete: ${initial.coverage.matched}/${manifest.assets.length} published assets have sealed detail/wheel posters; nothing to recapture.`);
  process.exit(0);
}

let browser, server, staging;
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const base = normalizeSiteBase(process.env.SITE_BASE || '/');
const mime = { '.html':'text/html; charset=utf-8', '.js':'text/javascript', '.css':'text/css', '.json':'application/json', '.png':'image/png', '.webp':'image/webp', '.glb':'model/gltf-binary', '.svg':'image/svg+xml' };
async function persistSourceGallery() {
  const sourceStaging = await mkdtemp(resolve(root, 'site/public/.gallery-source-'));
  try {
    await cp(resolve(outputRoot, 'gallery'), resolve(sourceStaging, 'gallery'), { recursive:true });
    await auditGalleryAssets(manifest, { root, outputRoot:sourceStaging, requireComplete:true });
    const sourceTarget = resolve(root, 'site/public/gallery'), sourcePrevious = resolve(sourceStaging, 'previous-gallery');
    await rename(sourceTarget, sourcePrevious);
    try { await rename(resolve(sourceStaging, 'gallery'), sourceTarget); }
    catch (error) { await rename(sourcePrevious, sourceTarget); throw error; }
    await auditGalleryAssets(manifest, { root, requireComplete:true });
    console.log('Saved the complete sealed gallery to site/public/gallery; future regular builds include it without browser capture.');
  } finally { await rm(sourceStaging, { recursive:true, force:true }); }
}
async function localSite() {
  const rootReal = await realpath(outputRoot);
  server = createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      if (!pathname.startsWith(base) || pathname.includes('\\') || pathname.includes('\0')) { response.writeHead(404).end(); return; }
      let file = resolve(outputRoot, pathname.slice(base.length) || '.');
      if (file !== outputRoot && !file.startsWith(outputRoot + sep)) { response.writeHead(404).end(); return; }
      if ((await stat(file)).isDirectory()) file = resolve(file, 'index.html');
      const real = await realpath(file);
      if (!real.startsWith(rootReal + sep)) { response.writeHead(404).end(); return; }
      response.writeHead(200, { 'Content-Type': mime[extname(real)] || 'application/octet-stream', 'Cache-Control':'no-store' });
      response.end(await readFile(real));
    } catch (error) { response.writeHead(error.code === 'ENOENT' ? 404 : 500).end(); }
  });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  return `http://127.0.0.1:${server.address().port}${base}models/`;
}

try {
  const url = process.env.GALLERY_URL || await localSite();
  const executablePath = process.env.CHROMIUM_PATH;
  browser = await chromium.launch({ ...(executablePath ? { executablePath } : {}), headless:true, args:CAPTURE_POLICY.args });
  const toolchain = JSON.parse(await readFile(resolve(root,'node_modules/playwright-core/browsers.json'),'utf8'));
  assert.equal(browser.version(), toolchain.browsers.find(item => item.name === 'chromium').browserVersion, 'Capture requires the lockfile-pinned Chromium; custom browser versions cannot stamp matching inputs');
  const page = await browser.newPage({ viewport:CAPTURE_POLICY.viewport, deviceScaleFactor:CAPTURE_POLICY.deviceScaleFactor, reducedMotion:CAPTURE_POLICY.reducedMotion });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error' && /THREE\.|WebGL|shader|GL_INVALID|CONTEXT_LOST/i.test(message.text())) errors.push(message.text()); });
  await page.goto(url, { waitUntil:'networkidle', timeout:120000 });
  await page.waitForFunction(() => window.__preview?.renderer?.detail?.model && window.__preview?.models?.length, null, { timeout:120000 });
  const loaded = await page.evaluate(() => window.__preview.models.map(asset => ({ id:asset.id, glb:asset.glb, sha256:asset.sha256?.glb })));
  const scope = rows => rows.map(row => `${row.id}\0${row.glb}\0${row.sha256}`).sort();
  assert.deepEqual(scope(loaded), scope(manifest.assets.map(asset => ({id:asset.id,glb:asset.glb,sha256:asset.sha256.glb}))), 'Capture page must load the exact complete published catalog');
  await page.evaluate(() => { window.__preview.renderer.stopHover(); window.__preview.settler?.stop(); });
  assert.equal(errors.length, 0, `Gallery startup errors: ${errors.join('; ')}`);

  staging = await mkdtemp(resolve(outputRoot, '.gallery-capture-'));
  await cp(resolve(outputRoot, 'gallery'), resolve(staging, 'gallery'), { recursive:true });
  const resources = structuredClone(initial.resources), assets = new Map(manifest.assets.map(asset => [asset.id, asset]));
  for (const [index, id] of initial.coverage.missing.entries()) {
    const capture = await page.evaluate(async id => {
      const preview = window.__preview, asset = preview.models.find(asset => asset.id === id);
      if (!asset) throw new Error(`Missing published asset ${id}`);
      const gl = preview.renderer.renderer.getContext();
      if (gl.isContextLost()) throw new Error(`WebGL context lost before ${id}`);
      const detail = await preview.renderer.poster(asset);
      const wheel = await preview.renderer.poster(asset, { wheel:true });
      const error = gl.getError();
      if (gl.isContextLost() || error !== gl.NO_ERROR) throw new Error(`WebGL capture failed for ${id}: ${error}`);
      return { detail, wheel, wheelSpec:preview.renderer.lastPosterSpec };
    }, id);
    const poster = { source_glb_sha256:assets.get(id).sha256.glb, input_sha256:posterInputKey(assets.get(id),initial.inputState.shared), browser_version:browser.version(), wheelSpec:capture.wheelSpec };
    resources.files = resources.files.filter(file => ![`gallery/posters/${id}.png`, `gallery/posters/${id}-wheel.png`].includes(file.path));
    for (const kind of ['detail', 'wheel']) {
      const data = capture[kind];
      assert(typeof data === 'string' && data.startsWith('data:image/png;base64,'), `PNG capture failed: ${id} ${kind}`);
      const bytes = Buffer.from(data.slice('data:image/png;base64,'.length), 'base64');
      const path = `gallery/posters/${id}${kind === 'wheel' ? '-wheel' : ''}.png`;
      const target = resolve(staging, path);
      await mkdir(dirname(target), { recursive:true }); await writeFile(target, bytes);
      resources.files.push({path, bytes:bytes.length, sha256:sha256(bytes)}); poster[kind] = path;
    }
    resources.posters[id] = poster;
    assert.equal(errors.length, 0, `Gallery render errors: ${errors.join('; ')}`);
    console.log(`Gallery capture ${index + 1}/${initial.coverage.missing.length}: ${id}`);
  }
  resources.generated_capture = { renderer:'approved PreviewRenderer.poster', browser:browser.version(), source_renderer_sha256:resources.source_renderer_sha256, runtime_renderer_sha256:sha256(await readFile(resolve(root,'site/gallery/renderer.js'))), assets:initial.coverage.missing, published_total:manifest.assets.length };
  await writeFile(resolve(staging, 'gallery/resources.json'), JSON.stringify(resources, null, 2) + '\n');
  await auditGalleryAssets(manifest, { root, outputRoot:staging, requireComplete:true });
  const previous = resolve(staging, 'previous-gallery');
  await rename(resolve(outputRoot, 'gallery'), previous);
  try { await rename(resolve(staging, 'gallery'), resolve(outputRoot, 'gallery')); }
  catch (error) { await rename(previous, resolve(outputRoot, 'gallery')); throw error; }
  const final = await auditGalleryAssets(manifest, { root, outputRoot, requireComplete:true });
  if (process.argv.includes('--source-output')) await persistSourceGallery();
  console.log(`Gallery capture complete: ${final.coverage.matched}/${manifest.assets.length} published assets, ${final.files} sealed resource files, ${final.bytes} bytes. Reviewed poster bytes and framing preserved.`);
} finally {
  await browser?.close();
  if (server?.listening) await new Promise(resolve => server.close(resolve));
  if (staging) await rm(staging, { recursive:true, force:true });
}
