import json,pathlib,hashlib,subprocess,os,datetime
R=pathlib.Path('/workspace/shared/lowpoly-batch108-20261021');O=pathlib.Path(__file__).parent;env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*a,data=None):return subprocess.check_output(['git','-c','protocol.allow=never',*a],cwd=R,env=env,input=data)
rows=[]
for line in git('ls-tree','-r','HEAD','production/batch-108').decode().splitlines():
 left,path=line.split('\t',1);mode,kind,oid=left.split();rows.append({'path':path,'commit_git_blob':oid})
actual=git('hash-object','--no-filters','--stdin-paths',data=('\n'.join(x['path'] for x in rows)+'\n').encode()).decode().splitlines()
for r,h in zip(rows,actual):r.update(local_git_blob=h,match=h==r['commit_git_blob'])
unchanged=[]
for r in json.loads((O/'source-baseline.json').read_text()):
 p=pathlib.Path(r['path']);h=hashlib.sha256(p.read_bytes()).hexdigest();unchanged.append({'path':r['path'],'sha256':h,'match':h==r['sha256']})
report={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':git('rev-parse','HEAD').decode().strip(),'all_commit_bytes_match':all(x['match'] for x in rows),'commit_files':rows,'source_unchanged':all(x['match'] for x in unchanged),'source_bytes':unchanged,'git_status_porcelain':git('status','--porcelain','--untracked-files=no').decode(),'global_network_used_by_git':False}
(O/'source-readonly-and-commit-proof.json').write_text(json.dumps(report,indent=2)+'\n');print('commit files',len(rows),'match',report['all_commit_bytes_match'],'source unchanged',report['source_unchanged'])
