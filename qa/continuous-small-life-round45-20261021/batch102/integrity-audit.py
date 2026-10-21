import sys,os,pathlib,hashlib,json,subprocess,datetime
from PIL import Image
sys.dont_write_bytecode=True
W=pathlib.Path('/workspace/shared/lowpoly-batch102-20261021');P=W/'production/small-life-batch102';O=pathlib.Path('/workspace/shared/lowpoly-batch102-independent-qa-20261021');C='df19360a8d19068395f93c9da394c371f2ffb91d';BASE='43e40fc89f2b369a5f1858e72fa58a0d10318124';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*args):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(W),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==C
files=git('diff','--name-only',BASE,C).decode().splitlines();changed=[]
for f in files:
 blob=git('show',C+':'+f);local=(W/f).read_bytes();assert blob==local;changed.append({'path':f,'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'local_equals_commit':True})
checks=[];dep=[]
for filename in ['delivery-manifest.json','original-freeze-manifest.json','build-dependencies.json','build-dependencies-v002.json']:
 d=json.loads((P/filename).read_text());records=d['files']
 for r in records:
  p=W/r['path'];assert H(p)==r['sha256'],str(p)
  if 'bytes'in r:assert p.stat().st_size==r['bytes']
  if filename.startswith('build-'):assert git('show',C+':'+r['path'])==p.read_bytes()
 for r in d.get('external_read_only_runtime',[]):assert H(pathlib.Path(r['path']))==r['sha256'];dep.append(r)
 if 'blender_binary'in d:assert H(pathlib.Path(d['blender_binary']['path']))==d['blender_binary']['sha256']
 checks.append({'manifest':filename,'sha256':H(P/filename),'verified_count':len(records)})
assert H(P/'handoff.json')=='10524d63485ebc105ef89a2bec46b6d6b7826bcddf95fed77b46815b03bc2db7';assert H(P/'original-freeze-manifest.json')=='ad788d2d7fac0c03b591cc0b61d64d941ffc26d25af916410cfde4c0452c256f'
sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb
assets=[]
for a in json.loads((P/'handoff.json').read_text())['items']:
 aid=a['asset_id'];rev=a['revision'];B=P/aid/rev;D=O/aid;candidate=json.loads((B/'candidate.json').read_text());triplet={k:v for k,v in json.loads((B/'subject.json').read_text()).items()if k!='bound_at'};g=B/'artifacts'/f'{aid}.glb'
 for r in candidate['artifacts'].values():assert H(W/r['path'])==r['sha256']
 static=audit_glb(g,14000,6,30);(D/'project-independent.json').write_text(json.dumps(static,indent=2)+'\n');assert not static['errors'];builds=[]
 prov=json.loads((B/'qa/execution-provenance.json').read_text())
 for label in ['a','b']:
  Q=B/'qa';rq=Q/('rebuild-'+label+'-request.json');rs=Q/('rebuild-'+label+'-result.json');exf=Q/('rebuild-'+label+'-execution.json');req=json.loads(rq.read_text());res=json.loads(rs.read_text());ex=json.loads(exf.read_text());output=pathlib.Path(req['argv'][req['argv'].index('--output')+1]);assert res['status']=='succeeded'and res['returncode']==0;assert ex['parent_pid']==res['pid'];assert req['created_at']<=res['started_at']<=ex['started_at']<=ex['finished_at']<=res['finished_at'];assert ex['generator_sha256']==candidate['artifacts']['generator']['sha256'];assert ex['config_sha256']==candidate['artifacts']['config']['sha256'];assert req['identity']['threads']==2;assert req['argv'][:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'];assert H(exf)==res['outputs']['execution.json']['sha256']
  raw=pathlib.Path(next(x for x in prov['two_distinct_real_rebuilds']if x['label']==label)['raw_path']);assert (raw/'request.json').read_bytes()==rq.read_bytes();assert(raw/'result.json').read_bytes()==rs.read_bytes();outputs=[]
  for name,r in res['outputs'].items():
   pp=output/name;assert pp.exists(),str(pp);assert H(pp)==r['sha256']and pp.stat().st_size==r['bytes'];outputs.append({'name':name,**r})
  rebuilt=output/aid/(aid+'.glb');rr=audit_glb(rebuilt,14000,6,30);assert rr['semantic_sha256']==static['semantic_sha256'];assert rebuilt.read_bytes()==g.read_bytes();builds.append({'run':label,'request_sha256':H(rq),'result_sha256':H(rs),'execution_sha256':H(exf),'stdout_sha256':H(raw/'stdout.log'),'stderr_sha256':H(raw/'stderr.log'),'parent_pid':res['pid'],'blender_pid':ex['pid'],'started_at':ex['started_at'],'finished_at':ex['finished_at'],'verified_output_directory':str(output),'actual_output_hashes_verified':outputs,'semantic_sha256':rr['semantic_sha256'],'byte_identical':True})
 assert builds[0]['blender_pid']!=builds[1]['blender_pid'];assert builds[0]['verified_output_directory']!=builds[1]['verified_output_directory'];images=[]
 for vp in [B/'views']+([B/'detail']if(B/'detail').exists()else[]):
  mf=json.loads((vp/'render-manifest.json').read_text());assert mf['subject']==triplet;assert H(vp/'render-config.json')==mf['config_sha256'];assert mf['source_unchanged'];assert mf['source_glb_sha256']==H(g)
  for f in mf['frames']:
   pp=vp/f['path'];assert H(pp)==f['sha256'];assert Image.open(pp).size==(512,512);images.append({'path':str(pp.relative_to(W)),'sha256':H(pp),'size':[512,512]})
 sheet=Image.open(B/'views/contact-sheet.png').convert('RGBA');assert sheet.size==(2048,1088);names=['hero','reversehero','front','side','rear','top','clay','silhouette']
 for i,n in enumerate(names):
  orig=Image.open(B/'views'/f'{n}.png').convert('RGBA');crop=sheet.crop(((i%4)*512,(i//4)*544,(i%4+1)*512,(i//4)*544+512));assert orig.tobytes()==crop.tobytes(),(aid,n)
 renderreq=json.loads((B/'qa/final-render-request.json').read_text());renderres=json.loads((B/'qa/final-render-result.json').read_text());assert renderres['status']=='succeeded';assert renderreq['identity']['threads']==2
 for key in ['glb','brief','references']:
  r=renderreq['identity']['inputs'][key];assert r['sha256']==triplet[{'glb':'glb_sha256','brief':'brief_sha256','references':'references_sha256'}[key]]
 source=json.loads((D/'source-audit.json').read_text());re=json.loads((D/'reexport-full.json').read_text());assert re['byte_identical']and source['source_unchanged'];refs=json.loads((P/aid/'r001/references.json').read_text());consult=[]
 for s in refs['sources']:
  for r in s['consult_only_files']:assert H(pathlib.Path(r['path']))==r['sha256'];consult.append(r)
 assets.append({'asset_id':aid,'revision':rev,'triplet':triplet,'artifacts':candidate['artifacts'],'builds':builds,'render_request_sha256':H(B/'qa/final-render-request.json'),'render_result_sha256':H(B/'qa/final-render-result.json'),'render_inputs_pinned':True,'image_hashes':images,'lossless_sheet_verified':True,'sheet_sha256':H(B/'views/contact-sheet.png'),'consult_source_hashes_verified':consult,'source_reexport_byte_identical':True})
r={'schema_version':1,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':C,'base_commit':BASE,'changed_path_count':len(changed),'changed_bytes':sum(x['bytes']for x in changed),'changed_paths':changed,'manifest_checks':checks,'external_dependency_checks':dep,'assets':assets,'status':'pass','limits':'Existing separate real generator PID queue traces and actual retained output bytes verified, not claimed as two new generator reruns. Fresh independent source reopen/reexport additionally performed. No filesystem mtimes used.'};(O/'integrity-provenance.json').write_text(json.dumps(r,indent=2)+'\n');print('integrity',len(changed),sum(x['bytes']for x in changed),[(a['asset_id'],[b['blender_pid']for b in a['builds']])for a in assets])
