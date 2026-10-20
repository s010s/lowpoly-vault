import bpy,sys,pathlib,hashlib,json,traceback,datetime
argv=sys.argv[sys.argv.index('--')+1:]; source,glb,out=map(pathlib.Path,argv)
out.parent.mkdir(parents=True,exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sh,gh=h(source),h(glb)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
bpy.context.view_layer.update()
col=bpy.data.collections.get('EXPORT')
if col is None: raise RuntimeError('Missing EXPORT collection')
objs=list(col.all_objects)
bpy.ops.object.select_all(action='DESELECT')
for o in objs:o.select_set(True)
root=col.get('asset_root')
if not root or root not in bpy.data.objects: raise RuntimeError('Missing asset_root object')
bpy.context.view_layer.objects.active=bpy.data.objects[root]
opts=dict(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts)
if h(source)!=sh or h(glb)!=gh: raise RuntimeError('Source or input GLB changed during QA')
newh=h(out)
report={'kind':'read_only_blender_reopen_exact_reexport','status':'pass_exact_bytes' if newh==gh else 'bytes_differ','source_sha256':sh,'input_glb_sha256':gh,'reexport_sha256':newh,'exact_bytes_equal':newh==gh,'reexport_bytes':out.stat().st_size,'blender_version':bpy.app.version_string,'source_saved':False,'autoexec_disabled':True,'collection':'EXPORT','object_count':len(objs),'export_settings':{k:v for k,v in opts.items() if k!='filepath'},'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limitations':'Read-only saved .blend open and exact GLB re-export under recorded settings. Does not prove GPU, composed scene, visual fidelity, or factual correctness.'}
reportpath=out.with_suffix('.report.json');reportpath.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
