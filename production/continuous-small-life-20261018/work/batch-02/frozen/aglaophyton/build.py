# SPDX-License-Identifier: MIT
"""Original palette-only static meshes. Blender -b -t 2 --python this.py -- --asset ID [--output PARENT] [--no-preview]."""
import argparse,sys,math,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').is_file())
sys.path.insert(0,str(Path(__file__).parent/'lib'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews,ground_asset
P=ROOT/'production/continuous-small-life-20261018'
PI=math.pi
class Mesh:
 def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  off=len(self.v);self.v+=v;self.f += [tuple(off+i for i in face) for face in f];self.mi += mi if isinstance(mi,list) else [mi]*len(f)
 def tube(self,pts,rads,mi=0,n=10,oval=None):
  pts=list(map(Vector,pts));v=[];prev=None
  for j,p in enumerate(pts):
   d=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized()
   u=prev-d*prev.dot(d) if prev is not None else d.cross(Vector((0,0,1)))
   if u.length<.01:u=d.cross(Vector((0,1,0)))
   u.normalize();prev=u.copy();w=d.cross(u).normalized()
   for k in range(n):v.append(tuple(p+rads[j]*(u*math.cos(k*2*PI/n)+w*math.sin(k*2*PI/n)*(oval or 1))))
  f=[tuple(reversed(range(n)))]+[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(pts)-1) for k in range(n)]+[tuple((len(pts)-1)*n+k for k in range(n))]
  self.add(v,f,mi)
 def loft(self,profiles,mi=0,n=20):
  # x lateral; longitudinal -Y; z vertical. Each row (y,width,z,height).
  v=[(w*math.cos(k*2*PI/n),y,z+h*math.sin(k*2*PI/n)) for y,w,z,h in profiles for k in range(n)]
  f=[tuple(reversed(range(n)))]+[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(profiles)-1) for k in range(n)]+[tuple((len(profiles)-1)*n+k for k in range(n))]
  self.add(v,f,mi)
 def ell(self,p,s,mi=0,n=16,r=8):
  v=[(p[0],p[1],p[2]+s[2])]+[(p[0]+s[0]*math.sin(j*PI/r)*math.cos(k*2*PI/n),p[1]+s[1]*math.sin(j*PI/r)*math.sin(k*2*PI/n),p[2]+s[2]*math.cos(j*PI/r)) for j in range(1,r) for k in range(n)]+[(p[0],p[1],p[2]-s[2])]
  f=[(0,1+k,1+(k+1)%n) for k in range(n)]+[(1+j*n+k,1+(j+1)*n+k,1+(j+1)*n+(k+1)%n,1+j*n+(k+1)%n) for j in range(r-2) for k in range(n)]+[(len(v)-1,1+(r-2)*n+(k+1)%n,1+(r-2)*n+k) for k in range(n)]
  self.add(v,f,mi)
 def finish(self,c,smooth=True):
  o=mesh_object(self.name,self.v,self.f,self.mats,c)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i;p.use_smooth=smooth
  return o

def star(c,m):
 a=Mesh('continuous-five-arm-disc',m);N=120;R=12;v=[]
 # Shared polar topology creates soft continuous arm roots. Gentle asymmetric bends.
 for side in (1,-1):
  for j in range(R+1):
   t=.025+.975*j/R
   for k in range(N):
    ang=2*PI*k/N;local=((ang+PI/5)%(2*PI/5))-PI/5
    ray=.0045/(abs(math.sin(local))+.0045/.035*math.cos(local))
    theta=ang+.12*t*t*math.sin(5*ang+.5)
    z=.0015+side*(.00032+.00105*(1-t)**.5)+.00055*t*t*(.5+.5*math.sin(3*ang))
    v.append((ray*t*math.cos(theta),ray*t*math.sin(theta),z))
 f=[];mi=[];L=(R+1)*N
 for s in range(2):
  for j in range(R):
   for k in range(N):
    face=(s*L+j*N+k,s*L+j*N+(k+1)%N,s*L+(j+1)*N+(k+1)%N,s*L+(j+1)*N+k)
    f.append(face if s==0 else tuple(reversed(face)));mi.append(1 if s else (2 if j in (3,6,9) else 0))
  center=len(v);v.append((0,0,.0015+(1 if s==0 else -1)*.00135))
  for k in range(N):f.append((center,s*L+k,s*L+(k+1)%N) if s==0 else (center,s*L+(k+1)%N,s*L+k));mi.append(s)
 for k in range(N):f.append((R*N+k,L+R*N+k,L+R*N+(k+1)%N,R*N+(k+1)%N));mi.append(1)
 a.add(v,f,mi);a.finish(c)

