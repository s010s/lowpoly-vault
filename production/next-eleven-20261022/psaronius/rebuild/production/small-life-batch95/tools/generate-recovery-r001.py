#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exact batch95 Psaronius r002 lineage, bounded recovery-r001 root-mantle geometry repair."""
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
def wedge(M,b,d,L,W,mi,tag):
 b=Vector(b);a=Vector(d).normalized();normal=Vector((0,0,1));side=normal.cross(a).normalized();normal=a.cross(side).normalized()
 # Broad toothed outer edge, narrow physically embedded base.
 outline=[(-.07*W,0),(-.5*W,.88*L)]
 for j in range(9):outline.append(((-.5+j/8)*W,L*(1 if j%2==0 else .91)))
 outline.append((.07*W,0));vs=[b+side*x+a*y+normal*.00045 for x,y in outline]+[b+side*x+a*y-normal*.00045 for x,y in outline];n=len(outline);center=b+a*.55*L
 # Use polygon tessellation in local2D.
 vv=[Vector((x,y,0)) for x,y in outline];tri=tessellate_polygon([vv]);ind={tuple(v):i for i,v in enumerate(vv)};ff=[tuple((v if isinstance(v,int) else ind[tuple(v)]) for v in t) for t in tri];ff+=[tuple(n+i for i in reversed(t)) for t in ff.copy()];ff +=[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)];M.add(vs,ff,mi,tag)
def sphenophyllum(c,m,col):
 p=c['parameters'];M=Mesh();main=[(-.15,0,.018),(-.11,.012,.032),(-.06,.018,.055),(0,.005,.10),(.04,-.008,.17),(.06,.008,.24),(.043,.015,.31)];tube(M,main,[.0032,.0032,.0030,.0028,.0025,.0021,.0014],6,0,'main_axis')
 branches=[(1,[main[1],(-.13,.03,.08),(-.16,.025,.13),(-.17,.015,.18)]),(2,[main[2],(-.045,-.035,.10),(-.02,-.06,.15),(-.04,-.055,.20)]),(3,[main[3],(.08,.035,.12),(.13,.04,.16),(.16,.028,.21)])]
 nodes=[Vector(x) for x in main]
 for k,(idx,pts) in enumerate(branches):tube(M,pts,[.0027,.0023,.0018,.0011],6,0,f'lateral_axis_{k}');nodes.extend(Vector(x) for x in pts[1:]);M.contacts.append({'child':f'lateral_axis_{k}','parent':'main_axis','kind':'centerline junction at shared point'})
 divided=set([8,9,20,21,44,45,68,69]);hooks=set([9,21,45,69]);leaf=0
 for ni,b in enumerate(nodes):
  for j in range(6):
   a=j*2*pi/6+ni*.31;rad=Vector((cos(a),sin(a),.18+.18*sin(ni*1.7+j)));L=p['nominal_leaf_length_m']*(.82+.18*cos(ni*1.9+j)**2);base=b+rad*.0006
   if leaf in divided:
    side=Vector((-sin(a),cos(a),0));end=base+rad*L
    for s in [-1,1]:blade(M,base,end+side*s*.0032,.0026,(0,0,1),2+j%2,f'divided_leaf_{leaf}')
    if leaf in hooks:
     q=end+side*.0032;pts=[q-rad*.0015,q,q+rad*.002+Vector((0,0,.002)),q+rad*.0002+Vector((0,0,.004)),q-rad*.002+Vector((0,0,.003))];tube(M,pts,[.00055,.0005,.00042,.00032,.00018],5,1,f'hook_{leaf}')
   else:wedge(M,base,rad,L,p['nominal_leaf_width_m']*(.85+.15*cos(j)),2+j%2,f'wedge_leaf_{leaf}')
   M.contacts.append({'child':('divided_leaf_' if leaf in divided else 'wedge_leaf_')+str(leaf),'parent':'node axis','kind':'leaf base inside node radius'});leaf+=1
 for j in range(5):a=j*2*pi/5;start=Vector(main[0]);end=start+Vector((.025*cos(a),.025*sin(a),-.014));tube(M,[start,start.lerp(end,.5)+Vector((0,0,-.008)),end],[.0012,.0008,.00025],5,0,f'root_{j}')
 o=M.emit('open-scrambling-wedge-whorls',m,col);o['design_whorls']=16;o['design_leaves']=96;o['design_divided_leaves']=8;o['design_hooks']=4;o['design_axes']=4;o['design_roots']=5

