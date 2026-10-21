#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Original geometry authored after immutable batch109 freeze readback2026-10-21T05:28:30Z.
import argparse,datetime,hashlib,json,math,os,sys,random
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from math import sin,cos,pi,sqrt,atan2,exp
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object
sys.path.insert(0,str(Path(__file__).resolve().parent))
from export_batch109 import export_asset
V=Vector
class Patch:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.solids=[]
 def vert(self,p):self.v.append(tuple(p));return len(self.v)-1
 def face(self,ids,mat=0):self.f.append(tuple(ids));self.mi.append(mat)
 def prism(self,lo,hi,mat=0):
  n=len(lo);o=len(self.v);self.v+=list(map(tuple,lo+hi));self.face(range(o+n-1,o-1,-1),mat);self.face(range(o+n,o+2*n),mat)
  for k in range(n):j=(k+1)%n;self.face([o+k,o+j,o+n+j,o+n+k],mat)
  self.solids.append(list(range(o,o+2*n)))
 def merge(self,p):
  o=len(self.v);self.v+=p.v;self.f +=[tuple(o+i for i in f) for f in p.f];self.mi+=p.mi;self.solids +=[[o+i for i in q] for q in p.solids]
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.components=[]
 def add(self,p,tag,kind,parent=None,details=None):
  o=len(self.v);self.v+=p.v;self.f +=[tuple(o+i for i in f) for f in p.f];self.mi+=p.mi
  self.components.append(dict(tag=tag,kind=kind,parent=parent,vertices=list(range(o,o+len(p.v))),solids=[[o+i for i in q] for q in p.solids],details=details or {}))
 def emit(self,aid,m,col):
  lo=V(tuple(min(p[k] for p in self.v) for k in range(3)));hi=V(tuple(max(p[k] for p in self.v) for k in range(3)));delta=V((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z))
  ob=mesh_object(aid+'-original-volume',[V(p)+delta for p in self.v],self.f,m,col)
  for f,mi in zip(ob.data.polygons,self.mi):f.material_index=mi
  for c in self.components:ob.vertex_groups.new(name=c['tag']).add(c['vertices'],1,'REPLACE')
  contract=dict(schema_version=1,object_name=ob.name,translation=list(delta),components=self.components,interpretation='Closed physical components. Solids subdivisions are actual plate/ossicle volume. Natural recess floors are external surface models, not internal digestive organs.')
  t=bpy.data.texts.new('BATCH109_COMPONENT_CONTRACT.json');t.write(json.dumps(contract,sort_keys=True));ob['component_contract']=t.name
  return ob

def frame(axis,preferred=None):
 a=V(axis).normalized();n=V(preferred or ((0,0,1) if abs(a.z)<.9 else (0,1,0)));n=(n-a*n.dot(a)).normalized();u=n.cross(a).normalized();return u,n,a

def tube(points,radii,sides=8,mat=0,cap=True):
 p=Patch();rings=[]
 for i,(pt,r) in enumerate(zip(points,radii)):
  a=V(points[min(i+1,len(points)-1)])-V(points[max(0,i-1)]);u,n,a=frame(a);c=V(pt);rings.append([p.vert(c+r*(u*cos(2*pi*k/sides)+n*sin(2*pi*k/sides))) for k in range(sides)])
 for j in range(len(rings)-1):
  for k in range(sides):q=(k+1)%sides;p.face([rings[j][k],rings[j][q],rings[j+1][q],rings[j+1][k]],mat)
 if cap:p.face(list(reversed(rings[0])),mat);p.face(rings[-1],mat)
 p.solids=[list(range(len(p.v)))];return p

def ellipsoid(c,scale,n=16,rows=8,mat=0,mapping=None):
 p=Patch();c=V(c);scale=V(scale)
 def q(v):return c+(mapping(V(v)) if mapping else V(tuple(v[k]*scale[k] for k in range(3))))
 p.vert(q((0,0,-1)))
 for j in range(1,rows):
  lat=-pi/2+pi*j/rows
  for k in range(n):a=2*pi*k/n;p.vert(q((cos(lat)*cos(a),cos(lat)*sin(a),sin(lat))))
 top=p.vert(q((0,0,1)))
 for k in range(n):p.face([0,1+(k+1)%n,1+k],mat)
 for j in range(rows-2):
  for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;p.face([a,b,b+n,a+n],mat)
 off=1+(rows-2)*n
 for k in range(n):p.face([off+k,off+(k+1)%n,top],mat)
 p.solids=[list(range(len(p.v)))];return p

