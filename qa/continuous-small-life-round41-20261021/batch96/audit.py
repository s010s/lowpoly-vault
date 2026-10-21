from pathlib import Path
import sys,os,json,hashlib,subprocess,datetime,shutil
from PIL import Image,ImageChops
R=Path('/workspace/shared/lowpoly-batch96-20261020');P=R/'production/batch96';Q=Path('/workspace/shared/lowpoly-batch96-independent-qa-20261021');E=Path('/workspace/shared/lowpoly-batch96-evidence')
os.environ.update(GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0',PYTHONDONTWRITEBYTECODE='1')
sys.path.insert(0,str(R/'scripts'));from qa_glb import audit_glb
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,d):
 with Path(p).open('x')as f:json.dump(d,f,indent=2);f.write('\n')
def run(name,cmd):
 st=now();log=Q/(name+'.log');save(Q/(name+'.request.json'),{'requested_at':st,'command':cmd})
 with log.open('x')as f:
  pr=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);rc=pr.wait()
 save(Q/(name+'.process.json'),{'started_at':st,'ended_at':now(),'runner_pid':pr.pid,'returncode':rc,'command':cmd,'log_sha256':H(log)})
 print(name,rc,flush=True)
 if rc:raise RuntimeError(name+' failed')
git=lambda *a:subprocess.check_output(['git','-c','protocol.allow=never',*a],cwd=R)
head=git('rev-parse','HEAD').decode().strip();assert head=='37a0a42092c6b7a5f02a3f6e72436dfe92191122';assert not git('status','--porcelain')
hand=json.load(open(P/'maker-handoff.json'));assert H(P/'maker-handoff.json')=='ae63042d5591b4a3c1eee27ee9372483b2fac198484b489f0478e7c9062061b5'
manifest=json.load(open(P/'DELIVERY-MANIFEST.json'));verified=[]
for e in manifest['files']:
 p=R/e['path'];assert p.stat().st_size==e['bytes'] and H(p)==e['sha256'],p
 blob=git('show',head+':'+e['path']);assert hashlib.sha256(blob).hexdigest()==e['sha256'],p
 verified.append(e['path'])
raw=json.load(open(P/'local-preservation-inventory.json'));raw_errors=[]
for e in raw['files']:
 p=Path(e['path'])
 if not p.exists()or p.stat().st_size!=e['bytes']or H(p)!=e['sha256']:raw_errors.append(e['path'])
inv=json.load(open(P/'batch-96-selected-inventory.json'));b=git('show',inv['source_inventory_commit']+':'+inv['source_inventory_path']);assert hashlib.sha256(b).hexdigest()==inv['source_inventory_sha256'];full=json.loads(b)
if isinstance(full,dict):full=full.get('assets',full.get('items',[]))
selected={x['id']:x for x in full if x['id'] in [a['id']for a in inv['assets']]};assert all(selected[a['id']]==a for a in inv['assets'])
freeze=json.load(open(P/'original-freeze-manifest.json'));freezechecks={};frames={};closure={}
for a in hand['selected_assets']:
 aid=a['asset_id'];rev=a['revision'];B=R/a['path'];D=Q/aid;D.mkdir(exist_ok=True)
 for key,n in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]:assert H(B/n)==a['hashes'][key]
 for n,h in freeze['assets'][aid]['files'].items():assert H(B.parent/'r001'/n)==h and H(B/n)==h
 freezechecks[aid]={'original_and_final_frozen_files_equal':True,'freeze':freeze['assets'][aid]['frozen_at'],'geometry_started_at':json.load(open(B/'execution.json'))['started_at']}
 dep=json.load(open(B/'build-dependencies.json'));assert all(H(R/n)==h for n,h in dep['inputs'].items());assert H(R/'package-lock.json')==dep['node_lockfile_sha256'];closure[aid]=dep
 d=audit_glb(B/'model.glb',14000,6,30);save(D/'project-audit.json',d);assert not d['errors'] and d['bytes']<=1000000
 rm=json.load(open(B/'proof-final/render-manifest.json'));bind=json.load(open(B/'preproof-binding.json'));assert bind['glb_sha256']==H(B/'model.glb')and bind['brief_sha256']==H(B/'candidate-brief.json')and bind['references_sha256']==H(B/'references.json')
 assert rm['subject']['glb_sha256']==H(B/'model.glb')and rm['subject']['brief_sha256']==H(B/'candidate-brief.json')and rm['subject']['references_sha256']==H(B/'references.json')
 stages=[json.loads(l)for l in open(B/'lifecycle.jsonl')];render=[s for s in stages if s['stage']=='proof-final'][-1];assert render['exit_code']==0 and bind['checked_at']<render['started_at']<rm['created_at']
 sheet=Image.open(B/'contact-sheet.png').convert('RGB');checks=[]
 for i,f in enumerate(rm['frames']):
  p=B/'proof-final'/f['path'];assert H(p)==f['sha256'];im=Image.open(p).convert('RGB');assert im.size==(512,512)
  # Contact-sheet composition metadata is tested by lossless exact pixel search, never thumbnail resemblance.
  matches=[]
  for y in range(0,sheet.height-511,512):
   for x in range(0,sheet.width-511,512):
    if ImageChops.difference(im,sheet.crop((x,y,x+512,y+512))).getbbox()is None:matches.append([x,y])
  checks.append({'view':f['id'],'path':str(p),'sha256':H(p),'size':list(im.size),'lossless_sheet_matches':matches})
 frames[aid]={'sheet_size':list(sheet.size),'sheet_sha256':H(B/'contact-sheet.png'),'frames':checks,'preproof_binding_at':bind['checked_at'],'render_started':render['started_at'],'render_completed':rm['created_at'],'all_exact':all(x['lossless_sheet_matches'] for x in checks)}
 save(D/'frozen-subject.json',a)
