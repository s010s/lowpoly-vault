from pathlib import Path
import json,hashlib,subprocess,sys
r=Path.cwd();p=r/'production/continuous-small-life-round15-20261018';b=p/'work/batch-43';h=json.loads((b/'HANDOFF.json').read_text());n=0

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
 if s=='kootenayscolex':assert m['representation']=='living-reconstruction' and m['nominal_body_length_m']==.045
 if s=='dillhoffia':assert m['representation']=='fossil-specimen' and abs(e['dimensions_m'][0]-.05)<.002
 if s=='beach-ridge':
  assert abs(e['dimensions_m'][0]-14)<1e-5 and m['coastal_water_datum_m']==.45
  context=json.loads((r/e['coastal_context']['path']).read_text());assert context['status']=='pass' and context['glb_sha256']==e['glb']['sha256']
 if s=='phycodes-palmate-burrow':
  assert m['trace_display']=='raised-fossil-relief' and m['nominal_trace_span_m']==.26
  src=json.loads((r/e['source_scene']['path']).read_text());relief=next(part for part in src['parts'] if 'single-continuous-main-tunnel' in part['name']);assert relief['connected_components']==1

sc=json.loads((b/'QA-HANDOFF-SCOPE.json').read_text());assert sc['expected_asset_ids']==[e['asset_id'] for e in h['assets']];assert sc['expected_source_commit']==h['model_source_commit'];assert sc['expected_glb_sha256_by_asset']=={e['asset_id']:e['glb']['sha256'] for e in h['assets']}
changed=subprocess.check_output(['git','diff','--name-only',h['base_main'],'HEAD'],text=True).splitlines();assert all(f.startswith(('production/continuous-small-life-round15-20261018/','assets/candidates/continuous-small-life-round15-20261018/batch-43/')) for f in changed)
print('PASS: exact path/hash/byte references:',n)
print('PASS: original facets/gates, four checkpoint GLBs and final model-source GLBs, exact four-ID/source/hash QA scope.')
print('PASS: frozen nominal scale/scope, attached fossil organ, continuous coast with exact-GLB context, Phycodes one-connected raised relief; zero GLB images.')
print('PASS: branch changed-path boundaries. Maker integrity only; independent acceptance pending.')

policy=json.loads((p/'review-policy.json').read_text());assert policy['independent_model_qa_rounds']==1
print('PASS: original parent-coordinated one-independent-QA policy pinned; no duplicate model acceptance asserted.')
