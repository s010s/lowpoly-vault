# SPDX-License-Identifier: MIT
"""Inspect saved editable source without changing or saving it."""
import bpy,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source
args=sys.argv[sys.argv.index('--')+1:];p=Path(args[0]);out=Path(args[1]);h=hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(p.resolve()))
col=bpy.data.collections.get('EXPORT');assert col is not None
report=audit_source(col,16000);assert not report['errors']
root=bpy.data.objects[col['asset_root']]
assert root.name=='borophagus' and root.parent is None
assert not [o for o in bpy.context.scene.objects if o.type in {'CAMERA','LIGHT'}]
assert len([o for o in col.objects if o.name.startswith('four_toes_')])==4
assert all(o['weight_bearing_toe_count']==4 for o in col.objects if o.name.startswith('four_toes_'))
external=[]
for image in bpy.data.images:
    if image.source=='FILE' and image.filepath and not image.packed_file:external.append(image.filepath)
for library in bpy.data.libraries:external.append(library.filepath)
assert not external
result={'status':'PASS','blend_sha256':h,'glb_sha256':hashlib.sha256(p.with_suffix('.glb').read_bytes()).hexdigest(),'editable_meshes':len([o for o in col.objects if o.type=='MESH']),'export_collection':'EXPORT','root_identity':True,'units':'meters','no_source_stage_camera_or_light':True,'external_dependencies':external,'four_digit_paws':4,'source_audit':report,'scope':'Saved editable source and declared static structure only; no independent anatomical acceptance.'}
out.write_text(json.dumps(result,indent=2)+'\n')
assert hashlib.sha256(p.read_bytes()).hexdigest()==h
print('BLEND_REOPEN_PASS')
