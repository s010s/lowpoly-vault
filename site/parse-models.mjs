// Headless parser/geometry test. This does NOT prove browser rendering or visual quality.
import { readFile,readdir,writeFile,mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { Box3,Vector3 } from 'three';
async function discover(dir){const found=[];for(const e of await readdir(dir,{withFileTypes:true})){const p=join(dir,e.name);if(e.isDirectory())found.push(...await discover(p));else if(e.name==='metadata.json')found.push(p);}return found.sort();}
const results=[];
for(const path of await discover('assets')){
 const a=JSON.parse(await readFile(path,'utf8'));
 try{const bytes=await readFile(a.glb),gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');const scene=gltf.scene;scene.updateMatrixWorld(true);let triangles=0,meshes=0;scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});const size=new Box3().setFromObject(scene).getSize(new Vector3()).toArray();const delta=Math.max(...size.map((n,i)=>Math.abs(n-a.dimensions[i])));if(triangles!==a.triangles)throw new Error(`Triangle mismatch: ${triangles} vs ${a.triangles}`);if(delta>.0001)throw new Error(`Bounds mismatch: ${delta} m`);results.push({id:a.id,status:'pass',meshes,triangles,dimensions:size,bounds_max_delta_m:delta});scene.traverse(o=>{o.geometry?.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});console.log(`PASS ${a.id}: ${meshes} meshes, ${triangles} triangles, dimensions match`);}catch(e){results.push({id:a.id,status:'fail',error:e.message});console.error(`FAIL ${a.id}: ${e.message}`);}
}
await mkdir('qa',{recursive:true});await writeFile('qa/threejs-parser.json',JSON.stringify({test:'Three.js GLTFLoader Node parser and geometry only',browser_rendering:'not_tested',visual_review:'not_tested',results},null,2)+'\n');if(!results.length||results.some(r=>r.status==='fail'))process.exitCode=1;
