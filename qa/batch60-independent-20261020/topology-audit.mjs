import fs from 'node:fs';
import * as THREE from '/tmp/lowpoly-batch60-20261020/node_modules/three/build/three.module.js';
import {GLTFLoader} from '/tmp/lowpoly-batch60-20261020/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
const files=[['collinsium','r002'],['yardang','r002'],['glacial-cirque','r001'],['aragonite-frostwork','r001']],base='/tmp/lowpoly-round23-qa60/gltf-copies';
const out=[],quantum=1e-6;
function key(v){return `${Math.round(v[0]/quantum)},${Math.round(v[1]/quantum)},${Math.round(v[2]/quantum)}`}
for(const [asset_id,revision] of files){
 const p=`${base}/${asset_id}-${revision}.glb`,b=fs.readFileSync(p),g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);
 const groups=new Map();
 g.scene.traverse(o=>{if(!o.isMesh)return;const as=g.parser.associations.get(o)||{},mi=as.meshes??-1;if(!groups.has(mi))groups.set(mi,{mesh_index:mi,parts:[],positions:[],faces:[]});const q=groups.get(mi),a=o.geometry.attributes.position,idx=o.geometry.index; const offset=q.positions.length;
  for(let i=0;i<a.count;i++){const v=new THREE.Vector3(a.getX(i),a.getY(i),a.getZ(i)).applyMatrix4(o.matrixWorld);q.positions.push(v.toArray());}
  const inds=idx?Array.from({length:idx.count},(_,i)=>idx.getX(i)):Array.from({length:a.count},(_,i)=>i);for(let i=0;i<inds.length;i+=3)q.faces.push([offset+inds[i],offset+inds[i+1],offset+inds[i+2]]);q.parts.push(o.name||'');
 });
 const reports=[];
 for(const q of groups.values()){
  const edges=new Map();let deg=0,nonfinite=0;
  for(const face of q.faces){const ps=face.map(i=>q.positions[i]);if(ps.flat().some(v=>!Number.isFinite(v))){nonfinite++;continue;}const u=ps[1].map((v,i)=>v-ps[0][i]),v=ps[2].map((v,i)=>v-ps[0][i]);const c=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];if(Math.hypot(...c)<1e-12)deg++;const ks=face.map(i=>key(q.positions[i]));for(let j=0;j<3;j++){let a=ks[j],b=ks[(j+1)%3],k=a<b?a+'|'+b:b+'|'+a;edges.set(k,(edges.get(k)||0)+1);}}
  let boundary=0,nm=0;for(const n of edges.values()){if(n===1)boundary++;else if(n>2)nm++;}
  reports.push({gltf_mesh_index:q.mesh_index,parts:q.parts,triangle_count:q.faces.length,source_position_count:q.positions.length,welded_position_count:new Set(q.positions.map(key)).size,edge_count:edges.size,boundary_edges:boundary,nonmanifold_edges:nm,degenerate_triangles:deg,nonfinite_triangles:nonfinite,coordinate_weld_tolerance_m:quantum});
 }
 out.push({asset_id,revision,mesh_count:reports.length,meshes:reports,boundary_edges_total:reports.reduce((s,x)=>s+x.boundary_edges,0),nonmanifold_edges_total:reports.reduce((s,x)=>s+x.nonmanifold_edges,0),degenerate_triangles_total:reports.reduce((s,x)=>s+x.degenerate_triangles,0),nonfinite_triangles_total:reports.reduce((s,x)=>s+x.nonfinite_triangles,0)});
}
fs.writeFileSync('/tmp/lowpoly-round23-qa60/glb-topology-audit.json',JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out.map(x=>({asset_id:x.asset_id,mesh_count:x.mesh_count,boundary_edges:x.boundary_edges_total,nonmanifold_edges:x.nonmanifold_edges_total,degenerate_triangles:x.degenerate_triangles_total,nonfinite_triangles:x.nonfinite_triangles_total})),null,2));
