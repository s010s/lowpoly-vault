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

def spinolestes(c,m):
 body=Mesh('compact-small-mammal-continuous-head-and-pelage-body',m);limbs=Mesh('short-connected-limbs-and-rounded-grounded-paws',m);details=Mesh('small-ears-eyes-and-blunt-muzzle',m);patch=Mesh('localized-short-dorsal-protospine-patch',m);tail=Mesh('short-tapering-tail',m)
 profiles=[(-.080,.007,.039,.006),(-.069,.014,.043,.012),(-.054,.022,.050,.020),(-.035,.024,.049,.024),(-.020,.026,.044,.026),(.002,.032,.041,.030),(.026,.033,.039,.031),(.045,.027,.036,.027),(.060,.013,.032,.015)];n=28;vs=[];fs=[];mi=[]
 for y,rx,z,rz in profiles:
  for k in range(n):a=2*pi*k/n;vs.append((rx*math.cos(a),y,z+rz*math.sin(a)))
 fs.append(tuple(range(n)));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append(tuple(reversed((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))));mi.append(1 if k>n//2 else 0)
 fs.append(tuple(reversed(tuple((len(profiles)-1)*n+k for k in range(n)))));mi.append(0);body.add(vs,fs,mi);o=body.finish(c);sub=o.modifiers.new('Continuous soft head-neck-trunk form','SUBSURF');sub.levels=1;sub.render_levels=1
 for sign in [-1,1]:
  for rear in [False,True]:
   y=.033 if rear else -.029;x=.025 if rear else .021
   p=smooth_path([(sign*x,y,.038),(sign*(x+.008),y+.004,.024),(sign*(x+.008),y-.010,.012)],14);limbs.tube(p,[.008*(1-i/13)+.0045*(i/13) for i in range(14)],0,n=12)
   limbs.ellipsoid((sign*(x+.008),y-.014,.008),(.008,.011,.006),1,n=16,r=8)
   for k in range(3):
    px=sign*(x+.008)+(k-1)*.003;limbs.ellipsoid((px,y-.022,.0055),(.0018,.004,.0020),1,n=8,r=5)
  details.ellipsoid((sign*.018,-.038,.063),(.0060,.0038,.0090),0,n=16,r=9)
  details.ellipsoid((sign*.018,-.041,.064),(.0039,.0012,.0050),1,n=14,r=8)
  details.ellipsoid((sign*.0165,-.060,.052),(.0022,.0025,.0021),3,n=14,r=8)
 details.ellipsoid((0,-.078,.042),(.006,.0035,.0035),4,n=18,r=8)
 p=smooth_path([(0,.054,.030),(.002,.076,.024),(.007,.095,.019),(.010,.105,.018)],18);tail.tube(p,[.0045*(1-i/17)+.0012*(i/17) for i in range(18)],0,n=10)
 # A small dorsal focus, not a radial hedgehog coat or a covering of long spikes.
 for row,x in enumerate([-.008,0,.008]):
  for j in range(4):
   y=.004+j*.009+(row%2)*.003;z=.070-.16*y-.0015*(abs(x)/.008);p=[(x,y,z-.001),(x,y+.0018,z+.0025),(x+.0004,y+.0032,z+.0045)];patch.tube(p,[.0015,.0010,.00035],2,n=7)
 limbs.finish(c);details.finish(c);patch.finish(c);tail.finish(c)

def odontogriphus(c,m):
 mantle=Mesh('continuous-shellless-flattened-oval-mantle-and-broad-foot',m);gills=Mesh('restrained-short-marginal-gill-fold-bands',m)
 n=56;vs=[];fs=[];mi=[]
 profiles=[(.15,.0008),(.70,.0008),(.86,.0014),(.98,.0030),(1,.0042),(.94,.0055),(.76,.0072),(.45,.0082),(.10,.0086)]
 for j,(r,z) in enumerate(profiles):
  for k in range(n):a=2*pi*k/n;vs.append((.020*r*math.cos(a),.035*r*math.sin(a),z+.0004*r*math.sin(a)))
 fs.append(tuple(reversed(range(n))));mi.append(1)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j<3 else 0)
 fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(0);mantle.add(vs,fs,mi)
 for sign in [-1,1]:
  for j in range(14):
   t=-.78+1.56*j/13;y=.035*t;x=sign*.020*math.sqrt(1-t*t)*.96
   # Short folds hug the soft margin; they are not long locomotor appendages.
   gills.ellipsoid((x,y,.0028),(.00115,.0010,.00085),2,n=8,r=5)
 mantle.finish(c);gills.finish(c)

