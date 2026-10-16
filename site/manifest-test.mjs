// Synthetic metadata/header fixtures only; never used by the gallery or published.
import { mkdtemp,mkdir,writeFile,readFile,rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';
import { collectManifest } from './generate-manifest.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-manifest-test-'));
try{
 const folder=join(root,'assets/prehistoric/geology/test-only');await mkdir(folder,{recursive:true});
 const base='assets/prehistoric/geology/test-only';
 const metadata={id:'test-only',name:{en:'Test fixture',zh:'测试夹具'},description:{en:'Not an asset',zh:'非真实资产'},category:'geology',collection:'prehistoric',license:'CC-BY-4.0',triangles:1,dimensions:[1,1,1],glb:`${base}/test-only.glb`,blend:`${base}/test-only.blend`,preview:`${base}/preview-hero.png`,scientific_notes:{en:'Preserved unchanged'}};
 const glb=Buffer.alloc(12);glb.write('glTF');glb.writeUInt32LE(2,4);glb.writeUInt32LE(12,8);await writeFile(join(folder,'test-only.glb'),glb);await writeFile(join(folder,'test-only.blend'),'TEST ONLY');await writeFile(join(folder,'preview-hero.png'),'TEST ONLY');await writeFile(join(folder,'metadata.json'),JSON.stringify(metadata));
 const qa={source:{status:'pass'},glb:{status:'pass'},khronos_validator:{status:'not_run'},threejs_runtime:{status:'not_run'},visual_review:{status:'pending'}};await writeFile(join(folder,'qa.json'),JSON.stringify(qa));
 await assert.rejects(()=>collectManifest(root),/khronos_validator QA is not_run/);const preview=await collectManifest(root,{preview:true});assert(preview.review_only);assert.equal(preview.assets[0].scientific_notes.en,'Preserved unchanged');
 for(const stage of Object.keys(qa))qa[stage].status='pass';await writeFile(join(folder,'qa.json'),JSON.stringify(qa));const release=await collectManifest(root);assert.equal(release.assets.length,1);assert.equal(release.review_only,undefined);
 qa.source={status:'pass_with_warnings',warnings:['Test warning']};await writeFile(join(folder,'qa.json'),JSON.stringify(qa));await assert.rejects(()=>collectManifest(root),/warnings need explicit review/);qa.reviewed_warnings=['Test warning reviewed'];await writeFile(join(folder,'qa.json'),JSON.stringify(qa));assert.equal((await collectManifest(root)).assets.length,1);
 await rm(join(folder,'preview-hero.png'));await assert.rejects(()=>collectManifest(root,{preview:true}),/ENOENT/);
 console.log('Manifest tests passed: review/release separation, mandatory QA, missing files, warnings, preserved science metadata.');
}finally{await rm(root,{recursive:true,force:true});}
