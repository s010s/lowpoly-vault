#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch103 geometry authored after the complete original freeze. No mesh/image inputs."""
import argparse,datetime,hashlib,json,math,os,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from math import sin,cos,pi
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset

def axes(d,n=(0,0,1)):
 a=Vector(d).normalized();n=Vector(n)
 if abs(a.dot(n.normalized()))>.98:n=Vector((0,1,0))
 w=n.cross(a).normalized();t=a.cross(w).normalized();return a,w,t
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.components=[]
 def add(self,v,f,mat,tag,kind,d=(0,1,0),n=(0,0,1),parent=None,base=None,design=None):
  off=len(self.v);a,w,t=axes(d,n);self.v.extend(Vector(x) for x in v);self.f.extend(tuple(off+i for i in x) for x in f);self.mi.extend([mat]*len(f));self.components.append({'tag':tag,'kind':kind,'vertices':list(range(off,off+len(v))),'axes':[list(a),list(w),list(t)],'parent':parent,'base_vertices':[off+i for i in (base or [])],'design':design or {}})
 def emit(self,aid,materials,col):
  lo=[min(v[k] for v in self.v) for k in range(3)];hi=[max(v[k] for v in self.v) for k in range(3)];off=Vector((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]));self.v=[v+off for v in self.v];o=mesh_object(aid+'-labeled-solids',self.v,self.f,materials,col)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i
  for c in self.components:o.vertex_groups.new(name=c['tag']).add(c['vertices'],1,'REPLACE')
  ct={'schema_version':1,'object_name':o.name,'translation':list(off),'components':self.components};txt=bpy.data.texts.new('BATCH103_COMPONENT_CONTRACT.json');txt.write(json.dumps(ct,sort_keys=True));o['component_contract']='BATCH103_COMPONENT_CONTRACT.json';o['editing']='Named semantic vertex groups; independent closed component solids; meters.';return o

def tube(M,pts,rs,mat,tag,kind,parent=None,sides=6):
 pts=[Vector(p) for p in pts];v=[]
 for i,p in enumerate(pts):
  a,w,t=axes(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)])
  for j in range(sides):v.append(p+rs[i]*(w*cos(2*pi*j/sides)+t*sin(2*pi*j/sides)))
 v.extend([pts[0],pts[-1]]);N=len(pts)*sides;f=[(N,(j+1)%sides,j) for j in range(sides)]
 for i in range(len(pts)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 for j in range(sides):f.append((N+1,N-sides+j,N-sides+(j+1)%sides))
 M.add(v,f,mat,tag,kind,pts[-1]-pts[0],parent=parent,base=list(range(sides))+[N],design={'centerline_length_m':sum((a-b).length for a,b in zip(pts,pts[1:])),'longitudinal_intervals':len(pts)-1})

def ell(M,c,dim,mat,tag,kind,parent=None,sides=10,rings=4):
 c=Vector(c);rx,ry,rz=[x/2 for x in dim];v=[c+Vector((0,-ry,0))]
 for k in range(1,rings):
  a=pi*k/rings
  for j in range(sides):b=2*pi*j/sides;v.append(c+Vector((rx*sin(a)*cos(b),-ry*cos(a),rz*sin(a)*sin(b))))
 v.append(c+Vector((0,ry,0)));N=len(v);f=[(0,1+(j+1)%sides,1+j) for j in range(sides)]
 for k in range(rings-2):
  for j in range(sides):a=1+k*sides+j;b=1+k*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 st=1+(rings-2)*sides
 for j in range(sides):f.append((N-1,st+j,st+(j+1)%sides))
 M.add(v,f,mat,tag,kind,parent=parent,base=list(range(N)),design={'nominal_dimensions_m':dim})

def prism(M,xy,z,T,mat,tag,kind,parent=None):
 # Explicit triangulated polygon, two closed skins and boundary walls. xy points need not be convex.
 poly=[Vector((x,y,0)) for x,y in xy];lookup={tuple(v):i for i,v in enumerate(poly)};ts=[tuple(i if isinstance(i,int) else lookup[tuple(i)] for i in tri) for tri in tessellate_polygon([poly])];N=len(xy);v=[(x,y,z+zz) for zz in [-T/2,T/2] for x,y in xy];f=ts+[tuple(i+N for i in reversed(t)) for t in ts]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)];M.add(v,f,mat,tag,kind,parent=parent,base=list(range(2*N)),design={'nominal_thickness_m':T})

