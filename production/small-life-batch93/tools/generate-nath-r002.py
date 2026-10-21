#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch93 original volumetric geometry, written after full original freeze."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from math import sin,cos,pi
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Mesh:
 def __init__(self): self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  n=len(self.v);self.v.extend([tuple(x) for x in v]);self.f.extend([tuple(n+x for x in face) for face in f]);self.mi.extend([mi]*len(f))
 def emit(self,name,m,col,weld=False):
  o=mesh_object(name,self.v,self.f,m,col)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i
  bm=bmesh.new();bm.from_mesh(o.data)
  if weld:bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();return o
 def normalize_height(self,H):
  lo=min(v[2] for v in self.v);hi=max(v[2] for v in self.v);s=H/(hi-lo);self.v=[(x*s,y*s,(z-lo)*s) for x,y,z in self.v]
def frame(axis):
 t=Vector(axis).normalized();u=t.cross(Vector((0,0,1)))
 if u.length<.01:u=t.cross(Vector((0,1,0)))
 u.normalize();return t,u,t.cross(u).normalized()
def tube(M,points,radii,sides,mat):
 v=[]
 for i,pp in enumerate(points):
  p=Vector(pp);t,u,w=frame(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]))
  for j in range(sides):v.append(p+radii[i]*(u*cos(2*pi*j/sides)+w*sin(2*pi*j/sides)))
 f=[tuple(range(sides))[::-1]]
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 f.append(tuple(range((len(points)-1)*sides,len(points)*sides)));M.add(v,f,mat)
def blade(M,base,tip,width,normal,mi):
 b=Vector(base);e=Vector(tip);a=e-b;n=Vector(normal).normalized();side=n.cross(a).normalized();c=b+a*.37
 v=[b,e,c+side*width*.5,c+n*width*.12,c-side*width*.5,c-n*width*.12];f=[]
 for j in range(4):x=2+j;y=2+(j+1)%4;f.extend([(0,x,y),(1,y,x)])
 M.add(v,f,mi)
def oval(M,center,rad,mi):
 c=Vector(center);x,y,z=rad;v=[c+Vector(d) for d in [(x,0,0),(-x,0,0),(0,y,0),(0,-y,0),(0,0,z),(0,0,-z)]];f=[(4,0,2),(4,2,1),(4,1,3),(4,3,0),(5,2,0),(5,1,2),(5,3,1),(5,0,3)];M.add(v,f,mi)
def roots(M,n,r,z,thickness):
 for j in range(n):
  a=j*2*pi/n+.12*sin(j*1.7);R=r*(.85+.12*sin(j*2.3));tube(M,[(.24*R*cos(a),.24*R*sin(a),z),(.48*R*cos(a+.07),.48*R*sin(a+.07),z*.63),(.8*R*cos(a+.10),.8*R*sin(a+.10),z*.15),(R*cos(a+.14),R*sin(a+.14),thickness*.2)],[thickness,thickness*.75,thickness*.37,thickness*.14],5,0)
