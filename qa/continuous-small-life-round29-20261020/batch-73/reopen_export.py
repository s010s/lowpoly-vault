import argparse,hashlib,json,math,pathlib,sys
from datetime import datetime,timezone
sys.path.insert(0,'/workspace/shared/lowpoly-batch73-20261020/scripts')
import bpy
from asset_common import audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
parser=argparse.ArgumentParser()
parser.add_argument('--asset',required=True)
parser.add_argument('--source',required=True)
parser.add_argument('--shipped-glb',required=True)
parser.add_argument('--output',required=True)
a=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
src=pathlib.Path(a.source).resolve(); shipped=pathlib.Path(a.shipped_glb).resolve(); output=pathlib.Path(a.output).resolve()
if output.exists(): raise RuntimeError('Refusing to overwrite existing QA export: '+str(output))
output.parent.mkdir(parents=True,exist_ok=True)
source_hash_before=sha(src); shipped_hash_before=sha(shipped)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False)
bpy.context.view_layer.update()
cols=[c for c in bpy.data.collections if 'asset_root' in c]
if len(cols)!=1: raise RuntimeError('Expected exactly one asset_root-marked export collection; found '+str(len(cols)))
col=cols[0]; meshes=[o for o in col.all_objects if o.type=='MESH']
if not meshes: raise RuntimeError('No export mesh in marked collection')
source_audit=audit_source(col,max_triangles=10**9)
if source_audit['errors']: raise RuntimeError('Saved-source audit errors: '+repr(source_audit['errors']))
orig_audit=audit_glb(shipped,max_triangles=10**9,max_materials=10**6,max_primitives=10**6)
if orig_audit['errors']: raise RuntimeError('Shipped GLB audit errors: '+repr(orig_audit['errors']))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects: obj.select_set(True)
root=bpy.data.objects.get(col.get('asset_root',''))
if root is not None: bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(output),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
res=bpy.ops.export_scene.gltf(**opts)
if 'FINISHED' not in res: raise RuntimeError('Blender export operator did not finish: '+repr(res))
fresh_audit=audit_glb(output,max_triangles=10**9,max_materials=10**6,max_primitives=10**6)
if fresh_audit['errors']: raise RuntimeError('Fresh source export audit errors: '+repr(fresh_audit['errors']))
source_hash_after=sha(src); shipped_hash_after=sha(shipped)
if source_hash_before!=source_hash_after or shipped_hash_before!=shipped_hash_after: raise RuntimeError('Input source/GLB changed during read-only re-open/export')
report={'schema_version':1,'check':'saved_source_read_only_reopen_and_fresh_export','asset_id':a.asset,'status':'pass','observed_at':datetime.now(timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'source_path':str(src),'source_sha256_before':source_hash_before,'source_sha256_after':source_hash_after,'source_saved':False,'shipped_glb_path':str(shipped),'shipped_glb_sha256_before':shipped_hash_before,'shipped_glb_sha256_after':shipped_hash_after,'export_collection':col.name,'mesh_objects':len(meshes),'source_audit':source_audit,'fresh_export_path':str(output),'fresh_export_sha256':fresh_audit['sha256'],'fresh_export_audit':fresh_audit,'shipped_glb_audit':orig_audit,'semantic_sha256_equal':fresh_audit.get('semantic_sha256')==orig_audit.get('semantic_sha256'),'triangle_count_equal':fresh_audit.get('scene_triangles')==orig_audit.get('scene_triangles'),'measured_bounds_max_abs_delta_m':max(abs(fresh_audit['bounds_m'][side][i]-orig_audit['bounds_m'][side][i]) for side in ['min','max'] for i in range(3)),'export_options':{k:v for k,v in opts.items() if k!='filepath'},'limitations':'Read-only source re-open/export and static decoded-GLB comparison only. No scientific, GPU, browser, composed-scene, or formal/user approval.'}
report['comparisons_pass']=report['semantic_sha256_equal'] and report['triangle_count_equal'] and report['measured_bounds_max_abs_delta_m']<=0.0001
if not report['comparisons_pass']: report['status']='fail'
(output.with_suffix('.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'asset_id':a.asset,'status':report['status'],'fresh_export_sha256':report['fresh_export_sha256'],'semantic_sha256_equal':report['semantic_sha256_equal'],'triangles':fresh_audit['scene_triangles'],'source_triangles':source_audit['triangles'],'bounds_max_delta_m':report['measured_bounds_max_abs_delta_m'],'source_unchanged':source_hash_before==source_hash_after},indent=2))
if report['status']!='pass': raise RuntimeError('Source re-export did not match shipped static semantics')
