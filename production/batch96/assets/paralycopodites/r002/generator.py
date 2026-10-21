# SPDX-License-Identifier: MIT
"""Batch96 original plant constructions, authored after complete immutable design freeze.
Only generic mesh/export infrastructure is shared. No imported models or reference pixels.
"""
import bpy,bmesh,sys,json,math,argparse,pathlib,hashlib,datetime,os
from mathutils import Vector,Matrix
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(args.config).read_text());p=cfg['parameters'];out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True);assert not(out/'model.glb').exists(),'Preserve old geometry';slug=cfg['asset_id'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(slug,cfg['seed']);m=[make_material(k,v)for k,v in cfg['palette'].items()];semantic={'attachments':[],'leaf_frames':[],'tubes':[]}
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.groups={}
 def add(self,v,f,mi,group):
  off=len(self.v);self.v +=[tuple(q)for q in v];self.f +=[tuple(off+x for x in face)for face in f];self.mi +=[mi]*len(f)if isinstance(mi,int)else mi;self.groups.setdefault(group,[]).extend(range(off,len(self.v)))
 def emit(self,name):
  o=mesh_object(name,self.v,self.f,m,col)
  for face,i in zip(o.data.polygons,self.mi):face.material_index=i
  for name,ix in self.groups.items():o.vertex_groups.new(name=name).add(ix,1,'REPLACE')
  return o
Z=Vector((0,0,1));rad=lambda a:Vector((math.cos(a),math.sin(a),0))
def attach(child,parent,kind='branch-base'):semantic['attachments'].append(dict(child=child,parent=parent,kind=kind))
def tube(M,points,radii,sides,mi,group,parent=None):
 pts=[Vector(q)for q in points];vs=[]
 for i,q in enumerate(pts):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();u=t.cross(Z)
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();v=t.cross(u).normalized()
  for j in range(sides):vs.append(q+radii[i]*(u*math.cos(math.tau*j/sides)+v*math.sin(math.tau*j/sides)))
 fs=[tuple(reversed(range(sides)))]+[(i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j)for i in range(len(pts)-1)for j in range(sides)]+[tuple(range((len(pts)-1)*sides,len(pts)*sides))];M.add(vs,fs,mi,group);semantic['tubes'].append(dict(group=group,sides=sides,stations=len(pts),base_indices=list(range(sides))))
 if parent:attach(group,parent)
def blade(M,base,direction,width,length,group,mi,parent,lobed=False):
 v=Vector(direction).normalized();u=v.cross(Z)
 if u.length<.01:u=Vector((1,0,0))
 u.normalize();n=u.cross(v).normalized();base=Vector(base)
 if lobed:poly=[(0,0),(-.34,.18),(-.14,.29),(-.50,.44),(-.17,.56),(-.35,.76),(0,1),(.35,.76),(.17,.56),(.50,.44),(.14,.29),(.34,.18)]
 elif slug=='paralycopodites':poly=[(0,0),(-.5,.46),(0,1),(.5,.46)]
 else:poly=[(0,0),(-.42,.22),(-.50,.65),(-.25,.91),(0,1),(.25,.91),(.50,.65),(.42,.22)]
 thick=.0007 if lobed else .0015;vs=[base+u*x*width+v*y*length+n*(s*thick/2+.018*width*math.sin(y*math.pi))for s in[-1,1]for x,y in poly];N=len(poly);fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)];M.add(vs,fs,mi,group);attach(group,parent,'leaf-base');semantic['leaf_frames'].append(dict(group=group,longitudinal=list(v),transverse=list(u),outline_vertices=N,base_indices=[0,N]))
def point_on(path,t):
 f=t*(len(path)-1);i=min(int(f),len(path)-2);return Vector(path[i]).lerp(Vector(path[i+1]),f-i)

