# SPDX-License-Identifier: MIT
"""Original Exogyra fossil-form art; no reference pixels or source mesh reused.
Run in Blender 4.3.2: --python this_file -- --output-root OUT --helpers DIR.
A single thick valve and attached stout lateral umbo retain semantic editability.
"""
import argparse, hashlib, json, math, sys, time
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--output-root',required=True); p.add_argument('--helpers',default=str(Path(__file__).with_name('vendor'))); p.add_argument('--config',default=str(Path(__file__).with_name('build-config.json'))); a=p.parse_args(argv)
sys.path.insert(0,a.helpers)
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset
C=json.loads(Path(a.config).read_text()); N=C['angular_segments']; pi=math.pi
collection=setup_scene('exogyra',C['seed'])
mats=[make_material(k,v,roughness=0.93) for k,v in C['palette'].items()]
rx,ry,H=C['outer_radius_x_m'],C['outer_radius_y_m'],C['rim_height_m']
# Low-frequency, growth-related outline asymmetry; no random vertex displacement.
def adiff(a,b): return math.atan2(math.sin(a-b),math.cos(a-b))
def outline(th):
    # Unequal developed shoulders: broad right/anterior flank, waisted umbo flank.
    return (1+.11*math.sin(th+.65)+.075*math.cos(2*th-.9)
        +.085*math.exp(-(adiff(th,.30)/.60)**2)
        -.12*math.exp(-(adiff(th,2.67)/.39)**2)
        +.045*math.exp(-(adiff(th,4.5)/.55)**2))

def edgez(th):
    return H+.0085*math.sin(th)+.0035*math.sin(2*th+.4)+.001*math.sin(5*th+.2)

def xy(r,th,inner=False):
    w=C['wall_thickness_m'] if inner else 0
    return ((rx-w)*r*math.cos(th)*outline(th)+.003*r*r*math.sin(th)+.003*r*r*math.cos(2*th),
            (ry-w)*r*math.sin(th)*outline(th)-.006*r*r+.003*r*r*r*math.sin(3*th))
# A few modest expanded arcs grow from the lateral apex, never horizontal stacked plates.
angles=[(pi/2)*(j/35) for j in range(1,36)]
def growth_world(x,y,z):
    # One growth-origin field is shared by the broad shoulder and the valve.
    d=Vector((x+.036,y-.038,z-.053)).length
    th=math.atan2(y-.038,x+.036)
    return (d+.0013*math.sin(3*th+.8)+.0006*math.sin(5*th-.3))/.04

def growth_coordinate(t,th):
    x,y=xy(math.sin(t),th);z=edgez(th)*(1-math.cos(t))
    return growth_world(x,y,z)

def relief_at(q):
    return sum(C['growth_relief_m']*amp*math.exp(-((q-g)/C['growth_band_width'])**2)
               for g,amp in zip(C['growth_band_centers'],C['growth_band_relative_heights']))
V=[(0,0,0)]; F=[]; M=[]; rings=[]
for k,t in enumerate(angles):
    ring=[]
    for i in range(N):
        th=2*pi*i/N
        # Growth relief remains subdued; not scaly or random rocky debris.
        # Geodesic-like arcs expand from the eccentric posterior umbo, not stacked horizontal rings.
        growth=growth_coordinate(t,th)
        rel=sum(C['growth_relief_m']*amp*math.exp(-((growth-q)/C['growth_band_width'])**2)
                for q,amp in zip(C['growth_band_centers'],C['growth_band_relative_heights']))
        rel*=.82+.18*math.sin(2*th+.6)
        r=math.sin(t)
        x,y=xy(r,th); x+=rel*math.sin(t)*math.cos(th); y+=rel*math.sin(t)*math.sin(th)
        z=edgez(th)*(1-math.cos(t))-rel*math.cos(t)
        ring.append(len(V)); V.append((x,y,z))
    rings.append(ring)
for i in range(N): F.append((0,rings[0][(i+1)%N],rings[0][i])); M.append(2)
for k in range(len(rings)-1):
    for i in range(N):
        j=(i+1)%N
        F.append((rings[k][i],rings[k][j],rings[k+1][j],rings[k+1][i]))
        tm=(angles[k]+angles[k+1])/2; th=2*pi*(i+.5)/N
        q=growth_coordinate(tm,th)
        M.append(1 if min(abs(q-v) for v in C['growth_band_centers'])<.055 else 0)
