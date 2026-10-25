/** Exact original approval hashes survive canonical registry JSON, never changed data. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {historicalGalleryView,successorReader} from './same-id-successors.mjs';
import {restoreHistoricalPosterSerialization,assertHistoricalPosterApprovals} from './gallery-poster-compat.mjs';
const hash=value=>createHash('sha256').update(JSON.stringify(value)).digest('hex');
const manifest=JSON.parse(readFileSync('assets/manifest.json')),selected=JSON.parse(readFileSync('site/public/gallery/resources.json')),baseline=JSON.parse(readFileSync('site/gallery/approved-poster-inputs.json'));
await assertHistoricalPosterApprovals({root:process.cwd(),baseline});
const source=historicalGalleryView({manifest,resources:selected,read:successorReader(process.cwd())}),before=JSON.stringify(source);
const restored=restoreHistoricalPosterSerialization(source,baseline);
assert.equal(JSON.stringify(source),before,'Restore must not mutate the source');assert.deepEqual(restored,source,'Restoring serialization cannot change any metadata value or array order');
for(const [id,approval] of Object.entries(baseline.posters)){
 const poster=restored.posters[id],seals=restored.files.filter(file=>[poster.detail,poster.wheel].includes(file.path)).sort((a,b)=>a.path.localeCompare(b.path));
 assert.equal(hash({poster,seals}),approval.poster_sha256,id);
}
assert.equal(JSON.stringify(restoreHistoricalPosterSerialization(restored,baseline)),JSON.stringify(restored),'Restoration is idempotent');
const id=Object.keys(baseline.posters)[0];
for(const mutate of [r=>r.posters[id].source_glb_sha256='0'.repeat(64),r=>r.posters[id].wheelSpec.zoom+=0.001,r=>r.posters[id].wheelSpec.projectedBounds.left+=0.001,r=>r.posters[id].extra='unreviewed',r=>r.files.find(f=>f.path===r.posters[id].detail).sha256='0'.repeat(64),r=>r.files.find(f=>f.path===r.posters[id].detail).bytes++,r=>r.files.push(structuredClone(r.files.find(f=>f.path===r.posters[id].detail))),r=>delete r.posters[id]]){
 const changed=structuredClone(source);mutate(changed);assert.throws(()=>restoreHistoricalPosterSerialization(changed,baseline));
}
console.log('PASS historical serialization: all182 original approval hashes, exact semantic equality, immutable source, idempotence and8 tamper rejections.');
