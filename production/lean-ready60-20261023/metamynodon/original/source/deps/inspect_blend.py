# SPDX-License-Identifier: MIT
"""Reopen the delivered editable source and check the intended static asset."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source
ap=argparse.ArgumentParser();ap.add_argument('blend');ap.add_argument('--report',required=True)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.blend).resolve();report=Path(a.report).resolve()
bpy.ops.wm.open_mainfile(filepath=str(path));c=bpy.data.collections.get('EXPORT');assert c
assert all(o.type in ('MESH','EMPTY') for o in bpy.context.scene.objects)
assert len(bpy.context.scene.objects)==len(c.all_objects)
assert not any(i.source=='FILE' and i.filepath for i in bpy.data.images)
assert not bpy.data.libraries
assert bpy.context.scene.camera is None
q=audit_source(c,16000);assert not q['errors']
root=bpy.data.objects[c['asset_root']]
assert root.get('fore_toes_each')==4 and root.get('hind_toes_each')==3 and root.get('horns')==0
result={'status':'PASS','blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'runtime':bpy.app.version_string,'mesh_objects':len([o for o in c.all_objects if o.type=='MESH']),'root_identity':True,'source_audit':q,'external_libraries':0,'external_file_images':0,'camera_or_light_objects':0,'scope':'Actual reopening of the editable delivered source, not just saved-file existence'}
report.write_text(json.dumps(result,indent=2)+'\n');print('SOURCE_REOPEN_PASS')
