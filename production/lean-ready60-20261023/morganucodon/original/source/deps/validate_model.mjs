// SPDX-License-Identifier: MIT
// CPU format and geometry parsing only. This is not a WebGL/GPU render test.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import crypto from 'node:crypto';
const [glbPath, moduleRoot, outputDir] = process.argv.slice(2);
const root=path.resolve(moduleRoot), bytes=fs.readFileSync(glbPath);
const sha=crypto.createHash('sha256').update(bytes).digest('hex');
const req=createRequire(path.join(root,'package.json'));
const validator=req('gltf-validator');
const validation=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',externalResourceFunction:()=>Promise.reject(new Error('External resources forbidden'))});
fs.writeFileSync(path.join(outputDir,'khronos.json'),JSON.stringify({status:validation.issues.numErrors===0?'PASS':'FAIL',source_glb_sha256:sha,validator_version:validator.version(),report:validation},null,2)+'\n');
const {GLTFLoader}=await import(pathToFileURL(path.join(root,'three/examples/jsm/loaders/GLTFLoader.js')));
const {Box3,Vector3,REVISION}=await import(pathToFileURL(path.join(root,'three/build/three.module.js')));
const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
gltf.scene.updateMatrixWorld(true);let meshes=0,triangles=0;const mats=new Set();
gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid);}});
const box=new Box3().setFromObject(gltf.scene),dims=box.getSize(new Vector3()).toArray();
const tech=JSON.parse(fs.readFileSync(path.join(outputDir,'technical.json'),'utf8'));
const delta=Math.max(...dims.map((v,i)=>Math.abs(v-tech.glb.bounds_m.size[i])));
if(delta>.0001||triangles!==tech.glb.scene_triangles)throw new Error('Three.js geometry mismatches static audit');
fs.writeFileSync(path.join(outputDir,'three-parse.json'),JSON.stringify({status:'PASS',scope:'Node GLTFLoader CPU geometry parsing only; no GPU context, shader evaluation, browser image or populated-scene performance was tested.',source_glb_sha256:sha,three_version:'0.'+REVISION+'.0',meshes,materials:mats.size,triangles,bounds_m:{min:box.min.toArray(),max:box.max.toArray(),size:dims},bounds_max_delta_m:delta,gpu:'UNKNOWN',scene:'UNKNOWN'},null,2)+'\n');
if(validation.issues.numErrors||validation.issues.numWarnings)throw new Error('Khronos errors or warnings require review');
console.log(JSON.stringify({status:'PASS',glb_sha256:sha,triangles,meshes,khronos_errors:validation.issues.numErrors,khronos_warnings:validation.issues.numWarnings}));