def psaronius(c,m,col):
 p=c['parameters'];M=Mesh();H=p['trunk_height_m'];zs=[0,.18,.65,1.25,1.9,H];rs=[.23,.21,.15,.12,.10,.12];tube(M,[(0,0,z) for z in zs],rs,12,0,'root_mantle_core')
 # recovery-r001 attempt-d: retain 18 roots and the unchanged core/crown.
 # At the upper mantle, position each root against the actual 12-sided core
 # rather than a shared circumradius. The exposed crest continues across the
 # old 1.9m kink, then tapers into the core over staggered terminal intervals.
 def core_surface_radius(z,a):
  z=max(zs[0],min(zs[-1],z))
  k=next((i for i in range(len(zs)-1) if z<=zs[i+1]),len(zs)-2)
  r=rs[k]+(rs[k+1]-rs[k])*(z-zs[k])/(zs[k+1]-zs[k])
  delta=a%(pi/6)-pi/12
  return r*cos(pi/12)/cos(delta)
 for j in range(18):
  a=j*2*pi/18;pts=[];radii=[]
  end=H-.025-.050*(.5+.5*sin(j*2.399963))
  root_zs=[0,.18,.65,1.25,1.9,2.20,end-.105,end]
  for k,z in enumerate(root_zs):
   phase=k if k<5 else 4+(z-1.9)/.6
   aa=a+.035*sin(j*2+phase);radius=.031*(1-.7*z/H)
   old_r=next((rs[i]+(rs[i+1]-rs[i])*(z-zs[i])/(zs[i+1]-zs[i]) for i in range(len(zs)-1) if z<=zs[i+1]),rs[-1])
   if z<=1.25:rr=old_r*(.91+.03*sin(j*1.3))
   else:
    q=min(1,(z-1.25)/.65);q=q*q*(3-2*q)
    support=core_surface_radius(z+.018,aa)
    # Keep positive crest exposure until the final curved runout.
    rr=(1-q)*old_r*(.91+.03*sin(j*1.3))+q*(support-.32*radius)
    u=max(0,min(1,(z-(end-.20))/.20));u=u*u*(3-2*u)
    rr-=u*radius*1.05
   pts.append((rr*cos(aa),rr*sin(aa),z+.018));radii.append(radius)
  # Continuous root-local frame: the generic tangent cross global-Z frame
  # reverses when the core flares again near the crown. Never flip a ring.
  original_pts=[]
  for kk,(zz,rr0) in enumerate(zip(zs,rs)):
   aaa=a+.035*sin(j*2+kk);rr0*=.91+.03*sin(j*1.3);original_pts.append(Vector((rr0*cos(aaa),rr0*sin(aaa),zz+.018)))
  vv=[];sides=5
  for k,pp in enumerate(pts):
   pos=Vector(pp);t=(Vector(pts[min(k+1,len(pts)-1)])-Vector(pts[max(0,k-1)])).normalized()
   aa=math.atan2(pos.y,pos.x);u=Vector((-sin(aa),cos(aa),0));u=(u-t*u.dot(t)).normalized();w=t.cross(u).normalized()
   if k<4:
    # Preserve all four lower original rings exactly, including base silhouette.
    t,u,w=frame(original_pts[min(k+1,len(original_pts)-1)]-original_pts[max(0,k-1)])
   for q in range(sides):vv.append(pos+radii[k]*(u*cos(2*pi*q/sides)+w*sin(2*pi*q/sides)))
  ff=[tuple(range(sides))[::-1]]
  for k in range(len(pts)-1):
   for q in range(sides):v0=k*sides+q;v1=k*sides+(q+1)%sides;ff.append((v0,v1,v1+sides,v0+sides))
  ff.append(tuple(range((len(pts)-1)*sides,len(pts)*sides)));M.add(vv,ff,1+j%2,f'root_bundle_{j}')
 for f in range(8):
  a=f*2*pi/8+.08*sin(f);R=1.45*(.88+.12*cos(f*1.9)**2);rise=.50+.18*sin(f*1.8);rad=Vector((cos(a),sin(a),0));side=Vector((-sin(a),cos(a),0));base=Vector((0,0,H-.035))
  def path(t):return base+rad*(R*t)+Vector((0,0,rise*sin(pi*t*.85)-.25*t*t))
  tube(M,[path(t/8) for t in range(9)],[.024*(1-.85*t/8) for t in range(9)],5,2,f'frond_rachis_{f}')
  for k in range(7):
   t=.18+k*.105;b=path(t);span=.36*sin(pi*(t*.85))*(1-.33*t)
   for sign in [-1,1]:
    tip=b+side*(sign*span)+rad*.09+Vector((0,0,-.025));axis=tip-b
    tube(M,[b, b.lerp(tip,.55),tip],[.008*(1-.35*t),.004,.0012],4,2,f'pinna_{f}_{k}_{sign}')
    for q in range(5):
     u=.17+q*.15;bb=b.lerp(tip,u);ll=p['nominal_pinnule_length_m']*(1-.40*u)*(1-.15*t)
     for s in [-1,1]:
      end=bb+rad*(s*ll)+axis.normalized()*ll*.18+Vector((0,0,-.25*ll));blade(M,bb,end,p['nominal_pinnule_width_m']*(1-.40*u),(Vector((0,0,1))+side*.35*sign),3+(f+k+q)%2,f'pinnule_{f}_{k}_{sign}_{q}_{s}')
  M.contacts.append({'child':f'frond_rachis_{f}','parent':'root_mantle_core','kind':'base embedded in crown'})
 o=M.emit('root-mantled-tree-eight-bipinnate-fronds',m,col);o['design_root_bundles']=18;o['design_fronds']=8;o['design_pinnae']=112;o['design_pinnules']=1120

