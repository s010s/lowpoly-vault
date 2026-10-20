# SPDX-License-Identifier: MIT
from pathlib import Path
import json,subprocess,datetime,time,hashlib,shutil
from PIL import Image,ImageDraw
R=Path.cwd();W=R/'production/continuous-small-life-round24-20261020/work/batch-63';P=W/'repair-r003';x=json.loads((P/'final-selection.json').read_text())[0];b=R/x['path'];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(name,args,heavy=False):
 if heavy:args=['flock','/tmp/lowpoly-production-blender.lock']+args
 t=time.monotonic();start=now()
 with (b/(name+'.log')).open('x') as log:
  proc=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT);pid=proc.pid;rc=proc.wait(timeout=1800)
 with (b/'lifecycle.jsonl').open('a') as log:log.write(json.dumps(dict(stage=name,command=args,pid=pid,started_at=start,ended_at=now(),wall_seconds=time.monotonic()-t,exit_code=rc))+'\n')
 print(name,rc,flush=True);assert rc==0
bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
run('build',bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(b)],True)
#Complete delivery roles and rights BEFORE final subject-bound proof render.
brief=json.loads((b/'brief.json').read_text());brief['required_deliverables']=[dict(role=k,path=str((b/n).relative_to(R)),sha256=H(b/n)) for k,n in [('generator','generator.py'),('config','build-config.json'),('source','source.blend')]];brief['packaging_adapter']=dict(created_at=now(),frozen_design_brief_sha256=H(b/'brief.json'),note='r003 localized QA repair; original frozen claims/scope/scale/views unchanged. Delivery source/generator/config binding and rights complete before final renders.');(b/'candidate-brief.json').write_text(json.dumps(brief,indent=2)+'\n')
assert (b/'LICENSES.md').exists();deps=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py',P/'render-fixed8.py'];(b/'build-dependencies.json').write_text(json.dumps(dict(schema_version=1,files={str(p.relative_to(R)):H(p) for p in deps},blender='4.3.2',three='0.180.0',required_external_assets=[],note='Texture-free deterministic geometry, no external source asset or changed installed dependency.'),indent=2)+'\n')
run('format',['node','scripts/validate_gltf.cjs',str(b/'model.glb')])
run('source-reopen',bl+['scripts/check_source_export.py','--','--source',str(b/'source.blend'),'--glb',str(b/'model.glb'),'--output',str(b/'source-final.report.json'),'--collection','EXPORT'],True)
run('proof-final',bl+[str(P/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision','r003','--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'],True)
shutil.copyfile(b/'proof-final/hero.png',b/'preview.png');sheet=Image.new('RGB',(2048,1060),'#ece8e0');draw=ImageDraw.Draw(sheet)
for i,v in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette']):
 im=Image.open(b/'proof-final'/(v+'.png')).convert('RGB');assert im.size==(512,512);xx=(i%4)*512;yy=(i//4)*530;sheet.paste(im,(xx,yy+18));draw.text((xx+8,yy+3),v,fill='#25231f')
sheet.save(b/'contact-sheet.png',compress_level=9)
run('runtime',['node',str(P/'runtime-parse.mjs'),str(b)])
run('source-counts',bl+[str(P/'count-source-vertices.py')],True)
#Each genuine single-job queue run acquires and releases the shared lock independently.
for i in [1,2]:
 job=dict(asset_id='caldera',revision='r003',job_id='semantic-rebuild-'+str(i),inputs=dict(generator=str(b/'generator.py'),config=str(b/'build-config.json'),helper=str(R/'scripts/asset_common.py'),audit=str(R/'scripts/qa_glb.py')),argv=['{blender}','--factory-startup','--disable-autoexec','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],outputs=['model.glb','source.blend','metrics.json','source-metrics.json']);jp=P/('rebuild-job-'+str(i)+'.json');jp.write_text(json.dumps(dict(schema_version=1,lane='build',jobs=[job]),indent=2)+'\n')
 run('rebuild-queue-'+str(i),['python3','scripts/run_asset_queue.py',str(jp),'--runs-root',str(P/('rebuild-runs-'+str(i))),'--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','180'],True)
 result=next((P/('rebuild-runs-'+str(i))).rglob('result.json'))
 run('repro-bound-'+str(i),['python3','scripts/check_reproducibility.py','--glb',str(b/'model.glb'),'--rebuilt-glb',str(result.parent/'outputs/model.glb'),'--generator',str(b/'generator.py'),'--config',str(b/'build-config.json'),'--build-request',str(result.parent/'request.json'),'--build-result',str(result),'--rebuilt-output','model.glb','--root',str(R),'--output',str(b/('repro-final-'+str(i)+'.report.json'))])
print('R003 lifecycle complete',flush=True)
