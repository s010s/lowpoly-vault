# SPDX-License-Identifier: MIT
"""Original batch92 geometry, authored after immutable 2026-10-20T22:23:07Z freeze."""
import bpy,bmesh,sys,json,math,argparse,pathlib,random,hashlib,datetime,os
from mathutils import Vector,Matrix
from mathutils.geometry import delaunay_2d_cdt
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(args.config).read_text());p=cfg['parameters'];out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(slug,cfg['seed']);m=[make_material(k,v)for k,v in cfg['palette'].items()];semantic={};rng=random.Random(cfg['seed'])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.groups={}
 def add(self,v,f,mi,group=None):
  off=len(self.v);self.v +=[tuple(q) for q in v];self.f +=[tuple(off+x for x in face)for face in f];self.mi += ([mi]*len(f) if isinstance(mi,int)else mi)
  if group:self.groups.setdefault(group,[]).extend(range(off,len(self.v)))
 def emit(self,name):
  o=mesh_object(name,self.v,self.f,m,col)
  for face,i in zip(o.data.polygons,self.mi):face.material_index=i
  for name,idx in self.groups.items():o.vertex_groups.new(name=name).add(idx,1,'REPLACE')
  return o

def tube(M,points,radii,sides=6,mi=0,group=None,flat=1):
 vs=[];pts=[Vector(q)for q in points]
 for i,q in enumerate(pts):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();v=t.cross(u).normalized()
  for j in range(sides):vs.append(tuple(q+radii[i]*(u*math.cos(math.tau*j/sides)+v*flat*math.sin(math.tau*j/sides))))
 fs=[tuple(reversed(range(sides)))]
 for i in range(len(pts)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;fs.append((a,b,b+sides,a+sides))
 fs.append(tuple(range((len(pts)-1)*sides,len(pts)*sides)));M.add(vs,fs,mi,group)

def leaf(M,base,direction,width,length,roll,idx):
 v=Vector(direction).normalized();u=v.cross(Vector((0,0,1))).normalized();n=u.cross(v).normalized();u2=u*math.cos(roll)+n*math.sin(roll);n2=-u*math.sin(roll)+n*math.cos(roll);u=u2;n=n2;base=Vector(base)
 tips=[(-.50,.67),(-.36,.88),(-.22,.97),(-.06,1),(.12,.91),(.28,.84),(.43,.75),(.50,.62)];poly=[(-.045,0),(-.13,.19)]
 for j,(x,y) in enumerate(tips):
  poly.append((x,y))
  if j<len(tips)-1:poly.append(((x+tips[j+1][0])*.48,.27+.012*j+.045*math.sin(j*1.7+.2)))
 poly +=[(.11,.19),(.045,0)];vs=[]
 for s in [-1,1]:
  for x,y in poly:vs.append(tuple(base+u*(x*width)+v*(y*length)+n*(.00013*math.sin(y*math.pi)*x+s*p['leaf_lamina_thickness_m']/2)))
 N=len(poly);fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)];M.add(vs,fs,1+idx%2,'leaf-%02d'%idx);semantic.setdefault('leaf_frames',[]).append(dict(group='leaf-%02d'%idx,longitudinal=list(v),transverse=list(u)))

def eophyllophyton():
 A=Mesh();L=Mesh();shoots=[]
 paths=[[(0,0,0),(.001,0,.018),(-.001,.001,.038),(.001,0,.060)],[(0,0,.009),(-.005,-.002,.020),(-.012,-.003,.034),(-.013,-.002,.045)],[(0,0,.014),(.007,.003,.025),(.012,.006,.035),(.014,.006,.048)]]
 for j,path in enumerate(paths):tube(A,path,[.00065*(1-.20*i)*(1-.16*j)for i in range(4)],6,0,'main-axis-%d'%j)
 for i in range(12):
  branch=i%3;level=i//3;path=paths[branch];t=(.14+.22*level)*2;seg=min(int(t),1)+1;start=Vector(path[seg]).lerp(Vector(path[seg+1]),t-(seg-1));a=.32+i*2.399;extent=.0105 if branch==0 else .0075;end=start+Vector((math.cos(a)*extent,math.sin(a)*extent,.0055));mid=start.lerp(end,.60)+Vector((0,0,.002));tube(A,[start,mid,end],[.00032,.00024,.00013],6,0,'terminal-shoot-%02d'%i)
  for side in [-1,1]:
   direct=Vector((math.cos(a+side*.55),math.sin(a+side*.55),.70)).normalized();idx=i*2+(side+1)//2;leaf(L,end,direct,.0032*(.88+.12*math.sin(i+.3)**2),.004*(.82+.18*math.cos(i*.73)**2),side*.28,idx)
 A.emit('slender-three-axis-framework');L.emit('twenty-four-deeply-dichotomized-leaves');semantic.update(uncertainty='Selected axis reconstruction only. Entire habit,size,color,count artistic; minimal basal junction, no claimed roots.')