def block(c,axis,inward,width,depth,length,mat=0,tri=False):
 u,n,a=frame(axis,inward);c=V(c)
 cross=[(-.5,-.5),(.5,-.5),(0,.5)] if tri else [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]
 lo=[c+u*x*width+n*y*depth-a*length/2 for x,y in cross];hi=[q+a*length for q in lo];p=Patch();p.prism(lo,hi,mat);return p

def recess(c,normal,rx,ry,depth,mat=1,sides=10):
 c=V(c);u,n,a=frame(normal,(0,1,0) if abs(V(normal).y)<.9 else (1,0,0));p=Patch();rings=[]
 for scale,h in [(1.45,-depth*1.2),(1.30,depth*.3),(1,depth*.3),(.78,-depth*.65)]:rings.append([p.vert(c+a*h+u*rx*scale*cos(2*pi*k/sides)+n*ry*scale*sin(2*pi*k/sides)) for k in range(sides)])
 for j in range(3):
  for k in range(sides):q=(k+1)%sides;p.face([rings[j][k],rings[j][q],rings[j+1][q],rings[j+1][k]],mat if j<2 else 2)
 p.face(list(reversed(rings[0])),mat);p.face(rings[-1],2);p.solids=[list(range(len(p.v)))];return p

def column(M,z0,length,r,N,parent=None):
 p=Patch();step=length/N
 for j in range(N):
  z=z0+j*step;p.merge(tube([(0,0,z-step*.08),(0,0,z+step*.18),(0,0,z+step*.82),(0,0,z+step*1.08)],[r*.88,r,r,r*.88],8,3 if j%3==0 else 0))
 M.add(p,'column','column',parent,dict(columnals=N));M.add(tube([(0,0,z0-.001),(0,0,z0-.0005),(0,0,z0+.001)],[r*2.5,r*3,r*.8],10,3),'attachment_disk','attachment','column')

def ring_plate(c,r0,z0,r1,z1,a0,a1,mat=0):
 p=Patch();c=V(c);angles=[a0+(a1-a0)*j/3 for j in range(4)];outer=[c+V((r0*cos(a),r0*sin(a),z0)) for a in angles]+[c+V((r1*cos(a),r1*sin(a),z1)) for a in reversed(angles)];inner=[c+V(((q.x-c.x)*.94,(q.y-c.y)*.94,q.z-c.z)) for q in outer];p.prism(inner,outer,mat);return p

def paired_axis(points,r,stations,mat=1,double=False):
 p=Patch();start,end=map(V,[points[0],points[-1]]);axis=(end-start).normalized();inward=V((-start.x,-start.y,0));
 if inward.length<1e-8:inward=V((0,-1,0))
 u,n,a=frame(axis,inward);L=(end-start).length;step=L/stations
 # Continuous aboral connective core is deliberately behind, not across, the adoral food groove.
 p.merge(tube([start-n*r*.43,end-n*r*.13],[r*.26,r*.08],3,0))
 for j in range(stations):
  t=(j+.5)/stations;rr=r*(1-.66*t)
  for side in [-1,1]:
   shift=side*.10*step;c=start+a*(t*L+shift)+u*side*rr*.42-n*rr*.20
   p.merge(block(c,a,n,rr*.96,rr*1.12,step*1.13,mat,not double))
   if double:p.merge(block(start+a*(t*L+shift)+u*side*rr*.69+n*rr*.43,a,n,rr*.43,rr*.42,step*1.13,3))
 return p

