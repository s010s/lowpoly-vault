from pathlib import Path
import json,subprocess,shutil,datetime
R=Path.cwd();W=R/'production/continuous-small-life-round21-20261020/work/batch-56';base=R/'assets/candidates/continuous-small-life-round21-20261020/batch-56'
# Pull exact successful new source builds from queue output; no regeneration or rename of revisions.
for f in (W/'repair-runs/build').rglob('result.json'):
 d=json.loads(f.read_text())
 if d['status']=='succeeded':
  b=base/d['asset_id']/d['revision']
  for name in ['source.blend','model.glb','metrics.json','source-metrics.json']:shutil.copy(f.parent/'outputs'/name,b/name)
slug='arthrophycus-annulated-burrow';old=base/slug/'r001';b=base/slug/'r002';b.mkdir(exist_ok=True)
for n in ['brief.json','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','dependency-hashes.json']:shutil.copy(old/n,b/n)
d=json.loads((b/'brief.json').read_text());d['brief_version']='r002';d['revision_reason']='Separate adjacent curved casts so annulation rhythm remains legible rather than intersecting.';(b/'brief.json').write_text(json.dumps(d,indent=2)+'\n')
d=json.loads((b/'build-config.json').read_text());d['revision']='r002';(b/'build-config.json').write_text(json.dumps(d,indent=2)+'\n')
import hashlib
(b/'modeling-freeze.json').write_text(json.dumps({'asset_id':slug,'revision':'r002','frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in b.iterdir()}},indent=2)+'\n')
(b/'generator.py').write_text((old/'generator.py').read_text().replace("(-.079,.011,.150,-.026,18)","(-.079,.020,.150,-.010,18)").replace("(-.043,.059,.104,.015,12)","(-.043,.065,.104,.010,12)"))
bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
with (b/'build.log').open('w') as log:subprocess.run(bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(b)],stdout=log,stderr=subprocess.STDOUT,check=True)
# Queue two independently executed reproducibility builds per final artifact.
jobs=[];final=[]
for slug in ['cycadeoidea','gondwanagaricites','deflation-hollow','arthrophycus-annulated-burrow']:
 rev='r001' if slug=='deflation-hollow' else 'r002';b=base/slug/rev;final.append({'asset_id':slug,'revision':rev,'path':str(b.relative_to(R))})
 for i in [1,2]:
  jobs.append({'asset_id':slug,'revision':rev,'job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(b/'generator.py'),'config':str(b/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py')},'argv':['{blender}','--factory-startup','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json']})
(W/'final-selection.json').write_text(json.dumps(final,indent=2)+'\n');(W/'rebuild-jobs.json').write_text(json.dumps({'schema_version':1,'lane':'build','jobs':jobs},indent=2)+'\n')
subprocess.run(['python3','scripts/run_asset_queue.py',str(W/'rebuild-jobs.json'),'--runs-root',str(W/'final-rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','120'],check=True)
for a in final:
 b=R/a['path'];slug=a['asset_id'];rev=a['revision']
 for result in (W/'final-rebuild-runs/build'/slug/rev).rglob('result.json'):
  d=json.loads(result.read_text());i=d['job_id'][-1]
  args=['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(R),'--output',str(b/('repro-bound-'+i+'.report.json'))]
  with (b/('repro-bound-'+i+'.log')).open('w') as log:subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,check=True)
 for stage,args in [('format',['node','scripts/validate_gltf.cjs',str(b/'model.glb')]),('source-reopen',bl+['scripts/check_source_export.py','--','--source',str(b/'source.blend'),'--glb',str(b/'model.glb'),'--collection','EXPORT','--output',str(b/('source-final.report.json'))]),('proof8',bl+[str(W/'render-batch56.py'),'--',str(b/'model.glb'),'--revision',rev,'--brief',str(b/'brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof8'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','24'])]:
  t=datetime.datetime.now(datetime.timezone.utc)
  with (b/(stage+'.log')).open('w') as log:p=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,timeout=180)
  with (b/'final-stage-times.jsonl').open('a') as log:log.write(json.dumps({'stage':stage,'started_at':t.isoformat(),'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode})+'\n')
  print(slug,stage,p.returncode,flush=True)
  if p.returncode:raise RuntimeError(stage)
 shutil.copy(b/'proof8/hero.png',b/'preview.png')
