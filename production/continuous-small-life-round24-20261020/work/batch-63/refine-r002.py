# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round24-20261020/work/batch-63';P=W/'repair-r002';P.mkdir();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();F=json.loads((W/'final-selection.json').read_text());new=[]
for x in F:
 if x['asset_id'] not in ['caldera','dogtooth-spar-cavity']:continue
 src=R/x['path'];b=src.parent/'r002';b.mkdir()
 for n in ['brief.json','brief.md','references.json','concept-original.png','concept-generation.json','concept-prompt.txt']:shutil.copyfile(src/n,b/n)
 cfg=json.loads((src/'build-config.json').read_text());cfg['revision']='r002';cfg['repair_decision']='Targeted craft refinement from actual r001 fixed8 pixel inspection. Preserve frozen original design, scale, claims and feature obligations. '+('Break smooth concentric terrace appearance by coherent radial erosion bays, more variable remnant rim and broader subdued breach.' if x['asset_id']=='caldera' else 'Break uniform ring-of-teeth appearance with nonuniform angular clusters, wall depths, varied crystal lengths and more irregular host rim. Preserve12triangular-face scalenohedral construction and central void.');(b/'build-config.json').write_text(json.dumps(cfg,indent=2)+'\n')
 (b/'candidate-brief.json').write_bytes((b/'brief.json').read_bytes());(b/'modeling-freeze.json').write_text(json.dumps(dict(schema_version=1,frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='targeted r002 repair freeze before r002 geometry',original_modeling_freeze_sha256=H(src/'modeling-freeze.json'),brief_sha256=H(b/'brief.json'),config_sha256=H(b/'build-config.json'),references_sha256=H(b/'references.json'),concept_sha256=H(b/'concept-original.png'),decision=cfg['repair_decision'],scope_changes='None; unchanged whole-organism/geological form and original feature obligations.'),indent=2)+'\n')
 x.update(revision='r002',path=str(b.relative_to(R)));new.append(x.copy())
(W/'final-selection.json').write_text(json.dumps(F,indent=2)+'\n');(P/'final-selection.json').write_text(json.dumps(new,indent=2)+'\n')
s=(W/'generator.py').read_text();s=s.replace('edge=1+.045*math.sin(3*a+.4)+.03*math.cos(7*a)','edge=1+.07*math.sin(3*a+.4)+.04*math.cos(7*a)+(.045*math.sin(17*a+.3) if k>=4 else .012*math.sin(9*a))');s=s.replace(')/.19)**2',')/.26)**2');s=s.replace('*22*(r**1.3)','*72*(r**1.3)');s=s.replace('breach*180*','breach*225*');s=s.replace('zz-=18*(.5+.5*math.cos(18*a))**4','zz-=48*(.5+.5*math.cos(18*a+.4))**4');s=s.replace("irr=1+.05*math.sin(3*a+.5)+.035*math.sin(7*a)","irr=1+.10*math.sin(3*a+.5)+.075*math.sin(7*a)+.035*math.sin(13*a+1.2)");s=s.replace("a=math.tau*(j+.25*tier)/count;rad=[.63,.51,.34][tier];yy=[-.10,-.025,.05][tier]","a=math.tau*(j+.31*tier)/count+.075*math.sin(j*2.17+1.6*tier);rad=[.63,.51,.34][tier]*(1+.085*math.sin(j*1.89+tier));yy=[-.10,-.025,.05][tier]+.018*math.sin(j*2.8+tier)");s=s.replace('length=.028+.045*','length=.017+.052*');s=s.replace('if tier==0 and j%5==0:length=.08','if tier==0 and j in [2,7,16]:length=.08')
(P/'generator.py').write_text(s)
for x in new:shutil.copyfile(P/'generator.py',R/x['path']/'generator.py')
for name in ['render-fixed8.py','runtime-parse.mjs','count-source-vertices.py','run-lifecycle.py','finalize-bundle.py']:
 s=(W/name).read_text().replace("W=R/'production/continuous-small-life-round24-20261020/work/batch-63'","W=R/'production/continuous-small-life-round24-20261020/work/batch-63/repair-r002'")
 (P/name).write_text(s)
print('R002 frozen before authoring',len(new))
