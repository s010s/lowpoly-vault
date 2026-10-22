import assert from 'node:assert/strict';
import {execFileSync,spawnSync} from 'node:child_process';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {classify} from './ci-scope.mjs';
const manifest={assets:[{id:'arch',glb:'assets/revisions/arch/r2/arch.glb',blend:'assets/revisions/arch/r2/arch.blend',preview:'assets/revisions/arch/r2/preview.webp'}]};
assert.deepEqual(classify(['docs/note.md'],manifest).tasks,['none']);
assert.equal(classify(['production/new/review.json'],manifest).runtime,true);
const asset=classify([manifest.assets[0].glb],manifest);
assert.equal(asset.ids,'arch');assert.deepEqual(asset.tasks,['models','previews']);
for(const path of ['site/style.css','site/main.js','site/viewer.js','site/routes.js','package-lock.json'])assert(classify([path],manifest).runtime,path);
assert.equal(classify(['site/ci-scope.mjs'],manifest).runtime,true);
assert(classify([],manifest,true).tasks.includes('shared'));
assert.equal(classify(['assets/manifest.json'],manifest).ids,'');
assert(classify(['site/render-preset.js'],manifest).previews);
console.log('CI routing: docs, unpublished candidates, model payload, runtime, manifest and full fallback passed.');

const appended={assets:[...manifest.assets,{id:'new',glb:'assets/new.glb'}]};
assert.equal(classify(['assets/manifest.json'],appended,false,{previousManifest:manifest}).ids,'new');
assert.equal(classify(['package.json'],manifest,false,{previousPackage:{scripts:{test:'a'}},currentPackage:{scripts:{test:'b'}}}).runtime,true);
for(const path of ['unknown.md','docs/run.js','.github/workflows/pages.yml','assets/unknown/new.glb','site/shared-model-browser-test.mjs'])assert(classify([path],manifest).runtime,path);
assert.deepEqual(classify(['docs/ci-validation.md'],manifest).tasks,['none']);
assert.equal(classify(['docs/runtime.js'],manifest).category,'unknown');
assert.equal(classify(['README.md','site/gallery/renderer.js'],manifest).runtime,true);
assert.equal(classify(['assets/manifest.json'],manifest,false,{previousManifest:appended}).runtime,true);
const round02={assets:appended.assets,publication:{round02_descriptor:{},approved_round02_ids:['new']}};
const scoped=classify(['assets/manifest.json'],round02,false,{previousManifest:{...round02,assets:manifest.assets}});
assert.equal(scoped.runtime,false);assert.equal(scoped.ids,'new');assert.deepEqual(scoped.tasks,['models','round02','previews']);
assert(classify(['site/hover-reveal-browser-test.mjs'],manifest).runtime);
assert(classify([],manifest,true).tasks.includes('hover'));
const round03={assets:appended.assets,publication:{round03_descriptor:{},approved_round03_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round03,false,{previousManifest:{...round03,assets:manifest.assets}}).tasks,['models','round03','previews']);

const round04={assets:appended.assets,publication:{round04_descriptor:{},approved_round04_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round04,false,{previousManifest:{...round04,assets:manifest.assets}}).tasks,['models','round04','previews']);

const round05={assets:appended.assets,publication:{round05_descriptor:{},approved_round05_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round05,false,{previousManifest:{...round05,assets:manifest.assets}}).tasks,['models','round05','previews']);

const round06={assets:appended.assets,publication:{round06_descriptor:{},approved_round06_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round06,false,{previousManifest:{...round06,assets:manifest.assets}}).tasks,['models','round06','previews']);
const round07={assets:appended.assets,publication:{round07_descriptor:{},approved_round07_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round07,false,{previousManifest:{...round07,assets:manifest.assets}}).tasks,['models','round07','previews']);
const round08={assets:appended.assets,publication:{round08_descriptor:{},approved_round08_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round08,false,{previousManifest:{...round08,assets:manifest.assets}}).tasks,['models','round08','previews']);
const round09={assets:appended.assets,publication:{round09_descriptor:{},approved_round09_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round09,false,{previousManifest:{...round09,assets:manifest.assets}}).tasks,['models','round09','previews']);
const round10={assets:appended.assets,publication:{round10_descriptor:{},approved_round10_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round10,false,{previousManifest:{...round10,assets:manifest.assets}}).tasks,['models','round10','previews']);
const round11={assets:appended.assets,publication:{round11_descriptor:{},approved_round11_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round11,false,{previousManifest:{...round11,assets:manifest.assets}}).tasks,['models','round11','previews']);

