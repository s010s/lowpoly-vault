/** Optional image sequences are separately sealed; source GLB/Blend publication remains unchanged. */
import { readFile, mkdir, cp, realpath, writeFile } from 'node:fs/promises';
import { dirname, resolve, relative } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { validateTurntable } from './image-scrub.js';
import { CARD_RENDER_PRESET } from './render-preset.js';
import { REFINABLE_ASSET_IDS } from './refined-release.mjs';
const variant=`v${CARD_RENDER_PRESET.version}-${CARD_RENDER_PRESET.image.width}-q${Math.round(CARD_RENDER_PRESET.image.quality*100)}`;
const presetHash=createHash('sha256').update(JSON.stringify(CARD_RENDER_PRESET)).digest('hex');
// Only the checked mixed manifest selects revision routes; image-index fields never grant approval.
export function publishedImagePaths(asset,manifest,imageVariant=variant) {
  assert(/^v[0-9]+-[0-9]+-q[0-9]+$/.test(imageVariant),'Safe render variant required');
  assert(/^[a-z0-9-]+$/.test(asset.id||''),'Safe published asset ID required');
  const selected=manifest.release_status==='mixed'&&manifest.publication?.approved_asset_ids?.includes(asset.id);
  const revised=selected||asset.revision!==undefined||asset.quality_status==='accepted_for_brief'||asset.revision_provenance!==undefined;
  if(revised) {
    assert(!manifest.review_only&&manifest.release_status==='mixed'&&manifest.quality_status==='mixed'&&selected&&REFINABLE_ASSET_IDS.includes(asset.id), 'Revision images require an explicitly authorized mixed-release asset');
    assert.equal(asset.quality_status,'accepted_for_brief','Revision images require individually accepted status');
    assert(typeof asset.revision==='string'&&/^[a-z0-9][a-z0-9._-]*$/.test(asset.revision),'Safe accepted revision identifier required');
    for(const key of ['glb','blend','preview'])assert.equal(dirname(asset[key]||''),`assets/revisions/${asset.id}/${asset.revision}`,'Revision images must match the mixed-release storage revision');
  }
  const suffix=revised?`/${asset.revision}`:'';
  return {revised,manifest:`assets/turntables/${asset.id}${suffix}/${imageVariant}/turntable.json`,poster:`assets/card-previews/${asset.id}${revised?`-${asset.revision}`:''}-${imageVariant}.webp`};
}
// Encoded alpha presence, not a substitute for decoding or independent pixel review.
// https://developers.google.com/speed/webp/docs/riff_container
export function webpHasAlpha(bytes) {
  webpDimensions(bytes);
  let extendedAlpha=false,alphaChunk=false,losslessAlpha=false;
  for(let offset=12;offset+8<=bytes.length;) {
    const name=bytes.toString('ascii',offset,offset+4),size=bytes.readUInt32LE(offset+4),p=offset+8;
    assert(p+size<=bytes.length,'Truncated WebP chunk');
    if(name==='VP8X'){assert(size>=10);extendedAlpha=Boolean(bytes[p]&0x10);assert(!(bytes[p]&0x02),'Animated WebP cannot be a static turntable frame');}
    if(name==='ALPH')alphaChunk=size>1;
    if(name==='VP8L'){assert(size>=5&&bytes[p]===0x2f);losslessAlpha=Boolean(bytes[p+4]&0x10);}
    offset=p+size+(size%2);
  }
  return losslessAlpha||(extendedAlpha&&alphaChunk);
}
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
  const paths=new Map();
  for(const asset of manifest.assets){assert(!paths.has(asset.id),'Duplicate published asset ID');paths.set(asset.id,publishedImagePaths(asset,manifest));}
  let source;
  try{source=JSON.parse(await readFile(resolve(root,'assets/turntables/index.json'),'utf8'));}
  catch(error){if(error.code==='ENOENT'){assert(![...paths.values()].some(item=>item.revised),'Accepted revisions require a sealed turntable index');return {descriptors:new Map(),posters:new Map(),files:[]};}throw error;}
  assert.equal(await realpath(resolve(root,'assets/turntables/index.json')),resolve(root,'assets/turntables/index.json'),'Turntable index symlinks are not allowed');
  assert.equal(source.version,1);assert(Array.isArray(source.assets));assert.equal(source.render_preset_sha256,presetHash,'Website frames must match the active viewer preset');const descriptors=new Map(),posters=new Map(),posterFrames=new Map(),files=[];
  for(const item of source.assets) {
    const asset=manifest.assets.find(a=>a.id===item.id);assert(asset,'Turntable must match a published asset');assert(!descriptors.has(item.id),'Duplicate turntable');
    const {manifest:path,revised}=paths.get(item.id);assert.equal(item.manifest,path);assert.equal(item.source_glb_sha256,asset.sha256.glb);
    assert.equal(await realpath(resolve(root,path)),resolve(root,path),'Turntable metadata symlinks are not allowed');
    const bytes=await readFile(resolve(root,path));assert.equal(createHash('sha256').update(bytes).digest('hex'),item.manifest_sha256,'Turntable metadata changed');
    const data=JSON.parse(bytes),descriptor={manifest:path,source_glb_sha256:asset.sha256.glb,frame_count:data.frame_count,width:data.width,height:data.height,poster_index:data.poster_index};
    assert.equal(data.target_renderer,'threejs-modelstage');assert.equal(data.alpha,true);assert.equal(data.background,'transparent');assert.equal(data.render_preset_sha256,presetHash);
    validateTurntable(data,descriptor);
    if(revised){assert.equal(data.poster_index,0,'Revision poster must be frame 0');assert.equal(data.frame_count,CARD_RENDER_PRESET.image.frames);assert.equal(data.width,CARD_RENDER_PRESET.image.width);assert.equal(data.height,CARD_RENDER_PRESET.image.height);assert.equal(data.format,'WEBP');assert.equal(data.quality,CARD_RENDER_PRESET.image.quality);}
    files.push(path);let total=0;
    for(const [index,frame] of data.frames.entries()) {
      assert.equal(frame.path,`${dirname(path)}/frame-${String(index).padStart(3,'0')}.webp`,'Only deterministic ordered frame paths may be delivered');
      if(revised){assert.equal(frame.view,'turntable','Revision frame view must be turntable');assert.equal(frame.azimuth_deg,CARD_RENDER_PRESET.camera.azimuth_deg+360*index/CARD_RENDER_PRESET.image.frames,'Revision frame azimuth must match the active preset angle');assert.equal(frame.elevation_deg,CARD_RENDER_PRESET.camera.elevation_deg,'Revision frame elevation must match the active preset angle');}
      assert.equal(relative(resolve(root),await realpath(resolve(root,frame.path))).split('\\').join('/'),frame.path,'Turntable symlinks are not allowed');
      const bytes=await readFile(resolve(root,frame.path));assert.equal(bytes.length,frame.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),frame.sha256,'Turntable frame changed');assert.deepEqual(webpDimensions(bytes),[data.width,data.height]);if(revised)assert(webpHasAlpha(bytes),'Revision frame must contain encoded alpha');total+=bytes.length;files.push(frame.path);
    }
    assert.equal(total,data.total_bytes,'Sequence total must equal measured frame files');descriptors.set(item.id,{...descriptor,total_bytes:total});posterFrames.set(item.id,data.frames[data.poster_index]);
  }
  assert.equal(source.posters?.length,manifest.assets.length,'Every published card needs a matching lightweight poster');
  for(const item of source.posters) {
    const asset=manifest.assets.find(a=>a.id===item.id);assert(asset);assert(!posters.has(item.id));
    const {poster:posterPath,revised}=paths.get(item.id);assert.equal(item.path,posterPath);assert.equal(item.source_glb_sha256,asset.sha256.glb);assert.equal(item.render_preset_sha256,presetHash);
    assert.equal(await realpath(resolve(root,item.path)),resolve(root,item.path),'Poster symlinks are not allowed');
    if(revised){const frame=posterFrames.get(item.id);assert(frame,'Revised cards require the accepted revision sequence');assert.equal(item.sha256,frame.sha256,'Revision poster must match frame 0');assert.equal(item.bytes,frame.bytes,'Revision poster bytes must match frame 0');assert.equal(item.sha256,asset.sha256.preview,'Revision poster must match the approved published preview');}
    if(manifest.publication?.approved_addition_ids?.includes(asset.id)){assert.equal(item.sha256,asset.sha256.preview,'Addition poster must match its published canonical preview');assert(!descriptors.has(asset.id),'Small-life additions are poster-only, never sequence frames');}
    const bytes=await readFile(resolve(root,item.path));assert.equal(bytes.length,item.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),item.sha256);
    assert.deepEqual(webpDimensions(bytes),[CARD_RENDER_PRESET.image.width,CARD_RENDER_PRESET.image.height]);if(revised||manifest.publication?.approved_addition_ids?.includes(asset.id))assert(webpHasAlpha(bytes),'Published accepted poster must contain encoded alpha');assert.equal(item.width,CARD_RENDER_PRESET.image.width);assert.equal(item.height,CARD_RENDER_PRESET.image.height);posters.set(item.id,item.path);files.push(item.path);
  }
  return {descriptors,posters,files};
}
export async function deliverTurntables(manifest,outDir,{root=process.cwd()}={}) {
  const {descriptors,posters,files}=await collectTurntables(manifest,root);
  for(const path of files){await mkdir(dirname(resolve(outDir,path)),{recursive:true});await cp(resolve(root,path),resolve(outDir,path));}
  const enriched={...manifest,assets:manifest.assets.map(asset=>({...asset,...(posters.has(asset.id)?{card_preview:posters.get(asset.id)}:{}),...(descriptors.has(asset.id)?{turntable:descriptors.get(asset.id)}:{})}))};
  await writeFile(resolve(outDir,'assets/manifest.json'),JSON.stringify(enriched,null,2)+'\n');
  console.log(`Image-scrub delivery: ${descriptors.size} published assets, ${files.length-descriptors.size-posters.size} individually lazy-loadable frames, ${posters.size} lightweight static posters.`);
  return enriched;
}
