# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess,json,datetime,time,shutil,hashlib,sys
R=Path.cwd();W=R/'production/batch88';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
bl=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
def run(b,name,args,timeout=3600):
 start=now();t=time.monotonic()
 with (b/(name+'.log')).open('w') as log:
  p=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT);code=p.wait(timeout=timeout)
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(dict(stage=name,runner_pid=p.pid,started_at=start,ended_at=now(),wall_seconds=time.monotonic()-t,exit_code=code,command=args))+'\n')
 print(b.name,name,code,flush=True)
 if code:raise RuntimeError(str(b)+' '+name)
sel=json.loads((W/'final-selection.json').read_text())
if len(sys.argv)>1:sel=[x for x in sel if x['asset_id'] in sys.argv[1:]]
for x in sel:
 b=R/x['path'];slug=x['asset_id'];assert json.loads((b/'diagnostic-disposition.json').read_text())['status']=='selected-for-full-lifecycle'
 original=b.parent/'r001';f=json.loads((original/'modeling-freeze.json').read_text());assert all(H(original/n)==h for n,h in f['files'].items());assert H(b/'brief.json')==H(original/'brief.json') and H(b/'references.json')==H(original/'references.json')
 if not (b/'gltf-validator.report.json').exists():run(b,'format',['node','scripts/validate_gltf.cjs',str(b/'model.glb')])
 if not (b/'source-final.report.json').exists():run(b,'source-reopen',bl+['scripts/check_source_export.py','--','--source',str(b/'source.blend'),'--glb',str(b/'model.glb'),'--output',str(b/'source-final.report.json'),'--collection','EXPORT'])
 if not (b/'source-vertex-counts.json').exists():run(b,'source-vertex-counts',bl+[str(W/'count-source-vertices.py'),'--',str(b)])
 if not (b/'build-dependencies.json').exists():
  dep=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py'];(b/'build-dependencies.json').write_text(json.dumps(dict(blender='/usr/bin/blender',blender_version='4.3.2',threads=2,python='Blender bundled Python',inputs={str(p.relative_to(R)):H(p) for p in dep},node_dependency_root='/workspace/shared/lowpoly-landair-web-integration/node_modules',three_version='0.180.0',node_lockfile_sha256=H(R/'package-lock.json'),created_at=now()),indent=2)+'\n')
 if not (b/'candidate-brief.json').exists():
  d=json.loads((b/'brief.json').read_text());d['packaging_adapter']=dict(created_at=now(),frozen_design_brief_sha256=H(b/'brief.json'),note='Postbuild source/generator/config hash closure only; original design and reference ledger unchanged.');d['required_deliverables']=[dict(role=k,path=str((b/n).relative_to(R)),sha256=H(b/n)) for k,n in [('source','source.blend'),('generator','generator.py'),('config','build-config.json')]];(b/'candidate-brief.json').write_text(json.dumps(d,indent=2)+'\n')
 d=json.loads((b/'candidate-brief.json').read_text());assert all(H(R/v['path'])==v['sha256'] for v in d['required_deliverables']);refs=json.loads((b/'references.json').read_text());assert refs['no_incorporated_third_party_assets'] and all(v.get('rights_note') for v in refs['sources'])
 if not (b/'preproof-binding.json').exists():(b/'preproof-binding.json').write_text(json.dumps(dict(checked_at=now(),glb_sha256=H(b/'model.glb'),brief_sha256=H(b/'candidate-brief.json'),references_sha256=H(b/'references.json'),original_freeze_unchanged=True,source_generator_config_binding='pass'),indent=2)+'\n')
 if not (b/'proof-final/render-manifest.json').exists():run(b,'proof-final',bl+[str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','24'])
 shutil.copy(b/'proof-final/hero.png',b/'preview.png')
 run(b,'runtime-parse',['node',str(W/'runtime-parse.mjs'),str(b)])
 for i in [1,2]:
  job={'asset_id':slug,'revision':x['revision'],'job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(b/'generator.py'),'config':str(b/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py'),'brief':str(b/'brief.json'),'references':str(b/'references.json')},'argv':['{blender}','--factory-startup','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json']}
  q=W/('queue-'+slug+'-'+x['revision']+'-'+str(i)+'.json')
  if not q.exists():q.write_text(json.dumps(dict(schema_version=1,lane='build',jobs=[job]),indent=2)+'\n')
  if not (b/('repro-final-'+str(i)+'.report.json')).exists():
   run(W,'queue-'+slug+'-'+x['revision']+'-'+str(i),['flock','/tmp/lowpoly-production-blender.lock','python3','scripts/run_asset_queue.py',str(q),'--runs-root',str(W/'rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','120','--resume'])
   matched=[]
   for result in (W/'rebuild-runs/build'/slug/x['revision']).rglob('result.json'):
    res=json.loads(result.read_text());request=json.loads((result.parent/'request.json').read_text());inputs=request['identity']['inputs']
    if res.get('status')=='succeeded' and res.get('job_id')==job['job_id'] and inputs['generator']['sha256']==H(b/'generator.py') and inputs['config']['sha256']==H(b/'build-config.json'):matched.append(result)
   assert len(matched)==1,matched;result=matched[0]
   run(b,'repro-final-'+str(i),['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(R),'--output',str(b/('repro-final-'+str(i)+'.report.json'))])
 print('LIFECYCLE_COMPLETE',slug,flush=True)
