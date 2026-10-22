# SPDX-License-Identifier: MIT
"""Original sculptural low-poly AMNH 20135-inspired fossil. No external mesh/texture."""
from pathlib import Path
import sys,json,math,hashlib,argparse,random
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy,bmesh
from mathutils import Vector
from asset_common import setup_scene,mesh_object,make_material,export_asset,ground_asset
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
P=json.loads((HERE/'params.json').read_text()); random.seed(P['seed'])
col=setup_scene(P['asset_id'],P['seed'])
bone=make_material('fossil-warm-limestone','#B9A58A',.91)
bone_light=make_material('fossil-facet-light','#C3B195',.91)
fracture=make_material('old-break-interior','#948471',.97)
tooth=make_material('worn-preserved-dentine','#A7957C',.86)
# Geometry is authored in the frozen anatomical frame then mapped to the project frame.
def cv(p):return (-p[1],-p[0],p[2])
def obj(name,v,f,mat=bone):return mesh_object(name,[cv(x) for x in v],f,mat,col)
def activate(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
# Main cranium: deliberate longitudinal stations, uneven widths and top/base profile.
# (anterior coordinate, half width, palate/base, dorsal height)
stations=[(-.395,.058,.067,.206),(-.372,.077,.061,.235),(-.333,.063,.095,.251),(-.285,.057,.113,.263),(-.238,.063,.119,.257),(-.191,.072,.111,.240),(-.145,.090,.092,.213),(-.101,.116,.069,.196),(-.055,.120,.063,.186),(-.005,.105,.061,.177),(.050,.091,.059,.169),(.107,.077,.057,.161),(.166,.068,.054,.155),(.225,.062,.052,.151),(.281,.066,.050,.146),(.327,.079,.050,.137),(.367,.091,.051,.123),(.408,.088,.053,.105),(.445,.062,.055,.084)]
N=20;v=[];f=[]
for j,(x,w,lo,hi) in enumerate(stations):
 for k in range(N):
  a=2*math.pi*k/N;s=math.sin(a);c=math.cos(a)
  # Flatten the palate and sharpen the low sagittal line without a separate horn.
  zz=(hi+lo)/2+(hi-lo)/2*s
  if s<-.35:zz=lo+(zz-lo)*.38
  if s>.88 and x<-.1:zz+=.009*(s-.88)/.12
  yy=w*c*(1+0.025*math.sin(j*2.3+k*1.7))
  v.append((x,yy,zz))
for j in range(len(stations)-1):
 for k in range(N):f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
f.extend([tuple(range(N-1,-1,-1)),tuple((len(stations)-1)*N+k for k in range(N))])
cranium=obj('Cranium_preserved_long_waisted_rostrum',v,f,[bone,bone_light,fracture])
# Controlled low-frequency triangular facets, no random decorative holes.
for poly in cranium.data.polygons:
 if random.random()<.14:poly.material_index=1

def ellipsoid_cut(name,center,radii,segments=16,rings=8):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,radius=1,location=cv(center))
 cut=bpy.context.object;cut.name=name
 cut.scale=(radii[1],radii[0],radii[2]);activate(cut);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 return cut

