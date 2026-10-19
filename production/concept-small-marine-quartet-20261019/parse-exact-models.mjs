// SPDX-License-Identifier: MIT
// Same Node GLTFLoader geometry path used by site/parse-models.mjs.
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
import {createHash} from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from 'three';
const revision=process.argv[2]||'r001';
const root=dirname(fileURLToPath(import.meta.url)),results=[];
const selected=process.argv.slice(3);
for(const id of selected.length?selected:['emeraldella','burgessia','tuzoia','sanctacaris']){
 const dir=join(root,id,revision),bytes=await readFile(join(dir,id+'.glb'));
 const metadata=JSON.parse(await readFile(join(dir,'metadata.json')));
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 gltf.scene.updateMatrixWorld(true);let triangles=0,meshes=0;const mats=new Set();
 gltf.scene.traverse(o=>{if(!o.isMesh)return;meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid);});
 const dimensions=new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray();
 const delta=Math.max(...dimensions.map((v,i)=>Math.abs(v-metadata.dimensions[i])));
 const report={asset_id:id,created_at:new Date().toISOString(),status:triangles===metadata.triangles&&delta<.0001?'pass':'fail',scope:'Node GLTFLoader geometry parse only',three_revision:REVISION,glb_sha256:createHash('sha256').update(bytes).digest('hex'),triangles,meshes,materials:mats.size,dimensions_m:dimensions,bounds_max_delta_m:delta,gpu_render:'not_run',populated_scene:'not_run'};
 await writeFile(join(dir,'threejs-parse.report.json'),JSON.stringify(report,null,2)+'\n');results.push(report);
 gltf.scene.traverse(o=>{o.geometry?.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});
 console.log(id,report.status,triangles,dimensions);
}
if(results.some(r=>r.status!=='pass'))process.exitCode=1;
