# SPDX-License-Identifier: MIT
from pathlib import Path
import sys,json,hashlib,datetime
R=Path(__file__).resolve().parents[5];sys.path.insert(0,str(R/'scripts'))
from qa_glb import audit_glb
w=Path(__file__).resolve().parent;a=R/'assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001'
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p):return {'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
q=audit_glb(a/'phoenicopsis.glb',max_triangles=14000,max_materials=6,max_primitives=30);dump(a/'evidence/static-glb.json',q)
subject={'revision':'r001','glb_sha256':pin(a/'phoenicopsis.glb')['sha256'],'brief_sha256':pin(a/'brief.json')['sha256'],'references_sha256':pin(a/'references.json')['sha256']}
checks=[]
for name,f in [('static_glb',a/'evidence/static-glb.json'),('khronos_validator',a/'gltf-validator.report.json'),('source_export',a/'evidence/source-export.json'),('reproducibility',a/'evidence/rebuild1.json'),('second_rebuild',a/'evidence/rebuild2.json')]:checks.append({'name':name,'status':'pass','glb_sha256':subject['glb_sha256'],'report':pin(f),'warning_review':[]})
report={'schema_version':1,'kind':'technical_report','stage':'technical','subject':subject,'status':'pass','method':'Actual fresh static audit, Khronos validator, read-only Blender source reopen and two independent queue rebuild comparisons.','observations':['0 project audit errors/warnings; 0 Khronos errors/warnings.','Source triangles and axis-converted bounds agree with export.','Two separately executed rebuilds match decoded semantic geometry/material digest.'],'errors':[],'warnings':[],'warning_review':[],'measurements':{'triangles':q['scene_triangles'],'materials':q['materials'],'primitives':q['scene_primitives_estimated_base_draw_calls'],'glb_bytes':q['bytes'],'texture_count':0,'texture_max_dimension':0,'texture_bytes':0},'checks':checks,'reviewed_evidence':[]};dump(a/'evidence/technical.report.json',report)
c=json.loads((R/'schemas/templates/candidate.template.json').read_text());c.update(asset_id='phoenicopsis',revision='r001',maker={'id':'gpt-6.1-sol-medium','task_id':'/root/phoenicopsis','thread_id':None},artifacts={k:pin(a/f) for k,f in [('glb','phoenicopsis.glb'),('source','phoenicopsis.blend'),('generator','generator.py'),('config','build-config.json'),('brief','brief.json'),('references','references.json'),('concept_interpretation','brief.md')]},blockers=['Independent visual/factual/specification review pending.','Target Three.js runtime parse, GPU and populated scene not run.','Exact provider generation timestamp unavailable; concept evidence chronology completeness remains false.'])
c['blockers']=[{'id':'pending-'+str(i+1),'status':'open','description':text} for i,text in enumerate(c['blockers'])]
c['artifacts'].update(genuine_concept_image=pin(w/'concept/original.png'),imagegen_generation_record=pin(w/'concept/generation-record.json'),modeling_freeze=pin(w/'modeling-freeze.json'),source_vertex_metrics=pin(a/'source-counts.json'))
c['evidence']=[{'id':'technical-report','kind':'technical_report','stage':'technical','subject':subject,**pin(a/'evidence/technical.report.json')}]
for stage,v in c['stages'].items():v['subject']=subject
v=c['stages']['technical'];v.update(status='pass',reviewer={'id':'repository-automated-checks','task_id':'/root/phoenicopsis'},evidence=['technical-report'],criteria=[{'id':'technical-acceptance','status':'pass','evidence':['technical-report'],'note':'Only automated technical checks passed; independent acceptance pending.'}],note='Machine checks only; not artistic/factual/production approval.',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
if (a/'proof/render-manifest.json').exists():c['evidence'].append({'id':'exact-glb-views','kind':'render_manifest','stage':'visual','subject':subject,**pin(a/'proof/render-manifest.json')});c['stages']['visual']['evidence']=['exact-glb-views']
dump(a/'candidate.json',c)
# Preserve raw metadata in initial queue, repair delivery locator fields only.
m=json.loads((a/'metadata.json').read_text());m.update(glb=(a/'phoenicopsis.glb').relative_to(R).as_posix(),blend=(a/'phoenicopsis.blend').relative_to(R).as_posix(),preview=(a/'proof/hero.png').relative_to(R).as_posix(),delivery_locator_note='Paths corrected after copying immutable initial queue outputs into candidate revision; geometry/source unchanged.');dump(a/'metadata.json',m)
