from pathlib import Path
import json,hashlib,subprocess,sys
r=Path.cwd();p=r/'production/continuous-small-life-round14-20261018';b=p/'work/batch-40';h=json.loads((b/'HANDOFF.json').read_text());n=0

def verify(x):
 global n
 if isinstance(x,dict):
  if 'path'in x and 'sha256'in x:
   f=r/x['path'];assert f.is_file(),f;assert hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256'],f
   if 'bytes'in x:assert f.stat().st_size==x['bytes'],f
   n+=1
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
verify(h);sys.path.insert(0,str(r/'scripts'));from qa_glb import read_glb
for e in h['assets']:
 s=e['asset_id'];inv=json.loads((p/'items'/s/'inventory-record.json').read_text());m=json.loads((r/e['metadata']['path']).read_text());assert e['catalog_facets']=={k:inv.get(k) for k in e['catalog_facets']};assert m['inventory_production_gate']==inv['production_gate'];assert hashlib.sha256(subprocess.check_output(['git','show',h['model_source_commit']+':'+e['glb']['path']])).hexdigest()==e['glb']['sha256']
 gltf,_,_=read_glb(r/e['glb']['path']);assert not gltf.get('images')
 assert 'review_policy' in e['artifact_dependencies']
 if s=='sidneyia':assert m['representation']=='living-reconstruction' and m['reconstruction_type']=='whole-organism' and m['nominal_body_tail_length_m']==.14 and .14<max(e['dimensions_m'])<.19
 if s=='botrychium':assert m['representation']=='fossil-specimen' and m['reconstruction_type']=='specimen' and abs(max(e['dimensions_m'])-.16)<1e-5
 if s=='barrier-island':
  assert abs(e['dimensions_m'][0]-20)<1e-5 and m['scale_class']=='landscape';co=m['coastal_display'];assert co['water_datum_m_after_grounding']==.3;ctx=json.loads((r/e['barrier_context']['path']).read_text());assert ctx['glb_sha256']==e['glb']['sha256'] and ctx['status']=='pass' and not ctx['errors'] and len(ctx['views'])==2
  for view in ctx['views']:assert hashlib.sha256((r/view['path']).read_bytes()).hexdigest()==view['sha256']
 if s=='diplocraterion-spreite-burrow':assert abs(max(e['dimensions_m'])-.25)<1e-5 and m['trace_display']=='sectional-structure' and m['spreite_structure']['continuous_solid_sheets']==8
sc=json.loads((b/'QA-HANDOFF-SCOPE.json').read_text());assert sc['expected_asset_ids']==[e['asset_id'] for e in h['assets']];assert sc['expected_source_commit']==h['model_source_commit'];assert sc['expected_glb_sha256_by_asset']=={e['asset_id']:e['glb']['sha256'] for e in h['assets']}
changed=subprocess.check_output(['git','diff','--name-only',h['base_main'],'HEAD'],text=True).splitlines();assert all(f.startswith(('production/continuous-small-life-round14-20261018/','assets/candidates/continuous-small-life-round14-20261018/batch-40/')) for f in changed)
print('PASS: exact path/hash/byte references:',n)
print('PASS: original facets/gates, four checkpoint GLBs and final model-source GLBs, exact four-ID/source/hash QA scope.')
print('PASS: Sidneyia nominal body-tail0.14m plus antennae; Botrychium fertile-only0.16m; barrier20m landscape and actual datum/context; Diplocraterion0.25m sectional structure and8 continuous sheets; zero GLB images.')
print('PASS: branch changed-path boundaries. Maker integrity only; independent acceptance pending.')

policy=json.loads((p/'review-policy.json').read_text());assert policy['independent_model_qa_rounds']==1
print('PASS: original parent-coordinated one-independent-QA policy pinned; no duplicate model acceptance asserted.')
