# SPDX-License-Identifier: MIT
"""Original Requienia fossil-form model. Scientific boundaries in brief.json.
Run: blender -b -t 2 --python-exit-code 1 --python generate.py -- --output-root /tmp/run
"""
from pathlib import Path
import sys, json, math, argparse, hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, export_asset

HERE=Path(__file__).resolve().parent
args=argparse.ArgumentParser(); args.add_argument('--output-root',required=True); args.add_argument('--params',default=str(HERE/'params.json'))
args=args.parse_args(sys.argv[sys.argv.index('--')+1:])
p=json.loads(Path(args.params).read_text()); col=setup_scene('requienia',p['seed'])
mats=[make_material(n,c,roughness=0.92) for n,c in zip(['limestone-body','growth-crest','old-shell-base','weathered-rv'],p['palette'])]
N=p['sweep_segments']; M=p['section_segments']; end=math.radians(p['end_angle_deg']); span=2*math.pi*p['turns']; b=math.log(p['radius_end']/p['radius_start'])/span

def section(t, phi, relief=True):
    theta=end-span*(1-t); r=p['radius_start']*math.exp(math.log(p['radius_end']/p['radius_start'])*t)
    radial=Vector((math.cos(theta),0,math.sin(theta)))
    tangent=Vector((b*math.cos(theta)-math.sin(theta),0,b*math.sin(theta)+math.cos(theta))).normalized()
    # Cross-section radial vector is orthogonal to the logarithmic-spine tangent.
    cross=Vector((tangent.z,0,-tangent.x))
    center=radial*r+Vector((0,-0.017*(1-t)**1.3,0))
    width=r*p['radial_width_ratio']*(0.61+0.39*t)
    depth=r*p['lateral_width_ratio']*(0.85+0.15*t)
    # Coarse asymmetric exterior growth relief, not section/chamber ornament.
    ridge=0.0
    if relief:
        for k,g in enumerate(p['growth_steps']):
            displaced=g+0.005*math.sin(2*phi+k*1.31)+0.003*math.sin(3*phi+1.1*k)
            ridge+=0.00030*(0.4+0.6*g)*math.exp(-((t-displaced)/0.012)**2)*(0.7+0.3*math.cos(phi-0.5))
    irregular=1+0.045*math.sin(3*phi+1.6*t)+0.015*math.sin(5*phi-2*t)
    pos=center+cross*((width+ridge)*math.cos(phi)*irregular)+Vector((0,(depth+ridge)*math.sin(phi)*(1+0.03*math.cos(phi)),0))
    return pos,center,cross,tangent

verts=[]; faces=[]; face_tags=[]
# Keep very tip closed and blunt; no hollow gastropod aperture.
pos,c0,cross,tan=section(0,0); tip=c0-tan*0.0008
verts.append(tuple(tip))
for j in range(N+1):
 t=j/N
 for k in range(M): verts.append(tuple(section(t,2*math.pi*k/M)[0]))
for k in range(M): faces.append((0,1+(k+1)%M,1+k));face_tags.append((0,k))
for j in range(N):
 for k in range(M):
  a=1+j*M+k;b0=1+j*M+(k+1)%M;c=1+(j+1)*M+(k+1)%M;d=1+(j+1)*M+k
  # Deliberate alternating diagonals prevent a uniform helical lighting zigzag.
  if (j+k)%2: faces.extend([(a,b0,d),(b0,c,d)])
  else: faces.extend([(a,b0,c),(a,c,d)])
  face_tags.extend([(j/N,k),(j/N,k)])
boundary=[Vector(verts[1+N*M+k]) for k in range(M)]
_,end_center,cross,tangent=section(1,0)
cap_center=len(verts);verts.append(tuple(end_center))
for k in range(M):faces.append((1+N*M+k,1+N*M+(k+1)%M,cap_center));face_tags.append((1,k))
# A fused shell core lies behind the umbonal curl. The real exterior photo
# supports a compact closed beak, not an open ammonite/gastropod coil lumen.
# This fills the unobserved hole without drawing section muscle scars outside.
base_index=len(verts);latn=8;longn=20
verts.append((0,-0.006,0.0052))
for j in range(1,latn):
 ang=math.pi*j/latn
 for k in range(longn):
  phi=2*math.pi*k/longn
  verts.append((0.0052*math.sin(ang)*math.cos(phi),-0.006+0.0105*math.sin(ang)*math.sin(phi),0.0052*math.cos(ang)))
