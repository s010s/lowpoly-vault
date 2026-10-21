import pathlib,json,hashlib,subprocess,os,datetime
Q=pathlib.Path(__file__).parent; W=pathlib.Path('/workspace/shared/lowpoly-batch99-label-repair-20261021'); B=W/'production/small-life-batch99'; OLD=pathlib.Path('/workspace/shared/lowpoly-batch99-20261021'); F='b989eeb8cd562a65d811fde8934293700b64bab7'; P='c6675b9180cc8751c532deab796443be576be93c'
h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0')
def git(*args): return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(W),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==F
assert git('rev-parse',F+'^').decode().strip()==P
assert git('branch','--show-current').decode().strip()=='candidate/batch99-label-repair-20261021'
assert h(B/'label-repair/HANDOFF.json')=='dffdd747813568bba62e0fc7d9142bd5ebe5edf4f6d9d5779f2dcc065a83f098'
assert h(B/'label-repair/manifest.json')=='c304d370593ec2bb1cf6b6f935a70589d39f89bd5c14de9b1ff2f60b1089c915'
manifest=json.loads((B/'label-repair/manifest.json').read_text())
for x in manifest['files']:assert h(W/x['path'])==x['sha256'] and (W/x['path']).stat().st_size==x['bytes'],x
orig=json.loads((B/'label-repair/original-immutable-sha256.json').read_text())
for path,sha in orig.items():assert h(path)==sha,path
def tree(ref):return {x.split(b'\t')[1].decode():x.split(b'\t')[0].decode() for x in git('ls-tree','-r','-z',ref).split(b'\0') if x}
a=tree(P);b=tree(F); assert all(b.get(k)==v for k,v in a.items())
freeze_path='production/small-life-batch99/original-freeze-manifest.json';blob=git('show',F+':'+freeze_path);assert hashlib.sha256(blob).hexdigest()=='120f41ebbfef8a292b8cbaad96295780b384aa1ef273ac4e37031861d86a19d6'
assert blob==git('show',P+':'+freeze_path)==(OLD/freeze_path).read_bytes()
closure=[]
for asset,old,new in [('monetianthus','r001','r002'),('proterocladus','r002','r003')]:
 p=B/asset/new;op=OLD/'production/small-life-batch99'/asset/old
 for name in ['config.json','original-brief.json','references.json']:assert (p/name).read_bytes()==(op/name).read_bytes(),(asset,name)
 for x in json.loads((p/'dependencies.json').read_text())['files']:assert h(W/x['path'])==x['sha256'];closure.append(x)
report={'source_commit':F,'parent_commit':P,'branch':git('branch','--show-current').decode().strip(),'manifest_files_verified':len(manifest['files']),'manifest_bytes':sum(x['bytes'] for x in manifest['files']),'original_files_rehashed_unchanged':len(orig),'old_git_entries_unchanged':len(a),'new_git_entries':len(b)-len(a),'freeze':{'path':freeze_path,'sha256':hashlib.sha256(blob).hexdigest(),'inherited_blob':True,'sparse_absence_is_not_defect':True,'matches_parent_and_original_worktree':True},'closure_entries_rehashed':len(closure),'frozen_config_brief_references_byte_identical':True,'old_failure_report_sha256':h('/workspace/shared/lowpoly-batch99-independent-qa-20261021/BATCH99-INDEPENDENT-QA-REPORT.json'),'status':'pass'}
(Q/'pin-verification.json').write_text(json.dumps(report,indent=2)+'\n')
with (Q/'recovery-progress.jsonl').open('a') as f:f.write(json.dumps({'stage':'immutable_pins_and_scope','status':'pass','at':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
print(json.dumps(report,indent=2))
