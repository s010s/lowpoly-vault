/** Trust comes from the successful deploy job's separate artifact and GitHub workflow_run,
 * never from a scope artifact's own base, SHA, URL or run claims. No publication authority.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,readdirSync,lstatSync,existsSync,appendFileSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
export const MARKER_PATH='release-build.json';
export const hash=b=>createHash('sha256').update(b).digest('hex');
const sha=x=>typeof x==='string'&&/^[a-f0-9]{40}$/.test(x)&&!/^0+$/.test(x);
const digest=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
const number=x=>Number.isSafeInteger(x)&&x>0;
export function assertIdentity(identity){
 assert(identity&&sha(identity.head)&&sha(identity.base),'Exact expected source and original push base required');
 assert(number(identity.runId)&&number(identity.runAttempt),'Expected run ID and attempt required');
 assert(typeof identity.repository==='string'&&/^[\w.-]+\/[\w.-]+$/.test(identity.repository),'Expected repository required');return identity;
}
export function pushIdentity(event,environment=process.env){
 assert.equal(environment.GITHUB_EVENT_NAME,'push','Deployment marker requires a real push context');
 assert.equal(event.ref,'refs/heads/main');assert.equal(environment.GITHUB_REF,event.ref);assert.equal(event.after,environment.GITHUB_SHA);
 assert.equal(event.repository.full_name,environment.GITHUB_REPOSITORY);
 return assertIdentity({head:event.after,base:event.before,runId:Number(environment.GITHUB_RUN_ID),runAttempt:Number(environment.GITHUB_RUN_ATTEMPT),repository:event.repository.full_name});
}
export function assertDeploymentReceipt(receipt,event){
 const run=event?.workflow_run;assert(run,'Expected GitHub workflow_run context');
 assert.equal(run.conclusion,'success');assert.equal(run.event,'push');assert.equal(run.head_branch,'main');
 const repository=event.repository?.full_name;assert.equal(run.head_repository?.full_name,repository,'Foreign deployment repository');
 assert.equal(receipt?.schema_version,1);assert.equal(receipt.kind,'successful-pages-deployment-v1');assert.equal(receipt.deploy_outcome,'success');assert.equal(receipt.source_event,'push');assert.equal(receipt.source_ref,'refs/heads/main');
 assert.equal(receipt.head,run.head_sha,'Wrong deployment SHA');assert.equal(receipt.runId,run.id,'Wrong deployment run');assert.equal(receipt.runAttempt,run.run_attempt,'Wrong deployment attempt');assert.equal(receipt.repository,repository);
 const identity=assertIdentity({head:receipt.head,base:receipt.base,runId:receipt.runId,runAttempt:receipt.runAttempt,repository});
 // Equal before/after is permitted ONLY when that is the independently recorded
 // source event. A normal shared-code-only push still has a distinct before SHA.
 assert.equal(receipt.same_commit_push,identity.base===identity.head);
 assert(digest(receipt.build_digest)&&digest(receipt.marker_sha256)&&digest(receipt.scope_sha256));
 const url=new URL(receipt.page_url);assert.equal(url.protocol,'https:');assert(!url.username&&!url.password&&!url.search&&!url.hash,'Invalid official deployment URL');assert(url.pathname.endsWith('/'),'Canonical official deployment directory required');
 return {...identity,pageURL:url.href,buildDigest:receipt.build_digest,markerSHA256:receipt.marker_sha256,scopeSHA256:receipt.scope_sha256};
}
export function readDeploymentContext({receiptPath=process.env.DEPLOYMENT_RECEIPT,eventPath=process.env.GITHUB_EVENT_PATH}={}){
 assert.equal(process.env.GITHUB_EVENT_NAME,'workflow_run','Detached verification requires workflow_run');
 return assertDeploymentReceipt(JSON.parse(readFileSync(receiptPath)),JSON.parse(readFileSync(eventPath)));
}
export function inventory(root,{excludeMarker=false}={}){
 const result=[];const walk=folder=>{for(const name of readdirSync(resolve(root,folder)).sort()){const path=folder?folder+'/'+name:name;if(excludeMarker&&path===MARKER_PATH)continue;const stat=lstatSync(resolve(root,path));assert(!stat.isSymbolicLink(),'Deployment symlink rejected');if(stat.isDirectory())walk(path);else{assert(stat.isFile());const bytes=readFileSync(resolve(root,path));result.push({path,bytes:bytes.length,sha256:hash(bytes)});}}};walk('');assert(result.length,'Empty deployment build');return result;
}
export function stampDeployment({root='.',identity}={}){
 assertIdentity(identity);assert.equal(execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),identity.head,'Marker source checkout differs');
 const timings=JSON.parse(readFileSync(resolve(root,'qa/ci-timings/build.json')));
 assert.equal(timings.status,'pass','All six build phases must pass before stamping');
 assert.deepEqual(timings.phases.map(p=>p.name),['publication-check','registry-check','vite','seal-render-template','copy-and-package','full-release-audit']);
 for(const p of timings.phases){assert.equal(p.exit_code,0);assert.equal(p.signal,null);}
 const dist=resolve(root,'dist');assert(!existsSync(resolve(dist,MARKER_PATH)),'Existing deployment marker cannot be silently replaced');
 const files=inventory(dist),marker={schema_version:1,kind:'exact-pages-build-v1',...identity,build_digest:hash(JSON.stringify(files)),files};
 const bytes=JSON.stringify(marker,null,2)+'\n';writeFileSync(resolve(dist,MARKER_PATH),bytes);
 // A supplemental inventory extension permits exactly this marker and proves
 // every originally audited file is unchanged. Original audit assertions remain.
 assert.deepEqual(inventory(dist,{excludeMarker:true}),files,'Stamp changed audited files');
 const all=inventory(dist);assert.equal(all.length,files.length+1);return {marker,marker_sha256:hash(bytes)};
}
export function verifyBuildMarker({root='.',context}={}){
 assertIdentity(context);const dist=resolve(root,'dist'),bytes=readFileSync(resolve(dist,MARKER_PATH)),marker=JSON.parse(bytes);
 assert.equal(hash(bytes),context.markerSHA256,'Marker artifact hash differs from successful deployment');
 assert.equal(marker.schema_version,1);assert.equal(marker.kind,'exact-pages-build-v1');
 for(const key of ['head','base','runId','runAttempt','repository'])assert.equal(marker[key],context[key],'Build marker subject differs: '+key);
 assert.equal(marker.build_digest,context.buildDigest);assert.deepEqual(marker.files,inventory(dist,{excludeMarker:true}));assert.equal(hash(JSON.stringify(marker.files)),marker.build_digest);return marker;
}
export async function waitForDeployedBuild({baseURL,marker,markerSHA256,timeout=180000,interval=5000,fetcher=fetch,now=Date.now,sleep=ms=>new Promise(r=>setTimeout(r,ms))}={}){
 const base=new URL(baseURL);assert.equal(base.protocol,'https:');const deadline=now()+timeout;let lastError;
 while(true){try{
  const get=async path=>{const url=new URL(path,base);assert.equal(url.origin,base.origin);assert(url.pathname.startsWith(base.pathname));const response=await fetcher(url.href,{cache:'no-store',redirect:'error',signal:AbortSignal.timeout(Math.min(15000,Math.max(1,deadline-now())))});assert(response.ok,'Deployed resource HTTP '+response.status+': '+path);return Buffer.from(await response.arrayBuffer());};
  const bytes=await get(MARKER_PATH);assert.equal(hash(bytes),markerSHA256,'Stale or absent deployed commit/build marker');assert.deepEqual(JSON.parse(bytes),marker,'Deployed marker subject differs');
  // Includes the FULL built manifest and every executable/style entry, not just
  // stable model payload hashes. An old UI with a fresh marker is rejected.
  const entries=marker.files.filter(f=>f.path==='assets/manifest.json'||/\.(?:js|css)$/.test(f.path)||['index.html','models/index.html','zh-CN/index.html','zh-CN/models/index.html'].includes(f.path));
  assert(entries.some(f=>f.path==='assets/manifest.json'),'Missing expected manifest');assert(entries.some(f=>f.path.endsWith('.js')),'Missing expected runtime entries');
  for(const entry of entries){const actual=await get(entry.path);assert.equal(actual.length,entry.bytes,'Deployed resource size differs: '+entry.path);assert.equal(hash(actual),entry.sha256,'Deployed resource hash differs: '+entry.path);}
  return {status:'PASS',head:marker.head,build_digest:marker.build_digest,verified_entries:entries.map(f=>f.path)};
 }catch(error){lastError=error;if(now()>=deadline)throw lastError;await sleep(Math.min(interval,Math.max(1,deadline-now())));}}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const report={status:'RUNNING',phase:'initialize',expected:{source_commit:process.env.GITHUB_SHA||null,run_id:process.env.GITHUB_RUN_ID||null,run_attempt:process.env.GITHUB_RUN_ATTEMPT||null},downstream:'NOT_RUN'};
 try{assert.equal(process.argv[2],'stamp');report.phase='source-event';const identity=pushIdentity(JSON.parse(readFileSync(process.env.GITHUB_EVENT_PATH)));report.phase='audit-and-stamp';const result=stampDeployment({identity});report.status='PASS';report.phase='complete';report.marker_sha256=result.marker_sha256;report.build_digest=result.marker.build_digest;if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,`marker_sha256=${result.marker_sha256}\nbuild_digest=${result.marker.build_digest}\n`);}
 catch(error){report.status='FAIL';report.failed_phase=report.phase;report.error=error.stack;process.exitCode=1;console.error(error);}
 finally{mkdirSync('qa/deployment-stamp',{recursive:true});writeFileSync('qa/deployment-stamp/report.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}
}
