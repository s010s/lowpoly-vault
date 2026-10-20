# SPDX-License-Identifier: MIT
import json,sys,subprocess,shutil,hashlib,datetime,time
from pathlib import Path
R=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'scripts'));s=sys.argv[1];o=R/'assets/candidates/continuous-small-life-round18-20261020/batch-53'/s/'r001';w=W/s/'r001';w.mkdir(parents=True,exist_ok=True)
def put(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def cmd(a,log):
 st=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with (w/log).open('w') as f:r=subprocess.run(a,cwd=R,stdout=f,stderr=subprocess.STDOUT)
 with (w/'execution.jsonl').open('a') as f:f.write(json.dumps({'argv':list(map(str,a)),'started_at':st,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'returncode':r.returncode,'log':log})+'\n')
 if r.returncode:raise RuntimeError(f'{log}: exit {r.returncode}')
inputs={k:str(p.resolve()) for k,p in {'generator':o/'generator.py','config':o/'config.json','helper':R/'scripts/asset_common.py','audit':R/'scripts/qa_glb.py','brief':o/'brief.json','references':o/'references.json'}.items()}
jobs=[]
for k in ['initial','rebuild-1','rebuild-2']:
 jobs.append({'asset_id':s,'revision':'r001','job_id':k,'inputs':inputs,'argv':['{blender}','--factory-startup','--disable-autoexec','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':[f'{s}/{s}.glb',f'{s}/{s}.blend',f'{s}/metadata.json',f'{s}/qa.json'],'config':{'original':'fresh deterministic build; independent original Blender process each attempt'},'timeout_seconds':180})
put(w/'build-jobs.json',{'schema_version':1,'lane':'build','jobs':jobs})
cmd(['python3','scripts/run_asset_queue.py',str(w/'build-jobs.json'),'--runs-root',str(w/'runs'),'--workers','1','--threads','2','--cpu-budget','2'],'queue.log')
runs={}
for p in (w/'runs/build').rglob('result.json'):
 q=json.loads(p.read_text());runs[q['job_id']]=p.parent
for f in [f'{s}.glb',f'{s}.blend','metadata.json','qa.json']:shutil.copy(runs['initial']/'outputs'/s/f,o/f)
cmd(['blender','-b','-t','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python','scripts/check_source_export.py','--','--source',str(o/(s+'.blend')),'--glb',str(o/(s+'.glb')),'--output',str(o/'source-export.report.json')],'source-reopen.log')
for k in ['rebuild-1','rebuild-2']:
 cmd(['python3','scripts/check_reproducibility.py','--glb',str(o/(s+'.glb')),'--rebuilt-glb',str(runs[k]/'outputs'/s/(s+'.glb')),'--generator',str(o/'generator.py'),'--config',str(o/'config.json'),'--build-request',str(runs[k]/'request.json'),'--build-result',str(runs[k]/'result.json'),'--rebuilt-output',f'{s}/{s}.glb','--root',str(R),'--output',str(o/(k+'.report.json'))],k+'.log')
cmd(['node','scripts/validate_gltf.cjs',str(o/(s+'.glb'))],'khronos.log')
cmd(['blender','-b','-t','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python',str(o/'proof-renderer.py'),'--',str(o/(s+'.glb')),'--revision','r001','--brief',str(o/'brief.json'),'--references',str(o/'references.json'),'--output-dir',str(o/'views'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette'+(',claytop' if s=='halopoa-furrowed-burrow' else ''),'--turntable-frames','0','--resolution','512','--samples','16'],'render.log')
shutil.copy(o/'views/hero.png',o/'preview-hero.png')
print(s,'build/reopen/two rebuilds/format/eight views completed')
