# SPDX-License-Identifier: MIT
"""Original stylized static fauna. Run with Blender 4.3.2 -b --python-exit-code 1.
-- --asset diplomystus|burgessomedusa|kalligramma [--output /absolute/parent] [--no-preview]
No external models, textures or source art incorporated. Seed 18.
"""
import sys, math, json, argparse
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews
pi=math.pi
class Part:
 def __init__(self,name,mats): self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  off=len(self.v);self.v.extend(v);self.f.extend([tuple(off+i for i in face) for face in f]);self.mi.extend(mi if isinstance(mi,list) else [mi]*len(f))
 def finish(self,c,smooth=False):
  o=mesh_object(self.name,self.v,self.f,self.mats,c)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i;p.use_smooth=smooth
  return o
 def tube(self,points,radii,mi=0,n=6):
  pts=[Vector(p) for p in points];v=[]
  for i,p in enumerate(pts):
   d=pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)];d.normalize();u=d.cross(Vector((0,0,1)))
   if u.length<.01:u=d.cross(Vector((0,1,0)))
   u.normalize();w=d.cross(u).normalized()
   for k in range(n):v.append(tuple(p+radii[i]*(u*math.cos(2*pi*k/n)+w*math.sin(2*pi*k/n))))
  f=[tuple(reversed(range(n)))]
  for i in range(len(pts)-1):
   for k in range(n): f.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
  f.append(tuple((len(pts)-1)*n+k for k in range(n)));self.add(v,f,mi)
 def ellipsoid(self,center,scale,mi=0,n=12,rings=7):
  # Nondegenerate poles and latitude strips.
  v=[(center[0],center[1],center[2]+scale[2])]
  for j in range(1,rings):
   a=pi*j/rings
   for k in range(n):
    b=2*pi*k/n;v.append((center[0]+scale[0]*math.sin(a)*math.cos(b),center[1]+scale[1]*math.sin(a)*math.sin(b),center[2]+scale[2]*math.cos(a)))
  bot=len(v);v.append((center[0],center[1],center[2]-scale[2]));f=[]
  for k in range(n):f.append((0,1+k,1+(k+1)%n))
  for j in range(rings-2):
   for k in range(n): a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b))
  for k in range(n):f.append((bot,1+(rings-2)*n+(k+1)%n,1+(rings-2)*n+k))
  self.add(v,f,mi)
 def sheet(self,outline,thickness,mi=0,axis=(1,0,0)):
  a=Vector(axis)*thickness/2;v=[tuple(Vector(p)+a) for p in outline]+[tuple(Vector(p)-a) for p in outline];n=len(outline)
  center=sum((Vector(p) for p in outline),Vector())/n
  v += [tuple(center+a),tuple(center-a)];f=[]
  for k in range(n):j=(k+1)%n;f.extend([(2*n,k,j),(2*n+1,n+j,n+k),(k,n+k,n+j,j)])
  self.add(v,f,mi)

