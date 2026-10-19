// Logical open state is separate from hidden so an exit can reverse in place.
export function createPopover(panel,trigger,{enter=200,exit=150,reduced=()=>false,schedule=setTimeout,cancel=clearTimeout,beforeEnter=()=>{}}={}){
 let open=false,timer=0,version=0;
 panel.classList.add('ui-popover');panel.dataset.open='false';panel.inert=true;
 const clear=()=>{cancel(timer);timer=0;};
 const mode=animate=>animate?(reduced()?'reduced':'true'):'false';
 function set(next,{animate=false}={}){
  if(open===next){if(!next&&!animate){clear();panel.hidden=true;}return;}
  open=next;clear();const owner=++version,motion=mode(animate),duration=motion==='reduced'?100:(motion==='true'?(next?enter:exit):0);
  panel.dataset.motion=motion;panel.style.setProperty('--ui-duration',duration+'ms');
  trigger?.setAttribute('aria-expanded',String(next));panel.inert=!next;panel.setAttribute('aria-hidden',String(!next));
  if(next){
   const wasHidden=panel.hidden;panel.hidden=false;beforeEnter();
   if(trigger&&(wasHidden||!panel.style.transformOrigin)){const p=panel.getBoundingClientRect(),t=trigger.getBoundingClientRect();panel.style.transformOrigin=`${Math.max(0,Math.min(p.width,t.left+t.width/2-p.left))}px ${Math.max(0,Math.min(p.height,t.top+t.height/2-p.top))}px`;}
   if(wasHidden&&duration)panel.getBoundingClientRect();
   panel.dataset.open='true';
  }else{
   panel.dataset.open='false';
   if(duration)timer=schedule(()=>{if(owner===version&&!open)panel.hidden=true;timer=0;},duration);
   else panel.hidden=true;
  }
 }
 return {get open(){return open;},show:options=>set(true,options),hide:options=>set(false,options),settle(){clear();panel.dataset.motion='false';panel.hidden=!open;},dispose(){clear();version++;}};
}

export function overflowRemaining(element){return element.scrollHeight-element.clientHeight-element.scrollTop>2;}
export function shouldAnimateBoundary(previousCount,nextCount,deliberate){return !!deliberate&&((previousCount===0)!==(nextCount===0));}

// All dimensions are layout-viewport CSS pixels, including visualViewport offsets.
// The panel may overlap its trigger when the keyboard leaves very little room,
// but it must never put its close control or scrolling viewport off screen.
export function fitInfoPanel({viewport,anchor,safe={},preferredHeight=340,maxWidth=320,gutter=12,gap=8}){
 const leftBound=(viewport.left||0)+(safe.left||0)+gutter;
 const topBound=(viewport.top||0)+(safe.top||0)+gutter;
 const rightBound=(viewport.left||0)+viewport.width-(safe.right||0)-gutter;
 const bottomBound=(viewport.top||0)+viewport.height-(safe.bottom||0)-gutter;
 const width=Math.max(1,Math.min(maxWidth,rightBound-leftBound));
 const height=Math.max(1,Math.min(preferredHeight,bottomBound-topBound));
 const left=Math.min(Math.max(anchor.left+anchor.width/2-width/2,leftBound),Math.max(leftBound,rightBound-width));
 const below=bottomBound-anchor.bottom-gap,above=anchor.top-gap-topBound;
 const minimum=Math.min(180,height);
 let top,maxHeight,placement;
 if(below>=minimum){maxHeight=Math.min(height,below);top=anchor.bottom+gap;placement='below';}
 else if(above>=minimum){maxHeight=Math.min(height,above);top=anchor.top-gap-maxHeight;placement='above';}
 else{maxHeight=height;top=Math.min(Math.max(anchor.bottom+gap,topBound),Math.max(topBound,bottomBound-maxHeight));placement='clamped';}
 top=Math.min(Math.max(top,topBound),Math.max(topBound,bottomBound-maxHeight));
 return {left,top,width,maxHeight,placement,availableHeight:Math.max(1,bottomBound-topBound)};
}

