import bpy, sys, os, json, hashlib, bmesh, math, traceback
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
opts={}
for i in range(0,len(args),2): opts[args[i].lstrip('-')]=args[i+1]
asset=opts['asset']; revision=opts['revision']; output=opts['output']; glb=opts['glb']
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
if not meshes: raise RuntimeError('No mesh objects in reopened .blend')
dg=bpy.context.evaluated_depsgraph_get()
minv=[math.inf]*3; maxv=[-math.inf]*3; parts=[]; total_v=0; total_poly=0; total_tri=0; boundary=0; nonmanifold=0
allmats=set()
for obj in meshes:
    ev=obj.evaluated_get(dg); me=ev.to_mesh(); me.calc_loop_triangles()
    bm=bmesh.new(); bm.from_mesh(me)
    nb=sum(1 for e in bm.edges if e.is_boundary)
    nm=sum(1 for e in bm.edges if (not e.is_manifold and not e.is_boundary))
    for v in me.vertices:
        world=obj.matrix_world @ v.co
        for ax in range(3): minv[ax]=min(minv[ax],world[ax]); maxv[ax]=max(maxv[ax],world[ax])
    matnames=[]
    for slot in obj.material_slots:
        if slot.material:
            allmats.add(slot.material.name); matnames.append(slot.material.name)
    row={'name':obj.name,'authored_vertices':len(obj.data.vertices),'evaluated_vertices':len(me.vertices),'authored_polygons':len(obj.data.polygons),'evaluated_polygons':len(me.polygons),'triangles':len(me.loop_triangles),'boundary_edges':nb,'nonmanifold_edges':nm,'materials':matnames}
    parts.append(row); total_v+=len(me.vertices); total_poly+=len(me.polygons); total_tri+=len(me.loop_triangles); boundary+=nb; nonmanifold+=nm
    ev.to_mesh_clear(); bm.free()
# Export only the saved project mesh objects, with the frozen deliverable GLB settings.
export_collection=bpy.data.collections.get('EXPORT')
selected_objects=list(export_collection.all_objects) if export_collection else list(bpy.context.scene.objects)
bpy.ops.object.select_all(action='DESELECT')
for obj in selected_objects: obj.select_set(True)
bpy.context.view_layer.objects.active=meshes[0]
os.makedirs(os.path.dirname(output),exist_ok=True)
result=bpy.ops.export_scene.gltf(filepath=output,export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
if 'FINISHED' not in result: raise RuntimeError('GLB export did not finish: '+str(result))
h=hashlib.sha256(open(output,'rb').read()).hexdigest(); n=os.path.getsize(output)
report={'asset_id':asset,'revision':revision,'opened_source_blend':bpy.data.filepath,'blender_version':bpy.app.version_string,'threads':bpy.context.scene.render.threads if bpy.context.scene.render.threads_mode=='FIXED' else 'system/default','mesh_objects':len(meshes),'selected_export_objects':[obj.name for obj in selected_objects],'source_counts':{'authored_vertices':sum(len(o.data.vertices) for o in meshes),'evaluated_vertices':total_v,'authored_polygons':sum(len(o.data.polygons) for o in meshes),'evaluated_polygons':total_poly,'triangles':total_tri,'materials':len(allmats),'parts':parts,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'bounds_min_blender_xyz':minv,'bounds_max_blender_xyz':maxv,'bounds_size_blender_xyz':[maxv[i]-minv[i] for i in range(3)]},'exported_reopen_glb':{'path':output,'bytes':n,'sha256':h},'export_return':list(result)}
with open(output+'.json','w') as f: json.dump(report,f,indent=2,sort_keys=True); f.write('\n')
print(json.dumps(report,indent=2,sort_keys=True))
