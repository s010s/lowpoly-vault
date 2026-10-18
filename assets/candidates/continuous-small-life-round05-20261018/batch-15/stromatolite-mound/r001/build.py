# SPDX-License-Identifier: MIT
"""Original evidence-informed marine teaching forms. Blender -b -t 2 --python build.py -- --config config.json --output /absolute/r001 [--preview]."""
import bpy,sys,math,json,random,hashlib,argparse
from pathlib import Path
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews
pi=math.pi
class Mesh:
 def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  off=len(self.v);self.v+=v;self.f += [tuple(off+i for i in q) for q in f];self.mi += mi if isinstance(mi,list) else [mi]*len(f)
 def finish(self,c,smooth=True):
  o=mesh_object(self.name,self.v,self.f,self.mats,c)
  for p,m in zip(o.data.polygons,self.mi):p.material_index=m;p.use_smooth=smooth
  return o
 def tube(self,pts,rads,mat=0,n=12,hollow=False):
  ps=[Vector(p) for p in pts];vs=[];fs=[];mis=[]
  for j,p in enumerate(ps):
   d=(ps[min(j+1,len(ps)-1)]-ps[max(j-1,0)]).normalized();u=d.cross(Vector((0,1,0)))
   if u.length<.01:u=d.cross(Vector((1,0,0)))
   u.normalize();w=d.cross(u).normalized()
   for k in range(n):a=2*pi*k/n;vs.append(tuple(p+rads[j]*(u*math.cos(a)+w*math.sin(a))))
  fs.append(tuple(reversed(range(n))));mis.append(mat)
  for j in range(len(ps)-1):
   for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mis.append(mat)
  base=(len(ps)-1)*n
  if hollow:
   # A closed wall/rim/interior bowl, with the visible opening modeled in geometry.
   for depth,ratio in [(0,.70),(.38,.64),(2.1,.42)]:
    p=ps[-1]-d*rads[-1]*depth
    for k in range(n):a=2*pi*k/n;vs.append(tuple(p+rads[-1]*ratio*(u*math.cos(a)+w*math.sin(a))))
   for j in range(3):
    for k in range(n):fs.append((base+j*n+k,base+j*n+(k+1)%n,base+(j+1)*n+(k+1)%n,base+(j+1)*n+k));mis.append(mat if j==0 else min(mat+1,len(self.mats)-1))
   fs.append(tuple(base+3*n+k for k in range(n)));mis.append(min(mat+1,len(self.mats)-1))
  else:fs.append(tuple(base+k for k in range(n)));mis.append(mat)
  self.add(vs,fs,mis)
 def ellipsoid(self,p,s,mat=0,n=16,r=9):
  vs=[(p[0],p[1],p[2]+s[2])];fs=[]
  for j in range(1,r):
   a=pi*j/r
   for k in range(n):b=2*pi*k/n;vs.append((p[0]+s[0]*math.sin(a)*math.cos(b),p[1]+s[1]*math.sin(a)*math.sin(b),p[2]+s[2]*math.cos(a)))
  bot=len(vs);vs.append((p[0],p[1],p[2]-s[2]))
  for k in range(n):fs.append((0,1+k,1+(k+1)%n))
  for j in range(r-2):
   for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;fs.append((a,b,b+n,a+n))
  for k in range(n):fs.append((bot,1+(r-2)*n+(k+1)%n,1+(r-2)*n+k))
  self.add(vs,fs,mat)

def smooth_path(points,n=28):
 # Catmull-Rom interpolation preserves named bends and a continuous taper.
 p=[Vector(q) for q in points];out=[]
 for i in range(n):
  t=i/(n-1)*(len(p)-1);k=min(int(t),len(p)-2);t-=k;a=p[max(0,k-1)];b=p[k];c=p[k+1];d=p[min(len(p)-1,k+2)]
  out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 return out

