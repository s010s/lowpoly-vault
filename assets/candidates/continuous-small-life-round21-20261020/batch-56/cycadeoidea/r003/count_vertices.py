from pathlib import Path
import sys,json,hashlib,datetime,bpy
p,out=map(Path,sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(p));deps=bpy.context.evaluated_depsgraph_get();objects=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 ev=o.evaluated_get(deps);mesh=ev.to_mesh()
 objects.append({'name':o.name,'source_vertices':len(o.data.vertices),'evaluated_vertices':len(mesh.vertices),'modifiers':len(o.modifiers)});ev.to_mesh_clear()
out.write_text(json.dumps({'kind':'source-and-evaluated-vertex-counts','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'source_vertices':sum(x['source_vertices'] for x in objects),'evaluated_vertices':sum(x['evaluated_vertices'] for x in objects),'objects':objects},indent=2)+'\n')
