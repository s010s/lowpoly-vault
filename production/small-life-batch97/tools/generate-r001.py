#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch97 geometry, authored strictly after original-v001 freeze."""
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

def leafvolume(M,outline,base,axis,side,T,mi,tag,fold=0):
 b=Vector(base);a=Vector(axis).normalized();s=Vector(side).normalized();n=s.cross(a).normalized();vv=[Vector((u,v,0)) for u,v in outline];ts=tessellate_polygon([vv]);lookup={tuple(v):i for i,v in enumerate(vv)};tri=[tuple(x if isinstance(x,int) else lookup[tuple(x)] for x in t) for t in ts];N=len(vv)
 def pp(u,v):return b+a*u+s*v+n*(fold*u)
 verts=[pp(u,v)+n*T*.5 for u,v in outline]+[pp(u,v)-n*T*.5 for u,v in outline];faces=tri+[tuple(i+N for i in reversed(t)) for t in tri]+[(j,(j+1)%N,(j+1)%N+N,j+N) for j in range(N)];M.add(verts,faces,mi,tag);return pp,n

def ginkgo(c,m,col):
 p=c['parameters'];M=Mesh();H=p['nominal_petiole_length_m'];T=p['nominal_lamina_thickness_m'];R=p['nominal_lamina_radius_m'];base=Vector((0,0,H));tube(M,[(0,0,0),(.001,0,H*.5),base+Vector((0,0,.005))],[.0010,.0011,.0013],6,0,'petiole')
 outline=[(-.001,H)];angles=[-1.02,-.61,-.20,.21,.62,1.03];rads=[.062,.075,.077,.073,.073,.059]
 for j,(a,r) in enumerate(zip(angles,rads)):
  if j:aa=(angles[j-1]+a)*.5;rr=.017 if j==3 else .034;outline.append((rr*sin(aa),H+rr*cos(aa)))
  for k in range(7):aa=a-.145+k*.29/6;rr=r*(.94+.06*sin(pi*k/6));outline.append((rr*sin(aa),H+rr*cos(aa)))
 outline.append((.001,H));fold=lambda x,z:.018*x+.0012*sin((z-H)/R*pi)
 polyvolume(M,outline,T,1,'six_lobed_lamina',fold)
 # Leaf surface follows the same explicit fold used by its solid, with vein ring intersecting lamina.
 def f(a,r):x=r*sin(a);z=H+r*cos(a);return Vector((x,fold(x,z)-T*.5-.000035,z))
 for j,(a,r) in enumerate(zip(angles,rads)):
  tag=f'radiating_vein_{j}';tube(M,[f(a,.002),f(a,r*.40)],[.00017,.00016],5,3,tag)
  for sign in [-1,1]:
   aa=a+sign*.055;tube(M,[f(a,r*.40),f(aa,r*.68)],[.00016,.000145],5,3,tag)
   for ss in [-1,1]:aaa=aa+ss*.032;tube(M,[f(aa,r*.68),f(aaa,r*.93)],[.000145,.00010],5,3,tag)
  M.contacts.append({'child':tag,'parent':'six_lobed_lamina'})
 M.contacts.append({'child':'six_lobed_lamina','parent':'petiole'});o=M.emit('six-lobed-jurassic-ginkgo-leaf',m,col);o['design_lobes']=6;o['design_terminal_veins']=24;o['design_petiole']=1

def ribbon(M,points,widths,thickness,side,mat,tag):
 v=[];side=Vector(side).normalized()
 for i,p in enumerate(points):
  p=Vector(p);a=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);n=a.cross(side).normalized()
  for sx,ny in [(1,0),(0,1),(-1,0),(0,-1)]:v.append(p+side*sx*widths[i]*.5+n*ny*thickness*.5)
 f=[(3,2,1,0)]
 for i in range(len(points)-1):
  for j in range(4):a=i*4+j;b=i*4+(j+1)%4;f.append((a,b,b+4,a+4))
 n=(len(points)-1)*4;f.append((n,n+1,n+2,n+3));M.add(v,f,mat,tag)

def dicranophyllum(c,m,col):
 p=c['parameters'];M=Mesh();H=p['axis_height_m']
 def stem(t):return Vector((.018*sin(t*pi*1.5),.012*sin(t*pi),H*t))
 tube(M,[stem(j/16) for j in range(17)],[.009*(1-.65*j/16) for j in range(17)],8,0,'slender_axis')
 for i in range(48):
  t=.07+.91*(i/47)**.80;a=i*2.399963;rad=Vector((cos(a),sin(a),0));side=Vector((-sin(a),cos(a),0));b=stem(t);length=.25*(.65+.35*sin(pi*t*.85));tag=f'leaf_{i:02d}';mid=b+rad*length*.20+Vector((0,0,length*.35));rootbend=b+rad*.012+Vector((0,0,-.002));ribbon(M,[b,rootbend,mid],[.0038,.0038,.0030],.00085,side,2+i%2,tag)
  # Narrow basal fork22deg, wider second fork40deg. Shared centers with intersecting widths, never disconnected tips.
  for s in [-1,1]:
   joint=mid+rad*length*.19+side*s*length*.045+Vector((0,0,length*.23));ribbon(M,[mid,joint],[.0032,.0024],.00075,side,2+i%2,tag)
   for ss in [-1,1]:end=joint+rad*length*.18+side*(s*.025+ss*.07)*length+Vector((0,0,length*.24));ribbon(M,[joint,end],[.0026,.00018],.00062,side,2+i%2,tag)
  M.contacts.append({'child':tag,'parent':'slender_axis'})
  # Small rhomboid cushion, visually subtle and embedded into the actual supporting axis.
  rr=.009*(1-.65*t);cb=b+rad*rr*.82;verts=[cb-side*.002,cb+Vector((0,0,.006)),cb+side*.002,cb-Vector((0,0,.006)),cb+rad*.0014,cb-rad*.0014];faces=[(4,j,(j+1)%4) for j in range(4)]+[(5,(j+1)%4,j) for j in range(4)];M.add(verts,faces,1,f'cushion_{i:02d}');M.contacts.append({'child':f'cushion_{i:02d}','parent':'slender_axis'})
 o=M.emit('slender-helical-doublefork-leafy-axis',m,col);o['design_leaves']=48;o['design_terminal_tips']=192;o['design_axes']=1;o['design_cushions']=48

