from pathlib import Path
import subprocess,json,datetime,time,shutil,hashlib,sys
R=Path('/workspace/shared/lowpoly-batch90-20261020');P=R/'production/batch90';E=Path('/workspace/shared/lowpoly-batch90-evidence');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
bl=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
def run(b,name,args):
 st=now();t=time.monotonic();log=E/'lifecycle-logs'/b.parent.name/(b.name+'-'+name+'.log');log.parent.mkdir(parents=True,exist_ok=True)
 if log.exists():log=log.with_name(log.stem+'-retry-'+str(time.time_ns())+log.suffix)
 with log.open('x') as f:
  proc=subprocess.Popen(args,cwd=R,stdout=f,stderr=subprocess.STDOUT);code=proc.wait(timeout=3600)
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(dict(stage=name,runner_pid=proc.pid,started_at=st,ended_at=now(),wall_seconds=time.monotonic()-t,exit_code=code,command=args,log=str(log),log_sha256=H(log)))+'\n')
 print(b.parent.name,b.name,name,code,flush=True)
 if code:raise RuntimeError(str(b)+' '+name)
selected=json.loads((P/'final-selection.json').read_text())
for x in selected:
 b=R/x['path'];aid=x['asset_id'];rev=x['revision'];assert json.loads((b/'diagnostic-disposition.json').read_text())['status']=='selected-for-full-lifecycle';assert json.loads((b/'source-vertex-counts.json').read_text())['all_numeric_checks_pass']
 orig=b.parent/'r001';f=json.loads((orig/'modeling-freeze.json').read_text());assert all(H(orig/n)==h for n,h in f['files'].items());assert H(b/'brief.json')==H(orig/'brief.json') and H(b/'references.json')==H(orig/'references.json')
 if not (b/'gltf-validator.report.json').exists():run(b,'khronos',['node','scripts/validate_gltf.cjs',str(b/'model.glb')])
 if not (b/'source-final.report.json').exists():run(b,'source-reopen',bl+[str(R/'scripts/check_source_export.py'),'--','--source',str(b/'source.blend'),'--glb',str(b/'model.glb'),'--output',str(b/'source-final.report.json'),'--collection','EXPORT'])
 if not (b/'runtime-parse.report.json').exists():run(b,'runtime-parse',['node',str(P/'runtime-parse.mjs'),str(b)])
 for i in [1,2]:
  job={'asset_id':aid,'revision':rev,'job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(b/'generator.py'),'config':str(b/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py'),'brief':str(b/'brief.json'),'references':str(b/'references.json')},'argv':['{blender}','--factory-startup','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json','execution.json']}
  q=E/('queue-'+aid+'-'+rev+'-'+str(i)+'.json')
  if not q.exists():q.write_text(json.dumps(dict(schema_version=1,lane='build',jobs=[job]),indent=2)+'\n')
  if not (b/('repro-final-'+str(i)+'.report.json')).exists():
   run(b,'queue-'+str(i),['flock','/tmp/lowpoly-production-blender.lock','python3','scripts/run_asset_queue.py',str(q),'--runs-root',str(E/'rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','120','--resume'])
   matches=[]
   for result in (E/'rebuild-runs/build'/aid/rev).rglob('result.json'):
    res=json.loads(result.read_text());request=json.loads((result.parent/'request.json').read_text());inputs=request['identity']['inputs']
    if res.get('status')=='succeeded' and res.get('job_id')==job['job_id'] and inputs['generator']['sha256']==H(b/'generator.py') and inputs['config']['sha256']==H(b/'build-config.json'):matches.append(result)
   assert len(matches)==1,matches;result=matches[0]
   snapshot=P/'rebuild-evidence'/aid/rev/('semantic-rebuild-'+str(i));snapshot.mkdir(parents=True,exist_ok=True)
   for name in ['request.json','result.json','stdout.log','stderr.log']:
    src=result.parent/name;dst=snapshot/name
    if src.exists() and not dst.exists():shutil.copyfile(src,dst)
    if src.exists():assert H(src)==H(dst)
   if not (snapshot/'execution.json').exists():shutil.copyfile(result.parent/'outputs/execution.json',snapshot/'execution.json')
   if not (snapshot/'byte-identity.json').exists():(snapshot/'byte-identity.json').write_text(json.dumps({'original_run_dir':str(result.parent),'recorded_at':now(),'note':'Byte-identical copies only. Original queue records, output GLB/Blend and logs retained locally. No execution time or subject rebinding.','files':{n:H(snapshot/n) for n in ['request.json','result.json','stdout.log','stderr.log','execution.json']}},indent=2)+'\n')
   run(b,'repro-'+str(i),['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(snapshot/'request.json'),'--build-result',str(snapshot/'result.json'),'--rebuilt-output','model.glb','--root',str(R),'--output',str(b/('repro-final-'+str(i)+'.report.json'))])
 if not (b/'build-dependencies.json').exists():
  dep=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py'];(b/'build-dependencies.json').write_text(json.dumps(dict(blender='/usr/bin/blender',blender_version='4.3.2',threads=2,python='Blender bundled Python',inputs={str(p.relative_to(R)):H(p) for p in dep},node_dependency_root='/workspace/shared/lowpoly-landair-web-integration/node_modules',three_version='0.180.0',node_lockfile_sha256=H(R/'package-lock.json'),created_at=now()),indent=2)+'\n')
 if not (b/'candidate-brief.json').exists():
  d=json.loads((b/'brief.json').read_text());d['packaging_adapter']=dict(created_at=now(),frozen_design_brief_sha256=H(b/'brief.json'),note='Derived postbuild source/generator/config closure only. Original complete design and ledger byte-identical.');d['required_deliverables']=[dict(role=k,path=str((b/n).relative_to(R)),sha256=H(b/n)) for k,n in [('source','source.blend'),('generator','generator.py'),('config','build-config.json')]];(b/'candidate-brief.json').write_text(json.dumps(d,indent=2)+'\n')
 d=json.loads((b/'candidate-brief.json').read_text());assert all(H(R/v['path'])==v['sha256'] for v in d['required_deliverables']);refs=json.loads((b/'references.json').read_text());assert refs['no_incorporated_third_party_assets'] and all(v.get('rights_note') for v in refs['sources'])
 sys.path.insert(0,str(R/'scripts'));from validate_candidate import check_brief,STATIC_PROFILE
 check_brief(d,{'asset_id':aid},set(s['id'] for s in refs['sources']),STATIC_PROFILE)
 if not (b/'preproof-binding.json').exists():(b/'preproof-binding.json').write_text(json.dumps(dict(checked_at=now(),glb_sha256=H(b/'model.glb'),brief_sha256=H(b/'candidate-brief.json'),references_sha256=H(b/'references.json'),original_freeze_unchanged=True,source_generator_config_binding='pass',source_geometry_check='pass'),indent=2)+'\n')
 if not (b/'proof-final/render-manifest.json').exists():run(b,'proof-final',bl+[str(P/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',rev,'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','32'])
 shutil.copyfile(b/'proof-final/hero.png',b/'preview.png');print('LIFECYCLE_COMPLETE',aid,flush=True)
