# SPDX-License-Identifier: MIT
"""Original batch-03 static teaching art. Blender 4.3.2, deterministic meters.
blender -b -t 2 --python-exit-code 1 --python THIS_FILE -- --asset cephalaspis
No reference images, meshes, palettes or textures incorporated.
"""
import sys, math, json, argparse, hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene, make_material, mesh_object, export_asset, ground_asset, render_previews
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
  # A tail fork is concave: use proper polygon tessellation, never center fans.
  from mathutils.geometry import tessellate_polygon
  poly=[Vector(p) for p in outline];triangles=tessellate_polygon([poly]);f=[]
  for tri in triangles:
   ids=[t if isinstance(t,int) else next(i for i,p in enumerate(poly) if (p-t).length<1e-8) for t in tri]
   f.extend([tuple(ids),tuple(n+i for i in reversed(ids))])
  for k in range(n):j=(k+1)%n;f.append((k,n+k,n+j,j))
  self.add(v,f,mi)


def catmull(points,steps=3,closed=False):
 p=[Vector(v) for v in points];out=[]
 for i in range(len(p) if closed else len(p)-1):
  a=p[(i-1)%len(p)] if closed or i else p[0];b=p[i];c=p[(i+1)%len(p)];d=p[(i+2)%len(p)] if closed or i+2<len(p) else p[-1]
  for j in range(steps):
   t=j/steps;out.append(tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)))
 if not closed:out.append(tuple(p[-1]))
 return out

def loft(part,profiles,n=24,mi=0):
 # x-offset, y, z-center, half-width, half-height along a -Y forward body.
 v=[];f=[];m=[]
 for x,y,z,w,h in profiles:
  for k in range(n):
   a=2*pi*k/n;v.append((x+w*math.cos(a),y,z+h*math.sin(a)))
 f.append(tuple(reversed(range(n))));m.append(mi)
 for j in range(len(profiles)-1):
  for k in range(n):
   f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));m.append(mi)
 f.append(tuple((len(profiles)-1)*n+k for k in range(n)));m.append(mi);part.add(v,f,m)

def cephalaspis(c,m):
 shield=Part('horseshoe-shield-swept-corners',m)
 half=[(0,-.083),(.016,-.081),(.031,-.073),(.042,-.058),(.048,-.038),(.049,-.014),(.047,.010),(.044,.023),(.040,.016),(.030,-.001),(.016,-.007),(0,-.009)]
 outline=catmull(half+ [(-x,y) for x,y in reversed(half[1:-1])],3,True);n=len(outline);v=[];f=[];mi=[]
 # Closed radial shield, broad smooth top planes, gently rounded rim and shallow underside.
 for r,z in [(.03,.027),(.26,.0267),(.52,.0245),(.76,.020),(.94,.013),(1,.010),(.96,.0075),(.62,.006),(.03,.006)]:
  for x,y in outline:v.append((x*r,-.043+(y+.043)*r,z))
 for j in range(8):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(0 if j<4 else 1 if j<6 else 2)
 f.extend([tuple(reversed(range(n))),tuple(8*n+k for k in range(n))]);mi.extend([0,2]);shield.add(v,f,mi);shield.finish(c,True)
 body=Part('tapered-continuous-trunk',m)
 prof=[(0,-.023,.013,.017,.010),(0,-.011,.014,.020,.012),(.0005,.004,.014,.018,.012),(.001,.022,.014,.014,.011),(.002,.043,.014,.010,.0085),(.005,.066,.014,.0065,.006),(.007,.085,.015,.004,.004),(.006,.104,.017,.0026,.003),(.003,.118,.019,.0014,.002)]
 loft(body,prof,24,1);o=body.finish(c,True)
 for p in o.data.polygons:
  if p.center.z<.011:p.material_index=2
 fins=Part('soft-paired-and-median-fin-membranes',m)
 for sign in [-1,1]:
  poly=[(sign*.014,-.008,.012),(sign*.023,.003,.010),(sign*.031,.022,.007),(sign*.028,.032,.006),(sign*.019,.029,.008),(sign*.010,.014,.011)]
  fins.sheet(catmull(poly,3,True),.00065,1,axis=(0,0,1))
 # Small dorsal fin and asymmetric upturned caudal web; no armored pectoral arms.
 fins.sheet(catmull([(.005,.051,.019),(.005,.062,.033),(.006,.074,.035),(.007,.084,.019),(.006,.076,.017)],3,True),.0006,0)
 fins.sheet(catmull([(.006,.095,.018),(.003,.115,.032),(.001,.135,.040),(.002,.137,.035),(.003,.127,.023),(.003,.133,.013),(.004,.128,.011),(.005,.113,.014)],3,True),.00065,1)
 fins.finish(c,True)
 details=Part('high-set-eyes-and-small-ventral-mouth',m)
 for s in [-1,1]:
  details.ellipsoid((s*.013,-.045,.026),(.0041,.0051,.0019),2,16,6)
  details.ellipsoid((s*.013,-.0457,.0275),(.0020,.0027,.0010),3,14,6)
  details.ellipsoid((s*.0126,-.0465,.0282),(.00055,.0007,.00025),2,8,4)
 details.ellipsoid((0,-.064,.0058),(.004,.0019,.0006),3,12,5);details.finish(c,True)
 marks=Part('quiet-shield-sensory-rim-and-tail-rays',m)
 # Restrained rim accent follows the shield, not a second floating plate.
 arc=[(x*.90,-.043+(y+.043)*.90,.0150) for x,y in outline if y<-.034]
 # Separate right and left arcs are intentionally short to avoid a closing crossbar.
 for sign in [-1,1]:
  pts=catmull([(sign*.007,-.078,.015),(sign*.025,-.070,.016),(sign*.039,-.055,.016),(sign*.044,-.038,.016)],3)
  marks.tube(pts,[.00038]*len(pts),1,6)
 for y,z in [(.126,.034),(.128,.026),(.126,.015)]:marks.tube([(.0058,.106,.019),(.0046,(y+.106)/2,(z+.019)/2),(.0032,y,z)],[.00035,.00025,.0001],0,5)
 marks.finish(c,True)

