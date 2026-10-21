#!/usr/bin/env python3
"""Decode actual scene-space GLB vertices; no nominal/config radii used in measurement."""
import sys,json,math,hashlib,struct,datetime,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,IDENTITY
path=Path(sys.argv[1]);output=Path(sys.argv[2]);doc,blob,data=read_glb(path);pts=[];faces=[];mats=[];lookup={}
def walk(index,parent):
 n=doc['nodes'][index];matrix=matmul(parent,node_matrix(n))
 if 'mesh' in n:
  for pr in doc['meshes'][n['mesh']]['primitives']:
   assert pr.get('mode',4)==4
   material=doc['materials'][pr['material']]['name'];local=[]
   for v in accessor_values(doc,blob,pr['attributes']['POSITION']):
    p=tuple(transform(matrix,v));key=(material,p)
    if key not in lookup:lookup[key]=len(pts);pts.append(p);mats.append(material)
    local.append(lookup[key])
   indices=[x[0] for x in accessor_values(doc,blob,pr['indices'])]
   faces.extend(tuple(local[x] for x in indices[k:k+3]) for k in range(0,len(indices),3))
 for child in n.get('children',[]):walk(child,matrix)
for i in doc['scenes'][doc.get('scene',0)]['nodes']:walk(i,IDENTITY)
adj=[set() for _ in pts]
for f in faces:
 for a,b in zip(f,f[1:]+f[:1]):adj[a].add(b);adj[b].add(a)
unseen=set(range(len(pts)));components=[]
def ulp32(x):
 a=abs(x)
 if a==0:return 2**-149
 return 2**(math.floor(math.log2(a))-23)
while unseen:
 start=min(unseen);component={start};unseen.remove(start);stack=[start]
 while stack:
  for i in adj[stack.pop()]:
   if i in unseen:unseen.remove(i);component.add(i);stack.append(i)
 pp=[pts[i] for i in sorted(component)];lo=[min(v[k] for v in pp) for k in range(3)];hi=[max(v[k] for v in pp) for k in range(3)];c={'component':len(components),'material':mats[start],'vertex_count':len(pp),'bounds_world_glb_m':{'min':lo,'max':hi,'size':[b-a for a,b in zip(lo,hi)]}}
 if mats[start].endswith('-2'):
  cx,cz=(lo[0]+hi[0])/2,(lo[2]+hi[2])/2;rad=[math.hypot(v[0]-cx,v[2]-cz) for v in pp];rings=collections.defaultdict(list)
  for v in pp:rings[v[1]].append([v[0],v[2]])
  assert len(rings)==2 and all(len(v)==12 for v in rings.values())
  rr=list(rings.values());c.update(center_xz_m=[cx,cz],points_world_glb_m=pp,vertex_radii_m=rad,circumradius_min_m=min(rad),circumradius_max_m=max(rad),ring_count=len(rings),radial_segments=len(rr[0]),top_bottom_identical_xz=sorted(rr[0])==sorted(rr[1]),minimum_margin_above_lower_m=min(rad)-.0026,maximum_margin_below_upper_m=.0048-max(rad),all_vertex_radii_in_original_range=min(rad)>=.0026 and max(rad)<=.0048,max_coordinate_float32_ulp_m=max(ulp32(v[k]) for v in pp for k in [0,2]))
 components.append(c)
shafts=[c for c in components if 'circumradius_min_m' in c];assert len(shafts)==7
r={'schema_version':1,'glb_path':str(path),'glb_sha256':hashlib.sha256(data).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Decode POSITION/index data from exact GLB; apply complete active scene graph transforms; exact position weld within material; traverse connected triangles. Each filled shaft has two 12-point horizontal rings, no side midpoint or inradius points. Center is XZ AABB midpoint; all Euclidean distances from center to unique actual ring vertices are measured. Report minimum and maximum vertex circumradius to retain float32 variation. No projection from rendered pixels, no nominal config values, no tolerance in the range comparison.','units':'meters','axes':'glTF +Y up','frozen_shaft_radius_range_m':[.0026,.0048],'shaft_count':len(shafts),'components':components,'all_shafts_within_original_range':all(c['all_vertex_radii_in_original_range'] for c in shafts),'minimum_circumradius_m':min(c['circumradius_min_m'] for c in shafts),'maximum_circumradius_m':max(c['circumradius_max_m'] for c in shafts),'textures':len(doc.get('textures',[]))}
with output.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(json.dumps({k:r[k] for k in ['glb_sha256','shaft_count','minimum_circumradius_m','maximum_circumradius_m','all_shafts_within_original_range']}))
