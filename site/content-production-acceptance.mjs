/** Content-bound acceptance reuses the actual legacy/v2 evidence validators.
 * No code hash, baseline credential, publication grant or runtime promotion. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,sep} from 'node:path';
import {sha256,assertProductionMaterial} from './inventory-type-acceptance.mjs';
import {inspectProductionContent,verifyTypedProjectionReviews} from './typed-production-release.mjs';
export const CONTENT_PRODUCTION_CHECKS=Object.freeze(['independent_source_acceptance','exact_subject_and_source','scientific_scope_and_limits','geometry_and_topology','source_reproducibility','standard_glb_and_decode','final_preview_and_posters','compact_provenance_and_credits']);
const digest=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
const exact=(x,keys)=>assert.deepEqual(Object.keys(x||{}).sort(),keys.slice().sort(),'Unknown/missing content descriptor fields');
function publicMaterial(value){
 assertProductionMaterial(value);
 if(typeof value==='string')assert(!/\/workspace\/|\/home\/|\/tmp\/|\/root\/|(?:drive|docs)\.google\.com|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})/.test(value),'Private locator or credential in public content record');
 else if(value&&typeof value==='object')for(const [key,child] of Object.entries(value)){if(key==='path')safePath(child);publicMaterial(child);}
}
function safePath(path){
 assert(typeof path==='string'&&path&&!/[\\\u0000-\u001f?#%]/.test(path)&&!path.startsWith('/')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..'),'Unsafe content path');
 assert(!/(?:^|\/)(?:\.env(?:\.[^/]*)?|\.ssh|\.aws|credentials(?:\.[^/]*)?|secrets?(?:\.[^/]*)?)(?:\/|$)/i.test(path),'Private file cannot be public content');
}
async function read(root,path){safePath(path);const full=resolve(root,path);assert(full.startsWith(resolve(root)+sep));assert.equal(await realpath(full),full,'Content symlink rejected');return readFile(full);}
async function bytesPin(root,pin){
 assert(pin&&digest(pin.sha256)&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0,'Exact content pin required');
 const raw=await read(root,pin.path);assert.equal(raw.length,pin.bytes,'Content bytes changed');assert.equal(sha256(raw),pin.sha256,'Content hash changed');return raw;
}
async function jsonPin(root,pin){const value=JSON.parse(await bytesPin(root,pin));publicMaterial(value);return value;}
function identity(value){assert(value&&['id','task_id'].every(k=>typeof value[k]==='string'&&value[k].trim()),'Content identity required');}
function independent(reviewer,maker){identity(reviewer);identity(maker);const normalize=x=>x.trim().toLowerCase().replace(/^\/root\//,'');for(const key of ['id','task_id'])assert.notEqual(normalize(reviewer[key]),normalize(maker[key]),'Content reviewer must be independent');}
function uniquePins(pins){assert(Array.isArray(pins)&&pins.length,'Source dependency closure required');const seen=new Set();for(const pin of pins){safePath(pin.path);assert(!seen.has(pin.path),'Duplicate source member');seen.add(pin.path);}}
export async function inspectContentProductionRelease(root,descriptorPath,raw){
 const actual=await read(root,descriptorPath);if(raw!==undefined)assert(Buffer.from(raw).equals(actual),'Descriptor bytes differ from actual file');
 const descriptor=JSON.parse(actual);publicMaterial(descriptor);
 exact(descriptor,['schema_version','kind','producer','baseline_commit','assets','review_path','scope_document','licenses','publication_authorized']);
 assert.equal(descriptor.kind,'content-production-release-v1');safePath(descriptor.review_path);
 assert(Array.isArray(descriptor.assets)&&descriptor.assets.length,'Content assets required');
 const ids=new Set(),licensePaths=new Set(['LICENSES/CC-BY-4.0.txt']);
 for(const item of descriptor.assets){
  exact(item,['id','metadata','evidence']);assert(/^[a-z0-9][a-z0-9-]*$/.test(item.id)&&!ids.has(item.id),'Duplicate/invalid content asset ID');ids.add(item.id);
  const asset=await jsonPin(root,item.metadata),record=await jsonPin(root,item.evidence);
  assert.equal(asset.id,item.id,'Metadata member mismatch');assert.equal(record.asset_id,item.id,'Evidence member mismatch');
  uniquePins(record.build_closure);for(const pin of Object.values(record.roles||{}))safePath(pin.path);
  if(asset.credits){licensePaths.add(asset.credits);safePath(asset.credits);assert(asset.credits.startsWith(`assets/additions/${item.id}/`)&&asset.credits.endsWith('/CREDITS.txt'),'Credits must belong to asset');}
 }
 uniquePins(descriptor.licenses);assert.deepEqual(descriptor.licenses.map(p=>p.path).sort(),[...licensePaths].sort(),'Exact license and attribution content required');
 for(const pin of descriptor.licenses){const text=(await bytesPin(root,pin)).toString('utf8');assert(text.trim(),'Empty license/attribution');publicMaterial(text);}
 return inspectProductionContent(root,descriptorPath,actual);
}
export async function verifyContentProjectionReviews(root,result,review){
 assert.equal(result.descriptor.kind,'content-production-release-v1');
 // Read the real on-disk review, not a caller-created PASS object.
 const actual=JSON.parse(await read(root,result.descriptor.review_path));
 if(review!==undefined)assert.deepEqual(review,actual,'Supplied content review differs from actual file');review=actual;publicMaterial(review);
 assert.equal(review.schema_version,1);assert.equal(review.kind,'independent-production-projection-review-v1');assert.equal(review.status,'PASS','Independent content review pending or nonpassing');
 assert.equal(review.reviewed_descriptor_sha256,result.descriptor_sha256,'Stale content review');
 independent(review.reviewer,result.descriptor.producer);for(const record of result.records)independent(review.reviewer,record.maker);
 assert.deepEqual(review.blocking_findings,[],'Unresolved independent content findings');assert.equal(review.publication_authorized,false,'Content review cannot grant publication');
 for(const check of CONTENT_PRODUCTION_CHECKS)assert.equal(review.checks?.[check],'PASS','Missing/nonpassing content review check: '+check);
 assert.deepEqual(review.original_acceptance_sha256?.slice().sort(),[...new Set(result.records.map(r=>r.original_acceptance.sha256))].sort(),'Missing original acceptance binding');
 assert(Array.isArray(review.inventory_compatibility)&&new Set(review.inventory_compatibility.map(r=>r.asset_id)).size===result.assets.length&&review.inventory_compatibility.length===result.assets.length,'Duplicate/missing independent content member');
 await verifyTypedProjectionReviews(root,{...result,descriptor:{...result.descriptor,kind:'typed-production-release-v1'}},review);
 return review;
}
