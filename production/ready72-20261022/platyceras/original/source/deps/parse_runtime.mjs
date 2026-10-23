// SPDX-License-Identifier: MIT
// Node GLTFLoader parse and bounds test. Deliberately not a WebGL/GPU test.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const [glb,threePackage,reportFile]=process.argv.slice(2);
const {GLTFLoader}=await import(pathToFileURL(path.join(threePackage,'examples/jsm/loaders/GLTFLoader.js')).href);
const {Box3,Vector3,REVISION}=await import(pathToFileURL(path.join(threePackage,'build/three.module.js')).href);
const bytes=fs.readFileSync(glb);
const asset=await new Promise((resolve,reject)=>new GLTFLoader().parse(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'',resolve,reject));
asset.scene.updateMatrixWorld(true); const bounds=new Box3().setFromObject(asset.scene); let triangles=0,meshes=0;
asset.scene.traverse(ob=>{if(ob.isMesh){meshes++; triangles+=(ob.geometry.index?.count ?? ob.geometry.attributes.position.count)/3;
  if(!ob.geometry.attributes.normal)throw Error('Missing normals');}});
const report={status:'pass',scope:'Node GLTFLoader parse only, not GPU rendering or museum-scene performance',
  glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),three_version:JSON.parse(fs.readFileSync(path.join(threePackage,'package.json'))).version,
  three_revision:REVISION,node_version:process.version,meshes,triangles,bounds_m:{min:bounds.min.toArray(),max:bounds.max.toArray(),size:bounds.getSize(new Vector3()).toArray()},
  animations:asset.animations.length,webgl_render:'NOT_RUN',populated_scene:'NOT_RUN'};
fs.writeFileSync(reportFile,JSON.stringify(report,null,2)+'\n'); console.log(JSON.stringify(report));
