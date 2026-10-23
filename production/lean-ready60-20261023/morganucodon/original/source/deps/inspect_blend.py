# SPDX-License-Identifier: MIT
import bpy,sys,json,hashlib
from pathlib import Path
argv=sys.argv[sys.argv.index('--')+1:];src=Path(argv[0]);out=Path(argv[1]);bpy.ops.wm.open_mainfile(filepath=str(src))
C=bpy.data.collections['EXPORT'];r=bpy.data.objects[C['asset_root']]
meshes=[o for o in C.all_objects if o.type=='MESH'];foreign=[o.name for o in bpy.data.objects if o.type in {'CAMERA','LIGHT'}]
external=[p for p in bpy.utils.blend_paths() if p and not p.startswith('//')]
assert len(meshes)==20 and not foreign and not external
assert all(not o.modifiers for o in meshes)
assert all(abs(r.matrix_world[i][j]-(1 if i==j else 0))<1e-8 for i in range(4) for j in range(4))
report={'status':'PASS','source_blend_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'editable_mesh_count':len(meshes),'editable_semantic_parts':[o.name for o in meshes],'camera_light_objects':foreign,'external_resource_paths':external,'unit_scale':bpy.context.scene.unit_settings.scale_length,'identity_export_root':True,'all_geometry_editable':True,'all_materials_node_based':all(m.use_nodes for m in bpy.data.materials),'scope':'Reopened source checks; overlapping anatomical component joins are intentional, not a watertight union claim.'}
out.write_text(json.dumps(report,indent=2)+'\n')
