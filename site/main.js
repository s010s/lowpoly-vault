import { ImageScrubPreview } from './image-scrub.js';
import { createCatalogToolbar } from './catalog-toolbar.js';
import { ModelAtlas } from './atlas.js';
import { CatalogStore } from './catalog.js';
import { initTheme } from './theme.js';
import { GalleryMotion } from './motion.js';
import { DialogMotion, DIALOG_TIMING } from './dialog-motion.js';
import { words } from './words.js';
import { routeHref, parseRoute, queryFromParams, filterAndSortCatalog } from './routes.js';
import './style.css';
import './atlas.css';

Object.assign(words.en, {initialRelease:'Initial collection · More refinement to come.',title:'All models',intro:'Original shapes. Ready for your next world.',collection:'The collection',sortPolyHigh:'Polygon count: high to low',themes:'World',pack:'Pack',refine:'Refine',anyWorld:'Every world',anyPack:'All packs',anyPolygons:'Any triangle count',trianglesUnder:'Up to',scaleReference:'Scale reference',scaleNote:'Grid spacing',scaleUnavailable:'Metric reference is unavailable for this model.',related:'From the same pack',previousModel:'Previous model',nextModel:'Next model',bundle:'Model + source + credits',none:'No models match these filters. Try a different term or clear the filters.',map:'Pack map',grid:'Grid',previewHint:'Hover to inspect',fileSizeUnknown:'Size unavailable'});
Object.assign(words.zh, {initialRelease:'首批模型 · 持续打磨中。',title:'全部模型',intro:'原创形状，为你的下一个世界而准备。',collection:'模型收藏',sortPolyHigh:'三角面数：从多到少',themes:'世界',pack:'组合包',refine:'筛选',anyWorld:'所有世界',anyPack:'全部组合包',anyPolygons:'不限三角面数',trianglesUnder:'不超过',scaleReference:'尺寸参照',scaleNote:'网格间距',scaleUnavailable:'此模型暂无可靠的米制尺寸参照。',related:'同一组合包中的模型',previousModel:'上一个模型',nextModel:'下一个模型',bundle:'模型、源文件与署名',none:'没有符合这些条件的模型。试试其他关键词，或清除筛选。',map:'组合地图',grid:'网格',previewHint:'悬停查看',fileSizeUnknown:'大小暂无数据'});

const $ = selector => document.querySelector(selector);
const siteRoot = new URL(import.meta.env.BASE_URL, location.origin).pathname;
const initialRoute = parseRoute(location.pathname, siteRoot);
let lang = initialRoute.lang === 'zh-CN' ? 'zh' : 'en'; // Explicit URL wins over storage.
const t = key => words[lang][key] || key;
const loc = value => typeof value === 'object' && value ? (value[lang] || value.en || '') : value || '';
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const href = (type, id, options = {}) => routeHref({type, id, lang, ...options}, siteRoot);
const plainClick = event => event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey;
const store = new CatalogStore({baseURL:new URL(siteRoot,location.origin).href});
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const fine = matchMedia('(hover: hover) and (pointer: fine)');
const motionUI = new GalleryMotion();
const dialogMotion = new DialogMotion($('#viewer-dialog'), reduced);
initTheme();
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

let index, items = [], category = 'all', world = 'all', pack = 'all', page = 0, pages = 0, maxTriangles = 0;
let selected, selectedSummary, origin, stage, stagePromise, hoverCard, hoverTimer;
let queryVersion = 0, detailVersion = 0, closing = false, modalAnimation, interruptedDialog, detailController, restoringFocus = false, hoverSuppressed = false, hoverPointer = null;
let browseMode = 'grid', atlas, atlasPackKey = '', atlasPackItems = [], currentView = 'home', directDetailId = initialRoute.type==='detail'?initialRoute.id:null;
let sourceContext = null, neighborItems = [], searchTimer, pendingRoute = false, queuedRoute = false;
const viewScroll = {home:0, catalog:0, about:0, detail:0};
const staticContent = $('#static-route-content');
const path = p => store.resolvePath(p);
const scrub = new ImageScrubPreview({resolvePath:path,language:()=>lang});
const queryOptions = () => ({query:$('#search').value, category, world, pack, sort:$('#sort').value, maxTriangles, page, view:browseMode === 'atlas' ? 'map' : 'grid'});
const listURL = () => href('models',undefined,{page,query:queryOptions()});
const setStatus = text => { $('#announcement').textContent = text; };

function paintIcons(root=document.body) {
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT), nodes=[];
  while(walker.nextNode()) if(/[↗↓←→]/.test(walker.currentNode.textContent)) nodes.push(walker.currentNode);
  for(const node of nodes){
    const fragment=document.createDocumentFragment();
    for(const part of node.textContent.split(/([↗↓←→])/)){
      if(!/[↗↓←→]/.test(part)){fragment.append(document.createTextNode(part));continue;}
      const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 16 16');svg.setAttribute('class','inline-icon');svg.setAttribute('aria-hidden','true');
      const line=document.createElementNS(svg.namespaceURI,'path');line.setAttribute('d',{'↗':'M3 13 13 3M3 3h10v10','↓':'M8 2v12m-5-5 5 5 5-5','←':'M14 8H2m5-5L2 8l5 5','→':'M2 8h12m-5-5 5 5-5 5'}[part]);svg.append(line);fragment.append(svg);
    }
    node.replaceWith(fragment);
  }
}
function formatBytes(bytes) {
  if(!Number.isFinite(bytes)) return t('fileSizeUnknown');
  return bytes < 1024 * 1024 ? `${(bytes/1024).toLocaleString(lang === 'zh'?'zh-CN':'en',{maximumFractionDigits:1})} KB` : `${(bytes/1024/1024).toLocaleString(lang === 'zh'?'zh-CN':'en',{maximumFractionDigits:2})} MB`;
}
function controlsReady(ready){
  for(const selector of ['.viewer-controls','.viewer-hint']){const element=$(selector);element.hidden=false;element.style.visibility=ready?'visible':'hidden';element.setAttribute('aria-hidden',String(!ready));}
  document.querySelectorAll('.viewer-controls button').forEach(button=>button.disabled=!ready);
  if(ready) $('#scale-reference').disabled = !stage?.scaleReferenceInfo?.available;
}
async function getStage(){return stagePromise ||= import('./viewer.js').then(({ModelStage}) => (stage=new ModelStage()));}
function stopHover(){hoverPointer=null;scrub.stop();clearTimeout(hoverTimer);if(hoverCard){hoverCard.querySelector('.card-status').textContent='';hoverCard=null;}if(!selected)stage?.hide();}
function bindImages(root=document){root.querySelectorAll('img').forEach(img=>img.onerror=()=>{img.style.visibility='hidden';img.alt=t('noPreview');});}

