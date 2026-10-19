/** Unchecked or incomplete scene inputs must fail before any browser can render. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,readFile,writeFile,cp,rm} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,join,dirname} from 'node:path';
import {spawnSync} from 'node:child_process';
const manifest=JSON.parse(await readFile('assets/manifest.json')),pack='prehistoric-small-life-round13-20261018',assets=manifest.assets.filter(a=>a.packs.includes(pack));assert.equal(assets.length,12);
const scratch=await mkdtemp(join(tmpdir(),'lpv-scene-input-')),output=join(scratch,'evidence'),probe=resolve('site/ci-scene-browser-test.mjs');
try{
 await mkdir(join(scratch,'assets'),{recursive:true});const file=join(scratch,'assets/manifest.json');await writeFile(file,JSON.stringify({assets}));for(const a of assets){await mkdir(dirname(join(scratch,a.glb)),{recursive:true});await cp(a.glb,join(scratch,a.glb));}
 const run=()=>spawnSync(process.execPath,[probe],{encoding:'utf8',timeout:10000,env:{...process.env,GALLERY_DIR:scratch,QA_ADDITION_PACK:pack,QA_OUTPUT_DIR:output}}),target=join(scratch,assets[0].glb),bytes=await readFile(target);
 await writeFile(target,Buffer.concat([bytes,Buffer.from('tamper')]));let result=run();assert.notEqual(result.status,0);assert.match(result.stderr,/scene input differs from checked publication/);assert(!existsSync(join(output,'functional-scene/scene.png')));
 await writeFile(target,bytes);await rm(target);result=run();assert.notEqual(result.status,0);assert.match(result.stderr,/ENOENT/);assert(!existsSync(join(output,'functional-scene/scene.png')));
 await writeFile(target,bytes);await writeFile(file,JSON.stringify({assets:assets.slice(1)}));result=run();assert.notEqual(result.status,0);assert.match(result.stderr,/Exact twelve-model publication scene required/);assert(!existsSync(join(output,'functional-scene/scene.png')));
 console.log('Scene input gate: corrupted bytes, missing GLB and incomplete cohort refused before rendering.');
}finally{await rm(scratch,{recursive:true,force:true});}
