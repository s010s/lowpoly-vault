/** Actual recipe differential and rejection tests. Fixtures are not approval evidence. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {resolve,dirname,join} from 'node:path';
import {tmpdir} from 'node:os';
import {posterSharedInputs} from './gallery-poster-inputs.mjs';
import {MAIN842_POSTER_RECIPE} from './gallery-main842-compat.mjs';
import {assertRecordedGalleryRecipe} from './gallery-publication-recipe-compat.mjs';
const root=resolve(process.env.GALLERY_RECIPE_SOURCE_ROOT||'.');
const current=await posterSharedInputs(root);
let tests=0;
const pass=label=>{tests++;console.log('PASS',label);};
assert.deepEqual(await assertRecordedGalleryRecipe(current,root),current);pass('exact current recipe remains accepted');
assert.deepEqual(await assertRecordedGalleryRecipe(MAIN842_POSTER_RECIPE,root),MAIN842_POSTER_RECIPE);pass('exact main842 recipe accepted only after complete byte proof');
for(const [label,change]of [
 ['recipe digest',x=>x.sha256='0'.repeat(64)],
 ['recipe version',x=>x.version=2],
 ['recorded dependency',x=>x.files[0][1]='0'.repeat(64)],
 ['recorded extra dependency',x=>x.files.push(['unreviewed.js','0'.repeat(64)])],
 ['recorded policy',x=>x.policy.detail=[1,1]],
 ['recorded browser',x=>x.browser='unreviewed']
]){
 const altered=structuredClone(MAIN842_POSTER_RECIPE);change(altered);
 await assert.rejects(assertRecordedGalleryRecipe(altered,root));pass('reject '+label);
}
const fixture=await mkdtemp(join(process.env.GALLERY_RECIPE_TEST_TMP||tmpdir(),'gallery-recipe-r004-'));
try{
 const files=[...current.files.map(x=>x[0]),'node_modules/playwright-core/browsers.json'];
 for(const file of files){const p=resolve(fixture,file);await mkdir(dirname(p),{recursive:true});await writeFile(p,await readFile(resolve(root,file)));}
 for(const file of files){
  const p=resolve(fixture,file),bytes=await readFile(p);
  try{
   if(file.endsWith('browsers.json')){const j=JSON.parse(bytes);j.browsers.find(x=>x.name==='chromium').browserVersion='unreviewed';await writeFile(p,JSON.stringify(j));}
   else await writeFile(p,Buffer.concat([bytes,Buffer.from('\n/* changed actual input */\n')]));
   await assert.rejects(assertRecordedGalleryRecipe(MAIN842_POSTER_RECIPE,fixture));pass('reject changed actual input '+file);
  }finally{await writeFile(p,bytes);}
 }
 const renderer=resolve(fixture,'site/gallery/renderer.js'),bytes=await readFile(renderer);
 await writeFile(resolve(fixture,'site/gallery/extra-unreviewed.js'),'export const unreviewed=true;\n');
 try{await writeFile(renderer,Buffer.concat([Buffer.from("import './extra-unreviewed.js';\n"),bytes]));await assert.rejects(assertRecordedGalleryRecipe(MAIN842_POSTER_RECIPE,fixture));pass('reject new actual renderer dependency');}finally{await writeFile(renderer,bytes);}
}finally{await rm(fixture,{recursive:true,force:true});}
console.log(`PASS publication recipe compatibility: ${tests} checks; no approval or stale-state changes.`);
