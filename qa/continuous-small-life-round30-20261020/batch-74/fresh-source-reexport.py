import bpy,sys,json,hashlib,datetime,os
from pathlib import Path
ROOT=Path('/workspace/shared/lowpoly-batch74-20261020')
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
from check_reproducibility import file_hash
args=sys.argv[sys.argv.index('--')+1:]
source=Path(args[args.index('--source')+1]); glb=Path(args[args.index('--glb')+1]); out=Path(args[args.index('--output')+1]); report_path=Path(args[args.index('--report')+1]); collection_name=args[args.index('--collection')+1]
if out.exists() or report_path.exists(): raise RuntimeError('refusing to overwrite QA output')
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); source_before=file_hash(source); glb_before=file_hash(glb)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
bpy.context.view_layer.update(); col=bpy.data.collections.get(collection_name)
if col is None: raise RuntimeError('missing export collection '+collection_name)
for obj in bpy.context.selected_objects: obj.select_set(False)
for obj in col.all_objects: obj.select_set(True)
root=bpy.data.objects.get(col.get('asset_root',''))
if root is None: raise RuntimeError('missing root object metadata')
bpy.context.view_layer.objects.active=root
source_audit=audit_source(col,max_triangles=10**9)
options=dict(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
missing=sorted(set(options)-available)
if missing: raise RuntimeError('Blender exporter lacks flags '+','.join(missing))
bpy.ops.export_scene.gltf(**options)
exported=audit_glb(out,max_triangles=10**9,max_materials=10**6,max_primitives=10**6)
semantic_match=exported.get('semantic_sha256')==audit_glb(glb,max_triangles=10**9,max_materials=10**6,max_primitives=10**6).get('semantic_sha256')
source_after=file_hash(source); glb_after=file_hash(glb)
report={'schema_version':1,'kind':'fresh_saved_source_reopen_and_export','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_path':str(source),'source_sha256_before':source_before,'source_sha256_after':source_after,'source_unchanged':source_before==source_after,'target_glb_path':str(glb),'target_glb_sha256_before':glb_before,'target_glb_sha256_after':glb_after,'target_glb_unchanged':glb_before==glb_after,'reexport_path':str(out),'reexport_sha256':file_hash(out),'reexport_bytes':out.stat().st_size,'byte_identical_to_target':file_hash(out)==glb_before,'semantic_sha256_reexport':exported.get('semantic_sha256'),'semantic_sha256_target':audit_glb(glb,max_triangles=10**9,max_materials=10**6,max_primitives=10**6).get('semantic_sha256'),'semantic_match':semantic_match,'triangle_match':exported.get('scene_triangles')==audit_glb(glb,max_triangles=10**9,max_materials=10**6,max_primitives=10**6).get('scene_triangles'),'source_audit':source_audit,'reexport_audit':exported,'blender_version':bpy.app.version_string,'script_autoexecute':False,'export_collection':collection_name,'export_options':{k:v for k,v in options.items() if k!='filepath'},'status':'pass' if source_before==source_after and glb_before==glb_after and not source_audit['errors'] and not exported['errors'] and semantic_match and exported.get('scene_triangles')==audit_glb(glb,max_triangles=10**9,max_materials=10**6,max_primitives=10**6).get('scene_triangles') else 'fail','limitations':'Fresh source re-open/export compares semantic geometry and static scene counts; not an artistic, factual, GPU or composed-scene validation.'}
report_path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['created_at','source_sha256_before','source_sha256_after','source_unchanged','target_glb_sha256_before','target_glb_sha256_after','target_glb_unchanged','reexport_sha256','byte_identical_to_target','semantic_match','triangle_match','status']},indent=2))
if report['status']!='pass': raise RuntimeError('fresh source re-export mismatch')
