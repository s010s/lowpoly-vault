#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch107 geometry, authored after immutable2026-10-21T04:07:32Z freeze.
All visible plates, tube rings and ambulacral cover plates are genuine closed solids.
No fossil pixels or third-party meshes are input to this deterministic generator.
"""
import argparse,datetime,hashlib,json,math,os,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from math import pi,sin,cos,sqrt,atan2
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Patch:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.base=[];self.solids=[]
 def vert(self,p):self.v.append(tuple(float(x) for x in p));return len(self.v)-1
 def face(self,ids,mat=0):self.f.append(tuple(ids));self.mi.append(mat)
 def prism(self,lower,upper,mat=0):
  n=len(lower);centroid=sum((Vector(v) for v in lower),Vector())/n;lower=[tuple(centroid+(Vector(v)-centroid)*.985) for v in lower];o=len(self.v);self.v.extend(tuple(p) for p in lower+upper);self.base.extend(range(o,o+n));self.face(list(range(o+n-1,o-1,-1)),mat)
  self.face(list(range(o+n,o+2*n)),mat)
  for i in range(n):j=(i+1)%n;self.face([o+i,o+j,o+n+j,o+n+i],mat)
  self.solids.append(list(range(o,o+2*n)))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.components=[];self.features=[]
 def add(self,P,tag,kind,parent=None,design=None,axis=(0,1,0)):
  off=len(self.v);self.v+=P.v;self.f+=[tuple(off+i for i in f) for f in P.f];self.mi+=P.mi
  a=Vector(axis).normalized();ref=Vector((0,0,1)) if abs(a.z)<.9 else Vector((0,1,0));w=ref.cross(a).normalized();t=a.cross(w).normalized()
  self.components.append(dict(tag=tag,kind=kind,vertices=list(range(off,off+len(P.v))),axes=[list(a),list(w),list(t)],parent=parent,base_vertices=[off+i for i in (P.base or list(range(len(P.v))))],design=design or {}))
  for j,ids in enumerate(P.solids):self.features.append(dict(tag=tag+'_plate_'+str(j),kind='geometric_plate',component=tag,vertices=[off+i for i in ids],side=None))
 def emit(self,aid,m,col):
  lo=[min(v[k] for v in self.v) for k in range(3)];hi=[max(v[k] for v in self.v) for k in range(3)];off=Vector((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]));obj=mesh_object(aid+'-original-organism',[Vector(v)+off for v in self.v],self.f,m,col)
  for f,mi in zip(obj.data.polygons,self.mi):f.material_index=mi
  for c in self.components:obj.vertex_groups.new(name=c['tag']).add(c['vertices'],1,'REPLACE')
  contract=dict(schema_version=1,object_name=obj.name,translation=list(off),components=self.components,integrated_features=self.features)
  bpy.data.texts.new('BATCH107_COMPONENT_CONTRACT.json').write(json.dumps(contract,sort_keys=True));obj['component_contract']='BATCH107_COMPONENT_CONTRACT.json';obj['editing']='Original closed component solids with editable semantic vertex groups. Plate seams and segmentation are actual volume, not metadata-only features.'
  return obj

def sphere_patch(mapping,n=24,rows=12,mat=0):
 P=Patch();P.vert(mapping(Vector((0,0,-1))))
 for j in range(1,rows):
  lat=-pi/2+pi*j/rows
  for k in range(n):a=2*pi*k/n;P.vert(mapping(Vector((cos(lat)*cos(a),cos(lat)*sin(a),sin(lat)))))
 top=P.vert(mapping(Vector((0,0,1))))
 for k in range(n):P.face([0,1+(k+1)%n,1+k],mat)
 for j in range(rows-2):
  for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;c=b+n;d=a+n;P.face([a,b,c,d],mat)
 off=1+(rows-2)*n
 for k in range(n):P.face([off+k,off+(k+1)%n,top],mat)
 return P

def dual_plates(mapping,subdiv=2,relief=.025,skip=None):
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=subdiv,radius=1);bm.verts.ensure_lookup_table();P=Patch()
 for i,v in enumerate(bm.verts):
  c=v.co.normalized()
  if skip and skip(c):continue
  ref=Vector((0,0,1)) if abs(c.z)<.9 else Vector((0,1,0));u=ref.cross(c).normalized();w=c.cross(u);corners=[f.calc_center_median().normalized() for f in v.link_faces];corners.sort(key=lambda p:atan2((p-c).dot(w),(p-c).dot(u)))
  lower=[mapping(p*.945) for p in corners];upper=[mapping((c+(p-c)*.91).normalized()*(1+relief)) for p in corners];P.prism(lower,upper,1 if i%7==0 else (3 if i%5==0 else 0))
 bm.free();return P

def segmented_tube(centers,radii,sides=8,mat=1,quarter_seam_until=None):
 P=Patch();rings=[]
 for i,(pt,r) in enumerate(zip(centers,radii)):
  pt=Vector(pt);a=(Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(0,i-1)])).normalized();ref=Vector((0,0,1)) if abs(a.z)<.9 else Vector((0,1,0));w=ref.cross(a).normalized();t=a.cross(w)
  ring=[]
  for k in range(sides):
   angle=2*pi*k/sides;seam=(1-.13*max(0,cos(4*angle))**4) if quarter_seam_until is not None and i<=quarter_seam_until else 1
   ring.append(P.vert(pt+r*seam*(w*cos(angle)+t*sin(angle))))
  rings.append(ring)
 for i in range(len(rings)-1):
  for k in range(sides):q=(k+1)%sides;P.face([rings[i][k],rings[i][q],rings[i+1][q],rings[i+1][k]],mat if i%4!=0 else 0)
 P.face(list(reversed(rings[0])),mat);P.face(rings[-1],mat);P.base=rings[0];return P

def cup(center,normal,r,depth=.0003,mat=1):
 P=Patch();c=Vector(center);n=Vector(normal).normalized();ref=Vector((0,0,1)) if abs(n.z)<.9 else Vector((0,1,0));w=ref.cross(n).normalized();t=n.cross(w);N=12;rings=[]
 for rad,h in [(r*1.35,-depth*2.6),(r*1.35,0),(r,0),(r*.70,-depth)]:rings.append([P.vert(c+n*h+rad*(w*cos(2*pi*k/N)+t*sin(2*pi*k/N))) for k in range(N)])
 for j in range(3):
  for k in range(N):q=(k+1)%N;P.face([rings[j][k],rings[j][q],rings[j+1][q],rings[j+1][k]],mat if j<2 else 2)
 P.face(list(reversed(rings[0])),mat);P.face(rings[3],2);P.base=rings[0];return P

def dendrocystites(cfg,m,col):
 p=cfg['parameters'];M=Mesh();W=p['theca_width_m'];L=p['theca_length_m'];T=p['theca_thickness_m']
 def shape(v):x,y,z=v;return Vector((W/2*x*(.86+.14*y)+.0008*max(0,y)*max(0,x),L/2*y,T/2*z))
 M.add(sphere_patch(shape),'theca','theca_core',design={'nominal_length_m':L,'nominal_width_m':W,'nominal_thickness_m':T})
 M.add(dual_plates(shape,p['plate_subdivisions'],.035),'thecal_plating','thecal_plating','theca',{'plate_count_is_artistic':True})
 C=[];R=[];N=p['brachiole_segments']
 for j in range(N*4+1):
  t=j/(N*4);C.append((-.002*sin(t*pi*.8),-L*.465-p['brachiole_length_m']*t,.0008*sin(t*pi)));R.append((.00075*(1-t)+.00014)*([.86,1.08,1.08,.86][j%4]))
 M.add(segmented_tube(C,R),'brachiole','brachiole','theca',{'unbranched':True,'visible_segments':N})
 C=[];R=[];N=p['proxistele_rings']+p['dististele_segments']
 for j in range(N*4+1):
  u=j/(N*4);prox=p['proxistele_rings']/N;t=.25*u/prox if u<prox else .25+.75*(u-prox)/(1-prox);C.append((.0035*sin(t*pi*.9),L*.46+p['homoiostele_length_m']*t,.0007*sin(t*pi)))
  rad=(.0019-(.0010*t/.25)) if t<.25 else (.0009*(1-(t-.25)/.75)+.00014);R.append(rad*[.86,1.08,1.08,.86][j%4])
 M.add(segmented_tube(C,R,sides=16,quarter_seam_until=p['proxistele_rings']*4),'homoiostele','homoiostele','theca',{'proximal_rings':p['proxistele_rings'],'distal_segments':p['dististele_segments'],'sharp_thecal_transition':True})
 P=Patch();P.prism([(x,y,z) for x,y,z in [(.0015,.008,.0018),(.004,.008,.0018),(.004,.0105,.0016),(.0015,.0105,.0016)]],[(.0017,.0085,.0031),(.0037,.0085,.0031),(.0037,.0098,.0042),(.0017,.0098,.0042)],1);M.add(P,'suranal','suranal_plate','theca')
 return M.emit('dendrocystites',m,col)

def groove_path(angles,W,L,z):
 P=Patch();cross=[(-1,-.00045),(-1,.00012),(-.48,.00012),(-.48,-.00016),(.48,-.00016),(.48,.00012),(1,.00012),(1,-.00045)];rings=[]
 for i,a in enumerate(angles):
  c=Vector((W*.46*cos(a),L*.46*sin(a),z));join=max(0,1-i/3) if angles[-1]<angles[0] else 0;c=c*(1-join)+Vector((.0063,-.0100,z))*join;r=Vector((cos(a),sin(a),0));rings.append([P.vert(c+r*x*.00045+Vector((0,0,h))) for x,h in cross])
 for i in range(len(rings)-1):
  for k in range(len(cross)):q=(k+1)%len(cross);P.face([rings[i][k],rings[i][q],rings[i+1][q],rings[i+1][k]],2 if k==3 else 1)
 P.face(list(reversed(rings[0])),1);P.face(rings[-1],1);P.base=[ring[k] for ring in rings for k in [0,7]];return P

def trochocystites(cfg,m,col):
 p=cfg['parameters'];M=Mesh();W=p['theca_width_m'];L=p['theca_length_m'];T=p['theca_thickness_m']
 def shape(v):x,y,z=v;return Vector((W*.45*x*(.94-.08*y)+.0006*y,L*.46*y,T*.5*z))
 M.add(sphere_patch(shape),'theca','theca_core');M.add(dual_plates(shape,2,.025),'thecal_plating','thecal_plating','theca')
 P=Patch();N=p['marginal_plate_count']
 for i in range(N):
  a=2*pi*(i+.008)/N;b=2*pi*(i+.992)/N
  def q(t,r,z):return (W*.5*r*cos(t)*( .94-.08*sin(t))+.0006*sin(t),L*.5*r*sin(t),z)
  lower=[q(a,.76,-.0009),q(a,.98,-.0009),q(b,.98,-.0009),q(b,.76,-.0009)];upper=[q(a+.006,.80,.0017),q(a+.006,.97,.00145),q(b-.006,.97,.00145),q(b-.006,.80,.0017)];P.prism(lower,upper,1 if i%3 else 3)
 # A continuous recessed organic/skeletal frame substrate closes the tiny plate joints.
 N2=64; rings=[]
 for rr,zz in [(.72,-.0008),(.985,-.0008),(.985,.0010),(.72,.0010)]:
  rings.append([P.vert((W*.5*rr*cos(2*pi*k/N2)*(.94-.08*sin(2*pi*k/N2))+.0006*sin(2*pi*k/N2),L*.5*rr*sin(2*pi*k/N2),zz)) for k in range(N2)])
 for j in range(4):
  for k in range(N2):q=(k+1)%N2;P.face([rings[j][k],rings[j][q],rings[(j+1)%4][q],rings[(j+1)%4][k]],0)
 M.add(P,'cinctus','marginal_frame','theca',{'visible_plate_count':N})
 M.add(sphere_patch(lambda v:Vector((v.x*.0038,v.y*.0025-.0102,v.z*.0010+.0021)),12,6,1),'operculum','operculum','theca')
 M.add(cup((.0063,-.0100,.00145),(.55,-.65,.52),p['mouth_radius_m'],.00035),'mouth','mouth','cinctus',{'anterolateral_right_of_operculum':True})
 for tag,start,end in [('left',-1.05,-3.93),('right',-1.05,-.265)]:M.add(groove_path([start+(end-start)*j/22 for j in range(23)],W,L,.00167),'groove_'+tag,'marginal_groove','cinctus',{'unequal_arc_degrees':abs(end-start)*180/pi})
 C=[];RR=[];N=p['stele_segments']
 for j in range(N*4+1):
  t=j/(N*4);C.append((.0006,L*.44+p['stele_length_m']*t,-.0001));RR.append((.0016*(1-t)+.0002)*[.88,1.04,1.04,.88][j%4])
 M.add(segmented_tube(C,RR),'homostele','homostele','theca',{'rigid':True,'visible_segments':N});return M.emit('trochocystites',m,col)

def clip_z(poly,lo,hi):
 for boundary,sgn in [(lo,1),(hi,-1)]:
  old=poly;poly=[]
  for a,b in zip(old,old[1:]+old[:1]):
   ina=(a[1]-boundary)*sgn>=0;inb=(b[1]-boundary)*sgn>=0
   if ina:poly.append(a)
   if ina!=inb:
    t=(boundary-a[1])/(b[1]-a[1]);poly.append((a[0]+t*(b[0]-a[0]),boundary))
  if len(poly)<3:return []
 return poly

def helicoplacus(cfg,m,col):
 p=cfg['parameters'];M=Mesh();H=p['height_m'];D=p['max_diameter_m'];R=D/2
 def rad(s):return R*(sin(pi*s)**.75)*(.79+.3*s) if 0<s<1 else 0
 def mapped(v):s=(v.z+1)/2;ang=atan2(v.y,v.x);r=rad(s);return Vector((r*cos(ang),r*sin(ang),H*s))
 M.add(sphere_patch(mapped,32,24),'theca','theca_core',axis=(0,0,1));P=Patch();NS=p['shell_segments'];NR=p['shell_rows'];shift=p['helical_row_shift'];num=0
 for j in range(-1,NR+shift+1):
  for k in range(NS):
   a=2*pi*k/NS;b=2*pi*(k+1)/NS;poly=clip_z([(a,(j-shift*k/NS)/NR),(b,(j-shift*(k+1)/NS)/NR),(b,(j+1-shift*(k+1)/NS)/NR),(a,(j+1-shift*k/NS)/NR)],.035,.965)
   if not poly:continue
   ca=sum(x[0] for x in poly)/len(poly);cz=sum(x[1] for x in poly)/len(poly)
   def mp(q,delta):a,s=q;r=rad(s)+delta;return (r*cos(a),r*sin(a),s*H)
   lower=[mp(q,-.00025) for q in poly];upper=[mp((ca+(a-ca)*.9,cz+(s-cz)*.86),p['plate_relief_m']) for a,s in poly];P.prism(lower,upper,0 if num%5 else 3);num+=1
 M.add(P,'helical_plating','helical_plating','theca',{'actual_closed_plate_count':num,'helix_z_slope_per_positive_angle':-shift/NR,'left_handed':True},axis=(0,0,1))
 mouthz=p['mouth_height_fraction'];mouththeta=-pi/2
 for path,end,branch in [('lower',p['ambulacral_low_fraction'],0),('upperC',p['ambulacral_high_fraction'],-1),('upperD',p['ambulacral_high_fraction'],1)]:
  P=Patch();N=p['ambulacral_stations']
  def center(t):s=mouthz+(end-mouthz)*t;a=mouththeta-2*pi*(s-mouthz)/.32+branch*.14*min(1,t*5);return a,s
  for j in range(N):
   for side in [-1,1]:
    t0=(j+.025)/N;t1=(j+.975)/N;a0,s0=center(t0);a1,s1=center(t1);w=p['ambulacral_width_m']/2
    poly=[(a0+side*.04*w/rad(s0),s0),(a0+side*.96*w/rad(s0),s0),(a1+side*.96*w/rad(s1),s1),(a1+side*.04*w/rad(s1),s1)]
    def mp(q,d):a,s=q;r=rad(s)+d;return (r*cos(a),r*sin(a),H*s)
    P.prism([mp(q,-.00015) for q in poly],[mp(q,.00046) for q in poly],1)
  M.add(P,'ambulacrum_'+path,'ambulacral_path','theca',{'branch':path,'stations':N,'z_start_fraction':mouthz,'z_end_fraction':end,'actual_pair_rows':2},axis=(0,0,1))
 n=Vector((cos(mouththeta),sin(mouththeta),0));c=n*(rad(mouthz)+.00047)+Vector((0,0,H*mouthz));M.add(cup(c,n,p['mouth_radius_m'],.00032),'mouth','mouth','theca');return M.emit('helicoplacus',m,col)

def stromatocystites(cfg,m,col):
 p=cfg['parameters'];M=Mesh();R=p['diameter_m']/2;T=p['disc_thickness_m'];amp=p['pentagonal_amplitude_fraction']
 def radius(a):return R*(1+amp*cos(5*(a-pi/2)))
 def shape(v):a=atan2(v.y,v.x);r=radius(a);return Vector((r*v.x,r*v.y,T*.5*v.z))
 M.add(sphere_patch(shape,40,12),'theca','theca_core');M.add(dual_plates(shape,3,.045,lambda v:v.z>.96 or v.z<-.92),'thecal_plating','thecal_plating','theca',{'fully_plated_both_surfaces':True,'central_oral_and_aboral_pad_regions_differentiated':True})
 for ray in range(5):
  a=pi/2+2*pi*ray/5;P=Patch();N=p['ambulacral_stations'];rmax=radius(a)*.955
  def angle(r):
   group=0 if ray==0 else (1.5 if ray in [1,2] else 3.5);start=pi/2+2*pi*group/5;u=min(1,r/.0045);return start+(a-start)*u
  def mp(r,x,delta):aa=angle(r);rr=radius(aa);z=T/2*sqrt(max(0,1-(r/rr)**2));return (r*cos(aa)-x*sin(aa),r*sin(aa)+x*cos(aa),z+delta)
  for j in range(N):
   r0=.00072+(rmax-.00072)*(j+.02)/N;r1=.00072+(rmax-.00072)*(j+.98)/N;w=p['ambulacral_width_m']/2
   for side in [-1,1]:
    poly=[(r0,side*.05*w),(r0,side*.97*w),(r1,side*.97*w),(r1,side*.05*w)];P.prism([mp(r,x,-.00020) for r,x in poly],[mp(r,x,p['ambulacral_relief_m']) for r,x in poly],1)
  M.add(P,'ambulacrum_'+str(ray),'ambulacral_path','theca',{'ray':ray,'paired_cover_plate_stations':N,'surface_bound_not_projecting_arm':True})
 M.add(cup((0,0,T/2+.00055),(0,0,1),p['mouth_radius_m'],.0003),'mouth','mouth','theca');a=pi/2+pi;r=.008;z=T/2*sqrt(1-(r/radius(a))**2);M.add(cup((r*cos(a),r*sin(a),z+.00045),(0,0,1),p['periproct_radius_m'],.00023),'periproct','periproct','theca')
 M.add(sphere_patch(lambda v:Vector((v.x*.0033,v.y*.0033,v.z*.0004-T/2)),16,6,3),'attachment_pad','attachment_pad','theca');return M.emit('stromatocystites',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();aid=cfg['asset_id'];col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])];globals()[aid](cfg,m,col);bpy.context.view_layer.update();export_asset(aid,aid,'animals',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Original immutable batch107 freeze. All dimensions nominal artistic; fossil/cast reference pixels not incorporated.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 (out/'execution.json').write_text(json.dumps({'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':start,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clock_note':'Executor filesystem/process clock is separately recorded and may differ from clock.curr_time; no provider timestamp inferred.','blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()},indent=2)+'\n')
if __name__=='__main__':main()
