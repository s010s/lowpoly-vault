#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch99 original botanical geometry, authored only after immutable original freeze.
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
  txt=bpy.data.texts.new('BATCH99_COMPONENT_CONTRACT.json');txt.write(json.dumps(dict(schema_version=1,object_name=o.name,translation=list(off),components=self.components),sort_keys=True))
  o['component_contract']='BATCH99_COMPONENT_CONTRACT.json';o['source_editing']='Named organ vertex groups; all dimensions in meters, translation only.'
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

def monetianthus(c,m,col):
 p=c['parameters'];M=Mesh();N=36;profile=[(.012,0),(.014,.020),(.030,.062),(.042,.092),(.045,.106),(.041,.120),(.031,.120),(.027,.106),(.010,.102),(.001,.102)]
 v=[]
 for r,z in profile:
  for j in range(N):
   a=2*pi*j/N;r2=r*(1+.018*cos(12*a))
   v.append((r2*cos(a),r2*sin(a),z))
 f=[]
 for k in range(len(profile)-1):
  for j in range(N):a=k*N+j;b=k*N+(j+1)%N;f.append((a,b,b+N,a+N))
 f.append(tuple(reversed(range(N))));f.append(tuple(range((len(profile)-1)*N,len(profile)*N)));M.add(v,f,0,'fused_flower_body','gynoecium_body')
 tube(M,[(0,0,.100),(0,0,.112),(0,0,.125)],[.006,.006,.0053],12,1,'central_column','central_column','fused_flower_body')
 for j in range(12):
  a=2*pi*j/12;rad=Vector((cos(a),sin(a),0));w=Vector((-sin(a),cos(a),0));profile2=[(.034,.112,.0065,.004),(.040,.128,.0057,.004),(.046,.142+.001*sin(j*1.7),.0033,.003),(.047,.148+.001*sin(j*1.7),.0030,.0025)]
  vs=[]
  for r,z,W,T in profile2:
   for q in range(6):aa=2*pi*q/6;vs.append(rad*(r+T*cos(aa))+w*W*sin(aa)+Vector((0,0,z)))
  fs=[tuple(reversed(range(6)))]+[(k*6+q,k*6+(q+1)%6,(k+1)*6+(q+1)%6,(k+1)*6+q) for k in range(3) for q in range(6)]+[tuple(range(18,24))]
  tag=f'carpel_tip_{j:02d}';M.add(vs,fs,1 if j%3 else 0,tag,'free_carpel_tip',(rad*.4+Vector((0,0,1))),w,'fused_flower_body',list(range(6)))
  for side in [-1,1]:
   b=rad*.0358+w*side*.0017+Vector((0,0,.125));e=rad*.0411+w*side*.0013+Vector((0,0,.139));tube(M,[b,e],[.00065,.00040],5,2,f'ventral_crest_{j:02d}_{side}','ventral_crest',tag)
 for j in range(10):
  a=2*pi*j/10+.045*sin(j*2.1);r=Vector((cos(a),sin(a),0));z=.094+.003*sin(j*1.3);rr=(.042+(.003*(z-.092)/.014)) if z>=.092 else (.030+.012*(z-.062)/.030);b=r*(rr-.0012)+Vector((0,0,z));ellipsoid(M,b,r,.004,.009,.004,2,f'outer_scar_{j:02d}','tepal_or_bract_scar','fused_flower_body',sides=8,rings=4)
 for j in range(20):
  a=2*pi*j/20+.03*cos(j*2);rad=Vector((cos(a),sin(a),0));z=.109+.002*sin(j*2.1);b=rad*.042+Vector((0,0,z));ellipsoid(M,b,rad,.0038,.0045,.006,1,f'stamen_base_{j:02d}','stamen_base_scar','fused_flower_body',sides=4,rings=3)
 box(M,(.040,-.040,0),(.094,-.035,.009),3,'label_plinth');text_label(M,(.067,-.04005,.0025),.005,0,'label_plinth')
 return M.emit('monetianthus-preserved-flower-enlarged',m,col)

