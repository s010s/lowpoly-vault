# SPDX-License-Identifier: MIT
import subprocess,pathlib,json,datetime,time,hashlib
r=pathlib.Path.cwd();w=r/'production/small-life-batch79'
for x in json.loads((w/'final-selection.json').read_text()):
 b=r/x['path']
 while not (b/'source.blend').exists():time.sleep(2)
 if (b/'physical-surfaces.report.json').exists():
  d=json.loads((b/'physical-surfaces.report.json').read_text());assert d['status']=='pass' and d['source_sha256']==hashlib.sha256((b/'source.blend').read_bytes()).hexdigest() and d['glb_sha256']==hashlib.sha256((b/'model.glb').read_bytes()).hexdigest();continue
 args=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(w/'check-physical-surfaces.py'),'--',str(b)]
 t=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (b/'physical-surfaces.log').open('w') as f:p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
 with (w/'physical-jobs.jsonl').open('a') as f:f.write(json.dumps({'asset_id':x['asset_id'],'revision':x['revision'],'runner_pid':p.pid,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':code,'command':args})+'\n')
 print(x['asset_id'],code,flush=True)
 if code:raise RuntimeError(str(b)+' physical surfaces failed')
