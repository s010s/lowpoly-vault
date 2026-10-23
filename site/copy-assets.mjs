/** Production delivery uses an explicit approved manifest allowlist, never a recursive asset copy. */
import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { deliverTurntables } from './turntable-delivery.mjs';
import { writeCatalog } from './catalog-build.mjs';
import { clearDeliveredAssets, deliverManifestAssets } from './asset-delivery.mjs';
import { writeStaticRoutes } from './static-routes.mjs';
import { productionGalleryResources } from './production-release.mjs';
export async function copyRelease({source,productionResults}={}){
await mkdir('dist/assets',{recursive:true});
await clearDeliveredAssets('dist');
let manifest={version:1,assets:[]};
try {
  source??=JSON.parse(await readFile('assets/manifest.json','utf8'));
  if(source.review_only)throw new Error('A review-only manifest cannot produce a release catalog.');
  manifest=await deliverTurntables(await deliverManifestAssets(source,'dist'),'dist',{productionResults});
  const index=await writeCatalog(manifest,'dist',{approvedOnly:true});
  console.log(`Release catalog: ${index.total} published assets in ${index.shards.length} summary shards.`);
} catch(error) {
  if(error.code!=='ENOENT'||error.path!=='assets/manifest.json')throw error;
  console.warn('No approved manifest: no raw assets, downloads, or public catalog were copied.');
}
await cp('THIRD_PARTY_NOTICES.md','dist/THIRD_PARTY_NOTICES.md');
await cp('LICENSE','dist/LICENSE');
await cp('LICENSES','dist/LICENSES',{recursive:true});
await rm('dist/home/editorial-hero.json',{force:true});
await rm('dist/home/editorial-hero.png',{force:true});
const resources=await productionGalleryResources(process.cwd(),manifest,JSON.parse(await readFile('dist/gallery/resources.json','utf8')),productionResults);
if(manifest.assets.some(a=>a.production_release))await writeFile('dist/gallery/resources.json',JSON.stringify({...resources,production_projection:true},null,2)+'\n');
const routes=await writeStaticRoutes(manifest,'dist');
console.log(`Static HTML: ${routes.pages} bilingual documents, ${routes.models} model detail pairs.`);

return manifest;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)await copyRelease();
