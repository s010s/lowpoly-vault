from pathlib import Path
import subprocess,json,datetime,os
O=Path(__file__).parent;R=Path('/workspace/shared/lowpoly-batch81-charnia-repair-20261020');P=R/'production/small-life-batch81/assets/charnia/r006'
prefix=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
runs=[]
for name,args in [('source-reexport',prefix+[str(O/'source_reexport.py'),'--',str(R),str(P),str(O/'saved-source')]),('supplemental-topclay',prefix+[str(O/'render_supplemental_topclay.py'),'--',str(P/'model.glb'),'--output-dir',str(O/'supplemental-topclay'),'--revision','r006','--brief',str(P/'candidate-brief.json'),'--references',str(P/'references.json'),'--resolution','512','--samples','16','--turntable-frames','0','--views','clay']),('runtime',['node',str(O/'runtime_checks.mjs')])]:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(name+'.log')).open('x') as f:
  p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,cwd=R);code=p.wait()
 runs.append({'stage':name,'wrapper_pid':p.pid,'started_at':t,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':code,'command':args})
 (O/'fresh-processes.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,code,flush=True)
 if code:break
