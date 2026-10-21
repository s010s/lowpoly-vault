#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch100 geometry, authored strictly after original-v001 freeze."""
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

def lygodium(c,m,col):
 p=c['parameters'];M=Mesh();T=p['nominal_lamina_thickness_m'];base=Vector((0,0,.009))
 tube(M,[(0,0,0),(.0005,0,.005),base+Vector((0,0,.002))],[.0005,.00050,.00043],6,0,'basal_axis')
 outline=[(-.0006,.009)];angles=[-.55,.58];rads=[.045,.041]
 for j,(a,r) in enumerate(zip(angles,rads)):
  if j:outline.append((.0002,.026))
  for k in range(15):aa=a-.225+k*.45/14;rr=r*(.91+.09*sin(pi*k/14));outline.append((rr*sin(aa),.009+rr*cos(aa)))
 outline.append((.0006,.009));polyvolume(M,outline,T,1,'bifid_lamina');M.contacts.append({'child':'bifid_lamina','parent':'basal_axis'})
 for j,(a,r) in enumerate(zip(angles,rads)):
  def pt(aa,rr):return Vector((rr*sin(aa),-T/2,.009+rr*cos(aa)))
  tag=f'dichotomous_veins_{j}';front=[(a,.002)]
  for depth,frac,spread in [(0,.40,.06),(1,.65,.045),(2,.90,.032)]:
   nxt=[]
   for aa,rr in front:
    for sign in [-1,1]:
     na=aa+sign*spread;nr=r*frac;tube(M,[pt(aa,rr),pt(na,nr)],[.000063-depth*.000009,.000060-depth*.000009],4,3,tag);nxt.append((na,nr))
   front=nxt
  M.contacts.append({'child':tag,'parent':'bifid_lamina'})
 b=Vector((0,0,.006));end=Vector((.0125,0,.016));tube(M,[b,end],[.00031,.00015],5,0,'fertile_axis');M.contacts.append({'child':'fertile_axis','parent':'basal_axis'})
 side=Vector((-.625,0,.781));axis=(end-b).normalized()
 for k in range(3):
  for sign in [-1,1]:
   root=b+(end-b)*(.36+k*.27);tip=root+axis*.001+side*sign*(.0016+.0002*k);tag=f'fertile_branchlet_{k}_{sign}'
   tube(M,[root,tip],[.00017,.00012],4,0,tag);M.contacts.append({'child':tag,'parent':'fertile_axis'})
   aa=(axis*.55+side*sign*.8).normalized();zz=tip+aa*.0024;outline2=[]
   for t,w in [(0,.00022),(.30,.0007),(.80,.00057),(1,.00015),(.80,-.00057),(.30,-.0007),(0,-.00022)]:
    q=tip+aa*(t*.0024)+Vector((-aa.z,0,aa.x))*w;outline2.append((q.x,q.z))
   lob=f'flattened_sorophore_{k}_{sign}';polyvolume(M,outline2,.00023,2,lob);M.contacts.append({'child':lob,'parent':tag})
 o=M.emit('bifid-foliage-with-small-fertile-branch',m,col);o['design_sterile_lobes']=2;o['design_sorophores']=6;o['design_terminal_vein_rays']=16

def flabellophyton(c,m,col):
 p=c['parameters'];M=Mesh();N=p['illustrative_filament_ridges']*2;zs=[0,.002,.006,.012,.024,.036,.048,.060];ws=[.001,.00065,.00065,.0018,.004,.0063,.0082,.0095];T=p['nominal_body_thickness_m'];v=[]
 for back in [False,True]:
  for i,(z,w) in enumerate(zip(zs,ws)):
   for j in range(N+1):
    u=2*j/N-1;zz=z-(.0011*abs(u)**1.3 if i==len(zs)-1 else 0);relief=(.00008 if j%2 else -.000025)*min(1,z/.012);y=(T*.5 if back else -T*.5-relief);v.append((u*w,y,zz))
 rows=len(zs);n=rows*(N+1);f=[]
 for back in [0,1]:
  off=back*n
  for i in range(rows-1):
   for j in range(N):a=off+i*(N+1)+j;face=(a,a+1,a+N+2,a+N+1);f.append(face if back==0 else tuple(reversed(face)))
 border=list(range(N+1))+[i*(N+1)+N for i in range(1,rows)]+list(range((rows-1)*(N+1)+N-1,(rows-1)*(N+1)-1,-1))+[i*(N+1) for i in range(rows-2,0,-1)]
 f.extend((a,b,b+n,a+n) for a,b in zip(border,border[1:]+border[:1]));M.add(v,f,1,'integral_fan_stalk_attachment');o=M.emit('narrow-radially-corrugated-thallus',m,col);o['design_filament_ridges']=32;o['design_roots']=0;o['design_bodies']=1

