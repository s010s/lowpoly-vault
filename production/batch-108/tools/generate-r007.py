#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c)2026 Leon Made This / s010s
"""Original batch108 geometry authored after04:59:08UTC verified immutable freeze.
Reusable primitive helpers adapted from local MIT batch107; all taxon geometry newly authored.
No reference image, mesh, tracing, network or external model is input.
"""
import argparse,datetime,hashlib,json,math,os,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from math import pi,sin,cos,sqrt,atan2
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Patch:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.base=[];self.solids=[]
 def vert(self,p):self.v.append(tuple(float(x) for x in p));return len(self.v)-1
 def face(self,ids,mat=0):self.f.append(tuple(ids));self.mi.append(mat)
 def prism(self,lower,upper,mat=0):
  n=len(lower);centroid=sum((Vector(v) for v in lower),Vector())/n;lower=[tuple(centroid+(Vector(v)-centroid)*.985) for v in lower];o=len(self.v);self.v.extend(tuple(p) for p in lower+upper);self.base.extend(range(o,o+n));self.face(list(range(o+n-1,o-1,-1)),mat)
  self.face(list(range(o+n,o+2*n)),mat)
  for i in range(n):j=(i+1)%n;self.face([o+i,o+j,o+n+j,o+n+i],mat)
  self.solids.append(list(range(o,o+2*n)))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.components=[];self.features=[]
 def add(self,P,tag,kind,parent=None,design=None,axis=(0,1,0)):
  off=len(self.v);self.v+=P.v;self.f+=[tuple(off+i for i in f) for f in P.f];self.mi+=P.mi
  a=Vector(axis).normalized();ref=Vector((0,0,1)) if abs(a.z)<.9 else Vector((0,1,0));w=ref.cross(a).normalized();t=a.cross(w).normalized()
  self.components.append(dict(tag=tag,kind=kind,vertices=list(range(off,off+len(P.v))),axes=[list(a),list(w),list(t)],parent=parent,base_vertices=[off+i for i in (P.base or list(range(len(P.v))))],design=design or {}))
  for j,ids in enumerate(P.solids):self.features.append(dict(tag=tag+'_plate_'+str(j),kind='geometric_plate',component=tag,vertices=[off+i for i in ids],side=None))
 def emit(self,aid,m,col):
  lo=[min(v[k] for v in self.v) for k in range(3)];hi=[max(v[k] for v in self.v) for k in range(3)];off=Vector((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]));obj=mesh_object(aid+'-original-organism',[Vector(v)+off for v in self.v],self.f,m,col)
  for f,mi in zip(obj.data.polygons,self.mi):f.material_index=mi
  for c in self.components:obj.vertex_groups.new(name=c['tag']).add(c['vertices'],1,'REPLACE')
  contract=dict(schema_version=1,object_name=obj.name,translation=list(off),components=self.components,integrated_features=self.features)
  bpy.data.texts.new('BATCH108_COMPONENT_CONTRACT.json').write(json.dumps(contract,sort_keys=True));obj['component_contract']='BATCH108_COMPONENT_CONTRACT.json';obj['editing']='Original closed component solids with editable semantic vertex groups. Plate seams and segmentation are actual volume, not metadata-only features.'
  return obj

def sphere_patch(mapping,n=24,rows=12,mat=0):
 P=Patch();P.vert(mapping(Vector((0,0,-1))))
 for j in range(1,rows):
  lat=-pi/2+pi*j/rows
  for k in range(n):a=2*pi*k/n;P.vert(mapping(Vector((cos(lat)*cos(a),cos(lat)*sin(a),sin(lat)))))
 top=P.vert(mapping(Vector((0,0,1))))
 for k in range(n):P.face([0,1+(k+1)%n,1+k],mat)
 for j in range(rows-2):
  for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;c=b+n;d=a+n;P.face([a,b,c,d],mat)
 off=1+(rows-2)*n
 for k in range(n):P.face([off+k,off+(k+1)%n,top],mat)
 return P

