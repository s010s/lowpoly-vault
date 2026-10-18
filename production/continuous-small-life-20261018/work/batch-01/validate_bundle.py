# SPDX-License-Identifier: MIT
"""Practical fixed-view candidate integrity checks; never independent art/science QA."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
from PIL import Image
BASE=ROOT/'assets/candidates/continuous-small-life-20261018/batch-01'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for a in sys.argv[1:] or ['archaeopteryx','canadaspis','ceratomyrmex','hydropteris']:
 d=BASE/a/'r001';c=json.loads((d/'candidate.json').read_text());assert c['approval']['status']=='pending';assert c['asset_id']==a
 for group in ['artifacts','technical_evidence']:
  for name,e in c[group].items():
   p=(ROOT/e['path']).resolve();assert p.is_relative_to(ROOT) and h(p)==e['sha256'],(a,name,'digest');assert p.stat().st_size==e['bytes']
 for line in (d/'checksums.sha256').read_text().splitlines():
  sha,f=line.split('  ',1);p=(d/f).resolve();assert p.is_relative_to(d) and h(p)==sha,(a,f)
 for name in ['brief.json','references.json','build-config.json']:
  assert h(d/name)==h(ROOT/'production/continuous-small-life-20261018/items'/a/name),(a,name,'frozen input changed')
 x=audit_glb(d/(a+'.glb'),14000,6,30);assert not x['errors'] and x['bytes']<=1000000
 q=json.loads((d/'qa.json').read_text());assert not q['source']['errors'] and not q['khronos_validator']['num_errors'] and not q['khronos_validator']['num_warnings'];assert q['khronos_validator']['sha256']==x['sha256'];assert all(p['boundary_edges']==0 and p['nonmanifold_edges']==0 for p in q['source']['parts'])
 b=json.loads((d/'brief.json').read_text());v=json.loads((d/'view-manifest.json').read_text());assert v['glb_sha256']==x['sha256'];assert {f['view'] for f in v['views']}==set(b['required_views']) and v['turntable_frames']==0
 for im in v['views']:
  p=ROOT/im['path'];assert h(p)==im['sha256'] and im['glb_sha256']==x['sha256'];img=Image.open(p);img.verify()
 assert Image.open(d/'preview-hero.png').getchannel('A').getextrema()==(0,255)
 rt=json.loads((d/'evidence/runtime/runtime.report.json').read_text());assert rt['status']=='pass' and rt['glb_sha256']==x['sha256'];assert len(rt['records'])==2
 for r in rt['records']:
  assert not r['errors'] and not r['failed'] and r['three']=='180' and r['instances']==(3 if r['scene'] else 1)
  expected=x['scene_triangles']*(3 if r['scene'] else 1)+(2 if r['scene'] else 0)
  assert all(view['triangles']==expected for view in r['views'])
  for view in r['views']:assert h(d/'evidence/runtime'/view['path'])==view['sha256']
  if not r['scene']:
   assert {80,160,240,360}.issubset({view['extent'] for view in r['views']})
   for i in range(3):assert abs(r['loaded'][0]['bounds']['min'][i]-x['bounds_m']['min'][i])<1e-7 and abs(r['loaded'][0]['bounds']['max'][i]-x['bounds_m']['max'][i])<1e-7
 t=d/'evidence/technical';rr=json.loads((t/'reproducibility.report.json').read_text());assert rr['status']=='pass' and rr['semantic_match'] and rr['glb_sha256']==x['sha256'];assert rr['generator_sha256']==c['artifacts']['generator']['sha256'] and rr['helper_sha256']==c['artifacts']['helper']['sha256'];assert all(r['returncode']==0 for r in rr['commands'])
 for name in ['source-export.report.json','glb-roundtrip.report.json']:
  r=json.loads((t/name).read_text());assert r['status'].startswith('pass') and not r['errors'] and r['glb_sha256']==x['sha256']
 rows.append({'asset':a,'glb_sha256':x['sha256'],'triangles':x['scene_triangles'],'bytes':x['bytes'],'status':'technical-integrity-pass','independent_QA':'pending'})
print(json.dumps({'status':'pass','scope':'Hashes, frozen input, standalone static audit, source manifoldness, official validator, eight actual image files/alpha, exact loader bounds, software WebGL work counts, three-copy scene and actual rebuild/reopen/import evidence. Does not certify art or science.','assets':rows},indent=2))
