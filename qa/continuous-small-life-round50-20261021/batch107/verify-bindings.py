import json,hashlib,pathlib,subprocess,os,datetime,re
R=pathlib.Path('/workspace/shared/lowpoly-batch107-20261021');B=R/'production/small-life-batch107';O=pathlib.Path('/workspace/shared/lowpoly-batch107-independent-qa-20261021');C='447d7976d5a94aa59c0c2d36ef7985e035ef440f'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text())
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');git=lambda *a:subprocess.check_output(['git','-c','protocol.allow=never','-C',str(R),*a],env=env)
assert git('rev-parse','HEAD').decode().strip()==C
errors=[]; records=[]
for name,sha in {'maker-handoff.json':'1c5cd7de2b63bf99eddb85e6b59b17adb5ab8f022114701fd9452ebd68cf48a9','submission-manifest.json':'0a91edcea8bd69d62655d931258de9b85fc415185c243721689acf806923d4ff','original-freeze-manifest.json':'9355fd049c9028a7fce6924b3fa7d32a756ca99d4c3fc9f17fe705ce4e7632c9'}.items():
 assert h(B/name)==sha,name
for name in ['submission-manifest.json','original-freeze-manifest.json','dependencies.json']:
 for f in j(B/name)['files']:
  p=R/f['path']; ok=p.exists() and h(p)==f['sha256']; committed=git('show',C+':'+f['path']); ok=ok and committed==p.read_bytes();records.append({'manifest':name,'path':f['path'],'sha256':h(p),'bytes':p.stat().st_size,'verified':ok})
  if not ok:errors.append(f['path'])
# Verify every explicit path/hash pair in committed JSON, including raw-source/rebuild outputs.
refs=[]
def walk(x,origin):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x and isinstance(x['path'],str):
   p=pathlib.Path(x['path']);p=p if p.is_absolute() else R/p
   if p.exists():
    ok=h(p)==x['sha256'];refs.append({'origin':origin,'path':str(p),'verified':ok});
    if not ok:errors.append(origin+':'+str(p))
   else:refs.append({'origin':origin,'path':str(p),'verified':None,'note':'Not a root-resolved current file; inspect relative path context.'})
  for y in x.values():walk(y,origin)
 elif isinstance(x,list):
  for y in x:walk(y,origin)
for f in B.rglob('*.json'):walk(j(f),str(f.relative_to(R)))
freeze=j(B/'original-freeze-manifest.json');chr=j(B/'chronology/timing-observation.json');retired=[]
for p in pathlib.Path('/workspace/shared/lowpoly-batch107-evidence').glob('retired-pre-final-binding*/relocation.json'):retired.append({'path':str(p),'sha256':h(p),'record':j(p)})
report={'stage':'identity_and_freeze','status':'pass' if not errors else 'fail','commit':C,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git_status':git('status','--porcelain','--untracked-files=no').decode(),'manifest_entries':records,'explicit_path_hash_bindings':refs,'errors':errors,'freeze_chronology':chr,'retired_binding_history':retired,'qualification':'Historical times are maker records, not independently observed past execution; current bytes and retained queue outputs independently verified.'}
(O/'identity-freeze-report.json').write_text(json.dumps(report,indent=2)+'\n');print('records',len(records),'refs',len(refs),'errors',errors,'unresolved',sum(x['verified'] is None for x in refs))
