// SPDX-License-Identifier: MIT
// Node GLTFLoader parse only. This is not GPU or populated-scene validation.
import fs from 'node:fs'; import crypto from 'node:crypto'; import path from 'node:path'; import {pathToFileURL} from 'node:url';
const [glb,moduleRoot,reportPath]=process.argv.slice(2);
const {GLTFLoader}=await import(pathToFileURL(path.resolve(moduleRoot,'examples/jsm/loaders/GLTFLoader.js')));
const {Box3,Vector3,REVISION}=await import(pathToFileURL(path.resolve(moduleRoot,'build/three.module.js')));
const b=fs.readFileSync(glb);const g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);
let triangles=0,meshes=0,materials=new Set();g.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid);}});
const box=new Box3().setFromObject(g.scene);
const report={schema_version:1,kind:'runtime_parse',status:'PASS',glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),three_version:JSON.parse(fs.readFileSync(path.join(moduleRoot,'package.json'))).version,three_revision:REVISION,parser:'Node GLTFLoader.parseAsync',triangles,meshes,materials:materials.size,bounds_glb_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new Vector3()).toArray()},errors:[],gpu:'UNKNOWN',scene:'UNKNOWN',limitations:'Node parser and decoded scene only; no actual browser, graphics device, or populated scene evidence.'};
fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
