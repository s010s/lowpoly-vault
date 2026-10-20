import subprocess,json,datetime,time,pathlib,os
out=pathlib.Path(__file__).parent
root=pathlib.Path('/workspace/shared/lowpoly-batch82-stratovolcano-repair-20261020')
src=root/'production/batch82-stratovolcano-repair/stratovolcano/r009'
c=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(out/'source_reexport.py'),'--',str(root),str(src),str(out/'saved-source')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with (out/'source-reexport.log').open('x') as log:
 p=subprocess.Popen(c,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});rc=p.wait()
e={'command':c,'runner_pid':p.pid,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':rc}
(out/'fresh-process.json').write_text(json.dumps(e,indent=2)+'\n');print(e);raise SystemExit(rc)
