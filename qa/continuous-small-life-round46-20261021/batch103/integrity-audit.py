import pathlib,json,hashlib,subprocess,os,datetime
from PIL import Image
W=pathlib.Path('/workspace/shared/lowpoly-batch103-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch103-independent-qa-20261021');B=W/'production/small-life-batch103';C='f2f79a6b4762d5e76bf7ef18111d6d23561f136a';env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_text());out={'commit':C,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':[]};err=out['errors']
def git(*args):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(W),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==C
out['branch']=git('branch','--show-current').decode().strip();out['parents']=git('show','-s','--format=%P',C).decode().strip().split();out['worktree_status']=git('status','--porcelain').decode()
paths=git('ls-tree','-r','--name-only',C,'production/small-life-batch103').decode().splitlines();rows=[]
for p in paths:
 raw=git('show',C+':'+p);local=(W/p).read_bytes();same=raw==local;rows.append({'path':p,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'local_exact':same})
 if not same:err.append('local_commit_mismatch:'+p)
out['committed_payload']=rows;out['committed_file_count']=len(rows);out['committed_bytes']=sum(r['bytes']for r in rows)
for f in ['submission-manifest.json','original-freeze-manifest.json','dependencies.json']:
 d=J(B/f);checked=[]
 for row in d['files']:
  p=W/row['path'];ok=p.exists() and H(p)==row['sha256'];checked.append({'path':row['path'],'match':ok})
  if not ok:err.append(f+':'+row['path'])
 out[f]=checked
extras=['production/policies/qa-passed-batch-publication-20261018.json','production/small-life-batch103/tools/render-ventral-detail.py'];out['dependency_commit_closure']=[]
for p in [r['path']for r in J(B/'dependencies.json')['files']]+extras:
 raw=git('show',C+':'+p);out['dependency_commit_closure'].append({'path':p,'sha256':hashlib.sha256(raw).hexdigest(),'matches_local':raw==(W/p).read_bytes()})
 if raw!=(W/p).read_bytes():err.append('dependency_commit:'+p)
hand=J(B/'maker-handoff.json');out['handoff_sha256']=H(B/'maker-handoff.json');pins=[]
def pinwalk(x):
 if isinstance(x,dict):
  if 'path'in x and 'sha256'in x:
   p=W/x['path'];ok=p.exists()and H(p)==x['sha256'];pins.append({'path':x['path'],'match':ok})
   if not ok:err.append('handoff_pin:'+x['path'])
  for v in x.values():pinwalk(v)
 elif isinstance(x,list):
  for v in x:pinwalk(v)
pinwalk(hand);out['handoff_pins']=pins
out['assets']=[]
for a in hand['assets']:
 aid=a['asset_id'];p=B/aid/'r001';trip={'revision':'r001','glb_sha256':H(p/'artifacts'/f'{aid}.glb'),'brief_sha256':H(p/'delivery-brief.json'),'references_sha256':H(p/'references.json')};assert trip==a['triplet']==J(p/'candidate-binding.json')['subject'];row={'asset_id':aid,'triplet':trip,'renders':[],'rebuilds':[]};orig=J(p/'original-brief.json');delivery=J(p/'delivery-brief.json');row['original_brief_preserved']=all(delivery.get(k)==v for k,v in orig.items() if k!='brief_version') and delivery['brief_version']=='delivery-v001';row['delivery_added_keys']=list(set(delivery)-set(orig))
 if not row['original_brief_preserved']:err.append('brief_modified:'+aid)
 for folder in [p/'views']+list((p/'details').glob('*')):
  man=J(folder/'render-manifest.json');assert man['subject']==trip and man['source_glb_sha256']==trip['glb_sha256'];frames=[]
  for f in man['frames']:
   q=folder/f['path'];assert H(q)==f['sha256'];im=Image.open(q);assert im.size==(512,512);frames.append({'path':str(q.relative_to(W)),'sha256':H(q),'size':list(im.size)})
  row['renders'].append({'directory':str(folder.relative_to(W)),'manifest_sha256':H(folder/'render-manifest.json'),'subject_matches':True,'frames':frames})
 sheet=Image.open(p/'views/contact-sheet.png');same=[]
 for n,name in enumerate(orig['required_views']):
  frame=Image.open(p/'views'/f'{name}.png');crop=sheet.crop(((n%4)*512,(n//4)*544,(n%4+1)*512,(n//4)*544+512));same.append(crop.convert('RGB').tobytes()==frame.convert('RGB').tobytes())
 row['contact_sheet_lossless_tiles']=same
 if not all(same):err.append('sheet_tiles:'+aid)
 for run in ['a','b']:
  d=p/'qa'/('rebuild-'+run);req=J(d/'request.json');res=J(d/'result.json');exe=J(d/'execution.json');assert res['status']=='succeeded' and res['returncode']==0;assert req['fingerprint']==res['fingerprint'];argv=req['argv'];assert argv[0]=='/usr/bin/flock' and argv[1]=='/tmp/lowpoly-production-blender.lock' and argv[argv.index('--threads')+1]=='2';inputs=[]
  for key,r in req['identity']['inputs'].items():
   q=pathlib.Path(r['path']);ok=q.exists()and H(q)==r['sha256'];inputs.append({'key':key,'match':ok})
   if not ok:err.append('rebuild_input:'+aid+':'+run+':'+key)
  outputsdir=pathlib.Path(argv[argv.index('--output')+1]);rawfile=outputsdir/aid/(aid+'.glb');report=J(p/'qa'/('reproducibility-'+run+'.report.json'));rawok=rawfile.exists() and H(rawfile)==trip['glb_sha256'];assert H(outputsdir/'execution.json')==H(d/'execution.json');assert exe['generator_sha256']==a['generator']['sha256'];assert exe['config_sha256']==H(p/'config.json');assert exe['pid']!=res['pid'];assert res['outputs'][f'{aid}/{aid}.glb']['sha256']==trip['glb_sha256'];assert report['semantic_match'];row['rebuilds'].append({'run':run,'actual_blender_pid':exe['pid'],'queue_pid':res['pid'],'started':exe['started_at_executor_clock'],'finished':exe['finished_at_executor_clock'],'inputs':inputs,'raw_rebuilt_glb_sha256':H(rawfile)if rawfile.exists()else None,'raw_output_byte_identical':rawok,'semantic_sha256':report['semantic_sha256'],'semantic_match':report['semantic_sha256']==report['rebuilt_semantic_sha256'],'blocking_lock_and_threads2':True})
  if not rawok:err.append('raw_rebuild:'+aid+':'+run)
 assert len(set(r['actual_blender_pid']for r in row['rebuilds']))==2
 out['assets'].append(row)
out['checker_correction']='Initial check incorrectly treated original-v001 to delivery-v001 schema role label as a changed requirement. The original file and every scientific/visual/numeric requirement are identical; original failed report retained in integrity-provenance-v1.json.';out['freeze_time']=J(B/'original-freeze-manifest.json')['frozen_at'];out['freeze_readback']=J(B/'freeze-readback-before-geometry.json');out['first_request']=J(B/'chronology/first-geometry-queue-request.json')['created_at'];out['concept_receipts']=[J(B/'concepts'/f'{a}-receipt.json')for a in ['habelia','alalcomenaeus','plenocaris','nectocaris']];out['status']='pass'if not err else'fail';(O/'integrity-provenance.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],err,out['committed_file_count'],out['committed_bytes'],len(pins))
