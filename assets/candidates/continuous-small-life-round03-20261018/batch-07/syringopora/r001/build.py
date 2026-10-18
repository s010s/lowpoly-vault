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

def syringopora(c,m):
 coral=Mesh('separate-growing-corallites-with-deep-calyces',m);bridge=Mesh('intermittent-lateral-connecting-tubules',m)
 # Staggered footprint and slow outward growth leave negative spaces rather than continuous walls.
 specs=[]
 rows=[(-.042,[-.028,-.005,.019]),(-.021,[-.047,-.024,0,.024,.046]),(.002,[-.050,-.027,-.003,.022,.046]),(.025,[-.039,-.015,.010,.035]),(.047,[-.023,.001,.024])]
 for ri,(y,xs) in enumerate(rows):
  for ci,x in enumerate(xs):
   x+=random.uniform(-.002,.002);y1=y+random.uniform(-.002,.002);r=random.uniform(.0037,.0051)
   h=.18-.53*math.hypot(x,y1)+random.uniform(-.014,.007);lean=Vector((x*.18,y1*.13,0));start=Vector((x,y1,.001))
   pts=[tuple(start+Vector((0,0,h*t))+lean*(t*t)+Vector((.0012*math.sin(t*pi)*math.sin(ci),.0011*math.sin(t*pi)*math.cos(ri),0))) for t in [i/9 for i in range(10)]]
   rads=[r*(1+.07*math.sin(j*1.4+ri)-.10*j/9) for j in range(10)];coral.tube(pts,rads,0,n=12,hollow=True);specs.append((start,lean,h,r))
 for i,(p,lean,h,r) in enumerate(specs):
  neighbors=sorted([(float((q-p).length),j) for j,(q,_,_,_) in enumerate(specs) if j>i])
  if not neighbors or neighbors[0][0]>.035:continue
  for z in [.034+(i%3)*.009,.087+(i%4)*.006][:1 if i%3==0 else 2]:
   j=neighbors[0][1];q,l2,h2,r2=specs[j];a=p+lean*(z/h)**2+Vector((0,0,z));b=q+l2*(z/h2)**2+Vector((0,0,z+.0015))
   bridge.tube([a,a.lerp(b,.33)+Vector((0,0,-.001)),a.lerp(b,.67),b],[r*.34,r*.29,r*.28,r2*.34],0,n=8)
 coral.finish(c);bridge.finish(c)

def vauxia(c,m):
 sponge=Mesh('tapered-dichotomous-fibrous-sponge',m);fibers=Mesh('restrained-longitudinal-fiber-rhythm',m)
 def grow(start,end,r,depth,key):
  s=Vector(start);e=Vector(end);delta=e-s;pts=[s+delta*t+Vector((.002*math.sin(pi*t+key)*math.sin(pi*t),.002*math.cos(pi*t+key)*math.sin(pi*t),0)) for t in [i/7 for i in range(8)]]
  rads=[r*(1-.30*j/7)*(1+.035*math.sin(j*2+key)) for j in range(8)]
  sponge.tube(pts,rads,0,n=12,hollow=depth==0)
  # Sparse raised fibers, following the trunk direction; no random needle field.
  if depth>0:
   for angle in [.4,2.7,4.7]:
    shift=Vector((math.cos(angle),math.sin(angle),0))*r*.96
    fibers.tube([p+shift*(1-.3*j/7) for j,p in enumerate(pts)],[.00020*(1-.3*j/7)]*8,2,n=4)
  if depth:
   d=delta.normalized();az=key*1.37
   for side in [-1,1]:
    lateral=Vector((math.cos(az),math.sin(az),.12))*side
    nd=(d*.72+lateral*.65+Vector((0,0,.22))).normalized();length=delta.length*(.67 if depth>1 else .72)
    grow(e-d*r*.65,e+nd*length,r*.65,depth-1,key+1.23+side*.6)
 grow((0,0,.003),(.004,.002,.068),.009,3,.6)
 grow((-.001,.001,.012),(-.035,.014,.079),.0067,2,2.7)
 grow((.002,.001,.014),(.034,-.025,.074),.0065,2,4.9)
 sponge.finish(c);fibers.finish(c)