const atlasHost=document.createElement('section');atlasHost.className='model-atlas';$('#grid').before(atlasHost);
const modes=document.createElement('div');modes.className='catalog-modes';modes.innerHTML='<button data-mode="grid" aria-pressed="true">Grid</button><button data-mode="atlas" aria-pressed="false">Pack map</button>';$('.search-row').append(modes);
const catalogToolbar=createCatalogToolbar({root:$('.search-row'),search:$('#search'),modes,language:()=>lang});
const refine=document.createElement('details');refine.className='catalog-refine';refine.innerHTML='<summary></summary><div class="refine-fields"><label><span data-label="world"></span><select id="world-filter"></select></label><label><span data-label="pack"></span><select id="pack-filter"></select></label><label><span data-label="triangles"></span><select id="poly-filter"></select></label></div>';$('.search-row').append(refine);
const canMap=()=>pack!=='all' && (index?.packs?.find(p=>p.id===pack)?.count||Infinity)<=30;
function paintModes(){
  if(!canMap())browseMode='grid';
  catalogToolbar.paint();modes.hidden=!canMap();
  modes.querySelector('[data-mode=atlas] span').textContent=t('map');modes.querySelector('[data-mode=grid] span').textContent=t('grid');
  modes.querySelectorAll('button').forEach(b=>b.ariaPressed=String(b.dataset.mode===browseMode));
  $('#catalog-page').classList.toggle('catalog-atlas-active',browseMode==='atlas');$('#grid').hidden=browseMode==='atlas';atlasHost.hidden=browseMode!=='atlas';
  if(browseMode==='atlas')$('.pagination').hidden=true;
}
modes.onclick=event=>{const button=event.target.closest('[data-mode]');if(!button||browseMode===button.dataset.mode)return;browseMode=button.dataset.mode;atlas?.setActive(browseMode==='atlas');updateListing();};
function facetName(facet){return loc(facet?.name)||t(facet?.id||'');}
function paintFilters(){
  if(!index)return;
  $('#library-count').textContent=index.total;
  $('#all-assets').classList.toggle('active',category==='all'&&world==='all'&&pack==='all'&&!maxTriangles&&!$('#search').value);
  $('#all-assets').ariaPressed=String(category==='all'&&world==='all'&&pack==='all'&&!maxTriangles&&!$('#search').value);
  $('#filters').innerHTML=[{id:'all',count:index.total},...index.categories].map(c=>`<button data-category="${esc(c.id)}" class="${category===c.id?'active':''}" aria-pressed="${category===c.id}">${esc(t(c.id))}<span>${c.count}</span></button>`).join('');
  refine.querySelector('summary').textContent=t('refine');refine.querySelector('[data-label=world]').textContent=t('themes');refine.querySelector('[data-label=pack]').textContent=t('pack');refine.querySelector('[data-label=triangles]').textContent=t('triangles');
  $('#world-filter').innerHTML=`<option value="all">${t('anyWorld')}</option>`+(index.worlds||index.collections).map(f=>`<option value="${esc(f.id)}">${esc(facetName(f))} (${f.count})</option>`).join('');
  $('#pack-filter').innerHTML=`<option value="all">${t('anyPack')}</option>`+(index.packs||[]).map(f=>`<option value="${esc(f.id)}">${esc(facetName(f))} (${f.count})</option>`).join('');
  $('#poly-filter').innerHTML=`<option value="0">${t('anyPolygons')}</option>`+[500,1000,5000].map(n=>`<option value="${n}">${t('trianglesUnder')} ${n.toLocaleString()}</option>`).join('');
  $('#world-filter').value=world;$('#pack-filter').value=pack;$('#poly-filter').value=String(maxTriangles);
  $('#search-suggestions').innerHTML=index.initial.slice(0,12).map(a=>`<option value="${esc(loc(a.name))}"></option>`).join('');
  const active=[category!=='all'?['category',t(category)]:null,world!=='all'?['world',facetName(index.worlds?.find(f=>f.id===world)||{id:world})]:null,pack!=='all'?['pack',facetName(index.packs?.find(f=>f.id===pack)||{id:pack})]:null,maxTriangles?['triangles',`${t('trianglesUnder')} ${maxTriangles.toLocaleString()} △`]:null].filter(Boolean);
  $('#active-filters').innerHTML=active.map(([key,label])=>`<button data-clear="${key}" aria-label="${esc(`${t('clear')}: ${label}`)}">${esc(label)} <span aria-hidden="true">×</span></button>`).join('');
}
function cardHTML(asset,i){return `<a href="${esc(href('detail',asset.id))}" class="asset-card${asset.turntable?' has-turntable':''}${asset.card_preview?' has-card-preview':''}" style="--i:${Math.min(i,7)}" data-id="${esc(asset.id)}" aria-label="${esc(loc(asset.name))}${asset.turntable?esc(lang==='zh'?'，左右键查看图片角度，回车打开 3D':', arrow keys rotate preview; Enter opens 3D'):''}"><div class="asset-image"><img src="${esc(path(asset.preview))}" alt="${esc(loc(asset.name))}" loading="lazy" decoding="async" width="640" height="640"><span class="card-action" aria-hidden="true">↗</span>${asset.turntable?`<span class="scrub-badge" aria-hidden="true">360°</span>`:''}<span class="card-status" role="status"></span></div><div class="card-label"><h3>${esc(loc(asset.name))}</h3><span>${Number.isFinite(asset.triangles)?asset.triangles.toLocaleString()+' △':''}</span></div><p class="card-category">${esc(t(asset.category))}</p></a>`;}
async function renderGrid(){
  if(!index)return;paintModes();paintFilters();const version=++queryVersion;stopHover();
  if(browseMode==='atlas'){
    const key=JSON.stringify([pack,world]);
    if(key!==atlasPackKey){const result=await store.search({pack,world,pageSize:100});if(version!==queryVersion)return;atlasPackItems=result.items;atlasPackKey=key;}
    const scope=filterAndSortCatalog(atlasPackItems,{query:$('#search').value,category,maxTriangles,sort:$('#sort').value});
    const counts=new Map();scope.forEach(a=>counts.set(a.category,(counts.get(a.category)||0)+1));
    const scopedIndex={...index,total:scope.length,categories:[...counts].map(([id,count])=>({id,count}))};
    const memoryStore={cancelSearch(){},async search(options={}){const found=filterAndSortCatalog(scope,options),size=options.pageSize||100,p=options.page||0;return {items:found.slice(p*size,(p+1)*size),total:found.length,page:p,pages:Math.ceil(found.length/size)};}};
    if(!atlas)atlas=new ModelAtlas({host:atlasHost,store:memoryStore,t,lang:()=>lang,cardHTML,onItems:visible=>{items=visible;},onOpen:id=>openAsset(id,{push:true}),onHover:requestHover,onStop:stopHover,onPointer:pointerMove});
    atlas.store=memoryStore;atlas.filterKey='';atlas.setActive(currentView==='catalog');
    // Avoid a distant overview of dozens of one-model regions in a small curated pack.
    await atlas.update({index:scopedIndex,flat:scopedIndex.categories.length>6});if(version!==queryVersion)return;
    $('#count').textContent=`${scope.length.toLocaleString()} ${t('count')}`;$('#grid').ariaBusy='false';$('#grid').inert=false;hideStaticFor('models');return;
  }
  atlas?.setActive(false);const previous=motionUI.capture($('#grid'));$('#grid').ariaBusy='true';$('#grid').inert=true;
  try{
    const result=await store.search({...queryOptions(),pageSize:24});if(version!==queryVersion)return;
    await motionUI.exit($('#grid'),result.items.map(a=>a.id));if(version!==queryVersion)return;
    items=result.items;page=result.page;pages=result.pages;
    $('#count').textContent=`${result.total.toLocaleString()} ${t('count')}`;
    $('#grid').innerHTML=items.length?items.map(cardHTML).join(''):`<div class="empty">${t('none')}<button id="clear-empty">${t('clear')}</button></div>`;
    $('#grid').ariaBusy='false';$('#grid').inert=false;
    $('#prev-page').disabled=page===0;$('#next-page').disabled=page>=pages-1;$('#page-number').textContent=pages?`${page+1} / ${pages}`:'';$('.pagination').hidden=pages<=1;
    bindImages($('#grid'));paintIcons($('#grid'));motionUI.commit($('#grid'),previous);hideStaticFor('models');
  }catch(error){if(error.name!=='AbortError'&&version===queryVersion)showError();}
}
function showError(){atlas?.setActive(false);atlasHost.hidden=true;$('#grid').hidden=false;$('#grid').ariaBusy='false';$('#grid').inert=false;$('#grid').innerHTML=`<div class="empty">${t('error')}<button id="retry">${t('retry')}</button></div>`;}
function readQuery(route=parseRoute(location.pathname,siteRoot)){
  const q=queryFromParams(location.search);category=q.category;world=q.world==='all'?q.collection:q.world;pack=q.pack;page=route.type==='models'?route.page:q.page;maxTriangles=q.maxTriangles||0;browseMode=q.view==='map'?'atlas':'grid';$('#search').value=q.query;$('#sort').value=q.sort;
}
function updateListing({push=false}={}){paintFilters();paintModes();if(currentView==='catalog')history[push?'pushState':'replaceState']({view:'catalog'},'',listURL());return renderGrid();}
function resetFilters({render=true}={}){category=world=pack='all';page=0;maxTriangles=0;browseMode='grid';$('#search').value='';$('#sort').value='name';if(render)updateListing();}

