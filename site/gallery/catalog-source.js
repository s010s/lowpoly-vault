/** The release manifest owns membership. Reviewed resources only decorate matching bytes. */
import {parseRoute,routeHref} from '../routes.js';
import {siteRoot,assetURL} from './urls.js';
export {siteRoot,assetURL};
export let models=[];
export let catalog={};
const safeAssetPath=value=>typeof value==='string'&&value.startsWith('assets/')&&!/[\\\u0000-\u001f?#%]/.test(value)&&!value.split('/').some(part=>!part||part==='.'||part==='..');
export function prepareModels(manifest,resources={}, {allowReview=false}={}) {
  if((manifest?.review_only&&!allowReview)||!Array.isArray(manifest?.assets))throw new Error('Published catalog unavailable.');
  const ids=new Set();
  return manifest.assets.map(asset=>{
    if(!/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(asset.id||'')||ids.has(asset.id)||!asset.name||!['glb','blend','preview'].every(key=>safeAssetPath(asset[key])))throw new Error('Invalid published model.');
    ids.add(asset.id);
    const poster=resources.posters?.[asset.id],matching=poster&&poster.source_glb_sha256===asset.sha256?.glb;
    return {...asset,author:asset.author||manifest.author||'Leon Made This / s010s',license:asset.license||manifest.license||'CC-BY-4.0',source_url:asset.source_url||manifest.attribution_url||'https://github.com/s010s/lowpoly-vault',worlds:asset.worlds||[asset.collection].filter(Boolean),packs:asset.packs||[],glb_bytes:asset.glb_bytes||asset.file_sizes?.glb||0,
      ...(matching?{galleryPosters:{detail:poster.detail,wheel:poster.wheel},wheelSpec:poster.wheelSpec}:{})};
  });
}
export async function loadGalleryCatalog({fetchImpl=fetch}={}) {
  const read=async path=>{const response=await fetchImpl(assetURL(path));if(!response.ok)throw new Error(`Catalog request failed (${response.status}).`);return response.json();};
  const [manifest,resources]=await Promise.all([read('assets/manifest.json'),read('gallery/resources.json')]);
  models=prepareModels(manifest,resources,{allowReview:document.body.dataset.reviewOnly==='true'});catalog={manifest,resources,route:parseRoute(location.pathname,siteRoot.pathname)};
  return {models,catalog};
}
export const emptyFacets=()=>({worlds:[],packs:[],category:[],collection:[],triangleBand:[],triangleMax:[]});
export function readGalleryQuery(params) {
  const facets=emptyFacets();
  for(const [key,param] of [['worlds','world'],['packs','pack'],['category','category'],['collection','collection'],['triangleBand','triangleBand']])facets[key]=[...new Set(params.getAll(param).filter(value=>value&&value!=='all'))];
  const max=Number(params.get('maxTriangles'));if(Number.isFinite(max)&&max>0)facets.triangleMax=[String(max)];
  const requested=params.get('sort'),sort=['curated','name','name-desc','triangles','triangles-asc','triangles-desc'].includes(requested)?requested:'curated';
  return {query:params.get('q')||'',facets,sort};
}
export function galleryURL(state,{base=siteRoot.pathname,origin=siteRoot.origin}={}) {
  const url=new URL(routeHref({type:'models',lang:state.lang,page:state.page||0},base),origin);
  if(state.selected)url.searchParams.set('model',state.selected);
  if(state.query.trim())url.searchParams.set('q',state.query.trim());
  for(const [key,param] of [['worlds','world'],['packs','pack'],['category','category'],['collection','collection'],['triangleBand','triangleBand']])for(const value of state.facets[key]||[])url.searchParams.append(param,value);
  if(state.facets.triangleMax?.[0])url.searchParams.set('maxTriangles',state.facets.triangleMax[0]);
  if(state.sort!=='curated')url.searchParams.set('sort',state.sort);
  return url;
}
export const detailHref=(id,lang)=>routeHref({type:'detail',id,lang},siteRoot.pathname);
