// SPDX-License-Identifier: MIT
// Pinned Three.js parser test only; does not claim WebGL rendering.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import crypto from 'node:crypto';
const [file, threeRoot, out] = process.argv.slice(2);
if (!file || !threeRoot || !out) throw new Error('Usage: file.glb /path/to/three output.json');
const THREE=await import(pathToFileURL(path.join(threeRoot,'build/three.module.js')).href);
const {GLTFLoader}=await import(pathToFileURL(path.join(threeRoot,'examples/jsm/loaders/GLTFLoader.js')).href);
const bytes=fs.readFileSync(file);
const loader=new GLTFLoader();
const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
gltf.scene.updateMatrixWorld(true);
const box=new THREE.Box3().setFromObject(gltf.scene);
let meshes=0, triangles=0; const materials=new Set(); let badNormals=0;
gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;
for (const m of Array.isArray(o.material)?o.material:[o.material]) materials.add(m.uuid);
if(!o.geometry.attributes.normal)badNormals++;}});
const report={status:badNormals?'FAIL':'PASS',claim_scope:'GLTFLoader parsing and bounds only. No GPU render, screenshot, browser context or populated scene performance test.',
three_version:THREE.REVISION,glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),
meshes,triangles,materials:materials.size,bounds_gltf_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new THREE.Vector3()).toArray()},bad_normals:badNormals,gpu:'NOT_RUN',scene:'NOT_RUN'};
fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