def paddle(M,b,d,L,W,T,mat,tag,kind,parent):
 b=Vector(b);a,w,t=axes(d);out=[(0,0),(-W*.38,L*.25),(-W*.5,L*.65),(-W*.28,L*.95),(0,L),(W*.28,L*.95),(W*.5,L*.65),(W*.38,L*.25)];N=len(out);v=[b+a*y+w*x for x,y in out];v.extend([b+a*L*.53+t*T/2,b+a*L*.53-t*T/2]);f=[]
 for i in range(N):j=(i+1)%N;f.extend([(N,i,j),(N+1,j,i)])
 M.add(v,f,mat,tag,kind,d,parent=parent,base=[0],design={'nominal_length_m':L,'nominal_width_m':W,'nominal_thickness_m':T})

def spine(M,b,d,L,r,mat,tag,kind,parent):
 b=Vector(b);a,w,t=axes(d);N=5;v=[]
 for y,rr in [(0,r),(L*.65,r*.46)]:
  for j in range(N):q=2*pi*j/N;v.append(b+a*y+rr*(w*cos(q)+t*sin(q)))
 v.extend([b+a*L,b]);f=[(2*N+1,(j+1)%N,j) for j in range(N)]
 for j in range(N):k=(j+1)%N;f.extend([(j,k,k+N,j+N),(2*N,j+N,k+N)])
 M.add(v,f,mat,tag,kind,d,parent=parent,base=list(range(N))+[2*N+1],design={'nominal_length_m':L,'single_vertex_tip':True})

def leg(M,base,sign,L,tag,parent,mat=2,kind='walking_leg'):
 b=Vector(base);pts=[b,b+Vector((sign*L*.32,L*.08,-L*.10)),b+Vector((sign*L*.64,L*.19,-L*.42)),b+Vector((sign*L*.53,L*.32,-L*.87))];tube(M,pts,[L*.10,L*.08,L*.06,L*.025],mat,tag,kind,parent)
 return pts

def biramous(M,base,sign,L,tag,parent,mat=2,head=False):
 pts=leg(M,base,sign,L,tag+'_endopod',parent,mat,'head_walking_leg' if head else 'walking_leg');b=Vector(base)+Vector((sign*L*.19,L*.08,-L*.04));d=Vector((sign*.8,.55,-.25));paddle(M,b,d,L*.75,L*.27,L*.085,1,tag+'_exopod','head_exopod' if head else 'thoracic_exopod',tag+'_endopod')
 for j in range(3):
  p=b+d.normalized()*(L*(.23+j*.15))+Vector((sign*L*.08,0,0));spine(M,p,(sign*.6,.8,-.1),L*.20,L*.015,3,f'{tag}_fringe{j}','exopod_fringe',tag+'_exopod')

