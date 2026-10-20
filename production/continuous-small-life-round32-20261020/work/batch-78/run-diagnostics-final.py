import pathlib,json,subprocess,time,datetime
r=pathlib.Path.cwd();w=r/'production/continuous-small-life-round32-20261020/work/batch-78'
for x in json.loads((w/'final-selection.json').read_text()):
 b=r/x['path']
 while not (b/'source.blend').exists():time.sleep(1)
 for tool in ['check-coplanar.py','check-intersections.py']:
  name=tool.removesuffix('.py')
  if (b/({'check-coplanar.py':'coplanar-overlap.report.json','check-intersections.py':'intersection-diagnostic.report.json'}[tool])).exists():continue
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  with (b/(name+'.log')).open('w') as f:
   p=subprocess.Popen(['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(w/tool),'--',str(b)],stdout=f,stderr=subprocess.STDOUT);rc=p.wait()
  with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':name,'runner_pid':p.pid,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':rc})+'\n')
  print(x['asset_id'],name,rc,flush=True)
