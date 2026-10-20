# SPDX-License-Identifier: MIT
import bpy,json,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());B=R/'production/continuous-small-life-round19-20261020/work/batch-54';A=R/'assets/candidates/continuous-small-life-round19-20261020/batch-54';records=[]
for slug,rev in json.loads((B/'current-revisions.json').read_text()).items():
 p=A/slug/rev/(slug+'.blend');bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);C=[c for c in bpy.data.collections if c.get('asset_root')][0];objects=[o for o in C.all_objects if o.type=='MESH'];data={o.data.as_pointer():o.data for o in objects};deps=bpy.context.evaluated_depsgraph_get();parts=[]
 for o in objects:
  e=o.evaluated_get(deps);m=e.to_mesh();parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'evaluated_vertices':len(m.vertices),'modifiers':[m.name for m in o.modifiers]});e.to_mesh_clear()
 records.append({'asset_id':slug,'revision':rev,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'authored_source_vertices_distinct_mesh_datablocks':sum(len(m.vertices) for m in data.values()),'evaluated_source_vertices_per_unique_object_variant':sum(x['evaluated_vertices'] for x in parts),'mesh_object_instances':len(objects),'distinct_mesh_datablocks':len(data),'parts':parts})
(B/'source-vertex-counts.json').write_text(json.dumps({'created_at':datetime.now(timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'method':'Read-only saved Blend load, distinct authored datablock counts and dependency-graph evaluated mesh counts. No source saved or exported. No modifiers or shared mesh instances in these candidates.','records':records},indent=2)+'\n')
