import json, os, hashlib, struct, subprocess, pathlib, datetime
from PIL import Image
ROOT=pathlib.Path('/workspace/shared/lowpoly-batch68-20261020')
OUT=pathlib.Path('/workspace/shared/lowpoly-round27-qa68')
BASE='assets/candidates/continuous-small-life-round27-20261020/batch-68'
WORK='production/continuous-small-life-round27-20261020/work/batch-68'
EXPECTED={
 'thaumaptilon':'5f4108c4b97377bd2df41273672c16e6e9d7295a5e7d6710b4bdf0ad2b22bf42',
 'sandstone-fin':'20d94267de302a60886dcfa05aaa4bb41450f42e5e60caa29203a451cf039905',
 'lava-dome':'ec4eee3edc6b6cfd676bc9cb75bff04611afd7ebcd63bf6c279a46d539a159f8',
 'ice-wedge-polygon-ground':'a5eaa19f0f0d4f1de495974fbed3d360ce5ebb0c97b973f95a224b01a30a1f7d'}
VIEWS=['hero','reversehero','front','side','rear','top','clay','silhouette']
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def j(p): return json.loads(pathlib.Path(p).read_text())
def glb_json(p):
 b=pathlib.Path(p).read_bytes();
 assert b[:4]==b'glTF' and struct.unpack_from('<I',b,4)[0]==2
 total=struct.unpack_from('<I',b,8)[0]; assert total==len(b)
 n,typ=struct.unpack_from('<II',b,12); assert typ==0x4E4F534A
 return json.loads(b[20:20+n].decode('utf-8').rstrip(' \0')), len(b)
def triangles(doc):
 count=0; prims=0; verts=0
 acc=doc.get('accessors',[])
 for mesh in doc.get('meshes',[]):
  for p in mesh.get('primitives',[]):
   prims+=1
   if p.get('mode',4)!=4: raise ValueError('non-triangle primitive')
   idx=p.get('indices')
   n=acc[idx]['count'] if idx is not None else acc[p['attributes']['POSITION']]['count']
   if n%3: raise ValueError('triangles accessor not divisible by3')
   count+=n//3; verts+=acc[p['attributes']['POSITION']]['count']
 return count,prims,verts