# Interior rings are centered around the visible oval adductor-scar impression,
# then gently recenter to the irregular lip. This is actual relief, not a disk.
inner=[]
for r in [.11,.18,.22,.245,.275,.31,.39,.49,.60,.71,.81,.90,.97,1.0]:
    ring=[]
    for i in range(N):
        th=2*pi*i/N
        x,y=xy(r,th,True)
        shift=max(0,1-r)**2
        x+=.009*shift; y+=.003*shift
        physical_r=min(1,math.sqrt((x/(rx-C['wall_thickness_m']))**2+(y/(ry-C['wall_thickness_m']))**2)/outline(th))
        # Broad quiet bowl; shape increases continuously into the thick lip.
        z=C['floor_thickness_m']+(edgez(th)-C['floor_thickness_m'])* (1-math.sqrt(max(0,1-r*r)))
        scarq=math.sqrt(((x-.008)/.0115)**2+((y-.0025)/.0095)**2)
        z-=.00125*math.exp(-(scarq/.84)**6)
        z+=.00033*math.exp(-((scarq-1.06)/.14)**2)
        ring.append(len(V)); V.append((x,y,z))
    inner.append(ring)
ci=len(V); V.append((.009,.003,C['floor_thickness_m']-.00125))
for i in range(N): F.append((ci,inner[0][i],inner[0][(i+1)%N])); M.append(4)
for k in range(len(inner)-1):
    for i in range(N):
        j=(i+1)%N
        F.append((inner[k][i],inner[k+1][i],inner[k+1][j],inner[k][j])); M.append(4 if k<3 else 3)
# Connected lip preserves a watertight wall around the whole true cavity.
for i in range(N):
    j=(i+1)%N; F.append((rings[-1][i],rings[-1][j],inner[-1][j],inner[-1][i])); M.append(1)
shell=mesh_object('deep-left-valve',V,F,mats,collection)
for p,m in zip(shell.data.polygons,M): p.material_index=m
shell['anatomy']='One deep asymmetric left valve: thick continuous lip, concave inner wall, adductor scar and subdued expanding growth bands.'
shell['surface_profile']='Deliberately faceted outer/inner shell; no texture or baked lighting.'
# A short broad eccentric umbo, curling laterally above the posterior-left hinge.
# Its basal rings are deeply embedded in the shell wall, not floating ridges.
# A small partial curl rides a broad shoulder, not a tube on a narrow stalk.
path=[(-.006,.044,.030,.007),(-.018,.049,.041,.0085),(-.030,.047,.050,.0075),
      (-.040,.041,.054,.0058),(-.043,.034,.054,.0044),(-.041,.030,.053,.0018)]
S=16; UV=[]; UF=[]; UM=[]; ur=[]
for k,pt in enumerate(path):
    c=Vector(pt[:3]); r=pt[3]
    tangent=Vector(path[min(k+1,len(path)-1)][:3])-Vector(path[max(k-1,0)][:3]); tangent.normalize()
    axis=tangent.cross(Vector((0,0,1)))
    if axis.length<.1: axis=tangent.cross(Vector((0,1,0)))
    axis.normalize(); other=tangent.cross(axis).normalized()
    ring=[]
    for i in range(S):
        t=2*pi*i/S
        # Broad dorsal planes and shallow growth corrugation follow the coil.
        profile=1+.025*math.cos(4*t+.35*k)
        v=c+r*profile*(math.cos(t)*axis+.98*math.sin(t)*other)
        ring.append(len(UV)); UV.append(tuple(v))
    ur.append(ring)
for k in range(len(ur)-1):
    for i in range(S):
        j=(i+1)%S; UF.append((ur[k][i],ur[k][j],ur[k+1][j],ur[k+1][i])); UM.append(0)
# Endcaps are small but finite polygons, with no zero-area tips.
UF.append(tuple(reversed(ur[0]))); UM.append(0)
UF.append(tuple(ur[-1])); UM.append(1)

