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

def heliophyllum(c,m):
 horn=Mesh('curved-corallum-with-continuous-deep-calyx',m);septa=Mesh('simplified-radial-septa-inside-calyx',m)
 n=64;vs=[];fs=[];mi=[];profiles=[]
 # Increasing diameter follows a single curved growth axis. Base is a blunt preserved-inspired tip.
 for j in range(19):
  t=j/18;profiles.append((.039*t**1.45,.003*math.sin(pi*t),.003+.112*t,.0018+.034*t**.88,0,t))
 # Rim and deep inner wall are one continuous closed shell, not a disk painted dark.
 for rr,d in [(.94,.0008),(.87,.004),(.72,.012),(.51,.022),(.28,.030),(.10,.034)]:profiles.append((.039,.0,.115-d,.0358*rr,1,1))
 for cx,cy,z,r,inside,t in profiles:
  for k in range(n):
   a=2*pi*k/n;rib=(.00048*math.cos(20*a)*math.sin(pi*t/2)+.00023*math.cos(t*2*pi*9)) if not inside else 0
   rr=r+rib;vs.append((cx+rr*math.cos(a),cy+rr*math.sin(a),z+(.00065*math.sin(a*3)*t if not inside else 0)))
 fs.append(tuple(reversed(range(n))));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(profiles[j+1][4])
 fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);horn.add(vs,fs,mi)
 # Fin-like septa rise from the modeled bowl surface. Counts are explicitly simplified teaching art.
 bowl=[(.0036,.081,.0006),(.009,.085,.0032),(.017,.093,.005),(.025,.103,.0045),(.031,.111,.0020),(.0335,.114,.0007)]
 for k in range(20):
  a=2*pi*k/20;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));sv=[];sf=[]
  for j,(r,z,h) in enumerate(bowl):
   ctr=Vector((.039,0,z))+u*r;w=.00045*(.65+.35*j/(len(bowl)-1))
   sv.extend([tuple(ctr-v*w),tuple(ctr+v*w),tuple(ctr+Vector((0,0,h*(1 if k%2==0 else .75))))])
  sf.append((2,1,0))
  for j in range(len(bowl)-1):
   for e in range(3):sf.append((j*3+e,j*3+(e+1)%3,(j+1)*3+(e+1)%3,(j+1)*3+e))
  sf.append(tuple((len(bowl)-1)*3+i for i in range(3)));septa.add(sv,sf,2)
 horn.finish(c,True);septa.finish(c,True)

def pirania(c,m):
 body=Mesh('thick-walled-low-branching-sponge-tubes',m);spines=Mesh('sparse-ordered-long-wall-spicules',m)
 body.ellipsoid((0,0,.017),(.014,.012,.017),0,n=20,r=10)
 branches=[((.001,.001,.020),(.010,.003,.143),.0125,4,6,.2),((-.003,.002,.014),(-.035,.015,.111),.0096,3,5,1.0),((.003,-.002,.015),(.034,-.021,.093),.0088,3,5,2.1)]
 for idx,(start,end,r,rows,count,phase) in enumerate(branches):
  s=Vector(start);e=Vector(end);d=e-s;pts=[];rads=[]
  for j in range(14):
   t=j/13;pts.append(s+d*t+Vector((.002*math.sin(pi*t),.0012*math.sin(pi*t)*math.sin(idx+1),0)));rads.append(r*(.82+.18*math.sin(pi*t*.8))*(1-.10*t))
  body.tube(pts,rads,0,n=24,hollow=True)
  tangent=d.normalized();u=tangent.cross(Vector((0,1,0))).normalized();v=tangent.cross(u).normalized()
  for row in range(rows):
   t=.24+row*(.61/max(rows-1,1));j=round(t*13);p=pts[j];rad=rads[j]
   for k in range(count):
    angle=2*pi*(k/count+row*.075)+phase;direction=(u*math.cos(angle)+v*math.sin(angle)).normalized();length=(.019 if idx==0 else .014)*(1+.16*math.sin(k*2.3+row));base=p+direction*rad*.94
    tip=base+direction*length+tangent*(length*.20);spines.tube([base,base+direction*length*.35+tangent*length*.07,base.lerp(tip,.77),tip],[.00085,.00064,.00030,.00006],2,n=8)
 body.finish(c,True);spines.finish(c,True)

def bosworthia(c,m):
 thallus=Mesh('preserved-flat-flexible-ribbon-thallus-fragment',m)
 def ribbon(points,widths,phase=0):
  ps=[Vector(p) for p in points];vs=[];fs=[];n=10
  for j,p in enumerate(ps):
   tangent=ps[min(j+1,len(ps)-1)]-ps[max(0,j-1)];u=Vector((-tangent.y,tangent.x,0)).normalized()
   for k in range(n):
    a=2*pi*k/n;vs.append(tuple(p+u*(widths[j]/2)*math.cos(a)+Vector((0,0,.00052*math.sin(a)))))
  fs.append(tuple(reversed(range(n))))
  for j in range(len(ps)-1):
   for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
  fs.append(tuple((len(ps)-1)*n+k for k in range(n)));thallus.add(vs,fs,0)
 def curve(points,width0,width1,phase=0):
  p=[Vector(q) for q in points];ps=[];ws=[]
  for j in range(16):
   t=j/15;q=(1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3];q.z+=.00035*math.sin(t*pi+phase);ps.append(q);ws.append(width0*(1-t)+width1*t)
  ribbon(ps,ws,phase)
 # A cut basal edge and broken, unequal distal lengths describe a fragment, not a complete rooted plant.
 curve([(.002,.055,.002),(-.008,.023,.002),(.008,-.018,.002),(-.006,-.054,.002)],.011,.005)
 curve([(-.004,.029,.002),(-.027,.017,.002),(-.043,-.008,.002),(-.045,-.043,.002)],.0088,.0035,.4)
 curve([(-.031,.002,.002),(-.047,-.003,.002),(-.060,-.012,.002),(-.061,-.026,.002)],.0058,.0028,.7)
 curve([(-.042,-.020,.002),(-.029,-.035,.002),(-.027,-.049,.002),(-.031,-.061,.002)],.0048,.0025,1.3)
 curve([(-.001,.008,.002),(.020,-.004,.002),(.037,-.022,.002),(.044,-.051,.002)],.0085,.0033,.8)
 curve([(.027,-.016,.002),(.047,-.016,.002),(.060,-.030,.002),(.061,-.043,.002)],.0054,.0025,.3)
 curve([(.003,-.020,.002),(.013,-.036,.002),(.014,-.053,.002),(.010,-.068,.002)],.006,.0028,1.6)
 thallus.finish(c,True)

