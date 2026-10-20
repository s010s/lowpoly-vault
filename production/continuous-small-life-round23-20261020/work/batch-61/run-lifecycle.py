# SPDX-License-Identifier: MIT
import subprocess,pathlib,json,datetime,time,shutil
R=pathlib.Path.cwd();W=R/'production/continuous-small-life-round23-20261020/work/batch-61';final=json.loads((W/'final-selection.json').read_text());now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(b,name,args,timeout=300):
 started=now();t=time.monotonic()
 with (b/(name+'.log')).open('x') as log:
  try:p=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,timeout=timeout);code=p.returncode
  except subprocess.TimeoutExpired:code=124
 event={'stage':name,'started_at':started,'ended_at':now(),'wall_seconds':time.monotonic()-t,'exit_code':code,'command':args}
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
 print(b.parent.name,name,code,round(event['wall_seconds'],2),flush=True)
 if code:raise RuntimeError(str(b)+' '+name)
bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
for x in final:
 b=R/x['path'];slug=x['asset_id']
 run(b,'build',bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(b)])
 run(b,'format',['node','scripts/validate_gltf.cjs',str(b/'model.glb')])
 run(b,'source-reopen',bl+['scripts/check_source_export.py','--','--source',str(b/'source.blend'),'--glb',str(b/'model.glb'),'--output',str(b/'source-final.report.json'),'--collection','EXPORT'])
 run(b,'proof-final',bl+[str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'],timeout=600)
 shutil.copyfile(b/'proof-final/hero.png',b/'preview.png')
run(W,'runtime',['node',str(W/'runtime-parse.mjs')]+[str(R/x['path']) for x in final])
jobs=[]
for x in final:
 b=R/x['path']
 for i in [1,2]:jobs.append({'asset_id':x['asset_id'],'revision':x['revision'],'job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(b/'generator.py'),'config':str(b/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py')},'argv':['{blender}','--factory-startup','--disable-autoexec','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json']})
(W/'rebuild-jobs.json').write_text(json.dumps({'schema_version':1,'lane':'build','jobs':jobs},indent=2)+'\n')
run(W,'rebuild-queue',['python3','scripts/run_asset_queue.py',str(W/'rebuild-jobs.json'),'--runs-root',str(W/'rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','180'],timeout=1800)
for x in final:
 b=R/x['path']
 for result in (W/'rebuild-runs/build'/x['asset_id']/x['revision']).rglob('result.json'):
  d=json.loads(result.read_text());i=d['job_id'][-1]
  run(b,'repro-bound-'+i,['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(R),'--output',str(b/('repro-final-'+i+'.report.json'))])
