# SPDX-License-Identifier: MIT
from pathlib import Path
import json,shutil,hashlib,datetime
w=Path('production/small-life-batch79');s=(w/'generator-r004.py').read_text()
s=s.replace("y=yb+.006*u*u*v+.00055*math.tanh(x/.002)","y=yb+.006*u*u*v*(1-v*v)+.00055*math.tanh(x/.002)*(1-v*v)")
s=s.replace("for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('fossil')","for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('fossil' if j%4 in [0,1] else 'matrix')",1)
s=s.replace("xx=x+rng.uniform(-.085,.085)*math.sin(math.pi*i/nx);yy=y+rng.uniform(-.12,.12)*math.sin(math.pi*j/ny)","xx=x+rng.uniform(-.085,.085)*math.sin(math.pi*i/nx)+.22*math.sin(y*.53+.4)*abs(x/7)**8;yy=y+rng.uniform(-.12,.12)*math.sin(math.pi*j/ny)+.20*math.sin(x*.72+.9)*abs(y/11)**8")
s=s.replace("endtaper=.70+.30*math.sin(math.pi*(u+1.6)/3.2)**.45","endtaper=.45+.55*math.sin(math.pi*(u+1.6)/3.2)**.34")
s=s.replace("shape=endtaper*(1+.065*math.sin(t*3+layer*1.79)+.025*math.sin(t*7+layer*.7))","shape=endtaper*(1+.10*math.sin(t*3+u*1.2)+.014*math.sin(t*7+layer*.7))")
s=s.replace("ledge=(.035+.045*(.5+.5*math.sin(layer*2.3+t*.7)))*flange","ledge=(.008+.022*(.5+.5*math.sin(layer*2.3+t*.7)))*flange*max(0,math.sin(t*2.7+layer*1.3))**2")
s=s.replace("x=u-.22*(z-.99)+.035*math.sin(z*3.8)","x=u-.22*(z-.99)+.060*math.sin(z*3.8+u*.2)")
s=s.replace("u+.035*math.sin(.99*3.8)","u+.060*math.sin(.99*3.8+u*.2)")
(w/'generator-r005.py').write_text(s)
a=json.loads((w/'final-selection.json').read_text());(w/'selection-before-r005.json').write_text(json.dumps(a,indent=2)+'\n')
keep=['brief.json','brief.md','references.json','build-config.json','modeling-freeze.json','premodel-schema-check.json','concept-original.png','concept-prompt.txt','concept-generation.json','build-dependencies.json']
for x in a:
 if x['asset_id']=='shield-volcano':continue
 old=Path(x['path']);new=old.parent/'r005';new.mkdir()
 for n in keep:shutil.copyfile(old/n,new/n)
 (new/'generator.py').write_text(s);d=json.loads((new/'build-dependencies.json').read_text());d['generator_sha256']=hashlib.sha256((new/'generator.py').read_bytes()).hexdigest();(new/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
 reasons={'dickinsonia':'Retain actual rib-aligned relief topology; taper end curvature to remove lobed tip anomaly, use existing muted sandstone palette to clarify ridge-versus-trough surfaces. No hidden overlap or regularity masked; actual ribs and central seam already present. Original35 simplified ribs and mould scope unchanged.','arroyo-wash':'Original freeze required less rectangular footprint. Add geometric uneven outer terrain margins, retaining exact shallow dry incision and seeded irregular ground relief. No camera/material changes.','schist-outcrop':'r0048-view geometry looked like a whole-ring wafer stack. Reduce full-ring discontinuities, use spatially localized unequal fracture ledges and smoothly varying coherent large outcrop contour with tapered broken ends. Preserve actual steep wavy foliation, no concealment by material or camera.'}
 (new/'repair-freeze.json').write_text(json.dumps({'revision':'r005','frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_frozen_design_unchanged':True,'reason':reasons[x['asset_id']],'generator_sha256':hashlib.sha256((new/'generator.py').read_bytes()).hexdigest(),'source_revision':x['revision']},indent=2)+'\n');x['revision']='r005';x['path']=str(new)
(w/'final-selection.json').write_text(json.dumps(a,indent=2)+'\n')