def caryocrinites(cfg,m,col):
 p=cfg['parameters'];M=Mesh();base=.002;column(M,base,p['column_length_m'],p['column_radius_m'],p['columnals']);bottom=base+p['column_length_m']-.001;H=p['theca_height_m'];R=p['theca_width_m']/2;cz=bottom+H/2
 M.add(ellipsoid((0,0,cz),(R*.96,R*.96,H*.5),24,12),'theca','theca','column');rings=[(-1.40,-.50,4,'basal'),(-.50,.30,6,'infralateral'),(.30,1.0,8,'lateral')]
 for lo,hi,N,kind in rings:
  for j in range(N):
   a0=2*pi*j/N+.012;a1=2*pi*(j+1)/N-.012;r0=R*cos(lo);r1=R*cos(hi);z0=H*.5*sin(lo);z1=H*.5*sin(hi)
   Q=Patch();na=3;nl=3;rr=[]
   for scale in [.935,1.025]:
    grid=[]
    for ii in range(nl+1):
     lat=lo+(hi-lo)*ii/nl;grid.append([Q.vert((R*cos(lat)*cos(a0+(a1-a0)*jj/na)*scale,R*cos(lat)*sin(a0+(a1-a0)*jj/na)*scale,cz+H*.5*sin(lat)*scale)) for jj in range(na+1)])
    rr.append(grid)
   for side in range(2):
    for ii in range(nl):
     for jj in range(na):
      face=[rr[side][ii][jj],rr[side][ii][jj+1],rr[side][ii+1][jj+1],rr[side][ii+1][jj]];Q.face(face if side else list(reversed(face)),3 if j%3==0 else 0)
   boundary=[(0,jj) for jj in range(na+1)]+[(ii,na) for ii in range(1,nl+1)]+[(nl,jj) for jj in range(na-1,-1,-1)]+[(ii,0) for ii in range(nl-1,0,-1)]
   for (ii,jj),(kk,ll) in zip(boundary,boundary[1:]+boundary[:1]):Q.face([rr[0][ii][jj],rr[0][kk][ll],rr[1][kk][ll],rr[1][ii][jj]],0)
   Q.solids=[list(range(len(Q.v)))];M.add(Q,kind+'_'+str(j),kind+'_plate','theca')
 top=cz+H*.47;M.add(ellipsoid((0,0,top-.001),(R*.66,R*.66,.002),16,6,3),'tegmen','tegmen','theca')
 axes=[]
 for g,(count,center) in enumerate(zip(p['arm_group_counts'],[-pi/2,5*pi/6,pi/6])):
  for k in range(count):
   a=center+(k-(count-1)/2)*.24;rad=V((cos(a),sin(a),0));start=rad*(R*.50)+V((0,0,top-.0007));end=rad*p['arm_spread_m']+V((0,0,top+p['arm_length_m']*(.92+.08*cos(k*1.8))))
   tag=f'axis_g{g}_{k}';M.add(paired_axis([start,end],p['main_axis_radius_m'],p['axis_plate_stations'],1,True),tag,'double_biserial_axis','tegmen',dict(primary_group=g,terminal_axis=k))
   axis=(end-start).normalized();u,n,ax=frame(axis,-rad)
   for j in range(p['lateral_brachioles_per_axis']):
    t=.20+.68*j/(p['lateral_brachioles_per_axis']-1);side=-1 if j%2 else 1;c=start+(end-start)*t+u*side*p['main_axis_radius_m']*.5;e=c+u*side*p['lateral_brachiole_length_m']*.95+axis*p['lateral_brachiole_length_m']*.25+n*.0002
    M.add(paired_axis([c,e],.00022,p['lateral_brachiole_stations'],1),tag+'_brachiole_'+str(j),'biserial_brachiole',tag,dict(selected_lateral=j))
 # Closed anal valves on posterior tegmen; not an invented central exposed mouth.
 z=top+.0004;P=Patch();N=6;r=p['anal_pyramid_radius_m']
 for k in range(N):
  a0=2*pi*k/N+.025;a1=2*pi*(k+1)/N-.025;lo=[V((0,.0038,z-.0007)),V((r*cos(a0),.0038+r*sin(a0),z-.0005)),V((r*cos(a1),.0038+r*sin(a1),z-.0005))];hi=[V((0,.0038,z+.0014)),V((r*cos(a0),.0038+r*sin(a0),z)),V((r*cos(a1),.0038+r*sin(a1),z))];P.prism(lo,hi,3)
 M.add(P,'posterior_anal_pyramid','anal_pyramid','tegmen',dict(valve_count='nominal6, exact specimen valve count not established'))
 return M.emit('caryocrinites',m,col)

def mosaic(R,cz):
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=3,radius=1);bm.faces.ensure_lookup_table();chosen=[f for i,f in enumerate(list(bm.faces)) if i%2==0]
 for f in chosen:
  vs=list(f.verts);center=bm.verts.new(f.calc_center_median().normalized());bm.faces.remove(f)
  for k in range(3):bm.faces.new((vs[k],vs[(k+1)%3],center))
 bm.normal_update();p=Patch()
 for i,v in enumerate(bm.verts):
  c=v.co.normalized()
  if c.z>.965:continue
  u,n,a=frame(c);corners=[f.calc_center_median().normalized() for f in v.link_faces];corners.sort(key=lambda q:atan2((q-c).dot(n),(q-c).dot(u)));lo=[V((0,0,cz))+q*R*.992 for q in corners];hi=[V((0,0,cz))+(c+(q-c)*.94).normalized()*R*1.008 for q in corners];p.prism(lo,hi,3 if i%6==0 else 0)
 bm.free();return p

