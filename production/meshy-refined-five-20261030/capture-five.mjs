/** Exact-five, read-only source capture wrapper. This produces unreviewed pixels,
 * not model acceptance, integration authority, a merge, or a deployment. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,realpath,stat,cp,rm} from 'node:fs/promises';
import {resolve,dirname,join,sep} from 'node:path';
import {tmpdir} from 'node:os';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';

export const EXPECTED = Object.freeze({
 gomphotherium:'98adc0276da06ca3883eb13d8274974609d30779c8cb5d13225a4467eb8e8616',
 paraceratherium:'9febf81df9730fda570a60f7ac7b5c293b818bee0b6bae7591b5db530ff669c2',
 uintatherium:'3a26fdaadc463c2053457df0d1a00cac8231e339e32602e1610b591b8a35ea94',
 thylacosmilus:'759b44b25a20d6e46c5dad067e4d6d8ecb58dfcd20cd78663d2ba6495c3fcc86',
 smilodon:'22fa65c2b4a37f8602794746d51e790ab1c74396c91f01a97dccd86e00411b26',
});
const ids=Object.keys(EXPECTED), hash=b=>createHash('sha256').update(b).digest('hex');
const safe=p=>typeof p==='string'&&p&&!p.startsWith('/')&&!/[\\\u0000-\u001f?#%:]/.test(p)&&p.split('/').every(x=>x&&x!=='.'&&x!=='..');
const codePins={
 'site/capture-model-images.mjs':'7eaf2ab9c7fabb04ff792f2eb12e11f3b45b355ada75eb37f0a4050308e0b6f9',
 'site/ci-build-simple.mjs':'99b9bbb1bb230349f25a7c31539bd468c82f17e9293940bffcbdfe626cdebd8d',
 'site/unified-delivery-contract.mjs':'a689294483614e860cf30c8056b881409332c00c410685499f78af0075520a31',
};

export function parseArgs(args){
 const allowed=new Set(['--repo','--manifest','--manifest-sha256','--expected-commit','--out']);
 assert.equal(args.length,10,'Required: --repo PATH --manifest PATH --manifest-sha256 SHA256 --expected-commit SHA40 --out NEW_DIRECTORY');
 const o={};for(let i=0;i<args.length;i+=2){assert(allowed.has(args[i])&&!Object.hasOwn(o,args[i]),'Unknown or repeated option');assert(args[i+1]&&!args[i+1].startsWith('--'),'Missing value');o[args[i]]=args[i+1];}
 assert(/^[a-f0-9]{64}$/.test(o['--manifest-sha256']),'Exact manifest SHA-256 required');
 assert(/^[a-f0-9]{40}$/.test(o['--expected-commit']),'Exact checkout commit required');return o;
}

function glbStructure(bytes){
 assert(bytes.length>=20&&bytes.readUInt32LE(0)===0x46546c67&&bytes.readUInt32LE(4)===2&&bytes.readUInt32LE(8)===bytes.length,'Invalid GLB header');
 const n=bytes.readUInt32LE(12);assert(bytes.readUInt32LE(16)===0x4e4f534a&&20+n<=bytes.length,'Missing GLB JSON chunk');
 const g=JSON.parse(bytes.subarray(20,20+n).toString('utf8').trim());
 assert(!(g.buffers||[]).some(x=>x.uri)&&!(g.images||[]).some(x=>x.uri),'Capture requires self-contained embedded GLB resources');
 return {meshes:g.meshes?.length||0,materials:g.materials?.length||0,images:g.images?.length||0};
}

export async function captureFive(o){
 const repo=await realpath(resolve(o['--repo'])),expectedCommit=o['--expected-commit'];
 const actualCommit=execFileSync('git',['-C',repo,'rev-parse','HEAD'],{encoding:'utf8'}).trim();assert.equal(actualCommit,expectedCommit,'Checkout commit differs from handoff');
 const tree=execFileSync('git',['-C',repo,'rev-parse','HEAD^{tree}'],{encoding:'utf8'}).trim();
 execFileSync('git',['-C',repo,'diff','--exit-code','HEAD','--','site','package.json','package-lock.json','vite.config.js'],{stdio:'pipe'});
 for(const [p,pin]of Object.entries(codePins))assert.equal(hash(await readFile(resolve(repo,p))),pin,'Pinned capture/build implementation changed: '+p);
 const input=await readFile(resolve(o['--manifest']));assert.equal(hash(input),o['--manifest-sha256'],'Capture manifest differs from handoff');
 const manifest=JSON.parse(input);assert(Array.isArray(manifest.assets)&&manifest.assets.length===ids.length,'Exactly five candidate rows required');
 assert.deepEqual([...manifest.assets.map(x=>x.id)].sort(),[...ids].sort(),'Candidate IDs differ');
 const selected=ids.map(id=>manifest.assets.find(a=>a.id===id)),sourceBytes=[],inputs=[];
 for(const a of selected){
  assert.equal(a.sha256?.glb,EXPECTED[a.id],'Wrong frozen candidate hash: '+a.id);
  assert(safe(a.glb)&&a.glb===`assets/revisions/meshy-refined-five-20261030/${a.id}/model.glb`,'Unexpected immutable GLB path: '+a.id);
  assert(Array.isArray(a.dimensions)&&a.dimensions.length===3&&a.dimensions.every(n=>Number.isFinite(n)&&n>0),'Measured positive dimensions required: '+a.id);
  const full=resolve(repo,a.glb);assert(full.startsWith(repo+sep)&&await realpath(full)===full,'Symlink/outside source rejected');assert((await stat(full)).isFile());
  const bytes=await readFile(full);assert.equal(hash(bytes),EXPECTED[a.id],'Actual GLB bytes differ: '+a.id);
  inputs.push({id:a.id,glb:a.glb,sha256:hash(bytes),bytes:bytes.length,dimensions:a.dimensions,glb_structure:glbStructure(bytes)});sourceBytes.push(bytes);
 }
 const out=resolve(o['--out']);assert(out!==repo&&!out.startsWith(repo+sep),'Keep capture output outside source checkout');
 await mkdir(out,{recursive:false}); // Never overwrite an existing run.
 const temp=await mkdtemp(join(tmpdir(),'lowpoly-exact-five-'));
 const record={status:'RUNNING',source_commit:actualCommit,source_tree:tree,input_manifest_sha256:hash(input),inputs,visual_review:'NOT_REVIEWED',model_qa:'NOT_REPEATED',published:false,outputs:[],errors:[]};
 try{
  await mkdir(resolve(temp,'assets'),{recursive:true});await writeFile(resolve(temp,'assets/manifest.json'),JSON.stringify({...manifest,assets:selected},null,2)+'\n');
  for(let i=0;i<selected.length;i++){const to=resolve(temp,selected[i].glb);await mkdir(dirname(to),{recursive:true});await writeFile(to,sourceBytes[i]);}
  // The imported module keeps codeRoot at the pinned checkout. Only selected
  // GLBs and the temporary manifest come from temp; renderer JS / Three.js
  // continue to resolve from repo and repo/node_modules, not temp/site.
  const {captureModelImages}=await import(pathToFileURL(resolve(repo,'site/capture-model-images.mjs')).href);
  const captured=await captureModelImages({root:temp,ids});assert.equal(captured.status,'CAPTURED_NOT_REVIEWED');assert.deepEqual(captured.errors,[]);
  for(const id of ids)for(const role of ['wheel','detail']){
   const relative=`images/${id}/${role}.png`,from=resolve(temp,'qa/model-image-capture',id,role+'.png'),bytes=await readFile(from);
   assert(bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])),'Invalid captured PNG');
   const width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);assert.deepEqual([width,height],role==='wheel'?[768,432]:[1536,1536],'Unexpected capture resolution');
   await mkdir(dirname(resolve(out,relative)),{recursive:true});await writeFile(resolve(out,relative),bytes);
   record.outputs.push({id,role,path:relative,sha256:hash(bytes),bytes:bytes.length,width,height,source_glb_sha256:EXPECTED[id]});
  }
  for(const a of selected)assert.equal(hash(await readFile(resolve(repo,a.glb))),EXPECTED[a.id],'Source changed during capture');
  await cp(resolve(temp,'qa/model-image-capture/report.json'),resolve(out,'renderer-report.json'));
  record.status='CAPTURED_NOT_REVIEWED';record.browser=captured.browser;record.runtime_scope='Pinned PreviewRenderer wheel and DetailRenderer 1536 capture in Chromium/SwiftShader; not physical-device, animation or broad interaction QA.';
  await rm(temp,{recursive:true,force:true});
 }catch(error){
  record.status='FAILED';record.errors.push(error.message);record.recovery_note='This run failed; no visual approval or publication claim. Temporary capture inputs were retained for diagnosis.';
  try{await cp(resolve(temp,'qa/model-image-capture/report.json'),resolve(out,'renderer-report.json'));}catch{}
  throw error;
 }finally{await writeFile(resolve(out,'capture-identity.json'),JSON.stringify(record,null,2)+'\n');}
 return record;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 const result=await captureFive(parseArgs(process.argv.slice(2)));console.log(JSON.stringify(result,null,2));
}
