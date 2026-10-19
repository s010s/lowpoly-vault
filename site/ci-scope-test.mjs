import assert from 'node:assert/strict';
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