def plant(c,m):
 stem=Mesh('connected-naked-dichotomous-axes',m);cap=Mesh('terminal-spindle-sporangia',m)
 stem.tube([(-.10,-.025,.005),(-.065,-.005,.008),(-.025,.005,.007),(.02,.015,.006),(.065,.002,.006),(.105,.025,.005)],[.0007,.005,.005,.0045,.0035,.0006],1)
 for i,(x,y,h,lean) in enumerate([(-.07,-.005,.145,-.025),(-.025,.005,.18,.016),(.022,.015,.163,.03),(.065,.002,.122,.025),(-.012,.045,.115,-.035)]):
  base=(x,y,.007)
  if i==4:stem.tube([(-.025,.005,.007),base],[.004,.003],1)
  fork=(x+lean*.4,y+.008,h*.58)
  control=Vector((x-lean*.1,y-.007,h*.28));start=Vector(base);end=Vector(fork)
  stem.tube([tuple((1-t)**2*start+2*t*(1-t)*control+t*t*end) for t in [j/7 for j in range(8)]],[.0042-.001*j/7 for j in range(8)],0,n=12)
  for sign in (-1,1):
   tip=(x+lean+sign*.018,y+sign*.011,h)
   control=Vector((fork[0]+sign*.015,fork[1]+sign*.008,h*.81));start=Vector(fork);end=Vector(tip)
   stem.tube([tuple((1-t)**2*start+2*t*(1-t)*control+t*t*end) for t in [j/5 for j in range(6)]],[.0032-.001*j/5 for j in range(6)],0,n=12)
   cap.tube([tip,(tip[0]+sign*.002,tip[1],h+.009),(tip[0]+sign*.003,tip[1],h+.019),(tip[0]+sign*.004,tip[1],h+.024)],[.0022,.0044,.0035,.0006],2,n=12)
 stem.finish(c);cap.finish(c)

def bird(c,m):
 b=Mesh('continuous-breast-neck-head',m)
 b.loft([(.048,.002,.070,.003),(.037,.013,.071,.014),(.018,.023,.076,.026),(-.005,.025,.082,.029),(-.025,.020,.091,.030),(-.037,.013,.111,.023),(-.046,.014,.129,.018),(-.058,.017,.137,.016),(-.071,.013,.136,.012),(-.078,.007,.134,.006)],0,n=24);b.finish(c)
 bill=Mesh('elongate-narrow-snout',m);bill.loft([(-.073,.007,.133,.0058),(-.088,.0055,.133,.0043),(-.111,.003,.132,.0026),(-.125,.0008,.131,.0008)],3,n=12);bill.finish(c)
 wings=Mesh('layered-folded-feather-wings',m)
 for s in (-1,1):
  # Bent tapered feather vanes originate within shoulder, sweep gently backward.
  for j in range(6):
   p=[(s*(.017+j*.0008),-.022+j*.007,.097-j*.0015),(s*(.026+j*.0002),.005+j*.006,.088-j*.002),(s*(.022-j*.001),.039+j*.002,.074-j*.001)]
   wings.tube(p,[.0075,.007,.0012],1 if j<4 else 2,n=8,oval=.48)
 wings.finish(c)
 tail=Mesh('short-feathered-tail-fan',m)
 for j in range(5):
  x=(j-2)*.006
  tail.tube([(x*.35,.031,.078),(x,.052,.073),(x*1.3,.075-abs(j-2)*.004,.071)],[.005,.0055,.001],1,n=8,oval=.5)
 tail.finish(c)
 legs=Mesh('legs-and-separated-toes',m)
 for s in (-1,1):
  x=s*.011
  legs.tube([(x,.008,.065),(x,.016,.036),(x,-.003,.007)],[.0047,.0028,.0022],3,n=10)
  for j in range(3):legs.tube([(x,-.003,.006),(x+(j-1)*.005,-.017,.003),(x+(j-1)*.008,-.028+abs(j-1)*.005,.0022)],[.0022,.0015,.0007],3,n=8)
  legs.tube([(x,-.001,.005),(x,.012,.0025)],[.0018,.0007],3,n=8)
 legs.finish(c)
 eyes=Mesh('eyes-with-subtle-socket',m)
 for s in (-1,1):
  eyes.ell((s*.0147,-.062,.141),(.003,.0034,.0034),3,n=12,r=6)
  eyes.ell((s*.0169,-.063,.1415),(.0015,.0022,.0022),4,n=12,r=6)
 eyes.finish(c)

