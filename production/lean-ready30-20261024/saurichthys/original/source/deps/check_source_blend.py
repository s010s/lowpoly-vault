# SPDX-License-Identifier: MIT
"""Reopen the exact editable blend and verify its retained data closure."""
import hashlib,json,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source
args=sys.argv[sys.argv.index('--')+1:]; blend=Path(args[0]); out=Path(args[1]); expected=hashlib.sha256(blend.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(blend.resolve()))
col=bpy.data.collections.get('EXPORT'); audit=audit_source(col,max_triangles=18000)
images=[x.name for x in bpy.data.images if x.type!='RENDER_RESULT']
external=[x.name for x in bpy.data.libraries]
non_asset=[o.name for o in bpy.data.objects if o.name not in col.all_objects]
non_mesh=[o.name for o in bpy.data.objects if o.type not in ['EMPTY','MESH']]
errors=list(audit['errors'])
if images or external or non_asset or non_mesh: errors.append('Unexpected external or presentation data')
report={'status':'PASS' if not errors else 'FAIL','blend_sha256':expected,'blender_version':bpy.app.version_string,'export_objects':len(col.all_objects),'source_audit':audit,'external_libraries':external,'image_datablocks':images,'non_asset_objects':non_asset,'non_mesh_or_empty':non_mesh,'errors':errors,'scope':'Exact saved editable source reopened; no camera, light, stage, external image or linked library; source mesh audit only, not independent visual review.'}
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if errors: raise RuntimeError(errors)
