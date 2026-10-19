from pathlib import Path
import json,shutil
R=Path.cwd();B=R/'production/undersea-invertebrates-concept-20261019';A=R/'assets/candidates/undersea-invertebrates-concept-20261019';jobs=[]
for p in A.iterdir():
 d=p/'r001';slug=p.name;at=list((B/'runs/build'/slug/'r001/initial-build').glob('*/*'))[0]
 for f in (at/'outputs'/slug).iterdir():shutil.copy2(f,d/f.name)
 m=json.loads((d/'metadata.json').read_text());m['glb']=str((d/(slug+'.glb')).relative_to(R));m['blend']=str((d/(slug+'.blend')).relative_to(R));m['preview']=str((d/'proof/hero.png').relative_to(R));(d/'metadata.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
 jobs.append({'asset_id':slug,'revision':'r001','job_id':'quick-proof','inputs':{'glb':str(d/(slug+'.glb')),'brief':str(d/'brief.md'),'references':str(d/'references.json'),'renderer':str(R/'scripts/render_candidate_views.py'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py')},'argv':['{blender}','--factory-startup','--python','{input:renderer}','--','{input:glb}','--revision','r001','--brief','{input:brief}','--references','{input:references}','--output-dir','{output_dir}','--views','hero,reversehero,right,top,clay','--turntable-frames','0','--resolution','256','--samples','4'],'outputs':['render-manifest.json','render-config.json','hero.png','reversehero.png','right.png','top.png','clay.png'],'timeout_seconds':180})
 print(slug,m['triangles'],m['glb_bytes'])
(B/'quick-jobs.json').write_text(json.dumps({'schema_version':1,'lane':'preview','jobs':jobs},indent=2)+'\n')
