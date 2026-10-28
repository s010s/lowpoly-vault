/** Mechanism tests use actual installed bytes when selected; never mint review grants. */
import test from 'node:test';import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';import {resolve} from 'node:path';
import {CORRECTIVE_IDS,CORRECTIVE_SAME_IDS,CORRECTIVE_REPRESENTATION_IDS,correctiveContext,correctiveManifestView,composeCorrectiveRegistry,correctiveSourceClosure,inspectCorrectiveSelection} from './old-corrective-ten-selection.mjs';
import {compileCorrectiveSource,validateCorrectiveSource} from './old-corrective-ten-source-binding.mjs';
const read=p=>readFileSync(resolve(p)),manifest=JSON.parse(read('assets/manifest.json'));
test('corrective selection is exact ten stable subjects, eleven configurations and no implicit grant',()=>{
 assert.equal(CORRECTIVE_IDS.length,11);assert.equal(new Set(CORRECTIVE_IDS).size,11);assert.equal(CORRECTIVE_SAME_IDS.length,5);assert.equal(CORRECTIVE_REPRESENTATION_IDS.length,6);
 assert.equal(correctiveContext({manifest:{assets:[]},read:()=>{throw Error('Unexpected read');}}),null);
 for(const pointer of [true,{}, {path:'outside',sha256:'0'.repeat(64),bytes:1}])assert.throws(()=>correctiveContext({manifest:{assets:[],publication:{old_corrective_ten:pointer}},read:()=>Buffer.from('{}')}));
 assert.throws(()=>inspectCorrectiveSelection({selection:{status:'PASS'},selectionPin:null,read}));
 for(const id of [...CORRECTIVE_IDS,'outsider'])assert.throws(()=>compileCorrectiveSource({entry_id:id,asset:{id},documents:{},media:{}}));
});
test('actual corrective source selection preserves exact selected621 or remains absent',()=>{
 const context=correctiveContext({manifest,read});
 if(!manifest.publication?.old_corrective_ten){assert.equal(context,null);assert.deepEqual(correctiveManifestView({manifest,read}),manifest);return;}
 assert(context);assert.equal(manifest.assets.length,627);assert.deepEqual(context.entries.map(e=>e.next.id),CORRECTIVE_IDS);assert.equal(context.baseline.manifest.assets.length,621);
 assert.deepEqual(correctiveManifestView({manifest,read}),context.baseline.manifest);assert.deepEqual(composeCorrectiveRegistry({baseOutput:context.baseline,context}).manifest,manifest);
 for(const path of correctiveSourceClosure(context,read))assert(read(path).length>0);
 for(const e of context.entries){const media={glb:read(e.next.asset.glb),blend:read(e.next.asset.blend)};validateCorrectiveSource(e.receipt,e.next.asset,media);
  for(const key of ['production_acceptance_created','world_accepted','hardware_gpu_accepted']){const r=structuredClone(e.receipt);r[key]=true;assert.throws(()=>validateCorrectiveSource(r,e.next.asset,media));}
  for(const key of ['units','dimensions','source_model_identity']){const a=structuredClone(e.next.asset);a[key]={changed:true};assert.throws(()=>validateCorrectiveSource(e.receipt,a,media));}
 }
 for(const mutate of [m=>m.assets.reverse(),m=>m.assets.pop(),m=>m.assets.find(a=>CORRECTIVE_IDS.includes(a.id)).units='centimeters']){const m=structuredClone(manifest);mutate(m);assert.throws(()=>correctiveContext({manifest:m,read}));}
 for(const path of [context.selectionPin.path,context.selection.review_path])assert.throws(()=>correctiveContext({manifest,read:p=>p===path?Buffer.from('{}'):read(p)}));
});
