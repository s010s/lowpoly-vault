import fs from 'node:fs';
import crypto from 'node:crypto';
import { GLTFLoader } from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import { Box3, Vector3, REVISION } from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/build/three.module.js';
for (const file of process.argv.slice(2)) {
  const b=fs.readFileSync(file);
  const parsed=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
  parsed.scene.updateMatrixWorld(true);
  let triangles=0,meshes=0,primitives=0,materials=new Set();
  parsed.scene.traverse(o=>{if(o.isMesh){meshes++;const p=o.geometry.index?.count??o.geometry.attributes.position.count;triangles+=p/3;primitives++;for(const m of (Array.isArray(o.material)?o.material:[o.material])) if(m) materials.add(m.name);}});
  const bounds=new Box3().setFromObject(parsed.scene);
  const report={file,sha256:crypto.createHash('sha256').update(b).digest('hex'),three_version:'0.180.0',three_revision:REVISION,parser:'Node GLTFLoader.parseAsync (independent read-only)',meshes,primitives,triangles,bounds_min_m:bounds.min.toArray(),bounds_max_m:bounds.max.toArray(),bounds_size_m:bounds.getSize(new Vector3()).toArray(),materials:[...materials],status:'pass',gpu:'not_run',scene:'not_run'};
  fs.writeFileSync('/workspace/shared/lowpoly-round25-qa65/technical/three-'+file.split('/').at(-3)+'.json',JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({file,sha256:report.sha256,status:report.status,meshes,primitives,triangles,dimensions:report.bounds_size_m}));
}