def hausmannia(c,m,col):
 p=c['parameters'];M=Mesh();N=128;K=5;R=p['nominal_radius_m'];T=p['nominal_lamina_thickness_m'];A=1.42
 def boundary(a):return R*(.92+.05*cos(a*1.7))*(1+.023*sin(a/A*16*2*pi)+.013*sin(a/A*8*2*pi))
 def point(a,t):
  r=boundary(a)*t;x=r*sin(a);z=r*cos(a);return Vector((x,.035*x+.015*z+.0018*sin(a*3)*t,z))
 v=[]
 # Distinct basal point avoids degenerate central ring.
 for back in [-1,1]:
  v.append(point(0,0)+Vector((0,back*T/2,0)))
  for k in range(1,K+1):
   for j in range(N+1):v.append(point(j/N*A,k/K)+Vector((0,back*T/2,0)))
 sidecount=1+K*(N+1);faces=[]
 for layer in [0,1]:
  off=layer*sidecount
  for j in range(N):faces.append((off,off+1+j,off+2+j))
  for k in range(K-1):
   for j in range(N):a=off+1+k*(N+1)+j;b=a+1;d=a+(N+1);faces.extend([(a,b,d+1),(a,d+1,d)])
 edge=[0]+[1+k*(N+1) for k in range(K)]+[1+(K-1)*(N+1)+j for j in range(1,N+1)]+[1+k*(N+1)+N for k in range(K-2,-1,-1)]
 faces.extend((edge[j],edge[(j+1)%len(edge)],edge[(j+1)%len(edge)]+sidecount,edge[j]+sidecount) for j in range(len(edge)))
 M.add(v,faces,1,'continuous_fan_lamina')
 def front(a,t):return point(a,t)+Vector((0,-T/2-.00012,0))
 # Four initial veins split into eight, then sixteen outward terminals.
 for j in range(4):
  a=(j+.5)/4*A;tube(M,[front(a*.8,.03),front(a,.35)],[.00042,.00032],5,3,f'major_initial_{j}')
  for s in [-1,1]:
   aa=a+s*A/16;tube(M,[front(a,.35),front(aa,.65)],[.00032,.00024],5,3,f'major_mid_{j}_{s}')
   for ss in [-1,1]:
    aaa=aa+ss*A/32;tube(M,[front(aa,.65),front(aaa,.98)],[.00024,.00012],5,3,f'major_terminal_{j}_{s}_{ss}')
 for k,t in enumerate([.28,.43,.58,.73,.88]):
  for j in range(15):
   aa=(j+.5)/16*A;bb=(j+1.5)/16*A;pts=[front(aa,t),front((aa+bb)/2,t+.012*sin(j*1.7)),front(bb,t)];tube(M,pts,[.00013]*3,4,2,f'net_cross_{k}_{j}')
 o=M.emit('continuous-paired-tooth-fossil-fan-sector',m,col);o['design_fan_sectors']=1;o['design_paired_teeth']=8;o['design_initial_veins']=4;o['design_terminal_veins']=16;o['design_crossbands']=5

