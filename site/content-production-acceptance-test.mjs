import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readFile,writeFile,mkdir,rm,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {sha256} from './inventory-type-acceptance.mjs';
import {publicMaterial,inspectContentProductionRelease,verifyContentProjectionReviews} from './content-production-acceptance.mjs';
import {collectProductionRelease,appendProductionRelease,productionSourceClosure,productionGalleryResources} from './production-release.mjs';
import {deliverManifestAssets,creditText} from './asset-delivery.mjs';
import {deliverTurntables} from './turntable-delivery.mjs';
import {spawnSync} from 'node:child_process';
import {isPreservedImplementationBridge} from './preserved-implementation-bridges.mjs';
const source=process.env.CONTENT_TEST_SOURCE_ROOT||resolve(dirname(fileURLToPath(import.meta.url)),'..');
const encode=x=>Buffer.from(JSON.stringify(x));
const pin=(path,b)=>({path,bytes:b.length,sha256:sha256(b)});
// Disposable copies of TWO actual legacy/v2 public assets, never a production receipt.
// The rewritten descriptor/review are test inputs, not new independent acceptance.
async function setup(route='v2'){
 const root=await mkdtemp(resolve(tmpdir(),'content-acceptance-')),path='production/content-check/release.json';
 const old=JSON.parse(await readFile(resolve(source,route==='inventory'?'production/next-eleven-20261022/release-r002.json':'production/ready72-20261022/release-v2.json'))),item=structuredClone(old.assets[0]);
 const copied=new Set();
 async function put(path,raw){await mkdir(dirname(resolve(root,path)),{recursive:true});await writeFile(resolve(root,path),raw);}
 async function copyPins(value){
  if(!value||typeof value!=='object')return;
  if(value.path&&value.sha256&&value.bytes&&!copied.has(value.path)){
   copied.add(value.path);let raw;try{raw=await readFile(resolve(source,value.path));}catch(e){if(e.code==='ENOENT')return;throw e;}await put(value.path,raw); // Historical source locators need not be public; mandatory public pins are checked by the validator.
   if(value.path.endsWith('.json'))await copyPins(JSON.parse(raw));
  }
  for(const child of Object.values(value))await copyPins(child);
 }
 await copyPins(item);await copyPins(old.scope_document);
 const asset=JSON.parse(await readFile(resolve(root,item.metadata.path))),record=JSON.parse(await readFile(resolve(root,item.evidence.path)));
 asset.production_release=path;const assetRaw=encode(asset);await put(item.metadata.path,assetRaw);item.metadata=pin(item.metadata.path,assetRaw);
 // Credits are generated delivery output, not a tracked source fixture.
 const licenses=[],licensePath='LICENSES/CC-BY-4.0.txt',licenseBytes=await readFile(resolve(source,licensePath));
 await put(licensePath,licenseBytes);licenses.push(pin(licensePath,licenseBytes));
 if(asset.credits){const b=Buffer.from(creditText(asset,{author:'Leon Made This / s010s',attribution_url:'https://github.com/s010s/lowpoly-vault'}));await put(asset.credits,b);licenses.push(pin(asset.credits,b));}
 const descriptor={...old,kind:'content-production-release-v1',assets:[item],review_path:'production/content-check/review.json',licenses};delete descriptor.implementation;
 const review=JSON.parse(await readFile(resolve(source,old.review_path)));
 review.inventory_compatibility=review.inventory_compatibility.filter(x=>x.asset_id===item.id);review.original_acceptance_sha256=[record.original_acceptance.sha256];delete review.checks.adapter_code_and_legacy_compatibility;
 async function save(){const raw=encode(descriptor);await put(path,raw);review.reviewed_descriptor_sha256=sha256(raw);await put(descriptor.review_path,encode(review));}
 await save();return {root,path,item,asset,record,descriptor,review,put,save,cleanup:()=>rm(root,{recursive:true,force:true})};
}
async function run(f){const result=await inspectContentProductionRelease(f.root,f.path);await verifyContentProjectionReviews(f.root,result);return result;}
async function changedRecord(f,mutate){mutate(f.record);const b=encode(f.record);await f.put(f.item.evidence.path,b);f.item.evidence=pin(f.item.evidence.path,b);await f.save();}
for(const route of ['inventory','v2'])test(`actual ${route} content retains strict acceptance and unverified runtime`,async()=>{
 const f=await setup(route);try{const r=await run(f);assert.equal(r.assets.length,1);assert.equal(r.productionAccepted,true);assert.equal(r.publication_authorized,false);assert.notEqual(r.postReleaseVerified,'PASS');assert.equal(r.releaseChecks,'PENDING_INDEPENDENT_PROJECTION_REVIEW');}finally{await f.cleanup();}
});
const mutations={
 'non-production record':async f=>changedRecord(f,r=>r.productionAccepted=false),
 'wrong metadata hash':async f=>{f.item.metadata.sha256='f'.repeat(64);await f.save();},
 'path traversal':async f=>{f.item.evidence.path='../outside.json';await f.save();},
 'duplicate ID':async f=>{f.descriptor.assets.push(structuredClone(f.item));await f.save();},
 'wrong member ID':async f=>changedRecord(f,r=>r.asset_id='different-animal'),
 'changed final GLB':async f=>f.put(f.record.roles.finalGLB.path,Buffer.from('tampered GLB')),
 'changed source':async f=>f.put(f.record.roles.generator.path,Buffer.from('tampered source')),
 'changed Blend':async f=>f.put(f.record.roles.finalBlend.path,Buffer.from('tampered Blend')),
 'changed preview':async f=>f.put(f.record.preview.path,Buffer.from('tampered PNG')),
 'changed license':async f=>f.put('LICENSES/CC-BY-4.0.txt',Buffer.from('All rights reserved')),
 'missing license':async f=>{f.descriptor.licenses=[];await f.save();},
 'duplicate source member':async f=>changedRecord(f,r=>r.build_closure.push(r.build_closure[0])),
 'non-independent reviewer':async f=>{f.review.reviewer=f.record.maker;await f.save();},
 'PENDING reviewer':async f=>{f.review.status='PENDING';await f.save();},
 'REVISE reviewer':async f=>{f.review.status='REVISE';await f.save();},
 'blocking finding':async f=>{f.review.blocking_findings=['repair silhouette'];await f.save();},
 'original acceptance mismatch':async f=>{f.review.original_acceptance_sha256=['f'.repeat(64)];await f.save();},
 'stale typed review':async f=>{f.review.inventory_compatibility[0].compatibility_sha256='f'.repeat(64);await f.save();},
 'private file path':async f=>{f.item.metadata.path='.env';await f.save();},
 'private locator leakage':async f=>changedRecord(f,r=>r.private_url='https://drive.google.com/private'),
 'implementation lock returns':async f=>{f.descriptor.implementation=[];await f.save();},
 'publication authority escalation':async f=>{f.review.publication_authorized=true;await f.save();},
 'symlink source':async f=>{const path=f.record.roles.generator.path;await rm(resolve(f.root,path));await symlink(resolve(source,path),resolve(f.root,path));},
};
for(const [label,mutate] of Object.entries(mutations))test(`reject ${label}`,async()=>{const f=await setup();try{await mutate(f);await assert.rejects(()=>run(f));}finally{await f.cleanup();}});
test('caller-provided PASS cannot replace actual pending review',async()=>{const f=await setup();try{const passing=structuredClone(f.review);f.review.status='PENDING';await f.save();const result=await inspectContentProductionRelease(f.root,f.path);await assert.rejects(()=>verifyContentProjectionReviews(f.root,result,passing));}finally{await f.cleanup();}});
test('the five frozen bridges require exact bridge AND review bytes and paths',async()=>{
 const registry=JSON.parse(await readFile(resolve(source,'production/production-releases-r002.json')));assert.equal(registry.descriptors.filter(x=>x.compatibility).length,5);
 for(const {compatibility:p}of registry.descriptors.filter(x=>x.compatibility)){const raw=await readFile(resolve(source,p.path)),bridge=JSON.parse(raw),reviewRaw=await readFile(resolve(source,bridge.review_path));assert.equal(isPreservedImplementationBridge(p.path,raw,bridge.review_path,reviewRaw),true);assert.equal(isPreservedImplementationBridge(p.path,Buffer.concat([raw,Buffer.from(' ')]),bridge.review_path,reviewRaw),false);assert.equal(isPreservedImplementationBridge(p.path,raw,bridge.review_path,Buffer.concat([reviewRaw,Buffer.from(' ')])),false);assert.equal(isPreservedImplementationBridge('production/new-bridge.json',raw,bridge.review_path,reviewRaw),false);}
});

