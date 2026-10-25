// SPDX-License-Identifier: MIT
// Scoped CPU parse plus official format validator. No GPU or scene-performance claim.
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { createRequire } from 'node:module';
const runtime=process.env.QA_NODE_ROOT||new URL('.',import.meta.url).pathname;
const require=createRequire(path.resolve(runtime,'package.json'));
const validator=require('gltf-validator');
const threePath=require.resolve('three');
const base=path.resolve(path.dirname(threePath),'..');
const {GLTFLoader}=await import(path.join(base,'examples/jsm/loaders/GLTFLoader.js'));
const {Box3,Vector3,REVISION}=await import(path.join(base,'build/three.module.js'));
const input=process.argv[2],output=process.argv[3];fs.mkdirSync(output,{recursive:true});
const bytes=fs.readFileSync(input);const sha=crypto.createHash('sha256').update(bytes).digest('hex');
const doc=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString());
if((doc.images||[]).length||(doc.textures||[]).length||(doc.animations||[]).length||(doc.skins||[]).length)throw Error('Outside declared static texture-free scope');
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async()=>{throw Error('External resource forbidden');}});
fs.writeFileSync(path.join(output,'khronos.json'),JSON.stringify({glb_sha256:sha,validator_version:validator.version(),status:report.issues.numErrors?'FAIL':'PASS',report},null,2)+'\n');
if(report.issues.numErrors||report.issues.numWarnings||report.issues.truncated)throw Error('Validator errors/warnings require review');
const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');gltf.scene.updateMatrixWorld(true);
let triangles=0,meshes=0,vertices=0,materials=new Set();gltf.scene.traverse(o=>{if(!o.isMesh)return;meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;vertices+=o.geometry.attributes.position.count;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid);});
const box=new Box3().setFromObject(gltf.scene);
const tech=JSON.parse(fs.readFileSync(path.join(path.dirname(input),'technical.json'),'utf8'));const expected=tech.glb.bounds_m;
const delta=Math.max(...box.min.toArray().map((n,i)=>Math.abs(n-expected.min[i])),...box.max.toArray().map((n,i)=>Math.abs(n-expected.max[i])));
if(delta>2.5e-8||triangles!==tech.glb.scene_triangles)throw Error('CPU parser source/export metrics differ');
fs.writeFileSync(path.join(output,'three-parse.json'),JSON.stringify({glb_sha256:sha,status:'PASS',three_version:'0.180.0',three_revision:REVISION,node_version:process.version,parser:'GLTFLoader Node CPU only',meshes,triangles,position_stream_vertices:vertices,materials:materials.size,bounds_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new Vector3()).toArray()},bounds_delta_m:delta,external_dependencies:0,textures:0,animation:0,gpu:'UNKNOWN',world_scene:'UNKNOWN'},null,2)+'\n');
console.log(JSON.stringify({sha,triangles,meshes,vertices,validator_errors:report.issues.numErrors,validator_warnings:report.issues.numWarnings,bounds_delta_m:delta}));