def saccocoma(c,m):
 cup=Part('small-stemless-scalloped-cup',m)
 # Bowl-like calyx with a closed underside and a shallow central oral surface.
 n=30;v=[];f=[];mi=[]
 for r,z in [(.0003,.007),(.0018,.0072),(.0031,.009),(.0033,.011),(.0029,.0116),(.0015,.0110),(.0003,.0107)]:
  for k in range(n):
   a=2*pi*k/n;rr=r*(1+.045*math.cos(5*a));v.append((rr*math.cos(a),rr*math.sin(a),z))
 for j in range(6):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(0 if j<3 else 1)
 f.extend([tuple(reversed(range(n))),tuple(6*n+k for k in range(n))]);mi.extend([0,1]);cup.add(v,f,mi);cup.finish(c,True)
 arms=Part('five-bifurcating-branching-arms',m);pinnules=Part('fine-featherlike-lateral-branches',m);flanges=Part('simplified-lateral-wing-ribbons',m)
 for j in range(5):
  ang=2*pi*j/5+.16;rad=Vector((math.cos(ang),math.sin(ang),0));tan=Vector((-math.sin(ang),math.cos(ang),0))
  trunk=[rad*.0025+Vector((0,0,.010)),rad*.005+Vector((0,0,.0117)),rad*.0075+Vector((0,0,.013))]
  arms.tube(trunk,[.00065,.00058,.00046],1,8)
  for s in [-1,1]:
   pts=[]
   for i in range(15):
    t=i/14;r=.0073+.0175*t;side=s*(.0001+.0055*t+.0024*math.sin(pi*t));z=.013+.0055*math.sin(pi*t*.85)+.0012*t*math.sin(ang)
    pts.append(rad*r+tan*side+Vector((0,0,z)))
   arms.tube(pts,[.00046*(1-i/15)**.9+.000045 for i in range(15)],1,8)
   # A sparse feather rhythm. Alternate lengths and upward curl keep the spaces open.
   for k in range(2,13):
    p=pts[k];direction=(pts[k+1]-pts[k-1]).normalized();sidevec=Vector((-direction.y,direction.x,0)).normalized()
    for side in [-1,1]:
     length=(.0024*(math.sin(pi*k/15)**.7)+.0004)*(1+.10*math.sin(j+k))
     end=p+sidevec*side*length+direction*length*.23+Vector((0,0,.00045))
     mid=p.lerp(end,.55)+Vector((0,0,.00025));pinnules.tube([p,mid,end],[.00016,.00012,.000035],2 if k%4==0 else 1,5)
   # The near-cup lateral flanges are economical closed membranes, not precise fossil cross-sections.
   for k in range(1,7):
    a=pts[k];b=pts[k+1];w=.00055*(1-k/9);sidevec=tan*s
    flanges.sheet([tuple(a),tuple(a+sidevec*w+Vector((0,0,.00018))),tuple(b+sidevec*w*.7),tuple(b)],.00008,0,axis=(0,0,1))
 arms.finish(c,True);pinnules.finish(c,True);flanges.finish(c,False)

