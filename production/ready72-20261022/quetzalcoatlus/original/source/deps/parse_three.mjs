// SPDX-License-Identifier: MIT
// Geometry parsing only, not WebGL/GPU rendering. node parse_three.mjs GLB NODE_MODULES OUT
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import{pathToFileURL}from'node:url';
const[file,modules,out]=process.argv.slice(2);
const{GLTFLoader}=await import(pathToFileURL(path.resolve(modules,'three/examples/jsm/loaders/GLTFLoader.js')));
const{Box3,Vector3,REVISION}=await import(pathToFileURL(path.resolve(modules,'three/build/three.module.js')));
const b=fs.readFileSync(file),g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);
let triangles=0,meshes=0;g.scene.traverse(o=>{if(o.isMesh){triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;meshes++;}});
const report={status:'PASS',claim_scope:'Node Three.js GLTFLoader parse only. No GPU rendering or populated-scene performance claim.',three_revision:REVISION,three_version:JSON.parse(fs.readFileSync(path.resolve(modules,'three/package.json'))).version,glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),meshes,triangles,bounds_m:new Box3().setFromObject(g.scene).getSize(new Vector3()).toArray(),gpu:'NOT_RUN',populated_scene:'NOT_RUN'};
fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
