/** Offline candidate collector, deliberately separate from deployed registry composition.
 * This does not grant publication, source rebuild, current presentation or GPU acceptance.
 */
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';
const repo=resolve(dirname(fileURLToPath(import.meta.url)),'..');
export function collectFinalDeliveryCandidates(root=repo){
 const result=JSON.parse(execFileSync('python3',[resolve(repo,'scripts/final_delivery.py'),'--root',resolve(root)],{encoding:'utf8',maxBuffer:4*1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}}));
 assert.equal(result.contract,'final-delivery-offline-v1');
 assert.deepEqual(result.publication_ready_ids,[]);
 assert(result.candidates.every(x=>x.publication_ready===false&&x.all_retained_artifact_roles_read_and_hashed.length===7));
 return result;
}
export function prepareFinalDeliveryCapture(root=repo){
 const checked=collectFinalDeliveryCandidates(root);
 return {contract:checked.contract,mode:'prepare-only-not-presentation-acceptance',publication_ready_ids:[],subjects:checked.candidates.map(c=>({id:c.id,glb:c.final_paths.glb,source_glb_sha256:c.native.glb_sha256,required:['canonical-preview','card','gallery-detail','gallery-wheel'],must_review_exact_final_pixels:true})),pending:checked.pending};
}
if(process.argv[1]===fileURLToPath(import.meta.url))console.log(JSON.stringify(process.argv.includes('--prepare-capture')?prepareFinalDeliveryCapture():collectFinalDeliveryCandidates(),null,2));
