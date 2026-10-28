/** Tiny integration fixtures, not model QA or publication acceptance. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {test} from 'node:test';
import {createHash} from 'node:crypto';
import {checkDelivery} from './unified-delivery-contract.mjs';
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
async function fixture(){const root=await mkdtemp(join(tmpdir(),'unified-delivery-'));const write=async(path,bytes)=>{await mkdir(dirname(join(root,path)),{recursive:true});await writeFile(join(root,path),bytes);return sha(bytes);};const glb=await write('assets/toy/toy.glb','fixture GLB bytes'),blend=await write('assets/toy/toy.blend','fixture Blender bytes');const left=await write('site/public/gallery/posters/toy-wheel.png','left fixture'),right=await write('site/public/gallery/posters/toy.png','right fixture');return {root,write,manifest:{assets:[{id:'toy',glb:'assets/toy/toy.glb',blend:'assets/toy/toy.blend',sha256:{glb,blend}}]},resources:{posters:{toy:{source_glb_sha256:glb,wheel:'gallery/posters/toy-wheel.png',detail:'gallery/posters/toy.png'}},files:[{path:'gallery/posters/toy-wheel.png',sha256:left},{path:'gallery/posters/toy.png',sha256:right}]},wheelIndex:{},detailIndex:{},cleanup:()=>rm(root,{recursive:true,force:true})};}
const check=(name,run)=>test(name,async()=>{const f=await fixture();try{await run(f);}finally{await f.cleanup();}});
check('existing manifest/resources resolve four actual paths without new schema',async f=>{const r=await checkDelivery(f);assert.equal(r.count,1);assert.equal(r.hash_checked,false);assert.equal(r.models[0].files.left.path,'site/public/gallery/posters/toy-wheel.png');});
check('default deliberately does not repeat handoff hashes or model QA',async f=>{await f.write('assets/toy/toy.glb','different nonempty bytes');assert.equal((await checkDelivery(f)).count,1);});
check('explicit one-time handoff hashes verify existing pins',async f=>{assert.equal((await checkDelivery({...f,hash:true})).hash_checked,true);await f.write('assets/toy/toy.glb','different bytes');await assert.rejects(checkDelivery({...f,hash:true}),/Handoff hash differs/);});
check('stale override retains actual renderer legacy fallback',async f=>{f.detailIndex={version:1,kind:'detail-only-presentations',presentations:{toy:{detail:'made-up.png'}}};const r=await checkDelivery(f);assert.equal(r.models[0].files.right.path,'site/public/gallery/posters/toy.png');});
for(const [name,mutate]of Object.entries({
 'duplicate ID':f=>f.manifest.assets.push(structuredClone(f.manifest.assets[0])),
 'missing Blend path':f=>{delete f.manifest.assets[0].blend;},
 'missing physical file':f=>rm(join(f.root,'assets/toy/toy.blend')),
 'empty left image':f=>f.write('site/public/gallery/posters/toy-wheel.png',''),
 'missing poster ID':f=>{delete f.resources.posters.toy;},
 'mismatched resource source identity':f=>{f.resources.posters.toy.source_glb_sha256='0'.repeat(64);},
 'traversal':f=>{f.manifest.assets[0].glb='../outside.glb';},
 'absolute path':f=>{f.manifest.assets[0].glb='/tmp/toy.glb';},
 'different model image path':f=>{f.resources.posters.toy.detail='gallery/posters/another.png';},
 'different model source path':f=>{f.manifest.assets[0].glb='assets/another/another.glb';},
 'wrong source extension':f=>{f.manifest.assets[0].blend='assets/toy/toy.glb';},
 'symlink file':async f=>{await rm(join(f.root,'site/public/gallery/posters/toy-wheel.png'));await symlink('toy.png',join(f.root,'site/public/gallery/posters/toy-wheel.png'));},
}))check(`reject ${name}`,async f=>{await mutate(f);await assert.rejects(checkDelivery(f));});
