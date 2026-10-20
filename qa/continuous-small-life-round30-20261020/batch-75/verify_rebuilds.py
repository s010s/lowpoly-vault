import json, hashlib, pathlib, os, time
W=pathlib.Path('/workspace/shared/lowpoly-batch75-20261020')
P=W/'production/continuous-small-life-round30-20261020/work/batch-75'; O=pathlib.Path('/workspace/shared/lowpoly-round30-qa75')
cases=[('parvancorina','r001'),('glacial-horn','r002'),('eruptive-fissure','r003'),('banded-gneiss-outcrop','r003')]
def sh(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
summaries=[]
for sf in sorted((P/'rebuild-runs/runs').glob('*/summary.json')):
 s=json.load(open(sf))
 for row in s.get('results',[]): summaries.append((sf,s,row))
out=[]
for aid,rev in cases:
 d=P/'assets'/aid/rev; final=sh(d/'model.glb'); g=sh(d/'generator.py'); c=sh(d/'build-config.json'); actual=[]
 for sf,summary,r in summaries:
  if r.get('asset_id')==aid and r.get('revision')==rev and r.get('job_id') in ('semantic-rebuild-1','semantic-rebuild-2') and r.get('status')=='succeeded': actual.append((sf,summary,r))
 actual.sort(key=lambda x:x[2]['started_at']); assert len(actual)>=2,(aid,[(x[1]['run_id'],x[2]['status']) for x in actual])
 jobs=[]
 for i,(sf,summary,r) in enumerate(actual[:2],1):
  jid=f'semantic-rebuild-{i}'; assert r['job_id']==jid,(aid,r['job_id'])
  at=pathlib.Path(r['attempt_dir']); req=json.load(open(at/'request.json')); result=json.load(open(at/'result.json'))
  assert summary['status']=='succeeded' and r['returncode']==0 and result['returncode']==0 and result['status']=='succeeded'
  assert req['run_id']==summary['run_id'] and req['identity']['threads']==2 and result['pid']==r['pid'] and result['fingerprint']==r['fingerprint']
  for role,expect in [('generator',g),('config',c)]: assert req['identity']['inputs'][role]['sha256']==expect,(aid,jid,role)
  for fn,rec in r['outputs'].items():
   p=at/'outputs'/fn; assert p.is_file() and p.stat().st_size==rec['bytes'] and sh(p)==rec['sha256'],(aid,jid,fn)
  assert r['outputs']['model.glb']['sha256']==final and r['outputs']['model.glb']['bytes']==os.path.getsize(d/'model.glb')
  assert (at/'stdout.log').is_file() and (at/'stderr.log').is_file()
  jobs.append({'job_id':jid,'summary_path':str(sf),'run_id':summary['run_id'],'attempt_dir':str(at),'fingerprint':r['fingerprint'],'pid':r['pid'],'started_at':r['started_at'],'finished_at':r['finished_at'],'returncode':r['returncode'],'status':r['status'],'output_hashes':{fn:rec['sha256'] for fn,rec in r['outputs'].items()},'output_files_verified':True,'stdout_log':str(at/'stdout.log'),'stderr_log':str(at/'stderr.log')})
 assert jobs[0]['run_id']!=jobs[1]['run_id'] and jobs[0]['pid']!=jobs[1]['pid'] and jobs[0]['fingerprint']!=jobs[1]['fingerprint'] and jobs[0]['started_at']!=jobs[1]['started_at']
 out.append({'asset_id':aid,'revision':rev,'final_glb_sha256':final,'generator_sha256':g,'config_sha256':c,'two_distinct_executed_rebuilds_verified':True,'rebuilds':jobs})
result={'checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'method':'Matched exact asset/revision/job records to separate rebuild-run summaries with status=succeeded (not cache reused), request/result records, unique run IDs/PIDs, return codes, generator/config hashes and actual output files. Two runs per final revision. Maker repro-final reports that explicitly say generator_executed=false are not used as execution evidence.','assets':out,'all_eight_rebuilds_verified':True}
json.dump(result,open(O/'rebuild-evidence.json','w'),indent=2,sort_keys=True)
for a in out: print(a['asset_id'],[(r['run_id'],r['pid'],r['started_at'],r['output_hashes']['model.glb']) for r in a['rebuilds']])
