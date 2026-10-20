# SPDX-License-Identifier: MIT
from pathlib import Path
import json,subprocess,datetime,time
R=Path.cwd();W=R/'production/continuous-small-life-round24-20261020/work/batch-62'
for x in json.loads((W/'repair-selection.json').read_text()):
 b=R/x['path']
 results=list((W/'repair-rebuild-runs/build'/x['asset_id']/x['revision']).rglob('result.json'));assert len(results)==2
 for result in results:
  d=json.loads(result.read_text());i=d['job_id'][-1];args=['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(R),'--output',str(b/('repro-final-'+i+'.report.json'))];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
  with (b/('repro-bound-'+i+'.log')).open('x') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
  with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':'repro-bound-'+i,'command':args,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':p.returncode})+'\n')
  print(x['asset_id'],i,p.returncode,flush=True);assert p.returncode==0
