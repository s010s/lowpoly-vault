/** Immutable historical golden approvals are not re-signed as new capture proof.
 * This narrow migration proves the complete pre-hook program and renderer closure
 * still have their old bytes. New orchestration remains a protected v3 control plane.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
// Exact existing182 approvals, independently compared with the pre-change HEAD.
export const HISTORICAL_APPROVALS_SHA256='3972f0c061496e5ea0cf295a0dabf76a0e8747c0a90d38a963fc17b623b8948f';
export async function assertHistoricalPosterApprovals({root,baseline}){
 let bytes;try{bytes=await readFile(resolve(root,'site/gallery/approved-poster-inputs.json'));}catch(error){if(error.code==='ENOENT'){assert.equal(baseline,null);return null;}throw error;}
 assert.equal(hash(bytes),HISTORICAL_APPROVALS_SHA256,'Historical approval catalog bytes changed; repository JSON cannot grant reviewed status');
 assert.deepEqual(JSON.parse(bytes),baseline,'Historical approval catalog parse differs');
 assert.equal(Object.keys(baseline.posters).length,182);return baseline;
}
const HOOK_COUNTS={'site/capture-gallery-posters.mjs':4,'site/gallery-poster-inputs.mjs':4};
const BEGIN='// BEGIN GALLERY POSTER V3 ORCHESTRATION\n',END='// END GALLERY POSTER V3 ORCHESTRATION\n';
export function historicalPosterSource(source,path){
 const expected=HOOK_COUNTS[path];assert(expected,'Unsupported historical recipe file');
 const pattern=/\/\/ BEGIN GALLERY POSTER V3 ORCHESTRATION\n[\s\S]*?\/\/ END GALLERY POSTER V3 ORCHESTRATION\n/g;
 const matches=source.match(pattern)||[];assert.equal(matches.length,expected,`Historical orchestration hook count differs: ${path}`);
 const original=source.replace(pattern,'');assert(!original.includes(BEGIN)&&!original.includes(END),'Malformed compatibility hook');return original;
}
export async function assertHistoricalPosterRecipe({root,baseline,shared}){
 const historical=baseline?.shared;assert.equal(historical?.version,2,'Only immutable v2 historical golden approvals have a compatibility boundary');
 assert.equal(historical.sha256,hash(JSON.stringify({policy:historical.policy,files:historical.files,browser:historical.browser})),'Historical recipe seal differs');
 assert.deepEqual(shared.policy,historical.policy,'Historical capture policy changed');assert.equal(shared.browser,historical.browser,'Historical browser changed');
 assert.deepEqual(shared.files.map(row=>row[0]),historical.files.map(row=>row[0]),'Historical renderer dependency closure changed');
 for(const [path,expected]of historical.files){
  const actual=HOOK_COUNTS[path]?hash(historicalPosterSource(await readFile(resolve(root,path),'utf8'),path)):shared.files.find(row=>row[0]===path)?.[1];
  assert.equal(actual,expected,`Historical actual renderer/harness input changed: ${path}; explicit visual review required`);
 }
 return historical;
}

/** Registry canonicalization changes JSON key order, not pixels. Reconstruct only
 * the two original seal layouts and original poster schema. The entire original
 * approval hash must match; no new hash or visual approval is manufactured.
 * Used solely for the authenticated successor inverse, not ordinary captures.
 */
export function restoreHistoricalPosterSerialization(resources,baseline){
 const result=structuredClone(resources);
 const ordered=(value,keys)=>{assert(value&&typeof value==='object'&&!Array.isArray(value));assert.deepEqual(Object.keys(value).sort(),keys.slice().sort(),'Historical poster serialization schema changed');return Object.fromEntries(keys.map(key=>[key,value[key]]));};
 for(const [id,approval] of Object.entries(baseline?.posters||{})){
  const source=result.posters[id];assert(source,`Missing historical approved poster: ${id}`);
  const poster=ordered(source,['source_glb_sha256','wheelSpec','detail','wheel']);
  poster.wheelSpec=ordered(poster.wheelSpec,['azimuth','elevation','zoom','offset','projectedBounds','aspect','floorCenter','floorPoints']);
  poster.wheelSpec.projectedBounds=ordered(poster.wheelSpec.projectedBounds,['left','right','top','bottom']);
  const files=result.files.filter(file=>[poster.detail,poster.wheel].includes(file.path)).sort((a,b)=>a.path.localeCompare(b.path));
  assert.equal(files.length,2,`Missing/duplicate historical poster seals: ${id}`);
  let restored;
  for(const first of [['path','sha256','bytes'],['path','bytes','sha256']])for(const second of [['path','sha256','bytes'],['path','bytes','sha256']]){
   const seals=[ordered(files[0],first),ordered(files[1],second)];
   if(hash(JSON.stringify({poster,seals}))===approval.poster_sha256)restored=seals;
  }
  assert(restored,`Approved poster pixels or metadata changed: ${id}; historical serialization cannot restore approval`);
  result.posters[id]=poster;
  for(const seal of restored){const index=result.files.findIndex(file=>file.path===seal.path);result.files[index]=seal;}
 }
 return result;
}
