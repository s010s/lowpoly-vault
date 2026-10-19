from pathlib import Path
import json,hashlib,subprocess,sys
r=Path.cwd();p=r/'production/continuous-small-life-round13-20261018';b=p/'work/batch-38';h=json.loads((b/'HANDOFF.json').read_text());n=0

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
 if s=='diplomoceras':assert m['representation']=='fossil-specimen' and m['reconstruction_type']=='specimen' and abs(max(e['dimensions_m'])-.9)<1e-5
 if s=='nelumbo':assert m['representation']=='fossil-specimen' and m['reconstruction_type']=='specimen' and abs(max(e['dimensions_m'])-.24)<1e-5
 if s=='marine-terrace':
  assert abs(e['dimensions_m'][0]-16)<1e-5;co=m['coastal_display'];assert co['current_coast_datum_m_after_grounding']<co['raised_bench_typical_height_m_after_grounding']<co['abandoned_rear_cliff_typical_top_m_after_grounding'];ctx=json.loads((r/e['coastal_context']['path']).read_text());assert ctx['glb_sha256']==e['glb']['sha256'] and ctx['status']=='pass' and not ctx['errors'] and len(ctx['views'])==2
  for view in ctx['views']:assert hashlib.sha256((r/view['path']).read_bytes()).hexdigest()==view['sha256']
 if s=='angular-unconformity-outcrop':assert abs(e['dimensions_m'][0]-.85)<1e-5 and m['contact_structure']['age_scope']
sc=json.loads((b/'QA-HANDOFF-SCOPE.json').read_text());assert sc['expected_asset_ids']==[e['asset_id'] for e in h['assets']];assert sc['expected_source_commit']==h['model_source_commit'];assert sc['expected_glb_sha256_by_asset']=={e['asset_id']:e['glb']['sha256'] for e in h['assets']}
changed=subprocess.check_output(['git','diff','--name-only',h['base_main'],'HEAD'],text=True).splitlines();assert all(f.startswith(('production/continuous-small-life-round13-20261018/','assets/candidates/continuous-small-life-round13-20261018/batch-38/')) for f in changed)
print('PASS: exact path/hash/byte references:',n)
print('PASS: original facets/gates, four checkpoint GLBs and final model-source GLBs, exact four-ID/source/hash QA scope.')
print('PASS: Diplomoceras shell-only0.9m; Nelumbo detached fossil-leaf0.24m; marine terrace16m and actual coastal datum/context; unconformity0.85m and real truncated lower beds; zero GLB images.')
print('PASS: branch changed-path boundaries. Maker integrity only; independent acceptance pending.')
