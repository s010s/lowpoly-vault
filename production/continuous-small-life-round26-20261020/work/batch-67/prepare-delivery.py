from pathlib import Path
import json,hashlib,sys,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round26-20261020/work/batch-67';sys.path.insert(0,str(R/'scripts'));import validate_candidate as vc
from qa_glb import audit_glb
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();results=[]
for x in json.load(open(W/'final-selection.json')):
 b=R/x['path'];refs=json.load(open(b/'references.json'));assert refs['no_incorporated_third_party_assets'];assert all(s.get('rights_note') for s in refs['sources']);shutil.copy(b/'references.json',b/'references.delivery-v001.json')
 brief=json.load(open(b/'candidate-brief.json'));c=json.load(open(R/'schemas/templates/candidate.template.json'));c.update(asset_id=x['asset_id'],revision=x['revision'],maker={'id':'GPT-6.1 Sol medium batch67','task_id':'/root/coordinate_new_model_batches/produce_batch67_models'})
 c['artifacts']={k:{'path':str((b/n).relative_to(R)),'sha256':H(b/n)} for k,n in {'glb':'model.glb','brief':'candidate-brief.json','references':'references.delivery-v001.json','source':'source.blend','generator':'generator.py','config':'build-config.json'}.items()}
 vc.check_brief(brief,c,{s['id'] for s in refs['sources']},vc.STATIC_PROFILE)
 for d in brief['required_deliverables']:assert c['artifacts'][d['role']]=={k:d[k] for k in ['path','sha256']}
 for n,h in json.load(open(b/'modeling-freeze.json'))['files'].items():assert H(b/n)==h,(b,n)
 qa=audit_glb(b/'model.glb',14000,6,30);assert not qa['errors'];(b/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
 results.append({'asset_id':x['asset_id'],'schema_brief_rights_frozen_binding':'pass','checked_at':now(),'glb_sha256':H(b/'model.glb'),'brief_sha256':H(b/'candidate-brief.json'),'references_sha256':H(b/'references.delivery-v001.json')})
(W/'pre-render-binding-checks.json').write_text(json.dumps(results,indent=2)+'\n');print('PRE RENDER SCHEMA/BINDINGS PASS')