def thrombolite():
 W,D,H=p['width_m'],p['depth_m'],p['height_m'];N=24;poly=[(-W/2,0)]
 # CCW x-z arch, polygon includes flat base.
 poly=[(W/2*math.cos(math.pi*i/N),H*math.sin(math.pi*i/N))for i in range(N+1)]
 points=list(poly);points +=[(x,z)for j in range(1,15)for i in range(1,29)if (x:=-W/2+W*(i+.24*math.sin(j*3.3+i))/29)**2/(W/2)**2+(z:=H*(j+.24*math.sin(i*2.1+j))/15)**2/H**2<.98]
 vv,ee,ff,*_=delaunay_2d_cdt([Vector(q)for q in points],[],[],0,1e-7);vs=[(q.x,-.12,q.y)for q in vv];fs=[];mi=[]
 def clot(x,z):
  # Branched aperiodic dark patches, not bedding laminae or surface stones.
  return math.sin(41*x+4*math.sin(18*z))+math.sin(37*z-4*math.cos(19*x))+.65*math.cos(79*x+29*z)
 for f in ff:
  q=sum((vv[k]for k in f),Vector((0,0)))/len(f);fs.append(tuple(f));c=clot(q.x,q.y);mi.append(3 if c>.60 else 4 if c>-.15 else 2)
 boundary={}
 for f in fs:
  for a,b in zip(f,f[1:]+f[:1]):key=tuple(sorted((a,b)));boundary[key]=boundary.get(key,0)+1
 edges=[e for e,k in boundary.items()if k==1];ring=list(range(N+1))
 # CDT preserves input vertex positions; find corresponding exact outline indices.
 ring=[min(range(len(vv)),key=lambda j:(vv[j]-Vector(q)).length_squared)for q in poly]
 old=ring
 for j in range(1,9):
  t=j/9;scale=math.cos(t*math.pi/2);y=-.12+D*math.sin(t*math.pi/2);new=[]
  for k,(x,z) in enumerate(poly):
   noise=1+.035*math.sin(k*.65+.4)+.020*math.cos(j*.8+k*.3);new.append(len(vs));vs.append((x*scale*noise,y,z*scale*noise))
  for k in range(len(old)):
   fs.append((old[k],old[(k+1)%len(old)],new[(k+1)%len(new)],new[k]));mi.append(0)
  old=new
 tip=len(vs);vs.append((0,-.12+D,0))
 for k in range(len(old)):fs.append((old[k],old[(k+1)%len(old)],tip));mi.append(0)
 M=Mesh();M.v=vs;M.f=fs;M.mi=mi;M.emit('one-continuous-mound-with-integrated-clotted-cut');semantic.update(mound_count=1,cutface='Front planar pedagogical exposure, macroscopic enlargement of clotted fabric, not thin-section topography.')

