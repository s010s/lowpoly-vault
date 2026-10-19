# SPDX-License-Identifier: MIT
"""Two minimal geometry-only trials derived from frozen original editable sources.
blender -b -t 2 --python experiments/cross-type-calibration-20261019/build.py
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
sys.path.insert(0,str(ROOT/'scripts'));from asset_common import export_asset
sources={'conglomerate-outcrop':ROOT/'assets/additions/conglomerate-outcrop/small-life-round08-20261018/conglomerate-outcrop.blend','horsetail-cluster':ROOT/'assets/prehistoric/plants/horsetail-cluster/horsetail-cluster.blend'}
def components(mesh):
 adj=[set() for v in mesh.vertices]
 for e in mesh.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 seen=set();out=[]
 for i in range(len(adj)):
  if i in seen:continue
  seen.add(i);stack=[i];ids=[]
  while stack:
   a=stack.pop();ids.append(a)
   for b in adj[a]:
    if b not in seen:seen.add(b);stack.append(b)
  out.append(sorted(ids))
 return out
logs={}
for slug,path in sources.items():
 bpy.ops.wm.open_mainfile(filepath=str(path));c=bpy.data.collections['EXPORT'];edits=[]
 if slug=='conglomerate-outcrop':
  o=next(o for o in c.all_objects if o.type=='MESH' and 'rounded clasts' in o.name)
  matrix=next(o for o in c.all_objects if o.type=='MESH' and 'continuous finer' in o.name)
  verts=[matrix.matrix_world@v.co for v in matrix.data.vertices];faces=[tuple(p.vertices) for p in matrix.data.polygons];tree=BVHTree.FromPolygons(verts,faces)
  choices=[]
  for idx,ids in enumerate(components(o.data)):
   pts=[o.matrix_world@o.data.vertices[i].co for i in ids];ctr=sum(pts,Vector())/len(pts)
   if ctr.y<-.09:continue # Preserve the entire original exposed teaching fracture.
   hit,n,_,_=tree.find_nearest(ctr);rad=max((p-ctr).length for p in pts)
   exposed=max((p-hit).dot(n) for p in pts)
   choices.append((exposed/rad,idx,ids,ctr,rad,n))
  selected=[]
  for item in sorted(choices,key=lambda q:(-q[0],q[1])):
   if all((item[3]-q[3]).length>.11 for q in selected):selected.append(item)
   if len(selected)==6:break
  assert len(selected)==6
  inv=o.matrix_world.inverted()
  for j,(_,idx,ids,ctr,rad,n) in enumerate(selected):
   sink=rad*[.30,.16,.35,.24,.18,.28][j];scale=[.92,1,.83,1,.95,1][j]
   for i in ids:
    old=o.matrix_world@o.data.vertices[i].co;o.data.vertices[i].co=inv@(ctr+(old-ctr)*scale-n*sink)
   edits.append({'component':idx,'center_before_m':list(ctr),'vertex_count':len(ids),'sink_m':sink,'size_factor':scale,'surface_normal':list(n)})
  category='geology';purpose='optional exposure-depth trial, original matrix and fracture unchanged'
 else:
  o=next(o for o in c.all_objects if o.type=='MESH' and 'Lower open whorls' in o.name)
  choices=[]
  for idx,ids in enumerate(components(o.data)):
   assert len(ids)==9,'Expected original 3-ring triangular branch loft'
   pts=[o.data.vertices[i].co.copy() for i in ids];base=sum(pts[:3],Vector())/3;tip=sum(pts[-3:],Vector())/3
   choices.append((-(tip.y-base.y),idx,ids,base,tip))
  selected=[];used=[]
  for item in sorted(choices,key=lambda q:(-q[0],q[1])):
   b=item[3]
   if any(math.hypot(b.x-v.x,b.y-v.y)<.08 for v in used):continue
   selected.append(item);used.append(b)
   if len(selected)==3:break
  assert len(selected)==3
  for j,(_,idx,ids,base,tip) in enumerate(selected):
   scale=[.88,1.08,.94][j];angle=math.radians([-8,6,10][j]);dz=[-.008,.005,.008][j]
   for k,i in enumerate(ids):
    t=(k//3)/2;v=o.data.vertices[i].co.copy()-base
    o.data.vertices[i].co=base+(Matrix.Rotation(angle*t,3,'Z')@v)*(1+(scale-1)*t)+Vector((0,0,dz*t*t))
   edits.append({'component':idx,'root_unchanged_m':list(base),'tip_before_m':list(tip),'tip_length_factor':scale,'tip_azimuth_delta_deg':[-8,6,10][j],'tip_z_delta_m':dz,'vertex_count':len(ids)})
  category='plants';purpose='retained control with only three branch-tip pose changes; not a defect correction'
 logs[slug]={'source_blend':str(path.relative_to(ROOT)),'source_blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'purpose':purpose,'edits':edits,'textures_added':0,'topology_added':0}
 export_asset(slug,{'en':slug+' minimal comparison trial','zh':('砾岩局部嵌入试验' if category=='geology' else '木贼三枝梢对照试验')},category,c,output_root=H/'candidates',render=False,max_triangles=14000,max_materials=6,max_primitives=30,metadata={'generator':'../../build.py','description':{'en':purpose,'zh':'仅供现状与最小改动对比；不改变原资产，不声称严格科学或特定物种复原。'},'candidate_status':'pending user comparison; no production approval','maker':'GPT-6.1 Sol medium','source_commit':'de413ef720463a2999516faf92c606bcdf9ab1b7','reference_actual_pixels':'three supplied photographs viewed, consulted only; no photo texture used','surface_profile':'inherited palette-only geometry; zero new textures'})
(H/'modifications.json').write_text(json.dumps(logs,indent=2))
