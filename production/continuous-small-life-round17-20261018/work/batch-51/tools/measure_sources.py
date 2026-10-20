# SPDX-License-Identifier: MIT
import sys,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
import bpy
from mathutils import Vector
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/qa_glb.py').is_file());sys.path.insert(0,str(R/'scripts'));from qa_glb import audit_glb
A=R/'assets/candidates/continuous-small-life-round17-20261018/batch-51'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for aid,rev in [('dicranurus','r001'),('calcite-raft-deposit','r002'),('accretionary-lapilli-bed','r002'),('conichnus-conical-burrow','r001')]:
 p=A/aid/rev;source=p/(aid+'.blend');glb=p/(aid+'.glb');bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);deps=bpy.context.evaluated_depsgraph_get();parts=[]
 for o in bpy.data.collections['EXPORT'].all_objects:
  if o.type!='MESH':continue
  ev=o.evaluated_get(deps);mesh=ev.to_mesh();mesh.calc_loop_triangles();parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'authored_polygons':len(o.data.polygons),'evaluated_vertices':len(mesh.vertices),'evaluated_triangles':len(mesh.loop_triangles),'modifiers':[m.type for m in o.modifiers]});ev.to_mesh_clear()
 audit=audit_glb(glb,14000,6,30)
 record={'source_sha256':sha(source),'glb_sha256':sha(glb),'created_at':datetime.now(timezone.utc).isoformat(),'method':'Actual saved Blend reopened with script execution disabled. Authored mesh and depsgraph-evaluated mesh counted separately; exported data independently decoded by qa_glb. No source saved or altered.','blender_version':bpy.app.version_string,'parts':parts,'source_authored_vertices':sum(x['authored_vertices'] for x in parts),'source_evaluated_vertices':sum(x['evaluated_vertices'] for x in parts),'source_evaluated_triangles':sum(x['evaluated_triangles'] for x in parts),'glb_unique_position_stream_vertices':audit['unique_position_accessor_vertices'],'glb_scene_triangles':audit['scene_triangles'],'glb_materials':audit['materials'],'glb_primitives':audit['scene_primitives_estimated_base_draw_calls'],'glb_bytes':audit['bytes'],'dimensions_glb_xyz_m':audit['bounds_m']['size'],'script_sha256':sha(Path(__file__))}
 (p/'source-metrics.json').write_text(json.dumps(record,indent=2)+'\n');md=json.loads((p/'metadata.json').read_text());md['geometry_metrics']=record;md['measurement_report']={'path':str((p/'source-metrics.json').relative_to(R)),'sha256':sha(p/'source-metrics.json')};(p/'metadata.json').write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n')
# Probe negative cavity against clean import of exact GLB, after discarding source scene.
p=A/'conichnus-conical-burrow/r001';glb=p/'conichnus-conical-burrow.glb';bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();hits=[]
for x in [0,.01,.02,.03,.04,.05]:
 hit,point,normal,index,obj,matrix=bpy.context.scene.ray_cast(deps,Vector((x,0,.30)),Vector((0,0,-1)),distance=1)
 hits.append({'x_m':x,'y_m':0,'ray_origin_z_m':.30,'hit':hit,'hit_position_blender_xyz_m':list(point) if hit else None,'normal':list(normal) if hit else None})
report={'kind':'negative-cavity-geometric-probe','glb_sha256':sha(glb),'method':'Clean exact-GLB import; actual downward raycasts at six X offsets in Blender Z-up coordinates. Center hit must lie deeply below outside top. Original model never changed.','created_at':datetime.now(timezone.utc).isoformat(),'hits':hits,'center_depth_below_outer_top_m':hits[-1]['hit_position_blender_xyz_m'][2]-hits[0]['hit_position_blender_xyz_m'][2],'negative_cavity_confirmed':hits[0]['hit_position_blender_xyz_m'][2]<.04 and hits[-1]['hit_position_blender_xyz_m'][2]>.13,'below_base_substrate_m':hits[0]['hit_position_blender_xyz_m'][2]}
(p/'negative-cavity-probe.json').write_text(json.dumps(report,indent=2)+'\n');assert report['negative_cavity_confirmed'];assert sha(glb)==report['glb_sha256']
