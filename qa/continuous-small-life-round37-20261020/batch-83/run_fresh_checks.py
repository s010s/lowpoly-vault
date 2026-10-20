import os,json,subprocess,datetime,pathlib,sys,time
r=pathlib.Path('/workspace/shared/lowpoly-batch83-20261020');out=pathlib.Path(__file__).parent;os.environ['PYTHONDONTWRITEBYTECODE']='1';runs=[]
for a in json.load(open(r/'production/small-life-batch83/handoff.json'))['assets']:
 p=r/a['path'];name=a['asset_id'];d=out/name;d.mkdir(exist_ok=True)
 c=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(out/'source_reexport.py'),'--',str(r),str(p),str(d/'saved-source')]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with (d/'source-reexport.log').open('x') as log:
  proc=subprocess.Popen(c,stdout=log,stderr=subprocess.STDOUT);code=proc.wait()
 event={'asset_id':name,'command':c,'runner_pid':proc.pid,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':code};runs.append(event);(out/'fresh-processes.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,code,flush=True)
 if code:raise SystemExit(code)
