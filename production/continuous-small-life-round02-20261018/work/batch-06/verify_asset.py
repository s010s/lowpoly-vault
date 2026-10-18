# SPDX-License-Identifier: MIT
"""Run existing technical checks for one exact batch06 candidate; never approves art."""
import sys,json,hashlib,subprocess
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/qa_glb.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
s=sys.argv[1];w=ROOT/'production/continuous-small-life-round02-20261018/work/batch-06';d=w/s/'r001';attempt={'aulopora':'attempt-03','thamnopora':'attempt-03','hallucigenia':'attempt-01','fenestella':'attempt-01'}[s];asset=ROOT/'assets/candidates/continuous-small-life-round02-20261018/batch-06'/s/'r001'/attempt/s;glb=asset/(s+'.glb')
def run(cmd,out):
 with (d/out).open('x') as f:r=subprocess.run(list(map(str,cmd)),cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=240)
 if r.returncode:raise RuntimeError(str(cmd)+' failed '+str(r.returncode)+'; see '+str(d/out))
if not (d/'rebuild-runs').exists():run(['python3','scripts/run_asset_queue.py',d/'rebuild-manifest.json','--runs-root',d/'rebuild-runs','--workers','1','--threads','2','--cpu-budget','2','--memory-mb','4096'],'rebuild-run.txt')
for result in sorted((d/'rebuild-runs').rglob('result.json')):
 r=json.loads(result.read_text());assert r['status']=='succeeded',r;rebuilt=result.parent/'outputs'/s/(s+'.glb');run(['python3','scripts/check_reproducibility.py','--glb',glb,'--rebuilt-glb',rebuilt,'--generator',w/'build_batch06.py','--config',d/'config.json','--build-request',result.parent/'request.json','--build-result',result,'--rebuilt-output',s+'/'+s+'.glb','--root',ROOT,'--output',d/(r['job_id']+'.json')],r['job_id']+'.txt')
run(['blender','-b','-t','2','--disable-autoexec','--python-exit-code','1','--python','scripts/check_source_export.py','--','--source',asset/(s+'.blend'),'--glb',glb,'--output',d/'source-export.json'],'source-export.txt')
run(['blender','-b','-t','2','--disable-autoexec','--python-exit-code','1','--python','scripts/check_glb_roundtrip.py','--',glb,'--output-dir',d/'roundtrip','--no-render'],'roundtrip.txt')
run(['node','scripts/validate_gltf.cjs',glb],'khronos.txt')
a=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30);assert not a['errors'];(d/'project-audit.json').write_text(json.dumps(a,indent=2)+'\n')
print(s,a['sha256'],a['bytes'],a['scene_triangles'],flush=True)
