import pathlib,json,hashlib,datetime,subprocess,os
from PIL import Image
r=pathlib.Path('/workspace/shared/lowpoly-batch86-20261020');w=r/'production/batch86';out=pathlib.Path(__file__).parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[];errors=[];inspected=[]
expect='3ab162a19f5b763f9e4105c43afdf2232759830bc8feb34748f32255df0975bb'
assert H(w/'handoff-assets.json')==expect
assert subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip()=='671bd5145dedae9ec7802a35069f81ab9eefcbf5'
assert subprocess.check_output(['git','-C',str(r),'rev-list','--parents','-n','1','HEAD'],text=True).strip().split()==['671bd5145dedae9ec7802a35069f81ab9eefcbf5','43e40fc89f2b369a5f1858e72fa58a0d10318124']
for a in json.load(open(w/'handoff-assets.json')):
 p=r/a['path'];original=p.parent/'r001';check={};freeze=json.load(open(original/'modeling-freeze.json'))
 check['original_freeze_hashes_match']=all(H(original/n)==h for n,h in freeze['files'].items())
 names={'glb':'model.glb','brief':'candidate-brief.json','references':'references.json','source':'source.blend','generator':'generator.py','config':'build-config.json'}
 check['handoff_artifact_hashes_match']=all(H(p/n)==a['hashes'][k] for k,n in names.items())
 check['original_design_and_ledger_unchanged']=H(original/'brief.json')==H(p/'brief.json') and H(original/'references.json')==H(p/'references.json')
 derived=json.load(open(p/'candidate-brief.json'));orig=json.load(open(original/'brief.json'));check['derived_only_packaging_changes']=all(derived.get(k)==v for k,v in orig.items() if k!='required_deliverables')
 check['delivery_closure']=all(H(r/x['path'])==x['sha256'] for x in derived['required_deliverables'])
 dep=json.load(open(p/'build-dependencies.json'));check['dependency_hashes_match']=all(H(r/n)==h for n,h in dep['inputs'].items()) and H(r/'package-lock.json')==dep['node_lockfile_sha256']
 manifest=json.load(open(p/'proof-final/render-manifest.json'));binding=json.load(open(p/'preproof-binding.json'));events=[json.loads(l) for l in (p/'lifecycle.jsonl').read_text().splitlines()];render=[x for x in events if x['stage']=='proof-final'];assert len(render)==1
 check['exact_subject_precedes_render']=all(binding[k+'_sha256']==a['hashes'][k]==manifest['subject'][k+'_sha256'] for k in ['glb','brief','references']) and binding['checked_at']<render[0]['started_at']<manifest['created_at']<=render[0]['ended_at']
 check['final_views_hashes_dimensions']=all(H(p/'proof-final'/f['path'])==f['sha256'] and Image.open(p/'proof-final'/f['path']).size==(512,512) for f in manifest['frames']) and len(manifest['frames'])==8
 im=Image.open(p/'contact-sheet.png').convert('RGBA');sheet=[]
 for i,f in enumerate(manifest['frames']):
  frame=Image.open(p/'proof-final'/f['path']).convert('RGBA');x=(i%4)*512;row=(i//4)*530
  offsets=[off for off in range(19) if im.crop((x,row+off,x+512,row+off+512)).tobytes()==frame.tobytes()];sheet.append({'view':f['id'],'offsets_matching':offsets})
  inspected.append({'asset_id':a['asset_id'],'kind':'final-individual-512','path':str(p/'proof-final'/f['path']),'sha256':H(p/'proof-final'/f['path']),'viewed_at':'2026-10-20T21:27:16Z to 2026-10-20T21:28:47Z','method':'Opened actual individual image at original resolution using view_image, not contact-sheet-only.'})
 check['sheet_lossless']=all(s['offsets_matching'] for s in sheet)
 gen=json.load(open(p/'concept-generation.json'));check['concept_original_receipt']=H(p/'concept-original.png')==gen['original_image_sha256'] and gen['observer_invoked_at']<gen['observer_result_at']<gen['inspected_at']<freeze['frozen_at']
 check['provider_unknown_honest']=gen['provider_internal_timestamps'] is None
 inspected.append({'asset_id':a['asset_id'],'kind':'concept','path':str(p/'concept-original.png'),'sha256':H(p/'concept-original.png'),'viewed_at':'2026-10-20T21:26:37Z'})
 rebuild=[]
 for z in json.load(open(p/'final-rebuild-binding.json'))['actual_distinct_runs']:
  q=r/z['request']['path'];res=r/z['result']['path'];req=json.load(open(q));result=json.load(open(res));
  valid=H(q)==z['request']['sha256'] and H(res)==z['result']['sha256'] and result['status']=='succeeded' and result['returncode']==0 and result['pid']==z['pid'] and result['started_at']<result['finished_at'] and result['wall_seconds']>0
  valid=valid and all(H(pathlib.Path(x['path']))==x['sha256'] for x in req['identity']['inputs'].values()) and all(H(res.parent/'outputs'/n)==v['sha256'] for n,v in result['outputs'].items()) and H(res.parent/'outputs/model.glb')==a['hashes']['glb']
  rebuild.append({'pid':result['pid'],'request':str(q),'result':str(res),'started_at':result['started_at'],'finished_at':result['finished_at'],'request_hash':H(q),'result_hash':H(res),'all_outputs_verified':valid})
 check['distinct_queued_rebuilds']=len(rebuild)==2 and len({x['pid'] for x in rebuild})==2 and len({x['request'] for x in rebuild})==2 and all(x['all_outputs_verified'] for x in rebuild)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');cp=subprocess.run(['python3',str(r/'scripts/validate_candidate.py'),str(p/'candidate.json'),'--root',str(r),'--profile','static-stylized-v1','--profile-contract',str(p/'profile-contract.json'),'--json'],env=env,capture_output=True,text=True);(out/a['asset_id']/'candidate-schema-fresh.json').write_text(cp.stdout);check['candidate_schema']=cp.returncode==0
 rows.append({'asset_id':a['asset_id'],'checks':check,'sheet_crops':sheet,'rebuilds':rebuild,'binding':binding,'render_started_at':render[0]['started_at'],'render_ended_at':render[0]['ended_at'],'frozen_at':freeze['frozen_at'],'generator_authoring_start':'not measured, maker attestation only'})
 errors += [a['asset_id']+': '+k for k,v in check.items() if not v]
index=json.load(open(w/'local-evidence-index.json'));index_checks={}
for k,items in index.items():
 if isinstance(items,list):
  ss=[x for x in items if isinstance(x,dict) and 'path' in x and 'sha256' in x]
  index_checks[k]={'files':len(ss),'all_match':all(pathlib.Path(x['path']).is_file() and H(pathlib.Path(x['path']))==x['sha256'] for x in ss)}
for f in ['hao-specimen-reconstruction-reproduced.jpg','beach-figure1.png','cinder.jpg','cinder-crater.jpg','putao-tower-karst.jpg']:
 p=pathlib.Path('/workspace/shared/lowpoly-batch86-consult-only')/f;inspected.append({'kind':'consult-only-primary-reference','path':str(p),'sha256':H(p),'viewed_at':'2026-10-20T21:26:37Z to 2026-10-20T21:26:59Z'})
report={'created_at':now(),'commit':'671bd5145dedae9ec7802a35069f81ab9eefcbf5','handoff_sha256':expect,'assets':rows,'local_evidence_index':index_checks,'errors':errors,'clock_note':'Maker event timestamps use orchestration UTC; own shell wall clock differs. Do not infer lifecycle from file mtimes.'}
(out/'immutable-input-audit.json').write_text(json.dumps(report,indent=2)+'\n');(out/'inspected-input-manifest.json').write_text(json.dumps(inspected,indent=2)+'\n');print(json.dumps({'errors':errors,'index':index_checks,'sheet':[{'asset':x['asset_id'],'crops':x['sheet_crops']} for x in rows]},indent=2))
