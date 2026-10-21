#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch101 original botanical geometry, authored only after immutable original freeze.
No downloaded mesh or image is an input. Every component is independently editable
through named vertex groups. Metric/attachment records are stored in a Blend Text.
"""
import argparse,datetime,hashlib,json,math,os,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from math import sin,cos,pi
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset

def axes(d,n=None):
 a=Vector(d).normalized();n=Vector(n) if n else Vector((0,0,1))
 if abs(a.dot(n.normalized()))>.98:n=Vector((0,1,0))
 w=n.cross(a).normalized();t=a.cross(w).normalized();return a,w,t
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.components=[]
 def add(self,v,f,mat,tag,kind,d=(0,0,1),n=None,parent=None,base=None,design=None):
  offset=len(self.v);vs=[Vector(x) for x in v];a,w,t=axes(d,n)
  self.v.extend(vs);self.f.extend(tuple(offset+i for i in x) for x in f);self.mi.extend([mat]*len(f))
  self.components.append(dict(tag=tag,kind=kind,vertices=list(range(offset,offset+len(v))),axes=[list(a),list(w),list(t)],parent=parent,base_vertices=[offset+i for i in (base or [])],design=design or {}))
 def emit(self,name,m,col):
  lo=[min(v[k] for v in self.v) for k in range(3)];hi=[max(v[k] for v in self.v) for k in range(3)];off=Vector((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]));self.v=[v+off for v in self.v]
  o=mesh_object(name,self.v,self.f,m,col)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
  for c in self.components:o.vertex_groups.new(name=c['tag']).add(c['vertices'],1,'REPLACE')
  # Text is not exported as glTF extras: avoids duplicating scientific metadata in GLB.
  txt=bpy.data.texts.new('BATCH101_COMPONENT_CONTRACT.json');txt.write(json.dumps(dict(schema_version=1,object_name=o.name,translation=list(off),components=self.components),sort_keys=True))
  o['component_contract']='BATCH101_COMPONENT_CONTRACT.json';o['source_editing']='Named organ vertex groups; all dimensions in meters, translation only.'
  return o

def tube(M,pts,radii,sides,mat,tag,kind='axis',parent=None):
 pts=[Vector(v) for v in pts];v=[]
 for i,p in enumerate(pts):
  a,w,t=axes(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)])
  for j in range(sides):v.append(p+radii[i]*(w*cos(2*pi*j/sides)+t*sin(2*pi*j/sides)))
 base_index=len(v);v.append(pts[0]);tip_index=len(v);v.append(pts[-1]);f=[(base_index,(j+1)%sides,j) for j in range(sides)]
 for i in range(len(pts)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 last=(len(pts)-1)*sides
 for j in range(sides):f.append((tip_index,last+j,last+(j+1)%sides))
 M.add(v,f,mat,tag,kind,pts[-1]-pts[0],parent=parent,base=[base_index]+list(range(sides)) if parent else [],design={'centerline_length_m':sum((b-a).length for a,b in zip(pts,pts[1:]))})

def blade(M,b,d,L,W,T,mat,tag,kind='leaf',parent=None,n=(0,0,1),rounded=True):
 b=Vector(b);a,w,t=axes(d,n)
 # Blunt tip with two terminal points, widest point at 45%; closed ten-triangle volume.
 outline=[(0,0),(-W/2,L*.45),(-W*.11,L),(W*.11,L),(W/2,L*.45)] if rounded else [(0,0),(-W/2,L*.45),(0,L),(W/2,L*.45)]
 v=[b+w*x+a*y for x,y in outline];v.extend([b+a*L*.48+t*T/2,b+a*L*.48-t*T/2]);N=len(outline)
 f=[]
 for i in range(N):j=(i+1)%N;f.extend([(N,i,j),(N+1,j,i)])
 M.add(v,f,mat,tag,kind,a,t,parent,[0] if parent else [],{'nominal_length_m':L,'nominal_width_m':W,'nominal_thickness_m':T})

def grooved(M,b,d,L,W,T,depth,mat,tag,parent):
 b=Vector(b);a,w,t=axes(d);v=[];stations=[(0,.12),(.16,1),(.84,.75),(1,.12)]
 for layer in [0,1]:
  for y,fac in stations:
   for x in [-1,0,1]:v.append(b+a*y*L+w*x*fac*W/2+t*((T/2-depth*(1-abs(x))) if layer==0 else -T/2))
 f=[]
 for layer in [0,1]:
  for i in range(3):
   for j in range(2):p=layer*12+i*3+j;f.append((p,p+1,p+4,p+3) if layer==0 else (p+3,p+4,p+1,p))
 edge=[0,1,2,5,8,11,10,9,6,3]
 for i,x in enumerate(edge):y=edge[(i+1)%len(edge)];f.append((x,y,y+12,x+12))
 M.add(v,f,mat,tag,'cladode',a,t,parent,[0,1,2,12,13,14],{'groove_depth_m':depth,'nominal_length_m':L,'nominal_width_m':W})

def fan(M,b,d,L,W,T,mat,tag,parent):
 b=Vector(b);a,w,t=axes(d);outline=[(-.045*W,0),(-.5*W,.72*L)]
 # Five rounded oblong lobes, separated by explicit deep sinuses.
 for j in range(5):
  x=(-.4+j*.2)*W;outline.extend([(x-.055*W,.94*L),(x,.995*L),(x+.055*W,.94*L)])
  if j<4:outline.append((x+.1*W,.67*L))
 outline.extend([(.5*W,.72*L),(.045*W,0)])
 xy=[Vector((x,y,0)) for x,y in outline];lookup={tuple(v):i for i,v in enumerate(xy)}
 tris=[tuple(i if isinstance(i,int) else lookup[tuple(i)] for i in tr) for tr in tessellate_polygon([xy])];N=len(outline)
 v=[b+w*x+a*y+t*z for z in [-T/2,T/2] for x,y in outline]
 f=tris+[tuple(N+i for i in reversed(tr)) for tr in tris]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 M.add(v,f,mat,tag,'five_lobed_cone_scale',a,t,parent,[0,N-1,N,2*N-1],{'lobes':5,'nominal_length_m':L,'nominal_width_m':W})

def ellipsoid(M,b,d,L,W,D,mat,tag,kind,parent=None,sides=8,rings=5):
 b=Vector(b);a,w,t=axes(d);v=[b]
 for k in range(1,rings):
  q=pi*k/rings
  for j in range(sides):r=2*pi*j/sides;v.append(b+a*(L*(1-cos(q))/2)+w*(W/2*sin(q)*cos(r))+t*(D/2*sin(q)*sin(r)))
 v.append(b+a*L);f=[]
 for j in range(sides):f.append((0,1+(j+1)%sides,1+j))
 for k in range(rings-2):
  for j in range(sides):i=1+k*sides+j;n=1+k*sides+(j+1)%sides;f.append((i,n,n+sides,i+sides))
 last=1+(rings-2)*sides
 for j in range(sides):f.append((last+j,last+(j+1)%sides,len(v)-1))
 M.add(v,f,mat,tag,kind,a,t,parent,[0] if parent else [],{'nominal_length_m':L,'nominal_width_m':W})

def prism(M,outline,b,d,n,T,mat,tag,kind,parent=None):
 b=Vector(b);a,w,t=axes(d,n);xy=[Vector((x,y,0)) for x,y in outline];look={tuple(v):i for i,v in enumerate(xy)};tris=[tuple(i if isinstance(i,int) else look[tuple(i)] for i in tr) for tr in tessellate_polygon([xy])];N=len(outline)
 v=[b+w*x+a*y+t*(z*(.20 if abs(y)<1e-10 else 1)) for z in [-T/2,T/2] for x,y in outline];f=tris+[tuple(N+i for i in reversed(tr)) for tr in tris]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 # Base pair are actual central vertices near attachment, not point declarations.
 bv=[i for i in range(N) if abs(outline[i][1])<1e-10];M.add(v,f,mat,tag,kind,a,t,parent,bv+[i+N for i in bv],{'nominal_thickness_m':T})

def box(M,lo,hi,mat,tag,kind='display_mount'):
 x0,y0,z0=lo;x1,y1,z1=hi;v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)];f=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];M.add(v,f,mat,tag,kind)

def text_label(M,b,size,mat,parent):
 curve=bpy.data.curves.new('enlarged-label','FONT');curve.body='ENLARGED';curve.size=size;curve.align_x='CENTER';curve.extrude=.00010;curve.resolution_u=1;curve.bevel_depth=0;o=bpy.data.objects.new('label-conversion',curve);bpy.context.collection.objects.link(o);o.rotation_euler.x=pi/2;o.location=b;bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;v=[o.matrix_world@x.co for x in o.data.vertices];f=[tuple(p.vertices) for p in o.data.polygons];M.add(v,f,mat,'enlarged_label','display_label');bpy.data.objects.remove(o,do_unlink=True)


def flat_polygon(M,outline,z,T,mat,tag,kind):
 xy=[Vector((x,y,0)) for x,y in outline];lookup={tuple(q):i for i,q in enumerate(xy)};N=len(xy)
 tris=[tuple(i if isinstance(i,int) else lookup[tuple(i)] for i in tr) for tr in tessellate_polygon([xy])]
 v=[Vector((x,y,zz)) for zz in [z,z+T] for x,y in outline]
 f=[tuple(reversed(tr)) for tr in tris]+[tuple(i+N for i in tr) for tr in tris]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 M.add(v,f,mat,tag,kind,(0,1,0),(0,0,1))

def cup(M,b,rx,ry,H,mat,tag,parent):
 b=Vector(b);N=16;profile=[(1,0),(.96,H*.58),(.78,H),(.60,H*.85),(.51,H*.28),(.12,H*.12)]
 v=[b+Vector((rx*r*cos(2*pi*j/N),ry*r*sin(2*pi*j/N),z)) for r,z in profile for j in range(N)]
 f=[tuple(reversed(range(N)))]+[(k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j) for k in range(len(profile)-1) for j in range(N)]+[tuple(range((len(profile)-1)*N,len(profile)*N))]
 M.add(v,f,mat,tag,'cup',(0,1,0),(0,0,1),parent,list(range(N)),{'open_center':True,'nominal_height_m':H})

def marchantites(c,m,col):
 M=Mesh();p=c['parameters'];mm=.001
 # Continuous connected ribbon outline: basal axis forks, right daughter forks again.
 outline=[(-.9,-8),(.9,-8),(.9,-4.5),(3.1,-.1),(5.9,5.7),(6.0,6.5),(5.6,7.1),(4.9,7.3),(4.2,6.9),(1.9,2.4),(1.45,6.5),(1.1,7.15),(.4,7.4),(-.3,7.1),(-.5,6.4),(.35,.8),(-1.0,-2.0),(-3.1,5.7),(-3.45,6.45),(-4.1,6.7),(-4.8,6.4),(-5.0,5.7),(-2.0,-3.5),(-.9,-4.7)]
 outline=[(x*mm,y*mm) for x,y in outline];flat_polygon(M,outline,.00025,p['thallus_thickness_m'],0,'thallus','thallus')
 paths=[[(0,-.0077,.00048),(0,-.004,.00048)],[(0,-.004,.00048),(-.00135,-.001,.00048),(-.00370,.00485,.00048)],[(0,-.004,.00048),(.0017,.0004,.00048)],[(.0017,.0004,.00048),(.00062,.00542,.00048)],[(.0017,.0004,.00048),(.00455,.00542,.00048)]]
 for k,pts in enumerate(paths):tube(M,pts,[.00018]*len(pts),6,1,f'costa_{k}','costa','thallus')
 for k,(x,y) in enumerate([(-.00410,.00565),(.00048,.00625),(.00505,.00625)]):cup(M,(x,y,.00042),p['cup_diameter_m']/2,p['cup_diameter_m']*.48,p['cup_height_m'],2,f'cup_{k}','thallus')
 # Twenty-four downward scales in two lines beside costa, deliberately visible low views.
 scalepts=[]
 for k,pts in enumerate(paths):
  a=Vector(pts[0]);b=Vector(pts[-1]);n=3 if k==1 else 2 if k in [0,2] else 2
  for j in range(n):scalepts.append((a.lerp(b,(j+.35)/(n+.1)),(b-a).normalized()))
 scalepts=scalepts[:11];scalepts.append((Vector((-.0038,.0048,.00048)),Vector((-.4,.9,0)).normalized()))
 for k,(b,d) in enumerate(scalepts):
  side=Vector((-d.y,d.x,0))
  for sign in [-1,1]:
   bb=b+side*sign*.00012;bb.z=.00032;dd=(side*sign*.7+Vector((0,0,-.7))).normalized();ellipsoid(M,bb,dd,.00042,p['ventral_scale_width_m'],.00013,3,f'scale_{k}_{sign}','ventral_scale','thallus',sides=8,rings=4)
 return M.emit('marchantites-three-distal-cups',m,col)

def winfrenatia(c,m,col):
 M=Mesh();p=c['parameters'];r=p['cell_outer_radius_m'];T=p['mat_thickness_m'];v=[];faces=[];mats=[];index={};edges={};pitgroups=[]
 def vertex(x,y,z):
  key=(round(x,10),round(y,10),round(z,10))
  if key not in index:index[key]=len(v);v.append(Vector(key))
  return index[key]
 cells=[(q,s) for q in range(-2,3) for s in range(-2,3) if max(abs(q),abs(s),abs(q+s))<=2]
 for k,(q,s) in enumerate(cells):
  cx=r*1.5*q;cy=r*math.sqrt(3)*(s+q/2);outer=[];inner=[];bottom=[];pr=p['pit_diameter_m']/2*(1+.035*sin(k*1.7));depth=p['pit_depth_m']*(1+.06*sin(k*2.3))
  for j in range(6):
   a=2*pi*j/6;outer.append(vertex(cx+r*cos(a),cy+r*sin(a),T));inner.append(vertex(cx+pr*cos(a),cy+pr*sin(a),T-.00003));bottom.append(vertex(cx+pr*.38*cos(a),cy+pr*.38*sin(a),T-depth))
  pc=vertex(cx,cy,T-depth)
  for j in range(6):
   n=(j+1)%6;faces.extend([(outer[j],outer[n],inner[n],inner[j]),(inner[j],inner[n],bottom[n],bottom[j]),(bottom[j],bottom[n],pc)]);mats.extend([0,1,3]);edge=tuple(sorted([outer[j],outer[n]]));edges.setdefault(edge,[]).append((outer[j],outer[n]))
  pitgroups.append({'tag':f'pit_{k:02d}','kind':'pit','vertices':inner+bottom+[pc],'axes':[[0,1,0],[1,0,0],[0,0,1]],'parent':'mat_body','base_vertices':inner,'shared_topology':True,'design':{'nominal_diameter_m':p['pit_diameter_m'],'nominal_depth_m':p['pit_depth_m']}})
 outerboundary=[arr[0] for arr in edges.values() if len(arr)==1];lower={}
 # Three exposed edge bands, the lower course marginally flared. One closed volume, not overlapping slabs.
 for j in set(i for edge in outerboundary for i in edge):
  x,y,z=v[j];lower[j]=[j]+[vertex(x*sc,y*sc,zz) for sc,zz in [(1.035,T*.67),(1.065,T*.34),(1.09,0)]]
 for a,b in outerboundary:
  for k in range(3):faces.append((lower[a][k],lower[a][k+1],lower[b][k+1],lower[b][k]));mats.append([1,2,3][k])
 center=vertex(0,0,0)
 for a,b in outerboundary:faces.append((center,lower[b][-1],lower[a][-1]));mats.append(3)
 M.add(v,faces,0,'mat_body','layered_mat',(0,1,0),(0,0,1));M.mi=mats;M.components+=pitgroups
 return M.emit('winfrenatia-nineteen-pitted-layered-fragment',m,col)

def palmate(M,b,d,L,T,mat,tag,parent):
 # Seven radial finger lobes remain joined by a substantial basal lamina.
 a,w,t=axes(d,(0,0,1));outline=[(-.006,0)];lens=[.115,.165,.205,L,.205,.165,.115]
 for j,ang in enumerate([-60,-40,-20,0,20,40,60]):
  aa=math.radians(ang);ll=lens[j];x=sin(aa);y=cos(aa);per=(y,-x);half=.010 if j in [0,6] else .013
  outline.extend([(x*ll*.72-per[0]*half,y*ll*.72-per[1]*half),(x*ll,y*ll),(x*ll*.72+per[0]*half,y*ll*.72+per[1]*half)])
  if j<6:
   aa=math.radians(ang+10);rr=.060 if j in [0,5] else .082;outline.append((sin(aa)*rr,cos(aa)*rr))
 outline.append((.006,0));prism(M,outline,b,d,(0,0,1),T,mat,tag,'leaf',parent)
 M.components[-1]['design']['lobes']=7

def macginitiea(c,m,col):
 M=Mesh();p=c['parameters'];trunk=[Vector((0,0,0)),Vector((-.025,.01,.35)),Vector((.015,.005,.80)),Vector((-.02,.015,1.25)),Vector((0,0,1.7))];tube(M,trunk,[.075,.052,.035,.023,.007],10,0,'trunk','trunk')
 branchpts=[]
 for k in range(3):
  angle=k*2*pi/3+.25;rad=Vector((cos(angle),sin(angle),0));side=Vector((-sin(angle),cos(angle),0));base=trunk[1].lerp(trunk[2],.55+k*.15);end=base+rad*(.55-.035*k)+Vector((0,0,.78+.12*k));mid=base.lerp(end,.52)+Vector((0,0,-.04));pts=[base,mid,end];tag=f'branch_{k}';tube(M,pts,[.029,.016,.005],8,0,tag,'branch','trunk');branchpts.append((pts,rad,side,tag))
  for j in range(8):
   # Spread in alternating side fans; no dense opaque canopy covering the heads.
   u=.20+j*.105;seg=0 if u<.52 else 1;f=u/.52 if seg==0 else (u-.52)/.48;node=pts[seg].lerp(pts[seg+1],f);sign=-1 if j%2 else 1
   ld=(side*sign*.73+rad*.50+Vector((0,0,.20+.10*sin(j)))).normalized();twig_end=node+ld*(.065+.025*(j%3))+Vector((0,0,.015));tw=f'twig_{k}_{j}';tube(M,[node,twig_end],[.0065,.0022],6,0,tw,'twig',tag)
   pe=twig_end+ld*p['petiole_length_m'];pt=f'petiole_{k}_{j}';tube(M,[twig_end-ld*.0003,pe],[.0019,.0015],6,0,pt,'petiole',tw)
   leaf_d=(ld*.92+Vector((0,0,.12*(-1 if j%3==0 else 1)))).normalized();palmate(M,pe-ld*.0005,leaf_d,p['leaf_length_m'],p['leaf_thickness_m'],1+(j+k)%3,f'leaf_{k}_{j}',pt)
  # Fruit axis beyond branch end and just below crown, clear of leaf blades.
  node=pts[1];stemend=node+rad*.22+side*.10+Vector((0,0,-.12));ft=f'fruit_stalk_{k}';tube(M,[node,stemend],[.003,.0014],6,0,ft,'fruit_stalk',tag);axis_end=stemend+Vector((.008*rad.x,.008*rad.y,-.135));ax=f'fruit_axis_{k}';tube(M,[stemend,axis_end],[.0014,.0006],6,0,ax,'fruit_axis',ft)
  for j in range(7):
   b=stemend.lerp(axis_end,(.012+j*p['head_axis_spacing_m'])/.135);ang=j*2.4;dd=rad*cos(ang)+side*sin(ang);e=b+dd*.013;pd=f'fruit_pedicel_{k}_{j}';tube(M,[b,e],[.0008,.00045],5,0,pd,'fruit_pedicel',ax);ellipsoid(M,e-dd*.0008,dd,p['head_diameter_m'],p['head_diameter_m'],p['head_diameter_m'],4,f'head_{k}_{j}','fruit_head',pd,sides=10,rings=6)
 return M.emit('macginitiea-airy-seven-lobed-tree',m,col)

def cross(M,x,z,L,W,depth,mat,tag,parent=None,base=None):
 # A single closed cross prism, curved across X, with visible tapered ray ends.
 w=W/2;out=[(-w*.22,-L), (w*.22,-L),(w,-w),(L,-w*.22),(L,w*.22),(w,w),(w*.22,L),(-w*.22,L),(-w,w),(-L,w*.22),(-L,-w*.22),(-w,-w)]
 tris=[(11,2,5,8),(0,1,2,11),(2,3,4,5),(8,5,6,7),(10,11,8,9)];N=len(out)
 def cy(xx):return .0045*(xx/.025)**2
 v=[Vector((x+a,cy(x+a)+yy,z+b)) for yy in [-depth/2,depth/2] for a,b in out];f=tris+[tuple(i+N for i in reversed(t)) for t in tris]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 # Explicit central surface vertices inside the parent ray for true intersection testing.
 center0=len(v);v.extend([Vector((x,cy(x)-depth/2,z)),Vector((x,cy(x)+depth/2,z))])
 # Split central triangulations by replacing with fully valid original triangulated faces; central vertices are legitimate topology anchors through split selected triangle.
 # Rather than loose vertices, use original outline vertices nearest specified parent axis for the base record.
 v=v[:-2];bv=list(range(N*2)) if parent else []
 M.add(v,f,mat,tag,'spicule_order_'+tag.split('_')[1],(0,0,1),(0,-1,0),parent,bv,{'ray_half_length_m':L,'single_closed_cross':True})

def protospongia(c,m,col):
 M=Mesh();p=c['parameters'];box(M,(-.028,-.006,0),(.028,.006,.003),3,'display_support','display_support')
 for iz in range(3):
  for ix in range(4):
   x=-.018+.012*ix;z=.008+.012*iz;prev='display_support' if iz==0 else f'cross_1_{iz-1}_{ix}';tag=f'cross_1_{iz}_{ix}';L=p['order_ray_lengths_m'][0];cross(M,x,z,L,.00075,.00070,0,tag,prev)
   px,pz=x,z
   for order in range(2,7):
    prevtag=f'cross_1_{iz}_{ix}'
    offsets={2:(.0036,0),3:(-.0033,0),4:(0,.0034),5:(0,-.0038),6:(-.0051,0)}
    dx,dz=offsets[order];px,pz=x+dx,z+dz
    tag=f'cross_{order}_{iz}_{ix}';L=p['order_ray_lengths_m'][order-1];W=max(.000075,.00052*(.57**(order-2)));cross(M,px,pz,L,W,W*.82,1 if order%2==0 else 2,tag,prevtag)
 return M.emit('protospongia-six-order-wall-fragment',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update()
 export_asset(aid,aid,'plants' if aid in ['marchantites','macginitiea'] else 'specimens',col,metadata={'representation':'living-reconstruction' if aid in ['marchantites','macginitiea'] else 'bounded-specimen','export_texcoords':False,'source_scope':'Original batch101 pregeometry freeze. Reference pixels and meshes not incorporated.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':start,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
