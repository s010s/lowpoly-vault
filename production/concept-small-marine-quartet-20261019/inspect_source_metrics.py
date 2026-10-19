# SPDX-License-Identifier: MIT
"""Read saved selected sources without edits; report authored/evaluated topology."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import bpy
HERE=Path(__file__).resolve().parent
for slug,rev in [('emeraldella','r002'),('burgessia','r002'),('tuzoia','r003'),('sanctacaris','r002')]:
 d=HERE/slug/rev;source=d/(slug+'.blend');bpy.context.preferences.filepaths.use_scripts_auto_execute=False
 bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
 col=bpy.data.collections['EXPORT'];meshes=[o for o in col.all_objects if o.type=='MESH'];bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 authored={'vertices':sum(len(o.data.vertices) for o in meshes),'polygon_faces':sum(len(o.data.polygons) for o in meshes)};evaluated={'vertices':0,'polygon_faces':0,'triangles':0}
 for o in meshes:
  e=o.evaluated_get(dg);m=e.to_mesh();m.calc_loop_triangles();evaluated['vertices']+=len(m.vertices);evaluated['polygon_faces']+=len(m.polygons);evaluated['triangles']+=len(m.loop_triangles);e.to_mesh_clear()
 record={'asset_id':slug,'revision':rev,'created_at':datetime.now(timezone.utc).isoformat(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'authored':authored,'evaluated':evaluated,'mesh_parts':len(meshes),'modifiers':sum(len(o.modifiers) for o in meshes),'source_sha256_after':hashlib.sha256(source.read_bytes()).hexdigest()}
 record['source_unchanged']=record['source_sha256']==record['source_sha256_after']
 (d/'source-topology.json').write_text(json.dumps(record,indent=2)+'\n')