bot=len(verts);verts.append((0,-0.006,-0.0052))
for k in range(longn):faces.append((base_index,base_index+1+k,base_index+1+(k+1)%longn));face_tags.append((0,k))
for j in range(latn-2):
 for k in range(longn):
  a=base_index+1+j*longn+k;bb=base_index+1+j*longn+(k+1)%longn;c=bb+longn;d=a+longn
  faces.extend([(a,bb,c),(a,c,d)]);face_tags.extend([(0,k),(0,k)])
for k in range(longn):faces.append((base_index+1+(latn-2)*longn+(k+1)%longn,base_index+1+(latn-2)*longn+k,bot));face_tags.append((0,k))
lv=mesh_object('LV-attached-involute-valve',verts[:base_index],[f for f in faces if max(f)<base_index],mats[:3],col)
core=mesh_object('Temporary-shell-core',verts[base_index:],[tuple(i-base_index for i in f) for f in faces if min(f)>=base_index],mats[0],col)


for poly,(t,k) in zip(lv.data.polygons,face_tags):
 phi=2*math.pi*k/M
 poly.material_index=2 if t<0.12 else 0
lv['anatomy']='Dominant inflated left valve with integrated compact coiled umbo'
lv['surface_source']='Original growth-informed geometry; not section muscle scars or a texture projection'

# A full shallow, independently watertight second valve closes the terminal ring.
# Outer convex face plus recessed inner disk ensure real volume, never a thin strip.
rvv=[];rvf=[];R=8;gap=p['commissure_gap_m']; depth=p['rv_depth_m']
for j in range(R):
 s=j/R
 for k,point in enumerate(boundary):
  phi=2*math.pi*k/M
  shrink=1-s
  bulge=depth*math.sin(s*math.pi/2)**0.78
  rvv.append(tuple(end_center+(point-end_center)*shrink+tangent*(gap+bulge)))
for j in range(R-1):
 for k in range(M):
  a=j*M+k;bb=j*M+(k+1)%M;c=(j+1)*M+(k+1)%M;d=(j+1)*M+k
  rvf.extend([(a,bb,c),(a,c,d)])
top=len(rvv);rvv.append(tuple(end_center+tangent*(gap+depth)))
for k in range(M):rvf.append(((R-1)*M+k,(R-1)*M+(k+1)%M,top))
inner=len(rvv);rvv.append(tuple(end_center+tangent*gap))
for k in range(M):rvf.append(((k+1)%M,k,inner))
rv=mesh_object('RV-complete-shallow-closing-valve',rvv,rvf,[mats[3],mats[1]],col)
for poly in rv.data.polygons: poly.material_index=1 if poly.center.length==0 else 0
rv['anatomy']='Complete shallow convex right closing valve, independent closed solid'
rv['uncertainty']='Full perimeter and depth are evidence-informed artistic completion; not measured from Figure 7 sections'

# Boolean union uses two closed solids, rather than relying on overlapping
# face parity during voxelization. Self-intersecting growth loft is resolved.
bpy.ops.object.select_all(action='DESELECT');lv.select_set(True);bpy.context.view_layer.objects.active=lv
un=lv.modifiers.new('Actual union of shell and enclosed core','BOOLEAN');un.operation='UNION';un.solver='EXACT';un.object=core;un.use_self=True;un.use_hole_tolerant=True
bpy.ops.object.modifier_apply(modifier=un.name);bpy.data.objects.remove(core,do_unlink=True)
# Orient for a small stable fossil contact, preserving integrated low curl.

# Coordinates are authored in meters; all transforms are baked into vertices.
all_verts=[v for obj in (lv,rv) for v in obj.data.vertices]
mins=[min(v.co[i] for v in all_verts) for i in range(3)];maxs=[max(v.co[i] for v in all_verts) for i in range(3)]
scale=p['max_axis_m']/max(maxs[i]-mins[i] for i in range(3))
for v in all_verts:
 v.co*=scale
 v.co.z=-v.co.z