def archaeocidaris(c,m):
 test=Part('rounded-test-with-fivefold-plate-fields',m)
 n=60;rings=18;v=[(0,0,.051)];f=[];mi=[]
 for j in range(1,rings):
  a=pi*j/rings
  for k in range(n):
   b=2*pi*k/n;rr=.0225*math.sin(a)*(1+.015*math.cos(10*b)*math.sin(a)**2)
   v.append((rr*math.cos(b),rr*math.sin(b),.031+.020*math.cos(a)))
 bot=len(v);v.append((0,0,.011))
 for k in range(n):f.append((0,1+k,1+(k+1)%n));mi.append(0)
 for j in range(rings-2):
  for k in range(n):
   a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b));mi.append(1 if (k%12 in [0,1,10,11]) else 0)
 for k in range(n):f.append((bot,1+(rings-2)*n+(k+1)%n,1+(rings-2)*n+k));mi.append(1)
 test.add(v,f,mi);test.finish(c,True)
 collars=Part('organized-plate-bosses',m);spines=Part('tapered-primary-spines',m);seams=Part('large-scale-plate-rhythm',m)
 for sector in range(5):
  for col in [-1,1]:
   for row,elevation in enumerate([-.37,.18,.73]):
    a=2*pi*sector/5+col*.24+(.035 if row%2 else -.035);d=Vector((math.cos(a)*math.cos(elevation),math.sin(a)*math.cos(elevation),math.sin(elevation)))
    base=Vector((d.x*.0225,d.y*.0225,.031+d.z*.020))
    length=[.025,.030,.024][row]*(1+.10*math.sin(sector*2+col));end=base+d*length;end.z=max(.001,end.z)
    # A narrow foot collar grows into each spine; lower spines sweep out above the contact plane.
    mid=base.lerp(end,.43)+Vector((-.0008*math.sin(a),.0008*math.cos(a),.0013))
    collars.tube([base-d*.0012,base,base+d*.0022],[.0029,.0031,.00165],2,10)
    pts=catmull([base+d*.0014,mid,end],4)
    spines.tube(pts,[.0016*(1-i/(len(pts)-.2))**.72+.00006 for i in range(len(pts))],2 if row!=2 else 3,8)
  # Plate boundaries and fine ambulacral bosses run between primary spine columns.
  a=2*pi*sector/5
  for e in [-.52,-.06,.42,.93]:
   pts=[]
   for k in range(7):
    b=a-.48+.96*k/6;rr=.02265*math.cos(e);pts.append((rr*math.cos(b),rr*math.sin(b),.031+.02015*math.sin(e)))
   seams.tube(pts,[.00018]*7,1,5)
  for e in [-.46,-.15,.17,.47,.77,1.02]:
   d=Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)));p=Vector((d.x*.0227,d.y*.0227,.031+d.z*.0202))
   collars.ellipsoid(p,(.00065,.00065,.0006),1,8,4)
 collars.finish(c,True);spines.finish(c,True);seams.finish(c,True)

