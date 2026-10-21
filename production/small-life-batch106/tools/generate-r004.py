#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch106 tubaria; authored after complete original freeze. No external meshes."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from math import sin,cos,pi
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.groups={};self.contacts=[];self.apertures=[]
 def add(self,v,f,mi,tag):
  n=len(self.v);self.v.extend([tuple(x) for x in v]);self.f.extend([tuple(n+i for i in ff) for ff in f]);self.mi.extend([mi]*len(f));self.groups.setdefault(tag,[]).extend(range(n,n+len(v)))
 def emit(self,name,m,col):
  lo=[min(v[k] for v in self.v) for k in range(3)];hi=[max(v[k] for v in self.v) for k in range(3)];off=Vector((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]));self.v=[Vector(v)+off for v in self.v]
  o=mesh_object(name,self.v,self.f,m,col)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i
  for tag,ids in self.groups.items():o.vertex_groups.new(name=tag).add(ids,1,'REPLACE')
  for ap in self.apertures:ap['center']=list(Vector(ap['center'])+off)
  o['contact_design']=json.dumps(self.contacts);o['aperture_design']=json.dumps(self.apertures);return o
 def join(self,child,parent):self.contacts.append({'child':child,'parent':parent})
def frame(t):
 t=Vector(t).normalized();a=Vector((0,1,0)) if abs(t.y)<.85 else Vector((1,0,0));u=(a-t*a.dot(t)).normalized();return t,u,t.cross(u).normalized()
def tube(M,points,radii,sides,mat,tag,wall=None,hollow_rings=3,ropy=False):
 pp=list(map(Vector,points));n=len(pp);v=[];frames=[]
 for k,p in enumerate(pp):
  t,u,w=frame(pp[min(k+1,n-1)]-pp[max(k-1,0)]);frames.append((t,u,w))
  for j in range(sides):
   a=2*pi*j/sides;rr=radii[k]*(.68+.32*cos(3*a+k*.65) if ropy else 1);v.append(p+rr*(u*cos(a)+w*sin(a)))
 f=[tuple(reversed(range(sides)))];mi=[mat]
 for k in range(n-1):
  for j in range(sides):a=k*sides+j;b=k*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides));mi.append(mat if not ropy or j%3 else 1)
 if wall is None:f.append(tuple(range((n-1)*sides,n*sides)));mi.append(mat)
 else:
  # Blind hollow recess: inner wall, closed floor and annular rim are one solid boundary.
  start=max(1,n-hollow_rings);offset=len(v)
  for k in range(start,n):
   t,u,w=frames[k]
   for j in range(sides):a=2*pi*j/sides;v.append(pp[k]+(radii[k]-wall)*(u*cos(a)+w*sin(a)))
  for k in range(n-start-1):
   for j in range(sides):a=offset+k*sides+j;b=offset+k*sides+(j+1)%sides;f.append((b,a,a+sides,b+sides));mi.append(2)
  f.append(tuple(range(offset,offset+sides)));mi.append(2)
  inn=offset+(n-start-1)*sides;out=(n-1)*sides
  for j in range(sides):k=(j+1)%sides;f.append((out+j,out+k,inn+k,inn+j));mi.append(1)
  M.apertures.append({'component':tag,'center':list(pp[-1]),'direction':list(frames[-1][0]),'inner_radius_m':radii[-1]-wall,'nominal_recess_m':sum((pp[k+1]-pp[k]).length for k in range(start,n-1)),'terminal_ring_local_indices':list(range(out,out+sides))})
 fi=len(M.f);M.add(v,f,mat,tag);M.mi[fi:]=mi

def didymograptus(c,M):
 p=c['parameters'];L=p['stipe_length_m'];a=p['stipe_center_top_halfspan_m'];b=p['stipe_center_bottom_halfspan_m'];r=p['stipe_core_radius_m']
 tube(M,[(0,0,L+.0017),(0,0,L+.0007),(0,0,L-.0003)],[.00004,.00045,.00072],8,0,'sicula',.00010,2)
 for s in [-1,1]:
  core=f'stipe_{s}';pts=[(s*a*.4,0,L+.00005),(s*a,0,L-.001),(s*(a+(b-a)*.5),0,L*.5),(s*b,0,0)];tube(M,pts,[r*.8,r,r*1.05,r*1.15],8,0,core);M.join(core,'sicula')
  for j in range(p['thecae_per_stipe']):
   z=L-.0011-j*p['theca_spacing_m'];x=s*(a+(b-a)*(1-z/L));rr=p['theca_mouth_radius_m']*(.73+.27*j/25);tag=f'theca_{s}_{j:02d}'
   pts=[(x,0,z+.00015),(x-s*.00015,0,z-.00030),(x-s*.00046,-.00004,z-.00095),(x-s*.00066,-.00005,z-.00155)]
   tube(M,pts,[rr*.48,rr*.78,rr,rr],8,0,tag,p['wall_thickness_m'],3);M.join(tag,core)

def monograptus(c,M):
 p=c['parameters'];N=p['thecae'];step=p['theca_spacing_m'];base=.0022;Z=base+(N-1)*step
 def x(z):return -.00125*max(0,1-z/.006)**2
 tube(M,[(x(base),0,base+.0004),(x(.001),0,.001),(x(.0001),-.00015,.0001)],[.00012,.00025,.00032],8,0,'sicula',.00007,2)
 points=[(x(base+k*(Z-base)/10),0,base+k*(Z-base)/10) for k in range(11)];tube(M,points,[p['core_radius_m']] *11,8,0,'stipe');M.join('stipe','sicula')
 for j in range(N):
  z=base+j*step;xx=x(z);rr=p['theca_outer_radius_m']*(.72+.28*j/(N-1));tag=f'theca_{j:02d}'
  pts=[(xx-.00004,0,z-.00125),(xx+.00014,-.00004,z+.0006),(xx+.00044,0,z+.00130),(xx+.00081,-.000015,z+.00170),(xx+.00112,-.00003,z+.00162),(xx+.00125,-.00005,z+.00135),(xx+.00122,-.00010,z+.00110)]
  tube(M,pts,[rr*.5,rr*.75,rr,rr,rr,rr*.95,rr*.90],8,0,tag,p['wall_thickness_m'],3);M.join(tag,'stipe')
 tube(M,[(x(Z),0,Z),(x(Z),0,Z+.0019),(x(Z)+.00005,0,Z+.0027)],[.00018,.00010,.000035],6,0,'nema');M.join('nema','stipe')

