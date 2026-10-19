/** Actual Chromium identity/layout evidence. No model-artwork acceptance is implied. */
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
const root=resolve(process.env.GALLERY_DIR||'dist'),output=resolve(process.env.BRAND_QA_OUTPUT_DIR||'qa/brand-browser');
const prefix=process.env.SITE_BASE||'/lowpoly-vault/';
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml'};
const report={status:'running',source_commit:process.env.GITHUB_SHA||null,cases:[],errors:[],limitations:['UI screenshots use Chromium. Mobile is emulated; font fallback depends on the operating system. Existing gallery tests own WebGL/model/motion acceptance.']};
let server,browser;
await mkdir(output,{recursive:true});
try {
 let base=process.env.QA_BASE_URL;
 if(!base){
  server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');assert(url.pathname.startsWith(prefix));let file=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');assert(file===root||file.startsWith(root+sep));if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'}).end(await readFile(file));}catch{res.writeHead(404).end();}});
  await new Promise((done,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',done);});
  base=`http://127.0.0.1:${server.address().port}${prefix}`;
 }
 if(!base.endsWith('/'))base+='/';report.base=base;
 const manifest=await (await fetch(new URL('assets/manifest.json',base))).json();
 const model=manifest.assets.find(a=>a.id==='cooperoceras')||manifest.assets[0];assert(model);
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,chromiumSandbox:true,headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 report.browser=browser.version();
 async function capture(name,path,{width=1440,height=1000,javaScriptEnabled=true,colorScheme='light'}={}) {
  const row={name,path,status:'running'},context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,colorScheme,javaScriptEnabled});report.cases.push(row);
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  try{
   await page.goto(new URL(path,base).href);await page.locator('.vault-brand').waitFor({state:'visible'});
   if(javaScriptEnabled&&/^(zh-CN\/)?models\/(?:\?|$)/.test(path))await page.waitForFunction(()=>window.__gallery?.models.length>0,undefined,{timeout:45000});
   else if(javaScriptEnabled)await page.waitForFunction(()=>document.documentElement.dataset.application==='site');
   await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(500);
   row.style=await page.evaluate(()=>{
    const brand=document.querySelector('.vault-brand'),mark=brand.querySelector('.vault-mark'),header=brand.closest('header');
    const box=mark.getBoundingClientRect(),r=header.getBoundingClientRect(),font=getComputedStyle(brand),root=getComputedStyle(document.documentElement);
    return {wordmark:brand.textContent.replace(/\s+/g,' ').trim(),font:font.fontFamily,weight:font.fontWeight,mark:{width:box.width,height:box.height},header:{left:r.left,right:r.right},bodyWidth:document.documentElement.scrollWidth,viewport:innerWidth,accent:root.getPropertyValue('--vault-accent').trim(),favicon:document.querySelector('link[rel=icon]')?.href,brandHref:brand.href,icons:[...document.querySelectorAll('.vault-icon,.icon svg')].filter(el=>el.getBoundingClientRect().width).map(el=>({width:el.getBoundingClientRect().width,height:el.getBoundingClientRect().height}))};
   });
   assert.equal(row.style.wordmark,'LOWPOLY VAULT');assert.match(row.style.font,/Georgia/);assert.equal(row.style.weight,'400');
   assert(row.style.mark.width>=24&&row.style.mark.width<=32);assert.equal(row.style.mark.width,row.style.mark.height);
   assert(row.style.bodyWidth<=row.style.viewport+1,'No horizontal overflow');
   assert.equal(row.style.accent,colorScheme==='dark'?'#bfd1b6':'#305742');
   assert.equal(row.style.favicon,new URL('brand/favicon.svg',base).href);assert((await page.request.get(row.style.favicon)).ok());
   assert.equal(row.style.brandHref,new URL(path.startsWith('zh-CN/')?'zh-CN/':'',base).href);
   for(const icon of row.style.icons)assert(icon.width<=24&&icon.height<=24,'Utility icons stay bounded');
   await page.screenshot({path:resolve(output,name+'.png'),fullPage:true});
   assert.deepEqual(errors,[]);row.status='pass';
  }catch(error){row.status='fail';row.error=error.stack;report.errors.push({name,message:error.message});await page.screenshot({path:resolve(output,name+'-failure.png'),fullPage:true}).catch(()=>{});}
  finally{await context.close();}
 }
 for(const [locale,folder] of [['en',''],['zh','zh-CN/']])for(const [device,viewport] of [['desktop',{}],['mobile',{width:390,height:844}]]){
  await capture(`${locale}-${device}-home`,folder,viewport);
  await capture(`${locale}-${device}-list`,folder+'models/?model='+model.id,viewport);
  await capture(`${locale}-${device}-detail`,folder+'models/'+model.id+'/',viewport);
 }
 await capture('en-desktop-home-dark','',{colorScheme:'dark'});
 await capture('zh-mobile-detail-nojs','zh-CN/models/'+model.id+'/',{width:390,height:844,javaScriptEnabled:false});
 await capture('en-desktop-404','404.html',{javaScriptEnabled:false});
 const context=await browser.newContext({viewport:{width:320,height:160},deviceScaleFactor:2});const page=await context.newPage();
 await page.setContent(`<body style="margin:0;background:#f6f3ec;display:flex;align-items:center;justify-content:center;gap:24px;height:160px"><img src="${new URL('brand/favicon.svg',base)}" width="16" height="16" alt="16 pixel favicon"><img src="${new URL('brand/favicon.svg',base)}" width="32" height="32" alt="32 pixel favicon"><img src="${new URL('brand/favicon.svg',base)}" width="64" height="64" alt="64 pixel enlarged inspection"></body>`);
 await page.locator('img').evaluateAll(images=>Promise.all(images.map(img=>img.decode())));await page.screenshot({path:resolve(output,'favicon-16-32.png')});await context.close();
 assert(report.cases.every(row=>row.status==='pass'),report.errors.map(e=>e.name+': '+e.message).join('\n'));report.status='pass';
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally{await browser?.close();if(server)await new Promise(done=>server.close(done));await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}
