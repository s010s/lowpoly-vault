# SPDX-License-Identifier: MIT
import bpy,json,pathlib,hashlib,datetime,sys
b=pathlib.Path(sys.argv[-1]);bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'));deps=bpy.context.evaluated_depsgraph_get();parts=[]
for o in bpy.data.collections['EXPORT'].all_objects:
 if o.type!='MESH':continue
 o.data.calc_loop_triangles();e=o.evaluated_get(deps);mesh=e.to_mesh();mesh.calc_loop_triangles();parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'evaluated_vertices':len(mesh.vertices),'authored_polygons':len(o.data.polygons),'evaluated_polygons':len(mesh.polygons),'authored_triangles':len(o.data.loop_triangles),'evaluated_triangles':len(mesh.loop_triangles)});e.to_mesh_clear()
d={'kind':'actual-source-vertex-counts','source_sha256':hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),'parts':parts,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Actual read-only source reopen; authored/evaluated/exported streams counted separately.'}
for k in ['authored_vertices','evaluated_vertices','authored_polygons','evaluated_polygons','authored_triangles','evaluated_triangles']:d[k]=sum(p[k] for p in parts)
(b/'source-vertex-counts.json').write_text(json.dumps(d,indent=2)+'\n');print(b,d['authored_vertices'])
