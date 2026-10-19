from pathlib import Path
import os,sys,json,subprocess,fcntl,time,signal,datetime,runpy
asset,phase=sys.argv[1:];ids=['selkirkia', 'dicroidium', 'waterfall-plunge-pool', 'cave-boxwork'];assert asset in ids and phase in ['build','evidence','render-runtime','detail','gray-top','complete']
root=Path('/workspace/batch41-'+asset);w=root/'production/continuous-small-life-round14-20261018/work/batch-41'/asset/'r001';out=root/'assets/candidates/continuous-small-life-round14-20261018/batch-41'/asset/'r001';logs=w/'logs';logs.mkdir(exist_ok=True)
lock=Path('/workspace/batch41-control/owned-process.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);lock.seek(0);lock.truncate();lock.write(json.dumps(dict(orchestrator_pid=os.getpid(),asset=asset,phase=phase)));lock.flush()
state=Path('/workspace/batch41-control/active-asset.json');previous=json.loads(state.read_text()) if state.exists() else {}
if previous and previous.get('asset')!=asset and previous.get('status')!='complete':raise RuntimeError('Previous asset lifecycle not complete: '+str(previous))
state.write_text(json.dumps(dict(asset=asset,status=phase,orchestrator_pid=os.getpid()))+'\n')
ledger=logs/'owned-processes.jsonl'
def record(**o):
 with ledger.open('a') as f:f.write(json.dumps(dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),asset=asset,phase=phase,orchestrator_pid=os.getpid(),**o))+'\n')
def run(root,args,log):
 log=log.parent/(os.environ.get('BATCH41_LOG_PREFIX','')+log.name)
 args=list(map(str,args));record(event='before_launch',argv=args,log=str(log),locked=True)
 with log.open('w') as f:
  p=subprocess.Popen(args,cwd=root,stdout=f,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2'})
  record(event='launch',owned_pid=p.pid,owned_process_group=p.pid,argv=args)
  try:code=p.wait(timeout=900)
  except subprocess.TimeoutExpired:
   os.killpg(p.pid,signal.SIGTERM);p.wait(timeout=15);record(event='timeout',owned_pid=p.pid);raise
  try:os.killpg(p.pid,0);remaining=True
  except ProcessLookupError:remaining=False
  record(event='exit',owned_pid=p.pid,returncode=code,owned_process_group_remaining=remaining)
  if remaining:raise RuntimeError('Owned process group remains; refuse next launch')
  if code:raise RuntimeError(str(log)+'\n'+log.read_text()[-5000:])
if phase=='build':run(root,['blender','-b','-t','2','--python-exit-code','1','--python',w/'build.py','--','--config',w/'config.json','--output',out,'--preview'],logs/os.environ.get('BATCH41_BUILD_LOG','build.log'))
elif phase=='render-runtime':
 run(root,['blender','-b','-t','2','--python-exit-code','1','--python',w/'render.py','--',out/(asset+'.glb'),out/'views'],logs/'render.log')
 run(root,['node',w/'runtime.mjs',out/(asset+'.glb'),out/'runtime'],logs/'runtime.log')
elif phase=='gray-top':run(root,['blender','-b','-t','2','--python-exit-code','1','--python',w/'gray-top.py','--',out/(asset+'.glb'),out/'diagnostics/gray-top'],logs/'gray-top.log')
elif phase=='detail':run(root,['node',w/'runtime-detail.mjs',out/(asset+'.glb'),out/'detail'],logs/'detail.log')
elif phase=='evidence':
 code=Path('/workspace/batch41-control/evidence.py').read_text();exec(compile(code,'evidence.py','exec'))
else:
 assert (out/'profile-checker.report.json').exists();record(event='asset_lifecycle_complete');state.write_text(json.dumps(dict(asset=asset,status='complete',orchestrator_pid=os.getpid()))+'\n')
record(event='phase_complete')