def haplophrentis(c,m):
 shell=Mesh('tapered-conch-with-visible-aperture',m);lid=Mesh('separate-simplified-operculum',m);helens=Mesh('two-long-curved-helens-from-aperture',m)
 n=40;vs=[];fs=[];mi=[];profiles=[]
 for j in range(26):
  t=j/25;profiles.append((.028-.041*t,.0045+.0018*t,.00040+.00775*t,.00032+.00568*t,0,t))
 # The visible aperture has real inner wall depth; no copied textures or assumed soft tissue.
 for ratio,depth in [(.91,.0002),(.84,.0015),(.70,.004),(.45,.009)]:profiles.append((-.013+depth,.0063,.00815*ratio,.006*ratio,1,1))
 for y,zc,w,h,mat,t in profiles:
  for k in range(n):
   a=2*pi*k/n;tri=1+.07*math.cos(3*a+.5*pi);growth=1+.012*math.sin(2*pi*t*13)*t;x=w*math.cos(a)*tri*growth;z=zc+h*math.sin(a)*tri*growth
   vs.append((x,y-.0010*(1-math.sin(a))*t,z))
 fs.append(tuple(reversed(range(n))));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(profiles[j+1][4])
 fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);shell.add(vs,fs,mi)
 # Closed shallow lid, posed close to the aperture without claiming an articulated mechanism.
 for inner in [False,True]:
  for j in range(6):
   rad=1-j/6
   for k in range(n):
    a=2*pi*k/n;tri=1+.055*math.cos(3*a+.5*pi);x=.0076*rad*math.cos(a)*tri;z=.0063+.0058*rad*math.sin(a)*tri;y=-.0158-.0011*(1-rad*rad)-.14*(z-.0063)+(0 if not inner else .00045);lid.v.append((x,y,z))
  lid.v.append((0,-.0169+(0 if not inner else .00045),.0063))
 half=6*n+1
 for side in [0,1]:
  off=side*half
  for j in range(5):
   for k in range(n):lid.f.append((off+j*n+k,off+j*n+(k+1)%n,off+(j+1)*n+(k+1)%n,off+(j+1)*n+k));lid.mi.append(2)
  for k in range(n):lid.f.append((off+5*n+k,off+5*n+(k+1)%n,off+6*n));lid.mi.append(2)
 for k in range(n):lid.f.append((k,(k+1)%n,half+(k+1)%n,half+k));lid.mi.append(2)
 for side in [-1,1]:
  p=[Vector((side*.0068,-.013,.0043)),Vector((side*.016,-.014,.003)),Vector((side*.032,.011,.0008)),Vector((side*.019,.022,.0016))];pts=[]
  for j in range(22):
   t=j/21;pts.append((1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3])
  helens.tube(pts,[.00072*(1-.90*j/21) for j in range(22)],3,n=10)
 shell.finish(c,True);lid.finish(c,True);helens.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'heliophyllum':[('corallum-warm-limestone','#BD9D80'),('calyx-wall','#AE9078'),('radial-septa','#D1B292')],'pirania':[('sponge-muted-ochre','#BD9A69'),('osculum-inner-wall','#8F7655'),('long-spicules','#D7BD92')],'bosworthia':[('preserved-thallus-muted-olive','#7D8A6A')],'haplophrentis':[('conch-soft-ivory','#CCB99A'),('aperture-interior','#9D8D74'),('operculum','#C2A985'),('helens','#BDAA8D')]}
 mats=[make_material(name,color,roughness=.80) for name,color in palettes[slug]];globals()[slug](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=max(hi[0]-lo[0],hi[1]-lo[1]) if slug in ['bosworthia','haplophrentis'] else hi[2]-lo[2];scale=cfg['nominal_scale']['meters']/extent
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=scale
 lo,hi=_bounds(_vertices_world(c))
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co.z-=lo[2]
 brief=json.loads((a.config.parent/'brief.json').read_text());refs=json.loads((a.config.parent/'references.json').read_text());description={'en':'Original evidence-informed stylized teaching form; artistic nominal scale, palette and simplified counts. Static only; no exact species or shared habitat claim.','zh':'原创依据基础形态的风格化教学造型；名义尺度、配色及简化数量属美术选择。仅静态，不声称精确种或共同栖息地复原。'}
 if slug=='bosworthia':description={'en':'Preserved Bosworthia-inspired thallus fragment, displayed as shallow-thickness ribbon branches. No whole parent organism, roots or unknown attachment reconstructed. Nominal span and color are artistic.','zh':'Bosworthia启发的保存藻体片段，以浅厚度柔带分枝展示。不重建完整母体、根或未知固着结构；名义跨度及配色属美术选择。'}
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':description,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir()
  mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