def onoclea(c,m):
 rhiz=Part('one-creeping-rhizome-and-attached-roots',m)
 pts=catmull([(-.105,0,.008),(-.055,-.010,.010),(0,0,.011),(.05,.008,.009),(.105,-.004,.008)],4)
 rhiz.tube(pts,[.0050+.0005*math.sin(i) for i in range(len(pts))],3,10)
 for x in [-.085,-.035,.025,.075]:
  for side in [-1,1]:rhiz.tube([(x,0,.009),(x+.009,side*.012,.003),(x+.020,side*.020,.001)],[.0014,.0007,.0002],3,6)
 rhiz.finish(c,True)
 stems=Part('tapered-sterile-and-fertile-frond-axes',m);leaves=Part('broad-lobed-sterile-blades',m);veins=Part('restrained-midveins',m);fertile=Part('narrow-beaded-fertile-branchlets',m)
 # Fronds grow at separate nodes along the same network, rather than a radial stock fern.
 specs=[(-.083,-2.1,.34,.18,.049),(-.035,-.65,.43,.16,.058),(.010,1.00,.38,.18,.054),(.054,2.10,.45,.15,.057),(.087,-.15,.32,.20,.050)]
 for idx,(x,angle,height,spread,width) in enumerate(specs):
  d=Vector((math.cos(angle),math.sin(angle),0));base=Vector((x,0,.010));axis=[]
  for k in range(26):
   t=k/25;axis.append(base+d*(spread*t**1.7)+Vector((0,0,height*(t-.17*t**3))))
  stems.tube(axis,[.0029*(1-k/26)**1.25+.00015 for k in range(26)],2,8)
  # Connected upper lamina, deep rounded sinuses and leaf-size taper. Each lobe is built into one blade mesh.
  side=Vector((-d.y,d.x,0));start=.29;v=[];f=[];mat=[];samples=49
  for layer in [1,-1]:
   for k in range(samples):
    t=k/(samples-1);u=start+(1-start)*t;center=base+d*(spread*u**1.7)+Vector((0,0,height*(u-.17*u**3)))
    envelope=math.sin(pi*(.08+.92*t))**.70
    # Six pairs of broad lobes separated by smoothly cut sinuses; integrated terminal lobe.
    rhythm=.34+.66*(.5+.5*math.cos(2*pi*((5.35+idx*.12)*t-.10)))**.50
    w=max(.0006,width*envelope*rhythm*(1-.48*t))
    for q in [-1,0,1]:
     qw=w*(1.14+.10*math.sin(t*17+idx+q*.8))*(1+.06*q*math.sin(t*11+idx));p=center+side*(q*qw)+d*(abs(q)*.008*math.sin(pi*t))+Vector((0,0,-abs(q)*.005*envelope+layer*.00038))
     v.append(tuple(p))
  layern=samples*3
  for layer in [0,1]:
   for k in range(samples-1):
    for q in [0,1]:
     a=layer*layern+3*k+q;b=a+3
     f.append((a,a+1,b+1,b) if layer==0 else (a,b,b+1,a+1));mat.append(0 if idx%3 else 1)
  for k in range(samples-1):
   for q in [0,2]:
    a=k*3+q;b=(k+1)*3+q;f.append((a,b,b+layern,a+layern));mat.append(1)
  for k in [0,samples-1]:
   for q in [0,1]:a=k*3+q;f.append((a,a+layern,a+1+layern,a+1));mat.append(1)
  leaves.add(v,f,mat)
  # Modest central rib follows the curved blade and fades into the terminal lobe.
  vv=[tuple(axis[k]+Vector((0,0,.00065))) for k in range(8,26)];veins.tube(vv,[.00075*(1-j/19)+.00008 for j in range(18)],2,6)
 # Three fertile fronds: contracted branchlets carry repeated curled bead-like fertile leaflets.
 for idx,(x,angle,h) in enumerate([(-.06,.55,.26),(.018,-1.50,.34),(.076,2.8,.29)]):
  d=Vector((math.cos(angle),math.sin(angle),0));side=Vector((-d.y,d.x,0));base=Vector((x,0,.011));axis=[base+d*(.045*(k/16)**1.5)+Vector((0,0,h*k/16)) for k in range(17)]
  stems.tube(axis,[.0020*(1-k/18)+.00022 for k in range(17)],3,8)
  for row in range(6):
   t=.42+row*.086;p=base+d*(.045*t**1.5)+Vector((0,0,h*t));length=.025*(1-row*.105)
   for sign in [-1,1]:
    end=p+side*sign*length+Vector((0,0,.013));fertile.tube([p,p.lerp(end,.55),end],[.0011,.00075,.0003],3,6)
    for bead in range(1,4):
     u=bead/3.4;pos=p.lerp(end,u)+d*(.0015*math.sin(row));r=.0034*(1-.17*bead/4)
     fertile.ellipsoid(pos,(r,r*.76,r*1.30),4 if row<4 else 3,6,4)
  fertile.ellipsoid(axis[-1],(.002,.002,.004),3,10,6)
 stems.finish(c,True);leaves.finish(c,True);veins.finish(c,True);fertile.finish(c,True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--asset',choices=['cephalaspis','saccocoma','archaeocidaris','onoclea'],required=True);ap.add_argument('--output',type=Path);ap.add_argument('--no-preview',action='store_true');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 slug=args.asset;plan=ROOT/'production/continuous-small-life-20261018/items'/slug;config=json.loads((plan/'build-config.json').read_text());brief=json.loads((plan/'brief.json').read_text())
 c=setup_scene(slug,config['seed'])
 palettes={'cephalaspis':['#90967B','#A6AC91','#CDCAB0','#283A39'], 'saccocoma':['#B38F8A','#D9C9B2','#C4A197'], 'archaeocidaris':['#9B8E89','#B8AA9B','#847675','#AC9184'], 'onoclea':['#67936A','#789F6D','#9BAC76','#797554','#A18A60']}
 m=[make_material(slug+'-'+str(i),color,.82) for i,color in enumerate(palettes[slug])];globals()[slug](c,m)
 # Set exact artistic size in the configured axis, preserving a common meter coordinate system.
 allverts=[o.matrix_world@v.co for o in c.all_objects if o.type=='MESH' for v in o.data.vertices]
 axis=1 if slug=='cephalaspis' else 2 if slug=='onoclea' else None
 extent=max(v[axis] for v in allverts)-min(v[axis] for v in allverts) if axis is not None else max(max(v[k] for v in allverts)-min(v[k] for v in allverts) for k in [0,1])
 factor=config['nominal_scale']['meters']/extent
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=factor
 ground_asset(c,center_xy=True)
 output=args.output or ROOT/'assets/candidates/continuous-small-life-20261018/batch-03';parent=output/slug/('r002' if slug=='onoclea' else 'r001')
 names={'cephalaspis':{'en':'Stylized Cephalaspis','zh':'风格化头甲鱼'},'saccocoma':{'en':'Stylized Saccocoma','zh':'风格化无柄游泳海百合'},'archaeocidaris':{'en':'Stylized Archaeocidaris','zh':'风格化板棘海胆'},'onoclea':{'en':'Onoclea-inspired dimorphic fern patch','zh':'球子蕨启发的双型叶丛'}}
 note={'cephalaspis':'Broad horseshoe shield, small dorsal eyes and a gently curved tapering body.','saccocoma':'Small stemless cup and five bifurcating arm bases with delicate open branches.','archaeocidaris':'Rounded plated test and organized long primary spines, with quiet space between.','onoclea':'Broad lobed sterile blades and narrow beaded fertile fronds attached to one creeping rhizome.'}
 zh={'cephalaspis':'宽马蹄形头盾、顶部小眼及轻弯渐细的躯尾。','saccocoma':'无长柄小杯体、五条分叉腕基和开放细枝。','archaeocidaris':'圆板壳和有序渐细长棘，留出可读壳体。','onoclea':'宽裂营养叶与狭窄珠状生殖叶相连于同一匍匐根茎。'}
 metadata={'description':{'en':note[slug]+' Original static child-friendly teaching art; not a scientific reconstruction.','zh':zh[slug]+'原创静态儿童场景教学美术，并非严格科考复原。'},'generator':str(Path(__file__).relative_to(ROOT)),'config':str((plan/'build-config.json').relative_to(ROOT)),'sources':json.loads((plan/'references.json').read_text())['sources'],'claim_scope':brief['claim_scope'],'artistic_choices':{'en':'Color, exact proportions, nominal dimensions, pose, simplified plate counts, flanges and fine anatomy are artistic. No third-party image/mesh/texture incorporated.','zh':'颜色、精确比例、标称尺寸、姿态、简化板列、翼缘和细部为艺术处理；不收录第三方图像、网格或纹理。'},'static_only':True,'texture_profile':'palette-only; zero textures','scale':config['nominal_scale'],'origin_detail':'floor contact center; suspended specimens may be translated upward by the scene author','maker':{'model':'GPT-6.1 Sol','reasoning':'medium'},'independent_qa':'pending parent dispatch'}
 record=export_asset(slug,names[slug],brief['subject']['category'],c,metadata=metadata,output_root=parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30,resolution=512,samples=8,diagnostics=False)
 if not args.no_preview:
  target=parent/slug
  render_previews(c,target,('hero','reversehero','front','side','rear','top','clay','silhouette'),resolution=512,samples=8,transparent=True)
  q=json.loads((target/'qa.json').read_text());q['previews']={'status':'rendered_not_independently_reviewed','engine':'Cycles CPU','resolution':512,'samples':8,'views':['hero','reversehero','front','side','rear','top','clay','silhouette'],'transparent':True};(target/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
 print(json.dumps({'asset':slug,'glb_sha256':record['sha256']['glb'],'bytes':record['glb_bytes'],'triangles':record['triangles'],'output':str(parent/slug)}),flush=True)
if __name__=='__main__':main()
