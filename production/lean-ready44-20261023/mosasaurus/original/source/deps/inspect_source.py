# SPDX-License-Identifier: MIT
"""Reopen delivered editable source and verify source-only structural/privacy facts."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
ap=argparse.ArgumentParser();ap.add_argument('--blend',type=Path,required=True);ap.add_argument('--report',type=Path,required=True)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.blend))
C=bpy.data.collections.get('EXPORT');errors=[]
if not C:raise RuntimeError('Missing export collection')
root=bpy.data.objects.get(C['asset_root']);parts=[]
for o in C.all_objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);vol=bm.calc_volume(signed=True);bd=sum(e.is_boundary for e in bm.edges);nm=sum(not e.is_manifold for e in bm.edges);bm.free()
 parts.append({'name':o.name,'signed_volume_m3':vol,'boundary_edges':bd,'nonmanifold_edges':nm,'matrix_determinant':o.matrix_world.to_3x3().determinant()})
 if vol<=0 or bd or nm:errors.append(o.name+' closed outward solid invariant failed')
 if o.parent!=root:errors.append(o.name+' is not a direct semantic child of the identity root')
identity=all(abs(root.matrix_world[r][c]-(1 if r==c else 0))<1e-7 for r in range(4) for c in range(4))
if not identity:errors.append('Nonidentity root')
if any(o.type in {'CAMERA','LIGHT'} for o in bpy.data.objects):errors.append('Preview scene leaked into source')
external_assets={'libraries':len(bpy.data.libraries),'images':len(bpy.data.images),'sounds':len(bpy.data.sounds),'texts':len(bpy.data.texts)}
if any(external_assets.values()):errors.append('Unexpected external-capable datablocks')
# Test constructed prefixes without embedding environment locators in public source.
raw=a.blend.read_bytes();prefixes=[bytes([47])+n.encode()+bytes([47]) for n in ('workspace','root','home','tmp')]
path_hits=[n for n,t in zip(('workspace','root','home','tmp'),prefixes) if t in raw]
if path_hits:errors.append('Unexpected absolute environment prefixes in binary')
rec={'status':'PASS' if not errors else 'FAIL','blend_sha256':hashlib.sha256(raw).hexdigest(),'source_inspector_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'scope':'Reopened source, per-part closed/outward solids and identity transforms, no preview stage, no external assets and limited binary locator scan. Not a boolean union, intersection proof or exhaustive secrets detector.','root_identity':identity,'swimming_mount':True,'mesh_parts':parts,'external_asset_datablocks':external_assets,'binary_environment_prefix_hits':path_hits,'errors':errors}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(rec,indent=2)+'\n')
if errors:raise RuntimeError(errors)
print('SOURCE_REOPEN_PASS',len(parts))
