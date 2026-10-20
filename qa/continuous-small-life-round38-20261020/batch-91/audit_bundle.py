import json,pathlib,hashlib,sys,datetime,subprocess,os
sys.dont_write_bytecode=True
from PIL import Image
S=pathlib.Path('/workspace/shared/lowpoly-batch91-20261020');D=pathlib.Path('/workspace/shared/lowpoly-batch91-independent-qa-20261020');B=S/'production/small-life-batch91';R=pathlib.Path('/workspace/shared/lowpoly-batch91-evidence')
sys.path.insert(0,str(S/'scripts'))
from qa_glb import audit_glb
from check_reproducibility import validate_build_run
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
load=lambda p:json.load(open(p))
errors=[];checked=[]
def verify(p,h,label=''):
 p=pathlib.Path(p);ok=p.is_file() and sha(p)==h;checked.append({'path':str(p),'sha256':h,'ok':ok})
 if not ok:errors.append('Hash mismatch/missing: '+str(p))
 return ok
H=load(B/'maker-handoff.json');F=load(B/'original-freeze-manifest.json')
for p,h in F['files'].items():verify(S/p,h)
for obj in [H,*[load(S/i['candidate']['path']) for i in H['items']]]:
 def walk(x):
  if isinstance(x,dict):
   if isinstance(x.get('path'),str) and 'sha256' in x:verify(S/x['path'],x['sha256'])
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(obj)
raw=load(R/'raw-evidence-manifest.json')
for p,v in raw['files'].items():verify(R/p,v['sha256']);assert (R/p).stat().st_size==v['bytes']
for v in load(B/'dependencies.json')['files']:verify(S/v['path'],v['sha256'])
inv=load(B/'batch-91-selected-inventory.json');orig=subprocess.check_output(['git','-C',str(S),'show',inv['source_inventory_commit']+':'+inv['source_inventory_path']]);inventory_source_match=hashlib.sha256(orig).hexdigest()==inv['source_inventory_sha256']
if not inventory_source_match:errors.append('Original source inventory commit content hash mismatch')
origj=json.loads(orig);origassets=origj if isinstance(origj,list) else origj['assets'];origby={x['id']:x for x in origassets};inventory_items_match=all(x==origby[x['id']] for x in inv['assets'])
if not inventory_items_match:errors.append('Selected inventory item differs from original')
rows=[]
for it in H['items']:
 aid=it['asset_id'];ar=it['artifacts'];dest=D/aid;glb=S/ar['glb']['path'];brief=load(S/ar['brief']['path']);refs=load(S/ar['references']['path']);rep=load(dest/'reopen-reexport.report.json');audit=audit_glb(glb,14000,6,30)
 (dest/'project-glb.report.json').write_text(json.dumps(audit,indent=2)+'\n')
 for ref in refs['sources']:
  assert ref['rights_note'] and ref['use']=='consulted-only' and ref['incorporated']==False
  for v in ref['consult_only_files']:verify(v['path'],v['sha256'])
 cand=load(S/it['candidate']['path']);command=[sys.executable,'-B',str(S/'scripts/validate_candidate.py'),str(S/it['candidate']['path']),'--root',str(S),'--profile','static-stylized-v1','--profile-contract',str(S/it['profile_contract']['path']),'--json'];p=subprocess.run(command,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});(dest/'candidate-schema.report.json').write_text(p.stdout);(dest/'candidate-schema.stderr.txt').write_text(p.stderr)
 if p.returncode:errors.append(aid+' candidate schema failed '+str(p.returncode))
 rebuilds=[]
 for re in load(S/it['two_rebuilds']['path'])['two_distinct_real_rebuilds']:
  req=load(S/re['request']['path']);res=load(S/re['result']['path']);exe=load(S/re['execution']['path']);out=pathlib.Path(re['raw_directory'])/'outputs';output=aid+'/'+aid+'.glb'
  for name,v in res['outputs'].items():verify(out/name,v['sha256']);assert (out/name).stat().st_size==v['bytes']
  for name,v in req['identity']['inputs'].items():verify(v['path'],v['sha256'])
  fingerprint=validate_build_run(req,res,ar['generator']['sha256'],ar['config']['sha256'],sha(out/output),output)
  sem=audit_glb(out/output,14000,6,30)['semantic_sha256'];assert sem==audit['semantic_sha256']==re['semantic_sha256'];assert exe['parent_pid']==res['pid'];assert req['created_at']<=res['started_at']<=exe['started_at']<exe['finished_at']<=res['finished_at'];assert exe['generator_sha256']==ar['generator']['sha256'] and exe['config_sha256']==ar['config']['sha256'];assert req['argv'][:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'];assert exe['argv'][exe['argv'].index('--threads')+1]=='2'
  rebuilds.append({'label':re['label'],'pid':exe['pid'],'wrapper_pid':res['pid'],'fingerprint':fingerprint,'started_at':exe['started_at'],'finished_at':exe['finished_at'],'semantic_sha256':sem,'sha256':sha(out/output),'all_output_hashes_match':True})
 assert rebuilds[0]['pid']!=rebuilds[1]['pid'] and rebuilds[0]['fingerprint']!=rebuilds[1]['fingerprint']
 by=load(S/it['byte_identity']['path']);ro=pathlib.Path(by['render_raw_directory']);req=load(ro.parent/'request.json');res=load(ro.parent/'result.json');rm=load(S/it['render_manifest']['path']);views=(S/it['render_manifest']['path']).parent
 for k in ['glb','brief','references']:assert req['identity']['inputs'][k]['sha256']==ar[k]['sha256']==rm['subject'][k+'_sha256'];verify(req['identity']['inputs'][k]['path'],ar[k]['sha256'])
 assert brief['delivery_bound_at']<req['created_at']<=res['started_at']<rm['created_at']<=res['finished_at'];assert res['status']=='succeeded' and res['returncode']==0
 frames=[];sheet=Image.open(S/it['contact_sheet']['path']).convert('RGB');assert sheet.size==(2048,1088)
 for j,frame in enumerate(rm['frames']):
  f=views/frame['path'];verify(f,frame['sha256']);assert sha(f)==sha(ro/frame['path'])==res['outputs'][frame['path']]['sha256'];im=Image.open(f).convert('RGB');assert im.size==(512,512);tile=sheet.crop(((j%4)*512,(j//4)*544,(j%4)*512+512,(j//4)*544+512));assert tile.tobytes()==im.tobytes();frames.append({'id':frame['id'],'sha256':sha(f),'dimensions':[512,512],'raw_byte_identical':True,'sheet_rgb_tile_identical':True})
 for n in ['render-manifest.json','render-config.json']:assert sha(views/n)==sha(ro/n)==res['outputs'][n]['sha256']
 receipts=load(B/'concepts'/f'{aid}-receipt.json');assert receipts['returned_at']<F['freeze_observed_at'];assert receipts['provider_timestamp']=='unknown' and receipts['provider_request_id']=='unknown'
 # Recover observed first geometry execution from original raw metadata snapshots, not mtime.
 md=pathlib.Path(by['metadata_snapshot']['raw_path']);initial=load(md.parent.parent/'execution.json');assert F['freeze_observed_at']<initial['started_at'];verify(md,by['metadata_snapshot']['lean_copy']['sha256']);assert sha(glb)==sha(md.parent/(aid+'.glb'));assert sha(S/ar['source']['path'])==sha(md.parent/(aid+'.blend'))
 rows.append({'asset_id':aid,'revision':it['revision'],'project_status':audit['status'],'schema_returncode':p.returncode,'rebuilds':rebuilds,'final_binding_at':brief['delivery_bound_at'],'render_requested_at':req['created_at'],'render_started_at':res['started_at'],'render_completed_at':res['finished_at'],'frames':frames,'initial_build_started_at':initial['started_at'],'initial_build_pid':initial['pid'],'concept_receipt':receipts,'source_reopen_pid':rep['pid'],'exact_reexport_match':rep['byte_identical']})
summary={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':errors,'checked_hashes':len(checked),'hash_checks':checked,'raw_manifest_files':len(raw['files']),'original_freeze_files':len(F['files']),'inventory_source_commit_match':inventory_source_match,'selected_inventory_items_match':inventory_items_match,'items':rows,'limitations':'Queue records and concept receipts are preserved attestations with independently verified bytes/times; provider-internal IDs/times and unrecorded generator authoring time remain unknown. No filesystem mtime used to fabricate chronology.'}
(D/'bundle-integrity.report.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'hash_checks':len(checked),'errors':errors,'items':len(rows)},indent=2))
