import assert from 'node:assert/strict';
import {readFile,mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';import {join,dirname} from 'node:path';
import {auditDetailPresentations} from './detail-presentations-audit.mjs';
const manifest=JSON.parse(await readFile('assets/manifest.json'));
const result=await auditDetailPresentations(manifest);assert(result.count>0);assert.equal(result.files.length,new Set(result.files).size);
const temp=await mkdtemp(join(tmpdir(),'detail-delivery-'));try{
 const first=result.files[0];await mkdir(dirname(join(temp,first)),{recursive:true});await writeFile(join(temp,first),'not the sealed PNG');
 await assert.rejects(auditDetailPresentations(manifest,{outputRoot:temp}),/Delivered right PNG differs/);
}finally{await rm(temp,{recursive:true,force:true});}
console.log(`PASS offline exact ${result.count} right delivery inventory and corrupted output rejection; no proof network required`);
