#!/usr/bin/env python3
"""Reopen an exact pinned GLB in Blender and compare imported geometry to GLB audit."""
import bpy, json, sys, hashlib
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
glb=Path(args[0]).resolve(); out=Path(args[1]).resolve()
sha=hashlib.sha256(glb.read_bytes()).hexdigest()
repo=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(repo/'scripts'))
from qa_glb import audit_glb
expected=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
# Factory startup leaves a default cube; remove defaults so only imported GLB content is measured.
for obj in list(bpy.data.objects): bpy.data.objects.remove(obj, do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
scene=bpy.context.scene; dg=bpy.context.evaluated_depsgraph_get()
objs=[o for o in scene.objects if o.type=='MESH']
materials=set(); parts=[]; tri_total=0
mins=[float('inf')]*3; maxs=[float('-inf')]*3
for obj in objs:
    obj_eval=obj.evaluated_get(dg); mesh=obj_eval.to_mesh(); mesh.calc_loop_triangles()
    ntri=len(mesh.loop_triangles); tri_total+=ntri
    for mat in mesh.materials:
        if mat: materials.add(mat.name)
    for vert in mesh.vertices:
        v=obj_eval.matrix_world @ vert.co
        xyz=(v.x,v.y,v.z)
        for i,c in enumerate(xyz): mins[i]=min(mins[i],c); maxs[i]=max(maxs[i],c)
    parts.append({'object':obj.name,'vertices':len(mesh.vertices),'triangles':ntri,'materials':[m.name for m in mesh.materials if m]})
    obj_eval.to_mesh_clear()
# The importer maps GLB Y-up coordinates to Blender Z-up; invert that mapping for direct bounds comparison.
gltf_min=[mins[0],mins[2],-maxs[1]]; gltf_max=[maxs[0],maxs[2],-mins[1]]
actual_size=[gltf_max[i]-gltf_min[i] for i in range(3)]
expected_bounds=expected.get('bounds_m',{})
errors=[]
if expected['status']!='pass': errors.append('Pinned GLB static audit did not pass')
if tri_total!=expected.get('scene_triangles'): errors.append('Blender imported triangle count differs from exact GLB scene count')
if len(materials)!=expected.get('materials'): errors.append('Blender imported material count differs from exact GLB material count')
if expected_bounds:
  delta=max(abs([gltf_min,gltf_max][j][i]-expected_bounds[side][i]) for j,side in enumerate(('min','max')) for i in range(3))
  if delta>1e-6: errors.append(f'Blender-imported bounds differ from GLB audit by {delta} m')
else: delta=None; errors.append('Exact GLB audit did not provide bounds')
report={'check':'blender_glb_reopen_import','status':'pass' if objs and tri_total>0 and not errors else 'fail','errors':errors,'glb_sha256':sha,'glb_path':str(glb),'blender_version':bpy.app.version_string,'scene_mesh_objects':len(objs),'triangles':tri_total,'materials':sorted(materials),'bounds_blender_z_up_m':{'min':mins,'max':maxs,'size':[maxs[i]-mins[i] for i in range(3)]},'bounds_gltf_y_up_m':{'min':gltf_min,'max':gltf_max,'size':actual_size},'comparison':{'static_glb_triangles':expected.get('scene_triangles'),'static_glb_materials':expected.get('materials'),'static_glb_bounds_m':expected_bounds,'bounds_max_error_m':delta,'bounds_tolerance_m':1e-6},'parts':parts,'limitations':'Verifies Blender GLTF importer can reopen the exact standalone GLB and matches the GLB static geometry/material/bounds audit. Does not export a replacement or establish visual/factual/GPU/target-scene acceptance.'}
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if report['status']!='pass': raise RuntimeError('; '.join(errors))