umbo=mesh_object('lateral-coiled-umbo',UV,UF,mats,collection)
for p,m in zip(umbo.data.polygons,UM): p.material_index=m
umbo['anatomy']='Short stout partial lateral coil, posterior-left, not a centered vertical horn or gastropod spire.'
umbo['assembly']='Basal umbo volume is intentionally embedded into the shell wall. Two closed editable parts; not represented as a printable boolean union.'
# Solid umbonal core closes the incidental handle-like tunnel. The surrounding
# short coil remains a growth ridge on this solid boss, not a free toroidal horn.
# A broad umbonal shoulder merges into a quarter of the actual valve wall.
# The upper curl is supported by this volume, not an exposed flat-ended appendage.
center=Vector((-.023,.032,.031));axes=Vector((.021,.021,.027))
EV=[tuple(center+Vector((0,0,-axes.z)))];EF=[];er=[];CS=32;CL=16
for j in range(1,CL):
    ph=-pi/2+pi*j/CL;rr=[]
    for i in range(CS):
        th=2*pi*i/CS
        unit=Vector((math.cos(ph)*math.cos(th),math.cos(ph)*math.sin(th),math.sin(ph)))
        v=center+Vector((axes.x*unit.x,axes.y*unit.y,axes.z*unit.z))
        n=Vector((unit.x/axes.x,unit.y/axes.y,unit.z/axes.z)).normalized()
        v+=n*relief_at(growth_world(*v))*.82
        rr.append(len(EV));EV.append(tuple(v))
    er.append(rr)
for i in range(CS):EF.append((0,er[0][(i+1)%CS],er[0][i]))
for j in range(len(er)-1):
    for i in range(CS):
        ii=(i+1)%CS;EF.append((er[j][i],er[j][ii],er[j+1][ii],er[j+1][i]))
cap=len(EV);EV.append(tuple(center+Vector((0,0,axes.z))))
for i in range(CS):EF.append((er[-1][i],er[-1][(i+1)%CS],cap))
core=mesh_object('solid-umbonal-core',EV,EF,mats,collection)
# Resolve the supported curled boss as a solid union before carving its inside.
# Voxel fusion is robust to the short curve's intentional internal overlap.
bpy.ops.object.select_all(action='DESELECT')
umbo.select_set(True);core.select_set(True);bpy.context.view_layer.objects.active=umbo
bpy.ops.object.join()
fuse=umbo.modifiers.new('Fuse-rounded-umbo-core','REMESH');fuse.mode='VOXEL';fuse.voxel_size=.0008;fuse.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=fuse.name)
# Trim only the umbo's hidden basal penetration to the real hollow interior.
# This prevents a spurious internal ledge while leaving the bowl itself untouched.
CV=[]; CF=[]; cr=[]
for ring in inner:
    rr=[]
    for idx in ring: rr.append(len(CV)); CV.append((V[idx][0]*1.012,V[idx][1]*1.012,V[idx][2]-.0006))
    cr.append(rr)
CV.append((V[ci][0],V[ci][1],V[ci][2]-.0006)); cc=len(CV)-1
for i in range(N): CF.append((cc,cr[0][(i+1)%N],cr[0][i]))
for k in range(len(cr)-1):
    for i in range(N):
        j=(i+1)%N; CF.append((cr[k][i],cr[k][j],cr[k+1][j],cr[k+1][i]))
# Keep the cavity fully clear above its aperture, rather than leaving a flat
# shelf from a low planar cutter cap under the umbonal shoulder.
upper=[]
for i in cr[-1]: upper.append(len(CV));CV.append((CV[i][0],CV[i][1],.16))
for i in range(N):
    j=(i+1)%N;CF.append((cr[-1][i],cr[-1][j],upper[j],upper[i]))
CF.append(tuple(upper))
cutter=mesh_object('construction-inner-negative',CV,CF,mats[3],collection)
bpy.context.view_layer.objects.active=umbo; umbo.select_set(True)
carve=umbo.modifiers.new('Preserve-empty-inner-cup','BOOLEAN'); carve.operation='DIFFERENCE'; carve.solver='EXACT'; carve.object=cutter
bpy.ops.object.modifier_apply(modifier=carve.name)
bpy.data.objects.remove(cutter,do_unlink=True)
# A small rounded terminal volume preserves the naturally rolled apex edge after
# clearing the cavity. It stays outside the usable aperture, not a handle loop.
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=1,location=(-.0415,.035,.054))
tip=bpy.context.object;tip.name='rounded-terminal-umbo'
tip.scale=(.0055,.008,.0048)
for m in mats:tip.data.materials.append(m)
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
umbo.select_set(True);bpy.context.view_layer.objects.active=umbo
bpy.ops.object.join()
blend=umbo.modifiers.new('Round-apex-transition','REMESH');blend.mode='VOXEL';blend.voxel_size=.0008;blend.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=blend.name)
# Give the carved inner continuation the same restrained inner-shell material.
from mathutils.bvhtree import BVHTree
cavity_bvh=BVHTree.FromPolygons([Vector(v) for v in CV],CF,all_triangles=False)
for face in umbo.data.polygons:
    hit=cavity_bvh.find_nearest(face.center)
    if hit[3] is not None and hit[3]<.0018:face.material_index=3


