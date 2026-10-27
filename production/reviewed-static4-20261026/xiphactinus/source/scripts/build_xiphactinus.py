# SPDX-License-Identifier: MIT
"""Original Xiphactinus audax reference-led living reconstruction, meters.
Factory-process deterministic source, no existing fish mesh, image texture or scan.
The fin shell is made from explicit midsurface triangles, not two n-gons.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
import asset_common as ac
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--gray',action='store_true')
A=p.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
coll=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[coll['asset_root']]
M={k:ac.make_material('xiphactinus-'+k,'#969696' if A.gray else c,roughness=.81,double_sided=False) for k,c in C['palette'].items()};parts={};links=[];fins=[]
def mesh(name,vertices,faces,materials,indices=None):
 o=ac.mesh_object(name,vertices,faces,[M[k] for k in materials],coll)
 if indices is not None:
  for f,i in zip(o.data.polygons,indices):f.material_index=i
 o['semantic_role']=name;vg=o.vertex_groups.new(name=name);vg.add(list(range(len(vertices))),1,'REPLACE');parts[name]=o;return o
P=C['profile_y_width_low_high_m'];N=C['ring_count']
def profile(y):
 for a,b in zip(P,P[1:]):
  if y<=b[0]:
   t=max(0,(y-a[0])/(b[0]-a[0]));return tuple(a[k]+t*(b[k]-a[k]) for k in range(1,4))
 return P[-1][1:]
def flank(y,z):
 w,l,h=profile(y);t=(z-(l+h)/2)/((h-l)/2);return w*math.sqrt(max(0,1-t*t))
# Each design interval is subdivided once in the trunk for restrained cell scale.
sections=[]
for i,(a,b) in enumerate(zip(P,P[1:])):
 sections.append(a)
 if i>=6:sections.append([(a[k]+b[k])/2 for k in range(4)])
sections.append(P[-1]);V=[]
for i,(y,w,l,h) in enumerate(sections):
 for j in range(N):
  a=2*math.pi*j/N;yy=y+(.012*math.sin(2*a) if 7<=i<len(sections)-2 else 0);ww,ll,hh=profile(yy)
  V.append((ww*math.sin(a),yy,(ll+hh)/2+(hh-ll)/2*math.cos(a)))
F=[];I=[];cells=0
for i in range(len(sections)-1):
 for j in range(N):
  q=[i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j];a=2*math.pi*(j+.5)/N;c=1 if math.cos(a)>.65 else 2 if math.cos(a)<-.63 else 0
  if i<6:
   F.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])]);I.extend([1 if math.cos(a)>.65 else 2 if math.cos(a)<-.63 else 3]*2);continue
  center=sum((Vector(V[k]) for k in q),Vector())/4;center+=Vector((math.sin(a),0,math.cos(a)))*C['scale_relief_m'];ci=len(V);V.append(tuple(center))
  for k in range(4):F.append((q[k],q[(k+1)%4],ci));I.append(c)
  cells+=1
for i,ids in [(0,list(range(N))),(len(sections)-1,[(len(sections)-1)*N+j for j in range(N)])]:
 center=sum((Vector(V[k]) for k in ids),Vector())/N;ci=len(V);V.append(tuple(center))
 for j in range(N):F.append((ci,ids[j],ids[(j+1)%N]));I.append(3 if i==0 else 0)
body=mesh('01-deep-head-tapered-body',V,F,['flank','back','belly','head'],I);body['nominal_head_length_m']=.72;body['connected_scale_cells']=cells
# Closed cross-section swept tubes make modest deeply embedded mouth/opercular seams.
def tube(name,points,radii,mat,parent=body.name):
 pts=list(map(Vector,points));v=[];n=8
 for i,p in enumerate(pts):
  tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();axis=Vector((1,0,0));u=(axis-tangent*axis.dot(tangent)).normalized();w=tangent.cross(u).normalized()
  for j in range(n):v.append(tuple(p+radii[i]*(u*math.cos(2*math.pi*j/n)+w*math.sin(2*math.pi*j/n))))
 f=[]
 for i in range(len(pts)-1):
  for j in range(n):
   a=i*n+j;b=i*n+(j+1)%n;c=(i+1)*n+(j+1)%n;d=(i+1)*n+j;f.extend([(a,b,c),(a,c,d)])
 for i in [0,len(pts)-1]:
  ci=len(v);v.append(tuple(pts[i]))
  for j in range(n):f.append((ci,i*n+j,i*n+(j+1)%n))
 o=mesh(name,v,f,[mat]);links.append({'child':name,'parent':parent,'intent':'closed shallow seam embedded into fleshy surface'});return o
# Nearly closed mouth ascends steeply at the front, no theatrically exposed teeth.
for label,s in [('L',-1),('R',1)]:
 yz=[(-2.14,1.30),(-2.10,1.27),(-2.04,1.19),(-1.94,1.10),(-1.84,1.04),(-1.73,1.02)]
 tube(label+'-near-closed-upturned-mouth',[(s*(flank(y,z)-.002),y,z) for y,z in yz],[.009,.010,.010,.009,.008,.003],'eye')
 yz=[(-1.64,1.35),(-1.51,1.27),(-1.45,1.12),(-1.46,.95),(-1.54,.81),(-1.64,.73)]
 sampled=[]
 for a,b in zip(yz,yz[1:]):
  for k in range(4):
   q=k/4;sampled.append((a[0]*(1-q)+b[0]*q,a[1]*(1-q)+b[1]*q))
 sampled.append(yz[-1]);radii=[.007]*len(sampled);radii[0]=radii[-1]=.003
 tube(label+'-subtle-gill-cover-seam',[(s*(flank(y,z)-.0005),y,z) for y,z in sampled],radii,'back')
# Anatomical eye volumes; no emission or detached spheres.
def oval(name,center,radii,material,parent):
 v=[(center[0],center[1],center[2]+radii[2])];nr=6;ns=16
 for i in range(1,nr):
  a=math.pi*i/nr
  for j in range(ns):
   b=2*math.pi*j/ns;v.append((center[0]+radii[0]*math.sin(a)*math.cos(b),center[1]+radii[1]*math.sin(a)*math.sin(b),center[2]+radii[2]*math.cos(a)))
 v.append((center[0],center[1],center[2]-radii[2]));f=[]
 for j in range(ns):f.append((0,1+j,1+(j+1)%ns))
 for i in range(nr-2):
  for j in range(ns):
   a=1+i*ns+j;b=1+i*ns+(j+1)%ns;c=b+ns;d=a+ns;f.extend([(a,b,c),(a,c,d)])
 for j in range(ns):f.append((len(v)-1,1+(nr-2)*ns+j,1+(nr-2)*ns+(j+1)%ns))
 mesh(name,v,f,[material]);links.append({'child':name,'parent':parent,'intent':'eye volume embedded into head or eye rim'})
for label,s in [('L',-1),('R',1)]:
 y=-1.96;z=1.35;x=flank(y,z)
 oval(label+'-fleshy-orbit',(s*(x-.004),y,z),(.018,.075,.068),'head',body.name)
 oval(label+'-nonemissive-eye',(s*(x+.010),y-.002,z),(.015,.045,.043),'eye',label+'-fleshy-orbit')
# Fins: fixed planar mid-surface, same explicit triangle connectivity both sides.
# Thickness uses the local normal obtained from actual mid-surface edges. No
# nonplanar-ngon triangulation, fixed-global-axis pseudo-thickness, or doubleSide.
def fin(name,roots,tips,identity):
 r=list(map(Vector,roots));t=list(map(Vector,tips));normal=(r[1]-r[0]).cross(t[0]-r[0]).normalized();n=len(r);ts=[0,.28,.62,1];v=[]
 mid=[r[i].lerp(t[i],u) for i in range(n) for u in ts];origin=mid[0]
 assert max(abs((p-origin).dot(normal)) for p in mid)<1e-6,(name,'not planar')
 for sign in [-1,1]:
  for i in range(n):
   for k,u in enumerate(ts):v.append(tuple(mid[i*4+k]+normal*sign*(.010*(1-u)+.004*u+(.0008 if i%2==0 and k>0 else 0))))
 count=len(mid);f=[];mi=[]
 for offset in [0,count]:
  for i in range(n-1):
   for k in range(3):
    a=offset+i*4+k;b=a+4;c=b+1;d=a+1;f.extend([(a,b,c),(a,c,d)]);mi.extend([1 if i%3==0 else 0]*2)
 perimeter=[i*4 for i in range(n)]+[(n-1)*4+k for k in range(1,4)]+[i*4+3 for i in range(n-2,-1,-1)]+[2,1]
 for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]):f.extend([(a,b,count+b),(a,count+b,count+a)]);mi.extend([0,0])
 o=mesh(name,v,f,['fin','flank'],mi);o['fin_identity']=identity;o['mid_surface_explicit_triangles']=True;o['local_normal']=list(normal)
 links.append({'child':name,'parent':body.name,'intent':'closed fin root genuinely embedded into continuous trunk'})
 fins.append({'name':name,'identity':identity,'roots_m':roots,'tips_m':tips,'local_normal':list(normal),'thickness_m':[.020,.008],'topology':'same explicit mid-surface triangle connectivity, opposite sides and closed perimeter','ray_count':'stylized not literal'})
ys=[.55,.65,.76,.87,.98,1.09,1.20];roots=[(0,y,profile(y)[2]-.020) for y in ys];tips=[(0,y,z) for y,z in [(.68,1.35),(.95,1.64),(1.10,1.74),(1.12,1.50),(1.17,1.30),(1.23,1.17),(1.25,1.08)]];fin('02-posterior-dorsal',roots,tips,'single dorsal')
ys=[.48,.60,.72,.84,.96,1.08,1.18];roots=[(0,y,profile(y)[1]+.020) for y in ys];tips=[(0,y,z) for y,z in [(.60,.62),(.91,.39),(1.08,.32),(1.13,.51),(1.18,.66),(1.23,.78),(1.23,.87)]];fin('03-posterior-anal',roots,tips,'single anal')
roots=[(0,1.48,.92+i*.01) for i in range(9)];tips=[(0,y,z) for y,z in [(2.15,.14),(2.12,.34),(1.98,.55),(1.78,.78),(1.68,.96),(1.78,1.14),(1.98,1.39),(2.12,1.62),(2.15,1.80)]];fin('04-deep-forked-caudal',roots,tips,'single forked caudal')
for label,s in [('L',-1),('R',1)]:
 # Roots share a short vertical attachment line inside the flank; outward swept
 # planar span has a real local normal, with no diagonal twist at the root.
 r=[(s*.235,-1.40,1.04-i*.035) for i in range(6)]
 # In this plane x and y displacement have a fixed ratio, z is free.
 spans=[.20,.34,.45,.48,.40,.23];dz=[-.04,-.10,-.17,-.24,-.28,-.25]
 t=[(s*(.235+q),-1.40+q*1.55,r[i][2]+dz[i]) for i,q in enumerate(spans)];fin(label+'-long-swept-pectoral',r,t,'paired pectoral '+label)
 r=[(s*.065,.14+i*.035,.765) for i in range(5)]
 # Pelvic plane spans lateral/up-down axis and longitudinal root rail.
 span=[.06,.12,.17,.16,.09];dy=[.10,.21,.32,.35,.27]
 t=[(s*(.065+q),r[i][1]+dy[i],.765-q*1.7) for i,q in enumerate(span)];fin(label+'-small-pelvic',r,t,'paired pelvic '+label)
assert len(fins)==7
# Confirm attachment with actual surfaces/contained vertices, not bounding boxes.
bpy.context.view_layer.update()
cache={n:BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],epsilon=0) for n,o in parts.items()}
def inside(point,tree):
 direction=Vector((1,.137,.219)).normalized();p=point.copy();hits=0
 for _ in range(80):
  h,_,_,_=tree.ray_cast(p,direction,20)
  if h is None:break
  hits+=1;p=h+direction*1e-6
 return hits%2==1
for link in links:
 a,b=link['child'],link['parent'];overlaps=len(cache[a].overlap(cache[b]));contained=sum(inside(parts[a].matrix_world@v.co,cache[b]) for v in parts[a].data.vertices)
 link.update(boundary_intersection_pairs=overlaps,child_vertices_inside_parent=contained,status='PASS' if overlaps or contained else 'FAIL')
fail=[l for l in links if l['status']=='FAIL']
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'Actual BVH triangle surface intersection plus ray-parity containment','checks':links,'failed':fail,'fin_count':7,'fins':fins,'self_intersection':'separate strict decoded GLB audit required; positive closed volume never substitutes'},indent=2));assert not fail,fail
offset=ac.ground_asset(coll,center_xy=True)
for o in parts.values():
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
root['species']='Xiphactinus audax';root['seven_fins']=[f['name'] for f in fins];root['reconstruction_notes']=C['reconstruction_notes'];root['representation']='living-reconstruction'
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=ac.export_asset('xiphactinus',{'en':'Xiphactinus audax','zh':'剑射鱼 Xiphactinus audax'},'fish',coll,metadata={'revision':'r001','representation':'living-reconstruction','description':{'en':'Original short deep-headed Xiphactinus reconstruction, seven thin solid fins and deeply forked tail.','zh':'原创剑射鱼活体复原：深短头、七枚闭合薄实心鳍和深叉尾。'},'generator':'scripts/build_xiphactinus.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':4.3,'reconstruction_notes':C['reconstruction_notes'],'origin_note':'Lowest swimming surface Z0; horizontal bounds centered, no terrestrial support claim.','anatomy':{'fins':7,'dorsal':1,'anal':1,'caudal':1,'pectoral':2,'pelvic':2}},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'export_meshes':len(parts),'fin_count':7,'datum_offset_m':offset,'glb_sha256':record['sha256']['glb'],'default_area_epsilon_m2':1e-10},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