def protosalvinia(c,m,col):
 p=c['parameters'];M=Mesh();W=p['nominal_width_m'];H=p['nominal_height_m'];T=p['nominal_thickness_m'];N=64;R=8;v=[]
 def boundary(a):
  x=W*.5*cos(a);z=H*.5*sin(a)
  # Broad two-rounded-lobe outline, shallow apical sinus; basal edge remains continuous.
  if sin(a)>0:z-=.00065*math.exp(-(x/.00062)**2)
  x*=1+.012*sin(7*a);z*=1+.008*cos(9*a);return x,z
 for back in [False,True]:
  v.append((0,T/2 if back else -T/2,0))
  for r in range(1,R+1):
   t=r/R
   for j in range(N):
    a=2*pi*j/N;x,z=boundary(a);x*=t;z*=t
    # Fine faceted relief is integral, not separate spore balls or buried objects.
    relief=(.000016*sin(j*2.41+r*1.2)+.000012*cos(j*.71-r*.53))*(1-t*.65)
    groove=.000032*math.exp(-(x/.00046)**2)*(1-t*.4)
    y=T/2 if back else -T/2-relief+groove;v.append((x,y,z))
 n=1+R*N;f=[]
 for back in [0,1]:
  off=back*n
  for j in range(N):face=(off,off+1+j,off+1+(j+1)%N);f.append(face if back==0 else face[::-1])
  for r in range(1,R):
   for j in range(N):a=off+1+(r-1)*N+j;b=off+1+(r-1)*N+(j+1)%N;face=(a,b,b+N,a+N);f.append(face if back==0 else face[::-1])
 for j in range(N):a=1+(R-1)*N+j;b=1+(R-1)*N+(j+1)%N;f.append((a,b,b+n,a+n))
 M.add(v,f,1,'bilobed_cancellate_body');o=M.emit('single-bilobed-compression',m,col);o['design_lobes']=2;o['design_bodies']=1;o['design_spores']=0

def chaetocladus(c,m,col):
 p=c['parameters'];M=Mesh();H=p['nominal_axis_height_m'];rad=p['nominal_axis_radius_m'];comp=p['nominal_depth_compression_factor']
 def axis(t):return Vector((.0018*sin(t*pi*.8),0,H*t))
 tube(M,[axis(i/18) for i in range(19)],[rad*(1-.28*i/18) for i in range(19)],6,0,'central_axis')
 for k in range(p['illustrative_whorls']):
  t=.045+k*.90/(p['illustrative_whorls']-1);b=axis(t);L=p['nominal_longest_lateral_length_m']*(.58+.42*sin(pi*t*.62))
  for j in range(p['illustrative_laterals_per_whorl']):
   a=2*pi*j/p['illustrative_laterals_per_whorl']+(k%2)*.026;d=Vector((cos(a),sin(a),0));tag=f'lateral_{k:02d}_{j:02d}'
   ps=[b,b+d*L*.47+Vector((0,0,L*.41)),b+d*L*.84+Vector((0,0,L*.93))];tube(M,ps,[.000075,.000066,.000027],3,1+(j%3==0),tag);M.contacts.append({'child':tag,'parent':'central_axis'})
 # Compression is part of the authored fossil volume and is measured after this transform.
 M.v=[(x,y*comp,z) for x,y,z in M.v];o=M.emit('single-order-whorled-fossil-axis',m,col);o['design_whorls']=15;o['design_laterals']=480;o['design_branch_orders']=1

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());aid=cfg['asset_id'];out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'plants',col,metadata={'representation':'fossil-specimen','export_texcoords':False,'source_scope':'Frozen original brief; no whole organism certainty. Ordovician C.plumula, not Silurian.' if aid=='chaetocladus' else 'Frozen original fossil-organ scope; no whole organism certainty.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
