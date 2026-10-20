# SPDX-License-Identifier: MIT
from pathlib import Path
import json,shutil,hashlib,datetime
w=Path('production/small-life-batch79');s=(w/'generator-r005.py').read_text();s=s.replace("amu=max(0,min(1,(.055-yb)/.018))","amu=max(0,min(1,(.045-yb)/.018))")
s=s.replace("ms.append('fossil' if j%4 in [0,1] else 'matrix')","ms.append('fossil' if j%4 in [0,1] or j>108 else 'matrix')")
s=s.replace("n=24;stations=[];u=-1.6;layer=0", "outline=[(-.65,0),(-.92,.2),(-.86,.65),(-.75,1.1),(-.65,1.6),(-.45,1.9),(-.05,2.1),(.35,2.04),(.65,1.7),(.80,1.2),(.72,.7),(.88,.25),(.6,0)];n=len(outline);stations=[];u=-1.6;layer=0")
s=s.replace("endtaper=.45+.55*math.sin(math.pi*(u+1.6)/3.2)**.34", "endtaper=.70+.30*math.sin(math.pi*(u+1.6)/3.2)**.45")
s=s.replace("y=.78*math.copysign(abs(cy)**.68,cy);z=.99+1.00*math.copysign(abs(sz)**.70,sz)", "y,z=outline[k];z*=.95+.12*math.sin(u*1.7)+.07*math.sin(u*4+.3)+.015*math.sin(layer*.8)")
s=s.replace("ledge=(.008+.022*(.5+.5*math.sin(layer*2.3+t*.7)))*flange*max(0,math.sin(t*2.7+layer*1.3))**2", "ledge=(.018+.040*(.5+.5*math.sin(layer*2.3+t*.7)))*flange*max(0,math.sin(t*2.7+layer*1.3))**2")
s=s.replace("z=.99+(z-.99)*shape+ledge*max(0,sz)", "z=z*(.97+.03*math.sin(u*2.1+t*.8))+ledge*max(0,sz)")
(w/'generator-r006.py').write_text(s)
a=json.loads((w/'final-selection.json').read_text());(w/'selection-before-r006.json').write_text(json.dumps(a,indent=2)+'\n')
keep=['brief.json','brief.md','references.json','build-config.json','modeling-freeze.json','premodel-schema-check.json','concept-original.png','concept-prompt.txt','concept-generation.json','build-dependencies.json']
for x in a:
 if x['asset_id'] not in ['dickinsonia','schist-outcrop']:continue
 old=Path(x['path']);new=old.parent/'r006';new.mkdir()
 for n in keep:shutil.copyfile(old/n,new/n)
 (new/'generator.py').write_text(s);d=json.loads((new/'build-dependencies.json').read_text());d['generator_sha256']=hashlib.sha256((new/'generator.py').read_bytes()).hexdigest();(new/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
 (new/'repair-freeze.json').write_text(json.dumps({'revision':'r006','frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_frozen_design_unchanged':True,'reason':('r005 actual8-view top inspection found ridge tone continued into smooth anterior cap, weakening required enlarged undivided anterior region. Make that area physically smoother over a larger original-scope head region and remove ridge tone accents there. Underlying fossil mould ribs remain geometry, not painted substitute. No scope/camera/renderer changes.' if x['asset_id']=='dickinsonia' else 'r005 actual8-view inspection: whole contour too rounded and cylinder-like. Replace rounded contour by irregular angular outcrop profile and unequal crest height while retaining small localized physical foliation fractures. No material/camera/renderer concealment or source scope change.'),'generator_sha256':hashlib.sha256((new/'generator.py').read_bytes()).hexdigest(),'source_revision':x['revision']},indent=2)+'\n');x['revision']='r006';x['path']=str(new)
(w/'final-selection.json').write_text(json.dumps(a,indent=2)+'\n')
