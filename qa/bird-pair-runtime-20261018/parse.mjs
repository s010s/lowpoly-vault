import fs from 'node:fs';import crypto from 'node:crypto';import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';import {Box3,Vector3,REVISION} from 'three';
const inputs=Object.fromEntries(['ichthyornis','confuciusornis'].map(a=>[a,`assets/${a}.glb`]));
const expected=JSON.parse(fs.readFileSync('expected.json'));
fs.mkdirSync('assets',{recursive:true});const reports=[];
for(const [asset,path] of Object.entries(inputs)){const b=fs.readFileSync(path);if(crypto.createHash('sha256').update(b).digest('hex')!==expected[asset])throw Error('Hash mismatch: '+asset);const g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);let tris=0,meshes=0;g.scene.traverse(o=>{if(o.isMesh){meshes++;tris+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;}});reports.push({asset,sha256:crypto.createHash('sha256').update(b).digest('hex'),bytes:b.length,status:'pass',three:REVISION,triangles:tris,meshes,bounds:new Box3().setFromObject(g.scene).getSize(new Vector3()).toArray(),animations:g.animations.length});}
fs.writeFileSync('node-parse.json',JSON.stringify(reports,null,2));console.log(reports);
