import os,sys,json,hashlib,subprocess,pathlib,datetime
from PIL import Image
sys.dont_write_bytecode=True
S=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-20261020');P=S/'production/batch91-archaeopteris-repair';A=P/'archaeopteris/r002';O=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-independent-qa-20261021');OLD=pathlib.Path('/workspace/shared/lowpoly-batch91-20261020');R=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-evidence')
sys.path.insert(0,str(S/'scripts'))
from qa_glb import audit_glb
from check_reproducibility import validate_build_run
load=lambda p:json.loads(pathlib.Path(p).read_text());sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();checks=[];errors=[]
def check(p,h):
 p=pathlib.Path(p);ok=p.is_file() and sha(p)==h;checks.append({'path':str(p),'sha256':h,'ok':ok});assert ok,str(p)
def walk(x,base):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x and isinstance(x['path'],str):
   q=pathlib.Path(x['path']);q=q if q.is_absolute() else base/q
   if not q.exists() and str(x['path']).startswith('production/small-life-batch91'):q=OLD/x['path']
   check(q,x['sha256'])
  for v in x.values():walk(v,base)
 elif isinstance(x,list):
  for v in x:walk(v,base)
H=load(P/'maker-handoff.json');subject=H['subject'];walk(H,S);walk(load(A/'candidate.json'),S);walk(load(A/'delivery-brief.json'),S);walk(load(P/'repair-freeze-v001.json'),S)
for f in ['package-manifest.json','raw-evidence-manifest.json','dependencies.json']:walk(load(P/f),S)
for ref in load(A/'references.json')['sources']:
 assert ref['rights_note'] and not ref['incorporated'] and ref['use']=='consulted-only';walk(ref,S)
assert sha(A/'original-brief.json')==sha(OLD/'production/small-life-batch91/archaeopteris/r001/original-brief.json')
assert sha(A/'references.json')==sha(OLD/'production/small-life-batch91/archaeopteris/r001/references.json')
oldcfg=load(OLD/'production/small-life-batch91/archaeopteris/r001/config.json');newcfg=load(A/'config.json')
for k in ['asset_id','seed','frozen_at','parameters','palette_srgb','design_brief','export']:assert oldcfg[k]==newcfg[k],k
for k,v in load(A/'subject.json').items():
 if k in subject:assert subject[k]==v
manifest=load(P/'package-manifest.json');env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*args):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(S),*args],env=env)
assert not git('status','--porcelain=v1');assert git('rev-parse','HEAD').decode().strip()=='08c1f20150c8a511aae6465074f49542f5e9884e'
diff=git('diff-tree','--no-commit-id','--name-status','-r','HEAD').decode().splitlines();assert all(x.startswith('A\tproduction/batch91-archaeopteris-repair/') for x in diff)
blobs=[]
for item in manifest['files']+load(P/'dependencies.json')['files']+[{'path':'production/batch91-archaeopteris-repair/package-manifest.json','sha256':sha(P/'package-manifest.json')}]:
 b=git('show','HEAD:'+item['path']);assert hashlib.sha256(b).hexdigest()==item['sha256'];blobs.append(item['path'])
oldreport=load('/workspace/shared/lowpoly-batch91-independent-qa-20261020/independent-report.json')
for it in oldreport['items']:
 for x in it['artifacts'].values():check(OLD/x['path'],x['sha256'])
