/** Isolated review build; never mutates the release manifest, assets, or original review output. */
import { build } from 'vite';
import { cp, writeFile, rm } from 'node:fs/promises';
import { resolve, sep } from 'node:path';
import { checkPublishedManifest } from './initial-release.mjs';
import { deliverTurntables } from './turntable-delivery.mjs';
import { writeCatalog } from './catalog-build.mjs';
import { deliverManifestAssets, clearDeliveredAssets } from './asset-delivery.mjs';
import { writeStaticRoutes } from './static-routes.mjs';
const out=resolve(process.env.REVIEW_OUT||'qa/redesign-v2-site');
if(out===resolve('.')||resolve('.').startsWith(out+sep)||out===resolve('qa')||['assets','site','dist','.git','scripts','node_modules','skills','qa/redesign-site'].some(path=>out===resolve(path)||out.startsWith(resolve(path)+sep))) throw new Error('REVIEW_OUT must be an isolated review directory and cannot replace the original redesign build.');
// Use the checked publication and its matching revision image paths.
// An original-ten preview manifest cannot consume the sealed mixed-release image index.
const source=await checkPublishedManifest();
await rm(out,{recursive:true,force:true});
await build({build:{outDir:out,emptyOutDir:true}});
await clearDeliveredAssets(out);
const delivered=await deliverTurntables(await deliverManifestAssets(source,out),out);
const manifest={...delivered,review_only:true};
await writeFile(`${out}/assets/manifest.json`,JSON.stringify(manifest,null,2)+'\n');
await writeCatalog(manifest,out);
await cp('THIRD_PARTY_NOTICES.md',`${out}/THIRD_PARTY_NOTICES.md`);
const routes=await writeStaticRoutes(manifest,out);
await writeFile(`${out}/REVIEW-ONLY.txt`,'Review-only build. Not approved for publication. Asset QA and production manifest are unchanged.\n');
console.log(`Isolated review: ${out}; ${manifest.assets.length} candidates; ${routes.pages} static documents; visual approval pending.`);
