/** Parser-time enhancement of real links; independent of the application bundle.
 * All content, geometry and downloads already exist if this script cannot run. */
(() => {
  const root=document.getElementById('static-route-content');
  if(!root?.classList.contains('gallery-static'))return;
  const wheel=root.querySelector('#wheel'),rows=[...root.querySelectorAll('.slot')];
  if(!wheel||!rows.length)return;
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
   frame=requestAnimationFrame(()=>{frame=0;if(typeof image.getAnimations==='function'&&!image.getAnimations().some(animation=>animation.transitionProperty==='opacity'))settle();});
  }
  // Opt in only when this independent script runs: no-JS native links and
  // posters remain visible. Match the enhanced queue's decode-before-reveal gate.
  for(const row of rows){
    const thumbnail=row.querySelector('.slot-image img');
    thumbnail.dataset.thumbnailState='pending';thumbnail.decoding='async';
    const fail=()=>{thumbnail.dataset.thumbnailState='error';};
    const loaded=()=>{
      if(thumbnail.dataset.thumbnailState!=='pending')return;
      thumbnail.dataset.thumbnailState='decoding';
      try{Promise.resolve(thumbnail.decode?.()).then(()=>{if(thumbnail.dataset.thumbnailState==='decoding'){thumbnail.dataset.thumbnailState='ready';revealDecodedThumbnail(thumbnail);}},fail);}catch{fail();}
    };
    thumbnail.addEventListener('load',loaded,{once:true});thumbnail.addEventListener('error',fail,{once:true});
    if(thumbnail.hasAttribute('src')&&thumbnail.complete){if(thumbnail.naturalWidth>0)loaded();else fail();}
  }
  const url=new URL(location.href),requested=url.searchParams.get('model');
  const explicit=rows.find(row=>row.dataset.id===requested);
  const selected=explicit||rows.find(row=>row.dataset.selected==='true')||rows[0];
  const mobileDetail=!!explicit&&matchMedia('(max-width:760px)').matches;
  document.body.classList.toggle('mobile-detail',mobileDetail);
  const back=root.querySelector('#mobile-back');
  url.searchParams.delete('model');back.href=url.pathname+url.search;back.hidden=!mobileDetail;
  const setText=(id,value)=>{const node=root.querySelector('#'+id);if(node)node.textContent=value;};
  for(const row of rows)row.dataset.selected=String(row===selected);
  selected.setAttribute('aria-current','true');
  const image=root.querySelector('#detail-poster');
  image.src=selected.dataset.poster;image.alt=selected.getAttribute('aria-label');
  setText('title',selected.dataset.title);setText('subtitle',selected.dataset.subtitle);setText('triangles',selected.dataset.triangles);setText('dimensions',selected.dataset.dimensions);setText('file-size',selected.dataset.fileSize);
  for(const id of ['download','blend','info'])root.querySelector('#'+id).href=selected.dataset[id];
  // Native lazy loading fetches rows far outside the clipped wheel. Until the
  // full app mounts, observe this actual scrolling viewport with zero overscan.
  const observer=new IntersectionObserver(entries=>{
    for(const entry of entries){const thumbnail=entry.target;
      if(entry.isIntersecting&&!thumbnail.hasAttribute('src'))thumbnail.src=thumbnail.dataset.src;
    }
  },{root:wheel,rootMargin:'0px'});
  const paint=()=>{
    const index=wheel.scrollTop/128,nearest=Math.max(0,Math.min(rows.length-1,Math.round(index))),reduced=matchMedia('(prefers-reduced-motion:reduce)').matches;
    for(let i=0;i<rows.length;i++){
      const row=rows[i],distance=i-index,host=row.querySelector('.slot-image');
      row.dataset.nameVisible=String(i===nearest);
      host.style.transform=reduced?'none':`translateX(0px) scale(${.58+.42*Math.exp(-.65*distance*distance)})`;
      host.style.opacity=String(reduced?1:Math.max(.55,1-.1*Math.abs(distance)));
    }
  };
  if(!mobileDetail)wheel.scrollTop=rows.indexOf(selected)*128;
  root.dataset.startupInitialized='true';paint();
  const observe=()=>{if(!mobileDetail)for(const row of rows)observer.observe(row.querySelector('.slot-image img'));};observe();
  // Detached roots must not keep observing the entire native catalog.
  document.addEventListener('gallery-restore',observe,{once:true});
  document.addEventListener('gallery-mount',()=>observer.disconnect(),{once:true});
  let frame=0;
  wheel.addEventListener('scroll',()=>{if(!frame)frame=requestAnimationFrame(()=>{frame=0;paint();});},{passive:true});
})();