def noeggerathia(c,m,col):
 p=c['parameters'];M=Mesh();H=p['nominal_rachis_length_m'];T=p['nominal_lamina_thickness_m']
 def axis(z):return Vector((.015*sin(z/H*pi),.003*sin(z/H*pi),z))
 tube(M,[axis(H*j/16) for j in range(17)],[.0025*(1-.85*j/16) for j in range(17)],6,0,'rachis')
 sizes=[.18,.35,.62,.84,1,1,.96,.87,.74,.60,.40,.22]
 for k in range(12):
  for sign in [-1,1]:
   z=.072+k*.034+(0.005 if sign>0 else 0);b=axis(z);L=.075*sizes[k];W=.043*sizes[k];d=Vector((sign*.88,0,.48)).normalized();side=Vector((-d.z,0,d.x));tag=f'pinnule_{k:02d}_{sign}';outline=[(0,-.0004),(L*.28,-W*.30),(L*.65,-W*.47)]
   # Broad rounded obovate distal rim; six shallow teeth, not long conifer tips.
   for j in range(13):a=-pi/2+j*pi/12;outline.append((L*(.72+.28*cos(a))*(1 if j%2==0 else .974),W*.5*sin(a)))
   outline.extend([(L*.28,W*.27),(0,.0004)]);pp,n=leafvolume(M,outline,b,d,side,T,1+(k%2),tag,fold=.015*sign)
   M.contacts.append({'child':tag,'parent':'rachis'})
   # Four equivalent radiating initial veins, eight terminals, no single pinnule midrib.
   vtag=f'fan_veins_{k:02d}_{sign}'
   for q in range(4):
    vv=(-.35+q*.70/3)*W;mid=pp(L*.48,vv*.42)+n*(T*.5+.000025);start=pp(L*.035,0)+n*(T*.5+.000025);tube(M,[start,mid],[.00014,.00012],4,3,vtag)
    for ss in [-1,1]:end=pp(L*.88,vv+ss*.045*W)+n*(T*.5+.000025);tube(M,[mid,end],[.00012,.00007],4,3,vtag)
   M.contacts.append({'child':vtag,'parent':tag})
 o=M.emit('sterile-twelve-pair-wedge-pinnule-frond',m,col);o['design_pinnule_pairs']=12;o['design_pinnules']=24;o['design_terminal_veins']=192

def bjuvia(c,m,col):
 p=c['parameters'];M=Mesh();L=p['nominal_leaf_length_m'];W=p['nominal_leaf_width_m'];T=p['nominal_lamina_thickness_m'];N=64
 def width(t):return W*.5*(sin(pi*t)**.38)*(.88+.12*t)
 outline=[]
 for sign,steps in [(-1,range(N+1)),(1,range(N-1,0,-1))]:
  for j in steps:t=j/N;outline.append((sign*width(t),L*t))
 fold=lambda x,z:.0006*sin(pi*z/L)+.015*abs(x)
 polyvolume(M,outline,T,1,'entire_strap_lamina',fold)
 pts=[(0,fold(0,L*t)-T*.3,L*t) for t in [0,.15,.4,.7,.94,1]];tube(M,pts,[.0014,.0021,.0018,.0012,.00055,.00015],8,0,'midrib');M.contacts.append({'child':'midrib','parent':'entire_strap_lamina'})
 for j in range(96):
  t=.035+j*.93/95
  for sign in [-1,1]:
   z=L*t;xx=width(t)*.965;pts=[]
   for f in [0,.4,1]:x=sign*xx*f;zz=z+.006*f*(1-t);pts.append((x,fold(x,zz)-T*.5-.00003,zz))
   tag=f'transverse_vein_{j:02d}_{sign}';tube(M,pts,[.00024,.00022,.00013],4,3,tag);M.contacts.append({'child':tag,'parent':'entire_strap_lamina'})
 o=M.emit('entire-strap-open-parallel-veins',m,col);o['design_laminae']=1;o['design_lateral_vein_rows']=96;o['design_reticulate_crossveins']=0

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'plants',col,metadata={'representation':'living-reconstruction' if aid=='dicranophyllum' else 'fossil-specimen','export_texcoords':False,'source_scope':'Immutable original brief and transparent prefreeze corrections. No copied reference pixels.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
