# SPDX-License-Identifier: MIT
"""Reopen the delivered source to check editability and dependency closure."""
from pathlib import Path
import sys,json,hashlib
import bpy
r=Path(sys.argv[sys.argv.index('--')+1]); p=r/'model.blend'; expected=hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(p))
meshes=[ob for ob in bpy.data.objects if ob.type=='MESH']; root=bpy.data.objects.get('elpistostege')
problems=[]
if root is None:problems.append('Missing identity root')
elif any(abs(root.matrix_world[i][j]-(1 if i==j else 0))>1e-7 for i in range(4) for j in range(4)):problems.append('Nonidentity root')
if any(ob.type in ['CAMERA','LIGHT'] for ob in bpy.data.objects):problems.append('Source contains preview-only cameras/lights')
if bpy.data.libraries:problems.append('External linked library dependency')
if any(image.filepath and not image.packed_file for image in bpy.data.images):problems.append('Unpacked image dependency')
if len(meshes)!=25:problems.append('Unexpected semantic mesh count')
result={'status':'PASS' if not problems else 'FAIL','blend_sha256':expected,'glb_sha256':hashlib.sha256((r/'model.glb').read_bytes()).hexdigest(),'errors':problems,'mesh_objects':len(meshes),'camera_light_objects':sum(ob.type in ['CAMERA','LIGHT'] for ob in bpy.data.objects),'linked_libraries':len(bpy.data.libraries),'images':len(bpy.data.images),'source_file_unchanged':hashlib.sha256(p.read_bytes()).hexdigest()==expected,'scope':'Reopen/editability/dependency check, not independent visual review.'}
(r/'qa/evidence/source-reopen.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert not problems
