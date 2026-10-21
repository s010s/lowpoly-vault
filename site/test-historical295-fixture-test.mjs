/** Bounded history projection regressions run inside mandatory final-five suite. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {historical295Fixture} from './test-historical295-fixture.mjs';
import {FINAL_FIVE_IDS} from './final-five-release.mjs';
const current=JSON.parse(readFileSync('assets/manifest.json')),bytes=JSON.stringify(current);
const projected=historical295Fixture(current);assert.equal(projected.assets.length,295);assert.equal(JSON.stringify(current),bytes);
const prior=structuredClone(current);prior.assets=prior.assets.filter(a=>!FINAL_FIVE_IDS.includes(a.id));delete prior.publication.final_five_presentation;
assert.deepEqual(historical295Fixture(prior),projected);
let rejected=0;
for(const [label,change] of [
 ['unknown extra',m=>m.assets.push({...m.assets.at(-1),id:'unreviewed-extra'})],
 ['unknown replacement',m=>m.assets.at(-1).id='unreviewed-extra'],
 ['duplicate new ID',m=>m.assets.at(-1).id=m.assets.at(-2).id],
 ['new content changed',m=>m.assets.at(-1).description.en+=' altered'],
 ['new objects reordered',m=>m.assets.reverse()],
 ['missing fixed new model',m=>m.assets.pop()],
 ['old content changed',m=>m.assets[0].description.en+=' altered'],
 ['old objects reordered',m=>[m.assets[0],m.assets[1]]=[m.assets[1],m.assets[0]]],
 ['forged presentation',m=>m.publication.final_five_presentation.sha256='0'.repeat(64)],
 ['missing presentation',m=>delete m.publication.final_five_presentation],
 ['extra header',m=>m.publication.unreviewed=true],
 ['self reported digest',m=>{m.assets[0].description.en+=' altered';m.publication.baseline347_sha256='7c86e7087dd1b1dd1e207bce67fc5b9dec3e5cf80bb433d762c70a1c48b2e463';}]
]){const bad=structuredClone(current);change(bad);assert.throws(()=>historical295Fixture(bad),undefined,label);rejected++;}
const oldBad=structuredClone(prior);oldBad.assets[0].description.en+=' altered';assert.throws(()=>historical295Fixture(oldBad));rejected++;
console.log(`PASS historical295 fixture: exact352 and exact347 restore identical fixed295; input unchanged; ${rejected} rejections.`);
