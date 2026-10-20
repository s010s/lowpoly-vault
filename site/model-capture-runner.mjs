/** Explicit draft-only path through the existing real PreviewRenderer.
 * Never edits shared gallery metadata or emits a trusted QA/publication proof. */
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile, realpath} from 'node:fs/promises';
import {resolve, extname, sep} from 'node:path';
import {chromium} from 'playwright';
import {CAPTURE_POLICY, posterSharedInputs, posterRendererFiles} from './gallery-poster-inputs.mjs';
import {assetFileAllowlist} from './asset-delivery.mjs';
import {localReader} from './model-registry-cli.mjs';
import {digest, hashBytes} from './model-registry.mjs';
import {createModelCaptureDraft, writeModelCaptureDraft} from './model-capture-package.mjs';

const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
export function parseModelCaptureOptions(args) {
  const options = {};
  for (let i = 0; i < args.length; i += 2) {
    assert(['--package-output', '--model-ids'].includes(args[i]) && args[i + 1] && !Object.hasOwn(options, args[i]), 'Package mode requires unique --package-output PATH and --model-ids ID[,ID]; no source-output/verify-recipe');
    options[args[i]] = args[i + 1];
  }
  assert(options['--package-output'] && options['--model-ids'], 'Package output and explicit model IDs are both required');
  const modelIDs = options['--model-ids'].split(',');
  assert(modelIDs.every(id => ID.test(id)) && new Set(modelIDs).size === modelIDs.length, 'Unique canonical capture IDs required');
  return {packageRoot: resolve(options['--package-output']), modelIDs: modelIDs.sort()};
}
export function selectPackageModels(manifest, modelIDs) {
  assert(Array.isArray(modelIDs) && modelIDs.length > 0 && modelIDs.every(id => ID.test(id)) && new Set(modelIDs).size === modelIDs.length, 'Explicit unique model capture scope required');
  assetFileAllowlist(manifest);
  const byID = new Map(manifest.assets.map(asset => [asset.id, asset]));
  assert.equal(byID.size, manifest.assets.length, 'Duplicate manifest model ID');
  return [...modelIDs].sort().map(id => { assert(byID.has(id), `Unknown package capture model: ${id}`); return byID.get(id); });
}
export async function packageCaptureInputs(root) {
  const shared = await posterSharedInputs(root), files = [];
  // Package orchestration is a distinct recipe, not a forged legacy capture stamp.
  for (const path of ['site/model-capture-runner.mjs', 'site/model-capture-package.mjs']) {
    const full = resolve(root, path); assert.equal(await realpath(full), full, 'Package recipe symlink rejected');
    files.push([path, hashBytes(await readFile(full))]);
  }
  return {...shared, sha256: digest({domain: 'unverified-per-model-capture-v1', shared_sha256: shared.sha256, files}), package_files: files, legacy_shared_sha256: shared.sha256};
}
export function storeCapturedModel({asset, shared, browserVersion, capture, read, packageRoot}) {
  const pixels = {};
  for (const kind of ['detail', 'wheel']) {
    const data = capture[kind]; assert(typeof data === 'string' && /^data:image\/png;base64,[A-Za-z0-9+/]+={0,2}$/.test(data), `Invalid ${kind} PNG data URL`);
    pixels[kind] = Buffer.from(data.slice('data:image/png;base64,'.length), 'base64');
  }
  return writeModelCaptureDraft(createModelCaptureDraft({asset, shared, browserVersion, pixels, wheelSpec: capture.wheelSpec, read}), packageRoot);
}