def dual_plates(mapping,subdiv=2,relief=.025,skip=None):
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=subdiv,radius=1);bm.verts.ensure_lookup_table();P=Patch()
 for i,v in enumerate(bm.verts):
  c=v.co.normalized()
  if skip and skip(c):continue
  ref=Vector((0,0,1)) if abs(c.z)<.9 else Vector((0,1,0));u=ref.cross(c).normalized();w=c.cross(u);corners=[f.calc_center_median().normalized() for f in v.link_faces];corners.sort(key=lambda p:atan2((p-c).dot(w),(p-c).dot(u)))
  lower=[mapping(p*.945) for p in corners];upper=[mapping((c+(p-c)*.91).normalized()*(1+relief)) for p in corners];P.prism(lower,upper,1 if i%7==0 else (3 if i%5==0 else 0))
 bm.free();return P

def segmented_tube(centers,radii,sides=8,mat=1,quarter_seam_until=None):
 P=Patch();rings=[]
 for i,(pt,r) in enumerate(zip(centers,radii)):
  pt=Vector(pt);a=(Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(0,i-1)])).normalized();ref=Vector((0,0,1)) if abs(a.z)<.9 else Vector((0,1,0));w=ref.cross(a).normalized();t=a.cross(w)
  ring=[]
  for k in range(sides):
   angle=2*pi*k/sides;seam=(1-.13*max(0,cos(4*angle))**4) if quarter_seam_until is not None and i<=quarter_seam_until else 1
   ring.append(P.vert(pt+r*seam*(w*cos(angle)+t*sin(angle))))
  rings.append(ring)
 for i in range(len(rings)-1):
  for k in range(sides):q=(k+1)%sides;P.face([rings[i][k],rings[i][q],rings[i+1][q],rings[i+1][k]],mat if i%4!=0 else 0)
 P.face(list(reversed(rings[0])),mat);P.face(rings[-1],mat);P.base=rings[0];return P

def cup(center,normal,r,depth=.0003,mat=1):
 P=Patch();c=Vector(center);n=Vector(normal).normalized();ref=Vector((0,0,1)) if abs(n.z)<.9 else Vector((0,1,0));w=ref.cross(n).normalized();t=n.cross(w);N=12;rings=[]
 for rad,h in [(r*1.35,-depth*2.6),(r*1.35,0),(r,0),(r*.70,-depth)]:rings.append([P.vert(c+n*h+rad*(w*cos(2*pi*k/N)+t*sin(2*pi*k/N))) for k in range(N)])
 for j in range(3):
  for k in range(N):q=(k+1)%N;P.face([rings[j][k],rings[j][q],rings[j+1][q],rings[j+1][k]],mat if j<2 else 2)
 P.face(list(reversed(rings[0])),mat);P.face(rings[3],2);P.base=rings[0];return P


def combine(patches):
 P=Patch()
 for p in patches:
  off=len(P.v);P.v+=p.v;P.f += [tuple(off+i for i in f) for f in p.f];P.mi+=p.mi;P.base += [off+i for i in p.base];P.solids += [[off+i for i in ids] for ids in p.solids]
 return P

def rectskin(fn,u0,u1,v0,v1,nu=3,nv=3,low=-.0003,high=.00015,mat=0):
 P=Patch();N=(nu+1)*(nv+1)
 for height in [low,high]:
  for j in range(nv+1):
   for i in range(nu+1):P.vert(fn(u0+(u1-u0)*i/nu,v0+(v1-v0)*j/nv,height))
 for j in range(nv):
  for i in range(nu):
   a=j*(nu+1)+i;b=a+1;c=b+nu+1;d=a+nu+1;P.face([a,d,c,b],mat);P.face([a+N,b+N,c+N,d+N],mat)
 edge=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,nv+1)]+[nv*(nu+1)+i for i in range(nu-1,-1,-1)]+[j*(nu+1) for j in range(nv-1,0,-1)]
 for a,b in zip(edge,edge[1:]+edge[:1]):P.face([a,b,b+N,a+N],mat)
 P.base=list(range(N));P.solids=[list(range(2*N))];return P

