from pathlib import Path
import json,hashlib,datetime,shutil,subprocess
r=Path.cwd();w=r/'production/continuous-small-life-round28-20261020/work/batch-70';b=r/'assets/candidates/continuous-small-life-round28-20261020/batch-70/waputikia/r001';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_design_freeze_sha256':H(b/'modeling-freeze.json'),'observation':'First exactGLB hero/front shows tips beyond slab and terminal sprays too sparse to read bush-like at512px. This is maker self-review, not acceptance.','repair':'Increase original support footprint to enclose all relief, retain finite specimen scope and robust axis, denser fast-dividing thicker fine terminal fans. Retain all initial generator/outputs/proofs in attempts/initial. Original immutable design brief/config/references unchanged.','scope_change':False}
(b/'diagnostic-repair-freeze.json').write_text(json.dumps(record,indent=2)+'\n')
keep={'concept-original.png','concept-prompt.txt','concept-generation.json','references.json','brief.json','brief.md','build-config.json','prefreeze-ledger-check.json','modeling-freeze.json','diagnostic-repair-freeze.json'};old=b/'attempts/initial';old.mkdir(parents=True)
for p in list(b.iterdir()):
 if p.name not in keep and p.name!='attempts':shutil.move(p,old/p.name)
s=(old/'generator.py').read_text().replace('Original batch68 geometry;','Original batch70 geometry;').replace('.037*rr*math.cos(a)', '.049*rr*math.cos(a)').replace('.040+.039*rr*math.sin(a)', '.044+.047*rr*math.sin(a)').replace('max(.00007,r*.5)','max(.00013,r*.5)').replace('max(.000075,r*.48)','max(.00013,r*.48)').replace('length*rng.uniform(.48,.64)','length*rng.uniform(.56,.72)').replace(".0064,r*.30,3)",".0072,r*.33,4)")
(b/'generator.py').write_text(s)
files=[b/'generator.py',b/'build-config.json',r/'scripts/asset_common.py',r/'scripts/qa_glb.py'];(b/'build-dependencies.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender':'4.3.2','seed':70,'files':[{'path':str(p.relative_to(r)),'sha256':H(p)} for p in files]},indent=2)+'\n')
# Reuse lifecycle runner with one-asset selection in separate script, no sharedselection overwrite.
s=(w/'run-lifecycle.py').read_text();s=s[:s.index("run(W,'runtime'")];s=s.replace("final=json.loads((W/'final-selection.json').read_text())","final=[x for x in json.loads((W/'final-selection.json').read_text()) if x['asset_id']=='waputikia']")
(w/'run-repair-waputikia.py').write_text(s)
