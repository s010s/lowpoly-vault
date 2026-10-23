// SPDX-License-Identifier: MIT
// Pinned official validator and Three.js GLTFLoader; parsing is not GPU rendering.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const [modelDir,dependencyRoot]=process.argv.slice(2);
if(!modelDir||!dependencyRoot)throw new Error('Usage: check_runtime.mjs MODEL_DIR NODE_MODULES');
const require=createRequire(pathToFileURL(path.resolve(dependencyRoot,'_runtime-entry.cjs')));
const validator=require('gltf-validator');
const THREE=await import(pathToFileURL(path.resolve(dependencyRoot,'three/build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.resolve(dependencyRoot,'three/examples/jsm/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(path.join(modelDir,'model.glb'));
const sha256=crypto.createHash('sha256').update(bytes).digest('hex');
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw new Error('External resource forbidden: '+uri)}});
const output=path.join(modelDir,'qa/evidence');
fs.mkdirSync(output,{recursive:true});
fs.writeFileSync(path.join(output,'khronos.json'),JSON.stringify({status:report.issues.numErrors?'FAIL':'PASS',glb_sha256:sha256,validator_version:validator.version(),report},null,2)+'\n');
if(report.issues.numErrors||report.issues.truncated)throw new Error('Khronos errors or truncated report');
const buf=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const gltf=await new Promise((resolve,reject)=>new GLTFLoader().parse(buf,'',resolve,reject));
gltf.scene.updateMatrixWorld(true);
let meshes=0,primitives=0,triangles=0,materials=new Set();
gltf.scene.traverse(o=>{if(o.isMesh){meshes++;primitives+=Math.max(1,o.geometry.groups.length);triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material]){materials.add(m.uuid);if(m.side!==THREE.FrontSide)throw new Error('Unexpected double-sided material')}}});
const box=new THREE.Box3().setFromObject(gltf.scene);
const result={status:'PASS',claim_scope:'Actual GLTFLoader parse and CPU scene bounds only; no WebGL, GPU, combined scene or performance claim.',glb_sha256:sha256,three_revision:THREE.REVISION,three_package_version:JSON.parse(fs.readFileSync(path.resolve(dependencyRoot,'three/package.json'),'utf8')).version,meshes,primitives,triangles,materials:materials.size,bounds_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new THREE.Vector3()).toArray()},gpu:'UNKNOWN',scene:'UNKNOWN'};
fs.writeFileSync(path.join(output,'threejs-parse.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({khronos_errors:report.issues.numErrors,khronos_warnings:report.issues.numWarnings,threejs_parse:'PASS',triangles,primitives,sha256}));
