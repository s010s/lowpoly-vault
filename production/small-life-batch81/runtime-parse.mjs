// SPDX-License-Identifier: MIT
import fs from 'node:fs';import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';import {Box3,Vector3,REVISION} from 'three';
for(const dir of process.argv.slice(2)){
 const b=fs.readFileSync(dir+'/model.glb');const g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);let triangles=0,meshes=0;g.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
 const report={schema_version:1,kind:'runtime_parse',status:'pass',glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),three_version:'0.180.0',three_revision:REVISION,parser:'Node GLTFLoader.parseAsync',triangles,meshes,bounds_glb_xyz_m:new Box3().setFromObject(g.scene).getSize(new Vector3()).toArray(),errors:[],gpu:'not_run',scene:'not_run',limitations:'Node parser check only; no browser, actual graphics device, or populated scene evidence.'};fs.writeFileSync(dir+'/runtime-parse.report.json',JSON.stringify(report,null,2)+'\n');console.log(dir,triangles);
}
