# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess,json,time,shutil
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());W=Path(__file__).resolve().parent;O=R/'assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003';B=O.with_name('r002');L=W/'logs';L.mkdir(exist_ok=True)
records=[]
def run(argv,name):
 t=time.monotonic()
 with (L/(name+'.log')).open('x') as out:r=subprocess.run([str(x) for x in argv],cwd=R,stdout=out,stderr=subprocess.STDOUT)
 rec={'name':name,'argv':[str(x) for x in argv],'returncode':r.returncode,'wall_seconds':time.monotonic()-t};records.append(rec);(W/'verification-commands.json').write_text(json.dumps(records,indent=2)+'\n');print(name,r.returncode,round(rec['wall_seconds'],3),flush=True);assert r.returncode==0,name
run(['python3',W/'check_color_only.py',B/'aturia.glb',O/'aturia.glb',O/'color-only.report.json'],'color-only')
for i in [1,2]:
 req=next((W/('runs/build/aturia/r003/semantic-rebuild-'+str(i))).glob('*/*/request.json'))
 run(['python3',R/'scripts/check_reproducibility.py','--glb',O/'aturia.glb','--rebuilt-glb',req.parent/'outputs/aturia.glb','--generator',O/'generator.py','--config',O/'config.json','--build-request',req,'--build-result',req.parent/'result.json','--rebuilt-output','aturia.glb','--root',R,'--output',O/('reproducibility-'+str(i)+'.report.json')],'rebuild-'+str(i))
bl=['blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
run([*bl,R/'scripts/check_source_export.py','--','--source',O/'aturia.blend','--glb',O/'aturia.glb','--output',O/'source-export.report.json'],'source-export')
run([*bl,W.parent/'inspect_source.py','--',O/'aturia.blend',O/'source-mesh-measurements.json'],'source-measure')
run(['python3',R/'scripts/qa_glb.py',O/'aturia.glb','--max-triangles','14000','--max-materials','6','--max-primitives','30','--report',O/'static-glb.report.json'],'static-glb')
run(['node',R/'scripts/validate_gltf.cjs',O/'aturia.glb'],'khronos')
run([*bl,W.parent/'render.py','--',O/'aturia.glb','--revision','r003','--brief',O/'brief.json','--references',O/'references.json','--output-dir',O/'proof','--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'],'render')
