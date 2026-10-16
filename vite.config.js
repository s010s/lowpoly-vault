import { defineConfig } from 'vite';
import { readFile, realpath } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
const assetRoot=resolve('assets');
export default defineConfig({
 root:'site',base:'./',build:{outDir:'../dist',emptyOutDir:true},
 plugins:[{name:'local-asset-preview',configureServer(server){server.middlewares.use(async(req,res,next)=>{
  const pathname=new URL(req.url,'http://localhost').pathname;
  if(!pathname.startsWith('/assets/'))return next();
  try{const file=await realpath(resolve(assetRoot,decodeURIComponent(pathname.slice(8))));if(!file.startsWith(assetRoot+sep))return next();const data=await readFile(file);const type={'.json':'application/json','.glb':'model/gltf-binary','.png':'image/png'}[extname(file)]||'application/octet-stream';res.setHeader('Content-Type',type);res.end(data);}catch{next();}
 });}}]
});
