# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/small-life-batch80';a=W/'assets/spriggina/r002';b=a.parent/'r003';b.mkdir();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json']:shutil.copy(a/n,b/n)
(b/'repair-freeze.json').write_text(json.dumps(dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision='r003',original_revision='r001',predecessor='r002',reason='Actual r002 final top inspection found sinusoidal slab boundary ornamental rather than broken sandstone. Replace only slab margin with unequal piecewise linear rock breaks. No fossil/source/scope/palette/camera change.',previous_generator_sha256=H(a/'generator.py'),original_brief_sha256=H(a/'brief.json'),original_references_sha256=H(a/'references.json'),repair_authored=False),indent=2)+'\n')
t=(a/'generator.py').read_text()
old="x*=1-.13*edgev**5+.055*math.sin(18*v+1)*edgeu**4+.025*math.cos(31*v)*edgeu**6;y*=1-.10*edgeu**5+.045*math.sin(19*u)*edgev**4"
new="""def interp(q,vals):
   f=q*(len(vals)-1);k=min(len(vals)-2,int(f));return vals[k]+(vals[k+1]-vals[k])*(f-k)
  offset=interp(v,[-.002,.0005,-.001,.0025,-.0006,.0013,-.003]) if u<.5 else interp(v,[.001,-.0022,.0004,-.003,.0015,-.001,.002])
  x=x*(1-.10*edgev**5)+offset*edgeu**5
  y=y*(1-.08*edgeu**5)+interp(u,[-.0015,.0006,-.001,.0018,-.0011,.0003])*(1 if v>.5 else -.6)*edgev**6"""
assert old in t;t=t.replace(old,new);(b/'generator.py').write_text(t)
