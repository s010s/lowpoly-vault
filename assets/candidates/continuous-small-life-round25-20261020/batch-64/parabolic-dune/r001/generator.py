# SPDX-License-Identifier: MIT
"""Original batch64 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
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

# Geometry authored only after four complete modeling freezes.
import random
rng=random.Random(cfg['seed'])
def chancelloria():
 n=24;h=.16
 def rad(t):return .018+.012*math.sin(t*math.pi*.65)**.65
 rings=[]
 # Outer body up, lip then inner body down, closing only at basal interior.
 for j in range(17):
  t=j/16;r=rad(t);rings.append([(r*(1+.035*math.sin(i*1.7+j*.5))*math.cos(i*math.tau/n),r*(1+.035*math.sin(i*1.7+j*.5))*math.sin(i*math.tau/n),.002+h*t) for i in range(n)])
 for j in range(16,-1,-1):
  t=j/16;r=rad(t)-.0035;rings.append([(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),.006+(h-.004)*t) for i in range(n)])
 # loft caps lower outer/inner loops separately, no apical cap.
 loft('complete_hollow_attached_sac_with_open_crown',rings,'body')
 for j in range(9):
  t=.08+.87*j/8;z=.002+h*t;r=rad(t)
  for k in range(11):
   a=k*math.tau/11+(j%2)*.23+.04*math.sin(j*3+k);normal=Vector((math.cos(a),math.sin(a),0));tang=Vector((-math.sin(a),math.cos(a),0));up=Vector((0,0,1));base=normal*(r+.0001)+up*z
   length=.0045+.0012*math.sin(k*2+j)**2
   tube('sclerite_outward_central_rays',[tuple(base-normal*.0005),tuple(base+normal*length)],[.0008,.000018],'sclerite',5)
   for q in range(4):
    b=q*math.tau/4+.25;direction=(math.cos(b)*tang+math.sin(b)*up+.22*normal).normalized();end=base+direction*length*1.24
    tube('sclerite_four_spreading_tangential_rays',[tuple(base),tuple(end)],[.0007,.000018],'sclerite',5)
 # Denser apical ring; rays rise around but never fill the pore.
 for k in range(20):
  a=k*math.tau/20;normal=Vector((math.cos(a),math.sin(a),0));tang=Vector((-math.sin(a),math.cos(a),0));base=normal*rad(.99)+Vector((0,0,.159))
  for q in range(5):
   d=normal if q==0 else (normal*.25+tang*math.cos((q-1)*math.pi/2)+Vector((0,0,math.sin((q-1)*math.pi/2)))).normalized();end=base+d*.0046
   tube('dense_crown_five_ray_sclerites',[tuple(base),tuple(end)],[.00065,.000018],'sclerite',5)
def terrain(name,w,l,nx,ny,height,mat):
 vs=[];fs=[]
 for j in range(ny+1):
  y=(j/ny-.5)*l
  for i in range(nx+1):
   x=(i/nx-.5)*w
   # soft clipped corners by shrinking edge extent toward corners
   xx=x*(1-.13*(abs(y)/(l/2))**6)
   vs.append((xx,y,height(xx,y)))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+nx+1
   fs.extend([(a,b,a+1),(a+1,b,b+1)] if (i+j)%2 else [(a,b,b+1),(a,b+1,a+1)])
 perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 o=len(vs)
 for v in perimeter:x,y,z=vs[v];vs.append((x,y,0))
 for k,a in enumerate(perimeter):q=(k+1)%len(perimeter);fs.append((a,o+k,o+q,perimeter[q]))
 fs.append(tuple(o+k for k in range(len(perimeter)-1,-1,-1)));part(name,vs,fs,mat)
def dune():
 def z(x,y):
  # U ridge: nose +Y, arms trailing -Y, lower and narrower upwind.
  t=max(0,min(1,(y+20)/33));armx=9.3-1.5*t
  arm=math.exp(-((abs(x)-armx)/(1.35+1.1*t))**2)*(1.2+3.6*t)*max(0,1-((y-1)/25)**8)
  nose=6.5*math.exp(-((x/8.0)**2+((y-12)/5.5)**2))
  return .9+max(arm,nose)+.10*math.sin(x*.7+y*.3)
 terrain('continuous_parabolic_dune_blowout_and_trailing_arms',30,46,32,46,z,'sand')
 for sign in [-1,1]:
  for k in range(18):
   y=-19+k*1.52;x=sign*(10.5+.7*math.sin(k*2.2));zz=z(x,y)
   ellipsoid('vegetation_anchoring_trailing_arms',(x,y,zz+.16),(.35+.18*rng.random(),.42+.2*rng.random(),.32),'vegetation',6,3)
def moraine():
 def crest(x):return -7+14*(abs(x)/25)**1.7
 def z(x,y):
  amp=max(0,1-(abs(x)/28)**4);ridge=6.8*amp*math.exp(-((y-crest(x))/(3.4+.5*math.sin(x*.2)))**2)
  return .8+ridge*(1+.10*math.sin(x*.7)+.055*math.sin(x*1.8+y*.6))+.1*math.sin(x*.3+y*.6)**2
 terrain('broad_arcuate_terminal_debris_ridge_and_valley_floor',54,40,48,36,z,'matrix')
 for k in range(100):
  x=rng.uniform(-25,25);y=crest(x)+rng.uniform(-4.2,4.2);size=(.25+rng.random()**3*1.35);zz=z(x,y)
  ellipsoid('embedded_unsorted_angular_debris_boulders',(x,y,zz+size*.22),(size,size*(.7+.5*rng.random()),size*.65),'stone' if k%3 else 'darkstone',6,3)
def cone():
 n=48;rings=[]
 # Broad closed foot rising through irregular depositional shoulder to narrow real vent.
 levels=[(1.65,.04),(1.64,.17),(1.35,.26),(1.3,.43),(1.03,.49),(.98,.67),(.72,.76),(.64,.96),(.43,1.10),(.40,1.25),(.23,1.26),(.205,.98),(.17,.58),(.15,.30)]
 for j,(r,z) in enumerate(levels):
  ring=[]
  for i in range(n):
   a=i*math.tau/n;mod=1+.065*math.sin(5*a+.5)+.035*math.sin(11*a+j*.23);zz=z+.025*math.sin(a*7+j*.5)+.015*math.sin(a*13)
   ring.append((r*mod*math.cos(a),r*.94*mod*math.sin(a),zz))
  rings.append(ring)
 loft('solid_irregular_sinter_cone_open_narrow_vent_throat',rings,'sinter')
 for k in range(14):
  a=k*2.39996;r=.77+.32*math.sin(k*1.7)**2;z=.43+.12*math.sin(k*2.3)**2
  ellipsoid('integrated_bulbous_geyserite_crust',(r*math.cos(a),r*.94*math.sin(a),z),(.22,.19,.16),'pale',8,4)
{'chancelloria':chancelloria,'parabolic-dune':dune,'terminal-moraine':moraine,'geyser-sinter-cone':cone}[slug]()
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if mat in ['sand','matrix','sinter','body']:
  alternatives={'sand':['sandlight','sanddark'],'matrix':['lightmatrix'],'sinter':['pale','ochre','throat'],'body':['bodylight','interior']}[mat]
  for key in alternatives:obj.data.materials.append(m[key])
  obj.data.update()
  for poly in obj.data.polygons:
   c=poly.center
   if mat=='sinter':poly.material_index=3 if c.z>.32 and math.hypot(c.x,c.y)<.24 else 2 if .20<c.z<.30 or .65<c.z<.76 else 1 if poly.normal.z>.65 else 0
   elif mat=='body':poly.material_index=2 if poly.normal.x*c.x+poly.normal.y*c.y<0 else 1 if poly.normal.x<-.5 else 0
   elif mat=='sand':poly.material_index=1 if poly.normal.z>.85 else 2 if poly.normal.y<-.25 else 0
   else:poly.material_index=1 if poly.normal.z>.8 else 0
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