test('frozen historical bridge still verifies descriptor, reviewer, snapshots and members, not current code',async()=>{
 const {resolveImplementationCompatibility}=await import('./typed-production-release.mjs');
 const root=await mkdtemp(resolve(tmpdir(),'historical-content-'));
 try{
  const registryPath='production/production-releases-r002.json',registry=JSON.parse(await readFile(resolve(source,registryPath))),entry=registry.descriptors[0];
  const copy=async path=>{const b=await readFile(resolve(source,path));await mkdir(dirname(resolve(root,path)),{recursive:true});await writeFile(resolve(root,path),b);return b;};
  await copy('assets/manifest.json');await copy(registryPath);
  // Registry membership verifies every descriptor and bridge, without loading all models.
  for(const p of registry.descriptors){await copy(p.path);if(p.compatibility)await copy(p.compatibility.path);}
  const raw=await readFile(resolve(root,entry.path)),descriptor=JSON.parse(raw),bridge=JSON.parse(await readFile(resolve(root,entry.compatibility.path)));
  const paths=[bridge.original_review.path,bridge.previous_manifest.path,bridge.review_path,...bridge.original_implementation.map(r=>r.preserved.path),...bridge.preserved_records.map(r=>r.path),...descriptor.assets.flatMap(i=>[i.metadata.path,i.evidence.path])];
  for(const path of new Set(paths))await copy(path);
  // No current site implementation is copied. A current-code edit is not model evidence.
  const run=()=>resolveImplementationCompatibility(root,entry.path,descriptor,raw,registryPath);
  assert.equal((await run()).length,descriptor.implementation.length);
  for(const path of [bridge.original_review.path,bridge.original_implementation[0].preserved.path,descriptor.assets[0].metadata.path,descriptor.assets[0].evidence.path,bridge.review_path]){
   const original=await readFile(resolve(root,path));await writeFile(resolve(root,path),Buffer.concat([original,Buffer.from(' ')]));await assert.rejects(run,undefined,`historical evidence tampering must fail: ${path}`);await writeFile(resolve(root,path),original);
  }
  // A self-consistent new bridge cannot inherit the frozen exception, even
  // when all current implementation pins and the claimed review are recomputed.
  for(const pin of bridge.current_implementation){const bytes=await copy(pin.path);pin.bytes=bytes.length;pin.sha256=sha256(bytes);}
  const bridgeBytes=encode(bridge),review=JSON.parse(await readFile(resolve(root,bridge.review_path)));
  review.bridge_sha256=sha256(bridgeBytes);review.current_implementation_sha256=sha256(encode(bridge.current_implementation));
  entry.compatibility.bytes=bridgeBytes.length;entry.compatibility.sha256=sha256(bridgeBytes);
  await writeFile(resolve(root,entry.compatibility.path),bridgeBytes);await writeFile(resolve(root,bridge.review_path),encode(review));await writeFile(resolve(root,registryPath),encode(registry));
  await assert.rejects(run,/Unknown or modified implementation bridge/);
  entry.compatibility.path='production/untrusted-bridge.json';await writeFile(resolve(root,entry.compatibility.path),bridgeBytes);await writeFile(resolve(root,registryPath),encode(registry));
  await assert.rejects(run,/Unknown or modified implementation bridge/);
 }finally{await rm(root,{recursive:true,force:true});}
});

