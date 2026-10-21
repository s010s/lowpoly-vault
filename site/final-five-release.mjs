/** Fixed owner-authorized website delivery. Compact protected review anchors replace
 * historical process-body reads only for these five; old release gates are unchanged.
 * This does not grant physical GPU, target-scene, formal-profile, CI, or live acceptance. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {collectFinalDeliveryCandidates} from './final-delivery.mjs';
import {digest} from './model-registry.mjs';
import {posterInputKey,posterSharedInputs} from './gallery-poster-inputs.mjs';
import {CARD_RENDER_PRESET} from './render-preset.js';
import {assetFileAllowlist} from './asset-delivery.mjs';
export const FINAL_FIVE_IDS=Object.freeze(['caryocrinites','echinosphaerites','eleutherocrinus','micraster','nucleocrinus']);
export const FINAL_FIVE_PRESENTATION=Object.freeze({path:'qa/final-delivery-20261021/website-presentation-index.json',sha256:'813016309e1db751efd0d784be59494e3167bd18a39b64a82a066f86e09edd9b'});
const BASE347_ASSETS='635a0838674969ffab5bba9dd8f1a5edc161059822d1a1c29dd8fc40cc2a5c47';
const sha=b=>createHash('sha256').update(b).digest('hex');
async function local(root,path){assert(typeof path==='string'&&!path.startsWith('/')&&!path.includes('\\')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..'));const full=resolve(root,path);assert.equal(await realpath(full),full,'Symlink substitution rejected');return readFile(full);}
async function checked(root,pin){assert(/^[a-f0-9]{64}$/.test(pin.sha256));const b=await local(root,pin.path);assert.equal(sha(b),pin.sha256,`Final5 pin changed: ${pin.path}`);if(pin.bytes!==undefined)assert.equal(b.length,pin.bytes);return b;}
function png(b,size){assert.equal(b.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.deepEqual([b.readUInt32BE(16),b.readUInt32BE(20)],size);}
export async function collectFinalFiveRelease(root=process.cwd(),pin=FINAL_FIVE_PRESENTATION){
 assert.deepEqual(pin,FINAL_FIVE_PRESENTATION,'Only exact independently reviewed fixed5 presentation is accepted');
 const index=JSON.parse(await checked(root,pin));
 assert.deepEqual(index.selected_ids,FINAL_FIVE_IDS);assert.equal(index.rows.length,5);
 assert.equal(index.hardware_gpu_verified,false);assert.equal(index.target_scene_verified,false);assert.equal(index.formal_profile_acceptance,'BLOCKED');
 assert.equal(index.independent_gallery_review.status,'PASS_BOUNDED_GALLERY_PRESENTATION');
 const content=collectFinalDeliveryCandidates(root); // Full seven-role reads, fixed original QA/archive anchors, actual GLB recomputation.
 assert.deepEqual(content.candidates.map(x=>x.id).sort(),FINAL_FIVE_IDS);
 const shared=await posterSharedInputs(root);assert.deepEqual(index.capture.shared,shared,'Exact current gallery recipe required');
 const cardIndex=JSON.parse(await checked(root,index.card_presentation_index));
 const gallery=JSON.parse(await local(root,'site/public/gallery/resources.json'));
 const cards=JSON.parse(await local(root,'assets/turntables/index.json'));
 const additions=[];
 for(const row of index.rows){
  const c=content.candidates.find(x=>x.id===row.id);assert(c,'Outside fixed5 content');
  const a=JSON.parse(await checked(root,row.metadata));assert.equal(a.id,row.id);assetFileAllowlist({assets:[a]});
  assert.equal(a.glb,c.final_paths.glb);assert.equal(a.blend,c.final_paths.source);
  assert.equal(a.sha256.glb,c.native.glb_sha256);assert.equal(a.sha256.blend,c.blend_sha256);
  assert.deepEqual(a.bounds_glb_m,c.native.bounds_m);assert.deepEqual(a.dimensions,c.native.bounds_m.size);assert.equal(a.triangles,c.native.triangles);assert.equal(a.materials,c.native.materials);
  assert.equal(a.approval_provenance.hardware_gpu_verified,false);assert.equal(a.approval_provenance.target_scene_verified,false);assert.equal(a.approval_provenance.publication_authority,false);
  assert.equal(a.preview,row.canonical_preview.path);assert.equal(a.sha256.preview,row.canonical_preview.sha256);png(await checked(root,row.canonical_preview),[768,768]);
  const cardReview=cardIndex.rows.find(x=>x.id===row.id);assert(cardReview);assert.equal(cardReview.decision,'PASS_BOUNDED_CARD_PRESENTATION');assert.equal(cardReview.source_glb_sha256,a.sha256.glb);assert.deepEqual(cardReview.preview,row.canonical_preview);assert.deepEqual(cardReview.card,row.card);
  await checked(root,row.card);assert.equal(row.card.source_glb_sha256,a.sha256.glb);assert.equal(row.card.render_preset_sha256,sha(JSON.stringify(CARD_RENDER_PRESET)));
  assert.deepEqual(cards.posters.filter(x=>x.id===row.id),[{id:row.id,...row.card}]);
  assert.equal(row.presentation_verdict,'PASS_BOUNDED_GALLERY_PRESENTATION');
  assert.equal(row.gallery.source_glb_sha256,a.sha256.glb);assert.equal(row.gallery.poster.input_sha256,posterInputKey(a,shared));assert.equal(row.poster_input_sha256,row.gallery.poster.input_sha256);
  assert.deepEqual(gallery.posters[row.id],row.gallery.poster);assert.equal(row.gallery.files.length,2);
  for(const kind of ['detail','wheel']){const path=`gallery/posters/${row.id}${kind==='wheel'?'-wheel':''}.png`,f=row.gallery.files.find(x=>x.path===path);assert(f);assert.equal(row.gallery.poster[kind],path);assert.deepEqual(gallery.files.filter(x=>x.path===path),[f]);png(await checked(root,{...f,path:`site/public/${path}`}),kind==='wheel'?[768,432]:[512,512]);}
  additions.push({...a,packs:['prehistoric-final-five-20261021']});
 }
 assert.deepEqual(additions.map(x=>x.id).sort(),FINAL_FIVE_IDS);
 return {additions,index,content};
}
export async function appendFinalFiveRelease(root,base,pin){
 assert.equal(base.assets.length,347);assert.equal(digest(base.assets),BASE347_ASSETS,'Existing347 assets must remain exact');assert(!base.assets.some(x=>FINAL_FIVE_IDS.includes(x.id)));
 const {additions}=await collectFinalFiveRelease(root,pin);
 return {...base,assets:[...base.assets,...additions],publication:{...base.publication,final_five_presentation:FINAL_FIVE_PRESENTATION}};
}
