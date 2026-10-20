import subprocess,pathlib,hashlib,json,time,datetime,os
R=pathlib.Path('/workspace/shared/lowpoly-batch78-20261020'); Q=pathlib.Path('/workspace/shared/lowpoly-round32-qa78/semantic-jobs')
assets=[('pteridinium','r003'),('pingo','r002'),('sill-ledge','r001'),('exfoliation-dome','r002')]
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for asset,rev in assets:
 d=R/f'production/continuous-small-life-round32-20261020/assets/{asset}/{rev}'
 input_hashes={name:h(d/name) for name in ['generator.py','build-config.json']}
 for n in (1,2):
  job=f'{asset}-semantic-{n}'; out=Q/asset/f'run-{n}/outputs'; out.mkdir(parents=True,exist_ok=False)
  req={'schema_version':1,'job_id':job,'asset_id':asset,'revision':rev,'created_at':now(),'input_hashes':input_hashes,'output_dir':str(out),'argv':['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(d/'generator.py'),'--','--config',str(d/'build-config.json'),'--output',str(out)]}
  rp=Q/asset/f'run-{n}/request.json';rp.write_text(json.dumps(req,indent=2)+'\n')
  log=(Q/asset/f'run-{n}/blender.log').open('wb'); started=now(); mono=time.monotonic()
  p=subprocess.Popen(req['argv'],cwd=R,stdout=log,stderr=subprocess.STDOUT); pid=p.pid; code=p.wait(); log.close()
  finish=now(); outputs={}
  for name in ['model.glb','source.blend','metrics.json','source-metrics.json']:
   f=out/name
   if f.exists(): outputs[name]={'bytes':f.stat().st_size,'sha256':h(f),'inode':f.stat().st_ino}
  post_inputs={name:h(d/name) for name in ['generator.py','build-config.json']}
  result={'schema_version':1,'job_id':job,'asset_id':asset,'revision':rev,'pid':pid,'started_at':started,'finished_at':finish,'wall_seconds':round(time.monotonic()-mono,3),'returncode':code,'status':'succeeded' if code==0 else 'failed','input_hashes_before':input_hashes,'input_hashes_after':post_inputs,'outputs':outputs,'distinct_request':True}
  (Q/asset/f'run-{n}/result.json').write_text(json.dumps(result,indent=2)+'\n'); records.append(result)
  print(job,result['status'],'pid',pid,'wall',result['wall_seconds'],'glb',outputs.get('model.glb',{}).get('sha256'),flush=True)
manifest={'schema_version':1,'kind':'independent_semantic_rebuilds','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'started_at':records[0]['started_at'] if records else None,'finished_at':now(),'jobs':records}
# Verify each pair has distinct PID, paths, timestamps; identical final artifact digest; source inputs unchanged.
checks=[]
for asset,rev in assets:
 pair=[x for x in records if x['asset_id']==asset]
 candidate=R/f'production/continuous-small-life-round32-20261020/assets/{asset}/{rev}/model.glb'; expected=h(candidate)
 checks.append({'asset_id':asset,'revision':rev,'distinct_pids':len({x['pid'] for x in pair})==2,'distinct_output_paths':len({str(Q/asset/f'run-{n}/outputs/model.glb') for n in (1,2)})==2,'distinct_times':len({x['started_at'] for x in pair})==2,'distinct_requests':len({str(Q/asset/f'run-{n}/request.json') for n in (1,2)})==2,'both_succeeded':len(pair)==2 and all(x['returncode']==0 and x['status']=='succeeded' for x in pair),'inputs_unchanged':all(x['input_hashes_before']==x['input_hashes_after'] for x in pair),'candidate_glb_sha256':expected,'rebuild_glb_sha256':[x['outputs'].get('model.glb',{}).get('sha256') for x in pair],'exact_glb_matches':[x['outputs'].get('model.glb',{}).get('sha256')==expected for x in pair]})
manifest['checks']=checks;manifest['status']='pass' if all(c['distinct_pids'] and c['distinct_output_paths'] and c['distinct_times'] and c['distinct_requests'] and c['both_succeeded'] and c['inputs_unchanged'] and all(c['exact_glb_matches']) for c in checks) else 'fail'
p=Q/'independent-semantic-rebuilds.json';p.write_text(json.dumps(manifest,indent=2)+'\n');print('OVERALL',manifest['status'])
if manifest['status']!='pass':raise SystemExit(1)
