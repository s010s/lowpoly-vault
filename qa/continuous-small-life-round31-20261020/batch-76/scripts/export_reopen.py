import bpy, hashlib, json, sys
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
source=Path(args[0]).resolve(); original=Path(args[1]).resolve(); output=Path(args[2]).resolve(); report_path=Path(args[3]).resolve()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
source_before, original_before = sha(source), sha(original)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
bpy.context.view_layer.update()
collections=[c for c in bpy.data.collections if c.get('asset_root')]
if len(collections)!=1: raise RuntimeError(f'Expected one asset_root export collection; got {len(collections)}')
collection=collections[0]
bpy.ops.object.select_all(action='DESELECT')
for obj in collection.all_objects: obj.select_set(True)
root=bpy.data.objects.get(collection.get('asset_root',''))
if root is None: raise RuntimeError('asset_root object not found')
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(output),export_format='GLB',use_selection=True,
 export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,
 export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,
 export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,
 export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
missing=set(options)-available
if missing: raise RuntimeError('Blender exporter lacks required flags: '+', '.join(sorted(missing)))
bpy.ops.export_scene.gltf(**options)
source_after, original_after = sha(source), sha(original)
result={"kind":"readonly-saved-blend-reopen-export","blender":bpy.app.version_string,
 "source_path":str(source),"original_glb_path":str(original),"export_path":str(output),
 "export_collection":collection.name,"export_root":root.name,"selection_count":len(collection.all_objects),
 "script_autoexec":False,"source_saved":False,"export_options":options,
 "source_sha256_before":source_before,"source_sha256_after":source_after,
 "original_glb_sha256_before":original_before,"original_glb_sha256_after":original_after,
 "reexport_sha256":sha(output),"reexport_bytes":output.stat().st_size,
 "original_glb_sha256":original_before,"byte_identical":sha(output)==original_before,
 "source_unchanged":source_before==source_after,"original_glb_unchanged":original_before==original_after}
report_path.parent.mkdir(parents=True,exist_ok=True)
report_path.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result))
if not result['source_unchanged'] or not result['original_glb_unchanged']: raise RuntimeError('Input changed during read-only re-export')