def palaeocarpinus(c,m,col):
 p=c['parameters'];M=Mesh();pts=[Vector((0,0,0)),Vector((.0006,0,.02)),Vector((-.0005,.0002,.04)),Vector((0,0,.06))];tube(M,pts,[.00055,.0005,.00045,.00025],8,0,'fruiting_axis','axis')
 for k in range(6):
  z=.010+k*.008;idx=min(int(z/.02),2);node=pts[idx].lerp(pts[idx+1],(z-idx*.02)/.02)
  for j in range(2):
   a=k*2.18+(j-.5)*1.15;rad=Vector((cos(a),sin(a),0));d=(rad*.62+Vector((0,0,.78))).normalized();side=Vector((-sin(a),cos(a),0));base=node+rad*.001;tag=f'pedicel_{k}_{j}';tube(M,[node,base],[.00055,.0004],6,0,tag,'pedicel','fruiting_axis')
   nut=f'nutlet_{k}_{j}';b=base-d*.00018;ellipsoid(M,b,d,p['nutlet_length_m'],p['nutlet_width_m'],p['nutlet_thickness_m'],3,nut,'nutlet',tag,sides=10,rings=6)
   # Two equal opposite bilobed bracts open away from the visible nut front.
   for sign in [-1,1]:
    bd=(Vector((0,0,1))*.88+side*sign*.48).normalized();bb=b+side*sign*.00025+d*.0005
    L=p['bract_length_m'];W=p['bract_width_m'];outline=[(0,0),(-.20*W,.24*L),(-.45*W,.43*L),(-.36*W,.47*L),(-.56*W,.63*L),(-.38*W,.65*L),(-.50*W,.80*L),(-.30*W,.78*L),(-.20*W,L),(-.02*W,.43*L),(.20*W,.95*L),(.28*W,.78*L),(.48*W,.81*L),(.37*W,.62*L),(.56*W,.62*L),(.35*W,.46*L),(.44*W,.42*L),(.19*W,.24*L)]
    prism(M,outline,bb,bd,rad,p['bract_thickness_m'],1+(k+j)%2,f'bract_{k}_{j}_{sign}','bilobed_bract',nut)
   # Low geometric striations run over nut surface, not unattached ropes.
   aa,ww,nn=axes(d)
   for q in range(5):
    angle=pi*(1.20+.15*q);rr=ww*cos(angle)+nn*sin(angle);rstart=b+d*.0008+ww*.00077*cos(angle)+nn*.00049*sin(angle);rend=b+d*.0036+ww*.00077*cos(angle)+nn*.00049*sin(angle);mid=b+d*.0022+ww*.0015*cos(angle)+nn*.00095*sin(angle)
    tube(M,[rstart,mid,rend],[.00007,.00010,.00006],4,1,f'nut_ridge_{k}_{j}_{q}','nutlet_ridge',nut)
   tip=b+d*.0043;st=f'style_{k}_{j}';tube(M,[tip,tip+d*.00022],[.00015,.00010],5,0,st,'style',nut)
   for sign in [-1,1]:tube(M,[tip+d*.00018,tip+d*.00036+side*sign*.00012],[.00008,.00004],4,0,f'style_lobe_{k}_{j}_{sign}','style_lobe',st)
 return M.emit('palaeocarpinus-six-paired-cymules',m,col)

def proterocladus(c,m,col):
 p=c['parameters'];M=Mesh();box(M,(-.0675,-.004,0),(.0675,.004,.190),2,'tablet')
 y=-.0049;ellipsoid(M,(0,-.0039,.017),(0,0,1),.004,.006,.004,1,'holdfast','holdfast','tablet',sides=10,rings=4)
 centers=[Vector((.004*sin(i*.60),y,.020+i*.019)) for i in range(9)]
 for i in range(8):
  b=centers[i];e=centers[i+1];mid=b.lerp(e,.55);r=.0013+.000035*i;tube(M,[b,mid,e],[r*.80,r,r*.80],7,0,f'main_cell_{i}','main_cell','holdfast' if i==0 else f'main_cell_{i-1}')
 branchspec=[(1,-1,.042,.047),(2,1,.045,.063),(4,-1,.042,.050),(5,1,.025,.047),(6,-1,.026,.037)];paths=[]
 for k,(idx,sgn,xspan,zspan) in enumerate(branchspec):
  b=centers[idx].lerp(centers[idx+1],.43);a=b+Vector((sgn*xspan*.5,0,zspan*.20));d=b+Vector((sgn*xspan*.87,0,zspan*.65));e=b+Vector((sgn*xspan,0,zspan));path=[b,a,d,e];tag=f'lateral_{k}';segpts=[];rads=[]
  for ii in range(3):
   if ii==0:segpts.append(path[ii]);rads.append(.0010)
   segpts.extend([path[ii].lerp(path[ii+1],.46),path[ii].lerp(path[ii+1],.91),path[ii+1]])
   broad=.0010+.00010*ii; rads.extend([broad,broad*.78,broad*.80])
  tube(M,segpts,rads,7,0,tag,'primary_lateral',f'main_cell_{idx}');paths.append((path,tag))
  if k in [0,2,4]:
   dd=(e-d).normalized();tube(M,[e-dd*.0002,e+dd*.004],[.00065,.00038],6,0,f'apical_extension_{k}','apical_extension',tag)
 for k,pk in enumerate([0,1]):
  path,parent=paths[pk];b=path[1].lerp(path[2],.10);sgn=-1 if pk==0 else 1;end=b+Vector((sgn*.022,0,.025));tube(M,[b,b+Vector((sgn*.013,0,.005)),end],[.0009,.0009,.00105],6,0,f'secondary_lateral_{k}','secondary_lateral',parent)
 # Main narrow apical extension and a modest heteromorphic distal swelling.
 e=centers[-1];tube(M,[e-Vector((0,0,.0002)),e+Vector((.0008,0,.004))],[.0008,.00045],6,0,'main_apical_extension','apical_extension','main_cell_7')
 box(M,(.009,-.0058,.004),(.063,-.0041,.013),3,'label_plinth');text_label(M,(.036,-.00585,.0065),.005,0,'label_plinth')
 return M.emit('proterocladus-asymmetric-multiorder-relief-enlarged',m,col)