def planar_plate(poly,zfunc,side=1,relief=.0002,mat=0):
 c=(sum(x for x,y in poly)/len(poly),sum(y for x,y in poly)/len(poly));shr=.965
 q=[(c[0]+(x-c[0])*shr,c[1]+(y-c[1])*shr) for x,y in poly];P=Patch()
 # Additional center creates shallow visible faceting without planar lid shortcuts.
 lower=[(x,y,zfunc(x,y)-side*.00045) for x,y in q];upper=[(x,y,zfunc(x,y)+side*relief) for x,y in q]
 P.prism(lower,upper,mat);return P

def articulated(path,length,radius,N,mat=3,sides=6):
 # Three physical stations per article: narrow contact waist, broad shoulder, broad distal bevel.
 # Geometry changes radius, not just mesh rings or material bands. One closed continuous solid.
 C=[];RR=[]
 for j in range(N):
  for frac,factor in [(0,.68),(.18,1),(.82,1)]:
   t=(j+frac)/N;C.append(path(t));RR.append(radius*(1-.77*t)*factor)
 C.append(path(1));RR.append(radius*.14)
 P=segmented_tube(C,RR,sides,mat)
 return P

def isorophus(cfg,m,col):
 p=cfg['parameters'];M=Mesh();R=p['diameter_m']/2;H=p['dome_height_m'];B=p['basal_thickness_m']
 def z(r):return H*sqrt(max(0,1-(r/R)**2))
 M.add(sphere_patch(lambda v:Vector((R*v.x,R*v.y,(H if v.z>=0 else B)*v.z)),48,16,0),'theca','theca_core')
 P=Patch();rows=p['interambulacral_plate_rows']
 for row in range(rows):
  r0=R*(.12+.72*row/rows);r1=R*(.12+.72*(row+1)/rows);n=12+4*row
  for k in range(n):
   a0=2*pi*(k+.035+(row%2)*.5)/n;a1=2*pi*(k+.965+(row%2)*.5)/n
   fn=lambda r,a,h:Vector((r*cos(a),r*sin(a),z(r)+h))
   P=combine([P,rectskin(fn,r0,r1,a0,a1,2,2,low=-.00045,high=.00012+row*.000009,mat=0 if (k+row)%4 else 3)])
 M.add(P,'interambulacral_plates','thecal_plating','theca',{'imbricate_roof_relief':True})
 P=Patch();n=40
 for row in range(p['peripheral_circlets']):
  r0=R-p['peripheral_width_m']+p['peripheral_width_m']*row/p['peripheral_circlets'];r1=R-p['peripheral_width_m']+p['peripheral_width_m']*(row+1)/p['peripheral_circlets']
  for k in range(n):
   a0=2*pi*(k+.025+(row%2)*.5)/n;a1=2*pi*(k+.975+(row%2)*.5)/n
   fn=lambda r,a,h:Vector((r*cos(a),r*sin(a),z(min(r,R*.999))+h))
   P=combine([P,rectskin(fn,r0,r1,a0,a1,1,1,low=-.00035,high=.00009,mat=3 if row%2 else 0)])
 M.add(P,'peripheral_circlets','peripheral_belt','theca',{'circlets':p['peripheral_circlets']})
 for ray,bend in enumerate(p['ray_curvature_radians']):
  P=Patch();N=p['ambulacral_stations'];a=pi/2+2*pi*ray/5
  def path(t):r=R*(.12+.78*t);theta=a+bend*t**1.3;return Vector((r*cos(theta),r*sin(theta),0))
  def fn(t,w,h):
   c=path(t);d=(path(min(1,t+.001))-path(max(0,t-.001))).normalized();q=c+Vector((-d.y,d.x,0))*w;q.z=z(sqrt(q.x*q.x+q.y*q.y))+h;return q
  for j in range(N):
   for side in [-1,1]:
    for sec in [0,1]:
     t0=(j+.025+sec*.58)/N;t1=(j+(.56 if sec==0 else .975))/N;w=p['ambulacral_width_m']/2*(1 if sec==0 else .58)
     P=combine([P,rectskin(fn,t0,t1,side*.000025,side*w,1,1,low=-.00035,high=.00048 if sec==0 else .00038,mat=1)])
  M.add(P,'ambulacrum_'+str(ray+1),'ambulacral_path','theca',{'curvature_radians':bend,'primary_secondary_pairs':N,'counterclockwise':bend>0})
 for j in range(4):
  a=2*pi*j/4+.12;b=2*pi*(j+1)/4+.12;r=.00145*(.9+.12*(j%2));poly=[(0,0),(r*cos(a),r*sin(a)),(r*cos(b),r*sin(b))];M.add(planar_plate(poly,lambda x,y:z(sqrt(x*x+y*y)),relief=.00038,mat=1),'oral_'+str(j),'principal_oral_plate','theca')
 for j in range(5):
  a=2*pi*j/5;r=.00165;poly=[((r+d)*cos(a+aa),(r+d)*sin(a+aa)) for aa,d in [(-.15,-.00025),(.15,-.00025),(.15,.00025),(-.15,.00025)]];M.add(planar_plate(poly,lambda x,y:z(sqrt(x*x+y*y)),relief=.00025,mat=1),'accessory_'+str(j),'accessory_oral_plate','theca')
 # Closed low valved periproct: no invented open funnel.
 rr=R*.60;ang=-.55;c=Vector((rr*cos(ang),rr*sin(ang),z(rr)));P=Patch();rad=p['periproct_diameter_m']/2
 for j in range(6):
  a=2*pi*j/6;b=2*pi*(j+1)/6;poly=[(c.x,c.y),(c.x+rad*cos(a),c.y+rad*sin(a)),(c.x+rad*cos(b),c.y+rad*sin(b))];P=combine([P,planar_plate(poly,lambda x,y:z(sqrt(x*x+y*y)),relief=.0003,mat=1)])
 M.add(P,'periproct','periproct','theca',{'valved_plate_set':True});return M.emit('isorophus',m,col)

