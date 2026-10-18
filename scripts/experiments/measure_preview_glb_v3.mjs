// SPDX-License-Identifier: MIT
// Node parser CPU proxy, not browser/GPU or rendered-frame performance.
import {readFile,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {performance} from 'node:perf_hooks';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
const root=resolve(import.meta.dirname,'../..');
const assets={'dinosaur-nest':'traces',lepidodendron:'plants','natural-arch':'geology'};
function dispose(gltf){gltf.scene.traverse(o=>{o.geometry?.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});}
const report={conditions:{node:process.version,three:'0.180.0',iterations:40,warmups:5,
 method:'In-memory GLTFLoader.parseAsync including typed-array/material/object allocation; fresh ArrayBuffer slice before each timing; no rendering, GPU upload, shader compilation, network, decoder or renderer library transfer.',
 comparability:'Node GLB parse and Pillow image decode use different runtimes. Directional CPU proxies only, not a browser head-to-head or user-device latency.'},assets:[]};
for(const [slug,category] of Object.entries(assets)){
 const source=await readFile(resolve(root,`assets/prehistoric/${category}/${slug}/${slug}.glb`));
 const times=[];let meshes=0,triangles=0;
 for(let i=0;i<45;i++){
  const buffer=source.buffer.slice(source.byteOffset,source.byteOffset+source.byteLength);
  const start=performance.now();const gltf=await new GLTFLoader().parseAsync(buffer,'');const elapsed=performance.now()-start;
  if(i===0)gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
  if(i>=5)times.push(elapsed);dispose(gltf);
 }
 const s=[...times].sort((a,b)=>a-b),round=v=>Math.round(v*10000)/10000;
 report.assets.push({asset:slug,glb_file_bytes:source.length,meshes,triangles,
  cpu_proxy_parse:{median_ms:round((s[19]+s[20])/2),p95_ms:round(s[37]),min_ms:round(s[0]),max_ms:round(s.at(-1)),samples_ms:times.map(round)}});
}
await writeFile(resolve(root,'experiments/preview-turntable-v3/glb-parser-proxy.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report.assets.map(a=>({asset:a.asset,...a.cpu_proxy_parse,samples_ms:undefined})),null,2));
