// SPDX-License-Identifier: MIT
// CPU parsing and official format validation are not GPU rendering evidence.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const [file,runtimeRoot,out]=process.argv.slice(2);
const bytes=fs.readFileSync(file);
const hash=crypto.createHash('sha256').update(bytes).digest('hex');
const runtime=path.resolve(runtimeRoot);
const three=await import(pathToFileURL(path.join(runtime,'three/build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.join(runtime,'three/examples/jsm/loaders/GLTFLoader.js')));
const validator=await import(pathToFileURL(path.join(runtime,'gltf-validator/module.mjs')));
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:1000,externalResourceFunction:async()=>{throw new Error('External resource not allowed');}});
fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'khronos.json'),JSON.stringify({status:report.issues.numErrors===0?'PASS':'FAIL',glb_sha256:hash,validator_version:validator.version(),report},null,2)+'\n');
const data=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const gltf=await new Promise((resolve,reject)=>new GLTFLoader().parse(data,'',resolve,reject));
gltf.scene.updateMatrixWorld(true);
let triangles=0,meshes=0,materials=new Set(),nonfinite=0;
gltf.scene.traverse(o=>{if(o.isMesh){meshes++;const g=o.geometry;triangles+=(g.index?g.index.count:g.attributes.position.count)/3;for(const x of g.attributes.position.array)if(!Number.isFinite(x))nonfinite++;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid);}});
const bb=new three.Box3().setFromObject(gltf.scene);
const result={status:nonfinite===0?'PASS':'FAIL',claim_scope:'PINNED_THREE_GLTFLOADER_CPU_PARSE_ONLY',glb_sha256:hash,three_revision:three.REVISION,three_version:JSON.parse(fs.readFileSync(path.join(runtime,'three/package.json'))).version,meshes,triangles,materials:materials.size,nonfinite,bounds_gltf_m:{min:bb.min.toArray(),max:bb.max.toArray(),size:bb.getSize(new three.Vector3()).toArray()},gpu:'UNKNOWN',scene:'UNKNOWN'};
fs.writeFileSync(path.join(out,'three-parse.json'),JSON.stringify(result,null,2)+'\n');
if(report.issues.numErrors||nonfinite)process.exitCode=1;
console.log(JSON.stringify({errors:report.issues.numErrors,warnings:report.issues.numWarnings,triangles,meshes,sha256:hash}));
