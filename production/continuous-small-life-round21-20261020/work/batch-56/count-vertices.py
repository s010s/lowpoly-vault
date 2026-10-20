# SPDX-License-Identifier: MIT
import bpy,json,hashlib,pathlib
R=pathlib.Path.cwd();W=R/'production/continuous-small-life-round21-20261020/work/batch-56'
for a in json.loads((W/'final-selection.json').read_text()):
 b=R/a['path'];bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'),load_ui=False);dep=bpy.context.evaluated_depsgraph_get();authored=evaluated=0
 for o in bpy.data.collections['EXPORT'].all_objects:
  if o.type!='MESH':continue
  authored+=len(o.data.vertices);e=o.evaluated_get(dep);mesh=e.to_mesh();evaluated+=len(mesh.vertices);e.to_mesh_clear()
 metrics=json.loads((b/'metrics.json').read_text())['glb'];report={'source_sha256':hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),'authored_vertices':authored,'evaluated_vertices':evaluated,'exported_position_stream_vertices':metrics['unique_position_accessor_vertices'],'note':'Authoring/evaluated counts measured by reopened Blend data API. Exported count recorded by static GLB audit, not derived by ratio.'};(b/'vertex-counts.report.json').write_text(json.dumps(report,indent=2)+'\n');print(a['asset_id'],report)