def blastoid(cfg,m,col,stemmed=False):
 p=cfg['parameters'];aid=cfg['asset_id'];M=Mesh();R=p['theca_diameter_m']/2 if stemmed else p['theca_width_m']/2;H=p['theca_height_m'];L=H if stemmed else p['theca_length_m'];offset=p.get('stem_length_m',0)+H/2 if stemmed else 0
 def surface(t,a,h=0):
  # t polar angle from oral summit; a around oral-aboral axis,0 upper side for stemless.
  rr=sin(t)*(R+h);axis=cos(t)*(L/2+h)
  if stemmed:
   rr*=.975+.025*cos(5*a);axis-=math.copysign(.00070*math.exp(-(sin(t)/.25)**2),cos(t));return Vector((rr*cos(a),rr*sin(a),offset+axis))
  zz=sin(t)*(H/2+h)*cos(a);zz*=.82 if zz<0 else 1
  return Vector((rr*sin(a),-axis,zz))
 def normal(t,a):return (surface(t,a,.0001)-surface(t,a,0)).normalized()
 def sh(v):t=math.acos(max(-1,min(1,v.z)));a=atan2(v.y,v.x);return surface(t,a,-.00023)
 M.add(sphere_patch(sh,32,14,0),'theca','theca_core',axis=(0,0,1) if stemmed else (0,1,0))
 angles=[2*pi*i/5 for i in range(5)] if stemmed else [pi+2*pi*i/5 for i in range(5)]
 # Large differentiated structural plates, no arbitrary all-over mosaic.
 P=Patch()
 for sector in range(5):
  a0=angles[sector]+.075;a1=angles[sector]+2*pi/5-.075
  for zone,(t0,t1) in enumerate([(.22,1.96),(1.99,2.78)] if stemmed else [(.2,.72+.07*sin(sector)),(.75+.07*sin(sector),2.64+.04*cos(sector)),(2.67+.04*cos(sector),3.02)]):
   def fn(t,a,h,t0=t0,t1=t1,a0=a0,a1=a1,zone=zone):
    u=(t-t0)/(t1-t0);edge=abs(2*(a-a0)/(a1-a0)-1)
    tt=t-.25*edge*(u if zone==0 else 1-u) if stemmed else t
    return surface(tt,a,h)
   P=combine([P,rectskin(fn,t0,t1,a0,a1,4,3,low=-.0004,high=.00005,mat=0 if zone!=1 else 3)])
 if stemmed:
  for j in range(3):
   fn=lambda t,a,h:surface(t,a,h);P=combine([P,rectskin(fn,2.80,3.07,2*pi*j/3+.035,2*pi*(j+1)/3-.035,3,3,low=-.0004,high=.00005,mat=0)])
 M.add(P,'structural_plates','thecal_plating','theca',{'differentiated_deltoid_radial_basal_regions':True,'basals':3 if stemmed else None})
 for ray,a in enumerate(angles):
  short=not stemmed and ray==0;N=p['ambulacral_stations'] if stemmed else (p['short_ambulacral_stations'] if short else p['long_ambulacral_stations']);end=.78 if short else 2.85;start=.20;P=Patch();width=p['ambulacral_width_m']*(1.65 if short else 1)
  def fn(t,w,h):
   tt=start+(end-start)*t;d=w/max(.0006,R*sin(tt));return surface(tt,a+d,h)
  for j in range(N):
   for side in [-1,1]:
    for sec in [0,1]:
     u0=(j+.03+.55*sec)/N;u1=(j+(.53 if not sec else .98))/N;w=width/2*(1 if not sec else .62)
     P=combine([P,rectskin(fn,u0,u1,side*.000015,side*w,1,1,low=-.00027,high=.00030 if not sec else .00025,mat=1)])
  M.add(P,'ambulacrum_'+str(ray),'ambulacral_path','theca',{'ray':ray,'short_D':short,'stations':N,'classification_tags':['short_ambulacrum' if short else 'long_ambulacrum'] if not stemmed else []})
  count=p['brachioles_per_ray'] if stemmed else (p['brachioles_short_ray'] if short else p['brachioles_per_long_ray'])
  for k in range(count):
   side=-1 if k%2 else 1;u=.18+.55*(k//2)/(max(1,(count+1)//2-1));u=(min(N-1,int(u*N))+.28)/N;tt=start+(end-start)*u;ang=a+side*width*.34/max(.0006,R*sin(tt));base=surface(tt,ang,.00008);n=normal(tt,ang)
   lower=not stemmed and cos(a)<0;length=p['brachiole_length_m'] if stemmed else (p['brachiole_length_lower_m'] if lower else p['brachiole_length_upper_m']);rad=p['brachiole_radius_m'] if stemmed else (p['brachiole_radius_lower_m'] if lower else p['brachiole_radius_upper_m'])
   tang=Vector((-sin(ang),cos(ang),0)) if stemmed else Vector((cos(ang),0,-sin(ang)))
   def path(t,base=base,n=n,tang=tang,length=length,side=side,lower=lower):
    up=Vector((0,0,1));return base+n*length*(.58*t-.22*t*t)+up*length*(.65*t*t if not lower else .1*t*t)+tang*(side*length*.22*t)
   M.add(articulated(path,length,rad,p['brachiole_segments'],3),'brachiole_%s_%s'%(ray,k),'brachiole','ambulacrum_'+str(ray),{'articles':p['brachiole_segments'],'unbranched':True,'inferred':True,'lower_stout':lower})
 # Orals lie near summit and are individually visible.
 for j,a in enumerate(angles):
  mid=a+pi/5;fn=lambda t,aa,h:surface(t,aa,h)
  if stemmed:
   # Solid arrow-shaped tegminal plate: narrow adoral point, paired shoulders, distal tip.
   outline=[(.025,mid),(.16,mid-.44),(.20,mid-.25),(.37,mid),(.20,mid+.25),(.16,mid+.44)];P=Patch();P.prism([surface(t,aa,-.00032) for t,aa in outline],[surface(t,aa,.00018) for t,aa in outline],1)
  else:P=rectskin(fn,.035,.22,mid-.42,mid+.42,2,2,low=-.00032,high=.00018,mat=1)
  M.add(P,'oral_'+str(j),'oral_plate','theca',{'arrow_shaped':stemmed})
 num=10 if stemmed else 4
 for j in range(num):
  a=angles[j//2]+(.23 if j%2 else -.23) if stemmed else angles[j+1]+pi/5;tt=.24 if stemmed else .25;c=surface(tt,a,.00045);d=p['spiracle_diameter_m'];M.add(cup(c,normal(tt,a),d/2,.00030,1),'spiracle_'+str(j),'spiracle','theca',{'local_curved_host_relative':True})
 tt=.48;a=angles[-1]+pi/5;c=surface(tt,a,.00048);d=p['anal_opening_diameter_m'] if stemmed else p['anispiracle_diameter_m'];M.add(cup(c,normal(tt,a),d/2,.00030,1),'anal_opening' if stemmed else 'anispiracle','anal_opening' if stemmed else 'anispiracle','theca',{'local_curved_host_relative':True})
 if stemmed:
  length=p['stem_length_m'];base=Vector((0,0,length+.0011));path=lambda t:base+Vector((.0004*sin(pi*t),0,-length*t));M.add(articulated(path,length,p['stem_diameter_m']/2,p['stem_articles'],1,8),'stem','stem','theca',{'articles':p['stem_articles'],'entire_extent_inferred':True},axis=(0,0,1))
  P=Patch()
  for j in range(3):
   a=2*pi*j/3;path=lambda t,a=a:Vector((p['attachment_radius_m']*t*cos(a),p['attachment_radius_m']*t*sin(a),.00115*(1-t)));P=combine([P,articulated(path,p['attachment_radius_m'],p['stem_diameter_m']*.43,4,1,6)])
  M.add(P,'attachment','inferred_attachment','stem',{'shape_and_extent_uncertain':True})
 return M.emit(aid,m,col)

def nucleocrinus(cfg,m,col):return blastoid(cfg,m,col,True)
def eleutherocrinus(cfg,m,col):return blastoid(cfg,m,col,False)

def placocystites(cfg,m,col):
 p=cfg['parameters'];M=Mesh();W=p['theca_width_m'];L=p['theca_length_m'];T=p['theca_thickness_m']
 def contour(a):return Vector((W/2*math.copysign(abs(cos(a))**.50,cos(a))*(.96+.04*sin(a)),L/2*math.copysign(abs(sin(a))**.50,sin(a)),0))
 def skin(x,y,side=1):return side*T*.5*(.72+.28*max(0,1-(x/(W/2))**2)*max(0,1-(y/(L/2))**2))
 # Full-volume rounded rectangle, not compressed ellipsoid point ends.
 P=Patch();N=48
 for side in [-1,1]:
  for k in range(N):q=contour(2*pi*k/N);q.z=skin(q.x,q.y,side);P.vert(q)
 P.face(list(range(N-1,-1,-1)),0);P.face(list(range(N,2*N)),0)
 for k in range(N):q=(k+1)%N;P.face([k,q,q+N,k+N],0)
 M.add(P,'theca','theca_core')
 # Explicit normal plate arrangement transcribed conceptually from named anatomical regions, not traced coordinates.
 dorsal=[('LOP_L',[(-.70,-1),(-.40,-1),(-.32,-.80),(-.63,-.82)]),('MOP',[(-.40,-1),(.32,-1),(.23,-.82),(-.32,-.80)]),('LOP_R',[(.32,-1),(.70,-1),(.65,-.80),(.23,-.82)]),('DLM_L',[(-.94,-.82),(-.70,-1),(-.63,-.82),(-.43,-.57),(-.92,-.60)]),('A',[(-.63,-.82),(-.32,-.80),(-.14,-.57),(-.40,-.36),(-.43,-.57)]),('DLM_R',[(.70,-1),(.96,-.78),(.94,-.55),(.46,-.56),(.65,-.80)]),('ILM_L',[(-.92,-.60),(-.43,-.57),(-.40,-.36),(-.40,.20),(-.98,.34)]),('C',[(-.32,-.80),(.23,-.82),(.65,-.80),(.46,-.56),(.43,.23),(-.40,.20),(-.40,-.36),(-.14,-.57)]),('ILM_R',[(.46,-.56),(.94,-.55),(.98,.35),(.43,.23)]),('PLM_L',[(-.98,.34),(-.40,.20),(-.38,.87),(-.65,.80),(-.90,.58)]),('PM_L',[(-.40,.20),(-.02,.25),(-.02,.82),(-.38,.87)]),('PM_R',[(-.02,.25),(.43,.23),(.40,.86),(-.02,.82)]),('PLM_R',[(.43,.23),(.98,.35),(.90,.68),(.62,.88),(.40,.86)])]
 ventral=[('V2',[(-.70,-1),(-.20,-1),(-.28,-.67),(-.66,-.68)]),('V3',[(-.20,-1),(.40,-1),(.48,-.70),(.12,-.61),(-.28,-.67)]),('V4',[(.40,-1),(.75,-.97),(.70,-.66),(.48,-.70)]),('V10',[(-.66,-.68),(-.28,-.67),(-.24,-.22),(-.53,-.09),(-.74,-.26)]),('V12',[(-.28,-.67),(.12,-.61),(.30,-.28),(.08,-.10),(-.24,-.22)]),('V14',[(.12,-.61),(.48,-.70),(.70,-.66),(.74,-.27),(.53,-.06),(.30,-.28)]),('V15',[(-.74,-.26),(-.53,-.09),(-.53,.40),(-.76,.49)]),('V16',[(-.53,-.09),(-.24,-.22),(.08,-.10),(-.17,.09),(-.16,.32),(-.35,.48),(-.53,.40)]),('V18',[(.08,-.10),(.30,-.28),(.53,-.06),(.50,.42),(.22,.42),(.12,.30),(.16,.08)]),('V19',[(.53,-.06),(.74,-.27),(.77,.44),(.50,.42)]),('V20',[(-.76,.49),(-.53,.40),(-.35,.48),(-.21,.71),(-.39,.92),(-.61,.89)]),('V21',[(-.35,.48),(-.16,.32),(.12,.30),(.22,.42),(.24,.66),(-.02,.78),(-.21,.71)]),('V22',[(.22,.42),(.50,.42),(.77,.44),(.66,.86),(.40,.93),(.24,.66)])]
 for side,plates in [(1,dorsal),(-1,ventral)]:
  for tag,poly in plates:
   pts=[(x*W*.48,y*L*.48) for x,y in poly]
   if side==1 and tag.startswith(('DLM','ILM','PLM')):
    cx=sum(x for x,y in pts)/len(pts);cy=sum(y for x,y in pts)/len(pts);pts=[(cx+.97*(x-cx),cy+.97*(y-cy)) for x,y in pts];P=Patch();P.prism([(x,y,skin(x,y,-1)-p['plate_relief_m']) for x,y in pts],[(x,y,skin(x,y,1)+p['plate_relief_m']) for x,y in pts],3);M.add(P,'marginal_'+tag,'marginal_plate','theca');continue
   kind='ventral_anterior_plate' if side<0 and tag in ['V2','V3','V4'] else 'thecal_plate';M.add(planar_plate(pts,lambda x,y,side=side:skin(x,y,side),side,p['plate_relief_m'],0 if side>0 else 1),('dorsal_' if side>0 else 'ventral_')+tag,kind,'theca')
 # Separate small round V17 among the ventral midline plates.
 rr=.00115;cx=0;cy=.0022;poly=[(cx+rr*cos(2*pi*j/10),cy+rr*sin(2*pi*j/10)) for j in range(10)];M.add(planar_plate(poly,lambda x,y:skin(x,y,-1),-1,p['plate_relief_m'],1),'ventral_V17','ventral_round_midline_plate','theca')
 for side in [-1,1]:
  base=Vector((side*W*.32,-L*.49,0));joint=sphere_patch(lambda v:base+Vector((v.x*.0008,v.y*.0009,v.z*.0007)),12,6,2);M.add(joint,'spine_joint_'+str(side),'spine_articulation','theca');end=base+Vector((side*.006,-p['oral_spine_length_m'],.0009));centers=[base+(end-base)*j/8 for j in range(9)];radii=[p['oral_spine_base_diameter_m']/2*(1-j/8)+.00003 for j in range(9)];M.add(segmented_tube(centers,radii,8,1),'spine_'+str(side),'oral_spine','spine_joint_'+str(side),{'unjointed_spine':True})
 # Three differentiated regions, broad plate-like proximal lobes and narrow articulated distal section.
 N=p['proximal_articles']+p['middle_articles']+p['distal_articles'];C=[];RR=[]
 for j in range(N):
  for frac,factor in [(0,.70),(.16,1),(.84,1)]:
   u=(j+frac)/N;phase=j/N;t=p['proximal_fraction']*(j+frac)/p['proximal_articles'] if j<p['proximal_articles'] else (p['proximal_fraction']+p['middle_fraction']*(j+frac-p['proximal_articles'])/p['middle_articles'] if j<p['proximal_articles']+p['middle_articles'] else p['proximal_fraction']+p['middle_fraction']+(1-p['proximal_fraction']-p['middle_fraction'])*(j+frac-p['proximal_articles']-p['middle_articles'])/p['distal_articles']);rad=p['proximal_width_m']/2*(1-.60*t/p['proximal_fraction']) if t<p['proximal_fraction'] else (p['distal_base_width_m']/2*(1-(t-p['proximal_fraction'])/(1-p['proximal_fraction'])))+.00005;C.append((.002*sin(t*pi),L*.42+p['aulacophore_length_m']*t,-.00015+.0005*sin(t*pi)));RR.append(rad*factor)
 C.append((0,L*.42+p['aulacophore_length_m'],0));RR.append(.00005)
 P=segmented_tube(C,RR,12,2,quarter_seam_until=p['proximal_articles']*3)
 M.add(P,'aulacophore','aulacophore','theca',{'proximal_articles':p['proximal_articles'],'middle_articles':p['middle_articles'],'distal_articles':p['distal_articles'],'sculpted_multirow_proximal_seams':True});return M.emit('placocystites',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();aid=cfg['asset_id'];col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'animals',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Immutable batch108 original freeze plus transparent prefreeze taxonomy clarifications; no source media incorporated.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 (out/'execution.json').write_text(json.dumps({'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':start,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clock_note':'Executor clock separate from clock.curr_time; no provider times inferred.','blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()},indent=2)+'\n')
if __name__=='__main__':main()
