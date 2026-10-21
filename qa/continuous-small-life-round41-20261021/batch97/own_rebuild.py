import json,pathlib,hashlib,datetime,subprocess,sys,os
W=pathlib.Path('/workspace/shared/lowpoly-batch97-20261020');B=W/'production/small-life-batch97';O=pathlib.Path(__file__).parent;sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
for aid,rev in [('ginkgo','r002'),('dicranophyllum','r003'),('noeggerathia','r002'),('bjuvia','r001')]:
 d=B/aid/rev;c=json.loads((d/'candidate.json').read_text());out=O/aid/'own-rebuild';out.mkdir(exist_ok=True)
 if (out/'result.json').exists():print('Existing own rebuild result, not rerunning',aid);continue
 assert not list(out.iterdir()),f'Uncertain unfinished own rebuild in {out}'
 pins={k:{'path':str(W/v['path']),'sha256':H(W/v['path'])} for k,v in c['artifacts'].items() if k in ['generator','config']};assert all(pins[k]['sha256']==c['artifacts'][k]['sha256'] for k in pins)
 for k in ['asset_common','qa_glb']:pins[k]={'path':str(W/'scripts'/(k+'.py')),'sha256':H(W/'scripts'/(k+'.py'))}
 cmd=['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','--background','--threads','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python',pins['generator']['path'],'--','--config',pins['config']['path'],'--output',str(out/'outputs')];req={'asset_id':aid,'revision':rev,'inputs':pins,'argv':cmd,'started_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Fresh independent third generator rebuild, exact maker source/config; no original file changes.'};(out/'request.json').write_text(json.dumps(req,indent=2)+'\n')
 with (out/'stdout.log').open('w') as log:p=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 z={'returncode':p.returncode,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request_sha256':H(out/'request.json'),'unchanged_inputs':all(H(v['path'])==v['sha256'] for v in pins.values())}
 if p.returncode==0:
  execution=json.loads((out/'outputs/execution.json').read_text());a=audit_glb(out/'outputs'/aid/(aid+'.glb'),14000,6,30);original=audit_glb(W/c['artifacts']['glb']['path'],14000,6,30);z.update(execution=execution,execution_sha256=H(out/'outputs/execution.json'),semantic_sha256=a['semantic_sha256'],candidate_semantic_sha256=original['semantic_sha256'],semantic_equal=a['semantic_sha256']==original['semantic_sha256'],byte_equal=H(out/'outputs'/aid/(aid+'.glb'))==c['artifacts']['glb']['sha256'],errors=a['errors'],files=[{'path':str(f),'sha256':H(f),'bytes':f.stat().st_size} for f in sorted((out/'outputs').rglob('*')) if f.is_file()])
 (out/'result.json').write_text(json.dumps(z,indent=2)+'\n');print(aid,'own generator rebuild',p.returncode,z.get('semantic_equal'),z.get('execution',{}).get('pid'),flush=True)
 if p.returncode:raise RuntimeError(aid+' failed')
