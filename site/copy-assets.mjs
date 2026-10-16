import { cp, mkdir } from 'node:fs/promises';
import { basename } from 'node:path';
await mkdir('dist/assets', {recursive:true});
try { await cp('assets','dist/assets',{recursive:true,filter:source=>!['manifest.review.json','manifest.json.tmp'].includes(basename(source))}); } catch(e) { if(e.code!=='ENOENT') throw e; console.warn('No asset collection yet: site will show an explicit unavailable state.'); }

await cp('THIRD_PARTY_NOTICES.md','dist/THIRD_PARTY_NOTICES.md');
