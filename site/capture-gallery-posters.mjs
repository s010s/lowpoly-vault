// BEGIN GALLERY POSTER V3 ORCHESTRATION
// Single supported entry: this narrow migration uses the same runtime recipe.
if(process.argv.includes('--detail-presentations')){
 const delta=process.argv.find(arg=>arg.startsWith('--detail-ids='));
 if(delta){const {captureDetailDelta}=await import('./detail-capture-delta.mjs');await captureDetailDelta(delta.slice('--detail-ids='.length).split(',').filter(Boolean));}
 else {const {default:detailIndex}=await import('./gallery/detail-presentations-index.js');if(Object.keys(detailIndex.presentations||{}).length)throw new Error('Existing right deliveries require explicit --detail-ids for incremental capture; a full renderer migration needs separate review');await import('./capture-detail-presentations.mjs');}
 process.exit(0);
}
import {preparePosterCapture,completePosterCapture} from './gallery-poster-orchestration.mjs';
// END GALLERY POSTER V3 ORCHESTRATION
/** Complete the published gallery using its actual approved browser renderer. */
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { cp, mkdir, mkdtemp, readFile, realpath, rename, rm, stat, writeFile } from 'node:fs/promises';
import { dirname, extname, resolve, sep } from 'node:path';
import { auditGalleryAssets } from './gallery-assets.mjs';
import { CAPTURE_POLICY, posterInputKey, posterRendererFiles } from './gallery-poster-inputs.mjs';

const root = process.cwd(), outputRoot = resolve(process.env.GALLERY_OUTPUT_DIR || 'dist');
const manifest = JSON.parse(await readFile(resolve(outputRoot, 'assets/manifest.json'), 'utf8'));
const initial = await auditGalleryAssets(manifest, { root, outputRoot });
const verifyRecipe = process.argv.includes('--verify-recipe');
// BEGIN GALLERY POSTER V3 ORCHESTRATION
if (!verifyRecipe) await preparePosterCapture(initial,{root,outputRoot,manifest});
// END GALLERY POSTER V3 ORCHESTRATION
if (!initial.inputState.capture.length && !verifyRecipe) {
  await auditGalleryAssets(manifest, { root, outputRoot, requireComplete: true });
  if (process.argv.includes('--source-output')) await persistSourceGallery();
  console.log(`Gallery capture complete: ${initial.coverage.matched}/${manifest.assets.length} published assets have sealed detail/wheel posters; nothing to recapture.`);
// BEGIN GALLERY POSTER V3 ORCHESTRATION
  await completePosterCapture(initial,initial.resources);
// END GALLERY POSTER V3 ORCHESTRATION
  process.exit(0);
}

let browser, server, reviewServer, staging;
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const mime = { '.html':'text/html; charset=utf-8', '.js':'text/javascript', '.mjs':'text/javascript', '.css':'text/css', '.json':'application/json', '.png':'image/png', '.webp':'image/webp', '.glb':'model/gltf-binary', '.svg':'image/svg+xml' };
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
  const base = CAPTURE_POLICY.site_base;
  const rendererFiles = new Set(await posterRendererFiles(root));
  const glbs = new Map(manifest.assets.map(asset => [asset.glb,asset.sha256.glb]));
  const prefix = `${base}__poster_capture__/`;
  const html = `<!doctype html><link rel="icon" href="data:,"><body data-site-base="${base}"><div id="stage" style="width:512px;height:512px"></div><script type="importmap">${JSON.stringify({imports:{three:prefix+'node_modules/three/build/three.module.js','three/':prefix+'node_modules/three/','three/addons/':prefix+'node_modules/three/examples/jsm/'}})}</script><script type="module">import {PreviewRenderer} from '${prefix}site/gallery/renderer.js'; const models=await (await fetch('${prefix}manifest.json')).json(); window.__posterCapture={renderer:new PreviewRenderer(document.querySelector('#stage'),()=>{}),models};</script>`;
  server = createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      if (pathname.includes('\\') || pathname.includes('\0')) throw new Error('Invalid capture URL');
      if (pathname === prefix) { response.writeHead(200, {'Content-Type':'text/html; charset=utf-8'}).end(html); return; }
      if (pathname === prefix+'manifest.json') { response.writeHead(200, {'Content-Type':'application/json'}).end(JSON.stringify(manifest.assets)); return; }
      let file, parent, expectedFile, expectedGLB;
      if (pathname.startsWith(prefix)) {
        const path = pathname.slice(prefix.length);
        if (!rendererFiles.has(path) && !/^node_modules\/three\/[a-zA-Z0-9_./-]+\.js$/.test(path)) throw new Error('Unlisted renderer dependency');
        file = resolve(root,path); parent = path.startsWith('node_modules/') ? await realpath(resolve(root,'node_modules/three')) : await realpath(root);
        expectedFile=resolve(parent,path.startsWith('node_modules/')?path.slice('node_modules/three/'.length):path);
      } else {
        if (!pathname.startsWith(base) || !glbs.has(pathname.slice(base.length))) throw new Error('Unlisted capture resource');
        file = resolve(outputRoot,pathname.slice(base.length)); parent = await realpath(outputRoot); expectedGLB=glbs.get(pathname.slice(base.length)); expectedFile=resolve(parent,pathname.slice(base.length));
      }
      const real = await realpath(file);
      if (!real.startsWith(parent+sep) || real!==expectedFile) throw new Error('Capture path escapes its input root or follows a symlink');
      const bytes=await readFile(real);
      if(expectedGLB)assert.equal(sha256(bytes),expectedGLB,'Capture GLB differs from checked source');
      response.writeHead(200, { 'Content-Type': mime[extname(real)] || 'application/octet-stream', 'Cache-Control':'no-store' }).end(bytes);
    } catch { response.writeHead(404).end(); }
  });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  return `http://127.0.0.1:${server.address().port}${prefix}`;
}