export function createUIFeedback({t,reduced,getSelection}){
 const root=document.documentElement,abort=new AbortController(),timers=new Set(),reveals=new Map(),chipNodes=new Map();
 let input='keyboard',copyVersion=0,copyTimer=0,copyState='idle',disposed=false;
 const later=(fn,ms)=>{const id=setTimeout(()=>{timers.delete(id);fn();},ms);timers.add(id);return id;};
 const clear=id=>{clearTimeout(id);timers.delete(id);};
 const listen=(target,type,fn,options={})=>target.addEventListener(type,fn,{...options,signal:abort.signal});
 const pointer=event=>!!event&&(event.type?.startsWith('pointer')||(event.type==='click'&&event.detail>0));
 listen(document,'pointerdown',()=>{input='pointer';root.dataset.uiInput=input;},{capture:true});
 listen(document,'keydown',()=>{input='keyboard';root.dataset.uiInput=input;},{capture:true});
 root.dataset.uiInput=input;
 const filter=createPopover(document.querySelector('#filter-panel'),document.querySelector('#filters'),{reduced,schedule:later,cancel:clear});
 const infoPanel=document.querySelector('#info-panel'),infoContent=document.querySelector('#info-content'),infoTrigger=document.querySelector('#info');
 let safeProbe=null;
 function safeInsets(){
  if(typeof window.getComputedStyle!=='function')return {};
  if(!safeProbe){safeProbe=document.createElement('div');safeProbe.className='info-safe-area-probe';safeProbe.setAttribute('aria-hidden','true');safeProbe.inert=true;document.body.append(safeProbe);}
  const style=window.getComputedStyle(safeProbe);
  return {top:parseFloat(style.paddingTop)||0,right:parseFloat(style.paddingRight)||0,bottom:parseFloat(style.paddingBottom)||0,left:parseFloat(style.paddingLeft)||0};
 }
 function positionInfo(){
  if(infoPanel.hidden)return;
  const visual=window.visualViewport;
  const viewport={left:visual?.offsetLeft||0,top:visual?.offsetTop||0,width:visual?.width||window.innerWidth||document.documentElement.clientWidth||1024,height:visual?.height||window.innerHeight||document.documentElement.clientHeight||768};
  const anchor=infoTrigger.getBoundingClientRect(),safe=safeInsets();
  const initial=fitInfoPanel({viewport,anchor,safe});
  infoPanel.style.width=initial.width+'px';
  infoPanel.style.setProperty('--info-max-height',initial.availableHeight+'px');
  const measured=Math.min(340,infoPanel.offsetHeight||340);
  const fitted=fitInfoPanel({viewport,anchor,safe,preferredHeight:measured});
  infoPanel.style.left=fitted.left+'px';infoPanel.style.top=fitted.top+'px';
  infoPanel.style.setProperty('--info-max-height',fitted.maxHeight+'px');
  infoPanel.dataset.placement=fitted.placement;
 }
 const info=createPopover(infoPanel,infoTrigger,{enter:150,exit:125,reduced,schedule:later,cancel:clear,beforeEnter:positionInfo});
 function updateOverflow(){infoPanel.dataset.more=String(info.open&&overflowRemaining(infoContent));}
 function refreshInfoViewport(){if(info.open)positionInfo();updateOverflow();}
 listen(infoContent,'scroll',updateOverflow,{passive:true});listen(window,'resize',refreshInfoViewport,{passive:true});listen(window,'scroll',refreshInfoViewport,{passive:true});
 if(window.visualViewport){listen(window.visualViewport,'resize',refreshInfoViewport,{passive:true});listen(window.visualViewport,'scroll',refreshInfoViewport,{passive:true});}
 const resize=typeof ResizeObserver==='function'?new ResizeObserver(updateOverflow):null;
 resize?.observe(infoContent);resize?.observe(infoPanel);
 const mutation=typeof MutationObserver==='function'?new MutationObserver(refreshInfoViewport):null;
 mutation?.observe(infoContent,{childList:true,subtree:true,characterData:true});
 function reveal(node,{animate=false,duration=150,remove=false}={}){
  const prior=reveals.get(node);if(prior){clear(prior);reveals.delete(node);}
  const motion=animate?(reduced()?'reduced':'true'):'false';
  node.classList.add('ui-reveal');node.dataset.motion=motion;node.style.setProperty('--ui-duration',(motion==='reduced'?100:duration)+'ms');
  const ms=motion==='false'?0:motion==='reduced'?100:duration;
  if(remove){node.dataset.visible='false';node.inert=true;node.setAttribute('aria-hidden','true');}
  else{
   const wasLeaving=node.dataset.visible==='false';node.inert=false;node.removeAttribute('aria-hidden');
   if(!wasLeaving&&ms){node.dataset.visible='false';node.getBoundingClientRect();}
   node.dataset.visible='true';
  }
  if(!ms){if(remove)node.remove();return;}
  reveals.set(node,later(()=>{reveals.delete(node);if(remove){node.remove();}else{node.classList.remove('ui-reveal');delete node.dataset.visible;}},ms));
 }
 const chips=document.querySelector('#chips');
 function renderChips(items,{animate=false,onRemove,onMore}={}){
  const visible=items.slice(0,2).map(item=>({...item,key:item.group+':'+item.id}));
  if(items.length>2)visible.push({key:'more',label:'+'+(items.length-2),more:true});
  const keys=new Set(visible.map(item=>item.key)),focused=document.activeElement;
  const removedFocus=[...chipNodes].some(([key,node])=>!keys.has(key)&&node===focused);
  visible.forEach((item,index)=>{
   let node=chipNodes.get(item.key);const added=!node;
   if(!node){node=document.createElement('button');node.type='button';node.dataset.chipKey=item.key;chipNodes.set(item.key,node);}
   node.textContent=item.label+(item.more?'':' ×');node.title=item.more?t('More filters','更多筛选'):t('Remove ','移除')+item.label;
   node.onclick=event=>item.more?onMore(event):onRemove(item,event);
   const at=[...chips.children].filter(child=>keys.has(child.dataset.chipKey))[index];
   if(at!==node)chips.insertBefore(node,at||null);
   if(added||node.inert)reveal(node,{animate,duration:150});
  });
  for(const [key,node] of chipNodes)if(!keys.has(key)){
   // Unchanged renders do not restart an outgoing transition.
   if(!node.inert)reveal(node,{animate,duration:100,remove:true});
   if(!animate){node.remove();chipNodes.delete(key);}
   else later(()=>{if(!node.isConnected&&chipNodes.get(key)===node)chipNodes.delete(key);},110);
  }
  if(removedFocus)([...chips.children].find(node=>!node.inert)||document.querySelector('#filters')).focus({preventScroll:true});
 }
 const credits=document.querySelector('#credits'),copyText=credits.querySelector('[data-en]'),status=document.querySelector('#copy-status');
 function resetCopy(){copyVersion++;clear(copyTimer);copyTimer=0;copyState='idle';credits.dataset.copyState='idle';credits.removeAttribute('aria-busy');copyText.textContent=copyText.dataset[root.lang==='zh-CN'?'zh':'en'];status.textContent='';}
 async function copyAttribution(asset,event){
  resetCopy();const owner=++copyVersion,selection=getSelection(),language=root.lang;
  copyState='pending';credits.dataset.copyState='pending';credits.setAttribute('aria-busy','true');
  const text=`${asset.name.en} — ${asset.author}, ${asset.license}. ${asset.source_url}`;
  try{
   if(!navigator.clipboard?.writeText)throw new Error('Clipboard is unavailable');
   await navigator.clipboard.writeText(text);
   if(disposed||owner!==copyVersion||selection!==getSelection()||language!==root.lang)return;
   copyState='success';credits.dataset.copyState='success';credits.removeAttribute('aria-busy');
   copyText.textContent=t('✓ Copied','✓ 已复制');status.textContent=t('Attribution copied','署名已复制');
   reveal(copyText,{animate:pointer(event),duration:150});
   copyTimer=later(()=>{if(owner===copyVersion)resetCopy();},2000);
  }catch{
   if(disposed||owner!==copyVersion||selection!==getSelection()||language!==root.lang)return;
   copyState='error';credits.dataset.copyState='error';credits.removeAttribute('aria-busy');
   copyText.textContent=t('Copy failed · Try again','复制失败 · 请重试');
   status.textContent=t('Could not copy attribution. Please try again or copy it from the model information.','署名未能复制，请重试或从模型说明中手动复制。');
   copyTimer=later(()=>{if(owner===copyVersion)resetCopy();},3500);
  }
 }
 // Native anchors retain their default navigation/download; feedback never waits.
 const downloads=[...document.querySelectorAll('.download-actions a')];
 downloads.forEach(link=>{
  listen(link,'pointerdown',event=>{if(event.isPrimary!==false&&event.button===0)link.dataset.pressed='true';});
  listen(link,'pointerleave',()=>{link.dataset.pressed='false';});
 });
 const release=()=>downloads.forEach(link=>{link.dataset.pressed='false';});
 listen(window,'pointerup',release,{passive:true});listen(window,'pointercancel',release,{passive:true});listen(window,'blur',release);
 const media=matchMedia('(prefers-reduced-motion: reduce)');
 listen(media,'change',()=>{filter.settle();info.settle();release();for(const [node,id] of reveals){clear(id);if(node.inert)node.remove();else{node.classList.remove('ui-reveal');delete node.dataset.visible;}}reveals.clear();updateOverflow();});
 return {filter,info,pointer,get pointerInput(){return input==='pointer';},get copyState(){return copyState;},renderChips,reveal,resetCopy,copyAttribution,updateOverflow,
  dispose(){if(disposed)return;disposed=true;abort.abort();resize?.disconnect();mutation?.disconnect();safeProbe?.remove();filter.dispose();info.dispose();resetCopy();for(const timer of timers)clearTimeout(timer);timers.clear();reveals.clear();}};
}
