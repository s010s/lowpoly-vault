#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch98 original botanical geometry, authored only after immutable original freeze.
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
  txt=bpy.data.texts.new('BATCH98_COMPONENT_CONTRACT.json');txt.write(json.dumps(dict(schema_version=1,object_name=o.name,translation=list(off),components=self.components),sort_keys=True))
  o['component_contract']='BATCH98_COMPONENT_CONTRACT.json';o['source_editing']='Named organ vertex groups; all dimensions in meters, translation only.'
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

def voltzia(c,m,col):
 p=c['parameters'];M=Mesh();pts=[Vector((0,0,0)),Vector((-.008,0,.065)),Vector((-.017,.003,.115)),Vector((-.023,0,.145))]
 tube(M,pts,[.003,.0029,.0024,.0014],7,0,'main_axis')
 b=pts[1];end=b+Vector((.077,.006,.045));fert=[b,b+Vector((.036,.005,.013)),end];tube(M,fert,[.0024,.002,.0018],7,0,'fertile_branch',parent='main_axis')
 axis=Vector((.30,.06,.952)).normalized();cone_b=end-axis*.001;cone_e=cone_b+axis*p['cone_axis_length_m'];tube(M,[cone_b,cone_b.lerp(cone_e,.5),cone_e],[.0030,.0035,.0014],7,1,'cone_axis',parent='fertile_branch')
 for j in range(96):
  if j<64:
   u=.03+.92*j/63;idx=min(int(u*3),2);b=pts[idx].lerp(pts[idx+1],u*3-idx);parent='main_axis'
  else:
   u=.08+.84*(j-64)/31;idx=min(int(u*2),1);b=fert[idx].lerp(fert[idx+1],u*2-idx);parent='fertile_branch'
  ang=j*2.39996;d=Vector((cos(ang),sin(ang),-.28 if j%4 else .12));blade(M,b,d,p['leaf_length_m'],p['leaf_width_m'],p['leaf_thickness_m'],2+j%2,f'leaf_{j:03d}',parent=parent,rounded=False)
 for k in range(6):
  for j in range(4):
   ang=j*pi/2+k*.73;_,w,t=axes(axis);rad=w*cos(ang)+t*sin(ang);b=cone_b+axis*(.002+k*.008);fan(M,b,rad*.78+axis*.62,p['scale_length_m'],p['scale_width_m'],p['scale_thickness_m'],1+(j+k)%3,f'cone_scale_{k}_{j}','cone_axis')
 return M.emit('voltzia-heterophylla-fruiting-branch',m,col)

def sciadopitys(c,m,col):
 p=c['parameters'];M=Mesh();pts=[Vector((0,0,0)),Vector((.002,0,.055)),Vector((-.001,.002,.108)),Vector((0,0,.16))];tube(M,pts,[.0024,.0023,.002,.0016],7,0,'axis')
 for k in range(3):
  b=pts[k+1]-Vector((0,0,.008))
  for j in range(12):
   ang=2*pi*j/12+k*.21;d=Vector((cos(ang),sin(ang),.20+.12*sin(j*1.7+k)));grooved(M,b,d,p['cladode_length_m'],p['cladode_width_m'],p['cladode_thickness_m'],p['groove_depth_m'],2+(j+k)%2,f'cladode_{k}_{j:02d}','axis')
 return M.emit('sciadopitys-three-whorls-twelve-cladodes',m,col)

