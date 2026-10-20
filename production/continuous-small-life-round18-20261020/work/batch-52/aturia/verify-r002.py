from pathlib import Path
import subprocess,json,shutil,time
R=Path('/workspace/lowpoly-vault');W=R/'production/continuous-small-life-round18-20261020/work/batch-52/aturia';O=R/'assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002';L=W/'logs-r002';L.mkdir(exist_ok=True)
def run(argv,name):
 t=time.monotonic()
 with (L/(name+'.log')).open('w') as out:p=subprocess.run([str(x) for x in argv],cwd=R,stdout=out,stderr=subprocess.STDOUT)
 print(name,p.returncode,time.monotonic()-t,flush=True)
 if p.returncode:raise RuntimeError(name)
initial=next((W/'runs-r002/build/aturia/r002/initial-build').glob('*/*/outputs'))
for p in initial.iterdir():shutil.copy2(p,O/p.name)
shutil.copy(W/'build-r002.py',O/'generator.py')
shutil.copy(O/'qa.json',O/'source-qa.json')
for i in [1,2]:
 req=next((W/('runs-r002/build/aturia/r002/semantic-rebuild-'+str(i))).glob('*/*/request.json'))
 run(['python3','scripts/check_reproducibility.py','--glb',O/'aturia.glb','--rebuilt-glb',req.parent/'outputs/aturia.glb','--generator',W/'build-r002.py','--config',O/'config.json','--build-request',req,'--build-result',req.parent/'result.json','--rebuilt-output','aturia.glb','--root',R,'--output',O/('reproducibility-'+str(i)+'.report.json')],'rebuild-'+str(i))
run(['flock','/tmp/batch52-blender.lock','blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python','scripts/check_source_export.py','--','--source',O/'aturia.blend','--glb',O/'aturia.glb','--output',O/'source-export.report.json'],'source-export')
run(['flock','/tmp/batch52-blender.lock','blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',W/'inspect_source.py','--',O/'aturia.blend',O/'source-mesh-measurements.json'],'source-measure')
run(['node','scripts/validate_gltf.cjs',O/'aturia.glb'],'khronos')
run(['flock','/tmp/batch52-blender.lock','blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',W/'render.py','--',O/'aturia.glb','--revision','r002','--brief',O/'brief-production.json','--references',O/'references.json','--output-dir',O/'proof','--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'],'render')
