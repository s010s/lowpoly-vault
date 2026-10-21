"""Run actual independent queued builds, preserving every attempt, no network."""
from pathlib import Path
import sys,os,json,subprocess,hashlib,shutil
Q=Path(__file__).resolve().parent
I=json.loads((Q/'final-intake.json').read_text());W=Path(I['worktree']);H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2',MKL_NUM_THREADS='2',NUMEXPR_NUM_THREADS='2')
sys.path.insert(0,str(W/'scripts'));sys.dont_write_bytecode=True
from qa_glb import audit_glb
records=[]
for item in I['assets']:
 a=item['asset_id'];jobs=[]
 for suffix in ['a','b']:
  jobs.append({'asset_id':a,'revision':item['revision'],'job_id':'independent-rebuild-'+suffix,'argv':['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','--background','--threads','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'inputs':{'generator':str(W/item['generator']),'config':str(W/item['config']),'asset_common':str(W/'scripts/asset_common.py'),'qa_glb':str(W/'scripts/qa_glb.py')},'outputs':[f'{a}/{a}.glb',f'{a}/{a}.blend',f'{a}/qa.json',f'{a}/metadata.json','execution.json'],'timeout_seconds':1800})
 used=sum(p.stat().st_size for p in Q.rglob('*')if p.is_file());free=shutil.disk_usage(Q).free
 if used>27_000_000 or free<120_000_000:raise RuntimeError(f'Capacity checkpoint used={used}, free={free}; pending asset={a}')
 m=Q/(a+'-independent-rebuild-jobs.json');m.open('x').write(json.dumps({'schema_version':1,'lane':'build','jobs':jobs},indent=2)+'\n');log=Q/(a+'-independent-rebuild.log')
 cmd=[sys.executable,str(W/'scripts/run_asset_queue.py'),str(m),'--runs-root',str(Q/'independent-rebuild-queue'),'--workers','1','--threads','2','--cpu-budget','2','--retries','0','--allow-executable','/usr/bin/flock']
 with log.open('x')as out:ret=subprocess.run(cmd,cwd=W,env=env,stdout=out,stderr=subprocess.STDOUT)
 records.append({'asset_id':a,'returncode':ret.returncode,'jobs_sha256':H(m),'log_sha256':H(log),'qa_bytes_before':used,'available_bytes_before':free})
 (Q/('rebuild-checkpoint-'+a+'.json')).open('x').write(json.dumps(records,indent=2)+'\n')
 print(a,ret.returncode,flush=True)
 if ret.returncode:raise RuntimeError('Independent queued build failed; failure evidence retained')
