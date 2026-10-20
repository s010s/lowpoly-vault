import bpy,sys,json,hashlib,pathlib
source=pathlib.Path(sys.argv[sys.argv.index('--')+1]).resolve()
original=pathlib.Path(sys.argv[sys.argv.index('--')+2]).resolve()
metadata=pathlib.Path(sys.argv[sys.argv.index('--')+3]).resolve()
output=pathlib.Path(sys.argv[sys.argv.index('--')+4]).resolve()
h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
source_hash=h(source); glb_hash=h(original); metadata_hash=h(metadata)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
coll=bpy.data.collections.get('EXPORT')
if coll is None: raise RuntimeError('EXPORT collection missing')
bpy.ops.object.select_all(action='DESELECT')
for obj in coll.all_objects: obj.select_set(True)
root=bpy.data.objects.get(str(coll.get('asset_root','')))
if root is None: raise RuntimeError('asset_root object missing in EXPORT')
bpy.context.view_layer.objects.active=root
opts=json.loads(metadata.read_text())['export_options'];opts['filepath']=str(output)
bpy.ops.export_scene.gltf(**opts)
report={'kind':'independent_saved_source_reexport','status':'pass' if h(output)==glb_hash else 'fail','blender_version':bpy.app.version_string,'source_sha256_before':source_hash,'source_sha256_after':h(source),'original_glb_sha256_before':glb_hash,'original_glb_sha256_after':h(original),'metadata_sha256':metadata_hash,'reexport_sha256':h(output),'byte_identical':h(output)==glb_hash,'bytes_original':original.stat().st_size,'bytes_reexport':output.stat().st_size,'options':opts|{'filepath':'<own QA output>'},'script_autoexec':False,'limitations':'Read-only reopen of saved editable blend and independent export with frozen metadata options. Does not establish factual/artistic quality.'}
report_path=output.with_suffix('.report.json');report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report,ensure_ascii=False))
if report['status']!='pass': raise RuntimeError('Independent re-export bytes differ')
