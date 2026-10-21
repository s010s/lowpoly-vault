"""Read-only source reopen + full selected authored collection re-export.
Run under Blender --factory-startup --disable-autoexec --python-exit-code 1.
Temporary GLB only; no source saving, repair generators, or private archive access.
"""
import sys,pathlib,json,tempfile,hashlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from final_delivery import collect_final_delivery,need
from qa_glb import audit_glb
from asset_common import audit_source
from check_source_export import compare_source_audit
import bpy
root=pathlib.Path(__file__).resolve().parents[1]
checked=collect_final_delivery(root);results=[]
for a in checked['candidates']:
 source=root/a['final_paths']['source'];glb=root/a['final_paths']['glb'];before=hashlib.sha256(source.read_bytes()).hexdigest()
 bpy.context.preferences.filepaths.use_scripts_auto_execute=False
 bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
 cols=[c for c in bpy.data.collections if c.get('asset_root')];need(len(cols)==1,'exact authored export collection required');col=cols[0]
 bpy.context.view_layer.update();src=audit_source(col,max_triangles=14000)
 original=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
 report=compare_source_audit(src,original,before,a['native']['glb_sha256'])
 need(report['status'] in ['pass','pass_with_warnings'],'source/export audit failed '+str(report['errors']))
 bpy.ops.object.select_all(action='DESELECT')
 for obj in col.all_objects:obj.select_set(True)
 bpy.context.view_layer.objects.active=bpy.data.objects.get(col.get('asset_root',''))
 with tempfile.TemporaryDirectory(prefix='final-reexport-') as temp:
  dest=pathlib.Path(temp)/'rebuilt.glb'
  bpy.ops.export_scene.gltf(filepath=str(dest),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
  rebuilt=audit_glb(dest,max_triangles=14000,max_materials=6,max_primitives=30)
  need(rebuilt['status']=='pass','re-export static failed')
  need(rebuilt['semantic_sha256']==original['semantic_sha256'],'whole source re-export semantic identity differs')
  need(hashlib.sha256(source.read_bytes()).hexdigest()==before,'original Blend changed')
  results.append({'id':a['id'],'source_sha256':before,'glb_sha256':a['native']['glb_sha256'],'source_export':report['status'],'full_collection_reexport':'PASS','semantic_sha256':rebuilt['semantic_sha256'],'byte_equal':dest.read_bytes()==glb.read_bytes(),'source_saved':False,'gpu':'UNKNOWN','visual':'NOT_PERFORMED'})
print('FINAL_DELIVERY_NATIVE='+json.dumps({'blender_version':bpy.app.version_string,'results':results}))
