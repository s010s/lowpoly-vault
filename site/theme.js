// UI-only theme controller: never imports, recreates, or resets the model renderer.
import { MOTION, animateOneShot } from './motion-system.js';
export function initTheme({doc=document,media=matchMedia,storage=()=>localStorage,viewport=()=>({width:innerWidth,height:innerHeight})}={}){
 const root=doc.documentElement,system=media('(prefers-color-scheme: dark)'),reduce=media('(prefers-reduced-motion: reduce)');
 let chosen=null,active=null,running=false,pending=null,fade=null;
 try{const saved=storage().getItem('vault-theme');if(saved==='light'||saved==='dark')chosen=saved;}catch{}
 let theme=chosen||(system.matches?'dark':'light');
 const buttons=[...doc.querySelectorAll('[data-theme-toggle]')];
 function labels(){const zh=(root.lang||'').startsWith('zh');for(const b of buttons){b.setAttribute('aria-label',zh?(theme==='dark'?'切换浅色主题':'切换深色主题'):(theme==='dark'?'Switch to light theme':'Switch to dark theme'));b.setAttribute('aria-pressed',String(theme==='dark'));b.title=b.getAttribute('aria-label');}}
 function apply(value){theme=value;root.dataset.theme=value;root.style.colorScheme=value;doc.querySelector('meta[name="theme-color"]')?.setAttribute('content',value==='dark'?'#282e26':'#f9f7f1');labels();}
 function pulseIcon(button){
  if(reduce.matches)return;
  const svg=button?.querySelector?.('svg');
  // Animate independent scale/opacity so :hover rotate(14deg) never snaps back.
  animateOneShot(svg,'theme-icon',[{scale:'0.82',opacity:.68},{scale:'1',opacity:1}],{duration:MOTION.base,easing:MOTION.easeStandard});
 }
 apply(theme);
 async function drain(){if(running||!pending)return;running=true;const request=pending;pending=null;const {value,button}=request;
  const rect=button?.getBoundingClientRect();const {width,height}=viewport();const x=rect?rect.left+rect.width/2:width/2,y=rect?rect.top+rect.height/2:0;
  const radius=Math.hypot(Math.max(x,width-x),Math.max(y,height-y));
  try{
   if(typeof doc.startViewTransition==='function'){
    active=doc.startViewTransition(()=>apply(value));
    const completed=active.finished.catch(()=>{});
    await active.ready;
    if(!pending){const frames=reduce.matches?[{opacity:0},{opacity:1}]:[{clipPath:`circle(0px at ${x}px ${y}px)`},{clipPath:`circle(${radius}px at ${x}px ${y}px)`}];
     await root.animate(frames,{duration:reduce.matches?MOTION.themeReduced:MOTION.theme,easing:MOTION.easeStandard,pseudoElement:'::view-transition-new(root)'}).finished.catch(()=>{});}
    await completed;
   }else{
    root.dataset.themeSwitching='true';
    apply(value);
    if(typeof root.getBoundingClientRect==='function')root.getBoundingClientRect();
    delete root.dataset.themeSwitching;
    pulseIcon(button);
    fade?.cancel();
    fade=root.animate([{opacity:.88},{opacity:1}],{duration:reduce.matches?MOTION.themeReduced:MOTION.themeFallback,easing:MOTION.easeStandard});
    await fade.finished.catch(()=>{});
   }
  }catch{delete root.dataset.themeSwitching;apply(value);}finally{delete root.dataset.themeSwitching;active=null;running=false;if(pending)void drain();}
 }
 function toggle(button){const next=(pending?.value||chosen||theme)==='dark'?'light':'dark';chosen=next;try{storage().setItem('vault-theme',next);}catch{}pending={value:next,button};active?.skipTransition();void drain();}
 buttons.forEach(b=>b.addEventListener('click',()=>toggle(b)));
 system.addEventListener('change',()=>{if(!chosen){pending={value:system.matches?'dark':'light'};active?.skipTransition();void drain();}});
 if(typeof MutationObserver==='function')new MutationObserver(labels).observe(root,{attributes:true,attributeFilter:['lang']});
 return {get theme(){return theme;},get chosen(){return chosen;}};
}
