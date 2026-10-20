import json,hashlib,os,sys
from pathlib import Path
ROOT=Path('/tmp/lowpoly-batch62-20261020'); OUT=Path('/workspace/shared/lowpoly-round24-qa62')
B='assets/candidates/continuous-small-life-round24-20261020/batch-62'
work=ROOT/'production/continuous-small-life-round24-20261020/work/batch-62'
finals=[('dinomischus','r002','repair-rebuild-runs'),('star-dune','r002','repair-rebuild-runs'),('slot-canyon','r001','rebuild-runs'),('flowstone-cascade','r002','repair-rebuild-runs')]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p):return json.loads(Path(p).read_text())
out=[]
for a,rev,runsfolder in finals:
 d=ROOT/B/a/rev; jobs=[]
 for n in (1,2):
  report=j(d/f'repro-final-{n}.report.json')
  req_rel=report['build_run']['request']['path']; res_rel=report['build_run']['result']['path']
  req=ROOT/req_rel; res=ROOT/res_rel; q=j(req); r=j(res)
  attempt=res.parent; summary_path=work/runsfolder/'runs'/q['run_id']/'summary.json'; summary=j(summary_path)
  sumentry=next((x for x in summary['results'] if x['attempt_dir']==str(attempt)),None)
  outs=r.get('outputs',{}); glb=attempt/'outputs/model.glb'; stdout=attempt/'stdout.log'; stderr=attempt/'stderr.log'
  sourcefile=d/'model.glb'
  fields={
   'job_id':r.get('job_id'),'asset_id':r.get('asset_id'),'revision':r.get('revision'),'fingerprint':r.get('fingerprint'),
   'attempt_dir':str(attempt),'run_id':q.get('run_id'),'request_sha256':sha(req),'request_pin_matches':sha(req)==report['build_run']['request']['sha256'],
   'result_sha256':sha(res),'result_pin_matches':sha(res)==report['build_run']['result']['sha256'],
   'queue_summary_path':str(summary_path.relative_to(ROOT)),'queue_summary_status':summary.get('status'),'queue_record':sumentry,
   'process_pid':r.get('pid'),'returncode':r.get('returncode'),'status':r.get('status'),'started_at':r.get('started_at'),'finished_at':r.get('finished_at'),'wall_seconds':r.get('wall_seconds'),
   'result_output_glb_sha256':outs.get('model.glb',{}).get('sha256'),'result_output_glb_bytes':outs.get('model.glb',{}).get('bytes'),'actual_output_glb_sha256':sha(glb),'actual_output_glb_bytes':glb.stat().st_size,'final_glb_sha256':sha(sourcefile),'output_equals_final':sha(glb)==sha(sourcefile),
   'semantic_target':report.get('semantic_sha256'),'semantic_rebuilt':report.get('rebuilt_semantic_sha256'),'semantic_match':report.get('semantic_match'),'byte_identical':report.get('byte_identical'),
   'generator_sha256':q.get('identity',{}).get('inputs',{}).get('generator',{}).get('sha256'),'config_sha256':q.get('identity',{}).get('inputs',{}).get('config',{}).get('sha256'),'helper_sha256':q.get('identity',{}).get('inputs',{}).get('helper',{}).get('sha256'),'audit_sha256':q.get('identity',{}).get('inputs',{}).get('audit',{}).get('sha256'),'runner_sha256':q.get('identity',{}).get('runner_sha256'),'blender_sha256':q.get('identity',{}).get('executable',{}).get('sha256'),'blender_argv':q.get('argv'),
   'stdout_sha256':sha(stdout),'stdout_bytes':stdout.stat().st_size,'stderr_sha256':sha(stderr),'stderr_bytes':stderr.stat().st_size,
   'queue_entry_matches':bool(sumentry and sumentry.get('pid')==r.get('pid') and sumentry.get('started_at')==r.get('started_at') and sumentry.get('finished_at')==r.get('finished_at') and sumentry.get('status')=='succeeded' and sumentry.get('outputs',{}).get('model.glb',{}).get('sha256')==sha(glb)),
   'successful_distinct_process':bool(r.get('status')=='succeeded' and r.get('returncode')==0 and r.get('pid') and sha(glb)==sha(sourcefile) and report.get('semantic_match')),
   'output_materialized':glb.exists(), 'report_status':report.get('status'), 'report_generator_executed':report.get('generator_executed')}
  jobs.append(fields)
 out.append({'asset_id':a,'revision':rev,'runs':jobs,'distinct_run_ids':len({x['run_id'] for x in jobs})==2,'distinct_pids':len({x['process_pid'] for x in jobs})==2,'distinct_fingerprints':len({x['fingerprint'] for x in jobs})==2,'distinct_attempt_dirs':len({x['attempt_dir'] for x in jobs})==2,'both_successful_queue_rebuilds':all(x['successful_distinct_process'] and x['queue_entry_matches'] and x['output_materialized'] and x['result_pin_matches'] and x['request_pin_matches'] for x in jobs)})
result={'schema_version':1,'source_repo_head':os.popen(f'cd {ROOT} && git rev-parse HEAD').read().strip(),'assets':out}
(OUT/'rebuild-audit.json').write_text(json.dumps(result,indent=2)+'\n')
for x in out:print(x['asset_id'], '2 successful bound rebuilds',x['both_successful_queue_rebuilds'],'distinct PIDs',x['distinct_pids'],[r['process_pid'] for r in x['runs']],'times',[(r['started_at'],r['finished_at']) for r in x['runs']],'hashes',[r['actual_output_glb_sha256'] for r in x['runs']])
