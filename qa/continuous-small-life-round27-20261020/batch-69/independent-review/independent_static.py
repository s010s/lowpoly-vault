import json, os, hashlib, struct, subprocess, pathlib, datetime
from PIL import Image
ROOT=pathlib.Path('/workspace/shared/lowpoly-batch69-20261020')
OUT=pathlib.Path('/workspace/shared/lowpoly-round27-qa69')
BASE='assets/candidates/continuous-small-life-round27-20261020/batch-69'
WORK='production/continuous-small-life-round27-20261020/work/batch-69'
IDS=['wiwaxia','hanging-valley','mudpot','dike-wall']
EXPECTED={
 'wiwaxia':'d1c7e67515487fc583fd0eb903a961aec5ba855a2e95183696c031531f53c266',
 'hanging-valley':'adb2ca389d1260ac1d2cd4f0ecd6153ed344484c95fd0667928339fa198be2b9',
 'mudpot':'7818b6e324a8da1f93db36fcb09c989bf0b98c3d4fa02873ae8750daf41f4bf1',
 'dike-wall':'f0c69989e84ca70dd90a039c78199e65b5448f5d85d52fa3b4b1beb856f617d7'}
VIEWS=['hero','reversehero','front','side','rear','top','clay','silhouette']
CONSULT=pathlib.Path('/workspace/shared/batch69-research-consult-only')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def j(p): return json.loads(pathlib.Path(p).read_text())
def glb_json(p):
 b=pathlib.Path(p).read_bytes()
 assert b[:4]==b'glTF' and struct.unpack_from('<I',b,4)[0]==2
 total=struct.unpack_from('<I',b,8)[0]; assert total==len(b)
 n,typ=struct.unpack_from('<II',b,12); assert typ==0x4E4F534A
 return json.loads(b[20:20+n].decode('utf-8').rstrip(' \0')),len(b)
def triangles(doc):
 count=0; prims=0; positions=0; nontri=[]
 acc=doc.get('accessors',[])
 for mesh in doc.get('meshes',[]):
  for prim in mesh.get('primitives',[]):
   prims+=1
   if prim.get('mode',4)!=4: nontri.append(prim.get('mode'))
   ix=prim.get('indices')
   n=acc[ix]['count'] if ix is not None else acc[prim['attributes']['POSITION']]['count']
   if n%3: raise ValueError('triangle stream not divisible by 3')
   count+=n//3; positions+=acc[prim['attributes']['POSITION']]['count']
 return count,prims,positions,nontri
branch=subprocess.check_output(['git','-C',str(ROOT),'branch','--show-current'],text=True).strip()
head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
status=subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain'],text=True).strip()
base='54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c'
inventory='research/prehistoric-1000-v1/inventory.json'
blob=subprocess.check_output(['git','-C',str(ROOT),'show',f'{head}:{inventory}'])
base_blob=subprocess.check_output(['git','-C',str(ROOT),'show',f'{base}:{inventory}'])
source_inventory_sha=hashlib.sha256(blob).hexdigest(); source_inv=json.loads(blob)
assert source_inventory_sha=='b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c'
assert blob==base_blob and source_inventory_sha==hashlib.sha256(base_blob).hexdigest()
assert len(source_inv['assets'])==1000
inventory_ids=[x['id'] for x in source_inv['assets']]
assert all(inventory_ids.count(a)==1 for a in IDS)
selected_source_records=j(ROOT/WORK/'coordination-selected-inventory.json')
for aid in IDS:
 assert next(x for x in source_inv['assets'] if x['id']==aid)==next(x for x in selected_source_records if x['id']==aid)
handoff=j(ROOT/WORK/'handoff-assets.json'); handmap={x['asset_id']:x for x in handoff}
assert set(handmap)==set(IDS)
verification=j(ROOT/WORK/'verification-final.json'); assert len(verification['results'])==4
concept_tool={x['id']:x for x in j(ROOT/WORK/'concept-tool-records.json')}
assert set(concept_tool)==set(IDS)
# Independently ensure hash-listed consult-only source pixels are outside this clean checkout.
consulted_catalog={}
for aid in IDS:
 for src in j(ROOT/BASE/aid/'r001/references.json')['sources']:
  for im in src.get('consulted_images',[]):
   assert (CONSULT/im['filename']).is_file() and sha(CONSULT/im['filename'])==im['sha256']
   consulted_catalog[im['sha256']]=im['filename']
