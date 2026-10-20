/** Real mobile navigation + image/GLB request regressions against built files. */
import assert from 'node:assert/strict';
import {resolve} from 'node:path';
import {writeFile} from 'node:fs/promises';
export async function checkMobileGallery({browser,baseURL,output,report,assets}){
 for(const width of [390,320]){
  const name=`mobile-navigation-${width}`,row={name,status:'running'};report.cases.push(row);
  const context=await browser.newContext({viewport:{width,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'}),page=await context.newPage(),trace=[];
  page.on('request',request=>{if(/\.(?:glb|png|webp)(?:\?|$)/.test(request.url()))trace.push({event:'request',url:request.url(),time:Date.now()});});
  page.on('requestfailed',request=>trace.push({event:'failed',url:request.url(),reason:request.failure()?.errorText,time:Date.now()}));
  page.on('pageerror',error=>report.errors.push({case:name,message:error.message}));
  const ready=()=>page.waitForFunction(()=>window.__gallery?.models.length>0);
  const collection=()=>page.waitForFunction(()=>window.__gallery?.state.view==='collection'&&!document.body.classList.contains('mobile-detail'));
  const snapshot=()=>page.evaluate(()=>{const wheel=document.querySelector('#wheel'),r=wheel.getBoundingClientRect();return{ids:window.__gallery.state.results.map(a=>a.id),scroll:wheel.scrollTop,slots:document.querySelectorAll('#slots .slot').length,visible:[...document.querySelectorAll('#slots .slot')].filter(el=>{const b=el.getBoundingClientRect();return b.bottom>r.top&&b.top<r.bottom;}).map(el=>el.dataset.id),url:location.href};});
  try{
   await page.goto(new URL('models/',baseURL).href);await ready();await collection();await page.waitForTimeout(250);
   assert.equal(new URL(page.url()).searchParams.has('model'),false,'Collection URL does not falsely identify a detail');
   const initial=await snapshot();assert.equal(initial.ids.length,assets.length);assert(initial.visible.length>=3);await page.screenshot({path:resolve(output,`${name}-collection.png`)});
   await page.locator('#slots [data-id="cooperoceras"]').tap();await page.waitForFunction(()=>document.body.classList.contains('mobile-detail'));assert.equal(new URL(page.url()).searchParams.get('model'),'cooperoceras');await page.screenshot({path:resolve(output,`${name}-detail.png`)});
   await page.locator('#mobile-back').tap();await collection();const back=await snapshot();assert.deepEqual(back.ids,initial.ids);assert(back.visible.length>=3,'Returning must remeasure a real multi-row wheel');assert(Math.abs(back.scroll-initial.scroll)<1);assert.equal(back.url,initial.url);await page.screenshot({path:resolve(output,`${name}-returned.png`)});
   await page.goForward();await page.waitForFunction(()=>document.body.classList.contains('mobile-detail'));assert.equal(new URL(page.url()).searchParams.get('model'),'cooperoceras');await page.goBack();await collection();
   await page.locator('#filters').tap();await page.locator('#filter-form input[data-group="category"][value="plants"]').check();await page.locator('#filter-apply').tap();await page.waitForFunction(()=>window.__gallery.state.facets.category.includes('plants'));
   await page.locator('#wheel').evaluate(el=>{el.scrollTop=128*4;});await page.waitForTimeout(250);const filtered=await snapshot();assert(filtered.ids.length>1&&filtered.ids.length<assets.length);const id=filtered.visible[Math.floor(filtered.visible.length/2)];
   await page.locator(`#slots [data-id="${id}"]`).tap();await page.waitForFunction(()=>document.body.classList.contains('mobile-detail'));assert.equal(new URL(page.url()).searchParams.get('category'),'plants');await page.goBack();await collection();const returned=await snapshot();assert.deepEqual(returned.ids,filtered.ids);assert(Math.abs(returned.scroll-filtered.scroll)<1);assert.equal(returned.url,filtered.url);
   await page.goForward();await page.waitForFunction(()=>document.body.classList.contains('mobile-detail'));await page.reload();await ready();assert(await page.locator('.workspace').isVisible());assert.equal(new URL(page.url()).searchParams.get('model'),id);await page.locator('#mobile-back').tap();await collection();assert.equal(new URL(page.url()).searchParams.get('category'),'plants');assert.equal(new URL(page.url()).searchParams.has('model'),false);assert.deepEqual((await snapshot()).ids,filtered.ids);
   assert(!trace.some(item=>new URL(item.url).pathname.endsWith('.glb')),'Mobile browse/open/back/reload remains image-only until explicit 3D interaction');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Narrow mobile has no horizontal overflow');
   row.initial=initial;row.returned=back;row.filtered=filtered;row.status='pass';
  }catch(error){row.status='fail';row.error=error.stack;await page.screenshot({path:resolve(output,`${name}-failure.png`)}).catch(()=>{});}
  finally{await writeFile(resolve(output,`${name}-network.json`),JSON.stringify(trace,null,2));await context.close();}
 }
 const name='mobile-loading-budget',row={name,status:'running'};report.cases.push(row);
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),page=await context.newPage(),trace=[];
 page.on('request',request=>{if(/\.(?:glb|png|webp)(?:\?|$)/.test(request.url()))trace.push({event:'request',url:request.url(),time:Date.now()});});
 page.on('requestfailed',request=>trace.push({event:'failed',url:request.url(),reason:request.failure()?.errorText,time:Date.now()}));
 page.on('pageerror',error=>report.errors.push({case:name,message:error.message}));
 let release;const gate=new Promise(done=>release=done);
 try{
  await page.goto(new URL('models/',baseURL).href);await page.waitForFunction(()=>window.__gallery?.models.length>0);await page.waitForTimeout(350);
  const before=trace.length;
  await page.evaluate(async()=>{const wheel=document.querySelector('#wheel');for(let i=40;i<175;i+=3){wheel.scrollTop=i*128;await new Promise(done=>requestAnimationFrame(done));}});await page.waitForTimeout(350);
  const fast=trace.slice(before).filter(item=>item.event==='request');assert(fast.length<45,'Fast traversal does not eagerly request each passing model image');assert(!trace.some(item=>new URL(item.url).pathname.endsWith('.glb')));
  await page.route('**/gallery/posters/*-wheel.png',async route=>{await gate;await route.continue().catch(()=>{});});
  await page.locator('#wheel').evaluate(el=>{el.scrollTop=65*128;});await page.waitForTimeout(250);
  const pending='.slot-image img[data-thumbnail-visible=true]:is([data-thumbnail-state=pending],[data-thumbnail-state=loading],[data-thumbnail-state=decoding])+.thumbnail-placeholder';
  await page.locator(pending).first().waitFor({state:'visible'});
  const placeholder=await page.locator(pending).first().evaluate(el=>({opacity:getComputedStyle(el).opacity,color:getComputedStyle(el).color,faces:[...el.querySelectorAll('.thumbnail-placeholder-face')].map(face=>getComputedStyle(face).backgroundColor),animation:getComputedStyle(el.firstElementChild).animationPlayState,imageVisibility:getComputedStyle(el.previousElementSibling).visibility}));
  assert.equal(placeholder.opacity,'1');assert.equal(placeholder.imageVisibility,'hidden');assert(placeholder.faces.every(color=>color==='rgba(0, 0, 0, 0)'));assert.equal(placeholder.animation,'running');
  await page.screenshot({path:resolve(output,'mobile-thumbnail-wireframe-pending.png')});row.placeholder=placeholder;
  await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.locator(pending).first().evaluate(el=>getComputedStyle(el.firstElementChild).animationName),'none');await page.emulateMedia({reducedMotion:'no-preference'});
  await page.locator('#wheel').evaluate(el=>{el.scrollTop=90*128;});await page.waitForTimeout(250);
  const budget=await page.evaluate(()=>window.__gallery.thumbnailStats);assert(budget.maxActive<=3);assert(budget.cancelled>0,'Offscreen pending thumbnails are cancelled');release();
  await page.waitForFunction(()=>[...document.querySelectorAll('.slot-image img[data-thumbnail-visible=true]')].every(image=>image.dataset.thumbnailState==='ready'||image.dataset.thumbnailState==='error'));await page.waitForTimeout(180);
  assert.equal(await page.locator('.thumbnail-placeholder:visible').count(),0,'Decoded thumbnails replace the placeholder without leaving animation visible');
  assert(await page.locator('.slot-image img[data-thumbnail-visible=true][data-thumbnail-state=ready]').first().isVisible(),'Decoded model image is visible');
  await page.screenshot({path:resolve(output,'mobile-thumbnail-wireframe-loaded.png')});
  row.fastRequests=fast.length;row.budget=budget;row.scrollGLBs=0;
  let requestedGLB,releaseGLB;const requested=new Promise(done=>requestedGLB=done),glbGate=new Promise(done=>releaseGLB=done);
  await page.route('**/*.glb',async route=>{requestedGLB();await glbGate;await route.continue().catch(()=>{});});
  try{
   await page.evaluate(id=>window.__gallery.choose(id),assets[0].id);await page.locator('#mobile-interact').tap();await requested;
   await page.locator('#mobile-back').tap();await page.waitForFunction(()=>window.__gallery.state.view==='collection'&&!document.body.classList.contains('mobile-detail'));
   await page.waitForFunction(()=>window.__gallery.renderer.stats.aborted>0);
   const stopped=await page.evaluate(()=>({status:window.__gallery.renderer.stats.detailStatus,enabled:window.__gallery.renderer.controls.enabled}));
   assert.equal(stopped.status,'suspended');assert.equal(stopped.enabled,false);assert.equal(new URL(page.url()).searchParams.has('model'),false);
   releaseGLB();await page.waitForTimeout(150);assert.equal(await page.locator('.workspace').isVisible(),false);row.backCancelledGLB=true;
  }finally{releaseGLB();}
  row.status='pass';await page.screenshot({path:resolve(output,`${name}.png`)});
 }catch(error){row.status='fail';row.error=error.stack;await page.screenshot({path:resolve(output,`${name}-failure.png`)}).catch(()=>{});}
 finally{release();await writeFile(resolve(output,`${name}-network.json`),JSON.stringify(trace,null,2));await context.close();}
}
