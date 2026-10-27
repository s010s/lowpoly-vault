# SPDX-License-Identifier: MIT
"""Original reference-led Dapedium stollorum reconstruction.
Build from factory: blender -b -t 2 --factory-startup --python build_dapedium.py -- --config config.json --output-dir PATH [--gray]
No imported model/texture. Coordinates below in mm, converted once. A single
watertight loft is subdivided into connected bevelled ganoid panels; seven fins
are closed ribbons with embedded bases, never DoubleSide sheets.
"""
import bpy,bmesh,json,math,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
import asset_common as ac
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--gray',action='store_true')
A=p.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
coll=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[coll['asset_root']];S=C['construction_mm_to_m']
mats={k:ac.make_material('dapedium-'+k,'#929292' if A.gray else col,roughness=.82,double_sided=False) for k,col in C['palette'].items()}
parts={};links=[];fin_names=[];geometry_records=[]
def add(name,verts,faces,mat,indices=None):
 materials=[mats[k] for k in mat] if isinstance(mat,list) else mats[mat]
 o=ac.mesh_object(name,[[float(x)*S for x in v] for v in verts],faces,materials,coll)
 if indices is not None:
  for poly,i in zip(o.data.polygons,indices):poly.material_index=i
 o['semantic_role']=name;v=o.vertex_groups.new(name=name);v.add(list(range(len(o.data.vertices))),1,'REPLACE');parts[name]=o
 return o

def connect(a,b,kind):links.append({'child':a,'parent':b,'kind':kind})
sections=C['sections_mm'];N=C['body_ring_vertices']
def profile(y):
 if y<=sections[0][0]:return sections[0][1:]
 for a,b in zip(sections,sections[1:]):
  if y<=b[0]:
   t=(y-a[0])/(b[0]-a[0]);return [a[k]*(1-t)+b[k]*t for k in range(1,4)]
 return sections[-1][1:]
def flank(y,z):
 w,lo,hi=profile(y);mid=(lo+hi)/2;r=(hi-lo)/2
 return w*math.sqrt(max(0,1-((z-mid)/r)**2))
# Connected ganoid armor, subtly skewed oblique rows. Front head is smooth faceted.
verts=[]
for i,(y,w,lo,hi) in enumerate(sections):
 for j in range(N):
  t=2*math.pi*j/N
  # 1.4mm skew produces coherent oblique rows without changing the silhouette.
  yy=y+(1.4*math.sin(2*t) if 5<=i<len(sections)-2 else 0)
  ww,ll,hh=profile(yy);verts.append((ww*math.sin(t),yy,(ll+hh)/2+(hh-ll)/2*math.cos(t)))
faces=[];indices=[];scale_cells=0
for i in range(len(sections)-1):
 for j in range(N):
  ids=[i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j]
  corners=[Vector(verts[q]) for q in ids];center=sum(corners,Vector())/4
  zcos=math.cos(2*math.pi*(j+.5)/N)
  color=1 if zcos>.73 else (2 if zcos<-.70 else 0)
  if i<5 or A.gray:
   faces.append(tuple(ids));indices.append(3 if i<5 else color);continue
  # Each quad has a flat central plateau and low bevels, not a spike.
  normal=Vector((center.x/(27.5**2),0,(center.z-110)/(100**2))).normalized()
  relief=C['scale_relief_mm']*(.65+.35*(1-abs(zcos)))
  inset=C['scale_inset'];inside=[]
  for a in corners:
   v=a.lerp(center,inset)+normal*relief;inside.append(len(verts));verts.append(tuple(v))
  for k in range(4):faces.append((ids[k],ids[(k+1)%4],inside[(k+1)%4],inside[k]));indices.append(color)
  faces.append(tuple(inside));indices.append(color if (i+j)%6 else 3);scale_cells+=1
