from pathlib import Path
import json,subprocess,datetime,time
R=Path.cwd();W=R/'production/small-life-batch77'
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path']
 if not (b/'source.blend').exists() or (b/'physical-surfaces.report.json').exists():continue
 argv=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'check-physical-surfaces.py'),'--',str(b)]
 with (b/'physical-surfaces.log').open('w') as log:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT);code=p.wait()
 print(x['asset_id'],code,flush=True)
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(dict(stage='physical-surfaces',runner_pid=p.pid,started_at=start,ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=code,command=argv))+'\n')
