# SPDX-License-Identifier: MIT
"""Original reference-led Pterichthyodes milleri; numeric mm converted to meters.
No imported meshes. Connected head/shield/posterior axis; paired bony paddles;
one dorsal; a single lower caudal web beneath the continuing upper tail axis.
"""
import bpy,bmesh,json,math,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import delaunay_2d_cdt
sys.path.insert(0,str(Path(__file__).parent));import asset_common as ac
P=argparse.ArgumentParser();P.add_argument('--config',type=Path,required=True);P.add_argument('--output-dir',type=Path,required=True);P.add_argument('--gray',action='store_true');A=P.parse_args(sys.argv[sys.argv.index('--')+1:])
C=json.loads(A.config.read_text());OUT=A.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
coll=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[coll['asset_root']]
mats={k:ac.make_material('pterichthyodes-'+k,'#929292' if A.gray else col,roughness=.88,double_sided=False) for k,col in C['palette'].items()}
parts={};links=[]
def add(name,verts,faces,materials,indices=None):
 m=[mats[k] for k in materials] if isinstance(materials,list) else mats[materials]
 o=ac.mesh_object(name,[[float(x)*.001 for x in v] for v in verts],faces,m,coll)
 if indices:
  for p,k in zip(o.data.polygons,indices):p.material_index=k
 o['semantic_role']=name;vg=o.vertex_groups.new(name=name);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');parts[name]=o;return o

def attach(a,b,kind):links.append({'child':a,'parent':b,'kind':kind})
# Main body cross sections: the head is genuinely continuous with the armor.
# Broad lower surface is horizontal while crown forms the arched armored box.
sections=C['sections_mm'];base_sections=sections[:]
# r002 modifies only armor-region surface subdivision. No circumferential rings.
def sample(y):
 for a,b in zip(base_sections,base_sections[1:]):
  if a[0]<=y<=b[0]:
   t=(y-a[0])/(b[0]-a[0]);return [y]+[a[k]*(1-t)+b[k]*t for k in [1,2,3]]
 raise ValueError(y)
angles=sorted(set([j*15 for j in range(24)]+[40,50,310,320]));N=len(angles)

def body_point(y,w,lo,hi,theta):
 c=math.cos(theta);sn=math.sin(theta)
 z=lo+(hi-lo)*(.43+.57*c) if c>=0 else lo+(hi-lo)*.43*max(0,(c+.866)/.866)
 return (w*sn,y,z)
v=[]
for i,(y,w,lo,hi) in enumerate(sections):
 for j in range(N):
  theta=math.radians(angles[j]);q=Vector(body_point(y,w,lo,hi,theta))
  v.append(tuple(q))
f=[];mi=[];scales=0
for i,(a,b) in enumerate(zip(sections,sections[1:])):
 y=(a[0]+b[0])/2
 for j in range(N):
  ids=[i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j];t=math.radians((angles[j]+(angles[(j+1)%N] if j+1<N else 360))/2)
  # Large armor regions are not a random mosaic. Posterior fine cells are
  # shallow connected geometry, not detached scales or sphere decorations.
  color=(0 if abs(math.sin(t))<.72 else 1) if y<-14 else 2
  if math.cos(t)<-.70:color=3
  if a[0]>=-81 and b[0]<=-14 and math.cos(t)>0:continue # replaced by connected crown patch below
  if y<-14 or y>86 or A.gray:
   f.append(ids);mi.append(color)
  else:
   q=sum((Vector(v[k]) for k in ids),Vector())/4
   q+=Vector((math.sin(t),0,math.cos(t)))*C['scale_relief_mm'];ci=len(v);v.append(tuple(q))
   for k in range(4):f.append((ids[k],ids[(k+1)%4],ci));mi.append(color)
   scales+=1
