# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,subprocess,shutil,sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent;B=R/'production/small-life-batch81/assets/charnia/r006';W=R/'production/small-life-batch81';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
def run(name,args):subprocess.run(['python3',str(T/'run-job.py'),str(B),name]+list(map(str,args)),cwd=R,check=True)
bl=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
put(B/'diagnostic-disposition.json',{'inspected_at':now(),'glb_sha256':H(B/'model.glb'),'decision':'selected_for_full_exact_subject_lifecycle_not_independent_acceptance','images_personally_opened':['diagnostic/hero.png','diagnostic/top.png','diagnostic/clay.png','diagnostic-topclay/clay.png'],'observations':'Continuous primary unit boundaries and three shorter subordinate divisions can now be followed in top and gray top, unlike r003 scattered slash facets. Geometry-only nesting is also more apparent in the foreshortened hero/clay, though intentionally shallow and subdued. Original scope and renderer unchanged. Final independent difference review remains required.','diagnostic_manifests':{n:H(B/n/'render-manifest.json') for n in ['diagnostic','diagnostic-topclay']}})
run('format',['node','scripts/validate_gltf.cjs',B/'model.glb'])
run('source-reopen',bl+[R/'scripts/check_source_export.py','--','--source',B/'source.blend','--glb',B/'model.glb','--output',B/'source-final.report.json','--collection','EXPORT'])
run('source-vertex-counts',bl+[T/'count-source-vertices.py','--',B])
run('physical-surfaces',bl+[T/'check-physical-surfaces.py','--',B])
run('saved-source-reexport',bl+[T/'source-reexport.py','--',R,B,B/'saved-source-reexport'])
run('runtime',['node',T/'runtime-parse.mjs',B])
for i in [1,2]:
 job={'asset_id':'charnia','revision':'r006','job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(B/'generator.py'),'config':str(B/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py'),'brief':str(B/'brief.json'),'references':str(B/'references.json')},'argv':['{blender}','--factory-startup','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json']}
 p=B/('queue-semantic-rebuild-'+str(i)+'.json');put(p,{'schema_version':1,'lane':'build','jobs':[job]})
 run('queue-semantic-rebuild-'+str(i),['flock','/tmp/lowpoly-production-blender.lock','python3','scripts/run_asset_queue.py',p,'--runs-root',W/'charnia-repair-rebuild-runs','--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','120','--resume'])
 results=list((W/'charnia-repair-rebuild-runs/build/charnia/r006').rglob('result.json'))
 result=next(p for p in results if json.loads(p.read_text())['job_id']==job['job_id']);d=json.loads(result.read_text());assert d['status']=='succeeded',d
 run('repro-final-'+str(i),['python3','scripts/check_reproducibility.py','--glb',B/'model.glb','--rebuilt-glb',result.parent/'outputs/model.glb','--generator',B/'generator.py','--config',B/'build-config.json','--build-request',result.parent/'request.json','--build-result',result,'--rebuilt-output','model.glb','--root',R,'--output',B/('repro-final-'+str(i)+'.report.json')])
d=json.loads((B/'brief.json').read_text());d['packaging_adapter']={'created_at':now(),'frozen_design_brief_sha256':H(B/'brief.json'),'note':'Derived artifact closure only. Original r001 scope/criteria/dimensions/budgets remain byte-identical. r006 repair specification implements the same originally required branching.'};d['required_deliverables']=[{'role':k,'path':str((B/n).relative_to(R)),'sha256':H(B/n)} for k,n in [('source','source.blend'),('generator','generator.py'),('config','build-config.json')]];put(B/'candidate-brief.json',d)
sys.path.insert(0,str(R/'scripts'));from validate_candidate import check_brief
refs=json.loads((B/'references.json').read_text());check_brief(d,{'asset_id':'charnia'},set(x['id'] for x in refs['sources']),validation_profile='static-stylized-v1');assert all(s.get('rights_note') for s in refs['sources']);assert all(H(R/v['path'])==v['sha256'] for v in d['required_deliverables'])
put(B/'preproof-binding.json',{'checked_at':now(),'glb_sha256':H(B/'model.glb'),'brief_sha256':H(B/'candidate-brief.json'),'references_sha256':H(B/'references.json'),'source_generator_config_binding':'pass','check_brief':'pass-static-stylized-v1','original_brief_and_references_unchanged':True,'note':'Checked before every final frame; earlier diagnostics are separate subjects with original brief.'})
paths=[B/'generator.py',B/'build-config.json']+[R/'scripts'/n for n in ['asset_common.py','qa_glb.py','check_source_export.py','check_reproducibility.py','run_asset_queue.py','validate_gltf.cjs']]+[T/n for n in ['render-fixed8.py','runtime-parse.mjs','check-physical-surfaces.py','source-reexport.py','count-source-vertices.py']]
put(B/'build-dependencies.json',{'created_at':now(),'files':{str(p.relative_to(R)):H(p) for p in paths},'blender':{'version':'4.3.2','executable':'/usr/bin/blender','sha256':H(Path('/usr/bin/blender'))},'runtime_dependency':{'source':'Existing read-only /workspace/shared/lowpoly-landair-web-integration/node_modules','three_version':'0.180.0','three_package_sha256':H(R/'node_modules/three/package.json'),'gltf_validator_package_sha256':H(R/'node_modules/gltf-validator/package.json')},'seed':81,'external_source_media_incorporated':False})
run('proof-final',bl+[T/'render-fixed8.py','--',B/'model.glb','--revision','r006','--brief',B/'candidate-brief.json','--references',B/'references.json','--output-dir',B/'proof-final','--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'])
shutil.copy(B/'proof-final/hero.png',B/'preview.png')
from PIL import Image,ImageDraw
canvas=Image.new('RGB',(2048,1060),'#e8e4dc');draw=ImageDraw.Draw(canvas)
for k,n in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette']):
 x=(k%4)*512;y=(k//4)*530;canvas.paste(Image.open(B/'proof-final'/f'{n}.png').convert('RGB'),(x,y+18));draw.text((x+8,y+2),n,fill='#242424')
canvas.save(B/'contact-sheet.png')
print('READY FOR INDIVIDUAL FINAL PIXEL INSPECTION',H(B/'model.glb'),flush=True)
