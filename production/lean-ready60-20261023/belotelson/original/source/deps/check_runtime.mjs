// SPDX-License-Identifier: MIT
// Official format validation and separate CPU Three.js GLTFLoader parsing.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import crypto from 'node:crypto';
const [glbPath,modules,outDir]=process.argv.slice(2);
const raw=fs.readFileSync(glbPath), hash=crypto.createHash('sha256').update(raw).digest('hex');
const validator=(await import(pathToFileURL(path.resolve(modules,'gltf-validator/index.js')).href)).default;
const official=await validator.validateBytes(new Uint8Array(raw),{uri:'model.glb',externalResourceFunction:async()=>{throw new Error('External resource prohibited');}});
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,'khronos.json'),JSON.stringify({glb_sha256:hash,validator_version:validator.version(),report:official},null,2)+'\n');
if(official.issues.numErrors>0)throw new Error('Official format errors');
const THREE=await import(pathToFileURL(path.resolve(modules,'three/build/three.module.js')).href);
const {GLTFLoader}=await import(pathToFileURL(path.resolve(modules,'three/examples/jsm/loaders/GLTFLoader.js')).href);
if(!globalThis.ProgressEvent)globalThis.ProgressEvent=class ProgressEvent{constructor(type,init={}){this.type=type;Object.assign(this,init);}};
const ab=raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength);
const gltf=await new Promise((resolve,reject)=>new GLTFLoader().parse(ab,'',resolve,reject));
gltf.scene.updateMatrixWorld(true);
let meshes=0,triangles=0,materials=new Set(),nonfinite=0,negativeDeterminants=0;
gltf.scene.traverse(o=>{if(o.isMesh){meshes++;const g=o.geometry;triangles+=(g.index?g.index.count:g.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid);if(o.matrixWorld.determinant()<=0)negativeDeterminants++;for(const x of g.attributes.position.array)if(!Number.isFinite(x))nonfinite++;}});
const bounds=new THREE.Box3().setFromObject(gltf.scene);
const report={status:'PASS_CPU_PARSE_ONLY',glb_sha256:hash,three_version:THREE.REVISION,loader:'GLTFLoader',meshes,triangles,materials:materials.size,nonfinite,negativeDeterminants,bounds_m:{min:bounds.min.toArray(),max:bounds.max.toArray(),size:bounds.getSize(new THREE.Vector3()).toArray()},external_resources:false,gpu:'UNKNOWN',scene:'UNKNOWN',claim:'Actual CPU GLTFLoader parse and world-bound inspection only. No WebGL renderer, GPU, draw-call timing or populated-scene assertion.'};
if(nonfinite||negativeDeterminants)throw new Error('Invalid geometry');
fs.writeFileSync(path.join(outDir,'three-parse.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({khronos_errors:official.issues.numErrors,khronos_warnings:official.issues.numWarnings,...report}));
