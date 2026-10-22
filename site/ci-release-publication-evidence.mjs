/** Integrity checks only; the caller must independently authenticate its expected baseline. */
import assert from 'node:assert/strict';
export function assertReusedPublicationReports(expected,reports){
 assert.equal(expected?.kind,'publication-unchanged-baseline-v1');assert.equal(expected.status,'REUSED_BASELINE');
 assert.equal(reports.length,4);const seen=new Set();
 for(const report of reports){const i=report.shard_index;assert(Number.isInteger(i)&&i>=0&&i<4&&!seen.has(i));seen.add(i);
  assert.deepEqual(report,{...expected,shard_index:i,suites:expected.suites.filter((_,j)=>j%4===i),executed_suites:[],fresh_pass:false});
 }
 return {status:'REUSED_BASELINE',executed_suites:[],fresh_pass:false};
}

/** The authenticated baseline is Pages production, not the asset caller's root runtime. */
export const publicationRuntimeCompatible=runtime=>runtime?.site_base==='/lowpoly-vault/'&&runtime?.site_origin==='https://s010s.github.io'&&runtime?.node_major==='22'&&runtime?.platform==='linux'&&runtime?.arch==='x64';