save(Q/'readback.json',{'created_at':now(),'commit':head,'branch':git('branch','--show-current').decode().strip(),'clean':True,'handoff_sha256':H(P/'maker-handoff.json'),'delivery_manifest_verified_local_and_committed_blobs':len(verified),'raw_preservation_entries':len(raw['files']),'raw_preservation_errors':raw_errors,'inventory_original_hash_verified':True,'freezes':freezechecks,'closure':closure,'frames':frames})
print('READBACK',len(verified),'raw_errors',raw_errors,'sheets',[x['all_exact']for x in frames.values()],flush=True)
bl=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
run('node-audit',['node',str(Q/'node-audit.mjs')])
for a in hand['selected_assets']:
 aid=a['asset_id'];B=R/a['path'];D=Q/aid
 run(aid+'-source',bl+[str(R/'scripts/check_source_export.py'),'--','--source',str(B/'source.blend'),'--glb',str(B/'model.glb'),'--output',str(D/'source-reopen.json'),'--collection','EXPORT'])
 run(aid+'-geometry',bl+[str(Q/'geometry.py'),'--',str(B),str(D)])
 jobs=[]
 for i in [1,2]:
  jobs.append({'asset_id':aid,'revision':a['revision'],'job_id':'independent-rebuild-'+str(i),'inputs':{'generator':str(B/'generator.py'),'config':str(B/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py')},'argv':['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','{blender}','-b','--threads','{threads}','--python-exit-code','1','--factory-startup','--disable-autoexec','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json','execution.json']})
 q=D/'queue.json';save(q,{'schema_version':1,'lane':'build','jobs':jobs})
 run(aid+'-queue',['python3',str(R/'scripts/run_asset_queue.py'),str(q),'--runs-root',str(Q/'rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','3600','--allow-executable','/usr/bin/flock'])
 results=sorted((Q/'rebuild-runs/build'/aid).rglob('result.json'));assert len(results)==2
 pids=[]
 for i,r in enumerate(results,1):
  pids.append(json.load(open(r.parent/'outputs/execution.json'))['pid'])
  run(aid+'-repro-'+str(i),['python3',str(R/'scripts/check_reproducibility.py'),'--glb',str(B/'model.glb'),'--rebuilt-glb',str(r.parent/'outputs/model.glb'),'--generator',str(B/'generator.py'),'--config',str(B/'build-config.json'),'--build-request',str(r.parent/'request.json'),'--build-result',str(r),'--rebuilt-output','model.glb','--root',str(Q),'--output',str(D/('repro-'+str(i)+'.json'))])
 assert len(set(pids))==2
 save(D/'rebuild-pids.json',{'pids':pids,'distinct':True})
print('AUDIT_DONE',flush=True)
