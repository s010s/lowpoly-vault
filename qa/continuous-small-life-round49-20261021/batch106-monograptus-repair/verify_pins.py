import os,subprocess,json,hashlib,datetime
from pathlib import Path
W=Path('/workspace/shared/lowpoly-batch106-monograptus-repair-20261021'); O=Path(__file__).parent; R=W/'production/small-life-batch106/monograptus/r005'; M=Path('/workspace/shared/lowpoly-batch106-monograptus-repair-evidence'); Q=Path('/workspace/shared/lowpoly-batch106-independent-qa-20261021')
C='a2e75f5642df323a05a9752426b90e1422012acb'; P='56591b51d9f1f2fffb409f05cbee108bff5c2bfc'; env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*a):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(W),*a],env=env)
h=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):return {'path':str(p),'sha256':h(p.read_bytes()),'bytes':p.stat().st_size}
def tree(c):return {x.split(b'\t')[1].decode():x.split(b'\t')[0].decode() for x in git('ls-tree','-r','-z',c).split(b'\0') if x}
a,b=tree(P),tree(C); inherited=[k for k in a if b.get(k)==a[k]]; added=sorted(set(b)-set(a)); changed=[k for k in a if b.get(k)!=a[k]]
assert git('rev-parse','HEAD').decode().strip()==C; assert git('rev-parse','HEAD^').decode().strip()==P; assert git('status','--porcelain').strip()==b''; assert not changed and len(a)==29133
expected={R/'handoff.json':'00041aeeb4402f52f07767037cff6b1867ac2a7df6d32e5cdc2eafdb1274f5c2',R/'necessary-payload-manifest.json':'7bbfe5756ec1eba4696cc72aa3cc58998ed48518634b1e0534be14385b94bd6e',M/'fixed-commit-readback.json':'83425fc1e0cfabd48e0526b29dc4691bd5aa762f2f62ff5a853d36158596be7e',Q/'independent-report.json':'d816b79a3f12642de849bbb6f5f394d8e825ba9998aa4be00d7c954ca5683156',Q/'monograptus/geometry-details.json':'40a982898a05aec37442f844e634033bb32f2c9b8be9900e0df10819ece2da3e'}
for p,v in expected.items():assert h(p.read_bytes())==v,str(p)
payload=json.loads((R/'necessary-payload-manifest.json').read_text()); deps=json.loads((R/'build-dependencies.json').read_text()); assert len(deps['files'])==29
records=[]
for d in payload['files']+deps['files']:
 p=W/d['path']; data=p.read_bytes(); assert h(data)==d['sha256'] and len(data)==d['bytes']; assert data==git('show',f'{C}:{d["path"]}'); records.append(ref(p))
assert sorted([d['path'] for d in payload['files']]+[str((R/'necessary-payload-manifest.json').relative_to(W))])==added
other=[k for k in a if any(k.startswith('production/small-life-batch106/'+x+'/') for x in ['didymograptus','diplograptus','dictyonema'])];assert len(other)==171
other_records=[]
for k in other:
 data=(W/k).read_bytes(); assert data==git('show',f'{P}:{k}');other_records.append(ref(W/k))
assert len(added)==67 and sum((W/k).stat().st_size for k in added)==3415832
history=[]
for base in [Q,M]:
 for p in sorted(base.rglob('*')):
  if p.is_file():history.append(ref(p))
r={'status':'PASS','commit':C,'parent':P,'branch':git('branch','--show-current').decode().strip(),'clean':True,'parent_tree_entries':len(a),'inherited_identical_entries':len(inherited),'changed_inherited_paths':changed,'added_files':67,'added_bytes':3415832,'declared_dependency_files':29,'fixed_pins':[ref(p) for p in expected],'payload_and_dependency_verification':records,'other_three_unchanged_files':other_records,'prior_history_preservation_baseline':history,'scope':'Independent local object and byte verification, no network or source edits.'}
(O/'bindings.json').write_text(json.dumps(r,indent=2)+'\n');(O/'recovery-01-bindings.json').write_text(json.dumps({'stage':'bindings','status':'PASS','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':C,'uncertain_jobs':[]},indent=2)+'\n');print({k:r[k] for k in ['status','commit','inherited_identical_entries','added_files','added_bytes','declared_dependency_files']})
