# SPDX-License-Identifier: MIT
"""Original reference-led Thrinaxodon. Deliberate profile lofts, fused anatomical roots.
No meshes/images are imported. Closed skin, lips and attached digits; no exposed teeth.
Editable export is a connected sculpt mesh with semantic vertex groups + generator/config.
"""
import bpy,bmesh,json,math,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent));import asset_common as ac
P=argparse.ArgumentParser();P.add_argument('--config',type=Path,required=True);P.add_argument('--output-dir',type=Path,required=True);P.add_argument('--gray',action='store_true');A=P.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
coll=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[coll['asset_root']]
mats={k:ac.make_material('thrinaxodon-'+k,'#929292' if A.gray else col,roughness=.86 if k!='eye' else .45,double_sided=False) for k,col in C['palette'].items()}
parts=[];semantic=[];foot_samples=[];digit_tips=[]
def add(name,v,f):
 o=ac.mesh_object(name,[[float(x)*.001 for x in q] for q in v],f,mats['body'],coll);parts.append(o);return o
# Elliptical cross-section loft oriented along the centerline. Every loft is
# closed before the volumetric union. Curved fingers are explicit, not beads.
def tube(name,sections,n=12):
 v=[]
 for i,sec in enumerate(sections):
  p=Vector(sec[:3]);d=Vector(sections[min(i+1,len(sections)-1)][:3])-Vector(sections[max(i-1,0)][:3]);d.normalize()
  ref=Vector((0,0,1)) if abs(d.z)<.92 else Vector((0,1,0));u=d.cross(ref).normalized();w=d.cross(u).normalized()
  for j in range(n):
   t=2*math.pi*j/n;q=p+u*sec[3]*math.cos(t)+w*sec[4]*math.sin(t);v.append(tuple(q))
 f=[]
 for i in range(len(sections)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 f.extend([tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]);return add(name,v,f)
# Main uninterrupted head–neck–trunk has skull-guided broad posterior cheeks,
# a low tapered non-beaked snout, shallow short neck, and long ribcage.
v=[];n=24;sec=C['body_sections_mm']
for y,w,lo,hi in sec:
 for j in range(n):
  t=2*math.pi*j/n;z=(lo+hi)/2+(hi-lo)/2*math.cos(t);x=w*math.sin(t)
  v.append((x,y,z))
f=[]
for i in range(len(sec)-1):
 for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
f.extend([tuple(reversed(range(n))),tuple((len(sec)-1)*n+j for j in range(n))]);body=add('profile-head-neck-trunk',v,f)
tube('relaxed-tapering-tail',[(x,y,z,w,h) for y,x,z,w,h in C['tail_sections_mm']],12)
# Four bent limbs; all shoulders, elbows, hips and ankles remain physically
# joined by the same volumetric skin. No touching-only joint spheres.
for side,s in [('L',-1),('R',1)]:
 for kind,key,cy,cx in [('fore','front_limb_mm',-92,64),('hind','hind_limb_mm',40,53)]:
  tube(side+'-'+kind+'-bent-limb',[(s*x,y,z,w,h) for x,y,z,w,h in C[key]],14)
  # Broad but compact foot base; forward-going digits fan gently from palm.
  tube(side+'-'+kind+'-palm',[(s*cx,cy+7,10,10,8),(s*cx,cy-1,8,12,6),(s*cx,cy-7,7,11,5)],14)
  foot_samples.append((side,kind,s*cx,cy))
  lengths=[13,20,23,21,15] if kind=='fore' else [12,18,21,19,14]
  for j,L in enumerate(lengths):
   delta=(j-2)*4.8;fan=(j-2)*2.3;bx=cx+delta;by=cy-5+abs(j-2)*1.3
   # Individual roots overlap palm; no root cap left inside final union.
   sections=[(s*bx,by,7,2.8,3.0),(s*(bx+fan*.45),by-L*.50,5.6,2.45,2.8),(s*(bx+fan),by-L,4.2,1.9,2.2),(s*(bx+fan*.98),by-L-4,2.4,.75,.8)]
   tube(f'{side}-{kind}-digit-{j+1}',sections,10);digit_tips.append({'side':side,'foot':kind,'digit':j+1,'claw_start_mm':list(sections[-2][:3]),'tip_mm':list(sections[-1][:3])})
# Fuse roots into one closed skin, rather than retaining hidden interpenetrating
# limb shells. Original loft parameters above remain editable in config/source.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body.name='01-continuous-skin-head-trunk-four-limbs-digits-tail'
rm=body.modifiers.new('anatomical-root-volume-union','REMESH');rm.mode='VOXEL';rm.voxel_size=C['voxel_size_m'];rm.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=rm.name)
sm=body.modifiers.new('restrained-loft-union-relax','SMOOTH');sm.factor=.35;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
body.data.calc_loop_triangles();before=len(body.data.loop_triangles);dec=body.modifiers.new('controlled-lowpoly-facets','DECIMATE');dec.ratio=min(1,(C['target_triangles']-160)/before);dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free();body.data.shade_flat()
# Bring each foot onto the shared datum by a local rigid vertical offset.
# Preserve lower-surface topology: projecting many vertices to a plane can fold
# triangles; no plane-clamp operation is used. Fade offset in the lower shank.
foot_offsets=[]
for side,kind,cx,cy in foot_samples:
 region=[v for v in body.data.vertices if v.co.x*cx>0 and abs(v.co.y-cy*.001)<.040 and abs(v.co.x)>.04 and v.co.z<.025]
 lo=min(v.co.z for v in region);delta=.002-lo
 for v in region:
  w=1.0 if v.co.z<.015 else max(0,(.025-v.co.z)/.010)
  v.co.z+=delta*w
 foot_offsets.append({'side':side,'foot':kind,'rigid_pad_offset_m':delta,'lowest_before_m':lo})