def habelia(c,m,col):
 M=Mesh();p=c['parameters'];z=p['body_center_z_m'];H=p['head_length_m'];T=p['trunk_length_m'];step=T/12
 ell(M,(0,-H/2,z),[p['head_width_m'],H,.0026],0,'head_shield','head_shield')
 for s in [-1,1]:
  ell(M,(s*.002,-.00265,z+.00035),[.00085,.00075,.00075],4,f'eye{s}','lateral_eye','head_shield',sides=8)
 for i in range(18):
  ang=i*2.399;r=.0015*math.sqrt((i+.5)/18);x=r*cos(ang);y=-H/2+r*.7*sin(ang);zz=z+.00115*math.sqrt(max(.1,1-(x/.0025)**2-((y+H/2)/.002)**2));ell(M,(x,y,zz),[.00035,.00038,.00038],1,f'tubercle{i}','head_tubercle','head_shield',sides=6,rings=3)
 prev='head_shield'
 for i in range(12):
  y=(i+.5)*step-.00015;width=.0045*(1-.055*i);tag=f'tergite{i+1:02d}';ell(M,(0,y,z),[width,step*1.3,.00245*(1-.035*i)],0 if i%2==0 else 1,tag,'trunk_tergite',prev,sides=10);prev=tag
  for s in [-1,1]:
   spine(M,(s*width*.24,y,z+.00080*(1-.035*i)),(s*.08,.33,1),.0018*(1-.055*i),.00030,2,f'dorsal{i}_{s}','dorsal_spine',tag)
   spine(M,(s*width*.40,y+.00010,z-.00015),(s*.75,.65,-.13),.0014*(1-.045*i),.00020,1,f'pleural{i}_{s}','pleural_spine',tag)
   b=(s*width*.19,y-.00016,z-.00060*(1-.035*i))
   if i<5:biramous(M,b,s,.0038+i*.00013,f'thoracic{i}_{s}',tag)
   else:paddle(M,b,(s*.75,.35,-.8),.00225*(1-.06*(i-5)),.0011*(1-.06*(i-5)),.00025,3,f'posterior_exopod{i}_{s}','posterior_exopod',tag)
 # Five pairs of differentiated gnathobases and forward endopods; sensory exopods fan laterally.
 for i in range(5):
  for s in [-1,1]:
   y=-.0034+i*.00063;b=(s*(.00060+i*.00012),y,z-.00095);gt=f'gnathobase{i}_{s}';ell(M,b,[.00125,.00095,.0007],2,gt,'gnathobase','head_shield',sides=8,rings=3)
   x=s*(.0012+i*.00055);pts=[Vector(b),Vector((x,y-.0011,z-.0011)),Vector((x*1.12,-.0065-i*.00030,z-.0019)),Vector((x*.88,-.0072-i*.0003,z-.00145))];tube(M,pts,[.00028,.00025,.00018,.000055],2,f'raptorial{i}_{s}','cephalic_raptorial',gt)
   # Minute endites are artistic samples, not an assertion of full setation.
   for k in range(2):
    q=pts[1].lerp(pts[2],.35+k*.35);spine(M,q,(-s*.8,-.3,.2),.0007,.000085,3,f'endite{i}_{s}_{k}','raptorial_endite',f'raptorial{i}_{s}')
   a=(s*(.00070 if i==0 else .00135),y+.00010,z-.00010);tube(M,[a,(s*(.003+i*.00035),y-.0013,z+.0001),(s*(.0038+i*.0004),-.0052+i*.0005,z+.0004)],[.00015,.00010,.000025],3,f'sensory_exopod{i}_{s}','cephalic_exopod','head_shield',sides=5)
 for s in [-1,1]:
  tube(M,[(s*.00035,-.00315,z-.00035),(s*.00050,-.0045,z-.00095),(s*.00025,-.0049,z-.0009)],[.00016,.00012,.00004],2,f'reduced{s}','reduced_anterior_appendage','head_shield',sides=5)
  biramous(M,(s*.001,-.00040,z-.0009),s,.0036,f'intermediary{s}','head_shield',head=True)
 start=Vector((0,T-.00055,z));L=p['telson_proximal_length_m'];joint=start+Vector((0,L,.00045));tube(M,[start,start+Vector((0,.0015,0)),start+Vector((0,L*.65,-.0001)),joint],[.00065,.00040,.00022,.00014],0,'telson_proximal','telson_proximal','tergite12',sides=8)
 end=joint+Vector((0,p['telson_distal_length_m'],.00005));tube(M,[joint-Vector((0,.00010,0)),end],[.00016,.000035],1,'telson_distal','telson_distal','telson_proximal',sides=6)
 for j in range(8):
  for s in [-1,1]:
   u=.08+j*.10
   if u<=.0015/L:q=start.lerp(start+Vector((0,.0015,0)),u/(.0015/L));r=.00065+(.00040-.00065)*u/(.0015/L)
   elif u<=.65:q=(start+Vector((0,.0015,0))).lerp(start+Vector((0,L*.65,-.0001)),(u-.0015/L)/(.65-.0015/L));r=.00040+(.00022-.00040)*(u-.0015/L)/(.65-.0015/L)
   else:q=(start+Vector((0,L*.65,-.0001))).lerp(joint,(u-.65)/.35);r=.00022+(.00014-.00022)*(u-.65)/.35
   q.x=s*r*.65;spine(M,q,(s*.7,.7,0),.00058*(1-u*.65),.00009,2,f'telson_spine{j}_{s}','telson_spine','telson_proximal')
 return M.emit('habelia',m,col)

