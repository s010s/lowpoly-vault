// SPDX-License-Identifier: MIT
// External pinned verification runtimes are passed as one module directory.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {pathToFileURL} from 'node:url';import {createRequire} from 'node:module';
const [glbFile,out,moduleDir]=process.argv.slice(2);const require=createRequire(path.join(path.resolve(moduleDir),'runtime.cjs'));
const validator=require('gltf-validator');const THREE=await import(pathToFileURL(path.join(path.resolve(moduleDir),'three/build/three.module.js')));const {GLTFLoader}=await import(pathToFileURL(path.join(path.resolve(moduleDir),'three/examples/jsm/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(glbFile);const sha=crypto.createHash('sha256').update(bytes).digest('hex');
const validation=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async()=>{throw Error('External dependency denied');}});
fs.writeFileSync(path.join(out,'khronos.json'),JSON.stringify({status:validation.issues.numErrors?'FAIL':'PASS',glb_sha256:sha,validator_version:validator.version(),report:validation},null,2)+'\n');
if(validation.issues.numErrors)throw Error('Khronos errors');
const scene=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');scene.scene.updateMatrixWorld(true);
let triangles=0,meshes=0;const materials=new Set();const paws=[];
scene.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid);}if(o.name.startsWith('four_toes_'))paws.push(o.name);});
const box=new THREE.Box3().setFromObject(scene.scene);const audit=JSON.parse(fs.readFileSync(path.join(out,'glb-audit.json')));const actual={min:box.min.toArray(),max:box.max.toArray()};const deviation=Math.max(...['min','max'].flatMap(k=>actual[k].map((v,i)=>Math.abs(v-audit.bounds_m[k][i]))));
if(triangles!==audit.scene_triangles||deviation>1e-5||paws.length!==4)throw Error('CPU scene geometry mismatch');
fs.writeFileSync(path.join(out,'three-parse.json'),JSON.stringify({status:'PASS',claim_scope:'CPU_GLTFLOADER_PARSE_AND_SCENE_GEOMETRY_ONLY',glb_sha256:sha,three_version:THREE.REVISION,triangles,meshes,materials:materials.size,bounds_gltf_m:actual,bounds_deviation_m:deviation,four_toe_paw_nodes:paws,gpu:'UNKNOWN',scene_performance:'UNKNOWN',notes:'No WebGL/browser rendering was performed. Primitive count is not measured draw calls.'},null,2)+'\n');
console.log(JSON.stringify({khronos_errors:validation.issues.numErrors,khronos_warnings:validation.issues.numWarnings,three_version:THREE.REVISION,triangles,meshes,materials:materials.size}));
