/** Explicit small-life publication scope. Never discover or promote neighboring candidates. */
import assert from 'node:assert/strict';
import { readFile, realpath } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { collectRefinedRelease } from './refined-release.mjs';
import { assetFileAllowlist } from './asset-delivery.mjs';
import { catalogMembership } from './curation.js';
export const SMALL_LIFE_IDS = ['asteroxylon','bothriolepis','confuciusornis','ichthyornis','juracimbrophlebia','waptia'];
const hash = data => createHash('sha256').update(data).digest('hex');
const safe = path => typeof path === 'string' && !path.startsWith('/') && !/[\\\u0000-\u001f?#%:]/.test(path) && path.split('/').every(p => p && p !== '.' && p !== '..');
async function checked(root, pin) {
  assert(pin && Object.keys(pin).sort().join(',') === 'path,sha256', 'Exact path/hash pin required');
  assert(safe(pin.path) && /^[a-f0-9]{64}$/.test(pin.sha256), 'Safe immutable pin required');
  const full = resolve(root,pin.path); assert.equal(await realpath(full),full,'No release symlink substitutions');
  const bytes = await readFile(full); assert.equal(hash(bytes),pin.sha256,`${pin.path}: release hash mismatch`); return bytes;
}
async function json(root,pin) { return JSON.parse(await checked(root,pin)); }
export async function collectSmallLifeRelease(root,pin) {
  assert(/^assets\/releases\/[a-z0-9-]+\.json$/.test(pin?.path),'Release descriptor path required');
  const release = await json(root,pin);
  assert.equal(release.version,1); assert.equal(release.scope,'small-life-six');
  assert.equal(release.authorization,'owner_requested_website_code_and_models');
  assert.equal(release.authorization_reference,'owner-authorized-six-model-release-20261018');
  assert.deepEqual(release.additions.map(a=>a.id).sort(),SMALL_LIFE_IDS,'Exact six reviewed additions required');
  const base = await collectRefinedRelease(root,release.base_descriptor);
  const additions=[];
  for(const entry of release.additions) {
    const folder = `assets/additions/${entry.id}/small-life-v1`;
    assert.equal(entry.metadata.path,`${folder}/release-metadata.json`);
    const asset=await json(root,entry.metadata),source=await json(root,entry.source_metadata);
    assert.equal(entry.source_metadata.path,`${folder}/source-metadata.json`);
    assert.equal(asset.id,entry.id); assert.equal(source.id,entry.id);
    assert.equal(asset.license,'CC-BY-4.0'); assert.equal(asset.author,'Leon Made This / s010s');
    assert.equal(asset.units,'meters'); assert.equal(asset.triangles,source.triangles); assert.deepEqual(asset.dimensions,source.dimensions);
    for(const key of ['name','description','scientific_scope'])for(const lang of ['en','zh'])assert(typeof asset[key]?.[lang]==='string'&&asset[key][lang].trim(),`${entry.id}: bilingual ${key} required`);
    assert.equal(asset.category,entry.id==='asteroxylon'?'plants':'animals');
    assert.equal(asset.collection,'prehistoric'); assert.deepEqual(asset.worlds,['prehistoric']); assert.deepEqual(asset.packs,['prehistoric-small-life']);
    for(const key of ['qa','review_only','release_status','quality_status','publication','downloads','turntable','card_preview','revision','revision_provenance'])assert(!Object.hasOwn(asset,key),`${entry.id}: reserved release field ${key}`);
    assert.match(entry.source_commit,/^[a-f0-9]{40}$/); assert(asset.source_url.startsWith(`https://github.com/s010s/lowpoly-vault/tree/${entry.source_commit}/`));
    assert.deepEqual(asset.sha256,entry.sha256,'Release payload hashes must match metadata');
    assetFileAllowlist({assets:[asset]});
    for(const key of ['glb','blend','preview']) {
      assert.equal(dirname(asset[key]),folder,'Addition payload must remain in its immutable folder');
      const bytes=await checked(root,{path:asset[key],sha256:entry.sha256[key]});
      if(key==='glb')assert(bytes.toString('ascii',0,4)==='glTF'&&bytes.readUInt32LE(4)===2&&bytes.readUInt32LE(8)===bytes.length,'Valid GLB 2 required');
      if(key!=='preview')assert.equal(entry.sha256[key],source.sha256[key],'Approved source geometry and editable Blend must remain byte-identical');
    }
    const visual=await checked(root,entry.visual_review);assert(visual.includes(entry.sha256.glb),'Independent visual review must name the exact GLB hash');
    if(entry.visual_review.path.endsWith('.json')){const review=JSON.parse(visual);assert.equal(review.status,'PASS');assert.equal(review.asset_results.find(a=>a.asset===entry.id)?.result,'PASS');}
    else assert(visual.toString().includes('All four candidates PASS'),'Independent visual review pass required');
    const validator=await json(root,entry.validator); assert.equal(validator.issues.numErrors,0); assert.equal(validator.issues.numWarnings,0);
    const runtime=await json(root,entry.runtime),parsed=await json(root,entry.parse);
    assert.equal(runtime.status,'pass'); assert.deepEqual(runtime.pageErrors,[]); assert.deepEqual(runtime.consoleErrors,[]); assert.deepEqual(runtime.evidence.errors,[]);
    assert.equal(runtime.hashes[entry.id],entry.sha256.glb,'Runtime evidence must test the released hash');
    assert(runtime.evidence.completed&&runtime.evidence.loads.some(item=>item.name===entry.id&&item.glError===0&&item.nonBackgroundPixels>0),'Actual rendered-model evidence required');
    const measured=parsed.find(a=>a.asset===entry.id); assert.equal(measured?.status,'pass'); assert.equal(measured?.sha256,entry.sha256.glb); assert.equal(measured?.triangles,asset.triangles); assert.equal(measured?.animations,0);
    additions.push({...asset,...catalogMembership(asset),quality_status:'accepted_environment_prop'});
  }
  assert(!additions.some(asset=>base.assets.some(a=>a.id===asset.id)),'Additions cannot replace existing assets');
  return {...base,assets:[...base.assets,...additions],publication:{...base.publication,additions_descriptor:pin,approved_addition_ids:[...SMALL_LIFE_IDS]}};
}

// Explicit staging command; a local manifest update never deploys main.
if(process.argv[1] && (await import('node:url')).pathToFileURL(resolve(process.argv[1])).href===import.meta.url) {
  const [path,flag,digest]=process.argv.slice(2); assert.equal(flag,'--sha256');
  const manifest=await collectSmallLifeRelease(process.cwd(),{path,sha256:digest});
  await (await import('node:fs/promises')).writeFile('assets/manifest.json',JSON.stringify(manifest,null,2)+'\n');
  console.log(`Staged ${manifest.assets.length} models, including exactly ${SMALL_LIFE_IDS.length} small-life additions. No deployment performed.`);
}
