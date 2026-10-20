/** Parser-time enhancement of real links; independent of the application bundle.
 * All content, geometry and downloads already exist if this script cannot run. */
(() => {
  const root=document.getElementById('static-route-content');
  if(!root?.classList.contains('gallery-static'))return;
  const wheel=root.querySelector('#wheel'),rows=[...root.querySelectorAll('.slot')];
  if(!wheel||!rows.length)return;
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
  let frame=0;
  wheel.addEventListener('scroll',()=>{if(!frame)frame=requestAnimationFrame(()=>{frame=0;paint();});},{passive:true});
})();
