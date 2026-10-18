# SPDX-License-Identifier: MIT
"""Current practical-profile integrity validation, deliberately no QA approval."""
from pathlib import Path
import hashlib,json,sys
from PIL import Image
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb,read_glb
WORK=ROOT/'production/continuous-small-life-20261018/work/batch-03';QA=ROOT/'qa/continuous-small-life-20261018/batch-03'
def read(p):return json.loads(p.read_text())
def verify(e):
 p=ROOT/e['path'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'],(str(p),'stale/missing evidence')
 if 'bytes' in e:assert p.stat().st_size==e['bytes']
 return p
summary=read(WORK/'result.json');rows=[]
for row in summary['assets']:
 s=row['id'];a=ROOT/row['asset_dir'];d=ROOT/row['execution_dir'];g=audit_glb(a/(s+'.glb'),14000,6,30);assert not g['errors'] and not g['warnings'];assert g['sha256']==row['glb_sha256'] and g['bytes']<=1000000
 freeze=read(d/'freeze.json')
 for e in freeze['files'].values():verify(e)
 candidate=read(d/'candidate.json');verify(candidate['freeze']);assert candidate['approval']['status']=='pending' and candidate['independent_review'] is None
 doc,_,_=read_glb(a/(s+'.glb'));assert not doc.get('images') and not doc.get('textures');assert all(not m.get('doubleSided',False) for m in doc.get('materials',[]));assert not doc.get('animations')
 official=read(a/'gltf-validator.report.json');assert official['issues']['numErrors']==official['issues']['numWarnings']==0
 q=read(a/'qa.json');assert q['source']['errors']==q['glb']['errors']==[]
 assert all(p['boundary_edges']==p['nonmanifold_edges']==0 for p in q['source']['parts'])
 for stage in ['source-export','source-metrics','reproducibility']:
  r=read(QA/s/'verification'/(stage+'.json'))
  if stage=='source-metrics':assert r['source_reopened'] and r['root_identity'] and r['scene_cameras']==r['scene_lights']==0 and not r['preview_objects']
  elif stage=='source-export':assert r['status'].startswith('pass') and r['glb_sha256']==g['sha256'] and r['triangles_match'] and r['bounds_match']
  else:
   assert r['status']=='pass' and r['glb_sha256']==g['sha256'] and r['rebuild_count']==2
   for b in r['rebuilds']:assert b['returncode']==0 and b['semantic_match'] and b['semantic_sha256']==g['semantic_sha256']
 for benchmark in [False,True]:
  r=read(QA/'browser'/(s+('-scene' if benchmark else '')+'.json'));assert r['status']=='pass' and not r['errors'] and not r['failed'];assert r['glb_sha256']==g['sha256'] and r['instances']==(9 if benchmark else 1);assert r['three']=='180' and 'SwiftShader' in r['renderer']
  b=r['loaded'][0]['bounds'];assert max(abs(b[k][i]-g['bounds_m'][k][i]) for k in ['min','max'] for i in range(3))<1e-6
  assert all(v['triangles']==g['scene_triangles']*(9 if benchmark else 1)+(2 if benchmark else 0) for v in r['views'])
 views=read(QA/(s+'-view-manifest.json'));assert views['glb_sha256']==g['sha256'] and views['turntable_frames']==0
 for e in views['frames']+views['contacts']:verify(e)
 exact=read(verify(views['exact_glb_cycles_manifest']));assert exact['glb_sha256']==g['sha256'] and exact['imported_from_glb'] and len(exact['frames'])==8
 for e in exact['frames']:verify(e)
 im=Image.open(a/'preview-hero.png');assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0
 rows.append({'id':s,'glb_sha256':g['sha256'],'bytes':g['bytes'],'triangles':g['scene_triangles'],'fixed_exact_glb_views':len(exact['frames']),'runtime_views':len(views['frames'])-8,'two_rebuilds':'pass','source_reopen':'pass','khronos_errors':0,'khronos_warnings':0,'independent_qa':'pending'})
result={'status':'pass','scope':'Current frozen artifact/evidence integrity, static GLB budgets, source reopen, two actual semantic rebuilds, Khronos format checks, exact GLB fixed renders and functional software WebGL2/multi-instance benchmark. No independent craft/factual/specification approval.','independent_qa':'pending','accepted_for_brief':False,'physical_gpu_performance':'not measured','assets':rows}
(QA/'bundle-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
