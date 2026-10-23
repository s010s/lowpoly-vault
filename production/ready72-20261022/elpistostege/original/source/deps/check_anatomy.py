# SPDX-License-Identifier: MIT
"""Exact design-space geometric checks; no species/CT accuracy certification."""
import ast,itertools,json,math,hashlib,sys
from pathlib import Path
root=Path(sys.argv[1]);tree=ast.parse((root/'source/generate.py').read_text());v={}
for n in tree.body:
 if isinstance(n,ast.Assign):
  for t in n.targets:
   if isinstance(t,ast.Name) and t.id in ['bones','finpoly']:v[t.id]=ast.literal_eval(n.value)
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def point_seg(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1]; t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
 return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def edges(p):return list(zip(p,p[1:]+p[:1]))
def inside(p,poly):
 if min(point_seg(p,a,b) for a,b in edges(poly))<1e-10:return True
 x,y=p; val=False
 for (x1,y1),(x2,y2) in edges(poly):
  if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1:val=not val
 return val
def distance(p,q):
 if any(inside(x,q) for x in p) or any(inside(x,p) for x in q):return 0
 out=1e9
 for a,b in edges(p):
  for c,d in edges(q):
   if cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0:return 0
   out=min(out,point_seg(a,c,d),point_seg(b,c,d),point_seg(c,a,b),point_seg(d,a,b))
 return out
bad=[];pairs=[]
for name,g,poly in v['bones']:
 for i,p in enumerate(poly):
  if not inside(p,v['finpoly']):bad.append({'bone':name,'vertex':i,'uv':p})
for a,b in itertools.combinations(v['bones'],2):pairs.append({'a':a[0],'b':b[0],'distance_m':distance([(u+.35*v,v) for u,v in a[2]],[(u+.35*v,v) for u,v in b[2]])})
small=sorted(pairs,key=lambda x:x['distance_m'])[:12]
out={'scope':'Design polygon containment and true planar separation, not scientific fidelity','glb_sha256':hashlib.sha256((root/'model.glb').read_bytes()).hexdigest(),'bone_count':len(v['bones']),'outside_fin_vertices':bad,'minimum_bone_gap_m':small[0]['distance_m'],'closest_bone_pairs':small,'status':'PASS' if not bad and small[0]['distance_m']>0 else 'FAIL'}
print(json.dumps(out,indent=2))
(root/'qa/evidence/anatomy-geometry.json').write_text(json.dumps(out,indent=2)+'\n')
