# SPDX-License-Identifier: MIT
"""Actual bounded rebuild, source reopen, and clean GLB import; no review verdict."""
import subprocess,sys,json,hashlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
GEN=Path(__file__).with_name('build_batch01.py')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for a in sys.argv[1:]:
 d=ROOT/'assets/candidates/continuous-small-life-20261018/batch-01'/a/'r001';ev=d/'evidence/technical';ev.mkdir(parents=True,exist_ok=True);scratch=ROOT/'production/continuous-small-life-20261018/work/batch-01'/a/'r001/rebuild';config=ROOT/'production/continuous-small-life-20261018/items'/a/'build-config.json'
 commands=[('rebuild',['blender','-b','-t','2','--python-exit-code','1','--python',str(GEN),'--','--asset',a,'--config',str(config),'--output',str(scratch)]),('source-reopen',['blender','-b','-t','2','--disable-autoexec','--python-exit-code','1','--python','scripts/check_source_export.py','--','--source',str(d/(a+'.blend')),'--glb',str(d/(a+'.glb')),'--output',str(ev/'source-export.report.json')]),('clean-import',['blender','-b','-t','2','--factory-startup','--python-exit-code','1','--python','scripts/check_glb_roundtrip.py','--',str(d/(a+'.glb')),'--output-dir',str(ev),'--no-render'])]
 runs=[]
 for label,cmd in commands:
  start=time.monotonic()
  with (ev/(label+'.txt')).open('w') as f:r=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
  runs.append({'label':label,'argv':cmd,'returncode':r.returncode,'wall_seconds':round(time.monotonic()-start,3),'log':label+'.txt'});assert r.returncode==0,(a,label)
 x=audit_glb(d/(a+'.glb'),14000,6,30);y=audit_glb(scratch/a/(a+'.glb'),14000,6,30)
 report={'status':'pass' if x['semantic_sha256']==y['semantic_sha256'] else 'fail','glb_sha256':x['sha256'],'rebuilt_glb_sha256':y['sha256'],'semantic_sha256':x['semantic_sha256'],'rebuilt_semantic_sha256':y['semantic_sha256'],'semantic_match':x['semantic_sha256']==y['semantic_sha256'],'byte_identical':x['sha256']==y['sha256'],'generator_sha256':h(GEN),'config_sha256':h(config),'helper_sha256':h(ROOT/'scripts/asset_common.py'),'commands':runs,'scope':'Actual separately executed deterministic build, decoded geometry/material/scene semantic comparison; source archive byte identity not required. No independent visual or scientific verdict.'}
 (ev/'reproducibility.report.json').write_text(json.dumps(report,indent=2)+'\n');assert report['status']=='pass'
 print(a,'rebuild/reopen/import pass',flush=True)
