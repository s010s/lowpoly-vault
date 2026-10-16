/** One interruptible owner per element. No permanent animation loop or hidden content. */
export class GalleryMotion {
 constructor(){this.reduce=matchMedia('(prefers-reduced-motion: reduce)');this.active=new Map();this.seen=new WeakSet();this.observer=new IntersectionObserver(entries=>{let order=0;for(const e of entries){if(e.isIntersecting&&!this.seen.has(e.target)){this.seen.add(e.target);this.observer.unobserve(e.target);this.enter(e.target,order++);}}},{threshold:.08});document.addEventListener('visibilitychange',()=>{for(const a of this.active.values())document.hidden?a.pause():a.play();});this.reduce.addEventListener('change',()=>{if(this.reduce.matches)this.cancelAll();});document.addEventListener('focusin',e=>this.cancel(e.target.closest('.asset-card')));}
 run(el,frames,options={}){if(!el||this.reduce.matches)return null;this.cancel(el);const a=el.animate(frames,{duration:300,fill:'backwards',easing:'cubic-bezier(.2,.8,.2,1)',...options});this.active.set(el,a);if(document.hidden)a.pause();a.finished.catch(()=>{}).finally(()=>{if(this.active.get(el)===a)this.active.delete(el);});return a;}
 cancel(el){this.active.get(el)?.cancel();this.active.delete(el);}
 cancelAll(){for(const a of this.active.values())a.cancel();this.active.clear();}
 capture(grid){const rects=new Map();for(const c of grid.querySelectorAll('.asset-card')){this.cancel(c);rects.set(c.dataset.id,c.getBoundingClientRect());}return rects;}
 async exit(grid,ids){const keep=new Set(ids),tasks=[];for(const c of grid.querySelectorAll('.asset-card'))if(!keep.has(c.dataset.id)){const a=this.run(c,[{opacity:1,transform:'none'},{opacity:0,transform:'translateY(-6px)'}],{duration:100});if(a)tasks.push(a.finished.catch(()=>{}));}await Promise.all(tasks);}
 enter(card,i=0){this.run(card,[{opacity:0,transform:'translateY(24px) scale(.96)'},{opacity:1,transform:'none'}],{duration:460,delay:Math.min(i*40,240)});}
 commit(grid,previous=new Map()){this.observer.disconnect();let i=0;for(const card of grid.querySelectorAll('.asset-card')){const r=card.getBoundingClientRect(),old=previous.get(card.dataset.id);if(old&&old.top<innerHeight&&old.bottom>0&&r.top<innerHeight&&r.bottom>0){this.seen.add(card);const dx=old.left-r.left,dy=old.top-r.top;this.run(card,[{opacity:.65,transform:`translate(${dx}px,${dy}px)`},{opacity:1,transform:'none'}],{duration:280});}else if(r.top<innerHeight&&r.bottom>0){this.seen.add(card);this.enter(card,i++);}else this.observer.observe(card);}}
 replay(grid){for(const c of grid.querySelectorAll('.asset-card'))this.cancel(c);this.commit(grid);}
 shell(){['.brand','.intro','.sidebar','.search-row'].forEach((s,i)=>this.run(document.querySelector(s),[{opacity:0,transform:'translateY(8px)'},{opacity:1,transform:'none'}],{duration:240,delay:i*45}));}
 feedback(el){this.run(el,[{transform:'scale(1)'},{transform:'scale(.96)',offset:.4},{transform:'scale(1)'}],{duration:180});}
 revealInfo(){document.querySelectorAll('.asset-info>*,.viewer-topline').forEach((el,i)=>this.run(el,[{opacity:0,transform:'translateY(8px)'},{opacity:1,transform:'none'}],{duration:220,delay:Math.min(i*22,132)}));}
 dispose(){this.observer.disconnect();this.cancelAll();}
}
