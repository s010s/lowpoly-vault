from pathlib import Path
import json,subprocess,sys
R=Path.cwd();W=R/'production/batch82-stratovolcano-repair';B=W/'stratovolcano/r009';run=lambda n,args:subprocess.run([sys.executable,str(W/'run-stage.py'),n]+[str(x) for x in args],check=True)
bl=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
run('format-r009',['node','scripts/validate_gltf.cjs',B/'model.glb'])
run('runtime-r009',['node',W/'runtime-parse.mjs',B])
run('source-final-r009',bl+['scripts/check_source_export.py','--','--source',B/'source.blend','--glb',B/'model.glb','--output',B/'source-final.report.json','--collection','EXPORT'])
run('source-count-r009',bl+[W/'count-source-vertices.py','--',B])
run('surface-r009',bl+[W/'check-physical-surfaces.py','--',B])
run('source-reexport-r009',bl+[W/'source-reexport.py','--',R,B,W/'raw/source-reopen-r009'])
for i in (1,2):
 job={'asset_id':'stratovolcano','revision':'r009','job_id':'semantic-rebuild-'+str(i),'inputs':{'generator':str(B/'generator.py'),'config':str(B/'build-config.json'),'helper':str(R/'scripts/asset_common.py'),'audit':str(R/'scripts/qa_glb.py'),'brief':str(B/'brief.json'),'references':str(B/'references.json')},'argv':['{blender}','--factory-startup','--python','{input:generator}','--','--config','{input:config}','--output','{output_dir}'],'outputs':['model.glb','source.blend','metrics.json','source-metrics.json','flank-network.json']}
 manifest=W/('queue-r009-'+str(i)+'.json');manifest.write_text(json.dumps({'schema_version':1,'lane':'build','jobs':[job]},indent=2)+'\n')
 run('queue-r009-'+str(i),['flock','/tmp/lowpoly-production-blender.lock',sys.executable,'scripts/run_asset_queue.py',manifest,'--runs-root',W/'raw/rebuild-runs','--workers','1','--threads','2','--cpu-budget','2','--timeout-seconds','120'])
 results=list((W/'raw/rebuild-runs/build/stratovolcano/r009'/job['job_id']).rglob('result.json'));assert len(results)==1,results
 result=results[0]
 run('repro-r009-'+str(i),[sys.executable,'scripts/check_reproducibility.py','--glb',B/'model.glb','--rebuilt-glb',result.parent/'outputs/model.glb','--generator',B/'generator.py','--config',B/'build-config.json','--build-request',result.parent/'request.json','--build-result',result,'--rebuilt-output','model.glb','--root',R,'--output',B/('repro-final-'+str(i)+'.report.json')])
print('ALL AUTOMATED CHECKS DONE; no independent acceptance')
