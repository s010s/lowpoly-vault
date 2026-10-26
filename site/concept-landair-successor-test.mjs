/** Actual selected Batch53 successor + immutable historical pins; private copies only. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdtempSync,mkdirSync,copyFileSync,rmSync} from 'node:fs';
import {dirname,resolve,join} from 'node:path';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {collectBatches5253Additions} from './concept-landair-release.mjs';
import {successorReader,successorSourceClosure,historicalTurntableView} from './same-id-successors.mjs';
const source=process.cwd(),read=successorReader(source),manifest=JSON.parse(read('assets/manifest.json'));
assert(manifest.publication?.same_id_successors,'This regression requires the actual selected successor release');
const selectionPin=manifest.publication.same_id_successors,selection=JSON.parse(read(selectionPin.path));
const descriptor=manifest.publication.batches52_53_descriptors.find(p=>p.path==='assets/releases/batch53-20261020.json');assert(descriptor);
const paths=new Set(['site/viewer.js','assets/manifest.json','assets/turntables/index.json',...successorSourceClosure({selection,selectionPin,read})]);
function pins(value){if(!value||typeof value!=='object')return;if(value.path&&value.sha256)paths.add(value.path);for(const child of Object.values(value))pins(child);}
const release=JSON.parse(read(descriptor.path));pins(descriptor);pins(release);pins(JSON.parse(read(release.source_bundle.path)));
for(const entry of release.additions){const asset=JSON.parse(read(entry.metadata.path));for(const key of ['glb','blend','preview'])paths.add(asset[key]);pins(JSON.parse(read(entry.candidate.path)));}
const capture=JSON.parse(read(release.capture.index.path));for(const entry of release.additions)paths.add(capture.posters.find(p=>p.id===entry.id).path);
const hash=b=>createHash('sha256').update(b).digest('hex'),snapshot=new Map([...paths].map(path=>[path,hash(read(path))]));
const root=mkdtempSync(join(tmpdir(),'landair-successor-'));let checks=0;
const collect=()=>collectBatches5253Additions(root,descriptor);
async function rejected(path,modify){const full=resolve(root,path),before=readFileSync(full);try{writeFileSync(full,modify(before));await assert.rejects(collect);checks++;}finally{writeFileSync(full,before);}}
try{
 for(const path of paths){mkdirSync(dirname(resolve(root,path)),{recursive:true});copyFileSync(resolve(source,path),resolve(root,path));}
 const before=await collect();assert.equal(before.additions.length,4);checks++;
 const id='welded-ignimbrite-outcrop',indexPath='assets/turntables/index.json';
 for(const key of ['path','source_glb_sha256','sha256','bytes'])await rejected(indexPath,raw=>{const value=JSON.parse(raw),row=value.posters.find(p=>p.id===id);row[key]=key==='bytes'?row[key]+1:row[key]+'tamper';return JSON.stringify(value);});
 await rejected(indexPath,raw=>{const value=JSON.parse(raw);value.posters.push(value.posters.find(p=>p.id===id));return JSON.stringify(value);});
 await rejected('assets/manifest.json',raw=>{const value=JSON.parse(raw);value.assets.find(a=>a.id===id).sha256.glb='0'.repeat(64);return JSON.stringify(value);});
 await rejected(selectionPin.path,raw=>Buffer.concat([raw,Buffer.from(' ')]));
 const original=capture.posters.find(p=>p.id===id);await rejected(original.path,raw=>Buffer.concat([raw,Buffer.from('tamper')]));
 const selected=selection.entries.find(e=>e.id===id),next=JSON.parse(read(selected.next.path));await rejected(next.turntable.poster.path,raw=>Buffer.concat([raw,Buffer.from('tamper')]));
 const manifestPath=resolve(root,'assets/manifest.json'),saved=readFileSync(manifestPath);rmSync(manifestPath);try{await assert.rejects(collect);checks++;}finally{writeFileSync(manifestPath,saved);}
 // The original small fixture needs no successor evidence when its exact frozen
 // card rows are already selected. It still validates original capture bytes.
 writeFileSync(resolve(root,indexPath),JSON.stringify(historicalTurntableView({manifest,turntables:JSON.parse(read(indexPath)),read})));
 rmSync(manifestPath);assert.deepEqual(await collect(),before);checks++;
 console.log(JSON.stringify({status:'PASS',checks,actual_id:id,source_unchanged:true,claim:'Collector authorization and immutable bytes only; not browser or world acceptance'}));
}finally{try{for(const [path,digest] of snapshot)assert.equal(hash(read(path)),digest,'Source mutated: '+path);}finally{rmSync(root,{recursive:true,force:true});}}
