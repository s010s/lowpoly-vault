// SPDX-License-Identifier: MIT
// Optional Node parsing evidence. Does not render or establish GPU behavior.
const fs=require('node:fs'),crypto=require('node:crypto'),url=require('node:url');
(async()=>{
const {GLTFLoader}=await import(url.pathToFileURL(require.resolve('three/addons/loaders/GLTFLoader.js')).href);
const {Box3,Vector3,REVISION}=await import(url.pathToFileURL(require.resolve('three')).href);
if(REVISION!=='180')throw Error('Pinned Three.js r180 required');
const bytes=fs.readFileSync(process.argv[2]||'model.glb');
const result=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
let triangles=0,meshes=0;result.scene.updateMatrixWorld(true);result.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
const box=new Box3().setFromObject(result.scene);const report={check:'Three.js GLTFLoader Node parsing',status:'PASS',three_version:'0.180.0',glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),triangles,meshes,bounds_glb_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new Vector3()).toArray()},gpu:'UNKNOWN',scene_performance:'UNKNOWN',limitations:'Node parser only. No GPU render or populated-scene performance test.'};
fs.writeFileSync(process.argv[3]||'qa/evidence/three-parser.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
})().catch(e=>{console.error(e);process.exitCode=1;});