def toothed(M,b,d,L,W,T,mat,tag,parent):
 # Elliptic/obovate blade with eight clear low marginal teeth, closed mesh.
 outline=[(0,0)]
 for sign in [-1,1]:
  vals=[(.16,.22),(.31,.36),(.34,.28),(.47,.47),(.50,.36),(.63,.50),(.66,.40),(.79,.40),(.81,.30),(.91,.24)]
  if sign==1:vals=list(reversed(vals))
  for u,w in vals:outline.append((sign*w*W,u*L))
  if sign==-1:outline.append((0,L))
 prism(M,outline,b,d,(0,0,1),T,mat,tag,'leaflet',parent)

def quereuxia(c,m,col):
 p=c['parameters'];M=Mesh();rh=[Vector((-.020,0,0)),Vector((0,0,.002)),Vector((.020,.001,.001))];tube(M,rh,[.0011,.0013,.0010],7,4,'rhizome','rhizome')
 st=[rh[1],Vector((-.003,0,.030)),Vector((-.001,.001,.060)),Vector((0,0,.087))];tube(M,st,[.0011,.00105,.0009,.0008],7,0,'stem','upright_stem','rhizome')
 top=st[-1]
 for k in range(4):
  a=pi/2*k;d=Vector((cos(a),sin(a),.025*(-1 if k%2 else 1))).normalized();side=Vector((-sin(a),cos(a),0));b=top-Vector((0,0,.002*(k//2)));pe=b+d*.012;tag=f'compound_petiole_{k}';tube(M,[b,pe],[.0005,.00035],6,0,tag,'petiole','stem');re=pe+d*.026;rt=f'rachis_{k}';tube(M,[pe-d*.0001,re],[.00035,.00018],5,0,rt,'rachis',tag)
  for j in range(4):
   node=pe+d*(.0035+j*.0062)
   for sign in [-1,1]:
    ld=(side*sign*.91+d*.42).normalized();pet=f'leaflet_petiole_{k}_{j}_{sign}';le=node+ld*.0012;tube(M,[node,le],[.00020,.00014],4,0,pet,'leaflet_petiole',rt);toothed(M,le-ld*.0001,ld,p['leaflet_length_m'],p['leaflet_width_m'],p['leaflet_thickness_m'],1+(j+k)%2,f'leaflet_{k}_{j}_{sign}',pet)
  toothed(M,re-d*.00010,d,p['leaflet_length_m'],p['leaflet_width_m'],p['leaflet_thickness_m'],2,f'terminal_leaflet_{k}',rt)
 for k in range(4):
  a=pi/4+k*pi/2;d=Vector((cos(a),sin(a),.20));b=top+Vector((0,0,-.0005));pe=b+d*.004;tag=f'simple_petiole_{k}';tube(M,[b,pe],[.00030,.00016],5,0,tag,'simple_petiole','stem');toothed(M,pe-d*.00005,d,.010,.006,.00045,2,f'simple_leaf_{k}',tag)
 for k in range(4):
  z=.024+.014*k;idx=min(int(z/.03),2);node=st[idx].lerp(st[idx+1],(z-st[idx].z)/(st[idx+1].z-st[idx].z));ang=k*2.39996;out=Vector((cos(ang),sin(ang),.18)).normalized();side=Vector((-sin(ang),cos(ang),0));first=node+out*.010;tag=f'submerged_petiole_{k}';tube(M,[node,first],[.00035,.00026],5,3,tag,'submerged_petiole','stem')
  def divide(b,d,level,parent,path):
   for sign in [-1,1]:
    aa=sign*.43;dd=(d*cos(aa)+side*sin(aa)).normalized();L=[.010,.007,.005][level];e=b+dd*L;tag=f'filiform_{k}_{path}{sign+1}';r=[.00027,.00021,.00016][level];tube(M,[b,e],[r,r*.73],5,3,tag,'submerged_filiform_segment',parent)
    if level<2:divide(e-dd*.00003,dd,level+1,tag,path+str(sign+1))
  divide(first-out*.00005,out,0,tag,'')
 for k in range(3):
  b=rh[0].lerp(rh[2],k/2);b.z=0 if k==0 else .002 if k==1 else .001;d=Vector(((-1+k)*.3,-.15,-1)).normalized();e=b+d*.018;tag=f'root_{k}';tube(M,[b,b.lerp(e,.5),e],[.00055,.00032,.00009],5,4,tag,'root','rhizome')
  for j in range(2):
   bb=b.lerp(e,.35+j*.28);ee=bb+Vector(((-1 if j==0 else 1)*.005,.002*(-1+k),-.005));tube(M,[bb,ee],[.00018,.00005],4,4,f'root_lateral_{k}_{j}','root_lateral',tag)
 return M.emit('quereuxia-compound-floating-and-filiform-submerged-leaves',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update()
 export_asset(aid,aid,'plants',col,metadata={'representation':'living-reconstruction' if aid=='quereuxia' else 'fossil-specimen','export_texcoords':False,'source_scope':'Original batch99 pregeometry freeze. No source pixels or external meshes bundled.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':start,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