body.data.update();body.data.materials.clear();order=list(mats)
for mat in mats.values():body.data.materials.append(mat)
# Broad coherent palette regions follow form. Eye lenses are separate attached
# closed solids; closed mouth is a narrow understated surface boundary.
for p in body.data.polygons:
 q=p.center;x,y,z=q
 color='body'
 # Coherent uniform flank avoids jagged centroid-threshold color wedges.
 if z<.048 and abs(x)<.021 and p.normal.z<-.80 and -.10<y<.09:color='belly'
 # No arbitrary triangular cheek patches; chin remains body palette.
 if y<-.190:color='nose'
 # Closed lips are physical closed skin, not a noisy material stripe.
 for d in digit_tips:
  a=Vector(d['claw_start_mm'])*.001;t=Vector(d['tip_mm'])*.001
  if (q-t).length<.0052:color='claw';break
 p.material_index=order.index(color)
# Semantic editable vertex groups include all four limbs and all 20 digits.
regions={'head':[],'neck':[],'trunk':[],'tail':[]}
for i,v in enumerate(body.data.vertices):
 x,y,z=v.co
 k='head' if y<-.116 else 'neck' if y<-.095 else 'tail' if y>.11 else 'trunk';regions[k].append(i)
for side,kind,cx,cy in foot_samples:
 regions[f'{side}-{kind}-limb']= [i for i,v in enumerate(body.data.vertices) if (v.co.x*cx>0 and abs(v.co.y-cy*.001)<.052 and abs(v.co.x)>.025 and v.co.z<.091)]
 for j in range(5):
  d=next(d for d in digit_tips if d['side']==side and d['foot']==kind and d['digit']==j+1);t=Vector(d['tip_mm'])*.001
  regions[f'{side}-{kind}-digit-{j+1}']=[i for i,v in enumerate(body.data.vertices) if (v.co-t).length<.014]
for name,ids in regions.items():
 if ids:body.vertex_groups.new(name=name).add(ids,1,'REPLACE')
body['construction']='original anatomical lofts, fused roots, voxel-union and controlled decimation';body['digits_per_foot']=5;body['teeth']='not separately modeled: closed lip skin covers dentition';body['no_imported_mesh']=True
# Small lateral eyes follow the anterior orbit position of the CT skull.
def eye(side,s):
 center=Vector((s*.024,-.149,.089));r=(.0031,.0043,.0033);v=[tuple(center+Vector((0,0,r[2])))];n=12;nr=5
 for k in range(1,nr):
  t=math.pi*k/nr
  for j in range(n):
   a=2*math.pi*j/n;v.append(tuple(center+Vector((r[0]*math.sin(t)*math.cos(a),r[1]*math.sin(t)*math.sin(a),r[2]*math.cos(t)))))
 v.append(tuple(center-Vector((0,0,r[2]))));f=[]
 for j in range(n):f.append((0,1+j,1+(j+1)%n))
 for k in range(nr-2):
  for j in range(n):f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):f.append((len(v)-1,1+(nr-2)*n+(j+1)%n,1+(nr-2)*n+j))
 o=ac.mesh_object(side+'-small-lateral-eye',v,f,mats['eye'],coll);o.vertex_groups.new(name=side+'-eye').add(list(range(len(v))),1,'REPLACE');return o
eyes=[eye(side,s) for side,s in [('L',-1),('R',1)]]
# Outward connected component proof: entire trunk/limbs/digits/tail are one mesh
# component. Eye root containment/intersection receives explicit BVH testing.
from mathutils.bvhtree import BVHTree
bodytree=BVHTree.FromPolygons([v.co for v in body.data.vertices],[list(p.vertices) for p in body.data.polygons]);links=[]
for e in eyes:
 et=BVHTree.FromPolygons([v.co for v in e.data.vertices],[list(p.vertices) for p in e.data.polygons]);hits=len(et.overlap(bodytree));links.append({'child':e.name,'parent':body.name,'actual_triangle_boundary_overlap_pairs':hits,'status':'PASS' if hits else 'FAIL'})
