# SPDX-License-Identifier: MIT
"""Read-only anatomy inventory and geometry check of the delivered editable source."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--blend',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(args)
bpy.ops.wm.open_mainfile(filepath=str(a.blend),load_ui=False)
assert not [o for o in bpy.data.objects if o.type in {'CAMERA','LIGHT'}]
assert not bpy.data.texts and not bpy.data.images and not bpy.data.libraries
col=bpy.data.collections['EXPORT'];root=bpy.data.objects[col['asset_root']]
assert all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))
meshes=[o for o in col.objects if o.type=='MESH'];groups={}
for o in meshes:groups.setdefault(o['semantic_part'],[]).append(o.name)
expected={'pointed-walking-terminal':8,'walking-podomere':24,'expanded-chela-palm':2,'chela-fixed-finger':2,'chela-movable-finger':2,'chelicera':2,'mesosoma-tergite':7,'metasoma-segment':5,'telson':1,'sting':1}
for kind,count in expected.items():assert len(groups[kind])==count,(kind,len(groups.get(kind,[])))
volumes=[]
for ob in meshes:
 bm=bmesh.new();bm.from_mesh(ob.data);v=bm.calc_volume(signed=True)
 assert v>0,(ob.name,v)
 assert all(e.is_manifold for e in bm.edges),ob.name
 volumes.append({'part':ob.name,'signed_volume_m3':v,'closed_manifold':True});bm.free()
carapace=bpy.data.objects['Carapace-subrectangular'];L=max(v.co.y for v in carapace.data.vertices)-min(v.co.y for v in carapace.data.vertices)
assert abs(L-.009)<1e-8
feet=[ob for ob in meshes if ob['semantic_part']=='pointed-walking-terminal'];low=min(v.co.z for ob in feet for v in ob.data.vertices)
assert abs(low)<1e-8
res={'status':'PASS','blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':['Actual saved blend reopened read-only','Identity root and meter-scale source','No cameras, lights, external libraries, images or Text blocks','Four distinct walking pairs with pointed compact terminal segments; pedipalps and chelicerae separately inventoried','Seven trunk tergites and five tail segments plus telson and sting','Every authored closed solid manifold with positive signed volume','Estimated carapace length 9 mm and grounded foot tips checked from actual vertices'],'estimated_carapace_length_m':L,'foot_ground_min_z_m':low,'semantic_groups':groups,'closed_solid_volumes':volumes,'limits':['Positive volume and manifold individual parts do not prove union watertightness or no visible overlap.','Simple venter intentionally does not claim fossil respiratory anatomy.','This is maker technical inspection, not independent factual or visual acceptance.']}
a.out.write_text(json.dumps(res,indent=2)+'\n')
