import fs from 'node:fs';
import crypto from 'node:crypto';
import {GLTFLoader} from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/build/three.module.js';
for (const dir of process.argv.slice(2)) {
 const p=dir+'/model.glb',b=fs.readFileSync(p),sha=crypto.createHash('sha256').update(b).digest('hex');
 const g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);
 let triangles=0,meshes=0,materials=new Set();g.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of (Array.isArray(o.material)?o.material:[o.material]))materials.add(m?.name||'<unnamed>')}});
 const box=new Box3().setFromObject(g.scene);const report={kind:'fresh_three_node_parse',path:p,glb_sha256:sha,bytes:b.length,three_version:'0.'+REVISION+'.0',three_revision:REVISION,triangles,meshes,materials:[...materials].sort(),bounds_glb_xyz_m:box.getSize(new Vector3()).toArray(),gpu:'not_run',scene:'not_run',errors:[],limitations:'Node GLTFLoader parse only; no browser, GPU or populated scene.'};console.log(JSON.stringify(report));
}
