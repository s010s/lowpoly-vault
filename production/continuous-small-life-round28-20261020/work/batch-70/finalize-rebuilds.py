from pathlib import Path
import subprocess,json,hashlib,datetime,time
r=Path.cwd();w=r/'production/continuous-small-life-round28-20261020/work/batch-70';selection=json.loads((w/'final-selection.json').read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run(['node',str(w/'runtime-parse.mjs')]+[str(r/x['path']) for x in selection],check=True)
a=['python3','scripts/run_asset_queue.py',str(w/'rebuild-jobs.json'),'--runs-root',str(w/'rebuild-runs'),'--blender',str(w/'locked-blender.sh'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','120','--resume'];p=subprocess.run(a);assert p.returncode==0
for x in selection:
 b=r/x['path'];sem=json.loads((b/'metrics.json').read_text())['glb']['semantic_sha256']
 for i in [1,2]:
  choices=[]
  for result in (w/'rebuild-runs/build'/x['asset_id']/x['revision']/f'semantic-rebuild-{i}').rglob('result.json'):
   d=json.loads(result.read_text());g=result.parent/'outputs/model.glb'
   if d['status']!='succeeded' or not g.exists():continue
   import sys;sys.path.insert(0,str(r/'scripts'));from qa_glb import audit_glb
   if audit_glb(g)['semantic_sha256']==sem:choices.append(result)
  assert choices,(x,i)
  result=sorted(choices)[-1];out=b/f'repro-final-{i}.report.json'
  if out.exists():
   prior=b/'attempts/obsolete-repro';prior.mkdir(parents=True,exist_ok=True);shutil.move(out,prior/out.name)
  subprocess.run(['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(r),'--output',str(out)],check=True)
