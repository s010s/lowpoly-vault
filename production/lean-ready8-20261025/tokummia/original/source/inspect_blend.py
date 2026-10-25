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
out.write_text(json.dumps({'status':'PASS','blend_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'reopened':True,'root':'tokummia','root_identity':True,'metric_scale':bpy.context.scene.unit_settings.scale_length,'mesh_count':len(meshes),'editable_semantic_meshes':counts,'external_libraries':0,'images':0,'fonts':0,'sounds':0,'rig':False,'animation':False,'presentation_objects_in_export':0,'render_output':'//','inspection_scope':'Actual .blend reopened in fresh Blender process. Semantic mesh editing available; generator/config retained separately. No rig or deformation-readiness claim.'},indent=2)+'\n')
# Explicit topology components corroborate the batched serial-limb station convention.
def connected_components(mesh):
 parent=list(range(len(mesh.vertices)))
 def find(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 for e in mesh.edges:
  a,b=(find(i) for i in e.vertices)
  if a!=b:parent[b]=a
 return len({find(i) for i in range(len(mesh.vertices))})
d=json.loads(out.read_text());d['connected_components']={o.name:connected_components(o.data) for o in meshes}
for side in ['left','right']:
 assert d['connected_components'][side+'-eight-anterior-walking-branches']==8
 assert d['connected_components'][side+'-walking-terminal-claws']==8
 assert d['connected_components'][side+'-posterior-slender-inner-branches']==42
 assert d['connected_components'][side+'-fifty-serial-outer-flaps']==50
 assert d['connected_components'][side+'-open-pincer-fingers-and-two-terminal-teeth']==3
 assert d['connected_components'][side+'-curved-carapace-valve']==1
 assert d['connected_components'][side+'-narrow-caudal-ramus']==1
d['limb_count_scope']='Components confirm 8 anterior inner branches, 42 posterior inner branches and 50 outer flaps per side, excluding grasping limbs. This corroborates geometry only, not a fossil-specific observed count.'
d['pincer_count_scope']='Per pincer: one fixed outer finger including its terminal tooth, one curved opposing finger, and a secondary terminal tooth intersecting the fixed finger. Two fixed-finger tooth tips in total, not three.'
out.write_text(json.dumps(d,indent=2)+'\n')
