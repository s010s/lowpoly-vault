/** Decorative rails follow rendered marker geometry, never list progress. */
export function guideGeometry({viewport,markers}){
 const visible=markers.filter(marker=>marker.bottom>viewport.top&&marker.top<viewport.bottom).sort((a,b)=>a.cy-b.cy);
 if(!visible.length||viewport.height<=0)return null;
 const first=visible[0],last=visible.at(-1),center=(viewport.top+viewport.bottom)/2;
 const nearest=visible.reduce((best,marker)=>Math.abs(marker.cy-center)<Math.abs(best.cy-center)?marker:best);
 return {left:{x:first.cx,top:first.cy,height:last.cy-first.cy,visible:visible.length>1},
  right:{top:viewport.top,height:viewport.height,gap:Math.min(nearest.rowHeight,viewport.height*.32)},
  visibleCount:visible.length,firstId:first.id,lastId:last.id};
}
const rectOf=element=>{
 const box=element.getBoundingClientRect();
 return {left:box.left,top:box.top,width:box.width,height:box.height,right:box.right??box.left+box.width,bottom:box.bottom??box.top+box.height};
};
export class WheelGuides{
 constructor({wrap,wheel,slots,left,right}){
  Object.assign(this,{wrap,wheel,slots,left,right});this.disposed=false;
  this.observer=typeof ResizeObserver==='function'?new ResizeObserver(()=>this.update()):null;
  this.observer?.observe(wrap);this.observer?.observe(wheel);
 }
 update(){
  if(this.disposed)return;
  // Read layout as one batch before updating either rail. Overscan and the
  // offscreen keyboard option are intentionally excluded from the endpoints.
  const wrap=rectOf(this.wrap),wheel=rectOf(this.wheel),top=Math.max(wrap.top,wheel.top),bottom=Math.min(wrap.bottom,wheel.bottom);
  const viewport={top:top-wrap.top,bottom:bottom-wrap.top,height:Math.max(0,bottom-top)};
  const markers=[];
  for(const row of this.slots.children){
   const marker=row.querySelector('.slot-marker');if(!marker)continue;
   const box=rectOf(marker),rowBox=rectOf(row);if(!box.width||!box.height)continue;
   markers.push({id:row.dataset.id,cx:box.left+box.width/2-wrap.left,cy:box.top+box.height/2-wrap.top,top:box.top-wrap.top,bottom:box.bottom-wrap.top,rowHeight:rowBox.height});
  }
  const layout=guideGeometry({viewport,markers});
  this.left.hidden=!layout?.left.visible;this.right.hidden=!layout||!wrap.width;
  if(!layout)return;
  // A partially clipped circle retains its real center beyond the clip; the
  // common wheel-wrap clipping/mask clips the line and its circle together.
  this.left.style.left=`${layout.left.x-.5}px`;this.left.style.top=`${layout.left.top}px`;this.left.style.height=`${layout.left.height}px`;
  this.left.dataset.firstId=layout.firstId;this.left.dataset.lastId=layout.lastId;
  this.right.style.top=`${layout.right.top}px`;this.right.style.height=`${layout.right.height}px`;this.right.style.setProperty('--focus-gap',`${layout.right.gap}px`);
 }
 dispose(){this.disposed=true;this.observer?.disconnect();}
}