def oncoids():
 M=Mesh();W,D,T=p['bed_width_m'],p['bed_depth_m'],p['base_thickness_m'];outline=[(-W/2,-D*.43),(-W*.42,-D/2),(W*.40,-D/2),(W/2,-D*.34),(W*.49,D*.39),(W*.32,D/2),(-W*.38,D*.48),(-W/2,D*.27)];N=len(outline);v=[(x,y,z)for z in [0,T]for x,y in outline];f=[tuple(range(N))[::-1],tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)];M.add(v,f,0,'sediment')
 positions=[(-.071,-.049),(-.011,-.051),(.053,-.050),(-.084,.002),(-.032,.003),(.024,.005),(.079,.002),(-.070,.052),(-.014,.052),(.048,.051),(-.103,.039),(.096,.047),(-.100,-.040),(.100,-.045),(-.043,-.025),(.047,.028)]
 for i,(cx,cy) in enumerate(positions):
  cut=i<3;r=(.023 if cut else .020)*( .87+.17*math.sin(i*1.7+.4)**2);cz=T+r*.90;N=20;group='grain-%02d'%i;vs=[];fs=[];mi=[]
  def point(q,a):
   rad=math.sqrt(max(0,1-q*q))*r*(1+.055*math.sin(3*a+i)+.025*math.cos(7*a+i));return (cx+rad*math.cos(a),cy+q*r,cz+rad*math.sin(a)*(.94+.05*math.cos(i)))
  qs=[-.45,0,.48,.82,.97]if cut else[-.97,-.82,-.48,0,.48,.82,.97]
  for q in qs:
   for j in range(N):vs.append(point(q,math.tau*j/N))
  for k in range(len(qs)-1):
   for j in range(N):a=k*N+j;b=k*N+(j+1)%N;fs.append((a,b,b+N,a+N));mi.append(1 if (i+j+k)%6 else 2)
  back=len(vs);vs.append((cx,cy+r,cz))
  for j in range(N):fs.append(((len(qs)-1)*N+j,(len(qs)-1)*N+(j+1)%N,back));mi.append(1)
  if cut:
   old=list(range(N));nx=cx+r*.14;nz=cz-r*.10
   for k,frac in enumerate([.78,.57,.36,.17]):
    new=[]
    for j in range(N):
     a=math.tau*j/N;outer=Vector(vs[j]);f=frac+.035*math.sin(a*3+k*.9+i);new.append(len(vs));vs.append((nx+(outer.x-nx)*f,cy-.45*r,nz+(outer.z-nz)*f))
    for j in range(N):fs.append((old[j],old[(j+1)%N],new[(j+1)%N],new[j]));mi.append(3 if (k+(j//4 if k==1 else 0))%2==0 else 4)
    old=new
   fs.append(tuple(reversed(old)));mi.append(5)
  else:
   front=len(vs);vs.append((cx,cy-r,cz))
   for j in range(N):fs.append((j,front,(j+1)%N));mi.append(1)
  off=len(M.v);M.add(vs,fs,mi,group)
  if cut:M.groups['cut-grain-%02d'%i]=list(range(off,off+len(vs)))
 M.emit('sixteen-separated-oncoids-and-quiet-contact-bed');semantic.update(grains=16,cut_grains=3,uncertainty='Generic art bed, not measuredHydra locality. Uneven internal coatings only; no specific organism inferred.')

def caytonia():
 A=Mesh();C=Mesh();path=[(.0005*math.sin(i*.5),0,p['axis_length_m']*i/12)for i in range(13)];tube(A,path,[p['axis_base_halfwidth_m']*(1-.66*i/12)for i in range(13)],8,0,'axis',p['axis_depth_ratio']);orient=[]
 for level in range(6):
  z=.008+.0071*level
  for side in [-1,1]:
   i=level*2+(side+1)//2;at=Vector((.0005*math.sin(z/.052*6),0,z+(.00045 if side>0 else 0)));neck=at+Vector((side*.0043,side*.00045*math.cos(level*.8),.001));center=at+Vector((side*.0074,side*.00085*math.cos(level*.8),-.0002));tube(A,[at,neck,center+Vector((-side*.0009,0,.0005))],[.00025,.00020,.00015],6,0,'stalk-%02d'%i)
   # Polar axis points back toward attachment. Small proximal mouth, rounded body elsewhere.
   d=(at-center).normalized();u=Vector((0,1,0));v=d.cross(u).normalized();rr=.0029*(.90+.10*math.sin(i+1)**2);depth=.0015;vs=[];fs=[];mi=[];N=16;angles=[.24,.50,.88,1.30,1.75,2.20,2.65,2.95]
   for k,theta in enumerate(angles):
    for j in range(N):
     a=math.tau*j/N;q=center+d*(rr*math.cos(theta))+u*(depth*math.sin(theta)*math.cos(a))+v*(rr*.95*math.sin(theta)*math.sin(a));vs.append(tuple(q))
   for k in range(len(angles)-1):
    for j in range(N):a=k*N+j;b=k*N+(j+1)%N;fs.append((a,b,b+N,a+N));mi.append(2 if k==0 else 1)
   bottom=len(vs);vs.append(tuple(center-d*rr))
   for j in range(N):fs.append(((len(angles)-1)*N+j,(len(angles)-1)*N+(j+1)%N,bottom));mi.append(1)
   # Actual shallow closed mouth depression, not transparent hole or far-side slit.
   inner=[]
   for j in range(N):
    a=math.tau*j/N;inner.append(len(vs));vs.append(tuple(center+d*(rr*.78)+u*(depth*.14*math.cos(a))+v*(rr*.12*math.sin(a))))
   for j in range(N):fs.append((j,inner[j],inner[(j+1)%N],(j+1)%N));mi.append(2)
   fs.append(tuple(inner));mi.append(3);C.add(vs,fs,mi,'cupule-%02d-pair-%d'%(i,level));orient.append(dict(group='cupule-%02d-pair-%d'%(i,level),attachment=list(at),center=list(center),opening_axis=list(d),opening_vertex_count=N,vertices_per_cupule=len(vs)))
 A.emit('slender-axis-and-subopposite-stalks');C.emit('twelve-recurved-rounded-proximal-mouth-cupules');semantic.update(cupule_frames=orient,uncertainty='Organ only. 3Ddepth,pose,color,count artistic. No wholeplant association asserted geometrically; no seed arrangement shown.')

{'eophyllophyton':eophyllophyton,'thrombolite-mound':thrombolite,'oncoid-bed':oncoids,'caytonia':caytonia}[slug]()
ground_asset(col,center_xy=True);root=bpy.data.objects[col['asset_root']]
for o in col.all_objects:
 if o.type=='MESH':
  world=o.matrix_world.copy();o.data.transform(world);o.parent=None;o.matrix_world.identity();o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4)
root.location=(0,0,0);bpy.context.view_layer.update();source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');(out/'geometry-semantics.json').write_text(json.dumps(semantic,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'));bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items()if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n')
(out/'execution.json').write_text(json.dumps(dict(pid=os.getpid(),parent_pid=os.getppid(),started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),generator_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),config_sha256=hashlib.sha256(pathlib.Path(args.config).read_bytes()).hexdigest(),blender=bpy.app.version_string,argv=sys.argv),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
