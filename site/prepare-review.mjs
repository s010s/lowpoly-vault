/** Builds an isolated CI-only review site. Never writes dist or the release manifest. */
import { build } from 'vite';
import { cp,mkdir,writeFile,rm } from 'node:fs/promises';
import { basename,resolve,sep } from 'node:path';
import { collectManifest } from './generate-manifest.mjs';
import { writeCatalog } from './catalog-build.mjs';
const out=resolve(process.env.REVIEW_OUT || 'qa/review-site');
if (out === resolve('.') || resolve('.').startsWith(out+sep) || out === resolve('qa') ||
  ['assets','site','dist','.git','scripts','node_modules','skills'].some(path=>out === resolve(path) || out.startsWith(resolve(path)+sep))) {
  throw new Error('REVIEW_OUT must be an isolated review directory.');
}
const manifest=await collectManifest(process.cwd(),{preview:true});
await rm(out,{recursive:true,force:true});
await build({build:{outDir:out,emptyOutDir:true}});
await mkdir(`${out}/assets`,{recursive:true});
await cp('assets',`${out}/assets`,{recursive:true,filter:p=>!['manifest.json','manifest.review.json','manifest.json.tmp','catalog','catalog.json','catalog-review','catalog-review.json'].includes(basename(p))});
await writeFile(`${out}/assets/manifest.json`,JSON.stringify(manifest,null,2)+'\n');
await writeCatalog(manifest,out);
await cp('THIRD_PARTY_NOTICES.md',`${out}/THIRD_PARTY_NOTICES.md`);
await writeFile(`${out}/REVIEW-ONLY.txt`,'CI review build. Not approved for publication. Does not change asset QA or production manifest.\n');
console.log(`Isolated review build: ${out}; ${manifest.assets.length} structurally checked assets; visual approval remains pending.`);
