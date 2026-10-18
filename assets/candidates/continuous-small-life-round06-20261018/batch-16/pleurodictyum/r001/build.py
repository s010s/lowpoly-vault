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

def pleurodictyum(c,m):
 colony=Mesh('low-domed-colony-disc-with-few-adjoining-large-calyces',m)
 colony.ellipsoid((0,0,.006),(.045,.038,.007),0,n=40,r=9)
 specs=[(-.004,-.003,.022,.017,.016,9),(-.025,-.014,.017,.016,.013,8),(.023,-.013,.019,.017,.014,9),(-.022,.017,.020,.017,.016,8),(.011,.023,.023,.018,.015,9),(.033,.012,.016,.013,.012,8)]
 for idx,(x,y,h,rx,ry,n) in enumerate(specs):
  vs=[];fs=[];mis=[];profiles=[(.002,.56),(.006,.89),(h-.004,1),(h,.98),(h-.001,.81),(h-.006,.72),(.008,.31)]
  for j,(z,r) in enumerate(profiles):
   for k in range(n):a=2*pi*k/n+idx*.23;vs.append((x+rx*r*math.cos(a),y+ry*r*math.sin(a),z+.0007*math.sin(a*2+idx)*(1 if j>1 else 0)))
  fs.append(tuple(reversed(range(n))));mis.append(0)
  for j in range(len(profiles)-1):
   for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mis.append(1 if j>=4 else 0)
  fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mis.append(1);colony.add(vs,fs,mis)
 o=colony.finish(c)
 rem=o.modifiers.new('Continuous colony-wall unions','REMESH');rem.mode='VOXEL';rem.voxel_size=.0017;rem.adaptivity=.25;rem.use_smooth_shade=True
 soft=o.modifiers.new('Soft calyx-to-disc transitions','SMOOTH');soft.factor=.32;soft.iterations=3
 # Deliberate smooth mixed contour preserves low domed transitions and large cup spacing.

def matonidium(c,m):
 axes=Mesh('preserved-frond-thin-radiating-rachises-only',m);pinn=Mesh('rounded-subtriangular-pinnules-with-ray-gaps',m)
 base=Vector((0,.052,.004));axes.tube([(0,.077,.004),(0,.062,.004),tuple(base)],[.0024,.0020,.0019],0,n=9)
 for idx,(deg,L) in enumerate([(-76,.112),(-39,.145),(-3,.164),(35,.150),(73,.119)]):
  a=math.radians(deg);u=Vector((math.sin(a),-math.cos(a),0));v=Vector((math.cos(a),math.sin(a),0));pts=[base+u*(L*t)+Vector((0,0,.006*math.sin(pi*t)+.0015*idx*t)) for t in [i/20 for i in range(21)]];axes.tube(pts,[.0018*(1-.80*i/20) for i in range(21)],0,n=8)
  for j in range(8):
   for sign in [-1,1]:
    t=.20+j*.090+(.025 if sign<0 else 0);center=pts[min(20,round(t*20))];d=(v*sign+.12*u).normalized();length=.014*math.sin(pi*t)**.55*(1-.15*t);width=.0038*(1-.25*t);p=center;z=Vector((0,0,1));side=d.cross(z).normalized()
    outline=[p,p+d*length*.20+side*width,p+d*length*.76+side*width*.72,p+d*length+side*width*.28,p+d*length-side*width*.28,p+d*length*.76-side*width*.72,p+d*length*.20-side*width]
    ctr=p+d*length*.52+z*.0010;vs=[tuple(q) for q in outline]+[tuple(ctr),tuple(ctr-z*.0015)];faces=[]
    for k in range(7):faces.extend([(7,k,(k+1)%7),(8,(k+1)%7,k)])
    pinn.add(vs,faces,1)
 axes.finish(c);pinn.finish(c,False)

def yohoia(c,m):
 head=Mesh('broad-subrectangular-head-shield',m);body=Mesh('gently-tapered-segmented-trunk',m);arms=Mesh('paired-two-segment-elbows-and-four-terminal-fingers',m);limbs=Mesh('simplified-ventral-support-and-swimming-limbs',m);tail=Mesh('broad-terminal-paddle-telson',m);eyes=Mesh('small-lateral-eyes',m)
 # A low bevelled shield with a broad front, squared corners, and a rounded dorsal crown.
 outline=[(-.006,-.012),(.006,-.012),(.008,-.010),(.008,-.004),(.006,-.002),(-.006,-.002),(-.008,-.004),(-.008,-.010)];vs=[];fs=[]
 for z,scale in [(.004,.88),(.0055,1),(.0085,.94),(.0093,.72)]:
  for x,y in outline:vs.append((x*scale,-.007+(y+.007)*scale,z))
 fs.append(tuple(reversed(range(8))))
 for j in range(3):
  for k in range(8):fs.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k))
 fs.append(tuple(24+k for k in range(8)));head.add(vs,fs,0)
 for j in range(9):
  t=j/8;y=.0005+j*.0026;w=.0066*(1-.50*t);body.ellipsoid((0,y,.0065-.002*t),(w,.0020,.0025*(1-.35*t)),0 if j%3 else 1,n=16,r=7)
  for sign in [-1,1]:
   p=[(sign*w*.70,y,.005),(sign*(w+.002),y+.001,.003),(sign*(w+.003),y+.002,.0016)];limbs.tube(p,[.0007,.0006,.00018],2,n=7)
 for sign in [-1,1]:
  p=smooth_path([(sign*.005,-.009,.005),(sign*.009,-.018,.006),(sign*.007,-.023,.014)],12);arms.tube(p,[.0011*(1-.20*i/11) for i in range(12)],1,n=10)
  start=p[-1]
  for k in range(4):
   d=Vector((sign*(k-1.5)*.0016,-.0085+.0004*abs(k-1.5),.0015-.0008*k));ps=[start+d*t+Vector((0,.0018*t*t,-.0015*t*t)) for t in [i/6 for i in range(7)]];arms.tube(ps,[.00048*(1-.88*i/6) for i in range(7)],2,n=7)
  eyes.ellipsoid((sign*.0068,-.011,.0086),(.0010,.0011,.0009),3,n=12,r=7)
 tail.ellipsoid((0,.026,.0043),(.0043,.0046,.00085),1,n=20,r=7)
 head.finish(c,False);body.finish(c);arms.finish(c);limbs.finish(c);tail.finish(c);eyes.finish(c)

