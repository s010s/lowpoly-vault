import sys,os,pathlib,hashlib,json,subprocess,datetime
from PIL import Image
sys.dont_write_bytecode=True
W=pathlib.Path('/workspace/shared/lowpoly-batch101-20261021');P=W/'production/small-life-batch101';O=pathlib.Path('/workspace/shared/lowpoly-batch101-independent-qa-20261021');C='4199dfcdb6e93d832b82b341a25935ba59edbc01';BASE='43e40fc89f2b369a5f1858e72fa58a0d10318124';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*args):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(W),*args],env=env)
files=git('diff','--name-only',BASE,C).decode().splitlines();changed=[]
for f in files:
 blob=git('show',C+':'+f);local=(W/f).read_bytes();assert blob==local;changed.append({'path':f,'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'local_equals_commit':True})
checks=[]
for filename in ['submission-manifest.json','original-freeze-manifest.json','dependency-closure-precommit.json']:
 records=json.loads((P/filename).read_text())['files']
 for r in records:
  p=W/r['path'];assert H(p)==r['sha256'],str(p)
  if 'bytes'in r:assert p.stat().st_size==r['bytes']
 checks.append({'manifest':filename,'sha256':H(P/filename),'verified_count':len(records)})
assert H(P/'maker-handoff.json')=='2057fe60812c6d441e09cc0b8446c6704b1c757c253cc1ecc9cd3e3971077692';assert H(P/'original-freeze-manifest.json')=='4d913f5b3716975a8310ffc584d3aeb7f4ce75bf65960e05aa067b67145e7659'
sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb
assets=[]
for a in json.loads((P/'maker-handoff.json').read_text())['assets']:
 aid=a['asset_id'];rev=a['revision'];B=P/aid/rev;D=O/aid;candidate=json.loads((B/'candidate.json').read_text());triplet=a['triplet'];g=B/'artifacts'/f'{aid}.glb'
 for r in candidate['artifacts'].values():assert H(W/r['path'])==r['sha256']
 static=audit_glb(g,14000,6,30);(D/'project-independent.json').write_text(json.dumps(static,indent=2)+'\n');assert not static['errors'];builds=[]
 for label in ['a','b']:
  Q=B/'qa'/('rebuild-'+label);req=json.loads((Q/'request.json').read_text());res=json.loads((Q/'result.json').read_text());ex=json.loads((Q/'execution.json').read_text());output=pathlib.Path(req['argv'][req['argv'].index('--output')+1]);assert res['status']=='succeeded'and res['returncode']==0;assert ex['parent_pid']==res['pid'];assert req['created_at']<=res['started_at']<=ex['started_at_executor_clock']<=ex['finished_at_executor_clock']<=res['finished_at'];assert ex['generator_sha256']==candidate['artifacts']['generator']['sha256'];assert ex['config_sha256']==candidate['artifacts']['config']['sha256'];assert req['identity']['threads']==2;assert req['argv'][:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'];assert H(Q/'execution.json')==res['outputs']['execution.json']['sha256']
  outputs=[]
  for name,r in res['outputs'].items():
   pp=output/name;assert pp.exists(),str(pp);assert H(pp)==r['sha256']and pp.stat().st_size==r['bytes'];outputs.append({'name':name,**r})
  rebuilt=output/aid/(aid+'.glb');rr=audit_glb(rebuilt,14000,6,30);assert rr['semantic_sha256']==static['semantic_sha256'];assert rebuilt.read_bytes()==g.read_bytes();builds.append({'run':label,'request_sha256':H(Q/'request.json'),'result_sha256':H(Q/'result.json'),'execution_sha256':H(Q/'execution.json'),'stdout_sha256':H(Q/'stdout.log'),'stderr_sha256':H(Q/'stderr.log'),'parent_pid':res['pid'],'blender_pid':ex['pid'],'started_at':ex['started_at_executor_clock'],'finished_at':ex['finished_at_executor_clock'],'verified_output_directory':str(output),'actual_output_hashes_verified':outputs,'semantic_sha256':rr['semantic_sha256'],'byte_identical':True})
 assert builds[0]['blender_pid']!=builds[1]['blender_pid'];assert builds[0]['verified_output_directory']!=builds[1]['verified_output_directory'];images=[]
 for vp in [B/'views']+list((B/'details').iterdir()if(B/'details').exists()else[]):
  mf=json.loads((vp/'render-manifest.json').read_text());assert mf['subject']==triplet;assert H(vp/'render-config.json')==mf['config_sha256'];assert mf['source_unchanged'];
  for f in mf['frames']:
   pp=vp/f['path'];assert H(pp)==f['sha256'];assert Image.open(pp).size==(512,512);images.append({'path':str(pp.relative_to(W)),'sha256':H(pp),'size':[512,512]})
 sheet=Image.open(B/'views/contact-sheet.png').convert('RGBA');assert sheet.size==(2048,1088);names=['hero','reversehero','front','side','rear','top','clay','silhouette']
 for i,n in enumerate(names):
  orig=Image.open(B/'views'/f'{n}.png').convert('RGBA');crop=sheet.crop(((i%4)*512,(i//4)*544,(i%4+1)*512,(i//4)*544+512));assert orig.tobytes()==crop.tobytes(),(aid,n)
 renderreq=json.loads((B/'qa/final-render/request.json').read_text());renderres=json.loads((B/'qa/final-render/result.json').read_text());assert renderres['status']=='succeeded';assert renderreq['identity']['threads']==2
 for key in ['glb','brief','references']:
  r=renderreq['identity']['inputs'][key];assert r['sha256']==triplet[{'glb':'glb_sha256','brief':'brief_sha256','references':'references_sha256'}[key]]
 source=json.loads((D/'source-audit.json').read_text());assert source['reexport_identical']and source['source_unchanged'];assets.append({'asset_id':aid,'revision':rev,'triplet':triplet,'source':a['source'],'generator':a['generator'],'config':candidate['artifacts']['config'],'builds':builds,'render_request_sha256':H(B/'qa/final-render/request.json'),'render_result_sha256':H(B/'qa/final-render/result.json'),'render_inputs_pinned':True,'image_hashes':images,'lossless_sheet_verified':True,'sheet_sha256':H(B/'views/contact-sheet.png')})
r={'schema_version':1,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':C,'base_commit':BASE,'changed_path_count':len(changed),'changed_bytes':sum(x['bytes']for x in changed),'changed_paths':changed,'manifest_checks':checks,'assets':assets,'status':'pass','limits':'Existing real execution traces and actual output bytes verified, not an independent rerun of both generators. Independent source reopen/reexport was additionally executed. Filesystem mtimes not used.'};(O/'integrity-provenance.json').write_text(json.dumps(r,indent=2)+'\n');print('integrity',len(changed),sum(x['bytes']for x in changed),[(a['asset_id'],[b['blender_pid']for b in a['builds']])for a in assets])
