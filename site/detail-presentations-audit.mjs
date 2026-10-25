/** Offline delivery inventory only. Publication authority is a separate mandatory release gate. */
import assert from 'node:assert/strict';
import {readFile,readdir} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import index from './gallery/detail-presentations-index.js';
import {resolveGalleryPoster} from './gallery/wheel-presentations.js';
export async function auditDetailPresentations(manifest,{root=process.cwd(),outputRoot}={}){
 const resources=JSON.parse(await readFile(resolve(root,'site/public/gallery/resources.json'))),files=[];
 const affected=manifest.assets.filter(a=>['blender-cycles-cpu-v1','blender-detail-preview-wheel-v1'].includes(resources.posters[a.id]?.render_route));
 assert.deepEqual(Object.keys(index.presentations).sort(),affected.map(a=>a.id).sort(),'Every affected right delivery must be inventoried');
 for(const asset of manifest.assets){const e=index.presentations[asset.id],poster=resolveGalleryPoster(asset,resources);if(!e){assert.equal(poster.detail,resources.posters[asset.id].detail,'Ordinary right path changed');continue;}
  assert.equal(poster.detail,e.detail,'Rejected right delivery binding '+asset.id);assert.equal(e.detail,`detail-presentations/${asset.id}.png`);
  const bytes=await readFile(resolve(root,'site/public',e.detail));assert.equal(bytes.length,e.png.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),e.png.sha256);
  if(outputRoot)assert((await readFile(resolve(outputRoot,e.detail))).equals(bytes),'Delivered right PNG differs '+asset.id);files.push(e.detail);
 }
 const names=await readdir(resolve(root,'site/public/detail-presentations'),{withFileTypes:true});assert(names.every(n=>n.isFile()&&!n.isSymbolicLink()));assert.deepEqual(names.map(n=>'detail-presentations/'+n.name).sort(),files.slice().sort());return {files,count:files.length};
}
