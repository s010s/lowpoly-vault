import assert from 'node:assert/strict';
import {classify} from './ci-scope.mjs';
const manifest={assets:[{id:'arch',glb:'assets/revisions/arch/r2/arch.glb',blend:'assets/revisions/arch/r2/arch.blend',preview:'assets/revisions/arch/r2/preview.webp'}]};
assert.deepEqual(classify(['docs/note.md'],manifest).tasks,['none']);
assert.deepEqual(classify(['production/new/review.json'],manifest).tasks,['none']);
const asset=classify([manifest.assets[0].glb],manifest);
assert.equal(asset.ids,'arch');assert.deepEqual(asset.tasks,['models','previews']);
for(const path of ['site/style.css','site/main.js','site/viewer.js','site/routes.js','package-lock.json'])assert(classify([path],manifest).runtime,path);
assert.equal(classify(['site/ci-scope.mjs'],manifest).runtime,false);
assert(classify([],manifest,true).tasks.includes('shared'));
assert.equal(classify(['assets/manifest.json'],manifest).ids,'');
assert(classify(['site/render-preset.js'],manifest).previews);
console.log('CI routing: docs, unpublished candidates, model payload, runtime, manifest and full fallback passed.');

const appended={assets:[...manifest.assets,{id:'new',glb:'assets/new.glb'}]};
assert.equal(classify(['assets/manifest.json'],appended,false,{previousManifest:manifest}).ids,'new');
assert.equal(classify(['package.json'],manifest,false,{previousPackage:{scripts:{test:'a'},dependencies:{a:'1'}},currentPackage:{scripts:{test:'b'},dependencies:{a:'1'}}}).runtime,false);
const {editorialDataOnly}=await import('./ci-scope.mjs');
assert(editorialDataOnly("export const PACK_LABELS = {'a':{en:'A'}};\nfunction x(){}", "export const PACK_LABELS = {'b':{en:'B'}};\nfunction x(){}"));
assert(!editorialDataOnly("export const PACK_LABELS = {};", "export const PACK_LABELS = {x:evil()};"));
assert(!editorialDataOnly("export const PACK_LABELS = {};\nfunction x(){}", "export const PACK_LABELS = {};\nfunction x(){evil()}"));
assert.deepEqual(classify(['site/shared-model-browser-test.mjs'],manifest).tasks,['shared']);
const round02={assets:appended.assets,publication:{round02_descriptor:{},approved_round02_ids:['new']}};
const scoped=classify(['assets/manifest.json'],round02,false,{previousManifest:manifest});
assert.equal(scoped.runtime,false);assert.equal(scoped.ids,'new');assert.deepEqual(scoped.tasks,['models','round02','previews']);
assert.deepEqual(classify(['site/hover-reveal-browser-test.mjs'],manifest).tasks,['hover']);
assert(classify([],manifest,true).tasks.includes('hover'));
const round03={assets:appended.assets,publication:{round03_descriptor:{},approved_round03_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round03,false,{previousManifest:manifest}).tasks,['models','round03','previews']);

const round04={assets:appended.assets,publication:{round04_descriptor:{},approved_round04_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round04,false,{previousManifest:manifest}).tasks,['models','round04','previews']);

const round05={assets:appended.assets,publication:{round05_descriptor:{},approved_round05_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round05,false,{previousManifest:manifest}).tasks,['models','round05','previews']);

const round06={assets:appended.assets,publication:{round06_descriptor:{},approved_round06_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round06,false,{previousManifest:manifest}).tasks,['models','round06','previews']);
const round07={assets:appended.assets,publication:{round07_descriptor:{},approved_round07_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round07,false,{previousManifest:manifest}).tasks,['models','round07','previews']);
const round08={assets:appended.assets,publication:{round08_descriptor:{},approved_round08_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round08,false,{previousManifest:manifest}).tasks,['models','round08','previews']);
const round09={assets:appended.assets,publication:{round09_descriptor:{},approved_round09_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round09,false,{previousManifest:manifest}).tasks,['models','round09','previews']);
const round10={assets:appended.assets,publication:{round10_descriptor:{},approved_round10_ids:['new']}};
assert.deepEqual(classify(['assets/manifest.json'],round10,false,{previousManifest:manifest}).tasks,['models','round10','previews']);
