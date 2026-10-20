from pathlib import Path
import json,subprocess,shutil,datetime
R=Path('/workspace/lowpoly-vault');W=R/'production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn';A=R/'assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003'
p=next((W/'r003-build-runs/build/cave-popcorn/r003/initial-build').glob('*/*/result.json')).parent
for n in ['cave-popcorn.blend','cave-popcorn.glb','metadata.json','qa.json']:shutil.copy2(p/'outputs/cave-popcorn'/n,A/n)
def run(name,cmd,lock=False):
 if lock:cmd=['flock','/tmp/batch52-blender.lock']+cmd
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (W/(name+'.log')).open('w') as f:r=subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT)
 (W/(name+'-execution.json')).write_text(json.dumps({'command':cmd,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':r.returncode},indent=2)+'\n')
 if r.returncode:raise RuntimeError(name+' failed '+str(r.returncode))
bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
run('r003-render',bl+[str(W/'renderer/render_candidate_views.py'),'--',str(A/'cave-popcorn.glb'),'--revision','r003','--brief',str(A/'brief.json'),'--references',str(A/'references.json'),'--output-dir',str(A/'proof'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'],True)
run('r003-source-reopen',bl+[str(R/'scripts/check_source_export.py'),'--','--source',str(A/'cave-popcorn.blend'),'--glb',str(A/'cave-popcorn.glb'),'--output',str(A/'source-export.report.json')],True)
jobs=json.loads((W/'r003-build-jobs.json').read_text());j=jobs['jobs'][0];j['job_id']='rebuild-1';j2=json.loads(json.dumps(j));j2['job_id']='rebuild-2';jobs['jobs']=[j,j2];(W/'r003-rebuild-jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
run('r003-rebuild',['python',str(R/'scripts/run_asset_queue.py'),str(W/'r003-rebuild-jobs.json'),'--runs-root',str(W/'r003-rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2'],True)
for i in [1,2]:
 p=next((W/'r003-rebuild-runs/build/cave-popcorn/r003'/f'rebuild-{i}').glob('*/*/result.json')).parent
 run(f'r003-rebuild-{i}-comparison',['python',str(R/'scripts/check_reproducibility.py'),'--glb',str(A/'cave-popcorn.glb'),'--rebuilt-glb',str(p/'outputs/cave-popcorn/cave-popcorn.glb'),'--generator',str(A/'generator.py'),'--config',str(A/'build-config.json'),'--build-request',str(p/'request.json'),'--build-result',str(p/'result.json'),'--rebuilt-output','cave-popcorn/cave-popcorn.glb','--root',str(R),'--output',str(A/f'rebuild-{i}.report.json')])
run('r003-khronos',['node',str(R/'scripts/validate_gltf.cjs'),str(A/'cave-popcorn.glb')])