def alalcomenaeus(c,m,col):
 M=Mesh();p=c['parameters'];z=p['body_center_z_m'];H=p['head_length_m'];T=p['trunk_length_m'];step=T/11
 ell(M,(0,-H/2,z),[p['head_width_m'],H,.0045],0,'head_shield','head_shield')
 prev='head_shield'
 for i in range(11):
  y=(i+.5)*step-.00025;w=.009*(1-.047*i);tag=f'tergite{i+1:02d}';ell(M,(0,y,z),[w,step*1.28,.0044*(1-.03*i)],0 if i%2==0 else 1,tag,'trunk_tergite',prev);prev=tag
  for s in [-1,1]:
   # Closed overlapping armor with downward flanks, not floating scalloped decorations.
   paddle(M,(s*w*.30,y-.00025,z+.00015),(s*.45,.25,-.8),.0029*(1-.025*i),step*.95,.00055,0,f'pleura{i}_{s}','enclosing_pleura',tag)
   tube(M,[(s*w*.19,y-step*.38,z+.00130*(1-.03*i)),(s*w*.19,y,z+.00202*(1-.03*i)),(s*w*.19,y+step*.41,z+.00125*(1-.03*i))],[.00023,.00023,.00021],2,f'carina{i}_{s}','dorsal_carina',tag,sides=5)
   biramous(M,(s*w*.17,y-.00015,z-.0014),s,.0050*(1-.025*i),f'trunk_limb{i}_{s}',tag)
 for s in [-1,1]:
  for i in range(2):biramous(M,(s*.002,-.0032+i*.0018,z-.0015),s,.0048,f'head_limb{i}_{s}','head_shield',head=True)
  tube(M,[(s*.0029,-.0054,z+.0004),(s*.0052,-.0062,z+.0011)],[.00048,.00036],2,f'eye_stalk{s}','eye_stalk','head_shield')
  ell(M,(s*.0053,-.00625,z+.0012),[.0016,.0015,.0015],4,f'lateral_eye{s}','lateral_eye',f'eye_stalk{s}',sides=10)
  tube(M,[(s*.0011,-.0051,z+.0015),(s*.0011,-.00535,z+.0027)],[.00028,.00020],2,f'median_stalk{s}','median_eye_stalk','head_shield')
  ell(M,(s*.0011,-.00535,z+.0026),[.00095,.00085,.00055],4,f'median_eye{s}','median_eye',f'median_stalk{s}',sides=8)
  b=Vector((s*.0025,-.0055,z-.0002));joint=Vector((s*.0034,-.009,z-.00005));tube(M,[b,b.lerp(joint,.55),joint],[.00065,.00072,.00048],0,f'great_base{s}','great_appendage_peduncle','head_shield',sides=8)
  for j in range(3):
   q=joint+Vector((s*(j-1)*.00025,.00020,(j-1)*.00015));tip=q+Vector((s*(j-1)*.0011,-.0032,-.0007));tube(M,[q,q.lerp(tip,.50)+Vector((0,0,.00055)),tip],[.00031,.00025,.000075],2,f'great_claw{s}_{j}','great_appendage_claw',f'great_base{s}')
   tube(M,[tip+Vector((0,.00009,0)),tip+Vector((s*.0007,-.0029,.0001)),tip+Vector((s*.0017,-.0057,.00065))],[.00010,.000065,.00002],3,f'flagellum{s}_{j}','great_appendage_flagellum',f'great_claw{s}_{j}',sides=5)
 # A single spatula with a narrow neck and broad rounded distal edge.
 y=T-.0008;L=p['telson_length_m'];W=p['telson_width_m'];outline=[(-.0012,y),(-W*.42,y+L*.36),(-W*.50,y+L*.76),(-W*.35,y+L),(.0,y+L*1.04),(W*.35,y+L),(W*.50,y+L*.76),(W*.42,y+L*.36),(.0012,y)];prism(M,outline,z-.0003,.0007,0,'spatulate_telson','spatulate_telson','tergite11')
 for j in range(9):
  x=(j-4)*W*.082;b=(x,y+L*(.98-.11*abs(j-4)/4),z-.0003);paddle(M,b,((j-4)*.13,1,0),.0031,.00048,.00018,2,f'tail_fringe{j}','telson_spine','spatulate_telson')
 return M.emit('alalcomenaeus',m,col)