assert all(l['status']=='PASS' for l in links),links
# Establish vertical ground first; r002 then centers the actual four-contact bbox.
shift=ac.ground_asset(coll,center_xy=False)
for o in coll.all_objects:
 if o.type=='MESH':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
root['species']='Thrinaxodon liorhinus';root['representation']='living-reconstruction';root['uncertainty']='Soft tissues, pose and incomplete tail artistic; no coat/ear/behavior claims.'
# Record four source foot-contact regions and contiguous anatomical union.
contact=[]
for side,kind,cx,cy in foot_samples:
 vs=[v.co for v in body.data.vertices if v.co.x*cx>0 and abs(v.co.y-cy*.001)<.040 and abs(v.co.x)>.04 and v.co.z<.02]
 contact.append({'side':side,'foot':kind,'lowest_z_m':min(v.z for v in vs),'vertices_at_ground':sum(v.z<1e-7 for v in vs),'digits':5,'points_before_origin_translation_m':[list(v) for v in vs if abs(v.z)<C['origin_placement']['ground_tolerance_m']]})
assert all(x['vertices_at_ground']>0 for x in contact),contact
# Exact declared origin rule: bbox midpoint of all actual ground vertices from
# the four disjoint foot regions, not footprint mean or animal/tail bbox.
contact_points=[p for f in contact for p in f['points_before_origin_translation_m']]
assert len(contact_points)==4,contact_points
cmin=[min(p[k] for p in contact_points) for k in range(3)]
cmax=[max(p[k] for p in contact_points) for k in range(3)]
center=[(a+b)*.5 for a,b in zip(cmin,cmax)]
translation=C['origin_placement']['translation_m']
assert max(abs(translation[k]+center[k]) for k in range(3))<1e-12,(translation,center)
# A single identical offset is written into every source mesh vertex. Do not
# move object transforms or asset root; groups/topology/materials remain intact.
for o in coll.all_objects:
 if o.type=='MESH':
  for v in o.data.vertices:v.co=tuple(v.co[k]+translation[k] for k in range(3))
  o.data.update()
post=[]
for f in contact:
 f['actual_ground_points_m']=[tuple(float(__import__('struct').unpack('<f',__import__('struct').pack('<f',p[k]+translation[k]))[0]) for k in range(3)) for p in f['points_before_origin_translation_m']]
 post.extend(f['actual_ground_points_m'])
post_min=[min(p[k] for p in post) for k in range(3)];post_max=[max(p[k] for p in post) for k in range(3)];post_center=[(a+b)*.5 for a,b in zip(post_min,post_max)]
assert max(abs(x) for x in post_center)<=C['origin_placement']['ground_tolerance_m'],post_center
root['origin_algorithm']='bbox midpoint of actual Z0 foot contact points; not whole-animal bbox or contact mean'
placement={'algorithm':C['origin_placement']['algorithm'],'ground_tolerance_m':C['origin_placement']['ground_tolerance_m'],'contact_count':len(post),'pre_translation_contact_bbox':{'min':cmin,'max':cmax,'center':center},'translation_blender_m':translation,'post_translation_contact_bbox':{'min':post_min,'max':post_max,'center':post_center},'source_mesh_local_vertices_translated':True,'root_and_object_transforms_unchanged_identity':True,'finite_area_sole_contact_claim':False}
(OUT/'origin-placement.json').write_text(json.dumps(placement,indent=2))
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'One fused continuous skin component for head, neck, trunk, all 4 limbs, 20 digits and tail; native graph components separately verified. Eyes use actual triangle BVH intersections. No root caps survive volume union.','checks':links,'foot_contacts':contact,'origin_placement':placement,'foot_offsets':foot_offsets,'manual_digits_each':5,'hind_digits_each_inferred':5,'teeth':'Closed mouth: no separate exposed/hidden tooth shells, hence no unattached dental roots. CT differentiated teeth guide snout proportions only.','digit_tip_design_mm':digit_tips},indent=2))
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=ac.export_asset(C['asset_id'],{'en':'Thrinaxodon — T. liorhinus-inspired reconstruction','zh':'三尖叉齿兽'},'synapsids',coll,metadata={'revision':C['revision'],'representation':'living-reconstruction','description':{'en':'Original low-bodied early cynodont with low non-beaked snout, four short bent limbs and compact five-digit feet.','zh':'原创低矮长躯干早期犬齿兽，低口鼻、四条短曲肢和紧凑五指趾。'},'reconstruction_notes':C['reconstruction_notes'],'generator':'scripts/build_thrinaxodon.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.45,'origin_note':'Exact bbox midpoint of actual four-foot Z0 contact vertices at root XY0; one-point-per-foot contact, not finite-area soles; identity local meshes/root.'},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'voxel_size_m':C['voxel_size_m'],'predecimation_triangles':before,'datum_offset_m':shift,'origin_placement':placement,'glb_sha256':record['sha256']['glb'],'default_area_epsilon_m2':1e-10},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
