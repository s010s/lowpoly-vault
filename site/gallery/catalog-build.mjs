import {releaseCatalogPath} from '../release-catalog-path.js';
/** Build-time presentation resolution. Provenance remains in the full manifest;
 * the browser receives the exact display fields after these source-bound checks. */
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {resolveGalleryPoster} from './wheel-presentations.js';
import {resolveDesktopHeadingBounds} from './detail-heading-policy.js';
import {createCatalog} from '../catalog-build.mjs';
import {validateGalleryCatalog,validateGalleryModels} from './catalog-source.js';
const safeAssetPath=value=>typeof value==='string'&&value.startsWith('assets/')&&!/[\\\u0000-\u001f?#%]/.test(value)&&!value.split('/').some(part=>!part||part==='.'||part==='..');
const safePreviewPath=value=>typeof value==='string'&&['assets/','gallery/','detail-presentations/','wheel-presentations/'].some(prefix=>value.startsWith(prefix))&&!/[\\\u0000-\u001f?#%]/.test(value)&&!value.split('/').some(part=>!part||part==='.'||part==='..');
export function prepareModels(manifest,resources={}, {allowReview=false}={}) {
  if((manifest?.review_only&&!allowReview)||!Array.isArray(manifest?.assets))throw new Error('Published catalog unavailable.');
  const ids=new Set();
  return manifest.assets.map(asset=>{
    if(!/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(asset.id||'')||ids.has(asset.id)||!asset.name||!['glb','blend'].every(key=>safeAssetPath(asset[key]))||!safePreviewPath(asset.preview))throw new Error('Invalid published model.');
    ids.add(asset.id);
    const poster=resolveGalleryPoster(asset,resources),matching=!!poster;
    const desktopHeadingBounds=resolveDesktopHeadingBounds(asset,poster,resources);
    const {detailPresentation:untrustedDetailPresentation,galleryPosters:untrustedPosters,wheelSpec:untrustedWheelSpec,desktopHeadingBounds:untrustedHeadingBounds,...sourceAsset}=asset;
    return {...sourceAsset,author:asset.author||manifest.author||'Leon Made This / s010s',license:asset.license||manifest.license||'CC-BY-4.0',source_url:asset.source_url||manifest.attribution_url||'https://github.com/s010s/lowpoly-vault',worlds:asset.worlds||[asset.collection].filter(Boolean),packs:asset.packs||[],glb_bytes:asset.glb_bytes||asset.file_sizes?.glb||0,blend_bytes:asset.blend_bytes||asset.file_sizes?.blend||0,
      ...(poster?.detailPresentation?{detailPresentation:poster.detailPresentation}:{}),
      ...(desktopHeadingBounds?{desktopHeadingBounds}:{}),
      ...(matching?{galleryPosters:{detail:poster.detail,wheel:poster.wheel},wheelSpec:poster.wheelSpec}:{})};
  });
}

export const DISPLAY_FIELDS=['id','name','category','collection','worlds','packs','glb','blend','preview','glb_bytes','blend_bytes','dimensions','units','axes','blender_unit_scale','triangles','description','reconstruction_notes','scientific_scope','sources','source_url','author','license','downloads','galleryPosters','wheelSpec','detailPresentation','desktopHeadingBounds'];
export function createGalleryCatalog(manifest,resources, {index=createCatalog(manifest).index,allowReview=false}={}){
 const prepared=prepareModels(manifest,resources,{allowReview});
 const assets=prepared.map(asset=>({...Object.fromEntries(DISPLAY_FIELDS.filter(key=>asset[key]!==undefined).map(key=>[key,asset[key]])),sha256:{glb:asset.sha256?.glb}}));
 const result={version:1,kind:'gallery-display-v1',total:assets.length,review_only:manifest.review_only===true,assets,worlds:index.worlds,packs:index.packs};
 validateGalleryModels(result,{allowReview});validateGalleryCatalog(result,assets,{reviewOnly:result.review_only});return result;
}
export async function writeGalleryCatalog(manifest,out,{root=process.cwd()}={}){
 const resources=JSON.parse(await readFile(resolve(root,'site/public/gallery/resources.json')));
 const result=createGalleryCatalog(manifest,resources);
 // Only opt-in heading bounds authorize this byte gate. Check the actual
 // emitted right poster before advertising the extent; no global media rehash.
 for(const asset of result.assets){
  const pin=asset.desktopHeadingBounds;
  if(!pin)continue;
  const bytes=await readFile(resolve(out,asset.galleryPosters.detail));
  if(bytes.length!==pin.detail_bytes||createHash('sha256').update(bytes).digest('hex')!==pin.detail_sha256)
   throw new Error('Desktop heading right raster payload differs: '+asset.id);
 }
 const body=JSON.stringify(result)+'\n';
 await writeFile(resolve(out,'assets/gallery.json'),body);
 const pinned=releaseCatalogPath('gallery',process.env.VITE_RELEASE_CATALOG_TOKEN||'');
 if(pinned!=='assets/gallery.json')await writeFile(resolve(out,pinned),body);return result;
}
