#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reopen the delivered Blender source and check closed editable semantic parts."""
import bpy,bmesh,sys,json,hashlib,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('blend',type=Path);p.add_argument('output',type=Path)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.blend))
parts=[];errors=[]
for o in bpy.data.objects:
    if o.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(o.data);vol=bm.calc_volume(signed=True)
    boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges)
    parts.append({'part':o.name,'signed_volume_m3':vol,'boundary_edges':boundary,'non_manifold_edges':nonmanifold,'vertex_count':len(bm.verts),'face_count':len(bm.faces),'positive_transform':o.matrix_world.determinant()>0})
    if vol<=0 or boundary or nonmanifold or o.matrix_world.determinant()<=0:errors.append(o.name)
    bm.free()
lights=[o.name for o in bpy.data.objects if o.type in ('LIGHT','CAMERA')]
libraries=[x.name for x in bpy.data.libraries]
if lights or libraries:errors.append('Unexpected presentation objects or linked library')
C=bpy.data.collections.get('EXPORT');root=bpy.data.objects.get('repenomamus')
identity=root and all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))
if not identity:errors.append('Root is not identity')
report={'status':'PASS' if not errors else 'FAIL','model_blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'errors':errors,'source_reopened':True,'mesh_parts':parts,'external_libraries':libraries,'presentation_objects':lights,'root_identity':bool(identity),'method':'BMesh closed-part signed volumes and boundary/manifold edges, source-only object and linked-library scan. No exhaustive self-intersection solver.','intentional_intersections':'Overlaps inside the torso/neck/head, jaw, ears, eyes, limb joints, paws, fur contour and tail roots are deliberate editable anatomical assemblies, not a print-ready Boolean union.'}
a.output.write_text(json.dumps(report,indent=2)+'\n')
if errors:raise RuntimeError(repr(errors))
