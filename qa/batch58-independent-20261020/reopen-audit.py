import bpy, json, os, hashlib
from mathutils import Vector
paths=[
('calamophyton','r001'),('perspicaris','r002'),('barchan-dune','r001'),('current-ripple-surface','r001')]
base='/tmp/lowpoly-batch58-20261020/assets/candidates/continuous-small-life-round22-20261020/batch-58'
out=[]
for aid,rev in paths:
 p=f'{base}/{aid}/{rev}/source.blend'
 with open(p,'rb') as f: sh=hashlib.sha256(f.read()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=p, load_ui=False)
 deps=bpy.context.evaluated_depsgraph_get()
 meshes=[]; coords=[]; total_authored_v=total_authored_f=total_eval_v=total_tris=0
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH': continue
  me=ob.data
  total_authored_v+=len(me.vertices); total_authored_f+=len(me.polygons)
  eo=ob.evaluated_get(deps); em=eo.to_mesh()
  em.calc_loop_triangles(); ntri=len(em.loop_triangles); total_tris+=ntri; total_eval_v+=len(em.vertices)
  for corner in ob.bound_box: coords.append(ob.matrix_world @ Vector(corner))
  meshes.append({'name':ob.name,'authored_vertices':len(me.vertices),'authored_faces':len(me.polygons),'evaluated_vertices':len(em.vertices),'evaluated_faces':len(em.polygons),'evaluated_triangles':ntri,'scale':list(ob.scale),'modifiers':[m.name+':'+m.type for m in ob.modifiers]})
  eo.to_mesh_clear()
 mn=[min(p[i] for p in coords) for i in range(3)] if coords else [None]*3
 mx=[max(p[i] for p in coords) for i in range(3)] if coords else [None]*3
 exp=bpy.data.collections.get('EXPORT')
 out.append({'asset_id':aid,'revision':rev,'source_sha256':sh,'blender_version':bpy.app.version_string,'object_count':len(bpy.context.scene.objects),'mesh_object_count':len(meshes),'authored_vertices':total_authored_v,'authored_faces':total_authored_f,'evaluated_vertices':total_eval_v,'evaluated_triangles':total_tris,'bounds_min':mn,'bounds_max':mx,'bounds_size':[mx[i]-mn[i] for i in range(3)],'export_collection_exists':bool(exp),'export_root_names':[o.name for o in (exp.objects if exp else []) if o.parent is None],'parts':meshes})
with open('/tmp/lowpoly-round22-qa58/source-reopen-audit.json','w') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
