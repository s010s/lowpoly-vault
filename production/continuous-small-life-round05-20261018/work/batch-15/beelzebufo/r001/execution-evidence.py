from pathlib import Path
import subprocess,json,shutil,os,time

for a in [asset]:
 root=Path('/workspace/batch15-'+a);w=root/'production/continuous-small-life-round05-20261018/work/batch-15'/a/'r001';out=root/'assets/candidates/continuous-small-life-round05-20261018/batch-15'/a/'r001';logs=w/'logs'
 for f in ['brief.json','references.json','freeze.json','config.json','build-config.json','inventory-record.json','reference-policy.json','profile-policy.json','references-profile.json','references-profile-mapping.json']:shutil.copy(w/f,out/f)
 run(root,['blender','-b','-t','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python',root/'scripts/check_source_export.py','--','--source',out/(a+'.blend'),'--glb',out/(a+'.glb'),'--output',out/'source-export.report.json'],logs/'source-export.log')
 run(root,['blender','-b','-t','2','--disable-autoexec','--python-exit-code','1','--python',w/'inspect_source.py','--',out/(a+'.blend'),out/'source-mesh-measurements.json'],logs/'source-mesh-measurements.log')
 jobs=[]
 for i in [1,2]:
  deps={'generator':w/'build.py','config':w/'config.json','brief':w/'brief.json','references':w/'references.json','freeze':w/'freeze.json','original_config':w/'build-config.json','policy':w/'reference-policy.json','helper':root/'scripts/asset_common.py','audit':root/'scripts/qa_glb.py'}
  jobs.append({'asset_id':a,'revision':'r001','job_id':'semantic-rebuild-'+str(i),'inputs':{k:str(v) for k,v in deps.items()},'argv':['{blender}','--factory-startup','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':[a+'.glb',a+'.blend','metadata.json','qa.json'],'config':{'seed':json.loads((w/'config.json').read_text())['seed'],'purpose':'fresh semantic rebuild '+str(i),'blender_version':'4.3.2'},'timeout_seconds':180})
 mf=w/'rebuild-jobs.json';mf.write_text(json.dumps({'schema_version':1,'lane':'build','jobs':jobs},indent=2)+'\n')
 run(root,['python3',root/'scripts/run_asset_queue.py',mf,'--runs-root',w/'runs','--workers','1','--threads','2','--cpu-budget','2'],logs/'queue.log')
 for i in [1,2]:
  reqs=list((w/'runs/build'/a/'r001'/('semantic-rebuild-'+str(i))).glob('*/*/request.json'));assert len(reqs)==1;req=reqs[0];attempt=req.parent
  run(root,['python3',root/'scripts/check_reproducibility.py','--glb',out/(a+'.glb'),'--rebuilt-glb',attempt/'outputs'/(a+'.glb'),'--generator',w/'build.py','--config',w/'config.json','--build-request',req,'--build-result',attempt/'result.json','--rebuilt-output',a+'.glb','--root',root,'--output',out/('reproducibility-'+str(i)+'.report.json')],logs/('rebuild-compare-'+str(i)+'.log'))
 run(root,['node',root/'scripts/validate_gltf.cjs',out/(a+'.glb')],logs/'khronos.log')
 run(root,['blender','-b','-t','2','--python-exit-code','1','--python',w/'render.py','--',out/(a+'.glb'),out/'views'],logs/'render.log')
 run(root,['node',w/'runtime.mjs',out/(a+'.glb'),out/'runtime'],logs/'runtime.log')
 print('ASSET_PIPELINE_DONE',a,flush=True)
