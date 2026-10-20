# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/small-life-batch80';a=W/'assets/tuya/r001';b=a.parent/'r002';b.mkdir();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json']:shutil.copy(a/n,b/n)
(b/'repair-freeze.json').write_text(json.dumps(dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision='r002',original_revision='r001',reason='Final hero showed overly smooth frustum sides and wedge-shaped material patch without legible volcanic facies. Repair actual flank/cap-edge relief with unequal angular fragments, localized rounded pillow-fragment relief and broken cap joints. No scope/source/scale/camera/material-palette change.',original_generator_sha256=H(a/'generator.py'),original_brief_sha256=H(a/'brief.json'),original_references_sha256=H(a/'references.json'),repair_authored=False),indent=2)+'\n')
t=(a/'generator.py').read_text().replace('n=144;vs=[]','n=96;vs=[]')
t=t.replace("joints=.004*math.sin(36*t)+.003*math.sin(19*t+.5)","joints=.009*math.sin(24*t)+.005*math.sin(13*t+.5)")
t=t.replace(".012*math.sin(11*t+j*.7)",".018*math.sin(11*t+j*.7)+.013*math.sin(29*t+j*2.1)")
t=t.replace("rr+=.014*patch*(.5+.5*math.cos(25*t+j*1.7))","rr+=.045*patch*(.5+.5*math.cos(17*t+j*1.7))")
t=t.replace("zz=z+(3.7*math.sin(5*t+1)+2.4*math.cos(9*t))*(1 if j<7 else .3)","zz=z+(3.7*math.sin(5*t+1)+2.4*math.cos(9*t))*(1 if j<7 else .3)\n   if j in [1,2,3]:zz+=11*math.sin(23*t+j*1.9)+7*math.cos(13*t+j)")
t=t.replace("'breccia' if (j<3 and 2.7<t<4.6) else 'tuff'","'breccia' if (j<4 and 2.7<t<4.6 and (math.sin(17*t+j*2)>-.25)) else 'tuff'")
(b/'generator.py').write_text(t)
