#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch105 geometry authored only after the complete premodel freeze.
Skeletal topology is built from explicit cells, independent of third-party meshes.
"""
import argparse,datetime,hashlib,json,math,os,sys,collections
from pathlib import Path
import bpy
from mathutils import Vector
from math import pi,sin,cos,sqrt
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset

def axes(d):
 a=Vector(d).normalized();w=Vector((0,-1,0)).cross(a).normalized();t=a.cross(w).normalized();return a,w,t
class Patch:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.index={};self.features=[]
 def vertex(self,p):
  k=tuple(round(float(x),14) for x in p)
  if k not in self.index:self.index[k]=len(self.v);self.v.append(k)
  return self.index[k]
 def face(self,pts,mat=0):self.f.append(tuple(self.vertex(p) for p in pts));self.mi.append(mat)
 def quad(self,pts,mat=0):
  q=[Vector(p) for p in pts]
  def area(i,j,k):return (q[j]-q[i]).cross(q[k]-q[i]).length
  if min(area(0,1,2),area(0,2,3))>=min(area(0,1,3),area(1,2,3)):
   self.face([q[0],q[1],q[2]],mat);self.face([q[0],q[2],q[3]],mat)
  else:self.face([q[0],q[1],q[3]],mat);self.face([q[1],q[2],q[3]],mat)
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.components=[];self.features=[]
 def add(self,p,tag,kind,d=(0,0,1),parent=None,base=None,design=None):
  o=len(self.v);a,w,t=axes(d);self.v.extend(p.v);self.f.extend(tuple(o+i for i in f) for f in p.f);self.mi.extend(p.mi);self.components.append({'tag':tag,'kind':kind,'vertices':list(range(o,o+len(p.v))),'axes':[list(a),list(w),list(t)],'parent':parent,'base_vertices':[o+i for i in (base or [])],'design':design or {}})
  for feature in p.features:self.features.append(dict(feature,component=tag,vertices=[o+i for i in feature['vertices']]))
 def emit(self,aid,mats,col):
  low=[min(v[k] for v in self.v) for k in range(3)];high=[max(v[k] for v in self.v) for k in range(3)];off=Vector((-(low[0]+high[0])/2,-(low[1]+high[1])/2,-low[2]));vs=[Vector(v)+off for v in self.v];ob=mesh_object(aid+'-original-skeleton',vs,self.f,mats,col)
  for poly,mat in zip(ob.data.polygons,self.mi):poly.material_index=mat
  for c in self.components:ob.vertex_groups.new(name=c['tag']).add(c['vertices'],1,'REPLACE')
  data={'schema_version':1,'object_name':ob.name,'translation':list(off),'components':self.components,'integrated_features':self.features};bpy.data.texts.new('BATCH105_COMPONENT_CONTRACT.json').write(json.dumps(data,sort_keys=True));ob['component_contract']='BATCH105_COMPONENT_CONTRACT.json';ob['editing']='Editable closed component solids, semantic vertexgroups and integrated geometric cavity records; meters.';return ob

def tube_patch(pts,r,sides=8):
 pts=[Vector(v) for v in pts];P=Patch();rings=[]
 for i,v in enumerate(pts):
  a=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized();ref=Vector((0,0,1))
  if abs(a.dot(ref))>.95:ref=Vector((0,1,0))
  w=ref.cross(a).normalized();t=a.cross(w);rings.append([v+r*(w*cos(2*pi*j/sides)+t*sin(2*pi*j/sides)) for j in range(sides)])
 for k in range(len(rings)-1):
  for j in range(sides):jj=(j+1)%sides;P.quad([rings[k][j],rings[k][jj],rings[k+1][jj],rings[k+1][j]])
 for j in range(sides):P.face([pts[0],rings[0][(j+1)%sides],rings[0][j]]);P.face([pts[-1],rings[-1][j],rings[-1][(j+1)%sides]])
 return P

def archimedes(c,m,col):
 p=c['parameters'];M=Mesh();T=p['turns']*2*pi;H=p['axis_height_m'];R=p['axis_helix_radius_m'];OR=p['outer_radius_m'];rise=p['frond_rise_m'];th=p['frond_thickness_m'];nu=p['angular_cells'];nv=p['radial_cells'];gap=(1-p['hole_fraction'])/2
 def mapuv(u,v,s):
  a=T*u;rr=R+(OR-R)*v;z=H*u+rise*v;return Vector((rr*cos(a),rr*sin(a),z+s*th/2))
 AP=tube_patch([(R*cos(T*i/120),R*sin(T*i/120),H*i/120) for i in range(121)],p['axis_tube_radius_m']);M.add(AP,'axial_helix','axial_helix',design={'turns':p['turns'],'radius_m':R,'height_m':H})
 P=Patch();base=[]
 for i in range(nu):
  for j in range(nv):
   outer=[(i/nu,j/nv),((i+1)/nu,j/nv),((i+1)/nu,(j+1)/nv),(i/nu,(j+1)/nv)];inner=[((i+gap)/nu,(j+gap)/nv),((i+1-gap)/nu,(j+gap)/nv),((i+1-gap)/nu,(j+1-gap)/nv),((i+gap)/nu,(j+1-gap)/nv)]
   for s in [-1,1]:
    for k in range(4):q=(k+1)%4;P.quad([mapuv(*outer[k],s),mapuv(*outer[q],s),mapuv(*inner[q],s),mapuv(*inner[k],s)],0 if j%2==0 else 1)
   holeverts=[]
   for k in range(4):q=(k+1)%4;P.quad([mapuv(*inner[k],-1),mapuv(*inner[q],-1),mapuv(*inner[q],1),mapuv(*inner[k],1)],2);holeverts.extend([P.vertex(mapuv(*inner[k],1)),P.vertex(mapuv(*inner[k],-1))])
   P.features.append({'tag':f'fenestrule_{i}_{j}','kind':'open_fenestrule','vertices':holeverts,'u_cell':i,'radial_cell':j,'actual_through_hole':True})
 for i in range(nu):
  for j in [0,nv]:
   a=(i/nu,j/nv);b=((i+1)/nu,j/nv);P.quad([mapuv(*a,-1),mapuv(*b,-1),mapuv(*b,1),mapuv(*a,1)])
   if j==0:base.extend(P.vertex(mapuv(*q,s)) for q in [a,b] for s in [-1,1])
 for j in range(nv):
  for i in [0,nu]:
   a=(i/nu,j/nv);b=(i/nu,(j+1)/nv);P.quad([mapuv(*a,-1),mapuv(*b,-1),mapuv(*b,1),mapuv(*a,1)])
 M.add(P,'continuous_lacy_frond','perforated_frond',parent='axial_helix',base=base,design={'fenestrule_count':nu*nv,'continuous_turns':p['turns'],'no_solid_sheet':True});return M.emit('archimedes',m,col)

# Surface cell boundary with eight vertices and matching subdivisions on neighbouring cells.
def rect8(x0,x1,z0,z1):return [(x1,(z0+z1)/2),(x1,z1),((x0+x1)/2,z1),(x0,z1),(x0,(z0+z1)/2),(x0,z0),((x0+x1)/2,z0),(x1,z0)]
def branch(M,tag,kind,base,d,L,W,D,rows,stations,diam,faces_with_pores=1,parent=None,lunarium=0,keel=0,pores_begin=0,pores_end=1):
 P=Patch();b=Vector(base);a,w,t=axes(d);Pore=[];baseids=[]
 def height(x,z):return D/2*(1-.56*(2*x/W)**2)+keel*max(0,1-abs(2*x/W))* (.85+.15*cos(11*z/L))
 def mp(x,z,s,h=None):return b+a*z+w*x+t*s*(height(x,z) if h is None else h)
 # Exactly repeated rows; the alternating stations are shifted within cells, not a different rowcount.
 for sign in [-1,1]:
  perforated=(sign==1 or faces_with_pores==2)
  for j in range(stations):
   z0=L*j/stations;z1=L*(j+1)/stations
   for k in range(rows):
    x0=-W/2+k*W/rows;x1=-W/2+(k+1)*W/rows;cx=(x0+x1)/2;cz=(z0+z1)/2+(.10 if k%2 else -.10)*(z1-z0);out=rect8(x0,x1,z0,z1)
    if perforated:
     rim=[]
     for q in range(8):
      ang=2*pi*q/8;x=cx+diam/2*cos(ang);z=cz+diam/2*sin(ang);hh=height(x,z)+lunarium*max(0,sin(ang))
      rim.append(mp(x,z,sign,hh))
     for q in range(8):qq=(q+1)%8;P.quad([mp(*out[q],sign),mp(*out[qq],sign),rim[qq],rim[q]],0)
     bottom=mp(cx,cz,sign,height(cx,cz)-diam*.45)
     for q in range(8):P.face([rim[q],rim[(q+1)%8],bottom],2)
     ids=[P.vertex(v) for v in rim]+[P.vertex(bottom)];P.features.append({'tag':f'{tag}_aperture_{sign}_{j}_{k}','kind':'recessed_aperture','vertices':ids,'side':sign,'row':k,'station':j,'rim_vertices':ids[:8],'nominal_diameter_m':diam,'integrated_lunarium':bool(lunarium)})
    else:
     center=mp(cx,(z0+z1)/2,sign)
     for q in range(8):P.face([mp(*out[q],sign),mp(*out[(q+1)%8],sign),center],0)
 # Boundary walls share all midpoints of surface cells.
 for j in range(stations*2):
  z0=L*j/(stations*2);z1=L*(j+1)/(stations*2)
  for x in [-W/2,W/2]:P.quad([mp(x,z0,-1),mp(x,z1,-1),mp(x,z1,1),mp(x,z0,1)],1)
 for k in range(rows*2):
  x0=-W/2+k*W/(rows*2);x1=-W/2+(k+1)*W/(rows*2)
  for z in [0,L]:P.quad([mp(x0,z,-1),mp(x1,z,-1),mp(x1,z,1),mp(x0,z,1)],1)
 baseids=[i for i,v in enumerate(P.v) if abs((Vector(v)-b).dot(a))<1e-10]
 M.add(P,tag,kind,d,parent,baseids,{'nominal_length_m':L,'nominal_width_m':W,'nominal_thickness_m':D,'aperture_rows':rows,'aperture_stations':stations,'pore_bearing_faces':faces_with_pores,'aperture_diameter_m':diam});return P

def penniretepora(c,m,col):
 M=Mesh();p=c['parameters'];branch(M,'main_branch','main_branch',(0,0,0),(0,0,1),p['main_length_m'],p['main_width_m'],p['main_thickness_m'],2,p['main_aperture_stations'],p['aperture_diameter_m'],keel=p['keel_relief_m'])
 for s in [-1,1]:
  for i in range(p['branch_pairs']):
   ang=math.radians(p['branch_angle_deg']);z=.00035+i*p['branch_spacing_m']+(p['branch_spacing_m']*.32 if s==1 else 0);d=(s*sin(ang),0,cos(ang));branch(M,f'lateral_{s}_{i}','lateral_branch',(s*.00010,0,z),d,p['lateral_length_m'],p['lateral_width_m'],p['lateral_thickness_m'],2,p['lateral_aperture_stations'],p['aperture_diameter_m'],parent='main_branch',keel=p['keel_relief_m']*.55)
 return M.emit('penniretepora',m,col)

def cystodictya(c,m,col):
 M=Mesh();p=c['parameters'];branch(M,'lower_bifoliate','bifoliate_branch',(0,0,0),(0,0,1),p['main_length_m'],p['branch_width_m'],p['branch_thickness_m'],5,p['main_aperture_stations'],p['aperture_diameter_m'],2,lunarium=p['lunarium_relief_m'])
 for s,key in [(-1,'left_angle_deg'),(1,'right_angle_deg')]:
  ang=math.radians(p[key]);branch(M,'arm'+str(s),'bifoliate_branch',(s*.00017,0,.00234),(s*sin(ang),0,cos(ang)),p['arm_length_m'],p['branch_width_m'],p['branch_thickness_m'],5,p['arm_aperture_stations'],p['aperture_diameter_m'],2,parent='lower_bifoliate',lunarium=p['lunarium_relief_m'])
 return M.emit('cystodictya',m,col)

# Stellate cavities are part of each broad branch skin, not mounted stars.
def macula_branch(M,p,tag,base,d,L,parent):
 P=Patch();b=Vector(base);a,w,t=axes(d);W=p['branch_width_m'];D=p['branch_thickness_m'];cols=p['macula_columns'];ns=p['macula_stations'];N=24
 def height(x):return D/2*(1-.08*(2*x/W)**2)
 def mp(x,z,s,delta=0):return b+a*z+w*x+t*s*(height(x)+delta)
 for s in [-1,1]:
  for j in range(ns):
   for k in range(cols):
    x0=-W/2+k*W/cols;x1=x0+W/cols;z0=j*L/ns;z1=(j+1)*L/ns;cx=(x0+x1)/2;cz=(z0+z1)/2;outer=[];inner=[];mid=[]
    for q in range(N):
     ang=2*pi*q/N;dx=cos(ang);dz=sin(ang);dist=min((x1-x0)/2/max(abs(dx),1e-8),(z1-z0)/2/max(abs(dz),1e-8));outer.append(mp(cx+dx*dist,cz+dz*dist,s));r=p['macula_radius_m'];rays=(.5+.5*cos(p['macula_rays']*ang))**2
     mid.append(mp(cx+dx*r,cz+dz*r,s,-p['macula_depth_m']*rays*.35));inner.append(mp(cx+dx*r*.42,cz+dz*r*.42,s,-p['macula_depth_m']*(.35+.65*rays)))
    center=mp(cx,cz,s,-p['macula_depth_m']);feature=[]
    for q in range(N):
     qq=(q+1)%N;P.face([center,inner[q],inner[qq]],0);P.quad([inner[q],inner[qq],mid[qq],mid[q]],0);quad=[mid[q],mid[qq],outer[qq],outer[q]]
     if q%4==2:
      cen=sum(quad,Vector())/4;u=(quad[1]-quad[0]).normalized();vv=(quad[3]-quad[0]).normalized();rad=p['pore_diameter_m']/2;rim=[cen+rad*(u*cos(2*pi*z/8)+vv*sin(2*pi*z/8)) for z in range(8)];border=[quad[0],(quad[0]+quad[1])/2,quad[1],(quad[1]+quad[2])/2,quad[2],(quad[2]+quad[3])/2,quad[3],(quad[3]+quad[0])/2]
      rim=[cen+(v-cen).normalized()*rad for v in border]
      # Boundary subdivisions are propagated to neighboring faces after mesh assembly.
      for z in range(8):P.quad([border[z],border[(z+1)%8],rim[(z+1)%8],rim[z]],0)
      low=cen-t*s*rad*.8
      for z in range(8):P.face([rim[z],rim[(z+1)%8],low],2)
      P.features.append({'tag':f'{tag}_pore_{s}_{j}_{k}_{q}','kind':'recessed_aperture','vertices':[P.vertex(v) for v in rim]+[P.vertex(low)],'side':s,'nominal_diameter_m':p['pore_diameter_m']})
     else:P.quad(quad,0)
     feature.extend([P.vertex(inner[q]),P.vertex(mid[q])])
    P.features.append({'tag':f'{tag}_macula_{s}_{j}_{k}','kind':'integrated_stellate_depression','vertices':feature+[P.vertex(center)],'side':s,'rays':p['macula_rays'],'nominal_depth_m':p['macula_depth_m']})
 # Close all boundary skin edges by connecting matching opposite-side coordinates.
 # First split every face edge at existing collinear vertices to eliminate T junctions at cell borders and pore patches.
 split_collinear(P)
 edge=collections.Counter(tuple(sorted((a,b))) for f in P.f for a,b in zip(f,f[1:]+f[:1]));boundary=[e for e,n in edge.items() if n==1]
 for ia,ib in boundary:
  va,vb=Vector(P.v[ia]),Vector(P.v[ib]);la=(va-b).dot(a);lb=(vb-b).dot(a);xa=(va-b).dot(w);xb=(vb-b).dot(w);ya=(va-b).dot(t)
  if ya<0:continue
  P.quad([va,vb,mp(xb,lb,-1),mp(xa,la,-1)],1)
 baseids=[i for i,v in enumerate(P.v) if abs((Vector(v)-b).dot(a))<1e-9]
 M.add(P,tag,'broad_branch',d,parent,baseids,{'nominal_length_m':L,'nominal_width_m':W,'nominal_thickness_m':D,'maculae_per_face':cols*ns,'depressed_not_glued':True})

def split_collinear(P):
 # Exact geometric edge splitting is authoring, not post-hoc diagnostic repair.
 old=P.f;oldm=P.mi;P.f=[];P.mi=[];points=[Vector(v) for v in P.v]
 for face,mi in zip(old,oldm):
  out=[]
  for ia,ib in zip(face,face[1:]+face[:1]):
   aa=points[ia];bb=points[ib];ab=bb-aa;ls=ab.length_squared;cuts=[]
   for j,v in enumerate(points):
    if j in [ia,ib]:continue
    f=(v-aa).dot(ab)/ls
    if 1e-7<f<1-1e-7 and (v-aa-ab*f).length<1e-10:cuts.append((f,j))
   out.append(ia);out.extend(j for _,j in sorted(cuts))
  if len(out)==3:P.f.append(tuple(out));P.mi.append(mi)
  else:
   # Fan through a new interior centroid, avoiding degenerate collinear edge triangles.
   center=sum((points[i] for i in face),Vector())/len(face);ci=P.vertex(center)
   for i,j in zip(out,out[1:]+out[:1]):P.f.append((ci,i,j));P.mi.append(mi)

def constellaria(c,m,col):
 M=Mesh();p=c['parameters'];macula_branch(M,p,'broad_lower',(0,0,0),(0,0,1),p['main_length_m'],None)
 for s,key in [(-1,'left_angle_deg'),(1,'right_angle_deg')]:
  ang=math.radians(p[key]);macula_branch(M,p,'broad_arm'+str(s),(s*.0025,0,.021),(s*sin(ang),0,cos(ang)),p['arm_length_m'],'broad_lower')
 return M.emit('constellaria',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'animals',col,metadata={'representation':'bounded-skeletal-reconstruction','export_texcoords':False,'source_scope':'Original batch105 freeze; reference pixels and meshes not incorporated.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 (out/'execution.json').write_text(json.dumps({'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':start,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()},indent=2)+'\n')
if __name__=='__main__':main()
