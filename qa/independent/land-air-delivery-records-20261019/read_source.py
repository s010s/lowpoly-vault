# SPDX-License-Identifier: MIT
"""Independent read-only source measurements. Writes only adjacent audit evidence."""
from pathlib import Path
from datetime import datetime, timezone
import bpy, hashlib, json, sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'scripts/qa_glb.py').is_file())
BASE=ROOT/'production/concept-small-land-air-20261019'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for asset in ['sapeornis','longirostravis','dunbaria','chimerarachne']:
    folder=BASE/asset/'r001/output'/asset; blend=folder/(asset+'.blend');glb=folder/(asset+'.glb')
    before={p.name:digest(p) for p in (blend,glb)}
    bpy.context.preferences.filepaths.use_scripts_auto_execute=False
    bpy.ops.wm.open_mainfile(filepath=str(blend),load_ui=False,use_scripts=False)
    bpy.context.view_layer.update()
    cols=[c for c in bpy.data.collections if c.get('asset_root')]; assert len(cols)==1
    col=cols[0]; meshes=[o for o in col.all_objects if o.type=='MESH']
    points=[]; triangles=0; details=[];materials={};depsgraph=bpy.context.evaluated_depsgraph_get()
    for obj in meshes:
        ev=obj.evaluated_get(depsgraph); mesh=ev.to_mesh();mesh.calc_loop_triangles()
        points.extend(tuple(ev.matrix_world @ v.co) for v in mesh.vertices);triangles+=len(mesh.loop_triangles)
        used={p.material_index for p in mesh.polygons}
        details.append({'object':obj.name,'authored_vertices':len(obj.data.vertices),'authored_polygon_faces':len(obj.data.polygons),'evaluated_triangles':len(mesh.loop_triangles),'material_names':[s.material.name if s.material else None for s in obj.material_slots],'used_material_indices':sorted(used),'modifiers':[m.type for m in obj.modifiers]})
        for i in used:
            mat=mesh.materials[i]
            if mat:
                pbs=[n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'] if mat.use_nodes else []
                materials[mat.name]={'base_color':list(pbs[0].inputs['Base Color'].default_value) if len(pbs)==1 else list(mat.diffuse_color),'roughness':pbs[0].inputs['Roughness'].default_value if len(pbs)==1 else mat.roughness,'metallic':pbs[0].inputs['Metallic'].default_value if len(pbs)==1 else mat.metallic}
        ev.to_mesh_clear()
    lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
    after={p.name:digest(p) for p in (blend,glb)}; assert before==after
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'asset_id':asset,'revision':'r001','blender_version':bpy.app.version_string,'unit_scale':bpy.context.scene.unit_settings.scale_length,'source_path':str(blend.relative_to(ROOT)),'read_only':True,'scripts_auto_execute':False,'source_saved':False,'export_run':False,'export_collection':col.name,'authored_vertices':sum(len(o.data.vertices) for o in meshes),'authored_polygon_faces':sum(len(o.data.polygons) for o in meshes),'mesh_objects':len(meshes),'evaluated_triangles':triangles,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]},'expected_glb_bounds_m':{'min':[lo[0],lo[2],-hi[1]],'max':[hi[0],hi[2],-lo[1]]},'hashes_before':before,'hashes_after':after,'model_bytes_unchanged':True,'used_materials':materials,'objects':details,'scope':'Raw evaluated source measurements only; no formal visual/factual/profile/hardware/performance/scene/release acceptance.'}
    output=OUT/(asset+'-fresh-blender-source.json');assert not output.exists();output.write_text(json.dumps(report,indent=2)+'\n')
    print(asset,triangles,report['authored_vertices'],report['authored_polygon_faces'],len(materials))
