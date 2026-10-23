# SPDX-License-Identifier: MIT
"""Read-only geometric/source audit, not a scientific or visual acceptance test."""
import hashlib,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils.bvhtree import BVHTree
argv=sys.argv[sys.argv.index('--')+1:]; path=Path(argv[0]); out=Path(argv[1])
bpy.ops.wm.open_mainfile(filepath=str(path))
report={'blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'python_version':sys.version,'objects':[],'source_contains_presentation_objects':False,'claim_scope':'Source topology, root, orientation and triangle-BVH overlap checks only. No anatomy, beauty, printability or GPU claim.'}
for obj in bpy.data.objects:
 d={'name':obj.name,'type':obj.type,'matrix_world':[[float(x) for x in row] for row in obj.matrix_world]}
 if obj.type in ['CAMERA','LIGHT']: report['source_contains_presentation_objects']=True
 if obj.type=='MESH':
  me=obj.data; me.calc_loop_triangles(); coords=[v.co.copy() for v in me.vertices]; ts=[tuple(t.vertices) for t in me.loop_triangles]
  tree=BVHTree.FromPolygons(coords,ts,all_triangles=True,epsilon=0.0)
  overlaps=set(tuple(sorted(pair)) for pair in tree.overlap(tree) if pair[0]!=pair[1] and not set(ts[pair[0]])&set(ts[pair[1]]))
  bm=bmesh.new(); bm.from_mesh(me)
  d.update(vertices=len(me.vertices),triangles=len(ts),boundary_edges=sum(e.is_boundary for e in bm.edges),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),signed_volume_m3=bm.calc_volume(signed=True),nonadjacent_bvh_overlap_pairs=len(overlaps),overlap_examples=list(overlaps)[:12],vertex_groups=[x.name for x in obj.vertex_groups],modifiers=[m.name for m in obj.modifiers]); bm.free()
  d['bvh_method']='Exact float triangle BVH overlap, excluding pairs sharing any original source vertex. Absence supports no self-crossing; not a formal solid-boolean proof.'
 report['objects'].append(d)
report['status']='PASS' if not report['source_contains_presentation_objects'] and all(not d.get('boundary_edges',0) and not d.get('nonmanifold_edges',0) and not d.get('nonadjacent_bvh_overlap_pairs',0) for d in report['objects']) else 'REVIEW'
out.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
