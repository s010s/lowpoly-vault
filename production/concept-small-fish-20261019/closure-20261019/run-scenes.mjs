// SPDX-License-Identifier: MIT
import {readFile,writeFile,mkdir,stat} from 'node:fs/promises';
import {createServer} from 'node:http';
import {resolve,dirname,extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {chromium} from 'playwright';
const here=dirname(fileURLToPath(import.meta.url)),root=resolve(here,'../../..');
const output=resolve(process.argv[2]||resolve(here,'software-webgl'));await mkdir(output,{recursive:true});
const hash=b=>createHash('sha256').update(b).digest('hex');
const inputHashes={};for(const id of ['metaspriggina','falcatus','pteraspis','dorypterus'])inputHashes[id]=hash(await readFile(resolve(here,'..',id,'r001/output',id+'.glb')));
const server=createServer(async(req,res)=>{try{
 const url=new URL(req.url,'http://localhost');if(url.pathname==='/favicon.ico'){res.writeHead(204).end();return;}
 const path=url.pathname==='/'?resolve(here,'scene.html'):resolve(root,'.'+decodeURIComponent(url.pathname));
 if(!path.startsWith(root+'/')||!(await stat(path)).isFile())throw Error('not found');
 res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.glb':'model/gltf-binary'})[extname(path)]||'application/octet-stream');res.end(await readFile(path));
}catch(e){res.writeHead(404).end(String(e));}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const errors=[],report={created_at:new Date().toISOString(),scope:'Functional 8/32-copy synthetic scene, Chromium software WebGL2; not target museum or physical GPU performance acceptance',browser:browser.version(),input_glb_sha256:inputHashes,tests:[],errors};
try{
 const page=await browser.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1});
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));
 await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.waitForFunction(()=>window.ready,null,{timeout:60000});
 for(const subject of ['metaspriggina','falcatus','pteraspis','dorypterus','mixed'])for(const count of [8,32])for(const view of ['hero','top']){
  const result=await page.evaluate(async a=>window.runScene(...a),[subject,count,view]);const name=`${subject}-${count}-${view}.png`;
  const bytes=await page.locator('canvas').screenshot({path:resolve(output,name)});result.screenshot={path:name,sha256:hash(bytes),bytes:bytes.length};
  result.software_renderer_confirmed=/SwiftShader/i.test(result.renderer);if(!result.software_renderer_confirmed)result.status='fail';report.tests.push(result);console.log(subject,count,view,result.status,result.render_calls,result.render_triangles);
 }
 await page.close();
}finally{await browser.close();await new Promise(r=>server.close(r));}
report.status=errors.length===0&&report.tests.length===20&&report.tests.every(x=>x.status==='pass')?'pass':'fail';
report.script_sha256=hash(await readFile(fileURLToPath(import.meta.url)));report.harness_sha256=hash(await readFile(resolve(here,'scene.html')));
await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');if(report.status!=='pass')process.exitCode=1;
