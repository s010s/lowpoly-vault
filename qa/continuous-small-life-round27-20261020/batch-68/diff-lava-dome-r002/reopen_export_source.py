import bpy, hashlib, json, os, sys
from pathlib import Path

args = sys.argv[sys.argv.index('--') + 1:]
source, output, expected = map(Path, args)
source_hash_before = hashlib.sha256(source.read_bytes()).hexdigest()
expected_hash = hashlib.sha256(expected.read_bytes()).hexdigest()
bpy.context.preferences.filepaths.use_scripts_auto_execute = False
bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
collection = bpy.data.collections.get('EXPORT')
if collection is None:
    raise RuntimeError('Expected EXPORT collection is absent')
root_name = collection.get('asset_root')
root = bpy.data.objects.get(root_name) if root_name else None
if root is None or root.name not in {obj.name for obj in collection.all_objects}:
    raise RuntimeError(f'Expected asset root named by EXPORT collection, got {root_name!r}')
bpy.ops.object.select_all(action='DESELECT')
for obj in collection.all_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = root
options = dict(
    filepath=str(output), export_format='GLB', use_selection=True, export_yup=True,
    export_apply=True, export_normals=True, export_texcoords=False, export_tangents=False,
    export_materials='EXPORT', export_vertex_color='NONE', export_animations=False,
    export_skins=False, export_morph=False, export_cameras=False, export_lights=False,
    export_extras=True, export_gpu_instances=False, export_gn_mesh=False,
    export_draco_mesh_compression_enable=False, export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**options)
source_hash_after = hashlib.sha256(source.read_bytes()).hexdigest()
output_hash = hashlib.sha256(output.read_bytes()).hexdigest()
result = {
    'status': 'pass' if source_hash_before == source_hash_after and output_hash == expected_hash else 'review',
    'check': 'independent_source_reopen_and_fresh_export',
    'blender_version': bpy.app.version_string,
    'source_path': str(source),
    'source_sha256_before': source_hash_before,
    'source_sha256_after': source_hash_after,
    'export_collection': collection.name,
    'export_object_names': [o.name for o in collection.all_objects],
    'expected_glb_path': str(expected),
    'expected_glb_sha256': expected_hash,
    'fresh_export_path': str(output),
    'fresh_export_sha256': output_hash,
    'byte_identical_to_candidate': output_hash == expected_hash,
    'source_unchanged': source_hash_before == source_hash_after,
    'gpu': 'not_run', 'scene': 'not_run'
}
report_path = output.with_suffix('.json')
report_path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print('INDEPENDENT_SOURCE_EXPORT=' + json.dumps(result, sort_keys=True))
if result['status'] != 'pass':
    raise RuntimeError('Source changed during export or fresh export differs from active candidate bytes')
