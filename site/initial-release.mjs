import {appendFinalFiveRelease} from './final-five-release.mjs';
import {appendFiftyTwoRelease} from './fifty-two-release.mjs';
import {appendFortyFourRelease} from './forty-four-release.mjs';
import {collectConceptLandairRelease,collectBatch54Release,collectBatches5253Release,appendBatches5657Release,appendBatches5155Release,appendBatches6061Release,appendBatches5861Release,appendBatches6267Release} from './concept-landair-release.mjs';
import {collectConceptQuartetsRelease} from './concept-quartets-release.mjs';
import {collectConceptSevenRelease} from './concept-seven-release.mjs';
import {collectRound13Release} from './small-life-round13-release.mjs';
/** Owner-authorized initial collection. This does not grant final artistic or scientific approval. */
import { readFile, writeFile, realpath } from 'node:fs/promises';
import { resolve, relative, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
import { collectManifest } from './generate-manifest.mjs';
import { assetFileAllowlist } from './asset-delivery.mjs';
import { collectRefinedRelease } from './refined-release.mjs';
import {collectRound12Release} from './small-life-round12-release.mjs';
import { collectRound11Release } from './small-life-round11-release.mjs';
import { collectRound10Release } from './small-life-round10-release.mjs';
import { collectRound09Release } from './small-life-round09-release.mjs';
import { collectRound08Release } from './small-life-round08-release.mjs';
import { collectRound07Release } from './small-life-round07-release.mjs';
import { collectRound06Release } from './small-life-round06-release.mjs';
import { collectRound05Release } from './small-life-round05-release.mjs';
import { collectRound04Release } from './small-life-round04-release.mjs';
import { collectRound03Release } from './small-life-round03-release.mjs';
import { collectRound02Release } from './small-life-round02-release.mjs';
import { collectSmallLifeBatchRelease } from './small-life-batch-release.mjs';
import { collectSmallFaunaRelease } from './small-fauna-release.mjs';
import { collectSmallLifeRelease } from './small-life-release.mjs';

export const INITIAL_ASSET_IDS = ['conifer-tree','cycad','dinosaur-nest','fern-cluster','horsetail-cluster','lepidodendron','natural-arch','stratified-cliff','three-toed-track','uprooted-log'];
export async function collectInitialRelease(root=process.cwd()) {
  const approval=JSON.parse(await readFile(resolve(root,'assets/initial-publication.json'),'utf8'));
  assert.equal(approval.version,1);
  assert.equal(approval.release_status,'initial');
  assert.equal(approval.quality_status,'work_in_progress');
  assert.equal(approval.authorization,'owner_requested_publication_of_existing_ten');
  assert.equal(approval.source_commit,'550ac6b1d4477d1fbd85ea9f8eb69502b20a42a7');
  assert.deepEqual(approval.assets.map(a=>a.id).sort(),INITIAL_ASSET_IDS,'Only the original ten assets are authorized');
  const {review_only,...candidate}=await collectManifest(root,{preview:true});
  assert.deepEqual(candidate.assets.map(a=>a.id).sort(),INITIAL_ASSET_IDS,'No extra or missing models may enter the initial collection');
  for(const asset of candidate.assets) {
    const approved=approval.assets.find(a=>a.id===asset.id);
    assetFileAllowlist({assets:[asset]});
    for(const key of ['glb','blend','preview']) {
      assert.equal(asset[key],approved[key],`${asset.id}: publication path changed`);
      assert.match(approved.sha256?.[key]||'',/^[a-f0-9]{64}$/,'Every published file needs a fixed SHA-256');
      const actualPath=relative(resolve(root),await realpath(resolve(root,asset[key]))).split('\\').join('/');
      assert.equal(actualPath,asset[key],'Initial publication does not allow symlink substitutions');
      const actualHash=createHash('sha256').update(await readFile(resolve(root,asset[key]))).digest('hex');
      assert.equal(actualHash,approved.sha256[key],`${asset.id}: original ${key} bytes changed`);
    }
    const qa=JSON.parse(await readFile(resolve(root,dirname(asset.glb),'qa.json'),'utf8'));
    assert(['pass','pass_with_warnings'].includes(qa.khronos_validator?.status),`${asset.id}: Khronos validation required`);
    assert(!qa.khronos_validator?.errors?.length,`${asset.id}: unresolved validator errors`);
    asset.sha256={...approved.sha256};
    asset.quality_status='work_in_progress';
  }
  return {...candidate,release_status:'initial',quality_status:'work_in_progress',publication:{authorization:approval.authorization,authorized_on:approval.authorized_on,source_commit:approval.source_commit},assets:candidate.assets};
}
export async function checkPublishedManifest(root=process.cwd()) {
  const current=JSON.parse(await readFile(resolve(root,'assets/manifest.json'),'utf8'));
  assert(!current.review_only,'A review-only manifest cannot be published');
  let expected=current.publication?.batches52_53_descriptors
    ?await collectBatches5253Release(root,current.publication.batches52_53_descriptors,current.publication.batches52_53_base_descriptor)
    :current.publication?.batch54_descriptor
    ?await collectBatch54Release(root,current.publication.batch54_descriptor)
    :current.publication?.concept_landair_descriptor
    ?await collectConceptLandairRelease(root,current.publication.concept_landair_descriptor)
    :current.publication?.concept_quartets_descriptor
    ?await collectConceptQuartetsRelease(root,current.publication.concept_quartets_descriptor)
    :current.publication?.concept_seven_descriptor
    ?await collectConceptSevenRelease(root,current.publication.concept_seven_descriptor)
    :current.publication?.round13_descriptor
    ?await collectRound13Release(root,current.publication.round13_descriptor)
    :current.publication?.round12_descriptor
    ?await collectRound12Release(root,current.publication.round12_descriptor)
    :current.publication?.round11_descriptor
    ?await collectRound11Release(root,current.publication.round11_descriptor)
    :current.publication?.round10_descriptor
    ?await collectRound10Release(root,current.publication.round10_descriptor)
    :current.publication?.round09_descriptor
    ?await collectRound09Release(root,current.publication.round09_descriptor)
    :current.publication?.round08_descriptor
    ?await collectRound08Release(root,current.publication.round08_descriptor)
    :current.publication?.round07_descriptor
    ?await collectRound07Release(root,current.publication.round07_descriptor)
    :current.publication?.round06_descriptor
    ?await collectRound06Release(root,current.publication.round06_descriptor)
    :current.publication?.round05_descriptor
    ?await collectRound05Release(root,current.publication.round05_descriptor)
    :current.publication?.round04_descriptor
    ?await collectRound04Release(root,current.publication.round04_descriptor)
    :current.publication?.round03_descriptor
    ?await collectRound03Release(root,current.publication.round03_descriptor)
    :current.publication?.round02_descriptor
    ?await collectRound02Release(root,current.publication.round02_descriptor)
    :current.publication?.batch_descriptor
    ?await collectSmallLifeBatchRelease(root,current.publication.batch_descriptor)
    :current.publication?.fauna_descriptor
    ?await collectSmallFaunaRelease(root,current.publication.fauna_descriptor)
    :current.publication?.additions_descriptor
    ?await collectSmallLifeRelease(root,current.publication.additions_descriptor)
    :current.release_status==='mixed'
    ?await collectRefinedRelease(root,current.publication?.descriptor)
    :current.release_status==='initial'?await collectInitialRelease(root):await collectManifest(root);
  if(current.publication?.batches56_57_descriptors)expected=await appendBatches5657Release(root,expected,current.publication.batches56_57_descriptors);
  if(current.publication?.batches5155_descriptors)expected=await appendBatches5155Release(root,expected,current.publication.batches5155_descriptors);
  if(current.publication?.batches58_59_descriptors)expected=await appendBatches5861Release(root,expected,current.publication.batches58_59_descriptors,current.publication.batches60_61_descriptors);
  else if(current.publication?.batches60_61_descriptors)expected=await appendBatches6061Release(root,expected,current.publication.batches60_61_descriptors);
  if(current.publication?.batches62_67_descriptors)expected=await appendBatches6267Release(root,expected,current.publication.batches62_67_descriptors);
  if(current.publication?.forty_four_descriptors)expected=await appendFortyFourRelease(root,expected,current.publication.forty_four_descriptors);
  if(current.publication?.fifty_two_descriptors)expected=await appendFiftyTwoRelease(root,expected,current.publication.fifty_two_descriptors);
  if(current.publication?.final_five_presentation)expected=await appendFinalFiveRelease(root,expected,current.publication.final_five_presentation);
  assert.deepEqual(current,expected,'Published manifest must exactly match the checked source and publication scope');
  return current;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href) {
  if(process.argv.includes('--check')) {
    const manifest=await checkPublishedManifest();
    console.log(`Publication gate passed: ${manifest.assets.length} checked assets; quality status: ${manifest.quality_status||'formal QA'}.`);
  } else {
    const manifest=await collectInitialRelease();
    await writeFile('assets/manifest.json',JSON.stringify(manifest,null,2)+'\n');
    console.log('Prepared the authorized initial collection. Formal artistic/scientific approval remains separate.');
  }
}