faces.append(tuple(reversed(range(N))));indices.append(3)
faces.append(tuple((len(sections)-1)*N+j for j in range(N)));indices.append(0)
body=add('01-continuous-ganoid-body',verts,faces,['armor','dorsal','belly','head'],indices)
body['continuous_scale_panels']=scale_cells;body['species']='Dapedium stollorum';body['head_region_unscaled']=True
# Low-profile closed opercular shields, embedded into body; wide integrated gill
# region without a carved canyon or disembodied armor disks.
for side,s in [('L',-1),('R',1)]:
 outline=[(-139,111),(-134,140),(-123,160),(-110,153),(-103,123),(-107,89),(-122,69),(-136,86)]
 yy=sum(p[0] for p in outline)/len(outline);zz=sum(p[1] for p in outline)/len(outline)
 v=[(s*(flank(y,z)+.5),y,z) for y,z in outline]+[(s*(flank(y,z)-1.5),y,z) for y,z in outline]
 v.append((s*(flank(yy,zz)+.65),yy,zz));v.append((s*(flank(yy,zz)-1.5),yy,zz));n=len(outline);f=[]
 for j in range(n):f.extend([(2*n,j,(j+1)%n),(2*n+1,n+(j+1)%n,n+j),(j,n+j,n+(j+1)%n,(j+1)%n)])
 name=side+'-opercular-shield';add(name,v,f,'head');connect(name,body.name,'opercular shield embedded into continuous flank')

def ellipsoid(name,center,radii,mat,n=12,rings=6):
 v=[(center[0],center[1],center[2]+radii[2])]
 for k in range(1,rings):
  t=math.pi*k/rings
  for j in range(n):
   a=2*math.pi*j/n;v.append((center[0]+radii[0]*math.sin(t)*math.cos(a),center[1]+radii[1]*math.sin(t)*math.sin(a),center[2]+radii[2]*math.cos(t)))
 v.append((center[0],center[1],center[2]-radii[2]));f=[]
 for j in range(n):f.append((0,1+j,1+(j+1)%n))
 for k in range(rings-2):
  for j in range(n):f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):f.append((len(v)-1,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
 add(name,v,f,mat);return name
for side,s in [('L',-1),('R',1)]:
 y=-147;z=124;x=flank(y,z)
 rim=ellipsoid(side+'-subtle-eye-rim',(s*x,y,z),(2.0,5.5,5.5),'belly');connect(rim,body.name,'eye rim partially embedded in head')
 eye=ellipsoid(side+'-nonemissive-eye',(s*(x+1.35),y-.35,z),(1.2,3.6,3.8),'eye');connect(eye,rim,'pupil intersects surrounding eye rim')
# Compact closed terminal mouth; dark narrow lip intersects the front head cap.
mouth=ellipsoid('closed-terminal-mouth',(0,-164.6,101.4),(4.3,.75,.65),'dorsal',12,4);connect(mouth,body.name,'closed mouth seam on terminal head')

# Each fin has its own editable closed manifold ribbon with connected web.
# Longitudinal bands carry restrained alternating colors, not separate stiff rods.
def fin(name,roots,tips,normal,kind):
 n=len(roots);normal=Vector(normal).normalized();v=[];ts=[0,.42,.77,1]
 for sign in [-1,1]:
  for i,(r,e) in enumerate(zip(roots,tips)):
   r,e=Vector(r),Vector(e)
   for t in ts:
    p=r.lerp(e,t);thick=1.25*(1-t)+.55*t
    # tiny ray-like ridges remain within the contiguous membrane surface
    p+=normal*sign*(thick+(.18 if i%2==0 and t>0 else 0));v.append(tuple(p))
 f=[];mi=[];M=n*len(ts)
 for sign in [0,1]:
  off=sign*M
  for i in range(n-1):
   for k in range(3):
    f.append((off+i*4+k,off+(i+1)*4+k,off+(i+1)*4+k+1,off+i*4+k+1));mi.append(1 if i%3==0 else 0)
 perimeter=[i*4 for i in range(n)]+[(n-1)*4+k for k in range(1,4)]+[i*4+3 for i in range(n-2,-1,-1)]+[2,1]
 for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]):f.append((a,b,M+b,M+a));mi.append(0)
 o=add(name,v,f,['fin','head'],mi);fin_names.append(name);o['fin_identity']=kind;o['closed_thin_solid']=True
 connect(name,body.name,'fin root vertices physically embedded in continuous body');geometry_records.append({'fin':name,'identity':kind,'root_centerline_mm':roots,'outer_margin_mm':tips,'normal':list(normal),'root_half_thickness_mm':1.25,'tip_half_thickness_mm':.55,'rays_are_stylized_not_count_claim':True})
