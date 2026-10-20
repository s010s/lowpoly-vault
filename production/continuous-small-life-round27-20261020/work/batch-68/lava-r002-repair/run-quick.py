import json,subprocess,pathlib,datetime,time
R=pathlib.Path.cwd();W=R/'production/continuous-small-life-round27-20261020/work/batch-68/lava-r002-repair';bl=['flock','/tmp/lowpoly-production-blender.lock','blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path']
 for stage,cmd in [('build',bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(b)]),('quick',bl+[str(W.parent/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision','r002','--brief',str(b/'brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-quick'),'--views','hero,top','--turntable-frames','0','--resolution','256','--samples','6'])]:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
  with (b/(stage+'.log')).open('w') as f:p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT);code=p.wait(timeout=1200)
  with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':stage,'command':cmd,'runner_pid':p.pid,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':code})+'\n')
  print(x['asset_id'],stage,code,flush=True)
  if code:raise RuntimeError(x['asset_id']+stage)
