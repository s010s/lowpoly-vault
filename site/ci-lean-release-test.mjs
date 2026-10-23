/** Small executable orchestration/selection fixtures, never model acceptance evidence. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,copyFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {checkProductionGlbs} from './ci-production-release-check.mjs';
import {classifyTests,needsGeometryRegression} from './ci-lean-scope.mjs';
assert.deepEqual(classifyTests(['assets/additions/new/model.glb','site/public/gallery/posters/new.png'],{appendOnly:true}).mode,'models');
for(const path of ['site/main.js','site/style.css','site/ci-build-release.mjs','scripts/qa_glb.py','.github/workflows/pages.yml','package.json'])assert.notEqual(classifyTests(['assets/additions/new/model.glb',path],{appendOnly:true}).mode,'models',path);
assert.equal(classifyTests(['site/main.js']).website,true);
assert.equal(classifyTests(['site/style.css']).publication,false);
assert.equal(classifyTests(['site/production-release.mjs']).publication,true);
assert.equal(classifyTests([], {known:false}).framework,true);
assert.equal(needsGeometryRegression(['site/ci-build-release.mjs','site/gallery-assets.mjs']),false);assert.equal(needsGeometryRegression(['site/gallery/renderer.js']),true);assert.equal(needsGeometryRegression(['package-lock.json']),true);assert.equal(needsGeometryRegression(undefined),true);
// Every actual relative renderer dependency must select geometry regressions,
// including viewer.js -> render-preset.js outside the gallery directory.
const rendererDependencies=new Set();
async function checkRendererDependencies(path){
 if(rendererDependencies.has(path))return;
 rendererDependencies.add(path);
 assert.equal(needsGeometryRegression([path]),true,`geometry regression missing for ${path}`);
 const source=await readFile(path,'utf8');
 for(const match of source.matchAll(/(?:import|export)\s[^;]*?from\s*['"](\.[^'"]+)['"]/g)){
  if(/\.m?js$/.test(match[1]))await checkRendererDependencies(join(dirname(path),match[1]));
 }
}
for(const name of ['reset-transition','single-framing','poster-projection','selection-orbit-controls','compare-ground-regression','model-support'])await checkRendererDependencies(`site/gallery/tests/${name}-test.mjs`);
assert(rendererDependencies.has('site/viewer.js'));
assert(rendererDependencies.has('site/render-preset.js'));
assert(rendererDependencies.has('site/curation.js'));
assert(rendererDependencies.has('site/routes.js'));
for(const path of ['site/ci-build-release.mjs','site/gallery-assets.mjs','site/style.css','site/catalog-data.json','site/gallery/wheel-framing.json','site/gallery/approved-poster-inputs.json'])assert.equal(needsGeometryRegression([path]),false,path);
const root=await mkdtemp(join(tmpdir(),'lean-build-'));
const put=async(p,s)=>{await mkdir(dirname(join(root,p)),{recursive:true});await writeFile(join(root,p),s);};
const fixture=`import {appendFileSync} from 'node:fs';export function event(n){appendFileSync('events',n+'\\n');if(process.env.FAIL_PHASE===n)throw Error('expected failure '+n);}`;
try{
 await put('package.json','{"type":"module"}');await put('site/fixture.mjs',fixture);await mkdir(join(root,'assets'));
 await put('assets/manifest.json','{"assets":[]}');
 const broken=Buffer.from('not a valid GLB');await put('assets/broken.glb',broken);await assert.rejects(checkProductionGlbs(root,[{id:'broken',glb:'assets/broken.glb',sha256:{glb:createHash('sha256').update(broken).digest('hex')}}]),/standard GLB validator errors|could not detect glTF format/);
 await copyFile(resolve('site/ci-build-release.mjs'),join(root,'site/ci-build-release.mjs'));
 await put('site/initial-release.mjs',`import {event} from './fixture.mjs';export async function checkPublishedManifest(root,{productionResults}){event('source');productionResults.set('checked',{assets:[]});return {assets:[]};}`);
 await put('site/ci-production-release-check.mjs',`import {event} from './fixture.mjs';export async function checkProductionGlbs(){event('glb');return {status:'PASS'};}`);
 await put('site/model-registry-cli.mjs','export function readRegistry(){return {};}');
 await put('site/model-registry-sync.mjs',`import {event} from './fixture.mjs';export function syncRegistry(){event('registry');}`);
 await put('node_modules/vite/package.json','{"type":"module"}');
 await put('node_modules/vite/bin/vite.js',`import {event} from '../../../site/fixture.mjs';event('vite');`);
 await put('site/ci-render-template.mjs',`import {event} from './fixture.mjs';event('template');`);
 for(const [file,fn,label]of [['copy-assets','copyRelease','copy'],['audit-release','auditRelease','audit']])await put(`site/${file}.mjs`,`import assert from 'node:assert/strict';import {event} from './fixture.mjs';export async function ${fn}({source,productionResults}){assert.deepEqual(source,{assets:[]});assert(productionResults.has('checked'));event('${label}');}`);
 const order=['source','glb','registry','vite','template','copy','audit'];
 const run=fail=>spawnSync(process.execPath,['site/ci-build-release.mjs'],{cwd:root,env:{...process.env,FAIL_PHASE:fail||''},encoding:'utf8'});
 await put('events','');let result=run();assert.equal(result.status,0,result.stderr);assert.deepEqual((await readFile(join(root,'events'),'utf8')).trim().split('\n'),order);
 let report=JSON.parse(await readFile(join(root,'qa/ci-timings/build.json')));assert.equal(report.status,'pass');assert.equal(report.phases.length,6);
 for(const name of order){await put('events','');result=run(name);assert.notEqual(result.status,0,name);assert.deepEqual((await readFile(join(root,'events'),'utf8')).trim().split('\n'),order.slice(0,order.indexOf(name)+1));report=JSON.parse(await readFile(join(root,'qa/ci-timings/build.json')));assert.equal(report.status,'fail');assert.equal(report.phases.at(-1).exit_code,1);}
 for(const file of ['turntable-delivery.mjs','image-scrub.js','render-preset.js','refinable-asset-ids.mjs'])await copyFile(resolve('site',file),join(root,'site',file));
 await put('site/production-release.mjs',`import assert from 'node:assert/strict';export let calls=0;export async function collectProductionRelease(){calls++;return [{id:'one',production_release:'batch'},{id:'two',production_release:'batch'}];}export function assertProductionMetadata(a,b){assert.deepEqual(a,b);}`);
 const module=await import('file://'+join(root,'site/turntable-delivery.mjs')),production=await import('file://'+join(root,'site/production-release.mjs'));
 const manifest={assets:[{id:'one',production_release:'batch'},{id:'two',production_release:'batch'}]};
 await module.collectTurntables(manifest,root);assert.equal(production.calls,1,'One collection per descriptor, not per model');
 const wrong=structuredClone(manifest);wrong.assets[1].unbound=true;await assert.rejects(module.collectTurntables(wrong,root));
 const pages=await readFile('.github/workflows/pages.yml','utf8'),pub=await readFile('.github/workflows/publication-regressions.yml','utf8');
 assert.equal((pages.match(/run: node site\/ci-build-release.mjs/g)||[]).length,1);assert(!/ci-production-release-check.mjs|ci-release-fast-path.mjs|CI_PUBLICATION_RECEIPT/.test(pages));
 assert.match(pages,/needs: \[build, publication\]/);assert.match(pub,/name: Require every publication suite/);assert(!/matrix:|shard: \[/.test(pub));
 console.log('PASS lean release: scope selection, exactly-once ordered build, all seven failure stops, same in-memory checked results, no four empty shard jobs.');
}finally{await rm(root,{recursive:true,force:true});}
