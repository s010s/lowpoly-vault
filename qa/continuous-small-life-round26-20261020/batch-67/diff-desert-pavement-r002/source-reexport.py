import bpy,sys,json,hashlib
from pathlib import Path
repo=Path('/workspace/shared/lowpoly-batch67-20261020');sys.path.insert(0,str(repo/'scripts'))
from qa_glb import audit_glb
args=sys.argv[sys.argv.index('--')+1:]
source=Path(args[0]);original=Path(args[1]);out=Path(args[2]);report_path=Path(args[3])
assert not out.exists() and not report_path.exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_sha=sha(source);glb_sha=sha(original)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
bpy.context.view_layer.update()
collections=[c for c in bpy.data.collections if c.get('asset_root')]
if len(collections)!=1: raise RuntimeError(f'Expected exactly one asset_root export collection; found {len(collections)}')
col=collections[0]
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
root=bpy.data.objects.get(col.get('asset_root'))
if root is None:raise RuntimeError('asset_root object is missing')
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**options)
orig_audit=audit_glb(original,max_triangles=14000,max_materials=6,max_primitives=30)
reexp_audit=audit_glb(out,max_triangles=14000,max_materials=6,max_primitives=30)
report={'kind':'independent_blend_reopen_reexport','status':'pass' if not reexp_audit['errors'] and orig_audit.get('semantic_sha256')==reexp_audit.get('semantic_sha256') and orig_audit['scene_triangles']==reexp_audit['scene_triangles'] and sha(source)==source_sha and sha(original)==glb_sha else 'fail','blender_version':bpy.app.version_string,'autoexec_disabled':True,'source_saved':False,'export_collection':col.name,'source_sha256':source_sha,'original_glb_sha256':glb_sha,'original_glb_bytes':original.stat().st_size,'reexport_path':str(out),'reexport_sha256':sha(out),'reexport_bytes':out.stat().st_size,'semantic_sha256_original':orig_audit.get('semantic_sha256'),'semantic_sha256_reexport':reexp_audit.get('semantic_sha256'),'triangles_original':orig_audit.get('scene_triangles'),'triangles_reexport':reexp_audit.get('scene_triangles'),'bounds_original':orig_audit.get('bounds_m'),'bounds_reexport':reexp_audit.get('bounds_m'),'export_options':options,'errors':reexp_audit['errors'],'limitations':'Actual Blender source reopen and GLB export; semantic static geometry comparison only, not materials visual equivalence, GPU, composed scene, scientific or release acceptance.'}
report_path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if report['status']!='pass':raise RuntimeError('Source re-export did not semantically match shipped GLB')
