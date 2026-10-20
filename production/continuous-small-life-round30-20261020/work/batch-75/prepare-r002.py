# SPDX-License-Identifier: MIT
from pathlib import Path
import json,datetime,hashlib,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round30-20261020/work/batch-75';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sel=json.loads((W/'final-selection.json').read_text());(W/'initial-selection-r001.json').write_text(json.dumps(sel,indent=2)+'\n')
notes={'glacial-horn':'Actual r001 hero/top/clay inspected: silhouette too soft/conical. r002 keeps original scope, makes four true planar-sided pyramidal faces with physical cirque concavity and cardinal convergent ridges; no camera/material/depth trick.', 'eruptive-fissure':'Actual r001 hero/top/clay inspected: top confirms recessed crack, shallow hero obscures it. r002 widens narrow inter-vent crack physically and roughens terrain outline/lips. Final diagnostic hero elevation38 specified before r002 proof, not to conceal surface defects.', 'banded-gneiss-outcrop':'Actual r001 hero/top/clay inspected: folded physical bands present but top blank and too smooth. r002 adds integrated triangulated broken top with coarse mineral band regions and surface relief, rougher natural side silhouette; single shared-vertex shell, no overlays.'}
for x in sel:
 if x['asset_id'] not in notes:continue
 old=R/x['path'];b=old.parent/'r002';b.mkdir();
 for n in ['concept-original.png','concept-prompt.txt','concept-generation.json','references.json']:shutil.copy(old/n,b/n)
 for n in ['brief.json','build-config.json']:
  d=json.loads((old/n).read_text());d['repair_design']=notes[x['asset_id']];d['derived_from_original_premodel_file_sha256']=H(old/n)
  if n=='brief.json':d['brief_version']='r002'
  else:d['revision']='r002'
  (b/n).write_text(json.dumps(d,indent=2)+'\n')
 (b/'brief.md').write_text((old/'brief.md').read_text()+'\n\n## Retained-scope r002 repair freeze\n'+notes[x['asset_id']]+'\n')
 (b/'premodel-schema-check.json').write_text(json.dumps(dict(checked_at=now(),original_freeze_preserved=str(old/'modeling-freeze.json'),repair_generator_authored=False,repair_geometry_built=False),indent=2)+'\n')
 (b/'modeling-freeze.json').write_text(json.dumps(dict(asset_id=x['asset_id'],revision='r002',frozen_at=now(),original_premodel_freeze_sha256=H(old/'modeling-freeze.json'),status='Derived transparent repair freeze before r002 generator authorship; original scope unchanged and r001 fully retained.',files={n:H(b/n) for n in ['brief.json','brief.md','build-config.json','references.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json']}),indent=2)+'\n')
 (b/'repair-freeze.json').write_text(json.dumps(dict(frozen_at=now(),reason=notes[x['asset_id']],original_revision='r001',original_glb_sha256=H(old/'model.glb'),original_freeze_sha256=H(old/'modeling-freeze.json'),repair_authorship_next=True),indent=2)+'\n');x['revision']='r002';x['path']=str(b.relative_to(R))
(W/'final-selection.json').write_text(json.dumps(sel,indent=2)+'\n');print(now(),sel)