def dictyophyllum(c,m,col):
 p=c['parameters'];M=Mesh();T=p['nominal_lamina_thickness_m'];base=Vector((0,0,.012));tube(M,[(0,0,.0006),base],[.0014,.0013],6,3,'short_petiole')
 for sign in [-1,1]:
  O=Vector((sign*.002,0,.014));angles=[.13,.43,.75,1.10];lens=[.052,.054,.049,.042];outline=[(O.x,O.z)]
  # Boundary walk: left edge of each ray outward, right edge inward, next ray via basal web.
  for k,(ang,L) in enumerate(zip(angles,lens)):
   d=Vector((sin(ang),0,cos(ang)));s=Vector((cos(ang),0,-sin(ang)));W=.0075*(1-.08*k)
   for side,steps in [(-1,range(15)),(1,range(14,-1,-1))]:
    for n in steps:
     t=.16+.84*n/14;half=W*.5*sin(pi*t)**.45*(1+.20*(1 if n%2 else -.25));q=O+Vector((sign,1,1))*(d*L*t+s*side*half)
     if n==14 and side==1:continue
     outline.append((q.x,q.z))
  # All four rays share a filled basal short web; no detached blade components.
  fold=lambda x,z:sign*.035*x+.008*z
  polyvolume(M,outline,T,1,'four_ray_web_'+str(sign),fold)
  tube(M,[base,O+Vector((0,fold(O.x,O.z),0))],[.0013,.0010],5,3,'basal_arm_'+str(sign))
  for k,(ang,L) in enumerate(zip(angles,lens)):
   d=Vector((sign*sin(ang),0,cos(ang)));s=Vector((sign*cos(ang),0,-sin(ang)));W=.0075*(1-.08*k)
   def f(t,off=0):
    q=O+d*(L*t)+s*off;q.y=fold(q.x,q.z)-T/2-.00010;return q
   tube(M,[f(0),f(.4),f(.78),f(.98)],[.00032,.00028,.00018,.00009],5,3,f'ray_midvein_{sign}_{k}')
   for j in range(6):
    t=.25+j*.105;half=W*.38*sin(pi*t)**.45
    for side in [-1,1]:
     tube(M,[f(t),f(t+.07,side*half)],[.00012,.00007],4,2,f'ray_sidevein_{sign}_{k}_{j}_{side}')
     if j<5:tube(M,[f(t+.07,side*half),f(t+.12,side*half*.6)],[.00008,.00007],4,2,f'ray_net_{sign}_{k}_{j}_{side}')
 o=M.emit('bifurcate-eight-lobate-rays-fossil-frond',m,col);o['design_basal_arms']=2;o['design_rays']=8;o['design_lobes_per_ray_side']=7;o['design_webs']=2

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'plants',col,metadata={'representation':'living-reconstruction' if aid in ['sphenophyllum','psaronius'] else 'fossil-specimen','export_texcoords':False,'source_scope':'Immutable original brief; all dimensions nominal artistic, actual world geometry measured; no third-party pixels.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
