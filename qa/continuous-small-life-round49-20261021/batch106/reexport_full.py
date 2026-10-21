import bpy,sys,json,os,hashlib,datetime
from pathlib import Path
src,out=map(Path,sys.argv[sys.argv.index('--')+1:]);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=h(src)
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();cs=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cs)==1;c=cs[0]
bpy.ops.object.select_all(action='DESELECT')
for ob in c.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[c['asset_root']]
opts=dict(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts)
r={'source_sha256':before,'source_unchanged':h(src)==before,'source_saved':False,'selected_objects':[o.name for o in c.all_objects],'root':c['asset_root'],'output_sha256':h(out),'pid':os.getpid(),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'options':opts,'diagnostic_correction':'First independent export selected only meshes and omitted the root empty; geometry and normals matched exactly but scene-structure semantic digest differed. This second export selects the full original marked export collection and restores all original export flags. No source/geometry changes.'};out.with_suffix('.json').write_text(json.dumps(r,indent=2));print(r['output_sha256'])