def echinosphaerites(cfg,m,col):
 p=cfg['parameters'];M=Mesh();stem=p['stem_length_m'];R=p['theca_diameter_m']/2;cz=stem+R;M.add(tube([(0,0,.0005),(0,0,stem+.001)],[p['stem_radius_m'],p['stem_radius_m']],8),'stem','stem');M.add(tube([(0,0,0),(0,0,.0006),(0,0,.001)],[.0022,.0025,.0008],10,3),'attachment_disk','attachment','stem')
 M.add(ellipsoid((0,0,cz),(R,R,R),32,16),'theca','theca','stem');M.add(mosaic(R,cz),'mosaic','mosaic','theca',dict(plate_count_is_nominal=True))
 top=cz+R;nr=p['oral_neck_radius_m'];neck=Patch();N=16;rings=[]
 for rx,ry,z in [(nr*1.5,nr*1.5*.67,top-.0014),(nr,nr*.67,top+p['oral_neck_height_m']),(p['oral_slit_length_m']/2,p['oral_slit_width_m']/2,top+p['oral_neck_height_m']),(p['oral_slit_length_m']*.39,p['oral_slit_width_m']*.34,top+.0003)]:rings.append([neck.vert((rx*cos(2*pi*k/N),ry*sin(2*pi*k/N),z)) for k in range(N)])
 for j in range(3):
  for k in range(N):q=(k+1)%N;neck.face([rings[j][k],rings[j][q],rings[j+1][q],rings[j+1][k]],0 if j<2 else 2)
 neck.face(list(reversed(rings[0])));neck.face(rings[-1],2);neck.solids=[list(range(len(neck.v)))];M.add(neck,'oral_neck','oral_neck','theca',dict(four_facets='RM Ec3304',surface_recess=True))
 for j,a in enumerate([-.45*pi,-.95*pi,.25*pi,.72*pi]):
  rad=V((cos(a),sin(a),0));start=V((cos(a)*nr*.85,sin(a)*nr*.67*.85,top+p['oral_neck_height_m']-.001));fork=start+rad*.005+V((0,0,.0075));tag='primary_brachiole_'+str(j);M.add(paired_axis([start,fork],p['brachiole_radius_m'],p['brachiole_plate_stations'],1),tag,'primary_brachiole','oral_neck')
  side=V((-sin(a),cos(a),0))
  for k in [-1,1]:end=fork+rad*.004+side*k*.0035+V((0,0,.007));M.add(paired_axis([fork-V((0,0,.00035)),end],p['brachiole_radius_m']*.65,p['brachiole_plate_stations'],1),tag+'_fork_'+str(k),'terminal_brachiole',tag,dict(genus_supported_interpretation=True))
 # Selected nominate form has five anal valves. Anatomical relation from primary Swedish specimens.
 normal=V((-.32,.76,.57)).normalized();c=V((0,0,cz))+normal*(R+.00012);u,n,a=frame(normal);r=p['anal_pyramid_radius_m'];P=Patch()
 for j in range(5):
  t0=2*pi*j/5+.025;t1=2*pi*(j+1)/5-.025;v0=u*cos(t0)+n*sin(t0);v1=u*cos(t1)+n*sin(t1);P.prism([c-normal*.0003,c+v0*r-normal*.0003,c+v1*r-normal*.0003],[c+normal*.0009,c+v0*r,c+v1*r],1)
 M.add(P,'anal_pyramid','anal_pyramid','theca',dict(valves=5));gn=V((.10,.55,.83)).normalized();gc=V((0,0,cz))+gn*(R+.00028);M.add(recess(gc,gn,p['gonopore_radius_m'],p['gonopore_radius_m'],.00035,3,8),'gonopore','gonopore','theca');return M.emit('echinosphaerites',m,col)

