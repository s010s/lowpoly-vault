/** Current actual final GLB Khronos + Three.js parse; no GPU/visual claim. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import validator from 'gltf-validator';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {Box3,Vector3} from 'three';
import {collectFinalDeliveryCandidates} from './final-delivery.mjs';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),results=[];
for(const a of collectFinalDeliveryCandidates(root).candidates){
 const bytes=readFileSync(resolve(root,a.final_paths.glb));
 const k=await validator.validateBytes(new Uint8Array(bytes),{uri:a.final_paths.glb,maxIssues:1000});assert.equal(k.issues.numErrors,0);
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');gltf.scene.updateMatrixWorld(true);
 let triangles=0;gltf.scene.traverse(o=>{if(o.isMesh)triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;});assert.equal(triangles,a.native.triangles);
 const bounds=new Box3().setFromObject(gltf.scene),dims=bounds.getSize(new Vector3()).toArray(),expected=a.native.bounds_m.max.map((x,i)=>x-a.native.bounds_m.min[i]);
 assert(dims.every((x,i)=>Math.abs(x-expected[i])<=0.0001));
 results.push({id:a.id,khronos_errors:k.issues.numErrors,khronos_warnings:k.issues.numWarnings,threejs_parse:'PASS',triangles,dimensions:dims,gpu:'UNKNOWN',visual:'NOT_PERFORMED'});
 gltf.scene.traverse(o=>{o.geometry?.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});
}
console.log(JSON.stringify({results}));
