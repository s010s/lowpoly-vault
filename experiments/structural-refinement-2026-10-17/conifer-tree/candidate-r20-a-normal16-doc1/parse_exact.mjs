// SPDX-License-Identifier: MIT
// Exact static GLB parser check. No browser or GPU claim.
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';
const dir=path.dirname(fileURLToPath(import.meta.url));
const deps=process.argv[2];if(!deps)throw new Error('Pass an existing node_modules directory; nothing is installed.');
const threeRoot=path.join(deps,'three');
const version=JSON.parse(await readFile(path.join(threeRoot,'package.json'))).version;
if(version!=='0.180.0')throw new Error(`Unexpected Three.js ${version}`);
const {GLTFLoader}=await import(pathToFileURL(path.join(threeRoot,'examples/jsm/loaders/GLTFLoader.js')));
const {Box3}=await import(pathToFileURL(path.join(threeRoot,'build/three.module.js')));
const data=await readFile(path.join(dir,'conifer-tree.glb'));
const sha256=createHash('sha256').update(data).digest('hex');
const scene=(await new GLTFLoader().parseAsync(data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength),'')).scene;
scene.updateMatrixWorld(true);
let triangles=0,meshes=0;const materials=new Set();const errors=[];const normalStorage=[];
scene.traverse(o=>{if(!o.isMesh)return;meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;
normalStorage.push({mesh:o.name,normalized:o.geometry.attributes.normal.normalized,component_array:o.geometry.attributes.normal.array.constructor.name,interleaved:Boolean(o.geometry.attributes.normal.isInterleavedBufferAttribute),vertex_count:o.geometry.attributes.normal.count});
for(const name of ['position','normal']){const a=o.geometry.attributes[name];if(!a||Array.from(a.array).some(x=>!Number.isFinite(x)))errors.push(`Invalid ${name}`);}
for(const m of Array.isArray(o.material)?o.material:[o.material]){materials.add(m.uuid);if(m.map)errors.push('Unexpected texture');}});
const bounds=new Box3().setFromObject(scene);
const qa=JSON.parse(await readFile(path.join(dir,'qa.json')));
const delta=Math.max(...['min','max'].flatMap(k=>bounds[k].toArray().map((x,i)=>Math.abs(x-qa.glb.bounds_m[k][i]))));
if(triangles!==qa.glb.scene_triangles||delta>0.0001||materials.size!==3)errors.push('Geometry/material metric mismatch');
const report={schema_version:1,check:'runtime_parse',status:errors.length?'fail':'pass',renderer:`Three.js ${version}`,glb_sha256:sha256,triangles,meshes,materials:materials.size,normal_storage:normalStorage,required_extension:'KHR_mesh_quantization',external_decoder_used:false,bounds_m:{min:bounds.min.toArray(),max:bounds.max.toArray()},bounds_max_delta_m:delta,errors,gpu:'not_run',scene:'not_run',limitations:'Node parser/geometry only; no graphics or performance claim.'};
await writeFile(path.join(dir,'runtime-parse.report.json'),JSON.stringify(report,null,2)+'\n');console.log(report);if(errors.length)process.exitCode=1;
