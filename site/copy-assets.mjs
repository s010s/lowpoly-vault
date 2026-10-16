import { cp, mkdir, readFile, rm } from 'node:fs/promises';
import { basename } from 'node:path';
import { writeCatalog } from './catalog-build.mjs';
await mkdir('dist/assets', {recursive:true});
// Standalone reruns must not retain a catalog or manifest removed from the source.
for (const name of ['manifest.json','manifest.review.json','catalog.json','catalog','catalog-review.json','catalog-review']) {
  await rm(`dist/assets/${name}`, {recursive:true,force:true});
}
try { await cp('assets','dist/assets',{recursive:true,filter:source=>!['manifest.review.json','manifest.json.tmp','catalog','catalog.json','catalog-review','catalog-review.json'].includes(basename(source))}); } catch(e) { if(e.code!=='ENOENT') throw e; console.warn('No asset collection yet: site will show an explicit unavailable state.'); }

try {
  const manifest = JSON.parse(await readFile('dist/assets/manifest.json', 'utf8'));
  if (manifest.review_only) throw new Error('A review-only manifest cannot produce a release catalog.');
  const index = await writeCatalog(manifest, 'dist', { approvedOnly: true });
  console.log(`Release catalog: ${index.total} approved assets in ${index.shards.length} summary shards.`);
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
  console.warn('No approved manifest: no public catalog was created. Review assets remain unpublished.');
}

await cp('THIRD_PARTY_NOTICES.md','dist/THIRD_PARTY_NOTICES.md');
