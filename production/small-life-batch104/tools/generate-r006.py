#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch104 geometry, authored strictly after original-v001 freeze."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from math import sin,cos,pi
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.groups={};self.contacts=[]
 def add(self,v,f,mi=0,tag=None):
  n=len(self.v);self.v.extend([tuple(x) for x in v]);self.f.extend([tuple(n+x for x in face) for face in f]);self.mi.extend([mi]*len(f))
  if tag:self.groups.setdefault(tag,[]).extend(range(n,n+len(v)))
 def emit(self,name,m,col):
  lo=[min(v[k] for v in self.v) for k in range(3)];hi=[max(v[k] for v in self.v) for k in range(3)];offset=Vector((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]));self.v=[Vector(v)+offset for v in self.v]
  o=mesh_object(name,self.v,self.f,m,col)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
  for tag,vs in self.groups.items():o.vertex_groups.new(name=tag).add(vs,1,'REPLACE')
  o['construction_counts']=json.dumps({k:len(v) for k,v in self.groups.items()});o['contact_design']=json.dumps(self.contacts);return o

def frame(axis):
 t=Vector(axis).normalized();u=t.cross(Vector((0,0,1)))
 if u.length<.01:u=t.cross(Vector((0,1,0)))
 u.normalize();return t,u,t.cross(u).normalized()
def tube(M,points,radii,sides,mat,tag):
 v=[]
 for i,pp in enumerate(points):
  p=Vector(pp);t,u,w=frame(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]))
  for j in range(sides):v.append(p+radii[i]*(u*cos(2*pi*j/sides)+w*sin(2*pi*j/sides)))
 f=[tuple(range(sides))[::-1]]
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 f.append(tuple(range((len(points)-1)*sides,len(points)*sides)));M.add(v,f,mat,tag)
def blade(M,base,tip,width,normal,mi,tag):
 b=Vector(base);e=Vector(tip);a=e-b;n=Vector(normal).normalized();side=n.cross(a).normalized();c=b+a*.43
 v=[b,e,c+side*width*.5,c+n*width*.10,c-side*width*.5,c-n*width*.10];f=[]
 for j in range(4):x=2+j;y=2+(j+1)%4;f.extend([(0,x,y),(1,y,x)])
 M.add(v,f,mi,tag)
def polyvolume(M,outline,thick,mi,tag,fold=lambda x,z:0):
 # Concave boundary tessellated in its XZ plane; front/back stay solid and closed.
 verts=[Vector((x,0,z)) for x,z in outline];tri=tessellate_polygon([verts]);lookup={tuple(v):i for i,v in enumerate(verts)};faces=[tuple((v if isinstance(v,int) else lookup[tuple(v)]) for v in t) for t in tri];n=len(verts)
 v=[(x,fold(x,z)-thick/2,z) for x,z in outline]+[(x,fold(x,z)+thick/2,z) for x,z in outline]
 f=faces+[tuple(n+i for i in reversed(t)) for t in faces]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)];M.add(v,f,mi,tag)

def oval(M,center,radii,mi,tag,N=12):
 # Closed two-ring faceted oblate solid, not a card.
 cx,cy,cz=center;rx,ry,rz=radii;v=[(cx,cy,cz-rz),(cx,cy,cz+rz)]
 for k,zf in enumerate([-.45,.45]):
  for j in range(N):a=2*pi*j/N;v.append((cx+rx*.894*cos(a),cy+ry*.894*sin(a),cz+rz*zf))
 f=[]
 for j in range(N):a=2+j;b=2+(j+1)%N;f.extend([(0,b,a),(a,b,b+N,a+N),(1,a+N,b+N)])
 M.add(v,f,mi,tag)

