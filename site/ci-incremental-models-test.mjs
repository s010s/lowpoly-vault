import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {assessIncrementalDiff,tasksForModelPlan} from './ci-incremental-models.mjs';
const clone=value=>structuredClone(value),read=path=>JSON.parse(readFileSync(path));
const before=read('assets/manifest.json'),catalog=read('site/catalog-data.json'),after=clone(before),newCatalog=clone(catalog);
const paths=['assets/manifest.json','site/catalog-data.json','assets/releases/existing-reviewed-descriptor.json'];
const pack={id:'incremental-fixture-pack',name:{en:'Fixture pack',zh:'测试模型组合'},description:{en:'No real publication',zh:'未发布的测试数据'},asset_ids:[]};
for(let n=1;n<=4;n++){
 const a=clone(before.assets[0]);a.id=`incremental-model-${n}`;a.packs=[pack.id];a.worlds=['prehistoric'];
 for(const key of ['glb','blend','preview'])a[key]=`assets/additions/${a.id}/fixture/model.${key==='preview'?'png':key}`;
 after.assets.push(a);pack.asset_ids.push(a.id);paths.push(...['glb','blend','preview'].map(k=>a[k]));
}
newCatalog.packs.push(pack);after.publication.fixture_descriptor={path:paths[2],sha256:'a'.repeat(64)};
const base={paths,before,after,readBefore:path=>{assert.equal(path,'site/catalog-data.json');return catalog;},readAfter:path=>{assert.equal(path,'site/catalog-data.json');return newCatalog;}};
const good=assessIncrementalDiff(base);assert.equal(good.eligible,true,good.reasons.join('; '));assert.equal(good.added_ids.length,4);assert.equal(after.assets.length,before.assets.length+4);
const reject=(edit,label)=>{const input={...base,paths:[...paths],before:clone(before),after:clone(after)};edit(input);assert.equal(assessIncrementalDiff(input).eligible,false,label);};
reject(input=>input.paths.push('qa/unclassified/test.py'),'Unknown executable');reject(input=>input.paths.push('site/viewer.js'),'Renderer');reject(input=>input.paths.push('site/new-unreviewed-release.mjs'),'Unknown collector');reject(input=>input.after.assets[0].sha256.glb='f'.repeat(64),'Old model changed');reject(input=>input.after.assets.shift(),'Old model removed');reject(input=>input.after.assets.push(clone(input.after.assets.at(-1))),'Duplicate new ID');reject(input=>input.paths.push('site/gallery/approved-poster-inputs.json'),'Golden metadata');
const auth={...base,paths:[...paths,'site/known-publication-only.mjs'],authorizationOnlyPaths:['site/known-publication-only.mjs']};assert.equal(assessIncrementalDiff(auth).eligible,true,'Explicit policy-supplied auth-only role; never from repository data');
// Real old190 resource metadata plus four owned additions. Capture diagnostics
// must not invalidate unchanged pixels, nor hide a renderer/recipe change.
const galleryPath='site/public/gallery/resources.json',oldGallery=read(galleryPath),newGallery=clone(oldGallery);
newGallery.generated_capture.assets=good.added_ids;newGallery.generated_capture.published_total=after.assets.length;
for(const id of good.added_ids){
 const source=Object.values(oldGallery.posters)[0],poster={...source,detail:`gallery/posters/${id}.png`,wheel:`gallery/posters/${id}-wheel.png`};
 newGallery.posters[id]=poster;
 for(const path of [poster.detail,poster.wheel])newGallery.files.push({...oldGallery.files[0],path});
}
const withGallery=value=>({...base,paths:[...paths,galleryPath],readBefore:path=>path===galleryPath?oldGallery:base.readBefore(path),readAfter:path=>path===galleryPath?value:base.readAfter(path)});
assert.equal(assessIncrementalDiff(withGallery(newGallery)).eligible,true,'Canonical four-only capture diagnostics preserve incremental eligibility');
for(const edit of [
 value=>value.generated_capture.browser='different-browser',
 value=>value.generated_capture.source_renderer_sha256='f'.repeat(64),
 value=>value.generated_capture.runtime_renderer_sha256='f'.repeat(64),
 value=>value.generated_capture.unknown_recipe_option=true,
 value=>value.generated_capture.assets.push(good.added_ids[0]),
 value=>value.generated_capture.assets.push('not-published'),
 value=>value.generated_capture.published_total=after.assets.length+1,
 value=>value.generated_capture.published_total=-1,
 value=>value.posters[before.assets[0].id].detail='gallery/posters/changed.png',
 value=>value.files[0].sha256='f'.repeat(64),
]){const changed=clone(newGallery);edit(changed);assert.equal(assessIncrementalDiff(withGallery(changed)).eligible,false,'Invalid diagnostics, changed recipe or old pixels must require full checks');}
assert.deepEqual(tasksForModelPlan(['models-1-of-5','models-2-of-5','handoff'],{fresh_ids:good.added_ids},after),['models-1-of-4','models-2-of-4','models-3-of-4','models-4-of-4','previews','handoff']);assert.deepEqual(tasksForModelPlan(['models-1-of-5','previews','handoff'],{fresh_ids:[]},after),['handoff']);
console.log('Incremental eligibility: exact owned additions, old-record preservation, explicit known publication role; unknown code/renderer/golden changes require full.');
