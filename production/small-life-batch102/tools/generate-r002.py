#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch102 geometry, authored strictly after original-v001 freeze."""
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

def arborea(c,m,col):
 p=c['parameters'];M=Mesh();H=p['frond_height_m'];B=p['frond_base_z_m'];W=p['frond_width_m'];T=p['backing_thickness_m'];N=p['rows_per_side']
 def half(t):return W*.5*max(0,sin(pi*t))**.67
 outline=[(half(k/40),B+H*k/40) for k in range(41)]+[(-half(k/40),B+H*k/40) for k in range(39,0,-1)]
 polyvolume(M,outline,T,0,'continuous_backing')
 tube(M,[(0,0,.004),(0,0,B+.015),(0,0,B+H*.94)],[p['stem_radius_m'],.006,.0012],8,0,'stalk_and_rachis');M.contacts.append({'child':'continuous_backing','parent':'stalk_and_rachis'})
 oval(M,(0,0,.0045),(p['holdfast_radius_m'],p['holdfast_radius_m'],.0045),0,'discoidal_holdfast',24);M.contacts.append({'child':'stalk_and_rachis','parent':'discoidal_holdfast'})
 for side in [-1,1]:
  for k in range(N):
   t=.028+.928*k/(N-1);z=B+H*t;rise=min(.017,H*(1-t)*.35);xmax=half(t+rise/H)*.89;a=Vector((side*.0018,-.0014,z));b=Vector((side*xmax,-.0014,z+rise));d=(b-a).normalized();trans=Vector((-d.z,0,d.x));v=[];S=6;steps=12
   for q in range(steps+1):
    u=q/steps;ctr=a+(b-a)*u;width=.00345*(.37+.63*sin(pi*u)**.5);dep=.0020*(.48+.52*sin(pi*u)**.5)
    # Five subtle ridges on a continuous module shell, alternating plateau positions.
    ridge=.00038 if q in [2,4,6,8,10] else 0
    for j in range(S):aa=2*pi*j/S;v.append(ctr+trans*(width*cos(aa))+Vector((0,(dep+ridge)*sin(aa),0)))
   f=[tuple(range(S))[::-1]]
   for q in range(steps):
    for j in range(S):i=q*S+j;ni=q*S+(j+1)%S;f.append((i,ni,ni+S,i+S))
   f.append(tuple(range(steps*S,(steps+1)*S)));tag=f'pod_{side}_{k:02d}';M.add(v,f,1+(k%3==0),tag);M.contacts.append({'child':tag,'parent':'continuous_backing'})
 o=M.emit('arborea-paddle-with-simple-pods',m,col);o['design_pod_rows']=2;o['design_pods']=64;o['design_integral_unit_cues_per_pod']=5

def swartpuntia(c,m,col):
 p=c['parameters'];M=Mesh();H=p['height_m'];W=p['vane_radius_m'];T=p['vane_thickness_m']
 def width(t):return W*(.16+.84*sin(pi*t)**.60)*(1-.67*t)
 tube(M,[(0,0,.001),(0,0,H*.5),(0,0,H-.001)],[p['axis_radius_m']*.8,p['axis_radius_m'],.0017],9,0,'nodular_axis')
 for j in range(3):
  ang=2*pi*j/3;start=len(M.v);outline=[(.001,.001)]+[(width(t),H*t) for t in [k/32 for k in range(33)]]+[(.001,H-.001)];tag=f'vane_{j}';polyvolume(M,outline,T,1,tag)
  # Ribs are narrow straight tubes on the anterior face of each vane. Their
  # grade increases smoothly distally, and endpoints remain within boundary.
  for k in range(p['modules_per_vane']):
   z=.0025+(H-.006)*k/(p['modules_per_vane']-1);t=z/H;slope=.05+.95*t**1.5;x=.004
   hi=width(t)
   for _ in range(25):hi=min(hi,width(min(.999,(z+(hi-x)*slope)/H))*.985)
   endz=z+(hi-x)*slope
   ribstart=len(M.v);rt=f'module_{j}_{k:02d}';tube(M,[(x,0,z),(hi,0,endz)],[p['module_radius_m']*.94,p['module_radius_m']*.78],6,2+(k%7==0),rt);M.contacts.append({'child':rt,'parent':tag})
   for vi in range(ribstart,len(M.v)):xx,yy,zz=M.v[vi];M.v[vi]=(xx,yy*2,zz)
  for i in range(start,len(M.v)):x,y,z=M.v[i];M.v[i]=(x*cos(ang)-y*sin(ang),x*sin(ang)+y*cos(ang),z)
  M.contacts.append({'child':tag,'parent':'nodular_axis'})
 for j in range(p['axis_node_sectors']):
  a=2*pi*(j+.5)/3
  for k in range(p['axis_nodes_per_sector']):
   z=.006+(H-.015)*(k+.17*j)/(p['axis_nodes_per_sector']);rad=p['axis_radius_m']*(1-.4*z/H);tag=f'axis_node_{j}_{k:02d}';oval(M,(rad*cos(a),rad*sin(a),z),(.0019,.0019,.0028),0,tag,8);M.contacts.append({'child':tag,'parent':'nodular_axis'})
 o=M.emit('stemless-three-vaned-swartpuntia',m,col);o['design_vanes']=3;o['design_modules_per_vane']=60;o['design_external_stems']=0

