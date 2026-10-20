# SPDX-License-Identifier: MIT
import bpy,sys,json,hashlib,datetime
from pathlib import Path
s,o=map(Path,sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(s.resolve()),load_ui=False,use_scripts=False);deps=bpy.context.evaluated_depsgraph_get();parts=[]
for ob in bpy.data.collections['EXPORT'].all_objects:
 if ob.type!='MESH':continue
 ev=ob.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();parts.append({'name':ob.name,'authored_vertices':len(ob.data.vertices),'authored_polygons':len(ob.data.polygons),'evaluated_vertices':len(me.vertices),'evaluated_triangles':len(me.loop_triangles)});ev.to_mesh_clear()
o.write_text(json.dumps({'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_reopened':True,'source_saved':False,'authored_vertices':sum(p['authored_vertices'] for p in parts),'evaluated_vertices':sum(p['evaluated_vertices'] for p in parts),'authored_polygons':sum(p['authored_polygons'] for p in parts),'evaluated_triangles':sum(p['evaluated_triangles'] for p in parts),'parts':parts},indent=2)+'\n')
