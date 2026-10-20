import bpy, argparse, hashlib, json, math, os, sys
from pathlib import Path
sys.path.insert(0, '/workspace/shared/lowpoly-batch71-20261020/scripts')
from asset_common import audit_source
from qa_glb import audit_glb

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1<<20),b''): h.update(c)
 return h.hexdigest()
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
ap=argparse.ArgumentParser(); ap.add_argument('--source',required=True); ap.add_argument('--target-glb',required=True); ap.add_argument('--output-glb',required=True); ap.add_argument('--report',required=True); ap.add_argument('--expected-glb-sha256',required=True); ap.add_argument('--asset',required=True)
a=ap.parse_args(argv)
src=Path(a.source).resolve(); tgt=Path(a.target_glb).resolve(); out=Path(a.output_glb).resolve(); rep=Path(a.report).resolve()
if out.exists() or rep.exists(): raise RuntimeError('Refusing to overwrite existing QA outputs')
src0=sha(src); tgt0=sha(tgt)
if tgt0 != a.expected_glb_sha256: raise RuntimeError('Target GLB hash mismatch before Blender execution')
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
# Blender startup file is the saved source, loaded by the parent command.
bpy.context.view_layer.update()
col=bpy.data.collections.get('EXPORT')
if col is None: raise RuntimeError('No EXPORT collection')
source_audit=audit_source(col,max_triangles=10**9)
# Export with the frozen static profile, selecting exactly the saved EXPORT collection hierarchy.
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:
 if obj.name in bpy.context.view_layer.objects:
  obj.select_set(True)
opts=dict(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.object.mode_set(mode='OBJECT') if bpy.context.object and bpy.context.object.mode!='OBJECT' else None
bpy.ops.export_scene.gltf(**opts)
exported=audit_glb(out,max_triangles=10**9,max_materials=10**6,max_primitives=10**6)
source_hash, target_hash, output_hash=sha(src),sha(tgt),sha(out)
if source_hash != src0 or target_hash != tgt0: raise RuntimeError('Input source or target changed during independent export')
result={'schema_version':1,'kind':'independent_saved_source_reopen_export','asset_id':a.asset,'blender_version':bpy.app.version_string,'blender_build_hash':bpy.app.build_hash.decode('ascii','replace') if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'source_path':str(src),'source_sha256_before':src0,'source_sha256_after':source_hash,'target_glb_path':str(tgt),'target_glb_sha256_before':tgt0,'target_glb_sha256_after':target_hash,'fresh_export_path':str(out),'fresh_export_sha256':output_hash,'byte_identical_to_target':output_hash==tgt0,'source_saved':False,'autoexec':False,'export_collection':'EXPORT','export_profile':'static-uncompressed-v1 exact frozen options','export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_audit':source_audit,'fresh_export_audit':exported,'fresh_export_bytes':out.stat().st_size,'target_bytes':tgt.stat().st_size}
rep.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'asset':a.asset,'source_sha256':source_hash,'target_sha256':target_hash,'fresh_export_sha256':output_hash,'byte_identical_to_target':output_hash==tgt0,'source_triangles':source_audit.get('triangles'),'export_triangles':exported.get('scene_triangles'),'source_bounds':source_audit.get('bounds_blender_m'),'export_bounds':exported.get('bounds_m'),'warnings':source_audit.get('warnings',[])+exported.get('warnings',[]),'report':str(rep)},sort_keys=True))
if source_audit.get('errors') or exported.get('errors'): raise RuntimeError('Independent saved-source/export check reported errors')