test('known runtime FAIL is preserved, never promoted by production acceptance',async()=>{const f=await setup();try{await changedRecord(f,r=>r.postReleaseVerified.status='FAIL');const result=await run(f);assert.equal(result.postReleaseVerified,'FAIL');assert.equal(result.publication_authorized,false);await assert.rejects(()=>collectProductionRelease(f.root,f.path),/Known post-release failure needs resolution/);}finally{await f.cleanup();}});

test('new content route integrates and cannot overwrite an existing ID',async()=>{const f=await setup();try{const accepted=await collectProductionRelease(f.root,f.path);assert.equal(accepted.length,1);await assert.rejects(()=>appendProductionRelease(f.root,{assets:[accepted[0]]},f.path),/duplicate or replace/);}finally{await f.cleanup();}});

test('content acceptance flows through closure, owned media and ZIP delivery',async()=>{
 const f=await setup();try{
  const results=new Map(),manifest=await appendProductionRelease(f.root,{assets:[]},f.path,results);
  const closure=await productionSourceClosure(f.root,manifest);for(const pin of f.descriptor.licenses)assert(closure.includes(pin.path));assert(!closure.includes('site/production-release.mjs'));
  const out=resolve(f.root,'dist');const delivered=await deliverTurntables(await deliverManifestAssets(manifest,out,{root:f.root}),out,{root:f.root,productionResults:results});
  assert.equal(delivered.assets.length,1);for(const key of ['glb','blend','preview'])assert.equal(sha256(await readFile(resolve(out,delivered.assets[0][key]))),f.asset.sha256[key]);
  const gallery=await productionGalleryResources(f.root,manifest,{posters:{},files:[]},results);assert.equal(gallery.files.length,2);
  const zip=spawnSync('python3',['-c',"import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); assert z.testzip() is None; assert len(z.namelist())==3; assert 'CREDITS.txt' in z.namelist()",resolve(out,delivered.assets[0].downloads.bundle)],{encoding:'utf8'});assert.equal(zip.status,0,zip.stderr);
 }finally{await f.cleanup();}
});

