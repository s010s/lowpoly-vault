/** Check adopted taxonomy in the actual built bilingual gallery and stable URL. */
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile,stat,writeFile} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {chromium} from 'playwright';
const root=resolve('dist'),folder='production/creature36-20261031/evidence',prefix='/lowpoly-vault/';
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.svg':'image/svg+xml'};
const server=createServer(async(req,res)=>{try{const u=new URL(req.url,'http://localhost');assert(u.pathname.startsWith(prefix));let p=resolve(root,decodeURIComponent(u.pathname.slice(prefix.length))||'index.html');assert(p.startsWith(root+sep));if((await stat(p)).isDirectory())p=resolve(p,'index.html');res.setHeader('Content-Type',mime[extname(p)]||'application/octet-stream');res.end(await readFile(p));}catch{res.writeHead(404).end();}});
await new Promise(ok=>server.listen(0,'127.0.0.1',ok));
const origin=`http://127.0.0.1:${server.address().port}`,browser=await chromium.launch({executablePath:process.env.CAPTURE_CHROMIUM_EXECUTABLE||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']}),results=[];
try{
 for(const lang of ['en','zh-CN']){
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce',serviceWorkers:'block'}),page=await context.newPage(),errors=[];
  try{
   page.on('pageerror',e=>errors.push(e.message));await page.route('**/*',r=>new URL(r.request().url()).origin===origin?r.continue():r.abort());
   await page.goto(origin+prefix+(lang==='en'?'':'zh-CN/')+'models/?model=gastornis');
   await page.waitForFunction(()=>window.__gallery?.state.selected==='gastornis'&&document.querySelector('#detail')?.dataset.state==='ready');
   const title=await page.locator('#title').innerText(),expected=lang==='en'?'Diatryma gigantea':'Diatryma gigantea（始新世巨鸟）';assert.equal(title,expected);assert.deepEqual(errors,[]);
   const id=await page.evaluate(()=>window.__gallery.state.selected);assert.equal(id,'gastornis');
   const path=folder+`/website/gastornis${lang==='en'?'':'-zh-CN'}.png`;await page.screenshot({path});
   results.push({lang,stable_id:id,title,screenshot:path,status:'PASS'});
  }finally{await context.close();}
 }
 await writeFile(folder+'/label-browser.json',JSON.stringify({browser:browser.version(),results},null,2)+'\n');console.log('PASS bilingual Diatryma display with unchanged gastornis URL');
}finally{await browser.close();await new Promise(ok=>server.close(ok));}
