import json,subprocess,pathlib,datetime,os
D=pathlib.Path('/workspace/shared/lowpoly-batch91-independent-qa-20261020');S=pathlib.Path('/workspace/shared/lowpoly-batch91-20261020');H=json.load(open(S/'production/small-life-batch91/maker-handoff.json'));results=[]
for item in H['items']:
 out=D/item['asset_id'];out.mkdir(exist_ok=True)
 cmd=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','--background','--threads','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python',str(D/'reopen_reexport.py'),'--',str(S/item['artifacts']['source']['path']),str(out)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (out/'reopen.log').open('w') as f:p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});code=p.wait()
 results.append({'asset_id':item['asset_id'],'argv':cmd,'requested_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wrapper_pid':p.pid,'returncode':code});(D/'reopen-jobs.json').write_text(json.dumps(results,indent=2)+'\n');print(item['asset_id'],code,flush=True)
 if code:break
