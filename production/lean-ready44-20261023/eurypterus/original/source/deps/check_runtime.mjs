// SPDX-License-Identifier: MIT
// Read-only Khronos validation and pinned Three.js CPU parsing, not GPU evidence.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const [glb, moduleRoot, output] = process.argv.slice(2);
if (!glb || !moduleRoot || !output) throw Error('Usage: node check_runtime.mjs GLB NODE_MODULES OUTPUT');
const require=createRequire(path.join(path.resolve(moduleRoot),'runtime-entry.cjs'));
const validator=require('gltf-validator');
const THREE=await import(pathToFileURL(path.resolve(moduleRoot,'three/build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.resolve(moduleRoot,'three/examples/jsm/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(glb), sha=crypto.createHash('sha256').update(bytes).digest('hex');
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async()=>{throw Error('External dependencies forbidden');}});
fs.mkdirSync(output,{recursive:true});
fs.writeFileSync(path.join(output,'khronos.json'),JSON.stringify({status:report.issues.numErrors?'FAIL':'PASS',glb_sha256:sha,validator_version:validator.version(),report},null,2)+'\n');
if(report.issues.numErrors||report.issues.numWarnings||report.issues.truncated) throw Error('Khronos errors/warnings require review');
const loader=new GLTFLoader();const ab=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const loaded=await new Promise((resolve,reject)=>loader.parse(ab,'',resolve,reject));
loaded.scene.updateMatrixWorld(true);let meshes=0,triangles=0,materials=new Set();
loaded.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;(Array.isArray(o.material)?o.material:[o.material]).forEach(x=>materials.add(x));if(!o.geometry.attributes.normal)throw Error('Missing normals');}});
const bb=new THREE.Box3().setFromObject(loaded.scene);
fs.writeFileSync(path.join(output,'three-parse.json'),JSON.stringify({status:'PASS',glb_sha256:sha,three_revision:THREE.REVISION,three_package_version:JSON.parse(fs.readFileSync(path.join(moduleRoot,'three/package.json'))).version,meshes,triangles,materials:materials.size,bounds_m:{min:bb.min.toArray(),max:bb.max.toArray()},animations:loaded.animations.length,scope:'Actual exact GLB loaded with Node GLTFLoader. No browser, WebGL/GPU frame, populated scene or user acceptance asserted.',gpu:'UNKNOWN',scene:'UNKNOWN'},null,2)+'\n');
console.log(JSON.stringify({glb_sha256:sha,khronos_errors:report.issues.numErrors,khronos_warnings:report.issues.numWarnings,three_revision:THREE.REVISION,meshes,triangles}));