tracked=subprocess.check_output(['git','-C',str(ROOT),'ls-files','-z']).split(b'\0')
consulted_hits=[]
for raw in tracked:
 if raw:
  p=ROOT/os.fsdecode(raw)
  if p.is_file() and sha(p) in consulted_catalog: consulted_hits.append(str(p))
assert not consulted_hits
assets={}
for aid in IDS:
 d=ROOT/BASE/aid/'r001'; cand=j(d/'candidate.json'); hand=handmap[aid]
 assert cand['asset_id']==aid and cand['revision']=='r001'
 assert cand['artifacts']['glb']['sha256']==EXPECTED[aid] and sha(d/'model.glb')==EXPECTED[aid]
 filehash={}
 for key,file in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]:
  assert cand['artifacts'][key]['path'].endswith(file)
  got=sha(d/file); assert got==cand['artifacts'][key]['sha256'],(aid,key,got,cand['artifacts'][key]['sha256'])
  assert got==hand['hashes'][key],(aid,key,'handoff mismatch')
  filehash[key]=got
 # Immutable design freeze + pre-model schema and rights ledgers.
 freeze=j(d/'modeling-freeze.json'); pre=j(d/'premodel-schema-check.json'); refs=j(d/'references.json')
 assert pre['check_brief']=='pass-static-stylized-v1' and pre['all_source_rights_note']=='pass'
 assert pre['no_incorporated_third_party_assets'] and pre['generator_authored'] is False and pre['geometry_built'] is False
 for file,h in freeze['files'].items(): assert sha(d/file)==h,(aid,file,'freeze hash')
 assert refs['no_incorporated_third_party_assets'] and refs.get('rights_note')
 assert refs['sources'] and all(s.get('rights_note') and s.get('incorporated') is False and s.get('use') in ('consulted-only','original-generated-concept') for s in refs['sources'])
 # Source pixels in ledger resolve to hash-verified consult-only originals outside the repository.
 consulted=[]
 for src in refs['sources']:
  for im in src.get('consulted_images',[]):
   p=CONSULT/im['filename']; assert p.is_file() and sha(p)==im['sha256'],(aid,im['filename'])
   assert not (ROOT/'assets'/im['filename']).exists()
   consulted.append({'filename':im['filename'],'sha256':im['sha256'],'outside_repo':True})
 # Original ImageGen prompt/image receipt: source tool events remain known; provider-internal time/id stay unknown.
 ce=j(d/'concept-evidence.json'); cg=j(d/'concept-generation.json'); prompt=d/'concept-prompt.txt'; concept=d/'concept-original.png'; tool=concept_tool[aid]
 assert cg['tool']=='image_gen.imagegen' and cg['provider_generated_at'] is None and cg['receipt_status']
 assert sha(prompt)==ce['concept']['prompt']['sha256'] and tool['prompt']==prompt.read_text().rstrip('\n')
 assert sha(concept)==ce['concept']['images'][0]['sha256']
 assert tool['path'] and pathlib.Path(tool['path']).is_file() and sha(tool['path'])==sha(concept)
 assert cg['call_started_observed_utc'] and cg['result_observed_utc'] and cg['inspected_at']
 # Original brief/config/reference freeze versus derived delivery closure and final artifact bindings.
 original_brief=j(d/'brief.json'); delivery=j(d/'candidate-brief.json'); config=j(d/'build-config.json')
 assert original_brief['required_stages']==['technical','visual','factual','specification','runtime_parse','gpu','scene']
 assert original_brief['required_views']==VIEWS and original_brief['turntable_frames']==0
 assert delivery['required_views']==VIEWS and delivery['required_stages']==original_brief['required_stages']
 assert config['seed']==69 and config['blender_threads']==2 and config['three_version']=='0.180.0'
 prebind=j(d/'preproof-binding.json')
 assert prebind['glb_sha256']==EXPECTED[aid] and prebind['brief_sha256']==filehash['brief'] and prebind['references_sha256']==filehash['references']
 assert prebind['source_generator_config_binding']=='pass' and prebind['original_freeze_unchanged']
 # GLB direct chunk inspection and strict stated budgets.
 glb,nbytes=glb_json(d/'model.glb'); tri,prims,pos,nontri=triangles(glb)
 mats=len(glb.get('materials',[])); tex=len(glb.get('textures',[]))
 assert tri<=14000 and nbytes<=1000000 and mats<=6 and prims<=30 and tex==0 and not nontri
 assert tri==hand['triangles'] and nbytes==hand['glb_bytes'] and mats==hand['materials'] and prims==hand['primitives'] and pos==hand['exported_position_vertices']
 assert len(glb.get('images',[]))==0 and len(glb.get('buffers',[]))==1
 # Independent direct .blend reopen, object-part counts, and bounds.
 reopen=j(OUT/f'source-reopen-{aid}.json'); assert reopen['source_sha256']==filehash['source'] and reopen['blender_version']=='4.3.2'
 sums={'authored_vertices':sum(x['authored_vertices'] for x in reopen['mesh_objects']), 'evaluated_vertices':sum(x['evaluated_vertices'] for x in reopen['mesh_objects']), 'authored_polygons':sum(x['authored_faces'] for x in reopen['mesh_objects']), 'evaluated_polygons':sum(x['evaluated_faces'] for x in reopen['mesh_objects'])}
 sc=hand['source_counts']; assert sums['authored_vertices']==sc['authored_vertices'] and sums['evaluated_vertices']==sc['evaluated_vertices']
 parts={x['name']:{'authored_vertices':x['authored_vertices'],'evaluated_vertices':x['evaluated_vertices'],'authored_polygons':x['authored_faces'],'evaluated_polygons':x['evaluated_faces']} for x in reopen['mesh_objects']}
 expected_parts={x['name']:{'authored_vertices':x['authored_vertices'],'evaluated_vertices':x['evaluated_vertices'],'authored_polygons':x['authored_polygons'],'evaluated_polygons':x['evaluated_polygons']} for x in sc['parts']}
 assert parts==expected_parts
 assert reopen['library_count']==0 and reopen['external_image_count']==0 and reopen['scene_count']>0
 lo=[min(x['bounds_min'][i] for x in reopen['mesh_objects']) for i in range(3)]
 hi=[max(x['bounds_max'][i] for x in reopen['mesh_objects']) for i in range(3)]
 source_size=[hi[i]-lo[i] for i in range(3)]
 assert all(abs(a-b)<1e-5 for a,b in zip(source_size,hand['measured_blender_xyz_m']))
 eval_lo=[min(x['evaluated_bounds_min'][i] for x in reopen['mesh_objects']) for i in range(3)]
 eval_hi=[max(x['evaluated_bounds_max'][i] for x in reopen['mesh_objects']) for i in range(3)]
 evaluated_size=[eval_hi[i]-eval_lo[i] for i in range(3)]
 assert all(abs(a-b)<1e-5 for a,b in zip(evaluated_size,hand['measured_blender_xyz_m']))
 # Render manifest subject fields were recorded by render script before producing frames; exact final byte identities.
 manifest=j(d/'proof-final/render-manifest.json'); pix=j(d/'pixel-inspection.json'); msha=sha(d/'proof-final/render-manifest.json')
 assert manifest['frame_count']==8 and manifest['subject']=={'revision':'r001','glb_sha256':EXPECTED[aid],'brief_sha256':filehash['brief'],'references_sha256':filehash['references']}
 assert manifest['source_glb_sha256']==EXPECTED[aid] and manifest['created_at']
 assert set(x['id'] for x in manifest['frames'])==set(VIEWS)
 assert pix['manifest_sha256']==msha and pix['glb_sha256']==EXPECTED[aid]
 imgs=[]
 for frame in manifest['frames']:
  p=d/'proof-final'/frame['path']; assert sha(p)==frame['sha256'] and frame['byte_length']==p.stat().st_size
  im=Image.open(p); assert im.size==(512,512) and (frame['width'],frame['height'])==(512,512)
  pf=next(x for x in pix['frames'] if x['id']==frame['id']); assert pf['sha256']==frame['sha256'] and pf['dimensions']==[512,512]
  imgs.append({'id':frame['id'],'sha256':frame['sha256'],'dimensions':[512,512]})
 sheet=d/'contact-sheet.png'; sheet_hash=sha(sheet); sheet_dims=Image.open(sheet).size
 assert sheet_hash==pix['contact_sheet_sha256'] and sheet_dims==(2048,1060)
 # Wiwaxia is supplemented by a distinct explicitly labelled exact-final ventral diagnostic, not counted as one fixed view.
 ventral=None
 if aid=='wiwaxia':
  v=j(d/'supplemental-ventral-inspection.json'); vf=d/'supplemental-ventral/bottom.png'; vm=d/'supplemental-ventral/render-manifest.json'
  assert v['glb_sha256']==EXPECTED[aid] and v['frame_sha256']==sha(vf) and v['manifest_sha256']==sha(vm) and v['dimensions']==[512,512]
  ventral={'sha256':sha(vf),'manifest_sha256':sha(vm),'dimensions':[512,512]}
 # Both exact-final semantic rebuilds: real independent request/result directories, output bytes and semantic reports.
 finalbind=j(d/'final-rebuild-binding.json'); assert finalbind['glb_sha256']==EXPECTED[aid] and finalbind['generator_sha256']==filehash['generator'] and finalbind['config_sha256']==filehash['config']
 assert len(finalbind['distinct_real_queue_runs'])==2
 rep_list=[]
 for idx,run in enumerate(finalbind['distinct_real_queue_runs'],1):
  run_dir=pathlib.Path(run['path']); rq=run_dir/'request.json'; rs=run_dir/'result.json'; out=run_dir/'outputs/model.glb'; rep=d/f'repro-final-{idx}.report.json'
  req=j(rq); res=j(rs); check=j(rep)
  assert run_dir.is_dir() and req['identity']['job']['asset_id']==aid and req['identity']['job']['revision']=='r001'
  assert req['identity']['job']['job_id']==f'semantic-rebuild-{idx}' and req['fingerprint']==run_dir.parent.name
  assert req['identity']['inputs']['generator']['sha256']==filehash['generator'] and req['identity']['inputs']['config']['sha256']==filehash['config']
  assert req['identity']['inputs']['references']['sha256']==filehash['references']
  assert req['identity']['inputs']['brief']['sha256']==sha(d/'brief.json')
  assert res['status']=='succeeded' and res['returncode']==0 and res['error'] is None
  assert res['pid']==run['pid'] and res['started_at']==run['started_at'] and res['finished_at']==run['finished_at']
  assert res['started_at']<res['finished_at'] and req['created_at']<=res['started_at']
  assert sha(out)==EXPECTED[aid] and res['outputs']['model.glb']['sha256']==EXPECTED[aid]
  assert check['status']=='pass' and check['generator_executed'] is False and check['glb_sha256']==EXPECTED[aid] and check['rebuilt_glb_sha256']==EXPECTED[aid]
  assert check['byte_identical'] and check['semantic_match'] and check['semantic_sha256']==check['rebuilt_semantic_sha256']
  assert check['build_run']['request']['sha256']==sha(rq) and check['build_run']['result']['sha256']==sha(rs)
  assert check['build_fingerprint']==req['fingerprint'] and check['provenance_status']=='bound_successful_build_run'
  rep_list.append({'job_id':run['job_id'],'pid':res['pid'],'started_at':res['started_at'],'finished_at':res['finished_at'],'fingerprint':req['fingerprint'],'request_sha256':sha(rq),'result_sha256':sha(rs),'output_sha256':sha(out),'semantic_sha256':check['semantic_sha256'],'byte_identical':check['byte_identical'],'semantic_match':check['semantic_match']})
 assert rep_list[0]['pid']!=rep_list[1]['pid'] and rep_list[0]['fingerprint']!=rep_list[1]['fingerprint']
 assert rep_list[0]['request_sha256']!=rep_list[1]['request_sha256'] and rep_list[0]['result_sha256']!=rep_list[1]['result_sha256']
 # Preserve, enumerate, but never treat old failed/stale attempts as final proof.
 attempts=[]
 for ap in sorted(p for p in d.iterdir() if p.is_dir() and p.name.startswith('attempt-')):
  note=j(ap/'attempt-note.json') if (ap/'attempt-note.json').exists() else {}
  glbp=ap/'model.glb'
  attempts.append({'path':str(ap.relative_to(d)),'retained_at':note.get('retained_at'),'reason':note.get('reason'),'glb_sha256':sha(glbp) if glbp.exists() else None})
 stale=[]
 stale_dir=d/'retained-stale-comparisons'
 if stale_dir.exists():
  for sp in sorted(stale_dir.glob('*.json')):
   sr=j(sp); stale.append({'path':str(sp.relative_to(d)),'sha256':sha(sp),'status':sr.get('status'),'original_glb_sha256':sr.get('glb_sha256'),'compared_output_sha256':sr.get('rebuilt_glb_sha256'),'byte_identical':sr.get('byte_identical'),'semantic_match':sr.get('semantic_match'),'errors':sr.get('errors',[])})
 # Producer's frozen concept plans and source ledgers reference a broad original inventory without rewriting it.
 assets[aid]={
  'revision':'r001','glb_sha256':EXPECTED[aid],'source_sha256':filehash['source'],'candidate_brief_sha256':filehash['brief'],'reference_ledger_sha256':filehash['references'],'generator_sha256':filehash['generator'],'config_sha256':filehash['config'],
  'triangle_count':tri,'glb_bytes':nbytes,'materials':mats,'primitives':prims,'textures':tex,'exported_position_vertices':pos,
  'source_reopen':{'sha256':reopen['source_sha256'],'blender_version':reopen['blender_version'],'mesh_object_count':len(reopen['mesh_objects']),'authored_vertices':sums['authored_vertices'],'evaluated_vertices':sums['evaluated_vertices'],'authored_polygons':sums['authored_polygons'],'evaluated_polygons':sums['evaluated_polygons'],'authored_bounds_min_m':lo,'authored_bounds_max_m':hi,'authored_bounds_size_m':source_size,'evaluated_bounds_min_m':eval_lo,'evaluated_bounds_max_m':eval_hi,'evaluated_bounds_size_m':evaluated_size,'library_count':reopen['library_count'],'external_image_count':reopen['external_image_count']},
  'nominal_dimensions_blender_xyz_m':hand['nominal_dimensions_blender_xyz_m'],'measured_dimensions_blender_xyz_m':hand['measured_blender_xyz_m'],'measured_dimensions_glb_xyz_m':hand['measured_glb_xyz_m'],
  'concept':{'sha256':sha(concept),'prompt_sha256':sha(prompt),'tool':'image_gen.imagegen','call_started_observed_utc':cg['call_started_observed_utc'],'result_observed_utc':cg['result_observed_utc'],'provider_internal_time':'unknown/not returned','provider_request_id':'unknown/not returned','original_tool_image_copy_matches':True},
  'consulted_reference_pixels':consulted,'render_manifest_sha256':msha,'render_subject':manifest['subject'],'render_manifest_created_at':manifest['created_at'],'images':imgs,'contact_sheet_sha256':sheet_hash,'contact_sheet_dimensions':list(sheet_dims),'ventral_diagnostic':ventral,'rebuilds':rep_list,'retained_earlier_attempts':attempts,'retained_stale_comparisons':stale,
  'approval_status':cand.get('approval',{}).get('status','not present'),'producer_record_approved':hand['approved']}
