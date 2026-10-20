import bpy, json, hashlib
from mathutils import Vector
paths=[('collinsium','r002'),('yardang','r002'),('glacial-cirque','r001'),('aragonite-frostwork','r001')]
base='/tmp/lowpoly-batch60-20261020/assets/candidates/continuous-small-life-round23-20261020/batch-60'
out=[]
for aid,rev in paths:
 p=f'{base}/{aid}/{rev}/source.blend'
 sh=hashlib.sha256(open(p,'rb').read()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=p, load_ui=False)
 deps=bpy.context.evaluated_depsgraph_get()
 exp=bpy.data.collections.get('EXPORT')
 objs=list(exp.all_objects) if exp else []
 meshobs=[]; coords=[]; total_auth=total_faces=total_eval=total_tris=0
 for ob in objs:
  if ob.type!='MESH': continue
  me=ob.data; eo=ob.evaluated_get(deps); em=eo.to_mesh(); em.calc_loop_triangles()
  ntri=len(em.loop_triangles); total_auth+=len(me.vertices); total_faces+=len(me.polygons); total_eval+=len(em.vertices); total_tris+=ntri
  # bounds from actual evaluated mesh vertices in world coordinates
  for v in em.vertices: coords.append(eo.matrix_world @ v.co)
  meshobs.append({'name':ob.name,'authored_vertices':len(me.vertices),'authored_polygons':len(me.polygons),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':ntri,'scale':list(ob.scale),'modifiers':[m.name+':'+m.type for m in ob.modifiers],'materials':[m.name if m else None for m in ob.data.materials]})
  eo.to_mesh_clear()
 mn=[min(v[i] for v in coords) for i in range(3)] if coords else [None]*3; mx=[max(v[i] for v in coords) for i in range(3)] if coords else [None]*3
 roots=[o.name for o in (exp.objects if exp else []) if o.parent is None]
 scene_objects=len(bpy.context.scene.objects)
 out.append({'asset_id':aid,'revision':rev,'source_sha256':sh,'blender_version':bpy.app.version_string,'scene_object_count':scene_objects,'export_collection_exists':bool(exp),'export_mesh_object_count':len(meshobs),'export_root_names':roots,'authored_vertices':total_auth,'authored_polygons':total_faces,'evaluated_vertices':total_eval,'evaluated_triangles':total_tris,'bounds_blender_xyz_m':{'min':mn,'max':mx,'size':[mx[i]-mn[i] for i in range(3)]},'parts':meshobs})
with open('/tmp/lowpoly-round23-qa60/source-reopen-audit.json','w') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
