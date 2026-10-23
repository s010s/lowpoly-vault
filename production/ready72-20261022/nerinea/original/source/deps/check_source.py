#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reopen editable source and inspect actual topology and source-only scene."""
import sys,json,hashlib
from pathlib import Path
import bpy,bmesh
args=sys.argv[sys.argv.index('--')+1:];src=Path(args[0]).resolve();out=Path(args[1]).resolve()
bpy.ops.wm.open_mainfile(filepath=str(src));parts=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();unseen=set(bm.verts);comps=[]
 while unseen:
  todo=[unseen.pop()];count=0
  while todo:
   v=todo.pop();count+=1
   for e in v.link_edges:
    q=e.other_vert(v)
    if q in unseen:unseen.remove(q);todo.append(q)
  comps.append(count)
 parts.append({'name':o.name,'components':comps,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'negative_determinant':o.matrix_world.to_3x3().determinant()<=0})
 bm.free()
cameras_lights=[o.name for o in bpy.data.objects if o.type in ['CAMERA','LIGHT']]
root=bpy.data.objects.get('nerinea');identity=bool(root) and all(abs(root.matrix_world[r][c]-(1 if r==c else 0))<1e-8 for r in range(4) for c in range(4))
passed=len(parts)==1 and all(len(p['components'])==1 and p['boundary_edges']==0 and p['nonmanifold_edges']==0 and p['signed_volume_m3']>0 and not p['negative_determinant'] for p in parts) and not cameras_lights and identity
r={'status':'PASS' if passed else 'FAIL','scope':'Reopened source topology and scene hygiene; does not prove all local self-intersections or scientific accuracy','blend_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'parts':parts,'camera_lights':cameras_lights,'identity_root':identity,'external_images':list(bpy.data.images.keys()),'scene_units':{'system':bpy.context.scene.unit_settings.system,'scale_length':bpy.context.scene.unit_settings.scale_length}}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));assert passed
