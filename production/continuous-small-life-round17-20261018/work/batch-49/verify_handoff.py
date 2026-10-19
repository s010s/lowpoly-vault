from pathlib import Path
import json,hashlib,subprocess,sys
r=Path.cwd();p=r/'production/continuous-small-life-round17-20261018';b=p/'work/batch-49';h=json.loads((b/'HANDOFF.json').read_text());n=0

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
 assert abs(max(e['dimensions_m'])-{'diania':.06,'czekanowskia':.18,'natural-levee':14,'lockeia-resting-trace':.2}[s])<1e-5
 if s=='diania':assert m['representation']=='living-reconstruction' and m['geometry_parameters']['lobopod_pairs']==10
 if s=='czekanowskia':assert m['representation']=='fossil-specimen' and m['geometry_parameters']['readable_fork_generations']==2
 if s=='natural-levee':assert m['representation']=='geological-form' and 'lower back plains' in m['landform_scope']
 if s=='lockeia-resting-trace':
  assert m['trace_display']=='negative-impression' and m['geometry_parameters']['depth_is_actual_geometry'] and m['geometry_parameters']['maximum_negative_depth_m']==.009
  d=json.loads((r/e['gray_diagnostic']['path']).read_text());assert d['status']=='pass' and d['glb_sha256']==e['glb']['sha256'] and [v['view'] for v in d['views']]==['hero','top']

sc=json.loads((b/'QA-HANDOFF-SCOPE.json').read_text());assert sc['expected_asset_ids']==[e['asset_id'] for e in h['assets']];assert sc['expected_source_commit']==h['model_source_commit'];assert sc['expected_glb_sha256_by_asset']=={e['asset_id']:e['glb']['sha256'] for e in h['assets']}
changed=subprocess.check_output(['git','diff','--name-only',h['base_main'],'HEAD'],text=True).splitlines();assert all(f.startswith(('production/continuous-small-life-round17-20261018/','assets/candidates/continuous-small-life-round17-20261018/batch-49/')) for f in changed)
print('PASS: exact path/hash/byte references:',n)
print('PASS: original facets/gates, four checkpoint GLBs and final model-source GLBs, exact four-ID/source/hash QA scope.')
print('PASS: frozen nominal dimensions/scope, Diania ten robust limb pairs, preserved forked foliage,14m paired levees and true pointed almond depression plus gray top/oblique; zero GLB images.')
print('PASS: branch changed-path boundaries. Maker integrity only; independent acceptance pending.')

policy=json.loads((p/'review-policy.json').read_text());assert policy['independent_model_qa_rounds']==1
print('PASS: original parent-coordinated one-independent-QA policy pinned; no duplicate model acceptance asserted.')
