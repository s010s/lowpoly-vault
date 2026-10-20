import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from 'three';
for (const dir of process.argv.slice(2)) {
  const b=fs.readFileSync(path.join(dir,'model.glb'));
  const gltf=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
  gltf.scene.updateMatrixWorld(true); let triangles=0, meshes=0, primitives=0, materials=0;
  gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;primitives++;}});
  materials=gltf.materials?.length ?? 0;
  const report={status:'pass',glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),three_revision:REVISION,parser:'independent Node GLTFLoader.parseAsync',triangles,meshes,primitives:meshes,bounds_glb_xyz_m:new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray(),errors:[],gpu:'not_run',scene:'not_run'};
  fs.writeFileSync(path.join(dir,'independent-runtime-parse.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({dir,...report}));
}
