# SPDX-License-Identifier: MIT
"""Actual v2 integrity checks; no subjective beauty or user-acceptance certification."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb,read_glb
QA=ROOT/'qa/small-fauna-trio-v2';BASE=ROOT/'production/small-fauna-trio-v2';ASSETS=ROOT/'assets/candidates/small-fauna-trio-v2'
rows=[]
for s in ['diplomystus','burgessomedusa','kalligramma']:
 d=BASE/s;a=ASSETS/s;freeze=json.loads((d/'freeze.json').read_text());q=json.loads((a/'qa.json').read_text());g=audit_glb(a/(s+'.glb'),14000,6,30);doc,_,_=read_glb(a/(s+'.glb'))
 for role,f in freeze['files'].items():assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'],(s,role,'stale freeze')
 assert not g['errors'],g['errors'];assert g['bytes']<500000
 official=json.loads((a/'gltf-validator.report.json').read_text());assert official['issues']['numErrors']==official['issues']['numWarnings']==0
 browser=json.loads((QA/'browser'/(s+'.json')).read_text());assert browser['status']=='pass' and browser['glb_sha256']==g['sha256'];assert not browser['errors'] and not browser['failed']
 b=browser['loaded'][0]['bounds'];assert max(abs(b[z][i]-g['bounds_m'][z][i]) for z in ['min','max'] for i in range(3))<1e-6
 for suffix in ['source-export','reproducibility']:
  report=json.loads((QA/'final-validation-r2'/(s+'-'+suffix+'.json')).read_text());assert report['status'].startswith('pass')
  if suffix=='source-export':assert report['glb_sha256']==g['sha256'] and report['triangles_match'] and report['bounds_match']
  else:assert report['delivered_sha256']==g['sha256'] and report['semantic_match']
 views=json.loads((QA/(s+'-view-manifest.json')).read_text());assert views['glb_sha256']==g['sha256'] and len(views['frames'])>=14
 for img in views['frames']:assert hashlib.sha256((ROOT/img['path']).read_bytes()).hexdigest()==img['sha256']
 review=json.loads((d/'independent-review.json').read_text());assert review['glb_sha256']==g['sha256'],(s,'stale review')
 row={'id':s,'glb_sha256':g['sha256'],'glb_bytes':g['bytes'],'blend_bytes':(a/(s+'.blend')).stat().st_size,'triangles':g['scene_triangles'],'exported_position_vertices':g['unique_position_accessor_vertices'],'materials':g['materials'],'primitives':g['scene_primitives_estimated_base_draw_calls'],'authored_parts':q['source']['parts'],'dimensions_glb_m':g['bounds_m']['size'],'textures':len(doc.get('images',[])),'extensions_used':g['extensions_used'],'browser_draw_calls':browser['views'][0]['calls'],'browser_render_triangles':browser['views'][0]['triangles'],'user_acceptance':'pending'};rows.append(row)
scene=json.loads((QA/'browser/scene.json').read_text());assert scene['status']=='pass' and scene['instances']==9
for a in scene['loaded']:assert a['glb_sha256']==next(r['glb_sha256'] for r in rows if r['id']==a['id'])
result={'status':'pass','scope':'Exact artifact/evidence bindings, format/geometry/budgets, reopen/rebuild and functional software browser checks only','beauty_or_user_approval':False,'assets':rows,'scene':{'instances':9,'calls':scene['views'][0]['calls'],'triangles':scene['views'][0]['triangles'],'renderer':scene['renderer']},'limitations':['No physical GPU or device FPS claim','No strict scientific reconstruction','Historical candidate validator incompatible with zero sequence profile; no formal approval claimed']}
(QA/'bundle-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'pass','assets':[{k:r[k] for k in ['id','glb_bytes','triangles','materials','primitives','textures']} for r in rows],'user_acceptance':'pending'},ensure_ascii=False,indent=2))
