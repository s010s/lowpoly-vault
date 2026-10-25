/** Isolated candidate probe, never a production build or accepted-baseline receipt.
 * Only this explicit CLI prepares a throwaway test root. Release commands never import it. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,cp,symlink,mkdtemp,rm,readdir,lstat} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
export const PROBE_IDS=['onoclea','pertica','azolla','sidneyia','arroyo-wash'];
const sha=b=>createHash('sha256').update(b).digest('hex');
export function parseCandidate(bytes,resolution,source){
 assert([1536,2048].includes(resolution));assert.match(source||'',/^[a-f0-9]{40}$/);
 const text=bytes.toString();assert(text.startsWith('export default '));const index=JSON.parse(text.slice(15).trim().replace(/;$/,''));
 assert.equal(index.version,1);assert.equal(index.kind,'detail-only-presentations');assert.equal(index.source_commit,source);assert.deepEqual(Object.keys(index.presentations).sort(),[...PROBE_IDS].sort());
 for(const id of PROBE_IDS){const e=index.presentations[id];assert.equal(e.id,id);assert.equal(e.detail,`detail-presentations/${id}.png`);assert.equal(e.capture.source_commit,source);assert.equal(e.capture.method,'PreviewRenderer.select(detail)/canonical-square-native-clipping-hires-v2');assert.deepEqual(e.capture.presentation,{revision:2,minimum_margin:.025,screen_shift:.06,raster_size:resolution});assert.equal(e.png.width,resolution);assert.equal(e.png.height,resolution);assert.equal(e.capture.detail_sha256,e.png.sha256);}
 return index;
}
export async function prepareCandidateRoot(root,temp){
 const listed=spawnSync('git',['ls-files','-z'],{cwd:root,encoding:'utf8',maxBuffer:32*1024*1024});assert.equal(listed.status,0);
 const paths=listed.stdout.split('\0').filter(Boolean);assert(paths.length>0);
 // Production readers intentionally reject symlinks. Copy every tracked input
 // as a private regular file; never relax those readers or copy untracked media.
 for(let start=0;start<paths.length;start+=24)await Promise.all(paths.slice(start,start+24).map(async path=>{assert(!path.startsWith('/')&&!path.split('/').includes('..'));const from=resolve(root,path),to=resolve(temp,path);assert((await lstat(from)).isFile(),'Tracked symlink/non-file rejected '+path);await mkdir(dirname(to),{recursive:true});await cp(from,to);}));
 await symlink(resolve(root,'node_modules'),resolve(temp,'node_modules'));return paths;
}
export function candidateBrowserProfile(value,resolution){const profile=value||'candidate-smoke';assert(['candidate-smoke','native-layer-diagnostic'].includes(profile),'Only unaccepted probe profiles allowed');if(profile==='native-layer-diagnostic')assert.equal(resolution,1536,'Native diagnostic is1536only');return profile;}
export async function runCandidateSmoke({fresh,resolution,output,source=process.env.GITHUB_SHA,root=process.cwd()}){
 const profile=candidateBrowserProfile(process.env.DETAIL_BROWSER_PROFILE,resolution);
 root=resolve(root);fresh=resolve(fresh);output=resolve(output);const head=spawnSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'});assert.equal(head.status,0);assert.equal(head.stdout.trim(),source,'Probe source must be the exact checked-out commit');const clean=spawnSync('git',['diff','--quiet','HEAD','--'],{cwd:root});assert.equal(clean.status,0,'Probe requires unchanged tracked source');assert(!output.startsWith(root+'/site/'),'Evidence must not overwrite runtime source');
 const bytes=await readFile(resolve(fresh,'detail-presentations-index.js')),index=parseCandidate(bytes,resolution,source);
 const capture=JSON.parse(await readFile(resolve(fresh,'capture-report.json')));assert.equal(capture.status,'pass');assert.equal(capture.smoke_only,true);assert.equal(capture.source_commit,source);assert.equal(capture.captured,5);assert.equal(capture.count,5);
 const original=await readFile(resolve(root,'site/gallery/detail-presentations-index.js'));
 const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json')));
 for(const id of PROBE_IDS){const a=manifest.assets.find(a=>a.id===id),e=index.presentations[id];assert(a);assert.equal(e.source_glb_sha256,a.sha256.glb);assert.equal(sha(await readFile(resolve(root,a.glb))),a.sha256.glb);const png=await readFile(resolve(fresh,e.detail));assert.equal(png.length,e.png.bytes);assert.equal(sha(png),e.png.sha256);assert.equal(png.readUInt32BE(16),resolution);assert.equal(png.readUInt32BE(20),resolution);}
 await mkdir(output,{recursive:true});const temp=await mkdtemp(resolve(root,'.detail-candidate-'));let failure;
 const report={kind:'unaccepted-right-detail-probe',profile,source_commit:source,ids:PROBE_IDS,resolution,candidate_index_sha256:sha(bytes),original_index_sha256:sha(original),capture_report_sha256:sha(await readFile(resolve(fresh,'capture-report.json'))),publication_authorized:false,accepted_baseline:false,repository:process.env.GITHUB_REPOSITORY||null,run_id:process.env.GITHUB_RUN_ID||null,run_attempt:process.env.GITHUB_RUN_ATTEMPT||null,source_files:[],phases:[],status:'running'};
 try{
  await prepareCandidateRoot(root,temp);
  const walk=async(folder)=>{for(const entry of await readdir(resolve(root,folder),{withFileTypes:true})){const p=folder+'/'+entry.name;if(p==='site/public')continue;if(entry.isDirectory())await walk(p);else if(entry.isFile())report.source_files.push({path:p,sha256:sha(await readFile(resolve(root,p)))});}};await walk('site');for(const p of ['vite.config.js','package.json','package-lock.json'])report.source_files.push({path:p,sha256:sha(await readFile(resolve(root,p)))});
  await writeFile(resolve(temp,'site/gallery/detail-presentations-index.js'),bytes);
  for(const id of PROBE_IDS){const e=index.presentations[id];await mkdir(dirname(resolve(temp,'site/public',e.detail)),{recursive:true});await cp(resolve(fresh,e.detail),resolve(temp,'site/public',e.detail));}
  const provenance=JSON.stringify(report,null,2);await writeFile(resolve(temp,'candidate-smoke-provenance.json'),provenance);await writeFile(resolve(output,'candidate-smoke-provenance.json'),provenance);
  const env={...process.env,GITHUB_SHA:source,SITE_BASE:'/lowpoly-vault/',DETAIL_BROWSER_PROFILE:profile,DETAIL_BROWSER_TARGET:'dist',DETAIL_BROWSER_SMOKE_RESOLUTION:String(resolution),GALLERY_DIR:'dist',QA_OUTPUT_DIR:output};
  const run=(name,args)=>{const result=spawnSync(process.execPath,args,{cwd:temp,env,stdio:'inherit'});report.phases.push({name,exit_code:result.status,signal:result.signal});assert(!result.error&&result.status===0,name+' failed');};
  run('candidate-vite',['node_modules/vite/bin/vite.js','build']);run('candidate-template',['site/ci-render-template.mjs']);run('candidate-copy',['site/copy-assets.mjs']);
  // Exact compiled build seals are retained even when a pixel gate fails.
  report.build_files=[];const buildWalk=async(folder)=>{for(const e of await readdir(resolve(temp,folder),{withFileTypes:true})){const p=folder+'/'+e.name;if(e.isDirectory())await buildWalk(p);else {const b=await readFile(resolve(temp,p));report.build_files.push({path:p.slice(5),bytes:b.length,sha256:sha(b)});}}};await buildWalk('dist');
  run('candidate-browser',['site/detail-presentation-browser-test.mjs']);run('candidate-retained-PNG-verifier',['site/detail-presentation-browser-test.mjs','--verify-evidence']);report.status='pass';
 }catch(error){failure=error;report.status='fail';report.error=error.stack;throw error;}finally{try{
  await writeFile(resolve(output,'candidate-build-provenance.json'),JSON.stringify(report,null,2));await writeFile(resolve(output,'candidate-index.js'),bytes);
  assert.deepEqual(await readFile(resolve(root,'site/gallery/detail-presentations-index.js')),original,'Production index mutated');assert.equal(spawnSync('git',['diff','--quiet','HEAD','--'],{cwd:root}).status,0,'Probe mutated tracked source');
 }catch(error){if(!failure)throw error;console.error('Probe evidence/immutability cleanup failed after original failure:',error);}finally{await rm(temp,{recursive:true,force:true});}}
 return report;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){const [fresh,resolution,output]=process.argv.slice(2);assert(fresh&&resolution&&output&&process.argv.length===5,'Usage: FRESH_DIR 1536|2048 EVIDENCE_DIR');await runCandidateSmoke({fresh,resolution:Number(resolution),output});}
