/** Test-only exact352/exact347 projection; never a publication authorization. */
import assert from 'node:assert/strict';
import {digest} from './model-registry.mjs';
import {FINAL_FIVE_IDS,FINAL_FIVE_PRESENTATION} from './final-five-release.mjs';
import {FIFTY_TWO_IDS,assertFiftyTwoBaseline} from './fifty-two-release.mjs';
import {FIFTY_TWO_RELEASES} from './accepted-fifty-two-release.mjs';
// Canonical whole manifests, not asset counts or caller-supplied claims.
// 347: bb8599225e2167d57282bbe19e6dc12fc6a2715d; 352: reviewed 24d75a5.
const FIXED347='da39151f8ffb135cc32e76a89cff03acf065f0419f9aebed5a0929f68a3aa2d8';
const FIXED352='2cee8d93b6054aa4d1cf6114a147c2a3f7702dec00234343071f99f0fcd8f427';
export function historical295Fixture(input){
 const manifest=structuredClone(input);
 if(manifest.assets?.length===352){
  assert.equal(digest(manifest),FIXED352,'Historical fixture requires exact reviewed352 whole objects');
  assert.deepEqual(manifest.assets.filter(a=>FINAL_FIVE_IDS.includes(a.id)).map(a=>a.id).sort(),FINAL_FIVE_IDS);
  assert.deepEqual(manifest.publication?.final_five_presentation,FINAL_FIVE_PRESENTATION);
  manifest.assets=manifest.assets.filter(a=>!FINAL_FIVE_IDS.includes(a.id));
  delete manifest.publication.final_five_presentation;
 }
 assert.equal(digest(manifest),FIXED347,'Historical fixture requires exact unchanged347 whole objects');
 assert.equal(manifest.assets?.length,347,'Historical fixture requires exact347 current objects');
 assert.deepEqual(manifest.assets.filter(a=>FIFTY_TWO_IDS.includes(a.id)).map(a=>a.id).sort(),FIFTY_TWO_IDS,'Historical fixture requires exact fixed52 new IDs');
 assert.deepEqual(manifest.publication?.fifty_two_descriptors,FIFTY_TWO_RELEASES.map(r=>r.descriptor),'Historical fixture requires exact fixed52 descriptor field');
 const base=structuredClone(manifest);
 base.assets=base.assets.filter(a=>!FIFTY_TWO_IDS.includes(a.id));
 delete base.publication.fifty_two_descriptors;
 // This fixed whole-object digest also binds every old field and array order.
 assertFiftyTwoBaseline(base);
 return base;
}
