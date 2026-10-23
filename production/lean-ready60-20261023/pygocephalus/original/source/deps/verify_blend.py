# SPDX-License-Identifier: MIT
"""Read-only semantic and geometric inspection of an editable delivered blend."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--blend',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(args)
bpy.ops.wm.open_mainfile(filepath=str(a.blend),load_ui=False)
assert not [o for o in bpy.data.objects if o.type in {'CAMERA','LIGHT'}]
assert not bpy.data.texts and not bpy.data.images
col=bpy.data.collections['EXPORT'];root=bpy.data.objects[col['asset_root']]
assert all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))
meshes=[o for o in col.objects if o.type=='MESH'];groups={}
for o in meshes: groups.setdefault(o['semantic_part'],[]).append(o.name)
assert len(groups['walking-thoracopod'])==12
assert len(groups['compact-thoracopod'])==4
assert len(groups['compact-feeding-base'])==4
assert len(groups['pleonal-segment'])==6
assert len(groups['telson-lobe-pair-1'])==2 and len(groups['telson-lobe-pair-2'])==2
assert len(groups['uropod-blade'])==4
assert len(groups['thoracic-sternite'])==8
assert len(groups['continuous-pleonal-axis'])==1
volumes=[]
for o in meshes:
 bm=bmesh.new();bm.from_mesh(o.data);volume=bm.calc_volume(signed=True)
 assert volume>0,(o.name,volume)
 assert all(e.is_manifold for e in bm.edges),o.name
 volumes.append({'part':o.name,'signed_volume_m3':volume,'closed_manifold':True});bm.free()
shield=bpy.data.objects['Shield-measured-GSC12858'];bounds={}
for ax,label in enumerate('xyz'):bounds[label]=[min(v.co[ax] for v in shield.data.vertices),max(v.co[ax] for v in shield.data.vertices)]
assert abs(bounds['x'][1]-bounds['x'][0]-.020310)<1e-8
assert abs(bounds['y'][1]-bounds['y'][0]-.017788)<1e-8
a.out.write_text(json.dumps({'status':'PASS','blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),'checks':['Editable source has no presentation rig, images or Text blocks','Source identity root','Semantic counts read from actual saved blend','Each intended closed solid is manifold and has positive signed volume','Measured shield length and width checked from actual vertices'],'shield_bounds_m':bounds,'semantic_groups':groups,'closed_solid_volumes':volumes,'limitations':['Ventral parts inspected by source geometry and semantic grouping without an additional image.','Manifold separate components and positive volume do not certify a fused printable union. Intentional overlaps at articulated joins remain.','This is maker technical inspection, not independent anatomy acceptance.']},indent=2)+'\n')
