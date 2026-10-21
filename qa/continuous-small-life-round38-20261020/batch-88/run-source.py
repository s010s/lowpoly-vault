from pathlib import Path
import json,subprocess,datetime,time
Q=Path('/workspace/shared/lowpoly-batch88-independent-qa-20261020');R=Path('/workspace/shared/lowpoly-batch88-20261020')
for a in json.load(open(R/'production/batch88/handoff-assets.json')):
 out=Q/a['asset_id'];out.mkdir(exist_ok=True)
 command=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(Q/'inspect-source.py'),'--',a['asset_id'],a['revision']]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with (out/'source-inspection.log').open('w') as f:p=subprocess.Popen(command,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
 r=dict(command=command,runner_pid=p.pid,started_at=start,ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=time.monotonic()-t,exit_code=code)
 (out/'source-run.json').write_text(json.dumps(r,indent=2)+'\n');print(a['asset_id'],code,flush=True)
 if code:break
