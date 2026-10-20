/** Real CLI/server/storage integration with an explicitly simulated browser.
 * This does not establish pinned-runtime, WebGL, pixel quality or publication QA. */
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {hashBytes} from './model-registry.mjs';
import {parseModelCaptureOptions, selectPackageModels, packageCaptureInputs, runModelCapturePackages} from './model-capture-runner.mjs';
import {CAPTURE_POLICY} from './gallery-poster-inputs.mjs';

const source = dirname(fileURLToPath(import.meta.url));
function fixture() {
  const root = mkdtempSync(join(tmpdir(), 'package-runner-contract-'));
  const put = (path, value) => { mkdirSync(dirname(join(root, path)), {recursive: true}); writeFileSync(join(root, path), typeof value === 'object' && !Buffer.isBuffer(value) ? JSON.stringify(value) : value); };
  const assets = Array.from({length: 8}, (_, index) => {
    const id = `model-${index + 1}`, bytes = Buffer.from(`synthetic GLB ${id}`), asset = {id, glb: `assets/additions/${id}/model.glb`, blend: `assets/additions/${id}/model.blend`, preview: `assets/additions/${id}/preview.png`, sha256: {glb: hashBytes(bytes)}};
    put(asset.glb, bytes); put(`dist/${asset.glb}`, bytes); return asset;
  });
  put('dist/assets/manifest.json', {assets}); put('site/gallery/renderer.js', '// synthetic renderer dependency fixture\n');
  for (const name of ['capture-gallery-posters.mjs', 'gallery-poster-inputs.mjs', 'model-capture-runner.mjs', 'model-capture-package.mjs']) put(`site/${name}`, readFileSync(join(source, name)));
  for (const name of ['package.json', 'package-lock.json', 'vite.config.js']) put(name, '{}');
  put('node_modules/playwright-core/browsers.json', {browsers: [{name: 'chromium', browserVersion: '141.0.7390.37'}]});
  put('site/public/gallery/resources.json', 'unchanged source gallery'); put('dist/gallery/resources.json', 'unchanged output gallery'); put('packages/keep.txt', 'unrelated retained content');
  const originalInputs = pathToFileURL(join(source, 'gallery-poster-inputs.mjs')).href;
  put('inputs-proxy.mjs', `export * from ${JSON.stringify(originalInputs)}; import {CAPTURE_POLICY as original} from ${JSON.stringify(originalInputs)}; export const CAPTURE_POLICY={...original,node_major:process.versions.node.split('.')[0]};`);
  put('browser-fixture.mjs', `
    import assert from 'node:assert/strict';
    export const chromium={launch:async()=>({version:()=> '141.0.7390.37',close:async()=>{},newPage:async()=>{
      let state;
      return {route:async()=>{},on:()=>{},goto:async url=>{
        assert((await fetch(url)).ok); const models=await (await fetch(url+'manifest.json')).json();
        const origin=new URL(url).origin;
        state={models,renderer:{renderer:{getContext:()=>({isContextLost:()=>false,getError:()=>0,NO_ERROR:0})},stopHover:()=>{},poster:async(asset,options={})=>{
          assert((await fetch(origin+'/'+asset.glb)).ok);
          const bytes=Buffer.alloc(80);Buffer.from('89504e470d0a1a0a','hex').copy(bytes);bytes.writeUInt32BE(options.wheel?768:512,16);bytes.writeUInt32BE(options.wheel?432:512,20);bytes[25]=6;bytes.write(asset.id,26);
          state.renderer.lastPosterSpec={zoom:1,offset:[0,0]};return 'data:image/png;base64,'+bytes.toString('base64');
        }}};
      },waitForFunction:async()=>{},evaluate:async(fn,arg)=>{globalThis.window={__posterCapture:state};try{return await fn(arg);}finally{delete globalThis.window;}}};
    }})};
  `);
  put('loader.mjs', `
    import {pathToFileURL} from 'node:url';
    const dir=${JSON.stringify(root)};
    export async function resolve(specifier,context,next){
      if(specifier==='playwright')return {url:pathToFileURL(dir+'/browser-fixture.mjs').href,shortCircuit:true};
      if(specifier==='./gallery-poster-inputs.mjs'&&context.parentURL.endsWith('/model-capture-runner.mjs'))return {url:pathToFileURL(dir+'/inputs-proxy.mjs').href,shortCircuit:true};
      return next(specifier,context);
    }
  `);
  const run = args => spawnSync(process.execPath, ['--experimental-loader', join(root, 'loader.mjs'), join(source, 'capture-gallery-posters.mjs'), ...args], {cwd: root, encoding: 'utf8', timeout: 30000, env: {...process.env, GALLERY_OUTPUT_DIR: 'dist', GALLERY_URL: '', CHROMIUM_PATH: ''}});
  return {root, assets, run, put, close: () => rmSync(root, {recursive: true, force: true})};
}
await test('explicit package options reject ambiguous, empty, duplicate or mixed global modes', () => {
  assert.deepEqual(parseModelCaptureOptions(['--model-ids', 'model-b,model-a', '--package-output', '/tmp']), {packageRoot: '/tmp', modelIDs: ['model-a', 'model-b']});
  for (const args of [[], ['--package-output', '/tmp'], ['--model-ids', 'model-a'], ['--model-ids','model-a,model-a','--package-output','/tmp'], ['--model-ids','../other','--package-output','/tmp'], ['--model-ids','model-a','--package-output','/tmp','--source-output'], ['--model-ids','model-a','--package-output','/tmp','--verify-recipe']]) assert.throws(() => parseModelCaptureOptions(args));
});
await test('explicit model scope rejects missing and duplicate IDs before rendering', () => {
  const f = fixture(); try {
    assert.equal(selectPackageModels({assets: f.assets}, ['model-7']).length, 1);
    assert.throws(() => selectPackageModels({assets: f.assets}, ['missing']), /Unknown/);
    assert.throws(() => selectPackageModels({assets: [...f.assets, f.assets[0]]}, ['model-1']), /Duplicate/);
  } finally { f.close(); }
});
await test('package recipe binds the new runner and writer code, not only the legacy renderer', async () => {
  const f = fixture(); try {
    const before = await packageCaptureInputs(f.root);
    f.put('site/model-capture-package.mjs', 'changed package implementation');
    assert.notEqual((await packageCaptureInputs(f.root)).sha256, before.sha256);
  } finally { f.close(); }
});
await test('production entry refuses this machine runtime when it is not the pinned Node major', {skip: process.versions.node.split('.')[0] === CAPTURE_POLICY.node_major}, async () => {
  const f = fixture(); try {
    await assert.rejects(() => runModelCapturePackages({root: f.root, packageRoot: join(f.root, 'packages'), modelIDs: ['model-1']}), /versioned Node toolchain/);
    assert.deepEqual(readdirSync(join(f.root, 'packages')), ['keep.txt']);
  } finally { f.close(); }
});
await test('actual opt-in CLI dispatch writes seven independent packages and no shared gallery snapshot', () => {
  const f = fixture(); try {
    const args = ['--package-output', join(f.root, 'packages'), '--model-ids', f.assets.slice(0, 7).map(asset => asset.id).join(',')], first = f.run(args);
    assert.equal(first.status, 0, first.stderr); const report = JSON.parse(first.stdout);
    assert.equal(report.publication_authority, false); assert.equal(report.packages.length, 7);
    assert.deepEqual(readdirSync(join(f.root, 'packages/registry/captures')).sort(), f.assets.slice(0, 7).map(asset => asset.id));
    for (const row of report.packages) {
      assert.deepEqual(readdirSync(join(f.root, 'packages', row.path)).sort(), ['capture.json', 'detail.png', 'wheel.png']);
      assert.equal(JSON.parse(readFileSync(join(f.root, 'packages', row.path, 'capture.json'))).publication_authority, false);
    }
    for (const [path, expected] of [['site/public/gallery/resources.json','unchanged source gallery'], ['dist/gallery/resources.json','unchanged output gallery'], ['packages/keep.txt','unrelated retained content']]) assert.equal(readFileSync(join(f.root, path), 'utf8'), expected);
    assert.deepEqual(readdirSync(join(f.root, 'dist')).sort(), ['assets', 'gallery']);
    const second = f.run(args); assert.equal(second.status, 0, second.stderr); assert(JSON.parse(second.stdout).packages.every(row => !row.created));
  } finally { f.close(); }
});
await test('CLI package path rejects changed delivered GLB and never falls back to whole-gallery mode', () => {
  const f = fixture(); try {
    f.put(`dist/${f.assets[0].glb}`, 'changed');
    const result = f.run(['--package-output', join(f.root, 'packages'), '--model-ids', 'model-1']);
    assert.notEqual(result.status, 0); assert.match(result.stderr, /delivered GLB changed/);
    assert.deepEqual(readdirSync(join(f.root, 'packages')), ['keep.txt']);
    assert.equal(readFileSync(join(f.root, 'dist/gallery/resources.json'), 'utf8'), 'unchanged output gallery');
  } finally { f.close(); }
});