def subtract(target,cut):
 activate(target);mod=target.modifiers.new('real_negative_space_'+cut.name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# Nasal opening genuinely removes upper/front bone, not a black patch.
subtract(cranium,ellipsoid_cut('nasal_aperture',(.394,0,.130),(.085,.048,.068)))
# Concave posterior orbital transitions are open to the temporal space, not dinosaur fenestrae.
for sign in (1,-1):
 subtract(cranium,ellipsoid_cut('orbital_transition_'+str(sign),(-.155,sign*.105,.118),(.087,.047,.058)))
# Modest cranial recess plus rear foramen. Internal anatomy remains intentionally simplified.
subtract(cranium,ellipsoid_cut('unresolved_simplified_cranial_cavity',(-.303,0,.147),(.066,.038,.048)))
bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.020,depth=.18,location=cv((-.37,0,.112)))
cut=bpy.context.object;cut.name='occipital_foramen';cut.rotation_euler.x=math.pi/2;activate(cut);bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);subtract(cranium,cut)
# Remove Boolean numerical slivers at <=10 micrometers, not visible anatomy.
# This cleanup is intentional and bounded before the strict source QA check.
bm=bmesh.new();bm.from_mesh(cranium.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-5)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(cranium.data);bm.free()
# Triangulate explicitly, retaining editability and a stable exported triangulation.
activate(cranium);mod=cranium.modifiers.new('frozen_triangulation','TRIANGULATE');bpy.ops.object.modifier_apply(modifier=mod.name)
# Canonical topology ordering removes Blender Boolean face-order nondeterminism.
# Positions are frozen at 1e-8 m, far below this artistic study's resolution.
old=cranium.data
positions=[tuple(round(float(q),8) for q in vert.co) for vert in old.vertices]
order=sorted(range(len(positions)),key=lambda i:positions[i]);remap={old_i:new_i for new_i,old_i in enumerate(order)}
polys=[]
for poly in old.polygons:
 ids=[remap[i] for i in poly.vertices];rot=min(tuple(ids[k:]+ids[:k]) for k in range(len(ids)))
 polys.append((poly.material_index,rot))
polys.sort();mesh=bpy.data.meshes.new('Cranium_canonical_mesh');mesh.from_pydata([positions[i] for i in order],[],[q[1] for q in polys]);mesh.update()
for mat in old.materials:mesh.materials.append(mat)
for poly,(mat_index,_) in zip(mesh.polygons,polys):poly.material_index=mat_index
cranium.data=mesh;bpy.data.meshes.remove(old)
# Closed irregular elliptical sweep: a continuous single preserved cheek bridge.
def sweep(name,path,n=10,mat=bone):
 vv=[];ff=[]
 for i,(x,y,z,rw,rh) in enumerate(path):
  center=Vector((x,y,z));a=Vector(path[max(0,i-1)][:3]);b=Vector(path[min(len(path)-1,i+1)][:3]);t=(b-a).normalized()
  u=Vector((-t.y,t.x,0)).normalized(); w=t.cross(u).normalized()
  for k in range(n):
   theta=2*math.pi*k/n; vv.append(tuple(center+u*(math.cos(theta)*rw)+w*(math.sin(theta)*rh)))
 for i in range(len(path)-1):
  for k in range(n):ff.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
 ff += [tuple(range(n-1,-1,-1)),tuple((len(path)-1)*n+k for k in range(n))]
 return obj(name,vv,ff,mat)
arch=sweep('Continuous_preserved_zygomatic_arch',[
 (-.035,.104,.094,.021,.029),(-.075,.148,.079,.019,.027),(-.130,.201,.061,.017,.026),(-.196,.244,.047,.017,.027),(-.261,.267,.041,.021,.032),(-.317,.261,.043,.030,.041),(-.352,.224,.063,.036,.047),(-.359,.170,.091,.041,.047),(-.345,.102,.121,.042,.040),(-.327,.058,.142,.029,.039)],10,[bone,bone_light])
for q in arch.data.polygons:
 if q.index%9==0:q.material_index=1