# The upper armored surface is one constrained height-field patch welded to
# existing perimeter vertices in the continuous body. Central and paired side
# regions follow Fig2's layout (not literal metric tracing): a broad central
# polygon with an anterior shoulder, wider middle and posterior medial notch;
# two lateral shoulder/side regions, plus a smaller posterior median region.
# This is NOT an overlapping thin plate or a separate mesh.
central=[(-7,-77),(7,-77),(13,-58),(8,-39),(0,-44),(-8,-39),(-13,-58)]
posterior=[(0,-44),(8,-39),(11,-21),(0,-14),(-11,-21),(-8,-39)]
shoulder_lines=[[(-13,-58),(-21.5,-58)],[(13,-58),(21.5,-58)]]
def poly_offset(poly,d):
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))
 out=[]
 for i,a in enumerate(poly):
  a=Vector(a);p=Vector(poly[i-1]);b=Vector(poly[(i+1)%len(poly)]);e0=(a-p).normalized();e1=(b-a).normalized()
  n0=Vector((e0.y,-e0.x));n1=Vector((e1.y,-e1.x))
  if area<0:n0=-n0;n1=-n1
  bis=(n0+n1).normalized();q=a+bis*(d/bis.dot(n1));out.append(tuple(q))
 return out

def distance_segment(q,a,b):
 q,a,b=Vector(q),Vector(a),Vector(b);d=b-a;t=max(0,min(1,(q-a).dot(d)/d.dot(d)));return (q-(a+t*d)).length

def in_poly(q,poly):
 x,y=q;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
coords=[];lookup={};original={};edges=set()
def point(xy,old=None):
 key=tuple(round(t,6) for t in xy)
 if key not in lookup:lookup[key]=len(coords);coords.append(Vector(xy))
 idx=lookup[key]
 if old is not None:original[idx]=old
 return idx

def constraint(poly,closed=True):
 ids=[point(q) for q in poly]
 for aa,bb in zip(ids,ids[1:]+(ids[:1] if closed else [])):
  if aa!=bb:edges.add(tuple(sorted((aa,bb))))
 return ids
# Every prior top-ring sample remains in the patch. Perimeter input vertices
# map back to the very same main-body IDs, so attachment is topological.
for i,(y,w,lo,hi) in enumerate(sections):
 if not -81<=y<=-14:continue
 for j,deg in enumerate(angles):
  if math.cos(math.radians(deg))>=-1e-10:point(v[i*N+j][:2],i*N+j)
# Exact top-view perimeter, all collinear and curved sample vertices retained.
front=[];back=[];left=[];right=[]
for inp,vid in original.items():
 x,y=coords[inp];w=sample(y)[1]
 if abs(y+81)<1e-5:front.append((x,inp))
 if abs(y+14)<1e-5:back.append((x,inp))
 if abs(x+w)<1e-5:left.append((y,inp))
 if abs(x-w)<1e-5:right.append((y,inp))
boundary=[i for x,i in sorted(front)]+[i for y,i in sorted(right)[1:]]+[i for x,i in sorted(back,reverse=True)[1:]]+[i for y,i in sorted(left,reverse=True)[1:-1]]
for aa,bb in zip(boundary,boundary[1:]+boundary[:1]):edges.add(tuple(sorted((aa,bb))))
constraint(central)
for d in [-.45,.45]:constraint(poly_offset(central,d))
constraint(posterior)
for line in shoulder_lines:constraint(line,False)
# Closed outer face clips triangulation to the actual armor crown perimeter.
cv,ce,cf,ov,oe,of=delaunay_2d_cdt(coords,list(sorted(edges)),[boundary],1,1e-6,True)
vm=[]
central_segments=list(zip(central,central[1:]+central[:1]));posterior_segments=list(zip(posterior,posterior[1:]+posterior[:1]))
for k,q in enumerate(cv):
 x,y=q;yy,w,lo,hi=sample(y);z=lo+(hi-lo)*(.43+.57*math.sqrt(max(0,1-(x/w)**2)))
 d=min(distance_segment(q,a,b) for a,b in central_segments)
 depth=.45 if d<1e-4 else 0
 if any(distance_segment(q,*line)<1e-4 for line in shoulder_lines):depth=max(depth,.30)
 if min(distance_segment(q,a,b) for a,b in posterior_segments)<1e-4:depth=max(depth,.22)
 if abs(y+81)<1e-5 or abs(y+14)<1e-5 or abs(abs(x)-w)<1e-5:depth=0 # preserve all patch perimeter vertices
 z-=depth
 olds=[original[i] for i in ov[k] if i in original]
 if olds:
  vi=olds[0];v[vi]=(v[vi][0],v[vi][1],v[vi][2]-depth)
 else:vi=len(v);v.append((x,y,z))
 vm.append(vi)
