import { defineConfig } from 'vite';
import { readFile, realpath, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { createCatalog } from './site/catalog-build.mjs';
const assetRoot=resolve('assets');
const catalogCache=new Map();
async function catalogFile(pathname){
 const match=pathname.match(/^\/assets\/(catalog(?:-review)?)(?:\.json|\/(?:shards|details)\/[a-zA-Z0-9._-]+\.json)$/);
 if(!match)return undefined;
 const name=match[1],file=resolve(assetRoot,name==='catalog-review'?'manifest.review.json':'manifest.json');
 const info=await stat(file),key=`${info.mtimeMs}:${info.size}`;
 let cached=catalogCache.get(name);
 if(!cached||cached.key!==key){
  const manifest=JSON.parse(await readFile(file,'utf8'));
  if(name==='catalog'&&manifest.review_only)throw new Error('Review manifest cannot supply a release catalog.');
  cached={key,catalog:createCatalog(manifest,{name})};catalogCache.set(name,cached);
 }
 const path=pathname.slice(1),catalog=cached.catalog;
 return path===`assets/${name}.json`?catalog.index:catalog.shards.get(path)||catalog.details.get(path);
}
export default defineConfig({
 root:'site',base:'./',build:{outDir:'../dist',emptyOutDir:true},
 plugins:[{name:'local-asset-preview',configureServer(server){server.middlewares.use(async(req,res,next)=>{
  const pathname=new URL(req.url,'http://localhost').pathname;
  if(!pathname.startsWith('/assets/'))return next();
  try{
   if(/^\/assets\/catalog(?:-review)?(?:\.json|\/)/.test(pathname)){
    const data=await catalogFile(pathname);
    if(!data){res.statusCode=404;res.end('Catalog file unavailable');return;}
    res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-cache');res.end(JSON.stringify(data));return;
   }
   const file=await realpath(resolve(assetRoot,decodeURIComponent(pathname.slice(8))));if(!file.startsWith(assetRoot+sep))return next();const data=await readFile(file);const type={'.json':'application/json','.glb':'model/gltf-binary','.png':'image/png'}[extname(file)]||'application/octet-stream';res.setHeader('Content-Type',type);res.end(data);
  }catch(error){
   if(/^\/assets\/catalog(?:-review)?(?:\.json|\/)/.test(pathname)){res.statusCode=error.code==='ENOENT'?404:500;res.setHeader('Content-Type','application/json');res.end(JSON.stringify({error:'Catalog unavailable'}));return;}
   next();
  }
 });}}]
});
