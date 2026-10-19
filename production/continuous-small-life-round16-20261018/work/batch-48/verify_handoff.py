from pathlib import Path
import json,hashlib,subprocess,sys
r=Path.cwd();p=r/'production/continuous-small-life-round16-20261018';b=p/'work/batch-48';h=json.loads((b/'HANDOFF.json').read_text());n=0

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
 if s=='facivermis':assert m['representation']=='living-reconstruction' and abs(max(e['dimensions_m'])-.075)<1e-5 and m['arm_pairs']==5 and not m['dwelling_tube_included']
 if s=='cave-pearl-pool':
  assert abs(max(e['dimensions_m'])-.38)<1e-5 and m['pool_structure']['discrete_concretions']==8
  src=json.loads((r/e['source_scene']['path']).read_text());pearls=next(p for p in src['parts'] if 'eight-discrete' in p['name']);assert pearls['connected_components']==8
 if s=='lava-tree-mold-crust':
  assert abs(max(e['dimensions_m'])-.7)<1e-5 and m['mold_structure']['tree_or_wood_assets']==0 and m['mold_structure']['actual_rim_to_floor_depth_m']>.23
  src=json.loads((r/e['source_scene']['path']).read_text());assert len(src['parts'])==1 and src['parts'][0]['connected_components']==1
 if s=='treptichnus-serial-probe-burrow':
  assert m['trace_display']=='sectional-structure' and abs(max(e['dimensions_m'])-.28)<1e-5 and m['section_structure']['serial_J_probes']==7 and m['section_structure']['sampled_max_half_channel_depth_m']>.003
  src=json.loads((r/e['source_scene']['path']).read_text());assert len(src['parts'])==1 and src['parts'][0]['connected_components']==1

sc=json.loads((b/'QA-HANDOFF-SCOPE.json').read_text());assert sc['expected_asset_ids']==[e['asset_id'] for e in h['assets']];assert sc['expected_source_commit']==h['model_source_commit'];assert sc['expected_glb_sha256_by_asset']=={e['asset_id']:e['glb']['sha256'] for e in h['assets']}
changed=subprocess.check_output(['git','diff','--name-only',h['base_main'],'HEAD'],text=True).splitlines();assert all(f.startswith(('production/continuous-small-life-round16-20261018/','assets/candidates/continuous-small-life-round16-20261018/batch-48/')) for f in changed)
print('PASS: exact path/hash/byte references:',n)
print('PASS: original facets/gates, four checkpoint GLBs and final model-source GLBs, exact four-ID/source/hash QA scope.')
print('PASS: exact nominal dimensions/scope, five anterior arm pairs, eight discrete pearls, deep negative tree mold and genuine serial J sectional channels; zero GLB images.')
print('PASS: branch changed-path boundaries. Maker integrity only; independent acceptance pending.')

policy=json.loads((p/'review-policy.json').read_text());assert policy['independent_model_qa_rounds']==1
print('PASS: original parent-coordinated one-independent-QA policy pinned; no duplicate model acceptance asserted.')
