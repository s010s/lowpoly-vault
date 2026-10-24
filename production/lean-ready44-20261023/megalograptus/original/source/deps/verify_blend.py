# SPDX-License-Identifier: MIT
"""Read the actual editable blend; inspect semantic counts and closed source solids."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
p=argparse.ArgumentParser();p.add_argument('--blend',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.open_mainfile(filepath=str(a.blend),load_ui=False)
assert not [o for o in bpy.data.objects if o.type in {'CAMERA','LIGHT'}]
assert not bpy.data.images and not bpy.data.texts
col=bpy.data.collections['EXPORT'];root=bpy.data.objects[col['asset_root']]
assert all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))
groups={};volumes=[]
for o in col.objects:
 if o.type!='MESH':continue
 groups.setdefault(o['semantic_part'],[]).append(o.name)
 bm=bmesh.new();bm.from_mesh(o.data);v=bm.calc_volume(signed=True);assert v>0,(o.name,v);assert all(e.is_manifold for e in bm.edges),o.name
 volumes.append({'part':o.name,'signed_volume_m3':v,'closed_manifold':True});bm.free()
expected={'carapace':1,'compound-eye':2,'ocellus':2,'metastoma':1,'appendage-I':2,'appendage-II':2,'appendage-III-base':2,'appendage-III-distal':2,'hypertrophied-III-spine':4,'appendage-IV':2,'appendage-V':2,'appendage-VI-stalk':2,'appendage-VI-paddle':2,'mesosoma-segment':7,'metasoma-segment':4,'pretelson':1,'telson':1,'cercal-blade':2}
for k,n in expected.items():assert len(groups[k])==n,(k,len(groups[k]),n)
head=bpy.data.objects['Compact-rounded-headshield'];hx=[v.co.x for v in head.data.vertices];hy=[v.co.y for v in head.data.vertices]
assert abs(max(hx)-min(hx)-.14)<1e-7;assert abs(max(hy)-min(hy)-.1)<1e-7
term=bpy.data.objects['Central-straight-telson'];tail_y=max(v.co.y for v in term.data.vertices);axial=tail_y-min(hy);assert abs(axial-.75)<.001
longspines=[]
for name in groups['hypertrophied-III-spine']:
 o=bpy.data.objects[name];v=[x.co for x in o.data.vertices];extent=max((x-y).length for x in v for y in v)
 assert .12<extent<.14;longspines.append({'part':name,'maximum_extent_m':extent,'endpoint_angles':'inferred, not a measurement'})
a.out.write_text(json.dumps({'status':'PASS','blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),'checks':['Saved source contains no presentation rig, image datablocks or Text blocks','Root is identity transform','Semantic anatomy counts read from actual saved mesh objects','All intended source solids have manifold topology and positive signed volume','Headshield 0.14 m wide and 0.10 m long; approximate axial body length 0.75 m','Four conspicuous appendage III spines are approximately 0.13 m long'],'axial_body_extent_m':axial,'expected_semantic_counts':expected,'semantic_groups':groups,'long_spines':longspines,'closed_solid_volumes':volumes,'limitations':['Counts and volume are maker technical evidence, not independent anatomical acceptance.','Anatomical joins intentionally overlap; this is not a fused printable union.','The live depth, posture and spinal endpoint angles are inferred.','Coxa III restoration and six appendage systems are semantic interpretations of the scientific reconstruction.']},indent=2)+'\n')