def plenocaris(c,m,col):
 M=Mesh();p=c['parameters'];z=p['body_center_z_m'];C=p['carapace_length_m'];T=p['abdomen_length_m'];step=T/13
 ell(M,(0,-C*.45,z),[.0017,C*1.07,.0015],2,'cephalothorax','cephalothorax')
 for s in [-1,1]:
  ell(M,(s*.00060,-C*.45,z+.00025),[.00165,C,.0021],0 if s<0 else 1,f'carapace{s}','carapace_valve','cephalothorax',sides=10)
  ell(M,(s*.00058,-C*.84,z+.00034),[.00045,.00050,.00045],4,f'eye{s}','lateral_eye','cephalothorax',sides=8,rings=3)
  pts=[]
  for j in range(11):pts.append(Vector((s*(.00052+j*.00018),-C*.85-j*.00028,z+.00012-.000024*j)))
  tube(M,pts,[.00016*(1-j*.06) for j in range(11)],1,f'antenna{s}','antenna','cephalothorax',sides=6)
  for j in range(10):q=pts[j].lerp(pts[j+1],.55);spine(M,q,(s*.25,-.15,-1),.00022,.000044,2,f'antenna_spine{s}_{j}','antenna_spine',f'antenna{s}')
  for j in range(3):leg(M,(s*.00040,-C*.65+j*.00060,z-.00030),s,.00155,f'anterior_leg{s}_{j}','cephalothorax',2,'anterior_leg')
 prev='cephalothorax'
 for j in range(13):
  y=step*(j+.5)-.00012;w=.00195*(1-.040*j);tag=f'abdomen{j+1:02d}';ell(M,(0,y,z-.00003*j),[w,step*1.30,.00140*(1-.035*j)],0 if j%2==0 else 1,tag,'abdominal_segment',prev,sides=10);prev=tag
 for s in [-1,1]:paddle(M,(s*.00030,T-.00033,z-.00035),(s*.43,1,-.08),p['caudal_ramulus_length_m'],p['caudal_ramulus_width_m'],.00020,0 if s<0 else 1,f'caudal_ramulus{s}','caudal_ramulus','abdomen13')
 return M.emit('plenocaris',m,col)

