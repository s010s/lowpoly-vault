# SPDX-License-Identifier: MIT
"""Original batch94 plant geometry, authored after immutable original design freeze.
Generic export helpers are shared project infrastructure. No downloaded meshes/pixels.
"""
import bpy,bmesh,sys,json,math,argparse,pathlib,hashlib,datetime,os
from mathutils import Vector,Matrix
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(args.config).read_text());p=cfg['parameters'];out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True);assert not (out/'model.glb').exists(),'Never overwrite prior geometry';slug=cfg['asset_id'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(slug,cfg['seed']);m=[make_material(k,v)for k,v in cfg['palette'].items()];semantic={'attachments':[],'leaf_frames':[],'tubes':[]}
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.groups={}
 def add(self,v,f,mi,group):
  off=len(self.v);self.v +=[tuple(q)for q in v];self.f +=[tuple(off+x for x in face)for face in f];self.mi +=([mi]*len(f)if isinstance(mi,int)else mi);self.groups.setdefault(group,[]).extend(range(off,len(self.v)));return off
 def emit(self,name):
  o=mesh_object(name,self.v,self.f,m,col)
  for face,i in zip(o.data.polygons,self.mi):face.material_index=i
  for name,idx in self.groups.items():o.vertex_groups.new(name=name).add(idx,1,'REPLACE')
  return o

def attach(child,parent,base,kind):semantic['attachments'].append(dict(child=child,parent=parent,anchor=list(base),kind=kind))
def radial(a):return Vector((math.cos(a),math.sin(a),0))
def tube(M,points,radii,sides=6,mi=0,group=None,parent=None,flat=1):
 pts=[Vector(q)for q in points];vs=[]
 for i,q in enumerate(pts):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();v=t.cross(u).normalized()
  for j in range(sides):vs.append(q+radii[i]*(u*math.cos(math.tau*j/sides)+v*flat*math.sin(math.tau*j/sides)))
 fs=[tuple(reversed(range(sides)))]
 for i in range(len(pts)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;fs.append((a,b,b+sides,a+sides))
 fs.append(tuple(range((len(pts)-1)*sides,len(pts)*sides)));off=M.add(vs,fs,mi,group);semantic['tubes'].append(dict(group=group,local_indices=list(range(len(M.groups[group])-len(vs),len(M.groups[group])-len(vs)+sides)),sides=sides,stations=len(pts)))
 if parent:attach(group,parent,pts[0],'branch-base')

def blade(M,base,direction,width,length,group,mi,parent,divided=False):
 v=Vector(direction).normalized();u=v.cross(Vector((0,0,1)))
 if u.length<.01:u=Vector((1,0,0))
 u.normalize();n=u.cross(v).normalized();base=Vector(base)
 if divided:
  left=[(-.045,0),(-.055,.14)]
  for y,w in [(.30,.50),(.52,.48),(.73,.35)]:left +=[(-.06,y-.09),(-w,y+.06),(-.065,y+.025)]
  poly=left+[(0,1)]+[(-x,y)for x,y in reversed(left)]
 else:poly=[(0,0),(-.5,.38),(0,1),(.5,.38)]
 thick=.00065 if divided else .0012;vs=[]
 for s in [-1,1]:
  for x,y in poly:vs.append(base+u*x*width+v*y*length+n*(s*thick/2+.035*width*math.sin(y*math.pi)))
 N=len(poly);fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)];M.add(vs,fs,mi,group);attach(group,parent,base,'leaf-base');semantic['leaf_frames'].append(dict(group=group,longitudinal=list(v),transverse=list(u),outline_vertices=N,base_indices=[0,N-1,N,2*N-1]))

def rhacophyton():
 M=Mesh();H=p['stem_height_m'];tube(M,[(0,0,0),(.002,0,.30),(-.002,.001,.62),(0,0,H)],[p['stem_radius_m'],.008,.005,.0014],8,0,'main-axis')
 for i in range(p['fronds']):
  a=.3+i*2.399963;d=radial(a);side=radial(a+math.pi/2);base=Vector((0,0,.18+i*.092));L=.35*(1-.038*i);fg=f'frond-{i:02d}';path=[base,base+d*L*.45+Vector((0,0,.08)),base+d*L+Vector((0,0,.13))];tube(M,path,[.004,.0027,.0008],6,0,fg,'main-axis')
  for level in range(p['pinna_pairs_per_frond']):
   t=.23+level*.19;at=path[0].lerp(path[1],t/.45)if t<=.45 else path[1].lerp(path[2],(t-.45)/.55)
   for s in [-1,1]:
    j=i*8+level*2+(s+1)//2;pg=f'pinna-{j:03d}';axis=(side*s*.88+d*.45+Vector((0,0,.20))).normalized();end=at+axis*(.12*(1-.14*level));tube(M,[at,at.lerp(end,.55)+Vector((0,0,.006)),end],[.0017,.0011,.00035],5,1,pg,fg)
    for k in range(p['forklets_per_pinna']):
     idx=j*4+k;gg=f'forklet-{idx:03d}';fb=at.lerp(end,.21+k*.20);fd=(d*.78+axis*.3+Vector((0,0,.35))).normalized();tip=fb+fd*(.029*(1-.08*level));tube(M,[fb,tip],[.00075,.0004],4,1,gg,pg)
     for sign in [-1,1]:tube(M,[tip,tip+fd*.018+side*sign*.010+Vector((0,0,.004))],[.00044,.00013],4,2,gg)
 M.emit('open-bipinnate-nonlaminate-framework');semantic.update(note='Eight historical spiral fronds,64pinnae,256bifurcated open forklets; no enlarged tip buds, reproductive organs or broad laminae.')

