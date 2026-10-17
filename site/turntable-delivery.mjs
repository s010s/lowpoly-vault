/** Optional image sequences are separately sealed; source GLB/Blend publication remains unchanged. */
import { readFile, mkdir, cp, realpath, writeFile } from 'node:fs/promises';
import { dirname, resolve, relative } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { validateTurntable } from './image-scrub.js';
import { CARD_RENDER_PRESET } from './render-preset.js';
const variant=`v${CARD_RENDER_PRESET.version}-${CARD_RENDER_PRESET.image.width}-q${Math.round(CARD_RENDER_PRESET.image.quality*100)}`;
const presetHash=createHash('sha256').update(JSON.stringify(CARD_RENDER_PRESET)).digest('hex');
export function webpDimensions(bytes) {
  assert.equal(bytes.toString('ascii',0,4),'RIFF');assert.equal(bytes.toString('ascii',8,12),'WEBP');assert.equal(bytes.readUInt32LE(4)+8,bytes.length);
  for(let offset=12;offset+8<=bytes.length;){const name=bytes.toString('ascii',offset,offset+4),size=bytes.readUInt32LE(offset+4),p=offset+8;assert(p+size<=bytes.length);
    if(name==='VP8X')return [1+bytes.readUIntLE(p+4,3),1+bytes.readUIntLE(p+7,3)];
    if(name==='VP8 '){assert.equal(bytes.toString('hex',p+3,p+6),'9d012a');return [bytes.readUInt16LE(p+6)&0x3fff,bytes.readUInt16LE(p+8)&0x3fff];}
    if(name==='VP8L'){assert.equal(bytes[p],0x2f);return [1+bytes[p+1]+((bytes[p+2]&63)<<8),1+(bytes[p+2]>>6)+(bytes[p+3]<<2)+((bytes[p+4]&15)<<10)];}
    offset=p+size+(size%2);
  }
  throw new Error('WebP dimensions unavailable');
}
export async function collectTurntables(manifest,root=process.cwd()) {
  let source;
  try{source=JSON.parse(await readFile(resolve(root,'assets/turntables/index.json'),'utf8'));}
  catch(error){if(error.code==='ENOENT')return {descriptors:new Map(),posters:new Map(),files:[]};throw error;}
  assert.equal(await realpath(resolve(root,'assets/turntables/index.json')),resolve(root,'assets/turntables/index.json'),'Turntable index symlinks are not allowed');
  assert.equal(source.version,1);assert(Array.isArray(source.assets));assert.equal(source.render_preset_sha256,presetHash,'Website frames must match the active viewer preset');const descriptors=new Map(),posters=new Map(),files=[];
  for(const item of source.assets) {
    const asset=manifest.assets.find(a=>a.id===item.id);assert(asset,'Turntable must match a published original');assert(!descriptors.has(item.id),'Duplicate turntable');
    const path=`assets/turntables/${item.id}/${variant}/turntable.json`;assert.equal(item.manifest,path);assert.equal(item.source_glb_sha256,asset.sha256.glb);
    assert.equal(await realpath(resolve(root,path)),resolve(root,path),'Turntable metadata symlinks are not allowed');
    const bytes=await readFile(resolve(root,path));assert.equal(createHash('sha256').update(bytes).digest('hex'),item.manifest_sha256,'Turntable metadata changed');
    const data=JSON.parse(bytes),descriptor={manifest:path,source_glb_sha256:asset.sha256.glb,frame_count:data.frame_count,width:data.width,height:data.height,poster_index:data.poster_index};
    assert.equal(data.target_renderer,'threejs-modelstage');assert.equal(data.alpha,true);assert.equal(data.background,'transparent');assert.equal(data.render_preset_sha256,presetHash);
    validateTurntable(data,descriptor);files.push(path);let total=0;
    for(const frame of data.frames) {
      assert.equal(relative(resolve(root),await realpath(resolve(root,frame.path))).split('\\').join('/'),frame.path,'Turntable symlinks are not allowed');
      const bytes=await readFile(resolve(root,frame.path));assert.equal(bytes.length,frame.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),frame.sha256,'Turntable frame changed');assert.deepEqual(webpDimensions(bytes),[data.width,data.height]);total+=bytes.length;files.push(frame.path);
    }
    assert.equal(total,data.total_bytes,'Sequence total must equal measured frame files');descriptors.set(item.id,{...descriptor,total_bytes:total});
  }
  assert.equal(source.posters?.length,manifest.assets.length,'Every published card needs a matching lightweight poster');
  for(const item of source.posters) {
    const asset=manifest.assets.find(a=>a.id===item.id);assert(asset);assert(!posters.has(item.id));
    assert.equal(item.path,`assets/card-previews/${item.id}-${variant}.webp`);assert.equal(item.source_glb_sha256,asset.sha256.glb);assert.equal(item.render_preset_sha256,presetHash);
    assert.equal(await realpath(resolve(root,item.path)),resolve(root,item.path),'Poster symlinks are not allowed');
    const bytes=await readFile(resolve(root,item.path));assert.equal(bytes.length,item.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),item.sha256);
    assert.deepEqual(webpDimensions(bytes),[CARD_RENDER_PRESET.image.width,CARD_RENDER_PRESET.image.height]);assert.equal(item.width,CARD_RENDER_PRESET.image.width);assert.equal(item.height,CARD_RENDER_PRESET.image.height);posters.set(item.id,item.path);files.push(item.path);
  }
  return {descriptors,posters,files};
}
export async function deliverTurntables(manifest,outDir,{root=process.cwd()}={}) {
  const {descriptors,posters,files}=await collectTurntables(manifest,root);
  for(const path of files){await mkdir(dirname(resolve(outDir,path)),{recursive:true});await cp(resolve(root,path),resolve(outDir,path));}
  const enriched={...manifest,assets:manifest.assets.map(asset=>({...asset,...(posters.has(asset.id)?{card_preview:posters.get(asset.id)}:{}),...(descriptors.has(asset.id)?{turntable:descriptors.get(asset.id)}:{})}))};
  await writeFile(resolve(outDir,'assets/manifest.json'),JSON.stringify(enriched,null,2)+'\n');
  console.log(`Image-scrub delivery: ${descriptors.size} original assets, ${files.length-descriptors.size-posters.size} individually lazy-loadable frames, ${posters.size} lightweight static posters.`);
  return enriched;
}
