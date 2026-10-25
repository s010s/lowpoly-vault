# SPDX-License-Identifier: MIT
"""Fresh source reopening and narrow topology/measurement checks, not factual approval."""
import bpy,json,sys,hashlib,math
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

def connected_components(mesh):
 parent=list(range(len(mesh.vertices)))
 def find(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 for e in mesh.edges:
  a,b=(find(i) for i in e.vertices)
  if a!=b:parent[b]=a
 return len({find(i) for i in range(len(mesh.vertices))})
components={o.name:connected_components(o.data) for o in meshes}
for side in ['left','right']:
 for n in [2,3]:assert components[side+f'-P{n}-paddle-leg']==5
 for n in [4,5]:assert components[side+f'-P{n}-reduced-posterior-leg']==(5 if n==4 else 4)
 assert components[side+'-P1-single-fixed-deflected-finger']==1
 assert components[side+'-P1-single-mobile-dactyl']==1
 assert components[side+'-large-unprotected-compound-eye']==1
 assert components[side+'-pediform-third-maxilliped']==4
assert components['paired-first-antennae']==2 and components['paired-second-antennae']==2
assert components['six-segment-symmetric-folded-pleon']==6
assert components['bifid-rostrum']==2
names=['fusiform-carapace-with-sculpted-grooves','bifid-rostrum']
verts=[v.co for n in names for v in bpy.data.objects[n].data.vertices]
carapace_size=[max(v[i] for v in verts)-min(v[i] for v in verts) for i in range(3)]
assert abs(carapace_size[0]-.0052)<1e-7
assert abs(carapace_size[1]-.0085)<1e-5
metrics={}
for side in ['left','right']:
 for n in [2,3,4,5]:
  o=bpy.data.objects[side+f'-P{n}-'+('paddle-leg' if n in [2,3] else 'reduced-posterior-leg')]
  xyz=[v.co for v in o.data.vertices];lo=[min(v[i] for v in xyz) for i in range(3)];hi=[max(v[i] for v in xyz) for i in range(3)]
  metrics[o.name]={'bounds_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]}}
result={'status':'PASS','blend_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'reopened':True,'root':'callichimaera','root_identity':True,'metric_scale':bpy.context.scene.unit_settings.scale_length,'mesh_count':len(meshes),'editable_semantic_meshes':counts,'external_libraries':0,'images':0,'fonts':0,'sounds':0,'rig':False,'animation':False,'presentation_objects_in_export':0,'render_output':'//','inspection_scope':'Actual .blend reopened in fresh Blender process; semantic mesh editing available. Component checks support authoring count only and do not establish paleontological validity.','connected_components':components,'carapace_plus_rostrum_dimensions_xyz_m':carapace_size,'carapace_nominal_length_m':.0085,'carapace_nominal_width_m':.0052,'carapace_length_tolerance_m':1e-5,'appendage_measurements':metrics,'factual_acceptance':'PENDING'}
out.write_text(json.dumps(result,indent=2)+'\n')
