import {defineConfig} from 'vite';
import {resolve,extname} from 'node:path';
import {readFile} from 'node:fs/promises';
const repo=resolve(import.meta.dirname,'../..');
export default defineConfig({root:resolve(import.meta.dirname,'app'),base:'./',
 server:{host:'127.0.0.1',port:5197,fs:{allow:[repo]}},
 build:{outDir:resolve(import.meta.dirname,'build'),emptyOutDir:true},
 plugins:[{name:'existing-preview-assets',configureServer(server){server.middlewares.use(async(req,res,next)=>{
  const path=new URL(req.url,'http://local').pathname;
  if(!path.startsWith('/assets/'))return next();
  if(path.split('/').some(p=>p==='..')||/%2e|%2f/i.test(path))return next();
  try{const bytes=await readFile(resolve(repo,'.'+path));res.setHeader('Content-Type',({'.glb':'model/gltf-binary','.png':'image/png','.webp':'image/webp','.blend':'application/octet-stream'})[extname(path)]||'application/octet-stream');res.end(bytes);}catch{next();}
 });}}]});
