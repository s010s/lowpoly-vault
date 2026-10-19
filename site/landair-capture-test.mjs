/** Candidate capture must not relax or mutate the publication contract. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,join,dirname} from 'node:path';
import {prepareLandairCapture} from './prepare-landair-capture.mjs';
import {LANDAIR_CAPTURE as fixed} from './accepted-landair-capture.mjs';
const scratch=await mkdtemp(join(tmpdir(),'lpv-candidate-capture-')),path='qa/landair-release-20261019/capture-inputs.json',published=await readFile('assets/manifest.json');
try{
 await mkdir(dirname(resolve(scratch,path)),{recursive:true});
 for(const change of [d=>d.publication_authority=true,d=>d.assets.pop(),d=>d.assets.push(d.assets[0]),d=>d.assets[0].glb.path='../escape',d=>d.assets[0].glb.sha256='0'.repeat(64),d=>d.review.sha256='0'.repeat(64),d=>d.delivery_review.sha256='0'.repeat(64)]){
  const d=structuredClone(fixed);change(d);await writeFile(resolve(scratch,path),JSON.stringify(d));await assert.rejects(()=>prepareLandairCapture({root:scratch,outDir:resolve(scratch,'capture')}));
 }
 assert.deepEqual(await readFile('assets/manifest.json'),published);
 console.log('Candidate capture: altered authority, scope, duplicate IDs, unsafe path and changed source/review pins rejected; publication unchanged.');
}finally{await rm(scratch,{recursive:true,force:true});}
