import {assetURL} from './geometry-fixtures.mjs';
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import * as T from 'three';
import {MEASURED_SUPPORTS,measuredSupport} from '../model-support.js';
const {fixture,compare,sample,step,models}=await import('./compare-ground-drift-audit.mjs');
const close=(a,b,m,eps=1e-7)=>assert(Math.abs(a-b)<eps,`${m}: ${a} vs ${b}`);
const point=new T.Vector3(),checks=[],rows=[];
const release=r=>{r.controls.dispose();r.viewMotion.cancelAll();r.removeReference();};
for(const asset of models){
 const r=fixture(asset),v=r.detail,center=v.entry.box.getCenter(new T.Vector3());
 assert.equal(!!v.supportRule,asset.id==='confuciusornis');
 // The split pivots cancel exactly in ordinary mode: no poster/canonical pose shift.
 v.model.updateMatrixWorld(true);const actual=new T.Box3().setFromObject(v.model,true);
 const expected=v.entry.box.clone().translate(new T.Vector3(-center.x,-v.entry.box.min.y,-center.z));expected.min.multiplyScalar(v.scale);expected.max.multiplyScalar(v.scale);
 close(actual.min.distanceTo(expected.min),0,asset.id+' ordinary min');close(actual.max.distanceTo(expected.max),0,asset.id+' ordinary max');
 close(v.contact.position.x,0,asset.id+' ordinary shadow X');close(v.contact.position.z,0,asset.id+' ordinary shadow Z');
 const c=compare(r),initial=sample(r),support=v.comparisonYaw.localToWorld(new T.Vector3()),reference=c.root.position.clone();
 const groundDepth=p=>p.clone().applyMatrix4(v.camera.matrixWorldInverse).z;
 close(v.contact.position.x,support.x,asset.id+' comparison shadow X');close(v.contact.position.z,support.z,asset.id+' comparison shadow Z');
 close(groundDepth(support),groundDepth(reference),asset.id+' ground support depth');
 close(support.clone().project(v.camera).y,reference.clone().project(v.camera).y,asset.id+' ground screen line');
 for(let angle=0;angle<360;angle+=10){r.rotate(10,0);r.zoom(angle%20?.8:1.25);v.model.updateMatrixWorld(true);const current=v.comparisonYaw.localToWorld(new T.Vector3());close(current.distanceTo(support),0,asset.id+' fixed yaw support');close(sample(r).modelMinY,0,asset.id+' grounded');close(current.clone().project(v.camera).y,reference.clone().project(v.camera).y,asset.id+' shared zoom ground');}
 rows.push({id:asset.id,supportMode:v.supportRule?'source-verified paired feet':'unchanged box-centered origin',supportAuthoredMeters:v.supportRule?.point??null,supportWorld:support.toArray(),referenceWorld:reference.toArray(),sourceSha256:v.entry.sha256,scale:v.scale,referenceScale:c.root.scale.x});release(r);
}
checks.push('All published GLBs: unchanged ordinary authored geometry, equal support/wrist ground depth, 36 yaw/zoom steps per model with stable support and common scalar');
const asset=models.find(a=>a.id==='confuciusornis'),r=fixture(asset),entry=r.detail.entry;
assert(measuredSupport(asset,entry));
for(const changed of [{...entry,sha256:null},{...entry,sha256:'bad'},{...entry,box:entry.box.clone().translate(new T.Vector3(.01,0,0))}])assert.equal(measuredSupport(asset,changed),null);
assert.equal(measuredSupport({...asset,sha256:{glb:'new-source'}},entry),null);
assert.equal(measuredSupport({...asset,id:'unreviewed-bird'},entry),null);
const bytes=await readFile(assetURL(asset.glb));assert.equal(createHash('sha256').update(bytes).digest('hex'),MEASURED_SUPPORTS.confuciusornis.sha256);
checks.push('Source binding rejects missing/mismatched fetched digest, catalog digest, id or geometry bounds; all other published assets keep existing origin');
release(r);
for(const angle of [-173,-90,63,179])for(const ms of [0,100,350,699]){
 const a=fixture(asset);compare(a);a.rotate(angle,0);a.reset();step(ms);a.detail.model.updateMatrixWorld(true);
 const before=[];a.detail.model.traverse(o=>{if(o.isMesh)before.push(o.matrixWorld.clone());});
 const contactBefore=a.detail.contact.position.clone();a.cancelCamera();close(a.detail.contact.position.distanceTo(contactBefore),0,'contact does not follow representation rebase');a.detail.model.updateMatrixWorld(true);let i=0;a.detail.model.traverse(o=>{if(o.isMesh){o.matrixWorld.elements.forEach((v,j)=>close(v,before[i].elements[j],'interrupted pivot fold'));i++;}});
 const snap=sample(a);step(.001);assert(a.detail.contact.position.distanceTo(contactBefore)<1e-5,'contact does not jump next frame');assert(a.detail.model.position.distanceTo(new T.Vector3().fromArray(snap.modelPosition))<1e-5,'no old-layout jump after pivot fold');step(900);close(a.detail.model.position.x,0,'layout finishes at single X');close(a.detail.model.position.z,0,'layout finishes at single Z');
 close(a.detail.contact.position.x,0,'ordinary contact X restored');close(a.detail.contact.position.z,0,'ordinary contact Z restored');a.rotate(25,10);close(sample(a).modelMinY,0,'ordinary pitch after support fold');release(a);
}
checks.push('16 partial Reset interruptions preserve every mesh world-matrix while folding foot-centered yaw into ordinary inspection; remaining layout finishes smoothly without an old-pivot position jump');
const source=await readFile(new URL('../renderer.js',import.meta.url),'utf8');assert(source.includes("crypto.subtle.digest('SHA-256',bytes)"));assert(source.includes('measuredSupport(asset,entry)'));checks.push('Production fetch computes reviewed-source SHA256 before selecting measured support');
const out={status:'passed',browserVerified:false,scope:'Production renderer, real GLB bounds/matrices and OrbitControls event harness; geometry-only texture placeholders; browser parser remains authoritative for texture decoding; no raster/browser claim',checks,rows};await mkdir(new URL('./evidence/reference-v55/',import.meta.url),{recursive:true});await writeFile(new URL('./evidence/reference-v55/support-regression.json',import.meta.url),JSON.stringify(out,null,2));console.log(JSON.stringify({status:out.status,checks,models:rows.length},null,2));
