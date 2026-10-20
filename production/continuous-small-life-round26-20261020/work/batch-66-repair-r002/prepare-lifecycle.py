from pathlib import Path
import json,hashlib
R=Path.cwd();old=R/'production/continuous-small-life-round26-20261020/work/batch-66';W=R/'production/continuous-small-life-round26-20261020/work/batch-66-repair-r002'
for n in ['package-candidates.py','write-metadata.py','compose-sheets.py','verify-package.py']:
 s=(old/n).read_text().replace("work/batch-66'","work/batch-66-repair-r002'")
 if n=='package-candidates.py':s=s.replace('GPT-6.1 Sol medium batch66','GPT-6.1 Sol medium batch66 boundedrepair').replace("'concept_inspected_at':gen['inspected_at']","'concept_inspected_at':gen['inspected_at']")
 (W/n).write_text(s)
s=(old/'run-lifecycle.py').read_text().replace("work/batch-66'","work/batch-66-repair-r002'")
s=s.replace("str(W/'count-source-vertices.py')","str(R/'production/continuous-small-life-round26-20261020/work/batch-66/count-source-vertices.py')").replace("str(W/'render-fixed8.py')","str(R/'production/continuous-small-life-round26-20261020/work/batch-66/render-fixed8.py')").replace("str(W/'runtime-parse.mjs')","str(R/'production/continuous-small-life-round26-20261020/work/batch-66/runtime-parse.mjs')")
s=s.replace("'argv':['{blender}','--factory-startup'","'argv':['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','{blender}','--background','--threads','2','--python-exit-code','1','--factory-startup','--disable-autoexec'")
s=s.replace("['flock','/tmp/lowpoly-production-blender.lock','python3','scripts/run_asset_queue.py'","['python3','scripts/run_asset_queue.py'").replace("'--workers','1','--threads','2'","'--allow-executable','/usr/bin/flock','--workers','1','--threads','2'")
# Do an actual schema/binding preflight before first exact final render.
needle=" if not (b/'proof-final/render-manifest.json').exists():"
insertion=""" if not (b/'binding-preflight-validation.json').exists():
  c=json.loads((R/'schemas/templates/candidate.template.json').read_text());c.update(asset_id=slug,revision=x['revision'],maker={'id':'GPT-6.1 Sol medium boundedrepair','task_id':'produce_batch66_models'})
  c['artifacts']={k:{'path':str((b/n).relative_to(R)),'sha256':H(b/n)} for k,n in {'glb':'model.glb','brief':'candidate-brief.json','references':'references.json','source':'source.blend','generator':'generator.py','config':'build-config.json'}.items()}
  for stage,e in c['stages'].items():e['criteria']=[{'id':q['id'],'status':'unknown','evidence':[],'note':'Pending final pixels and independent differential QA.'} for q in d['criteria'] if q['stage']==stage]
  (b/'binding-preflight.candidate.json').write_text(json.dumps(c,indent=2)+'\\n')
  with (b/'binding-preflight.profile.json').open('w') as f:subprocess.run(['python3','scripts/candidate_profile.py',str((b/'binding-preflight.candidate.json').relative_to(R)),'--root',str(R)],stdout=f,check=True)
  with (b/'binding-preflight-validation.json').open('w') as f:subprocess.run(['python3','scripts/validate_candidate.py',str(b/'binding-preflight.candidate.json'),'--root',str(R),'--profile','static-stylized-v1','--profile-contract',str(b/'binding-preflight.profile.json'),'--json'],stdout=f,check=True)
"""
s=s.replace(needle,insertion+needle)
(W/'run-lifecycle.py').write_text(s)
print('PER-JOB FLOCK LIFECYCLE PREPARED')