function requestHover(card,clientX){
  if(selected||restoringFocus||hoverSuppressed||!fine.matches||!card||hoverCard===card)return;
  stopHover();const asset=items.find(a=>a.id===card.dataset.id);if(!asset?.turntable)return;
  hoverCard=card;hoverPointer=Number.isFinite(clientX)?{x:clientX,frame:asset.turntable.poster_index||0}:null;hoverTimer=setTimeout(()=>{if(hoverCard===card&&!selected)scrub.activate(card,asset);},120);
}
function pointerMove(event){
  if(event.pointerType==='touch')return;
  if(hoverSuppressed&&!selected){if(!event.movementX&&!event.movementY)return;hoverSuppressed=false;requestHover(event.target.closest('.asset-card'));}
  if(hoverCard&&!selected){const r=hoverCard.querySelector('.asset-image').getBoundingClientRect();if(!hoverPointer)hoverPointer={x:event.clientX,frame:scrub.current?.frame||0};if(scrub.current)scrub.request(hoverPointer.frame+(event.clientX-hoverPointer.x)/r.width*scrub.current.descriptor.frame_count);}
}
$('#grid').addEventListener('pointerover',event=>{const card=event.target.closest('.asset-card');if(card&&!card.contains(event.relatedTarget)&&event.pointerType!=='touch')requestHover(card,event.clientX);});
$('#grid').addEventListener('pointerout',event=>{const card=event.target.closest('.asset-card');if(event.pointerType!=='touch'&&card&&!card.contains(event.relatedTarget))stopHover();});
$('#grid').addEventListener('pointermove',pointerMove);
$('#grid').addEventListener('focusout',event=>{if(!scrub.current?.card.contains(event.relatedTarget))stopHover();});
// Explicit keyboard inspection works with reduced motion; Enter still opens real 3D details.
document.addEventListener('keydown',event=>{
  const card=event.target.closest('.asset-card');if(!card||selected||!['ArrowLeft','ArrowRight','Home','End','Escape'].includes(event.key))return;
  const asset=items.find(a=>a.id===card.dataset.id);if(!asset?.turntable)return;
  event.preventDefault();event.stopPropagation();if(event.key==='Escape'){stopHover();return;}
  clearTimeout(hoverTimer);hoverCard=card;scrub.activate(card,asset);
  if(event.key==='Home')scrub.request(0);else if(event.key==='End')scrub.request(asset.turntable.frame_count-1);else scrub.step(event.key==='ArrowLeft'?-1:1);
},true);
let previewTouch=null,suppressedTouchCard=null;
$('#grid').addEventListener('pointerdown',event=>{
  if(event.pointerType!=='touch'||event.button!==0)return;const card=event.target.closest('.asset-card'),asset=items.find(a=>a.id===card?.dataset.id);
  if(!asset?.turntable){stopHover();return;}previewTouch={card,asset,pointerId:event.pointerId,x:event.clientX,y:event.clientY,dragging:false};
});
$('#grid').addEventListener('pointermove',event=>{
  const touch=previewTouch;if(!touch||event.pointerId!==touch.pointerId)return;const dx=event.clientX-touch.x,dy=event.clientY-touch.y;
  if(!touch.dragging){if(Math.abs(dy)>9&&Math.abs(dy)>Math.abs(dx)){previewTouch=null;return;}if(Math.abs(dx)<9||Math.abs(dx)<Math.abs(dy)*1.25)return;touch.dragging=true;hoverSuppressed=false;hoverCard=touch.card;scrub.activate(touch.card,touch.asset);touch.card.setPointerCapture(event.pointerId);}
  event.preventDefault();const width=touch.card.querySelector('.asset-image').getBoundingClientRect().width;scrub.request((touch.asset.turntable.poster_index||0)+dx/width*touch.asset.turntable.frame_count);
},{passive:false});
function endPreviewTouch(event){if(!previewTouch||event.pointerId!==previewTouch.pointerId)return;if(previewTouch.dragging)suppressedTouchCard=previewTouch.card;if(event.type==='pointercancel')stopHover();previewTouch=null;}
$('#grid').addEventListener('pointerup',endPreviewTouch);$('#grid').addEventListener('pointercancel',endPreviewTouch);
$('#grid').addEventListener('click',event=>{if(suppressedTouchCard&&event.target.closest('.asset-card')===suppressedTouchCard){suppressedTouchCard=null;event.preventDefault();event.stopImmediatePropagation();}},true);
document.addEventListener('pointerdown',event=>{suppressedTouchCard=null;if(scrub.current&&!scrub.current.card.contains(event.target))stopHover();},true);

