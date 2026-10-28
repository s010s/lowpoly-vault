/** Integration only: existing IDs/paths and nonempty files. No QA replays,
 * new receipts, or default hashing. --hash checks existing handoff pins once. */
import assert from 'node:assert/strict';
import {readFile,realpath,stat} from 'node:fs/promises';
import {resolve,sep,extname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {resolveGalleryPoster} from './gallery/wheel-presentations.js';
export function assertDeliveryPath(path){assert(typeof path==='string'&&path&&!path.startsWith('/')&&!/[\\\u0000-\u001f?#%:]/.test(path)&&path.split('/').every(x=>x&&x!=='.'&&x!=='..'),'Unsafe delivery path');}
const owned=(id,path)=>path.split('/').some(part=>part===id||part.startsWith(id+'.')||part===id+'-wheel.png');
export async function checkDelivery({root=process.cwd(),manifest,resources,wheelIndex,detailIndex,hash=false}={}){
 root=await realpath(root);manifest??=JSON.parse(await readFile(resolve(root,'assets/manifest.json')));resources??=JSON.parse(await readFile(resolve(root,'site/public/gallery/resources.json')));
 wheelIndex??=(await import(pathToFileURL(resolve(root,'site/gallery/wheel-presentations-index.js')))).default;
 detailIndex??=(await import(pathToFileURL(resolve(root,'site/gallery/detail-presentations-index.js')))).default;
 assert(Array.isArray(manifest.assets)&&manifest.assets.length,'Nonempty model manifest required');const ids=new Set(),models=[];
 for(const asset of manifest.assets){
  assert(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(asset.id)&&!ids.has(asset.id),'Duplicate or invalid model ID');ids.add(asset.id);
  // Same resolver as the site, including legacy fallback; never invent a path.
  const poster=resolveGalleryPoster(asset,resources,wheelIndex,detailIndex);assert(poster,`Missing or mismatched poster entry: ${asset.id}`);
  const paths={glb:asset.glb,blend:asset.blend,left:poster.wheel,right:poster.detail},files={};
  for(const [role,path]of Object.entries(paths)){
   assertDeliveryPath(path);assert(owned(asset.id,path),`Model ID/path mismatch: ${asset.id} ${role}`);
   if(role==='glb'||role==='blend'){assert(path.startsWith('assets/'),'Model file must be in assets');assert.equal(extname(path),'.'+role,`${role} extension mismatch`);}
   const relative=(role==='left'||role==='right')?'site/public/'+path:path,full=resolve(root,relative);assert(full.startsWith(root+sep),'Delivery path escapes root');assert.equal(await realpath(full),full,'Delivery symlink rejected');
   const info=await stat(full);assert(info.isFile()&&info.size>0,`Missing or empty delivery: ${asset.id} ${role}`);files[role]={path:relative,bytes:info.size};
   if(hash){
    const pin=(role==='glb'||role==='blend')?asset.sha256?.[role]:resources.files?.find(file=>file.path===path)?.sha256??(role==='left'&&wheelIndex.presentations?.[asset.id]?.wheel===path?wheelIndex.presentations[asset.id].png?.sha256:undefined)??(role==='right'&&detailIndex.presentations?.[asset.id]?.detail===path?detailIndex.presentations[asset.id].png?.sha256:undefined);
    assert(/^[a-f0-9]{64}$/.test(pin||''),`No existing handoff hash: ${asset.id} ${role}`);const actual=createHash('sha256').update(await readFile(full)).digest('hex');assert.equal(actual,pin,`Handoff hash differs: ${asset.id} ${role}`);files[role].sha256=actual;
   }
  }models.push({id:asset.id,files});
 }return {models,count:models.length,hash_checked:hash};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){const args=process.argv.slice(2);assert(args.length===0||(args.length===1&&args[0]==='--hash'),'Usage: node site/unified-delivery-contract.mjs [--hash]');const result=await checkDelivery({hash:args.includes('--hash')});console.log(`Delivery files: ${result.count} models, four nonempty role paths each; hashes ${result.hash_checked?'verified':'not repeated'}.`);}
