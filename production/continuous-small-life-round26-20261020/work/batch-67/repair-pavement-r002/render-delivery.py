from pathlib import Path
import json,subprocess,datetime,time
R=Path.cwd();W=R/'production/continuous-small-life-round26-20261020/work/batch-67/repair-pavement-r002'
for x in json.load(open(W/'final-selection.json')):
 b=R/x['path'];cmd=[str(W/'blender-locked.sh'),'-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.delivery-v001.json'),'--output-dir',str(b/'proof-delivery'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16']
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with (b/'proof-delivery.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=500)
 with (W/'delivery-render-runs.jsonl').open('a') as f:f.write(json.dumps({'asset_id':x['asset_id'],'revision':x['revision'],'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'returncode':p.returncode,'command':cmd})+'\n')
 print(x['asset_id'],p.returncode,flush=True)
 if p.returncode:raise RuntimeError(x['asset_id'])