# Retain editable semantic construction geometry outside EXPORT before an exact union.
construction=bpy.data.collections.new('CONSTRUCTION_EDITABLE'); bpy.context.scene.collection.children.link(construction)
for part in (shell,umbo):
    copy=part.copy(); copy.data=part.data.copy(); copy.name='source-'+part.name; copy.parent=None
    construction.objects.link(copy); copy.hide_render=True; copy.hide_set(True)
# Union removes hidden intersection surfaces and the distracting seam at the hinge.
bpy.context.view_layer.objects.active=shell; shell.select_set(True)
mod=shell.modifiers.new('Fuse-basal-umbo','BOOLEAN'); mod.operation='UNION'; mod.solver='EXACT'; mod.object=umbo
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(umbo,do_unlink=True)
# Remove only coplanar intersection-edge fragments (0.00057 degrees), retaining
# the actual curved shell and coil facets. This avoids collinear ngon ears.
bm=bmesh.new();bm.from_mesh(shell.data)
bmesh.ops.dissolve_limit(bm,angle_limit=.00001,use_dissolve_boundaries=True,verts=list(bm.verts),edges=list(bm.edges),delimit={'NORMAL','MATERIAL'})
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(shell.data);bm.free()
# Bounded geometric cleanup closes the accidental submillimeter umbo seam.
# Primary cup/coil design was authored explicitly above, not generated by Decimate.
# Preserve source parts and transfer only our original structural material regions.
from mathutils.bvhtree import BVHTree
shell.data.calc_loop_triangles()
oldverts=[v.co.copy() for v in shell.data.vertices]
oldtris=[tuple(t.vertices) for t in shell.data.loop_triangles]
oldmats=[shell.data.polygons[t.polygon_index].material_index for t in shell.data.loop_triangles]
bvh=BVHTree.FromPolygons(oldverts,oldtris,all_triangles=True)
bpy.context.view_layer.objects.active=shell
remesh=shell.modifiers.new('Close-incidental-submillimeter-seam','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0012;remesh.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=remesh.name)
# Blend the actual two-volume junction over a bounded broad shoulder region.
# This removes the applied-oval seam while leaving the remote growth arcs and
# quiet cavity untouched. Original semantic parts stay editable for inspection.
def part_bvh(obj):
    obj.data.calc_loop_triangles()
    return BVHTree.FromPolygons([v.co.copy() for v in obj.data.vertices],
        [tuple(t.vertices) for t in obj.data.loop_triangles],all_triangles=True)
body_bvh=part_bvh(bpy.data.objects['source-deep-left-valve'])
umbo_bvh=part_bvh(bpy.data.objects['source-lateral-coiled-umbo'])
vg=shell.vertex_groups.new(name='Bounded-shoulder-continuity')
for v in shell.data.vertices:
    d0=body_bvh.find_nearest(v.co)[3];d1=umbo_bvh.find_nearest(v.co)[3]
    hit=bvh.find_nearest(v.co)
    if d0 is None or d1 is None or hit[2] is None or oldmats[hit[2]] in (3,4):continue
    w=max(0,1-abs(d0-d1)/C['shoulder_blend_width_m'])**2
    if w>.01:vg.add([v.index],w,'REPLACE')
fair=shell.modifiers.new('Continuous-umbonal-growth-transition','SMOOTH')
fair.vertex_group=vg.name;fair.factor=.55;fair.iterations=C['shoulder_blend_smoothing_iterations']
bpy.ops.object.modifier_apply(modifier=fair.name)

relax=shell.modifiers.new('Remove-voxel-stepping','SMOOTH');relax.factor=.32;relax.iterations=1
bpy.ops.object.modifier_apply(modifier=relax.name)
shell.data.calc_loop_triangles(); pre_reduce=len(shell.data.loop_triangles)
reduce=shell.modifiers.new('Restore-authored-lowpoly-budget','DECIMATE');reduce.ratio=min(1.0,C['final_triangle_target']/pre_reduce);reduce.use_collapse_triangulate=True
bpy.ops.object.modifier_apply(modifier=reduce.name)
for face in shell.data.polygons:
    hit=bvh.find_nearest(face.center)
    if hit[2] is not None:face.material_index=oldmats[hit[2]]
shell['seam_cleanup_voxel_size_m']=.0012
shell['seam_cleanup_pre_reduction_triangles']=pre_reduce
shell['seam_cleanup_purpose']='Close accidental tiny hinge tunnel; retain explicitly authored cup, coiled umbo, cavity and original material regions. Original semantic meshes remain editable.'
# Rotate the specimen, not the preview camera, to show the true cup in an honest hero.
from mathutils import Matrix
rot=Matrix.Rotation(math.radians(C['specimen_forward_tilt_deg']),3,'X')
for v in shell.data.vertices: v.co=rot@v.co
# Identity root lies at the actual floor contact center after posing.
zmin=min(v.co.z for v in shell.data.vertices)
contact=[v.co for v in shell.data.vertices if v.co.z<=zmin+.00035]
contact_x=sum(v.x for v in contact)/len(contact); contact_y=sum(v.y for v in contact)/len(contact)
for v in shell.data.vertices: v.co.x-=contact_x; v.co.y-=contact_y
shell['contact_center_shift_xy_m']=[-contact_x,-contact_y]
shell.data.update()
shell['assembly']='One closed union surface; original pre-union parts retained hidden in CONSTRUCTION_EDITABLE.'
shift=ground_asset(collection,center_xy=False)
root=bpy.data.objects[collection['asset_root']]
root['representation']='fossil-specimen'; root['claim_scope']='Original genus-level fossil-form art informed by E. ponderosa; not a scan or exact museum-specimen replica.'
metadata={
'revision':C['revision'],'generator':'source/generate_exogyra.py','config':'source/build-config.json',
'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest(),
'description':{'en':'Original low-poly fossil left valve of Exogyra: a deep irregular cup, lateral coiled umbo, continuous thick rim and quiet adductor-scar cavity. Evidence-informed genus-level art, not a specimen scan.','zh':'原创 Exogyra 化石左壳：深而不对称的壳腔、偏侧短卷壳顶、连续厚壳缘与内侧闭壳肌痕。属级化石形态美术，不是标本扫描。'},
'sources':[{'title':'Cretaceous Atlas, Exogyra ponderosa: YPM 538078 and UNM 2097','url':'https://www.cretaceousatlas.org/species/exogyra-ponderosa/','use':'consulted-only; no source media, mesh or texture incorporated'}],
'claim_scope':root['claim_scope'],'representation':'fossil-specimen','category_original':'animals','subcategory':'mollusk','target_three_version':C['target_three_version'],
'scale_note':'Approximate hand-scale artistic dimensions in meters; no measured dimensions of the cited specimens are claimed.',
'reconstruction_notes':['Single fossil valve only: no animal tissue, opposite valve, sediment slab or display plinth.','Color and exact extent of wear are artistic. Fine ornament is simplified.','One closed Boolean-unioned shell and umbo. Original semantic parts remain editable in a hidden non-export construction collection; not certified as a printable fossil replica.'],
'surface_profile':C['surface_profile'],'ground_shift_m':shift,'reviewed_warnings':[]}
shell.data.calc_loop_triangles()
for t in shell.data.loop_triangles:
    if t.area<1e-10: print('DEGENERATE_DETAIL',t.area,list(t.vertices),[list(shell.data.vertices[i].co) for i in t.vertices])
rec=export_asset('exogyra',{'en':'Exogyra spiral-beaked oyster','zh':'Exogyra（螺喙牡蛎类）'},'animals',collection,metadata=metadata,output_root=a.output_root,render=False,max_triangles=C['max_triangles'],max_materials=C['max_materials'],max_primitives=C['max_primitives'])
print('EXOGYRA_BUILD_COMPLETE '+json.dumps({'glb':rec['glb'],'triangles':rec['triangles'],'bytes':rec['glb_bytes'],'sha256':rec['sha256']['glb']}))
