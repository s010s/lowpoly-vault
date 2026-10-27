/** Small executable orchestration/selection fixtures, never model acceptance evidence. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,copyFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname,resolve} from 'node:path';
import {spawnSync,execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {checkProductionGlbs} from './ci-production-release-check.mjs';
import {classifyTests,needsGeometryRegression,leanScope} from './ci-lean-scope.mjs';
assert.deepEqual(classifyTests(['assets/additions/new/model.glb','site/public/gallery/posters/new.png'],{appendOnly:true}).mode,'models');
for(const path of ['site/main.js','site/style.css','site/ci-build-release.mjs','scripts/qa_glb.py','.github/workflows/pages.yml','package.json'])assert.notEqual(classifyTests(['assets/additions/new/model.glb',path],{appendOnly:true}).mode,'models',path);
assert.equal(classifyTests(['site/main.js']).website,true);
assert.equal(classifyTests(['site/style.css']).publication,false);
assert.equal(classifyTests(['site/production-release.mjs']).publication,true);
assert.equal(classifyTests([], {known:false}).framework,true);
// The exception is exactly these two files, never a self-declared mode or CI edit.
const contentFiles=['site/content-production-acceptance.mjs','site/content-production-acceptance-test.mjs'];
for(const paths of [[contentFiles[0]],[contentFiles[1]],contentFiles]){
 const scope=classifyTests(paths);assert.equal(scope.mode,'content');
 for(const key of ['framework','publication','website'])assert.equal(scope[key],false);
 assert.equal(classifyTests(paths,{known:false}).mode,'full');
}
for(const path of ['site/typed-production-release.mjs','site/inventory-type-acceptance.mjs','site/production-release.mjs','site/ci-lean-scope.mjs','site/ci-lean-regressions.mjs','site/ci-lean-release-test.mjs','.github/workflows/pages.yml','assets/additions/new/model.glb','site/main.js','unknown.txt']){
 assert.equal(classifyTests([...contentFiles,path],{appendOnly:true}).mode,'full',path);
 assert.equal(classifyTests([path]).mode,'full',path);
}
assert.equal(classifyTests([]).mode,'full');
// Exercise the real event/SHA/clean-checkout boundary with small Git objects.
const scopeRoot=await mkdtemp(join(tmpdir(),'content-scope-'));
try{
 const git=(...args)=>execFileSync('git',args,{cwd:scopeRoot,encoding:'utf8'}).trim();
 await mkdir(join(scopeRoot,'site'));await writeFile(join(scopeRoot,contentFiles[0]),'before');
 git('init','-q');git('add','.');git('-c','user.name=Scope Test','-c','user.email=scope@example.invalid','commit','-qm','before');const base=git('rev-parse','HEAD');
 await writeFile(join(scopeRoot,contentFiles[0]),'after');git('add','.');git('-c','user.name=Scope Test','-c','user.email=scope@example.invalid','commit','-qm','after');const head=git('rev-parse','HEAD');
 const eventPath=join(scopeRoot,'event.json'),repo='owner/repository';
 const event={ref:'refs/heads/main',before:base,after:head,repository:{full_name:repo}};
 await writeFile(eventPath,JSON.stringify(event));
 const env={GITHUB_EVENT_PATH:eventPath,GITHUB_EVENT_NAME:'push',GITHUB_REF:event.ref,GITHUB_REPOSITORY:repo,GITHUB_SHA:head};
 assert.equal(leanScope({root:scopeRoot,env}).mode,'content');
 for(const changes of [{GITHUB_SHA:base},{GITHUB_REPOSITORY:'wrong/repository'},{GITHUB_EVENT_NAME:'workflow_dispatch'},{GITHUB_EVENT_PATH:''}])assert.equal(leanScope({root:scopeRoot,env:{...env,...changes}}).mode,'full');
 await writeFile(join(scopeRoot,contentFiles[0]),'dirty');assert.equal(leanScope({root:scopeRoot,env}).mode,'full');git('restore',contentFiles[0]);
 git('update-index','--assume-unchanged',contentFiles[0]);assert.equal(leanScope({root:scopeRoot,env}).mode,'full');git('update-index','--no-assume-unchanged',contentFiles[0]);
 const pr={pull_request:{base:{ref:'main',sha:base,repo:{full_name:repo}},head:{sha:head,repo:{full_name:repo}}}};
 await writeFile(eventPath,JSON.stringify(pr));const prEnv={...env,GITHUB_EVENT_NAME:'pull_request'};
 assert.equal(leanScope({root:scopeRoot,env:prEnv}).mode,'content');
 pr.pull_request.head.repo.full_name='fork/repository';await writeFile(eventPath,JSON.stringify(pr));assert.equal(leanScope({root:scopeRoot,env:prEnv}).mode,'full');
 // Selection must actually run the focused suite, propagate failure, and claim no historical PASS.
 await copyFile(resolve('site/ci-lean-regressions.mjs'),join(scopeRoot,'site/ci-lean-regressions.mjs'));
 await writeFile(join(scopeRoot,'site/ci-lean-scope.mjs'),`export const leanScope=()=>({mode:'content',framework:false,publication:false,website:false});export const needsGeometryRegression=()=>false;`);
 await writeFile(join(scopeRoot,contentFiles[1]),`import {appendFileSync} from 'node:fs';appendFileSync('events','content\\n');process.exitCode=Number(process.env.FOCUS_FAIL||0);`);
 const runFocused=(mode,fail='0')=>spawnSync(process.execPath,['site/ci-lean-regressions.mjs',mode],{cwd:scopeRoot,env:{...process.env,FOCUS_FAIL:fail},encoding:'utf8'});
 assert.equal(runFocused('contracts').status,0);assert.equal(await readFile(join(scopeRoot,'events'),'utf8'),'content\n');
 assert.notEqual(runFocused('contracts','1').status,0);
 for(const mode of ['publication','pipeline']){const result=runFocused(mode);assert.equal(result.status,0);assert.match(result.stdout,/NOT_APPLICABLE/);}
 assert.equal(await readFile(join(scopeRoot,'events'),'utf8'),'content\ncontent\n');
 // Untrusted caller hints cannot replace an authenticated Git diff.
 assert.equal(leanScope({root:scopeRoot,env:{CONTENT_ONLY:'1'}}).mode,'full');
}finally{await rm(scopeRoot,{recursive:true,force:true});}
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
 for(const file of ['turntable-delivery.mjs','image-scrub.js','render-preset.js','refinable-asset-ids.mjs','same-id-successors.mjs','same-id-append-continuation.mjs','model-registry.mjs','curation.js','catalog-data.json','final-delivery.mjs'])await copyFile(resolve('site',file),join(root,'site',file));
 await put('site/production-release.mjs',`import assert from 'node:assert/strict';export let calls=0;export async function collectProductionRelease(){calls++;return [{id:'one',production_release:'batch'},{id:'two',production_release:'batch'}];}export function assertProductionMetadata(a,b){assert.deepEqual(a,b);}`);
 const module=await import('file://'+join(root,'site/turntable-delivery.mjs')),production=await import('file://'+join(root,'site/production-release.mjs'));
 const manifest={assets:[{id:'one',production_release:'batch'},{id:'two',production_release:'batch'}]};
 await module.collectTurntables(manifest,root);assert.equal(production.calls,1,'One collection per descriptor, not per model');
 const wrong=structuredClone(manifest);wrong.assets[1].unbound=true;await assert.rejects(module.collectTurntables(wrong,root));
 const pages=await readFile('.github/workflows/pages.yml','utf8'),pub=await readFile('.github/workflows/publication-regressions.yml','utf8');
 // Parse the bounded, literal build step rather than assuming a one-line YAML run.
 // Fail closed on shell wrappers, conditionals, ignored failures or extra commands.
 const buildCommands=[
  'node site/detail-capture-provenance-test.mjs','node site/detail-presentations-test.mjs',
  'node site/detail-presentations-audit-test.mjs','node site/detail-pixels-test.mjs',
  'node site/detail-capture-delta-test.mjs','node site/detail-capture-authority-test.mjs',
  'node site/detail-presentation-contract.mjs','node site/ci-build-release.mjs',
 ];
 function assertMandatoryBuild(workflow){
  const steps=workflow.split(/(?=^      - )/m);
  const matches=steps.filter(step=>/^        id: build$/m.test(step));
  assert.equal(matches.length,1,'Exactly one build step');
  const step=matches[0];
  assert(!/^        (?:if|continue-on-error|shell):/m.test(step),'No build bypass or custom shell');
  const run=step.match(/^        run: \|\n((?:          [^\n]*\n)+)/m);
  assert(run,'Build must use a literal ordered command block');
  assert.deepEqual(run[1].trimEnd().split('\n').map(line=>line.slice(10)),buildCommands,
   'Mandatory detail checks must succeed before the exactly-once build');
  for(const command of [buildCommands.at(-2),buildCommands.at(-1)])
   assert.equal(workflow.split(command).length-1,1,`${command} occurs exactly once`);
 }
 assertMandatoryBuild(pages);
 const contract='          node site/detail-presentation-contract.mjs\n';
 const build='          node site/ci-build-release.mjs\n';
 for(const [name,mutated] of [
  ['missing contract',pages.replace(contract,'')],
  ['contract after build',pages.replace(contract+build,build+contract)],
  ['duplicate build',pages.replace(build,build+build)],
  ['ignored contract failure',pages.replace(contract,contract.trimEnd()+' || true\n')],
  ['conditional contract',pages.replace(contract,'          if false; then node site/detail-presentation-contract.mjs; fi\n')],
  ['conditional step',pages.replace('        id: build\n','        id: build\n        if: false\n')],
  ['ignored step failure',pages.replace('        id: build\n','        id: build\n        continue-on-error: true\n')],
  ['custom non-failing shell',pages.replace('        id: build\n','        id: build\n        shell: bash {0}\n')],
  ['duplicate build step',pages.replace('        id: contracts\n','        id: build\n')],
 ])assert.throws(()=>assertMandatoryBuild(mutated),undefined,name);
 assert(!/ci-production-release-check.mjs|ci-release-fast-path.mjs|CI_PUBLICATION_RECEIPT/.test(pages));
 assert.match(pages,/needs: \[build, publication\]/);assert.match(pub,/name: Require every publication suite/);assert(!/matrix:|shard: \[/.test(pub));
 console.log('PASS lean release: scope selection, exactly-once ordered build, all seven failure stops, same in-memory checked results, no four empty shard jobs.');
}finally{await rm(root,{recursive:true,force:true});}