freeze=load(OLD/'production/small-life-batch91/original-freeze-manifest.json')
for p,h in freeze['files'].items():check(OLD/p,h)
oldpkg=load(OLD/'production/small-life-batch91/package-manifest.json') if (OLD/'production/small-life-batch91/package-manifest.json').exists() else None
if oldpkg:walk(oldpkg,OLD)
a=audit_glb(A/'artifacts/archaeopteris.glb',14000,6,30);(O/'project-glb.report.json').write_text(json.dumps(a,indent=2)+'\n');assert not a['errors']
rebuilds=[]
for label in ['a','b']:
 req=load(A/f'qa/rebuild-{label}-request.json');res=load(A/f'qa/rebuild-{label}-result.json');exe=load(A/f'qa/rebuild-{label}-execution.json');out=pathlib.Path(req['argv'][req['argv'].index('--output')+1]);walk(req,S)
 for name,x in res['outputs'].items():check(out/name,x['sha256']);assert (out/name).stat().st_size==x['bytes']
 check(out/'execution.json',sha(A/f'qa/rebuild-{label}-execution.json'))
 fingerprint=validate_build_run(req,res,H['artifacts']['generator']['sha256'],H['artifacts']['config']['sha256'],sha(out/'archaeopteris/archaeopteris.glb'),'archaeopteris/archaeopteris.glb')
 sem=audit_glb(out/'archaeopteris/archaeopteris.glb',14000,6,30)['semantic_sha256'];assert sem==a['semantic_sha256'];assert exe['parent_pid']==res['pid'];assert req['created_at']<=res['started_at']<=exe['started_at']<exe['finished_at']<=res['finished_at'];assert exe['generator_sha256']==H['artifacts']['generator']['sha256'];assert exe['config_sha256']==H['artifacts']['config']['sha256'];assert req['argv'][:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'];assert exe['argv'][exe['argv'].index('--threads')+1]=='2'
 rebuilds.append({'label':label,'pid':exe['pid'],'wrapper_pid':res['pid'],'fingerprint':fingerprint,'started_at':exe['started_at'],'finished_at':exe['finished_at'],'semantic_sha256':sem,'sha256':sha(out/'archaeopteris/archaeopteris.glb'),'all_input_output_hashes_match':True})
assert len({x['pid'] for x in rebuilds})==2 and len({x['fingerprint'] for x in rebuilds})==2
rqs=list((R/'final-render-queue').rglob('request.json'));assert len(rqs)==1;rq=rqs[0];req=load(rq);res=load(rq.parent/'result.json');walk(req,S);rm=load(A/'views/render-manifest.json');bound=load(A/'subject.json')['bound_at'];assert bound<req['created_at']<=res['started_at']<rm['created_at']<=res['finished_at'];assert res['status']=='succeeded' and res['returncode']==0
assert rm['subject']==subject
for key in ['glb','brief','references']:assert req['identity']['inputs'][key]['sha256']==subject[key+'_sha256']
for n,x in res['outputs'].items():check(rq.parent/'outputs'/n,x['sha256']);check(A/'views'/n,x['sha256'])
sheet=Image.open(A/'views/contact-sheet.png');assert sheet.size==(2048,1088) and sheet.format=='PNG';frames=[]
for j,f in enumerate(rm['frames']):
 im=Image.open(A/'views'/f['path']);assert im.size==(512,512) and im.format=='PNG';check(A/'views'/f['path'],f['sha256']);tile=sheet.crop(((j%4)*512,(j//4)*544,(j%4)*512+512,(j//4)*544+512));assert tile.convert('RGB').tobytes()==im.convert('RGB').tobytes();frames.append({'id':f['id'],'sha256':f['sha256'],'png_size':[512,512],'sheet_tile_identical':True,'raw_output_identical':True})
command=[sys.executable,'-B',str(S/'scripts/validate_candidate.py'),str(A/'candidate.json'),'--root',str(S),'--profile','static-stylized-v1','--profile-contract',str(A/'profile-contract.json'),'--json'];p=subprocess.run(command,capture_output=True,text=True,env={**env,'PYTHONDONTWRITEBYTECODE':'1'});(O/'candidate-schema.report.json').write_text(p.stdout);(O/'candidate-schema.stderr.txt').write_text(p.stderr);assert p.returncode==0,p.stdout+p.stderr
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pass','subject':subject,'checks':checks,'checked_hash_records':len(checks),'package_files':len(manifest['files']),'raw_files':len(load(P/'raw-evidence-manifest.json')['files']),'committed_blobs':blobs,'changed_paths':diff,'all_changes_additive_repair_only':True,'original_inputs_and_other_three_assets_unchanged':True,'original_freeze_file_count':len(freeze['files']),'config_original_parameters_seed_palette_identical':True,'rebuilds':rebuilds,'final_binding_at':bound,'final_render_requested_at':req['created_at'],'final_render_started_at':res['started_at'],'final_render_completed_at':res['finished_at'],'frames':frames,'sheet_sha256':sha(A/'views/contact-sheet.png'),'schema_returncode':p.returncode,'limitations':'Queue times/PIDs are recorded attestations backed by independently verified actual inputs/outputs. No filesystem mtime inferred chronology, no network operation.'}
(O/'closure.report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','checked_hash_records','package_files','raw_files','original_freeze_file_count','rebuilds']},indent=2))
