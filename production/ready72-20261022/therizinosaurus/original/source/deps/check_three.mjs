// SPDX-License-Identifier: MIT
// Usage: node check_three.mjs model.glb output.json /path/to/node_modules/three
import fs from 'node:fs';import crypto from 'node:crypto';import {pathToFileURL} from 'node:url';import path from 'node:path';
const [file,out,moduleRoot]=process.argv.slice(2);const root=path.resolve(moduleRoot);
const THREE=await import(pathToFileURL(path.join(root,'build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.join(root,'examples/jsm/loaders/GLTFLoader.js')));
const b=fs.readFileSync(file);const gltf=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');gltf.scene.updateMatrixWorld(true);
let triangles=0,meshes=0;gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3}});const bounds=new THREE.Box3().setFromObject(gltf.scene);const value={status:'PASS',claim_scope:'Three.js GLTFLoader CPU parse and world bounds only; not browser GPU or populated scene',version:THREE.REVISION,glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),meshes,triangles,bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()},gpu:'NOT_RUN',scene:'NOT_RUN'};fs.writeFileSync(out,JSON.stringify(value,null,2)+'\n');console.log(JSON.stringify(value));
