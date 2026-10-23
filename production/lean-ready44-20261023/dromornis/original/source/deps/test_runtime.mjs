// SPDX-License-Identifier: MIT
// CPU-only Three.js parsing/bounds test. It does NOT create WebGL or prove GPU rendering.
import fs from 'node:fs'; import crypto from 'node:crypto'; import { createRequire } from 'node:module'; import { pathToFileURL } from 'node:url';
const req=createRequire(import.meta.url);
const THREE=await import(pathToFileURL(req.resolve('three')).href);
const {GLTFLoader}=await import(pathToFileURL(req.resolve('three/addons/loaders/GLTFLoader.js')).href);
const bytes=fs.readFileSync(process.argv[2]);const digest=crypto.createHash('sha256').update(bytes).digest('hex');
const loaded=await new Promise((res,rej)=>new GLTFLoader().parse(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'',res,rej));
loaded.scene.updateMatrixWorld(true);const box=new THREE.Box3().setFromObject(loaded.scene);let meshes=0,triangles=0;const mats=new Set();let negative=false;
loaded.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;negative ||= o.matrixWorld.determinant()<=0;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid)}});
const report={status:'PASS',claim_scope:'CPU GLTFLoader parsing and scene bounds only, no GPU or populated scene test',three_version:THREE.REVISION,glb_sha256:digest,mesh_instances:meshes,triangles,materials:mats.size,negative_determinant:negative,bounds_glb_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new THREE.Vector3()).toArray()},gpu:'NOT_RUN',populated_scene:'NOT_RUN'};
if(negative||!meshes||!Number.isFinite(triangles))throw Error('Invalid parsed scene');fs.writeFileSync(process.argv[3],JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
