# SPDX-License-Identifier: MIT
import bpy,json,sys,hashlib
from pathlib import Path
out=Path(sys.argv[sys.argv.index('--')+1]);p=Path(bpy.data.filepath)
col=bpy.data.collections.get('EXPORT');assert col is not None
objs=list(col.all_objects);root=bpy.data.objects[col['asset_root']]
assert root.type=='EMPTY' and all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-8 for i in range(4) for j in range(4))
assert not bpy.data.libraries and not bpy.data.images and not bpy.data.fonts and not bpy.data.sounds
assert not [o for o in objs if o.type not in ['EMPTY','MESH']]
assert bpy.context.scene.render.filepath=='//'
meshes=[o for o in objs if o.type=='MESH'];counts={o.name:{'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'materials':len(o.data.materials)} for o in meshes}
for o in meshes:assert not o.modifiers and not o.constraints and not o.animation_data
out.write_text(json.dumps({'status':'PASS','blend_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'reopened':True,'root':'dunkleosteus','root_identity':True,'metric_scale':bpy.context.scene.unit_settings.scale_length,'mesh_count':len(meshes),'editable_semantic_meshes':counts,'external_libraries':0,'images':0,'fonts':0,'sounds':0,'rig':False,'animation':False,'presentation_objects_in_export':0,'render_output':'//','inspection_scope':'Actual .blend reopened in fresh Blender process. Semantic mesh editing available; generator/config retained separately. No rig or deformation-readiness claim.'},indent=2)+'\n')
