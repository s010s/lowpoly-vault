// SPDX-License-Identifier: MIT
// Node parse-only QA. THREE_ROOT names a local npm three package; no browser/GPU claim.
import fs from 'node:fs';import crypto from 'node:crypto';import path from 'node:path';import {pathToFileURL} from 'node:url';
const [input,output]=process.argv.slice(2);const base=process.env.THREE_ROOT;
if(!base)throw Error('Set THREE_ROOT to the installed three 0.180.0 package directory.');
const pkg=JSON.parse(fs.readFileSync(path.join(base,'package.json'),'utf8'));
if(pkg.version!=='0.180.0')throw Error('Pinned Three.js 0.180.0 required');
const THREE=await import(pathToFileURL(path.join(base,'build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.join(base,'examples/jsm/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(input);const ab=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const gltf=await new GLTFLoader().parseAsync(ab,'');gltf.scene.updateMatrixWorld(true);
let primitives=0,triangles=0,materials=new Set(),meshNodes=[];
gltf.scene.traverse(o=>{if(o.isMesh){primitives++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;for(const m of(Array.isArray(o.material)?o.material:[o.material]))materials.add(m.uuid);meshNodes.push(o.name);}});
const bbox=new THREE.Box3().setFromObject(gltf.scene);
const report={status:'PASS_PARSE_ONLY',glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),three_version:pkg.version,loader:'GLTFLoader',primitives,triangles,materials:materials.size,bounds_glTF_m:{min:bbox.min.toArray(),max:bbox.max.toArray(),size:bbox.getSize(new THREE.Vector3()).toArray()},mesh_nodes:meshNodes,gpu:'NOT_RUN',populated_scene:'NOT_RUN',claim:'Actual delivered GLB successfully loaded by pinned GLTFLoader. No GPU, screenshot, draw-call, frame-rate or populated-scene assertion.'};fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
