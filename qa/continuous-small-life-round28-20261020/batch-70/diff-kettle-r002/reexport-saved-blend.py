import bpy,sys,pathlib,json,hashlib,os
args=sys.argv[sys.argv.index('--')+1:]
source=pathlib.Path(args[0]).resolve(); output=pathlib.Path(args[1]).resolve(); record=pathlib.Path(args[2]).resolve()
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
source_before=sha(source)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
col=bpy.data.collections.get('EXPORT')
if col is None: raise RuntimeError('EXPORT collection missing')
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects: obj.select_set(True)
root_name=col.get('asset_root')
root=bpy.data.objects.get(root_name) if root_name else None
if root is None or root.name not in col.all_objects: raise RuntimeError(f'asset_root object missing: {root_name!r}')
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(output),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts)
record.write_text(json.dumps({'blender_version':bpy.app.version_string,'source_path':str(source),'source_sha256_before':source_before,'source_sha256_after':sha(source),'saved_source_unchanged':source_before==sha(source),'output_path':str(output),'output_sha256':sha(output),'output_bytes':output.stat().st_size,'exact_export_options':{k:v for k,v in opts.items() if k!='filepath'}},indent=2)+'\n')
print('saved_blend_reexport_sha256',sha(output),'bytes',output.stat().st_size)