def coronacollina(c,m,col):
 p=c['parameters'];M=Mesh();N=24;rb=p['cone_base_radius_m'];rr=p['cone_rim_radius_m'];H=p['cone_height_m'];v=[(0,0,0)];rings=[(rb,0),(rb*.85,H*.45),(rr,H),(rr*.55,H-p['recess_depth_m'])]
 for r,z in rings:
  for j in range(N):a=2*pi*j/N;node=(p['rim_node_height_m']*max(0,cos(3*a))**8 if z==H else 0);v.append((r*cos(a),r*sin(a),z+node))
 v.append((0,0,H-p['recess_depth_m']));f=[]
 for j in range(N):a=1+j;b=1+(j+1)%N;f.append((0,b,a))
 for k in range(3):
  for j in range(N):a=1+k*N+j;b=1+k*N+(j+1)%N;f.append((a,b,b+N,a+N))
 for j in range(N):f.append((len(v)-1,1+3*N+j,1+3*N+(j+1)%N))
 M.add(v,f,0,'rimmed_cone')
 for k,(L,deg) in enumerate(zip(p['spicule_lengths_m'],p['spicule_angles_deg'])):
  a=deg*pi/180;u=Vector((cos(a),sin(a),0));root=u*(rr*.88)+Vector((0,0,H-.0005));drop=root.z-p['spicule_radius_m'];tip=root+u*math.sqrt(L*L-drop*drop)+Vector((0,0,-drop));tag=f'spicule_{k}';tube(M,[root,tip],[p['spicule_radius_m']]*2,6,2+(k%2),tag);M.contacts.append({'child':tag,'parent':'rimmed_cone'})
 o=M.emit('low-cone-four-rigid-spicules',m,col);o['design_spicules']=4;o['design_rim_nodes']=3

def echmatocrinus(c,m,col):
 p=c['parameters'];M=Mesh();N=p['body_plate_sectors'];R=p['body_plate_rows'];H=p['stalk_height_m']+p['cup_height_m'];base=p['attachment_height_m']*.55;v=[]
 def radius(t):return .00125+(p['cup_radius_m']-.00125)*t**.90
 # Irregular ring nodes and triangle-center relief form a single closed body,
 # not overlapping detached armor. Each cell is an identifiable plate region.
 for k in range(R+1):
  t=k/R
  for j in range(N):a=2*pi*j/N+.065*sin(k*1.8+j*.6);z=base+H*t+(.0007*sin(j*2.1+k) if k not in [0,R] else 0);r=radius(t)*(1+.025*sin(j*1.8+k*2.3));v.append((r*cos(a),r*sin(a),z))
 f=[]
 for k in range(R):
  for j in range(N):
   ids=[k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j];ctr=sum((Vector(v[i]) for i in ids),Vector())/4;out=Vector((ctr.x,ctr.y,0)).normalized();ci=len(v);v.append(ctr+out*p['plate_relief_m']);f.extend((ids[q],ids[(q+1)%4],ci) for q in range(4))
 f.append(tuple(range(N))[::-1]);v.append((0,0,base+H-.00045));center=len(v)-1
 for j in range(N):f.append((center,R*N+j,R*N+(j+1)%N))
 M.add(v,f,1,'integral_plated_body');offset=len(M.f)-len(f)
 for k in range(R):
  for j in range(N):
   for q in range(4):M.mi[offset+(k*N+j)*4+q]=[1,2,4][(j*5+k*7)%3]
 oval(M,(0,0,.00075),(p['attachment_radius_m'],p['attachment_radius_m'],.00075),0,'small_attachment',12);M.contacts.append({'child':'integral_plated_body','parent':'small_attachment'})
 for j in range(p['arm_count']):
  a=2*pi*j/p['arm_count'];u=Vector((cos(a),sin(a),0));side=Vector((-sin(a),cos(a),0));points=[];radii=[]
  for k in range(p['arm_segments']+1):
   t=k/p['arm_segments'];points.append(u*(p['cup_radius_m']*.94+p['arm_radial_reach_m']*sin(t*pi*.48))+Vector((0,0,base+H-.00045+p['arm_vertical_rise_m']*t)));radii.append(p['arm_radius_m']*(1-.48*t)*(1+.12*(k%2)))
  tag=f'arm_{j}';tube(M,points,radii,7,1+(j%2),tag);M.contacts.append({'child':tag,'parent':'integral_plated_body'})
  for k in range(p['soft_projections_per_arm']):
   t=(k+1)/(p['soft_projections_per_arm']+1);q=t*p['arm_segments'];lo=int(q);ctr=points[lo].lerp(points[min(lo+1,len(points)-1)],q-lo);sgn=1 if k%2==0 else -1;tip=ctr+side*sgn*p['soft_projection_length_m']+u*.00045+Vector((0,0,.00045));pt=f'soft_process_{j}_{k}';tube(M,[ctr,tip],[.00037,.00012],5,3,pt);M.contacts.append({'child':pt,'parent':tag})
 o=M.emit('eight-arm-irregular-plated-cone',m,col);o['design_arms']=8;o['design_soft_projections_per_arm']=6;o['design_integral_plate_regions']=R*N

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());aid=cfg['asset_id'];out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'fossils',col,metadata={'representation':'fossil-form-interpretation' if aid!='echmatocrinus' else 'living-reconstruction','export_texcoords':False,'source_scope':'Frozen original brief; uncertain affinities retained; no specimen cast claim.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