def diplograptus(c,M):
 p=c['parameters'];N=p['thecae_per_row'];step=p['theca_spacing_m'];Z=.0014
 tube(M,[(0,0,.0021),(0,0,.0010),(0,0,.0002)],[.00010,.00025,.00020],8,0,'sicula',.000055,2)
 tube(M,[(0,0,.00103),(0,0,.003),(0,0,.0116)],[.00025,.00032,.00030],8,0,'axial_colony');M.join('axial_colony','sicula')
 for s in [-1,1]:
  for j in range(N):
   z=Z+j*step+(p['opposite_row_offset_m'] if s==1 else 0);t=j/(N-1);half=p['basal_mouth_center_halfspan_m']+(p['distal_mouth_center_halfspan_m']-p['basal_mouth_center_halfspan_m'])*min(1,j/6);r=p['mouth_radius_m'];tag=f'theca_{s}_{j:02d}'
   pts=[(s*.00004,0,z-.00055),(s*half*.48,0,z-.00018),(s*half*.90,0,z+.00025),(s*half,-.00022,z+.00065),(s*half,-.00042,z+.00091)]
   tube(M,pts,[r*.5,r*.8,r,r,r],8,0,tag,p['wall_thickness_m'],3);M.join(tag,'axial_colony' if j else 'sicula')
   if j==0:
    sp=f'first_pair_spine_{s}';tube(M,[(s*half,0,z+.0003),(s*(half+.00045),0,z-.0001),(s*(half+.00060),0,z-.00025)],[.00013,.00009,.000035],6,1,sp);M.join(sp,tag)
 tube(M,[(.00020,0,.00045),(.00023,0,-.00045)],[.00012,.000035],6,0,'virgella');M.join('virgella','sicula')
 tube(M,[(0,0,.0112),(0,0,.0129)],[.00010,.000035],6,0,'nema');M.join('nema','axial_colony')

def dictyonema(c,M):
 p=c['parameters'];zs=p['branch_levels_z_m'];rs=p['branch_radii_m'];segments=[]
 for level,N in enumerate([16,32,64]):
  for j in range(N):
   a1=2*pi*j/N;a0=2*pi*(j//2)/(N//2) if level else a1
   st=Vector((rs[level]*cos(a0),rs[level]*sin(a0),zs[level]));en=Vector((rs[level+1]*cos(a1),rs[level+1]*sin(a1),zs[level+1]));direction=(en-st).normalized();st-=direction*(.0005 if level else 0);mid=st.lerp(en,.5);tag=f'stipe_{level}_{j:02d}'
   tube(M,[st,mid,en],[p['compound_stipe_radius_m']]*3,p['compound_cross_section_sides'],0,tag,ropy=True);segments.append((level,j,N,st,en,tag))
   if level:M.join(tag,f'stipe_{level-1}_{j//2:02d}')
 def pos(level,j,z):
  ss=next(v for v in segments if v[0]==level and v[1]==j);st,en=ss[3:5];return st.lerp(en,(z-st.z)/(en.z-st.z))
 for k,z in enumerate(p['bridge_levels_z_m']):
  level=0 if z<zs[1] else 1 if z<zs[2] else 2;N=[16,32,64][level]
  for j in range(N):
   p0=pos(level,j,z);z2=z+(.0004 if (j+k)%2 else -.0004);p1=pos(level,(j+1)%N,z2);tag=f'thecal_bridge_{k}_{j:02d}';tube(M,[p0,p1],[p['bridge_radius_m']]*2,6,0,tag);M.join(tag,f'stipe_{level}_{j:02d}');M.join(tag,f'stipe_{level}_{(j+1)%N:02d}')
 for level,j,N,st,en,par in segments:
  if j%[1,2,4][level]:continue
  z=(zs[level]+zs[level+1])*.5+.001;pt=pos(level,j,z);rad=Vector((pt.x,pt.y,0)).normalized();length=p['aperture_free_length_m'];tag=f'aperture_{level}_{j:02d}'
  points=[pt-rad*.00015,pt+rad*.00055+Vector((0,0,.0003)),pt+rad*(length+.00055)+Vector((0,0,.0006)),pt+rad*(length+.00070)+Vector((0,0,.00075))];r=p['aperture_outer_radius_m'];tube(M,points,[r*.7,r,r,r],6,0,tag,p['aperture_wall_m'],3);M.join(tag,par)
 # Basal stipes connected circumferentially through real thecal bridges, no invented holdfast.
 for j in range(16):M.join(f'stipe_0_{j:02d}',f'thecal_bridge_0_{j:02d}')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());out=Path(a.output);out.mkdir(parents=True,exist_ok=True);aid=cfg['asset_id'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),v) for i,v in enumerate(cfg['palette_srgb'])];M=Mesh();globals()[aid](cfg,M);M.emit(aid+'-original-tubarium',m,col);bpy.context.view_layer.update();export_asset(aid,aid,'fossils',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Type-centered primary-supported skeletal tubarium; color, selected counts and inferred thickness artistic.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 record={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':main()