# r002 local repair: the former radial strip mapping folded at the first ray.
# Use a single planar, simple boundary instead; prove every center fan triangle
# has one positive projected orientation, then give identical front/back topology.
def pectoral_planar(name,roots,tips,kind):
 r=[Vector(p) for p in roots];e=[Vector(p) for p in tips]
 origin=sum(r,Vector())/len(r);direction=sum(e,Vector())/len(e)-origin
 normal=direction.cross(r[-1]-r[0]).normalized()
 original=[r[0]]+e+list(reversed(r[1:]))
 projected=[p-normal*(p-origin).dot(normal) for p in original]
 center=sum(projected,Vector())/len(projected);n=len(projected)
 areas=[(projected[(i+1)%n]-projected[i]).cross(center-projected[i]).dot(normal) for i in range(n)]
 # Positive fan sectors + simple star polygon guarantee a nonfolding midsurface.
 if min(areas)<=1e-4:raise RuntimeError('Pectoral midsurface fan is not a strict star polygon')
 # The outline is explicitly checked for nonadjacent edge crossings in its own 2D plane.
 u=direction.normalized();v=normal.cross(u).normalized()
 xy=[((q-origin).dot(u),(q-origin).dot(v)) for q in projected]
 def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 for i in range(n):
  for j in range(i+1,n):
   if j==i+1 or (i==0 and j==n-1):continue
   a,b=xy[i],xy[(i+1)%n];c,d=xy[j],xy[(j+1)%n]
   if orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0:raise RuntimeError('Pectoral outline crosses itself')
 thickness=[C['pectoral_repair']['root_half_thickness_mm']]+[C['pectoral_repair']['tip_half_thickness_mm']]*len(e)+[C['pectoral_repair']['root_half_thickness_mm']]*(len(r)-1)
 vv=[]
 for sign in [-1,1]:
  vv.extend(tuple(q+normal*(sign*t)) for q,t in zip(projected,thickness))
  vv.append(tuple(center+normal*(sign*C['pectoral_repair']['center_half_thickness_mm'])))
 f=[];mi=[];M=n+1
 for i in range(n):
  j=(i+1)%n;f.extend([(n,j,i),(M+n,M+i,M+j),(i,j,M+j),(i,M+j,M+i)]);mi.extend([1 if i%3==0 else 0,1 if i%3==0 else 0,0,0])
 o=add(name,vv,f,['fin','head'],mi);fin_names.append(name);o['fin_identity']=kind;o['closed_thin_solid']=True;o['repair_revision']='r002 nonfolding planar midsurface'
 connect(name,body.name,'repaired planar fin root embedded into unchanged body')
 geometry_records.append({'fin':name,'identity':kind,'method':'simple projected polygon / strict positive center fan / paired same triangle indices / normal-directed positive thickness','normal':list(normal),'original_outline_mm':[list(x) for x in original],'projected_outline_mm':[list(x) for x in projected],'center_mm':list(center),'projected_triangle_double_areas_mm2':areas,'all_projected_triangles_same_positive_sign':True,'max_projection_displacement_mm':max((a-b).length for a,b in zip(original,projected)),'outline_edges_non_crossing':True,'half_thickness_mm':thickness,'center_half_thickness_mm':C['pectoral_repair']['center_half_thickness_mm']})