def trapa(c,m):
 fruit=Mesh('compact-preserved-fruit-body-with-four-horn-bases',m);horns=Mesh('four-spreading-horns-and-recurved-short-barbs',m)
 # A few broad longitudinal ribs express a fruit body, rather than a flower or leafy whole plant.
 n=20;profiles=[(.001,.0035),(.004,.010),(.009,.012),(.016,.0115),(.022,.0090),(.026,.0040)];vs=[];fs=[];mi=[]
 for j,(z,r) in enumerate(profiles):
  for k in range(n):a=2*pi*k/n;rr=r*(1+.08*math.cos(a*4));vs.append((rr*math.cos(a),rr*.84*math.sin(a),z))
 fs.append(tuple(reversed(range(n))));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(0 if k%5 else 1)
 fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);fruit.add(vs,fs,mi)
 for idx,deg in enumerate([8,98,188,278]):
  a=math.radians(deg);u=Vector((math.cos(a),math.sin(a),0));length=.025 if idx%2==0 else .022;z=.015 if idx%2==0 else .012
  p=smooth_path([u*.008+Vector((0,0,z)),u*.016+Vector((0,0,z+.003)),u*length+Vector((0,0,z+.010)),u*(length+.002)+Vector((0,0,z+.014))],16);horns.tube(p,[.0033*(1-i/15)+.00065*(i/15) for i in range(16)],0,n=10)
  # Backward-facing barbs point toward the fruit base, not outward like extra horns.
  base=p[11];tip=base-u*.004+Vector((0,0,-.001));horns.tube([base,base-u*.001+Vector((0,0,.001)),tip],[.0013,.0010,.00045],1,n=8)
  horns.ellipsoid(tuple(p[-1]),(.00075,.00075,.00075),0,n=8,r=5)
 fruit.finish(c,False);horns.finish(c)

def flint_nodule(c,m):
 stone=Mesh('rounded-chalk-cortex-nodule-with-single-conchoidal-fracture',m)
 normal=Vector((0,-.62,.785)).normalized();u=Vector((1,0,0));v=normal.cross(u).normalized();n=64;vs=[];fs=[];mi=[]
 profiles=[(-.075,.014,.018,0),(-.068,.047,.040,0),(-.050,.080,.063,0),(-.025,.095,.074,0),(.002,.090,.068,0),(.020,.078,.058,0),(.024,.069,.049,0),(.022,.067,.047,1)]
 # A concave flake scar with coherent curved ripples and a focus slightly off centre.
 for j in range(1,13):
  r=1-j/13;depth=.012*(1-r*r);ripple=.00085*math.sin(r*7*pi)*(math.sin(pi*r)**.65);profiles.append((.022-depth+ripple,.067*r,.047*r,1))
 profiles.append((.010,.0007,.0006,1))
 for j,(h,rx,ry,mat) in enumerate(profiles):
  for k in range(n):
   a=2*pi*k/n;warp=(1+.045*math.sin(3*a+.4)+.025*math.cos(2*a-.7)) if j<7 else (1+.020*math.sin(3*a+.4));x=rx*math.cos(a)*warp;y=ry*math.sin(a)*warp
   if j>=7:x+=.003*(1-rx/.067);y+=.002*(1-ry/.047)
   p=u*x+v*y+normal*(h+(.0012*math.sin(a*2) if j<7 else 0));vs.append(tuple(p))
 fs.append(tuple(reversed(range(n))));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(profiles[j+1][3])
 fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);stone.add(vs,fs,mi);o=stone.finish(c)
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'spinolestes':[('quiet-soft-pelage','#9B9079'),('belly-paws-and-ear-interiors','#B4A48A'),('localized-short-protospines','#817963'),('small-eyes','#343E37'),('blunt-nose','#5B6050')],'odontogriphus':[('smooth-shellless-mantle','#A7A28C'),('broad-ventral-foot','#C0B6A0'),('restrained-gill-folds','#B9AD96')],'trapa':[('preserved-fruit-body-and-horns','#9B876A'),('broad-fruit-ribs-and-barbs','#AE9A7C')],'flint-nodule':[('pale-artistic-chalk-cortex','#C6BFAE'),('conchoidal-flint-fracture','#6F7874')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=.14 if slug=='spinolestes' else (hi[1]-lo[1] if slug=='odontogriphus' else hi[0]-lo[0]);scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'spinolestes':{'en':'Spinolestes-inspired compact small mammal teaching form with quiet pelage, short grounded limbs and a localized short dorsal protospine patch. Soft tissue, palette, exact spine count and tail proportions are artistic; not a modern hedgehog recolor or exact pelage-histology restoration.','zh':'Spinolestes启发紧凑小兽教学造型，具安静毛面、短接地四肢和局部短原刺区。软组织、配色、刺数和尾部比例属美术选择，不是现代刺猬换色或精确皮毛组织复原。'},'odontogriphus':{'en':'Odontogriphus-inspired shellless flattened oval teaching animal, smooth dorsum, broad continuous foot and restrained marginal gill bands excluding the anterior. Fine radula/gill counts omitted; no modern slug tentacles, shell or dorsal plates.','zh':'Odontogriphus启发无壳扁椭圆教学动物，光滑背面、连续宽腹足及前端以外克制边缘鳃带。省略微细齿舌和鳃片计数，不加现代蛞蝓触角、壳或背甲。'},'trapa':{'en':'Preserved Trapa fruit-only teaching organ with compact central body, four spreading horns and small backward-directed barbs, with rounded tips. No unknown leaves, stems, roots or whole plant; scale, color and exact pose artistic.','zh':'仅保存Trapa果实器官的教学展示：紧凑中央体、四条展开角臂及反向小倒刺，末端钝化。不添未知叶、茎、根或整株；尺度、颜色与姿态属美术选择。'},'flint-nodule':{'en':'Original rounded irregular flint-nodule teaching form, pale cortex as artistic generalization and one coherent curved conchoidal fracture scar. Fracture pattern is geological, not a shell animal; no exact paleolocality, artifact or additional broken/whole variant ID.','zh':'原创不规则圆钝燧石结核教学造型，浅色外皮属美术概括，具一处连贯弧形贝壳状断面。断口是地质形态，不是贝壳动物；不指定古地点或工具，不另计完整/破损变体。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
