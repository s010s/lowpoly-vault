/** Bounded additive release, falling back to the original complete pipeline. */
import {spawnSync} from 'node:child_process';
import {mkdirSync,writeFileSync} from 'node:fs';
import {verifiedFastScope,restoreFastBase,writeFastBase} from './ci-release-fast-base.mjs';
import {canReuseBuildContracts,fastBuildIdentity} from './ci-release-fast-contracts.mjs';
import {incrementalDelivery} from './ci-incremental-delivery.mjs';
const mode=process.argv[2];
const originalContracts='npm run test:manifest && node site/validate.mjs --review && npm run test:catalog && npm run test:theme && npm run test:preview && npm run test:redesign && npm run test:scrub && npm run test:gallery';
const command=(file,args)=>{const r=spawnSync(file,args,{stdio:'inherit',env:process.env});if(r.error||r.status!==0)throw Error(`${file} failed (${r.status}): ${r.error||''}`);};
const scope=mode==='seal'?null:await verifiedFastScope();
if(mode==='build'){
 let restored=null;
 if(scope.eligible){try{restored=await restoreFastBase(scope);}catch(e){console.log('FULL_FALLBACK: '+e.message);}}
 if(!restored)command(process.execPath,['site/ci-timed.mjs','build']);
 else{
  const report={version:1,mode:'additive',...fastBuildIdentity(),status:'running',baseline:restored.baseline,artifact_id:restored.artifact_id,artifact_digest:restored.artifact_digest,reused:['vite','historical-package-generation'],added_ids:restored.added_ids,phases:[]};
  const phase=async(name,fn)=>{const start=performance.now();try{await fn();report.phases.push({name,seconds:(performance.now()-start)/1000,exit_code:0,signal:null});}catch(e){report.phases.push({name,seconds:(performance.now()-start)/1000,exit_code:1,signal:null});throw e;}};
  try{
   await phase('publication-check',()=>command(process.execPath,['site/ci-publication.mjs']));
   await phase('registry-check',()=>command(process.execPath,['site/model-registry-sync.mjs','check','--registry-root','.','--release-manifest','assets/manifest.json','--target-root','.']));
   await phase('incremental-copy-and-package',()=>incrementalDelivery({addedIds:restored.added_ids}));
   await phase('full-release-audit',()=>command(process.execPath,['site/audit-release.mjs']));report.status='pass';
  }catch(e){report.status='fail';report.fallback_reason=e.message;console.log('FULL_FALLBACK after additive attempt: '+e.message);}
  finally{mkdirSync('qa/ci-timings',{recursive:true});writeFileSync(report.status==='pass'?'qa/ci-timings/build.json':'qa/ci-timings/additive-attempt.json',JSON.stringify(report,null,2)+'\n');}
  if(report.status!=='pass')command(process.execPath,['site/ci-timed.mjs','build']);
 }
}else if(mode==='contracts'){
 if(canReuseBuildContracts(scope)){console.log('REUSED_BASELINE: unchanged contract-test code and old inputs; fresh full source/output validation follows.');command(process.execPath,['site/validate.mjs','--review']);command(process.execPath,['site/gallery-assets.mjs']);}
 else command('bash',['-e','-c',originalContracts]);
}else if(mode==='seal')await writeFastBase();
else throw Error('Expected build, contracts or seal');
