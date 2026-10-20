// The arrival transition belongs to image UI state, never the WebGL renderer.
// Completion/cancellation and a bounded fallback all leave the decoded image
// opaque; no-JS, cached/no-transition and reduced-motion paths cannot stick.
function revealDecodedThumbnail(image){
 image.dataset.thumbnailReveal='entering';
 if(!image.addEventListener){image.dataset.thumbnailReveal='settled';return;}
 let timer,frame,finished=false;
 const settle=()=>{if(finished)return;finished=true;clearTimeout(timer);if(frame)cancelAnimationFrame(frame);image.removeEventListener('transitionend',ended);image.removeEventListener('transitioncancel',ended);image.dataset.thumbnailReveal='settled';};
 const ended=event=>{if(event.target===image&&event.propertyName==='opacity')settle();};
 image.addEventListener('transitionend',ended);image.addEventListener('transitioncancel',ended);
 timer=setTimeout(settle,250);
 frame=requestAnimationFrame(()=>{frame=0;if(!image.getAnimations().some(animation=>animation.transitionProperty==='opacity'))settle();});
}
/** Small, cancelable image-only queue. Passing a model is never a GLB request. */
export class ThumbnailQueue {
 // Wrap Window timers: calling a native timer as this.setTimer gives it an
 // invalid receiver in real browsers, even though Node timer mocks allow it.
 constructor({delay=120,setTimer=(...args)=>setTimeout(...args),clearTimer=(...args)=>clearTimeout(...args)}={}){
  Object.assign(this,{delay,setTimer,clearTimer});this.concurrency=0;this.active=new Map();this.desired=new Map();this.timer=0;this.stats={started:0,cancelled:0,active:0,maxActive:0,budget:0};
 }
 update(items){
  const desired=new Map(items.filter(item=>item.visible!==false).map(item=>[item.image,item]));
  this.concurrency=desired.size;this.stats.budget=this.concurrency;
  const changed=desired.size!==this.desired.size||[...desired.keys()].some(image=>!this.desired.has(image));
  for(const image of desired.keys()){image.dataset.thumbnailVisible='true';if(!image.dataset.thumbnailState||image.dataset.thumbnailState==='idle')image.dataset.thumbnailState='pending';}
  for(const image of this.desired.keys())if(!desired.has(image))image.dataset.thumbnailVisible='false';
  this.desired=desired;
  if(changed){this.clearTimer(this.timer);this.timer=this.setTimer(()=>{this.timer=0;this.pump();},this.delay);}
  for(const [image,cancel] of this.active)if(!desired.has(image))cancel();
 }
 pump(){
  for(const [image,item] of this.desired){
   if(this.active.size>=this.concurrency)break;
   if(this.active.has(image)||image.dataset.thumbnailState==='ready'||image.dataset.thumbnailState==='error')continue;
   let settled=false,fallback=false;
   const finish=state=>{if(settled)return;settled=true;image.onload=image.onerror=null;this.active.delete(image);this.stats.active=this.active.size;image.dataset.thumbnailState=state;if(state==='ready')revealDecodedThumbnail(image);if(!this.timer)this.pump();};
   const cancel=()=>{if(settled)return;this.stats.cancelled++;image.removeAttribute('src');finish('idle');};
   this.active.set(image,cancel);this.stats.active=this.active.size;this.stats.maxActive=Math.max(this.stats.maxActive,this.active.size);this.stats.started++;
   image.decoding='async';image.dataset.thumbnailState='loading';image.onload=()=>{if(settled||image.dataset.thumbnailState==='decoding')return;image.dataset.thumbnailState='decoding';try{Promise.resolve(image.decode?.()).then(()=>finish('ready'),()=>finish('error'));}catch{finish('error');}};
   image.onerror=()=>{if(!fallback&&item.fallback&&item.fallback!==item.url){fallback=true;image.src=item.fallback;}else finish('error');};
   image.src=item.url;
   // A memory-cached image may already be complete before its load event runs.
   // Decode still owns readiness; the eventual event cannot restart the reveal.
   if(image.complete&&image.naturalWidth>0)image.onload?.();
  }
 }
 clear(){this.clearTimer(this.timer);this.timer=0;for(const image of this.desired.keys())image.dataset.thumbnailVisible='false';this.desired.clear();this.concurrency=0;this.stats.budget=0;for(const cancel of [...this.active.values()])cancel();}
}
