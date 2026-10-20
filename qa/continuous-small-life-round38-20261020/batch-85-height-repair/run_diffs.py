import subprocess,json,datetime
from pathlib import Path
O=Path(__file__).parent;N=Path('/workspace/shared/lowpoly-batch85-height-repair-20261020');R=Path('/workspace/shared/lowpoly-batch85-20261020');records=[]
for aid,old,new in [('piedmont-glacier','r004','r005'),('lava-channel','r002','r003'),('karst-polje','r002','r003')]:
 args=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(O/'source_diff.py'),'--',str(R/'production/small-life-batch85'/aid/old/'artifacts'/(aid+'.blend')),str(N/'production/small-life-batch85-height-repair'/aid/new/'artifacts'/(aid+'.blend')),str(O/aid/'source-difference.json'),aid]
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/aid/'source-difference.log').open('x') as f:p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
 records.append({'asset_id':aid,'runner_pid':p.pid,'started_at':t,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':args,'exit_code':code});(O/'difference-processes.json').write_text(json.dumps(records,indent=2)+'\n');print(aid,code,flush=True)