def cupressocrinites(cfg,m,col):
 p=cfg['parameters'];M=Mesh();column(M,.002,p['column_length_m'],p['column_radius_m'],p['columnals']);z0=.002+p['column_length_m']-.001;H=p['cup_height_m'];R=p['cup_radius_m'];M.add(tube([(0,0,z0-.001),(0,0,z0+.002),(0,0,z0+H)],[.002,.006,R*.96],20,0),'cup_core','cup','column')
 for kind,bz,tz,br,tr in [('basal',z0,z0+H*.50,.003,R*.73),('radial',z0+H*.45,z0+H,.008,R)]:
  for k in range(5):M.add(ring_plate((0,0,0),br,bz,tr,tz,2*pi*k/5+.01,2*pi*(k+1)/5-.01,3 if k%2 else 0),kind+'_'+str(k),kind+'_plate','cup_core')
 # Modest fused infrabasal pedestal, not five independent orals.
 M.add(tube([(0,0,z0-.0016),(0,0,z0+.0004)],[.003,.004],10,3),'fused_pedestal','infrabasal_pedestal','cup_core')
 N=p['brachials_per_arm'];L=p['arm_length_m'];step=L/N
 # Cross section traces a broad rounded-W profile. Adoral side positive y.
 cross=[(-.5,-.40),(.5,-.40),(.50,.05),(.33,.50),(.15,.22),(0,.42),(-.15,.22),(-.33,.50),(-.5,.05)]
 for arm in range(5):
  angle=-pi/2+2*pi*arm/5;rad=V((cos(angle),sin(angle),0));tan=V((-sin(angle),cos(angle),0));P=Patch();armbase=rad*(R*.82)+V((0,0,z0+H-.0003))
  def pos(t):return armbase+rad*(.008*t*t)+V((0,0,L*t))
  for j in range(N):
   t=(j+.5)/N;c=pos(t);axis=(pos(min(1,t+.001))-pos(max(0,t-.001))).normalized();u,n,a=frame(axis,-rad);taper=1-.66*t;w=p['brachial_base_width_m']*taper;d=p['brachial_base_depth_m']*taper
   lo=[c+u*x*w+n*y*d-a*step*.55 for x,y in cross];hi=[c+u*x*w+n*y*d+a*step*.55 for x,y in cross];Q=Patch();Q.prism(lo,hi,3 if j%4==0 else 0);P.merge(Q)
   if j==0:continue
   for side in [-1,1]:
    root=c+u*side*w*.31+n*d*.25;length=p['pinnule_length_m']*(1-.50*t);pts=[]
    for k in range(p['pinnule_segments']+1):
     f=k/p['pinnule_segments'];curl=(1.60*pi if j%3 else .75*pi)*f;pts.append(root+u*side*length*.45*sin(curl)+n*length*.45*(1-cos(curl))+a*length*.10*f)
    Q=Patch()
    for k in range(p['pinnule_segments']):
     a0=pts[k]-(n*d*.22 if k==0 else V());b=pts[k+1];vv=b-a0;Q.merge(block((a0+b)/2,vv,axis,p['pinnule_radius_m']*2*(1-.45*k/4),p['pinnule_radius_m']*2*(1-.45*k/4),vv.length*1.12,1,True))
    M.add(Q,f'arm{arm}_pinnule{j}_{side}','pinnule',f'arm{arm}',dict(ossicles=p['pinnule_segments'],bilateral_series=side,posture='inward curled or partly unrolled'))
  M.add(P,f'arm{arm}','W_brachial_arm','cup_core',dict(brachials=N,first_nonpinnulate=True))
 ac=V((0,.0035,z0+H-.0004));P=Patch();segs=5
 for j in range(segs):
  zz=p['anal_sac_length_m']*j/segs;P.merge(tube([ac+V((0,0,zz-.00018)),ac+V((0,0,zz+p['anal_sac_length_m']/segs+.00018))],[p['anal_sac_radius_m']*(1-.2*j/segs)]*2,8,3 if j%2 else 0))
 M.add(P,'anal_sac','anal_sac','cup_core',dict(offcenter_CD_interray=True,distal_height_nominal=True));M.add(recess(ac+V((0,0,p['anal_sac_length_m']+.0002)),(0,0,1),.0008,.0008,.0004,3,8),'anal_sac_aperture','anal_aperture','anal_sac');return M.emit('cupressocrinites',m,col)

