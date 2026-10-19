# SPDX-License-Identifier: MIT
"""Original concept-first volumetric geometry. Blender 4.3.2. Deterministic."""
import argparse,json,math,sys,time
from pathlib import Path
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,export_asset,ground_asset
from math import sin,cos,pi,sqrt

def mesh(name,v,f,mat):return mesh_object(name,v,f,mat,C)
def loft(name,rings,n,mat,ridge=0,ridges=8):
 v=[];f=[]
 for z,r,cx,cy in rings:
  for i in range(n):
   a=2*pi*i/n;rr=r*(1+ridge*cos(ridges*a));v.append((cx+rr*cos(a),cy+rr*sin(a),z))
 for j in range(len(rings)-1):
  for i in range(n):k=j*n+i;l=j*n+(i+1)%n;f.append((k,l,l+n,k+n))
 f.extend([tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))])
 return mesh(name,v,f,mat)
def ellipsoid(name,center,radii,mat,n=16,rings=6):
 v=[(center[0],center[1],center[2]-radii[2])];f=[]
 for j in range(1,rings):
  p=-pi/2+pi*j/rings
  for i in range(n):a=2*pi*i/n;v.append((center[0]+radii[0]*cos(p)*cos(a),center[1]+radii[1]*cos(p)*sin(a),center[2]+radii[2]*sin(p)))
 v.append((center[0],center[1],center[2]+radii[2]));top=len(v)-1
 for i in range(n):f.append((0,1+(i+1)%n,1+i));f.append((top,1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n))
 for j in range(rings-2):
  for i in range(n):k=1+j*n+i;l=1+j*n+(i+1)%n;f.append((k,l,l+n,k+n))
 return mesh(name,v,f,mat)
def tube(name,points,radii,mat,n=6):
 v=[];f=[]
 for j,(p,r) in enumerate(zip(points,radii)):
  P=Vector(p);D=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(0,j-1)])
  D.normalize();u=D.cross(Vector((0,0,1)))
  if u.length<.01:u=D.cross(Vector((0,1,0)))
  u.normalize();w=D.cross(u).normalized()
  for i in range(n):v.append(tuple(P+r*(cos(2*pi*i/n)*u+sin(2*pi*i/n)*w)))
 for j in range(len(points)-1):
  for i in range(n):k=j*n+i;l=j*n+(i+1)%n;f.append((k,l,l+n,k+n))
 f.extend([tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+i for i in range(n))]);return mesh(name,v,f,mat)
def mackenzia():
 mats=[make_material('sac-peach','#D99A81'),make_material('fold-warm','#C98A76'),make_material('ridge-cream','#EBC1A2'),make_material('holdfast','#D8B492'),make_material('apical-inner','#B67A67')]
 # Integrated eightfold profile, continuous wall folds rather than separate rods.
 body=loft('Eight-fold soft sac',[(.009,.004,0,0),(.017,.008,0,0),(.029,.015,0,0),(.047,.020,0,0),(.069,.022,0,0),(.089,.021,0,0),(.108,.017,.001,0),(.124,.011,.002,0),(.136,.0058,.002,0),(.140,.0051,.002,0),(.1398,.0035,.002,0),(.133,.0028,.002,0),(.131,.0016,.002,0)],64,mats,.13)
 for p in body.data.polygons:
  if p.center.z>.138:p.material_index=2
  elif p.center.z>.130 and p.index>=10*64:p.material_index=4
  else:
   a=math.atan2(p.center.y,p.center.x);c=cos(8*a);p.material_index=2 if c>.78 else 1 if c<-.70 else 0
 loft('Short anchoring stalk',[(0,.007,0,0),(.002,.009,0,0),(.004,.007,0,0),(.008,.004,0,0),(.014,.0045,0,0)],24,mats[3])
 return mats

