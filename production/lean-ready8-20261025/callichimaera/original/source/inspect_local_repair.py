# SPDX-License-Identifier: MIT
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
from mathutils import Vector
old,new,out=map(Path,sys.argv[sys.argv.index('--')+1:])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(path):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
 rows={};surfaces={}
 for o in bpy.context.scene.objects:
  if o.type!='MESH':continue
  o.data.calc_loop_triangles();v=[list(o.matrix_world@p.co) for p in o.data.vertices];f=[list(t.vertices) for t in o.data.loop_triangles]
  mats=[{'name':m.name,'base_color':list(m.diffuse_color),'roughness':m.roughness,'metallic':m.metallic,'single_sided':m.use_backface_culling} for m in o.data.materials]
  record={'vertices':v,'triangles':f,'materials':mats,'face_material_indices':[p.material_index for p in o.data.polygons],'transform':[list(r) for r in o.matrix_world]}
  rows[o.name]={'digest':hashlib.sha256(json.dumps(record,sort_keys=True).encode()).hexdigest(),'vertices':v,'triangles':f,'materials':mats,'face_material_indices':record['face_material_indices']}
  surfaces[o.name]=(BVHTree.FromPolygons([Vector(p) for p in v],f,all_triangles=True),v,f)
 return rows,surfaces
before,_=snapshot(old);after,surfaces=snapshot(new)
assert set(before)==set(after)
allowed={side+'-P1-'+part for side in ['left','right'] for part in ['stout-spanner-manus','single-fixed-deflected-finger','single-mobile-dactyl']};unchanged=[];changed=[]
for n in sorted(before):
 a,b=before[n],after[n]
 if a['digest']==b['digest']:unchanged.append({'object':n,'digest':b['digest']});continue
 assert n in allowed,(n,'unexpected change')
 assert a['materials']==b['materials'],(n,'material changed')
 changed.append({'object':n,'before_digest':a['digest'],'after_digest':b['digest'],'materials_unchanged':True,'vertices_before':len(a['vertices']),'vertices_after':len(b['vertices']),'triangle_count_before':len(a['triangles']),'triangle_count_after':len(b['triangles'])})
assert {x['object'] for x in changed}==allowed
tests=[]
for side in ['left','right']:
 palm=side+'-P1-stout-spanner-manus'
 for part in ['cheliped-arm','single-fixed-deflected-finger','single-mobile-dactyl']:
  n=side+'-P1-'+part
  overlap=surfaces[palm][0].overlap(surfaces[n][0])
  assert overlap,(palm,n,'not surface attached')
  tests.append({'part':n,'target':palm,'triangle_overlap_pairs':len(overlap),'status':'INTERSECTS_PALM_SURFACE','limitation':'Actual surface intersections support continuous attachment, not a boolean-unified mesh or factual acceptance.'})
import math
wrist=Vector((3.69,-3.16));palm=Vector((4.30,-3.22));root=Vector((3.70,-3.70));tip=Vector((3.43,-5.76))
angle=math.degrees((palm-wrist).angle(tip-root))
assert 80<angle<100
result={'before_glb_sha256':sha(old),'after_glb_sha256':sha(new),'scope':'Only the two P1 palms, fixed pollices and opposed mobile dactyls changed. Unchanged wrists and every other semantic object match exactly in clean GLB imports. No scale, material, or unrelated anatomical changes.','unchanged_objects':unchanged,'changed_objects':changed,'attachment_tests':tests,'right_palm_axis_proxy':{'wrist_mm':list(wrist),'palm_center_mm':list(palm),'fixed_root_mm':list(root),'fixed_tip_mm':list(tip),'top_projection_angle_degrees':angle,'limitation':'Transparent author centerline proxy corroborates local construction, not a unique fossil measurement or independent factual acceptance.'},'status':'PASS_LOCAL_TECHNICAL_SCOPE','independent_closure':'PENDING_RECHECK'}
out.write_text(json.dumps(result,indent=2)+'\n')
print('UNCHANGED',len(unchanged),'CHANGED',len(changed),'ANGLE',angle);print(tests)
