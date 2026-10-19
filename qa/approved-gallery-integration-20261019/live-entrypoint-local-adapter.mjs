// Run the existing deployment scenario against this unshipped local build.
// Only transport/provenance labels and data-module import resolution change.
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile,stat,writeFile,mkdir} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const root=resolve('dist'),basePath='/lowpoly-vault/';
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.webp':'image/webp','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const path=decodeURIComponent(new URL(req.url,'http://localhost').pathname);assert(path.startsWith(basePath));let file=resolve(root,path.slice(basePath.length)||'index.html');assert(file.startsWith(root+sep));if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'}).end(await readFile(file));}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}${basePath}`,original=await readFile('site/live-release-browser-test.mjs','utf8');
assert(original.includes("const base='https://s010s.github.io/lowpoly-vault/'"));
let source=original.replace("const base='https://s010s.github.io/lowpoly-vault/'",`const base=${JSON.stringify(base)}`)
 .replace('Actual public Pages origin in Chromium SwiftShader','Exact unpublished build on local cloud loopback in Chromium SwiftShader; not public Pages acceptance')
 .replace(/from '(\.\/[^']+)'/g,(_,path)=>`from '${pathToFileURL(resolve('site',path)).href}'`)
 .replace("from 'playwright'",`from '${pathToFileURL(resolve('node_modules/playwright/index.mjs')).href}'`);
try{
 const output=resolve(process.env.QA_OUTPUT_DIR);await mkdir(output,{recursive:true});
 await writeFile(resolve(output,'adapter-provenance.json'),JSON.stringify({source_sha:process.env.GITHUB_SHA,original_entrypoint:'site/live-release-browser-test.mjs',original_sha256:createHash('sha256').update(original).digest('hex'),base,changes:['Only substitute hard-coded public origin with local loopback','Resolve relative imports for data module','Correct public-origin limitation label'],runtime_code_unchanged:true},null,2)+'\n');
 await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
}finally{await new Promise(r=>server.close(r));}