def longbody(M,L,W,H,Z,mi,tag,rings=32,sides=12,y0=0,box=False,constant=False):
 v=[]
 for k in range(rings+1):
  t=k/rings;y=y0-L/2+L*t
  taper=(.42+.58*sin(pi*t)**.42) if not box else (.80+.20*sin(pi*t))*(1-.30*t)
  if constant:taper=1
  ann=1+(.035 if k%2==0 else -.025)
  for j in range(sides):
   a=2*pi*j/sides;x=cos(a);z=sin(a)
   if box:x=math.copysign(abs(x)**.43,x);z=math.copysign(abs(z)**.65,z)
   v.append((W*.5*taper*ann*x,y,Z+H*.5*taper*ann*z))
 f=[tuple(range(sides))[::-1]]
 for k in range(rings):
  for j in range(sides):a=k*sides+j;b=k*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 f.append(tuple(range(rings*sides,(rings+1)*sides)));M.add(v,f,mi,tag)
def xyshape(M,outline,thick,mi,tag):
 # Full-volume faceted convex outline with cambered middle; six boundary points give24tri.
 n=len(outline);center=sum((Vector(x) for x in outline),Vector())/n
 v=[Vector(x)+Vector((0,0,-thick/2)) for x in outline]+[Vector(x)+Vector((0,0,thick/2)) for x in outline]+[center-Vector((0,0,thick)),center+Vector((0,0,thick))]
 f=[]
 for j in range(n):k=(j+1)%n;f.extend([(2*n,k,j),(2*n+1,j+n,k+n),(j,k,k+n,j+n)])
 M.add(v,f,mi,tag)
def flap(M,side,y,root,reach,width,z,tipz,mi,tag,pointed=False):
 # Nonzero root width, embedded in body; posterior sweep and open tip gaps.
 x=side*root;end=side*reach
 outline=[(x,y-width*.42,z),(side*(root+(reach-root)*.60),y-width*.40,z+(tipz-z)*.50),(end,y+width*(.15 if pointed else .05),tipz),(side*(root+(reach-root)*.70),y+width*.48,z+(tipz-z)*.75),(side*(root+(reach-root)*.25),y+width*.45,z+(tipz-z)*.25),(x,y+width*.35,z)]
 xyshape(M,outline,max(width*.07,.00005),mi,tag)
def join(M,child,parent):M.contacts.append({'child':child,'parent':parent})
def softappendage(M,side,base,length,radius,mi,tag,rings=14):
 pts=[];rr=[]
 for k in range(rings+1):
  t=k/rings;pts.append((side*(abs(base[0])+length*.27*sin(pi*t)),base[1]-length*t,base[2]+length*.12*sin(pi*t)-length*.09*t));rr.append(radius*(1-.75*t)*(1+.08*(k%2)))
 tube(M,pts,rr,8,mi,tag);return pts,rr

def topz(M,tag,x,y):
 # Double-precision XY barycentric intersection of ACTUAL authored triangles.
 # No fixed meter-sized ray epsilon; suitable for the39.8mm juvenile.
 ss=set(M.groups[tag]);hits=[]
 for f in M.f:
  if not set(f)<=ss:continue
  for i in range(1,len(f)-1):
   a,b,c=[M.v[q] for q in [f[0],f[i],f[i+1]]];den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
   if abs(den)<1e-30:continue
   u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den;v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den;w=1-u-v
   if min(u,v,w)>=-1e-9:hits.append(u*a[2]+v*b[2]+w*c[2])
 if not hits:raise ValueError(('No actual parent surface',tag,x,y))
 return max(hits)
def trilobed_plate(M,y,half,step,Z,mi,tag,collum=False):
 xs=[-1,-.65,-.4,0,.4,.65,1];zs=[-.0006,-.00035,.00035,.0012,.00035,-.00035,-.0006]
 if collum:zs=[-.0001,.00045,.00085,.0012,.00085,.00045,-.0001]
 v=[]
 for off in [-.00045,0]:
  for row in [-.53,0,.53]:
   for x,z in zip(xs,zs):v.append((x*half*(.88 if row<0 else 1),y+step*row,Z+z+off))
 f=[];n=21
 for row in range(2):
  for j in range(6):
   a=row*7+j;f.extend([(a,a+1,a+8,a+7),(a+n,a+7+n,a+8+n,a+1+n)])
 border=list(range(7))+[13,20]+list(range(19,13,-1))+[7]
 for i,a in enumerate(border):b=border[(i+1)%len(border)];f.append((a,b,b+n,a+n))
 M.add(v,f,mi,tag)

