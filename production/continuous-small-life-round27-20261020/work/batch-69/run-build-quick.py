# SPDX-License-Identifier: MIT
import pathlib,json,subprocess,datetime,time
R=pathlib.Path.cwd();W=R/'production/continuous-small-life-round27-20261020/work/batch-69';bl=['flock','/tmp/lowpoly-production-blender.lock','blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
def run(name,args,log):
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with log.open('w') as f:p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
 event={'stage':name,'runner_pid':p.pid,'started_at':started,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':code,'command':args}
 with (W/'early-lifecycle.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
 print(name,code,flush=True);assert code==0
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];slug=x['asset_id']
 if not (b/'model.glb').exists():run('build-'+slug,bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(b)],b/'build.log')
 run('quick-'+slug,bl+[str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision','r001','--output-dir',str(b/'quick'),'--views','hero,reversehero,top'+(',bottom' if slug=='wiwaxia' else ''),'--resolution','256','--samples','8','--turntable-frames','0'],b/'quick.log')
