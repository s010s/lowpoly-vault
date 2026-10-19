# SPDX-License-Identifier: MIT
"""Fresh read-only selected Blender measurements; never saves, exports, or mutates source files."""
from pathlib import Path
from datetime import datetime, timezone
import bpy, hashlib, json, sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
BASE=ROOT/'production/concept-small-marine-quartet-20261019'
SELECTED={'emeraldella':'r002','burgessia':'r002','tuzoia':'r003','sanctacaris':'r002'}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for asset,revision in SELECTED.items():
    folder=BASE/asset/revision; blend=folder/(asset+'.blend'); glb=folder/(asset+'.glb')
    before={p.name:digest(p) for p in [blend,glb]}
    bpy.context.preferences.filepaths.use_scripts_auto_execute=False
    bpy.ops.wm.open_mainfile(filepath=str(blend),load_ui=False,use_scripts=False)
    bpy.context.view_layer.update()
    meshes=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH']
    points=[];triangles=0;details=[]
    depsgraph=bpy.context.evaluated_depsgraph_get()
    for obj in meshes:
        ev=obj.evaluated_get(depsgraph); mesh=ev.to_mesh(); mesh.calc_loop_triangles()
        pts=[ev.matrix_world @ v.co for v in mesh.vertices]
        points.extend(tuple(p) for p in pts); triangles+=len(mesh.loop_triangles)
        details.append({'object':obj.name,'authored_vertices':len(obj.data.vertices),'authored_polygon_faces':len(obj.data.polygons),'evaluated_triangles':len(mesh.loop_triangles),'material_names':[s.material.name if s.material else None for s in obj.material_slots]})
        ev.to_mesh_clear()
    lo=[min(p[i] for p in points) for i in range(3)]; hi=[max(p[i] for p in points) for i in range(3)]
    after={p.name:digest(p) for p in [blend,glb]}; assert before==after
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'asset_id':asset,'revision':revision,'blender_version':bpy.app.version_string,'unit_scale':bpy.context.scene.unit_settings.scale_length,'source_path':str(blend.relative_to(ROOT)),'read_only':True,'scripts_auto_execute':False,'source_saved':False,'export_run':False,'authored_vertices':sum(len(o.data.vertices) for o in meshes),'authored_polygon_faces':sum(len(o.data.polygons) for o in meshes),'mesh_objects':len(meshes),'evaluated_triangles':triangles,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]},'expected_glb_bounds_m':{'min':[lo[0],lo[2],-hi[1]],'max':[hi[0],hi[2],-lo[1]]},'hashes_before':before,'hashes_after':after,'model_bytes_unchanged':before==after,'objects':details,'limitations':'Direct source counts and evaluated world bounds only; no formal visual, factual, profile, hardware, performance, scene, or release acceptance.'}
    output=OUT/(asset+'-fresh-blender-source.json'); assert not output.exists(); output.write_text(json.dumps(report,indent=2)+'\n')
    print(asset,triangles,report['authored_vertices'],report['authored_polygon_faces'])