def sigillaria():
 A=Mesh();L=Mesh();H=p['stem_height_m'];N=p['vertical_ribs']*4;zs=[0,.17,.4,1,2,3,4,5,H];vs=[];fs=[];mi=[]
 def radius(z):return p['stem_radius_m']*(1-.23*z/H)+(.07*max(0,1-z/.4))
 for z in zs:
  for j in range(N):a=math.tau*j/N;r=radius(z)+.012*(1+math.cos(a*p['vertical_ribs']))/2;vs.append((r*math.cos(a),r*math.sin(a),z))
 fs=[tuple(reversed(range(N)))];mi=[0]
 for k in range(len(zs)-1):
  for j in range(N):a=k*N+j;b=k*N+(j+1)%N;fs.append((a,b,b+N,a+N));mi.append(1 if j%4 in[0,3]else 0)
 fs.append(tuple(range((len(zs)-1)*N,len(zs)*N)));mi.append(1);A.add(vs,fs,mi,'main-axis')
 for rib in range(p['vertical_ribs']):
  a=math.tau*rib/p['vertical_ribs'];d=radial(a);u=radial(a+math.pi/2)
  for k in range(p['scars_per_rib']):
   z=.38+k*.307;center=d*(radius(z)+.013)+Vector((0,0,z));poly=[(-.040,-.046),(-.048,.020),(-.025,.045),(.025,.045),(.048,.020),(.040,-.046)];vv=[center+u*x+Vector((0,0,y))+d*t for t in[-.010,.0015]for x,y in poly];nn=len(poly);ff=[tuple(reversed(range(nn))),tuple(range(nn,2*nn))]+[(j,(j+1)%nn,(j+1)%nn+nn,j+nn)for j in range(nn)];gg=f'scar-{rib:02d}-{k:02d}';A.add(vv,ff,2,gg);attach(gg,'main-axis',center-d*.008,'shallow-scar-inset')
 for i in range(p['rhizomorph_beginnings']):
  a=.45+i*math.pi/2;d=radial(a);tube(A,[d*.10+Vector((0,0,.11)),d*.33+Vector((0,0,.07)),d*.64+Vector((0,0,.027))],[.12,.075,.025],8,0,f'rhizomorph-{i}','main-axis')
 for i in range(p['crown_leaves']):
  a=i*2.399963;d=radial(a);ring=i//14;z=H-.18+ring*.09;base=d*(.15-.035*ring)+Vector((0,0,z));length=p['leaf_nominal_length_m']*(.86+.14*(i%7)/6);reach=[1.0,.8,.50][ring];up=[.15,.60,1.0][ring];path=[base]
  for t in [.20,.45,.70,1]:path.append(base+d*(length*reach*t)+Vector((0,0,length*(up*math.sin(t*math.pi*.72)-.18*t*t))))
  tube(L,path,[.035,.044,.037,.022,.001],4,3+(i%4==0),f'leaf-{i:02d}','main-axis',flat=.09)
 A.emit('unbranched-twelve-rib-column-separated-leaf-scars');L.emit('forty-two-simple-strap-microphylls');semantic.update(vertical_ribs=12,note='One selected unbranched ribbed habit; scars shallow and vertically separated. Four short basal beginnings, no whole root reconstruction.')

