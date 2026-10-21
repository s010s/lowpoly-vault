/** Historical storage indices are restoration metadata, never acceptance or CI evidence. */
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {FIFTY_TWO_RELEASES} from './accepted-fifty-two-release.mjs';
import {collectFiftyTwoAdditions} from './fifty-two-release.mjs';
const root=process.cwd(),sha=b=>createHash('sha256').update(b).digest('hex');
const removed=new Map();let indices=0;
for(const {release} of FIFTY_TWO_RELEASES){
 const path=release.source_bundle.path.replace('source-bundle.json','process-archive-index.json');
 const bytes=readFileSync(`${root}/${path}`),index=JSON.parse(bytes);
 assert.equal(index.original_snapshot_commit,'86b818b3b8e89bf0ccd3980433c28b309de38ab1');
 assert.equal(index.original_snapshot_tree,'f13f1f77d847be7b2e95e0e2e409b970b6cc86ea');
 assert.equal(index.source_commit,release.source_commit);assert.equal(index.independent_review_commit,release.review_commit);
 assert.match(index.status,/grants no model or publication approval/);
 assert(!/drive\.google|docs\.google|drive_file_id|chatgpt\.com|Bearer\s|private_key/i.test(bytes.toString()));
 const bundle=JSON.parse(readFileSync(`${root}/${release.source_bundle.path}`));
 assert.equal(release.files.filter(p=>p.path===path).length,1);
 assert.equal(release.files.find(p=>p.path===path).sha256,sha(bytes));
 assert.equal(bundle.files.find(p=>p.path===path).sha256,sha(bytes));
 for(const row of index.files){
  assert.match(row.sha256,/^[a-f0-9]{64}$/);assert.match(row.git_blob,/^[a-f0-9]{40}$/);
  assert(['100644','100755'].includes(row.mode));assert(Number.isSafeInteger(row.bytes)&&row.bytes>=0);
  assert(!row.path.startsWith('/')&&!row.path.split('/').some(x=>!x||x==='.'||x==='..'));
  assert(!existsSync(`${root}/${row.path}`),`Archived path still exists: ${row.path}`);
  assert(!release.files.some(p=>p.path===row.path));assert(!bundle.files.some(p=>p.path===row.path));
  if(removed.has(row.path))assert.deepEqual(row,removed.get(row.path));
  removed.set(row.path,row);
 }
 indices++;
}
assert.equal(indices,22);assert.equal(removed.size,1376);assert.equal([...removed.values()].reduce((n,r)=>n+r.bytes,0),12523243);
const {additions}=await collectFiftyTwoAdditions(root,FIFTY_TWO_RELEASES.map(r=>r.descriptor));
const manifest=JSON.parse(readFileSync(`${root}/assets/manifest.json`));assert.equal(manifest.assets.length,347);
for(const asset of additions){assert.deepEqual(asset,manifest.assets.find(a=>a.id===asset.id));assert.equal(asset.approval_provenance.formal_profile_acceptance,'BLOCKED');assert.equal(asset.approval_provenance.hardware_gpu_verified,false);assert.equal(asset.approval_provenance.target_scene_verified,false);}
console.log('PASS fixed52 historical storage: 22 restoration indices; 1376 absent originals; 12523243 bytes; real52 collector and347 manifest unchanged asset contract');
