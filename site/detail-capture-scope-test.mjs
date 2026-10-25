import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {assertDetailV2Migration,DETAIL_V2_SCOPE_KIND} from './detail-capture-scope.mjs';
const scopeBytes=await readFile('qa/detail-presentation-scope-20261025.json'),scope=JSON.parse(scopeBytes),ids=scope.cohorts.flatMap(c=>c.assets.map(a=>a.id)),all=JSON.parse(await readFile('assets/manifest.json')).assets,assets=all.filter(a=>ids.includes(a.id));
const input={scopeBytes,assets,ids,presentation:{revision:2,minimum_margin:.025,screen_shift:.06,raster_size:1536}};
test('exact authorized two cohorts admit only fixed1536 migration',()=>{const r=assertDetailV2Migration(input);assert.equal(r.kind,DETAIL_V2_SCOPE_KIND);assert.equal(r.ids.length,264);assert.deepEqual(r.ids,[...ids].sort());});
for(const [name,mutate] of [
 ['missingID',x=>x.ids.pop()],['duplicateID',x=>x.ids[0]=x.ids[1]],['ordinaryID',x=>x.ids[0]='natural-arch'],
 ['differentGLB',x=>x.assets[0].sha256.glb='0'.repeat(64)],['differentmetadata',x=>x.assets[0].name.en+=' changed'],
 ['2048',x=>x.presentation.raster_size=2048],['margin',x=>x.presentation.minimum_margin=0],['shift',x=>x.presentation.screen_shift=0],
 ['smoke',x=>x.smoke=true],['extraaffected',x=>x.assets.push({...x.assets[0],id:'extra'})]
])test('reject '+name,()=>{const x=structuredClone(input);x.scopeBytes=scopeBytes;mutate(x);assert.throws(()=>assertDetailV2Migration(x));});
test('reject rewritten historical scope bytes',()=>assert.throws(()=>assertDetailV2Migration({...input,scopeBytes:Buffer.concat([scopeBytes,Buffer.from(' ')] )})));
