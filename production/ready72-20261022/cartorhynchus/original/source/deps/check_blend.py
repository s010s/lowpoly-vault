# SPDX-License-Identifier: MIT
"""Reopen the shipped editable scene and inspect actual data, not a generator assertion."""
from pathlib import Path
import bpy,bmesh,json,hashlib,sys
args=sys.argv[sys.argv.index('--')+1:]; blend=Path(args[0]);out=Path(args[1])
bpy.ops.wm.open_mainfile(filepath=str(blend))
C=bpy.data.collections.get('EXPORT');assert C is not None
root=bpy.data.objects.get('cartorhynchus');assert root is not None
assert all(abs(root.matrix_world[r][c]-(1 if r==c else 0))<1e-8 for r in range(4) for c in range(4))
assert not [o for o in bpy.data.objects if o.type in ['CAMERA','LIGHT']]
assert not any(c.name.startswith('_PREVIEW') for c in bpy.data.collections)
assert bpy.context.scene.unit_settings.scale_length==1
parts=[]
for ob in C.objects:
 if ob.type!='MESH':continue
 assert ob.parent==root
 assert ob.matrix_world.to_3x3().determinant()>0
 bm=bmesh.new();bm.from_mesh(ob.data)
 boundaries=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True)
 assert boundaries==0 and nonmanifold==0 and volume>0
 bm.free();parts.append({'name':ob.name,'vertices':len(ob.data.vertices),'boundary_edges':boundaries,'nonmanifold_edges':nonmanifold,'signed_volume_m3':volume,'vertex_groups':[v.name for v in ob.vertex_groups]})
assert len(parts)==6
out.write_text(json.dumps({'status':'PASS','claim_scope':'Editable source reopening, semantic parts, identity root, metre scale, no preview scene, closed part manifolds and positive signed part volumes; overlapping attachments intentionally not a printable union','blend_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),'parts':parts,'preview_objects':0,'external_images':len(bpy.data.images),'external_libraries':len(bpy.data.libraries)},indent=2)+'\n')