def paralycopodites():
 A=Mesh();L=Mesh();H=p['trunk_height_m'];tube(A,[(0,0,0),(0,0,.3),(0,0,H*.5),(0,0,H)],[.19,.15,.13,.075],10,0,'main-axis')
 crowns=[]
 for i,s in enumerate([-1,1]):
  path=[Vector((0,0,H-.025)),Vector((s*.31,0,H+.52)),Vector((s*.56,.025*s,H+1.1))];crowns.append(path);tube(A,path,[.075,.050,.026],8,0,f'crown-{i}','main-axis')
 systems=[]
 for i in range(p['main_lateral_systems']):
  s=-1 if i%2==0 else 1;z=.75+(i//2)*.48+(i%2)*.13;systems.append((Vector((0,0,z)),s,'main-axis',.80-.045*(i//2)))
 for i,path in enumerate(crowns):
  for j in range(2):systems.append((point_on(path,.35+j*.42),-1 if i==0 else 1,f'crown-{i}',.54-.10*j))
 for i,(base,s,parent,reach)in enumerate(systems):
  d=Vector((s,0,0));side=Vector((0,1,0));tip=base+d*reach+Z*.21;path=[base,base+d*reach*.44+Z*.13,tip];g=f'lateral-{i:02d}';tube(A,path,[.025,.014,.006],7,0,g,parent)
  for j in range(4):
   t=.25+j*.20;at=point_on(path,t);spread=(-1 if j%2==0 else 1)*(.17+.02*(j//2));end=at+d*(reach*(.40-.035*j))+side*spread+Z*(.11+.015*j);tg=f'twig-{i*4+j:03d}';tube(A,[at,end],[.007,.0023],5,1,tg,g);dir=(end-at).normalized()
   for k in range(p['microphylls_per_terminal']):
    li=(i*4+j)*7+k;lb=at.lerp(end,.12+.11*k);ld=(dir*.3+side*((-1)**k)*.7+Z*.6).normalized();blade(L,lb,ld,.004,.025,f'leaf-{li:03d}',1+(li%5==0),tg)
   cg=f'cone-{i*4+j:03d}';cb=end-dir*.002;length=p['cone_length_m'];r=p['cone_width_m']/2;tube(A,[cb,cb+dir*length*.15,cb+dir*length*.72,cb+dir*length],[.0024,r,r*.90,.001],6,3,cg,tg)
 for k in range(p['trunk_microphylls']):
  a=k*2.399963;z=.25+k*.040;rr=.15-.075*z/H;base=rad(a)*(rr*.90)+Z*z;li=392+k;blade(L,base,rad(a)*.35+Z,.006,.035,f'leaf-{li:03d}',1,'main-axis')
 for i in range(4):
  d=rad(.4+i*math.pi/2);tube(A,[d*.07+Z*.09,d*.23+Z*.045,d*.43+Z*.02],[.095,.055,.018],7,0,f'root-{i}','main-axis')
 A.emit('opposite-row-compact-lycopsid-scaffold');L.emit('small-persistent-microphylls');semantic['note']='Two opposite lateral rows, limited crown fork, compact planar branch systems; small elongated terminal cones. Historical anatomy pixels do not demonstrate whole habit.'

def lyginopteris():
 A=Mesh();L=Mesh();path=[Vector((0,0,0)),Vector((.08,.015,.40)),Vector((.23,-.01,.85)),Vector((.35,.04,1.20)),Vector((p['lean_x_m'],.015,p['stem_height_m']))];tube(A,path,[.026,.022,.018,.014,.006],8,0,'main-axis')
 # Dead support reaches and physically contacts the leaning living axis at station2.
 support=[Vector((.34,-.10,0)),Vector((.23,-.01,.85)),Vector((.19,.015,1.04))];tube(A,support,[.026,.017,.008],7,4,'support-axis');tube(A,[support[1],Vector((.36,.015,1.00))],[.016,.006],6,4,'support-fork','support-axis');semantic['support_contact']={'living':'main-axis','support':'support-axis','world_point_pre_ground':list(path[2])}
 for i in range(6):
  base=point_on(path,.18+i*.135);a=.35+i*2.399963;d=rad(a);side=rad(a+math.pi/2);fg=f'frond-{i:02d}';fork=base+d*(.19-.012*i)+Z*.06;tube(A,[base,fork],[.0065,.0048],6,0,fg,'main-axis')
  for j,s in enumerate([-1,1]):
   fi=i*2+j;ag=f'fan-{fi:02d}';end=fork+d*(.32-.018*i)+side*s*.13+Z*.06;tube(A,[fork,end],[.0049,.0014],5,0,ag,fg)
   for k in range(3):
    idx=fi*3+k;at=fork.lerp(end,.24+k*.28);pg=f'pinna-{idx:03d}';dd=(side*s*.72+d*.5+Z*.08).normalized();pe=at+dd*(.14-.015*k);tube(A,[at,pe],[.0018,.0005],5,0,pg,ag)
    for q in range(6):
     li=idx*6+q;lb=at.lerp(pe,.13+(q//2)*.30);ld=(d*.65+dd*.24+side*((-1)**q)*.55+Z*.04).normalized();blade(L,lb,ld,.028,.045,f'leaf-{li:03d}',1+(li%5==0),pg,True)
 for i in range(24):
  t=.08+i*.035;at=point_on(path,t);a=i*2.399963;d=rad(a);r=.026*(1-.65*t);base=at+d*r*.75;tube(A,[base,base+d*.005,base+d*.007],[.0031,.0034,.0018],5,3,f'gland-{i:02d}','main-axis')
 A.emit('leaning-axis-forked-support-and-scattered-gland-bases');L.emit('small-lobed-bipartite-frond-pinnules')

def medullosa():
 A=Mesh();L=Mesh();H=p['stem_height_m'];tube(A,[(0,0,0),(.015,0,.25),(0,.015,1.4),(0,0,H)],[.18,.15,.135,.105],10,0,'main-axis')
 for i in range(12):
  a=i*2.399963;base=Vector((0,0,.35+i*.125));d=rad(a);tube(A,[base,base+d*.18+Z*.07],[.055,.023],6,0,f'stub-{i:02d}','main-axis')
 for i in range(6):
  a=.23+i*2.399963;d=rad(a);side=rad(a+math.pi/2);base=Vector((0,0,H-.70+i*.11));fg=f'frond-{i:02d}';fork=base+d*.50+Z*(.35+.055*i);tube(A,[base,base.lerp(fork,.5),fork],[.055,.046,.035],8,1,fg,'main-axis')
  for j,s in enumerate([-1,1]):
   fi=i*2+j;ag=f'fan-{fi:02d}';end=fork+d*1.34+side*s*.47+Z*(.15-.045*i);mid=fork.lerp(end,.52)+Z*.28;path=[fork,mid,end];tube(A,path,[.036,.020,.006],6,1,ag,fg)
   for k in range(4):
    idx=fi*4+k;at=point_on(path,.19+k*.22);pg=f'pinna-{idx:03d}';dd=(side*s*.80+d*.55+Z*.06).normalized();pe=at+dd*(.62-.085*k)+Z*(-.10);tube(A,[at,at.lerp(pe,.55),pe],[.011,.007,.0022],5,1,pg,ag)
    for q in range(8):
     li=idx*8+q;t=.12+(q//2)*.22;lb=at.lerp(pe,t);ld=(d*.76+side*((-1)**q)*.55+Z*(-.18)).normalized();blade(L,lb,ld,.072,.19*(1-.07*k),f'leaf-{li:03d}',2+(li%6==0),pg)
 A.emit('self-standing-stem-with-sparse-petiole-stubs');L.emit('six-massive-multi-order-compound-fronds')

def ribbon(M,path,width,group,mi,parent):
 path=[Vector(q)for q in path];v=(path[-1]-path[0]).normalized();u=v.cross(Z)
 if u.length<.01:u=Vector((1,0,0))
 u.normalize();n=u.cross(v).normalized();N=len(path);bands=5;stride=6;vs=[];widths=[.13,1,1,.05];thick=.0025
 for sign in[-1,1]:
  for i,pt in enumerate(path):
   for j in range(stride):vs.append(pt+u*((j/bands-.5)*width*widths[i])+n*sign*thick/2)
 fs=[];mis=[];layer=N*stride
 for i in range(N-1):
  for j in range(bands):
   a=i*stride+j;fs +=[(a+1,a,a+stride,a+stride+1),(a+layer,a+1+layer,a+stride+1+layer,a+stride+layer)];mis +=[mi if j%2==0 else 2]*2
 for i in range(N-1):
  a=i*stride;b=a+stride;fs +=[(a,b,b+layer,a+layer),(a+5+layer,b+5+layer,b+5,a+5)];mis +=[mi,mi]
 for j in range(bands):
  a=j;b=(N-1)*stride+j;fs +=[(a,a+1,a+1+layer,a+layer),(b+layer,b+1+layer,b+1,b)];mis +=[mi,mi]
 M.add(vs,fs,mis,group);attach(group,parent,'leaf-base');semantic['leaf_frames'].append(dict(group=group,longitudinal=list(v),transverse=list(u),outline_vertices=None,base_indices=list(range(stride))+list(range(layer,layer+stride))))

def cordaites():
 A=Mesh();L=Mesh();H=p['trunk_height_m'];tube(A,[(0,0,0),(.02,0,.35),(0,.02,3.5),(0,0,5.5),(.03,0,H)],[.30,.23,.18,.11,.035],12,0,'main-axis')
 for i in range(7):
  a=.25+i*2.399963;d=rad(a);side=rad(a+math.pi/2);z=3.65+i*.45;base=Vector((0,0,z));end=base+d*(1.38-.10*i)+Z*(.65-.03*i);lg=f'limb-{i:02d}';limbpath=[base,base.lerp(end,.48)+Z*.10,end];tube(A,limbpath,[.082-.006*i,.050-.004*i,.021],8,0,lg,'main-axis')
  for j in range(3):
   ti=i*3+j;at=point_on(limbpath,.45+j*.25);dd=(d*.85+side*(j-1)*.45).normalized();tip=at+dd*(.40-.03*i)+Z*.28;tg=f'twig-{ti:02d}';tube(A,[at,tip],[.024,.008],6,0,tg,lg)
   for k in range(5):
    li=ti*5+k;lb=at.lerp(tip,.50+k*.10);theta=a+k*2.399963+j*.18;ld=rad(theta);length=p['leaf_nominal_length_m']*(.84+.04*(li%5));path=[lb+ld*(length*t*.92)+Z*(length*(.24*math.sin(t*math.pi)-.50*t*t))for t in[0,.30,.70,1]];ribbon(L,path,p['leaf_nominal_width_m']*(.90+.05*(li%3)),f'leaf-{li:03d}',1 if li%7 else 3,tg)
 A.emit('upland-juvenile-trunk-and-upper-woody-crown');L.emit('individual-parallel-sided-strap-leaves-equal-vein-bands')

{'paralycopodites':paralycopodites,'lyginopteris':lyginopteris,'medullosa':medullosa,'cordaites':cordaites}[slug]()
offset=ground_asset(col,center_xy=True);root=bpy.data.objects[col['asset_root']];semantic['grounding_translation_m']=offset;semantic['normalization_applied']=False
for o in col.all_objects:
 if o.type=='MESH':o.data.transform(o.matrix_world.copy());o.parent=None;o.matrix_world.identity();o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4)
root.location=(0,0,0);bpy.context.view_layer.update();source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');(out/'geometry-semantics.json').write_text(json.dumps(semantic,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'));bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items()if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n')
(out/'execution.json').write_text(json.dumps(dict(pid=os.getpid(),parent_pid=os.getppid(),started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),generator_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),config_sha256=hashlib.sha256(pathlib.Path(args.config).read_bytes()).hexdigest(),blender=bpy.app.version_string,argv=sys.argv),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
