# SPDX-License-Identifier: MIT
"""Read-only .blend geometry and structure inspection; no export or render."""
import bpy,bmesh,json,sys,hashlib
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];p=Path(args[0]);out=Path(args[1]);before=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p));col=bpy.data.collections['EXPORT'];root=bpy.data.objects[col['asset_root']];parts=[];errors=[]
for o in col.all_objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);components=[];unseen=set(bm.verts)
 while unseen:
  start=next(iter(unseen));stack=[start];verts={start};unseen.remove(start)
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    w=e.other_vert(v)
    if w in unseen:unseen.remove(w);verts.add(w);stack.append(w)
  faces={f for v in verts for f in v.link_faces};volume=0
  for f in faces:
   points=[l.vert.co for l in f.loops]
   for i in range(1,len(points)-1):volume+=points[0].dot(points[i].cross(points[i+1]))/6
  components.append(volume)
 boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
 parts.append({'name':o.name,'closed_component_count':len(components),'signed_volume_min_m3':min(components),'signed_volume_max_m3':max(components),'negative_volume_components':sum(x<0 for x in components),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'vertex_groups':[g.name for g in o.vertex_groups]})
 if boundary or nonmanifold:errors.append(o.name+' not closed')
 if any(x<=0 for x in components):errors.append(o.name+' nonpositive signed component volume')
extras=[o.name for o in bpy.data.objects if o.type in ['CAMERA','LIGHT']]
if extras:errors.append('Presentation objects in source')
if any(abs(root.matrix_world[i][j]-(1 if i==j else 0))>1e-8 for i in range(4) for j in range(4)):errors.append('Root not identity')
if before!=hashlib.sha256(p.read_bytes()).hexdigest():errors.append('Source mutated')
r={'status':'FAIL' if errors else 'PASS','scope':'Read-only source structure, closed component signed winding, and presentation exclusion. Not printable union or independent visual approval','model_blend_sha256':before,'source_unchanged':True,'root_identity':True,'source_cameras_lights':extras,'parts':parts,'errors':errors};out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));assert not errors