for face in cf:
 xy=sum((cv[i] for i in face),Vector((0.,0.)))/len(face)
 color=0 if in_poly(xy,central) or in_poly(xy,posterior) else (4 if xy.y<-58 else 1)
 f.append(tuple(vm[i] for i in face));mi.append(color)
# Explicit cap fans preserve collinear flat-belly rim vertices without zero-area ears.
for ring,mat in [(0,0),(len(sections)-1,2)]:
 ids=[ring*N+j for j in range(N)];center=sum((Vector(v[k]) for k in ids),Vector())/N;ci=len(v);v.append(tuple(center))
 for j in range(N):f.append((ci,ids[j],ids[(j+1)%N]));mi.append(mat)
body=add('01-attached-head-armored-box-and-upper-tail-axis',v,f,['armor','armor_side','tail','belly','armor_shoulder'],mi);body['integrated_fine_scale_cells']=scales;body['continuous_attached_head']=True
# Armor organization is integrated into the closed main mesh as source-led
# central-dorsal, paired shoulder/lateral, and posterior median plate regions.
# No floating plate overlays, disconnected tips or coplanar patch z-fighting.
# Anatomically modest dorsal eyes and attached low headshield. No helmet void.
def ellipsoid(name,center,radii,material,n=12,rings=6):
 verts=[(center[0],center[1],center[2]+radii[2])]
 for k in range(1,rings):
  t=math.pi*k/rings
  for j in range(n):
   a=2*math.pi*j/n;verts.append((center[0]+radii[0]*math.sin(t)*math.cos(a),center[1]+radii[1]*math.sin(t)*math.sin(a),center[2]+radii[2]*math.cos(t)))
 verts.append((center[0],center[1],center[2]-radii[2]));faces=[]
 for j in range(n):faces.append((0,1+j,1+(j+1)%n))
 for k in range(rings-2):
  for j in range(n):faces.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):faces.append((len(verts)-1,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
 add(name,verts,faces,material);return name
for label,s in [('L',-1),('R',1)]:
 rim=ellipsoid(label+'-dorsal-eye-rim',(s*4.4,-90,18.0),(2.9,3.4,1.9),'armor');attach(rim,body.name,'eye surround embedded in continuous attached head')
 eye=ellipsoid(label+'-small-dorsal-eye',(s*4.4,-90.3,19.1),(1.5,1.95,.9),'eye');attach(eye,rim,'small eye lens intersects dorsal rim; no empty opening')
mouth=ellipsoid('ventral-closed-mouth',(0,-97.5,4.8),(3.9,1.3,.55),'armor_side',12,4);attach(mouth,body.name,'subtle closed underside mouth; no teeth')
# Two long articulated BONY paddles, not fan-shaped modern fish fins. The
# joint is a narrowed continuous band inside a single closed mesh per side.
for label,s in [('L',-1),('R',1)]:
 verts=[];rails=C['paddle_rails_mm'];rn=10
 for i,(x,y,z,width,thick) in enumerate(rails):
  a=Vector(rails[max(0,i-1)][:3]);b=Vector(rails[min(len(rails)-1,i+1)][:3]);d=(b-a).normalized();across=Vector((-d.y,d.x,0)).normalized()
  for j in range(rn):
   t=2*math.pi*j/rn;q=Vector((x,y,z))+across*width*math.cos(t)+Vector((0,0,thick*math.sin(t)));verts.append((s*q.x,q.y,q.z))
 faces=[];indices=[]
 for i in range(len(rails)-1):
  for j in range(rn):faces.append((i*rn+j,i*rn+(j+1)%rn,(i+1)*rn+(j+1)%rn,(i+1)*rn+j));indices.append(1 if i==3 else 0)
 faces+=[tuple(reversed(range(rn))),tuple((len(rails)-1)*rn+j for j in range(rn))];indices+=[0,0]
 name=label+'-articulated-bony-pectoral-paddle';o=add(name,verts,faces,['armor','armor_side'],indices);o['proximal_distal_segments']=2;o['not_leg_not_fan']=True;attach(name,body.name,'bony root embedded into lateral anterior shield, continuous proximal/distal articulation')
# Vertical median fins: closed prisms on simple 2D polygons, no crossing
# interpolation rails. Explicit center-fan triangulation works for these convex
# dorsal and caudal outlines; the outline centroid must lie inside each polygon.
def median_fin(name,yz,halfwidth,material):
 n=len(yz);verts=[(s*halfwidth,y,z) for s in [-1,1] for y,z in yz]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
 for j in range(n):faces.append((j,n+j,n+(j+1)%n,(j+1)%n))
 o=add(name,verts,faces,material);o['closed_thin_solid']=True;attach(name,body.name,'closed fin base overlaps continuing posterior tail body')
median_fin('03-single-small-dorsal',[(14,21),(17,29),(22,37),(28,39),(33,36),(38,25),(40,21)],.75,'fin')
median_fin('04-single-lower-caudal-web',[(36,13),(43,7),(55,5),(67,8),(79,17),(90,30),(100,41),(84,33),(65,24),(47,17)],.65,'fin')
# Physical surface/inside contacts, never merely overlapping bounding boxes.
bpy.context.view_layer.update()
def tree(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],epsilon=0)
cache={n:tree(o) for n,o in parts.items()}
def inside(p,t):
 d=Vector((1,.137,.219)).normalized();pos=p.copy();count=0
 for _ in range(100):
  hit,_,_,_=t.ray_cast(pos,d,1)
  if hit is None:break
  count+=1;pos=hit+d*1e-9
 return count%2==1
for link in links:
 a,b=link['child'],link['parent'];hits=len(cache[a].overlap(cache[b]));contained=sum(inside(parts[a].matrix_world@v.co,cache[b]) for v in parts[a].data.vertices)
 link.update(boundary_intersection_pairs=hits,child_vertices_inside_parent=contained,status='PASS' if hits or contained else 'FAIL')
failed=[r for r in links if r['status']=='FAIL']
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'Actual source triangle BVH overlap and ray-parity contained vertices; not AABB-only','checks':links,'failed':failed,'count':len(links),'external_appendages':{'bony_pectoral_paddles':2,'dorsal':1,'caudal':1,'pelvic':0,'anal':0,'legs':0},'joint_semantics':'Each paddle is one closed mesh, continuous through its narrowed articulation.','not_claimed':'Interobject intersections at documented joins intentional; nonjoin visual inspection separate.'},indent=2));assert not failed,failed
shift=ac.ground_asset(coll,center_xy=True)
for o in coll.all_objects:
 if o.type=='MESH':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
