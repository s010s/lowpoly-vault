// SPDX-License-Identifier: MIT
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from 'three';
const base='assets/candidates/continuous-small-life-round19-20261020/batch-54';
const current=JSON.parse(fs.readFileSync('production/continuous-small-life-round19-20261020/work/batch-54/current-revisions.json'));
for(const [id,revision] of Object.entries(current)){
 const d=path.join(base,id,revision),f=path.join(d,id+'.glb'),b=fs.readFileSync(f);let report;
 try{
 const g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);const bb=new Box3().setFromObject(g.scene);let tris=0,vertices=0,meshes=0;const mats=new Set();g.scene.traverse(o=>{if(o.isMesh){meshes++;tris+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;vertices+=o.geometry.attributes.position.count;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid);}});
 report={status:'pass',check:'runtime_parse',asset_id:id,revision,glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),created_at:new Date().toISOString(),loader:'Three.js GLTFLoader',three_revision:REVISION,node:process.version,bounds_glb_xyz_m:{min:bb.min.toArray(),max:bb.max.toArray(),size:bb.getSize(new Vector3()).toArray()},scene_triangles:tris,exported_position_vertices:vertices,meshes,materials:mats.size,limitations:'Actual Node GLTFLoader parse and scene traversal only. No WebGL/GPU render or populated scene acceptance, no physical device or frame-time evidence.'};
 }catch(e){report={status:'fail',error:String(e)};process.exitCode=1;}
 fs.writeFileSync(path.join(d,'runtime-parse.json'),JSON.stringify(report,null,2)+'\n');console.log(id,report.status);
}
