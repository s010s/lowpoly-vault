from pathlib import Path
import subprocess,hashlib,json,os,datetime
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;E=Path('/workspace/shared/lowpoly-batch90-rosary-repair-evidence');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*args,check=True,data=None):return subprocess.run(['git','-c','protocol.allow=never',*args],cwd=R,env=env,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=check)
assert git('branch','--show-current').stdout.decode().strip()=='candidate/batch90-rosary-repair-20261020'
assert not git('diff','--cached','--name-only').stdout
allow={str(p.relative_to(R)):H(p) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
(E/'exact-staging-allowlist.json').write_text(json.dumps({'created_at_host':now(),'base':git('rev-parse','HEAD').stdout.decode().strip(),'files':allow},indent=2)+'\n')
ignored=git('check-ignore','-z','--stdin',check=False,data='\0'.join(allow).encode()+b'\0');assert ignored.returncode in [0,1],ignored.stderr;ig=set(x.decode() for x in ignored.stdout.split(b'\0') if x)
for path,hashval in allow.items():
 assert path.startswith('production/batch90-rosary-repair/') and H(R/path)==hashval
 git('add',*(['-f'] if path in ig else []),'--',path)
staged=set(git('diff','--cached','--name-only','-z').stdout.decode().split('\0'))-{''};assert staged==set(allow),(staged-set(allow),set(allow)-staged)
for path,hashval in allow.items():assert hashlib.sha256(git('show',':'+path).stdout).hexdigest()==hashval,path
result=git('-c','user.name=Leon Made This','-c','user.email=8357465+s010s@users.noreply.github.com','commit','-m','Fix batch90 rosary chamber support within frozen radius')
commit=git('rev-parse','HEAD').stdout.decode().strip()
for path,hashval in allow.items():assert hashlib.sha256(git('cat-file','blob',commit+':'+path).stdout).hexdigest()==hashval,path
status=git('status','--porcelain=v1','--untracked-files=all').stdout.decode();assert not status,status
receipt={'created_at_host':now(),'commit':commit,'branch':'candidate/batch90-rosary-repair-20261020','author':'Leon Made This <8357465+s010s@users.noreply.github.com>','files':len(allow),'all_staged_blobs_readback_verified':True,'all_committed_blobs_readback_verified':True,'clean_status':True,'force_added_only_exact_ignored_paths':sorted(ig),'allowlist_sha256':H(E/'exact-staging-allowlist.json'),'remote_operation':False,'stdout':result.stdout.decode()};(E/'local-commit-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
