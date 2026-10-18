/** Explicit twelve-asset publication, composed on the unchanged nineteen. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {ACCEPTED_BATCH_ASSETS} from './accepted-small-life-batch-data.mjs';
import {collectSmallFaunaRelease} from './small-fauna-release.mjs';
import {assetFileAllowlist} from './asset-delivery.mjs';
export const BATCH_IDS=Object.keys(ACCEPTED_BATCH_ASSETS).sort();
export const BATCH_PACK='prehistoric-small-life-20261018';
const plants=new Set(['aglaophyton','hydropteris','onoclea']);
const hash=b=>createHash('sha256').update(b).digest('hex');
const pin=p=>({path:p.path,sha256:p.sha256});
async function checked(root,p) {
 assert(p&&Object.keys(p).sort().join(',')==='path,sha256','Exact release pin required');
 assert(typeof p.path==='string'&&/^(assets|production|qa)\//.test(p.path)&&!/[\\\u0000-\u001f?#%:]/.test(p.path)&&p.path.split('/').every(s=>s&&s!=='.'&&s!=='..'),'Safe release path required');
 assert(/^[a-f0-9]{64}$/.test(p.sha256));const full=resolve(root,p.path);assert.equal(await realpath(full),full,'Release symlinks forbidden');
 const bytes=await readFile(full);assert.equal(hash(bytes),p.sha256,`${p.path}: release hash mismatch`);return bytes;
}
const json=async(root,p)=>JSON.parse(await checked(root,p));
function runtimeErrors(value) {
 if(Array.isArray(value)){for(const child of value)runtimeErrors(child);return;}
 if(!value||typeof value!=='object')return;
 for(const[key,v]of Object.entries(value)){
  if(['errors','failed','page_errors','pageErrors','consoleErrors','resource_errors'].includes(key))assert(Array.isArray(v)&&v.length===0,'Frozen runtime error arrays must be empty');
  if(key==='gl_error')assert.equal(v,0);runtimeErrors(v);
 }
}
export async function collectSmallLifeBatchRelease(root,p) {
 assert.equal(p?.path,'assets/releases/small-life-twelve-20261018.json');const release=await json(root,p);
 assert.equal(release.version,1);assert.equal(release.scope,'small-life-twelve-20261018');
 assert.equal(release.authorization,'owner_authorized_publish_independent_qa_passed_batches');assert.equal(release.authorization_reference,'owner-qa-pass-production-policy-20261018');
 assert.equal(release.base_descriptor.path,'assets/releases/small-fauna-trio-v002-20261018.json');
 assert.deepEqual(release.additions.map(a=>a.id).sort(),BATCH_IDS,'Exact independently reviewed twelve required');
 const additions=[];assert.equal(release.batches.length,3);
 for(const entry of release.additions) {
  const accepted=ACCEPTED_BATCH_ASSETS[entry.id],id=entry.id,folder=`assets/additions/${id}/small-life-20261018`;
  const batch=release.batches.find(b=>b.batch===accepted.batch);assert(batch);
  assert.equal(batch.source_commit,accepted.source_commit);assert.equal(batch.review_commit,accepted.review_commit);assert.deepEqual(batch.review,accepted.review);assert(batch.ids.includes(id));
  assert.equal(entry.metadata.path,`${folder}/release-metadata.json`);const a=await json(root,entry.metadata),source=await json(root,accepted.source_metadata);
  assert.equal(a.id,id);assert.equal(source.id,id);assert.deepEqual(a.name,source.name,'Retain reviewed display names');assert.deepEqual(a.description,source.description,'Retain reviewed description and uncertainty wording');
  assert.equal(a.source_category,source.category);assert.equal(a.category,plants.has(id)?'plants':'animals');assert.equal(a.collection,'prehistoric');
  assert.deepEqual(a.worlds,['prehistoric']);assert.deepEqual(a.packs,[BATCH_PACK]);assert.equal(a.license,'CC-BY-4.0');assert.equal(a.author,'Leon Made This / s010s');assert.equal(a.units,'meters');
  for(const key of ['triangles','dimensions','axes','origin','bounds_glb_m','sources','nominal_scale'])assert.deepEqual(a[key],source[key],`Preserve reviewed ${key}`);
  assert.equal(a.source_url,`https://github.com/s010s/lowpoly-vault/tree/${accepted.source_commit}/${dirname(source.glb)}`);
  for(const key of ['name','description','scientific_scope'])for(const lang of ['en','zh'])assert(a[key]?.[lang]?.trim(),`Bilingual ${key} required`);
  for(const key of ['qa','review_only','release_status','quality_status','publication','downloads','turntable','card_preview','revision','revision_provenance'])assert(!Object.hasOwn(a,key),`Reserved release field ${key}`);
  assert.deepEqual(a.sha256,entry.sha256);assetFileAllowlist({assets:[a]});
  for(const key of ['glb','blend','preview']) {
   assert.equal(dirname(a[key]),folder,'Immutable addition folder required');const b=await checked(root,{path:a[key],sha256:entry.sha256[key]});
   if(key!=='preview'){
    assert.equal(entry.sha256[key],accepted[key].sha256,'Exact reviewed payload required');assert.equal(b.length,accepted[key].bytes);assert.equal(hash(await checked(root,pin(accepted[key]))),entry.sha256[key]);assert.equal(source.sha256[key],entry.sha256[key]);
   }
   if(key==='glb')assert(b.toString('ascii',0,4)==='glTF'&&b.readUInt32LE(4)===2&&b.readUInt32LE(8)===b.length,'Real GLB 2 required');
  }
  await checked(root,accepted.candidate);await checked(root,accepted.views);
  const validator=await json(root,accepted.validator);assert.equal(validator.issues.numErrors,0);assert.equal(validator.issues.numWarnings,0);
  const runtime=await json(root,accepted.runtime);assert.equal(runtime.status,'pass');assert.equal(runtime.glb_sha256,a.sha256.glb);runtimeErrors(runtime);
  const views=runtime.records?.flatMap(r=>r.views)||runtime.views;assert(views?.some(v=>v.triangles>0||v.rendered_triangles>0),'Frozen functional rendering work required');
  const review=(await checked(root,accepted.review)).toString();assert(review.includes(accepted.source_commit),'Independent QA must bind exact source commit');
  assert(new RegExp('(?:###\\s+'+id+'\\b[^\\n]*PASS|`'+id+'`[^\\n]*PASS)','i').test(review),'Per-asset independent PASS required');
  for(const snapshot of Object.values(accepted.source_snapshots))await checked(root,snapshot);
  additions.push({...a,quality_status:'independent_qa_accepted_stylized_prop',approval_provenance:{source_commit:accepted.source_commit,review_commit:accepted.review_commit,review_sha256:accepted.review.sha256}});
 }
 const base=await collectSmallFaunaRelease(root,release.base_descriptor);assert.equal(base.assets.length,19);
 assert(!additions.some(a=>base.assets.some(b=>b.id===a.id)),'Reviewed additions cannot replace existing assets');
 return {...base,assets:[...base.assets,...additions],publication:{...base.publication,batch_descriptor:p,approved_batch_ids:BATCH_IDS}};
}