function fillInfo(asset){
  $('#asset-title').textContent=loc(asset.name);$('#asset-category').textContent=t(asset.category||'');$('#asset-collection').textContent=(asset.worlds||[asset.collection]).filter(Boolean).map(t).join(' · ');$('#asset-description').textContent=loc(asset.description);
  const dims=Array.isArray(asset.dimensions)?asset.dimensions.map(n=>Number(n).toFixed(2)).join(' × ')+' m':t('notAvailable');
  $('#asset-stats').innerHTML=`<dt>${t('triangles')}</dt><dd>${Number.isFinite(asset.triangles)?asset.triangles.toLocaleString():'—'}</dd><dt>${t('dimensions')}</dt><dd>${esc(dims)}</dd><dt>${t('license')}</dt><dd><a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0 ↗</a></dd>`;
  $('#downloads').innerHTML=['bundle','glb','blend'].map(key=>{const file=asset.downloads?.[key]||asset[key];return file?`<a href="${esc(path(file))}" download class="${key==='bundle'?'bundle':'secondary'}"><span>${t(key)}<small>${formatBytes(asset.file_sizes?.[key])}</small></span><span aria-hidden="true">↓</span></a>`:'';}).join('')+(asset.glb?`<button id="copy-attribution">${t('copy')}</button>`:'');
  if($('#copy-attribution'))$('#copy-attribution').onclick=()=>copyText(`${loc(asset.name)} by Leon Made This / s010s — https://github.com/s010s/lowpoly-vault — CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ (indicate any changes)`,$('#copy-attribution'));
  $('#asset-provenance').innerHTML=(asset.scientific_scope?`<p>${esc(loc(asset.scientific_scope))}</p>`:'')+(asset.sources||[]).filter(source=>/^https:\/\//.test(source.url)).map(source=>`<p><a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.title)} ↗</a></p>`).join('');
  $('#provenance').hidden=!$('#asset-provenance').textContent;paintIcons($('#viewer-dialog'));
}
async function copyText(text,button){try{await navigator.clipboard.writeText(text);button.textContent=t('copied');}catch{button.textContent=t('copyFail')+' '+text;}}
function paintNeighbors(){
  const position=neighborItems.findIndex(a=>a.id===selected?.id);
  for(const [selector,offset,key] of [['#previous-model',-1,'previousModel'],['#next-model',1,'nextModel']]){
    const anchor=$(selector),asset=position>=0?neighborItems[position+offset]:null;anchor.hidden=!asset;
    if(asset){anchor.href=href('detail',asset.id);anchor.dataset.modelId=asset.id;anchor.textContent=`${offset<0?'← ':''}${t(key)}${offset>0?' →':''}`;anchor.ariaLabel=`${t(key)}: ${loc(asset.name)}`;}
  }
  paintIcons($('.model-pagination'));
}
async function prepareRelated(asset,version){
  try{
    const packID=asset.packs?.[0];if(!packID){$('#related').hidden=true;await extendNeighbors(version);return;}
    const result=await store.search({pack:packID,pageSize:100});if(version!==detailVersion)return;
    if(!sourceContext){neighborItems=result.items;paintNeighbors();}
    const related=result.items.filter(a=>a.id!==asset.id).slice(0,3);
    $('#related-models').innerHTML=related.map(a=>`<a href="${esc(href('detail',a.id))}" data-model-id="${esc(a.id)}"><img src="${esc(path(a.preview))}" alt="" width="80" height="80" loading="lazy"><span>${esc(loc(a.name))}</span></a>`).join('');$('#related').hidden=!related.length;
    await extendNeighbors(version);
  }catch(error){if(error.name!=='AbortError')$('#related').hidden=true;}
}
async function extendNeighbors(version){
  if(!sourceContext||sourceContext.view!=='catalog'||browseMode==='atlas')return;
  const position=sourceContext.items.findIndex(a=>a.id===selected?.id);
  if(position<0)return;
  let direction=0;
  if(position===0&&sourceContext.firstPage>0)direction=-1;
  else if(position===sourceContext.items.length-1&&sourceContext.lastPage+1<sourceContext.pages)direction=1;
  if(!direction)return;
  const adjacentPage=direction<0?sourceContext.firstPage-1:sourceContext.lastPage+1;
  const result=await store.search({...sourceContext.options,page:adjacentPage,pageSize:24});
  if(version!==detailVersion)return;
  const summaries=result.items.map(a=>({id:a.id,name:a.name}));
  sourceContext.items=direction<0?[...summaries,...sourceContext.items]:[...sourceContext.items,...summaries];
  if(direction<0)sourceContext.firstPage=adjacentPage;else sourceContext.lastPage=adjacentPage;
  // Only adjacent pages are retained; this is not an unbounded second catalog cache.
  if(sourceContext.items.length>72){if(direction>0){sourceContext.items=sourceContext.items.slice(-72);sourceContext.firstPage++;}else{sourceContext.items=sourceContext.items.slice(0,72);sourceContext.lastPage--;}}
  neighborItems=sourceContext.items;history.replaceState({...history.state,source:sourceContext},'',location.href);paintNeighbors();
}
function releaseVisual(node){if(!node)return;node.getAnimations?.().forEach(a=>a.cancel());node.remove();if(node instanceof HTMLCanvasElement){node.width=0;node.height=0;}}
function clearHost(){for(const node of [...$('#canvas-host').children])if(!node.classList.contains('model-canvas'))releaseVisual(node);$('#canvas-host').replaceChildren();}
function copyVisual(source,{square=false}={}){
  if(!source)return null;let copy;
  const width=source.naturalWidth||source.width,height=source.naturalHeight||source.height;
  if(source instanceof HTMLCanvasElement||(source instanceof HTMLImageElement&&source.complete&&source.naturalWidth)){
    copy=document.createElement('canvas');const side=Math.min(width,height),w=square?side:width,h=square?side:height,scale=Math.min(1,1024/Math.max(w,h));copy.width=Math.max(1,Math.round(w*scale));copy.height=Math.max(1,Math.round(h*scale));copy.getContext('2d').drawImage(source,square?(width-side)/2:0,square?(height-side)/2:0,w,h,0,0,copy.width,copy.height);
  }else return null;
  copy.className='model-handoff';copy.setAttribute('aria-hidden','true');copy.dataset.assetId=source.dataset.assetId||'';copy.__presentation=source.__presentation;return copy;
}
function currentDetailVisual({square=false}={}){
  const flight=$('#viewer-dialog .stage-flight');if(flight)return copyVisual(flight,{square});
  const actual=stage?.snapshot(),overlay=$('#canvas-host .model-handoff');
  if(actual&&overlay){const context=actual.getContext('2d'),rect=containRect({left:0,top:0,width:actual.width,height:actual.height},overlay.width/overlay.height);context.globalAlpha=Number(getComputedStyle(overlay).opacity);context.drawImage(overlay,rect.left,rect.top,rect.width,rect.height);if(context.globalAlpha>0)actual.dataset.assetId='';context.globalAlpha=1;}
  const visible=actual||copyVisual(overlay)||copyVisual($('#canvas-host img'));
  if(!square||!visible)return visible;const result=copyVisual(visible,{square:true});releaseVisual(visible);return result;
}
function rememberInterruptedDialog(){
  // Keep the painted frame and opacity across a queued Back/Forward reversal.
  if(interruptedDialog)return;
  interruptedDialog=$('#viewer-dialog').open?{assetId:selected?.id,visual:currentDetailVisual(),rect:$('#viewer-dialog .stage-flight')?.getBoundingClientRect(),chrome:dialogMotion.capture()}:null;
}
function restoreOriginVisual(){document.querySelectorAll('[data-detail-origin]').forEach(card=>card.removeAttribute('data-detail-origin'));}
function cancelDialogMotion(){modalAnimation?.cancel();modalAnimation=null;dialogMotion.cancel();document.querySelectorAll('.stage-flight').forEach(releaseVisual);$('#canvas-host').style.opacity='';}
function containRect(rect,ratio){const width=Math.min(rect.width,rect.height*ratio),height=width/ratio;return {left:rect.left+(rect.width-width)/2,top:rect.top+(rect.height-height)/2,width,height};}
async function animateDialog(from,to,reverse=false,version=detailVersion,flightStart=null){
  const dialog=$('#viewer-dialog'),host=$('#canvas-host');
  if(reduced.matches||!from||!to||from.width<1||from.height<1)return;
  const source=host.querySelector('.model-handoff')||host.querySelector('img'),reuse=source instanceof HTMLCanvasElement,clone=reuse?source:copyVisual(source);if(!clone)return;
  const ratio=(source.naturalWidth||source.width)/(source.naturalHeight||source.height),small=containRect(from,ratio),large=containRect(to,ratio);
  clone.className='stage-flight';Object.assign(clone.style,{left:`${large.left}px`,top:`${large.top}px`,width:`${large.width}px`,height:`${large.height}px`});dialog.append(clone);host.style.opacity='0';
  const transform=`translate(${small.left-large.left}px,${small.top-large.top}px) scale(${small.width/large.width})`;
  const start=flightStart?containRect(flightStart,ratio):null,startTransform=start?`translate(${start.left-large.left}px,${start.top-large.top}px) scale(${start.width/large.width})`:null;
  const animation=modalAnimation=clone.animate(reverse?[{transform:startTransform||'none',opacity:1},{transform,opacity:1}]:[{transform:startTransform||transform,opacity:1},{transform:'none',opacity:1}],{duration:reverse?DIALOG_TIMING.flightClose:DIALOG_TIMING.flightOpen,easing:'cubic-bezier(.18,.8,.2,1)',fill:'forwards'});
  const deadline=reverse?setTimeout(()=>{if(version===detailVersion&&animation.playState==='running')animation.finish();},DIALOG_TIMING.flightClose):null;
  await animation.finished.catch(()=>{});clearTimeout(deadline);if(version!==detailVersion){releaseVisual(clone);return;}
  // Move the exact retained bitmap between the flight and host. Re-copying a
  // large canvas here forces another GPU upload during the short close gesture.
  animation.cancel();if(reuse){clone.className='model-handoff';clone.style.cssText='';host.append(clone);}else releaseVisual(clone);
  host.style.opacity='';if(modalAnimation===animation)modalAnimation=null;
}
reduced.addEventListener('change',()=>{if(reduced.matches)modalAnimation?.finish();});
function releaseHandoff(version){
  const visual=$('#canvas-host .model-handoff');if(!visual)return;
  requestAnimationFrame(()=>{if(version!==detailVersion||!visual.isConnected)return;if(reduced.matches){releaseVisual(visual);return;}const fade=visual.animate([{opacity:1},{opacity:0}],{duration:160,easing:'linear'});fade.finished.catch(()=>{}).finally(()=>releaseVisual(visual));});
}
async function openAsset(id,{push=false,replace=false}={}){
  if(selectedSummary?.id===id&&!closing&&detailController&&!detailController.signal.aborted&&['loading','ready'].includes($('#canvas-host').dataset.modelState))return;
  const dialog=$('#viewer-dialog'),host=$('#canvas-host'),switching=dialog.open&&!closing;
  const previous=interruptedDialog;interruptedDialog=null;
  const resume=previous?.assetId===id?previous:null;if(previous&&!resume)releaseVisual(previous.visual);
  const chromeFrom=previous?.chrome||dialogMotion.capture(),flightStart=resume?.rect||$('#viewer-dialog .stage-flight')?.getBoundingClientRect();
  const interrupted=resume?.visual||(closing?currentDetailVisual():null);
  const cardCapture=!switching&&!interrupted&&scrub.current?.id===id?scrub.capture({transfer:true}):null;
  const retained=interrupted||(switching?currentDetailVisual():cardCapture?.canvas);
  const version=++detailVersion;closing=false;cancelDialogMotion();stopHover();detailController?.abort();detailController=new AbortController();stage?.hide();atlas?.setActive(false);
  const asset=items.find(a=>a.id===id)||index?.initial.find(a=>a.id===id);
  if(push){sourceContext={url:location.pathname+location.search,view:currentView,scroll:scrollY,triggerId:id,pages,firstPage:page,lastPage:page,items:items.map(a=>({id:a.id,name:a.name})),options:queryOptions()};history.pushState({vaultDetail:true,source:sourceContext},'',href('detail',id));}
  else if(replace)history.replaceState(history.state,'',href('detail',id));
  selectedSummary=asset||{id};selected=asset||{id,name:{en:'…',zh:'…'}};
  neighborItems=sourceContext?.items||items;restoreOriginVisual();origin=currentView==='catalog'?document.querySelector(`.asset-card[data-id="${CSS.escape(id)}"]`):null;
  const from=!switching||resume?.rect?origin?.querySelector('.asset-image')?.getBoundingClientRect():null;fillInfo(selected);paintNeighbors();$('#related').hidden=true;clearHost();host.dataset.modelState='loading';
  let poster;
  const addPoster=record=>{const preview=record?.card_preview||record?.preview;if(!preview)return;poster=new Image();poster.src=path(preview);poster.alt=loc(record.name);poster.className='model-poster';poster.dataset.assetId=record.id;if(host.querySelector('.model-handoff')||retained)poster.style.visibility='hidden';host.prepend(poster);};
  addPoster(asset);if(retained){retained.className='model-handoff';host.append(retained);}else{const copy=copyVisual(origin?.querySelector('.asset-image img'));if(copy){copy.dataset.assetId=id;host.append(copy);}}
  $('#viewer-status').textContent=t('viewLoading');controlsReady(false);$('#wireframe').ariaPressed='false';$('#scale-reference').ariaPressed='false';$('#scale-status').textContent='';$('#provenance').open=false;
  if(origin)origin.dataset.detailOrigin='true';
  if(!dialog.open)dialog.showModal();document.body.style.overflow='hidden';const motion=Promise.all([dialogMotion.start({from:chromeFrom}),animateDialog(from,host.getBoundingClientRect(),false,version,flightStart)]);$('#close').focus({preventScroll:true});
  try{
    const detail=await store.getDetail(asset||id);if(version!==detailVersion)return;selected=detail;fillInfo(detail);document.title=`${loc(detail.name)} · Lowpoly Vault`;prepareRelated(detail,version);
    if(!poster)addPoster(detail);
    const s=await getStage();if(version!==detailVersion)return;
    await s.show(host,path(detail.glb),{mode:'detail',metadata:detail,presentationReady:motion,initialView:interrupted?.__presentation||cardCapture?.view,signal:detailController.signal,onStatus:status=>{if(version===detailVersion){controlsReady(status==='ready');$('#viewer-status').textContent=status==='ready'?'':status==='error'?t('viewError'):t('viewLoading');if(status==='ready'){if(poster)poster.style.visibility='hidden';releaseHandoff(version);}else if(status==='error'&&poster){poster.style.visibility='visible';}}}});
    await motion;
  }catch(error){
    // A fast fetch/import failure can arrive while its retained bitmap is still
    // owned by the flight. Wait for it to return before retiring the overlay.
    await motion;
    if(version===detailVersion&&error.name!=='AbortError'){$('#viewer-status').textContent=selected?.glb?t('viewError'):t('detailError');if(!selected?.glb)$('#asset-description').textContent=t('missing');let decoded=false;if(poster){try{await poster.decode();decoded=true;}catch{}}if(version===detailVersion){if(decoded){poster.style.visibility='visible';releaseHandoff(version);}else if(host.querySelector('.model-handoff'))$('#viewer-status').textContent=lang==='zh'?'新预览暂时不可用，保留上一个画面。':'New preview unavailable; the previous view is retained.';}}
  }
}
async function closeAsset(){
  if(!$('#viewer-dialog').open)return;
  const previous=interruptedDialog;interruptedDialog=null;
  const alreadyClosing=closing,retained=previous?.visual?copyVisual(previous.visual,{square:true}):currentDetailVisual({square:true}),returnView=retained?.__presentation,returnAsset=selected;
  const chromeFrom=previous?.chrome||dialogMotion.capture(),flightStart=previous?.rect||$('#viewer-dialog .stage-flight')?.getBoundingClientRect();releaseVisual(previous?.visual);
  hoverSuppressed=true;closing=true;const version=++detailVersion;cancelDialogMotion();detailController?.abort();store.cancelDetail();stage?.hide();clearHost();
  if(retained){retained.className='model-handoff';$('#canvas-host').append(retained);}
  const target=origin?.isConnected?origin.querySelector('.asset-image').getBoundingClientRect():null;
  const matching=retained&&retained.dataset.assetId===returnAsset?.id;
  const visible=matching&&target&&target.bottom>0&&target.top<innerHeight&&target.right>0&&target.left<innerWidth;
  if(!alreadyClosing)await Promise.all([dialogMotion.start({reverse:true,from:chromeFrom}),visible?animateDialog(target,$('#canvas-host').getBoundingClientRect(),true,version,flightStart):Promise.resolve()]);
  if(!closing||version!==detailVersion)return;$('#viewer-dialog').close();dialogMotion.cancel();document.body.style.overflow='';
  if(visible&&origin?.isConnected&&returnAsset?.id===origin.dataset.id){scrub.retainSnapshot(origin,returnAsset,retained,returnView,{transfer:true});hoverCard=origin;}
  clearHost();restoreOriginVisual();selected=selectedSummary=null;closing=false;restoringFocus=true;origin?.isConnected&&origin.focus({preventScroll:true});restoringFocus=false;origin=null;atlas?.setActive(currentView==='catalog'&&browseMode==='atlas');
}
function requestClose(){if(history.state?.vaultDetail)history.back();else{history.replaceState({view:'catalog'},'',href('models'));syncRoute();}}
function hideStaticFor(type){if(staticContent?.dataset.routeType===type)staticContent.hidden=true;}
function showView(view){
  if(view!=='catalog')stopHover();
  if(!['home','catalog','about','detail'].includes(view))view='home';if(view!==currentView)viewScroll[currentView]=scrollY;currentView=view;
  $('#home-page').hidden=view!=='home';$('#catalog-page').hidden=view!=='catalog';$('#about-page').hidden=view!=='about';
  if(staticContent){const type=view==='catalog'?'models':view;staticContent.hidden=staticContent.dataset.routeType!==type || (view==='detail'&&staticContent.dataset.assetId!==directDetailId);if(index&&view!=='detail'&&(view!=='catalog'||$('#grid').ariaBusy==='false'))staticContent.hidden=true;}
  atlas?.setActive(view==='catalog'&&browseMode==='atlas');
  document.querySelectorAll('[data-route]').forEach(anchor=>anchor.setAttribute('aria-current',anchor.dataset.route===view?'page':'false'));
}
async function syncRoute(){
  if(!index)return;
  if(pendingRoute){queuedRoute=true;detailController?.abort();store.cancelDetail();++detailVersion;rememberInterruptedDialog();cancelDialogMotion();return;}
  pendingRoute=true;
  try{
    const oldHash=location.hash;
    if(oldHash.startsWith('#asset=')){const id=decodeURIComponent(oldHash.slice(7));if(/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(id))history.replaceState(null,'',href('detail',id));}
    else if(['#catalog','#collection','#about'].includes(oldHash))history.replaceState(null,'',href(oldHash==='#about'?'about':'models'));
    const route=parseRoute(location.pathname,siteRoot);const nextLang=route.lang==='zh-CN'?'zh':'en';if(lang!==nextLang){lang=nextLang;paintLanguage();}
    if(route.type==='detail'){
      if(history.state?.vaultDetail){sourceContext=history.state.source;showView(sourceContext?.view||'catalog');await openAsset(route.id);}
      else if(staticContent?.dataset.assetId===route.id){directDetailId=route.id;showView('detail');await openAsset(route.id);}
      else {showView('catalog');await openAsset(route.id);}
    }else{
      const source=sourceContext,sameCatalog=route.type==='models'&&source?.view==='catalog'&&source.url===location.pathname+location.search&&$('#grid').ariaBusy==='false';await closeAsset();if(queuedRoute)return;directDetailId=null;readQuery(route);showView(route.type==='models'?'catalog':route.type==='about'?'about':'home');
      if(route.type==='models'&&!sameCatalog)await renderGrid();
      if(source?.url===location.pathname+location.search){scrollTo(0,source.scroll);const trigger=scrub.current?.card||document.querySelector(`.asset-card[data-id="${CSS.escape(source.triggerId||'')}"]`);trigger?.focus({preventScroll:true});}
      else scrollTo(0,viewScroll[currentView]||0);
      sourceContext=null;document.title=`${currentView==='catalog'?t('allModels'):currentView==='about'?t('about'):'Original low-poly assets'} · Lowpoly Vault`;
    }
  }finally{pendingRoute=false;if(queuedRoute){queuedRoute=false;syncRoute();}}
}
function navigate(view){history.pushState({view},'',view==='catalog'?listURL():href(view));syncRoute();}
function paintHome(){
  if(!index)return;document.querySelectorAll('[data-browse] [data-t="exploreAll"]').forEach(e=>e.textContent=lang==='zh'?`浏览全部 ${index.total} 个模型`:`Explore all ${index.total} models`);
  const specs=[['plants','cycad','01'],['geology','natural-arch','02'],['traces','dinosaur-nest','03']];
  $('#home-categories').innerHTML=specs.map(([cat,id,n])=>{const a=index.initial.find(x=>x.id===id)||index.initial.find(x=>x.category===cat),count=index.categories.find(c=>c.id===cat)?.count||0;return a?`<a class="curation-card" href="${esc(href('models',undefined,{query:{category:cat}}))}" data-home-category="${cat}"><div><img src="${esc(path(a.preview))}" alt="${esc(loc(a.name))}" loading="lazy" width="640" height="640"><span class="curation-number">${n}</span></div><span class="curation-title">${t(cat)}<span>${count} ${t('count')} ↗</span></span></a>`:'';}).join('');paintIcons($('#home-page'));
}
function paintLanguage(){
  document.documentElement.lang=lang==='zh'?'zh-CN':'en';$('#filters').ariaLabel=lang==='zh'?'按资产类型筛选':'Filter by category';$('.model-pagination').ariaLabel=lang==='zh'?'上一个和下一个模型':'Previous and next models';$('#sort').ariaLabel=t('sort');document.querySelectorAll('[data-t]').forEach(e=>e.innerHTML=t(e.dataset.t));$('#language').textContent=lang==='en'?'中文':'EN';$('#language').ariaLabel=lang==='en'?'切换为中文':'Switch to English';$('#search').placeholder=t('search');$('#search').ariaLabel=t('search');$('#close').ariaLabel=t('close');$('#canvas-host').ariaLabel=t('canvas');$('#zoom-in').ariaLabel=t('zoomIn');$('#zoom-out').ariaLabel=t('zoomOut');$('.skip').textContent=t('skip');$('.skip').href=href('models');$('#home-query').placeholder=t('homeSearch');$('#home-query').ariaLabel=t('homeSearch');
  document.querySelectorAll('[data-route]').forEach(a=>a.href=href(a.dataset.route));
  document.querySelectorAll('a[href$="THIRD_PARTY_NOTICES.md"]').forEach(a=>a.href=new URL('THIRD_PARTY_NOTICES.md',new URL(siteRoot,location.origin)).href);
  $('.hero-art').src=new URL('home/editorial-hero.webp',new URL(siteRoot,location.origin)).href;
  if($('.review-notice'))$('.review-notice').textContent=t('review');if($('.initial-release-notice'))$('.initial-release-notice').textContent=t('initialRelease');paintHome();paintFilters();paintModes();if(selected){fillInfo(selected);paintNeighbors();}paintIcons();
}

// Ordinary anchor clicks are enhanced; modified/new-tab clicks retain browser behavior.
document.addEventListener('click',event=>{
  const card=event.target.closest('#grid .asset-card');if(card&&plainClick(event)){event.preventDefault();openAsset(card.dataset.id,{push:true});return;}
  const adjacent=event.target.closest('[data-model-id]');if(adjacent&&plainClick(event)){event.preventDefault();openAsset(adjacent.dataset.modelId,{replace:true});return;}
  const enhance=event.target.closest('[data-enhance-model]');if(enhance){openAsset(enhance.dataset.enhanceModel);return;}
  const asset=event.target.closest('[data-home-asset]');if(asset){openAsset(asset.dataset.homeAsset,{push:true});return;}
  const nav=event.target.closest('[data-route]');if(nav&&plainClick(event)){event.preventDefault();navigate(nav.dataset.route);return;}
  const browse=event.target.closest('[data-browse]');if(browse){resetFilters({render:false});navigate('catalog');return;}
  const facet=event.target.closest('[data-home-category]');if(facet&&plainClick(event)){event.preventDefault();resetFilters({render:false});category=facet.dataset.homeCategory;navigate('catalog');return;}
  if(event.target.id==='clear-empty')resetFilters();if(event.target.id==='retry')load();
  const control=event.target.closest('button:not(.asset-card),#downloads a');if(control)motionUI.feedback(control);
});
$('#home-search').onsubmit=event=>{event.preventDefault();resetFilters({render:false});$('#search').value=$('#home-query').value;navigate('catalog');};
$('#close').onclick=requestClose;
$('#viewer-dialog').addEventListener('cancel',event=>{event.preventDefault();requestClose();});
$('#viewer-dialog').addEventListener('click',event=>{if(event.target===$('#viewer-dialog')){const r=event.target.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)requestClose();}});
window.addEventListener('popstate',syncRoute);window.addEventListener('hashchange',syncRoute);
$('#reset').onclick=()=>stage?.reset();$('#zoom-in').onclick=()=>stage?.zoom(1/1.2);$('#zoom-out').onclick=()=>stage?.zoom(1.2);$('#wireframe').onclick=()=>{const on=$('#wireframe').ariaPressed!=='true';$('#wireframe').ariaPressed=String(on);stage?.wireframe(on);};
$('#scale-reference').onclick=()=>{const on=stage?.scaleReference($('#scale-reference').ariaPressed!=='true');$('#scale-reference').ariaPressed=String(!!on);const info=stage?.scaleReferenceInfo;$('#scale-status').textContent=on?`${t('scaleNote')}: ${info.spacingMeters} m`:info?.available?'':t('scaleUnavailable');};
$('#share').onclick=()=>copyText(new URL(href('detail',selected.id),location.origin).href,$('#share'));
$('#language').onclick=()=>{
  const route=parseRoute(location.pathname,siteRoot),next=lang==='en'?'zh':'en';lang=next;
  const target=href(route.type==='not-found'?'home':route.type,route.id,{page:route.page,query:queryOptions()});
  if(currentView==='detail'&&!history.state?.vaultDetail){location.href=target;return;}
  history.replaceState(history.state,'',target);paintLanguage();if(index&&currentView==='catalog')renderGrid();
};
$('#all-assets').onclick=()=>resetFilters();$('#filters').onclick=event=>{const b=event.target.closest('[data-category]');if(b){category=b.dataset.category;page=0;updateListing();}};
$('#world-filter').onchange=()=>{world=$('#world-filter').value;page=0;updateListing();};$('#pack-filter').onchange=()=>{pack=$('#pack-filter').value;page=0;updateListing();};$('#poly-filter').onchange=()=>{maxTriangles=Number($('#poly-filter').value)||0;page=0;updateListing();};
$('#active-filters').onclick=event=>{const b=event.target.closest('[data-clear]');if(!b)return;({category:()=>category='all',world:()=>world='all',pack:()=>pack='all',triangles:()=>maxTriangles=0})[b.dataset.clear]?.();page=0;updateListing();};
$('#search').addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(()=>{page=0;updateListing();},150);});
$('#sort').onchange=()=>{page=0;updateListing();};$('#prev-page').onclick=()=>{page--;updateListing({push:true});$('#collection').scrollIntoView({block:'start'});};$('#next-page').onclick=()=>{page++;updateListing({push:true});$('#collection').scrollIntoView({block:'start'});};
$('#provenance').addEventListener('toggle',()=>{if($('#provenance').open)motionUI.run($('#asset-provenance'),[{opacity:0,transform:'translateY(6px)'},{opacity:1,transform:'none'}],{duration:180});});
$('#downloads').addEventListener('click',event=>{if(event.target.closest('a'))setStatus(lang==='zh'?'已请求下载文件，是否完成请查看浏览器。':'Download requested. Check your browser for progress.');});
document.addEventListener('pointerdown',event=>{if(refine.open&&!refine.contains(event.target))refine.open=false;});
document.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&!selected&&refine.open){refine.open=false;refine.querySelector('summary').focus();}
  if(event.key==='Tab'&&$('#viewer-dialog').open){
    const dialog=$('#viewer-dialog');
    const focusable=[...dialog.querySelectorAll('a[href],button,input,select,textarea,summary,[tabindex]')].filter(el=>!el.disabled&&el.tabIndex>=0&&el.getClientRects().length&&!el.closest('[hidden],[inert]'));
    const first=focusable[0],last=focusable.at(-1),active=document.activeElement;
    if(first&&((event.shiftKey&&(active===first||!dialog.contains(active)))||(!event.shiftKey&&(active===last||!dialog.contains(active))))){event.preventDefault();(event.shiftKey?last:first).focus();}
  }
  if(event.key==='/'&&!selected&&!['INPUT','TEXTAREA','SELECT'].includes(event.target.tagName)){event.preventDefault();if(currentView==='home')$('#home-query').focus();else catalogToolbar.open();}
  if(selected&&['ArrowLeft','ArrowRight'].includes(event.key)&&!event.altKey&&!event.ctrlKey&&!event.metaKey&&!event.target.closest('#canvas-host,input,textarea,select')){const link=$(event.key==='ArrowLeft'?'#previous-model':'#next-model');if(!link.hidden){event.preventDefault();openAsset(link.dataset.modelId,{replace:true});}}
});
window.addEventListener('pagehide',()=>{restoreOriginVisual();releaseVisual(interruptedDialog?.visual);scrub.dispose();stage?.dispose();motionUI.dispose();dialogMotion.dispose();atlas?.dispose();store.dispose();});
async function load(){
  if(!staticContent)$('#grid').innerHTML=Array.from({length:8},()=>'<div class="skeleton" aria-hidden="true"></div>').join('');$('#grid').ariaBusy='true';
  try{
    const review=import.meta.env.DEV&&new URLSearchParams(location.search).get('review')==='1';index=await store.load(new URL(review?'assets/catalog-review.json':'assets/catalog.json',new URL(siteRoot,location.origin)).href);
    if(index.review_only&&!$('.review-notice')){const notice=document.createElement('p');notice.className='review-notice';notice.textContent=t('review');document.body.prepend(notice);}
    if(index.release_status==='initial'&&!$('.initial-release-notice')){const notice=document.createElement('p');notice.className='initial-release-notice';notice.textContent=t('initialRelease');document.querySelector('footer').prepend(notice);}
    paintHome();readQuery();paintFilters();await renderGrid();await syncRoute();
  }catch{showError();}
}
showView(initialRoute.type==='detail'?'detail':initialRoute.type==='models'?'catalog':initialRoute.type==='about'?'about':'home');
paintLanguage();motionUI.shell();load();
