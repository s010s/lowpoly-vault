import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm,readFile,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {posterSharedInputs,posterInputKey,posterInputState,posterRendererFiles} from './gallery-poster-inputs.mjs';
import {sha256} from './ci-provenance.mjs';
const root=await mkdtemp(join(tmpdir(),'poster-recipe-'));
try{
 await mkdir(join(root,'site/gallery'),{recursive:true});
 await mkdir(join(root,'node_modules/playwright-core'),{recursive:true});
 await writeFile(join(root,'node_modules/playwright-core/browsers.json'),JSON.stringify({browsers:[{name:'chromium',browserVersion:'pinned'}]}));
 const files={'site/gallery/renderer.js':"import './lighting.json'; import './helper.js'; const camera = 42, light = 1.1;",'site/gallery/helper.js':"export const font = new URL('./font.woff2',import.meta.url);",'site/gallery/font.woff2':'rendered-font','site/capture-gallery-posters.mjs':'// fixed harness','site/gallery-poster-inputs.mjs':'// versioned recipe','site/gallery/lighting.json':'{"key":1}','package.json':'{}','package-lock.json':'{}','vite.config.js':'build-v1'};
 for(const [path,value]of Object.entries(files))await writeFile(join(root,path),value);
 const asset={id:'one',glb:'assets/one.glb',sha256:{glb:'a'.repeat(64)}},manifest={assets:[asset]},shared=await posterSharedInputs(root),key=posterInputKey(asset,shared);
 const poster={detail:'gallery/posters/one.png',wheel:'gallery/posters/one-wheel.png',source_glb_sha256:asset.sha256.glb,input_sha256:key,browser_version:'pinned'};
 const resources={posters:{one:poster},files:[]};
 assert.deepEqual((await posterInputState(manifest,resources,{root})).valid,['one']);
 assert.deepEqual((await posterInputState(manifest,resources,{root})).capture,['one'],'A source-authored matching key is not proof: non-golden pixels must be regenerated');
 assert.equal(posterInputKey({...asset,downloads:{glb:'derived'},file_sizes:{glb:5},qa:'private'},shared),key);
 assert.deepEqual((await posterInputState(manifest,{posters:{one:{...poster,browser_version:'different'}},files:[]},{root})).stale,['one']);
 assert.notEqual(posterInputKey({...asset,sha256:{glb:'b'.repeat(64)}},shared),key);
 for(const path of Object.keys(files)){
  await writeFile(join(root,path),files[path]+'\n// changed');
  assert.deepEqual((await posterInputState(manifest,resources,{root})).stale,['one'],path);
  await writeFile(join(root,path),files[path]);
 }
 await writeFile(join(root,'site/gallery/bootstrap.js'),'// UI startup only');
 await writeFile(join(root,'site/brand.css'),'body{font-family:Brand}');await writeFile(join(root,'site/font.woff2'),'brand-font');
 assert.equal((await posterSharedInputs(root)).sha256,shared.sha256,'UI fonts/styles are not drawn into WebGL poster pixels; UI changes still receive full routing coverage');
 const missing={posters:{one:{...poster,input_sha256:undefined}},files:[]};
 assert.deepEqual((await posterInputState(manifest,missing,{root})).stale,['one']);
 const legacy={...poster};delete legacy.input_sha256;delete legacy.browser_version;resources.posters.one=legacy;
 await writeFile(join(root,'site/gallery/approved-poster-inputs.json'),JSON.stringify({version:1,posters:{one:{input_sha256:key,poster_sha256:sha256(JSON.stringify({poster:legacy,seals:[]}))}}}));
 assert.deepEqual((await posterInputState(manifest,resources,{root})).valid,['one']);
 assert.deepEqual((await posterInputState(manifest,resources,{root})).capture,[],'Verified golden pairs are preserved');
 await writeFile(join(root,'site/gallery/renderer.js'),'const camera = 43');
 await assert.rejects(()=>posterInputState(manifest,resources,{root}),/Approved poster inputs changed/);
 const changedShared=await posterSharedInputs(root);
 resources.posters.one={...legacy,input_sha256:posterInputKey(asset,changedShared),browser_version:changedShared.browser};
 await assert.rejects(()=>posterInputState(manifest,resources,{root}),/Approved poster pixels or metadata changed/);
 await writeFile(join(root,'site/gallery/renderer.js'),"import(dynamicName)");
 await assert.rejects(()=>posterRendererFiles(root),/Computed poster dependencies/);
 await symlink('helper.js',join(root,'site/gallery/linked.js'));
 await writeFile(join(root,'site/gallery/renderer.js'),"import './linked.js'");
 await assert.rejects(()=>posterRendererFiles(root),/symlink rejected/);
 await writeFile(join(root,'site/gallery/renderer.js'),"import 'unversioned-library'");
 await assert.rejects(()=>posterRendererFiles(root),/lockfile-pinned Three/);
 console.log('Poster inputs: unchanged generation/baseline preserved; GLB, renderer/camera/light, config, lockfile and lighting-config changes invalidate (imported renderer fonts are bound; UI bootstrap/styles/fonts remain outside isolated WebGL pixels); missing receipt regenerates; changed approved baseline blocks.');
}finally{await rm(root,{recursive:true,force:true});}
