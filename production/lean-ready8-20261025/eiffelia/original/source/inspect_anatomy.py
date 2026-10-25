# SPDX-License-Identifier: MIT
"""Read-only reopened source checks for bounded Eiffelia assembly obligations."""
import sys,json,hashlib,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[sys.argv.index('--')+1]);blend=Path(bpy.data.filepath)
body=bpy.data.objects['continuous-hollow-sac-open-osculum'];bm=bmesh.new();bm.from_mesh(body.data)
boundary=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
assert boundary==0 and volume>0
bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
hits=[]
for x,y in [(0,0),(.001,0),(-.001,0),(0,.001),(0,-.001)]:
    hit,normal,index,dist=bvh.ray_cast(Vector((x,y,.05)),Vector((0,0,-1)),.06)
    assert hit is not None and hit.z<.006, (x,y,hit)
    hits.append({'xy_m':[x,y],'first_downward_hit_z_m':hit.z,'depth_below_rim_m':.0301-hit.z})
verts=[v.co.copy() for v in body.data.vertices[:body['outer_vertex_count']]]
diameter=max(math.hypot(p.x-q.x,p.y-q.y) for i,p in enumerate(verts) for q in verts[:i])
assert abs(diameter-.031)<1e-8
groups=[]
for ob in bpy.context.scene.objects:
    if ob.type!='MESH' or ob==body:continue
    adj={i:set() for i in range(len(ob.data.vertices))}
    for e in ob.data.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
    unseen=set(adj);components=[]
    while unseen:
        start=next(iter(unseen));stack=[start];component=set()
        while stack:
            q=stack.pop()
            if q in component:continue
            component.add(q);stack.extend(adj[q]-component)
        unseen-=component;components.append(component)
    b=bmesh.new();b.from_mesh(ob.data);nonmanifold=sum(not e.is_manifold for e in b.edges);vol=b.calc_volume(signed=True);b.free()
    assert nonmanifold==0 and vol>0
    attached=0;component_records=[]
    for comp in components:
        signed=[]
        for vi in comp:
            p=ob.matrix_world@ob.data.vertices[vi].co;hit,normal,index,distance=bvh.find_nearest(p)
            signed.append((p-hit).dot(normal))
        # A meaningful part of every closed star embeds into body material.
        inner=sum(x<-.00002 for x in signed);outer=sum(x>.00002 for x in signed)
        assert inner>=4 and outer>=1,(ob.name,inner,outer)
        attached+=1;component_records.append({'vertices':len(comp),'embedded_vertex_count':inner,'exposed_vertex_count':outer,'signed_distance_min_m':min(signed),'signed_distance_max_m':max(signed)})
    groups.append({'name':ob.name,'closed_stars':len(components),'all_stars_embedded':attached==len(components),'nonmanifold_edges':nonmanifold,'signed_volume_m3':vol,'components':component_records})
assert [g['closed_stars'] for g in sorted(groups,key=lambda g:g['name'])]==[35,27,58]
out.write_text(json.dumps({'status':'PASS_SCOPED_GEOMETRY','blend_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(blend.with_suffix('.glb').read_bytes()).hexdigest(),'source_reopened':True,'body_connected_material_wall':True,'body_nonmanifold_edges':boundary,'body_signed_volume_m3':volume,'measured_transverse_body_diameter_m':diameter,'osculum_axis_ray_tests':hits,'basal_min_z_m':min(v.co.z for v in body.data.vertices),'spicule_groups':groups,'limits':'Topology/attachment/cavity evidence only. Scientific accuracy, visual craft, GPU, scene coexistence and publication are not established. Stars use embedded overlap, not a Boolean union; small external ray tips can be at the outer surface.'},indent=2)+'\n')
