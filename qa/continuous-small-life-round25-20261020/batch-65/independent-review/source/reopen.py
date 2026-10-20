import bpy, bmesh, json, sys, os
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
blend_path, out_path=args[:2]
bpy.ops.wm.open_mainfile(filepath=blend_path)
meshes=[]; allpoints=[]; total_triangles=0; total_volume=0.0
for ob in sorted([o for o in bpy.data.objects if o.type=='MESH'],key=lambda o:o.name):
    deps=bpy.context.evaluated_depsgraph_get(); eo=ob.evaluated_get(deps); me=eo.to_mesh()
    bm=bmesh.new(); bm.from_mesh(me)
    bounds=[eo.matrix_world @ v.co for v in me.vertices]
    allpoints += bounds
    tris=sum(max(0,len(p.vertices)-2) for p in me.polygons)
    vol=abs(bm.calc_volume(signed=True)) if len(bm.faces) else 0.0
    boundary=sum(1 for e in bm.edges if e.is_boundary)
    nonmanifold=sum(1 for e in bm.edges if not e.is_manifold)
    total_triangles+=tris; total_volume+=vol
    meshes.append({'name':ob.name,'authored_vertices':len(ob.data.vertices),'evaluated_vertices':len(me.vertices),'authored_polygons':len(ob.data.polygons),'evaluated_polygons':len(me.polygons),'triangles':tris,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'closed_solid_volume_m3':vol,'bounds_min_xyz':list(map(float,[min(p[i] for p in bounds) for i in range(3)])),'bounds_max_xyz':list(map(float,[max(p[i] for p in bounds) for i in range(3)])),'modifiers':[{'name':m.name,'type':m.type} for m in ob.modifiers]})
    bm.free(); eo.to_mesh_clear()
if allpoints:
    lo=[min(p[i] for p in allpoints) for i in range(3)]; hi=[max(p[i] for p in allpoints) for i in range(3)]
else: lo=hi=[0.,0.,0.]
r={'blend_path':blend_path,'blender_version':bpy.app.version_string,'scene_objects':len(bpy.data.objects),'mesh_objects':len(meshes),'parts':meshes,'totals':{'triangles':total_triangles,'closed_solid_volume_sum_m3':total_volume,'bounds_min_xyz':lo,'bounds_max_xyz':hi,'bounds_size_xyz':[hi[i]-lo[i] for i in range(3)]},'status':'pass' if meshes and all(x['boundary_edges']==0 and x['nonmanifold_edges']==0 and x['closed_solid_volume_m3']>0 for x in meshes) else 'fail','read_only':True}
open(out_path,'w').write(json.dumps(r,indent=2)+'\n')
print(json.dumps({'file':blend_path,'objects':len(meshes),'tris':total_triangles,'volume_sum':total_volume,'size':r['totals']['bounds_size_xyz'],'status':r['status']}))
