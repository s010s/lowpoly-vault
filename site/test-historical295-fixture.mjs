/** Test-only projection for the fixed347 delivery; never a publication authorization. */
import assert from 'node:assert/strict';
import {FIFTY_TWO_IDS,assertFiftyTwoBaseline} from './fifty-two-release.mjs';
import {FIFTY_TWO_RELEASES} from './accepted-fifty-two-release.mjs';
export function historical295Fixture(manifest){
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
