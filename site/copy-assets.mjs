/** Production delivery uses an explicit approved manifest allowlist, never a recursive asset copy. */
import { cp, mkdir, readFile, rm } from 'node:fs/promises';
import { deliverTurntables } from './turntable-delivery.mjs';
import { writeCatalog } from './catalog-build.mjs';
import { clearDeliveredAssets, deliverManifestAssets } from './asset-delivery.mjs';
import { writeStaticRoutes } from './static-routes.mjs';
await mkdir('dist/assets',{recursive:true});
await clearDeliveredAssets('dist');
let manifest={version:1,assets:[]};
try {
  const source=JSON.parse(await readFile('assets/manifest.json','utf8'));
  if(source.review_only)throw new Error('A review-only manifest cannot produce a release catalog.');
  manifest=await deliverTurntables(await deliverManifestAssets(source,'dist'),'dist');
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
const routes=await writeStaticRoutes(manifest,'dist');
console.log(`Static HTML: ${routes.pages} bilingual documents, ${routes.models} model detail pairs.`);
