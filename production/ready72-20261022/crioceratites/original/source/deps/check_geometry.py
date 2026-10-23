# SPDX-License-Identifier: MIT
"""Inspect saved editable source topology. This is not an independent review."""
import bpy,bmesh,json,sys,hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
r=Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(r/'model.blend'))
col=bpy.data.collections['EXPORT'];objs=[x for x in col.all_objects if x.type=='MESH'];assert len(objs)==1
m=objs[0].data;bm=bmesh.new();bm.from_mesh(m);bm.verts.ensure_lookup_table()
remaining=set(bm.verts);components=0
while remaining:
 components+=1;todo=[remaining.pop()]
 while todo:
  v=todo.pop()
  for e in v.link_edges:
   w=e.other_vert(v)
   if w in remaining:remaining.remove(w);todo.append(w)
boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True)
m.calc_loop_triangles();tri=[tuple(t.vertices) for t in m.loop_triangles];vertices=[tuple(v.co) for v in m.vertices]
bvh=BVHTree.FromPolygons(vertices,tri,all_triangles=True,epsilon=1e-10)
pairs=sorted(set(tuple(sorted((a,b))) for a,b in bvh.overlap(bvh) if a!=b and not (set(tri[a])&set(tri[b]))))
rpt={'status':'PASS' if components==1 and boundary==0 and nonmanifold==0 and volume>0 and not pairs else 'FAIL','claim_scope':'Saved source geometry topology check, not identity or visual acceptance','glb_sha256':hashlib.sha256((r/'model.glb').read_bytes()).hexdigest(),'blend_sha256':hashlib.sha256((r/'model.blend').read_bytes()).hexdigest(),'source_meshes':len(objs),'connected_components':components,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'signed_volume_m3':volume,'nonadjacent_triangle_overlap_pairs':len(pairs),'example_overlap_pairs':pairs[:10],'overlap_method':'Blender BVH source triangulation, exclude triangles sharing vertices; epsilon 1e-10 m','normals_method':'Positive signed source volume, manifold topology and exact-GLB view inspection; not a proof of every local normal','preview_objects_in_source':[o.name for o in bpy.context.scene.objects if o.type not in ('MESH','EMPTY')]}
(r/'qa/evidence/geometry.json').write_text(json.dumps(rpt,indent=2)+'\n');print(json.dumps(rpt));bm.free()
if rpt['status']!='PASS':raise RuntimeError('Geometry audit failed')