def kerygmachela(c,m,col):
 p=c['parameters'];M=Mesh();L=p['trunk_length_m'];W=p['trunk_width_m'];Z=p['body_center_z_m'];H=p['trunk_height_m'];longbody(M,L,W,H,Z,0,'soft_trunk',44)
 for k in range(11):
  t=k/10;y=-L*.42+L*.84*t;reach=p['max_flap_reach_m']*[.58,.76,.91,1,1,.95,.84,.72,.61,.48,.36][k];width=p['flap_foreaft_width_m']*(.65+.35*sin(pi*t));root=W*.32
  for side in [-1,1]:
   tag=f'flap_{side}_{k:02d}';flap(M,side,y,root,reach,width,Z,Z-.002,1+(k%3==0),tag);join(M,tag,'soft_trunk')
   tag=f'leg_{side}_{k:02d}';tube(M,[(side*.006,y,Z-.003),(side*.012,y-.001,.008),(side*.015,y-.003,.002)],[.0026,.002,.0011],6,0,tag);join(M,tag,'soft_trunk')
  taper=(.42+.58*sin(pi*(y/L+.5))**.42)
  for j,xfrac in enumerate([-.68,-.25,.25,.68]):
   x=W*.5*taper*xfrac;z=Z+H*.5*taper*math.sqrt(1-xfrac*xfrac);tag=f'tubercle_{k:02d}_{j}';oval(M,(x,y,z-.0002),(.00115,.0014,.0011),2,tag,6);join(M,tag,'soft_trunk')
 oval(M,(0,-.052,Z+.001),(.009,.009,.006),1,'anterior_lobe',12);join(M,'anterior_lobe','soft_trunk')
 # One median tail with no segmentation, sharply tapering but closed tip.
 tube(M,[(0,.045,Z),(0,.088,Z-.002),(0,.140,Z-.004)],[.0033,.0015,.00014],8,0,'median_tail');join(M,'median_tail','soft_trunk')
 for side in [-1,1]:
  tag=f'frontal_{side}';pts,rr=softappendage(M,side,(side*.007,-.052,Z),p['frontal_appendage_length_m'],.004,0,tag);join(M,tag,'anterior_lobe')
  for k in range(p['frontal_spines_per_appendage']):
   i=3+k;root=Vector(pts[i]);tip=root+Vector((-side*(.008+.004*k/7),-.004,.0007));s=f'frontal_spine_{side}_{k}';tube(M,[root,tip],[.0011,.00013],5,2,s);join(M,s,tag)
  # Bent flattened lens, low on the outside of the frontal attachment, not eyeball spheres.
  ey=f'eye_{side}';tube(M,[(side*.008,-.049,Z-.002),(side*.011,-.052,Z-.004),(side*.012,-.056,Z-.003)],[.0018,.0022,.0015],8,4,ey);join(M,ey,'anterior_lobe')
  rs=f'rostral_spine_{side}';tube(M,[(side*.003,-.054,Z-.004),(side*.004,-.066,Z-.007)],[.0011,.0001],5,2,rs);join(M,rs,'anterior_lobe')
 oval(M,(0,-.056,Z-.0045),(.0035,.002,.0015),3,'ventral_mouth',10);join(M,'ventral_mouth','anterior_lobe');M.emit('kerygmachela-soft-single-tail',m,col)

