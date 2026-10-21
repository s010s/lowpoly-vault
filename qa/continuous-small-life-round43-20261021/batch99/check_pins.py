import pathlib,json,hashlib,subprocess,os,sys,datetime
W=pathlib.Path('/workspace/shared/lowpoly-batch99-20261021'); Q=pathlib.Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021'); B=W/'production/small-life-batch99'; C='e872d300c1c58ad9770cab8ba5996c9d6c868d14';env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0',PYTHONDONTWRITEBYTECODE='1')
def git(*a):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(W),*a],env=env)
def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(p.read_text())
def pin(p,h,n=None,blob=False):
 p=pathlib.Path(p);p=p if p.is_absolute() else W/p;b=p.read_bytes();assert sha(b)==h,(p,sha(b),h)
 if n is not None:assert len(b)==n,p
 if blob:assert git('show',C+':'+str(p.relative_to(W)))==b,p
 return {'path':str(p),'sha256':h,'bytes':len(b),'git_blob_checked':blob}
assert git('rev-parse','HEAD').decode().strip()==C
parent=git('show','-s','--format=%P',C).decode().strip();assert parent=='43e40fc89f2b369a5f1858e72fa58a0d10318124'
manifest=B/'submission-manifest.json';assert sha(manifest.read_bytes())=='102f824e119ae2fbe781edf83adf7badeb1368ce4c072b7f2af992a9f4ccbaad'
files=[pin(f['path'],f['sha256'],f['bytes'],True) for f in load(manifest)['files']]; files.append(pin(manifest,sha(manifest.read_bytes()),blob=True))
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',C).decode().splitlines());assert changed=={str(pathlib.Path(f['path']).relative_to(W)) for f in files}
freeze=B/'original-freeze-manifest.json';assert sha(freeze.read_bytes())=='120f41ebbfef8a292b8cbaad96295780b384aa1ef273ac4e37031861d86a19d6'
freeze_files=[pin(f['path'],f['sha256'],f['bytes'],True) for f in load(freeze)['files']]
d=load(B/'dependency-closure-precommit.json'); deps=[pin(f['path'],f['sha256'],blob=True) for f in d['files']+[d['extra_qa_helper']]]
sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb,read_glb,semantic_digest
assets=[]
for a,r in [('monetianthus','r001'),('quereuxia','r001'),('palaeocarpinus','r001'),('proterocladus','r002')]:
 root=B/a/r; cand=load(root/'candidate.json');artifact_pins=[pin(x['path'],x['sha256'],blob=True) for x in cand['artifacts'].values()];glb=W/cand['artifacts']['glb']['path'];expected=semantic_digest(*read_glb(glb)[:2]);rebuilds=[]
 for run in ['a','b']:
  rr=root/'qa'/('rebuild-'+run);req=load(rr/'request.json');exe=load(rr/'execution.json');res=load(rr/'result.json');out=pathlib.Path(req['argv'][-1]);assert res['status']=='succeeded' and res['returncode']==0;assert exe['parent_pid']==res['pid'];assert exe['pid']!=res['pid'];assert req['argv'][:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'];assert exe['argv'][exe['argv'].index('--threads')+1]=='2'
  rawpins=[pin(out/n,f['sha256'],f['bytes']) for n,f in res['outputs'].items()];raw_glb=out/a/(a+'.glb');semantic=semantic_digest(*read_glb(raw_glb)[:2]);assert semantic==expected;assert exe['generator_sha256']==cand['artifacts']['generator']['sha256'];assert exe['config_sha256']==cand['artifacts']['config']['sha256'];assert exe['started_at_executor_clock']<exe['finished_at_executor_clock'];assert req['created_at']<=exe['started_at_executor_clock']<res['finished_at'];rebuilds.append({'run':run,'real_blender_pid':exe['pid'],'flock_pid':res['pid'],'started_at':exe['started_at_executor_clock'],'finished_at':exe['finished_at_executor_clock'],'raw_output_pins':rawpins,'semantic_sha256':semantic})
 assert rebuilds[0]['real_blender_pid']!=rebuilds[1]['real_blender_pid']
 refs=[pin(f['path'],f['sha256']) for s in load(root/'references.json')['sources'] for f in s.get('consult_only_files',[])]
 audit=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30);(Q/(a+'-project-audit.json')).write_text(json.dumps(audit,indent=2)+'\n')
 assets.append({'asset_id':a,'revision':r,'artifact_pins':artifact_pins,'raw_rebuilds':rebuilds,'reference_pins':refs,'glb_semantic_sha256':expected})
r={'status':'pass','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':C,'parent':parent,'submission_file_count':len(files),'submission_bytes':sum(x['bytes'] for x in files),'file_checks':files,'freeze_checks':freeze_files,'dependency_checks':deps,'assets':assets,'source_mutated':False};(Q/'pin-and-rebuild-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['file_checks','freeze_checks','dependency_checks','assets']}))
