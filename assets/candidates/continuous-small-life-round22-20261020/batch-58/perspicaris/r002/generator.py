# SPDX-License-Identifier: MIT
"""Original batch58 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
import bpy,sys,json,math,argparse,pathlib,datetime,hashlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};groups={}
def part(name,vs,fs,mat):
 v,f=groups.setdefault((name,mat),([],[]));n=len(v);v.extend(vs);f.extend([tuple(n+i for i in face) for face in fs])
def loft(name,rings,mat):
 n=len(rings[0]);vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));part(name,vs,fs,mat)
def tube(name,points,radii,mat,n=6):
 rings=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.95 else Vector((1,0,0));u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
  rings.append([tuple(Vector(p)+radii[i]*(u*math.cos(j*math.tau/n)+w*math.sin(j*math.tau/n))) for j in range(n)])
 loft(name,rings,mat)
def ellipsoid(name,c,r,mat,n=12,k=6):
 rings=[]
 for j in range(k+1):
  t=-math.pi/2+.15+(math.pi-.30)*j/k
  rings.append([(c[0]+r[0]*math.cos(t)*math.cos(i*math.tau/n),c[1]+r[1]*math.cos(t)*math.sin(i*math.tau/n),c[2]+r[2]*math.sin(t)) for i in range(n)])
 loft(name,rings,mat)
def calamophyton():
 # Trunk rises through the crown without dividing into modern-tree boughs.
 heights=[0,.07,.24,.6,1.0,1.4,1.7,1.95,2.18,2.34,2.39];radii=[.135,.111,.072,.058,.050,.049,.053,.059,.065,.062,.020]
 rings=[]
 for z,r in zip(heights,radii):rings.append([(.018*math.sin(z)+r*math.cos(i*math.tau/12),.012*math.sin(z*.7)+r*math.sin(i*math.tau/12),z) for i in range(12)])
 loft('unbranched_trunk_narrow_middle_domed_apex',rings,'bark')
 for j in range(12):
  t=j*math.tau/12+.11;r=.12+.035*math.sin(j*1.7);tube('slender_unbranched_root_traces',[(.065*math.cos(t),.065*math.sin(t),.065),(.15*math.cos(t),.15*math.sin(t),.018),((.25+.02*math.sin(j))*math.cos(t),(.25+.02*math.sin(j))*math.sin(t),.005)],[.010,.008,.0025],'bark',5)
 for level in range(5):
  z=.58+level*.23
  for rank in range(6):
   t=rank*math.tau/6+.07*math.sin(level);r=.052;tube('retained_branch_bases_in_longitudinal_ranks',[(r*math.cos(t),r*math.sin(t),z),((r+.038)*math.cos(t),(r+.038)*math.sin(t),z+.012)],[.014,.009],'bark',5)
 for level in range(3):
  for rank in range(6):
   t=rank*math.tau/6+.10*math.sin(level*1.2+rank);z=1.62+level*.24+.03*math.sin(rank*1.3);length=.56-.075*level+.055*math.sin(rank*1.8);u=Vector((math.cos(t),math.sin(t),0));v=Vector((-math.sin(t),math.cos(t),0));base=u*.045+Vector((0,0,z));end=u*length+Vector((.012,0,z+.22+.03*level))
   pts=[base,base*.65+end*.35+Vector((0,0,.07)),base*.25+end*.75+Vector((0,0,.07)),end];tube('upper_lateral_digitate_primary_sprays',[tuple(p) for p in pts],[.023,.019,.013,.009],'bark',6)
   # Distal fingers are the crown representation scale; no laminate leaves.
   for f in range(4):
    spread=(f-1.5)*.105;start=pts[2] if f in [0,3] else end;tip=end+u*(.19+.025*math.sin(f+rank))+v*spread+Vector((0,0,.16+.05*math.cos(f)))
    mid=start*.5+tip*.5+Vector((0,0,.045));tube('digitate_finger_axes',[tuple(start),tuple(mid),tuple(tip)],[.009,.006,.0035],'twig',5)
    for s in [-1,1]:
     endpoint=tip+u*.07+v*s*.035+Vector((0,0,.065));tube('terminal_dichotomous_leafless_twigs',[tuple(tip),tuple(tip*.45+endpoint*.55),tuple(endpoint)],[.0038,.0025,.0012],'twig',4)
def perspicaris():
 # Forward -Y; straight dorsal hinge; laterally bulged valves are closed thin shells.
 for sign in [-1,1]:
  nu=25;nv=14;vs=[];fs=[]
  for layer in [0,1]:
   for j in range(nu):
    u=-.985+1.97*j/(nu-1);g=math.sqrt(1-u*u);yy=-.003+.0125*u
    for k in range(nv+1):
     t=k*math.pi/nv;x=sign*(.00045+.0056*g*math.sin(t)-.00030*layer);zz=.0103-.0105*g*(1-math.cos(t))/2;vs.append((x,yy,zz))
  stride=nv+1;offset=nu*stride
  for layer in [0,1]:
   b=layer*offset
   for j in range(nu-1):
    for k in range(nv):
     a=b+j*stride+k;c=a+stride;f=(a,c,c+1,a+1);fs.append(f if layer==0 else tuple(reversed(f)))
  boundary=list(range(stride))+[j*stride+nv for j in range(1,nu)]+[(nu-1)*stride+k for k in range(nv-1,-1,-1)]+[j*stride for j in range(nu-2,0,-1)]
  for j,a in enumerate(boundary):q=boundary[(j+1)%len(boundary)];fs.append((a,q,q+offset,a+offset))
  part('left_suboval_carapace_valve' if sign<0 else 'right_suboval_carapace_valve',vs,fs,'shell')
 tube('straight_dorsal_hinge',[(0,-.013,.0103),(0,.007,.0103)],[.00045,.00045],'bark',6)
 # Ten compact thoracic stations, concealed dorsally but inspectable ventrally.
 for j in range(10):
  y=-.0125+j*.0022;rad=.0021+.0003*math.sin(j*.4)
  ellipsoid('ten_thoracic_segments',(0,y,.0041),[rad,.00115,.0020],'bark',8,4)
  for s in [-1,1]:
   # Closed blade-like flap, flattened in thickness and swept toward rear.
   origin=Vector((s*.0018,y,.003));tip=Vector((s*(.0069-.00008*j),y+.0016,.0002));mid=origin*.35+tip*.65;u=Vector((0,.00105,0));th=Vector((0,0,.00022));vs=[tuple(origin-u),tuple(origin+u),tuple(mid+u),tuple(tip),tuple(mid-u)]
   vs+=[tuple(Vector(v)+th) for v in vs];fs=[(4,3,2,1,0),(5,6,7,8,9)]+[(i,(i+1)%5,(i+1)%5+5,i+5) for i in range(5)];part('ten_pairs_flat_swimming_flaps',vs,fs,'sand')
 # Exactly seven abdominal segments beyond posterior shell edge.
 for j in range(7):
  y=.010+j*.0017;rad=.0025*(1-.075*j);loft('seven_exposed_abdominal_segments',[[((rad*s)*math.cos(i*math.tau/10),y+dy,.0043+(rad*s)*math.sin(i*math.tau/10)) for i in range(10)] for s,dy in [(.88,-.00085),(1,-.00055),(.93,.0008)]],'lee')
 for s in [-1,1]:
  tube('two_tapered_unsegmented_tail_rami',[(s*.0006,.0205,.0043),(s*.0024,.0248,.0044),(s*.0046,.030,.0046)],[.0008,.00055,.00009],'bark',6)
  tube('two_forward_eye_stalks',[(s*.0017,-.0127,.0065),(s*.0030,-.0176,.0070)],[.0009,.00085],'lee',7)
  ellipsoid('two_large_oval_eyes',(s*.0030,-.0184,.0072),[.0018,.0015,.0020],'dark',12,6)
  # Antennal axis plus modest collars keeps joint count obvious without hair geometry.
  points=[(s*(.0018+.0048*t),-.0138-.012*t,.0048-.002*t+.0007*math.sin(t*math.pi)) for t in [i/9 for i in range(10)]];radii=[.00062*(1-i/11) for i in range(10)];tube('two_stout_segmented_antennae',points,radii,'sand',6)
  for j in range(1,9):
   p=Vector(points[j]);d=(Vector(points[j+1])-Vector(points[j-1])).normalized();tube('antennal_joint_collars',[tuple(p-d*.00014),tuple(p+d*.00014)],[radii[j]*1.17,radii[j]*1.17],'bark',6)
def barchan():
 n=40;cross=[0,.22,.48,.70,.78,.88,1];vs=[];fs=[]
 # Cross sections run from long windward toe to curved crest to concave lee toe.
 # End stations are single horn vertices, avoiding degenerate collapsed rings.
 vs.append((-4,-2.8,0))
 for j in range(1,n):
  u=-1+2*j/n;g=math.sqrt(1-u*u);cy=-2.5*u*u+.30*u;h=1.6*(1-u*u)**.72
  for t in cross:
   if t<=.78:
    s=t/.78;y=cy+(3.4-2.6*s)*g;z=h*(s**1.25)
   else:
    s=(t-.78)/.22;y=cy+(.8-1*s)*g;z=h*(1-s)
   vs.append((4*u,y,z))
 last=len(vs);vs.append((4,-2.2,0));k=len(cross)
 for i in range(k-1):fs.append((0,1+i,1+i+1))
 for j in range(n-2):
  b=1+j*k;c=b+k
  for i in range(k-1):fs.extend([(b+i,c+i,c+i+1),(b+i,c+i+1,b+i+1)])
 b=1+(n-2)*k
 for i in range(k-1):fs.append((b+i,last,b+i+1))
 # Flat closed underside follows outer and inner crescent perimeter.
 perimeter=[0]+[1+j*k for j in range(n-1)]+[last]+[1+j*k+k-1 for j in range(n-2,-1,-1)]
 # All perimeter Z=0, and a central fan lies within crescent strips, not in the crescent hole.
 for j in range(n-2):
  a=1+j*k;b=a+k;fs.append((a,a+k-1,b+k-1,b))
 fs.extend([(0,k,1),(last,1+(n-2)*k,1+(n-2)*k+k-1)])
 part('single_continuous_crescent_dune',vs,fs,'sand')
def current_ripple():
 nx=32;ridge=8;fractions=[0,.22,.46,.65,.78,.88];rows=[]
 for r in range(ridge):
  for f in fractions:rows.append((r+f)/ridge)
 rows.append(1);ny=len(rows)-1;vs=[];fs=[]
 for j,t in enumerate(rows):
  phase=(t*ridge)%1;z=.035+.052*(phase/.78 if phase<=.78 else (1-phase)/.22)
  if j==ny:z=.035
  for i in range(nx+1):
   x=-.6+1.2*i/nx;drift=.011*math.sin(5*x+.25)+.004*math.sin(11*x);y=.45-.9*t+drift*math.sin(math.pi*t)
   # Gentle ridge-height rhythm, not random face-color decoration.
   height=.035+(z-.035)*(1+.06*math.sin(5*x+1.1*t));vs.append((x,y,height))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+nx+1;fs.extend([(a,b,b+1),(a,b+1,a+1)])
 perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 start=len(vs)
 for a in perimeter:x,y,z=vs[a];vs.append((x,y,0))
 for j,a in enumerate(perimeter):q=(j+1)%len(perimeter);fs.append((a,start+j,start+q,perimeter[q]))
 fs.append(tuple(start+j for j in range(len(perimeter)-1,-1,-1)));part('continuous_asymmetric_current_ripple_slab',vs,fs,'sand')
{'calamophyton':calamophyton,'perspicaris':perspicaris,'barchan-dune':barchan,'current-ripple-surface':current_ripple}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
