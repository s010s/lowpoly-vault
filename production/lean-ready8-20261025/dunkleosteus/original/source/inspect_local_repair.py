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
allowed={'pectoral-fin--1','pectoral-fin-1','pelvic-fin--1','pelvic-fin-1'};unchanged=[];changed=[]
for n in sorted(before):
 a=before[n];b=after[n]
 if a['digest']==b['digest']:unchanged.append({'object':n,'digest':b['digest']});continue
 assert n in allowed,(n,'unexpected change')
 assert a['materials']==b['materials'],(n,'unexpected material change')
 edits={'exported_vertex_count_before':len(a['vertices']),'exported_vertex_count_after':len(b['vertices']),'note':'Recomputed split normals and quad triangulation may reorder changed fin buffers; exact source edit indices verified separately.'}
 changed.append({'object':n,'before_digest':a['digest'],'after_digest':b['digest'],'position_edits':edits,'triangles_unchanged':a['triangles']==b['triangles'],'materials_unchanged':True})
assert {x['object'] for x in changed}==allowed
body=surfaces['continuous-stocky-trunk-and-caudal-peduncle'][0];tests=[]
for n in sorted(allowed):
 bvh,vs,faces=surfaces[n];overlap=bvh.overlap(body);mind=999
 for tri in faces:
  a,b,c=[Vector(vs[i]) for i in tri]
  for u in range(11):
   for v in range(11-u):
    q=a*(u/10)+b*(v/10)+c*(1-(u+v)/10);hit=body.find_nearest(q)
    if hit:mind=min(mind,hit[3])
 assert overlap,(n,'still detached')
 tests.append({'fin':n,'target':'continuous-stocky-trunk-and-caudal-peduncle','triangle_overlap_pairs':len(overlap),'minimum_surface_sample_distance_m':mind,'status':'INTERSECTS_BODY_SURFACE','limitation':'Geometric intersection supports attachment, not visual quality or a watertight unified mesh.'})
out.write_text(json.dumps({'before_glb_sha256':sha(old),'after_glb_sha256':sha(new),'scope':'Only four paired fin meshes changed; materials and every other semantic object stayed identical in clean GLB imports. Changed root normals/quad triangulation were re-evaluated by export.','unchanged_objects':unchanged,'changed_objects':changed,'attachment_tests':tests,'status':'PASS_LOCAL_TECHNICAL_SCOPE','independent_closure':'PENDING'},indent=2)+'\n')
print('UNCHANGED',len(unchanged),'CHANGED',len(changed));print([(t['fin'],t['triangle_overlap_pairs']) for t in tests])
