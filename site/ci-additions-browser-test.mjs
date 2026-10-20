/** Exact-selection, built-site acceptance. It never imports publication collectors. */
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import {createServer} from 'node:http';
import {readFile,writeFile,mkdir,stat,realpath} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {ADDITIONS_BROWSER_VERSION,ADDITIONS_BROWSER_KIND,ADDITIONS_BROWSER_PIN,ADDITIONS_VIEWPORTS,parseAddedModelIDs,selectAddedModels,assertAdditionsReport,assertAdditionsDesktopSource} from './ci-additions-browser-contract.mjs';

const root=resolve(process.env.GALLERY_DIR||'dist'),out=resolve(process.env.QA_OUTPUT_DIR||'qa/ci-additions-browser');
const prefix=process.env.SITE_BASE||'/lowpoly-vault/';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const git=(...args)=>execFileSync('git',args,{encoding:'utf8'}).trim();
const report={version:ADDITIONS_BROWSER_VERSION,kind:ADDITIONS_BROWSER_KIND,status:'running',selected_ids:[],actual_glb_ids:[],cases:[],page_errors:[],resource_errors:[],fallback_events:[],sequence_requests:0,served_output_only:true,visual_approval:false,formal_approval:false,
  limitations:['Functional Chromium/SwiftShader and emulated-touch checks only, not visual or formal publication approval.','Physical-device performance and physical GPU behavior are not established.']};
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.glb':'model/gltf-binary','.woff2':'font/woff2'};
let server,browser;
try{
  await mkdir(out,{recursive:true});
  const selectedIDs=parseAddedModelIDs(process.env.QA_ADDED_MODEL_IDS);
  assert(/^\/(?:[a-zA-Z0-9._-]+\/)*$/.test(prefix)&&!prefix.split('/').some(part=>part==='.'||part==='..'),'SITE_BASE must be a safe absolute directory prefix');
  assert(out!==root&&!out.startsWith(root+sep),'Browser reports must be outside the served build');
  assert.equal(await realpath(root),root,'Built output may not be a symlink');
  const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'),'utf8'));
  const assets=selectAddedModels(manifest,selectedIDs);
  const identity={source_commit:git('rev-parse','HEAD'),source_tree:git('rev-parse','HEAD^{tree}'),run_id:Number(process.env.GITHUB_RUN_ID),run_attempt:Number(process.env.GITHUB_RUN_ATTEMPT)};
  assert.equal(identity.source_commit,process.env.GITHUB_SHA,'Runner checkout differs from workflow source');
  assert(Number.isSafeInteger(identity.run_id)&&identity.run_id>0,'GITHUB_RUN_ID is required');
  assert(Number.isSafeInteger(identity.run_attempt)&&identity.run_attempt>0,'GITHUB_RUN_ATTEMPT is required');
  Object.assign(report,identity,{selected_ids:selectedIDs});
  const installed=JSON.parse(await readFile(resolve('node_modules/playwright-core/package.json'),'utf8'));
  const installedBrowsers=JSON.parse(await readFile(resolve('node_modules/playwright-core/browsers.json'),'utf8'));
  const pin=installedBrowsers.browsers.find(item=>item.name==='chromium');
  report.browser_pin={playwright:installed.version,chromium:pin?.browserVersion,revision:pin?.revision};
  assert.deepEqual(report.browser_pin,ADDITIONS_BROWSER_PIN,'Installed browser differs from protected browser pin');
  const actualIDs=new Set();
  let viewports=ADDITIONS_VIEWPORTS;
  if(process.env.QA_DESKTOP_REPORT){
    const source=JSON.parse(await readFile(resolve(process.env.QA_DESKTOP_REPORT),'utf8'));
    const desktop=assertAdditionsDesktopSource(source,{manifest,selectedIDs,identity});
    report.cases.push(...structuredClone(desktop.cases));
    for(const id of desktop.actual_glb_ids)actualIDs.add(id);
    report.desktop_source='validated-current-shard-strict-gpu';viewports=ADDITIONS_VIEWPORTS.filter(viewport=>viewport.touch);
  }else report.desktop_source='standalone-built-gallery';
  server=createServer(async(req,res)=>{
    try{
      const url=new URL(req.url,'http://localhost');assert(url.pathname.startsWith(prefix));
      let file=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');
      assert(file.startsWith(root+sep),'Request escaped built output');
      if((await stat(file)).isDirectory())file=resolve(file,'index.html');
      assert.equal(await realpath(file),file,'Build symlink rejected');assert((await stat(file)).isFile());
      res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream','Cache-Control':'no-store'}).end(await readFile(file));
    }catch{res.writeHead(404).end();}
  });
  await new Promise((done,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',done);});
  const base=`http://127.0.0.1:${server.address().port}${prefix}`;
  browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  report.chromium_version=browser.version();
  assert.equal(report.chromium_version,ADDITIONS_BROWSER_PIN.chromium,'Actual browser differs from protected Chromium pin');
  for(const viewport of viewports){
    const viewportConfig={width:viewport.width,height:viewport.height,hasTouch:viewport.touch,isMobile:viewport.touch};
    const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height},hasTouch:viewport.touch,isMobile:viewport.touch,deviceScaleFactor:1,reducedMotion:'reduce'});
    const page=await context.newPage(),observed=[],responseTasks=[];
    page.setDefaultTimeout(30000);page.setDefaultNavigationTimeout(60000);
    page.on('pageerror',error=>report.page_errors.push({viewport:viewport.name,message:error.message}));
    page.on('console',message=>{
      if(message.type()==='error')report.page_errors.push({viewport:viewport.name,message:message.text()});
      if(/Static fallback|Hover fallback/.test(message.text()))report.fallback_events.push({viewport:viewport.name,message:message.text()});
    });
    page.on('request',request=>{if(new URL(request.url()).pathname.includes('/turntables/'))report.sequence_requests++;});
    page.on('requestfailed',request=>report.resource_errors.push({viewport:viewport.name,url:request.url(),error:request.failure()?.errorText||'Request failed'}));
    page.on('response',response=>{
      if(response.status()>=400)report.resource_errors.push({viewport:viewport.name,url:response.url(),status:response.status()});
      if(new URL(response.url()).pathname.endsWith('.glb'))responseTasks.push((async()=>{
        const asset=assets.find(asset=>new URL(asset.glb,base).href===response.url());
        if(!asset)throw Error(`Unselected GLB requested: ${response.url()}`);
        assert(response.ok(),`${asset.id}: browser GLB response failed`);
        const bytes=await response.body();observed.push({id:asset.id,path:asset.glb,sha256:hash(bytes),bytes:bytes.length});actualIDs.add(asset.id);
      })().catch(error=>report.resource_errors.push({viewport:viewport.name,message:error.message})));
    });
    await page.addInitScript(()=>{
      window.__additionsFallbackEvents=[];
      new MutationObserver(records=>{for(const record of records)if(record.target.id==='detail'&&(record.target.dataset.state==='fallback'||record.oldValue==='fallback'))window.__additionsFallbackEvents.push({id:record.target.dataset.modelId,state:'fallback'});}).observe(document,{subtree:true,attributes:true,attributeFilter:['data-state'],attributeOldValue:true});
    });
    const waitCollection=()=>page.waitForFunction(()=>window.__gallery?.state.view==='collection'&&!document.body.classList.contains('mobile-detail'));
    const collectionState=()=>page.evaluate(()=>({url:location.href,scroll:document.querySelector('#wheel').scrollTop,ids:window.__gallery.state.results.map(asset=>asset.id)}));
    try{
      // A selected ID prevents desktop bootstrap from loading the old default model.
      await page.goto(new URL(`${viewport.touch?'zh-CN/':''}models/?model=${selectedIDs[0]}`,base).href);
      await page.waitForFunction(()=>window.__gallery?.models.length>0);
      assert.deepEqual((await page.evaluate(()=>window.__gallery.models.map(asset=>asset.id))).sort(),manifest.assets.map(asset=>asset.id).sort(),'Browser catalog differs from the published manifest');
      await page.waitForLoadState('networkidle');await Promise.all(responseTasks);
      if(viewport.touch){await page.locator('#mobile-back').tap();await waitCollection();await page.waitForLoadState('networkidle');}
      for(const asset of assets){
        const row={id:asset.id,viewport:viewport.name,viewport_config:viewportConfig,lang:viewport.lang,status:'running'};report.cases.push(row);
        await page.locator('#wheel').evaluate((wheel,id)=>{const index=window.__gallery.state.results.findIndex(asset=>asset.id===id);if(index<0)throw Error('Selected model missing from wheel');wheel.scrollTop=index*128;},asset.id);
        const card=page.locator(`#slots .slot[data-id="${asset.id}"]`);
        await card.scrollIntoViewIfNeeded();
        await page.waitForFunction(id=>{const image=document.querySelector(`#slots .slot[data-id="${id}"] img`);return image?.dataset.thumbnailState==='ready'&&image.complete&&image.naturalWidth>0;},asset.id);
        row.discovery=await card.locator('img').evaluate(async image=>{await image.decode();return{id:image.closest('.slot').dataset.id,poster_decoded:true,poster_width:image.naturalWidth,poster_height:image.naturalHeight};});
        await page.waitForLoadState('networkidle');
        const before=viewport.touch?await collectionState():null;
        if(viewport.touch){await card.tap();await page.locator('#mobile-interact').tap();}else await card.click();
        await page.waitForFunction(id=>document.querySelector('#detail')?.dataset.state==='ready'&&window.__gallery?.renderer?.stats.detailFirstFrameId===id,asset.id);
        row.detail=await page.evaluate(()=>{
          const gallery=window.__gallery,renderer=gallery.renderer,detail=document.querySelector('#detail');
          return{id:detail.dataset.modelId,selected_id:gallery.state.selected,title:document.querySelector('#info-content h2').textContent,first_frame_id:renderer.stats.detailFirstFrameId,renderer_id:renderer.detail.asset?.id,state:detail.dataset.state,renderer_status:renderer.stats.detailStatus,model_present:!!renderer.detail.model,live_bytes:renderer.detail.entry?.bytes,renderer_count:document.querySelectorAll('canvas.preview-renderer').length,context_lost:!!renderer.lost,gl_error:renderer.renderer.getContext().getError(),poster_source:document.querySelector('#detail-poster').dataset.source};
        });
        row.horizontal_overflow=await page.locator('html').evaluate(node=>node.scrollWidth>node.clientWidth+1);
        row.fallback=await page.locator('#retry').isVisible();
        row.navigation={detail_model:new URL(page.url()).searchParams.get('model')};
        row.downloads={};
        for(const format of ['glb','blend']){
          const link=page.locator(format==='glb'?'#download':'#blend'),href=await link.getAttribute('href');
          assert.equal(new URL(href,page.url()).href,new URL(asset[format],base).href,`${asset.id}: wrong ${format} download link`);
          const response=await page.request.get(href);assert(response.ok(),`${asset.id}: ${format} download failed`);
          const bytes=await response.body();row.downloads[format]={path:asset[format],sha256:hash(bytes),bytes:bytes.length};
          assert.equal(row.downloads[format].sha256,asset.sha256[format],`${asset.id}: ${format} download hash differs`);
        }
        await page.waitForLoadState('networkidle');await Promise.all(responseTasks);
        row.observed_glbs=observed.filter(file=>file.id===asset.id).map(({id,...file})=>file);
        row.screenshot=`${viewport.name}-${asset.id}.png`;await page.screenshot({path:resolve(out,row.screenshot)});
        if(viewport.touch){
          await page.locator('#mobile-back').tap();await waitCollection();await page.waitForLoadState('networkidle');
          const after=await collectionState();
          Object.assign(row.navigation,{back_to_collection:true,collection_model:new URL(after.url).searchParams.get('model'),collection_url_restored:after.url===before.url,wheel_visible:await page.locator('#wheel').isVisible(),scroll_restored:Math.abs(after.scroll-before.scroll)<1,results_restored:JSON.stringify(after.ids)===JSON.stringify(before.ids)});
          assert.equal(await page.locator('html').evaluate(node=>node.scrollWidth>node.clientWidth+1),false,'Mobile collection has horizontal overflow');
        }else assert(await page.locator('#wheel').isVisible(),'Desktop wheel missing after selection');
        row.status='pass';
      }
      await Promise.all(responseTasks);
      report.fallback_events.push(...(await page.evaluate(()=>window.__additionsFallbackEvents)).map(event=>({...event,viewport:viewport.name})));
    }finally{await context.close();}
  }
  report.actual_glb_ids=[...actualIDs].sort();report.status='pass';
  assertAdditionsReport(report,{manifest,selectedIDs,identity});
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally{
  await browser?.close();if(server?.listening)await new Promise(done=>server.close(done));
  await mkdir(out,{recursive:true});await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
}
