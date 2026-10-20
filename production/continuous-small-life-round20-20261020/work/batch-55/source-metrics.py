# SPDX-License-Identifier: MIT
import bpy,sys,json,hashlib,argparse,bmesh
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.source),load_ui=False,use_scripts=False)
dg=bpy.context.evaluated_depsgraph_get();parts=[]
for o in bpy.data.collections['EXPORT'].all_objects:
 if o.type!='MESH':continue
 eo=o.evaluated_get(dg);m=eo.to_mesh();bm=bmesh.new();bm.from_mesh(m);m.calc_loop_triangles()
 parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'evaluated_vertices':len(m.vertices),'triangles':len(m.loop_triangles),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True)})
 bm.free();eo.to_mesh_clear()
a.out.write_text(json.dumps({'source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'parts':parts,'authored_vertices':sum(x['authored_vertices'] for x in parts),'evaluated_vertices':sum(x['evaluated_vertices'] for x in parts),'unit_scale':bpy.context.scene.unit_settings.scale_length,'source_saved':False},indent=2))