def beelzebufo(c,m):
 torso=Mesh('continuous-broad-flanged-head-and-low-frog-body',m);legs=Mesh('muscular-folded-hindlimbs-and-grounded-forelimbs',m);digits=Mesh('splayed-grounded-simplified-digits',m);eyes=Mesh('small-bony-orbital-rises-and-eyes',m);mouth=Mesh('restrained-closed-mouth-line',m)
 # One smooth axial loft, with broad posterolateral head corners and a distinct stout trunk.
 prof=[(-.112,.025,.032,.008),(-.105,.060,.034,.018),(-.085,.087,.039,.027),(-.057,.095,.041,.034),(-.028,.084,.040,.030),(-.004,.078,.043,.040),(.030,.079,.045,.047),(.063,.068,.042,.040),(.087,.047,.035,.027),(.105,.018,.028,.012)];n=28;vs=[];fs=[]
 for j,(y,rx,z,rz) in enumerate(prof):
  for k in range(n):a=2*pi*k/n;vs.append((rx*math.cos(a),y,z+rz*math.sin(a)))
 fs.append(tuple(reversed(range(n))))
 for j in range(len(prof)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 fs.append(tuple((len(prof)-1)*n+k for k in range(n)));torso.add(vs,[tuple(reversed(f)) for f in fs],0);o=torso.finish(c);sub=o.modifiers.new('Soft anatomical head-to-trunk transition','SUBSURF');sub.levels=1;sub.render_levels=1
 for sign in [-1,1]:
  # Hind leg follows a visible out-and-back fold, with a broad thigh and tapering shin.
  ps=smooth_path([(sign*.053,.045,.041),(sign*.095,.063,.036),(sign*.100,.034,.023),(sign*.069,.025,.015),(sign*.092,.064,.008)],22);r=[.023*(1-t)+.005*t for t in [i/21 for i in range(22)]];legs.tube(ps,r,0,n=14)
  ps=smooth_path([(sign*.065,-.036,.032),(sign*.087,-.024,.022),(sign*.090,-.061,.012),(sign*.103,-.073,.006)],16);legs.tube(ps,[.011*(1-i/15)+.004*(i/15) for i in range(16)],0,n=12)
  for idx,base in enumerate([(sign*.103,-.073,.006),(sign*.092,.064,.008)]):
   for k in range(3 if idx==0 else 4):
    ang=(-.9+.6*k);dx=sign*(.008+.004*math.sin(ang));dy=(-.017 if idx==0 else .019)*(1-.12*abs(k-1));p=[base,(base[0]+dx*.65,base[1]+dy*.60,.0035),(base[0]+dx,base[1]+dy,.0023)];digits.tube(p,[.0028,.0019,.0008],1,n=8)
  eyes.ellipsoid((sign*.052,-.065,.065),(.020,.019,.011),0,n=16,r=8)
  eyes.ellipsoid((sign*.055,-.075,.070),(.008,.007,.0055),2,n=16,r=8)
  eyes.ellipsoid((sign*.055,-.079,.072),(.0032,.0022,.0034),3,n=12,r=7)
 # A quiet closed line follows broad snout contour rather than a toothy grin.
 ps=[(-.066+.132*i/18,-.094+.014*abs(-1+2*i/18)**1.7,.034-.002*(1-abs(-1+2*i/18))) for i in range(19)];mouth.tube(ps,[.0008]*19,4,n=6)
 legs.finish(c);digits.finish(c);eyes.finish(c);mouth.finish(c)

def pluricarpellatia(c,m):
 rhiz=Mesh('horizontal-rhizome-with-visible-petiole-bases',m);roots=Mesh('rooted-shallow-freshwater-rootlets',m);pet=Mesh('curved-simple-petioles',m);leaves=Mesh('simple-cordate-to-peltate-leaf-blades',m)
 ps=smooth_path([(-.072,.006,.010),(-.035,-.001,.009),(.010,.003,.010),(.052,.011,.012),(.075,.006,.009)],22);rhiz.tube(ps,[.0045*(1-.30*i/21) for i in range(22)],0,n=12)
 specs=[(-.058,.008,-.073,-.025,.071,.023,.029,-.45),(-.035,.002,-.032,.036,.093,.027,.034,.4),(-.009,.003,.005,-.036,.104,.029,.036,-.2),(.017,.007,.033,.035,.081,.023,.030,.3),(.046,.011,.067,-.018,.063,.021,.027,.6),(.064,.008,.065,.018,.043,.013,.018,.2)]
 for idx,(x,y,cx,cy,h,rx,ry,rot) in enumerate(specs):
  start=Vector((x,y,.010));center=Vector((cx,cy,h));ps=smooth_path([start,start+Vector((.002,0,.016)),(start+center)*.5+Vector((-.004,.002,0)),center],15);pet.tube(ps,[.0015*(1-.3*i/14) for i in range(15)],1,n=8)
  for sign in [-1,1]:
   for q in range(2):
    tip=start+Vector((sign*(.012+.004*q),.008*(q-.4),-.009));rp=smooth_path([start,start+Vector((sign*.004,0,-.003)),tip],7);roots.tube(rp,[.0008*(1-.86*i/6) for i in range(7)],0,n=6)
  n=28;v=[];f=[]
  for bottom in [False,True]:
   v.append(tuple(center+Vector((0,0,-.0007 if bottom else .0035))))
   for k in range(n):
    a=2*pi*k/n;notch=math.exp(-((a-pi/2)/.31)**2);xx=rx*math.cos(a)*(1+.13*math.sin(a));yy=ry*math.sin(a)-.011*notch;zz=-.0028+.0023*math.cos(a*2)+.002*math.sin(a+idx*.3);z=zz-(.0007 if bottom else 0);v.append(tuple(center+Vector((xx*math.cos(rot)-yy*math.sin(rot),xx*math.sin(rot)+yy*math.cos(rot),z))))
  off=n+1
  for k in range(n):q=(k+1)%n;f.extend([(0,k+1,q+1),(off,off+q+1,off+k+1),(k+1,off+k+1,off+q+1,q+1)])
  leaves.add(v,f,2 if idx<4 else 3)
 rhiz.finish(c);roots.finish(c);pet.finish(c);leaves.finish(c)

def small_blade(mesh,start,direction,length,width,mat,up):
 p=Vector(start);u=Vector(direction).normalized();v=u.cross(Vector((0,0,1))).normalized();z=Vector((0,0,1));outline=[p,p+u*length*.30+v*width,p+u*length*.74+v*width*.65+z*up*.5,p+u*length+z*up,p+u*length*.74-v*width*.65+z*up*.5,p+u*length*.30-v*width]
 ctr=p+u*length*.48+z*(up*.33+width*.13);vs=[tuple(q) for q in outline]+[tuple(ctr),tuple(ctr-z*.0015)];fs=[]
 for k in range(6):fs.extend([(6,k,(k+1)%6),(7,(k+1)%6,k)])
 mesh.add(vs,fs,mat)

def paratingia(c,m):
 trunk=Mesh('slender-single-stem-with-crown-leaf-bases',m);rach=Mesh('arching-compound-leaf-rachises',m);pinn=Mesh('four-pinnule-rows-on-each-rachis-two-large-above-two-small-below',m)
 ps=smooth_path([(0,0,0),(.006,.003,.23),(-.004,.002,.51),(.005,0,.74),(0,0,.82)],26);trunk.tube(ps,[.020*(1-.58*i/25) for i in range(26)],0,n=14)
 # Eight compound leaves form a modest crown; every rachis independently has four pinnule rows.
 for idx in range(8):
  ang=idx*2*pi/8+.12*math.sin(idx*1.6);u=Vector((math.cos(ang),math.sin(ang),0));v=Vector((-math.sin(ang),math.cos(ang),0));base=Vector((0,0,.66+.025*(idx%4)));L=.31+.045*math.sin(idx*1.3);height=.14 if idx%3 else .06
  ps=[base+u*(L*t)+v*.012*math.sin(pi*t)+Vector((0,0,height*math.sin(pi*t*.85)-.045*t*t)) for t in [i/21 for i in range(22)]];rach.tube(ps,[.005*(1-.90*i/21) for i in range(22)],1,n=8)
  for j in range(7):
   t=.16+j*.112;pos=ps[round(t*21)];length=.085*math.sin(pi*t)**.75*(1-.30*t);width=length*.15
   for sign in [-1,1]:
    # Adaxial pair is larger and lifted; abaxial pair is smaller and visibly below each side.
    d=(v*sign*.94+u*.34).normalized();small_blade(pinn,pos+Vector((0,0,.003)),d,length*(1 if sign>0 else .90),width,2,.006)
    d=(v*sign*.84+u*.54).normalized();small_blade(pinn,pos+Vector((0,0,-.004)),d,length*.52,width*.61,3,-.010)
 trunk.finish(c);rach.finish(c);pinn.finish(c,False)

def stromatolite_mound(c,m):
 rock=Mesh('low-microbial-mound-with-continuous-domed-laminae',m)
 # An intentional front teaching face exposes coherent nested curved laminae.
 n=32;layers=10;vs=[];fs=[];mi=[]
 # Each layer is a solid half-domed shell, joined at the front section and base.
 def point(r,a,z):return (r*math.cos(a),r*.76*math.sin(a)-.025,z)
 for layer in range(layers):
  h=(layer+1)*.014;rx=.29;th=.014;vv=[];ff=[]
  # Outer and inner concentric dome surfaces sharing a deliberate low front section.
  for inner in [False,True]:
   for j in range(6):
    t=j/5;rr=rx*(1-t*.998);zz=(h-th if inner else h)*(math.sin(t*pi/2)**.82)+.008
    for k in range(n+1):
     a=pi*k/n;rr2=rr*(1+.045*math.cos(3*a+.3));vv.append(point(rr2,a,zz+.004*math.sin(2*a)*math.sin(pi*t)))
  off=6*(n+1)
  for j in range(5):
   for k in range(n):a=j*(n+1)+k;b=a+1;ff.extend([(a,b,b+n+1,a+n+1),(off+a,off+a+n+1,off+b+n+1,off+b)])
  boundary=list(range(n+1))+[j*(n+1)+n for j in range(1,6)]+[5*(n+1)+k for k in range(n-1,-1,-1)]+[j*(n+1) for j in range(4,0,-1)]
  for k,a in enumerate(boundary):b=boundary[(k+1)%len(boundary)];ff.append((a,off+a,off+b,b))
  # Weld only within each independent lamina, preserving material interfaces as separate solids.
  unique=[];index={};mapping=[]
  for v in vv:
   key=tuple(round(x,10) for x in v)
   if key not in index:index[key]=len(unique);unique.append(v)
   mapping.append(index[key])
  cleaned=[]
  for face in ff:
   q=[]
   for i in face:
    if not q or q[-1]!=mapping[i]:q.append(mapping[i])
   if len(q)>1 and q[0]==q[-1]:q.pop()
   if len(set(q))>=3:cleaned.append(tuple(q))
  rock.add(unique,cleaned,layer%3)
 o=rock.finish(c,False)
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'beelzebufo':[('body-and-flanged-skull','#9A9276'),('digits','#AA9D7B'),('quiet-eye-gold','#A69862'),('pupils','#373E35'),('closed-mouth','#726F5B')],'pluricarpellatia':[('rhizome-and-rootlets','#91866C'),('simple-petioles','#819568'),('mature-peltate-blades','#6F9165'),('young-cordate-blades','#8EA378')],'paratingia':[('slender-single-stem','#9D8B6C'),('compound-leaf-rachis','#8C966A'),('large-adaxial-pinnules','#72916A'),('small-abaxial-pinnules','#91A175')],'stromatolite-mound':[('warm-microbial-lamina','#B4A085'),('pale-sedimentary-lamina','#CABBA0'),('quiet-dark-lamina','#9D8B73')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=hi[0]-lo[0] if slug in ['pluricarpellatia','stromatolite-mound'] else (.217 if slug=='beelzebufo' else hi[2]-lo[2]);scale=cfg['nominal_scale']['meters']/extent
 # Scale authored edge skeletons and skin radii together; evaluated source remains editable and physically scaled.
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=scale
   if o.data.skin_vertices:
    for d in o.data.skin_vertices[0].data:d.radius=(d.radius[0]*scale,d.radius[1]*scale)
 lo,hi=_bounds(_vertices_world(c))
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co.z-=lo[2]
 brief=json.loads((a.config.parent/'brief.json').read_text());refs=json.loads((a.config.parent/'references.json').read_text());desc={'en':'Original evidence-informed stylized teaching form; nominal scale, palette and simplified counts are artistic. Static only; no exact species, location, locomotion or shared habitat reconstruction.','zh':'原创依据基础形态的风格化教学造型；名义尺度、配色及简化数量属美术选择。仅静态，不声称精确种、地点、运动机制或共同栖息地复原。'}
 descriptions={'beelzebufo':{'en':'Friendly static Beelzebufo-inspired teaching frog, broad thick flanged head, low stout body and folded grounded limbs. Soft tissue, color, scale and pose are artistic; no toxicity, feeding or jumping mechanism claim.','zh':'友善静态Beelzebufo启发教学蛙，宽厚侧扩头部、矮壮躯干与接地折叠四肢。软组织、颜色、尺度及姿态属美术选择，不声称毒性、捕食或跳跃机制。'},'pluricarpellatia':{'en':'Rooted shallow freshwater Pluricarpellatia-inspired herb with horizontal rhizome, visible petiole bases and simple cordate to peltate leaves. No modern waterlily flower or unassociated reproductive organs.','zh':'有根浅淡水Pluricarpellatia启发草本，具水平根茎、可见柄基和简单心形至盾形叶。不加现代睡莲大花或未关联繁殖器官。'},'paratingia':{'en':'Paratingia-inspired small monocaulous tree. Each compound-leaf rachis carries two larger adaxial pinnule rows and two smaller abaxial rows; crown leaf number is artistic. No fern flowers or cones added.','zh':'Paratingia启发单干小树，每条复叶轴有上侧两列较大小叶、下侧两列较小小叶；冠叶数量属美术选择。不添加现代蕨花或球果。'},'stromatolite-mound':{'en':'Low microbial sedimentary mound teaching form with continuous curved laminae exposed on an intentional section. Not coral or plant; no exact microbial taxon, paleolocality or age assigned.','zh':'低矮微生物沉积丘教学造型，展示连续弧形叠层和有意教学露面。不是珊瑚或植物，不指定精确微生物类群、古地点或年龄。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
