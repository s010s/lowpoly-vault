# SPDX-License-Identifier: MIT
"""Original batch69 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
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

# Original geometry authoring begins after all four freezes2026-10-20T14:03:28Z.
import random
rng=random.Random(cfg['seed'])
def wi():
 # Full unsegmented soft body; independently closed oval foot remains naked below armour.
 rings=[]
 for j in range(25):
  y=-.0245+j*.049/24;f=math.sqrt(max(.002,1-(y/.025)**2));rings.append([(.0145*f*math.cos(k*math.tau/24),y,.007+(.0065*f if math.sin(k*math.tau/24)>=0 else .0055)*math.sin(k*math.tau/24)) for k in range(24)])
 loft('complete_soft_body',rings,'body');ellipsoid('continuous_naked_ventral_creeping_foot',(0,0,.0018),(.0135,.0239,.0018),'foot',24,6)
 def scale(name,c,u,normal,length,width,mat,curved=False,ribs=True):
  c=Vector(c);u=Vector(u).normalized();n=Vector(normal).normalized();v=Vector((0,1,-.13 if c.y>0 else .04)).normalized()
  # Closed flattened six-sided leaf, upper and lower face; broad shoulder and narrow inserted root.
  plan=[(-.10,0),(.10,0),(.5,.40),(.35,.77),(0,1),(-.42,.72),(-.5,.36)]
  vs=[]
  for t in [-1,1]:
   for x,y in plan:
    shift=(.18*length*y*y if curved else 0);vs.append(tuple(c+u*(x*width+shift)+v*(y*length)+n*(t*.00012+.00025*math.sin(y*math.pi))))
  m=len(plan);fs=[tuple(range(m-1,-1,-1)),tuple(m+i for i in range(m))]
  for i in range(m):q=(i+1)%m;fs.append((i,q,q+m,i+m))
  part(name,vs,fs,mat)
  if ribs:
   for side in [-.19,.19]:
    a=c+u*(side*width)+v*(.15*length)+n*.00025;b=c+u*(side*width*.45)+v*(.80*length)+n*.00034
    # Sparse geometric ridge shorthand, not literal microscopic rib count.
    d=(b-a).normalized();w=u*.000055;h=n*.000075
    part('sparse_longitudinal_ridge_relief',[tuple(a-w),tuple(a+w),tuple(a+h),tuple(b-w*.4),tuple(b+w*.4),tuple(b+h*.4)],[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],mat)
 for row in range(8):
  y=-.020+row*.0054;f=math.sqrt(max(.12,1-(y/.027)**2))
  for s in [-1,1]:
   # Three dorsal, four upper, one lower and five narrow ventrolaterals per half-row.
   for zone,angles,length,width,mat in [('dorsal',[.10,.30,.49],.0084,.0035,'dorsal'),('upper',[.68,.83,.98,1.12],.0082,.0031,'lateral'),('lower',[1.32],.0082,.0032,'lateral'),('ventrolateral',[1.49,1.57,1.65,1.73,1.81],.0092,.00135,'dorsal')]:
    for k,t in enumerate(angles):
     c=(s*.0145*f*math.sin(t),y+.00025*math.sin(k+row),.007+.0065*f*math.cos(t));u=(s*math.cos(t),0,-math.sin(t));normal=(s*math.sin(t),0,math.cos(t))
     scale('eight_trunk_rows_'+zone,c,u,normal,length*(.88+.12*f),width*f,mat,zone=='ventrolateral')
 # Explicit anterior paired fans, no continuous sickle skirt across mouth.
 for s in [-1,1]:
  for k,t in enumerate([.15,.4,.65,.9,1.1,1.3,1.5]):
   scale('anterior_paired_serial_fan',(s*.008*math.sin(t),-.024,.0065+.004*math.cos(t)),(s*math.cos(t),-.25,-math.sin(t)),(s*math.sin(t),-.5,math.cos(t)),.0054,.0027,'lateral',k==6,False)
 # Two adult dorsolateral ranks,9 unequal thin flattened blades per side, no generic cones.
 for s in [-1,1]:
  for j in range(9):
   y=-.019+j*.0047;f=math.sqrt(max(.1,1-(y/.026)**2));length=.010+.012*math.sin((j+.5)*math.pi/9);c=Vector((s*.009*f,y,.012*f+.001));d=Vector((s*.32,.10 if j>4 else -.10,1)).normalized();u=Vector((0,1,0));n=d.cross(u).normalized();rings=[]
   for q,width,thick in [(0,.00080,.00013),(.68,.00080,.00013),(.96,.00010,.00004),(1,.000018,.000018)]:rings.append([tuple(c+d*(q*length)+u*x*width+n*z*thick) for x,z in [(-1,-1),(1,-1),(1,1),(-1,1)]])
   loft('adult_unequal_flattened_spine_ranks',rings,'spines')
 # Small ventral supporting pad and two tooth rows, tucked beneath anterior margin.
 ellipsoid('small_ventral_anterior_feeding_support',(0,-.0208,.00125),(.0032,.0024,.00045),'spines',14,4)
 for row in range(2):
  for k in range(9):
   x=(k-4)*.00056;y=-.0216+row*.00115+.00025*(x/.0025)**2
   tube('two_curved_ventral_tooth_rows',[(x,y,.00125),(x,y-.00020,.00040),(x,y-.00036,.00017)],[.00018,.00011,.000025],'teeth',5)
def terrain(name,nx,ny,xs,ys,height,matfn,keys):
 vs=[];fs=[];mats=[]
 for j in range(ny+1):
  y=ys[0]+(ys[1]-ys[0])*j/ny
  for i in range(nx+1):
   x=xs[0]+(xs[1]-xs[0])*i/nx;vs.append((x,y,height(x,y)))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+nx+1
   for f in [(a,a+1,b+1),(a,b+1,b)]:
    fs.append(f);cx=sum(vs[k][0] for k in f)/3;cy=sum(vs[k][1] for k in f)/3;cz=sum(vs[k][2] for k in f)/3;mats.append(matfn(cx,cy,cz))
 per=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];off=len(vs)
 for k in per:x,y,z=vs[k];vs.append((x,y,0))
 for k,a in enumerate(per):q=(k+1)%len(per);fs.append((a,per[q],off+q,off+k));mats.append(keys[0])
 fs.append(tuple(off+k for k in range(len(per)-1,-1,-1)));mats.append(keys[0]);obj=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,mat in zip(obj.data.polygons,mats):p.material_index=keys.index(mat)
def hanging():
 def h(x,y):
  a=abs(x);main=4 if a<=9 else 4+(min(1,(a-9)/12)**.58)*20
  if x>=9 and abs(y-8)<7:
   # A real steep cliff-lip alcove rather than stream floating over a sloping flank.
   weight=max(0,min(1,(7-abs(y-8))/3))
   alcove=4 if x<=13 else 4+12*min(1,x-13)
   main=main*(1-weight)+min(main,alcove)*weight
  if x>=14:
   t=abs(y-8);branch=16 if t<=4 else 16+8*min(1,(t-4)/7)**.7;main=min(main,branch)
  # Quiet bounded faceting does not erase diagnostic floors/lip.
  noise=(.28*math.sin(x*1.7+y*.6)+.15*math.cos(y*1.3-x*.4)) if main>4.2 else .05*math.sin(y*.5)
  return main+noise
 terrain('solid_main_trough_and_elevated_tributary',80,70,(-40,40),(-35,35),h,lambda x,y,z:'upper' if z>22 else 'floor' if z<4.4 else 'rock',['rock','upper','floor'])
 # Finite opaque stream feed and waterfall. Main flow kept narrow so diagnostic floors legible.
 tube('elevated_tributary_stream',[(x,8+.25*math.sin(x*.3),16.08) for x in range(14,41)],[.34]*27,'water',6)
 tube('hanging_lip_static_waterfall',[(14,8,16.08),(13,8,15.8),(12.8,8,9),(12.7,8,4.2)],[.35,.35,.26,.4],'water',6)
 tube('main_valley_stream',[(1.2*math.sin(y*.13),y,4.11) for y in range(-35,36)],[.32]*71,'water',6)
def mud():
 # A single closed radial basin with integrated domes/collapsed bubble cup.
 n=112;nr=28;vs=[(0,0,.26)];fs=[];mats=[]
 def xy(r,a):return (2.5*r*(1+.025*math.sin(5*a)+.017*math.sin(9*a))*math.cos(a),2*r*(1+.025*math.cos(7*a))*math.sin(a))
 def z(r,a,x,y):
  if r<.70:h=.26+.012*math.sin(x*7+y*5)
  elif r<.88:h=.26+(r-.70)/.18*(.34+.06*math.sin(a*5))
  else:h=(.60+.06*math.sin(a*5))*(1-(r-.88)/.12)+.06*(r-.88)/.12
  # Real slumped front-right rim, not a geometric break opening underside.
  slump=math.exp(-((a+1.1)/.27)**2)*max(0,1-abs(r-.88)/.20)*.25;h-=slump
  if r<.72:
   for cx,cy,rad,up in [(-.75,.3,.38,.22),(.62,.64,.28,.14),(-.4,-.65,.25,.12)]:
    d=math.hypot(x-cx,y-cy)/rad
    if d<1:h+=up*math.sqrt(max(0,1-d*d))
   d=math.hypot(x-.65,y+.45);h+=.11*math.exp(-((d-.38)/.065)**2)-.12*math.exp(-(d/.27)**4)
  return max(.035,h)
 for j in range(1,nr+1):
  r=j/nr
  for i in range(n):
   a=-math.pi+i*math.tau/n;x,y=xy(r,a);vs.append((x,y,z(r,a,x,y)))
 for i in range(n):fs.append((0,1+i,1+(i+1)%n));mats.append('mud')
 for j in range(nr-1):
  for i in range(n):
   a=1+j*n+i;b=1+j*n+(i+1)%n;c=a+n;d=b+n
   fs.extend([(a,b,d),(a,d,c)]);mat='mud' if (j+1)/nr<.72 else 'rim' if (j+1)/nr<.90 else 'bank';mats.extend([mat,mat])
 off=len(vs)
 for i in range(n):x,y,_=vs[1+(nr-1)*n+i];vs.append((x,y,0))
 for i in range(n):q=(i+1)%n;fs.append((1+(nr-1)*n+i,off+i,off+q,1+(nr-1)*n+q));mats.append('bank')
 fs.append(tuple(off+i for i in range(n-1,-1,-1)));mats.append('bank');keys=list(cfg['palette']);obj=mesh_object('integrated_muddy_basin_rim_domes_and_collapsed_cup',vs,fs,[m[k] for k in keys],col)
 for p,mat in zip(obj.data.polygons,mats):p.material_index=keys.index(mat)
def dike():
 # All host beds stop at the actual tabular intrusion. End cuts show crosscut relation.
 ns=32;ys=[-12+24*j/ns for j in range(ns+1)]
 def edge(y,s):return .10*math.sin(y*.3)+s*.45
 for s in [-1,1]:
  for layer,(lo,hi,mat) in enumerate([(0,1,'host'),(1,2,'rust'),(2,3,'pale')]):
   vs=[]
   for y in ys:
    inner=edge(y,s);outer=s*8;top=hi
    vs.extend([(inner,y,lo),(outer,y,lo),(outer,y,top+.14*math.sin(y*.9) if layer==2 else top),(inner,y,top)])
   fs=[(3,2,1,0)]
   for j in range(ns):
    for k in range(4):q=(k+1)%4;fs.append((j*4+k,j*4+q,(j+1)*4+q,(j+1)*4+k))
   fs.append(tuple(ns*4+k for k in range(4)));part('bedded_host_'+str(s)+'_'+str(layer),vs,fs,mat)
 rings=[]
 for j,y in enumerate(ys):
  c=.10*math.sin(y*.3);top=7.4+.55*math.sin(j*.36)+rng.uniform(-.72,.88)
  # Continuous irregular fractured planes above host, but exact bed contacts below3m.
  right=.46+rng.uniform(-.035,.14);left=.46+rng.uniform(-.035,.14);topwidth=.28+rng.uniform(-.035,.09)
  rings.append([(c-.45,y,0),(c+.45,y,0),(c+.45,y,3),(c+right,y,5.1+rng.uniform(-.25,.25)),(c+topwidth,y,top),(c-topwidth,y,top+rng.uniform(-.12,.12)),(c-left,y,5.1+rng.uniform(-.25,.25)),(c-.45,y,3)])
 loft('continuous_crosscutting_resistant_tabular_intrusion',rings,'dike')
{'wiwaxia':wi,'hanging-valley':hanging,'mudpot':mud,'dike-wall':dike}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
