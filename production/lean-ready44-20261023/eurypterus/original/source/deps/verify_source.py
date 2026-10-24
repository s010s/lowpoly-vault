# SPDX-License-Identifier: MIT
"""Reopen the delivered source and measure its actual semantic anatomy and solid geometry."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
p=argparse.ArgumentParser();p.add_argument('--blend',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);bpy.ops.wm.open_mainfile(filepath=str(a.blend),load_ui=False)
assert not [o for o in bpy.data.objects if o.type in {'CAMERA','LIGHT'}];assert not bpy.data.texts and not bpy.data.images and not bpy.data.libraries
col=bpy.data.collections['EXPORT'];root=bpy.data.objects[col['asset_root']];assert all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))
groups={};vol=[]
for ob in col.objects:
 if ob.type!='MESH':continue
 groups.setdefault(ob['semantic_part'],[]).append(ob.name)
 bm=bmesh.new();bm.from_mesh(ob.data);volume=bm.calc_volume(signed=True);assert volume>0,(ob.name,volume);assert all(e.is_manifold for e in bm.edges),ob.name
 vol.append({'name':ob.name,'signed_volume_m3':volume,'closed_manifold':True});bm.free()
expected={'carapace':1,'chelicera':2,'chelicera-fixed-finger':2,'chelicera-moving-finger':2,'trunk-tergite':12,'telson':1,'walking-terminal':8,'walking-podomere':24,'paddle-stalk':8,'swimming-paddle':2,'lateral-eye':2,'median-ocellus':2,'metastoma':1,'operculum':1,'type-A-appendage':1}
for k,v in expected.items():assert len(groups.get(k,[]))==v,(k,groups.get(k))
head=bpy.data.objects['Carapace-remipes-embayed-margin'];tel=bpy.data.objects['Straight-slender-telson'];front=min(v.co.y for v in head.data.vertices);rear=max(v.co.y for v in tel.data.vertices);L=rear-front
assert abs(L-.200)<1e-7;assert abs((max(v.co.y for v in head.data.vertices)-front)-.033)<1e-7
tergites=[bpy.data.objects[n] for n in groups['trunk-tergite']];assert sorted(ob['segment_index'] for ob in tergites)==list(range(1,13))
assert sum(ob['trunk_region']=='preabdomen' for ob in tergites)==6;assert sum(ob['trunk_region']=='postabdomen' for ob in tergites)==6
assert max(abs(v.co.x) for v in tel.data.vertices)<=.00346
lowest=min(v.co.z for ob in col.objects if ob.type=='MESH' for v in ob.data.vertices);assert abs(lowest)<1e-8
result={'status':'PASS','blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Maker technical inventory of saved editable source, not independent factual or visual acceptance.','checks':['Actual saved blend reopened','Identity root and meter coordinates','No cameras, lights, images, text blocks or external libraries','Each semantic solid closed-manifold with positive signed volume','Four walking pairs II-V distinct from small chelicerae I and swimming pair VI','Twelve numbered trunk tergites: six preabdomen, six postabdomen','Straight telson on posterior axis and body length 200 mm excluding limb projections','Lowermost mounting plane at zero'],'body_axial_length_m':L,'author_estimate_not_measurement':True,'lowest_mounting_z_m':lowest,'semantic_groups':groups,'closed_solid_volumes':vol,'limits':['Individual closed solids overlap at normal anatomical joints; this does not establish a fused printable mesh.','Depth, color, limb completion and ventral simplification remain interpretive.']}
a.out.write_text(json.dumps(result,indent=2)+'\n')
