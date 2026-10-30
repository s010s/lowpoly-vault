import './style.css';
import './thumbnail-placeholder.css';
import {thumbnailPlaceholderMarkup,synchronizeThumbnailPlaceholders} from './thumbnail-placeholder.js';
import {mountIcons} from './icons.js';
import {createUIFeedback,shouldAnimateBoundary} from './ui-feedback.js';
import {modelHeight,dimensionDetails,dimensionNote,comparisonText} from './model-dimensions.js';
import {models,catalog,siteRoot,assetURL,readGalleryQuery,galleryURL,emptyFacets,detailHref} from './catalog-source.js';
import {parseRoute} from '../routes.js';
import {modelShortName} from './presentation-labels.js';
import {HoverTurntable} from './hover-turntable.js';
import {HoverIntent,hoverRowAt} from './hover-intent.js';
import {ThumbnailQueue} from './thumbnail-queue.js';
import {WheelTitle} from './wheel-title.js';
import {WheelGuides} from './wheel-guides.js';
import {filterItems,WheelSettler} from './state.js';
import {DetailRenderer as PreviewRenderer,POSTER_IMAGE_SCALE} from './detail-renderer.js';
import {validDetailPresentation,detailScreenFrame} from './detail-presentation-policy.js';
// Importing this module prepares code and CSS without touching the SSG document.
// Bootstrap mounts only after every startup dependency has finished loading.
export async function mountGallery(){
mountIcons(document);
document.documentElement.style.setProperty('--poster-scale',POSTER_IMAGE_SCALE);
const $=selector=>document.querySelector(selector),all=selector=>[...document.querySelectorAll(selector)];
const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const mobile=()=>matchMedia('(max-width:760px)').matches;
const t=(en,zh)=>state.lang==='zh'?zh:en;
const short=a=>modelShortName(a,state.lang);
const categories={animals:['Animal forms','动物形态'],plants:['Plants','植物'],geology:['Geology','地质'],wood:['Wood','木材'],traces:['Traces','痕迹']};
const packLabels=Object.fromEntries((catalog.packs||[]).map(record=>[record.id,record.name]));
const worldLabels=Object.fromEntries((catalog.worlds||[]).map(record=>[record.id,record.name]));
const packNames={'prehistoric-starter':['Starter collection','初始精选'],'prehistoric-small-life-round12-20261018':['Small life · XII','小生命 · XII']};
function packLabel(id){return packLabels[id]?.[state.lang]||packNames[id]?.[state.lang==='zh'?1:0]||id.replace('prehistoric-small-life-','Small life · ').replace('-20261018','').replace('round','');}
const sample=models.map(a=>({...a,triangleBand:Number.isFinite(a.triangles)?a.triangles<=5000?'under5k':a.triangles<=10000?'5to10k':'over10k':'unknown'}));
const initial=new URL(location.href).searchParams,queryState=readGalleryQuery(initial);
const initialModel=initial.get('model'),savedState=history.state?.gallery?history.state:null;
const hasInitialModel=models.some(asset=>asset.id===initialModel);
const defaultSelection=models.find(a=>a.id===initialModel)?.id||models.find(a=>a.id===savedState?.selected)?.id||(!(catalog.route.page||0)&&models.find(a=>a.id==='cooperoceras')?.id)||sample[Math.min(sample.length-1,(catalog.route.page||0)*24)]?.id||null;
const state={lang:catalog.route.lang==='zh-CN'?'zh':'en',page:catalog.route.page||0,...queryState,results:sample,selected:defaultSelection,center:defaultSelection,keyboard:defaultSelection,mobileOpen:false,view:hasInitialModel?'detail':'collection',detailDepth:hasInitialModel?Math.max(0,savedState?.detailDepth||0):0};
if(initialModel&&!models.some(a=>a.id===initialModel))setTimeout(()=>toast(t('This model does not exist.','该模型不存在。')),50);
let renderer,selectionVersion=0,composition=false,searchTimer,resizeTimer,infoOpenTimer,infoCloseTimer,infoPinned=false,infoSuppressed=false,draft=null,toastTimer;
let currentReady=false,programmaticPosition=null,selectionLoadingTimer=0,cancelSelectedPoster=null;
let collectionScroll=0,measuredPad=0,restoringHistory=false,collectionReturnPending=false;
const detailPosterCache=new Map(),DETAIL_POSTER_CACHE_LIMIT=8;
const thumbnails=new ThumbnailQueue();let warmPosterTimer=0,hasBrowsed=false;
function setWheelPosition(value){collectionScroll=Math.max(0,value);if(!wheel.clientHeight)return;wheel.scrollTop=collectionScroll;programmaticPosition=wheel.scrollTop;collectionScroll=wheel.scrollTop;}
const wheel=$('#wheel'),slots=$('#slots'),SLOT=128;
const guides=new WheelGuides({wheel,slots,wrap:$('.wheel-wrap'),left:$('.focus-guide-left'),right:$('.focus-guide-right')});
const ui=createUIFeedback({t,reduced,getSelection:()=>state.selected});
let resultArrivalVersion=0;
function disposeUI(){hover.clear();thumbnails.clear();clearTimeout(warmPosterTimer);clearTimeout(infoOpenTimer);clearTimeout(infoCloseTimer);clearTimeout(searchTimer);clearTimeout(toastTimer);guides.dispose();ui.dispose();}
const wheelTitle=new WheelTitle({read:()=>wheel.scrollTop,targets:()=>state.results.map((a,i)=>({id:a.id,offset:i*SLOT})),change:()=>renderWheel()});
window.addEventListener('pagehide',event=>{if(!event.persisted){cancelSelectedPoster?.();renderer?.suspend();wheelTitle.dispose();settler.dispose();disposeUI();}});
if(import.meta.hot)import.meta.hot.dispose(()=>{cancelSelectedPoster?.();renderer?.suspend();wheelTitle.dispose();settler.dispose();disposeUI();});
const urlAsset=assetURL;
function poster(asset,{wheel=false}={}){return urlAsset(asset.galleryPosters?.[wheel?'wheel':'detail']||asset.preview);}
// Warm only nearby canonical detail posters, never wheel-angle images or GLBs.
// Keeping a few decoded image nodes avoids blank selections without retaining
// an unbounded collection of raster surfaces while browsing.
function warmDetailPosters(){
 // Mobile is poster-first on explicit selection, never prefetch hidden detail.
 if(!hasBrowsed||!currentReady||mobile()||!wheel.clientHeight||navigator.connection?.saveData)return;
 const center=Math.max(0,Math.round(wheel.scrollTop/SLOT));
 const nearby=state.results.slice(Math.max(0,center-1),center+2);
 for(const [id,entry] of detailPosterCache)if(!entry.ready&&!nearby.some(asset=>asset.id===id)){entry.image.onload=entry.image.onerror=null;entry.image.removeAttribute('src');detailPosterCache.delete(id);}
 for(const asset of nearby){
  if(asset.id===state.selected||detailPosterCache.has(asset.id))continue;
  const image=document.createElement('img'),entry={image,ready:false};image.decoding='async';detailPosterCache.set(asset.id,entry);
  image.onload=()=>{Promise.resolve(image.decode?.()).then(()=>{if(detailPosterCache.get(asset.id)===entry)entry.ready=true;},()=>{});};
  image.onerror=()=>{if(detailPosterCache.get(asset.id)===entry)detailPosterCache.delete(asset.id);};image.src=poster(asset);
 }
 while(detailPosterCache.size>DETAIL_POSTER_CACHE_LIMIT){const [id,entry]=detailPosterCache.entries().next().value;entry.image.onload=entry.image.onerror=null;entry.image.removeAttribute('src');detailPosterCache.delete(id);}
}
function cancelPosterWarmup(){
 clearTimeout(warmPosterTimer);
 for(const [id,entry] of detailPosterCache)if(!entry.ready){entry.image.onload=entry.image.onerror=null;entry.image.removeAttribute('src');detailPosterCache.delete(id);}
}
function toast(message){$('#toast').textContent=message;$('#toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),2500);}
function updateComparisonLabel(kind){const label=$('#comparison-label');label.dataset.kind=kind;label.textContent=comparisonText(kind,state.lang,sample.find(asset=>asset.id===state.selected));}
function translate(){$('#gallery-github').ariaLabel=t('GitHub repository (opens in a new tab)','GitHub 代码仓库（在新标签页打开）');document.documentElement.lang=state.lang==='zh'?'zh-CN':'en';document.title=t('All models | Lowpoly Vault','全部模型 | Lowpoly Vault');for(const link of all('[data-gallery-route]'))link.href=new URL((state.lang==='zh'?'zh-CN/':'')+(link.dataset.galleryRoute==='home'?'':'about/'),siteRoot).href;all('[data-en]').forEach(el=>el.textContent=el.dataset[state.lang]);$('#language').textContent=state.lang==='zh'?'中文 / EN':'EN / 中文';$('#search').placeholder=t('Search the collection','搜索精选模型');$('#search').ariaLabel=t('Search models','搜索模型');wheel.ariaLabel=t('Model collection','模型列表');$('#info').ariaLabel=t('Model information','模型说明');$('#detail').ariaLabel=t('3D model. Drag to rotate, wheel or plus/minus to zoom, arrows to rotate.','3D模型。拖拽旋转，滚轮或加减号缩放，方向键旋转。');$('#filters').setAttribute('aria-label',t('Filters','筛选'));$('#info-content').setAttribute('aria-label',t('Model details and sources','模型说明与来源'));if(renderer?.comparison&&$('#comparison-label').dataset.kind)updateComparisonLabel($('#comparison-label').dataset.kind);}
function facetLabels(){return {worlds:t('World','世界主题'),collection:t('Collection','集合'),triangleMax:t('Maximum triangles','最高三角面数'),packs:t('Theme · collection','主题 · 集合'),category:t('Object type','物体类型'),triangleBand:t('Specification · triangles','技术规格 · 三角面')};}
function valueLabel(group,id){if(group==='worlds')return worldLabels[id]?.[state.lang]||id;if(group==='collection')return worldLabels[id]?.[state.lang]||id;if(group==='triangleMax')return t('Up to ','不超过 ')+Number(id).toLocaleString();if(group==='category')return categories[id]?.[state.lang==='zh'?1:0]||id;if(group==='packs')return packLabel(id);return {under5k:t('Up to 5,000','5千及以下'),'5to10k':t('5,001–10,000','5千至1万'),over10k:t('Over 10,000','超过1万')}[id]||id;}
function measure(){if(!wheel.clientHeight)return measuredPad;const pad=measuredPad=Math.max(0,wheel.clientHeight/2-SLOT/2);slots.style.height=`${state.results.length*SLOT+pad*2}px`;slots.style.setProperty('--pad',pad+'px');return pad;}
const hover=new HoverIntent({
 hit:point=>hoverRowAt(document,wheel,slots,point),
 enabled:()=>!document.hidden&&!reduced()&&matchMedia('(hover:hover) and (pointer:fine)').matches,
 ready:()=>currentReady&&!!renderer, idle:()=>settler.state==='idle',
 create:row=>{
  const asset=state.results.find(asset=>asset.id===row.dataset.id),host=row.querySelector('.slot-image');
  const table=new HoverTurntable(host,asset.wheelSpec,{reduced});
  return {prepare:()=>{const request=renderer.preview(asset,host);if(renderer.hover)renderer.hover.effect=table;return request;},
   ready:()=>table.ready(),reveal:()=>renderer.revealHover(),animate:()=>renderer.animateHover(),
   stop:()=>{table.stop();renderer?.stopHover();}};
 }
});
function stopHover(){hover.clear();renderer?.stopHover();}
document.addEventListener('pointermove',event=>hover.pointer(event),{passive:true});
document.addEventListener('pointerdown',event=>{if(event.pointerType==='touch')stopHover();},{passive:true});
document.documentElement.addEventListener('pointerleave',stopHover);
window.addEventListener('pointercancel',stopHover);
document.addEventListener('visibilitychange',stopHover);
window.addEventListener('pagehide',stopHover);
matchMedia('(hover:hover) and (pointer:fine)').addEventListener('change',stopHover);
function renderWheel(){
 // Hidden mobile collection geometry is zero. Keep its measured rows and scroll
 // intact until it is visible again; never virtualize against display:none.
 if(!wheel.clientHeight)return;
 collectionScroll=wheel.scrollTop;
 const pad=measure(),position=wheel.scrollTop;const half=wheel.clientHeight/(SLOT*2);const range=new Set();state.center=settler.nearest(position)?.id||null;const browseId=wheelTitle.update();const centerIndex=position/SLOT;for(let i=Math.max(0,Math.floor(centerIndex-half)-3);i<=Math.min(state.results.length-1,Math.ceil(centerIndex+half)+3);i++)range.add(i);
 const keyIndex=state.results.findIndex(a=>a.id===state.keyboard);if(keyIndex>=0)range.add(keyIndex);
 const existing=new Map([...slots.children].map(el=>[el.dataset.id,el]));
 for(const i of [...range].sort((a,b)=>a-b)){
  const asset=state.results[i];let row=existing.get(asset.id);
  if(!row){row=document.createElement('div');row.className='slot';row.dataset.id=asset.id;row.id='option-'+asset.id;row.role='option';row.innerHTML='<span class="slot-marker" aria-hidden="true"></span><div class="slot-image"><img alt="" draggable="false">'+thumbnailPlaceholderMarkup()+'</div><div class="slot-copy"><strong></strong><small></small><div class="current"></div></div>';
   row.addEventListener('click',()=>choose(asset.id,{center:true}));
   slots.append(row);
  }
  existing.delete(asset.id);row.dataset.browseCenter=String(asset.id===browseId);row.dataset.nameVisible=String(asset.id===browseId);row.setAttribute('aria-label',asset.name[state.lang]||asset.name.en);row.style.top=`${pad+i*SLOT}px`;row.setAttribute('aria-selected',String(state.selected===asset.id));row.setAttribute('aria-posinset',String(i+1));row.setAttribute('aria-setsize',String(state.results.length));row.querySelector('strong').textContent=short(asset);row.querySelector('small').textContent=String(i+1).padStart(3,'0');row.querySelector('.current').textContent=state.selected===asset.id?t('CURRENT','当前'):'';
  const d=(i*SLOT-position)/SLOT,s=reduced()?1:.58+.42*Math.exp(-.65*d*d);row.querySelector('.slot-image').style.transform=`translateX(0px) scale(${s})`;row.querySelector('.slot-image').style.opacity=String(reduced()?1:Math.max(.55,1-.1*Math.abs(d)));
 }
 for(const row of existing.values()){if(row===hover.row)hover.pause();row.remove();}
 if(keyIndex>=0&&$('#option-'+state.keyboard))wheel.setAttribute('aria-activedescendant','option-'+state.keyboard);else wheel.removeAttribute('aria-activedescendant');
 const viewport=wheel.getBoundingClientRect();
 const visible=[...slots.children].map(row=>({row,index:state.results.findIndex(a=>a.id===row.dataset.id),bounds:row.querySelector('.slot-image').getBoundingClientRect()})).filter(({bounds})=>bounds.bottom>viewport.top&&bounds.top<viewport.bottom&&bounds.right>viewport.left&&bounds.left<viewport.right).sort((a,b)=>Math.abs(a.index-centerIndex)-Math.abs(b.index-centerIndex));
 // Budget follows the actual clipped viewport, not the virtualized overscan.
 // Every visible thumbnail may load together after settling; offscreen rows do not.
 thumbnails.update(visible.map(({row,index})=>({image:row.querySelector('img'),url:poster(state.results[index],{wheel:true}),fallback:urlAsset(state.results[index].preview)})));
 synchronizeThumbnailPlaceholders(all('.thumbnail-placeholder-cube'));
 clearTimeout(warmPosterTimer);warmPosterTimer=setTimeout(warmDetailPosters,180);
 $('.wheel-wrap').dataset.empty=String(!state.results.length);
 const empty=$('#empty-state');empty.hidden=!!state.results.length;wheel.tabIndex=state.results.length?0:-1;$('#empty-message').textContent=t('No models match these conditions.','没有符合这些条件的模型。');
 guides.update();
}
const settler=new WheelSettler({read:()=>wheel.scrollTop,write:value=>{setWheelPosition(value);renderWheel();},targets:()=>state.results.map((a,i)=>({id:a.id,offset:i*SLOT})),center:id=>{state.center=id;},settled:()=>hover.refresh(),reduced});
wheel.addEventListener('scroll',()=>{if(!wheel.clientHeight||restoringHistory)return;collectionScroll=wheel.scrollTop;if(programmaticPosition!==null&&Math.abs(wheel.scrollTop-programmaticPosition)<1){programmaticPosition=null;renderWheel();saveCurrentHistory();return;}programmaticPosition=null;hover.pause();settler.scrolled();renderWheel();saveCurrentHistory();},{passive:true});
wheel.addEventListener('wheel',()=>{hasBrowsed=true;hover.pause();settler.input(true);},{passive:true});wheel.addEventListener('pointerdown',event=>{hasBrowsed=true;if(event.pointerType==='touch')stopHover();else hover.pause();settler.pointerDown();},{passive:true});window.addEventListener('pointerup',()=>{if(settler.pressed)settler.pointerUp();},{passive:true});window.addEventListener('pointercancel',()=>{if(settler.pressed)settler.pointerUp();},{passive:true});wheel.addEventListener('touchstart',()=>{hasBrowsed=true;stopHover();settler.input();},{passive:true});
wheel.addEventListener('keydown',event=>{
 if(event.ctrlKey||event.metaKey||event.altKey)return;const keys=['ArrowUp','ArrowDown','Home','End','PageUp','PageDown','Enter',' '];if(!keys.includes(event.key))return;hasBrowsed=true;event.preventDefault();stopHover();settler.stop();let index=Math.max(0,state.results.findIndex(a=>a.id===state.keyboard));
 if(event.key==='Enter'||event.key===' '){if(state.results[index])choose(state.results[index].id,{center:true});return;}
 if(event.key==='Home')index=0;else if(event.key==='End')index=state.results.length-1;else index+=({ArrowUp:-1,ArrowDown:1,PageUp:-Math.max(1,Math.floor(wheel.clientHeight/SLOT)),PageDown:Math.max(1,Math.floor(wheel.clientHeight/SLOT))})[event.key];index=Math.max(0,Math.min(state.results.length-1,index));if(!state.results[index])return;state.keyboard=state.results[index].id;
 const pad=measure(),top=pad+index*SLOT;if(top<wheel.scrollTop)setWheelPosition(top);else if(top+SLOT>wheel.scrollTop+wheel.clientHeight)setWheelPosition(top+SLOT-wheel.clientHeight);renderWheel();settler.stop();saveCurrentHistory();
});
function renderSummary({animate=false}={}){
 $('#results').textContent=t(`${state.results.length} models`,`${state.results.length}个模型`);
 const active=Object.entries(state.facets).flatMap(([group,values])=>values.map(id=>({group,id,label:valueLabel(group,id)})));
 $('#filter-count').textContent=active.length?' '+active.length:'';
 ui.renderChips(active,{animate,onMore:openFilters,onRemove:({group,id},event)=>{state.facets[group]=state.facets[group].filter(v=>v!==id);applyResults(true,{animate:ui.pointer(event)});}});
 $('#excluded').hidden=state.results.some(a=>a.id===state.selected);if(state.query||active.length)$('#excluded').title=t('Modify filters to change results','修改筛选以调整结果');
}
function compute(query=state.query,facets=state.facets,sort=state.sort){const result=filterItems(sample,query,facets);if(sort==='name'||sort==='name-desc')result.sort((a,b)=>(sort==='name-desc'?-1:1)*short(a).localeCompare(short(b),state.lang));if(sort==='triangles'||sort==='triangles-asc'||sort==='triangles-desc')result.sort((a,b)=>(sort==='triangles-desc'?-1:1)*(a.triangles-b.triangles));return result;}
function applyResults(push=false,{animate=false}={}){
 state.page=0;
 const previousCount=state.results.length,focusedEmpty=$('#empty-state').contains(document.activeElement);
 stopHover();settler.stop();wheelTitle.reset();state.results=compute();state.keyboard=state.results[0]?.id||null;state.center=state.keyboard;setWheelPosition(0);renderSummary({animate});renderWheel();settler.stop();
 if(shouldAnimateBoundary(previousCount,state.results.length,animate)){
  const target=state.results.length?$('#option-'+state.results[0].id):$('#empty-state');
  if(target){target.dataset.resultArrival=String(++resultArrivalVersion);ui.reveal(target,{animate:true,duration:180});}
 }
 if(focusedEmpty&&state.results.length)wheel.focus({preventScroll:true});
 if(push)pushHistory();else saveCurrentHistory();
}
$('#empty-filters').onclick=openFilters;
$('#empty-clear').onclick=event=>{clearTimeout(searchTimer);state.query='';$('#search').value='';state.facets=emptyFacets();applyResults(true,{animate:ui.pointer(event)});};
function infoContent(asset){const c=$('#info-content');c.replaceChildren();const heading=document.createElement('h2');heading.textContent=asset.name[state.lang]||asset.name.en;c.append(heading);for(const text of [dimensionDetails(asset,state.lang),dimensionNote(state.lang),asset.reconstruction_notes?.[state.lang]||asset.description?.[state.lang],asset.scientific_scope?.[state.lang]])if(text){const p=document.createElement('p');p.textContent=text;c.append(p);}const p=document.createElement('p');p.textContent=t('Sources and provenance','来源与制作记录');c.append(p);for(const source of asset.sources||[]){if(!/^https?:/.test(source.url))continue;const a=document.createElement('a');a.href=source.url;a.target='_blank';a.rel='noopener noreferrer';a.textContent=source.title||source.id||source.url;c.append(a,document.createElement('br'));}const source=document.createElement('a');source.href=asset.source_url;source.target='_blank';source.rel='noopener noreferrer';source.textContent=t('Original asset source','原始资产来源');c.append(source);const attribution=document.createElement('p');attribution.className='attribution-copy';attribution.textContent=t('Attribution: ','署名：')+`${asset.name.en} — ${asset.author}, ${asset.license}. ${asset.source_url}`;c.append(attribution);const page=document.createElement('a');page.href=detailHref(asset.id,state.lang);page.textContent=t('Open model page','打开模型详情页');c.append(page,document.createElement('br'));for(const [key,en,zh] of [['bundle','Complete ZIP download','下载完整 ZIP'],['credits','Download attribution text','下载署名文本']])if(asset.downloads?.[key]){const link=document.createElement('a');link.href=urlAsset(asset.downloads[key]);link.download='';link.textContent=t(en,zh);c.append(link,document.createElement('br'));}c.scrollTop=0;ui.updateOverflow();}
// Replace the image node rather than changing src on a displayed, decoded
// bitmap: browsers may retain that old bitmap until the new request completes.
function updateSelectedPosterFrame(){
 const image=$('#detail-poster'),asset=sample.find(a=>a.id===state.selected);
 if(!image||image.dataset.modelId!==asset?.id)return;
 const frame=image.dataset.source==='canonical'&&validDetailPresentation(asset.detailPresentation)
  ?detailScreenFrame($('#detail').getBoundingClientRect(),{width:innerWidth,height:innerHeight},Math.min(devicePixelRatio||1,1.75)):null;
 if(frame){image.style.transformOrigin='0 0';image.style.transform=`matrix(${frame.css_matrix.join(',')})`;image.dataset.presentationFrame='native-viewport-v2';}
 else{image.style.removeProperty('transform-origin');image.style.removeProperty('transform');delete image.dataset.presentationFrame;}
}
function selectPoster(asset,version){
 cancelSelectedPoster?.();
 const previous=$('#detail-poster'),warmed=detailPosterCache.get(asset.id),image=warmed?.ready?warmed.image:document.createElement('img');
 if(warmed&&!warmed.ready){warmed.image.onload=warmed.image.onerror=null;warmed.image.removeAttribute('src');}
 detailPosterCache.delete(asset.id);image.id='detail-poster';image.alt=asset.name[state.lang]||asset.name.en;image.dataset.modelId=asset.id;image.dataset.state='loading';image.dataset.source='canonical';image.style.visibility='hidden';image.decoding='async';image.fetchPriority='high';
 const active=()=>version===selectionVersion&&state.selected===asset.id&&$('#detail-poster')===image;
 let fallback=false,frame=0,settled=false,resolveReady;
 const ready=new Promise(resolve=>resolveReady=resolve);
 const finish=value=>{if(settled)return;settled=true;if(frame)cancelAnimationFrame(frame);frame=0;resolveReady(value);};
 cancelSelectedPoster=()=>finish(false);
 const reveal=()=>{
  if(!active()){finish(false);return;}updateSelectedPosterFrame();image.dataset.state='ready';image.style.visibility='visible';image.classList.toggle('ready',currentReady);
  // A decoded cached poster still gets a real presentation opportunity before
  // its matching 3D surface can appear. No simulated network delay is added.
  const painted=phase=>{frame=0;if(!active()){finish(false);return;}if(phase===0){frame=requestAnimationFrame(()=>painted(1));return;}finish(true);};
  if(!settled&&!frame)frame=requestAnimationFrame(()=>painted(0));
 };
 image.onload=()=>{if(!active())return;Promise.resolve(image.decode?.()).then(reveal,reveal);};
 image.onerror=()=>{if(!active())return;if(!fallback){fallback=true;image.dataset.source='fallback';updateSelectedPosterFrame();image.src=urlAsset(asset.preview);}else{image.dataset.state='error';image.style.visibility='hidden';finish(false);}};
 if(previous){previous.onload=previous.onerror=null;previous.replaceWith(image);previous.removeAttribute('src');}else $('#detail').prepend(image);
 if(warmed?.ready)reveal();else{image.src=poster(asset);if(image.complete&&image.naturalWidth>0)image.onload();}
 return {image,ready};
}
async function choose(id,{push=true,openMobile=true,activateMobile=false,center=false,syncHistory=true}={}){
 const asset=sample.find(a=>a.id===id);if(!asset)return;cancelPosterWarmup();ui.resetCopy();if(push&&syncHistory)saveCurrentHistory();if(push)state.view='detail';const version=++selectionVersion;clearTimeout(selectionLoadingTimer);selectionLoadingTimer=0;closeInfo();hover.pause();settler.stop();state.selected=id;state.keyboard=id;currentReady=false;$('#detail').dataset.modelId=id;$('#detail').dataset.state='loading';$('#title').textContent=short(asset);$('#subtitle').textContent=t(categories[asset.category]?.[0]||asset.category,categories[asset.category]?.[1]||asset.category)+' / '+t('Stylized specimen','风格化示意');$('#triangles').textContent=asset.triangles.toLocaleString();$('#dimensions').textContent=modelHeight(asset);$('#file-size').textContent=Math.round((asset.glb_bytes||0)/1024)+' KB';
 $('#download').href=urlAsset(asset.glb);$('#blend').href=urlAsset(asset.blend);const selectedPoster=selectPoster(asset,version);$('#retry').hidden=true;$('#loading').textContent='';infoContent(asset);$('#comparison-label').hidden=true;$('#compare').setAttribute('aria-pressed','false');$('#compare').disabled=true;$('#wireframe').setAttribute('aria-pressed',String(renderer?.wire||false));renderSummary();renderWheel();settler.stop();
 state.mobileOpen=state.view==='detail'&&openMobile;syncMobileView();updateSelectedPosterFrame();
 if(center)settler.centerOn(id,{immediate:mobile()});
 if(syncHistory){if(push)pushHistory();else saveCurrentHistory();}
 $('#mobile-interact').hidden=!mobile();$('#mobile-interact').textContent=t(activateMobile?'Exit interaction':'Interact in 3D',activateMobile?'退出交互':'交互查看');$('#detail').style.touchAction=mobile()&&!activateMobile?'pan-y':'none';
 if(mobile()&&!activateMobile){renderer?.suspend();$('#detail').dataset.state='static';return;}
 const loadingTimer=selectionLoadingTimer=setTimeout(()=>{if(version===selectionVersion&&!currentReady)$('#loading').textContent=t('Preparing the 3D view…','正在准备3D视图…');},600);
 if(!renderer){clearTimeout(loadingTimer);showError(version,id);return;}
 try{const ready=await renderer.select(asset,{presentationReady:selectedPoster.ready});if(version!==selectionVersion||!ready)return;currentReady=true;hover.refresh();$('#detail').dataset.state='ready';$('#detail-poster').classList.add('ready');$('#loading').textContent='';$('#compare').disabled=!renderer.detail.metric?.available;$('#compare').title=renderer.detail.metric?.available?'':t('Metric scale is unverified','米制尺寸未验证');}
 catch{showError(version,id);}finally{clearTimeout(loadingTimer);if(selectionLoadingTimer===loadingTimer)selectionLoadingTimer=0;}
}
function showError(version=selectionVersion,id=state.selected){if(version!==selectionVersion||id!==state.selected)return;clearTimeout(selectionLoadingTimer);selectionLoadingTimer=0;cancelSelectedPoster?.();currentReady=false;hover.pause();$('#detail').dataset.state='fallback';$('#detail-poster').classList.remove('ready');$('#loading').textContent=t('Static preview · 3D unavailable','静态预览 · 3D暂不可用');$('#retry').hidden=false;}
function syncMobileView(){
 const open=mobile()&&state.mobileOpen;
 document.body.classList.toggle('mobile-detail',open);$('#mobile-back').hidden=!open;
 if(open){thumbnails.clear();clearTimeout(warmPosterTimer);}
 if(!open){measure();setWheelPosition(collectionScroll);renderWheel();settler.stop();}
}
function snapshot(){return {gallery:true,lang:state.lang,page:state.page,selected:state.selected,query:state.query,facets:structuredClone(state.facets),sort:state.sort,scroll:collectionScroll,keyboard:state.keyboard,mobileOpen:state.mobileOpen,view:state.view,detailDepth:state.detailDepth};}
function historyURL(){return galleryURL(state);}
function saveCurrentHistory(){if(!restoringHistory)history.replaceState(snapshot(),'',historyURL());}
function pushHistory(){
 if(restoringHistory)return;
 const previous=history.state;
 state.detailDepth=state.view==='detail'&&previous?.gallery?(previous.view==='collection'?1:previous.detailDepth>0?previous.detailDepth+1:0):0;
 history.pushState(snapshot(),'',historyURL());
}
function returnToCollection(){
 if(collectionReturnPending)return;
 stopHover();settler.stop();
 // Close owns cancellation immediately, not when asynchronous popstate arrives.
 ++selectionVersion;cancelSelectedPoster?.();clearTimeout(selectionLoadingTimer);renderer?.suspend();currentReady=false;$('#detail').dataset.state='static';$('#detail-poster').classList.remove('ready');
 // A real collection entry precedes every in-app model activation. Returning to
 // it preserves filters/scroll and makes browser Back/Forward agree with the UI.
 if(state.detailDepth>0){collectionReturnPending=true;history.go(-state.detailDepth);return;}
 // A direct/shared detail link has no owned collection entry to traverse.
 saveCurrentHistory();state.view='collection';state.detailDepth=0;state.mobileOpen=false;
 syncMobileView();pushHistory();wheel.focus({preventScroll:true});
}
window.addEventListener('popstate',async event=>{
 restoringHistory=true;collectionReturnPending=false;
 let selection;
 try{
  const saved=event.state?.gallery?event.state:null,url=new URL(location.href),route=parseRoute(url.pathname,siteRoot.pathname);
  if(route.type!=='models'){location.reload();return;}
  closeFilters(false);closeInfo();stopHover();settler.stop();
  const query=readGalleryQuery(url.searchParams),id=url.searchParams.get('model'),selected=sample.find(a=>a.id===id)?.id||sample.find(a=>a.id===saved?.selected)?.id||defaultSelection;
  Object.assign(state,query,{lang:route.lang==='zh-CN'?'zh':'en',page:route.page||0,view:id&&sample.some(a=>a.id===id)?'detail':'collection',selected,detailDepth:saved?.detailDepth||0});
  state.mobileOpen=state.view==='detail';translate();$('#search').value=state.query;state.results=compute();state.keyboard=sample.some(a=>a.id===saved?.keyboard)?saved.keyboard:selected;
  collectionScroll=Number.isFinite(saved?.scroll)?Math.max(0,saved.scroll):Math.max(0,state.results.findIndex(a=>a.id===selected))*SLOT;
  syncMobileView();renderSummary();wheelTitle.reset();renderWheel();
  // choose performs route/DOM writes synchronously, then awaits the model.
  // Release history ownership before that network wait so scroll and retries
  // remain live. Selection tokens, not a later navigation callback, own frames.
  selection=choose(selected,{push:false,syncHistory:false,openMobile:state.mobileOpen});
  state.keyboard=sample.some(asset=>asset.id===saved?.keyboard)?saved.keyboard:selected;
  syncMobileView();renderWheel();settler.stop();
 }finally{restoringHistory=false;}
 saveCurrentHistory();await selection;
});
function openFilters(event){clearTimeout(searchTimer);if(!composition&&state.query!==$('#search').value){state.query=$('#search').value;applyResults(false);}stopHover();settler.stop();if(!ui.filter.open)draft={query:state.query,facets:structuredClone(state.facets),sort:state.sort};renderFilters();ui.filter.show({animate:ui.pointer(event)});$('#filter-close').focus({preventScroll:true});}
function closeFilters(focus=true,{animate=false}={}){ui.filter.hide({animate});draft=null;if(focus)$('#filters').focus({preventScroll:true});}
function renderFilters(){if(!draft)return;const form=$('#filter-form');form.replaceChildren();for(const group of ['worlds','packs','category','triangleBand']){const field=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent=facetLabels()[group];field.append(legend);const values=document.createElement('div');values.className='filter-values';const ids=[...new Set(sample.flatMap(a=>Array.isArray(a[group])?a[group]:[a[group]]))].filter(id=>id&&id!=='unknown');for(const id of ids){const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=draft.facets[group].includes(id);input.value=id;input.dataset.group=group;input.onchange=()=>{draft.facets[group]=input.checked?[...draft.facets[group],id]:draft.facets[group].filter(v=>v!==id);updateDraftCount();};label.append(input,document.createTextNode(valueLabel(group,id)));values.append(label);}field.append(values);form.append(field);}
 const field=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent=t('Order','排序');field.append(legend);const select=document.createElement('select');select.ariaLabel=t('Sort models','模型排序');for(const [id,en,zh] of [['curated','Curated sequence','精选顺序'],['name','Name','名称'],['triangles','Triangle count','三角面数'],['triangles-desc','Triangle count: high to low','三角面数：从多到少'],['name-desc','Name: Z–A','名称：倒序']]){const option=document.createElement('option');option.value=id;option.textContent=t(en,zh);select.append(option);}select.value=draft.sort==='triangles-asc'?'triangles':draft.sort;select.onchange=()=>{draft.sort=select.value;};field.append(select);form.append(field);updateDraftCount();}
function updateDraftCount(){const n=compute(draft.query,draft.facets,draft.sort).length;$('#filter-apply').textContent=t(`Show ${n} models`,`显示${n}个模型`);}
$('#filters').onclick=event=>ui.filter.open?closeFilters(true,{animate:ui.pointer(event)}):openFilters(event);
$('#filter-close').onclick=event=>closeFilters(true,{animate:ui.pointer(event)});
$('#filter-cancel').onclick=event=>closeFilters(true,{animate:ui.pointer(event)});
$('#filter-clear').onclick=()=>{if(!draft)return;draft.query='';draft.facets=emptyFacets();renderFilters();};
$('#filter-apply').onclick=event=>{if(!draft)return;clearTimeout(searchTimer);state.query=draft.query;$('#search').value=state.query;state.facets=structuredClone(draft.facets);state.sort=draft.sort;const animate=ui.pointer(event);closeFilters(true,{animate});applyResults(true,{animate});};
$('#filter-form').onsubmit=e=>e.preventDefault();
$('#search').addEventListener('compositionstart',()=>{composition=true;clearTimeout(searchTimer);});$('#search').addEventListener('compositionend',()=>{composition=false;queueSearch();});function queueSearch(){if(composition)return;clearTimeout(searchTimer);searchTimer=setTimeout(()=>{state.query=$('#search').value;applyResults(false);},200);}$('#search').addEventListener('input',queueSearch);$('#search').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.isComposing&&!composition){clearTimeout(searchTimer);state.query=e.target.value;applyResults(false);}});
function openInfo({animate=false}={}){if(infoSuppressed)return;clearTimeout(infoCloseTimer);$('#info-close').ariaLabel=t('Close model information','关闭模型说明');ui.info.show({animate});ui.updateOverflow();}
$('#info-close').onclick=event=>closeInfo({returnFocus:true,suppress:true,animate:ui.pointer(event)});
function closeInfo({returnFocus=false,suppress=false,animate=false}={}){clearTimeout(infoOpenTimer);clearTimeout(infoCloseTimer);infoPinned=false;ui.info.hide({animate});infoSuppressed=suppress;ui.updateOverflow();if(returnFocus)$('#info').focus({preventScroll:true});}
const canHoverInfo=()=>matchMedia('(hover:hover) and (pointer:fine)').matches;
$('.info-region').addEventListener('pointerenter',event=>{if(event.pointerType==='touch'||!canHoverInfo())return;clearTimeout(infoCloseTimer);if(!infoSuppressed)infoOpenTimer=setTimeout(()=>openInfo({animate:true}),200);});
$('.info-region').addEventListener('pointerleave',event=>{if(event.pointerType==='touch'||!canHoverInfo())return;clearTimeout(infoOpenTimer);infoSuppressed=false;if(!infoPinned)infoCloseTimer=setTimeout(()=>{if(!$('.info-region').contains(document.activeElement))closeInfo({animate:true});},100);});
$('.info-region').addEventListener('focusin',()=>{if(!infoSuppressed)openInfo({animate:ui.pointerInput});});
$('.info-region').addEventListener('focusout',()=>{if(ui.info.open&&!infoPinned)infoCloseTimer=setTimeout(()=>{if(!$('.info-region').contains(document.activeElement)&&(!canHoverInfo()||!$('.info-region').matches(':hover')))closeInfo();},0);});
$('#info').onclick=event=>{if(infoPinned)closeInfo({suppress:true,animate:ui.pointer(event)});else{infoSuppressed=false;openInfo({animate:ui.pointer(event)});infoPinned=true;}};
document.addEventListener('pointerdown',event=>{if(ui.filter.open&&!$('#filter-panel').contains(event.target)&&!$('#filters').contains(event.target))closeFilters(false,{animate:true});if(!$('.info-region').contains(event.target))closeInfo({animate:true});if(renderer?.comparison&&!$('#detail').contains(event.target)&&!$('#compare').contains(event.target)){renderer.compare();$('#compare').ariaPressed='false';$('#comparison-label').hidden=true;}},{capture:true});
document.addEventListener('keydown',event=>{if(event.key!=='Escape')return;if(!$('#info-panel').hidden){event.preventDefault();event.stopPropagation();closeInfo({returnFocus:true,suppress:true});return;}if(!$('#filter-panel').hidden){event.preventDefault();closeFilters();return;}if(renderer?.comparison){renderer.compare();$('#compare').ariaPressed='false';$('#comparison-label').hidden=true;}});
$('#language').onclick=()=>{ui.resetCopy();state.lang=state.lang==='en'?'zh':'en';try{localStorage.setItem('wheel-language',state.lang);}catch{}if(state.sort==='name'||state.sort==='name-desc'){const anchor=settler.nearest(wheel.scrollTop),offset=anchor?wheel.scrollTop-anchor.offset:0;stopHover();settler.stop();state.results=compute();const index=state.results.findIndex(a=>a.id===anchor?.id);if(index>=0)setWheelPosition(index*SLOT+offset);wheelTitle.reset();}translate();renderSummary();renderWheel();saveCurrentHistory();const a=sample.find(a=>a.id===state.selected);if(!a)return;$('#title').textContent=short(a);$('#subtitle').textContent=t(categories[a.category]?.[0]||a.category,categories[a.category]?.[1]||a.category)+' / '+t('Stylized specimen','风格化示意');infoContent(a);if(draft)renderFilters();};
$('#wireframe').onclick=()=>{if(!currentReady)return;renderer.wireframe(!renderer.wire);$('#wireframe').ariaPressed=String(renderer.wire);};$('#compare').onclick=()=>{if(!currentReady)return;const result=renderer.compare();$('#compare').ariaPressed=String(!!result);$('#comparison-label').hidden=!result;if(result)updateComparisonLabel(result.kind);};$('#reset').onclick=()=>{if(currentReady){stopHover();renderer.reset();$('#compare').ariaPressed='false';$('#comparison-label').hidden=true;}};$('#retry').onclick=()=>choose(state.selected,{push:false,preserve:false,activateMobile:mobile()});$('#mobile-interact').addEventListener('pointerdown',event=>event.stopPropagation());$('#mobile-interact').onclick=()=>choose(state.selected,{push:false,preserve:false,activateMobile:!currentReady});
$('#detail').addEventListener('keydown',event=>{if(event.ctrlKey||event.metaKey||event.altKey||!currentReady)return;const action={'+':()=>renderer.zoom(.9),'=':()=>renderer.zoom(.9),'-':()=>renderer.zoom(1.1),ArrowLeft:()=>renderer.rotate(-5,0),ArrowRight:()=>renderer.rotate(5,0),ArrowUp:()=>renderer.rotate(0,5),ArrowDown:()=>renderer.rotate(0,-5)}[event.key];if(action){event.preventDefault();stopHover();action();}});
$('#credits').onclick=event=>{const asset=sample.find(a=>a.id===state.selected);if(asset)ui.copyAttribution(asset,event);};
$('#mobile-back').onclick=returnToCollection;window.addEventListener('blur',stopHover);window.addEventListener('resize',()=>{updateSelectedPosterFrame();stopHover();clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{const id=state.center,index=state.results.findIndex(a=>a.id===id);settler.stop();measure();if(index>=0)setWheelPosition(index*SLOT);renderWheel();settler.stop();syncMobileView();updateSelectedPosterFrame();renderer?.draw();},80);});matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',()=>{stopHover();settler.stop();renderWheel();});
translate();$('#search').value=state.query;state.results=compute();state.keyboard=state.selected;renderSummary();renderWheel();setWheelPosition(Number.isFinite(savedState?.scroll)?Math.max(0,savedState.scroll):Math.max(0,state.results.findIndex(a=>a.id===state.selected))*SLOT);wheelTitle.reset();renderWheel();settler.stop();
try{renderer=new PreviewRenderer($('#detail'));renderer.onReferenceError=error=>{$('#compare').ariaPressed='false';$('#comparison-label').hidden=false;$('#comparison-label').textContent=t('Reference could not load. Try again.','参照加载失败，请重试。');console.warn(error);};renderer.onInteraction=stopHover;renderer.onError=(error,context)=>{if(!context||context.assetId===state.selected)showError();};renderer.onRestore=()=>choose(state.selected,{push:false,preserve:false,activateMobile:mobile()});}catch(error){console.warn('Static fallback',error.message);}
window.__preview={state,models:sample,choose,settler,get renderer(){return renderer;},get detailPosterCacheStats(){const entries=[...detailPosterCache].map(([id,e])=>({id,ready:e.ready,width:e.image.naturalWidth,height:e.image.naturalHeight,src:e.image.currentSrc||e.image.src}));return {size:entries.length,limit:DETAIL_POSTER_CACHE_LIMIT,entries,estimatedDecodedRGBABytes:entries.filter(e=>e.ready).reduce((n,e)=>n+e.width*e.height*4,0)};},get thumbnailStats(){return thumbnails.stats;},renderWheel,returnToCollection,async generatePosters(){const output={};for(const asset of sample)output[asset.id]=await renderer.poster(asset);return output;},async generateWheelPosters(){const images={},specs={};for(const asset of sample){images[asset.id+'-wheel']=await renderer.poster(asset,{wheel:true});specs[asset.id]=renderer.lastPosterSpec;}return {images,specs};}};
if(state.selected)await choose(state.selected,{push:false,preserve:false,openMobile:hasInitialModel});else{$('#title').textContent=t('No published models yet','暂无已发布模型');$('.download-card').hidden=true;$('#detail').hidden=true;}
window.__gallery=window.__preview;

if(catalog.manifest.review_only){const note=document.createElement('span');note.className='gallery-review-notice';note.setAttribute('role','status');note.textContent=t('Review only · Not approved for publication','仅供审阅 · 尚未批准发布');document.querySelector('header').append(note);}
}
