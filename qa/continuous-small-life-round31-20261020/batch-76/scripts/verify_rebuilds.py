import hashlib,json,sys
from pathlib import Path
repo=Path('/workspace/shared/lowpoly-batch76-20261020').resolve(); qa=Path('/workspace/shared/lowpoly-round31-qa76').resolve()
sys.path.insert(0,str(repo/'scripts'))
from check_reproducibility import compare_rebuild,write_new_report
items=[('rangea','r002'),('serac','r001'),('moulin-shaft','r002'),('solifluction-lobe','r002')]
rows=[]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for aid,rev in items:
 d=repo/'production/continuous-small-life-round31-20261020/assets'/aid/rev
 runs=[]
 for i in (1,2):
  producer=json.loads((d/f'repro-final-{i}.report.json').read_text())
  request=repo/producer['build_run']['request']['path']; result=repo/producer['build_run']['result']['path']
  rebuilt=Path(producer['rebuilt_glb_path'])
  r=compare_rebuild(d/'model.glb',rebuilt,d/'generator.py',d/'build-config.json',request,result,'model.glb',repo)
  p=qa/'rebuild-evidence'/f'{aid}-{rev}-{i}.json'; write_new_report(p,r)
  q=json.loads(request.read_text()); z=json.loads(result.read_text()); output=Path(result).parent/'outputs/model.glb'
  runs.append({'index':i,'checker_status':r['status'],'checker_errors':r['errors'],'request_path':str(request.relative_to(repo)),'request_sha256':sha(request),'request_created_at':q.get('created_at'),'request_fingerprint':q.get('fingerprint'),'request_run_id':q.get('run_id'),'result_path':str(result.relative_to(repo)),'result_sha256':sha(result),'pid':z.get('pid'),'started_at':z.get('started_at'),'finished_at':z.get('finished_at'),'status':z.get('status'),'returncode':z.get('returncode'),'wall_seconds':z.get('wall_seconds'),'output_path':str(output.relative_to(repo)),'output_exists':output.is_file(),'output_is_distinct_from_final':output.resolve()!= (d/'model.glb').resolve(),'output_samefile_with_peer':None,'output_sha256':z.get('outputs',{}).get('model.glb',{}).get('sha256'),'output_actual_sha256':sha(output) if output.is_file() else None})
 a,b=runs
 p1=repo/a['output_path']; p2=repo/b['output_path']
 distinct={'pid':a['pid']!=b['pid'],'request_created_at':a['request_created_at']!=b['request_created_at'],'started_at':a['started_at']!=b['started_at'],'finished_at':a['finished_at']!=b['finished_at'],'request_path':a['request_path']!=b['request_path'],'request_sha256':a['request_sha256']!=b['request_sha256'],'request_fingerprint':a['request_fingerprint']!=b['request_fingerprint'],'result_path':a['result_path']!=b['result_path'],'result_sha256':a['result_sha256']!=b['result_sha256'],'output_path':a['output_path']!=b['output_path'],'output_files_not_samefile':not p1.samefile(p2),'each_output_matches_final_glb':a['output_actual_sha256']==b['output_actual_sha256']==sha(d/'model.glb')}
 a['output_samefile_with_peer']=p1.samefile(p2); b['output_samefile_with_peer']=p1.samefile(p2)
 success=all(distinct.values()) and all(r['checker_status']=='pass' and r['status']=='succeeded' and r['returncode']==0 and r['pid'] and r['output_exists'] and r['output_is_distinct_from_final'] for r in runs)
 rows.append({'asset_id':aid,'revision':rev,'status':'pass' if success else 'fail','distinct_checks':distinct,'queue_batch_run_id_shared_between_pair':a['request_run_id']==b['request_run_id'],'runs':runs,'note':'Queue run_id is a batch/session label shared across all eight runs; distinctness is established by separate PID, timestamps, unique request/result/fingerprint paths and output files.'})
report={'kind':'independent-validation-of-producer-queue-rebuild-evidence','producer_generator_not_reexecuted_by_this_comparison':True,'candidate_count':len(items),'rebuild_count':sum(len(x['runs']) for x in rows),'status':'pass' if all(x['status']=='pass' for x in rows) else 'fail','assets':rows,'limits':'Validates preserved successful queue requests/results and output hashes plus separate process/timestamp/path evidence; queue records are attestations, not cryptographic proof of execution.'}
out=qa/'rebuild-evidence'/'summary.json';write_new_report(out,report)
print(json.dumps(report,indent=2))
if report['status']!='pass': raise SystemExit(1)