assert(classify(['assets/manifest.json'],{...appended,license:'changed'},false,{previousManifest:manifest}).runtime,'Asset addition cannot hide shared metadata changes');

const registryPath=`registry/models/new/revisions/${'a'.repeat(64)}/record.json`;
const registryScope=classify([registryPath,'registry/batches/independent-new.json'],appended,false,{previousManifest:manifest});
assert.equal(registryScope.runtime,false);assert.equal(registryScope.ids,'new');assert.deepEqual(registryScope.tasks,['models','previews']);
for(const path of ['registry/baseline.json','registry/models/not-published/revisions/'+ 'a'.repeat(64)+'/record.json','registry/models/new/run.js','registry/unclassified.json'])assert(classify([path],appended,false,{previousManifest:manifest}).runtime,path);
assert(classify(['registry/batches/independent-new.json'],manifest,false,{previousManifest:manifest}).runtime,'A batch without published additions is not narrowly classified');
console.log('Registry scope: exact known per-ID record paths and new batch data select only new model work; unknown/baseline paths remain full.');

// Exercise the real CLI, not only classify(): a 217-model predecessor exceeds
// Node's default Git stdout buffer, but adding one owned record stays scoped.
const root=mkdtempSync(join(tmpdir(),'registry-scope-large-'));
try{
 const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
 git('init','-q');git('config','user.name','Scope fixture');git('config','user.email','scope@example.invalid');
 const put=(path,value)=>{const parts=path.split('/');parts.pop();if(parts.length)mkdirSync(join(root,...parts),{recursive:true});writeFileSync(join(root,path),typeof value==='string'?value:JSON.stringify(value));};
 const large={assets:Array.from({length:217},(_,index)=>({id:`historical-${index}`,description:'x'.repeat(6000)}))};
 assert(Buffer.byteLength(JSON.stringify(large))>1024*1024);
 put('assets/manifest.json',large);put('site/curation.js','export {};\n');put('package.json',{});
 git('add','.');git('commit','-qm','217-model predecessor');const base=git('rev-parse','HEAD');
 put('assets/manifest.json',{assets:[...large.assets,{id:'scope-new'}]});
 put(`registry/models/scope-new/revisions/${'b'.repeat(64)}/record.json`,{id:'scope-new'});
 put('registry/batches/scope-new.json',{id:'scope-new'});
 git('add','.');git('commit','-qm','Independent record addition');
 const run=base=>spawnSync(process.execPath,[fileURLToPath(new URL('./ci-scope.mjs',import.meta.url))],{cwd:root,encoding:'utf8',env:{...process.env,BASE_SHA:base,FULL_REVIEW:'false',GITHUB_OUTPUT:''},maxBuffer:16*1024*1024});
 const result=run(base);assert.equal(result.status,0,result.stderr);
 const scope=JSON.parse(result.stdout);
 assert.equal(scope.runtime,false);assert.equal(scope.ids,'scope-new');assert.deepEqual(scope.tasks,['models-1-of-1','previews']);
 assert(!result.stderr.includes('Diff provenance unavailable'));
 const failed=run('0'.repeat(40));assert.equal(failed.status,0,failed.stderr);
 assert.equal(JSON.parse(failed.stdout).runtime,true,'Missing provenance still requires full review');
 put('assets/manifest.json',{...large,note:'x'.repeat(16*1024*1024)});
 git('add','.');git('commit','-qm','Oversized predecessor');
 const oversized=run(git('rev-parse','HEAD'));assert.equal(oversized.status,0,oversized.stderr);
 assert.equal(JSON.parse(oversized.stdout).runtime,true,'Provenance exceeding the finite buffer still requires full review');
 assert(oversized.stderr.includes('Diff provenance unavailable'));
 console.log('Real scope CLI: 217-model >1 MiB predecessor plus one record stays model-scoped; invalid or >16 MiB provenance stays full.');
}finally{rmSync(root,{recursive:true,force:true});}

const separated=classify(['site/main.js','assets/manifest.json'],appended,false,{previousManifest:manifest});assert.equal(separated.runtime,true);assert.equal(separated.ids,'');assert.deepEqual(separated.captureIds,['new'],'Broad shared-code tests must not silently select all models for capture');
