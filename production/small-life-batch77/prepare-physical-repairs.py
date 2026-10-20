from pathlib import Path
import json,shutil,datetime,hashlib
W=Path('production/small-life-batch77');f=json.loads((W/'final-selection.json').read_text());(W/'selection-before-physical-repairs.json').write_text((W/'final-selection.json').read_text())
for slug,oldrev,newrev,note in [('loess-bluff','r003','r004','r003 BVH18 overlaps. r004 aligns joint incision into crest/roof so face cannot fold through roof, and uses a gently bowed end boundary plus proper concave bottom cap rather than invalid fan.'),('slump-folded-bed','r002','r003','r002 BVH3 overlaps where nonplanar fan cap crossed upper wall. r003 constructs constrained triangulated full roof with interior elevations and shared rim; unchanged fold/bounding-strata scope.')]:
 old=W/'assets'/slug/oldrev;b=old.parent/newrev;b.mkdir()
 for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json','build-dependencies.json']:shutil.copyfile(old/n,b/n)
 (b/'repair-freeze.json').write_text(json.dumps({'asset_id':slug,'revision':newrev,'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':note,'prior_failure_generator_sha256':hashlib.sha256((old/'generator.py').read_bytes()).hexdigest(),'unchanged_original_freeze_sha256':hashlib.sha256((old.parent/'r001/modeling-freeze.json').read_bytes()).hexdigest(),'geometry_authorship_next':True,'validator_renderer_material_scope_unchanged':True},indent=2)+'\n')
 s=(old/'generator.py').read_text()
 if slug=='loess-bluff':
  s=s.replace("center=len(vs);vs.append((sum(vs[b+i][0] for i in range(len(boundary)))/len(boundary),sum(vs[b+i][1] for i in range(len(boundary)))/len(boundary),0))\n for i in range(len(boundary)):fs.append((center,b+i,b+(i+1)%len(boundary)));ms.append(mat)\n return multi(name,vs,fs,ms)","fs.append(tuple(b+i for i in range(len(boundary)-1,-1,-1)));ms.append(mat);return multi(name,vs,fs,ms)")
  s=s.replace('yy=y+(g*(1.05 if 3<j<9 else .3) if front else .1*math.sin(x*.7+j))','factor=.3 if j<3 else 1.05 if j<=10 else .6 if j==11 else .3 if j==12 else 0\n   yy=y+g*factor')
  s=s.replace('xx=x+.065*math.sin(j*1.6+i*.7)*edge','xx=x+.065*math.sin(j*1.6+i*.7)*edge+math.copysign(.06*math.sin(math.pi*j/ny),x)*abs(x/8)**20')
 else:
  s=s.replace("o=(len(records)-1)*n;cap=len(vs);vs.append((0,0,4.05))\n for i in range(n):fs.append((cap,o+i,o+(i+1)%n));ms.append('earth')",'''o=(len(records)-1)*n
 from mathutils.geometry import delaunay_2d_cdt
 from mathutils import Vector
 pts=[Vector((vs[o+i][0],vs[o+i][1])) for i in range(n)]
 for jy in range(1,9):
  for ix in range(1,25):pts.append(Vector((-3.5+7*ix/25,-1+2*jy/9)))
 pv,pe,pf,orig,_,_=delaunay_2d_cdt(pts,[(i,(i+1)%n) for i in range(n)],[],1,1e-6)
 mapping={}
 for k,p in enumerate(pv):
  oldids=[a for a in orig[k] if a<n]
  if oldids:mapping[k]=o+oldids[0]
  else:
   mapping[k]=len(vs);vs.append((p.x,p.y,4+(.14*math.sin(p.x*2.3+p.y*.8)+.08*math.sin(p.x*4.2+.3))+.025*math.sin(p.x*5.1+p.y*7.3)))
 for f in pf:fs.append(tuple(mapping[k] for k in f));ms.append('earth')''')
 (b/'generator.py').write_text(s)
 for x in f:
  if x['asset_id']==slug:x['revision']=newrev;x['path']=str(b)
(W/'final-selection.json').write_text(json.dumps(f,indent=2)+'\n')