# Only short surviving attachment roots on the missing side; no mirrored bridge.
stub1=sweep('Missing_arch_anterior_break',[(-.033,-.106,.090,.022,.027),(-.064,-.130,.079,.022,.026),(-.079,-.140,.071,.018,.024)],7,[bone,fracture]);stub1.data.polygons[-1].material_index=1
stub2=sweep('Missing_arch_posterior_break',[(-.349,-.057,.125,.035,.039),(-.359,-.084,.100,.036,.033),(-.354,-.109,.081,.028,.029)],7,[bone,fracture]);stub2.data.polygons[-1].material_index=1
# Worn unequal upper crowns. Missing/dashed canine is never modeled.
def crown(name,x,y,base,sx,sy,depth,seed):
 rng=random.Random(seed);nn=8;vv=[];ff=[]
 for j,(fac,z) in enumerate([(1,base),(1.04,base-depth*.52),(.62,base-depth)]):
  for k in range(nn):
   a=2*math.pi*k/nn;zz=z+((.004*math.cos(2*a+.5*seed)+rng.uniform(-.003,.003)) if j==2 else 0);fac2=fac*(1+rng.uniform(-.12,.12))
   vv.append((x+math.cos(a)*sx*fac2,y+math.sin(a)*sy*fac2,zz))
 for j in range(2):
  for k in range(nn):ff.append((j*nn+k,j*nn+(k+1)%nn,(j+1)*nn+(k+1)%nn,(j+1)*nn+k))
 ff.extend([tuple(range(nn-1,-1,-1)),tuple(2*nn+k for k in range(nn))])
 return obj(name,vv,ff,tooth)
# Teeth correspond only to broad solid-line preserved positions, not a full dental formula.
for side in (1,-1):
 for i,(x,y,sx,sy,d) in enumerate([(.287,.061,.018,.014,.021),(.236,.059,.019,.015,.030),(.178,.064,.020,.017,.037),(.117,.075,.022,.020,.036),(.056,.088,.026,.022,.028),(-.004,.101,.028,.022,.024)]):
  if side==-1 and i==1:continue
  crown(f'Preserved_worn_upper_crown_{side}_{i}',x,side*y,.064,sx,sy,d,20135+i+side*19)
# Short irregular front teeth, not the large dashed canine.
for i,(x,y,d) in enumerate([(.426,-.044,.023),(.442,-.018,.017),(.443,.012,.022),(.426,.044,.026)]):
 crown(f'Front_preserved_tooth_{i}',x,y,.065,.010,.009,d,501+i)
# Record axis/mount rather than disguising the asymmetric specimen as a complete skull.
shift=ground_asset(col,center_xy=False)
root=bpy.data.objects[col['asset_root']];root['specimen']='AMNH 20135';root['preservation']='viewer-right arch preserved; viewer-left absent; no mandible; no reconstructed canine';root['scale_note']='0.85 m artistic envelope, not calibrated measurement';root['mounting_origin']='dental contact plane; longitudinal center at anatomical a=0'
# Select all semantic anatomy parts for later editing; no camera, light, or support exported.
record=export_asset('andrewsarchus',{'en':'Andrewsarchus — fossil skull study','zh':'Andrewsarchus 化石头骨研究'},'animals',col,
 metadata={'description':{'en':'Original low-poly representation of the long, broad type upper cranium AMNH 20135, retaining its one-sided cheek-arch loss.','zh':'基于 AMNH 20135 上颅的原创低模表现，保留长宽头骨与单侧颧弓缺失。'},'revision':P['revision'],'representation':'fossil-specimen','claim_scope':P['claim'],'generator':'source/build.py','parameters':'source/params.json','source_reference_ids':['AMNH-2013','OSBORN-1924-DORSAL-VENTRAL','OSBORN-1924-SIDE-REAR'],'scale_uncertainty':'Artistic ~0.85 m envelope; no verified 834/560 mm measurements; no body estimates.','ground_shift_m':shift,'reconstruction_notes':['Negative spaces are real geometry.','One continuous preserved cheek arch, opposing short broken attachment roots only.','No lower jaw, restored canine, tissue, eyes or hidden anatomy assertion.','Tooth crown shapes and cranial interior are low-frequency artistic simplifications, not diagnostic cusp replicas.'],'runtime_target':'Three.js 0.180.0 static palette; GPU not run'},output_root=args.output,render=False,max_triangles=P['budget_triangles'],max_materials=P['budget_materials'],max_primitives=P['budget_primitives'])
(args.output/'build-receipt.json').write_text(json.dumps({'revision':P['revision'],'blender':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'parameters_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'record':record},indent=2)+'\n')
print('BUILD_COMPLETE',record['sha256']['glb'],record['triangles'],record['dimensions'])
