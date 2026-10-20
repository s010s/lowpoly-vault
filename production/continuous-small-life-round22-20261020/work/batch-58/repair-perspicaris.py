# SPDX-License-Identifier: MIT
from pathlib import Path
import json,shutil,datetime,hashlib
R=Path.cwd();W=R/'production/continuous-small-life-round22-20261020/work/batch-58';old=R/'assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r001';b=old.parent/'r002';b.mkdir(exist_ok=True)
for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','dependency-hashes.json']:shutil.copy(old/n,b/n)
d=json.loads((b/'brief.json').read_text());d['brief_version']='r002';d['revision_reason']='Replace clamped radial domes with explicit dorsal-to-ventral valve grid, eliminating visible dorsal holes and preserving straight hinge.';(b/'brief.json').write_text(json.dumps(d,indent=2)+'\n')
d=json.loads((b/'build-config.json').read_text());d['revision']='r002';(b/'build-config.json').write_text(json.dumps(d,indent=2)+'\n')
(b/'modeling-freeze.json').write_text(json.dumps({'asset_id':'perspicaris','revision':'r002','frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repair_scope':'Valve surface topology only. Counts, source, concept and original design scope unchanged. Prior evidence retained.','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in b.iterdir()}},indent=2)+'\n')
s=(old/'generator.py').read_text();a=s.index(' for sign in [-1,1]:',s.index('def perspicaris():'));z=s.index(" tube('straight_dorsal_hinge'",a)
new=''' for sign in [-1,1]:
  nu=25;nv=14;vs=[];fs=[]
  for layer in [0,1]:
   for j in range(nu):
    u=-.985+1.97*j/(nu-1);g=math.sqrt(1-u*u);yy=-.003+.0125*u
    for k in range(nv+1):
     t=k*math.pi/nv;x=sign*(.00045+.0056*g*math.sin(t)-.00030*layer);zz=.0103-.0105*g*(1-math.cos(t))/2;vs.append((x,yy,zz))
  stride=nv+1;offset=nu*stride
  for layer in [0,1]:
   b=layer*offset
   for j in range(nu-1):
    for k in range(nv):
     a=b+j*stride+k;c=a+stride;f=(a,c,c+1,a+1);fs.append(f if layer==0 else tuple(reversed(f)))
  boundary=list(range(stride))+[j*stride+nv for j in range(1,nu)]+[(nu-1)*stride+k for k in range(nv-1,-1,-1)]+[j*stride for j in range(nu-2,0,-1)]
  for j,a in enumerate(boundary):q=boundary[(j+1)%len(boundary)];fs.append((a,q,q+offset,a+offset))
  part('left_suboval_carapace_valve' if sign<0 else 'right_suboval_carapace_valve',vs,fs,'shell')
'''
s=s[:a]+new+s[z:];(b/'generator.py').write_text(s)
x=json.loads((W/'final-selection.json').read_text())
for a in x:
 if a['asset_id']=='perspicaris':a.update(revision='r002',path=str(b.relative_to(R)))
(W/'final-selection.json').write_text(json.dumps(x,indent=2)+'\n')
