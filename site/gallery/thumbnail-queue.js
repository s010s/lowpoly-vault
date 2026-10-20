/** Small, cancelable image-only queue. Passing a model is never a GLB request. */
export class ThumbnailQueue {
 // Wrap Window timers: calling a native timer as this.setTimer gives it an
 // invalid receiver in real browsers, even though Node timer mocks allow it.
 constructor({concurrency=3,delay=120,setTimer=(...args)=>setTimeout(...args),clearTimer=(...args)=>clearTimeout(...args)}={}){
  Object.assign(this,{concurrency,delay,setTimer,clearTimer});this.active=new Map();this.desired=new Map();this.timer=0;this.stats={started:0,cancelled:0,active:0,maxActive:0};
 }
 update(items){
  const desired=new Map(items.map(item=>[item.image,item]));
  const changed=desired.size!==this.desired.size||[...desired.keys()].some(image=>!this.desired.has(image));
  for(const [image,item] of desired){image.dataset.thumbnailVisible=String(item.visible!==false);if(!image.dataset.thumbnailState)image.dataset.thumbnailState='pending';}
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
   const finish=state=>{if(settled)return;settled=true;image.onload=image.onerror=null;this.active.delete(image);this.stats.active=this.active.size;image.dataset.thumbnailState=state;if(!this.timer)this.pump();};
   const cancel=()=>{if(settled)return;this.stats.cancelled++;image.removeAttribute('src');finish('idle');};
   this.active.set(image,cancel);this.stats.active=this.active.size;this.stats.maxActive=Math.max(this.stats.maxActive,this.active.size);this.stats.started++;
   image.decoding='async';image.dataset.thumbnailState='loading';image.onload=()=>{if(settled)return;image.dataset.thumbnailState='decoding';Promise.resolve(image.decode?.()).then(()=>finish('ready'),()=>finish('error'));};
   image.onerror=()=>{if(!fallback&&item.fallback&&item.fallback!==item.url){fallback=true;image.src=item.fallback;}else finish('error');};
   image.src=item.url;
  }
 }
 clear(){this.clearTimer(this.timer);this.timer=0;for(const image of this.desired.keys())image.dataset.thumbnailVisible='false';this.desired.clear();for(const cancel of [...this.active.values()])cancel();}
}