def stem(M,height,r,baseR,baseH,ribs=0):
 n=48 if ribs else 16;v=[];zs=[.003,baseH*.20,baseH*.60,baseH,height*.8,height]
 rs=[baseR*.55,baseR,baseR*.86,r,r*.78,r*.48]
 for i,(z,rr) in enumerate(zip(zs,rs)):
  for j in range(n):
   a=2*pi*j/n;rho=rr*(1+(.07*cos(ribs*a) if ribs and i<4 else 0));v.append((rho*cos(a),rho*sin(a),z))
 f=[tuple(range(n))[::-1]]
 for i in range(len(zs)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;f.append((a,b,b+n,a+n))
 f.append(tuple(range((len(zs)-1)*n,len(zs)*n)));M.add(v,f,0)
def nathorstiana(c,m,col):
 p=c['parameters'];M=Mesh();stem(M,p['stem_height_m'],p['stem_radius_m'],p['base_radius_m'],p['base_height_m'],p['basal_meridional_ribs']);roots(M,p['root_count'],.080,.025,.0015)
 for j in range(p['leaf_count']):
  a=j*2.399963;t=j/(p['leaf_count']-1);spread=.025+.060*(.5+.5*sin(j*1.9));z=p['stem_height_m']-.008+.006*t;L=p['leaf_length_m']*(.82+.18*sin(j*2.4)**2);b=Vector((.003*cos(a),.003*sin(a),z));e=b+Vector((spread*cos(a),spread*sin(a),math.sqrt(max(.001,L*L-spread*spread))));blade(M,b,e,p['leaf_width_m'],(cos(a),sin(a),.15),2+j%2)
 M.normalize_height(p['art_total_height_m']);o=M.emit('short-unbranched-stem-quill-crown-ribbed-rooting-base',m,col);o['design_leaf_count']=20;o['design_root_count']=18;o['reproductive_organs']='absent, unknown in selected evidence'
def chaloneria(c,m,col):
 p=c['parameters'];M=Mesh();H=p['stem_height_m'];stem(M,H,p['stem_radius_m'],p['corm_radius_m'],p['corm_height_m']);roots(M,p['root_count'],.22,.075,.009)
 for j in range(p['vegetative_leaf_count']):
  t=j/(p['vegetative_leaf_count']-1);z=.20+t*(H*.66-.20);a=j*2.399963;L=p['leaf_length_m']*(.85+.15*sin(j*1.4));b=Vector((.016*cos(a),.016*sin(a),z));e=b+Vector((L*.78*cos(a),L*.78*sin(a),L*(.32+.38*t)));blade(M,b,e,p['leaf_width_m'],(cos(a),sin(a),.15),2+j%2)
 for j in range(p['fertile_leaf_count']):
  t=j/(p['fertile_leaf_count']-1);z=H*(.66+.34*t);a=j*2.399963;L=.16*(1-.6*t);r=.015*(1-.3*t);b=Vector((r*.7*cos(a),r*.7*sin(a),z));e=b+Vector((L*.48*cos(a),L*.48*sin(a),L*.88));blade(M,b,e,.009*(1-.45*t),(cos(a),sin(a),.12),2+j%2);band=min(3,int(t*4));sr=.008 if band%2==0 else .006;oval(M,((r+sr*.40)*cos(a),(r+sr*.40)*sin(a),z+.006),(sr,sr,.012),4 if band%2==0 else 1)
 M.normalize_height(p['art_total_height_m']);o=M.emit('unbranched-cormose-plant-continuous-fertile-apex',m,col);o['design_vegetative_leaves']=112;o['design_fertile_leaves']=72;o['design_fertile_alternating_regions']=4

def omphalophloios(c,m,col):
 p=c['parameters'];M=Mesh();H=p['trunk_height_m'];tube(M,[(0,0,.02),(.015,0,.22),(.025,.012,H)],[p['trunk_radius_m']*1.2,p['trunk_radius_m'],.07],10,0);roots(M,p['root_count'],.42,.20,.042)
 terminals=[];branches=[]
 def split(start,direction,order,r,index):
  if order==p['dichotomy_orders']:
   L=.47;end=start+direction*L;tube(M,[start-direction*r*.6,start.lerp(end,.55),end],[r,r*.74,r*.27],6,0);terminals.append((start,end,r,index));return
  L=[.48,.40,.34,.29,.25][order];axis,u,w=frame(direction);ang=order*1.37+index*.41;spread=u*cos(ang)+w*sin(ang)
  for side in [-1,1]:
   d=(axis*.90+spread*side*.40+Vector((0,0,.12))).normalized();end=start+d*L;nr=r*.72;tube(M,[start-axis*r*.8,start.lerp(end,.53),end],[r,nr*1.15,nr],7,0);branches.append((start,end));split(end,d,order+1,nr,index*2+(1 if side>0 else 0))
 split(Vector((.025,.012,H)),Vector((0,0,1)),0,.060,1)
 for s,e,r,idx in terminals:
  ax,u,w=frame(e-s)
  for j in range(p['terminal_leaves_per_axis']):
   t=.12+j*.075;a=j*2.399963+idx*.31;rad=u*cos(a)+w*sin(a);b=s.lerp(e,t);L=p['leaf_length_m']*(1-.38*t);tip=b+rad*L*.70+ax*L*.66;blade(M,b-rad*r*.2,tip,p['leaf_width_m']*(1-.45*t),rad,2+j%2)
   if j>=4:oval(M,b+rad*r*.8+ax*.013,(.012,.012,.020),4)
 # Modest proximal foliage on second-order axes, not giant terminal rosettes.
 for k,(s,e) in enumerate(branches[:14]):
  ax,u,w=frame(e-s)
  for j in range(3):
   b=s.lerp(e,.35+.2*j);rad=u*cos(k+j*2.4)+w*sin(k+j*2.4);blade(M,b,b+rad*.17+ax*.10,.015,rad,2+(j%2))
 M.normalize_height(p['art_total_height_m']);o=M.emit('five-order-dichotomous-crown-elongated-fertile-axes',m,col);o['design_dichotomy_orders']=5;o['design_terminal_axis_count']=len(terminals);o['design_terminal_leaf_count']=len(terminals)*12;o['design_sporangia_count']=len(terminals)*8

def diplopora(c,m,col):
 p=c['parameters'];M=Mesh();N=p['pores_per_whorl'];K=p['annular_segments']*p['pore_whorls_per_segment'];H=p['art_fragment_height_m'];R=p['outer_radius_m'];ri=p['inner_radius_m']
 def point(t,z,inside=False):
  a=t*2*pi;wav=p['rim_irregularity_m']*(.55*sin(a*3)+.3*cos(a*5));zz=z*H+wav*(abs(z-.5)*2)**9
  rr=ri if inside else R-p['annular_groove_depth_m']*math.exp(-(sin(pi*3*z)/.14)**2)
  return (rr*cos(a),rr*sin(a),zz)
 # Each rectangular parameter-space cell is an annular patch with an octagonal pore.
 border=[(-.5,-.5),(0,-.5),(.5,-.5),(.5,0),(.5,.5),(0,.5),(-.5,.5),(-.5,0)]
 for k in range(K):
  for j in range(N):
   tc=(j+.5)/N;zc=(k+.5)/K;hole=[(p['pore_half_cell_angular_fraction']*cos(-3*pi/4+i*pi/4),p['pore_half_cell_axial_fraction']*sin(-3*pi/4+i*pi/4)) for i in range(8)]
   # Align octagon angles with corresponding perimeter corners, clockwise mapping.
   hole=[(p['pore_half_cell_angular_fraction']*x/math.hypot(x,y),p['pore_half_cell_axial_fraction']*y/math.hypot(x,y)) for x,y in border]
   v=[]
   for inside in [False,True]:
    for ring in [border,hole]:v.extend([point(tc+x/N,zc+y/K,inside) for x,y in ring])
   f=[]
   for i in range(8):q=(i+1)%8;f.extend([(i,q,8+q,8+i),(16+q,16+i,24+i,24+q),(8+i,8+q,24+q,24+i)])
   M.add(v,f,0 if (j+k)%7 else 2)
 # Annular top and bottom faces bridge inner/outer wall, lumen remains truly open.
 for z in [0,1]:
  for j in range(N*2):
   t=j/(N*2);u=(j+1)/(N*2);M.add([point(t,z),point(u,z),point(u,z,True),point(t,z,True)],[(0,1,2,3)],1)
 lo=min(v[2] for v in M.v);M.v=[(x,y,z-lo) for x,y,z in M.v];o=M.emit('annulated-fossil-wall-96-through-pores-open-lumen',m,col,True);o['design_real_radial_channels']=N*K;o['design_annular_segments']=3;o['design_pore_whorls']=6;o['physical_scope']='enlarged fossil fragment; not whole living thallus'
 # Every shell edge should have exactly two incident faces: open lumen is bounded by annular rims.
 bm=bmesh.new();bm.from_mesh(o.data);assert all(len(e.link_faces)==2 for e in bm.edges);bm.free()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'plants' if aid!='diplopora' else 'algae',col,metadata={'representation':'living-reconstruction' if aid!='diplopora' else 'fossil-specimen-concept','export_texcoords':False,'source_scope':'Immutable original-brief.json. Original volumetric geometry; nominal artistic scales; genus/species limitations explicit.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
