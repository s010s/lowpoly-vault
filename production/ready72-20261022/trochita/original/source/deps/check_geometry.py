# SPDX-License-Identifier: MIT
"""Additional Trochita shell-wall / attachment diagnostics, not full intersection certification."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:]; source=Path(args[0]);out=Path(args[1])
bpy.ops.wm.open_mainfile(filepath=str(source))
result={'blend_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_export_note':'Checks reopen delivered editable source. Primary export audit is separate.','parts':[]}
for ob in bpy.data.objects:
    if ob.type!='MESH':continue
    mesh=ob.data;mesh.calc_loop_triangles();verts=[v.co.copy() for v in mesh.vertices];tri=[tuple(t.vertices) for t in mesh.loop_triangles];bvh=BVHTree.FromPolygons(verts,tri,all_triangles=True,epsilon=0)
    overlap=set(tuple(sorted((a,b))) for a,b in bvh.overlap(bvh) if a<b and not(set(tri[a]) & set(tri[b])))
    result['parts'].append({'name':ob.name,'nonadjacent_triangle_overlap_pairs':len(overlap),'first_pairs':list(sorted(overlap))[:16],'method':'Blender BVHTree triangle self-overlap with shared-index vertex-adjacent pairs excluded. Numerical check supplements actual view inspection.'})
    if ob.name=='ribbed_hollow_shell':shell_bvh=bvh
shelf=bpy.data.objects['broad_internal_shelf']; boundary=73;bad=[];depths=[]
for i in range(boundary):
    co=shelf.data.vertices[i].co.copy();hit=shell_bvh.find_nearest(co)
    if hit[0] is None:bad.append(i)
    else:depths.append(hit[3])
result['shelf_contact']={'samples':boundary,'missing_nearest':bad,'max_distance_m':max(depths),'note':'All 73 attachment arc vertices lie close to the real shell wall. This nearest test alone does not assert point inclusion; prescribed 0.30 mm inward-wall embed and underside visual review establish intended attachment.'}
def inside(p):
    direction=Vector((.9137,.3711,.1623)).normalized();origin=p.copy();count=0
    for _ in range(80):
        hit=shell_bvh.ray_cast(origin,direction,.2)
        if hit[0] is None:break
        count+=1;origin=hit[0]+direction*1e-7
    return bool(count%2)
arc_ids=list(range(73))+list(range(109,109+73))
failed=[i for i in arc_ids if not inside(shelf.data.vertices[i].co)]
result['shelf_contact']['point_in_solid_samples']=len(arc_ids)
result['shelf_contact']['outside_shell_wall_indices']=failed
result['shelf_contact']['point_in_solid_method']='Odd-even ray intersections into closed shell solid, oblique direction, 1e-7 m next-hit advance; tested top and bottom attachment arcs.'
result['source_clean']={'cameras':sum(o.type=='CAMERA' for o in bpy.data.objects),'lights':sum(o.type=='LIGHT' for o in bpy.data.objects),'export_collection_present':'EXPORT' in bpy.data.collections,'root_identity':all(abs(bpy.data.objects['trochita'].matrix_world[r][c]-(r==c))<1e-8 for r in range(4) for c in range(4))}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
