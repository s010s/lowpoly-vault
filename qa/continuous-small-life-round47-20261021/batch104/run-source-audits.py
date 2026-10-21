from pathlib import Path
import os,json,subprocess,sys
Q=Path(__file__).resolve().parent
I=json.loads((Q/'final-intake.json').read_text());env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2',MKL_NUM_THREADS='2',NUMEXPR_NUM_THREADS='2')
for item in I['assets']:
 a=item['asset_id'];D=Q/a;D.mkdir(exist_ok=True);cmd=['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','--background','--threads','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python',str(Q/'source-audit.py'),'--',a]
 with(D/'source-audit.log').open('x')as out:r=subprocess.run(cmd,cwd=Q,env=env,stdout=out,stderr=subprocess.STDOUT)
 print(a,'source audit exit',r.returncode,flush=True)
 if r.returncode:sys.exit(r.returncode)