const esrf='https://www.esrf.fr/home/news/general/content-news/general/esrf-scans-most-complete-heterodontosaurus-skeleton-ever-found.html';
for(const value of ['Coverage: 100%.','https://commons.wikimedia.org/wiki/File:Eurhinosaurus_and_Stenopterygius_NHM.jpg',esrf,`Source: ${esrf}`,`Source: ${esrf}.`, `Sources: ${esrf},https://example.org/home/paper; see text.`,{citation:esrf},'https://example.org/home/paper?section=science#results'])test('accept public HTTPS source '+JSON.stringify(value),()=>assert.doesNotThrow(()=>publicMaterial(value)));
for(const value of [
 '/home/user/source.json','/tmp/source.json','/workspace/model.glb','/root/private','file:///opt/private',
 `${esrf} and /home/user/private.json`,`${esrf}?path=/home/user/source`,`${esrf}?path=%2Ftmp%2Fprivate`,
 `${esrf}#file:///secret`,`${esrf}?access_token=private`,`${esrf}?api%5Fkey=private`,`${esrf}?password=private`,`${esrf}?token=private`,`${esrf}?X-Amz-Credential=private`,`${esrf}?sig=private`,
 'https://user:password@example.org/home/paper','https://user@example.org/home/paper',
 'https://drive.google.com/file/d/private','https://docs.google.com/document/private','https://DRIVE.GOOGLE.COM/private',
 'https://localhost/home/file','https://127.0.0.1/home/file','https://10.0.0.1/home/file','https://192.168.0.1/home/file','https://[::1]/home/file',
 'https://example.org/home/ghp_12345678901234567890','https://example.org/home/%67hp_12345678901234567890',
 'https://example.org/home/paper?next=https://drive.google.com/private','https://example.org/home/paper?next=file:///opt/private',
 'https://example.org/home/paper?ok=1;path=%2Fhome%2Fuser',
 'https://example.org/home/paper?ok=1;%74oken=private',
 'https://example.org/home/paper,%67hp_12345678901234567890',
 'https://foo.internal../home/private',
 'https://server/home/private','https://foo.internal./home/private','https://foo.local./home/private',
 'https://example.org/home/paper,https://user:pass@localhost/home/private',
 'https://example.org/home/paper#token=private','https://example.org/home/paper#%74oken=private',
 'https://example.org/home/%2567hp_12345678901234567890','https://example.org/home/paper?path=%252Fhome%252Fuser',
 'https://example.org/home/paper;file:///opt/private',
 'https://','https://example.org/%ZZ','-----BEGIN PRIVATE KEY-----'
])test('reject private source '+value,()=>assert.throws(()=>publicMaterial(value)));
