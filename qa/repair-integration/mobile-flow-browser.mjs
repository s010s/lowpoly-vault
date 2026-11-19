/** Compare two loopback builds with identical assets before and after the responsive mobile detail flow. */
import {chromium} from 'playwright';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const out=process.env.QA_OUTPUT_DIR,originA=process.env.QA_ORIGINAL,originB=process.env.QA_CANDIDATE;
assert(out&&originA&&originB,'Set QA_ORIGINAL, QA_CANDIDATE and QA_OUTPUT_DIR');
assert([originA,originB].every(x=>['127.0.0.1','localhost'].includes(new URL(x).hostname)),'Use loopback QA builds');
const assets=JSON.parse(await readFile('assets/manifest.json')).assets;
const app=n=>assets.find(x=>x.id===n), hash=x=>createHash('sha256').update(x).digest('hex');
const core=[
 ['paratingia',667,375,'en'],['araucaria-mirabilis',667,375,'zh'],['araucaria-mirabilis',320,667,'zh'],
 ['paratingia',740,844,'en'],['confuciusornis',390,844,'en'],['confuciusornis',1440,1000,'en']
];
const assetsMore=[
 ['paratingia',441,800,'en'],['paratingia',440,801,'en'],['paratingia',412,800,'en'],
 ['spinolestes',370,710,'en'],['spinolestes',740,390,'en'],['flint-nodule',370,710,'en'],
 ['araucaria-mirabilis',320,667,'zh',20],['sawdonia',390,740,'zh',20],
];
const samples=[
 ['cambroraster',360,700,'en'],['cambroraster',370,690,'en'],['cambroraster',370,710,'en'],['cambroraster',390,740,'en'],
 ['cooksonia',370,710,'en'],['flint-nodule',370,710,'en'],
 ['spinolestes',360,700,'en'],['spinolestes',370,690,'en'],['spinolestes',370,710,'en'],
];
const target=({extra:assetsMore,samples})[process.env.QA_GROUP]||core;
await mkdir(out,{recursive:true});
const b=await chromium.launch({headless:true,chromiumSandbox:true});const results=[];
const stable=(box,after)=>assert.deepEqual(box,after);
const download=async(p,sel,want)=>{const w=p.waitForEvent('download');await p.locator(sel).tap();const d=await w;const result=hash(await readFile(await d.path()));assert.equal(result,want);await d.delete();return result;};
try{
  for(const [id,width,height,lang,inset=0] of target){
  const compact=width<=760;
  const row={id,width,height,lang,inset,compact};
  for(const [label,base] of [['before',originA],['probe',originB]]){
   const phone=width<761,p=await b.newPage({viewport:{width,height},isMobile:phone,hasTouch:phone,acceptDownloads:true});p.setDefaultTimeout(16000);
   const errors=[],responses=[],a=app(id);
   if(inset){const cd=await p.context().newCDPSession(p);await cd.send('Emulation.setSafeAreaInsetsOverride',{insets:{top:12,right:4,left:4,bottom:inset}});}
   await p.context().grantPermissions(['clipboard-read','clipboard-write']);
   p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>responses.push(r));
   let open,requested;const gate=new Promise(r=>open=r),seen=new Promise(r=>requested=r);await p.route('**/'+a.glb,async r=>{requested();await gate;await r.continue()});
   const measure=()=>p.evaluate(()=>{
    const q=s=>document.querySelector(s),R=s=>{const r=q(s).getBoundingClientRect().toJSON();for(const k of ['y','top','bottom'])r[k]+=scrollY;for(const k of ['x','left','right'])r[k]+=scrollX;return r;},coords={stage:R('#detail'),title:R('#title'),heading:R('.heading'),button:R('#mobile-interact'),back:R('#mobile-back'),tools:R('.tools'),download:R('.download-card'),links:['#download','#blend','#credits'].map(R),buttons:['#wireframe','#compare','#reset'].map(R)};
    coords.subtitle=R('#subtitle'); const p=q('#detail-poster');const poster={rect:R('#detail-poster'),source:p.currentSrc,state:p.dataset.state,naturalWidth:p.naturalWidth};const st=q('#detail'),rv=window.__preview?.renderer?.detail;
    let pose=null,bounds=null,vertices=null;
    if(st.dataset.state==='ready'&&rv?.model){
     pose=rv.orientation.quaternion.toArray();
     bounds={left:Infinity,top:Infinity,right:-Infinity,bottom:-Infinity};
     vertices={title:0,subtitle:0,heading:0,button:0,back:0,tools:0,download:0,outside:0};
     const {stage}=coords,v=rv.camera.position.clone();
     rv.model.updateWorldMatrix(true,true);rv.camera.updateMatrixWorld(true);
     rv.model.traverse(o=>{if(!o.isMesh)return; const att=o.geometry.attributes.position;
      for(let i=0;i<att.count;i++){
       v.set(att.getX(i),att.getY(i),att.getZ(i)).applyMatrix4(o.matrixWorld).project(rv.camera);
       const x=stage.left+(v.x+1)*stage.width/2,y=stage.top+(1-v.y)*stage.height/2;
       for(const k of Object.keys(vertices)){
        const r=coords[k==='outside'?'stage':k];const inside=r.width>0&&x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom;
        if(k==='outside'?!inside:inside)vertices[k]++;
       }
       bounds.left=Math.min(x,bounds.left);bounds.right=Math.max(x,bounds.right);bounds.top=Math.min(y,bounds.top);bounds.bottom=Math.max(y,bounds.bottom);
      }
     });
    }
    return {coords,poster,pose,bounds,vertices,scroll:{width:innerWidth,height:innerHeight,viewHeight:document.documentElement.clientHeight,documentHeight:document.documentElement.scrollHeight,y:scrollY},state:st.dataset.state,labels:['#wireframe','#compare','#reset'].map(s=>q(s).textContent.trim()),interact:q('#mobile-interact').textContent.trim()};
   });
   try{
    await p.goto(base+(lang==='zh'?'/zh-CN/models/':'/models/'));await p.locator('#search').fill(id);
    const option=p.locator('#option-'+id);if(phone)await option.tap();else await option.click();
    await p.waitForFunction(id=>{const q=document.querySelector('#detail-poster');return q?.dataset.modelId===id&&q.dataset.state==='ready'&&q.naturalWidth>0&&!document.querySelector('.continuity-poster');},id);
    const insetPixels=inset?await p.evaluate(()=>{const probe=document.createElement('div');probe.style.paddingBottom='env(safe-area-inset-bottom,0px)';document.body.append(probe);const v=parseFloat(getComputedStyle(probe).paddingBottom);probe.remove();return v;}):0;assert.equal(insetPixels,inset);
    const prefix=`${out}/${id}-${width}x${height}-${lang}-inset${inset}-${label}`;
    const poster=await measure();if(phone)await p.locator('#mobile-interact').tap();
    await Promise.race([seen,new Promise((_,r)=>setTimeout(()=>r(Error('GLB not requested')),8000))]);
    await p.waitForFunction(id=>{const q=document.querySelector('#detail-poster');return q?.dataset.modelId===id&&q.dataset.state==='ready'&&q.naturalWidth>0&&getComputedStyle(q).visibility==='visible'&&!document.querySelector('.continuity-poster');},id);
    const held=await measure();assert.equal(held.state,'loading');await p.screenshot({path:prefix+'-held.png'});
    open();await p.waitForFunction(id=>window.__preview?.renderer?.detail?.asset?.id===id&&document.querySelector('#detail').dataset.state==='ready',id);
    const ready=await measure();await p.screenshot({path:prefix+'-ready.png',fullPage:height<450});
    const fromHTTP=async path=>hash(await responses.findLast(r=>r.url().endsWith('/'+path)).body());const sha={glb:await fromHTTP(a.glb),poster:await fromHTTP(a.galleryPosters.detail)};
    assert.deepEqual(sha,{glb:a.sha256.glb,poster:a.sha256.preview});
    assert.deepEqual(ready.pose,[0,0,0,1]);
    for(const k of ['stage','heading','tools','download','back','button'])stable(held.coords[k],ready.coords[k]);
    stable(held.poster.rect,ready.poster.rect);
    const clickTargets=await p.evaluate(()=>['#mobile-back','#mobile-interact','#download','#blend','#credits'].map(sel=>{const el=document.querySelector(sel),r=el.getBoundingClientRect();return {sel,visible:r.width>0&&r.height>0&&r.left>=0&&r.top>=0&&r.right<=innerWidth&&r.bottom<=innerHeight,clickable:el.contains(document.elementFromPoint(r.left+r.width/2,r.top+r.height/2))};}));
    const result={poster,held,ready,sha,errors,clickTargets,insetPixels};
    if(label==='probe'&&phone){
     const overlap=(a,b)=>a.width&&b.width&&a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom;
     stable(poster.coords.tools,held.coords.tools);stable(poster.coords.download,held.coords.download);
     result.diagnostics={collision:Object.fromEntries(Object.entries(ready.vertices).filter(([,n])=>n)),topButtonsOverlap:!!overlap(ready.coords.back,ready.coords.button),toolBoundsOverlap:!!overlap(ready.coords.tools,ready.bounds),toolsCardOverlap:!!overlap(ready.coords.tools,ready.coords.download),allTargetsInitiallyVisible:clickTargets.every(x=>x.visible&&x.clickable)};
     const unsafe=(r)=>r.width<44||r.height<44;
     result.diagnostics.smallToolTargets=[...ready.coords.buttons,ready.coords.button,ready.coords.back].filter(unsafe).length;
     assert.deepEqual(result.diagnostics.collision,{});assert(!result.diagnostics.topButtonsOverlap&&!result.diagnostics.toolBoundsOverlap&&!result.diagnostics.toolsCardOverlap&&!result.diagnostics.smallToolTargets);
     const reachable=async sel=>{
      const item=p.locator(sel);await item.scrollIntoViewIfNeeded();
      return item.evaluate(el=>{const r=el.getBoundingClientRect();return r.width>0&&r.height>0&&r.left>=0&&r.top>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&el.contains(document.elementFromPoint(r.left+r.width/2,r.top+r.height/2));});
     };
     result.reachability={};
     for(const sel of ['#mobile-back','#mobile-interact','#download','#blend','#credits'])result.reachability[sel]=await reachable(sel);
     assert.ok(Object.values(result.reachability).every(Boolean),JSON.stringify(result.reachability));
     assert.deepEqual(ready.labels,lang==='zh'?['线框','尺寸对比','重置']:['Wireframe','Compare size','Reset']);
     assert.equal(ready.interact,lang==='zh'?'退出交互':'Exit interaction');
     await p.locator('#wireframe').tap();assert.equal(await p.locator('#wireframe').getAttribute('aria-pressed'),'true');
     await p.locator('#detail').focus();await p.keyboard.press('ArrowRight');await p.waitForFunction(()=>__preview.renderer.detail.orientation.quaternion.toArray().some((v,i)=>Math.abs(v-(i===3?1:0))>.001));
     await p.locator('#wireframe').focus();
     let order=['wireframe'];
     for(let i=0;i<4;i++){await p.keyboard.press('Tab');order.push(await p.evaluate(()=>document.activeElement.id));}
     assert.deepEqual(order.filter(k=>k!=='compare').slice(0,4),['wireframe','reset','download','blend']);
     await p.locator('#reset').tap();await p.waitForFunction(()=>__preview.renderer.detail.orientation.quaternion.toArray().every((v,i)=>Math.abs(v-(i===3?1:0))<.001));
     result.tabOrder=order;
     await p.locator('#credits').focus();assert.equal(await p.evaluate(()=>document.activeElement.id),'credits');
     await p.keyboard.press('Enter');await p.waitForFunction(()=>document.querySelector('#credits').dataset.copyState==='success');
     result.creditsKeyboard=true;
     await p.locator('#mobile-interact').scrollIntoViewIfNeeded();
     await p.locator('#mobile-interact').focus();
     assert.equal(await p.evaluate(()=>document.activeElement.id),'mobile-interact');

      result.downloads={glb:await download(p,'#download',a.sha256.glb),blend:await download(p,'#blend',a.sha256.blend)};
     await p.locator('#mobile-interact').tap();await p.waitForFunction(()=>document.querySelector('#detail').dataset.state==='static');
     result.exitPassed=true;
     const after=await measure();
     stable(ready.coords.stage,after.coords.stage);stable(ready.coords.tools,after.coords.tools);stable(ready.coords.download,after.coords.download);
     await p.locator('#mobile-back').tap();await p.locator('#search').waitFor({state:'visible'});

    }
    assert.deepEqual(errors,[]);row[label]=result;
   }catch(error){row[label+'_error']=String(error);row[label+'_debug']=await measure().catch(()=>null);await p.screenshot({path:`${out}/${id}-${width}x${height}-${lang}-${label}-error.png`}).catch(()=>{});}
   finally{open();await p.close();}
  }
  if(row.before&&row.probe){
    try{
     if(!compact)stable(row.before.ready.coords.stage,row.probe.ready.coords.stage);
     stable(row.before.ready.pose,row.probe.ready.pose);
     if(!compact){stable(row.before.ready.bounds,row.probe.ready.bounds);stable(row.before.ready.poster.rect,row.probe.ready.poster.rect);}
     else{
      const [a,b]=[row.before.ready.bounds,row.probe.ready.bounds];
      const sizes=x=>[x.right-x.left,x.bottom-x.top];
      row.oldSize=sizes(a);row.newSize=sizes(b);
      assert(row.oldSize.every((x,i)=>Math.abs(x-row.newSize[i])<.05),'Existing model projected size must not shrink');
     }
     if(!compact)for(const k of ['tools','download','button','buttons','links'])stable(row.before.ready.coords[k],row.probe.ready.coords[k]);
     row.pass=true;
    }catch(error){row.regression=String(error);}
  }
  results.push(row);await writeFile(out+'/REPORT.json',JSON.stringify(results,null,2));console.log(id,width,height,lang,inset,row.pass?JSON.stringify({checks:'PASS',diag:row.probe.diagnostics}):(row.probe_error||row.before_error||row.regression));
 }
}finally{await b.close();}
if(results.some(x=>!x.pass))process.exitCode=1;
