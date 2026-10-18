# SPDX-License-Identifier: MIT
import bpy,bmesh,sys,json,hashlib,math
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];source=Path(args[0]);out=Path(args[1]);bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);dg=bpy.context.evaluated_depsgraph_get();c=bpy.data.collections['EXPORT'];parts=[]
for o in c.all_objects:
 if o.type!='MESH':continue
 ev=o.evaluated_get(dg);m=ev.to_mesh();bm=bmesh.new();bm.from_mesh(m)
 parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'evaluated_vertices':len(m.vertices),'authored_polygons':len(o.data.polygons),'modifiers':[x.type for x in o.modifiers],'nonfinite_vertex_normals':sum(not all(math.isfinite(x) for x in v.normal) for v in m.vertices),'nonpositive_face_area':sum(p.area<=0 for p in m.polygons),'signed_volume_m3':bm.calc_volume(signed=True),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'scale':list(o.scale)})
 bm.free();ev.to_mesh_clear()
root=bpy.data.objects[c['asset_root']];report={'check':'source-mesh-measurements','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'blender':bpy.app.version_string,'unit_scale_length':bpy.context.scene.unit_settings.scale_length,'root_world_matrix':[list(row) for row in root.matrix_world],'parts':parts,'authored_vertices':sum(p['authored_vertices'] for p in parts),'evaluated_vertices':sum(p['evaluated_vertices'] for p in parts),'nonfinite_vertex_normals':sum(p['nonfinite_vertex_normals'] for p in parts),'nonpositive_face_area':sum(p['nonpositive_face_area'] for p in parts),'source_saved':False};out.write_text(json.dumps(report,indent=2)+'\n')
assert not report['nonfinite_vertex_normals'] and not report['nonpositive_face_area']
