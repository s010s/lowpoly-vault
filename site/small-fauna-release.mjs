/** Owner-accepted v002 trio. Historical candidate pending fields remain immutable evidence. */
import assert from 'node:assert/strict';
import { readFile, realpath } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { collectSmallLifeRelease } from './small-life-release.mjs';
import { assetFileAllowlist } from './asset-delivery.mjs';
export const FAUNA_SOURCE_COMMIT = 'c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184';
export const FAUNA_HASHES = {
  burgessomedusa: '3e875212addc1bcf0337e3af02c8fa980fa71c7c14402aca8075afe7df3f20e9',
  diplomystus: '36f382a00d8f93c0970d5cc9fef34a0ac4099cf9eec7edd0ce9f3f4a5f54cbe8',
  kalligramma: '6a5a15ea887312171f5ee213a7db1774459170b9f99df3ef4e9fa81e60fcd39e',
};
export const FAUNA_IDS = Object.keys(FAUNA_HASHES).sort();
const hash = b => createHash('sha256').update(b).digest('hex');
const safe = p => typeof p === 'string' && /^(assets|production|qa|scripts)\//.test(p);
async function checked(root,pin) {
  assert(pin && Object.keys(pin).sort().join(',') === 'path,sha256','Exact path/hash pin required');
  assert(safe(pin.path) && !/[\\\u0000-\u001f?#%:]/.test(pin.path) && pin.path.split('/').every(p=>p&&p!=='.'&&p!=='..'),'Safe release path required');
  assert(/^[a-f0-9]{64}$/.test(pin.sha256),'SHA-256 required');
  const full=resolve(root,pin.path);assert.equal(await realpath(full),full,'Release symlinks forbidden');
  const bytes=await readFile(full);assert.equal(hash(bytes),pin.sha256,`${pin.path}: release hash mismatch`);return bytes;
}
const json = async(root,pin)=>JSON.parse(await checked(root,pin));
export async function collectSmallFaunaRelease(root,pin) {
  assert.equal(pin?.path,'assets/releases/small-fauna-trio-v002-20261018.json');
  const release=await json(root,pin);
  assert.equal(release.version,1);assert.equal(release.scope,'small-fauna-trio-v002');
  assert.equal(release.authorization,'owner_accepted_v002_and_requested_production_publication');
  assert.equal(release.authorization_reference,'owner-accepted-small-fauna-v002-20261018');
  assert.equal(release.source_commit,FAUNA_SOURCE_COMMIT);
  assert.deepEqual(release.additions.map(a=>a.id).sort(),FAUNA_IDS,'Only exact accepted trio may be added');
  assert.equal(release.base_descriptor.path,'assets/releases/small-life-six-20261018.json');
  const base=await collectSmallLifeRelease(root,release.base_descriptor),additions=[];
  for(const entry of release.additions) {
    const id=entry.id,folder=`assets/additions/${id}/small-fauna-v2`,candidateFolder=`assets/candidates/small-fauna-trio-v2/${id}`;
    assert.equal(entry.metadata.path,`${folder}/release-metadata.json`);
    assert.equal(entry.candidate.path,`production/small-fauna-trio-v2/${id}/candidate.json`);
    assert.equal(entry.source_metadata.path,`${candidateFolder}/metadata.json`);
    const asset=await json(root,entry.metadata),source=await json(root,entry.source_metadata),candidate=await json(root,entry.candidate);
    assert.equal(asset.id,id);assert.equal(source.id,id);assert.equal(candidate.asset_id,id);assert.equal(candidate.revision,'v002');
    assert.equal(asset.category,'animals');assert.equal(asset.collection,'prehistoric');
    assert.deepEqual(asset.worlds,['prehistoric']);assert.deepEqual(asset.packs,['prehistoric-small-fauna']);
    assert.equal(asset.author,'Leon Made This / s010s');assert.equal(asset.license,'CC-BY-4.0');assert.equal(asset.units,'meters');
    assert.equal(asset.triangles,source.triangles);assert.deepEqual(asset.dimensions,source.dimensions);
    assert.equal(asset.source_url,`https://github.com/s010s/lowpoly-vault/tree/${FAUNA_SOURCE_COMMIT}/${candidateFolder}`);
    for(const key of ['name','description','scientific_scope'])for(const lang of ['en','zh'])assert(asset[key]?.[lang]?.trim(),`Bilingual ${key} required`);
    for(const field of ['qa','review_only','release_status','quality_status','publication','downloads','turntable','card_preview','revision','revision_provenance'])assert(!Object.hasOwn(asset,field),`Reserved field: ${field}`);
    assert.equal(asset.sha256.glb,FAUNA_HASHES[id],'Exact user-accepted GLB required');
    assert.deepEqual(asset.sha256,entry.sha256);assetFileAllowlist({assets:[asset]});
    for(const key of ['glb','blend','preview']) {
      assert.equal(dirname(asset[key]),folder,'Release payload must stay in its immutable folder');
      const bytes=await checked(root,{path:asset[key],sha256:entry.sha256[key]});
      if(key!=='preview') {
        const role=key==='glb'?'glb':'source';
        assert.equal(candidate.artifacts[role].path,`${candidateFolder}/${id}.${key}`);
        assert.equal(entry.sha256[key],candidate.artifacts[role].sha256,'No changes to accepted GLB/Blend');
        assert.equal(hash(await checked(root,candidate.artifacts[role])),entry.sha256[key]);
        assert.equal(entry.sha256[key],source.sha256[key]);
      }
      if(key==='glb')assert(bytes.toString('ascii',0,4)==='glTF'&&bytes.readUInt32LE(4)===2&&bytes.readUInt32LE(8)===bytes.length,'Real GLB 2 required');
    }
    for(const [role,sourcePin] of Object.entries(candidate.technical_evidence)) {
      const {path,sha256}=sourcePin;await checked(root,{path,sha256});
      assert(/^(khronos|source_export|reproducibility|browser|views)$/.test(role),'Known frozen evidence role required');
    }
    const validator=await json(root,{path:candidate.technical_evidence.khronos.path,sha256:candidate.technical_evidence.khronos.sha256});
    assert.equal(validator.issues.numErrors,0);assert.equal(validator.issues.numWarnings,0);
    const runtime=await json(root,{path:candidate.technical_evidence.browser.path,sha256:candidate.technical_evidence.browser.sha256});
    assert.equal(runtime.status,'pass');assert.deepEqual(runtime.errors,[]);assert.deepEqual(runtime.failed,[]);assert.equal(runtime.glb_sha256,asset.sha256.glb);
    const review=await json(root,candidate.independent_review);
    assert.equal(review.glb_sha256,asset.sha256.glb);assert.deepEqual(review.blockers,[]);
    assert(review.criteria.every(c=>c.status==='pass'||(c.id==='scientific-species-and-venation-fidelity'&&c.status==='unknown')),'Required review criteria must pass; species fidelity remains outside stylized-art scope');
    additions.push({...asset,quality_status:'owner_accepted_stylized_prop'});
  }
  assert(!additions.some(a=>base.assets.some(b=>a.id===b.id)),'Trio cannot replace existing published assets');
  return {...base,assets:[...base.assets,...additions],publication:{...base.publication,fauna_descriptor:pin,approved_fauna_ids:FAUNA_IDS}};
}