def halimeda(c,m):
 plates=Mesh('calcified-fan-segments',m);nodes=Mesh('narrow-flexible-nodes',m)
 def plate(base,tip,width,angle,mat):
  b=Vector(base);t=Vector(tip);d=t-b;axis=d.normalized();u=Vector((math.cos(angle),math.sin(angle),0));u=(u-axis*u.dot(axis)).normalized();normal=axis.cross(u).normalized()
  # Deliberate flared fan outline: narrowed lower articulation, broad rounded upper edge.
  coords=[(-.15,0),(-.64,.18),(-.98,.47),(-1,.69),(-.82,.88),(-.45,1.0),(0,1.045),(.46,1.0),(.84,.86),(1,.65),(.91,.40),(.57,.16),(.15,0)]
  outline=[b+d*y+u*x*width/2+normal*(.0006*math.sin(y*pi)) for x,y in coords];vs=[];fs=[];n=len(outline)
  # Two gently convex faces meeting at a rounded rim; broad face facets remain quiet.
  for side in [1,-1]:
   vs.append(tuple(b+d*.57+normal*side*.0014))
   for p in outline:vs.append(tuple(p+normal*side*.00040))
  for k in range(n):fs.extend([(0,1+k,1+(k+1)%n),(n+1,n+2+(k+1)%n,n+2+k),(1+k,n+2+k,n+2+(k+1)%n,1+(k+1)%n)])
  plates.add(vs,fs,mat)
 def chain(points,widths,angle,seed):
  for j in range(len(points)-1):
   b=Vector(points[j]);t=Vector(points[j+1]);gap=(t-b).normalized()*.003
   nodes.tube([b-gap*.55,b+gap*.8],[.00115,.00095],3,n=8)
   plate(b+gap*.35,t-gap*.5,widths[j],angle+.16*math.sin(seed+j),j%3)
 chain([(0,0,.002),(-.004,0,.027),(-.002,.002,.055),(-.014,.004,.083),(-.008,.006,.112),(-.019,.009,.140)],[.017,.023,.026,.028,.026],.15,0)
 chain([(-.002,.002,.052),(.025,-.001,.076),(.040,-.002,.101),(.052,.001,.125)],[.024,.026,.024],-.16,1)
 chain([(-.013,.004,.079),(-.039,.012,.097),(-.052,.014,.121),(-.057,.018,.145)],[.023,.025,.022],.42,2)
 chain([(.024,-.001,.074),(.034,-.030,.091),(.040,-.043,.116)],[.024,.026],1.15,3)
 chain([(0,0,.007),(.018,.023,.033),(.025,.037,.059),(.015,.041,.083),(.022,.045,.108)],[.020,.026,.028,.023],.9,4)
 chain([(.025,.037,.056),(.049,.043,.077),(.060,.045,.100)],[.023,.022],.37,5)
 plates.finish(c,True);nodes.finish(c)

