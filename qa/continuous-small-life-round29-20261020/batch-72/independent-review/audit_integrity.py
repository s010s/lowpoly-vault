import hashlib,json,subprocess,sys
from pathlib import Path
REPO=Path('/workspace/shared/lowpoly-batch72-20261020')
QA=Path('/workspace/shared/lowpoly-round29-qa72')
W=REPO/'production/continuous-small-life-round29-20261020/work/batch-72'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p): return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
errors=[]; checks={}
def check(name,ok,detail=None):
 checks[name]={'pass':bool(ok),'detail':detail}
 if not ok: errors.append(name)
# fixed source worktree + upstream base inventory
head=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','-C',str(REPO),'branch','--show-current'],text=True).strip()
porcelain=subprocess.check_output(['git','-C',str(REPO),'status','--porcelain=v1'],text=True).strip()
check('exact_commit',head=='1a11f05899680c5bfba452ea56a2bcbc8f75d409',head)
check('branch',branch=='candidate/small-life-batch72-concept-20261020',branch)
check('worktree_clean',not porcelain,porcelain or 'clean')
base_hash=subprocess.check_output(['git','-C',str(REPO),'show','54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c:research/prehistoric-1000-v1/inventory.json'],text=False)
base_sha=hashlib.sha256(base_hash).hexdigest()
check('base_inventory_sha',base_sha=='b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c',base_sha)
# manifest closure: every raw file exists, exact SHA/length and tracked in fixed commit
m=json.load(open(W/'source-evidence-manifest.json')); bad=[]; missing=[]; untracked=[]
for e in m['files']:
 p=REPO/e['path']
 if not p.is_file(): missing.append(e['path']); continue
 if p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']: bad.append(e['path'])
 try: subprocess.check_call(['git','-C',str(REPO),'cat-file','-e',f'HEAD:{e["path"]}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 except subprocess.CalledProcessError: untracked.append(e['path'])
check('source_manifest_files_exist_and_match',not bad and not missing,{'count':len(m['files']),'bad':bad[:10],'missing':missing[:10]})
check('source_manifest_all_tracked',not untracked,{'untracked':untracked[:10]})
# earlier tracked closure including raw logs + manifest is itself tracked
c=json.load(open(W/'tracked-closure.json')); cbad=[]; cuntracked=[]
for e in c['raw_logs']:
 p=REPO/e['path']
 if not p.is_file() or sha(p)!=e['sha256']: cbad.append(e['path'])
 try: subprocess.check_call(['git','-C',str(REPO),'cat-file','-e',f'HEAD:{e["path"]}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 except subprocess.CalledProcessError: cuntracked.append(e['path'])
check('raw_log_closure',not cbad and not cuntracked,{'count':len(c['raw_logs']),'bad':cbad[:10],'untracked':cuntracked[:10]})
# pinned handoff records + exact final six hashes; freeze/raw evidence continuity
h=json.load(open(W/'HANDOFF.json')); assets=[]
for a in h['assets']:
 ap=REPO/a['path']; hashes={k:sha(ap/f) for k,f in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]}
 expected=a['hashes']; freeze=json.load(open(ap/'modeling-freeze.json')); old=REPO/f'assets/candidates/continuous-small-life-round29-20261020/batch-72/{a["asset_id"]}/r001/modeling-freeze.json'
 origh=sha(old) if old.exists() else None
 check(a['asset_id']+'_six_hashes',hashes==expected,{'expected':expected,'actual':hashes})
 freeze_bad=[]
 for fn,expected_sha in freeze['files'].items():
  fp=ap/fn
  if not fp.is_file() or sha(fp)!=expected_sha: freeze_bad.append(fn)
 original_sha=a.get('original_premodel_freeze_sha256')
 original_path=ap.parent/'r001'/'modeling-freeze.json'
 original_actual=sha(original_path) if original_path.is_file() else None
 current_freeze_sha=sha(ap/'modeling-freeze.json')
 check(a['asset_id']+'_freeze_file_hashes',not freeze_bad,{'bad':freeze_bad,'frozen_files':freeze['files']})
 check(a['asset_id']+'_original_and_selected_freeze_hashes',original_actual==original_sha and current_freeze_sha==a.get('selected_modeling_freeze_sha256'),{'original_expected':original_sha,'original_actual':original_actual,'selected_expected':a.get('selected_modeling_freeze_sha256'),'selected_actual':current_freeze_sha})
 # all four final renders individually verified against render manifest plus pixel-inspection record
 rm=json.load(open(ap/'proof-final/render-manifest.json')); pi=json.load(open(ap/'pixel-inspection.json')); view_errors=[]; dims=[]
 for fr in rm['frames']:
  f=ap/'proof-final'/fr['path']
  if not f.is_file() or sha(f)!=fr['sha256']: view_errors.append(fr['path']); continue
  from PIL import Image
  with Image.open(f) as im:
   dims.append((fr['id'],im.size))
   if im.size!=(512,512): view_errors.append(fr['path']+':dimensions='+repr(im.size))
 view_errors+=[] if pi.get('glb_sha256')==hashes['glb'] and pi.get('manifest_sha256')==sha(ap/'proof-final/render-manifest.json') else ['pixel-inspection target mismatch']
 check(a['asset_id']+'_8frames_and_binding',len(rm['frames'])==8 and not view_errors,{'frame_count':len(rm['frames']),'errors':view_errors,'dimensions':dims,'manifest_sha256':sha(ap/'proof-final/render-manifest.json'),'contact_sha256':sha(ap/'contact-sheet.png')})
 # each concept evidence target, original concept, prompt and generation record hashes
 ce=json.load(open(ap/'concept-evidence.json')); concept_bad=[]
 for kind in ['glb','brief','references','source','generator','config']:
  p=ap/ce['artifacts'][kind]['path']
  if not p.is_file() or sha(p)!=ce['artifacts'][kind]['sha256']: concept_bad.append(kind)
 for kind in ['prompt','generation_record']:
  p=ap/ce['concept'][kind]['path']
  if not p.is_file() or sha(p)!=ce['concept'][kind]['sha256']: concept_bad.append(kind)
 for it in ce['concept']['images']:
  p=ap/it['path']
  if not p.is_file() or sha(p)!=it['sha256']: concept_bad.append(it['id'])
 check(a['asset_id']+'_concept_evidence_hashes',not concept_bad,concept_bad)
 # two real queue producer runs: verify request/result, input binding, PID/time, output digest
 rebuilds=[]; rb_errors=[]
 for i in (1,2):
  rr=json.load(open(ap/f'repro-final-{i}.report.json')); br=rr.get('build_run',{}); req=REPO/br.get('request',{}).get('path',''); res=REPO/br.get('result',{}).get('path','')
  if not req.is_file() or not res.is_file(): rb_errors.append(f'{i}: request/result missing'); continue
  rq=json.load(open(req)); rs=json.load(open(res)); out_dir=Path(rq.get('argv',[])[-1]) if rq.get('argv') else Path('/')
  out=out_dir/'model.glb'; recorded=rs.get('outputs',{}).get('model.glb',{})
  identity=rq.get('identity',{}); ins=identity.get('inputs',{});
  input_expected={'generator':hashes['generator'],'config':hashes['config'],'brief':freeze['files']['brief.json'],'references':hashes['references']}
  input_checks={k:(ins.get(k,{}).get('sha256')==v) for k,v in input_expected.items()}
  run={'index':i,'report_sha256':sha(ap/f'repro-final-{i}.report.json'),'request':rec(req),'result':rec(res),'request_run_id':rq.get('run_id'),'result_status':rs.get('status'),'returncode':rs.get('returncode'),'pid':rs.get('pid'),'started_at':rs.get('started_at'),'finished_at':rs.get('finished_at'),'output_dir':str(out_dir),'output':rec(out) if out.is_file() else None,'result_output_hash':recorded.get('sha256'),'output_matches_final':out.is_file() and sha(out)==hashes['glb'],'input_hash_checks':input_checks,'repro_target_hash':rr.get('glb_sha256'),'rebuilt_hash':rr.get('rebuilt_glb_sha256'),'rebuilt_file_sha':sha(rr['rebuilt_glb_path']) if Path(rr.get('rebuilt_glb_path','')).is_file() else None}
  valid=(rr.get('status')=='pass' and rs.get('status')=='succeeded' and rs.get('returncode')==0 and Path(res).parent==Path(req).parent and rs.get('pid') and rs.get('started_at') and rs.get('finished_at') and out.is_file() and sha(out)==hashes['glb'] and recorded.get('sha256')==hashes['glb'] and all(input_checks.values()) and rr.get('glb_sha256')==hashes['glb'] and rr.get('rebuilt_glb_sha256')==hashes['glb'])
  if not valid: rb_errors.append(f'{i}: evidence binding mismatch')
  rebuilds.append(run)
 distinct=len(rebuilds)==2 and rebuilds[0].get('pid')!=rebuilds[1].get('pid') and rebuilds[0].get('started_at')!=rebuilds[1].get('started_at')
 if not distinct: rb_errors.append('two producer runs not independently identified')
 check(a['asset_id']+'_two_queue_rebuilds',len(rebuilds)==2 and not rb_errors,{'runs':rebuilds,'errors':rb_errors})
 assets.append({'asset_id':a['asset_id'],'revision':a['revision'],'hashes':hashes,'source_blend_bytes':(ap/'source.blend').stat().st_size,'dimensions_verified':dims})
report={'schema_version':1,'task':'independent_batch72_static_qa','source_commit':head,'branch':branch,'base_inventory_sha256':base_sha,'handoff_sha256':sha(W/'HANDOFF.json'),'source_evidence_manifest_sha256':sha(W/'source-evidence-manifest.json'),'source_evidence_files':len(m['files']),'assets':assets,'checks':checks,'status':'pass' if not errors else 'fail','errors':errors}
(QA/'integrity-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'errors':errors,'checks':checks},indent=2))
sys.exit(bool(errors))