def prasopora():
 mats=[make_material('colony-seafoam','#9FBEB0'),make_material('pore-interior','#71998E'),make_material('epitheca-cream','#D8CFAD')]
 # Connected dome; inset chambers are integral faces, not black stickers or floating tubes.
 n=36;L=9;v=[];f=[];mi=[]
 for j in range(L+1):
  t=(pi/2-.05)*j/L
  for i in range(n):a=2*pi*(i+.30*sin(j*1.71))/n;v.append((.030*cos(t)*cos(a),.029*cos(t)*sin(a),.003+.024*sin(t)))
 for j in range(L):
  for i in range(n):
   ids=[j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i]
   # Pore clusters follow colony regions; broad quiet strips remain.
   pore=j>0 and j<8 and ((i//4+j//2)%3!=0)
   if not pore:f.append(tuple(ids));mi.append(0);continue
   corners=[Vector(v[k]) for k in ids];ctr=sum(corners,Vector())/4;normal=Vector((ctr.x/.030**2,ctr.y/.029**2,(ctr.z-.003)/.024**2)).normalized()
   start=len(v)
   # Octagonal mouths with tapered cavity walls, clustered across curved regions.
   inner=[]
   for k,q in enumerate(corners):
    for near in [corners[(k-1)%4],corners[(k+1)%4]]:
     inner.append(ctr+(q-ctr)*.40+(near-ctr)*.13)
   for q in inner:v.append(tuple(q))
   for q in inner:v.append(tuple(ctr+(q-ctr)*.70-normal*.00070))
   for k in range(4):
    q=(k+1)%4
    f.append((ids[k],start+2*k,start+2*k+1));mi.append(0)
    f.append((ids[k],ids[q],start+2*q,start+2*k+1));mi.append(0)
   for k in range(8):
    q=(k+1)%8;f.append((start+k,start+q,start+8+q,start+8+k));mi.append(1)
   f.append(tuple(start+8+k for k in range(8)));mi.append(1)
 f.append(tuple(L*n+i for i in range(n)));mi.append(0)
 f.append(tuple(range(n-1,-1,-1)));mi.append(2)
 o=mesh('Porous integrated bryozoan dome',v,f,mats)
 for p,m in zip(o.data.polygons,mi):p.material_index=m
 # Broad nearly flat wrinkled underside closes at ground and is part of the colony.
 # Real closed radially corrugated underside. No planar cap hiding the folds.
 profile=[(.00045,.002,0,0)]
 for rad in [.004,.006,.0072,.008,.0088,.010,.0128,.014,.0152,.017,.0188,.020,.0212,.023,.024,.025,.026]:
  depth=.00050-.00042*sum(math.exp(-((rad-r)/.00070)**2) for r in [.008,.014,.020,.025])
  profile.append((depth,rad,0,0))
 profile.extend([(.00035,.028,0,0),(.00070,.0296,0,0),(.0016,.0305,0,0),(.0028,.0303,0,0),(.0032,.0299,0,0),(.003,.002,0,0)])
 loft('Closed epitheca with visible concentric lower folds',profile,48,mats[2])
 return mats

def strophomena():
 mats=[make_material('shell-sand','#DDC4A1'),make_material('growth-lavender','#B9A4AD'),make_material('hinge-warm','#C2AB92')]
 # Polar fan topology, hinge exactly straight; no scallop ears. Continuous solid shell.
 N=96;J=12;v=[];f=[];mi=[]
 # upper surface shallow concavity, lower surface convexity; rims seal same perimeter.
 for side in [0,1]:
  v.append((0,.013,.006 if side==0 else .004))
  for j in range(1,J+1):
   r=j/J
   for i in range(N+1):
    a=-pi/2+pi*i/N;rib=.5+.5*cos(32*(a+pi/2));edge=.00030*r**4*rib
    x=(.0275*r+edge)*sin(a);y=.013-(.041*r+edge)*cos(a)
    base=.0045-.0025*sin(pi*r)*cos(a)**2
    z=base+(.0007+.00115*sqrt(r)*rib if side==0 else -.00075+.0008*sqrt(r)*rib)
    v.append((x,y,z))
 K=1+J*(N+1)
 for s in range(2):
  off=s*K
  for i in range(N):f.append((off,off+1+i,off+2+i));mi.append(0)
  for j in range(J-1):
   for i in range(N):
    k=off+1+j*(N+1)+i;f.append((k,k+1,k+N+2,k+N+1));mi.append(1 if j in [7,8] and i%6 in [1,2,3,4] else 0)
 # perimeter includes radial hinge edges and front semicircle, bridge upper/lower.
 border=[0]+[1+j*(N+1) for j in range(J)]+[1+(J-1)*(N+1)+i for i in range(1,N+1)]+[1+j*(N+1)+N for j in range(J-2,-1,-1)]
 for i,k in enumerate(border):l=border[(i+1)%len(border)];f.append((k,l,l+K,k+K));mi.append(2)
 o=mesh('Shallow articulated radial-ribbed valves',v,f,mats)
 for p,m in zip(o.data.polygons,mi):p.material_index=m
 return mats

def ctenoimbricata():
 mats=[make_material('membrane-dusty-violet','#9D8FA8'),make_material('marginal-ivory','#DCC7A7'),make_material('comb-peach','#CB9C86'),make_material('ossicle-light','#D4C0AB'),make_material('oral-cavity','#6B5E70')]
 # All features in meters; central body is 20 mm long, longer dimensions include spines.
 ellipsoid('Low plated membrane',(0,.0003,.0015),(.0064,.0093,.00145),mats[0],32,8)
 # Discrete closed frame segments, four paired lateral positions, one posterior.
 for s in [-1,1]:
  for k,(y,x,ry) in enumerate([(-.0055,.0053,.0018),(-.0019,.0064,.0019),(.002,.0061,.0019),(.0056,.0049,.0019)]):
   ellipsoid('Marginal M%d %s'%(k+2,'L' if s<0 else 'R'),(s*x,y,.00165),(.00145,ry,.00095),mats[1],8,4)
   tube('Lateral spine %d %s'%(k+2,s),[(s*(x+.0006),y,.0015),(s*(x+.003),y+.0001,.0013),(s*(x+.005),y+.0009,.0008)],[.00048,.00031,.000045],mats[2],6)
  for k,x in enumerate([.001,.0032]):ellipsoid('Anterior marginal M%d %s'%(k,s),(s*x,-.0074,.0013),(.0011,.0015,.00075),mats[1],8,4)
 ellipsoid('Single posterior marginal Mp',(0,.0087,.0015),(.0027,.0014,.0008),mats[1],10,4)
 # Broad anterior gap, shaded cavity has a solid back. No radial mouth or legs.
 ellipsoid('Anterior oral recess',(0,-.00845,.001),(.0048,.001,.00065),mats[4],16,4)
 for i in range(14):
  x=(i-6.5)*.00062; y=-.0083+.00055*(abs(x)/.0041)**2;length=.0030-.00065*(abs(x)/.0041)**1.5
  tube('Ventral anterior ctenidial element %02d'%(i+1),[(x,y,.00085),(x*1.1,y-length*.60,.00063),(x*1.15,y-length,.0004)],[.00030,.00022,.000045],mats[2],6)
 # Overlapping roof, broad plate surfaces retain imbricate hierarchy.
 for row in range(3):
  for i in range(7-row):
   x=(i-(6-row)/2)*.00113;y=-.0068-row*.00058
   ellipsoid('Dorsal imbricate roof %d-%d'%(row,i),(x,y,.0021-row*.00015),(.00070,.00064,.00032),mats[1],6,4)
 for y,xs in [(-.0034,[-.002,0,.002]),(0,[-.003,0,.003]),(.0032,[-.002,0,.002]),(.0058,[0])]:
  for x in xs:ellipsoid('Sparse dorsal stud %s %s'%(x,y),(x,y,.00275),(.00028,.00030,.00024),mats[3],5,3)
 # Group repeated closed elements by semantic structure while retaining individual mesh islands.
 for prefix,label in [('Ventral anterior ctenidial','Anterior comb - 14 closed elements'),('Dorsal imbricate','Imbricate dorsal roof'),('Sparse dorsal','Sparse dorsal stud field')]:
  group=[o for o in C.objects if o.type=='MESH' and o.name.startswith(prefix)]
  bpy.ops.object.select_all(action='DESELECT')
  for o in group:o.select_set(True)
  bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();group[0].name=label
 return mats

def main():
 global C
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 cfg=json.loads(args.config.read_text());slug=cfg['asset_id'];C=setup_scene(slug,seed=cfg['seed']);t=time.time();globals()[slug]();ground_asset(C,center_xy=False)
 record=export_asset(slug,{'en':slug.title(),'zh':{'mackenzia':'肋囊古生动物','prasopora':'穹顶苔藓动物','strophomena':'宽凹壳腕足动物','ctenoimbricata':'双侧棘缘棘皮动物'}[slug]},'animals',C,metadata={'generator':str(Path(__file__).resolve().relative_to(ROOT)),'description':{'en':cfg['notes'],'zh':'具名属形态启发的原创柔和低多边形概念；非标本级科学复原。'},'scientific_scope':'Genus-informed stylized interpretation; uncertain soft anatomy and colors are artistic; no coexistence claim.','surface_profile':'original-palette-only','config_sha256':__import__('hashlib').sha256(args.config.read_bytes()).hexdigest()},output_root=args.output_dir,render=False,max_triangles=cfg['max_triangles'],max_materials=cfg['max_materials'],max_primitives=cfg['max_primitives'],collection_id='undersea-concept')
 print(json.dumps({'asset_id':slug,'wall_seconds':time.time()-t,'glb':record['glb'],'triangles':record['triangles']}))
if __name__=='__main__':main()
