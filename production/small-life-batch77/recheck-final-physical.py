from pathlib import Path
import json,subprocess,datetime,shutil,time
R=Path.cwd();W=R/'production/small-life-batch77';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path']
 for n in ['physical-surfaces.report.json','physical-surfaces.log']:
  if (b/n).exists():shutil.copyfile(b/n,b/('initial-'+n))
 argv=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'check-physical-surfaces.py'),'--',str(b)]
 start=now();t=time.monotonic()
 with (b/'physical-surfaces.log').open('w') as f:p=subprocess.Popen(argv,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':'post-pixel-final-physical-check','runner_pid':p.pid,'started_at':start,'ended_at':now(),'wall_seconds':time.monotonic()-t,'exit_code':code,'command':argv})+'\n')
 assert code==0,x
 print(x['asset_id'],'final physical pass',flush=True)
