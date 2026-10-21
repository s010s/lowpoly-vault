# SPDX-License-Identifier: MIT
"""Execute full exact-subject proof only after maker selects geometry diagnostics."""
from pathlib import Path
import sys,json,hashlib,subprocess,datetime,time,shutil
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent;rev=sys.argv[1];B=W/'assets/ernietta'/rev
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
def run(name,cmd,timeout=3600):
 start=now();clock=time.monotonic()
 with (B/(name+'.log')).open('x') as log:
  p=subprocess.Popen(cmd,cwd=R,stdout=log,stderr=subprocess.STDOUT)
  try:rc=p.wait(timeout=timeout)
  except subprocess.TimeoutExpired:p.terminate();p.wait();rc=124
 event={'stage':name,'started_at':start,'finished_at':now(),'runner_pid':p.pid,'command':cmd,'returncode':rc,'wall_seconds':time.monotonic()-clock}
 with (B/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
 print(name,rc,flush=True)
 if rc:raise RuntimeError(name+' failed')
bl=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
assert json.loads((B/'diagnostic-disposition.json').read_text())['disposition']=='SELECT_FOR_FULL_PROOF'
assert json.loads((B/'physical-surfaces.report.json').read_text())['status']=='pass'
for key,expected in json.loads((W/'original-freeze/modeling-freeze.json').read_text())['files'].items():assert H(W/'original-freeze'/key)==expected
shutil.copy2(W/'original-freeze/references.json',B/'references.json')
run('format',['node','scripts/validate_gltf.cjs',str(B/'model.glb')])
run('source-reopen',bl+['scripts/check_source_export.py','--','--source',str(B/'source.blend'),'--glb',str(B/'model.glb'),'--output',str(B/'source-final.report.json'),'--collection','EXPORT'])
run('source-counts',bl+[str(W/'count-source-vertices.py'),'--',str(B)])
run('runtime-parse',['node',str(W/'runtime-parse.mjs'),str(B)])
jobs=[]
for i in [1,2]:
 job={'asset_id':'ernietta','revision':rev,'job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(B/'generator.py'),'config':str(B/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py'),'brief':str(W/'original-freeze/brief.json'),'references':str(B/'references.json'),'repair_freeze':str(W/'repair-intent-freeze.json')},'argv':['{blender}','--factory-startup','--disable-autoexec','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json']}
 manifest=W/('queue-'+rev+'-'+str(i)+'.json');write(manifest,{'schema_version':1,'lane':'build','jobs':[job]})
 run('semantic-queue-'+str(i),['flock','/tmp/lowpoly-production-blender.lock','python3','scripts/run_asset_queue.py',str(manifest),'--runs-root',str(W/'rebuild-runs'),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','180','--resume'])
 results=list((W/'rebuild-runs/build/ernietta'/rev/job['job_id']).rglob('result.json'));assert len(results)==1,results
 result=results[0];run('repro-final-'+str(i),['python3','scripts/check_reproducibility.py','--glb',str(B/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(B/'generator.py'),'--config',str(B/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(R),'--output',str(B/('repro-final-'+str(i)+'.report.json'))])
 jobs.append({'job':job['job_id'],'request':str((result.parent/'request.json').relative_to(R)),'request_sha256':H(result.parent/'request.json'),'result':str(result.relative_to(R)),'result_sha256':H(result),'output_glb_sha256':H(result.parent/'outputs/model.glb'),'result_record':json.loads(result.read_text())})
assert jobs[0]['result_record']['pid']!=jobs[1]['result_record']['pid']
write(B/'final-rebuild-binding.json',{'created_at':now(),'glb_sha256':H(B/'model.glb'),'generator_sha256':H(B/'generator.py'),'config_sha256':H(B/'build-config.json'),'jobs':jobs})
d=json.loads((W/'original-freeze/brief.json').read_text());d['packaging_adapter']={'created_at':now(),'frozen_design_brief_sha256':H(W/'original-freeze/brief.json'),'repair_intent_sha256':H(W/'repair-intent-freeze.json'),'note':'Derived delivery closure only. Original scope, criteria, required views and budgets unchanged; repair provenance explicit.'};d['required_deliverables']=[{'role':k,'path':str((B/n).relative_to(R)),'sha256':H(B/n)} for k,n in [('source','source.blend'),('generator','generator.py'),('config','build-config.json')]];write(B/'candidate-brief.json',d)
files=['package.json','package-lock.json','production/batch77-ernietta-repair/complete-final.py','production/batch77-ernietta-repair/package-final.py','production/batch77-ernietta-repair/rebuild-final.sh','scripts/asset_common.py','scripts/qa_glb.py','scripts/check_source_export.py','scripts/check_reproducibility.py','scripts/run_asset_queue.py','scripts/validate_gltf.cjs','scripts/candidate_profile.py','scripts/validate_candidate.py','scripts/validate_concept_evidence.py','production/batch77-ernietta-repair/render-fixed8.py','production/batch77-ernietta-repair/runtime-parse.mjs','production/batch77-ernietta-repair/count-source-vertices.py','production/batch77-ernietta-repair/check-physical-surfaces.py']
write(B/'build-dependencies.json',{'created_at':now(),'files':{n:H(R/n) for n in files},'blender':'4.3.2 threads2 CPU','node_modules':'/workspace/shared/lowpoly-landair-web-integration/node_modules read-only','three':'0.180.0','khronos':'2.0.0-dev.3.10','seed':77})
write(B/'preproof-binding.json',{'created_at':now(),'revision':rev,'glb_sha256':H(B/'model.glb'),'brief_sha256':H(B/'candidate-brief.json'),'references_sha256':H(B/'references.json'),'source_sha256':H(B/'source.blend'),'generator_sha256':H(B/'generator.py'),'config_sha256':H(B/'build-config.json'),'original_freeze_verified':True,'two_distinct_queue_pids':True,'all_checks_before_final_render':True})
sys.path.insert(0,str(R/'scripts'))
from validate_candidate import check_brief
refs=json.loads((B/'references.json').read_text())
check_brief(d,{'asset_id':'ernietta'},{v['id'] for v in refs['sources']},'static-stylized-v1')
assert all(v.get('rights_note') for v in refs['sources'])
write(B/'fresh-schema-check.json',{'checked_at':now(),'brief_sha256':H(B/'candidate-brief.json'),'references_sha256':H(B/'references.json'),'check_brief':'pass-static-stylized-v1','source_rights':'pass','before_final_render':True})
run('proof-final',bl+[str(W/'render-fixed8.py'),'--',str(B/'model.glb'),'--revision',rev,'--brief',str(B/'candidate-brief.json'),'--references',str(B/'references.json'),'--output-dir',str(B/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'])
shutil.copy2(B/'proof-final/hero.png',B/'preview.png')
from PIL import Image,ImageDraw
views=d['required_views'];sheet=Image.new('RGB',(2048,1060),'#E8E4DC');draw=ImageDraw.Draw(sheet)
for i,v in enumerate(views):
 im=Image.open(B/'proof-final'/f'{v}.png');assert im.size==(512,512);x=(i%4)*512;y=(i//4)*530;sheet.paste(im.convert('RGB'),(x,y));draw.text((x+8,y+514),f'ernietta {rev} / {v}',fill='#202020')
sheet.save(B/'contact-sheet.png')
print('FULL PROOF READY; inspect every frame before packaging.',flush=True)
