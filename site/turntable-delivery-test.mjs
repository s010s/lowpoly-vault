import assert from 'node:assert/strict';
import { readFile, writeFile, mkdtemp, mkdir, cp, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { collectTurntables, webpDimensions } from './turntable-delivery.mjs';
const root=process.cwd(),manifest=JSON.parse(await readFile('assets/manifest.json'));const hash=b=>createHash('sha256').update(b).digest('hex');
const initial=await collectTurntables(manifest);assert.equal(initial.descriptors.size,3);assert.equal(initial.files.length,85);let checks=1;
const temp=await mkdtemp(resolve(tmpdir(),'vault-turntables-'));
try{
 await mkdir(resolve(temp,'assets'),{recursive:true});await cp(resolve(root,'assets/turntables'),resolve(temp,'assets/turntables'),{recursive:true});await cp(resolve(root,'assets/card-previews'),resolve(temp,'assets/card-previews'),{recursive:true});
 const indexPath=resolve(temp,'assets/turntables/index.json'),indexBytes=await readFile(indexPath),index=JSON.parse(indexBytes),first=index.assets[0],dataPath=resolve(temp,first.manifest),dataBytes=await readFile(dataPath),data=JSON.parse(dataBytes),framePath=resolve(temp,data.frames[0].path),frameBytes=await readFile(framePath);
 assert.deepEqual(webpDimensions(frameBytes),[data.width,data.height]);assert.throws(()=>webpDimensions(Buffer.from('not webp')));checks+=2;
 async function invalidIndex(mutate){const changed=structuredClone(index);mutate(changed);await writeFile(indexPath,JSON.stringify(changed));await assert.rejects(collectTurntables(manifest,temp));await writeFile(indexPath,indexBytes);checks++;}
 await invalidIndex(i=>i.assets[0].id='unpublished-candidate');await invalidIndex(i=>i.assets.push(i.assets[0]));await invalidIndex(i=>i.assets[0].manifest='../escape.json');await invalidIndex(i=>i.assets[0].source_glb_sha256='b'.repeat(64));await invalidIndex(i=>i.assets[0].manifest_sha256='b'.repeat(64));
 async function invalidManifest(mutate){const changed=structuredClone(data);mutate(changed);const bytes=Buffer.from(JSON.stringify(changed));await writeFile(dataPath,bytes);const next=structuredClone(index);next.assets[0].manifest_sha256=hash(bytes);await writeFile(indexPath,JSON.stringify(next));await assert.rejects(collectTurntables(manifest,temp));await writeFile(dataPath,dataBytes);await writeFile(indexPath,indexBytes);checks++;}
 await invalidManifest(d=>d.total_bytes++);await invalidManifest(d=>d.frames[0].path='assets/turntables/natural-arch/../outside.webp');await invalidManifest(d=>d.width=511);await invalidManifest(d=>d.frames[0].sha256='b'.repeat(64));
 await writeFile(framePath,Buffer.from('corrupt'));await assert.rejects(collectTurntables(manifest,temp));await writeFile(framePath,frameBytes);checks++;
 const outside=resolve(temp,'outside.webp');await writeFile(outside,frameBytes);await rm(framePath);await symlink(outside,framePath);await assert.rejects(collectTurntables(manifest,temp));checks++;
 assert.equal((await collectTurntables(manifest,await mkdtemp(resolve(temp,'empty-')))).descriptors.size,0);checks++;
}finally{await rm(temp,{recursive:true,force:true});}
console.log(JSON.stringify({status:'pass',checks,assets:initial.descriptors.size,frames:initial.files.length-initial.descriptors.size-initial.posters.size,source:'immutable original GLB hashes',coverage:'sealed metadata/bytes/dimensions/path allowlist/symlink rejection/static-only fallback'}));
