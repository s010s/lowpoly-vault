/** Immutable fixed44 source/card checks and publication-denial regressions. No render is fabricated. */
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
import {posterSharedInputs} from './gallery-poster-inputs.mjs';
import {historical295Fixture} from './test-historical295-fixture.mjs';
import {digest} from './model-registry.mjs';
import {mkdtemp,mkdir,readFile,writeFile,link,unlink,symlink,rm} from 'node:fs/promises';
import {resolve,join,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {FORTY_FOUR_RELEASES as fixed} from './accepted-forty-four-release.mjs';
import {FORTY_FOUR_IDS,preflightFortyFourAdditions,collectFortyFourAdditions,appendFortyFourRelease,assertFortyFourGallerySubjects} from './forty-four-release.mjs';

const source=process.cwd(),root=await mkdtemp(join(dirname(source),'.vault-fixed44-negative-'));
const descriptors=fixed.map(record=>record.descriptor),first=fixed[0].release,entry=first.additions[0];
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
let checks=0;
const passed=label=>{checks++;console.log('PASS',label);};
const pins=new Map();
function collectPins(value){
 if(!value||typeof value!=='object')return;
 if(typeof value.path==='string'&&/^[a-f0-9]{64}$/.test(value.sha256)&&!value.path.startsWith('/'))pins.set(value.path,value.sha256);
 for(const child of Object.values(value))collectPins(child);
}
collectPins(fixed);
for(const {release}of fixed){
 const bundle=JSON.parse(await readFile(resolve(source,release.source_bundle.path)));collectPins(bundle);
 const cardIndex=JSON.parse(await readFile(resolve(source,release.capture.index.path)));
 for(const entry of release.additions){
  const asset=JSON.parse(await readFile(resolve(source,entry.metadata.path)));
  for(const kind of ['glb','blend','preview'])pins.set(asset[kind],asset.sha256[kind]);
  const card=cardIndex.posters.find(row=>row.id===asset.id);pins.set(card.path,card.sha256);
 }
}
async function materialize(path){
 const target=resolve(root,path);await mkdir(dirname(target),{recursive:true});
 await link(resolve(source,path),target);
}
async function mutate(path,transform,action){
 const target=resolve(root,path),original=await readFile(target);
 // Break the hard link before every mutation. Never write to reviewed checkout bytes.
 await unlink(target);await writeFile(target,transform(original));
 try{await action();}finally{await unlink(target);await writeFile(target,original);}
}
async function rejectBytes(label,path){
 await mutate(path,bytes=>Buffer.concat([bytes,Buffer.from('\nnegative-test-mutation')]),async()=>{
  await assert.rejects(()=>preflightFortyFourAdditions(root,descriptors),/hash mismatch/);passed(label);
 });
}
async function rejectDescriptor(label,change){
 await mutate(descriptors[0].path,bytes=>{const value=JSON.parse(bytes);change(value);return Buffer.from(JSON.stringify(value));},async()=>{
  const changed=structuredClone(descriptors);changed[0].sha256=sha(await readFile(resolve(root,changed[0].path)));
  await assert.rejects(()=>preflightFortyFourAdditions(root,changed),/exact fixed44 descriptor pins|fixed independently reviewed/);passed(label);
 });
}
try{
 for(const path of pins.keys())await materialize(path);
 await materialize('site/viewer.js');
 const result=await preflightFortyFourAdditions(root,descriptors);
 assert.equal(result.publication_ready,false);assert.equal(result.additions.length,44);
 assert.deepEqual(result.additions.map(asset=>asset.id).sort(),FORTY_FOUR_IDS);
 passed('all16 immutable source groups produce exact44 staging assets without publication authority');
 for(const asset of result.additions){
  assert.equal(asset.quality_status,'independent_qa_accepted_stylized_prop');
  assert.equal(asset.approval_provenance.candidate_record_approved_for_brief,false);
  assert.equal(asset.approval_provenance.formal_profile_acceptance,'BLOCKED');
  assert.equal(asset.approval_provenance.hardware_gpu_verified,false);
  assert.equal(asset.approval_provenance.target_scene_verified,false);
 }
 passed('all44 final assets retain pending formal/GPU/scene limits');

 const metadata=JSON.parse(await readFile(resolve(root,entry.metadata.path)));
 const candidate=JSON.parse(await readFile(resolve(root,entry.candidate.path)));
 const proof=JSON.parse(await readFile(resolve(root,entry.proof.path)));
 const index=JSON.parse(await readFile(resolve(root,first.capture.index.path)));
 const card=index.posters.find(row=>row.id===entry.id);
 for(const [label,path]of [
  ['descriptor byte tamper',descriptors[0].path],['source bundle byte tamper',first.source_bundle.path],
  ['source GLB byte tamper',candidate.artifacts.glb.path],['source blend byte tamper',candidate.artifacts.source.path],
  ['delivery GLB byte tamper',metadata.glb],['delivery blend byte tamper',metadata.blend],
  ['metadata byte tamper',entry.metadata.path],['candidate byte tamper',entry.candidate.path],
  ['active profile byte tamper',entry.active_profile.path],['original metrics byte tamper',entry.original_metrics.path],
  ['active independent review byte tamper',entry.active_review.path],['proof8 manifest byte tamper',entry.proof.path],
  ['proof8 PNG byte tamper',`${dirname(entry.proof.path)}/${proof.frames[0].path}`],
  ['original capture metadata byte tamper',entry.capture_input_metadata.path],
  ['card PNG byte tamper',entry.capture_reference.path],['card WebP byte tamper',card.path],
  ['original gallery receipt byte tamper',first.capture.original_gallery_receipt.path],
  ['original visual review byte tamper',first.capture.independent_review.path],
  ['artifact binding byte tamper',first.capture.artifact_verification.path],
  ['bounded44 subset byte tamper',first.capture.subset.path],
 ])await rejectBytes(label,path);
 await rejectDescriptor('rehashing cannot admit a non44 ID',release=>{release.additions[0].id='braided-river-reach';});
 await rejectDescriptor('rehashing cannot replace the source commit',release=>{release.source_commit='0'.repeat(40);});
 await rejectDescriptor('rehashing cannot promote formal acceptance',release=>{release.formal_profile_acceptance='APPROVED';});
 await rejectDescriptor('rehashing cannot claim hardware GPU verification',release=>{release.hardware_gpu_verified=true;});
 await rejectDescriptor('rehashing cannot claim intended-scene verification',release=>{release.target_scene_verified=true;});
 await rejectDescriptor('rehashing cannot relabel the original receipt as final',release=>{release.capture.final_gallery_receipt=release.capture.original_gallery_receipt;});
 await rejectDescriptor('rehashing cannot omit a protected source input',release=>{release.protected_source_inputs.pop();});
 await assert.rejects(()=>preflightFortyFourAdditions(root,descriptors.slice(0,15)),/exact 16 fixed44 descriptors/);
 passed('missing source group rejected');
 await assert.rejects(()=>preflightFortyFourAdditions(root,[...descriptors].reverse()),/exact 16 fixed44 descriptors/);
 passed('source-group reordering rejected');
 {
  const target=resolve(root,entry.metadata.path),original=await readFile(target);
  await unlink(target);await symlink(resolve(source,entry.metadata.path),target);
  try{await assert.rejects(()=>preflightFortyFourAdditions(root,descriptors),/symlinks forbidden/);passed('exact-byte symlink evidence rejected');}
  finally{await unlink(target);await writeFile(target,original);}
 }
 const historical=JSON.parse(await readFile(resolve(root,first.capture.original_gallery_receipt.path)));
 assert.throws(()=>assertFortyFourGallerySubjects(historical,result.additions),/exactly44/);
 passed('original47 capture is never a final44 receipt');
 // In-memory negative fixture only: narrowing selection cannot change the original captured subject.
 const narrowed=structuredClone(historical);narrowed.selected_ids=[...FORTY_FOUR_IDS];
 narrowed.rows=narrowed.rows.filter(row=>FORTY_FOUR_IDS.includes(row.id));
 assert.throws(()=>assertFortyFourGallerySubjects(narrowed,result.additions),/final gallery subject mismatch/);
 passed('even exact44 historical rows fail final metadata subject binding');
 const changedFinal=structuredClone(result.additions);changedFinal[0].description.en+=' changed';
 assert.throws(()=>assertFortyFourGallerySubjects(narrowed,changedFinal),/final gallery subject mismatch/);
 passed('final metadata changes cannot reuse historical poster inputs');
 const extra=structuredClone(result.additions);extra.push({...extra[0],id:'kettle-basin'});
 assert.throws(()=>assertFortyFourGallerySubjects(narrowed,extra),/exact fixed44/);
 passed('gallery cannot expand to excluded or extra IDs');
 for(const [field,value]of [['formal_acceptance','APPROVED'],['physical_gpu_verified',true],['target_scene_verified',true]]){
  const invalid=structuredClone(narrowed);invalid[field]=value;
  assert.throws(()=>assertFortyFourGallerySubjects(invalid,result.additions));passed(`gallery cannot promote ${field}`);
 }
 const current=JSON.parse(await readFile(resolve(source,'assets/manifest.json'))),currentBytes=JSON.stringify(current);
 const manifest=historical295Fixture(current);
 assert.equal(JSON.stringify(current),currentBytes);passed('fixed347 projection preserves complete canonical old295 without mutating input');
 for(const [label,change]of [
  ['old model field',m=>{m.assets[0].description.en+=' changed';}],
  ['old model order',m=>{[m.assets[0],m.assets[1]]=[m.assets[1],m.assets[0]];}],
  ['old review pin',m=>{m.assets.find(a=>a.source_identity?.active_review).source_identity.active_review.sha256='0'.repeat(64);}],
  ['new wrong ID',m=>{m.assets.find(a=>a.id==='arroyo-wash').id='kettle-basin';}],
  ['new duplicate ID',m=>{m.assets.find(a=>a.id==='arroyo-wash').id='badlands-ridge-network';}],
  ['extra deletion',m=>{m.assets.shift();}],
  ['new descriptor field',m=>{m.publication.fifty_two_descriptors[0].sha256='0'.repeat(64);}],
  ['forged digest',m=>{m.assets[0].description.en+=' changed';m.publication.baseline295_canonical_sha256=digest(manifest);}],
  ['extra stripped-looking field',m=>{m.publication.fifty_two_unreviewed=true;}]
 ]){const bad=structuredClone(current);change(bad);assert.throws(()=>historical295Fixture(bad));passed('fixed historical projection refuses '+label);}
 const base={...manifest,publication:{...manifest.publication},assets:manifest.assets.filter(asset=>!FORTY_FOUR_IDS.includes(asset.id))};
 delete base.publication.forty_four_descriptors;
 assert.equal(digest(base),'7f6c94c26f0a47b7a1b461f48070868be57f94161c9a1e3c11b5666cd8b273e0','Complete immutable main43 predecessor changed');
 assert.equal(base.assets.length,251);const baseBytes=JSON.stringify(base);
 await assert.rejects(()=>appendFortyFourRelease(root,{...base,assets:base.assets.slice(1)},descriptors),/exact251/);
 passed('append rejects a non251 baseline');
 const collision={...base,assets:[...base.assets.slice(1),result.additions[0]]};
 await assert.rejects(()=>appendFortyFourRelease(root,collision,descriptors),/replace an existing251/);
 passed('append rejects collisions instead of changing existing assets');
 const ready=fixed.every(({release})=>['final_gallery_receipt','final_gallery_review','final_gallery_artifact_verification'].every(key=>release.capture[key]));
 if(!ready){
  await assert.rejects(()=>collectFortyFourAdditions(root,descriptors),/final gallery subject mismatch.*pending/);
  passed('publication collector remains BLOCKED pending actual final-subject evidence');
  await assert.rejects(()=>appendFortyFourRelease(root,base,descriptors),/final gallery subject mismatch.*pending/);
  assert.equal(JSON.stringify(base),baseBytes);passed('blocked publication leaves existing251 wholly unchanged');
 }else{
  // Actual final-subject evidence is available: verify byte-tamper refusal without
  // ever mutating the reviewed source tree. Fixture links are broken by mutate().
  const finalReceipt=JSON.parse(await readFile(resolve(source,first.capture.final_gallery_receipt.path)));
  const shared=await posterSharedInputs(source);
  for(const path of [...shared.files.map(([path])=>path),'assets/turntables/index.json','site/public/gallery/resources.json',...finalReceipt.rows.flatMap(row=>row.files.map(file=>'site/public/'+file.path))])
   if(!existsSync(resolve(root,path)))await materialize(path);
  await symlink(resolve(source,'node_modules'),resolve(root,'node_modules'),'dir');
  for(const [label,path]of [
   ['actual final receipt byte tamper',first.capture.final_gallery_receipt.path],
   ['actual final artifact verification byte tamper',first.capture.final_gallery_artifact_verification.path],
   ['actual final independent pixel review byte tamper',first.capture.final_gallery_review.path],
   ['actual final detail PNG byte tamper','site/public/'+finalReceipt.rows[0].poster.detail],
   ['actual final wheel PNG byte tamper','site/public/'+finalReceipt.rows[0].poster.wheel],
  ])await mutate(path,bytes=>Buffer.concat([bytes,Buffer.from('negative-final-byte-tamper')]),async()=>{
   await assert.rejects(()=>collectFortyFourAdditions(root,descriptors));passed(label);
  });
  await mutate('site/public/gallery/resources.json',bytes=>{const data=JSON.parse(bytes);data.posters[finalReceipt.rows[0].id].input_sha256='0'.repeat(64);return Buffer.from(JSON.stringify(data));},async()=>{
   await assert.rejects(()=>collectFortyFourAdditions(root,descriptors));passed('public final gallery metadata tamper rejected');
  });
  assert.throws(()=>assertFortyFourGallerySubjects(finalReceipt,changedFinal),/final gallery subject mismatch/);
  passed('actual final receipt cannot be reused after metadata changes');
  const collected=await collectFortyFourAdditions(source,descriptors);assert.equal(collected.additions.length,44);
  const appended=await appendFortyFourRelease(source,base,descriptors);
  assert.equal(appended.assets.length,295);assert.deepEqual(appended.assets.slice(0,251),base.assets);assert.deepEqual(appended,manifest);
  assert.equal(JSON.stringify(base),baseBytes);passed('verified final receipt allows exact251→295 without baseline mutation');
 }
 console.log(JSON.stringify({status:'PASS',checks,source_card_preflight:'PASS',final_gallery_publication_gate:ready?'PASS':'BLOCKED_PENDING_REAL_FINAL_SUBJECT_CAPTURE_AND_REVIEW',formal_acceptance:'BLOCKED',hardware_gpu_verified:false,target_scene_verified:false}));
}finally{await rm(root,{recursive:true,force:true});}