def agathis(c,m,col):
 p=c['parameters'];M=Mesh();H=p['trunk_height_m'];trunk=[Vector((0,0,0)),Vector((.008,-.012,.6)),Vector((-.01,.008,1.25)),Vector((0,0,H))];tube(M,trunk,[p['trunk_base_radius_m'],.058,.038,.008],9,0,'trunk')
 for i in range(9):
  tier=i//3;j=i%3;ang=2*pi*j/3+tier*.85;rad=Vector((cos(ang),sin(ang),0));side=Vector((-sin(ang),cos(ang),0));z=.75+tier*.43;idx=1 if z<1.25 else 2;f=(z-trunk[idx].z)/(trunk[idx+1].z-trunk[idx].z);b=trunk[idx].lerp(trunk[idx+1],f);span=.66-tier*.13;e=b+rad*span+Vector((0,0,.18));br=f'branch_{i}';tube(M,[b,b.lerp(e,.55)-Vector((0,0,.04)),e],[.027-tier*.005,.015,.006],7,0,br,parent='trunk')
  for k in range(3):
   u=.44+k*.25;mid=b.lerp(e,.55)-Vector((0,0,.04));bb=b.lerp(mid,u/.55) if u<=.55 else mid.lerp(e,(u-.55)/.45);dd=(rad+side*((k-1)*.70)+Vector((0,0,.22))).normalized();L=.24-.02*tier;ee=bb+dd*L;tw=f'twig_{i}_{k}';tube(M,[bb,ee],[.006,.0021],5,1,tw,parent=br)
   # Opposite/subopposite insertion pairs. Twisting petioles display all blades in two ranks.
   lat=Vector((-dd.y,dd.x,0)).normalized();up=dd.cross(lat).normalized()
   for q in range(8):
    t=.12+q*.10;root=bb.lerp(ee,t)
    for sign in [-1,1]:
     # Base positions alternate around twig (decussate), then twist into two-ranked blades.
     ins=(lat if q%2==0 else up)*sign;pb=root+ins*.001;d=(lat*sign*.94+dd*.34).normalized();pe=pb+d*p['petiole_length_m'];pet=f'petiole_{i}_{k}_{q}_{sign}';tube(M,[pb,pe],[.0012,.00085],4,2,pet,'petiole',tw)
     blade(M,pe-d*.0003,d,p['leaf_length_m'],p['leaf_width_m'],p['leaf_thickness_m'],2+(q+i+k)%3,f'leaf_{i}_{k}_{q}_{sign}','leaf',pet,n=up,rounded=True)
   ellipsoid(M,ee-dd*.002,dd,.012,p['bud_diameter_m'],p['bud_diameter_m'],5,f'bud_{i}_{k}','terminal_bud',tw,sides=6,rings=4)
 # Single fossil-dimension immature seed cone, visibly tiny on whole-tree scale.
 i=0;tb=trunk[1].lerp(trunk[2],(.75-trunk[1].z)/(trunk[2].z-trunk[1].z));te=tb+Vector((.66,0,.18));tm=tb.lerp(te,.55)-Vector((0,0,.04));b=tm.lerp(te,.14);parent='branch_0';d=Vector((.55,-.35,.76)).normalized();fb='fertile_branch';tube(M,[b,b+d*.075],[.0105,.0105],8,1,fb,'fertile_branch',parent)
 cb=b+d*.070;ellipsoid(M,cb,d,p['seed_cone_length_m'],p['seed_cone_width_m'],p['seed_cone_width_m'],5,'seed_cone_core','seed_cone',fb,sides=10,rings=6)
 a,w,t=axes(d)
 for k in range(5):
  z=.0015+k*.0063;zend=min(.034,z+.008);r=.0165*math.sqrt(max(0,1-(1-2*z/.034)**2));rend=.0165*math.sqrt(max(0,1-(1-2*zend/.034)**2))
  for j in range(8):
   ang=j*pi/4+k*.28;rad=w*cos(ang)+t*sin(ang);base=cb+d*z+rad*(r*.82);end=cb+d*zend+rad*(rend*1.035+.0005);vec=end-base;blade(M,base,vec,vec.length,.008,.0012,5,f'cone_scale_{k}_{j}','cone_scale','seed_cone_core',n=rad,rounded=True)
 return M.emit('agathis-zamunerae-restrained-tree',m,col)

