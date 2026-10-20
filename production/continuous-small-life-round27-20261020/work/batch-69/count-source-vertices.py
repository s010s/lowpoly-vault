# SPDX-License-Identifier: MIT
import bpy,json,pathlib,hashlib,datetime,sys
b=pathlib.Path(sys.argv[-1]);bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'));deps=bpy.context.evaluated_depsgraph_get();parts=[]
for o in bpy.data.collections['EXPORT'].all_objects:
 if o.type!='MESH':continue
 e=o.evaluated_get(deps);mesh=e.to_mesh();parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'evaluated_vertices':len(mesh.vertices),'authored_polygons':len(o.data.polygons),'evaluated_polygons':len(mesh.polygons)});e.to_mesh_clear()
d={'kind':'actual-source-vertex-counts','source_sha256':hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),'parts':parts,'authored_vertices':sum(p['authored_vertices'] for p in parts),'evaluated_vertices':sum(p['evaluated_vertices'] for p in parts),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Saved-source read-only reopen measurement; exported POSITION-stream counts separately retained.'};(b/'source-vertex-counts.json').write_text(json.dumps(d,indent=2)+'\n');print(b,d['authored_vertices'])
