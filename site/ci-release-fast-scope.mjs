/** Fail-closed append classification. Eligibility is NOT baseline trust or a PASS. */
import assert from 'node:assert/strict';
import {isDeepStrictEqual} from 'node:util';
import {execFileSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {assessIncrementalDiff} from './ci-incremental-models.mjs';
import {immutableGitEnv} from './ci-git.mjs';
const aggregates=new Set(['assets/manifest.json','site/catalog-data.json','assets/turntables/index.json','site/gallery/wheel-framing.json','site/public/gallery/resources.json','production/production-releases-r002.json']);
const equal=(a,b,m)=>assert(isDeepStrictEqual(a,b),m||'Append-only comparison differs');
const prefix=(a,b,m)=>{assert(Array.isArray(a)&&Array.isArray(b));equal(b.slice(0,a.length),a,m);};
export function classifyReleaseAppend({beforeEntries,afterEntries,readBefore,readAfter,readAfterBytes}){
 try{
  const entries=rows=>{const m=new Map();for(const r of rows){assert(!m.has(r.path));assert(r.type==='blob'&&['100644','100755'].includes(r.mode),'Only regular files');m.set(r.path,r);}return m;};
  const old=entries(beforeEntries),next=entries(afterEntries),before=readBefore('assets/manifest.json'),after=readAfter('assets/manifest.json');
  const oldIDs=new Set(before.assets.map(a=>a.id)),added=after.assets.filter(a=>!oldIDs.has(a.id)),ids=new Set(added.map(a=>a.id));
  assert(ids.size&&ids.size===added.length&&oldIDs.size===before.assets.length,'Nonempty unique additions required');
  equal(after.assets.slice(0,before.assets.length),before.assets,'Existing manifest order/records changed');assert.equal(after.assets.length,before.assets.length+ids.size);
  const {assets:_a,...a}=before,{assets:_b,...b}=after;equal(a,b,'Shared manifest metadata changed');
  const changes=[];for(const [path,row] of old){assert(next.has(path),'Removed path: '+path);assert.equal(next.get(path).mode,row.mode,'Existing file mode changed: '+path);if(next.get(path).oid!==row.oid){assert(aggregates.has(path),'Existing immutable input changed: '+path);changes.push(path);}}
  const prodPath='production/production-releases-r002.json',p=readBefore(prodPath),q=readAfter(prodPath);
  const {descriptors:d,asset_ids:i,...ps}=p,{descriptors:e,asset_ids:j,...qs}=q;equal(ps,qs);prefix(d,e,'Previous production descriptors changed');prefix(i,j,'Previous production identities changed');equal([...j.slice(i.length)].sort(),[...ids].sort(),'New production IDs differ');assert(new Set(j).size===j.length);
  const roots=e.slice(d.length).map(row=>{assert(/^production\/[a-z0-9-]+\/release(?:-[a-z0-9]+)?\.json$/.test(row.path));assert(!old.has(row.path),'Existing descriptor reused');return row.path.slice(0,row.path.lastIndexOf('/')+1);});assert(roots.length,'New immutable descriptor required');
  const own=path=>added.some(asset=>path.startsWith(`assets/additions/${asset.id}/`)||path.startsWith(`assets/turntables/${asset.id}/`)||path.startsWith(`assets/card-previews/${asset.id}-`)||path===`site/public/gallery/posters/${asset.id}.png`||path===`site/public/gallery/posters/${asset.id}-wheel.png`);
  const newPaths=[];for(const [path,row] of next)if(!old.has(path)){
   assert.equal(row.mode,'100644','New executable entry requires full validation');
   assert(!path.split('/').some(x=>x==='..'||x==='.'||!x),'Unsafe path');
   assert((own(path)&&/\.(?:json|png|webp|jpg|jpeg|glb|blend|py|txt)$/.test(path))||(roots.some(r=>path.startsWith(r))&&/\.(?:json|md|png|webp|jpg|jpeg|glb|blend|py|txt)$/.test(path))||/^registry\/(?:models\/[^/]+\/revisions\/[a-f0-9]{64}\/record|batches\/[^/]+)\.json$/.test(path),'Unknown new dependency: '+path);
   changes.push(path);newPaths.push(path);
  }
  // Registry projection sorts new definitions into existing arrays. Preserve all
  // old records and their relative order, then validate new ownership using the
  // existing append checker on an equivalent normalized order. No file is edited.
  const oldCatalog=readBefore('site/catalog-data.json'),newCatalog=readAfter('site/catalog-data.json'),normalized=structuredClone(newCatalog);
  for(const kind of ['worlds','packs']){const names=new Set(oldCatalog[kind].map(x=>x.id));equal(newCatalog[kind].filter(x=>names.has(x.id)),oldCatalog[kind],'Existing catalog definition changed/reordered');normalized[kind]=[...oldCatalog[kind],...newCatalog[kind].filter(x=>!names.has(x.id))];}
  const scopedAfter=p=>p==='site/catalog-data.json'?normalized:readAfter(p);
  // The existing classifier validates catalog additions, poster seals, recipes,
  // typed registry records and projection identity. It is never sufficient alone.
  const filtered=changes.filter(p=>!p.endsWith('.py')&&!p.endsWith('.txt'));
  const result=assessIncrementalDiff({paths:filtered,before,after,readBefore,readAfter:scopedAfter,registryState:{beforePaths:[...old.keys()],readAfterBytes}});
  assert(result.eligible,result.reasons.join('; '));equal(result.added_ids,[...ids].sort());
  return {eligible:true,mode:'additive',added_ids:[...ids].sort(),changed_paths:changes.sort(),new_paths:newPaths.sort(),reasons:['All pre-existing nonaggregate Git blobs unchanged; known aggregates append only']};
 }catch(error){return {eligible:false,mode:'full',added_ids:[],reasons:[error.message]};}
}
export function releaseAppendFromGit(baseSha,{root=process.cwd(),currentSha=process.env.GITHUB_SHA}={}){
 try{
  const git=(...args)=>execFileSync('git',args,{cwd:root,env:immutableGitEnv(),encoding:'utf8',maxBuffer:128*1024*1024}).trimEnd();
  for(const sha of [baseSha,currentSha])assert(/^[a-f0-9]{40}$/.test(sha||'')&&!/^0+$/.test(sha));
  assert.equal(git('rev-parse','HEAD'),currentSha);assert(git('ls-files','-v').split('\n').every(line=>line.startsWith('H ')),'Hidden index flags require full validation');assert.equal(git('status','--porcelain','--untracked-files=no'),'','Tracked checkout dirty');git('merge-base','--is-ancestor',baseSha,currentSha);
  const inventory=sha=>git('ls-tree','-rz',sha).split('\0').filter(Boolean).map(line=>{const [meta,path]=line.split('\t'),[mode,type,oid]=meta.split(' ');return {mode,type,oid,path};});
  const bytes=(sha,path)=>execFileSync('git',['show',`${sha}:${path}`],{cwd:root,env:immutableGitEnv(),maxBuffer:128*1024*1024});
  return classifyReleaseAppend({beforeEntries:inventory(baseSha),afterEntries:inventory(currentSha),readBefore:p=>JSON.parse(bytes(baseSha,p)),readAfter:p=>JSON.parse(bytes(currentSha,p)),readAfterBytes:p=>bytes(currentSha,p)});
 }catch(error){return {eligible:false,mode:'full',added_ids:[],reasons:[error.message]};}
}
