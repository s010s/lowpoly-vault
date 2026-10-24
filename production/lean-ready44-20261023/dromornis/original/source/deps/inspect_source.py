# SPDX-License-Identifier: MIT
"""Inspect the delivered editable source without changing it."""
from pathlib import Path
import hashlib,json,sys
import bpy,bmesh
r=Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str((r/'model.blend').resolve()));col=bpy.data.collections['EXPORT'];parts=[]
for o in col.all_objects:
    if o.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(o.data);vol=bm.calc_volume(signed=True);nonman=sum(not e.is_manifold for e in bm.edges);bm.free()
    vs=[v.co for v in o.data.vertices];dims=[max(v[i] for v in vs)-min(v[i] for v in vs) for i in range(3)]
    parts.append({'name':o.name,'signed_volume_m3':vol,'nonmanifold_edges':nonman,'dimensions_blender_xyz_m':dims,'identity_transform':all(abs(o.matrix_local[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))})
assert all(x['signed_volume_m3']>0 and x['nonmanifold_edges']==0 and x['identity_transform'] for x in parts)
assert len([x for x in parts if x['name'].startswith('wing-')])==2
assert len([x for x in parts if x['name'].startswith('toe-')])==6
assert len([x for x in parts if x['name'].startswith('claw-')])==6
assert not any(o.type in {'CAMERA','LIGHT'} for o in bpy.data.objects)
assert not bpy.data.images and not bpy.data.libraries
root=bpy.data.objects['dromornis'];assert root.type=='EMPTY' and all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))
report={'status':'PASS','claim_scope':'Editable-source closure, outward individually closed parts and anatomy inventory only. Intentional joined-part overlaps are not a watertight-union or independent visual claim.',
 'blend_sha256':hashlib.sha256((r/'model.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((r/'model.glb').read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,
 'root':'dromornis','root_identity':True,'external_libraries':0,'external_images':0,'presentation_objects':0,'parts':parts,
 'factual_limits':'All live head/body proportions estimated. P9464-106 braincase and P932-2 rostrum are separate specimens; no casque, damaged cavitation or extreme side compression used as normal anatomy.'}
(r/'qa/evidence/source-inspection.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','closed_outward_parts':len(parts)}))
