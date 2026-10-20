# SPDX-License-Identifier: MIT
import subprocess,pathlib,json,datetime,time,sys,shutil
R=pathlib.Path.cwd();base=R/'assets/candidates/continuous-small-life-round21-20261020/batch-56';W=R/'production/continuous-small-life-round21-20261020/work/batch-56'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(b,name,args):
 started=now();t=time.monotonic()
 with (b/(name+'.log')).open('w') as log:
  try:p=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,timeout=240);code=p.returncode
  except subprocess.TimeoutExpired:code=124
 event={'stage':name,'started_at':started,'ended_at':now(),'wall_seconds':time.monotonic()-t,'exit_code':code,'command':args}
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
 print(b.parent.name,name,code,round(event['wall_seconds'],2),flush=True);return code
bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
for slug in ['cycadeoidea','gondwanagaricites','deflation-hollow','arthrophycus-annulated-burrow']:
 b=base/slug/'r001';start=json.loads((b/'model-start.json').read_text());start['geometry_process_started_at']=now();(b/'model-start.json').write_text(json.dumps(start,indent=2)+'\n')
 if run(b,'build',bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(b)]):continue
 run(b,'format',['node','scripts/validate_gltf.cjs',str(b/'model.glb')])
 run(b,'source-reopen',bl+['scripts/check_source_export.py','--','--source',str(b/'source.blend'),'--glb',str(b/'model.glb'),'--output',str(b/'source-export.report.json'),'--collection','EXPORT'])
 for n in [1,2]:
  dest=W/slug/'r001'/('rebuild-'+str(n));dest.mkdir(parents=True,exist_ok=True)
  if not run(b,'rebuild-'+str(n),bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(dest)]):
   run(b,'repro-'+str(n),['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(dest/'model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--root',str(R),'--output',str(b/('repro-'+str(n)+'.report.json'))])
 # Silhouette isn't implemented by standard renderer, separately render exact GLB emission silhouette below.
 run(b,'proof',bl+[str(W/'render-batch56.py'),'--',str(b/'model.glb'),'--revision','r001','--brief',str(b/'brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','12'])
