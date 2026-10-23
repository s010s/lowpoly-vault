# SPDX-License-Identifier: MIT
"""Reopen editable source and check intended EXPORT scope; invoke via Blender."""
import json,sys,hashlib
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
import asset_common as ac
args=sys.argv[sys.argv.index('--')+1:];source=Path(args[0]);out=Path(args[1])
bpy.ops.wm.open_mainfile(filepath=str(source))
report=ac.audit_source(bpy.data.collections['EXPORT'],16000)
report.update(blend_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),blender_version=bpy.app.version_string,preview_objects_present=any(o.type in {'CAMERA','LIGHT'} or o.name.startswith('_preview') for o in bpy.context.scene.objects),source_only_collections=[c.name for c in bpy.data.collections],packed_images=[i.name for i in bpy.data.images if i.packed_file])
if report['preview_objects_present']:raise RuntimeError('Presentation contamination in saved source')
out.write_text(json.dumps(report,indent=2)+'\n')
