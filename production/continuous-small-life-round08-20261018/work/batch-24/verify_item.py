# SPDX-License-Identifier: MIT
"""Bounded live verification of exact delivered source and two real rebuilds."""
import sys,json,hashlib,subprocess
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
s=sys.argv[1];b=Path(__file__).resolve().parent;w=b/s/'r001';attempt=json.loads((w/'config.json').read_text()).get('selected_attempt','attempt-01');d=ROOT/f'assets/candidates/continuous-small-life-round08-20261018/batch-24/{s}/r001/{attempt}/{s}'
def run(cmd,name):
 with (w/name).open('w') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=900)
run(['python3','scripts/run_asset_queue.py',str(w/'rebuild-jobs.json'),'--runs-root',str(w/'rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2'],'two-rebuilds.txt')
a=audit_glb(d/(s+'.glb'),14000,6,30);reports=[]
for result_path in sorted((w/'rebuild-runs').rglob('result.json')):
 result=json.loads(result_path.read_text());request=json.loads((result_path.parent/'request.json').read_text())
 if request['identity']['inputs']['generator']['sha256']!=hashlib.sha256((w/'generator.py').read_bytes()).hexdigest():continue
 assert result['status']=='succeeded',result
 output=result_path.parent/'outputs'/s/(s+'.glb');q=audit_glb(output,14000,6,30)
 reports.append({'result_path':str(result_path.relative_to(ROOT)),'result_sha256':hashlib.sha256(result_path.read_bytes()).hexdigest(),'glb_path':str(output.relative_to(ROOT)),'glb_sha256':q['sha256'],'bytes':q['bytes'],'semantic_sha256':q['semantic_sha256'],'semantic_match':q['semantic_sha256']==a['semantic_sha256'],'byte_match':q['sha256']==a['sha256']})
assert len(reports)==2 and all(q['semantic_match'] for q in reports)
report={'status':'pass','check':'two_actual_semantic_rebuilds','delivered_glb_sha256':a['sha256'],'semantic_sha256':a['semantic_sha256'],'runs':reports,'limitation':'Decoded geometry/material/scene equality; Blend byte identity and independent visual/factual acceptance are separate.'}
(w/'reproducibility.json').write_text(json.dumps(report,indent=2)+'\n')
if (w/'source-export.json').exists():
 (w/'source-export.json').rename(w/'source-export-initial.json')
run(['blender','-b','-t','2','--disable-autoexec','--python-exit-code','1','--python','scripts/check_source_export.py','--','--source',str(d/(s+'.blend')),'--glb',str(d/(s+'.glb')),'--output',str(w/'source-export.json')],'source-reopen.txt')
run(['blender','-b','-t','2','--disable-autoexec','--python-exit-code','1','--python',str(b/'inspect_source.py'),'--',str(d/(s+'.blend')),str(w/'source-scene.json')],'source-scene.txt')
run(['node','scripts/validate_gltf.cjs',str(d)],'khronos.txt')
run(['node',str(b/'browser_qa.mjs'),s],'runtime.txt')
print(s,'two rebuilds, source reopen, Khronos and software browser checks completed',flush=True)