# Seam-like median fins: anterior rays tallest, distally diminishing.
ys=[-14,0,14,28,42,56,70,84,98,105];heights=[6,24,23,21,18,15,11,8,4,1]
roots=[(0,y,profile(y)[2]-2.0) for y in ys]
tips=[(0,y+4,profile(y)[2]+h) for y,h in zip(ys,heights)]
fin('02-dorsal-seam-fin',roots,tips,(1,0,0),'single posterior dorsal')
ys=[5,18,31,44,57,70,83,96,104];heights=[6,25,23,19,15,11,7,3,1]
roots=[(0,y,profile(y)[1]+2.0) for y in ys]
tips=[(0,y+4,profile(y)[1]-h) for y,h in zip(ys,heights)]
fin('03-anal-seam-fin',roots,tips,(1,0,0),'single posterior anal')
roots=[(0,109,92+i*1.75) for i in range(9)]
tips=[(0,y,z) for y,z in [(166,56),(173,64),(175,77),(168,91),(165,100),(168,109),(175,124),(173,137),(166,145)]]
fin('04-broad-shallow-notch-caudal-fin',roots,tips,(1,0,0),'single broad caudal fan')
for side,s in [('L',-1),('R',1)]:
 roots=[]
 for i,z in enumerate([108,102,96,90,84]):
  y=-106+i*.6;roots.append((s*(flank(y,z)-1.0),y,z))
 tips=[(s*x,y,z) for x,y,z in [(36,-84,98),(43,-72,93),(44,-65,84),(41,-68,76),(34,-78,72)]]
 pectoral_planar(side+'-pectoral-fin',roots,tips,'paired pectoral behind operculum')
 roots=[]
 for y in [-53,-49,-45,-41,-37]:
  z=profile(y)[1]+2.7;roots.append((s*(flank(y,z)-.6),y,z))
 tips=[(s*x,y,z) for x,y,z in [(11,-43,7),(16,-35,3),(18,-29,1),(17,-26,2),(13,-29,6)]]
 fin(side+'-small-pelvic-fin',roots,tips,(s*.25,0,.97),'paired small pelvic')
# Verify actual mesh intersection or containment, not only AABB touch.
bpy.context.view_layer.update()
def bvh(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],epsilon=0)
cache={n:bvh(o) for n,o in parts.items()}
def inside(p,tree):
 d=Vector((1,.137,.219)).normalized();pos=p.copy();count=0
 for _ in range(60):
  hit,_,_,_=tree.ray_cast(pos,d,1)
  if hit is None:break
  count+=1;pos=hit+d*1e-9
 return count%2==1
for link in links:
 a,b=link['child'],link['parent'];intersections=len(cache[a].overlap(cache[b]));contained=sum(inside(parts[a].matrix_world@v.co,cache[b]) for v in parts[a].data.vertices)
 link.update({'boundary_intersection_pairs':intersections,'child_vertices_inside_parent':contained,'status':'PASS' if intersections or contained else 'FAIL'})
failed=[x for x in links if x['status']!='PASS'];assert len(fin_names)==7
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'Source mesh BVH surface intersection and ray-parity contained vertices','count':len(links),'failed':failed,'checks':links,'fin_count':len(fin_names),'fins':geometry_records,'nonadjacent_intersections':'Not exhaustively tested; intended part intersections annotated.'},indent=2))
if failed:raise RuntimeError('Disconnected anatomy: '+repr(failed))
# Datum is lowest swimming surface, no stage/ground geometry or support.
offset=ac.ground_asset(coll,center_xy=True)
for o in coll.all_objects:
 if o.type=='MESH':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
root['species']='Dapedium stollorum';root['seven_fins']=fin_names;root['reconstruction_notes']=C['reconstruction_notes'];root['representation']='living-reconstruction'
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=ac.export_asset(C['asset_id'],{'en':'Dapedium stollorum','zh':'深体硬鳞鱼 Dapedium'},'fish',coll,metadata={'revision':C['revision'],'representation':'living-reconstruction','description':{'en':'Original Dapedium stollorum-inspired living reconstruction: deep ganoid body, compact head and seven closed solid fins.','zh':'原创深体硬鳞鱼复原：侧扁椭圆鳞甲躯干、紧凑头部与七枚闭合实心鳍。'},'reconstruction_notes':C['reconstruction_notes'],'origin_note':'Lowest swimming surface at Z0, horizontal bounds centered; no substrate contact claim.','generator':'scripts/build_dapedium.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.34,'anatomy':{'fins':7,'paired_pectoral':2,'paired_pelvic':2,'dorsal':1,'anal':1,'caudal':1,'continuous_scale_panels':scale_cells}},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'export_meshes':len(parts),'fin_count':len(fin_names),'scale_panels':scale_cells,'datum_offset_m':offset,'glb_sha256':record['sha256']['glb'],'default_area_epsilon_m2':1e-10},indent=2))
print('BUILD_COMPLETE',record['sha256']['glb'])
