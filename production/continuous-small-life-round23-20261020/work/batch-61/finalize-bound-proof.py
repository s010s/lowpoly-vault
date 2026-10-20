# SPDX-License-Identifier: MIT
from pathlib import Path
import json,subprocess,time,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round23-20261020/work/batch-61';final=json.loads((W/'final-selection.json').read_text());bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
def run(b,name,args):
 t=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (b/(name+'.log')).open('x') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=600)
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':name,'command':args,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':p.returncode})+'\n')
 print(b.parent.name,name,p.returncode,flush=True);assert p.returncode==0
for x in final:
 b=R/x['path']
 if x['revision']=='r003':
  run(b,'format',['node','scripts/validate_gltf.cjs',str(b/'model.glb')]);run(b,'source-reopen',bl+['scripts/check_source_export.py','--','--source',str(b/'source.blend'),'--glb',str(b/'model.glb'),'--output',str(b/'source-final.report.json'),'--collection','EXPORT'])
 run(b,'proof-bound',bl+[str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16']);shutil.copyfile(b/'proof-final/hero.png',b/'preview.png')
 if x['revision']=='r003':run(b,'head-detail',bl+[str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-head-detail'),'--views','detail','--detail-target','.5,.18,.58','--detail-scale','.35','--turntable-frames','0','--resolution','512','--samples','24'])
run(W,'runtime-final',['node',str(W/'runtime-parse.mjs')]+[str(R/x['path']) for x in final])
x=final[0];b=R/x['path'];jobs=[]
for i in [1,2]:jobs.append({'asset_id':x['asset_id'],'revision':x['revision'],'job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(b/'generator.py'),'config':str(b/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py')},'argv':['{blender}','--factory-startup','--disable-autoexec','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json']})
(W/'rebuild-r003-jobs.json').write_text(json.dumps({'schema_version':1,'lane':'build','jobs':jobs},indent=2)+'\n');run(W,'rebuild-r003-queue',['python3','scripts/run_asset_queue.py',str(W/'rebuild-r003-jobs.json'),'--runs-root',str(W/'rebuild-r003-runs'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','180'])
for result in (W/'rebuild-r003-runs/build/pseudopulex/r003').rglob('result.json'):
 i=json.loads(result.read_text())['job_id'][-1];run(b,'repro-bound-'+i,['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(R),'--output',str(b/('repro-final-'+i+'.report.json'))])
run(W,'source-counts-final',bl+[str(W/'count-source-vertices.py')])
