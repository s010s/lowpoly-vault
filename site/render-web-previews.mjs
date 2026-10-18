/** Offline image generation: the public list receives WebP, never this WebGL process. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, readdir, stat } from 'node:fs/promises';
import { resolve, extname, dirname, sep } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { CARD_RENDER_PRESET } from './render-preset.js';
import { publishedImagePaths } from './turntable-delivery.mjs';
const root=resolve(process.env.GALLERY_DIR||'dist'),out=resolve(process.env.PREVIEW_OUTPUT||'qa/web-card-previews'),prefix='/lowpoly-vault/';
const imageSize=Number(process.env.PREVIEW_SIZE||CARD_RENDER_PRESET.image.width),imageQuality=Number(process.env.PREVIEW_QUALITY||CARD_RENDER_PRESET.image.quality);
assert(Number.isInteger(imageSize)&&imageSize>=320&&imageSize<=1024);assert(imageQuality>=.75&&imageQuality<=1);
const activePreset={...CARD_RENDER_PRESET,image:{...CARD_RENDER_PRESET.image,width:imageSize,height:imageSize,quality:imageQuality}};
const hash=bytes=>createHash('sha256').update(bytes).digest('hex'),presetHash=hash(JSON.stringify(activePreset));
const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),sealed=JSON.parse(await readFile('assets/turntables/index.json','utf8')),selectedIds=process.env.PREVIEW_ASSET_IDS?new Set(process.env.PREVIEW_ASSET_IDS.split(',')):null,selected=manifest.assets.filter(asset=>!selectedIds||selectedIds.has(asset.id)),pilots=new Set(process.env.PREVIEW_POSTERS_ONLY==='1'?[]:sealed.assets.map(asset=>asset.id)),variant=`v${activePreset.version}-${imageSize}-q${Math.round(imageQuality*100)}`;
assert(selected.length>0&&(!selectedIds||selected.length===selectedIds.size),'Every requested capture ID must be in the checked manifest');
const files=await readdir(resolve(root,'assets')),viewer=files.find(f=>/^viewer-.*\.js$/.test(f));assert(viewer);
const mime={'.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.css':'text/css','.png':'image/png','.webp':'image/webp','.html':'text/html'};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');if(url.pathname===prefix+'capture.html'){res.writeHead(200,{'Content-Type':'text/html'}).end(`<!doctype html><html><body style="margin:0"><div id="capture" style="position:relative;width:${imageSize}px;height:${imageSize}px"></div></body></html>`);return;}if(!url.pathname.startsWith(prefix))throw Error();let path=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length)));if(path!==root&&!path.startsWith(root+sep))throw Error();if((await stat(path)).isDirectory())path=resolve(path,'index.html');const b=await readFile(path);res.writeHead(200,{'Content-Type':mime[extname(path)]||'application/octet-stream'}).end(b);}catch{res.writeHead(404).end();}});
const verification=[];
let browser;const index={version:1,render_preset_sha256:presetHash,assets:sealed.assets.filter(a=>!selected.some(b=>a.id===b.id)||!pilots.has(a.id)),posters:sealed.posters.filter(a=>!selected.some(b=>a.id===b.id))},report={status:'running',target_renderer:'threejs-modelstage',render_preset:activePreset,render_preset_sha256:presetHash,viewer_source_sha256:hash(await readFile('site/viewer.js')),assets:[]};
async function save(path,bytes){await mkdir(dirname(resolve(out,path)),{recursive:true});await writeFile(resolve(out,path),bytes);if(process.env.VERIFY_SHIPPED_PREVIEWS==='1'&&path.endsWith('.webp')){const existing=await readFile(resolve(root,path));verification.push({path,bytes:bytes.length,matches:hash(bytes)===hash(existing)});}}
try{
 await mkdir(out,{recursive:true});await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}${prefix}`;
 browser=await chromium.launch({args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.chromium_version=browser.version();
 const context=await browser.newContext({viewport:{width:imageSize,height:imageSize},deviceScaleFactor:1,reducedMotion:'reduce'}),page=await context.newPage();await page.goto(base+'capture.html');
 await page.evaluate(async module=>{const {ModelStage}=await import(module);window.captureStage=new ModelStage();},base+'assets/'+viewer);
 for(const asset of selected){
  const started=performance.now();assert.equal(hash(await readFile(resolve(root,asset.glb))),asset.sha256.glb);
  await page.evaluate(async({asset,url})=>{const okay=await window.captureStage.show(document.querySelector('#capture'),url,{mode:'detail',metadata:asset});if(!okay||document.querySelector('#capture').dataset.modelState!=='ready')throw Error('A real 3D first paint is required');},{asset,url:base+asset.glb});
  const paths=publishedImagePaths(asset,manifest,variant);
  const frames=[],count=pilots.has(asset.id)?CARD_RENDER_PRESET.image.frames:1;
  for(let i=0;i<count;i++){
   const azimuth=CARD_RENDER_PRESET.camera.azimuth_deg+360*i/CARD_RENDER_PRESET.image.frames,elevation=CARD_RENDER_PRESET.camera.elevation_deg;
   const data=await page.evaluate(({azimuth,elevation,quality})=>{window.captureStage.setView(azimuth,elevation);return document.querySelector('#capture canvas').toDataURL('image/webp',quality);},{azimuth,elevation,quality:imageQuality});
   if(i===0&&process.env.CAPTURE_REFERENCE==='1'){const png=await page.evaluate(({azimuth,elevation})=>{window.captureStage.setView(azimuth,elevation);return document.querySelector('#capture canvas').toDataURL('image/png');},{azimuth,elevation});await save(`references/${asset.id}.png`,Buffer.from(png.split(',')[1],'base64'));}
   assert(data.startsWith('data:image/webp;base64,'));const bytes=Buffer.from(data.split(',')[1],'base64');
   if(i===0){const path=paths.poster;await save(path,bytes);index.posters.push({id:asset.id,path,sha256:hash(bytes),bytes:bytes.length,width:imageSize,height:imageSize,source_glb_sha256:asset.sha256.glb,render_preset_sha256:presetHash});}
   if(pilots.has(asset.id)){const path=`${dirname(paths.manifest)}/frame-${String(i).padStart(3,'0')}.webp`;await save(path,bytes);frames.push({path,bytes:bytes.length,sha256:hash(bytes),azimuth_deg:azimuth,elevation_deg:elevation,view:'turntable'});}
  }
  if(pilots.has(asset.id)){const data={version:1,target_renderer:'threejs-modelstage',source_glb_sha256:asset.sha256.glb,render_preset_sha256:presetHash,frame_count:frames.length,width:imageSize,height:imageSize,poster_index:0,background:'transparent',alpha:true,format:'WEBP',quality:imageQuality,frames,total_bytes:frames.reduce((s,f)=>s+f.bytes,0),decoded_rgba_bytes_estimate:frames.length*imageSize*imageSize*4,license:'CC-BY-4.0'};const path=paths.manifest,bytes=Buffer.from(JSON.stringify(data)+'\n');await save(path,bytes);index.assets.push({id:asset.id,manifest:path,source_glb_sha256:asset.sha256.glb,manifest_sha256:hash(bytes)});}
  report.assets.push({id:asset.id,source_glb_sha256:asset.sha256.glb,frames:count,wall_ms:Math.round(performance.now()-started),frame_bytes_total:frames.reduce((s,f)=>s+f.bytes,0),poster_bytes:index.posters.at(-1).bytes});
 }
 report.gpu=await page.evaluate(()=>window.captureStage.stats);assert.equal(report.gpu.peakRequests,1);await page.evaluate(()=>window.captureStage.dispose());await context.close();await save('assets/turntables/index.json',JSON.stringify(index,null,2)+'\n');if(process.env.VERIFY_SHIPPED_PREVIEWS==='1'){report.reproducibility={checked:verification.length,mismatches:verification.filter(item=>!item.matches)};assert.equal(verification.length,selected.reduce((sum,asset)=>sum+(pilots.has(asset.id)?CARD_RENDER_PRESET.image.frames+1:1),0));assert.equal(report.reproducibility.mismatches.length,0,'Pinned renderer capture must reproduce the shipped card pixels/encoding');}report.status='pass';
 console.log(JSON.stringify(report,null,2));
}catch(error){report.status='fail';report.error=error.stack;console.error(error);process.exitCode=1;}
finally{await save('render-report.json',JSON.stringify(report,null,2)+'\n');await browser?.close();if(server.listening)await new Promise(r=>server.close(r));}