def insect(c,m):
 b=Mesh('tapered-segmented-body',m)
 b.loft([(-.005,.0007,.003,.0007),(-.0038,.0014,.003,.0012),(-.002,.0012,.0032,.0011),(0,.0015,.003,.0012),(.002,.0017,.0027,.0012),(.004,.0016,.0026,.001),(.006,.0011,.0025,.0008),(.008,.00025,.0024,.00025)],0,n=16);b.finish(c)
 h=Mesh('head-eyes-antennae',m);h.ell((0,-.006,.0033),(.0017,.0013,.0011),1)
 for s in (-1,1):
  h.ell((s*.00145,-.0063,.0036),(.00065,.0008,.00075),4,n=12,r=6)
  h.tube([(s*.0008,-.0069,.0037),(s*.0015,-.009,.0046),(s*.0028,-.0115,.005),(s*.0036,-.013,.0046)],[.00014,.00012,.00008,.00004],1,n=6)
 h.finish(c)
 l=Mesh('six-articulated-legs',m)
 for i,y in enumerate([-.0035,-.001,.001]):
  for s in (-1,1):
   l.tube([(s*.0009,y,.0029),(s*.003,y+(-.001 if i==0 else .001),.0025),(s*.0045,y+(i-1)*.002,.0009),(s*.0058,y+(i-1)*.003,.00016)],[.00032,.00028,.00018,.00010],1,n=8)
 l.finish(c)
 w=Mesh('long-hindwings-and-short-forewing-covers',m)
 for s in (-1,1):
  w.tube([(s*.0009,-.001,.0037),(s*.002,.002,.0036),(s*.0024,.006,.0034),(s*.0017,.0086,.0031)],[.0005,.00115,.001,.0001],2,n=10,oval=.15)
  w.tube([(s*.0008,-.0025,.004),(s*.0018,-.0012,.0041),(s*.0023,.0005,.0039)],[.00065,.00095,.00025],3,n=10,oval=.3)
 w.finish(c)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--asset',required=True);ap.add_argument('--output');ap.add_argument('--no-preview',action='store_true');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);s=args.asset
 cfg=json.loads((P/'items'/s/'build-config.json').read_text());brief=json.loads((P/'items'/s/'brief.json').read_text());refs=json.loads((P/'items'/s/'references.json').read_text());c=setup_scene(s,cfg['seed'])
 palettes={'urasterella':['#B98E6B','#927057','#C19B78','#D9BA90','#292B28'],'aglaophyton':['#72937A','#596F54','#AB8A52','#C3A56C','#30362B'],'longipteryx':['#82908B','#596E70','#6D7E7B','#977F64','#202C2C'],'alienopterus':['#716957','#806E4E','#A29777','#594F3D','#2D332E']}
 m=[make_material(s+'-'+str(i),h,roughness=.84) for i,h in enumerate(palettes[s])]
 {'urasterella':star,'aglaophyton':plant,'longipteryx':bird,'alienopterus':insect}[s](c,m)
 ground_asset(c)
 parent=Path(args.output) if args.output else ROOT/'assets/candidates/continuous-small-life-20261018/batch-02/r001'
 meta={'description':{'en':f'Original static stylized-inspired {s}; evidence-informed teaching art, not a strict scientific reconstruction.','zh':f'{s} 原创静态风格化教学美术；参考基本形态，并非严格科考复原。'},'generator':str(Path(__file__).relative_to(ROOT)),'sources':refs['sources'],'claim_scope':brief['claim_scope'],'nominal_scale':brief['scale'],'artistic_choices':brief['artistic_choices'],'static_only':True,'texture_count':0,'texture_decoded_bytes':0,'revision':'r001','maker':{'model':'GPT-6.1 Sol','reasoning':'medium'},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256((P/'items'/s/'build-config.json').read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256((Path(__file__).parent/'lib/asset_common.py').read_bytes()).hexdigest()}
 record=export_asset(s,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata=meta,output_root=parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not args.no_preview:
  render_previews(c,parent/s,views=('hero','reversehero','front','side','rear','top','clay','silhouette'),resolution=512,samples=16,transparent=True)
 print('BATCH02_COMPLETE',json.dumps(record))