def pambdelurion(c,m,col):
 p=c['parameters'];M=Mesh();L=p['trunk_length_m'];W=p['trunk_width_m'];H=p['trunk_height_m'];Z=p['body_center_z_m'];longbody(M,L,W,H,Z,0,'annulated_trunk',110)
 oval(M,(0,-.117,Z),(.031,.027,.025),1,'rounded_head',16);join(M,'rounded_head','annulated_trunk')
 for k in range(11):
  t=k/10;y=-.097+.192*t;reach=p['max_flap_reach_m']*(.75+.25*sin(pi*t));width=p['flap_foreaft_width_m'];root=.022
  for side in [-1,1]:
   tag=f'flap_{side}_{k:02d}';flap(M,side,y,root,reach,width,Z+.001,Z-.012,1+(k%3==0),tag);join(M,tag,'annulated_trunk')
   tag=f'leg_{side}_{k:02d}';tube(M,[(side*.016,y,Z-.010),(side*.027,y-.001,.027),(side*.038,y-.003,.005)],[.007,.006,.003],7,4,tag);join(M,tag,'annulated_trunk')
 for side in [-1,1]:
  tag=f'frontal_{side}';pts,rr=softappendage(M,side,(side*.021,-.131,Z-.006),p['frontal_appendage_length_m'],.008,0,tag,20);join(M,tag,'rounded_head')
  for k in range(6):
   root=Vector(pts[5+4*(k//2)])+Vector((0,0,(-1 if k%2 else 1)*.0028));s=f'inner_spine_{side}_{k}';tube(M,[root,root+Vector((-side*.014,-.004,0))],[.002,.0003],5,2,s);join(M,s,tag)
  for j in range(3):
   root=Vector(pts[-2]);s=f'distal_spine_{side}_{j}';tube(M,[root,root+Vector((side*(j-1)*.008,-.022-.007*(j==1),.003*(j-1)))],[.002,.0002],5,2,s);join(M,s,tag)
  for j in range(3):
   x=side*(.006+.008*j);base=(x,-.130,Z+.006);s=f'cephalic_spine_{side}_{j}';tube(M,[base,(x,-.150-.002*(j==1),Z+.012)],[.0025,.0003],6,2,s);join(M,s,'rounded_head')
  s=f'posterior_lobe_{side}';tube(M,[(side*.010,.113,Z),(side*.015,.139,Z-.002)],[.006,.0017],7,0,s);join(M,s,'annulated_trunk')
 # Shallow ventral mouth disk, with cone-shaped raised lip but no horn/nose.
 oval(M,(0,-.134,Z-.019),(.014,.013,.006),3,'oral_cone',16);join(M,'oral_cone','rounded_head')
 for j in range(16):
  a=2*pi*j/16;x=.008*cos(a);y=-.134+.008*sin(a);tag=f'oral_plate_{j:02d}';blade(M,(x,y,Z-.022),(x*.65,-.134+(y+.134)*.65,Z-.027),.003,(0,0,-1),2,tag);join(M,tag,'oral_cone')
 M.emit('pambdelurion-benthic-soft-lobopodian',m,col)

def aegirocassis(c,m,col):
 p=c['parameters'];M=Mesh();L=p['trunk_length_m'];Z=p['body_center_z_m'];longbody(M,L,p['trunk_width_m'],p['trunk_height_m'],Z,0,'box_trunk',22,12,y0=.40,box=True)
 oval(M,(0,-.060,Z),(.150,.12,.13),0,'head_under_shields',12);join(M,'head_under_shields','box_trunk')
 outline=[(0,-.84,.48),(.10,-.62,.49),(.145,-.25,.51),(.11,-.02,.50),(0,.015,.51),(-.11,-.02,.50),(-.145,-.25,.51),(-.10,-.62,.49)]
 xyshape(M,outline,.028,1,'central_carapace');join(M,'central_carapace','head_under_shields')
 tube(M,[(0,-.81,.493),(0,-.42,.548),(0,-.03,.525)],[.004,.008,.004],5,2,'carapace_ridge');join(M,'carapace_ridge','central_carapace')
 for side in [-1,1]:
  tag=f'lateral_shield_{side}';oval(M,(side*.135,-.083,.455),(.077,.145,.058),1,tag,12);join(M,tag,'head_under_shields')
  tag=f'carapace_extension_{side}';blade(M,(side*.115,-.22,.51),(side*.155,-.08,.34),.09,(side,0,0),1,tag);join(M,tag,'central_carapace')
  tag=f'inferred_eye_{side}';oval(M,(side*.182,.009,.428),(.015,.017,.014),4,tag,8);join(M,tag,f'lateral_shield_{side}')
 for k in range(10):
  t=k/10;y=.035+k*.071;root=.12*(1-.28*t);factor=1-.42*t
  for side in [-1,1]:
   tag=f'dorsal_flap_{side}_{k:02d}';flap(M,side,y,root,p['dorsal_flap_reach_m']*factor,.067,Z+.06,Z+.12,1,tag,True);join(M,tag,'box_trunk')
   tag=f'ventral_flap_{side}_{k:02d}';flap(M,side,y,root,p['ventral_flap_reach_m']*factor,.072,Z-.055,Z-.10,2,tag);join(M,tag,'box_trunk')
  # Twelve broad linear setal-blade cues per band; fine lamellae not fabricated.
  for j in range(12):
   x=(j-5.5)*.021*(1-.30*t);z=Z+.093*(.80+.20*sin(pi*(y/.8)))*(1-.30*y/.8);tag=f'dorsal_band_{k:02d}';tube(M,[(x,y-.022,topz(M,'box_trunk',x,y-.022)-.001),(x,y+.022,topz(M,'box_trunk',x,y+.022)+.003)],[.0032,.0032],4,3,tag)
  join(M,f'dorsal_band_{k:02d}','box_trunk')
 for side in [-1,1]:
  pts=[(side*(.082+.008*k/7),-.105-.12*k/7,(.36 if k==0 else .307-.012*k/7)) for k in range(8)];tag=f'frontal_support_{side}';tube(M,pts,[.014*(1-.25*k/7)*(1+.08*(k%2)) for k in range(8)],6,0,tag);join(M,tag,'head_under_shields')
  # First is proximal article with short combspine; intermediate five bear longendites.
  s=f'proximal_comb_{side}';root=Vector(pts[1]);tube(M,[root,root+Vector((-side*.02,.018,-.06))],[.004,.001],5,3,s);join(M,s,tag)
  s=f'downturned_tip_{side}';tube(M,[pts[-1],Vector(pts[-1])+Vector((0,-.015,-.018))],[.008,.002],5,0,s);join(M,s,tag)
  for j in range(5):
   root=Vector(pts[j+2]);tip=root+Vector((-side*.067,-.005,-.241));et=f'filter_endite_{side}_{j}';tube(M,[root,tip],[.004,.0015],5,3,et);join(M,et,tag)
   st=f'filter_setae_{side}_{j}'
   for k in range(70):
    t=.025+.95*k/69;a=root.lerp(tip,t);b=a+Vector((-side*.007,-.027*(.75+.25*sin(pi*t)),.0005));tube(M,[a,b],[.00055,.00020],4,3,st)
   join(M,st,et)
 M.emit('aegirocassis-double-flaps-filter-baskets',m,col)

def octa(M,center,radii,mi,tag,N=4):
 c=Vector(center);rx,ry,rz=radii;v=[c+Vector(a) for a in [(rx,0,0),(-rx,0,0),(0,ry,0),(0,-ry,0),(0,0,rz),(0,0,-rz)]];M.add(v,[(4,0,2),(4,2,1),(4,1,3),(4,3,0),(5,2,0),(5,1,2),(5,3,1),(5,0,3)],mi,tag)

def arthropleura(c,m,col):
 p=c['parameters'];M=Mesh();L=p['body_length_m'];Z=p['body_center_z_m'];step=L/24
 # Small core is closed, under the sclerites. Plates are separate closed volumes.
 longbody(M,L,.004,.0028,Z-.0003,3,'ventral_core',24,10,constant=True)
 for k in range(24):
  y=-L/2+step*(k+.5);t=k/23;width=p['max_body_width_m']*(.82+.18*sin(pi*t))*(1-.46*t**4)
  if k==0:width*=.46
  if k==23:width*=.65
  half=width/2;tag=f'dorsal_unit_{k+1:02d}';outline=[(-half*.75,y-step*.57,Z),(-half,y+step*.30,Z-.0007),(-half*.55,y+step*.57,Z+.0001),(0,y+step*.55,Z+.0010),(half*.55,y+step*.57,Z+.0001),(half,y+step*.30,Z-.0007),(half*.75,y-step*.57,Z),(0,y-step*.59,Z+.0011)]
  trilobed_plate(M,y,half,step,Z,1+(k%4==0),tag,k==0);join(M,tag,'ventral_core')
  if 1<=k<=22:
   # Central ridge and paired wings form one trilobed closed shell, with low relief.
   for side in [-1,1]:
    for j in range(4):
     x=side*half*(.12+.18*(j%2));yy=y+(-.22 if j<2 else .22)*step;zz=topz(M,tag,x,yy)-.000045;s=f'tubercle_{k:02d}_{side}_{j}';octa(M,(x,yy,zz),(.00019,.00019,.00019),2,s,4);join(M,s,tag)
   # Four lateral relief cues per side; restrained, not long spines.
   for side in [-1,1]:
    for j in range(4):
     x=side*half*.80;yy=y+step*(-.25+.18*j);zz=topz(M,tag,x,yy)-.000045;s=f'lateral_tubercle_{k:02d}_{side}_{j}';octa(M,(x,yy,zz),(.00015,.00013,.00018),2,s,4);join(M,s,tag)
  if k==23:continue
  for pair in range(1 if k<2 else 2):
   yy=y+(pair-.5)*step*.48 if k>=2 else y
   for side in [-1,1]:
    # Eight successive limb articles, final one a tapered terminalclaw.
    start=Vector((side*.0015,yy,Z-.0007));mid=Vector((side*half*.86,yy-.0002,.0014));end=Vector((side*(half+.0007),yy-.0005,.00015));pts=[]
    for q in range(9):
     t=q/8;pt=start.lerp(mid,t/.55) if t<=.55 else mid.lerp(end,(t-.55)/.45);pts.append(pt)
    rr=[.00030*(1-.65*q/8)*(1+.12*(q%2)) for q in range(9)];s=f'leg_{k+1:02d}_{pair}_{side}';tube(M,pts,rr,5,0,s);join(M,s,'ventral_core')
 oval(M,(0,-L/2-.0006,Z-.00055),(.0024,.0019,.0012),0,'flattened_head',12);join(M,'flattened_head','ventral_core')
 for side in [-1,1]:
  s=f'antenna_{side}';pts=[]
  for j in range(8):t=j/7;pts.append((side*(.0012+.0018*t),-L/2-.001-.0041*t,Z-.0012-.0006*t))
  tube(M,pts,[.00034]+[.00024+.00004*j/7 for j in range(1,8)],6,0,s);join(M,s,'flattened_head')
  s=f'ocular_stalk_{side}';tube(M,[(side*.0018,-L/2-.0006,Z),(side*.0033,-L/2-.0011,Z+.0003)],[.00022,.00030],6,0,s);join(M,s,'flattened_head')
  e=f'ocular_club_{side}';oval(M,(side*.0035,-L/2-.0012,Z+.00035),(.0005,.00035,.0004),3,e,8);join(M,e,s)
  s=f'mouthpart_{side}';tube(M,[(side*.0011,-L/2-.0014,Z-.0012),(side*.0005,-L/2-.0017,Z-.0016)],[.00033,.00023],5,4,s);join(M,s,'flattened_head')
 M.emit('arthropleura-juvenile-24-dorsal-units',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());aid=cfg['asset_id'];out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'fossils',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Frozen primary-supported interpretation; artistic color and dimensions; juvenile Arthropleura not giant adult.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
