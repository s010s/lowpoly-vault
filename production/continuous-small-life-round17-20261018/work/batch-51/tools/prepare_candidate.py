import json,sys,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path('/workspace/lowpoly-vault');W=R/'production/continuous-small-life-round17-20261018/work/batch-51';aid=sys.argv[1];rev=sys.argv[2] if len(sys.argv)>2 else 'r001';a=R/'assets/candidates/continuous-small-life-round17-20261018/batch-51'/aid/rev

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
b=json.loads((a/'brief.json').read_text());b['brief_version']=b['brief_version']+'-candidate-contract-v001';b['construction_plan']={'path':'brief.json','sha256':sha(a/'brief.json'),'freeze':'derived-freeze.json','freeze_sha256':sha(a/'derived-freeze.json')};b['candidate_contract_note']='Post-build artifact identity freeze only. The concept-led structural plan was frozen before execution; source, GLB, config and generator are unchanged. Adds exact required deliverable hashes, without lowering or changing any model/QA requirement.'
artifacts={k:pin(a/v) for k,v in {'glb':aid+'.glb','source':aid+'.blend','generator':'generator.py','config':'build-config.json','references':'references.json'}.items()}
b['required_deliverables']=[{'role':role,**artifacts[role]} for role in ['source','generator','config']];save(a/'candidate-brief.json',b);artifacts['brief']=pin(a/'candidate-brief.json')
freeze={'schema_version':1,'kind':'candidate-artifact-freeze','asset_id':aid,'revision':rev,'frozen_at':datetime.now(timezone.utc).isoformat(),'derived_plan_freeze':pin(a/'derived-freeze.json'),'artifacts':artifacts,'status':'candidate; independent QA pending','hardware_gpu_verified':False,'parent_scene_verified':False};save(a/'candidate-freeze.json',freeze)
cmd=['blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'tools/render_views.py'),'--',str(a/(aid+'.glb')),'--revision',rev,'--brief',str(a/'candidate-brief.json'),'--references',str(a/'references.json'),'--output-dir',str(a/'candidate-proof'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','8']
if rev=='r002':cmd+=['--camera-config',str(a.parent/'r001/proof/render-config.json')]
with (a/'candidate-render.stdout.txt').open('w') as f:subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True)
print('FINAL_CANDIDATE_PROOF_READY',aid,rev)
