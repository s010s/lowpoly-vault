import os,json,hashlib,datetime,subprocess,sys
from pathlib import Path
from PIL import Image
OLD=Path('/workspace/shared/lowpoly-batch85-20261020'); OP=OLD/'production/small-life-batch85'; R=Path('/workspace/shared/lowpoly-batch85-height-repair-20261020'); E=Path('/workspace/shared/lowpoly-batch85-height-repair-evidence-20261020'); O=Path(__file__).parent; P=R/'production/small-life-batch85-height-repair'; sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from validate_candidate import validate_candidate,STATIC_PROFILE
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
get=lambda p:json.loads(Path(p).read_text())
issues=[];checked={}
def pincheck(p,h,label):
 p=Path(p);v=sha(p);checked[str(p)]={'sha256':v,'bytes':p.stat().st_size}
 if v!=h:issues.append(label+': hash mismatch')
 return v==h
H=get(P/'maker-handoff.json');pincheck(P/'maker-handoff.json','678b730ca4c713d567c1d7a2b672eb4b3b8759b016a26b84eb139082cd6dd17c','handoff')
freeze=get(OP/'original-freeze-manifest.json')
for p,h in freeze['files'].items():pincheck(OLD/p,h,'original freeze')
raw=get(E/'raw-evidence-manifest.json');pincheck(E/'raw-evidence-manifest.json',H['local_raw_evidence_manifest']['sha256'],'raw manifest')
for p,v in raw['files'].items():pincheck(E/p,v['sha256'],'raw '+p)
original_raw=Path('/workspace/shared/lowpoly-batch85-evidence');oraw=get(original_raw/'raw-evidence-manifest.json')
pincheck(original_raw/'raw-evidence-manifest.json','bc0a7f5a61cebf2bd3d5c62b1114ebc2378348e996aafa8d1bcac465c1f7884b','original raw manifest')
for p,v in oraw['files'].items():pincheck(original_raw/p,v['sha256'],'original raw '+p)
for role in ['original_independent_qa','original_qa_handoff']:
 v=H[role];pincheck(v['path'],v['sha256'],role)
for role in ['repair_intent_freeze','dependencies','original_evidence_preservation']:
 v=H[role];pincheck(R/v['path'],v['sha256'],role)
repair=get(R/H['repair_intent_freeze']['path'])
for job in E.glob('build-queue/build/*/*/*/*/*/request.json'):
 rq=get(job)
 if not repair['frozen_at']<rq['created_at']:issues.append('repair intent not before generator execution')
for item in repair['items']:
 for key in ['original_brief','original_config','original_references','failed_glb','previous_final_views','concept_pixels_inspected']:
  v=item[key];pincheck(v['path'],v['sha256'],'repair retained original '+key)
