/** Exact one-time authorized v2 migration; not a generic all-catalog switch. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {posterInputKey} from './gallery-poster-inputs.mjs';
export const DETAIL_V2_SCOPE_SHA256='a9903a78cbb5750e07c44a1ab2c1b5d0c4304f52935ab738ff78825d5cfe1778';
export const DETAIL_V2_SCOPE_KIND='authorized-right264-hires-v2';
export function assertDetailV2Migration({scopeBytes,assets,ids,presentation,smoke=false}){
 assert(!smoke,'Migration cannot be candidate smoke');
 assert.deepEqual(presentation,{revision:2,minimum_margin:.025,screen_shift:.06,raster_size:1536},'Only reviewed 1536 policy can migrate');
 assert.equal(createHash('sha256').update(scopeBytes).digest('hex'),DETAIL_V2_SCOPE_SHA256,'Immutable authorized cohorts changed');
 const scope=JSON.parse(scopeBytes);assert.deepEqual(scope.cohorts.map(c=>[c.id,c.count]),[['original-right250',250],['pr72-replacement14',14]]);
 const pins=scope.cohorts.flatMap(c=>c.assets);assert.equal(pins.length,264);assert.equal(new Set(pins.map(p=>p.id)).size,264);
 assert(Array.isArray(ids)&&ids.length===264&&new Set(ids).size===264,'Explicit exact264 IDs required');
 assert.deepEqual([...ids].sort(),pins.map(p=>p.id).sort());assert.deepEqual(assets.map(a=>a.id).sort(),[...ids].sort(),'Affected asset routes changed');
 for(const p of pins){const a=assets.find(a=>a.id===p.id);assert.equal(a.sha256.glb,p.source_glb_sha256,'Migration GLB changed '+p.id);assert.equal(posterInputKey(a,{sha256:'detail-scope-source-only-v1'}),p.asset_input_sha256,'Migration metadata changed '+p.id);}
 return {kind:DETAIL_V2_SCOPE_KIND,sha256:DETAIL_V2_SCOPE_SHA256,ids:[...ids].sort()};
}