def gypsum_desert_rose(c,m):
 core=Mesh('intergrown-sandy-gypsum-core',m);plates=Mesh('overlapping-tabular-crystals-with-hierarchical-sizes-and-angles',m)
 core.ellipsoid((0,0,.022),(.023,.019,.019),0,n=18,r=8)
 specs=[(-160,.070,.026,.30,0),(-112,.062,.024,.57,0),(-67,.081,.028,.22,0),(-19,.067,.024,.78,0),(31,.074,.027,.40,0),(88,.061,.023,.66,0),(145,.069,.025,.35,0),(-138,.043,.019,1.12,1),(-80,.048,.018,1.30,1),(-27,.048,.019,1.05,1),(27,.042,.020,1.30,1),(83,.046,.018,1.16,1),(156,.040,.017,1.32,1),(-45,.030,.015,1.52,2),(60,.027,.014,1.45,2)]
 for idx,(deg,L,W,elev,group) in enumerate(specs):
  az=math.radians(deg);u=Vector((math.cos(az)*math.cos(elev),math.sin(az)*math.cos(elev),math.sin(elev)));v=Vector((-math.sin(az),math.cos(az),0));v=(v*math.cos(.22*math.sin(idx))+u.cross(v)*math.sin(.22*math.sin(idx))).normalized();normal=u.cross(v).normalized();origin=Vector((.003*math.sin(idx*.7),.003*math.cos(idx),.012+.005*group));th=.0032 if group==0 else .0025
  outline=[(-.08,0),(.10,.62),(.34,1),(.72,.93),(.96,.46),(1.0,.05),(.94,-.49),(.66,-.93),(.29,-.92),(.07,-.55)];vs=[];fs=[];mis=[]
  # A bevelled tabular crystal is a closed solid, with plate thickness retained at all orientations.
  for ratio,height in [(1,0),(.90,th*.5),(.90,-th*.5)]:
   for x,y in outline:vs.append(tuple(origin+u*(L*(.46+(x-.46)*ratio))+v*(W*y*ratio)+normal*height))
  n=len(outline);fs.append(tuple(n+k for k in reversed(range(n))));mis.append(group)
  fs.append(tuple(2*n+k for k in range(n)));mis.append(group)
  for k in range(n):q=(k+1)%n;fs.extend([(k,q,n+q,n+k),(k,2*n+k,2*n+q,q)]);mis.extend([group,group])
  # The local perimeter is clockwise; cap winding and bevel winding are handled separately.
  plates.add(vs,fs[:2]+[tuple(reversed(f)) for f in fs[2:]],mis)
 core.finish(c,False);plates.finish(c,False)
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'pleurodictyum':[('low-colony-wall','#B79E88'),('large-calyx-interiors','#9D8774')],'matonidium':[('preserved-frond-axes','#9D9970'),('preserved-organ-pinnules','#8C9B71')],'yohoia':[('head-and-tergites','#A58D76'),('elbow-appendages-and-paddle','#BAA286'),('limbs-and-terminal-spines','#C7B396'),('small-eyes','#44483D')],'gypsum-desert-rose':[('sandy-tabular-gypsum','#B69B7A'),('inner-angled-crystals','#C2AB8B'),('small-core-crystals','#CBB696')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=.042 if slug=='yohoia' else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'pleurodictyum':{'en':'Low domed Pleurodictyum-inspired colony disc carrying a few adjoining large calyces. Original teaching geometry, not a resized old coral or exact specimen. Scale, color and cup counts are artistic.','zh':'低穹盘Pleurodictyum启发群体，具有少量相邻大杯。原创教学几何，不是旧珊瑚缩放或精确标本；尺度、配色和杯数属美术选择。'},'matonidium':{'en':'Preserved-frond-only Matonidium-inspired teaching organ, with thin radiating axes and rounded subtriangular pinnules. Connections and exact layout are teaching assembly: organic connection was not preserved in the cited Matonidium sp. analogy. No tree, roots or whole living crown.','zh':'仅保存蕨叶器官的Matonidium启发教学展示，具细放射轴及圆端亚三角羽片。连接和布局属教学整合：引用的Matonidium sp.类比未保存完整有机连接。不添加干、根或整株活体冠。'},'yohoia':{'en':'Yohoia-inspired static teaching arthropod with a subrectangular head shield, paired elbowed anterior appendages and four long terminal fingers, segmented trunk and paddle telson. Fine anatomy and counts simplified; no flagellate whip fingers or lanceolate tail.','zh':'Yohoia启发静态教学节肢动物，具方形头甲、成对肘状前附肢及四根末端长指、分节体和桨状尾。细节与数量简化；无鞭丝指或矛头尾。'},'gypsum-desert-rose':{'en':'Original gypsum desert-rose mineral teaching aggregate with intergrown tabular crystals of hierarchical sizes, real thickness and varied angles. Not a botanical flower or an exact mineral locality/specimen.','zh':'原创石膏沙漠玫瑰矿物教学集合体，具主次尺度、真实厚度及变化夹角的交叠板晶。不是植物花朵，不指定精确矿点或标本。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
