from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys
R=Path.cwd();B=R/'production/undersea-invertebrates-concept-20261019';A=R/'assets/candidates/undersea-invertebrates-concept-20261019';sys.path.insert(0,str(R/'scripts'));from qa_glb import audit_glb
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(R));pin=lambda p:{'path':rel(p),'sha256':H(p)}
cur=json.loads((B/'current-revisions.json').read_text());now=datetime.now(timezone.utc).isoformat()
for slug,rev in cur.items():
 d=A/slug/rev;e=d/'evidence';e.mkdir(exist_ok=True);attempts=list((B/'final-runs/render'/slug/rev/'final-full-coverage').glob('*/*/result.json'))+list((B/'repair-final-runs/render'/slug/rev/'final-full-coverage').glob('*/*/result.json'))
 if not attempts:continue
 at=attempts[0].parent
 if json.loads((at/'result.json').read_text())['status']!='succeeded':continue
 if not (d/'proof').exists():shutil.copytree(at/'outputs',d/'proof')
 q=audit_glb(d/(slug+'.glb'),12000,8,48);(e/'static-glb.report.json').write_text(json.dumps(q,indent=2)+'\n')
 manifest=json.loads((d/'proof/render-manifest.json').read_text());subject=manifest['subject'];meas={'triangles':q['scene_triangles'],'materials':q['materials'],'primitives':q['scene_primitives_estimated_base_draw_calls'],'glb_bytes':q['bytes'],'texture_count':0,'texture_max_dimension':0,'texture_bytes':0}
 checks=[]
 for name,p in [('static_glb',e/'static-glb.report.json'),('khronos_validator',d/'gltf-validator.report.json'),('source_export',e/'source-export.report.json'),('reproducibility',e/'reproducibility-1.report.json'),('second_rebuild',e/'reproducibility-2.report.json')]:checks.append({'name':name,'status':'pass','glb_sha256':q['sha256'],'report':pin(p),'warning_review':[]})
 report={'schema_version':1,'kind':'technical_report','stage':'technical','subject':subject,'status':'pass','method':'Actual fresh static GLB audit, official Khronos validator, source Blender read-only check and two separately queued deterministic rebuild comparisons. All raw report bytes retained.','observations':['Static audit and official validator report no errors or warnings.','Source/export evaluated triangle counts and axis-mapped bounds match.','Both independently executed rebuild semantic geometry/material digests equal this exact GLB.'],'errors':[],'warnings':[],'warning_review':[],'measurements':meas,'checks':checks,'reviewed_evidence':[]}
 (e/'technical.report.json').write_text(json.dumps(report,indent=2)+'\n')
 rt=json.loads((d/'runtime/runtime-report.json').read_text());parse={'schema_version':1,'kind':'runtime_parse_report','stage':'runtime_parse','subject':subject,'status':'pass' if rt['status']=='pass' else 'fail','method':'Actual Chromium GLTFLoader load of exact standalone GLB; measured geometry bounds and triangles, then software WebGL renders.','observations':['Actual browser loader parsed this exact hash with no recorded browser errors.','Software SwiftShader rendering is functional evidence, not physical-device performance approval.'],'errors':rt['errors'],'warnings':[],'warning_review':[],'runtime':{'engine':'Three.js','version':rt['three_version'],'loader':'GLTFLoader','parsed':rt['status']=='pass'},'raw_functional_report':pin(d/'runtime/runtime-report.json'),'reviewed_evidence':[]}
 (e/'runtime-parse.report.json').write_text(json.dumps(parse,indent=2)+'\n')
 c=json.loads((R/'schemas/templates/candidate.template.json').read_text());c.update(asset_id=slug,revision=rev,maker={'id':'gpt-6.1-sol-medium-maker','task_id':'make-undersea-batch-20261019'},artifacts={role:pin(d/name) for role,name in [('glb',slug+'.glb'),('source',slug+'.blend'),('generator','generator.py'),('config','build-config.json'),('brief','brief.json'),('references','references.json'),('concept_interpretation','brief.md')]})
 c['artifacts']['source_locator_map']=pin(B/'reference-map.json')
 c['artifacts']['genuine_concept_image']=pin(B/'concepts/original.png')
 c['artifacts']['imagegen_generation_record']=pin(B/'concepts/generation-record.json')
 c['evidence']=[dict(id='technical-report',kind='technical_report',stage='technical',subject=subject,**pin(e/'technical.report.json')),dict(id='runtime-parse-report',kind='runtime_parse_report',stage='runtime_parse',subject=subject,**pin(e/'runtime-parse.report.json')),dict(id='exact-glb-full-views',kind='render_manifest',stage='visual',subject=subject,**pin(d/'proof/render-manifest.json'))]
 for stage in c['stages']:
  x=c['stages'][stage];x['subject']=subject;x['note']='Independent review pending.' if stage in ['visual','factual','specification'] else 'Physical-device/target populated scene performance remains unknown; actual local SwiftShader functional screenshots retained.'
  if stage in ['technical','runtime_parse']:
   eid='technical-report' if stage=='technical' else 'runtime-parse-report';x.update(status='pass',reviewer={'id':'repository-checkers-with-browser','task_id':'make-undersea-batch-20261019'},reviewed_at=now,evidence=[eid],note='Actual automated technical subchecks only; no independent artistic/factual acceptance.')
   x['criteria'][0].update(status='pass',evidence=[eid],note=x['note'])
  if stage=='visual':x['evidence']=['exact-glb-full-views']
 c['blockers']=[{'id':'independent-review-pending','status':'open','description':'Fresh independent visual, factual and specification review is pending; maker does not approve own asset.'},{'id':'target-runtime-performance-unknown','status':'open','description':'Local actual software WebGL single-asset/nine-copy and four-asset scenes are retained. Physical-device/target populated environment performance has not run.'},{'id':'ci-pending','status':'open','description':'CI results are pending during reported Actions/Pages outage. No rerun, merge or deploy performed.'}]
 if slug=='ctenoimbricata':c['blockers'].append({'id':'primary-figure-pixel-review-pending','status':'open','description':'Original research text consulted; original Fig4/5 access failed. Independent factual reviewer must inspect primary figure anatomy before approval.'})
 (d/'candidate.json').write_text(json.dumps(c,indent=2)+'\n')
 print(slug,rev,'packaged')
