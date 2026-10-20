import json,sys,subprocess,hashlib,shutil
from pathlib import Path
R=Path('/workspace/lowpoly-vault');W=R/'production/continuous-small-life-round17-20261018/work/batch-51';s=R/'scripts';aid=sys.argv[1];rev=sys.argv[2] if len(sys.argv)>2 else 'r001';w=W/aid/rev;a=R/'assets/candidates/continuous-small-life-round17-20261018/batch-51'/aid/rev
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def run(cmd,log):
 with log.open('w') as f:r=subprocess.run(list(map(str,cmd)),cwd=R,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode: print('FAILED',r.returncode,log);print(log.read_text()[-3000:]);sys.exit(r.returncode)
shutil.copyfile(a/'qa.json',a/'export-qa.json')
run(['node',s/'validate_gltf.cjs',a/(aid+'.glb')],a/'khronos.stdout.txt')
run(['blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',s/'check_source_export.py','--','--source',a/(aid+'.blend'),'--glb',a/(aid+'.glb'),'--output',a/'source-export.report.json'],a/'source-reopen.stdout.txt')
m=json.loads((w/'build-jobs.json').read_text());jobs=[]
for n in [1,2]:
 j=json.loads(json.dumps(m['jobs'][0]));j['job_id']='rebuild-'+str(n);j['config']['purpose']='separate deterministic semantic rebuild '+str(n);jobs.append(j)
m['jobs']=jobs;save(w/'rebuild-jobs.json',m)
run([sys.executable,s/'run_asset_queue.py',w/'rebuild-jobs.json','--runs-root',w/'rebuild-runs','--workers','1','--threads','2','--cpu-budget','2'],a/'rebuilds.stdout.txt')
for n in [1,2]:
 result=next((w/'rebuild-runs/build'/aid/rev/('rebuild-'+str(n))).glob('*/*/result.json'));out=result.parent/'outputs'
 run([sys.executable,s/'check_reproducibility.py','--glb',a/(aid+'.glb'),'--rebuilt-glb',out/(aid+'.glb'),'--generator',w/'generator.py','--config',w/'build-config.json','--build-request',result.parent/'request.json','--build-result',result,'--rebuilt-output',aid+'.glb','--root',R,'--output',a/('rebuild-'+str(n)+'.report.json')],a/('rebuild-'+str(n)+'.stdout.txt'))
md=json.loads((a/'metadata.json').read_text());md['preview_status']='rendered exact GLB; pending independent review';md['preview']=str((a/'proof/hero.png').relative_to(R));md['preview_sha256']=hashlib.sha256((a/'proof/hero.png').read_bytes()).hexdigest();md['limitations']=['Independent QA pending','SwiftShader is software only; hardware GPU not verified','Nine-copy neutral benchmark is not parent/museum scene integration'];save(a/'metadata.json',md)
print('TECHNICAL_READY',aid)