def pseudobornia():
 A=Mesh();L=Mesh();H=p['stem_height_m'];nodes=[.42,.76,1.10,1.43];zs=[0]
 for z in nodes:zs +=[z-.013,z,z+.013]
 zs +=[H];rs=[p['stem_radius_m']*(1-.65*z/H)*(1.07 if z in nodes else 1)for z in zs];tube(A,[(0,0,z)for z in zs],rs,10,0,'main-axis')
 nodelist=[0,0,1,2,2,3];angles=[.2,3.35,1.8,.75,3.88,5.3]
 for i,(ni,a)in enumerate(zip(nodelist,angles)):
  base=Vector((0,0,nodes[ni]));d=radial(a);reach=.43-.034*ni;end=base+d*reach+Vector((0,0,.28));sg=f'second-{i:02d}';tube(A,[base,base.lerp(end,.5),end],[.018,.013,.006],7,0,sg,'main-axis')
  for j in range(2):
   idx=i*2+j;at=base.lerp(end,.51+j*.39);dd=radial(a+(-.58 if j==0 else .42));te=at+dd*.19+Vector((0,0,.16));tg=f'third-{idx:02d}';tube(A,[at,te],[.006,.0028],6,0,tg,sg);fg=f'fourth-{idx:02d}';fe=te+dd*.095+Vector((0,0,.14));tube(A,[te,te.lerp(fe,.5),fe],[.0029,.0022,.0012],6,1,fg,tg)
   for node in range(p['leaf_nodes_per_terminal']):
    at=te.lerp(fe,.31+node*.45)
    for q in range(p['leaves_per_whorl']):
     li=idx*8+node*4+q;ld=radial(a+q*math.pi/2+node*.35)*.58+Vector((0,0,.82));blade(L,at,ld,p['leaf_nominal_width_m'],p['leaf_nominal_length_m'],f'leaf-{li:03d}',2+(li%5==0),fg,True)
 A.emit('articulated-four-order-open-scaffold');L.emit('ninety-six-coherent-laciniate-leaves-in-four-leaf-whorls');semantic.update(main_stem_branch_nodes=nodes,second_order_node_assignment=nodelist,note='Leaf whorls on thin fourth-order nodal twigs only; two nodes of four leaves each. No trunk foliage, modern undivided needles or cones.')

def calamites():
 A=Mesh();L=Mesh();H=p['stem_height_m'];nodes=[.50+.54*i for i in range(p['nodes'])];zs=[0]
 for z in nodes:zs +=[z-.025,z,z+.025]
 zs +=[H];rs=[p['stem_radius_m']*(1-.55*z/H)*(1.045 if z in nodes else 1)for z in zs];tube(A,[(0,0,z)for z in zs],rs,12,0,'main-axis')
 for tier in range(p['branch_tiers']):
  z=nodes[tier*2+1]
  for j in range(p['branches_per_tier']):
   i=tier*5+j;a=.22+tier*.47+j*math.tau/5;d=radial(a);base=Vector((0,0,z));end=base+d*(1.18-.15*tier)+Vector((0,0,.32));pg=f'primary-{i:02d}';tube(A,[base,base.lerp(end,.36),base.lerp(end,.69),end],[.048-.005*tier,.034,.020,.009],7,0,pg,'main-axis')
   for k in range(p['secondary_twigs_per_branch']):
    idx=i*2+k;at=base.lerp(end,.56+k*.35);dd=radial(a+(-.66 if k==0 else .51));tip=at+dd*.23+Vector((0,0,.20));sg=f'secondary-{idx:02d}';tube(A,[at,at.lerp(tip,.5),tip],[.010,.006,.002],6,1,sg,pg)
    for node in range(p['leaf_whorls_per_twig']):
     lb=at.lerp(tip,.37+node*.43)
     for q in range(p['leaves_per_whorl']):
      li=idx*14+node*7+q;ld=radial(a+q*math.tau/7+node*.22)+Vector((0,0,.20));blade(L,lb,ld,p['leaf_nominal_width_m'],p['leaf_nominal_length_m'],f'leaf-{li:03d}',2+(li%6==0),sg)
 A.emit('quiet-barked-eight-node-woody-sphenopsid');L.emit('five-hundred-sixty-small-lanceolate-whorled-leaves');semantic.update(main_stem_nodes=nodes,branch_tier_nodes=[nodes[i*2+1]for i in range(4)],note='Modest integrated trunk nodes, quiet external bark. Cast ribs not copied as external bark. Small subordinate Annularia-like leaves.')

{'rhacophyton':rhacophyton,'sigillaria':sigillaria,'pseudobornia':pseudobornia,'calamites':calamites}[slug]()
offset=ground_asset(col,center_xy=True);root=bpy.data.objects[col['asset_root']]
for a in semantic['attachments']:a['anchor']=[x+y for x,y in zip(a['anchor'],offset)]
semantic['grounding_translation_m']=offset;semantic['normalization_applied']=False
for o in col.all_objects:
 if o.type=='MESH':
  o.data.transform(o.matrix_world.copy());o.parent=None;o.matrix_world.identity();o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4)
root.location=(0,0,0);bpy.context.view_layer.update();source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');(out/'geometry-semantics.json').write_text(json.dumps(semantic,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'));bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items()if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n')
(out/'execution.json').write_text(json.dumps(dict(pid=os.getpid(),parent_pid=os.getppid(),started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),generator_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),config_sha256=hashlib.sha256(pathlib.Path(args.config).read_bytes()).hexdigest(),blender=bpy.app.version_string,argv=sys.argv),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
