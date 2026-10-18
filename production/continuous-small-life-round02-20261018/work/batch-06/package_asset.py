# SPDX-License-Identifier: MIT
"""Freeze exact delivery inventory and review-pending record. Does not grant acceptance."""
import sys,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/qa_glb.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
w=ROOT/'production/continuous-small-life-round02-20261018/work/batch-06';s=sys.argv[1];d=w/s/'r001';attempt={'aulopora':'attempt-03','thamnopora':'attempt-03','hallucigenia':'attempt-01','fenestella':'attempt-01'}[s];a=ROOT/'assets/candidates/continuous-small-life-round02-20261018/batch-06'/s/'r001'/attempt/s
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def record(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':H(p),'bytes':p.stat().st_size}
r=d/'runtime-attempt-01';glb=a/(s+'.glb');audit=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
views=['hero','reversehero','front','rear','side','top','clay','silhouette','80px','160px','240px']
sheet=Image.new('RGB',(1024,950),'#e8e4dc');draw=ImageDraw.Draw(sheet);draw.text((12,10),s+' | exact GLB '+H(glb),fill='#253b42')
for i,v in enumerate(views):
 im=Image.open(r/(s+'-'+v+'.png')).convert('RGB');im.thumbnail((250,250));x=(i%4)*256;y=36+(i//4)*300;sheet.paste(im,(x,y));draw.text((x+10,y+255),v+(' / 480px envelope' if i<8 else ' / normal viewing'),fill='#253b42')
sheet.save(r/(s+'-contact-sheet.png'))
source_images=[record(p) for p in sorted(a.glob('*.png'))]
save(d/'source-view-manifest.json',{'source':record(a/(s+'.blend')),'glb':record(glb),'scope':'Blender source renders; exact export geometry counts/bounds verified separately; runtime images are direct GLB renders.','engine':'Blender 4.3.2 Cycles CPU','samples':8,'resolution':512,'view_transform':'Standard','look':'None','exposure':0,'transparent_cover':'cover-transparent.png','images':source_images})
runtime=json.loads((r/(s+'.json')).read_text());assert runtime['status']=='pass' and runtime['glb_sha256']==H(glb)
save(r/'hashes.json',{'glb':record(glb),'renderer':record(w/'viewer.html'),'runner':record(w/'browser_qa.mjs'),'files':[record(p) for p in sorted(r.iterdir()) if p.is_file() and p.name!='hashes.json']})
qa=json.loads((a/'qa.json').read_text());qa['threejs_runtime']={'status':runtime['status'],'glb_sha256':H(glb),'report':record(r/(s+'.json')),'renderer':runtime['renderer'],'scope':'Functional software WebGL2 only; physical GPU and museum performance unmeasured'};qa['visual_review']={'status':'pending','note':'Maker inspection notes supplied; independent parent-dispatched Luna xhigh QA pending'};save(a/'qa.json',qa)
# Bilingual source metadata gains provenance records without changing source or GLB.
meta=json.loads((a/'metadata.json').read_text());meta['config_sha256']=H(d/'config.json');meta['current_config']=record(d/'config.json');meta['dependency_hashes']=[record(w/'build_batch06.py'),record(ROOT/'scripts/asset_common.py'),record(ROOT/'scripts/qa_glb.py')];meta['reference_access']=json.loads((d/'references.json').read_text())['maker_access'];meta['runtime_contact_sheet']=record(r/(s+'-contact-sheet.png'));meta['independent_review']='pending; parent dispatches Luna xhigh';meta['counts']={'authored_vertices':sum(p['vertices'] for p in json.loads((a/'qa.json').read_text())['source']['parts']),'evaluated_vertices':sum(p['vertices'] for p in json.loads((a/'qa.json').read_text())['source']['parts']),'exported_position_vertices':audit['unique_position_accessor_vertices'],'triangles':audit['scene_triangles'],'materials':audit['materials'],'primitives':audit['scene_primitives_estimated_base_draw_calls'],'textures':0,'texture_encoded_bytes':0,'texture_decoded_bytes':0};save(a/'metadata.json',meta)
checks={}
for f in ['source-export.json','roundtrip/glb-roundtrip.report.json','semantic-rebuild-a.json','semantic-rebuild-b.json','project-audit.json']:
 v=json.loads((d/f).read_text());checks[f]={'status':v['status'],'evidence':record(d/f)}
checks['khronos']={'status':json.loads((a/'qa.json').read_text())['khronos_validator']['status'],'evidence':record(a/'gltf-validator.report.json')}
checks['runtime']={'status':runtime['status'],'evidence':record(r/(s+'.json')),'scope':'Pinned Three.js 0.180.0; Chromium ANGLE Vulkan SwiftShader software WebGL2. No physical GPU performance claim.'}
scene=w/'runtime-scene-attempt-01/scene.json'
if scene.exists():
 shared=json.loads(scene.read_text());assert shared['status']=='pass' and any(x['id']==s and x['glb_sha256']==H(glb) for x in shared['loaded']);checks['scene']={'status':'pass','evidence':record(scene),'instances':12,'scale':'actual meters; no display normalization; synthetic catalogue gallery only'}
assert all(v['status'] in ['pass','pass_with_warnings'] for v in checks.values()),checks
save(d/'maker-qa.json',{'asset_id':s,'revision':'r001','glb':record(glb),'checks':checks,'warnings_disposition':'Smooth shading is intentional for softly connected organic forms; spines deliberately faceted. No open/non-manifold edges are expected. Any checker-specific additional warning is retained in its original report.','independent_acceptance':'unknown; maker checks are not independent QA','visual_self_check':'Actual runtime contact sheet and targeted full-size images inspected by maker; observations logged in MAKER-NOTES.md.','scene_evidence':'shared runtime-scene-attempt-01/scene.json; 12 actual-scale copies, software WebGL2' if scene.exists() else 'pending'})
c=json.loads((ROOT/'schemas/templates/candidate.template.json').read_text());c.update(asset_id=s,revision='r001',maker={'id':'GPT-6.1-Sol-medium','task_id':'batch-06-formal-exclusive-claim'},blockers=['Fresh independent Luna xhigh QA must be dispatched by parent before acceptance/release.'])
paths={'glb':glb,'source':a/(s+'.blend'),'generator':w/'build_batch06.py','config':d/'config.json','brief':w/'planning-snapshot/items'/s/'brief.json','references':d/'references.json'}
c['artifacts']={k:{'path':record(v)['path'],'sha256':H(v)} for k,v in paths.items()}
for st in c['stages'].values():st['note']='Independent review pending. Maker automated evidence is indexed in maker-qa.json; no independent PASS asserted.'
save(d/'candidate.json',c)
allfiles=[p for p in a.rglob('*') if p.is_file()]+[p for p in d.rglob('*') if p.is_file() and p.name not in ['delivery-hashes.json','candidate-record-check.json'] and 'rebuild-runs' not in p.parts]
save(d/'delivery-hashes.json',{'asset_id':s,'revision':'r001','glb':record(glb),'counts':meta['counts'],'semantic_sha256':audit['semantic_sha256'],'artifacts':{k:record(v) for k,v in paths.items()},'files':[record(p) for p in sorted(allfiles)]})
print(s,H(glb),glb.stat().st_size,audit['scene_triangles'])
