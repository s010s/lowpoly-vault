# SPDX-License-Identifier: MIT
"""Independent technical inspection of the saved source, not artistic approval."""
import bpy,bmesh,hashlib,json,sys
from pathlib import Path
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:]; root=Path(args[0])
bpy.ops.wm.open_mainfile(filepath=str(root/'model.blend'))
objects=list(bpy.data.objects)
assert not any(ob.type in {'LIGHT','CAMERA'} for ob in objects)
ob=next(ob for ob in objects if ob.type=='MESH'); mesh=ob.data; mesh.calc_loop_triangles()
vertices=[v.co.copy() for v in mesh.vertices]; triangles=[tuple(t.vertices) for t in mesh.loop_triangles]
bvh=BVHTree.FromPolygons(vertices,triangles,all_triangles=True,epsilon=0)
pairs=[(a,b) for a,b in bvh.overlap(bvh) if a<b and not set(triangles[a])&set(triangles[b])]
bm=bmesh.new(); bm.from_mesh(mesh)
components=0; seen=set()
for vertex in bm.verts:
    if vertex in seen: continue
    components+=1; stack=[vertex]; seen.add(vertex)
    while stack:
        v=stack.pop()
        for e in v.link_edges:
            n=e.other_vert(v)
            if n not in seen: seen.add(n); stack.append(n)
report={'status':'pass' if not pairs else 'needs_review','glb_sha256':hashlib.sha256((root/'model.glb').read_bytes()).hexdigest(),
        'blend_sha256':hashlib.sha256((root/'model.blend').read_bytes()).hexdigest(),'objects':[{'name':x.name,'type':x.type} for x in objects],
        'preview_helpers_in_source':False,'mesh_components':components,'boundary_edges':sum(e.is_boundary for e in bm.edges),
        'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'nonadjacent_BVH_overlap_pairs':len(pairs),
        'overlap_examples':[list(pair) for pair in pairs[:30]],
        'method':'Blender BVHTree triangle overlap with shared-vertex pairs excluded. A practical intersection screen, not a general proof of printability.'}
bm.free(); (root/'qa/evidence/source-inspection.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report))
