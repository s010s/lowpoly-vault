import json,sys,subprocess,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone
R=Path('/workspace/lowpoly-vault');W=R/'production/continuous-small-life-round17-20261018/work/batch-51'
aid=sys.argv[1];rev=sys.argv[2] if len(sys.argv)>2 else 'r001';w=W/aid/rev;s=R/'scripts';gen=W/'tools/generator.py';config=w/'build-config.json'
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['generator.py']:shutil.copyfile(gen,w/name)
# Actual first model-start timestamp before dispatch; source concept and freeze preexist.
start={'modeling_started_at':datetime.now(timezone.utc).isoformat(),'meaning':'First generator construction complete; first Blender geometry execution begins after this receipt. Modeling source authored after frozen concepts.','inputs':{'generator':sha(w/'generator.py'),'config':sha(config),'freeze':sha(w/'derived-freeze.json')}};save(w/'model-start.json',start)
inputs={'generator':str(w/'generator.py'),'config':str(config),'brief':str(w/'brief.json'),'references':str(w/'references.json'),'helper':str(s/'asset_common.py'),'audit':str(s/'qa_glb.py')}
manifest={'schema_version':1,'lane':'build','jobs':[{'asset_id':aid,'revision':rev,'job_id':'build-original','inputs':inputs,'argv':['{blender}','--factory-startup','--disable-autoexec','--python','{input:generator}','--','--config','{input:config}','--output-dir','{output_dir}'],'outputs':[aid+'.blend',aid+'.glb','metadata.json','qa.json'],'config':{'blender':'4.3.2','seed':json.loads(config.read_text())['seed'],'purpose':'first actual concept-led build'},'timeout_seconds':240}]}
save(w/'build-jobs.json',manifest)
subprocess.run([sys.executable,str(s/'run_asset_queue.py'),str(w/'build-jobs.json'),'--runs-root',str(w/'runs'),'--workers','1','--threads','2','--cpu-budget','2'],cwd=R,check=True)
results=list((w/'runs/build'/aid/rev/'build-original').glob('*/*/result.json'));result=json.loads(results[-1].read_text());print('RESULT',result['status']);out=results[-1].parent/'outputs'
a=R/'assets/candidates/continuous-small-life-round17-20261018/batch-51'/aid/rev
if result['status']!='succeeded':sys.exit(1)
a.mkdir(parents=True,exist_ok=True)
for f in out.iterdir():shutil.copyfile(f,a/f.name)
for name in ['brief.json','references.json','build-config.json','generator.py','concept-brief.md','derived-freeze.json','model-start.json']:shutil.copyfile(w/name,a/name)
shutil.copytree(w/'concepts',a/'concepts',dirs_exist_ok=True)
# Correct candidate metadata to final destination; model/source bytes untouched.
md=json.loads((a/'metadata.json').read_text());md.update(glb=str((a/(aid+'.glb')).relative_to(R)),blend=str((a/(aid+'.blend')).relative_to(R)),preview=str((a/'proof/hero.png').relative_to(R)),preview_status='pending actual exact GLB render');save(a/'metadata.json',md)
subprocess.run(['blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'tools/render_views.py'),'--',str(a/(aid+'.glb')),'--revision',rev,'--brief',str(a/'brief.json'),'--references',str(a/'references.json'),'--output-dir',str(a/'proof'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','8'],cwd=R,stdout=(a/'proof-render.stdout.txt').open('w'),stderr=subprocess.STDOUT,check=True)
print('PROOF_READY',a)