def micraster(cfg,m,col):
 p=cfg['parameters'];M=Mesh();W=p['test_width_m'];L=p['test_length_m'];H=p['test_height_m'];yc=.002;petals=[-pi/2-.64,-pi/2+.64,pi/2-.72,pi/2+.72];PL=p['petal_length_m']
 def radius(a):
  r=1/sqrt((cos(a)/(W/2))**2+(sin(a)/(L/2))**2)
  return r*(1-.15*exp(-((a+pi/2)/.19)**2))
 def xy(t,a):return V((radius(a)*t*cos(a),yc+radius(a)*t*sin(a),0))
 def zh(x,y):
  a=atan2(y-yc,x);r=sqrt(x*x+(y-yc)**2);t=min(.999999,r/radius(a));z=.003+(H-.003)*sqrt(max(0,1-t*t))
  # Actual local surface depressions, not raised painted petals.
  if y<yc+.001:z-=p['anterior_groove_depth_m']*exp(-(x/.0014)**2)*min(1,(yc+.001-y)/.005)
  for angle in petals:
   v=V((cos(angle),sin(angle),0));q=V((x,y-yc,0));s=q.dot(v);d=abs(q.x*v.y-q.y*v.x)
   if .001<s<PL:
    edge=sin(pi*(s-.001)/(PL-.001))**.30;z-=edge*(p['petal_depth_m']*exp(-(d/.00046)**2)+.00035*exp(-(d/.0015)**4))
  return z
 def normal(x,y):
  e=.00003;return V((-(zh(x+e,y)-zh(x-e,y))/(2*e),-(zh(x,y+e)-zh(x,y-e))/(2*e),1)).normalized()
 P=Patch();N=72;NR=22;P.vert((0,yc,zh(0,yc)))
 rings=[]
 for j in range(1,NR+1):
  t=j/NR;ring=[]
  for k in range(N):a=-pi+2*pi*k/N;q=xy(t,a);ring.append(P.vert((q.x,q.y,zh(q.x,q.y))))
  rings.append(ring)
 for k in range(N):P.face([0,rings[0][k],rings[0][(k+1)%N]])
 for j in range(NR-1):
  for k in range(N):q=(k+1)%N;P.face([rings[j][k],rings[j+1][k],rings[j+1][q],rings[j][q]])
 prev=rings[-1]
 for j in range(1,6):
  t=1-j/6;ring=[]
  for k in range(N):a=-pi+2*pi*k/N;q=xy(t,a);z=.003-.003*sqrt(1-t*t);ring.append(P.vert((q.x,q.y,z)))
  for k in range(N):q=(k+1)%N;P.face([prev[k],ring[k],ring[q],prev[q]])
  prev=ring
 b=P.vert((0,yc,0))
 for k in range(N):P.face([prev[k],b,prev[(k+1)%N]])
 P.solids=[list(range(len(P.v)))];M.add(P,'test','test',details=dict(paired_petals=4,unpaired_anterior_ambulacrum=1,actual_depressions=True))
 test_tree=BVHTree.FromPolygons([V(q) for q in M.v],M.f,all_triangles=False)
 # Real pore rims and recessed cavities, seated above depressed host surface so the host cannot plug them.
 P=Patch();feet=[]
 for g,a in enumerate(petals):
  ray=V((cos(a),sin(a),0));side=V((-sin(a),cos(a),0))
  for j in range(p['pore_pairs_per_petal']):
   s=.003+(PL-.004)*j/(p['pore_pairs_per_petal']-1)
   for k in [-1,1]:
    q=ray*s+side*k*p['petal_width_m']*.37+V((0,yc,0));z=zh(q.x,q.y);n=normal(q.x,q.y);c=V((q.x,q.y,z))+n*.00021;P.merge(recess(c,n,.00020,.00016,.00023,1,6))
    if j in [1,4] and len(feet)<p['tube_foot_sample_count']:feet.append((c,n))
 M.add(P,'petal_pore_pairs','pore_pairs','test',dict(pore_pairs_per_petal=p['pore_pairs_per_petal'],nominal_sample=True))
 F=Patch()
 for c,n in feet:F.merge(tube([c-n*.00023,c+n*.00035,c+n*p['tube_foot_length_m']+V((.0002,0,0))],[.00010,.00009,.00007],4,1))
 M.add(F,'tube_feet','tube_feet','petal_pore_pairs',dict(sample_count=len(feet),softparts_inferred=True))
 # Fine spines arise from actual tubercle volumes, kept off the diagnostic petal channels.
 P=Patch();B=Patch();count=0;i=0;rng=random.Random(cfg['seed']+19)
 while count<p['spine_sample_count']:
  i+=1;a=rng.uniform(-pi,pi);t=sqrt(rng.random())*.96;q=xy(t,a)
  if q.y<yc and abs(q.x)<.0018:continue
  if any(.001<V((q.x,q.y-yc,0)).dot(V((cos(b),sin(b),0)))<PL and abs(q.x*sin(b)-(q.y-yc)*cos(b))<.0018 for b in petals):continue
  under=count>=int(p['spine_sample_count']*.8)
  if under:
   if abs(q.x)<.004 and -.019<q.y<-.009:continue
   z=.003-.003*sqrt(1-t*t);n=V((q.x*.3,q.y*.3,-1)).normalized()
  else:z=zh(q.x,q.y);n=normal(q.x,q.y)
  hit,hn,fi,hd=test_tree.ray_cast(V((q.x,q.y,-H if under else H*2)),V((0,0,1 if under else -1)),H*4)
  if hit is None:continue
  c=hit;n=hn;B.merge(ellipsoid(c,(.00033,.00033,.00028),4,2,3));direction=(n+V((0,-.23,0))).normalized();length=p['spine_length_m']*(.7+.3*((i*17)%11)/10);P.merge(tube([c-n*.00010,c+direction*length],[p['spine_radius_m'],.000025],4,1));count+=1
 M.add(B,'tubercles','tubercles','test');M.add(P,'spines','spines','tubercles',dict(nominal_sample_count=count,orientation_inferred=True))
 # Anterior ventral mouth modeled as recessed cavity with labral overhang, not a central rosette.
 mc=V((0,-.0154,.0002));M.add(recess(mc,(0,0,-1),p['peristome_width_m']/2,.0010,p['peristome_depth_m']*.45,1,12),'peristome','peristome','test',dict(anterior=True,opening_visible_obliquely=True))
 lab=Patch();outline=[(-.0025,-.0174),(.0025,-.0174),(.0035,-.0162),(.0033,-.0102),(0,-.0096),(-.0033,-.0102),(-.0035,-.0162)];lo=[V((x,y,.0010 if y>-.012 else -.0006)) for x,y in outline];hi=[V((x,y,-.00055 if y>-.012 else -.00115)) for x,y in outline];lab.prism(lo,hi,3);M.add(lab,'labrum','labrum','test',dict(overhangs_anterior_peristome=True,curved_spatulate_outline=True))
 # Posterior periproct sits high on posterior face; an oval subanal fasciole remains below.
 an=pi/2;yy=yc+radius(an)*.92;z=zh(0,yy);n=normal(0,yy);ac=V((0,yy,z))+n*.00045;M.add(recess(ac,n,p['periproct_radius_m'],p['periproct_radius_m']*.85,.00055,1,10),'periproct','periproct','test')
 F=Patch();C=[]
 for j in range(33):
  a=2*pi*j/32;x=.007*cos(a);zz=.0045+.0016*sin(a);hit,hn,fi,hd=test_tree.ray_cast(V((x,L,zz)),V((0,-1,0)),L*2);assert hit is not None;C.append(hit+V((0,.00008,0)))
 # The fine bristled band is a closed loop around subanal field, not another anus.
 for j in range(32):
  c=(C[j]+C[j+1])/2;a=C[j+1]-C[j];F.merge(block(c,a,(0,1,0),p['subanal_fasciole_width_m'],.0003,a.length*1.12,3));F.merge(tube([c-V((0,.0002,0)),c+V((0,.00065,0))],[.00012,.00003],4,1))
 M.add(F,'subanal_fasciole','subanal_fasciole','test',dict(below_periproct=True,short_bristle_band=True));return M.emit('micraster',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);ap.add_argument('--rebuild-only',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();aid=cfg['asset_id'];col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),c) for i,c in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'animals',col,metadata=dict(representation='living-reconstruction',export_texcoords=False,source_scope='Original batch109 freeze; dimensions and sampling artistic; no third-party source meshes/pixels incorporated.'),output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30,rebuild_only=a.rebuild_only)
 (out/'execution.json').write_text(json.dumps(dict(pid=os.getpid(),parent_pid=os.getppid(),argv=sys.argv,started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),blender_version=bpy.app.version_string,generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),config_sha256=hashlib.sha256(Path(a.config).read_bytes()).hexdigest()),indent=2)+'\n')
if __name__=='__main__':main()
