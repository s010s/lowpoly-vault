import {downloadModelZip} from '../client-zip.js';
import {createDetailHeadingLayout} from './detail-heading-policy.js';
import './style.css';
import './thumbnail-placeholder.css';
import {thumbnailPlaceholderMarkup,synchronizeThumbnailPlaceholders} from './thumbnail-placeholder.js';
import {mountIcons} from './icons.js';
import {createUIFeedback,shouldAnimateBoundary} from './ui-feedback.js';
import {primaryDimension,dimensionDetails,dimensionNote,comparisonText} from './model-dimensions.js';
import {models,catalog,siteRoot,assetURL,readGalleryQuery,galleryURL,emptyFacets,detailHref} from './catalog-source.js';
import {parseRoute} from '../routes.js';
import {initTheme} from '../theme.js';
import {modelShortName,galleryCategoryLabel,duplicateZhNames,disambiguatedName} from './presentation-labels.js';
import {categoryLabel,isUserFacingPack,curatedPackLabel,formatBytes,formatTrianglesCompact,setStoredLang,getStoredWireframe,setStoredWireframe} from '../shared-ui.js';
import {HoverTurntable} from './hover-turntable.js';
import {HoverIntent,hoverRowAt} from './hover-intent.js';
import {ThumbnailQueue} from './thumbnail-queue.js';
import {WheelTitle} from './wheel-title.js';
import {WheelGuides} from './wheel-guides.js';
import {createWheelContinuity} from './wheel-continuity.js';
import {createPhoneContinuity,createStagePoster,detailArtwork,wheelArtwork} from './detail-continuity.js';
import {filterItems,WheelSettler} from './state.js';
import {DetailRenderer as PreviewRenderer,POSTER_IMAGE_SCALE} from './detail-renderer.js';
import {validDetailPresentation,detailScreenFrame} from './detail-presentation-policy.js';
import {createMobileActivationIntent} from './mobile-activation-intent.js';
import {canonicalEntrancePlan,hasCanonicalDetail} from './canonical-entrance.js';
// Importing this module prepares code and CSS without touching the SSG document.
// Bootstrap mounts only after every startup dependency has finished loading.
export async function mountGallery(){
mountIcons(document);
initTheme();
document.documentElement.style.setProperty('--poster-scale',POSTER_IMAGE_SCALE);
const $=selector=>document.querySelector(selector),all=selector=>[...document.querySelectorAll(selector)];
const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const mobile=()=>matchMedia('(max-width:760px)').matches;
const t=(en,zh)=>state.lang==='zh'?zh:en;
const zhDupes=duplicateZhNames(models);
const short=a=>disambiguatedName(a,state.lang,zhDupes);
const packLabels=Object.fromEntries((catalog.packs||[]).map(record=>[record.id,record.name]));
const worldLabels=Object.fromEntries((catalog.worlds||[]).map(record=>[record.id,record.name]));
const sample=models.map(a=>({...a,triangleBand:Number.isFinite(a.triangles)?a.triangles<=5000?'under5k':a.triangles<=10000?'5to10k':'over10k':'unknown'}));
const distinctWorlds=[...new Set(sample.flatMap(a=>a.worlds||[]))].filter(Boolean);
const initial=new URL(location.href).searchParams,queryState=readGalleryQuery(initial);
if(queryState.sort==='triangles')queryState.sort='triangles-asc';
const initialModel=initial.get('model'),savedState=history.state?.gallery?history.state:null;
const hasInitialModel=models.some(asset=>asset.id===initialModel);
const missingInitialModel=initialModel&&!hasInitialModel?initialModel:null;
const state={lang:catalog.route.lang==='zh-CN'?'zh':'en',page:catalog.route.page||0,...queryState,results:sample,selected:null,center:null,keyboard:null,mobileOpen:false,view:hasInitialModel?'detail':'collection',detailDepth:hasInitialModel?Math.max(0,savedState?.detailDepth||0):0};
function hasActiveCriteria(query=state.query,facets=state.facets){return Boolean(query.trim()||Object.values(facets).some(values=>values.length));}
function compute(query=state.query,facets=state.facets,sort=state.sort){
 const result=filterItems(sample,query,facets);
 if(sort==='name'||sort==='name-desc')result.sort((a,b)=>(sort==='name-desc'?-1:1)*short(a).localeCompare(short(b),state.lang));
 if(sort==='triangles'||sort==='triangles-asc'||sort==='triangles-desc')result.sort((a,b)=>(sort==='triangles-desc'?-1:1)*((a.triangles??Infinity)-(b.triangles??Infinity)));
 return result;
}
function pickDefaultSelection(results,preferredId=null){
 if(preferredId&&models.some(a=>a.id===preferredId))return preferredId;
 if(hasActiveCriteria()||(catalog.route.page||0)>0)return results[0]?.id||null;
 return (!(catalog.route.page||0)&&results.find(a=>a.id==='cooperoceras')?.id)||results[Math.min(results.length-1,(catalog.route.page||0)*24)]?.id||results[0]?.id||null;
}
const initialResults=compute();
const defaultSelection=hasInitialModel?initialModel:(savedState?.selected&&initialResults.some(a=>a.id===savedState.selected)?savedState.selected:pickDefaultSelection(initialResults));
state.results=initialResults;state.selected=defaultSelection;state.center=defaultSelection;state.keyboard=defaultSelection;
let renderer,selectionVersion=0,composition=false,searchTimer,resizeTimer,toastTimer;
let currentReady=false,programmaticPosition=null,selectionLoadingTimer=0,cancelSelectedPoster=null;
let collectionScroll=0,measuredPad=0,restoringHistory=false,collectionReturnPending=false;
let stageNoticeKind=null,compareLoadKind=null,compareError=false,mobile3DActive=false;
let zipController=null,zipVersion=0,integrityBlocked=false,filterHistoryPushed=false,focusSearchAfterReturn=false;
function cancelGalleryZip(){
 zipVersion++;zipController?.abort();zipController=null;
 const btn=$('#download-zip');
 if(btn){btn.removeAttribute('aria-busy');btn.disabled=integrityBlocked;const label=btn.querySelector('[data-en]');if(label)label.textContent=label.dataset[state.lang];}
}
const detailPosterCache=new Map(),DETAIL_POSTER_CACHE_LIMIT=8;
const thumbnails=new ThumbnailQueue();let warmPosterTimer=0,hasBrowsed=false;
function setWheelPosition(value){collectionScroll=Math.max(0,value);if(!wheel.clientHeight)return;wheel.scrollTop=collectionScroll;programmaticPosition=wheel.scrollTop;collectionScroll=wheel.scrollTop;}
const wheel=$('#wheel'),slots=$('#slots'),stage=$('#detail'),title=$('#title'),SLOT=128;
const guides=new WheelGuides({wheel,slots,wrap:$('.wheel-wrap'),left:$('.focus-guide-left'),right:$('.focus-guide-right')});
const wheelContinuity=createWheelContinuity({wheel,slots,reduced,mobile,onFinish:()=>{renderWheel();hover.refresh();}});
const stagePoster=createStagePoster(stage,reduced,mobile);
const phoneContinuity=createPhoneContinuity({main:$('main'),collection:$('.catalog'),workspace:$('.workspace'),wheel,title,reduced,stagePoster});
title.tabIndex=-1;
const ui=createUIFeedback({t,reduced,getSelection:()=>state.selected});
const mobileInteract=$('#mobile-interact'),stageEnter3D=$('#stage-enter-3d');
const mobileIntentStatus=document.createElement('span');
mobileIntentStatus.className='sr-only';
mobileIntentStatus.setAttribute('role','status');
mobileIntentStatus.setAttribute('aria-atomic','true');
mobileInteract.after(mobileIntentStatus);
// A visual mirror only: the separate mobile live region already announces the intent.
const mobilePendingCopy=document.createElement('span');
mobilePendingCopy.setAttribute('aria-hidden','true');
function clearMobilePendingCopy(){mobilePendingCopy.remove();}
function showMobilePendingCopy(){
 const image=$('#detail-poster'),loading=$('#loading');
 if(stage.dataset.state!=='static'||loading.textContent||!image||image.dataset.modelId!==state.selected||
  image.dataset.source!=='canonical'||image.dataset.state!=='loading'||image.style.visibility!=='hidden'||
  stagePoster.frame(state.selected))return;
 mobilePendingCopy.textContent=t('Preparing the model preview…','正在准备模型预览…');
 loading.append(mobilePendingCopy);
}
const mobileIntent=createMobileActivationIntent({
 eligible({id,sha,src,version,image},mode){
  if(!mobile()||document.hidden||collectionReturnPending||state.view!=='detail'||!state.mobileOpen||
   !document.body.classList.contains('mobile-detail')||stage.dataset.state!=='static'||
   version!==selectionVersion||state.selected!==id||$('#detail-poster')!==image||
   !image.isConnected||image.dataset.modelId!==id||image.dataset.glbSha!==sha)return false;
  if(mode==='pending')return true;
  if(stagePoster.frame(id))return false;
  if(mode==='missing')return image.dataset.state==='error'&&image.dataset.source==='unavailable';
  const style=getComputedStyle(image),box=image.getBoundingClientRect();
  return image.dataset.source==='canonical'&&image.dataset.state==='ready'&&image.currentSrc===src&&
   image.complete&&image.naturalWidth>0&&image.naturalHeight>0&&style.visibility==='visible'&&
   Number(style.opacity)===1&&box.width>0&&box.height>0;
 },
 activate({id}){void choose(id,{push:false,preserve:false,activateMobile:true});},
 announce(status){
  const busy=status==='pending';
  mobileInteract.setAttribute('aria-busy',String(busy));
  stageEnter3D.setAttribute('aria-busy',String(busy));
  stageEnter3D.disabled=busy;
  if(busy){stageEnter3D.querySelector('[data-en]').textContent=t('Loading 3D…','正在载入 3D…');showMobilePendingCopy();}
  else{mobileInteract.removeAttribute('aria-busy');stageEnter3D.removeAttribute('aria-busy');stageEnter3D.disabled=false;stageEnter3D.querySelector('[data-en]').textContent=t('Inspect in 3D','进入 3D 查看');clearMobilePendingCopy();}
  mobileIntentStatus.textContent=busy?t('Opening 3D view…','正在打开 3D 视图…'):
   status==='unavailable'?t('Preview unavailable. Opening 3D view…','预览图暂不可用，正在直接打开 3D 视图…'):'';
 }
});
document.addEventListener('visibilitychange',()=>{if(document.hidden)mobileIntent.cancel();});
window.addEventListener('pagehide',()=>{mobileIntent.cancel();cancelGalleryZip();});
matchMedia('(max-width:760px)').addEventListener('change',()=>{
 mobileIntent.cancel();
 syncMobileView();
 if(!state.selected)return;
 if(!mobile()){
  mobile3DActive=false;
  if(stage.dataset.state==='static')void choose(state.selected,{push:false,syncHistory:false,openMobile:false});
 }else{
  if(state.mobileOpen&&stage.dataset.state!=='static'){
   mobile3DActive=true;
   $('#detail').style.touchAction='none';
  }else{
   mobile3DActive=false;
   $('#detail').style.touchAction='pan-y';
   if(stage.dataset.state==='ready'||stage.dataset.state==='loading'){renderer?.suspend();stage.dataset.state='static';currentReady=false;}
  }
  syncMobileChrome();
 }
});
function disposeUI(){cancelGalleryZip();mobileIntent.clear();phoneContinuity.stop();stagePoster.clear();wheelContinuity.stop();hover.clear();thumbnails.clear();clearTimeout(warmPosterTimer);clearTimeout(searchTimer);clearTimeout(toastTimer);guides.dispose();ui.dispose();}
const wheelTitle=new WheelTitle({read:()=>wheel.scrollTop,targets:()=>state.results.map((a,i)=>({id:a.id,offset:i*SLOT})),change:()=>renderWheel()});
window.addEventListener('pagehide',event=>{if(!event.persisted){cancelSelectedPoster?.();renderer?.suspend();wheelTitle.dispose();settler.dispose();disposeUI();}});
if(import.meta.hot)import.meta.hot.dispose(()=>{cancelSelectedPoster?.();renderer?.suspend();wheelTitle.dispose();settler.dispose();disposeUI();});
const urlAsset=assetURL;
function poster(asset,{wheel=false}={}){return urlAsset(asset.galleryPosters?.[wheel?'wheel':'detail']||asset.preview);}
function cacheDetailPoster(id,entry){
 detailPosterCache.set(id,entry);
 if(detailPosterCache.size<=DETAIL_POSTER_CACHE_LIMIT)return;
 const [oldId,old]=detailPosterCache.entries().next().value;
 old.image.onload=old.image.onerror=null;old.image.removeAttribute('src');detailPosterCache.delete(oldId);
}
function warmDetailPosters(){
 if(!hasBrowsed||!currentReady||mobile()||!wheel.clientHeight||navigator.connection?.saveData)return;
 const center=Math.max(0,Math.round(wheel.scrollTop/SLOT));
 const nearby=state.results.slice(Math.max(0,center-1),center+2);
 for(const [id,entry] of detailPosterCache)if(!entry.ready&&!nearby.some(asset=>asset.id===id)){entry.image.onload=entry.image.onerror=null;entry.image.removeAttribute('src');detailPosterCache.delete(id);}
 for(const asset of nearby){
  if(asset.id===state.selected||detailPosterCache.has(asset.id)||!asset.galleryPosters?.detail)continue;
  const image=document.createElement('img'),entry={image,ready:false};image.dataset.glbSha=asset.sha256?.glb||'';image.decoding='async';cacheDetailPoster(asset.id,entry);
  image.onload=()=>{Promise.resolve(image.decode?.()).then(()=>{if(detailPosterCache.get(asset.id)===entry)entry.ready=true;},()=>{});};
  image.onerror=()=>{if(detailPosterCache.get(asset.id)===entry)detailPosterCache.delete(asset.id);};image.src=poster(asset);
 }
}
function cancelPosterWarmup(){
 clearTimeout(warmPosterTimer);
 for(const [id,entry] of detailPosterCache)if(!entry.ready){entry.image.onload=entry.image.onerror=null;entry.image.removeAttribute('src');detailPosterCache.delete(id);}
}
function toast(message,{actionLabel=null,onAction=null,duration=2800}={}){
 const host=$('#toast'),msg=$('#toast-message'),btn=$('#toast-action');
 msg.textContent=message;
 if(actionLabel&&onAction){btn.textContent=actionLabel;btn.hidden=false;btn.onclick=event=>{host.classList.remove('visible');onAction(event);};}
 else{btn.hidden=true;btn.onclick=null;}
 host.classList.add('visible');clearTimeout(toastTimer);
 toastTimer=setTimeout(()=>host.classList.remove('visible'),actionLabel?4500:duration);
}
function stageHintText(){
 if(renderer?.comparison)return mobile()?t('Drag horizontally to turn · Pinch to zoom','水平拖动旋转 · 双指缩放'):t('Drag horizontally to turn · Scroll to zoom','水平拖动旋转 · 滚轮缩放');
 return mobile()?t('Drag to rotate · Pinch to zoom','单指拖动旋转 · 双指缩放'):t('Drag to rotate · Scroll to zoom','拖动旋转 · 滚轮缩放');
}
function syncStageHint(){
 const hint=$('#stage-hint');if(!hint)return;
 hint.textContent=stageHintText();
 hint.hidden=!state.selected||(mobile()&&!mobile3DActive);
}
function syncStageTools(){
 const tools=$('#stage-tools');
 const hideMobileTools=mobile()&&!mobile3DActive;
 tools.hidden=hideMobileTools||!state.selected;
 $('#wireframe').disabled=!currentReady;
 $('#zoom-in').disabled=!currentReady;
 $('#zoom-out').disabled=!currentReady;
 $('#reset').disabled=!currentReady||!renderer?.dirty;
 const metricAvailable=Boolean(currentReady&&renderer?.detail?.metric?.available);
 $('#compare').hidden=!metricAvailable;
 $('#compare').disabled=!metricAvailable;
}
function syncMobileChrome(){
 const isPhone=mobile();
 $('#mobile-interact').hidden=!isPhone||!mobile3DActive;
 $('#mobile-interact').textContent=t('Exit 3D','退出 3D');
 const showEnter=isPhone&&!mobile3DActive&&Boolean(state.selected)&&stage.dataset.state==='static';
 stageEnter3D.hidden=!showEnter;
 if(showEnter&&!stageEnter3D.disabled)stageEnter3D.querySelector('[data-en]').textContent=t('Inspect in 3D','进入 3D 查看');
 const idx=state.results.findIndex(a=>a.id===state.selected);
 const stepper=$('#mobile-stepper');
 const showStepper=isPhone&&state.mobileOpen&&idx>=0&&state.results.length>1;
 stepper.hidden=!showStepper;
 if(showStepper){
  $('#mobile-position').textContent=`${idx+1} / ${state.results.length}`;
  $('#mobile-prev').disabled=idx<=0;
  $('#mobile-next').disabled=idx>=state.results.length-1;
  const prevAsset=state.results[idx-1],nextAsset=state.results[idx+1];
  $('#mobile-prev').ariaLabel=prevAsset?t(`Previous model: ${short(prevAsset)}`,`上一个模型：${short(prevAsset)}`):t('Previous model','上一个模型');
  $('#mobile-next').ariaLabel=nextAsset?t(`Next model: ${short(nextAsset)}`,`下一个模型：${short(nextAsset)}`):t('Next model','下一个模型');
 }
 syncStageHint();
 syncStageTools();
}
function updateComparisonLabel(kind){
 const label=$('#comparison-label');
 label.dataset.kind=kind||'';
 if(compareError){label.textContent=t('Could not load scale reference. Try again.','参照加载失败，请重试。');return;}
 if(compareLoadKind){label.textContent=t('Loading scale reference…','正在载入尺寸参照…');return;}
 if(kind)label.textContent=comparisonText(kind,state.lang,sample.find(asset=>asset.id===state.selected));
}
function renderSortOptions(){
 const select=$('#sort-select');if(!select)return;
 const current=state.sort==='triangles'?'triangles-asc':state.sort;
 select.replaceChildren();
 for(const [id,en,zh] of [
  ['curated','Curated','精选顺序'],
  ['name','Name (A–Z)','名称（A–Z）'],
  ['name-desc','Name (Z–A)','名称（Z–A）'],
  ['triangles-asc','Triangles (low–high)','三角面（少到多）'],
  ['triangles-desc','Triangles (high–low)','三角面（多到少）'],
 ]){
  const option=document.createElement('option');
  option.value=id;option.textContent=t(en,zh);
  select.append(option);
 }
 select.value=current;
 select.ariaLabel=t('Sort models','模型排序');
}
function syncLoadingCopy(){
 if(!stageNoticeKind)return;
 const messages={
  preparing:t('Preparing preview…','正在准备预览…'),
  loading3d:t('Loading 3D model…','正在载入 3D 模型…'),
  previewUnavailableLoading:t('Preview unavailable · loading 3D model…','预览图暂不可用，正在载入 3D 模型…'),
  previewUnavailableStatic:t('Preview unavailable · tap Inspect in 3D','预览图暂不可用，点击下方进入 3D 查看'),
  previewAnd3dUnavailable:t('Preview and 3D unavailable. Please retry.','预览图与 3D 暂不可用，请重试。'),
  staticFallback:t('3D unavailable here · showing rendered preview','当前无法加载 3D，已展示渲染预览'),
  integrityFailed:t('File check failed. Preview and downloads are paused to avoid corrupted files — please retry.','文件校验未通过，为避免下到损坏文件已暂停预览与下载，请重试。'),
 };
 $('#loading').textContent=messages[stageNoticeKind]||'';
}
function setStageNotice(kind){stageNoticeKind=kind;if(!kind){$('#loading').textContent='';return;}syncLoadingCopy();}
function syncMissingBanner(){
 const banner=$('#missing-banner');
 if(!banner||banner.hidden)return;
 const id=banner.dataset.missingId||'';
 $('#missing-text').textContent=t(`Couldn’t find model “${id}”. Showing a featured model instead.`,`未找到模型「${id}」，已为你展示推荐模型。`);
 $('#missing-close').ariaLabel=t('Dismiss notice','关闭提示');
}
function updateSearchClear(){
 const input=$('#search'),clearBtn=$('#search-clear');
 clearBtn.hidden=!input.value;
 clearBtn.ariaLabel=t('Clear search','清除搜索词');
}
function translate(){
 $('#gallery-github').ariaLabel=t('GitHub repository (opens in a new tab)','GitHub 代码仓库（在新标签页打开）');
 document.documentElement.lang=state.lang==='zh'?'zh-CN':'en';
 document.title=t('All models | Lowpoly Vault','全部模型 | Lowpoly Vault');
 for(const link of all('[data-gallery-route]'))link.href=new URL((state.lang==='zh'?'zh-CN/':'')+(link.dataset.galleryRoute==='home'?'':'about/'),siteRoot).href;
 all('[data-en]').forEach(el=>el.textContent=el.dataset[state.lang]);
 if(stageEnter3D.getAttribute('aria-busy')==='true'){const l=stageEnter3D.querySelector('[data-en]');if(l)l.textContent=t('Loading 3D…','正在载入 3D…');}
 if($('#download-zip').getAttribute('aria-busy')==='true'){const l=$('#download-zip').querySelector('[data-en]');if(l)l.textContent=t('Preparing ZIP…','正在打包 ZIP…');}
 $('#language').textContent=state.lang==='zh'?'EN':'中文';
 $('#language').ariaLabel=state.lang==='zh'?'Switch to English':'切换为简体中文';
 $('#search').placeholder=t('Search models…','搜索模型…');
 $('#search').ariaLabel=t('Search models','搜索模型');
 wheel.ariaLabel=t('Models','模型列表');
 $('#info').ariaLabel=t('Model details','模型说明');
 $('#info-close').ariaLabel=t('Close model details','关闭模型说明');
 $('#detail').ariaLabel=t('3D model. Drag to rotate, scroll or plus/minus to zoom, arrow keys to rotate, Home or R to reset.','3D 模型。拖动旋转，滚轮或加减键缩放，方向键旋转，按 Home 或 R 重置视角。');
 $('#filters').setAttribute('aria-label',t('Filters','筛选'));
 $('#filter-close').setAttribute('aria-label',t('Close filters','关闭筛选'));
 $('#info-content').setAttribute('aria-label',t('Model details and sources','模型说明与来源'));
 $('#zoom-in').ariaLabel=t('Zoom in','放大');
 $('#zoom-out').ariaLabel=t('Zoom out','缩小');
 renderSortOptions();
 updateSearchClear();
 syncStageHint();
 syncMobileChrome();
 syncLoadingCopy();
 syncMissingBanner();
 if((renderer?.comparison||compareLoadKind||compareError)&&!$('#comparison-label').hidden)updateComparisonLabel($('#comparison-label').dataset.kind);
}
function facetLabels(){return {worlds:t('World','世界主题'),collection:t('Collection','合集'),triangleMax:t('Maximum triangles','三角面数上限'),packs:t('Collections','精选合集'),category:t('Category','分类'),triangleBand:t('Triangles','三角面数')};}
function valueLabel(group,id){
 if(group==='worlds'||group==='collection')return worldLabels[id]?.[state.lang]||id;
 if(group==='triangleMax')return t(`Up to ${Number(id).toLocaleString('en-US')}`,`${Number(id).toLocaleString('zh-CN')} 以下`);
 if(group==='category')return categoryLabel(id,state.lang);
 if(group==='packs')return curatedPackLabel(id,state.lang,packLabels);
 return {under5k:t('Up to 5,000','5,000 以下'),'5to10k':t('5,001 – 10,000','5,001 – 10,000'),over10k:t('Over 10,000','10,000 以上')}[id]||id;
}
function measure(){if(!wheel.clientHeight)return measuredPad;const pad=measuredPad=Math.max(0,wheel.clientHeight/2-SLOT/2);slots.style.height=`${state.results.length*SLOT+pad*2}px`;slots.style.setProperty('--pad',pad+'px');return pad;}
const hover=new HoverIntent({
 hit:point=>hoverRowAt(document,wheel,slots,point),
 enabled:()=>!document.hidden&&!reduced()&&!wheelContinuity.active&&matchMedia('(hover:hover) and (pointer:fine)').matches,
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
function syncJumpCurrent(){
 const jump=$('#jump-current'),hintCopy=$('#list-hint-copy');
 if(!jump||!hintCopy)return;
 const idx=state.results.findIndex(a=>a.id===state.selected);
 if(idx<0||!wheel.clientHeight){jump.hidden=true;hintCopy.hidden=false;return;}
 const top=measuredPad+idx*SLOT,bottom=top+SLOT;
 const outOfView=bottom<wheel.scrollTop+8||top>wheel.scrollTop+wheel.clientHeight-8;
 jump.hidden=!outOfView;
 hintCopy.hidden=outOfView;
}
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
  if(!row){row=document.createElement('div');row.className='slot';row.dataset.id=asset.id;row.id='option-'+asset.id;row.role='option';row.innerHTML='<div class="slot-motion"><span class="slot-marker" aria-hidden="true"></span><div class="slot-image"><img alt="" draggable="false">'+thumbnailPlaceholderMarkup()+'</div><div class="slot-copy"><strong></strong><small></small><div class="current"></div></div></div>';
   row.addEventListener('click',()=>choose(asset.id,{center:true}));
   slots.append(row);
  }
  existing.delete(asset.id);row.dataset.browseCenter=String(asset.id===browseId);row.dataset.nameVisible='true';row.dataset.keyboardActive=String(asset.id===state.keyboard);row.setAttribute('aria-label',asset.name[state.lang]||asset.name.en);row.style.top=`${pad+i*SLOT}px`;row.setAttribute('aria-selected',String(state.selected===asset.id));row.setAttribute('aria-posinset',String(i+1));row.setAttribute('aria-setsize',String(state.results.length));row.querySelector('strong').textContent=short(asset);row.querySelector('small').textContent=[galleryCategoryLabel(asset.category,state.lang),formatTrianglesCompact(asset.triangles)].filter(Boolean).join(' · ');row.querySelector('.current').textContent=state.selected===asset.id?t('Viewing','查看中'):'';
  const d=(i*SLOT-position)/SLOT,s=reduced()?1:.58+.42*Math.exp(-.65*d*d);row.querySelector('.slot-image').style.transform=`translateX(0px) scale(${s})`;row.querySelector('.slot-image').style.opacity=String(reduced()?1:Math.max(.55,1-.1*Math.abs(d)));
 }
 for(const row of existing.values()){if(row===hover.row)hover.pause();row.remove();}
 if(keyIndex>=0&&$('#option-'+state.keyboard))wheel.setAttribute('aria-activedescendant','option-'+state.keyboard);else wheel.removeAttribute('aria-activedescendant');
 const viewport=wheel.getBoundingClientRect();
 const visible=[...slots.children].map(row=>({row,index:state.results.findIndex(a=>a.id===row.dataset.id),bounds:row.querySelector('.slot-image').getBoundingClientRect()})).filter(({bounds})=>bounds.bottom>viewport.top&&bounds.top<viewport.bottom&&bounds.right>viewport.left&&bounds.left<viewport.right).sort((a,b)=>Math.abs(a.index-centerIndex)-Math.abs(b.index-centerIndex));
 thumbnails.update(visible.map(({row,index})=>({image:row.querySelector('img'),url:poster(state.results[index],{wheel:true}),fallback:urlAsset(state.results[index].preview)})));
 synchronizeThumbnailPlaceholders(all('.thumbnail-placeholder-cube'));
 clearTimeout(warmPosterTimer);warmPosterTimer=setTimeout(warmDetailPosters,180);
 $('.wheel-wrap').dataset.empty=String(!state.results.length);
 const empty=$('#empty-state');empty.hidden=!!state.results.length;wheel.tabIndex=state.results.length?0:-1;$('#empty-message').textContent=t('No models match these conditions.','没有符合这些条件的模型。');
 syncJumpCurrent();
 guides.update();
}
const settler=new WheelSettler({read:()=>wheel.scrollTop,write:value=>{setWheelPosition(value);renderWheel();},targets:()=>state.results.map((a,i)=>({id:a.id,offset:i*SLOT})),center:id=>{state.center=id;},settled:()=>hover.refresh(),reduced});
wheel.addEventListener('scroll',()=>{if(!wheel.clientHeight||restoringHistory)return;collectionScroll=wheel.scrollTop;if(programmaticPosition!==null&&Math.abs(wheel.scrollTop-programmaticPosition)<1){programmaticPosition=null;if(!wheelContinuity.active)renderWheel();saveCurrentHistory();return;}programmaticPosition=null;phoneContinuity.stop();wheelContinuity.stop();hover.pause();settler.scrolled();renderWheel();saveCurrentHistory();},{passive:true});
wheel.addEventListener('wheel',()=>{hasBrowsed=true;hover.pause();settler.input(true);},{passive:true});wheel.addEventListener('pointerdown',event=>{hasBrowsed=true;if(event.pointerType==='touch')stopHover();else hover.pause();settler.pointerDown();},{passive:true});window.addEventListener('pointerup',()=>{if(settler.pressed)settler.pointerUp();},{passive:true});window.addEventListener('pointercancel',()=>{if(settler.pressed)settler.pointerUp();},{passive:true});wheel.addEventListener('touchstart',()=>{hasBrowsed=true;stopHover();settler.input();},{passive:true});
wheel.addEventListener('keydown',event=>{
 if(event.ctrlKey||event.metaKey||event.altKey)return;const keys=['ArrowUp','ArrowDown','Home','End','PageUp','PageDown','Enter',' '];if(!keys.includes(event.key))return;hasBrowsed=true;event.preventDefault();stopHover();settler.stop();let index=Math.max(0,state.results.findIndex(a=>a.id===state.keyboard));
 if(event.key==='Enter'||event.key===' '){if(state.results[index])choose(state.results[index].id,{center:true});return;}
 phoneContinuity.stop();wheelContinuity.stop();
 if(event.key==='Home')index=0;else if(event.key==='End')index=state.results.length-1;else index+=({ArrowUp:-1,ArrowDown:1,PageUp:-Math.max(1,Math.floor(wheel.clientHeight/SLOT)),PageDown:Math.max(1,Math.floor(wheel.clientHeight/SLOT))})[event.key];index=Math.max(0,Math.min(state.results.length-1,index));if(!state.results[index])return;state.keyboard=state.results[index].id;
 setWheelPosition(index*SLOT);renderWheel();settler.stop();saveCurrentHistory();
});
function activeFacetEntries(){return Object.entries(state.facets).flatMap(([group,values])=>values.map(id=>({group,id,label:valueLabel(group,id)})));}
function renderSummary({animate=false}={}){
 const locale=state.lang==='zh'?'zh-CN':'en-US';
 $('#results').textContent=t(`${state.results.length.toLocaleString(locale)} models`,`${state.results.length.toLocaleString(locale)} 个模型`);
 const active=activeFacetEntries();
 $('#filter-count').textContent=active.length?' '+active.length:'';
 ui.renderChips(active,{
  animate,
  onMore:openFilters,
  onRemove:({group,id},event)=>{state.facets[group]=state.facets[group].filter(v=>v!==id);applyResults(true,{animate:ui.pointer(event)});},
  onClearAll:event=>{state.facets=emptyFacets();applyResults(true,{animate:ui.pointer(event)});},
 });
 const excluded=Boolean(state.selected&&!state.results.some(a=>a.id===state.selected));
 $('#excluded').hidden=!excluded;
 $('#excluded-first').hidden=!excluded||!state.results.length;
 $('#excluded-clear').hidden=!excluded;
 syncMobileChrome();
}
function showEmptyWorkspace(){
 cancelGalleryZip();integrityBlocked=false;
 state.selected=null;state.keyboard=null;currentReady=false;mobile3DActive=false;
 renderer?.suspend();stagePoster.clear();closeInfo();
 $('.heading').hidden=true;$('.detail-media').hidden=true;$('.workspace-bottom').hidden=true;$('#comparison-label').hidden=true;$('#stage-hint').hidden=true;
 $('#workspace-empty').hidden=false;
 syncMobileChrome();
}
function showModelWorkspace(){
 $('.heading').hidden=false;$('.detail-media').hidden=false;$('.workspace-bottom').hidden=false;
 $('#workspace-empty').hidden=true;
}
function applyResults(push=false,{animate=false,autoSelectIfExcluded=false,autoSelectFirst=false}={}){
 state.page=0;
 const previousCount=state.results.length,focusedEmpty=$('#empty-state').contains(document.activeElement);
 phoneContinuity.stop();stopHover();settler.stop();
 wheelContinuity.update(()=>{
  wheelTitle.reset();state.results=compute();state.keyboard=state.results[0]?.id||null;state.center=state.keyboard;setWheelPosition(0);renderSummary({animate});renderWheel();settler.stop();
 },{keyboard:!animate});
 if((!state.results.length||!wheel.animate)&&shouldAnimateBoundary(previousCount,state.results.length,animate)){
  const target=state.results.length?$('#option-'+state.results[0].id):$('#empty-state');
  if(target)ui.reveal(target,{animate:true,duration:180});
 }
 if(focusedEmpty&&state.results.length)wheel.focus({preventScroll:true});
 if(ui.filter.open)renderFilters();
 const excluded=!state.results.some(a=>a.id===state.selected);
 if(!state.results.length&&!state.selected){showEmptyWorkspace();}
 else if(state.results.length&&(autoSelectFirst||!state.selected||(autoSelectIfExcluded&&excluded))){
  void choose(state.results[0].id,{push,openMobile:false,center:true});
  return;
 }
 if(push)pushHistory();else saveCurrentHistory();
}
function clearSearchAndFilters(event){
 clearTimeout(searchTimer);state.query='';$('#search').value='';updateSearchClear();state.facets=emptyFacets();
 applyResults(true,{animate:ui.pointer(event),autoSelectIfExcluded:true});
}
$('#empty-filters').onclick=openFilters;
$('#empty-clear').onclick=clearSearchAndFilters;
$('#workspace-empty-clear').onclick=clearSearchAndFilters;
$('#excluded-first').onclick=()=>{if(state.results[0])void choose(state.results[0].id,{push:true,center:true});};
$('#excluded-clear').onclick=event=>{
 if(Object.values(state.facets).some(v=>v.length)){state.facets=emptyFacets();applyResults(true,{animate:ui.pointer(event)});}
 else clearSearchAndFilters(event);
};
$('#jump-current').onclick=()=>{if(state.selected)settler.centerOn(state.selected);};
function assetSummaryLine(asset){
 const cat=galleryCategoryLabel(asset.category,state.lang);
 const raw=asset.description?.[state.lang]||asset.reconstruction_notes?.[state.lang]||'';
 const firstSentence=raw.split(/[。.!?！？]/)[0]?.trim()||'';
 if(!firstSentence||firstSentence.length>72||/stylized|风格化|Blender|教学模型|teaching specimen/i.test(firstSentence))return cat;
 return `${cat} · ${firstSentence}`;
}
function infoContent(asset){
 const c=$('#info-content');c.replaceChildren();
 const heading=document.createElement('h2');heading.textContent=short(asset);c.append(heading);
 // 1. What is this model? Put description first so users understand the subject immediately.
 const desc=asset.reconstruction_notes?.[state.lang]||asset.description?.[state.lang];
 if(desc){const p=document.createElement('p');p.className='info-description';p.textContent=desc;c.append(p);}
 // 2. Dimensions & concise artistic-scale disclaimer tucked right beneath.
 const dimBlock=document.createElement('div');dimBlock.className='info-dimensions';
 const dimLine=document.createElement('p');dimLine.textContent=dimensionDetails(asset,state.lang);dimBlock.append(dimLine);
 const noteLine=document.createElement('p');noteLine.className='info-note';noteLine.textContent=dimensionNote(state.lang,asset);dimBlock.append(noteLine);
 c.append(dimBlock);
 // 3. Scientific scope (only if present and distinct from description).
 const scope=asset.scientific_scope?.[state.lang];
 if(scope&&scope!==desc){
  const scopeTitle=document.createElement('h3');scopeTitle.textContent=t('Scientific scope','科学说明');c.append(scopeTitle);
  const p=document.createElement('p');p.textContent=scope;c.append(p);
 }
 // 4. Reference sources (only render heading when actual links exist).
 const validSources=(asset.sources||[]).filter(source=>/^https?:/.test(source.url||''));
 if(validSources.length){
  const srcTitle=document.createElement('h3');srcTitle.textContent=t('Sources','参考来源');c.append(srcTitle);
  const list=document.createElement('ul');list.className='info-sources';
  for(const source of validSources){
   const li=document.createElement('li'),a=document.createElement('a');
   a.href=source.url;a.target='_blank';a.rel='noopener noreferrer';a.textContent=`${source.title||source.id||source.url} ↗`;
   li.append(a);list.append(li);
  }
  c.append(list);
 }
 // 5. Utility links (standalone page, GitHub source, credits download).
 const links=document.createElement('div');links.className='info-links';
 const page=document.createElement('a');page.href=detailHref(asset.id,state.lang);page.textContent=t('Open standalone model page →','打开独立详情页 →');links.append(page);
 const source=document.createElement('a');source.href=asset.source_url;source.target='_blank';source.rel='noopener noreferrer';source.textContent=t('Source repository ↗','GitHub 源码仓库 ↗');links.append(source);
 if(asset.downloads?.credits){
  const link=document.createElement('a');link.href=urlAsset(asset.downloads.credits);link.download='';link.textContent=t('Download attribution text','下载署名文本');links.append(link);
 }
 c.append(links);
 c.scrollTop=0;ui.updateOverflow();
}
function updateSelectedPosterFrame(){
 const image=$('#detail-poster'),asset=sample.find(a=>a.id===state.selected);
 if(!image||image.dataset.modelId!==asset?.id)return;
 const frame=image.dataset.source==='canonical'&&validDetailPresentation(asset.detailPresentation)
  ?detailScreenFrame($('#detail').getBoundingClientRect(),{width:innerWidth,height:innerHeight},Math.min(devicePixelRatio||1,1.75)):null;
 if(frame){image.style.transformOrigin='0 0';image.style.transform=`matrix(${frame.css_matrix.join(',')})`;image.dataset.presentationFrame='native-viewport-v2';}
 else{image.style.removeProperty('transform-origin');image.style.removeProperty('transform');delete image.dataset.presentationFrame;}
}
const detailHeadingLayout=createDetailHeadingLayout({heading:$('.workspace .heading'),title:$('#title'),stage:$('#detail'),footer:$('.workspace-bottom'),button:$('#mobile-interact'),tools:$('.workspace-bottom .tools'),download:$('.workspace-bottom .download-card'),isMobile:mobile});
document.fonts?.ready.then(()=>detailHeadingLayout.refresh());
function selectPoster(asset,version,source,{beforeCanonicalVisible,desktopCanonical=false}={}){
 cancelSelectedPoster?.();
 const isPhone=mobile(),previous=$('#detail-poster'),cachedWarm=detailPosterCache.get(asset.id),warmed=cachedWarm?.ready&&cachedWarm.image.complete&&cachedWarm.image.naturalWidth>0&&cachedWarm.image.dataset.glbSha===asset.sha256?.glb&&cachedWarm.image.currentSrc===new URL(poster(asset),location.href).href?cachedWarm:null;
 const sameDecoded=!!(previous&&previous.dataset.modelId===asset.id&&previous.dataset.glbSha===asset.sha256?.glb&&previous.dataset.source==='canonical'&&previous.dataset.state==='ready'&&previous.complete&&previous.naturalWidth>0&&previous.currentSrc===new URL(poster(asset),location.href).href);
 const image=sameDecoded?previous:warmed?.ready?warmed.image:document.createElement('img');
 if(sameDecoded)stagePoster.clear();
 const bridge=sameDecoded?null:stagePoster.prepare(asset.id,warmed?.ready&&!isPhone?null:source);
 if(cachedWarm&&cachedWarm.image!==image){cachedWarm.image.onload=cachedWarm.image.onerror=null;cachedWarm.image.removeAttribute('src');}
 detailPosterCache.delete(asset.id);image.id='detail-poster';image.alt=asset.name[state.lang]||asset.name.en;image.dataset.modelId=asset.id;image.dataset.glbSha=asset.sha256?.glb||'';image.dataset.state=sameDecoded?'ready':'loading';image.dataset.source='canonical';image.style.visibility=sameDecoded?'visible':'hidden';image.style.removeProperty('opacity');image.style.removeProperty('transition');image.decoding='async';image.fetchPriority='high';
 const active=()=>version===selectionVersion&&state.selected===asset.id&&$('#detail-poster')===image&&image.dataset.state!=='invalid-version';
 let frame=0,settled=false,revealing=false,resolveReady;
 const ready=new Promise(resolve=>resolveReady=resolve);
 const finish=value=>{if(settled)return;settled=true;if(frame)cancelAnimationFrame(frame);frame=0;resolveReady(value);};
 cancelSelectedPoster=()=>finish(false);
 const reveal=()=>{
  if(!active()){finish(false);return;}if(revealing)return;revealing=true;clearMobilePendingCopy();updateSelectedPosterFrame();image.dataset.state='ready';image.classList.toggle('ready',currentReady);
  if(desktopCanonical&&(!image.complete||!image.naturalWidth||!image.naturalHeight||image.currentSrc!==new URL(poster(asset),location.href).href)){image.onerror();return;}
  const painted=phase=>{frame=0;if(!active()){finish(false);return;}if(phase===0){frame=requestAnimationFrame(()=>painted(1));return;}finish(true);};
  const acknowledge=()=>{if(!settled)frame=requestAnimationFrame(()=>painted(0));};
  if(bridge)Promise.resolve().then(()=>active()&&stagePoster.reveal(image)).then(acknowledge);
  else{
   if(desktopCanonical){image.classList.remove('ready');image.style.transition='none';image.style.opacity='1';}
   beforeCanonicalVisible?.();image.style.visibility='visible';acknowledge();
  }
 };
 image.onload=()=>{if(!active())return;Promise.resolve(image.decode?.()).then(reveal,reveal);};
 image.onerror=()=>{
  if(!active())return;
  clearMobilePendingCopy();
  image.dataset.state='error';image.dataset.source='unavailable';image.style.visibility='hidden';
  stagePoster.clear();finish(false);
  if(!currentReady)setStageNotice(stage.dataset.state==='fallback'?'previewAnd3dUnavailable':stage.dataset.state==='static'?'previewUnavailableStatic':'previewUnavailableLoading');
 };
 if(previous&&previous!==image){
  previous.onload=previous.onerror=null;previous.replaceWith(image);
  const previousId=previous.dataset.modelId;
  if(!isPhone&&previousId&&previousId!==asset.id&&previous.dataset.state==='ready'&&previous.dataset.source==='canonical'&&previous.naturalWidth){
   cacheDetailPoster(previousId,{image:previous,ready:true});
  }else previous.removeAttribute('src');
 }else if(!previous)stage.prepend(image);
 if(!asset.galleryPosters?.detail)queueMicrotask(image.onerror);else if(sameDecoded||warmed?.ready)reveal();else{image.src=poster(asset);if(image.complete&&image.naturalWidth>0)image.onload();}
 return {image,ready,bridge};
}
function syncMetricCard(asset){
 const dim=primaryDimension(asset,state.lang);
 $('#triangles').textContent=Number.isFinite(asset.triangles)?asset.triangles.toLocaleString(state.lang==='zh'?'zh-CN':'en-US'):'—';
 $('#dimensions').textContent=dim.value;
 const dimLabel=$('#dimensions-label');
 dimLabel.dataset.en=dim.labelEn;dimLabel.dataset.zh=dim.labelZh;dimLabel.textContent=dim.label;
 const glbText=formatBytes(asset.glb_bytes||asset.file_sizes?.glb||0,state.lang)||'—';
 const blendText=formatBytes(asset.blend_bytes||asset.file_sizes?.blend||0,state.lang);
 $('#file-size').textContent=glbText;
 $('#download-glb-size').textContent=glbText!=='—'?glbText:'';
 $('#download-blend-size').textContent=blendText;
}
function setDownloadsDisabled(disabled){
 for(const link of [$('#download'),$('#blend')]){
  if(disabled){link.removeAttribute('href');link.setAttribute('aria-disabled','true');link.style.opacity='.45';link.style.pointerEvents='none';}
  else{link.removeAttribute('aria-disabled');link.style.removeProperty('opacity');link.style.removeProperty('pointer-events');}
 }
 const zip=$('#download-zip');
 if(zip){zip.disabled=disabled;}
}
async function choose(id,{push=true,openMobile=true,activateMobile=false,center=false,syncHistory=true,phoneSource=null,keepMissingBanner=false}={}){
 const asset=sample.find(a=>a.id===id);if(!asset)return;
 cancelGalleryZip();integrityBlocked=false;
 if(!keepMissingBanner&&!$('#missing-banner').hidden)$('#missing-banner').hidden=true;
 showModelWorkspace();
 mobileIntent.clear();
 const row=$('#option-'+id),isPhone=mobile(),wasOpen=document.body.classList.contains('mobile-detail');
 const entering=phoneSource||(isPhone&&openMobile&&push&&!wasOpen?phoneContinuity.fromWheel(id,row):null);
 const {opening,canonicalFirst}=canonicalEntrancePlan({asset,isPhone,openMobile,activateMobile,opening:entering,reviewOnly:catalog.manifest?.review_only===true});
 const desktopCanonical=!isPhone&&catalog.manifest?.review_only===false&&hasCanonicalDetail(asset);
 const source=canonicalFirst||desktopCanonical?null:(opening?.art||(!isPhone?wheelArtwork(row):wasOpen?stagePoster.frame(id):null));
 if(opening||wasOpen)phoneContinuity.stop();
 cancelPosterWarmup();ui.resetCopy();if(push&&syncHistory)saveCurrentHistory();if(push)state.view='detail';const version=++selectionVersion;clearTimeout(selectionLoadingTimer);selectionLoadingTimer=0;closeInfo();hover.pause();settler.stop();state.selected=id;state.keyboard=id;currentReady=false;compareLoadKind=null;compareError=false;mobile3DActive=Boolean(isPhone&&activateMobile);stage.dataset.modelId=id;stage.dataset.state='loading';title.textContent=short(asset);$('#subtitle').textContent=assetSummaryLine(asset);syncMetricCard(asset);
 $('#download').href=urlAsset(asset.glb);$('#blend').href=urlAsset(asset.blend);setDownloadsDisabled(false);
 const zipBtn=$('#download-zip');zipBtn.hidden=!(asset.downloads?.bundle||(asset.glb&&asset.blend));
 detailHeadingLayout.apply(asset);
 const canonicalPending=canonicalFirst||desktopCanonical;
 setStageNotice(canonicalPending?'preparing':null);
 const selectedPoster=selectPoster(asset,version,source,canonicalPending?{desktopCanonical,beforeCanonicalVisible:()=>{
  if(version===selectionVersion&&state.selected===id&&stageNoticeKind==='preparing')setStageNotice(null);
 }}:undefined);
 $('#retry').hidden=true;infoContent(asset);$('#comparison-label').hidden=true;$('#compare').setAttribute('aria-pressed','false');$('#compare').removeAttribute('aria-busy');$('#wireframe').setAttribute('aria-pressed',String(Boolean(renderer?.wire)));renderSummary();renderWheel();settler.stop();
 state.mobileOpen=state.view==='detail'&&openMobile;syncMobileView();updateSelectedPosterFrame();
 if(center)settler.centerOn(id,{immediate:mobile()});
 if(syncHistory){if(push)pushHistory();else saveCurrentHistory();}
 $('#detail').style.touchAction=isPhone&&!activateMobile?'pan-y':'none';
 syncMobileChrome();detailHeadingLayout.refresh();
 if(opening){
  wheelContinuity.stop();
  phoneContinuity.travel(opening,{opening:true,poster:selectedPoster.bridge,staticTitle:canonicalFirst});
  title.focus({preventScroll:true});
 }
 if(isPhone&&!activateMobile){
  renderer?.suspend();stage.dataset.state='static';syncMobileChrome();
  mobileIntent.bind({id,sha:asset.sha256?.glb||'',src:new URL(poster(asset),location.href).href,version,image:selectedPoster.image},selectedPoster.ready);
  return;
 }
 const loadingTimer=selectionLoadingTimer=desktopCanonical?0:setTimeout(()=>{if(version===selectionVersion&&!currentReady)setStageNotice('loading3d');},450);
 if(!renderer){clearTimeout(loadingTimer);showError(version,id);return;}
 try{
  const ready=await renderer.select(asset,{
   presentationReady:selectedPoster.ready,
   beforeFirstFrame:()=>{if(selectedPoster.image.dataset.state==='error')stagePoster.clear();},
   afterFirstRender:()=>{if(version===selectionVersion&&$('#detail-poster')===selectedPoster.image){selectedPoster.image.style.transition='none';selectedPoster.image.style.opacity='0';}},
  });
  if(version!==selectionVersion||!ready)return;currentReady=true;hover.refresh();$('#detail').dataset.state='ready';$('#detail-poster').classList.add('ready');setStageNotice(null);syncMobileChrome();
 }catch(error){showError(version,id,error);}finally{clearTimeout(loadingTimer);if(selectionLoadingTimer===loadingTimer)selectionLoadingTimer=0;}
}
function showError(version=selectionVersion,id=state.selected,error){
 if(version!==selectionVersion||id!==state.selected)return;
 mobileIntent.cancel();
 clearTimeout(selectionLoadingTimer);selectionLoadingTimer=0;cancelSelectedPoster?.();currentReady=false;hover.pause();
 const image=$('#detail-poster'),integrityFailure=['MODEL_VERSION_MISMATCH','MODEL_IDENTITY_MISSING','MODEL_INTEGRITY_UNAVAILABLE'].includes(error?.code);
 $('#detail').dataset.state=integrityFailure?'version-error':'fallback';image.classList.remove('ready');image.style.removeProperty('opacity');image.style.removeProperty('transition');
 if(integrityFailure){
  integrityBlocked=true;cancelGalleryZip();
  image.dataset.state='invalid-version';image.dataset.source='invalid-version';image.onload=image.onerror=null;image.style.visibility='hidden';image.removeAttribute('src');stagePoster.clear();
  setDownloadsDisabled(true);
  setStageNotice('integrityFailed');
 }else setStageNotice(image.dataset.state==='error'?'previewAnd3dUnavailable':'staticFallback');
 $('#retry').hidden=false;
 syncMobileChrome();
}
function syncMobileView(){
 const open=mobile()&&state.mobileOpen;
 document.body.classList.toggle('mobile-detail',open);$('#mobile-back').hidden=!open;
 if(open){thumbnails.clear();clearTimeout(warmPosterTimer);}
 if(!open){measure();setWheelPosition(collectionScroll);renderWheel();settler.stop();}
 syncMobileChrome();
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
function capturePhoneDetail(id){
 return phoneContinuity.fromDetail(id,()=>{
  const temporary=stagePoster.frame(id);
  if(temporary)return temporary;
  const image=$('#detail-poster');
  if(currentReady&&renderer?.detail.model){
   try{return detailArtwork(image,renderer.captureDetail({transparent:true}),stage);}catch{}
  }
  return detailArtwork(image,null,stage);
 });
}
function finishPhoneReturn(frame){
 const row=$('#option-'+frame.id),box=row?.getBoundingClientRect(),viewport=wheel.getBoundingClientRect();
 const opener=box&&box.bottom>viewport.top&&box.top<viewport.bottom?row:null;
 if(opener){state.keyboard=frame.id;renderWheel();}
 phoneContinuity.travel(frame,{opening:false,row:opener});
 (state.results.length?wheel:$('#empty-filters')).focus({preventScroll:true});
}
function returnToCollection(){
 if(collectionReturnPending)return;
 mobileIntent.clear();
 stopHover();settler.stop();
 if(state.detailDepth>0){collectionReturnPending=true;history.go(-state.detailDepth);return;}
 const frame=mobile()?capturePhoneDetail(state.selected):null;
 saveCurrentHistory();state.view='collection';state.detailDepth=0;state.mobileOpen=false;mobile3DActive=false;
 syncMobileView();
 ++selectionVersion;cancelSelectedPoster?.();clearTimeout(selectionLoadingTimer);renderer?.suspend();currentReady=false;$('#detail').dataset.state='static';$('#detail-poster').classList.remove('ready');
 phoneContinuity.stop();stagePoster.clear();if(frame)finishPhoneReturn(frame);else wheel.focus({preventScroll:true});pushHistory();
}
window.addEventListener('popstate',async event=>{
 mobileIntent.clear();
 restoringHistory=true;collectionReturnPending=false;
 let selection;
 try{
  const saved=event.state?.gallery?event.state:null,url=new URL(location.href),route=parseRoute(url.pathname,siteRoot.pathname);
  if(route.type!=='models'){location.reload();return;}
  closeFilters(false);closeInfo();stopHover();settler.stop();$('#missing-banner').hidden=true;
  const query=readGalleryQuery(url.searchParams);if(query.sort==='triangles')query.sort='triangles-asc';
  const id=url.searchParams.get('model');
  Object.assign(state,query,{lang:route.lang==='zh-CN'?'zh':'en',page:route.page||0});
  const computed=compute();
  const selected=sample.find(a=>a.id===id)?.id||(saved?.selected&&computed.some(a=>a.id===saved.selected)?saved.selected:pickDefaultSelection(computed));
  const wasOpen=mobile()&&document.body.classList.contains('mobile-detail'),willOpen=mobile()&&!!id&&id===selected;
  const entering=!wasOpen&&willOpen?phoneContinuity.fromWheel(selected,$('#option-'+selected)):null;
  const leaving=wasOpen&&!willOpen?capturePhoneDetail(state.selected):null;
  wheelContinuity.stop();
  if(leaving)phoneContinuity.stop();
  Object.assign(state,{view:id&&sample.some(a=>a.id===id)?'detail':'collection',selected,detailDepth:saved?.detailDepth||0,results:computed});
  state.mobileOpen=state.view==='detail';translate();$('#search').value=state.query;updateSearchClear();state.keyboard=sample.some(a=>a.id===saved?.keyboard)?saved.keyboard:selected;
  collectionScroll=Number.isFinite(saved?.scroll)?Math.max(0,saved.scroll):Math.max(0,state.results.findIndex(a=>a.id===selected))*SLOT;
  syncMobileView();
  renderSummary();wheelTitle.reset();renderWheel();
  if(selected)selection=choose(selected,{push:false,syncHistory:false,openMobile:state.mobileOpen,phoneSource:entering});
  else showEmptyWorkspace();
  state.keyboard=sample.some(asset=>asset.id===saved?.keyboard)?saved.keyboard:selected;
  syncMobileView();renderWheel();settler.stop();
  if(leaving)finishPhoneReturn(leaving);
  if(focusSearchAfterReturn&&!state.mobileOpen){focusSearchAfterReturn=false;$('#search').focus();$('#search').select();}
 }finally{restoringHistory=false;}
 saveCurrentHistory();await selection;
});
function visibleFilterGroups(){
 const groups=[];
 // 1. Category (sorted by catalog count descending).
 const catIds=[...new Set(sample.map(a=>a.category).filter(Boolean))];
 if(catIds.length>1){
  const totals=new Map(catIds.map(id=>[id,sample.filter(a=>a.category===id).length]));
  catIds.sort((a,b)=>(totals.get(b)||0)-(totals.get(a)||0));
  groups.push({group:'category',ids:catIds});
 }
 // 2. Triangles band.
 groups.push({group:'triangleBand',ids:['under5k','5to10k','over10k']});
 // 3. Active URL triangleMax (if present in URL so badge always matches panel).
 if(state.facets.triangleMax.length)groups.push({group:'triangleMax',ids:[...state.facets.triangleMax]});
 // 4. User-facing curated packs (+ any active URL pack so nothing is hidden behind a badge).
 const allPacks=[...new Set(sample.flatMap(a=>a.packs||[]))];
 const shownPacks=allPacks.filter(id=>isUserFacingPack(id)||state.facets.packs.includes(id));
 if(shownPacks.length)groups.push({group:'packs',ids:shownPacks});
 // 5. Worlds (only shown once multiple worlds exist, or if URL explicitly filtered a non-universal world).
 if(distinctWorlds.length>1||state.facets.worlds.some(w=>!distinctWorlds.includes(w))){
  groups.push({group:'worlds',ids:[...new Set([...distinctWorlds,...state.facets.worlds])]});
 }
 return groups;
}
function openFilters(event){
 clearTimeout(searchTimer);
 if(!composition&&state.query!==$('#search').value){state.query=$('#search').value;applyResults(false);}
 filterHistoryPushed=false;
 stopHover();settler.stop();renderFilters();
 const backdrop=$('#filter-backdrop');if(backdrop)backdrop.hidden=false;
 ui.filter.show({animate:ui.pointer(event)});
 const firstControl=$('#filter-form input, #filter-form button')||$('#filter-close');
 firstControl.focus({preventScroll:true});
}
function closeFilters(focus=true,{animate=false}={}){
 filterHistoryPushed=false;
 const backdrop=$('#filter-backdrop');if(backdrop)backdrop.hidden=true;
 ui.filter.hide({animate});
 if(focus)$('#filters').focus({preventScroll:true});
}
function renderFilters(){
 const form=$('#filter-form');
 const groups=visibleFilterGroups();
 const sig=groups.map(g=>`${g.group}:${g.ids.join(',')}`).join('|')+'|'+state.lang;
 const countsByGroup=new Map();
 for(const {group,ids} of groups){
  const baseItems=filterItems(sample,state.query,{...state.facets,[group]:[]});
  countsByGroup.set(group,new Map(ids.map(id=>[id,filterItems(baseItems,'',{[group]:[id]}).length])));
 }
 if(form.dataset.structureSig===sig&&form.children.length){
  for(const field of form.children){
   const group=field.dataset?.group;
   if(!group||!countsByGroup.has(group))continue;
   const counts=countsByGroup.get(group);
   for(const label of field.querySelectorAll('label')){
    const input=label.querySelector('input');
    const badge=label.querySelector('.filter-item-count');
    if(!input)continue;
    const id=input.value,count=counts.get(id)||0;
    input.checked=state.facets[group].includes(id);
    label.classList.toggle('is-zero',count===0&&!input.checked);
    if(badge)badge.textContent=String(count);
   }
  }
 }else{
  const prevScroll=form.scrollTop;
  const activeEl=form.contains(document.activeElement)?document.activeElement:null;
  const focusKey=activeEl?.dataset?.group&&activeEl.value?{group:activeEl.dataset.group,value:activeEl.value}:null;
  form.replaceChildren();
  for(const {group,ids} of groups){
   const field=document.createElement('fieldset'),legend=document.createElement('legend');
   field.dataset.group=group;
   legend.textContent=facetLabels()[group];field.append(legend);
   const values=document.createElement('div');values.className='filter-values';
   const counts=countsByGroup.get(group);
   for(const id of ids){
    const count=counts.get(id)||0;
    const label=document.createElement('label'),input=document.createElement('input');
    input.type='checkbox';input.checked=state.facets[group].includes(id);input.value=id;input.dataset.group=group;
    if(count===0&&!input.checked)label.classList.add('is-zero');
    input.onchange=event=>{
     state.facets[group]=input.checked?[...state.facets[group],id]:state.facets[group].filter(v=>v!==id);
     const shouldPush=!filterHistoryPushed;filterHistoryPushed=true;
     applyResults(shouldPush,{animate:ui.pointer(event),autoSelectIfExcluded:true});
    };
    const text=document.createElement('span');text.textContent=valueLabel(group,id);
    const badge=document.createElement('em');badge.className='filter-item-count';badge.textContent=String(count);
    label.append(input,text,badge);values.append(label);
   }
   field.append(values);form.append(field);
  }
  form.dataset.structureSig=sig;
  form.scrollTop=prevScroll;
  if(focusKey){
   for(const input of form.querySelectorAll('input')){
    if(input.dataset.group===focusKey.group&&input.value===focusKey.value){input.focus({preventScroll:true});break;}
   }
  }
 }
 const activeCount=activeFacetEntries().length;
 $('#filter-clear').disabled=activeCount===0;
 const n=state.results.length;
 $('#filter-apply').textContent=t(`Done · ${n.toLocaleString('en-US')} models`,`完成 · ${n.toLocaleString('zh-CN')} 个模型`);
 ui.updateFilterOverflow();
}
$('#filters').onclick=event=>ui.filter.open?closeFilters(true,{animate:ui.pointer(event)}):openFilters(event);
$('#filter-close').onclick=event=>closeFilters(true,{animate:ui.pointer(event)});
$('#filter-clear').onclick=event=>{
 // Only reset filters inside this panel; never silently wipe the user's search query.
 state.facets=emptyFacets();
 const shouldPush=!filterHistoryPushed;filterHistoryPushed=true;
 applyResults(shouldPush,{animate:ui.pointer(event),autoSelectIfExcluded:true});
 ($('#filter-form input')||$('#filter-apply')).focus({preventScroll:true});
};
$('#filter-apply').onclick=event=>closeFilters(true,{animate:ui.pointer(event)});
$('#filter-form').onsubmit=e=>e.preventDefault();
$('#filter-backdrop').addEventListener('pointerdown',event=>event.stopPropagation());
$('#filter-backdrop').onclick=event=>{event.preventDefault();event.stopPropagation();closeFilters(false,{animate:true});};
$('#sort-select').onchange=event=>{
 state.sort=event.target.value;
 applyResults(true,{animate:false});
};
$('#search').addEventListener('compositionstart',()=>{composition=true;clearTimeout(searchTimer);});
$('#search').addEventListener('compositionend',()=>{composition=false;queueSearch();});
function queueSearch(){
 updateSearchClear();
 if(composition)return;
 clearTimeout(searchTimer);
 searchTimer=setTimeout(()=>{state.query=$('#search').value;applyResults(false);},200);
}
$('#search').addEventListener('input',queueSearch);
$('#search').addEventListener('keydown',e=>{
 if(e.key==='Enter'&&!e.isComposing&&!composition){
  e.preventDefault();clearTimeout(searchTimer);state.query=e.target.value;updateSearchClear();
  applyResults(true,{autoSelectFirst:true});
 }else if(e.key==='Escape'){
  e.preventDefault();e.stopPropagation();
  if($('#search').value){clearTimeout(searchTimer);$('#search').value='';state.query='';updateSearchClear();applyResults(false);}
  else{$('#search').blur();wheel.focus({preventScroll:true});}
 }
});
$('#search-clear').onclick=()=>{
 clearTimeout(searchTimer);$('#search').value='';state.query='';updateSearchClear();
 applyResults(false);$('#search').focus({preventScroll:true});
};
function openInfo({animate=false}={}){
 $('#info-close').ariaLabel=t('Close model details','关闭模型说明');
 const backdrop=$('#info-backdrop');if(backdrop)backdrop.hidden=false;
 ui.info.show({animate});ui.updateOverflow();
}
function closeInfo({returnFocus=false,animate=false}={}){
 const backdrop=$('#info-backdrop');if(backdrop)backdrop.hidden=true;
 ui.info.hide({animate});ui.updateOverflow();
 if(returnFocus)$('#info').focus({preventScroll:true});
}
$('#info-close').onclick=event=>closeInfo({returnFocus:true,animate:ui.pointer(event)});
$('#info-backdrop').addEventListener('pointerdown',event=>event.stopPropagation());
$('#info-backdrop').onclick=event=>{event.preventDefault();event.stopPropagation();closeInfo({animate:true});};
$('#info').onclick=event=>{
 if(ui.info.open)closeInfo({animate:ui.pointer(event)});
 else openInfo({animate:ui.pointer(event)});
};
$('#share-link').onclick=event=>{
 const asset=sample.find(a=>a.id===state.selected);
 if(asset)void ui.copyShareLink(asset,event);
};
$('#missing-close').onclick=()=>{$('#missing-banner').hidden=true;};
document.addEventListener('pointerdown',event=>{
 if(event.target===$('#filter-backdrop')||event.target===$('#info-backdrop'))return;
 if(ui.filter.open&&!$('#filter-panel').contains(event.target)&&!$('#filters').contains(event.target))closeFilters(false,{animate:true});
 if(ui.info.open&&!$('.info-region').contains(event.target))closeInfo({animate:true});
},{capture:true});
document.addEventListener('keydown',event=>{
 if(event.key==='Tab'&&ui.filter.open){
  const panel=$('#filter-panel');
  const focusable=[...panel.querySelectorAll('button,input,select,a[href],[tabindex]')].filter(el=>!el.disabled&&el.tabIndex>=0&&el.getClientRects().length&&!el.closest('[hidden],[inert]'));
  if(focusable.length){
   const first=focusable[0],last=focusable.at(-1),active=document.activeElement;
   if(event.shiftKey&&(active===first||!panel.contains(active))){event.preventDefault();last.focus();}
   else if(!event.shiftKey&&(active===last||!panel.contains(active))){event.preventDefault();first.focus();}
  }
  return;
 }
 if(event.key==='Escape'){
  if(!$('#info-panel').hidden){event.preventDefault();event.stopPropagation();closeInfo({returnFocus:true});return;}
  if(!$('#filter-panel').hidden){event.preventDefault();closeFilters(true);return;}
  if(renderer?.comparison){renderer.compare(false);$('#compare').setAttribute('aria-pressed','false');$('#compare').removeAttribute('aria-busy');$('#comparison-label').hidden=true;compareLoadKind=null;compareError=false;syncStageHint();syncStageTools();return;}
 }
 if(event.ctrlKey||event.metaKey||event.altKey)return;
 const inInput=['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName);
 if(event.key==='/'&&!inInput&&!ui.filter.open){
  event.preventDefault();
  if(ui.info.open)closeInfo({animate:false});
  if(mobile()&&state.mobileOpen){
   if(state.detailDepth>0){focusSearchAfterReturn=true;returnToCollection();return;}
   returnToCollection();
  }
  $('#search').focus();$('#search').select();return;
 }
 if((event.key==='['||event.key===']')&&!inInput&&!ui.filter.open&&!ui.info.open&&state.results.length>1){
  const idx=state.results.findIndex(a=>a.id===state.selected);
  const next=idx>=0?idx+(event.key===']'?1:-1):0;
  if(state.results[next]){event.preventDefault();void choose(state.results[next].id,{push:true,center:true});}
 }
});
$('#language').onclick=()=>{
 phoneContinuity.stop();wheelContinuity.stop();ui.resetCopy();
 state.lang=state.lang==='en'?'zh':'en';
 setStoredLang(state.lang);
 if(state.sort==='name'||state.sort==='name-desc'){
  const anchor=settler.nearest(wheel.scrollTop),offset=anchor?wheel.scrollTop-anchor.offset:0;
  stopHover();settler.stop();state.results=compute();
  const index=state.results.findIndex(a=>a.id===anchor?.id);
  if(index>=0)setWheelPosition(index*SLOT+offset);
  wheelTitle.reset();
 }
 translate();renderSummary();renderWheel();saveCurrentHistory();
 const a=sample.find(a=>a.id===state.selected);
 if(a){$('#title').textContent=short(a);$('#subtitle').textContent=assetSummaryLine(a);syncMetricCard(a);infoContent(a);detailHeadingLayout.refresh();}
 if(ui.filter.open)renderFilters();
};
$('#wireframe').onclick=()=>{
 if(!currentReady)return;
 const next=!renderer.wire;
 renderer.wireframe(next);setStoredWireframe(next);
 $('#wireframe').setAttribute('aria-pressed',String(renderer.wire));
};
$('#compare').onclick=()=>{
 if(!currentReady)return;
 compareError=false;
 const result=renderer.compare();
 if(!result){
  compareLoadKind=null;
  $('#compare').setAttribute('aria-pressed','false');$('#compare').removeAttribute('aria-busy');
  $('#comparison-label').hidden=true;syncStageHint();syncStageTools();return;
 }
 $('#compare').setAttribute('aria-pressed','true');
 $('#comparison-label').hidden=false;
 if(result.ready){compareLoadKind=null;$('#compare').removeAttribute('aria-busy');updateComparisonLabel(result.kind);}
 else{compareLoadKind=result.kind;$('#compare').setAttribute('aria-busy','true');updateComparisonLabel(result.kind);}
 syncStageHint();syncStageTools();
};
$('#zoom-in').onclick=()=>{if(!currentReady)return;stopHover();renderer.zoom(.85);};
$('#zoom-out').onclick=()=>{if(!currentReady)return;stopHover();renderer.zoom(1.18);};
$('#reset').onclick=()=>{
 if(!currentReady)return;
 stopHover();compareLoadKind=null;compareError=false;
 renderer.reset();
 $('#compare').setAttribute('aria-pressed','false');$('#compare').removeAttribute('aria-busy');
 $('#comparison-label').hidden=true;syncStageHint();syncStageTools();
};
$('#retry').onclick=()=>choose(state.selected,{push:false,preserve:false,activateMobile:mobile()});
$('#mobile-interact').addEventListener('pointerdown',event=>event.stopPropagation());
mobileInteract.onclick=()=>{
 if(!mobile())return;
 if(stage.dataset.state==='static'){mobileIntent.request();return;}
 return choose(state.selected,{push:false,preserve:false,activateMobile:false});
};
stageEnter3D.addEventListener('pointerdown',event=>event.stopPropagation());
stageEnter3D.onclick=()=>{
 if(!mobile())return;
 if(stage.dataset.state==='static'){mobileIntent.request();return;}
 void choose(state.selected,{push:false,preserve:false,activateMobile:true});
};
$('#mobile-prev').onclick=()=>{
 const idx=state.results.findIndex(a=>a.id===state.selected);
 if(idx>0)void choose(state.results[idx-1].id,{push:true,openMobile:true,activateMobile:false,center:true});
};
$('#mobile-next').onclick=()=>{
 const idx=state.results.findIndex(a=>a.id===state.selected);
 if(idx>=0&&idx<state.results.length-1)void choose(state.results[idx+1].id,{push:true,openMobile:true,activateMobile:false,center:true});
};
$('#detail').addEventListener('keydown',event=>{
 if(event.ctrlKey||event.metaKey||event.altKey||!currentReady)return;
 const action={
  '+':()=>renderer.zoom(.85),'=':()=>renderer.zoom(.85),
  '-':()=>renderer.zoom(1.18),'_':()=>renderer.zoom(1.18),
  ArrowLeft:()=>renderer.rotate(-8,0),ArrowRight:()=>renderer.rotate(8,0),
  ArrowUp:()=>renderer.rotate(0,8),ArrowDown:()=>renderer.rotate(0,-8),
  Home:()=>$('#reset').click(),r:()=>$('#reset').click(),R:()=>$('#reset').click(),
 }[event.key];
 if(action){event.preventDefault();stopHover();action();}
});
$('#credits').onclick=event=>{const asset=sample.find(a=>a.id===state.selected);if(asset)void ui.copyAttribution(asset,event);};
for(const link of [$('#download'),$('#blend')]){
 link.addEventListener('click',()=>{
  const asset=sample.find(a=>a.id===state.selected);
  if(!asset||link.getAttribute('aria-disabled')==='true')return;
  toast(t('Download started · Remember CC BY 4.0 credit','已开始下载 · 别忘了附带 CC BY 4.0 署名'),{
   actionLabel:t('Copy credit','复制署名'),
   onAction:ev=>ui.copyAttribution(asset,ev),
  });
 });
}
$('#download-zip').onclick=async()=>{
 const btn=$('#download-zip'),asset=sample.find(a=>a.id===state.selected);
 if(!asset||btn.disabled||integrityBlocked)return;
 if(asset.downloads?.bundle){window.location.assign(urlAsset(asset.downloads.bundle));return;}
 zipController?.abort();
 const controller=zipController=new AbortController();
 const gen=++zipVersion;
 btn.disabled=true;btn.setAttribute('aria-busy','true');
 const label=btn.querySelector('[data-en]');label.textContent=t('Preparing ZIP…','正在打包 ZIP…');
 try{
  const {filename}=await downloadModelZip(asset,{resolveURL:urlAsset,signal:controller.signal});
  if(gen!==zipVersion||state.selected!==asset.id||integrityBlocked||controller.signal.aborted)return;
  toast(t(`Downloading ${filename}`,`已开始下载 ${filename}`),{actionLabel:t('Copy credit','复制署名'),onAction:ev=>ui.copyAttribution(asset,ev)});
 }catch(error){
  if(error?.name==='AbortError'||gen!==zipVersion)return;
  toast(t('ZIP failed. Try again or download GLB / Blender separately.','ZIP 打包失败，请重试或单独下载 GLB / Blender 文件。'),{duration:4200});
 }finally{
  if(zipController===controller)zipController=null;
  if(gen===zipVersion){
   btn.disabled=integrityBlocked;btn.removeAttribute('aria-busy');
   label.textContent=label.dataset[state.lang];
  }
 }
};
$('#mobile-back').onclick=returnToCollection;
window.addEventListener('blur',stopHover);
window.addEventListener('resize',()=>{
 phoneContinuity.stop();wheelContinuity.stop();detailHeadingLayout.refresh();updateSelectedPosterFrame();stopHover();clearTimeout(resizeTimer);
 resizeTimer=setTimeout(()=>{const id=state.center,index=state.results.findIndex(a=>a.id===id);settler.stop();measure();if(index>=0)setWheelPosition(index*SLOT);renderWheel();settler.stop();syncMobileView();detailHeadingLayout.refresh();updateSelectedPosterFrame();renderer?.draw();},80);
});
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',()=>{phoneContinuity.stop();wheelContinuity.stop();stopHover();settler.stop();renderWheel();});
let detailScrollFrame=0;
window.addEventListener('scroll',()=>{
 if(detailScrollFrame||!document.body.classList.contains('mobile-detail'))return;
 detailScrollFrame=requestAnimationFrame(()=>{detailScrollFrame=0;if(document.body.classList.contains('mobile-detail'))renderer?.draw();});
},{passive:true});

translate();$('#search').value=state.query;updateSearchClear();state.results=compute();state.keyboard=state.selected;renderSummary();renderWheel();
setWheelPosition(Number.isFinite(savedState?.scroll)?Math.max(0,savedState.scroll):Math.max(0,state.results.findIndex(a=>a.id===state.selected))*SLOT);
wheelTitle.reset();renderWheel();settler.stop();
if(missingInitialModel){
 const banner=$('#missing-banner');banner.dataset.missingId=missingInitialModel;banner.hidden=false;syncMissingBanner();
 saveCurrentHistory();
}
try{
 renderer=new PreviewRenderer($('#detail'));
 renderer.wire=getStoredWireframe();
 renderer.onDirtyChange=()=>syncStageTools();
 renderer.onReferenceStateChange=(status,kind)=>{
  if(status==='loading'){compareLoadKind=kind;compareError=false;$('#compare').setAttribute('aria-busy','true');$('#comparison-label').hidden=false;updateComparisonLabel(kind);}
  else if(status==='ready'){compareLoadKind=null;compareError=false;$('#compare').removeAttribute('aria-busy');$('#comparison-label').hidden=false;updateComparisonLabel(kind);}
  else if(status==='idle'){compareLoadKind=null;compareError=false;$('#compare').removeAttribute('aria-busy');$('#compare').setAttribute('aria-pressed','false');$('#comparison-label').hidden=true;}
  syncStageHint();syncStageTools();
 };
 renderer.onReferenceError=error=>{
  compareLoadKind=null;compareError=true;
  $('#compare').setAttribute('aria-pressed','false');$('#compare').removeAttribute('aria-busy');
  $('#comparison-label').hidden=false;updateComparisonLabel('');syncStageHint();syncStageTools();
  console.warn(error);
 };
 renderer.onInteraction=stopHover;
 renderer.onError=(error,context)=>{if(!context||context.assetId===state.selected)showError(selectionVersion,state.selected,error);};
 renderer.onRestore=()=>choose(state.selected,{push:false,preserve:false,activateMobile:mobile()});
}catch(error){console.warn('Static fallback',error.message);}
window.__preview={state,models:sample,choose,settler,get renderer(){return renderer;},get detailPosterCacheStats(){const entries=[...detailPosterCache].map(([id,e])=>({id,ready:e.ready,width:e.image.naturalWidth,height:e.image.naturalHeight,src:e.image.currentSrc||e.image.src}));return {size:entries.length,limit:DETAIL_POSTER_CACHE_LIMIT,entries,estimatedDecodedRGBABytes:entries.filter(e=>e.ready).reduce((n,e)=>n+e.width*e.height*4,0)};},get thumbnailStats(){return thumbnails.stats;},renderWheel,returnToCollection,async generatePosters(){const output={};for(const asset of sample)output[asset.id]=await renderer.poster(asset);return output;},async generateWheelPosters(){const images={},specs={};for(const asset of sample){images[asset.id+'-wheel']=await renderer.poster(asset,{wheel:true});specs[asset.id]=renderer.lastPosterSpec;}return {images,specs};}};
if(state.selected)await choose(state.selected,{push:false,preserve:false,openMobile:hasInitialModel,keepMissingBanner:Boolean(missingInitialModel)});
else if(sample.length)showEmptyWorkspace();
else{$('#title').textContent=t('No published models yet','暂无已发布模型');$('.download-card').hidden=true;$('#detail').hidden=true;}
window.__gallery=window.__preview;
if(catalog.manifest.review_only){const note=document.createElement('span');note.className='gallery-review-notice';note.setAttribute('role','status');note.textContent=t('Review only · Not approved for publication','仅供审阅 · 尚未批准发布');document.querySelector('header').append(note);}
}