export async function runModelCapturePackages({root = process.cwd(), outputRoot = process.env.GALLERY_OUTPUT_DIR || 'dist', packageRoot, modelIDs}) {
  root = resolve(root); outputRoot = resolve(root, outputRoot); packageRoot = resolve(packageRoot);
  for (const path of [root, outputRoot, packageRoot]) assert.equal(await realpath(path), path, 'Package capture roots cannot be symlinks');
  assert.equal(process.versions.node.split('.')[0], CAPTURE_POLICY.node_major, 'Capture requires the versioned Node toolchain');
  assert(!process.env.GALLERY_URL && !process.env.CHROMIUM_PATH, 'Package capture requires the isolated renderer and pinned browser, not external/custom runtime');
  const read = localReader(root), delivered = localReader(outputRoot);
  const manifest = JSON.parse(delivered('assets/manifest.json')), assets = selectPackageModels(manifest, modelIDs), shared = await packageCaptureInputs(root);
  const sourceHashes = new Map();
  for (const asset of assets) {
    assert.equal(hashBytes(read(asset.glb)), asset.sha256?.glb, `Package source GLB changed: ${asset.id}`);
    assert.equal(hashBytes(delivered(asset.glb)), asset.sha256.glb, `Package delivered GLB changed: ${asset.id}`);
    sourceHashes.set(asset.glb, asset.sha256.glb);
  }
  const rendererFiles = new Set(await posterRendererFiles(root)), base = CAPTURE_POLICY.site_base, prefix = `${base}__model_package_capture__/`;
  const html = `<!doctype html><link rel="icon" href="data:,"><body data-site-base="${base}"><div id="stage" style="width:512px;height:512px"></div><script type="importmap">${JSON.stringify({imports:{three:prefix+'node_modules/three/build/three.module.js','three/':prefix+'node_modules/three/','three/addons/':prefix+'node_modules/three/examples/jsm/'}})}</script><script type="module">import {PreviewRenderer} from '${prefix}site/gallery/renderer.js'; const models=await (await fetch('${prefix}manifest.json')).json(); window.__posterCapture={renderer:new PreviewRenderer(document.querySelector('#stage'),()=>{}),models};</script>`;
  const mime = {'.js':'text/javascript', '.mjs':'text/javascript', '.json':'application/json', '.glb':'model/gltf-binary'};
  let browser, server; const packages = [];
  try {
    server = createServer(async (request, response) => {
      try {
        const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
        assert(!pathname.includes('\\') && !pathname.includes('\0'));
        if (pathname === prefix) { response.writeHead(200, {'Content-Type':'text/html'}).end(html); return; }
        if (pathname === `${prefix}manifest.json`) { response.writeHead(200, {'Content-Type':'application/json'}).end(JSON.stringify(assets)); return; }
        let path, bytes;
        if (pathname.startsWith(prefix)) {
          path = pathname.slice(prefix.length);
          if (path.startsWith('node_modules/three/')) {
            assert(/^node_modules\/three\/[a-zA-Z0-9_./-]+\.js$/.test(path) && path.split('/').every(part => part && part !== '.' && part !== '..'));
            const parent = await realpath(resolve(root, 'node_modules/three')), full = resolve(parent, path.slice('node_modules/three/'.length));
            assert(full.startsWith(`${parent}${sep}`) && await realpath(full) === full); bytes = await readFile(full);
          } else { assert(rendererFiles.has(path), 'Unlisted renderer dependency'); bytes = read(path); }
        } else {
          assert(pathname.startsWith(base)); path = pathname.slice(base.length); assert(sourceHashes.has(path), 'Unselected model');
          bytes = delivered(path); assert.equal(hashBytes(bytes), sourceHashes.get(path), 'Delivered model changed during capture');
        }
        response.writeHead(200, {'Content-Type':mime[extname(path)] || 'application/octet-stream', 'Cache-Control':'no-store'}).end(bytes);
      } catch { response.writeHead(404).end(); }
    });
    await new Promise((ready, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', ready); });
    const url = `http://127.0.0.1:${server.address().port}${prefix}`;
    browser = await chromium.launch({headless: true, args: CAPTURE_POLICY.args});
    assert.equal(browser.version(), shared.browser, 'Package capture requires lockfile-pinned Chromium');
    const page = await browser.newPage({viewport: CAPTURE_POLICY.viewport, deviceScaleFactor: CAPTURE_POLICY.deviceScaleFactor, reducedMotion: CAPTURE_POLICY.reducedMotion, serviceWorkers: 'block'}), errors = [];
    await page.route('**/*', route => new URL(route.request().url()).origin === new URL(url).origin ? route.continue() : route.abort());
    page.on('response', response => { if (response.status() >= 400) errors.push(`Missing capture input: ${response.url()}`); });
    page.on('requestfailed', request => errors.push(`Blocked capture input: ${request.url()}`));
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error' && /THREE\.|WebGL|shader|GL_INVALID|CONTEXT_LOST/i.test(message.text())) errors.push(message.text()); });
    await page.goto(url, {waitUntil: 'networkidle', timeout: 120000});
    await page.waitForFunction(() => window.__posterCapture?.renderer && window.__posterCapture?.models?.length, null, {timeout: 120000});
    assert.deepEqual(await page.evaluate(() => window.__posterCapture.models.map(asset => asset.id)), assets.map(asset => asset.id), 'Renderer model scope differs');
    await page.evaluate(() => window.__posterCapture.renderer.stopHover());
    for (const asset of assets) {
      const capture = await page.evaluate(async id => {
        const {renderer, models} = window.__posterCapture, model = models.find(asset => asset.id === id), gl = renderer.renderer.getContext();
        if (gl.isContextLost()) throw Error('WebGL context lost before capture');
        const detail = await renderer.poster(model), wheel = await renderer.poster(model, {wheel: true});
        if (gl.isContextLost() || gl.getError() !== gl.NO_ERROR) throw Error('WebGL model capture failed');
        return {detail, wheel, wheelSpec: renderer.lastPosterSpec};
      }, asset.id);
      assert.equal(errors.length, 0, errors.join('; '));
      assert.equal((await packageCaptureInputs(root)).sha256, shared.sha256, 'Package capture recipe changed during render');
      packages.push({id: asset.id, ...storeCapturedModel({asset, shared, browserVersion: browser.version(), capture, read, packageRoot})});
    }
    return {kind: 'unverified-model-capture-packages', publication_authority: false, models: assets.map(asset => asset.id), packages};
  } finally {
    await browser?.close();
    if (server?.listening) await new Promise(done => server.close(done));
  }
}
export async function runModelCapturePackagesCLI(args = process.argv.slice(2)) {
  const report = await runModelCapturePackages(parseModelCaptureOptions(args));
  console.log(JSON.stringify(report, null, 2)); return report;
}
