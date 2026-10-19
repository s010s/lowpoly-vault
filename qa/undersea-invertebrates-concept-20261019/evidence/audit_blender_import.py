import bpy, json, hashlib
from mathutils import Vector
base='/workspace/lowpoly-vault/assets/candidates/undersea-invertebrates-concept-20261019'
items=[('mackenzia','r001'),('prasopora','r003'),('strophomena','r003'),('ctenoimbricata','r001')]
def get_color(m):
 if m.use_nodes:
  n=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if n and 'Base Color' in n.inputs: return [round(float(x),8) for x in n.inputs['Base Color'].default_value]
 return [round(float(x),8) for x in m.diffuse_color]
def mesh_info(objects):
 meshes=[o for o in objects if o.type=='MESH']; pts=[]; tris=0; mats={}
 for o in meshes:
  pts.extend(o.matrix_world @ Vector(c) for c in o.bound_box)
  o.data.calc_loop_triangles(); tris+=len(o.data.loop_triangles)
  for m in o.data.materials:
   if m: mats[m.name.removesuffix('.001')]=get_color(m)
 mins=[min(p[i] for p in pts) for i in range(3)]; maxs=[max(p[i] for p in pts) for i in range(3)]
 return {'mesh_objects':len(meshes),'triangles':tris,'dimensions_m':[maxs[i]-mins[i] for i in range(3)],'materials':mats}
out=[]
for asset,rev in items:
 root=f'{base}/{asset}/{rev}'; blend=f'{root}/{asset}.blend'; glb=f'{root}/{asset}.glb'
 bpy.ops.wm.open_mainfile(filepath=blend)
 coll=bpy.data.collections.get('EXPORT'); source=mesh_info(list(coll.all_objects) if coll else list(bpy.context.scene.objects))
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
 bpy.ops.import_scene.gltf(filepath=glb)
 imported=mesh_info(list(bpy.context.scene.objects))
 color_deltas={}
 for n,c in source['materials'].items():
  if n in imported['materials']:
   color_deltas[n]=max(abs(a-b) for a,b in zip(c,imported['materials'][n]))
 out.append({'asset':asset,'source':source,'imported_glb':imported,'material_color_max_abs_delta_linear':color_deltas,'colors_equal_within_1e-6':all(v<1e-6 for v in color_deltas.values()) and len(color_deltas)==len(source['materials'])==len(imported['materials'])})
print('QA_COLORS='+json.dumps(out,separators=(',',':')))