root['species']='Pterichthyodes milleri';root['representation']='living-reconstruction';root['evidence_limit']='Fossil photograph, secondary reconstruction and comparative drawing kept distinct. No ancient color inference.'
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=ac.export_asset(C['asset_id'],{'en':'Pterichthyodes milleri — plated antiarch fish','zh':'翼鳍鱼 Pterichthyodes milleri'},'fish',coll,metadata={'revision':'r002','representation':'living-reconstruction','description':{'en':'Original box-armored antiarch with two articulated bony pectoral paddles, one dorsal fin, and a strongly upper-extended tail.','zh':'原创甲箱型翼鳍鱼：两侧关节胸桨、单背鳍和上叶延长尾。'},'reconstruction_notes':C['reconstruction_notes'],'generator':'scripts/build_pterichthyodes.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.2,'origin_note':'Centerline/bounds centered, lowest flat belly Z0; neutral aquatic pose not walking.','anatomy':{'paired_bony_paddles':2,'dorsal':1,'caudal':1,'pelvic':0,'anal':0,'fine_connected_scale_cells':scales}},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'export_meshes':len(parts),'fine_scale_cells':scales,'datum_offset_m':shift,'glb_sha256':record['sha256']['glb'],'default_area_epsilon_m2':1e-10,'armor_patch_vertices':len(cv),'armor_patch_faces':len(cf),'central_plate_xy_mm':central,'posterior_plate_xy_mm':posterior,'shoulder_seams_xy_mm':shoulder_lines},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