assets=[]
for a in H['items']:
 aid=a['asset_id'];d=P/aid/a['revision'];ad=O/aid
 for role,v in a['artifacts'].items():pincheck(R/v['path'],v['sha256'],aid+' '+role)
 for role in ['candidate','profile_contract','maker_inspection','contact_sheet','render_manifest','candidate_integrity','two_rebuilds']:pincheck(R/a[role]['path'],a[role]['sha256'],aid+' '+role)
 orig=get(OP/aid/'r001/original-brief.json');brief=get(R/a['artifacts']['brief']['path']);orig_config=get(OP/aid/'r001/config.json');config=get(R/a['artifacts']['config']['path']);refs=get(R/a['artifacts']['references']['path'])
 changed=[k for k,v in orig.items() if k!='brief_version' and brief.get(k)!=v]
 if changed:issues.append(aid+': original brief changed '+str(changed))
 if orig_config['parameters']!=config['parameters']:issues.append(aid+': original parameter ledger changed')
 for v in get(R/a['artifacts']['dependencies']['path'])['files']:pincheck(R/v['path'],v['sha256'],aid+' dependencies')
 for v in brief['required_deliverables']:pincheck(R/v['path'],v['sha256'],aid+' closure')
 for s in refs['sources']:
  if not s.get('rights_note') or s.get('incorporated')!=False:issues.append(aid+': source rights')
  if 'consult_only_raw_path' in s:pincheck(s['consult_only_raw_path'],s['consult_only_sha256'],aid+' primary')
 receipt=get(OP/'concepts'/(aid+'-receipt.json'));concept=OP/'concepts'/(aid+'-concept.png')
 if sha(concept)!=orig['concept_inspection']['sha256']:issues.append(aid+': concept original differs')
 if not receipt['observed_call_returned_at']<freeze['freeze_observed_at']:issues.append(aid+': concept after freeze')
 subj=get(d/'subject.json'); expected={'revision':a['revision'],**{r+'_sha256':a['artifacts'][r]['sha256'] for r in ['glb','brief','references']}}
 if any(subj.get(k)!=v for k,v in expected.items()):issues.append(aid+': subject mismatch')
 rm=get(d/'views/render-manifest.json')
 if rm['subject']!=expected:issues.append(aid+': render subject mismatch')
 frames=[]
 for f in rm['frames']:
  im=d/'views'/f['path'];pincheck(im,f['sha256'],aid+' image');sz=Image.open(im).size
  if sz!=(512,512):issues.append(aid+': non512 frame')
  frames.append({'view':f['view'],'path':str(im),'sha256':sha(im),'pixels':list(sz)})
 # Verify contact sheet is a lossless row-major composition of source image pixels.
 sheet=Image.open(d/'views/contact-sheet.png').convert('RGB');ss=[]
 for i,f in enumerate(rm['frames']):
  im=Image.open(d/'views'/f['path']).convert('RGB');tile=sheet.crop(((i%4)*512,(i//4)*544,(i%4+1)*512,(i//4)*544+512));ss.append(tile.tobytes()==im.tobytes())
 if not all(ss):issues.append(aid+': contact sheet does not match assumed 4x2 tiles')
 rp=list((E/'final-render-queue'/'render'/aid/a['revision']/'final-eight-views').glob('*/ */request.json'.replace(' ','')))
 assert len(rp)==1,rp
 req=get(rp[0]);res=get(rp[0].parent/'result.json');render_check=all(req['identity']['inputs'][r]['sha256']==expected[r+'_sha256'] for r in ['glb','brief','references'])
 chronology=subj['bound_at']<req['created_at']<=res['started_at']<res['finished_at']
 if not render_check or not chronology or res['status']!='succeeded':issues.append(aid+': final render provenance')
 for rel,v in res['outputs'].items():pincheck(rp[0].parent/'outputs'/rel,v['sha256'],aid+' rendered output')
 rebuilds=[]
 for v in get(d/'qa/execution-provenance.json')['two_distinct_real_rebuilds']:
  for role in ['request','result','execution']:pincheck(R/v[role]['path'],v[role]['sha256'],aid+' rebuild '+role)
  rq=get(R/v['request']['path']);rs=get(R/v['result']['path']);ex=get(R/v['execution']['path']);rawdir=Path(v['raw_directory'])
  for role,filename in [('request','request.json'),('result','result.json')]:pincheck(rawdir/filename,v[role]['sha256'],aid+' raw rebuild')
  for rel,out in rs['outputs'].items():pincheck(rawdir/'outputs'/rel,out['sha256'],aid+' raw output')
  valid=(rq['created_at']<=rs['started_at']<=ex['started_at']<ex['finished_at']<=rs['finished_at'] and rs['status']=='succeeded' and rs['returncode']==0 and ex['generator_sha256']==a['artifacts']['generator']['sha256'] and ex['config_sha256']==a['artifacts']['config']['sha256'] and rs['outputs'][aid+'/'+aid+'.glb']['sha256']==a['artifacts']['glb']['sha256'])
  if not valid:issues.append(aid+': invalid rebuild '+v['label'])
  rebuilds.append({'label':v['label'],'blender_pid':ex['pid'],'runner_pid':rs['pid'],'request_at':rq['created_at'],'started_at':ex['started_at'],'finished_at':ex['finished_at'],'raw_directory':str(rawdir),'rebuilt_glb_sha256':rs['outputs'][aid+'/'+aid+'.glb']['sha256'],'valid':valid})
 if rebuilds[0]['blender_pid']==rebuilds[1]['blender_pid']:issues.append(aid+': repeated rebuild pid')
 project=validate_candidate(a['candidate']['path'],R,None,STATIC_PROFILE,a['profile_contract']['path']);(ad/'project-validation-fresh.json').write_text(json.dumps(project,indent=2)+'\n')
 if not project['valid']:issues.append(aid+': project validation errors')
 assets.append({'asset_id':aid,'revision':a['revision'],'subject':expected,'original_design_unchanged':not changed,'original_config_parameters_unchanged':orig_config['parameters']==config['parameters'],'concept_original_byte_match':sha(concept)==orig['concept_inspection']['sha256'],'final_bound_at':subj['bound_at'],'final_render_request_at':req['created_at'],'final_render_started_at':res['started_at'],'final_render_finished_at':res['finished_at'],'final_render_bound_correctly':render_check,'render_chronology_pass':chronology,'individual_views':frames,'lossless_sheet_matches':ss,'rebuilds':rebuilds,'project_schema_valid':project['valid'],'project_approved':project['approved_for_brief']})
report={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root_commit':subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip(),'clean_source_tree':subprocess.check_output(['git','-C',str(R),'status','--porcelain'],text=True)=='','original_raw_file_count':len(oraw['files']),'original_raw_bytes':sum(v['bytes'] for v in oraw['files'].values()),'raw_file_count':len(raw['files']),'raw_bytes':sum(v['bytes'] for v in raw['files'].values()),'checked_hash_count':len(checked),'issues':issues,'assets':assets}
(O/'immutable-input-audit.json').write_text(json.dumps(report,indent=2)+'\n');(O/'inspected-input-manifest.json').write_text(json.dumps(checked,indent=2)+'\n');print(json.dumps({'issues':issues,'checked':len(checked),'assets':len(assets)}))
