/** Small model additions do not launch four jobs to prove that historical tests did not change. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {leanScope,needsGeometryRegression} from './ci-lean-scope.mjs';
const mode=process.argv[2],scope=leanScope();assert(['contracts','publication','pipeline'].includes(mode));console.log('Regression selection:',JSON.stringify(scope));
const run=(file,args=[])=>{const result=spawnSync(file,args,{stdio:'inherit',env:process.env});assert.equal(result.status,0,result.error?.message||`${file} ${args.join(' ')} failed`);};
if(mode==='publication'){
 if(scope.publication)run(process.execPath,['site/ci-timed.mjs','publication']);
 else console.log('NOT_APPLICABLE: historical publication implementation unchanged; no historical suite result claimed.');
}else if(mode==='pipeline'){
 if(scope.framework){run('python3',['scripts/test_qa_glb_scale_aware.py','-v']);run('npm',['run','test:pipeline']);run('npm',['run','test:manifest']);run('python3',['scripts/test_final_delivery.py']);run(process.execPath,['site/final-delivery-test.mjs']);}
 else console.log('NOT_APPLICABLE: pipeline implementation unchanged; model content validation belongs to the pages source gate.');
}else{
 if(scope.framework){
  for(const file of ['ci-lean-release-test','ci-release-fast-scope-test','ci-production-baseline-test','ci-production-incremental-test','model-registry-test','model-registry-sync-test','content-production-acceptance-test','audit-release-test','production-poster-input-memo-test'])run(process.execPath,[`site/${file}.mjs`]);
 }
 if(scope.website){
  for(const task of ['test:catalog','test:theme','test:preview','test:redesign'])run('npm',['run',task]);
  for(const file of ['image-scrub-test','turntable-mixed-source-test'])run(process.execPath,[`site/${file}.mjs`]);
  // The source/output gallery audit belongs to the build, not a second test pass.
  const geometry=new Set(['reset-transition-test','single-framing-test','poster-projection-test','selection-orbit-controls-test','compare-ground-regression-test','model-support-test'].map(name=>`node site/gallery/tests/${name}.mjs`));
  const runGeometry=needsGeometryRegression(scope.paths);
  const gallery=JSON.parse(readFileSync('package.json')).scripts['test:gallery'].split(' && ').filter(command=>command!=='node site/gallery-assets.mjs'&&(runGeometry||!geometry.has(command)));
  if(!runGeometry)console.log('NOT_APPLICABLE: renderer geometry unchanged; full-catalog geometry matrices are not re-run.');
  for(const command of gallery){assert(/^node site\/[a-zA-Z0-9_./-]+\.mjs$/.test(command));run(process.execPath,[command.slice(5)]);}
 }
 else run(process.execPath,['site/model-preview-test.mjs']);
}
