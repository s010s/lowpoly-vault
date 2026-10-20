/** Actual thumbnail-host geometry before and after enhancement, including the
 * mobile breakpoint. This does not recenter authored image pixels or labels. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';

export async function checkGalleryThumbnailAxis({browser,baseURL,root,output,report}){
 const html=await readFile(resolve(root,'models/index.html'),'utf8'),entry=html.match(/<script\b[^>]*\bsrc="([^"]+)"[^>]*>/)?.[1];
 assert(entry,'A real built entry module is required for first-paint gating');
 const snapshot=page=>page.evaluate(()=>{
  const wheel=document.querySelector('#wheel'),viewport=wheel.getBoundingClientRect();
  return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,scroll:wheel.scrollTop,rows:[...document.querySelectorAll('#slots .slot')].map(row=>{
   const host=row.querySelector('.slot-image'),bounds=host.getBoundingClientRect(),copy=row.querySelector('.slot-copy').getBoundingClientRect(),marker=row.querySelector('.slot-marker').getBoundingClientRect(),matrix=new DOMMatrixReadOnly(getComputedStyle(host).transform);
   return {id:row.dataset.id,visible:bounds.bottom>viewport.top&&bounds.top<viewport.bottom,x:bounds.x+bounds.width/2,y:bounds.y,width:bounds.width,height:bounds.height,scale:matrix.a,shift:matrix.e,copyX:copy.x,markerX:marker.x};
  }).filter(row=>row.visible).sort((a,b)=>a.y-b.y)};
 });
 const assertAxis=(state,reduced)=>{
  assert(state.rows.length>=3,'The actual wheel must expose several rows');
  assert(state.scrollWidth<=state.width,'No horizontal document overflow');
  if(state.width<=760||reduced){
   const centers=state.rows.map(row=>row.x);
   assert(Math.max(...centers)-Math.min(...centers)<.01,'Visible thumbnail hosts share one column X axis');
   assert(state.rows.every(row=>Math.abs(row.shift)<.001),'Mobile has no per-row horizontal displacement');
  }else assert(Math.max(...state.rows.map(row=>row.shift))>10,'Desktop preserves the original horizontal emphasis');
  if(reduced)assert(state.rows.every(row=>row.scale===1),'Reduced motion removes scaling');
 };
 for(const width of [320,390,760,761,1180])for(const reduced of [false,true]){
  const name=`thumbnail-axis-${width}${reduced?'-reduced':''}`,result={name,status:'running'};report.cases.push(result);
  const context=await browser.newContext({viewport:{width,height:844},isMobile:width<=760,hasTouch:width<=760,reducedMotion:reduced?'reduce':'no-preference'}),page=await context.newPage();
  page.on('pageerror',error=>report.errors.push({case:name,message:error.message}));
  let release;const gate=new Promise(done=>release=done);
  await page.route(new URL(entry,baseURL).href,async route=>{await gate;await route.continue().catch(()=>{});});
  try{
   await page.goto(new URL('models/',baseURL).href,{waitUntil:'commit'});
   await page.waitForFunction(()=>document.querySelector('.gallery-static')?.dataset.startupInitialized==='true');
   const native=await snapshot(page);assertAxis(native,reduced);
   release();await page.waitForFunction(()=>window.__gallery?.models.length>0);
   await page.waitForFunction(()=>[...document.querySelectorAll('.slot-image img[data-thumbnail-visible=true]')].length>=3&&[...document.querySelectorAll('.slot-image img[data-thumbnail-visible=true]')].every(image=>image.dataset.thumbnailState==='ready'));
   const enhanced=await snapshot(page);assertAxis(enhanced,reduced);
   assert.deepEqual(enhanced.rows.map(row=>row.id),native.rows.map(row=>row.id),'Enhancement keeps the same visible models');
   for(let i=0;i<native.rows.length;i++)for(const key of ['x','y','width','height','scale','shift','copyX','markerX'])assert(Math.abs(native.rows[i][key]-enhanced.rows[i][key])<1,`No thumbnail or label ${key} jump at enhancement`);
   if(width<=760){
    const centered=await page.locator('.slot[data-browse-center=true]').getAttribute('data-id');
    await page.locator(`.slot[data-id="${centered}"]`).tap();await page.waitForFunction(()=>document.body.classList.contains('mobile-detail'));
    await page.locator('#mobile-back').tap();await page.waitForFunction(()=>window.__gallery.state.view==='collection'&&!document.body.classList.contains('mobile-detail'));
    const returned=await snapshot(page);assertAxis(returned,reduced);assert(Math.abs(returned.scroll-enhanced.scroll)<1);assert.deepEqual(returned.rows.map(row=>row.id),enhanced.rows.map(row=>row.id));
    await page.locator('#wheel').evaluate(el=>{el.scrollTop=63*128+37;});await page.waitForTimeout(250);assertAxis(await snapshot(page),reduced);
   }
   // Repeated responsive transitions exercise the mounted renderer's existing
   // resize path without introducing a second observer or scroll controller.
   if(width===390&&!reduced){
    for(const next of [761,760,320,390]){await page.setViewportSize({width:next,height:844});await page.waitForTimeout(150);assertAxis(await snapshot(page),false);}
    await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(50);assertAxis(await snapshot(page),true);
    await page.emulateMedia({reducedMotion:'no-preference'});await page.waitForTimeout(50);assertAxis(await snapshot(page),false);
   }
   result.native=native;result.enhanced=enhanced;result.status='pass';await page.screenshot({path:resolve(output,`${name}.png`)});
  }catch(error){result.status='fail';result.error=error.stack;await page.screenshot({path:resolve(output,`${name}-failure.png`)}).catch(()=>{});}
  finally{release();await context.close();}
 }
}
