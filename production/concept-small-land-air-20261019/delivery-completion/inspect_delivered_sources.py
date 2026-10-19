# SPDX-License-Identifier: MIT
"""Fresh read-only measurements; never save the source or export a model."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys
import bpy
HERE=Path(__file__).resolve().parent; BASE=HERE.parent
REPO=next(p for p in HERE.parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
from check_source_export import compare_source_audit
for asset in ['sapeornis','longirostravis','dunbaria','chimerarachne']:
 d=BASE/asset/'r001/output'/asset; blend=d/(asset+'.blend'); glb=d/(asset+'.glb')
 digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 before={p.name:digest(p) for p in (blend,glb)}; start=datetime.now(timezone.utc).isoformat()
 bpy.context.preferences.filepaths.use_scripts_auto_execute=False
 bpy.ops.wm.open_mainfile(filepath=str(blend),load_ui=False,use_scripts=False)
 bpy.context.view_layer.update()
 cols=[c for c in bpy.data.collections if c.get('asset_root')]
 assert len(cols)==1, [c.name for c in cols]
 col=cols[0]; source=audit_source(col,max_triangles=16000)
 export=audit_glb(glb,max_triangles=16000,max_materials=8,max_primitives=160)
 comparison=compare_source_audit(source,export,before[blend.name],before[glb.name])
 authored={'vertices':sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH'),'polygon_faces':sum(len(o.data.polygons) for o in col.all_objects if o.type=='MESH')}
 after={p.name:digest(p) for p in (blend,glb)}
 assert before==after and not source['errors'] and not export['errors'] and comparison['status'] in ('pass','pass_with_warnings'), comparison
 record={'asset_id':asset,'revision':'r001','started_at':start,'finished_at':datetime.now(timezone.utc).isoformat(),'measurement_scope':'fresh read-only source audit and exact GLB comparison; not formal stage acceptance','source':source,'authored':authored,'source_export':comparison,'export_collection':col.name,'script_autoexec':False,'source_saved':False,'blender_version':bpy.app.version_string,'blender_unit_scale':bpy.context.scene.unit_settings.scale_length,'hashes_before':before,'hashes_after':after,'model_bytes_unchanged':before==after}
 (HERE/'evidence'/(asset+'-source.json')).write_text(json.dumps(record,indent=2)+'\n')
 print(asset,comparison['status'],authored)
