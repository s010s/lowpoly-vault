import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';
const root = resolve(process.env.GALLERY_DIR || 'dist');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/hover-reveal');
const baseline = process.env.BASELINE === '1';
const report = { baseline, cases: [], errors: [], limitations: ['Chromium software WebGL on CI; not a physical-device timing benchmark.'] };
const server = createServer(async (req, res) => {
  try {
    let path = resolve(root, decodeURIComponent(new URL(req.url, 'http://localhost').pathname.replace(/^\/lowpoly-vault\//, '')) || 'index.html');
    if (!path.startsWith(root + sep)) throw Error('Outside root');
    if ((await stat(path)).isDirectory()) path = resolve(path, 'index.html');
    res.setHeader('Content-Type', {'.js':'text/javascript','.css':'text/css','.html':'text/html','.json':'application/json','.png':'image/png','.webp':'image/webp','.glb':'model/gltf-binary'}[extname(path)] || 'application/octet-stream');
    res.end(await readFile(path));
  } catch { res.writeHead(404).end(); }
});
let browser;
try {
  await mkdir(output, {recursive:true}); await new Promise(r => server.listen(0, '127.0.0.1', r));
  browser = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-gpu-rasterization']});
  const base = `http://127.0.0.1:${server.address().port}/lowpoly-vault/models/`;
  async function test(name, fn, reducedMotion='no-preference') {
    const context = await browser.newContext({viewport:{width:1440,height:1000},reducedMotion});
    const page = await context.newPage(); page.on('pageerror', e => report.errors.push(e.message));
    const result = {name}; report.cases.push(result);
    try { await page.goto(base); await page.waitForFunction(()=>document.querySelector('#grid')?.ariaBusy==='false'); await page.mouse.move(1,1); await fn(page,result); result.pass=true; }
    catch(e) { result.pass=false; result.error=e.stack; }
    await context.close();
  }
  const selector = '#grid [data-id="natural-arch"]';
  async function hover(page) { await page.locator(selector).scrollIntoViewIfNeeded(); const r=await page.locator(selector+' .asset-image').boundingBox(); await page.mouse.move(r.x+r.width/2,r.y+r.height/2); }
  async function settled(page) { await page.waitForFunction(()=>document.querySelector('#grid [data-id="natural-arch"]')?.dataset.previewState==='ready'&&!document.querySelector('.model-hover-reveal')); }
  async function probe(page) {
    await page.evaluate(()=>{
      window.__revealFrames=[];window.__revealPNG=null;
      window.__vaultFrameProbe=({canvas,host})=>{
        if(host.closest('[data-id="natural-arch"]')){
          const side=Math.min(canvas.width,canvas.height),copy=document.createElement('canvas');copy.width=copy.height=Math.min(side,1024);
          copy.getContext('2d').drawImage(canvas,(canvas.width-side)/2,(canvas.height-side)/2,side,side,0,0,copy.width,copy.height);window.__revealUpper=copy;
        }
      };
      const sample=()=>{
        const card=document.querySelector('#grid [data-id="natural-arch"]'), host=card.querySelector('.asset-image'), c=host.querySelector('.model-hover-reveal'), live=host.querySelector('.model-canvas'), img=host.querySelector('img');
        const frame={state:card.dataset.previewState||'poster',time:performance.now(),canvases:document.querySelectorAll('.model-canvas').length,weight:c?Number(c.dataset.revealWeight):null,surfaceOpacity:c?Number(getComputedStyle(c).opacity):null,posterOpacity:Number(getComputedStyle(img).opacity),liveVisible:live&&getComputedStyle(live).visibility!=='hidden'};
        if(c){
          const w=c.width,h=c.height,ctx=c.getContext('2d'),actual=ctx.getImageData(0,0,w,h).data;
          const buffer=document.createElement('canvas');buffer.width=w;buffer.height=h;const b=buffer.getContext('2d');b.drawImage(img,0,0,w,h);const lower=b.getImageData(0,0,w,h).data;
          b.clearRect(0,0,w,h);b.drawImage(window.__revealUpper,0,0,w,h);const upper=b.getImageData(0,0,w,h).data;
          let error=0,count=0;
          for(let i=0;i<actual.length;i+=4){const a=lower[i+3]*(1-frame.weight)+upper[i+3]*frame.weight;error=Math.max(error,Math.abs(actual[i+3]-a));for(let k=0;k<3;k++){const expected=(lower[i+k]*lower[i+3]*(1-frame.weight)+upper[i+k]*upper[i+3]*frame.weight)/255;error=Math.max(error,Math.abs(actual[i+k]*actual[i+3]/255-expected));}if(actual[i+3])count++;}
          frame.maxPremultipliedError=error;frame.foreground=count;
          if(frame.weight>0&&frame.weight<1&&!window.__revealPNG)window.__revealPNG=c.toDataURL();
        }
        window.__revealFrames.push(frame);window.__revealRAF=requestAnimationFrame(sample);
      };sample();
    });
  }
  await test('cold-and-warm-alpha-correct-reveal',async(page,result)=>{
    for(const temperature of ['cold','warm']){
      await probe(page);await hover(page);await settled(page);
      const frames=await page.evaluate(()=>{cancelAnimationFrame(window.__revealRAF);return window.__revealFrames;});result[temperature]=frames;
      const partial=frames.filter(f=>f.weight>0&&f.weight<1);
      if(!baseline){assert(partial.length>=2,'At least two painted intermediate weights');assert(partial.every(f=>f.maxPremultipliedError<=3&&f.foreground>0),'Premultiplied alpha/color match analytic blend');assert(frames.every(f=>f.canvases<=1),'Single WebGL canvas');assert(frames.filter(f=>f.weight!==null).every(f=>!f.liveVisible&&f.posterOpacity===0&&f.surfaceOpacity===1),'Only blend surface displayed');}
      else assert.equal(partial.length,0,'Baseline has atomic swap');
      const png=await page.evaluate(()=>window.__revealPNG||null);if(png)await writeFile(resolve(output,temperature+'-blend.png'),Buffer.from(png.split(',')[1],'base64'));
      await page.screenshot({path:resolve(output,temperature+'-settled.png')});
      result[temperature+'GPU']=await page.evaluate(()=>({...window.__vaultGPU}));
      await page.mouse.move(1,1);await page.waitForTimeout(220);
    }
    assert.equal(result.warmGPU.networkRequests,result.coldGPU.networkRequests);assert.equal(result.warmGPU.parseCount,result.coldGPU.parseCount);
  });
  if(!baseline){
    await test('interrupt-leave-switch-and-detail',async(page,result)=>{
      await hover(page);await page.waitForSelector('.model-hover-reveal');await page.mouse.move(1,1);assert.equal(await page.locator('.model-hover-reveal,.model-canvas').count(),0);
      const other=page.locator('#grid .has-model-preview:not([data-id="natural-arch"])').first();await other.hover();
      await page.waitForFunction(()=>document.querySelector('#grid .has-model-preview:not([data-id="natural-arch"])[data-preview-state="ready"]'));
      assert.equal(await page.locator(selector+' .model-canvas,'+selector+' .model-hover-reveal').count(),0);
      await page.mouse.move(1,1);
      await page.evaluate(()=>{
        const watch=()=>{const c=document.querySelector('.model-hover-reveal');if(c&&Number(c.dataset.revealWeight)>0){window.__clickedWeight=Number(c.dataset.revealWeight);document.querySelector('#grid [data-id="natural-arch"]').click();}else requestAnimationFrame(watch);};watch();
      });await hover(page);await page.waitForFunction(()=>document.querySelector('#viewer-dialog').open&&document.querySelector('#canvas-host').dataset.modelState==='ready');
      result.clickedWeight=await page.evaluate(()=>window.__clickedWeight);assert(result.clickedWeight>0&&result.clickedWeight<1);assert.equal(await page.locator('.model-hover-reveal').count(),0);assert.equal(await page.locator('.model-canvas').count(),1);
      await page.locator('#close').click();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open&&!document.querySelector('.stage-flight'));
      assert.equal(await page.locator('.model-hover-reveal').count(),0);
    });
    await test('reduced-motion',async(page)=>{await probe(page);await hover(page);await settled(page);const frames=await page.evaluate(()=>{cancelAnimationFrame(window.__revealRAF);return window.__revealFrames;});assert(frames.every(f=>f.weight===null));},'reduce');
    await test('failed-fetch-keeps-poster',async(page)=>{await page.route('**/*.glb',route=>route.abort());await hover(page);await page.waitForFunction(()=>document.querySelector('#grid [data-id="natural-arch"]')?.dataset.previewState==='fallback');assert.equal(await page.locator('.model-hover-reveal').count(),0);assert.equal(await page.locator(selector+' img').evaluate(img=>Number(getComputedStyle(img).opacity)),1);});
  }
  report.pass=report.cases.every(c=>c.pass)&&!report.errors.length;
} catch(e) {report.pass=false;report.error=e.stack;}
finally {await browser?.close();server.close();await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));if(!report.pass)process.exitCode=1;}
