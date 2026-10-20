#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch89 original geometry authored after original-freeze-manifest.json."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy
from mathutils import Vector
from math import sin,cos,pi
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  n=len(self.v);self.v+=v;self.f += [tuple(n+x for x in face) for face in f];self.mi += [mi]*len(f)
 def emit(self,name,m,col):
  o=mesh_object(name,self.v,self.f,m,col)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i
  return o

def tube(M,points,radii,sides,mat):
 v=[]
 for i,pp in enumerate(points):
  p=Vector(pp);t=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])).normalized();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();w=t.cross(u).normalized()
  for j in range(sides):v.append(tuple(p+radii[i]*(u*cos(2*pi*j/sides)+w*sin(2*pi*j/sides))))
 f=[tuple(range(sides))[::-1]]
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 f.append(tuple(range((len(points)-1)*sides,len(points)*sides)));M.add(v,f,mat)

def extrude(M,poly,z0,z1,mat):
 n=len(poly);v=[(x,y,z) for z in (z0,z1) for x,y in poly];f=[tuple(range(n))[::-1],tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)];M.add(v,f,mat)

def psilo(c,m,col):
 p=c['parameters'];M=Mesh();height=p['height_m'];N=p['radial_segments'];path=[]
 for i in range(13):
  t=i/12;path.append((.012*sin(t*2.2),.008*sin(t*3),height*t))
 tube(M,path,[.011*(1-i/14)**.9 for i in range(13)],N,0)
 for j in range(5):
  a=j*2*pi/5+.2;r=p['basal_anchorage_radius_m'];tube(M,[(0,0,.018),(.5*r*cos(a),.5*r*sin(a),.008),(r*cos(a),r*sin(a),.002)],[.005,.003,.001],5,0)
 def pair(q,a,serial):
  q=Vector(q);side=Vector((-sin(a),cos(a),0));out=Vector((cos(a),sin(a),0));L=p['sporangium_length_m'];r=p['sporangium_diameter_m']/2
  for sg in [-1,1]:
   neck=q+side*sg*.0037+out*.002+Vector((0,0,-.002));tube(M,[q,neck,neck+Vector((0,0,-.004))],[.001,.0008,.0007],5,1)
   pts=[neck+Vector((0,0,-.002)),neck+out*.001+Vector((0,0,-L*.28)),neck+out*.0015+Vector((0,0,-L*.60)),neck+out*.002+Vector((0,0,-L))]
   tube(M,pts,[r*.28,r,r*.82,r*.08],7,2 if serial%4 else 3)
 def fork(q,a,L,level,fertile,serial):
  q=Vector(q);direction=Vector((cos(a),sin(a),.33 if fertile else .6));end=q+direction*L;mid=q.lerp(end,.55)+Vector((0,0,L*.12));rad=.0010+.0005*level
  tube(M,[q,mid,end],[rad,rad*.78,rad*.62],N,1 if level<2 else 0)
  if level==0:
   if fertile:pair(end,a,serial)
   return
  for sign in [-1,1]:fork(end,a+sign*(.48 if level>1 else .62),L*.61,level-1,fertile,serial*2+(sign+1)//2)
 for i in range(p['spray_count']):
  z=.15+i*.073;a=[.25,2.63,4.70,1.29,3.78,5.54,2.2][i];q=Vector((.012*sin((z/height)*2.2),.008*sin((z/height)*3),z));L=.090*(1-.03*i)
  fork(q,a,L,p['fork_depth'],i not in (0,4),i)
 # Unequal upper dichotomy, subordinate naked apical fork.
 tube(M,[path[-3],(.054,.009,.675),(.075,.012,.705)],[.0035,.0020,.0010],N,0)
 minz=min(v[2] for v in M.v);M.v=[(x,y,z-minz) for x,y,z in M.v];M.emit('dominant-naked-axis-dichotomized-sprays-paired-sporangia',m,col)

def ross(c,m,col):
 p=c['parameters'];M=Mesh();A=p['radial_segments_half'];K=p['vertical_segments'];H=p['height_m'];R=p['block_radius_m'];rt=p['central_tube_radius_m'];layers=p['concentric_layers'];S=4
 def radius(b,t,a):
  if b==0:return 0
  if b==1:return rt
  if b==layers+2:return R*(1+.025*sin(3*a+.4))
  cone=p['cone_bottom_radius_m']+(p['cone_top_radius_m']-p['cone_bottom_radius_m'])*t**1.55
  return rt+(cone-rt)*(b-1)/layers
 # Distinct closed envelopes; real shallow front convex ribs and top grooves expose their volumes.
 for band in range(layers+2):
  if band==0:
   v=[(rt*cos(pi*j/A),rt*sin(pi*j/A),z) for z in [0,H] for j in range(A+1)];n=A+1;f=[tuple(range(n))[::-1],tuple(range(n,2*n))]+[(j,j+1,j+1+n,j+n) for j in range(A)]+[(A,0,n,2*n-1)];M.add(v,f,4);continue
  v=[]
  def idx(k,s,j):return (k*(S+1)+s)*(A+1)+j
  for k in range(K+1):
   t=k/K
   for ss in range(S+1):
    u=ss/S;relief=sin(pi*u) if band<=layers else 0
    for j in range(A+1):
     a=pi*j/A;r=radius(band,t,a)*(1-u)+radius(band+1,t,a)*u
     y=r*sin(a)-.00058*relief*math.exp(-10*sin(a))*sin(pi*(.1+.8*t))
     z=H*t-(.00035*relief if k==K else 0)
     v.append((r*cos(a),y,z))
  f=[]
  for k in range(K):
   for j in range(A):
    for ss in [0,S]:f.append((idx(k,ss,j),idx(k+1,ss,j),idx(k+1,ss,j+1),idx(k,ss,j+1)))
  for ss in range(S):
   for j in range(A):
    for k in [0,K]:f.append((idx(k,ss,j),idx(k,ss+1,j),idx(k,ss+1,j+1),idx(k,ss,j+1)))
  for k in range(K):
   for ss in range(S):
    for j in [0,A]:f.append((idx(k,ss,j),idx(k+1,ss,j),idx(k+1,ss+1,j),idx(k,ss+1,j)))
  # Remove unused interior lattice vertices before audit; surface is closed and connected.
  used=sorted(set(q for face in f for q in face));remap={q:i for i,q in enumerate(used)};M.add([v[q] for q in used],[tuple(remap[q] for q in face) for face in f],0 if band==layers+1 else 1 if band%2 else 2 if band%4 else 3)
 M.emit('volumetric-concentric-funnel-exposed-ribs',m,col)

def skolithos(c,m,col):
 p=c['parameters'];M=Mesh();W,D,H=p['block_dimensions_m'];
 poly=[(-.05,-.035),(-.040,-.035),(-.040,-.015),(-.020,-.015),(-.020,-.008),(.012,-.008),(.012,-.019),(.041,-.019),(.041,-.035),(.05,-.035),(.05,.035),(-.05,.035)]
 extrude(M,poly,0,H,0);host=M.emit('sectioned-host-sandstone',m,col)
 positions=[(-.03,-.015,.0044),(-.003,-.008,.0035),(.028,-.019,.0048),(-.035,.020,.0032),(-.010,.018,.0042),(.016,.018,.0026),(.036,.023,.0036)]
 for i,(x,y,r) in enumerate(positions):
  cutter=Mesh();tube(cutter,[(x,y,-.001),(x,y,H+.001)],[r,r],p['shaft_radial_segments'],0);o=cutter.emit('temporary-shaft-cutter',m,col)
  bpy.context.view_layer.objects.active=host;mod=host.modifiers.new('exact-shaft-negative','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(o,do_unlink=True)
  # Filled shaft is exact hole complement, no coplanar surface overlay: host top has real hole.
  shaft=Mesh();tube(shaft,[(x,y,0),(x,y,H+.0006)],[r*.999,r*.999],p['shaft_radial_segments'],2);shaft.emit('continuous-filled-vertical-shaft-%02d'%i,m,col)
 # Join all intact source meshes into one editable multi-material mesh; closed components kept.
 objs=[o for o in bpy.data.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=host;bpy.ops.object.join()

def teich(c,m,col):
 p=c['parameters'];M=Mesh();W,D,T=p['slab_dimensions_m'];poly=[(-W*.5,-D*.40),(-W*.39,-D*.50),(W*.40,-D*.48),(W*.50,-D*.29),(W*.47,D*.42),(W*.19,D*.50),(-W*.44,D*.44),(-W*.5,D*.13)]
 extrude(M,poly,0,T,0);M.emit('irregular-illustrative-sediment-slab',m,col)
 L=p['wall_length_m'];N=p['length_segments'];Q=p['gutter_cross_sections'];step=(p['wall_height_m']-.006)/p['lamina_count'];width=p['wall_thickness_m'];M=Mesh();S=4
 for layer in range(p['lamina_count']):
  v=[]
  def idx(s,i,j):return (s*(N+1)+i)*(Q+1)+j
  for ss in range(S+1):
   f=ss/S
   for i in range(N+1):
    x=-L/2+L*i/N;und=.00065*sin(x/L*2*pi+.5)+.0004*cos(i*.71)
    for j in range(Q+1):
     u=-1+2*j/Q;y=width*.5*u+.0008*sin(i*.4)+.00115*sin(pi*f)*u**3;z=T+layer*step+f*step+.0036*u*u+und;v.append((x,y,z))
  faces=[]
  for i in range(N):
   for j in range(Q):
    for ss in [0,S]:faces.append((idx(ss,i,j),idx(ss,i+1,j),idx(ss,i+1,j+1),idx(ss,i,j+1)))
  for ss in range(S):
   for i in range(N):
    for j in [0,Q]:faces.append((idx(ss,i,j),idx(ss+1,i,j),idx(ss+1,i+1,j),idx(ss,i+1,j)))
   for j in range(Q):
    for i in [0,N]:faces.append((idx(ss,i,j),idx(ss+1,i,j),idx(ss+1,i,j+1),idx(ss,i,j+1)))
  used=sorted(set(q for face in faces for q in face));remap={q:i for i,q in enumerate(used)};M.add([v[q] for q in used],[tuple(remap[q] for q in face) for face in faces],1 if layer%2 else 2)
 pts=[]
 for i in range(N+1):
  x=-L/2+L*i/N;pts.append((x,.0008*sin(i*.4),T+p['lamina_count']*step+.0012+.00065*sin(x/L*2*pi+.5)+.0004*cos(i*.71)))
 tube(M,pts,[p['causative_tunnel_radius_m']]*(N+1),12,3);M.emit('gutter-laminae-with-real-layer-edge-relief',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])]
 {'psilophyton':psilo,'rosselia-concentrically-filled-burrow':ross,'skolithos-pipe-field':skolithos,'teichichnus-spreite-wall':teich}[aid](cfg,m,col);bpy.context.view_layer.update()
 export_asset(aid,aid,'plants' if aid=='psilophyton' else 'traces',col,metadata={'representation':'living-reconstruction' if aid=='psilophyton' else 'trace-concept','export_texcoords':False,'source_scope':'Immutable original-brief.json; original geometry; no creator species for trace.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
