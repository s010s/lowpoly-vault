import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm,readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {posterSharedInputs,posterInputKey,posterInputState} from './gallery-poster-inputs.mjs';
import {sha256} from './ci-provenance.mjs';
const root=await mkdtemp(join(tmpdir(),'poster-recipe-'));
try{
 await mkdir(join(root,'site/gallery'),{recursive:true});
 await mkdir(join(root,'node_modules/playwright-core'),{recursive:true});
 await writeFile(join(root,'node_modules/playwright-core/browsers.json'),JSON.stringify({browsers:[{name:'chromium',browserVersion:'pinned'}]}));
 const files={'site/gallery/renderer.js':'camera = 42; light = 1.1;','site/font.woff2':'font-v1','package.json':'{}','package-lock.json':'{}','vite.config.js':'build-v1'};
 for(const [path,value]of Object.entries(files))await writeFile(join(root,path),value);
 const asset={id:'one',glb:'assets/one.glb',sha256:{glb:'a'.repeat(64)}},manifest={assets:[asset]},shared=await posterSharedInputs(root),key=posterInputKey(asset,shared);
 const poster={detail:'gallery/posters/one.png',wheel:'gallery/posters/one-wheel.png',source_glb_sha256:asset.sha256.glb,input_sha256:key,browser_version:'pinned'};
 const resources={posters:{one:poster},files:[]};
 assert.deepEqual((await posterInputState(manifest,resources,{root})).valid,['one']);
 assert.equal(posterInputKey({...asset,downloads:{glb:'derived'},file_sizes:{glb:5},qa:'private'},shared),key);
 assert.deepEqual((await posterInputState(manifest,{posters:{one:{...poster,browser_version:'different'}},files:[]},{root})).stale,['one']);
 assert.notEqual(posterInputKey({...asset,sha256:{glb:'b'.repeat(64)}},shared),key);
 for(const path of Object.keys(files)){
  await writeFile(join(root,path),files[path]+' changed');
  assert.deepEqual((await posterInputState(manifest,resources,{root})).stale,['one'],path);
  await writeFile(join(root,path),files[path]);
 }
 const missing={posters:{one:{...poster,input_sha256:undefined}},files:[]};
 assert.deepEqual((await posterInputState(manifest,missing,{root})).stale,['one']);
 const legacy={...poster};delete legacy.input_sha256;delete legacy.browser_version;resources.posters.one=legacy;
 await writeFile(join(root,'site/gallery/approved-poster-inputs.json'),JSON.stringify({version:1,posters:{one:{input_sha256:key,poster_sha256:sha256(JSON.stringify({poster:legacy,seals:[]}))}}}));
 assert.deepEqual((await posterInputState(manifest,resources,{root})).valid,['one']);
 await writeFile(join(root,'site/gallery/renderer.js'),'changed camera');
 await assert.rejects(()=>posterInputState(manifest,resources,{root}),/Approved poster inputs changed/);
 console.log('Poster inputs: unchanged generation/baseline preserved; GLB, renderer/camera/light, config, lockfile and font changes invalidate; missing receipt regenerates; changed approved baseline blocks.');
}finally{await rm(root,{recursive:true,force:true});}
