/** Poster-capture evidence is independent from strict-GPU/model acceptance. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,writeFile,mkdir,realpath,rm} from 'node:fs/promises';
import {resolve,dirname,sep} from 'node:path';
import {execFileSync} from 'node:child_process';
import {CAPTURE_POLICY,posterInputKey} from './gallery-poster-inputs.mjs';
import {modelPolicyDigest} from './ci-model-proof.mjs';
import {prepareModelSource} from './ci-model-cache.mjs';
import {immutableGitEnv} from './ci-git.mjs';
import {readVerifiedPosterBundle} from './gallery-poster-cache.mjs';

export const POSTER_PROOF_FILE='gallery-poster-proof.json';
export const posterArtifactName=attempt=>`gallery-poster-proof-v1-${attempt}`;
export const posterHash=bytes=>createHash('sha256').update(bytes).digest('hex');
const canonical=value=>value&&typeof value==='object'?(Array.isArray(value)?value.map(canonical):Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])]))):value;
export const posterObjectHash=value=>posterHash(JSON.stringify(canonical(value)));
const HASH=/^[a-f0-9]{64}$/,SHA=/^[a-f0-9]{40}$/,ID=/^[a-z0-9-]+$/;
export const posterRuntime=shared=>({node_major:process.versions.node.split('.')[0],platform:process.platform,arch:process.arch,browser:shared.browser,capture_policy:CAPTURE_POLICY});
export function posterCatalogIDs(manifest){
 assert(Array.isArray(manifest?.assets)&&manifest.assets.length&&!manifest.review_only,'Published poster catalog required');
 const ids=manifest.assets.map(asset=>asset.id);assert(ids.every(id=>ID.test(id||'')));assert.equal(new Set(ids).size,ids.length,'Duplicate poster model ID');return ids.sort();
}
export function assertPosterPNG(bytes,seal,kind){
 assert(Number.isSafeInteger(seal?.bytes)&&seal.bytes>0&&seal.bytes<=8*1024*1024,'Invalid poster byte seal');
 assert(HASH.test(seal.sha256||''),'Invalid poster hash seal');assert(Buffer.isBuffer(bytes),'Missing PNG bytes');
 assert.equal(bytes.length,seal.bytes,'Poster byte count differs');assert.equal(posterHash(bytes),seal.sha256,'Poster SHA-256 differs');
 assert(bytes.length>=26&&bytes.subarray(0,8).toString('hex')==='89504e470d0a1a0a','Not a PNG');
 assert.deepEqual([bytes.readUInt32BE(16),bytes.readUInt32BE(20)],CAPTURE_POLICY[kind],'Poster dimensions differ');
 assert([4,6].includes(bytes[25]),'Transparent poster required');
}
export function assertPosterRecord(row){
 assert(ID.test(row?.id||''),'Invalid poster record ID');assert(HASH.test(row.input_sha256||''));assert(HASH.test(row.source_glb_sha256||''));
 assert(['captured','reused','reviewed'].includes(row.evidence),'Missing capture evidence');
 assert.equal(row.poster?.source_glb_sha256,row.source_glb_sha256,'Poster source binding differs');
 assert(Array.isArray(row.files)&&row.files.length===2,'One sealed pair required');
 for(const kind of ['detail','wheel']){
  const path=`gallery/posters/${row.id}${kind==='wheel'?'-wheel':''}.png`;
  assert.equal(row.poster[kind],path,'Noncanonical poster path');assert.equal(row.files.filter(file=>file.path===path).length,1,'Missing or duplicate PNG seal');
 }
 if(row.evidence!=='reviewed')assert.equal(row.poster.input_sha256,row.input_sha256,'Capture stamp differs');
 return row;
}
export function assertPosterProof(proof,{repository,sourceSha,runId,runAttempt,policy_sha256,runtime,manifest}={}){
 assert.equal(proof?.version,1,'Unsupported poster proof');assert.equal(proof.kind,'gallery-poster-capture-proof','Wrong proof domain');assert.equal(proof.status,'pass');
 assert.equal(proof.repository,repository);assert.equal(proof.source_commit,sourceSha);assert(SHA.test(proof.source_commit||''));
 assert.equal(proof.run_id,runId);assert.equal(proof.run_attempt,runAttempt);assert.equal(proof.policy_sha256,policy_sha256,'Poster control plane differs');
 assert.deepEqual(proof.runtime,runtime,'Poster runtime differs');assert.deepEqual(proof.catalog_ids,posterCatalogIDs(manifest),'Poster baseline source catalog differs');
 assert(HASH.test(proof.shared_sha256||''));assert(Array.isArray(proof.posters));assert.equal(new Set(proof.posters.map(row=>row.id)).size,proof.posters.length,'Duplicate poster proof');
 for(const row of proof.posters){assertPosterRecord(row);const asset=manifest.assets.find(asset=>asset.id===row.id);assert(asset,'Poster not in independently read source');assert.equal(row.source_glb_sha256,asset.sha256?.glb,'Poster baseline source GLB differs');if(row.evidence!=='reviewed')assert.equal(row.poster.browser_version,runtime.browser,'Poster capture browser differs');}
 return proof;
}
export function selectPosterCaptures({manifest,shared,approved=[],verified=null,policy_sha256,runtime=posterRuntime(shared)}){
 const ids=posterCatalogIDs(manifest),golden=new Set(approved),bundle=readVerifiedPosterBundle(verified),reused=[],capture=[];
 assert([...golden].every(id=>ids.includes(id)),'Unknown approved poster');
 const usable=bundle&&bundle.proof.policy_sha256===policy_sha256&&posterObjectHash(bundle.proof.runtime)===posterObjectHash(runtime)&&bundle.proof.shared_sha256===shared.sha256;
 for(const asset of manifest.assets){
  const prior=usable?bundle.proof.posters.find(row=>row.id===asset.id):null;
  if(prior&&prior.input_sha256===posterInputKey(asset,shared)&&prior.source_glb_sha256===asset.sha256?.glb)reused.push(asset.id);
  else if(!golden.has(asset.id))capture.push(asset.id);
 }
 return {capture,reused,approved:[...golden],verified:usable?verified:null};
}
/** Copy only independently checked PNGs to the temporary output gallery. */
export async function importVerifiedPosters({manifest,shared,resources,outputRoot,approved=[],verified,policy_sha256,runtime}){
 const selection=selectPosterCaptures({manifest,shared,approved,verified,policy_sha256,runtime}),bundle=readVerifiedPosterBundle(selection.verified);
 const next=structuredClone(resources);
 for(const id of selection.reused){
  const row=bundle.proof.posters.find(row=>row.id===id);
  // Reviewed source pixels retain their original seals/metadata without rewrites.
  if(approved.includes(id)){
   assert.equal(posterObjectHash(next.posters[id]),posterObjectHash(row.poster),'Trusted artifact disagrees with reviewed poster');
   for(const seal of row.files)assert.equal(posterObjectHash(next.files.find(file=>file.path===seal.path)),posterObjectHash(seal),'Trusted artifact disagrees with reviewed PNG seal');
   continue;
  }
  for(const kind of ['detail','wheel']){
   const path=row.poster[kind],seal=row.files.find(file=>file.path===path),bytes=bundle.files.get(path);assertPosterPNG(bytes,seal,kind);
   const target=resolve(outputRoot,path);assert(target.startsWith(resolve(outputRoot)+sep));await mkdir(dirname(target),{recursive:true});await writeFile(target,bytes);
  }
  next.files=next.files.filter(file=>!row.files.some(seal=>seal.path===file.path));next.files.push(...structuredClone(row.files));next.posters[id]=structuredClone(row.poster);
 }
 return {resources:next,selection};
}
/** Emit only complete, audited current results; later GitHub success grants trust. */
export async function writePosterProof({root=process.cwd(),outputRoot,manifest,resources,shared,captured=[],approved=[],verified=null,policy_sha256,sourceContext,directory=process.env.CI_GALLERY_PROOF_DIR,identity,runtime=posterRuntime(shared)}={}){
 if(!directory)return null;
 if(policy_sha256===undefined){
  if(sourceContext===undefined)({sourceContext}=await prepareModelSource({root,forceFull:process.env.CI_GALLERY_FORCE_FULL==='true'||process.env.FULL_REVIEW==='true'||process.env.GITHUB_EVENT_NAME==='workflow_dispatch'}));
  policy_sha256=modelPolicyDigest(root,{sourceContext});
 }
 if(!identity){
  assert(!process.env.CHROMIUM_PATH,'Custom browser executable cannot establish poster proof');
  const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',env:immutableGitEnv()}).trim();
  assert.equal(git('status','--porcelain','--untracked-files=no'),'','Poster proof requires unchanged tracked source');
  identity={repository:process.env.GITHUB_REPOSITORY,source_commit:git('rev-parse','HEAD'),run_id:Number(process.env.GITHUB_RUN_ID),run_attempt:Number(process.env.GITHUB_RUN_ATTEMPT)};
  assert.equal(identity.source_commit,process.env.GITHUB_SHA,'Poster source differs from workflow source');assert.equal(runtime.node_major,CAPTURE_POLICY.node_major,'Poster proof needs pinned Node');
 }
 assert(/^[\w.-]+\/[\w.-]+$/.test(identity.repository||''));assert(SHA.test(identity.source_commit||''));assert(Number.isSafeInteger(identity.run_id)&&identity.run_id>0);assert(Number.isSafeInteger(identity.run_attempt)&&identity.run_attempt>0);
 const selection=selectPosterCaptures({manifest,shared,approved,verified,policy_sha256,runtime}),fresh=new Set(captured),golden=new Set(approved),reused=new Set(selection.reused);
 assert.equal(fresh.size,captured.length);assert.deepEqual([...new Set([...fresh,...golden,...reused])].sort(),posterCatalogIDs(manifest),'Poster proof lacks independently established generation coverage');
 const artifactRoot=resolve(root,directory);assert(artifactRoot!==resolve(root)&&artifactRoot!==resolve(outputRoot),'Unsafe proof destination');
 await rm(artifactRoot,{recursive:true,force:true});await mkdir(artifactRoot,{recursive:true});
 const posters=[];
 for(const asset of manifest.assets){
  const poster=resources.posters[asset.id],files=resources.files.filter(file=>[poster?.detail,poster?.wheel].includes(file.path));
  const row=assertPosterRecord({id:asset.id,input_sha256:posterInputKey(asset,shared),source_glb_sha256:asset.sha256.glb,poster,files,evidence:golden.has(asset.id)?'reviewed':fresh.has(asset.id)?'captured':'reused'});
  if(row.evidence!=='reviewed')assert.equal(poster.browser_version,shared.browser,'Capture browser differs');
  for(const kind of ['detail','wheel']){const path=poster[kind],source=resolve(outputRoot,path);assert.equal(await realpath(source),source,'Poster symlink rejected');const bytes=await readFile(source);assertPosterPNG(bytes,files.find(file=>file.path===path),kind);const target=resolve(artifactRoot,path);await mkdir(dirname(target),{recursive:true});await writeFile(target,bytes);}
  posters.push(row);
 }
 const proof={version:1,kind:'gallery-poster-capture-proof',status:'pass',...identity,policy_sha256,runtime,shared_sha256:shared.sha256,catalog_ids:posterCatalogIDs(manifest),posters,
  captured_ids:[...fresh].sort(),reused_ids:[...reused].sort(),reviewed_ids:[...golden].sort(),...(selection.verified?{verified_baseline:selection.verified}:{})};
 await writeFile(resolve(artifactRoot,POSTER_PROOF_FILE),JSON.stringify(proof,null,2)+'\n');return proof;
}
