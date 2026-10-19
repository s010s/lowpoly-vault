import bpy, bmesh, json, math, sys, hashlib, pathlib

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def collect_mesh(objects):
    dg=bpy.context.evaluated_depsgraph_get()
    rows=[]; allpts=[]; tris=0; verts=0; materials=set(); boundary=0; nonmanifold=0; degenerate=0; nonfinite=0
    for ob in objects:
        if ob.type!='MESH': continue
        eo=ob.evaluated_get(dg); me=eo.to_mesh(); me.calc_loop_triangles()
        pts=[]
        for v in me.vertices:
            p=eo.matrix_world @ v.co
            q=[float(p.x),float(p.y),float(p.z)]; pts.append(q); allpts.append(q)
            if not all(math.isfinite(x) for x in q): nonfinite+=1
        bm=bmesh.new(); bm.from_mesh(me)
        b=sum(len(e.link_faces)==1 for e in bm.edges)
        nm=sum(len(e.link_faces)!=2 for e in bm.edges)
        boundary+=b; nonmanifold+=nm
        degen=sum(f.calc_area()<=1e-12 for f in bm.faces); degenerate+=degen
        bm.free()
        t=len(me.loop_triangles); tris+=t; verts+=len(me.vertices)
        mats=sorted({m.name for m in ob.data.materials if m})
        materials.update(mats)
        if pts:
            lo=[min(p[i] for p in pts) for i in range(3)]; hi=[max(p[i] for p in pts) for i in range(3)]
        else: lo=hi=[]
        rows.append({'name':ob.name,'vertices_evaluated':len(me.vertices),'triangles':t,'materials':mats,'boundary_edges':b,'nonmanifold_edges':nm,'degenerate_faces':degen,'bounds_min':lo,'bounds_max':hi})
        eo.to_mesh_clear()
    if allpts:
        bounds={'min':[min(p[i] for p in allpts) for i in range(3)],'max':[max(p[i] for p in allpts) for i in range(3)]}
    else: bounds={'min':[],'max':[]}
    return {'parts':rows,'vertices_evaluated':verts,'triangles':tris,'materials':sorted(materials),'bounds':bounds,'boundary_edges_total':boundary,'nonmanifold_edges_total':nonmanifold,'degenerate_faces_total':degenerate,'nonfinite_vertices':nonfinite}
args=sys.argv[sys.argv.index('--')+1:]
assert len(args)%3==0, args
out=[]
for i in range(0,len(args),3):
    asset,blend,glb=args[i:i+3]
    bpy.ops.wm.open_mainfile(filepath=blend)
    exp=bpy.data.collections.get('EXPORT')
    meshes=list(exp.all_objects) if exp else list(bpy.context.scene.objects)
    source=collect_mesh(meshes)
    source.update({'export_collection_found':exp is not None,'export_object_names':sorted(o.name for o in meshes),'unit_scale_length':float(bpy.context.scene.unit_settings.scale_length),'length_unit':bpy.context.scene.unit_settings.length_unit,'blender_version':bpy.app.version_string})
    sh=sha(blend); gh=sha(glb)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.gltf(filepath=glb)
        imported=collect_mesh(list(bpy.context.scene.objects))
        imported['import_status']='pass'
    except Exception as e:
        imported={'import_status':'fail','error':str(e)}
    out.append({'asset_id':asset,'blend_sha256':sh,'glb_sha256':gh,'blend_bytes':pathlib.Path(blend).stat().st_size,'glb_bytes':pathlib.Path(glb).stat().st_size,'source':source,'glb_import':imported})
print('BATCH41_AUDIT_JSON '+json.dumps(out,separators=(',',':')))
