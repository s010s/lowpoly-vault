# SPDX-License-Identifier: MIT
"""Reopen editable delivery and report its actual source inventory."""
import hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source
argv=sys.argv[sys.argv.index('--')+1:]
blend=Path(argv[0]).resolve();out=Path(argv[1]).resolve()
before=hashlib.sha256(blend.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(blend))
col=bpy.data.collections.get('EXPORT');assert col
audit=audit_source(col,18000)
parts=[]
for o in sorted(col.objects,key=lambda o:o.name):
    if o.type!='MESH': continue
    o.data.calc_loop_triangles();volume=0
    for tri in o.data.loop_triangles:
        a,b,c=[o.matrix_world@o.data.vertices[i].co for i in tri.vertices];volume+=a.dot(b.cross(c))/6
    parts.append({'name':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'signed_volume_m3':volume,'modifiers':len(o.modifiers)})
disallowed=[o.name for o in bpy.data.objects if o.type not in ('MESH','EMPTY')]
external_images=[i.name for i in bpy.data.images if i.source=='FILE' and not i.packed_file]
assert not disallowed and not external_images and not audit['errors']
assert all(p['signed_volume_m3']>0 for p in parts)
assert before==hashlib.sha256(blend.read_bytes()).hexdigest()
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'status':'PASS','blend_sha256':before,'blender_version':bpy.app.version_string,'source_reopened':True,'presentation_objects':disallowed,'external_images':external_images,'editable_mesh_parts':parts,'source_audit':audit,'signed_volume_scope':'Closed authored components have positive total signed volumes. This is not a Boolean-union, collision or printability test.'},indent=2)+'\n')
