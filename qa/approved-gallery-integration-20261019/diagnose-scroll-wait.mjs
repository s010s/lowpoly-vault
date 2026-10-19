import {chromium} from 'playwright';
import {createServer} from 'node:http';
import {readFile,writeFile,mkdir,stat} from 'node:fs/promises';
import {resolve,sep,extname} from 'node:path';
const root=resolve('dist'),prefix='/lowpoly-vault/',out=resolve('qa/approved-gallery-integration-20261019/scroll-wait-diagnostic');await mkdir(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{let file=resolve(root,decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(prefix.length)||'index.html');if(!file.startsWith(root+sep))throw Error();if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'}).end(await readFile(file));}catch{res.writeHead(404).end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-gpu-rasterization']});
const rows=[];
try{
 for(let i=0;i<5;i++){
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage();
  await page.goto(`http://127.0.0.1:${server.address().port}${prefix}models/?model=cooperoceras`);await page.waitForFunction(()=>document.querySelector('#detail')?.dataset.state==='ready');
  const snapshot=()=>page.evaluate(()=>({time:performance.now(),scroll:document.querySelector('#wheel').scrollTop,state:window.__gallery.settler.state,selected:window.__gallery.state.selected,center:window.__gallery.state.center}));
  const before=await snapshot(),box=await page.locator('#wheel').boundingBox();await page.mouse.move(box.x+box.width*.3,box.y+box.height*.5);await page.mouse.wheel(0,900);
  await page.waitForFunction(()=>window.__gallery.settler.state==='idle'&&document.querySelector('#wheel').scrollTop>0);
  const afterOriginalWait=await snapshot();await page.waitForTimeout(250);const after250ms=await snapshot();
  await page.waitForFunction(before=>window.__gallery.settler.state==='idle'&&document.querySelector('#wheel').scrollTop>before,before.scroll);
  const afterChangedAndIdle=await snapshot();rows.push({run:i+1,before,afterOriginalWait,after250ms,afterChangedAndIdle,original_assertion_would_pass:afterOriginalWait.scroll>before.scroll});
  await page.screenshot({path:resolve(out,`settled-${i+1}.png`)});await context.close();
 }
 console.log(JSON.stringify(rows,null,2));
}finally{await browser.close();await new Promise(r=>server.close(r));await writeFile(resolve(out,'timing.json'),JSON.stringify({source_sha:process.env.GITHUB_SHA,browser:browser.version(),rows},null,2)+'\n');}
