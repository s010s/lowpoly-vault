import pathlib,subprocess,json,time,datetime,os
r=pathlib.Path('/workspace/shared/lowpoly-batch92-20261020');out=pathlib.Path('/workspace/shared/lowpoly-batch92-independent-qa-20261020');records=[]
for a in json.load(open(r/'production/batch92/handoff-assets.json')):
 d=out/a['asset_id'];d.mkdir(exist_ok=True)
 for name,cmd in [('source',['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(out/'inspect-source.py'),'--',str(r/a['path']),str(d)]),('runtime',['node',str(out/'inspect-runtime.mjs'),str(r/a['path']/'model.glb'),str(d)])]:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
  with (d/(name+'.log')).open('w') as f:
   p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});code=p.wait()
  records.append(dict(asset=a['asset_id'],stage=name,cmd=cmd,runner_pid=p.pid,started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed=time.monotonic()-t,exit_code=code));(out/'execution.json').write_text(json.dumps(records,indent=2)+'\n')
  print(a['asset_id'],name,code,flush=True)
