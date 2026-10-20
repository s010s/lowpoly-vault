/** One premultiplied-alpha presentation surface, including both handoffs. */
export class HoverPresentation {
 constructor(host){
  host.__hoverPresentation?.dispose();this.host=host;this.poster=host.querySelector('img');this.poster.style.transition='none';
  this.canvas=document.createElement('canvas');this.canvas.className='hover-surface';this.canvas.setAttribute('aria-hidden','true');
  this.frame=document.createElement('canvas');this.mix=0;this.raf=0;this.visible=false;host.append(this.canvas);host.__hoverPresentation=this;
 }
 update(source,sx,sy,sw,sh,width,height){
  for(const canvas of [this.frame,this.canvas])if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
  const ctx=this.frame.getContext('2d');ctx.clearRect(0,0,width,height);ctx.drawImage(source,sx,sy,sw,sh,0,0,width,height);this.hasFrame=true;this.draw();
 }
 draw(){
  const ctx=this.canvas.getContext('2d'),{width,height}=this.canvas;ctx.clearRect(0,0,width,height);
  // CSS source-over fades lose 25% of silhouette alpha halfway through. Add
  // weighted premultiplied pixels instead, so matched pixels keep their alpha.
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1-this.mix;
  if(this.poster.complete&&this.poster.naturalWidth)ctx.drawImage(this.poster,0,0,width,height);
  ctx.globalCompositeOperation='lighter';ctx.globalAlpha=this.mix;ctx.drawImage(this.frame,0,0);
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
 }
 animate(to){
  if(this.raf)cancelAnimationFrame(this.raf);this.resolve?.(false);const from=this.mix;let started;
  return new Promise(resolve=>{this.resolve=resolve;const tick=now=>{
   if(this.host.__hoverPresentation!==this){resolve(false);return;}
   started??=now;const t=Math.min(1,(now-started)/160);this.mix=from+(to-from)*t;this.draw();
   if(t<1)this.raf=requestAnimationFrame(tick);else{this.raf=0;this.resolve=null;resolve(true);}
  };this.raf=requestAnimationFrame(tick);});
 }
 async reveal(){
  // update() has already copied a real rendered frame. The first visible
  // presentation is exactly the poster; only then blend towards that frame.
  if(!this.hasFrame)return false;
  this.mix=0;this.draw();this.canvas.style.opacity='1';this.poster.style.opacity='0';this.visible=true;
  return this.animate(1);
 }
 async exit(){if(!this.visible){this.dispose();return;}if(await this.animate(0))this.dispose();}
 dispose(){
  if(this.raf)cancelAnimationFrame(this.raf);this.raf=0;this.resolve?.(false);this.resolve=null;
  // This decoded poster has already arrived. Keep its transition disabled so
  // removing the alpha-mixed surface cannot start a second loading fade.
  if(this.host.__hoverPresentation===this){this.poster.style.opacity='';delete this.host.__hoverPresentation;}
  this.canvas.remove();
 }
}
