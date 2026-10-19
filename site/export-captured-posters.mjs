/** Public capture transport for environments unable to download Actions artifacts. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {LANDAIR_CAPTURE} from './accepted-landair-capture.mjs';
import {QUARTETS_CAPTURE} from './accepted-quartets-capture.mjs';
import {CONCEPT_SEVEN_IDS} from './concept-seven-release.mjs';
const root=resolve(process.env.PREVIEW_OUTPUT||'qa/ci-publication-capture');
const report=JSON.parse(await readFile(resolve(root,'render-report.json')));
const index=JSON.parse(await readFile(resolve(root,'assets/turntables/index.json')));
const ids=process.env.PREVIEW_ASSET_IDS.split(',');
if(ids.includes(LANDAIR_CAPTURE.assets[0].id))assert.deepEqual(ids.slice().sort(),LANDAIR_CAPTURE.assets.map(a=>a.id).sort());
else if(ids.length===QUARTETS_CAPTURE.assets.length)assert.deepEqual(ids.slice().sort(),QUARTETS_CAPTURE.assets.map(a=>a.id).sort());
else if(ids.length===7)assert.deepEqual(ids.slice().sort(),CONCEPT_SEVEN_IDS);
else assert.equal(new Set(ids).size,12);
assert.equal(report.status,'pass');
assert.equal(report.chromium_version,report.pinned_chromium_version);
assert.deepEqual(report.assets.map(a=>a.id).sort(),ids.slice().sort());
console.log('PUBLICATION_CAPTURE_REPORT '+JSON.stringify({capture_only:true,source_commit:process.env.GITHUB_SHA,report,index}));
for(const id of ids){
 const entry=index.posters.find(p=>p.id===id);assert(entry);
 const bytes=await readFile(resolve(root,entry.path));
 assert.equal(bytes.length,entry.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),entry.sha256);
 console.log('PUBLICATION_CAPTURE_FILE '+JSON.stringify(entry));
 const encoded=bytes.toString('base64');
 for(let offset=0;offset<encoded.length;offset+=4096)console.log('PUBLICATION_CAPTURE_DATA '+JSON.stringify({path:entry.path,offset,data:encoded.slice(offset,offset+4096)}));
}
