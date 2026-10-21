/** Test-only exact352/exact347 projection; never a publication authorization. */
import assert from 'node:assert/strict';
import {digest} from './model-registry.mjs';
import {FINAL_FIVE_IDS,FINAL_FIVE_PRESENTATION} from './final-five-release.mjs';
import {FIFTY_TWO_IDS,assertFiftyTwoBaseline} from './fifty-two-release.mjs';
import {FIFTY_TWO_RELEASES} from './accepted-fifty-two-release.mjs';
// Canonical whole manifests, not asset counts or caller-supplied claims.
// 347: reviewed migration main 7ab45923c28a59e91f54ad1efde2928fe5bd4faf.
// 352: exactly that whole347 plus unchanged reviewed24d75 five objects/presentation.
const FIXED347='7c86e7087dd1b1dd1e207bce67fc5b9dec3e5cf80bb433d762c70a1c48b2e463';
const FIXED352='3640bfe31556f321f8dc4f292625ddd858bbf7426ec1e6e89b851cfb4f6e367d';
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
