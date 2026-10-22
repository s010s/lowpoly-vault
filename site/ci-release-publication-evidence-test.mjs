import assert from 'node:assert/strict';
import {assertReusedPublicationReports} from './ci-release-publication-evidence.mjs';
const expected={kind:'publication-unchanged-baseline-v1',status:'REUSED_BASELINE',identity:{source:'a',run:1},baseline:{source:'b',run:2},added_ids:['new'],suites:['a','b','c','d','e']};
const reports=()=>Array.from({length:4},(_,i)=>({...structuredClone(expected),shard_index:i,suites:expected.suites.filter((_,j)=>j%4===i),executed_suites:[],fresh_pass:false}));
assert.equal(assertReusedPublicationReports(expected,reports().reverse()).status,'REUSED_BASELINE');let n=1;
for(const edit of [r=>r.pop(),r=>r.push(r[0]),r=>r[1]=r[0],r=>r[0].status='PASS',r=>r[0].fresh_pass=true,r=>r[0].executed_suites=['a'],r=>r[0].baseline.run=3,r=>r[0].identity.source='other',r=>r[0].added_ids=[],r=>r[0].suites=[],r=>r[0].shard_index=9]){const r=reports();edit(r);assert.throws(()=>assertReusedPublicationReports(expected,r));n++;}
console.log(`Publication reuse integrity: ${n} cases passed; reuse never reported as new suite PASS.`);

const {publicationRuntimeCompatible}=await import('./ci-release-publication-evidence.mjs');
const productionRuntime={site_base:'/lowpoly-vault/',site_origin:'https://s010s.github.io',node_major:'22',platform:'linux',arch:'x64'};
assert(publicationRuntimeCompatible(productionRuntime));
for(const delta of [{node_major:'24'},{platform:'darwin'},{arch:'arm64'}])assert.equal(publicationRuntimeCompatible({...productionRuntime,...delta}),false);
for(const runtime of [{site_base:'/',site_origin:''},{site_base:'/',site_origin:'https://s010s.github.io'},{site_base:'/lowpoly-vault/',site_origin:''}])assert.equal(publicationRuntimeCompatible(runtime),false);
const {readFileSync}=await import('node:fs');
const caller=readFileSync(new URL('../.github/workflows/asset-pipeline.yml',import.meta.url),'utf8');
assert(!/site_base:|site_origin:/.test(caller),'Asset caller must retain default root runtime for shared/quality/dispatch/full paths');
console.log('Publication runtime: 8 matching/Node/platform/default-root preservation assertions passed.');
