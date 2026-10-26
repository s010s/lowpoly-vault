# SPDX-License-Identifier: MIT
"""Original continuous growing shell; editable semantic centerline, no imported meshes."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,bmesh
import numpy as np
from mathutils import Vector,Quaternion
sys.path.insert(0,str(Path(__file__).parent));import asset_common as ac
P=argparse.ArgumentParser();P.add_argument('--config',type=Path,required=True);P.add_argument('--output-dir',type=Path,required=True);P.add_argument('--stage',choices=['gray','palette','final'],default='final');A=P.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir;OUT.mkdir(exist_ok=True,parents=True)
assert bpy.app.version_string==C['blender_version'];COL=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[C['asset_id']];bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
M={k:ac.make_material(k,'#929292' if A.stage=='gray' else v,roughness=.87,double_sided=False) for k,v in C['palette'].items()}
# Original authored chord-length cubic control path, continuously joined to juvenile coil.
q=np.linspace(C['juvenile_turns']*2*math.pi,0,1400);r=np.linspace(*C['juvenile_radius_m'],len(q));early=np.c_[r*np.sin(q),np.zeros(len(q)),r*np.cos(q)]
control=np.array(C['adult_path_m'],float);knots=np.r_[0,np.cumsum(np.linalg.norm(np.diff(control,axis=0),axis=1))];h=np.diff(knots);n=len(control);matrix=np.zeros((n,n));rhs=np.zeros((n,3));matrix[0,0]=matrix[-1,-1]=1
for i in range(1,n-1):
 matrix[i,i-1]=h[i-1];matrix[i,i]=2*(h[i-1]+h[i]);matrix[i,i+1]=h[i];rhs[i]=6*((control[i+1]-control[i])/h[i]-(control[i]-control[i-1])/h[i-1])
second=np.linalg.solve(matrix,rhs);samp=np.linspace(0,knots[-1],2600);adult=[]
for t in samp:
 i=min(n-2,max(0,int(np.searchsorted(knots,t)-1)));a=(knots[i+1]-t)/h[i];b=(t-knots[i])/h[i];adult.append(a*control[i]+b*control[i+1]+((a**3-a)*second[i]+(b**3-b)*second[i+1])*h[i]**2/6)
adult=np.array(adult)
dense=np.vstack([early[:-1],adult]);ds=np.linalg.norm(np.diff(dense,axis=0),axis=1);s=np.r_[0,np.cumsum(ds)];juvenile_arc=s[len(early)-1];fract=np.clip((s-juvenile_arc)/(s[-1]-juvenile_arc),0,1);rad=np.where(s<=juvenile_arc,C['tube_radius_m'][0]+(.0042-C['tube_radius_m'][0])*(s/juvenile_arc),.0042+(C['tube_radius_m'][1]-.0042)*fract**C['growth_exponent'])
# Adaptive arc/radius sampling retains juvenile curvature without thousands of rings.
weighted=np.r_[0,np.cumsum(ds/((rad[:-1]+rad[1:])/2))];levels=np.linspace(0,weighted[-1],C['rings']);arc=np.interp(levels,weighted,s);points=np.c_[[np.interp(arc,s,dense[:,i]) for i in range(3)]].T;radii=np.interp(arc,s,rad)
# Orient single final aperture toward -Y and a modest +Z (not hydrostatic claim).
tan=Vector(points[-1]-points[-2]).normalized();rot=tan.rotation_difference(Vector((0,-1,.14)).normalized());points=np.array([tuple(rot@Vector(p)) for p in points]);tangents=[]
for i,p in enumerate(points):tangents.append(Vector(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized())
# Rotation-minimizing transport, so ribs remain coherent across changing bend planes.
u=tangents[0].cross(Vector((0,1,0))).normalized();frames=[]
for i,tan in enumerate(tangents):
 if i:u=tangents[i-1].rotation_difference(tan)@u
 u=(u-tan*u.dot(tan)).normalized();v=tan.cross(u).normalized();frames.append((u.copy(),v.copy()))
N=C['radial_segments'];verts=[];faces=[];mats=[];stage_relief=C['rib_relief_fraction'] if A.stage=='final' else 0
for i,p in enumerate(points):
 u,v=frames[i];phase=2*math.pi*C['rib_count']*levels[i]/levels[-1]
 for j in range(N):
  a=2*math.pi*j/N;rib=(.5+.5*math.cos(phase+.28*math.cos(a)))**3
  rr=radii[i]*(1+stage_relief*rib);verts.append(tuple(Vector(p)+u*(rr*math.cos(a))+v*(rr*C['oval_ratio']*math.sin(a))))
def quad(a,b,c,d,mi=0):faces.extend([(a,b,c),(a,c,d)]);mats.extend([mi,mi])
for i in range(len(points)-1):
 for j in range(N):
  a=i*N+j;b=i*N+(j+1)%N;c=(i+1)*N+(j+1)%N;d=(i+1)*N+j
  ridge=(.5+.5*math.cos(2*math.pi*C['rib_count']*(levels[i]+levels[i+1])/(2*levels[-1])))**3
  quad(a,b,c,d,1 if ridge>.66 and A.stage=='final' else 0)
# Early rounded technical closure: low-radius tip, never a duplicate aperture.
ci=len(verts);verts.append(tuple(Vector(points[0])-tangents[0]*radii[0]*.45))
for j in range(N):faces.append((ci,(j+1)%N,j));mats.append(0)
# Terminal opening is part of this same continuous solid boundary: annular rim,
# inward cavity wall tracking the last 20mm of actual centerline, recessed backing.
outer_start=(len(points)-1)*N;inner_ids=[];cavity_begin=max(0,arc[-1]-C['cavity_depth_m']);indices=[len(points)-1]+[i for i in range(len(points)-2,-1,-1) if arc[i]>cavity_begin]
for k,i in enumerate(indices):
 u,v=frames[i];rr=radii[i]-C['aperture_wall_thickness_m'];assert rr>0
 start=len(verts);inner_ids.append(start)
 for j in range(N):a=2*math.pi*j/N;verts.append(tuple(Vector(points[i])+u*(rr*math.cos(a))+v*(rr*C['oval_ratio']*math.sin(a))))
 if k==0:
  for j in range(N):quad(outer_start+j,outer_start+(j+1)%N,start+(j+1)%N,start+j,2)
 else:
  prev=inner_ids[k-1]
  for j in range(N):quad(prev+j,prev+(j+1)%N,start+(j+1)%N,start+j,3)
ci=len(verts);verts.append(tuple(points[indices[-1]]));last=inner_ids[-1]
for j in range(N):faces.append((ci,last+j,last+(j+1)%N));mats.append(3)
# Explicit deterministic triangles, no n-gon or hidden opposite-side diagonal.
obj=ac.mesh_object('continuous-growing-shell-with-integral-ribs-rim-and-cavity',verts,faces,list(M.values()),COL,recalculate_normals=True)
for p,mi in zip(obj.data.polygons,mats):p.material_index=mi
# No modifiers, nonidentity or hidden attachments; full final evaluated AABB datum.
bpy.context.view_layer.update();before=ac._vertices_world(COL);lo,hi=ac._bounds(before);center=Vector([(lo[i]+hi[i])/2 for i in range(3)])
for v in obj.data.vertices:v.co-=center
points-=np.array(center);obj.data.update();bpy.context.view_layer.update();lo2,hi2=ac._bounds(ac._vertices_world(COL));residual=[(a+b)/2 for a,b in zip(lo2,hi2)];assert max(map(abs,residual))<1e-7
# Non-exported editable path preserves all sampled centers/radii and phase meaning.
raw=bpy.data.collections.new('EDITABLE_GROWTH_PATH_NOT_EXPORTED');bpy.context.scene.collection.children.link(raw);curve=bpy.data.curves.new('single-continuous-ontogeny-path','CURVE');curve.dimensions='3D';sp=curve.splines.new('POLY');sp.points.add(len(points)-1)
for i,(p,cp) in enumerate(zip(points,sp.points)):cp.co=(*p,1);cp.radius=float(radii[i])
helper=bpy.data.objects.new('editable-continuous-centerline',curve);raw.objects.link(helper);helper.hide_render=True;helper.hide_set(True);raw['not_exported']=True;helper['tube_radius_m_by_point']=list(map(float,radii));helper['early_phase_end_arc_m']=float(s[len(early)-1]);helper['centerline_parameterization']='Original four alternating spatial U-bends joined by a chord-length cubic spline, not torus objects; see generator/config.'
root['representation']='fossil-shell-reconstruction';root['no_soft_tissues']=True;root['non_grounded_origin']='ALL final exported world vertices XYZ AABB center';obj['geometry']='one connected closed outward solid with integral aperture wall, cavity and low ribs';obj['cavity_closure']='Technical art backing, not anatomical septum'
bm=bmesh.new();bm.from_mesh(obj.data);volume=bm.calc_volume(signed=True);bad_edges=sum(not e.is_manifold for e in bm.edges);bm.free();assert volume>0 and not bad_edges
# Nonneighbor tube envelope test uses conservative maximal oval/rib radius. Only
# local arclength neighbors within1.6(sum radii) omitted here; exact triangle audit is separate.
rmax=radii*(1+stage_relief);distance=np.linalg.norm(points[:,None]-points[None,:],axis=2);rsum=rmax[:,None]+rmax[None,:];nonlocal_mask=np.abs(arc[:,None]-arc[None,:])>1.6*rsum;clearance=np.where(nonlocal_mask,distance-rsum,np.inf);minimum=float(clearance.min());pair=list(map(int,np.unravel_index(clearance.argmin(),clearance.shape)))
if minimum<0:raise RuntimeError('Nonlocal tube-envelope overlap '+str((minimum,pair)))
record=ac.export_asset('nipponites',{'en':'Nipponites — reconstructed heteromorph shell','zh':'日本菊石（异形外壳复原）'},'molluscs',COL,metadata={'revision':'r001','representation':'fossil-shell-reconstruction','description':{'en':'Original continuous heteromorph shell with small juvenile spiral, alternating three-dimensional U-bends, restrained ribs and one thick-rimmed terminal aperture. No soft tissues.','zh':'连续渐粗异形壳、幼体开旋圈、交替三维U弯、简化横肋与单一厚缘壳口；不复原未知软体。'},'reconstruction_notes':C['notes'],'generator':'scripts/build_nipponites.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'origin_note':'NON-GROUNDED: full final evaluated EXPORT world XYZ AABB centered, not footprint, mean or COM.','source_reference_images_incorporated':False},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
report={'status':'PASS','stage':A.stage,'original_authored_centerline':True,'centerline_points_m':points.tolist(),'tube_radius_m':radii.tolist(),'arc_m':arc.tolist(),'points_count':len(points),'radial_segments':N,'continuous_components':1,'manifold_bad_edges':bad_edges,'signed_volume_m3':volume,'cavity_depth_m':float(arc[-1]-arc[indices[-1]]),'rim_thickness_m':C['aperture_wall_thickness_m'],'terminal_tube_nominal_diameter_m':float(2*radii[-1]),'minimum_nonlocal_envelope_gap_m':minimum,'closest_nonlocal_rings':pair,'origin':{'method':'World XYZ AABB of every final evaluated exported mesh vertex; subtract center in geometry; root and object transforms identity. Non-grounded.','precenter_bounds':{'min':lo,'max':hi},'translation_m':list(-center),'final_bounds':{'min':lo2,'max':hi2},'center_residual_m':residual},'exact_glb_sha256':record['sha256']['glb']};(OUT/'growth-path-and-origin.json').write_text(json.dumps(report,indent=2))
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'stage':A.stage,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'default_area_epsilon_m2':1e-10,'glb_sha256':record['sha256']['glb']},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
