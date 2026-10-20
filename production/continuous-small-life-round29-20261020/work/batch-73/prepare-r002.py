# SPDX-License-Identifier: MIT
from pathlib import Path
import json,shutil,hashlib,datetime
R=Path.cwd();W=R/'production/continuous-small-life-round29-20261020/work/batch-73';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
notes={'fractofusus':'Inspected actual r001 hero/top/clay. Spindle and low relief present, but secondary subdivisions align into quilt-like grid. Repair to distinct compact curved primary modules with locally varying secondary/tertiary hierarchy, no leaf/stem or raised organism.','striated-bedrock':'Inspected actual r001 hero/top/clay. Real incisions present but rectangular footprint and near-constant rails read manufactured. Repair natural broken perimeter, unequal traversing gouges, coherent slight wandering, minor crossfracture and low natural undulation.','fumarole-vent':'Inspected actual r001 hero/top/clay. Cavity/crust present but radial rings and bowl-like smooth outline too regular. Repair angular narrow crooked fissure in non-radial rock terrain, interrupted rough relief crust and branching fractures; no smoke/water.','banded-iron-formation':'Inspected actual r001 hero/top/clay. Fine real laminae visible but continuous regular bellows perimeter and flat dark cap not natural broken specimen. Repair coherent unequal ribs, local nonperiodic erosional notches, rough tapered broken top with bands terminating on smaller angular top. Do not replace relief by color.'}
(W/'maker-r001-observations.json').write_text(json.dumps(notes,indent=2)+'\n');shutil.copy(W/'generator.py',W/'generator-r001.py');shutil.copy(W/'final-selection.json',W/'initial-selection-r001.json')
final=[]
for x in json.loads((W/'final-selection.json').read_text()):
 old=R/x['path'];b=old.parent/'r002';b.mkdir();files=['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json']
 for f in files:shutil.copy(old/f,b/f)
 d={'asset_id':x['asset_id'],'revision':'r002','frozen_at':now(),'original_freeze_path':str((old/'modeling-freeze.json').relative_to(R)),'original_freeze_sha256':H(old/'modeling-freeze.json'),'repair_reason':notes[x['asset_id']],'unchanged_scope':True,'original_design_and_config_immutable':True,'implementation_authoring_next':True,'files':{f:H(b/f) for f in files}}
 (b/'repair-freeze.json').write_text(json.dumps(d,indent=2)+'\n');final.append({**x,'revision':'r002','path':str(b.relative_to(R))})
(W/'final-selection.json').write_text(json.dumps(final,indent=2)+'\n')
print('Repair freezes fixed',now())
