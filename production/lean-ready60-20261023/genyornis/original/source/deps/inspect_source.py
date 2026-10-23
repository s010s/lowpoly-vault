# SPDX-License-Identifier: MIT
"""Read-only source-artifact topology, anatomy inventory, and closure evidence."""
from pathlib import Path
import hashlib,json,sys
import bpy,bmesh
args=sys.argv[sys.argv.index('--')+1:];root=Path(args[0]);bpy.ops.wm.open_mainfile(filepath=str(root/'model.blend'))
col=bpy.data.collections['EXPORT'];parts=[]
for ob in col.all_objects:
    if ob.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(ob.data);vol=bm.calc_volume(signed=True);nonman=sum(not e.is_manifold for e in bm.edges);bm.free()
    coords=[v.co for v in ob.data.vertices];dims=[max(v[i] for v in coords)-min(v[i] for v in coords) for i in range(3)]
    parts.append({'name':ob.name,'signed_volume_m3':vol,'nonmanifold_edges':nonman,'bounds_dimensions_xyz_m':dims})
assert all(p['signed_volume_m3']>0 and p['nonmanifold_edges']==0 for p in parts)
assert len([p for p in parts if p['name'].startswith('wing-')])==2
assert len([p for p in parts if p['name'].startswith('toe-')])==6
assert len([p for p in parts if p['name'].startswith('hoof-claw-')])==6
assert not any(o.type in {'CAMERA','LIGHT'} for o in bpy.data.objects)
assert not bpy.data.images and not bpy.data.libraries
report={'status':'PASS','claim_scope':'Saved editable source is independent of presentation scene; closed outward-facing individual components, not a union or printable manifold claim. Intentional anatomical overlaps at body/neck/wing/limb attachments remain subject to independent visual inspection.',
'blend_sha256':hashlib.sha256((root/'model.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((root/'model.glb').read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'external_libraries':0,'external_images':0,'presentation_objects':0,'parts':parts,
'factual_limits':'Nominal measured rostrum/casque dimensions constrain a soft-tissue interpretation. Complete head/body height, neck pose, feathers, skin coverage and colors are estimates, not measurements of an articulated individual.'}
(root/'qa/evidence/source-inspection.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','closed_positive_volume_parts':len(parts)}))