# Pin clean target; do not mutate producer checkout.
branch=subprocess.check_output(['git','-C',str(ROOT),'branch','--show-current'],text=True).strip()
head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
status=subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain'],text=True).strip()
base='54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c'
inventory='research/prehistoric-1000-v1/inventory.json'
blob=subprocess.check_output(['git','-C',str(ROOT),'show',f'{head}:{inventory}'])
base_blob=subprocess.check_output(['git','-C',str(ROOT),'show',f'{base}:{inventory}'])
source_inventory_sha=hashlib.sha256(blob).hexdigest()
# Confirm true freeze inventory is same at pinned base and candidate commit.
assert source_inventory_sha=='b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c'
assert hashlib.sha256(base_blob).hexdigest()==source_inventory_sha
assert blob==base_blob
handoff=j(ROOT/WORK/'handoff-assets.json')
assets={}
for aid,expected in EXPECTED.items():
 d=ROOT/BASE/aid/'r001'; candidate=j(d/'candidate.json'); hand=next(x for x in handoff if x['asset_id']==aid)
 assert candidate['asset_id']==aid and candidate['revision']=='r001'
 assert candidate['artifacts']['glb']['sha256']==expected
 assert sha(d/'model.glb')==expected
 # All six finalized deliverable bindings are exact.
 for key,file in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]:
  assert candidate['artifacts'][key]['path'].endswith(file)
  got=sha(d/file); declared=candidate['artifacts'][key]['sha256']
  assert got==declared, (aid,key,got,declared)
  assert hand['hashes'][key]==declared
 # Frozen original brief/config/reference/concept/prompt/generation records are immutable.
 freeze=j(d/'modeling-freeze.json'); pref=j(d/'prefreeze-ledger-check.json')
 assert pref['status']=='pass' and pref['all_entries_have_rights_note'] and pref['no_incorporated_third_party_assets']
 for file,h in freeze['files'].items(): assert sha(d/file)==h,(aid,file)
 assert j(d/'build-config.json')['concept_inspected_at'] <= freeze['frozen_at']
 brief=j(d/'brief.json'); cfg=j(d/'build-config.json'); refs=j(d/'references.json')
 assert brief['required_stages']==['technical','visual','factual','specification','runtime_parse','gpu','scene']
 assert brief['required_views']==VIEWS and brief['turntable_frames']==0
 assert cfg['seed']==68 and cfg['blender_threads']==2 and cfg['three_version']=='0.180.0'
 assert refs['no_incorporated_third_party_assets'] and refs.get('rights_note')
 assert refs['sources'] and all(s.get('rights_note') and s.get('incorporated') is False and s.get('use') in ('consulted-only','original-generated-concept') for s in refs['sources'])
 assert j(d/'candidate-validation.json')['approved_for_brief'] is False
 assert candidate['approval']['status']=='pending'
 # Genuine concept asset hash and tool receipt. Verify original output still exists if available.
 evidence=j(d/'concept-evidence.json'); concept=d/'concept-original.png'
 assert sha(concept)==evidence['concept']['images'][0]['sha256']
 generation=j(d/'concept-generation.json')
 assert generation['tool']=='image_gen.imagegen' and generation['provider_generated_at'] is None and generation['receipt_status']
 concept_tool=j(ROOT/WORK/'concept-tool-records.json')[aid]
 assert concept_tool['prompt']==(d/'concept-prompt.txt').read_text().rstrip('\n')
 generated=pathlib.Path(concept_tool['path'])
 external_concept={'path':str(generated),'exists':generated.exists()}
 if generated.exists(): external_concept['sha256']=sha(generated); assert external_concept['sha256']==sha(concept)
 # Source rights ledger hashes resolve to consulted-only (outside repository); do not copy these.
 source_map={'thaum-full-scaled.jpg':'thaum-full-scaled.jpg','thaum-2022-fig2.png':'thaum-2022-fig2.png','fin.jpg':'fin.jpg','dome.jpg':'dome.jpg','dome-rubble.jpg':'dome-rubble.jpg','ice.jpg':'ice.jpg','ice-aerial.jpg':'ice-aerial.jpg'}
 consulted=[]
 for s in refs['sources']:
  for im in s.get('consulted_images',[]):
   p=pathlib.Path('/workspace/shared/batch68-consulted-only')/im['filename']
   assert p.exists() and sha(p)==im['sha256'], (aid,im['filename'])
   assert not (ROOT/'assets'/im['filename']).exists()
   consulted.append({'filename':im['filename'],'sha256':im['sha256'],'outside_repo':True})
 # Original source inventory ledger and initial claim preserve exact target and dedup.
 # Inspect the model's own target mesh budgets from the shipped GLB bytes.
 doc,nbytes=glb_json(d/'model.glb'); tri,prims,pos=triangles(doc)
 mats=len(doc.get('materials',[])); tex=len(doc.get('textures',[]))
 assert tri<14000 and nbytes<1000000 and mats<6 and prims<30 and tex==0
 # Final render images and contact sheet hash binding.
 manifest=j(d/'proof-final/render-manifest.json'); pix=j(d/'pixel-inspection.json')
 assert manifest['frame_count']==8 and manifest['source_glb_sha256']==expected
 assert set(x['id'] for x in manifest['frames'])==set(VIEWS)
 imgs=[]
 for frame in manifest['frames']:
  p=d/'proof-final'/frame['path']; digest=sha(p); im=Image.open(p)
  assert im.size==(512,512) and digest==frame['sha256'] and frame['byte_length']==p.stat().st_size
  assert frame['id'] in {x['id'] for x in pix['frames']}
  pixf=next(x for x in pix['frames'] if x['id']==frame['id'])
  assert pixf['sha256']==digest and pixf['dimensions']==[512,512]
  imgs.append({'id':frame['id'],'sha256':digest,'dimensions':list(im.size)})
 sheet=d/'contact-sheet.png'; sheet_hash=sha(sheet); sheet_size=Image.open(sheet).size
 assert sheet_hash==pix['contact_sheet_sha256'] and sheet_size==(2048,1060)
 # Keep every actual failed attempt. Dome and polygon require preserved prior diagnostics.
 attempts=[]
 for rel in ['attempts/01-quick-shape/model.glb','attempts/02-full-diagnostic-retained/model.glb']:
  p=d/rel
  if p.exists(): attempts.append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size})
 if aid in ('lava-dome','ice-wedge-polygon-ground'): assert len(attempts)==2
 # Build receipt two separate execution reports; validate path->files->hashes at each hop.
 rebuilds=[]
 for idx in (1,2):
  r=j(d/f'repro-final-{idx}.report.json'); assert r['status']=='pass' and r['byte_identical'] and r['semantic_match']
  assert r['glb_sha256']==expected and r['rebuilt_glb_sha256']==expected and r['generator_executed'] is False
  req_path=ROOT/r['build_run']['request']['path']; res_path=ROOT/r['build_run']['result']['path']; out=ROOT/r['rebuilt_glb_path']
  assert sha(req_path)==r['build_run']['request']['sha256'] and sha(res_path)==r['build_run']['result']['sha256']
  req=j(req_path); res=j(res_path)
  assert req['identity']['inputs']['generator']['sha256']==candidate['artifacts']['generator']['sha256']
  assert req['identity']['inputs']['config']['sha256']==candidate['artifacts']['config']['sha256']
  assert req['identity']['job']['asset_id']==aid and req['identity']['job']['revision']=='r001'
  assert res['status']=='succeeded' and res['returncode']==0 and res['error'] is None and res['pid']
  assert res['outputs']['model.glb']['sha256']==expected and sha(out)==expected
  assert res['started_at']<res['finished_at']
  rebuilds.append({'job':idx,'fingerprint':req['fingerprint'],'pid':res['pid'],'started_at':res['started_at'],'finished_at':res['finished_at'],'request_sha256':sha(req_path),'result_sha256':sha(res_path),'glb_sha256':sha(out),'bytes':out.stat().st_size,'semantic_sha256':r['semantic_sha256'],'semantic_match':r['semantic_match'],'byte_identical':r['byte_identical'],'provenance_status':r['provenance_status'],'runner_sha256':req['identity']['runner_sha256']})
 assert rebuilds[0]['fingerprint']!=rebuilds[1]['fingerprint']
 assert rebuilds[0]['pid']!=rebuilds[1]['pid']
 assert rebuilds[0]['request_sha256']!=rebuilds[1]['request_sha256']
 assert rebuilds[0]['result_sha256']!=rebuilds[1]['result_sha256']
 # Stage classifications based on independent evidence are added after deeper fact/art inspection.
 assets[aid]={
  'revision':'r001','glb_sha256':expected,'source_sha256':candidate['artifacts']['source']['sha256'],
  'candidate_brief_sha256':candidate['artifacts']['brief']['sha256'],'reference_ledger_sha256':candidate['artifacts']['references']['sha256'],
  'generator_sha256':candidate['artifacts']['generator']['sha256'],'config_sha256':candidate['artifacts']['config']['sha256'],
  'bytes':nbytes,'triangles':tri,'materials':mats,'primitives':prims,'textures':tex,'exported_position_vertices':pos,
  'source_object_counts_recorded':hand['source_counts'],'bounds_blender_m':hand['measured_blender_xyz_m'],'bounds_glb_xyz_m':hand['measured_glb_xyz_m'],
  'images':imgs,'contact_sheet_sha256':sheet_hash,'contact_sheet_dimensions':list(sheet_size),
  'concept':{'sha256':sha(concept),'source_receipt_status':generation['receipt_status'],'tool_output':external_concept},
  'consulted_reference_pixels':consulted,'rebuilds':rebuilds,'preserved_failed_attempts':attempts,
  'producer_stage_state':{'approval':candidate['approval']['status'],'stages':candidate.get('stages',{}), 'handoff_approved':hand['approved']}
 }
assert len(assets)==4
report={'schema_version':1,'kind':'independent_batch68_qa','reviewer_model':'GPT-6 Luna xhigh','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'target':{'branch':branch,'head':head,'worktree_clean':not status,'base_main':base,'source_inventory_path':inventory,'source_inventory_sha256':source_inventory_sha,'inventory_unchanged_from_base':blob==base_blob,'dedup_status':j(ROOT/WORK/'coordination-preclaim-dedup.json')['status'],'claimed_ids':j(ROOT/WORK/'coordination-batch-68-claim.json')['ids'],'selected_ids':[x['asset_id'] for x in handoff]},
 'limits':{'gpu':'not_run','scene':'not_run','provider_internal_imagegen_time':'unknown','provider_generation_id':'not returned; no inference from file mtimes','formal_user_release_approval':'not granted; none inferred'},'assets':assets}
(OUT/'independent-static-checks.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'branch':branch,'head':head,'clean':not status,'source_inventory_sha256':source_inventory_sha,'assets':{a:{'glb':v['glb_sha256'],'triangles':v['triangles'],'bytes':v['bytes'],'images':len(v['images']),'rebuilds':len(v['rebuilds'])} for a,v in assets.items()},'report':str(OUT/'independent-static-checks.json')},indent=2))
