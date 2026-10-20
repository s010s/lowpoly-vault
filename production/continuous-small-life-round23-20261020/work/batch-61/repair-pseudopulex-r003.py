# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round23-20261020/work/batch-61';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();final=json.loads((W/'final-selection.json').read_text());x=final[0];old=R/x['path'];b=old.parent/'r003';b.mkdir()
for n in ['brief.json','brief.md','references.json','concept-original.png','concept-prompt.txt','concept-generation.json']:shutil.copyfile(old/n,b/n)
cfg=json.loads((old/'build-config.json').read_text());cfg['revision']='r003';cfg['repair_decision']='Head macro revealed separated palp beads in r002. Add continuous slender segmented support shafts connecting them to head. No antenna/stylet/leg/abdomen change and no scope narrowing.';(b/'build-config.json').write_text(json.dumps(cfg,indent=2)+'\n')
(b/'modeling-freeze.json').write_text(json.dumps({'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'targeted palp connectivity repair under unchanged original premodel brief','brief_sha256':H(b/'brief.json'),'config_sha256':H(b/'build-config.json'),'references_sha256':H(b/'references.json'),'original_freeze_sha256':H(old.parent/'r001/modeling-freeze.json'),'repair':cfg['repair_decision'],'no_scope_narrowing':True},indent=2)+'\n')
s=(old/'generator.py').read_text();needle="  for j,(rooty,kneey,footy) in enumerate("
insert="  for q,count in [(0,3),(1,4)]:\n   pts=[(s*(.00045+.00016*j+.00023*q),-.00715-.00028*j,.0028-.00016*j) for j in range(count)]\n   tube('short_artistic_maxillary_and_labial_palps',pts,[.000095 for _ in pts],'chitin',6)\n"
s=s.replace(needle,insert+needle);(b/'generator.py').write_text(s)
d=json.loads((old/'candidate-brief.json').read_text());d['required_deliverables']=[{'role':k,'path':str((b/n).relative_to(R)),'sha256':H(b/n)} for k,n in [('generator','generator.py'),('config','build-config.json')]];d['packaging_adapter']['note']='Source binding added after saved-source creation; design/claims remain original. r003 repairs palp continuity only.';(b/'candidate-brief.json').write_text(json.dumps(d,indent=2)+'\n')
x.update(revision='r003',path=str(b.relative_to(R)));(W/'final-selection.json').write_text(json.dumps(final,indent=2)+'\n')
#Only build + reopen first; bind saved-source before final evidence renders.
