// SPDX-License-Identifier: MIT
// Pinned Three.js geometry parsing only. This does not create a GPU renderer.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const [glbPath,threeRoot,output]=process.argv.slice(2);
if(!glbPath||!threeRoot||!output)throw Error('Usage: node check_parser.mjs GLB THREE_PACKAGE_DIRECTORY REPORT');
const pkg=JSON.parse(fs.readFileSync(path.join(threeRoot,'package.json'),'utf8'));
if(pkg.name!=='three'||pkg.version!=='0.180.0')throw Error('Requires pinned three 0.180.0');
const {GLTFLoader}=await import(pathToFileURL(path.join(threeRoot,'examples/jsm/loaders/GLTFLoader.js')));
const {Box3,Vector3}=await import(pathToFileURL(path.join(threeRoot,'build/three.module.js')));
const b=fs.readFileSync(glbPath),gltf=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
gltf.scene.updateMatrixWorld(true);
let triangles=0,meshes=0;
gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
const bounds=new Box3().setFromObject(gltf.scene);
fs.writeFileSync(output,JSON.stringify({status:'PASS',claim_scope:'Node GLTFLoader exact GLB geometry parsing only; no browser or GPU rendering',three_version:pkg.version,node_version:process.version,glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),triangles,meshes,bounds_m:{min:bounds.min.toArray(),max:bounds.max.toArray(),size:bounds.getSize(new Vector3()).toArray()},gpu:'NOT_RUN',populated_scene:'NOT_RUN'},null,2)+'\n');
console.log('Three.js parser PASS:',triangles,'triangles,',meshes,'meshes');