// Comparison only: the regular built app runs in a separate browser context/origin.
// It is never used as the source of a stamped capture.
async function currentAppSite(){
 const base=process.env.SITE_BASE||'/';
 assert(/^\/(?:[a-zA-Z0-9_.-]+\/)*$/.test(base)&&!base.split('/').some(part=>part==='.'||part==='..'),'Comparison requires a normalized local SITE_BASE');
 const parent=await realpath(outputRoot);
 reviewServer=createServer(async(request,response)=>{try{
  const pathname=decodeURIComponent(new URL(request.url,'http://localhost').pathname);
  if(!pathname.startsWith(base)||pathname.includes('\\')||pathname.includes('\0'))throw new Error('Invalid URL');
  let file=resolve(outputRoot,pathname.slice(base.length)||'.');
  if((await stat(file)).isDirectory())file=resolve(file,'index.html');
  const real=await realpath(file);if(!real.startsWith(parent+sep))throw new Error('Outside output');
  response.writeHead(200,{'Content-Type':mime[extname(real)]||'application/octet-stream'}).end(await readFile(real));
 }catch{response.writeHead(404).end();}});
 await new Promise((resolve,reject)=>{reviewServer.once('error',reject);reviewServer.listen(0,'127.0.0.1',resolve);});
 return `http://127.0.0.1:${reviewServer.address().port}${base}models/`;
}
async function capturePair(page,id,isolated=true){
 return page.evaluate(async({id,isolated})=>{
  const preview=isolated?window.__posterCapture:window.__preview,asset=preview.models.find(asset=>asset.id===id);
  if(!asset)throw new Error(`Missing published asset ${id}`);
  const gl=preview.renderer.renderer.getContext();if(gl.isContextLost())throw new Error(`WebGL context lost before ${id}`);
  const detail=await preview.renderer.poster(asset),wheel=await preview.renderer.poster(asset,{wheel:true}),error=gl.getError();
  if(gl.isContextLost()||error!==gl.NO_ERROR)throw new Error(`WebGL capture failed for ${id}: ${error}`);
  return {detail,wheel,wheelSpec:preview.renderer.lastPosterSpec};
 },{id,isolated});
}