end_center.z=-end_center.z; tangent.z=-tangent.z
lowest=min(v.co.z for v in all_verts)
contacts=[v.co.copy() for v in lv.data.vertices if v.co.z-lowest<0.001*scale]
center=Vector((sum(v.x for v in contacts)/len(contacts),sum(v.y for v in contacts)/len(contacts),lowest))
for v in all_verts:
 v.co-=center
 # Restrained attachment facet, 0.3 mm tall. No display base included.
 if v.co.z<0.0003: v.co.z=0
for obj in (lv,rv):
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()
# Cleanup only: merge the physically overlapping coil into one shell body.
# The authored anatomical loft, not decimation, establishes the whole silhouette.
source_col=bpy.data.collections.new('AUTHORING_LOFT');bpy.context.scene.collection.children.link(source_col)
original=lv.copy();original.data=lv.data.copy();original.name='AUTHORING_LV_preunion';source_col.objects.link(original)
original.hide_render=True;original.hide_viewport=True;original.parent=None
lv.data.remesh_voxel_size=p['voxel_m'];lv.data.remesh_voxel_adaptivity=0
bpy.ops.object.select_all(action='DESELECT');lv.select_set(True);bpy.context.view_layer.objects.active=lv
bpy.ops.object.voxel_remesh()
sm=lv.modifiers.new('Submillimetric cleanup smoothing','SMOOTH');sm.factor=0.4;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)

lv.data.calc_loop_triangles();dec=lv.modifiers.new('Cleanup only: simplify voxel union','DECIMATE');dec.ratio=min(1,p['final_lv_triangles']/len(lv.data.loop_triangles));dec.use_collapse_triangulate=True
bpy.ops.object.modifier_apply(modifier=dec.name)
bm=bmesh.new();bm.from_mesh(lv.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(lv.data);bm.free()
for poly in lv.data.polygons:poly.use_smooth=False;poly.material_index=0
lv['cleanup']='Voxel union and bounded simplification of intentionally intersecting growth loft. Original loft retained outside EXPORT.'
# Topology cleanup is numerical and explicit, not ignored source errors.
bm=bmesh.new();bm.from_mesh(lv.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000012)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=0.000025)
bmesh.ops.triangulate(bm,faces=list(bm.faces))
# Voxel union can produce microscopic zero-volume disconnected islands.
# Remove only disconnected components outside the dominant single shell body.
seen=set();components=[]
for v in bm.verts:
 if v in seen:continue
 component=[];todo=[v];seen.add(v)
 while todo:
  q=todo.pop();component.append(q)
  for edge in q.link_edges:
   other=edge.other_vert(q)
   if other not in seen:seen.add(other);todo.append(other)
 components.append(component)
components.sort(key=len,reverse=True);discarded=[len(c) for c in components[1:]]
if any(n>10 for n in discarded):raise RuntimeError('Unexpected disconnected shell volume: '+repr(discarded))
for c in components[1:]:bmesh.ops.delete(bm,geom=c,context='VERTS')
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(lv.data);bm.free();lv.data.update()
if lv.data.validate(verbose=True):raise RuntimeError('Mesh validation changed final body; reject generator')
lv['removed_micro_island_vertex_counts']=json.dumps(discarded)

# Trim LV to a plane 0.16 mm inside its terminal closure, eliminating
# accidental intersections with the separate RV. Cap the actual cut contour.
bm=bmesh.new();bm.from_mesh(lv.data)
plane_center=end_center*scale-center-tangent*0.00016
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,plane_co=plane_center,plane_no=tangent,clear_outer=True,clear_inner=False)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000012)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=0.000025)
edges=[e for e in bm.edges if e.is_boundary]
if edges:bmesh.ops.holes_fill(bm,edges=edges,sides=0)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=0.000025)
bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(lv.data);bm.free();lv.data.update()
# Remove sub-threshold slivers introduced by clipping, using local shortest
# edge collapses and then rechecking the actual final topology.
bm=bmesh.new();bm.from_mesh(lv.data)
for attempt in range(12):
 bad=[f for f in bm.faces if f.calc_area()<1.1e-10]
 if not bad:break
 face=min(bad,key=lambda f:f.calc_area());edge=min(face.edges,key=lambda e:e.calc_length())
 bmesh.ops.collapse(bm,edges=[edge],uvs=False)
 bmesh.ops.triangulate(bm,faces=list(bm.faces))
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(lv.data);bm.free();lv.data.update()
if lv.data.validate(verbose=True):raise RuntimeError('Cut closure mesh invalid')

