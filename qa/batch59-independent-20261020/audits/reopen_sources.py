import bpy, sys, json, hashlib
from pathlib import Path
ROOT=Path('/tmp/lowpoly-batch59-20261020')
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import audit_source
jobs=[('erbenochile','r003'),('glacial-erratic','r002'),('gypsum-cave-flower','r002'),('stalactite-group','r002')]
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
results=[]
for aid,rev in jobs:
  base=ROOT/'assets/candidates/continuous-small-life-round22-20261020/batch-59'/aid/rev
  src=base/(aid+'.blend'); glb=base/(aid+'.glb')
  bpy.context.preferences.filepaths.use_scripts_auto_execute=False
  bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False)
  bpy.context.view_layer.update()
  roots=[c for c in bpy.data.collections if c.get('asset_root')]
  if len(roots)!=1: raise RuntimeError(f'{aid}: expected 1 asset_root collection, got {len(roots)}')
  audit=audit_source(roots[0],max_triangles=14000)
  imported={'id':aid,'revision':rev,'blender_version':bpy.app.version_string,'source_sha256':digest(src),'glb_sha256':digest(glb),'collection':roots[0].name,'source_saved':False,'autoexec_disabled':not bpy.context.preferences.filepaths.use_scripts_auto_execute,'audit':audit}
  results.append(imported)
  print(json.dumps({'id':aid,'source_sha256':imported['source_sha256'],'glb_sha256':imported['glb_sha256'],'triangles':audit['triangles'],'materials':audit['materials'],'bounds_blender_m':audit['bounds_blender_m'],'source_warnings':audit['warnings'],'source_errors':audit['errors']}),flush=True)
Path('/tmp/lowpoly-round22-qa59/audits/source-reopening.json').write_text(json.dumps(results,indent=2)+'\n')
