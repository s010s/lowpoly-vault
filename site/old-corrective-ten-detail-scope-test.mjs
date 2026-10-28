import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {resolve} from 'node:path';
import {selectedCorrectiveDetail,assertCorrectiveDetailDelta,CORRECTIVE_DETAIL_BASE}from './old-corrective-ten-detail-scope.mjs';
import {correctiveContext,CORRECTIVE_IDS}from './old-corrective-ten-selection.mjs';import{parseDeclarativeModule}from './detail-capture-authority.mjs';
const read=p=>readFileSync(resolve(p)),manifest=JSON.parse(read('assets/manifest.json'));
test('corrective right scope never grants a missing or forged selection',()=>{
 assert.equal(selectedCorrectiveDetail({manifest:{assets:[]},index:{},proofs:{},read:()=>{throw Error('Unexpected read')}}),null);
 assert.throws(()=>assertCorrectiveDetailDelta({context:{},index:{},proofs:{},read:()=>Buffer.from('{}')}));
 assert.throws(()=>selectedCorrectiveDetail({manifest:{publication:{old_corrective_ten:{path:'fake',sha256:'0'.repeat(64),bytes:2}}},index:{},proofs:{},read:()=>Buffer.from('{}')}));
});
test('actual installed new right11 preserves all 282 unchanged entries and exact old receipts',()=>{
 const context=correctiveContext({manifest,read});if(!context)return;
 const index=parseDeclarativeModule(read('site/gallery/detail-presentations-index.js')),proofs=parseDeclarativeModule(read('site/gallery/detail-input-proofs.js'));
 const args={context,index,proofs,read};const result=assertCorrectiveDetailDelta(args);assert.equal(result.current_count,293);assert.equal(result.unchanged_count,282);assert.equal(result.subjects.length,11);
 for(const change of [x=>delete x.presentations[CORRECTIVE_IDS[0]],x=>x.presentations.outsider=x.presentations[CORRECTIVE_IDS[0]],x=>x.presentations.pertica.source_glb_sha256='0'.repeat(64),x=>x.browser_version='other',x=>x.renderer_input_sha256='0'.repeat(64)]){const x=structuredClone(index);change(x);assert.throws(()=>assertCorrectiveDetailDelta({...args,index:x}));}
 for(const change of [x=>x.receipts.pop(),x=>x.receipts[0].source_commit='0'.repeat(40),x=>x.receipts.at(-1).requested_ids.pop(),x=>x.receipts.at(-1).assets.extra={}]){const x=structuredClone(proofs);change(x);assert.throws(()=>assertCorrectiveDetailDelta({...args,proofs:x}));}
 for(const id of CORRECTIVE_IDS){const x=structuredClone(index);x.presentations[id].png.sha256='0'.repeat(64);assert.throws(()=>assertCorrectiveDetailDelta({...args,index:x}));}
 for(const pin of Object.values(CORRECTIVE_DETAIL_BASE))assert.throws(()=>assertCorrectiveDetailDelta({...args,read:p=>p===pin.path?Buffer.from('changed'):read(p)}));
});
