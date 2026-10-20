import fs from 'node:fs';
import crypto from 'node:crypto';
import * as THREE from '/tmp/lowpoly-batch60-20261020/node_modules/three/build/three.module.js';
import {GLTFLoader} from '/tmp/lowpoly-batch60-20261020/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
const files=[['collinsium','r002'],['yardang','r002'],['glacial-cirque','r001'],['aragonite-frostwork','r001']];
const base='/tmp/lowpoly-round23-qa60/gltf-copies';
const out=[];
for(const [asset_id,revision] of files){
 const path=`${base}/${asset_id}-${revision}.glb`, bytes=fs.readFileSync(path);
 const glb_sha256=crypto.createHash('sha256').update(bytes).digest('hex');
 const arrayBuffer=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
 const gltf=await new GLTFLoader().parseAsync(arrayBuffer,'');
 gltf.scene.updateMatrixWorld(true);
 const json=gltf.parser.json, meshes=[]; let tri=0,positionVertices=0,nonfinite=0,negativeDet=[];
 const box=new THREE.Box3().setFromObject(gltf.scene); const size=new THREE.Vector3(); box.getSize(size);
 gltf.scene.traverse(o=>{
  if(!o.isMesh)return;
  const a=o.geometry.attributes.position, ix=o.geometry.index; const ntri=ix?ix.count/3:a.count/3; tri+=ntri; positionVertices+=a.count;
  if(o.matrixWorld.determinant()<0)negativeDet.push(o.name);
  let nf=0; for(let i=0;i<a.count;i++){ if(!Number.isFinite(a.getX(i))||!Number.isFinite(a.getY(i))||!Number.isFinite(a.getZ(i)))nf++; }
  nonfinite+=nf;
  const assoc=gltf.parser.associations.get(o)||{};
  meshes.push({name:o.name||'', gltf_mesh_index:assoc.meshes??null, primitive_index:assoc.primitives??null, node_index:assoc.nodes??null, triangle_count:ntri, position_vertices:a.count, materials:Array.isArray(o.material)?o.material.map(x=>x.name):[o.material?.name||''], bounds:(()=>{const b=new THREE.Box3().setFromObject(o);return {min:b.min.toArray(),max:b.max.toArray(),size:b.getSize(new THREE.Vector3()).toArray()}})()});
 });
 const sourceMaterials=new Set(); for(const m of meshes)for(const x of m.materials)sourceMaterials.add(x);
 const imgCount=json.images?.length||0, textureCount=json.textures?.length||0;
 out.push({asset_id,revision,glb_sha256,parse:'pass',three_version:THREE.REVISION,scene_node_count:json.nodes?.length||0,glb_mesh_count:json.meshes?.length||0,mesh_primitive_count:(json.meshes||[]).reduce((n,m)=>n+(m.primitives?.length||0),0),scene_mesh_object_count:meshes.length,triangles:tri,position_accessor_vertices:positionVertices,materials:json.materials?.length||0,material_names:[...sourceMaterials].sort(),images:imgCount,textures:textureCount,extensions_used:json.extensionsUsed||[],extensions_required:json.extensionsRequired||[],animation_count:json.animations?.length||0,skin_count:json.skins?.length||0,bounds_y_up_m:{min:box.min.toArray(),max:box.max.toArray(),size:size.toArray()},nonfinite_position_vertices:nonfinite,negative_determinant_meshes:negativeDet,meshes});
}
fs.writeFileSync('/tmp/lowpoly-round23-qa60/three-parse-audit.json',JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out.map(x=>({asset_id:x.asset_id,parse:x.parse,glb_sha256:x.glb_sha256,meshes:x.glb_mesh_count,primitives:x.mesh_primitive_count,triangles:x.triangles,positions:x.position_accessor_vertices,materials:x.materials,images:x.images,textures:x.textures,extensions:x.extensions_used,bounds:x.bounds_y_up_m,nonfinite:x.nonfinite_position_vertices,negative:x.negative_determinant_meshes})),null,2));