def archaefructus(c,m,col):
 p=c['parameters'];M=Mesh();base=Vector((0,0,.035));main=[base,Vector((-.005,0,.10)),Vector((.006,.002,.17)),Vector((0,0,.26))];tube(M,main,[.0015,.0013,.001,.0005],6,0,'main_stem')
 shoots=[(main[2],main[-1],'main_stem')]
 for i,(angle,z,height,span) in enumerate([(2.8,.09,.24,.062),(.15,.12,.28,.058),(4.7,.15,.30,.044)]):
  ix=0 if z<.10 else 1;bb=main[ix].lerp(main[ix+1],(z-main[ix].z)/(main[ix+1].z-main[ix].z));tip=Vector((span*cos(angle),span*sin(angle),height));tag=f'lateral_stem_{i}';tube(M,[bb,bb.lerp(tip,.40),tip],[.0006,.0006,.0005],5,0,tag,'lateral_stem','main_stem');shoots.append((bb,tip,tag))
 for s,(b,tip,tag) in enumerate(shoots):
  d=(tip-b).normalized();fb=tip-d*.010;fe=fb+d*p['fertile_axis_length_m'];ft=f'fertile_axis_{s}';tube(M,[fb,fe],[.00048,.00022],5,0,ft,'fertile_axis',tag)
  a,w,t=axes(d)
  for j in range(16):
   u=.026+j*.0021;ang=j*2.39996+s;rad=w*cos(ang)+t*sin(ang);bb=fb+d*u;st=f'carpel_stalk_{s}_{j}';end=bb+rad*.002;tube(M,[bb,end],[.00013,.00011],4,1,st,'carpel_stalk',ft)
   blade(M,end-rad*.00003,rad*.44+d*.90,p['carpel_length_m'],p['carpel_width_m'],p['carpel_thickness_m'],3,f'carpel_{s}_{j}','carpel',st,n=rad,rounded=True)
  for j in range(8):
   ang=j*2.39996;rad=w*cos(ang)+t*sin(ang);bb=fb+d*(.003+j*.0023);st=f'stamen_stalk_{s}_{j}';ee=bb+rad*.002;tube(M,[bb,ee],[.00011,.00009],4,2,st,'paired_stamen_stalk',ft)
   for sign in [-1,1]:
    ftag=f'filament_{s}_{j}_{sign}';side=d.cross(rad).normalized();ff=ee+side*sign*.00035+d*.00094;tube(M,[ee,ff],[.00007,.00005],4,2,ftag,'filament',st)
    blade(M,ff-d*.00002,d,p['anther_length_m'],p['anther_width_m'],.0003,3,f'anther_{s}_{j}_{sign}','anther',ftag,n=rad,rounded=True)
 # 12 genuinely three-level, ternately divided leaves; 27 separately tagged terminal lobes each.
 for i in range(12):
  s=i%4;b,tip,tag=shoots[s];t=.16+.22*(i//4);node=b.lerp(tip,t);ang=i*2.39996;out=Vector((cos(ang),sin(ang),.16)).normalized();side=Vector((-sin(ang),cos(ang),0));L=.035-.010*(i//4);sw=f'swollen_base_{i}';ellipsoid(M,node-out*.0004,out,.0022,.0028,.0028,1,sw,'swollen_leaf_base',tag,sides=6,rings=4)
  pet=f'leaf_petiole_{i}';end=node+out*L;tube(M,[node,end],[.0004,.00023],4,1,pet,'petiole',sw)
  size=1-.20*(i//4)
  def divide(origin,direction,level,parent,path):
   for q in [-1,0,1]:
    aa=q*(.60 if level==0 else .48);v=(direction*cos(aa)+side*sin(aa)).normalized();ll=[.009,.005,.003][level]*size;ee=origin+v*ll;ct=f'leaf_axis_{i}_{path}{q+1}';r=[.00019,.00012,.000075][level];tube(M,[origin,ee],[r,r*.62],4,1,ct,'leaf_division_axis',parent)
    if level<2:divide(ee-v*.00003,v,level+1,ct,path+str(q+1))
    else:blade(M,ee-v*.00003,v,p['leaf_tip_length_m'],p['leaf_tip_width_m'],.00010,2,f'ultimate_lobe_{i}_{path}{q+1}','ultimate_lobe',ct,n=(0,0,1),rounded=True)
  divide(end-out*.0001,out,0,pet,'')
 rootend=base+Vector((.004,0,-p['root_length_m']));tube(M,[base,base.lerp(rootend,.5),rootend],[.0011,.00065,.0002],5,4,'primary_root','primary_root','main_stem')
 for j in range(4):
  bb=base.lerp(rootend,.2+j*.16);a=j*2.39996;end=bb+Vector((.011*cos(a),.011*sin(a),-.008));tube(M,[bb,end],[.00035,.00007],4,4,f'secondary_root_{j}','secondary_root','primary_root')
 return M.emit('archaefructus-sinensis-four-open-fertile-shoots',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update()
 export_asset(aid,aid,'plants',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Original batch98 pregeometry freeze; source-constrained organs with explicitly interpretive architecture; no source pixels bundled.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':start,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clock_note':'Raw executor clock, not ImageGen/provider timestamp; compare host observation records instead of assuming historic offset.','blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