def nectocaris(c,m,col):
 M=Mesh();p=c['parameters'];z=p['body_center_z_m'];L=p['trunk_length_m'];W=p['trunk_width_m'];D=p['trunk_thickness_m']
 # Continuous shallow spindle with broad anterior shoulders and a tapered, undivided rear.
 ys=[-.0009,0,.004,.010,.018,.027,L];widths=[.0021,.0031,.0048,.005,.0041,.0023,.00007];hs=[.0011,.0016,.002,.0019,.0015,.0008,.00004];v=[];sides=12
 for y,r,h in zip(ys,widths,hs):
  for j in range(sides):a=2*pi*j/sides;v.append((r*cos(a),y,z+h*sin(a)))
 N=len(v);v.extend([(0,ys[0],z),(0,ys[-1],z)]);f=[(N,(j+1)%sides,j) for j in range(sides)]
 for k in range(len(ys)-1):
  for j in range(sides):a=k*sides+j;b=k*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 for j in range(sides):f.append((N+1,N-sides+j,N-sides+(j+1)%sides))
 M.add(v,f,0,'trunk','trunk',base=[],design={'nominal_length_m':L})
 ell(M,(0,-.0025,z),[.0044,.006,.0024],0,'head','head','trunk',sides=10)
 # Fin top/bottom connected sheets with transverse low ridges; ray count is an art sample.
 for s in [-1,1]:
  n=p['ray_count_per_fin'];v=[];stations=[]
  for i in range(2*n+1):
   u=i/(2*n);y=.0002+u*(L-.0003);q=sin(pi*u)**.8;inner=.00004+.0031*q;outer=inner+(.00015+.0059*q);stations.append((y,inner,outer))
  for layer in [-1,1]:
   for i,(y,inner,outer) in enumerate(stations):
    ridge=.00012 if i%2 else 0
    for j in range(3):x=inner+(outer-inner)*j/2;v.append((s*x,y,z+layer*(.00017+ridge*(1 if j==1 else .45))))
  K=len(stations)*3;f=[]
  for k in range(2):
   for i in range(len(stations)-1):
    for j in range(2):a=k*K+i*3+j;f.append((a,a+1,a+4,a+3))
  edge=[0,1,2]+[i*3+2 for i in range(1,len(stations))]+[K-2,K-3]+[i*3 for i in range(len(stations)-2,0,-1)]
  for j,a in enumerate(edge):b=edge[(j+1)%len(edge)];f.append((a,b,b+K,a+K))
  M.add(v,f,1,f'fin{s}','lateral_fin',parent='trunk',base=[i*3 for i in range(len(stations))]+[K+i*3 for i in range(len(stations))],design={'transverse_relief_ridges':n,'nominal_span_m':p['fin_span_m'],'closed_thickened_fin':True})
 for s in [-1,1]:
  tube(M,[(s*.0016,-.0030,z+.0002),(s*.0034,-.0033,z+.0004)],[.00045,.00032],0,f'eye_stalk{s}','eye_stalk','head')
  ell(M,(s*.0036,-.00335,z+.0004),[.0015,.00165,.0015],4,f'eye{s}','lateral_eye',f'eye_stalk{s}',sides=10)
  b=Vector((s*.00125,-.0044,z+.0001));pts=[b,b+Vector((s*.0010,-.005,-.0001)),b+Vector((s*.0022,-.010,.00005)),b+Vector((s*.0042,-.0165,.0006))];tube(M,pts,[.00030,.00021,.00013,.000025],3,f'antenna{s}','antenna','head',sides=6)
 # A closed cup-shaped tube wall: open lumen but not open mesh. Base embedded in head.
 N=12;start=Vector((0,-.0040,z-.00060));length=p['mouth_length_m'];a,w,t=axes((0,-1,-.05));v=[]
 for longitudinal,r in [(0,.00065),(length,.0011),(length,.00078),(.00055,.00030)]:
  for j in range(N):q=2*pi*j/N;v.append(start+a*longitudinal+r*(w*cos(q)+t*sin(q)))
 v.append(start+a*.00055);v.append(start);f=[]
 for k in range(3):
  for j in range(N):a0=k*N+j;b=k*N+(j+1)%N;f.append((a0,b,b+N,a0+N))
 for j in range(N):f.extend([(4*N,3*N+j,3*N+(j+1)%N),(4*N+1,(j+1)%N,j)])
 M.add(v,f,2,'flared_mouth','flared_tubular_mouth',(0,-1,-.05),parent='head',base=list(range(N))+[4*N+1],design={'aperture_diameter_m':.0022,'lumen_recess_depth_m':length-.00055,'interpretation':'External tubular mouth, internal jaws deliberately not exposed.'})
 return M.emit('nectocaris',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'animals',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Original batch103 pregeometry freeze; primary pixels and third-party meshes not incorporated.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':start,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
