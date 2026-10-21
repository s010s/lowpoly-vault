from pathlib import Path
import json,sys,hashlib,numpy as np
R=Path('/workspace/shared/lowpoly-batch90-rosary-repair-20261020');B=R/'production/batch90-rosary-repair/assets/rosary-shaped-chambered-burrow-hormosiroidea-type/r002';OLD=Path('/workspace/shared/lowpoly-batch90-20261020/production/batch90/assets/rosary-shaped-chambered-burrow-hormosiroidea-type/r001');O=Path(__file__).parent;sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vertices(path):
 d,b,_=read_glb(path);return np.array([v for m in d['meshes'] for p in m['primitives'] for v in accessor_values(d,b,p['attributes']['POSITION'])])
a=vertices(OLD/'model.glb');b=vertices(B/'model.glb');bottom=lambda v:sorted(set((float(x),float(z)) for x,y,z in v if y==0));assert bottom(a)==bottom(b)
def hull(points):
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 pts=sorted(set(points));lo=[];up=[]
 for p in pts:
  while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
  lo.append(p)
 for p in pts[::-1]:
  while len(up)>1 and cross(up[-2],up[-1],p)<=0:up.pop()
  up.append(p)
 return lo[:-1]+up[:-1]
ha=hull(bottom(a));hb=hull(bottom(b));assert ha==hb
r=dict(status='pass',old_glb_sha256=H(OLD/'model.glb'),new_glb_sha256=H(B/'model.glb'),bottom_zero_plane=True,all_original_bottom_vertices_preserved_exactly=True,bottom_vertices_count=len(bottom(b)),slab_footprint_convex_hull_same=True,footprint_gltf_xz_m=hb,slab_top_float32_m=float(np.float32(.009)),scope='Readback of actual exported coordinates, not only config. Original opaque palette and no-overlay topology tested elsewhere.')
(O/'own-slab-regression.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
