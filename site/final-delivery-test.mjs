import assert from 'node:assert/strict';
import {collectFinalDeliveryCandidates,prepareFinalDeliveryCapture} from './model-registry.mjs';
import {protectedModelPath} from './ci-model-proof.mjs';
const c=collectFinalDeliveryCandidates();
assert.deepEqual(c.candidates.map(c=>c.id).sort(),['caryocrinites','echinosphaerites','eleutherocrinus','micraster','nucleocrinus']);
assert.deepEqual(c.publication_ready_ids,[]);
for(const path of ['scripts/final_delivery.py','scripts/final_delivery_fixed.py','scripts/final_delivery_relations.py','site/final-delivery.mjs'])assert(protectedModelPath(path),`${path} must remain protected`);
const plan=prepareFinalDeliveryCapture();assert.equal(plan.subjects.length,5);assert(plan.subjects.every(x=>x.must_review_exact_final_pixels));
console.log('PASS: five offline candidates; protected code/map; capture preparation does not authorize publication.');
