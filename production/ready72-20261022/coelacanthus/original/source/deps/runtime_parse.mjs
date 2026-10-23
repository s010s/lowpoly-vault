// SPDX-License-Identifier: MIT
// Explicit Node parse check, not a GPU, browser or populated-scene check.
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [model,threeRoot,reportPath]=process.argv.slice(2);
if(!model||!threeRoot||!reportPath) throw Error('Usage: runtime_parse.mjs model.glb three-package-dir report.json');
const {GLTFLoader}=await import(pathToFileURL(path.resolve(threeRoot,'examples/jsm/loaders/GLTFLoader.js')));
const {Box3,Vector3,REVISION}=await import(pathToFileURL(path.resolve(threeRoot,'build/three.module.js')));
const data=fs.readFileSync(model);
const doc=await new Promise((resolve,reject)=>new GLTFLoader().parse(data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength),'',resolve,reject));
doc.scene.updateMatrixWorld(true);
const box=new Box3().setFromObject(doc.scene);let meshes=0,triangles=0;const materials=new Set();
doc.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;if(!o.geometry.attributes.normal)throw Error('Missing normal');for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid);}});
const report={status:'PASS',scope:'Node GLTFLoader parse and scene statistics only; no WebGL rendering',glb_sha256:crypto.createHash('sha256').update(data).digest('hex'),three_version:JSON.parse(fs.readFileSync(path.join(threeRoot,'package.json'))).version,three_revision:REVISION,node_version:process.version,meshes,triangles,materials:materials.size,bounds_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new Vector3()).toArray()},animations:doc.animations.length,gpu:'NOT_RUN',populated_scene:'NOT_RUN'};
fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