def isoxys(c,m):
 shell=Mesh('paired-convex-carapace-valves',m);rims=Mesh('subtle-carapace-rim',m);soft=Mesh('conservative-internal-body-and-paddles',m);eyes=Mesh('stalked-eyes',m)
 # Two closed, cupped valves. Their upper hinge meets, the lower rims enclose a narrow ventral gap.
 n=40
 for side in [-1,1]:
  vs=[];fs=[];mis=[]
  # concentric outline rings, both outer and inner faces; continuous shallow convexity.
  for inner in [False,True]:
   for j in range(6):
    rad=1-j/6
    for k in range(n):
     a=2*pi*k/n;y=.025*rad*math.cos(a);z=.011*rad*math.sin(a)
     x=side*(.0013+.0088*(1-rad*rad)**.65+(.00035 if not inner else -.00035))
     # upper hinge narrows gently, ventral rim stays parted.
     x*=1-.70*max(0,math.sin(a))*rad
     vs.append((x,y,z))
   vs.append((side*(.0101+(.00035 if not inner else -.00035)),0,0))
  half=6*n+1
  for inner in [0,1]:
   off=inner*half
   for j in range(5):
    for k in range(n):fs.append((off+j*n+k,off+j*n+(k+1)%n,off+(j+1)*n+(k+1)%n,off+(j+1)*n+k));mis.append(0 if j<4 else 1)
   for k in range(n):fs.append((off+5*n+k,off+5*n+(k+1)%n,off+6*n));mis.append(1)
  for k in range(n):fs.append((k,half+k,half+(k+1)%n,(k+1)%n));mis.append(1)
  shell.add(vs,fs,mis)
  outline=[(side*(.00165)*(1-.70*max(0,math.sin(2*pi*k/n))),.025*math.cos(2*pi*k/n),.011*math.sin(2*pi*k/n)) for k in range(n+1)]
  rims.tube(outline,[.00028]*len(outline),1,n=5)
  # Long opposed carapace spines, tapering from integrated shell ends rather than stray rods.
  for front in [-1,1]:
   rims.tube([(side*.0017,front*.020,.003),(side*.0014,front*.027,.005),(side*.0007,front*.037,.009),(0,front*(.050 if front<0 else .047),.0115)],[.0026,.0018,.0009,.00004],0,n=12)
  soft.tube([(side*.003,-.016,-.002),(side*.007,-.027,.0005),(side*.011,-.031,.002)],[.0016,.0012,.0008],3,n=10)
  eyes.ellipsoid((side*.011,-.031,.002),(.0028,.0027,.0029),4,n=16,r=10)
  eyes.ellipsoid((side*.0115,-.032,.003),(.0007,.0005,.00065),5,n=10,r=6)
  for j in range(7):
   y=-.016+j*.005
   soft.tube([(side*.0015,y,-.005),(side*.0036,y+.001,-.011),(side*.006,y+.004,-.014)],[.0011,.00075,.00030],3,n=8)
   soft.ellipsoid((side*.006,y+.004,-.014),(.0013,.0028,.00035),3,n=10,r=5)
 soft.ellipsoid((0,0,-.002),(.0035,.022,.005),3,n=16,r=10)
 shell.finish(c);rims.finish(c);soft.finish(c);eyes.finish(c)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'syringopora':[('living-coral-ivory','#C8AD92'),('calyx-interior','#8D7464')], 'vauxia':[('ochre-sponge','#C99F69'),('inner-cavity','#806644'),('fiber-ridges','#B78B55')], 'halimeda':[('older-calcified-green','#709D72'),('mid-green','#86B27C'),('young-tip-green','#A1C28B'),('noncalcified-node','#577F57')], 'isoxys':[('ochre-carapace','#BE8D61'),('warm-shell-center','#C89969'),('unused','#BA8B60'),('soft-body','#917B67'),('eyes','#283B39'),('eye-soft-highlight','#91A7A0')]}
 mats=[make_material(name,color,roughness=.76) for name,color in palettes[slug]];globals()[slug](c,mats)
 # Respect nominal art scale without relabeling it as a measured organism size.
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));axis=1 if slug=='isoxys' else 2;target=cfg['nominal_scale']['meters'];extent=.05 if slug=='isoxys' else hi[axis]-lo[axis];scale=target/extent
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=scale
 if slug!='isoxys':
  lo,hi=_bounds(_vertices_world(c))
  for o in c.all_objects:
   if o.type=='MESH':
    for v in o.data.vertices:v.co.z-=lo[2]
 brief=json.loads((a.config.parent/'brief.json').read_text());refs=json.loads((a.config.parent/'references.json').read_text())
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':{'en':'Original evidence-informed stylized teaching form; artistic nominal scale and palette. Static only, no exact species or habitat claim.','zh':'原创依据基础形态的风格化教学造型；名义尺度和配色属美术选择。仅静态，不声称精确种或共同栖息地复原。'},'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'animation_ready':False,'origin':'internal-body swimming mount (0,0,0)' if slug=='isoxys' else 'base contact at z=0; identity root at origin','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 # export_asset adds <slug>; output folder must have that basename for relocation below.
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir()
  mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
