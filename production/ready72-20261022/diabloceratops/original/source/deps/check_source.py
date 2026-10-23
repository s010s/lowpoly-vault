# SPDX-License-Identifier: MIT
"""Inspect the delivered editable source, never its maker's in-memory scene."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source
p=argparse.ArgumentParser();p.add_argument('blend',type=Path);p.add_argument('--out',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.blend.resolve()))
col=bpy.data.collections['EXPORT'];audit=audit_source(col,max_triangles=6500)
parts=[];failures=[]
for o in col.all_objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);volume=bm.calc_volume(signed=True);bm.free()
 coords=[o.matrix_world@v.co for v in o.data.vertices]
 bounds={'min':[min(v[i] for v in coords) for i in range(3)],'max':[max(v[i] for v in coords) for i in range(3)]}
 parts.append({'name':o.name,'signed_volume_m3':volume,'bounds_blender_m':bounds})
 if volume<=0:failures.append(o.name+' has non-positive signed volume')
feet=[v for v in parts if 'weight-bearing foot' in v['name']]
if len(feet)!=4:failures.append('Expected four independently editable feet')
for f in feet:
 if abs(f['bounds_blender_m']['min'][2])>1e-6:failures.append(f['name']+' not on floor')
if any(o.type in {'CAMERA','LIGHT'} for o in bpy.data.objects):failures.append('Presentation helpers in source')
external_images=[x.filepath for x in bpy.data.images if x.filepath and not x.packed_file]
if external_images:failures.append('External images in source')
root=bpy.data.objects[col['asset_root']]
foot_min=[min(f['bounds_blender_m']['min'][i] for f in feet) for i in range(2)]
foot_max=[max(f['bounds_blender_m']['max'][i] for f in feet) for i in range(2)]
# Contact ring itself is slightly narrower than foot widest upper ring.
contacts=[o.matrix_world@v.co for o in col.all_objects if o.type=='MESH' and 'weight-bearing foot' in o.name for v in o.data.vertices if abs((o.matrix_world@v.co).z)<1e-7]
contact_mid=[(min(v[i] for v in contacts)+max(v[i] for v in contacts))/2 for i in range(2)]
if max(map(abs,contact_mid))>1e-6:failures.append('Origin does not center floor-contact envelope')
r={'status':'PASS' if not failures and not audit['errors'] else 'FAIL','blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),
   'blender_version':bpy.app.version_string,'python_version':sys.version,'audit':audit,'part_count':len(parts),'parts':parts,
   'four_grounded_feet':len(feet)==4,'contact_envelope_center_xy_m':contact_mid,'external_images':external_images,'failures':failures,
   'signed_volume_scope':'Closed source parts checked independently. Positive signed volume is not proof of a printable Boolean union or absence of internal overlaps.'}
a.out.write_text(json.dumps(r,indent=2)+'\n')
if r['status']!='PASS':raise RuntimeError(failures or audit['errors'])
print('SOURCE_REOPEN_PASS',len(parts),'semantic mesh parts')
