// SPDX-License-Identifier: MIT
// Offline official validation and Three.js parsing. Does not claim GPU rendering.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const [file,output,modules]=process.argv.slice(2);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const bytes=fs.readFileSync(file),hash=sha(bytes);
const require=createRequire(path.join(path.resolve(modules),'runtime-loader.cjs'));
const validator=require('gltf-validator');
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,externalResourceFunction:async()=>{throw Error('External resource rejected');}});
fs.writeFileSync(path.join(output,'khronos.json'),JSON.stringify({glb_sha256:hash,validator_version:validator.version(),status:report.issues.numErrors?'FAIL':'PASS',report},null,2)+'\n');
const THREE=await import(pathToFileURL(path.join(path.resolve(modules),'three/build/three.module.js')));
const loaderPath=path.join(path.resolve(modules),'three/examples/jsm/loaders/GLTFLoader.js');
const {GLTFLoader}=await import(pathToFileURL(loaderPath));
const ab=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const asset=await new Promise((resolve,reject)=>new GLTFLoader().parse(ab,'',resolve,reject));
asset.scene.updateMatrixWorld(true);const box=new THREE.Box3().setFromObject(asset.scene);let triangles=0,meshes=0;const materials=new Set();
asset.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>materials.add(m.uuid));}});
fs.writeFileSync(path.join(output,'three-parse.json'),JSON.stringify({status:'PASS',scope:'GLTFLOADER_PARSE_ONLY_NOT_GPU',glb_sha256:hash,three_version:JSON.parse(fs.readFileSync(path.join(modules,'three/package.json'),'utf8')).version,loader_sha256:sha(fs.readFileSync(loaderPath)),meshes,triangles,materials:materials.size,bounds_gltf_m:{min:box.min.toArray(),max:box.max.toArray()},gpu_rendered:false},null,2)+'\n');
if(report.issues.numErrors)process.exitCode=1;
console.log(JSON.stringify({khronos_errors:report.issues.numErrors,khronos_warnings:report.issues.numWarnings,three_meshes:meshes,triangles,glb_sha256:hash}));
