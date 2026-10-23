#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only geometry checks on saved editable source; not independent review."""
import bpy,bmesh,sys,json,hashlib,math,importlib.util
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:];root=Path(args[0]).resolve();dest=Path(args[1])
bpy.ops.wm.open_mainfile(filepath=str(root/'model.blend'))
spec=importlib.util.spec_from_file_location('microgen',root/'source/generate.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
receipt=json.loads((root/'private/final-v002/build-receipt.json').read_text()) if (root/'private/final-v002/build-receipt.json').exists() else json.loads((root/'qa/evidence/build-receipt.json').read_text())
shift=Vector(receipt['ground_shift_m']);_,_,holes=gen.plate_template()
errors=[];rows=[];bvhs={};meshes={o.name:o for o in bpy.data.objects if o.type=='MESH'}
for name,ob in meshes.items():
 bm=bmesh.new();bm.from_mesh(ob.data)
 bvhs[name]=BVHTree.FromBMesh(bm,epsilon=0)
 bm.verts.ensure_lookup_table();seen=set();components=0
 for v in bm.verts:
  if v.index in seen:continue
  components+=1;stack=[v]
  while stack:
   a=stack.pop()
   if a.index in seen:continue
   seen.add(a.index);stack.extend(e.other_vert(a) for e in a.link_edges)
 row={'name':name,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'components':components,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges)}
 if name.startswith('perforated_sclerite_'):
  chi=len(bm.verts)-len(bm.edges)+len(bm.faces);row.update(euler_characteristic=chi,genus=(2-chi)//2,signed_volume_m3=bm.calc_volume(signed=True))
  if components!=1 or chi!=-24 or row['boundary_edges'] or row['nonmanifold_edges'] or row['signed_volume_m3']<=0:errors.append(name+' incorrect closed perforated topology')
  side=-1 if '_L' in name else 1;i=int(name[-2:])-1;y=-.0215+i*.0058;sizes=[.76,.88,.98,1,1,1,.98,.88,.7];rays=[]
  for u,v in holes:
   yy=y+u*.0025*sizes[i];angle=.82+v*.65*sizes[i]
   n=gen.radial_direction(yy,side,angle);centre=Vector((gen.cx(yy),yy,gen.cz(yy)))+shift
   start=centre+n*(gen.radius(yy)+.0025);hit=bvhs[name].ray_cast(start,-n,.005)
   rays.append(hit[0] is None)
  row['aperture_normal_ray_clear_count']=sum(rays);row['aperture_normal_ray_count']=len(rays)
  if not all(rays):errors.append(name+' aperture normal ray hit')
 if name=='paired_terminal_claws_36' and components!=36:errors.append('Claw component count is not 36')
 rows.append(row);bm.free()
plates=[n for n in meshes if n.startswith('perforated_sclerite_')];legs=[n for n in meshes if n.startswith('lobopod_')]
if len(plates)!=18 or len(legs)!=18:errors.append('Bilateral station count mismatch')
intersections=[]
for i,a in enumerate(plates):
 for b in plates[i+1:]+legs+['soft_annulated_trunk_and_limb_free_anterior']:
  overlaps=bvhs[a].overlap(bvhs[b])
  if overlaps:intersections.append({'a':a,'b':b,'triangle_pair_count':len(overlaps)})
if intersections:errors.append('Sclerite unwanted surface intersections')
report={'role':'maker self-check','claim_scope':'Necessary source topology, anatomical count and geometric aperture checks; not independent visual or scientific acceptance.','source_blend_sha256':hashlib.sha256((root/'model.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((root/'model.glb').read_bytes()).hexdigest(),'status':'PASS' if not errors else 'FAIL','errors':errors,'parts':rows,'sclerite_count':len(plates),'limb_count':len(legs),'actual_aperture_ray_tests':sum(r.get('aperture_normal_ray_count',0) for r in rows),'plate_plate_body_limb_surface_intersections':intersections,'method_notes':['Genus uses source indexed topology, not the split-normal GLB index topology.','Aperture rays interrogate only the plate; underlying soft trunk is not counted as blocking the plate aperture.','Plate intersections use exact source triangulated BVH surface overlap, not a printable union claim.','Soft leg attachments intentionally overlap the trunk.','The mouth rim is an intentional coincident two-object interface, not an accidental side opening.']}
dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'errors':errors,'rays':report['actual_aperture_ray_tests'],'intersections':len(intersections)}))
if errors:raise RuntimeError('Geometry obligations failed')
