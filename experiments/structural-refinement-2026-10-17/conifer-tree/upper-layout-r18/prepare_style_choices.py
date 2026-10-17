#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Prepare one explicitly separate style proposal after the bounded layout failed.
The r18 QA model is never changed. A leaves, main wood and layout are untouched.
Option B proposes an opaque connected feather core under each existing A fringe.
This is an art-direction choice, not a second arrangement iteration or approval.
"""
import hashlib,importlib.util,json,sys
from pathlib import Path
import bpy
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('r18_layout',P/'build_upper_layout.py');layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
r17=layout.r17;ac=layout.ac
config=json.loads((P/'layout-config.json').read_text());base=P/'build-attempt-01/conifer-upper/conifer-upper.blend'
bpy.ops.wm.open_mainfile(filepath=str(base),load_ui=False,use_scripts=False)
col=next(c for c in bpy.data.collections if c.get('asset_root'))
obj=next(o for o in col.all_objects if o.type=='MESH' and 'Frozen r17' in o.name)
verts=[tuple(v.co) for v in obj.data.vertices];faces=[tuple(p.vertices) for p in obj.data.polygons];materials=[p.material_index for p in obj.data.polygons];old_v=len(verts);old_f=len(faces)
# Low-frequency feather-core outline. Flat, no raised ridge or round volume.
# Single continuous band per spray, fourteen triangles, beneath the A fringe.
ts=[0,.16,.30,.44,.59,.73,.88,1.03];half_widths=[.004,.055,.12,.083,.108,.074,.055,.002]
for item in layout.arranged_axes(config):
 sp=item['sp'];span=(sp(1)-sp(0)).length;side,n=r17.frame(sp(1)-sp(0));offset=len(verts)
 for t,width in zip(ts,half_widths):
  point=sp(t)-n*span*.002
  verts.extend([tuple(point-side*span*width),tuple(point+side*span*width)])
 for k in range(len(ts)-1):
  faces.append((offset+2*k,offset+2*k+1,offset+2*k+3,offset+2*k+2));materials.append(item['material'])
mesh=bpy.data.meshes.new('Style proposal B | frozen A fringe plus connected feather core');mesh.from_pydata(verts,[],faces);mesh.update()
for m in obj.data.materials:mesh.materials.append(m)
for poly,mi in zip(mesh.polygons,materials):poly.material_index=mi;poly.use_smooth=True
obj.data=mesh
assert [tuple(v.co) for v in obj.data.vertices[:old_v]]==verts[:old_v]
meta={'description':{'en':'Style proposal B only: continuous feather-group core plus unchanged A narrow fringe. Not the r18 QA model and not approved.','zh':'风格提案B：连续羽簇核心面与不变A窄叶缘。非r18排布验收模型，未批准。'},'profile':'style-choice proposal only; opaque double-sided palette geometry; no textures','provenance':'Original procedural style proposal. No third-party image or geometry incorporated.','scientific_status':'Artistic aggregation; the connected opaque core is a chosen visual abstraction, not an anatomical claim.','artistic_choices':['Option A preserves separated narrow needles and open sky. Option B adds an opaque feather-group core behind the same thin needle fringe to prioritize thumbnail cluster mass.','Original A leaf mesh prefix, wood and all43 placements are unchanged.','Connected core adds602 triangles in this upper excerpt; this cost is outside and explicitly separate from the bounded r18 added-spray budget.'],'generator':str((P/'prepare_style_choices.py').relative_to(layout.REPO)),'topology_notes':'Intentional double-sided open feather-core surfaces. Concept image is not independent art approval, runtime validation or a released asset.'}
result=ac.export_asset('conifer-upper',{'en':'Unapproved feather-mass style choice B','zh':'未批准的羽簇体面风格选项B'},'plants',col,meta,output_root=P/'style-proposal-b',render=False,max_triangles=6500,max_materials=3,max_primitives=3)
(P/'style-proposal-b/measurements.json').write_text(json.dumps({'kind':'unapproved_style_proposal','original_r18_qa_model_unchanged':True,'A_original_vertex_prefix_unchanged':True,'base_triangles':5634,'added_core_triangles':602,'total_triangles':result['triangles'],'glb_bytes':result['glb_bytes'],'glb_sha256':result['sha256']['glb'],'body_form':'flat connected feather-group band under frozen narrow A fringe; not rounded tubing','next_action':'User chooses representation scale before implementation proceeds'},indent=2)+'\n')
print(result['triangles'],result['glb_bytes'])