try {
  assert(!process.env.GALLERY_URL, 'Hash-bound capture requires the isolated local renderer, never an external page');
  const url = await localSite();
  assert.equal(process.versions.node.split('.')[0], CAPTURE_POLICY.node_major, 'Capture requires the versioned Node toolchain');
  const executablePath = process.env.CHROMIUM_PATH;
  browser = await chromium.launch({ ...(executablePath ? { executablePath } : {}), headless:true, args:CAPTURE_POLICY.args });
  const toolchain = JSON.parse(await readFile(resolve(root,'node_modules/playwright-core/browsers.json'),'utf8'));
  assert.equal(browser.version(), toolchain.browsers.find(item => item.name === 'chromium').browserVersion, 'Capture requires the lockfile-pinned Chromium; custom browser versions cannot stamp matching inputs');
  const page = await browser.newPage({ viewport:CAPTURE_POLICY.viewport, deviceScaleFactor:CAPTURE_POLICY.deviceScaleFactor, reducedMotion:CAPTURE_POLICY.reducedMotion, serviceWorkers:'block' });
  const errors = [];
  await page.route('**/*', route => new URL(route.request().url()).origin === new URL(url).origin ? route.continue() : route.abort());
  page.on('response', response => { if (response.status() >= 400) errors.push(`Unlisted or missing capture input: ${response.url()}`); });
  page.on('requestfailed', request => errors.push(`Blocked capture input: ${request.url()}`));
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error' && /THREE\.|WebGL|shader|GL_INVALID|CONTEXT_LOST/i.test(message.text())) errors.push(message.text()); });
  await page.goto(url, { waitUntil:'networkidle', timeout:120000 });
  await page.waitForFunction(() => window.__posterCapture?.renderer && window.__posterCapture?.models?.length, null, { timeout:120000 });
  const loaded = await page.evaluate(() => window.__posterCapture.models.map(asset => ({ id:asset.id, glb:asset.glb, sha256:asset.sha256?.glb })));
  const scope = rows => rows.map(row => `${row.id}\0${row.glb}\0${row.sha256}`).sort();
  assert.deepEqual(scope(loaded), scope(manifest.assets.map(asset => ({id:asset.id,glb:asset.glb,sha256:asset.sha256.glb}))), 'Capture page must load the exact complete published catalog');
  await page.evaluate(() => window.__posterCapture.renderer.stopHover());
  assert.equal(errors.length, 0, `Gallery startup errors: ${errors.join('; ')}`);

  let comparisonPage;
  if(verifyRecipe){
    const appURL=await currentAppSite();
    comparisonPage=await browser.newPage({viewport:CAPTURE_POLICY.viewport,deviceScaleFactor:CAPTURE_POLICY.deviceScaleFactor,reducedMotion:CAPTURE_POLICY.reducedMotion,serviceWorkers:'block'});
    await comparisonPage.route('**/*',route=>new URL(route.request().url()).origin===new URL(appURL).origin?route.continue():route.abort());
    comparisonPage.on('pageerror',error=>errors.push(error.message));
    await comparisonPage.goto(appURL,{waitUntil:'networkidle',timeout:120000});
    await comparisonPage.waitForFunction(()=>window.__preview?.renderer?.detail?.model&&window.__preview?.models?.length,null,{timeout:120000});
    await comparisonPage.evaluate(()=>{window.__preview.renderer.stopHover();window.__preview.settler?.stop();});
  }
  staging = await mkdtemp(resolve(outputRoot, '.gallery-capture-'));
  await cp(resolve(outputRoot, 'gallery'), resolve(staging, 'gallery'), { recursive:true });
  const resources = structuredClone(initial.resources), assets = new Map(manifest.assets.map(asset => [asset.id, asset]));
  const selected = verifyRecipe ? ['metaspriggina','strophomena','waptia','conifer-tree','confuciusornis','diplomystus'] : initial.inputState.capture;
  for (const [index, id] of selected.entries()) {
    const capture = await capturePair(page,id);
    if (verifyRecipe) {
      const appCapture=await capturePair(comparisonPage,id,false);
      for (const kind of ['detail','wheel']) assert.equal(sha256(capture[kind]),sha256(appCapture[kind]),`Isolated recipe differs from the current app: ${id} ${kind}`);
      assert.equal(errors.length,0,errors.join('; '));
      console.log(`Isolated recipe matches current app detail/wheel pixels: ${id}`); continue;
    }
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
    console.log(`Gallery capture ${index + 1}/${initial.inputState.capture.length}: ${id}`);
  }
  if (verifyRecipe) process.exitCode = 0;
  else {
  resources.generated_capture = { renderer:'approved PreviewRenderer.poster', browser:browser.version(), source_renderer_sha256:resources.source_renderer_sha256, runtime_renderer_sha256:sha256(await readFile(resolve(root,'site/gallery/renderer.js'))), assets:initial.inputState.capture, published_total:manifest.assets.length };
  await writeFile(resolve(staging, 'gallery/resources.json'), JSON.stringify(resources, null, 2) + '\n');
  await auditGalleryAssets(manifest, { root, outputRoot:staging, requireComplete:true });
  const previous = resolve(staging, 'previous-gallery');
  await rename(resolve(outputRoot, 'gallery'), previous);
  try { await rename(resolve(staging, 'gallery'), resolve(outputRoot, 'gallery')); }
  catch (error) { await rename(previous, resolve(outputRoot, 'gallery')); throw error; }
  const final = await auditGalleryAssets(manifest, { root, outputRoot, requireComplete:true });
  if (process.argv.includes('--source-output')) await persistSourceGallery();
// BEGIN GALLERY POSTER V3 ORCHESTRATION
  await completePosterCapture(initial,final.resources);
// END GALLERY POSTER V3 ORCHESTRATION
  console.log(`Gallery capture complete: ${final.coverage.matched}/${manifest.assets.length} published assets, ${final.files} sealed resource files, ${final.bytes} bytes. Reviewed poster bytes and framing preserved.`);
  }
} finally {
  await browser?.close();
  if (server?.listening) await new Promise(resolve => server.close(resolve));
  if (reviewServer?.listening) await new Promise(resolve => reviewServer.close(resolve));
  if (staging) await rm(staging, { recursive:true, force:true });
}
