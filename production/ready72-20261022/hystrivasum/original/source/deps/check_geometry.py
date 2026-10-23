# SPDX-License-Identifier: MIT
"""Source topology / non-adjacent triangle intersection checks, not visual approval."""
from pathlib import Path
import sys,json,hashlib,bpy,bmesh
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:]
source=Path(args[0]);output=Path(args[1])
bpy.ops.wm.open_mainfile(filepath=str(source))
meshes=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH']
reports=[]
for ob in meshes:
    m=ob.data;m.calc_loop_triangles();v=[ob.matrix_world@p.co for p in m.vertices];t=[tuple(x.vertices) for x in m.loop_triangles]
    tree=BVHTree.FromPolygons(v,t,all_triangles=True,epsilon=0)
    pairs=set((min(a,b),max(a,b)) for a,b in tree.overlap(tree) if a!=b and not (set(t[a])&set(t[b])))
    bm=bmesh.new();bm.from_mesh(m)
    vol=bm.calc_volume(signed=True)
    boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges)
    bm.free()
    reports.append({'object':ob.name,'vertices':len(v),'triangles':len(t),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'signed_volume_m3':vol,'nonadjacent_triangle_overlap_count':len(pairs),'overlap_examples':[list(p) for p in sorted(pairs)[:30]],'vertex_groups':[x.name for x in ob.vertex_groups]})
result={'source_blend_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Blender BVHTree non-adjacent triangle overlap plus bmesh source topology/signed volume; epsilon zero. Shared-vertex triangle pairs excluded. Positive volume is not proof of local outward normals.','parts':reports,'status':'PASS' if all(x['nonadjacent_triangle_overlap_count']==0 and x['nonmanifold_edges']==0 and x['signed_volume_m3']>0 for x in reports) else 'REVIEW_REQUIRED','scope':'Geometric checks only; no scientific or artistic acceptance.'}
output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
