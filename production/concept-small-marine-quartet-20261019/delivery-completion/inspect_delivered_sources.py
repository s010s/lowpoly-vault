# SPDX-License-Identifier: MIT
"""Read the exact delivered sources; do not save or export. Current measurements only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
import bpy
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
from check_source_export import compare_source_audit
BASE=HERE.parent
for asset,revision in [('emeraldella','r002'),('burgessia','r002'),('tuzoia','r003'),('sanctacaris','r002')]:
 d=BASE/asset/revision;blend=d/(asset+'.blend');glb=d/(asset+'.glb')
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (blend,glb)}
 start=datetime.now(timezone.utc).isoformat()
 bpy.context.preferences.filepaths.use_scripts_auto_execute=False
 bpy.ops.wm.open_mainfile(filepath=str(blend),load_ui=False,use_scripts=False)
 col=bpy.data.collections['EXPORT'];source=audit_source(col,max_triangles=16000);export=audit_glb(glb,max_triangles=16000,max_materials=7,max_primitives=220)
 comparison=compare_source_audit(source,export,before[blend.name],before[glb.name])
 authored={'vertices':sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH'),'polygon_faces':sum(len(o.data.polygons) for o in col.all_objects if o.type=='MESH')}
 after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (blend,glb)}
 assert before==after and not source['errors'] and not export['errors'] and comparison['status']=='pass'
 record={'asset_id':asset,'revision':revision,'started_at':start,'finished_at':datetime.now(timezone.utc).isoformat(),'measurement_scope':'fresh read-only source audit and exact GLB comparison; not formal stage acceptance','source':source,'authored':authored,'source_export':comparison,'blender_version':bpy.app.version_string,'blender_unit_scale':bpy.context.scene.unit_settings.scale_length,'hashes_before':before,'hashes_after':after,'model_bytes_unchanged':before==after}
 (HERE/'evidence'/(asset+'-source.json')).write_text(json.dumps(record,indent=2)+'\n')