def fish(c,m):
 body=Part('profile-loft-body',m)
 # y,half width,z center,half depth. Intentional deep forebody and gentle tail arc.
 profiles=[(-.128,.0015,.020,.0025),(-.123,.007,.016,.009),(-.112,.013,.009,.021),(-.100,.018,.006,.030),(-.084,.021,.002,.038),(-.065,.022,0,.043),(-.042,.021,0,.044),(-.018,.0195,-.001,.039),(.008,.016,-.001,.031),(.030,.012,-.001,.022),(.049,.0085,0,.014),(.065,.006,0,.008),(.079,.0045,.001,.006),(.088,.003,.002,.005)]
 n=20;v=[]
 for y,w,z,h in profiles:
  for k in range(n):a=2*pi*k/n;v.append((w*math.cos(a),y,z+h*math.sin(a)))
 f=[tuple(reversed(range(n)))];mi=[0]
 for j in range(len(profiles)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(0 if math.sin(2*pi*(k+.5)/n)>.55 else 1)
 f.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(0);body.add(v,f,mi);body.finish(c,True)
 fins=Part('fins-with-raised-ray-rhythm',m)
 # Dorsal, anal and deeply forked caudal: thickness gives honest backfaces.
 dorsal=[(0,-.032,.036),(0,-.020,.069),(0,-.008,.077),(0,.014,.034),(0,.027,.025)]
 anal=[(0,-.014,-.034),(0,.007,-.052),(0,.037,-.033),(0,.056,-.011)]
 tail=[(0,.078,.005),(0,.118,.040),(0,.143,.046),(0,.132,.023),(0,.111,.002),(0,.136,-.030),(0,.144,-.044),(0,.116,-.036),(0,.079,-.004)]
 for poly in [dorsal,anal,tail]:fins.sheet(poly,.0018,2)
 # Paired pectoral + pelvic fins attach directly to side surface.
 for s in [-1,1]:
  fins.sheet([(s*.017,-.087,-.008),(s*.046,-.066,-.030),(s*.035,-.044,-.025),(s*.019,-.061,-.016)],.0014,2,axis=(0,0,1))
  fins.sheet([(s*.011,-.021,-.029),(s*.024,-.003,-.050),(s*.016,.011,-.036),(s*.009,-.003,-.025)],.0012,2,axis=(0,0,1))
 for s in [-1,1]:
  for end in [(-.018,.065),(-.008,.072),(.004,.054)]:fins.tube([(s*.0012,-.025,.036),(s*.0012,end[0],end[1])],[.00048,.00022],1,5)
  for yy,zz in [(.132,.038),(.126,.027),(.128,-.026),(.136,-.037)]:fins.tube([(s*.0012,.084,.001),(s*.0012,yy,zz)],[.00048,.0002],1,5)
 fins.finish(c)
 face=Part('eyes-opercula-and-upturned-lip',m)
 for s in [-1,1]:
  face.ellipsoid((s*.0133,-.109,.016),(.0024,.0047,.0048),2,16,7)
  face.ellipsoid((s*.0153,-.110,.017),(.0010,.0029,.0030),3,16,7)
  face.ellipsoid((s*.0160,-.111,.018),(.00045,.0009,.0009),1,8,5)
  face.tube([(s*.013,-.092,.028),(s*.020,-.087,.018),(s*.021,-.085,.002),(s*.016,-.087,-.017)],[.00065]*4,0,5)
  # The lifted small mouth is a dark seam ending at the pointed, raised snout.
  face.tube([(s*.007,-.119,.010),(s*.004,-.126,.017),(s*.0015,-.129,.021)],[.00085,.0007,.00045],3,6)
 for j in range(12):
  y=-.082+j*.0041;z=.0405+(.0017 if j>3 else -.002)
  face.sheet([(-.0018,y,z),(0,y-.0018,z+.0034),(.0018,y,z),(0,y+.002,z-.001)],.001,0,axis=(0,1,0))
 face.finish(c)

def jelly(c,m):
 shell=Part('hollow-rounded-square-bell',m);n=32
 # Continuous thick shell with open oral cavity. Rounded square section, tall bell.
 rings=[(.004,.042),(.010,.046),(.040,.047),(.080,.043),(.112,.035),(.135,.023),(.145,.009),(.148,.0015),(.144,.0015),(.139,.008),(.130,.020),(.108,.031),(.078,.039),(.040,.043),(.010,.0425),(.004,.039)]
 v=[]
 for z,r in rings:
  for k in range(n):
   a=2*pi*k/n;co=math.cos(a);si=math.sin(a);v.append((r*math.copysign(abs(co)**.65,co),r*math.copysign(abs(si)**.65,si),z))
 f=[];mi=[]
 for j in range(len(rings)-1):
  if j==7:continue
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(2 if j in [0,14] else 1 if j>7 else 0 if k%8 in [0,1,7] else 1)
 f.extend([tuple(7*n+k for k in range(n)),tuple(reversed([8*n+k for k in range(n)]))]);mi.extend([1,1])
 # crown closure and closed wall around oral lip, cavity remains empty.
 for k in range(n):f.append(((len(rings)-1)*n+k,(len(rings)-1)*n+(k+1)%n,(k+1)%n,k));mi.append(2)
 shell.add(v,f,mi);shell.finish(c,True)
 fingers=Part('ninety-six-short-marginal-tentacles',m)
 for k in range(96):
  a=2*pi*k/96;co=math.cos(a);si=math.sin(a);x=.0405*math.copysign(abs(co)**.65,co);y=.0405*math.copysign(abs(si)**.65,si)
  length=.016+.003*(.5+.5*math.cos(4*a));d=Vector((co,si,0))
  p=Vector((x,y,.006));pts=[p,p+d*.002+Vector((0,0,-.006)),p+d*.004+Vector((0,0,-length*.75)),p+d*.0045+Vector((0,0,-length))]
  fingers.tube(pts,[.00115,.00110,.00085,.00028],3 if k%4 else 2,n=5)
 fingers.finish(c,True)
 # Subtle four inner corner supports; no invented face or long oral streamers.
 inner=Part('four-inner-radial-folds',m)
 for a in [pi/4,3*pi/4,5*pi/4,7*pi/4]:
  inner.tube([(.015*math.cos(a),.015*math.sin(a),.129),(.033*math.cos(a),.033*math.sin(a),.080),(.039*math.cos(a),.039*math.sin(a),.014)],[.0028,.0021,.0014],2,n=6)
 inner.finish(c,True)

def insect(c,m):
 wings=Part('four-volumetric-rounded-wings',m);veins=Part('branched-wing-veins',m);spots=Part('four-inlaid-eye-spots',m)
 # Parametric tapered root, rounded distal edge. Each wing a closed lens.
 for s in [-1,1]:
  for fore in [True,False]:
   root=Vector((s*.002,-.006 if fore else .004,.004 if fore else .0025))
   u=Vector((s*(.053 if fore else .043),-.029 if fore else .032,.009 if fore else .004))
   perp=Vector((s*.012,.024 if fore else .020,-.001))
   def pos(t,q,z=0):return root+u*t+perp*(math.sin(pi*t)**.72)*q+Vector((0,0,z+.0025*math.sin(pi*t)))
   # Elliptical outline around root/tip, each pair connected in order.
   outline=[pos(0,0)]
   for j in range(1,13):outline.append(pos(j/13,-1))
   outline.append(pos(1,0))
   for j in range(12,0,-1):outline.append(pos(j/13,1))
   # layered fill with a curved middle ridge rather than a flat playing card.
   n=len(outline);center=pos(.52,0);v=[tuple(p+Vector((0,0,.00035))) for p in outline]+[tuple(p-Vector((0,0,.00035))) for p in outline]+[tuple(center+Vector((0,0,.0011))),tuple(center-Vector((0,0,.0006)))];f=[];mi=[]
   for k in range(n):j=(k+1)%n;f.extend([(2*n,k,j),(2*n+1,n+j,n+k),(k,n+k,n+j,j)]);mi.extend([0 if k%13<8 else 1,0 if k%13<8 else 1,1])
   wings.add(v,f,mi)
   # Sparse primary and cross-vein rhythm, readable at normal prop size.
   for q in [-.7,0,.7]:
    pts=[pos(t,q,.00105) for t in [.04,.25,.50,.74,.94]];veins.tube(pts,[.00028,.00025,.00022,.00018,.00010],2,5)
   for t in [.28,.45,.64,.80]:
    for q in [-1,1]:veins.tube([pos(t,0,.00110),pos(t+.06,q*.48,.00105),pos(min(t+.10,.96),q*.95,.0007)],[.00019,.00016,.00010],2,5)
   # Pattern is original artwork: muted rings with central dark pupil on each wing.
   p=pos(.59,0,.0017)
   for rr,z,mat in [(.0065,0,2),(.0048,.00016,1),(.0028,.0003,3),(.0011,.00040,0)]:
    vs=[tuple(p+Vector((0,0,z)))]+[tuple(p+Vector((rr*math.cos(2*pi*k/20),rr*.85*math.sin(2*pi*k/20),z))) for k in range(20)]
    spots.add(vs,[(0,1+k,1+(k+1)%20) for k in range(20)],mat)
 wings.finish(c);veins.finish(c);spots.finish(c)
 body=Part('head-thorax-and-segmented-abdomen',m)
 body.ellipsoid((0,-.004,.0045),(.0048,.008,.0047),2,12,8)
 body.ellipsoid((0,-.014,.0048),(.0037,.0038,.0037),2,12,7)
 for j in range(7):body.ellipsoid((0,.005+j*.003,.0025-j*.00025),(.0036-j*.00035,.0025,.0031-j*.00025),2 if j%2==0 else 1,10,6)
 for s in [-1,1]:body.ellipsoid((s*.0028,-.0155,.0055),(.0017,.0018,.0018),3,10,6)
 body.finish(c,True)
 limbs=Part('six-legs-two-antennae-and-proboscis',m)
 for s in [-1,1]:
  for j in range(3):
   y=-.009+j*.005
   limbs.tube([(s*.0025,y,.003),(s*.008,y+(-.005+j*.004),-.002),(s*.012,y+(-.008+j*.007),-.007),(s*.015,y+(-.011+j*.010),-.007)],[.00065,.00050,.00035,.00018],2,6)
  limbs.tube([(s*.0015,-.016,.007),(s*.003,-.023,.010),(s*.006,-.030,.0105),(s*.008,-.033,.0095)],[.00036,.00027,.00020,.00010],2,6)
 limbs.tube([(0,-.017,.003),(0,-.025,.001),(0,-.034,-.002),(0,-.037,-.004)],[.00048,.00040,.00029,.00015],2,7)
 limbs.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',required=True,choices=['diplomystus','burgessomedusa','kalligramma']);p.add_argument('--output',type=Path,default=ROOT/'assets/candidates/small-fauna-trio-v1');p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);s=a.asset;c=setup_scene(s,18)
 palettes={'diplomystus':['#527D8C','#B5D9D5','#DAAE7A','#233B49'],'burgessomedusa':['#A995BD','#C7B6D7','#E2D9DD','#81B6B2'],'kalligramma':['#D9B379','#F2DDB1','#85654C','#354B50']}
 mats=[make_material(s+'-'+str(i),color,roughness=.72 if s=='diplomystus' else .85) for i,color in enumerate(palettes[s])]
 {'diplomystus':fish,'burgessomedusa':jelly,'kalligramma':insect}[s](c,mats)
 meta={'description':{'en':'Original child-friendly stylized concept inspired by '+s+'. Artistic palette, pose, scale and simplified detail; static, not a scientific reconstruction.','zh':'原创儿童友好史前启发造型；颜色、姿态、尺寸和简化细节属于艺术选择。静态模型，非严格科学复原。'},'generator':'production/small-fauna-trio-v1/build_trio.py','revision':'v001','status':'candidate','mounting_point':'body/bell centerline at local origin; free-swimming/flying static specimen, not ground contact','textures':[],'claim_scope':'named-taxon-inspired stylized art','sources':json.loads((ROOT/'production/small-fauna-trio-v1'/s/'references.json').read_text())['sources']}
 export_asset(s,{'en':'Stylized '+s.capitalize(),'zh':{'diplomystus':'古鱼 Diplomystus','burgessomedusa':'箱钟水母 Burgessomedusa','kalligramma':'宽翅蝶蛉 Kalligramma'}[s]},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=10000,max_materials=4,max_primitives=24)
 if not a.no_preview:render_previews(c,a.output/s,views=('hero','reversehero','front','side','rear','top','clay','silhouette'),resolution=640,samples=32,transparent=True)
if __name__=='__main__':main()