# Resolve only small local folds left by bounded simplification at the
# fused umbo. This is geometry repair with fail-closed intersection checks.
from mathutils.bvhtree import BVHTree
repair_counts=[];original_coords=[v.co.copy() for v in lv.data.vertices]
for iteration in range(20):
 lv.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in lv.data.loop_triangles]
 tree=BVHTree.FromPolygons([v.co for v in lv.data.vertices],tris,all_triangles=True,epsilon=0)
 pairs=[(a,b) for a,b in tree.overlap(tree) if a<b and not set(tris[a])&set(tris[b])]
 repair_counts.append(len(pairs))
 if not pairs:break
 affected=set(i for a,b in pairs for t in (tris[a],tris[b]) for i in t)
 bm=bmesh.new();bm.from_mesh(lv.data);bm.verts.ensure_lookup_table()
 chosen=set(bm.verts[i] for i in affected)
 chosen|=set(e.other_vert(v) for v in list(chosen) for e in v.link_edges)
 bmesh.ops.smooth_vert(bm,verts=list(chosen),factor=0.55,use_axis_x=True,use_axis_y=True,use_axis_z=True)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(lv.data);bm.free();lv.data.update()
if repair_counts[-1]:raise RuntimeError('Remaining nonadjacent self-overlaps: '+repr(repair_counts))
max_repair=max((v.co-original_coords[i]).length for i,v in enumerate(lv.data.vertices))
if max_repair>0.0012:raise RuntimeError('Cleanup displaced meaningful morphology: '+str(max_repair))
lv['local_fold_repair_pair_counts']=json.dumps(repair_counts);lv['local_fold_repair_max_m']=max_repair
# Put actual post-union export solids on the declared floor.


zmin=min(v.co.z for ob in (lv,rv) for v in ob.data.vertices)
for ob in (lv,rv):
 for v in ob.data.vertices:v.co.z-=zmin
root=bpy.data.objects['requienia'];root['claim_scope']='Evidence-informed fossil-form interpretation, not specimen accurate'
root['revision']=p['revision'];root['estimated_max_axis_m']=p['max_axis_m'];root['closure_gap_m']=gap*scale
record=export_asset('requienia',{'en':'Requienia coiled-base rudist','zh':'Requienia（卷基厚壳蛤类）'},'animals',col,metadata={
 'revision':p['revision'],'generator':'source/generate.py','parameters':'source/params.json','description':{'en':'Original evidence-informed fossil-form interpretation of an inflated tightly coiled attached valve with a smaller shallow closing valve. Not a specimen-accurate reconstruction.','zh':'原创证据约束化石形态：厚实紧卷附着阀配完整浅凸闭合阀；非标本精确复原。'},
 'taxon':'Requienia','representation':'fossil-specimen','scale_kind':'artistic to 60 mm order of magnitude, not specimen XYZ','source_references':['Masse et al. 2026 Fig.7; DOI 10.2110/carnets.2026.2603','Hectonichus, Requienia ammonia photograph (CC BY-SA 3.0), consulted only'],
 'uncertainties':['Back surface and depth distribution','Exact RV outline and convexity','Attachment contact geometry','Limestone palette is artistic'],
 'geometry_method':'Original variable-section involute loft plus closed shallow valve; no imported third-party geometry or maps',
 'params_sha256':hashlib.sha256(Path(args.params).read_bytes()).hexdigest()},output_root=args.output_root,render=False,max_triangles=6500,max_materials=4,max_primitives=8)
out=Path(args.output_root)/'requienia'
# Semantic editability/source topology evidence beyond the helper.
parts=[]
for obj in (lv,rv):
 bm=bmesh.new();bm.from_mesh(obj.data)
 parts.append({'name':obj.name,'closed':all(e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'vertices':len(bm.verts),'faces':len(bm.faces),'bounds_m':{'min':[min(v.co[i] for v in bm.verts) for i in range(3)],'max':[max(v.co[i] for v in bm.verts) for i in range(3)]}});bm.free()
(out/'anatomy-measurements.json').write_text(json.dumps({'parts':parts,'closure_gap_m':gap*scale,'scale_factor':scale,'unit':'m','representation_warning':'Closed solids are an asset representation, not shell-wall histological measurements'},indent=2))
print('BUILD_FINISHED',out)
