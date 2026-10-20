# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round24-20261020/work/batch-62';B=R/'assets/candidates/continuous-small-life-round24-20261020/batch-62/star-dune';old=B/'r001';b=B/'r002';b.mkdir(exist_ok=False);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['brief.json','brief.md','candidate-brief.json','references.json','modeling-freeze.json','concept-original.png','concept-prompt.txt','concept-generation.json']:shutil.copyfile(old/n,b/n)
c=json.loads((old/'build-config.json').read_text());c['revision']='r002';(b/'build-config.json').write_text(json.dumps(c,indent=2)+'\n');s=(old/'generator.py').read_text();s=s.replace("arm=int((5*a/math.tau+.5)%5);outer=(.74+.26*ridge)*arms[arm]","outer=(.94+.06*ridge)*(1+.07*math.sin(2*a)+.04*math.cos(3*a))")
s=s.replace("z=100*(1-t)**1.13*(.48+.52*ridge)*(1-.04*math.sin(3*a)*t)","z=100*(1-t)**1.13*(1-.65*(1-ridge)*4*t*(1-t))*(1-.04*math.sin(3*a)*t)")
(b/'generator.py').write_text(s)
(b/'repair-freeze.json').write_text(json.dumps({'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repair':'Remove stepwise arm-length discontinuities and near-summit radial canyon wedges. Smooth unequal lower apron, connected five ridges, concave saddles with angular relief fading continuously into summit and ground. Same generic landform brief, no scope narrowing.','parent_glb_sha256':H(old/'model.glb'),'brief_sha256':H(b/'candidate-brief.json'),'config_sha256':H(b/'build-config.json'),'generator_sha256':H(b/'generator.py')},indent=2)+'\n')
deps=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py',W/'render-fixed8.py'];(b/'build-dependencies.json').write_text(json.dumps({str(p.relative_to(R)):H(p) for p in deps},indent=2)+'\n')
a=json.loads((W/'repair-selection.json').read_text());a.append({'asset_id':'star-dune','revision':'r002','path':str(b.relative_to(R))});(W/'repair-selection.json').write_text(json.dumps(a,indent=2)+'\n')
