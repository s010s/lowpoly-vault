from pathlib import Path
import sys,os,hashlib,json,subprocess
sys.dont_write_bytecode=True
Q=Path(__file__).resolve().parent;I=json.loads((Q/'final-intake.json').read_text());W=Path(I['worktree']);sys.path.insert(0,str(W/'scripts'))
from qa_glb import audit_glb
from check_reproducibility import validate_build_run
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();reports=[]
for item in I['assets']:
 a=item['asset_id'];d=Q/a
 r=audit_glb(W/item['glb'],max_triangles=14000,max_materials=6,max_primitives=30);(d/'project-independent.json').open('x').write(json.dumps(r,indent=2)+'\n');assert not r['errors'],r['errors']
 original=json.loads((W/item['original_brief']).read_text());delivery=json.loads((W/item['delivery_brief']).read_text());diff={k:{'original':v,'delivery':delivery.get(k)}for k,v in original.items()if v!=delivery.get(k)}
 cpath=W/item['candidate'];contract=cpath.parent/'profile-contract.json';p=subprocess.run([sys.executable,str(W/'scripts/validate_candidate.py'),str(cpath),'--root',str(W),'--profile','static-stylized-v1','--profile-contract',str(contract),'--json'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),text=True);(d/'candidate-validation.json').open('x').write(p.stdout);(d/'candidate-validation.stderr').open('x').write(p.stderr);assert p.returncode==0,(a,p.returncode,p.stdout,p.stderr)
 runs=[]
 for result in (Q/'independent-rebuild-queue/build'/a/item['revision']).rglob('result.json'):
  request=result.parent/'request.json';execution=result.parent/'outputs/execution.json';rebuilt=result.parent/f'outputs/{a}/{a}.glb';req=json.loads(request.read_text());res=json.loads(result.read_text());ex=json.loads(execution.read_text());rr=audit_glb(rebuilt,max_triangles=14000,max_materials=6,max_primitives=30);fp=validate_build_run(req,res,H(W/item['generator']),H(W/item['config']),H(rebuilt),f'{a}/{a}.glb')
  assert rr['semantic_sha256']==r['semantic_sha256'];assert ex['generator_sha256']==H(W/item['generator'])and ex['config_sha256']==H(W/item['config'])
  runs.append({'request':{'path':str(request),'sha256':H(request)},'result':{'path':str(result),'sha256':H(result)},'execution':{'path':str(execution),'sha256':H(execution)},'output':{'path':str(rebuilt),'sha256':H(rebuilt)},'fingerprint':fp,'pid':ex['pid'],'semantic_sha256':rr['semantic_sha256'],'byte_identical':H(rebuilt)==H(W/item['glb']),'status':res['status'],'host_started_at':ex['started_at'],'host_finished_at':ex['finished_at']})
 assert len(runs)==2 and len({z['pid']for z in runs})==2
 # Existing maker evidence is checked separately, not confused with these fresh runs.
 maker=[]
 for suf in ['a','b']:
  b=W/item['qa'];reqp=b/f'rebuild-{suf}-request.json';resp=b/f'rebuild-{suf}-result.json';exp=b/f'rebuild-{suf}-execution.json';req=json.loads(reqp.read_text());res=json.loads(resp.read_text());ex=json.loads(exp.read_text());out=res['outputs'][f'{a}/{a}.glb'];fp=validate_build_run(req,res,H(W/item['generator']),H(W/item['config']),out['sha256'],f'{a}/{a}.glb');maker.append({'pid':ex['pid'],'request_sha256':H(reqp),'result_sha256':H(resp),'execution_sha256':H(exp),'fingerprint':fp,'glb_sha256':out['sha256']})
 assert len({z['pid']for z in maker})==2
 result={'asset_id':a,'source_commit':I['source_commit'],'glb_sha256':H(W/item['glb']),'semantic_sha256':r['semantic_sha256'],'independent_rebuilds':runs,'maker_rebuild_provenance':maker,'original_brief_changes_in_delivery':diff,'original_brief_preserved_and_hashed':True,'candidate_integrity_returncode':p.returncode,'no_publication_or_approval':True}
 (d/'rebuild-and-contract-audit.json').open('x').write(json.dumps(result,indent=2)+'\n');reports.append({'asset_id':a,'distinct_independent_pids':[x['pid']for x in runs],'distinct_maker_pids':[x['pid']for x in maker],'semantic_match':True,'bytes_match':all(x['byte_identical']for x in runs),'project_errors':r['errors'],'brief_keys_changed':list(diff)})
print(json.dumps(reports,indent=2))
