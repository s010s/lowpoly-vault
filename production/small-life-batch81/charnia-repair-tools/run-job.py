# SPDX-License-Identifier: MIT
import json,datetime,pathlib,subprocess,sys,time
out=pathlib.Path(sys.argv[1]);name=sys.argv[2];cmd=sys.argv[3:];log=out/(name+'.log');assert not log.exists();start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with log.open('x') as f:
 p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
event={'stage':name,'pid':p.pid,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':code,'command':cmd}
with (out/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
print(json.dumps(event),flush=True);sys.exit(code)
