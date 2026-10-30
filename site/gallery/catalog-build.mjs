/** Build-time presentation resolution. Provenance remains in the full manifest;
 * the browser receives the exact display fields after these source-bound checks. */
import {readFile,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {resolveGalleryPoster} from './wheel-presentations.js';
import {createCatalog} from '../catalog-build.mjs';
import {validateGalleryCatalog,validateGalleryModels} from './catalog-source.js';
const safeAssetPath=value=>typeof value==='string'&&value.startsWith('assets/')&&!/[\\\u0000-\u001f?#%]/.test(value)&&!value.split('/').some(part=>!part||part==='.'||part==='..');
export function prepareModels(manifest,resources={}, {allowReview=false}={}) {
  if((manifest?.review_only&&!allowReview)||!Array.isArray(manifest?.assets))throw new Error('Published catalog unavailable.');
  const ids=new Set();
  return manifest.assets.map(asset=>{
    if(!/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(asset.id||'')||ids.has(asset.id)||!asset.name||!['glb','blend','preview'].every(key=>safeAssetPath(asset[key])))throw new Error('Invalid published model.');
    ids.add(asset.id);
    const poster=resolveGalleryPoster(asset,resources),matching=!!poster;
    const {detailPresentation:untrustedDetailPresentation,...sourceAsset}=asset;
    return {...sourceAsset,author:asset.author||manifest.author||'Leon Made This / s010s',license:asset.license||manifest.license||'CC-BY-4.0',source_url:asset.source_url||manifest.attribution_url||'https://github.com/s010s/lowpoly-vault',worlds:asset.worlds||[asset.collection].filter(Boolean),packs:asset.packs||[],glb_bytes:asset.glb_bytes||asset.file_sizes?.glb||0,
      ...(poster?.detailPresentation?{detailPresentation:poster.detailPresentation}:{}),
      ...(matching?{galleryPosters:{detail:poster.detail,wheel:poster.wheel},wheelSpec:poster.wheelSpec}:{})};
  });
}

export const DISPLAY_FIELDS=['id','name','category','collection','worlds','packs','glb','blend','preview','glb_bytes','dimensions','units','axes','blender_unit_scale','triangles','description','reconstruction_notes','scientific_scope','sources','source_url','author','license','downloads','galleryPosters','wheelSpec','detailPresentation'];
export function createGalleryCatalog(manifest,resources, {index=createCatalog(manifest).index,allowReview=false}={}){
 const prepared=prepareModels(manifest,resources,{allowReview});
 const assets=prepared.map(asset=>({...Object.fromEntries(DISPLAY_FIELDS.filter(key=>asset[key]!==undefined).map(key=>[key,asset[key]])),sha256:{glb:asset.sha256?.glb}}));
 const result={version:1,kind:'gallery-display-v1',total:assets.length,review_only:manifest.review_only===true,assets,worlds:index.worlds,packs:index.packs};
 validateGalleryModels(result,{allowReview});validateGalleryCatalog(result,assets,{reviewOnly:result.review_only});return result;
}
export async function writeGalleryCatalog(manifest,out,{root=process.cwd()}={}){
 const resources=JSON.parse(await readFile(resolve(root,'site/public/gallery/resources.json')));
 const result=createGalleryCatalog(manifest,resources);
 await writeFile(resolve(out,'assets/gallery.json'),JSON.stringify(result)+'\n');return result;
}
