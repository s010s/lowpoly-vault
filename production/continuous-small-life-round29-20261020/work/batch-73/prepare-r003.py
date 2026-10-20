from pathlib import Path
import json,shutil,datetime,hashlib
R=Path.cwd();W=R/'production/continuous-small-life-round29-20261020/work/batch-73';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();final=json.loads((W/'final-selection.json').read_text());shutil.copy(W/'final-selection.json',W/'selection-r002.json');shutil.copy(W/'generator.py',W/'generator-r002.py')
notes={'striated-bedrock':'Actual r002 hero/clay inspected: more natural edge but principal groove centers still too evenly distributed and similar scale. Keep all nine aligned incisions, cluster narrow scratches apart from three broader unequal gouges with broad intervening smoothed rock, strengthen natural broken perimeter.','banded-iron-formation':'Actual r002 hero inspected: improved rough tapered top and genuinely unequal laminae but repeated ridges still too continuously bellows-like. Keep64 laminae but damp and interrupt rib relief with coherent irregular erosional patches and crosscut fracture notches, without switching to color-only bands.'}
for x in final:
 if x['asset_id'] not in notes:continue
 old=R/x['path'];b=old.parent/'r003';b.mkdir();files=['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json']
 for f in files:shutil.copy(old/f,b/f)
 d={'asset_id':x['asset_id'],'revision':'r003','frozen_at':now(),'original_freeze_path':str((old.parent/'r001/modeling-freeze.json').relative_to(R)),'original_freeze_sha256':H(old.parent/'r001/modeling-freeze.json'),'previous_attempt_path':str(old.relative_to(R)),'repair_reason':notes[x['asset_id']],'unchanged_scope':True,'implementation_authoring_next':True,'files':{f:H(b/f) for f in files}}
 (b/'repair-freeze.json').write_text(json.dumps(d,indent=2)+'\n');x.update(revision='r003',path=str(b.relative_to(R)))
(W/'maker-r002-targeted-observations.json').write_text(json.dumps(notes,indent=2)+'\n');(W/'final-selection.json').write_text(json.dumps(final,indent=2)+'\n');print('r003 repair frozen',now())