assert set(assets)==set(IDS)
report={'schema_version':1,'kind':'independent_batch69_static_qa','reviewer_model':'GPT-6 Luna xhigh','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'target':{'branch':branch,'head':head,'expected_head':'0a58b9eab9bd4b777a1cf73262cfee00c4ba009d','worktree_clean':not status,'base_main':base,'source_inventory_path':inventory,'source_inventory_sha256':source_inventory_sha,'source_inventory_count':len(source_inv['assets']),'source_inventory_unchanged_from_base':blob==base_blob,'selected_asset_ids':IDS,'each_selected_once_in_source_inventory':True,'full_inventory_records_match_selected_copy':True,'dedup_status':j(ROOT/WORK/'coordination-preclaim-dedup.json')['status'],'claim_status':j(ROOT/WORK/'coordination-batch-69-claim.json')['status'],'claimed_ids':j(ROOT/WORK/'coordination-batch-69-claim.json')['ids'],'hash_listed_consult_pixels_absent_from_clean_worktree':not consulted_hits,'consulted_pixel_files_hashed':len(consulted_catalog)},
 'method_limits':{'independent_blend_reopen':'Blender 4.3.2 read-only, separate blocking global flock per process, --threads 2','official_validator':'to be recorded in separate independent-runtime-checks.json','three_js':'Node CPU parser only, no GPU evidence','gpu':'not_run','scene':'not_run','provider_internal_imagegen_time':'unknown/not returned; no filesystem timestamps substituted','exact_authoring_start':'unknown; freeze-before-geometry chronology uses explicit producer-observed process records only','release_or_user_approval':'not granted or inferred'},'assets':assets}
(OUT/'independent-static-checks.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'branch':branch,'head':head,'clean':not status,'source_inventory_sha256':source_inventory_sha,'inventory_count':len(source_inv['assets']),'assets':{a:{'glb':v['glb_sha256'],'triangles':v['triangle_count'],'bytes':v['glb_bytes'],'images':len(v['images']),'rebuilds':len(v['rebuilds']),'source_counts':v['source_reopen']['authored_vertices']} for a,v in assets.items()},'report':str(OUT/'independent-static-checks.json')},indent=2))
