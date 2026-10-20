import subprocess,time,datetime,json,sys,pathlib
W=pathlib.Path(__file__).resolve().parent;name=sys.argv[1];cmd=sys.argv[2:];now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();start=now();t=time.monotonic()
log=W/(name+'.log');assert not log.exists(),log
with log.open('w') as f:
 p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
with (W/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':name,'pid':p.pid,'started_at':start,'ended_at':now(),'seconds':time.monotonic()-t,'exit_code':code,'command':cmd})+'\n')
print(name,code,round(time.monotonic()-t,2),flush=True);sys.exit(code)
