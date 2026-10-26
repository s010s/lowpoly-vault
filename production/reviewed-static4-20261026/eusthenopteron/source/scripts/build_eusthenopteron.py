# SPDX-License-Identifier: MIT
"""Original reference-led small Eusthenopteron foordi. No imported model.
Factory build: blender -b -t 2 --factory-startup --python build_eusthenopteron.py
 -- --config config.json --output-dir PATH [--gray]
Design coordinates are millimeters; export meters. Body is one low-relief loft,
paired fins transition from thick flesh to closed ray-bearing webs. Eight fins.
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
mats={k:ac.make_material('eusthenopteron-'+k,'#929292' if A.gray else col,roughness=.84,double_sided=False) for k,col in C['palette'].items()}
parts={};links=[];fins=[];fin_records=[]
def add(name,verts,faces,material,indices=None):
 m=[mats[k] for k in material] if isinstance(material,list) else mats[material]
 o=ac.mesh_object(name,[[float(x)*S for x in v] for v in verts],faces,m,coll)
 if indices is not None:
  for poly,i in zip(o.data.polygons,indices):poly.material_index=i
 o['semantic_role']=name;vg=o.vertex_groups.new(name=name);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');parts[name]=o;return o

def connect(child,parent,kind):links.append({'child':child,'parent':parent,'kind':kind})
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
# Elongate moderately flattened head flows into thicker trunk. Fine low-relief
# staggered cells are part of the SAME watertight surface, never floating tiles.
v=[]
for i,(y,w,lo,hi) in enumerate(sections):
 for j in range(N):
  t=2*math.pi*j/N;yy=y+(.55*math.sin(2*t) if 7<i<len(sections)-3 else 0)
  ww,ll,hh=profile(yy);v.append((ww*math.sin(t),yy,(ll+hh)/2+(hh-ll)/2*math.cos(t)))
f=[];mi=[];cells=0
for i in range(len(sections)-1):
 for j in range(N):
  ids=[i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j]
  theta=2*math.pi*(j+.5)/N;color=1 if math.cos(theta)>.62 else (2 if math.cos(theta)<-.65 else 0)
  if i<7 or A.gray:
   f.append(tuple(ids));mi.append(3 if i<7 else color);continue
  corners=[Vector(v[k]) for k in ids];center=sum(corners,Vector())/4
  outward=Vector((math.sin(theta),0,math.cos(theta))).normalized();center+=outward*C['scale_relief_mm'];ci=len(v);v.append(tuple(center))
  # Four very shallow facets per cell. No large armor plate bevels or spines.
  for k in range(4):f.append((ids[k],ids[(k+1)%4],ci));mi.append(color)
  cells+=1
f.append(tuple(reversed(range(N))));mi.append(3);f.append(tuple((len(sections)-1)*N+j for j in range(N)));mi.append(0)
body=add('01-continuous-head-trunk-peduncle',v,f,['body','dorsal','belly','head'],mi)
body['fine_connected_scale_cells']=cells;body['head_length_nominal_mm']=43
# Low-profile finite cheek volumes remain embedded in the head. Subtle seam at
# their posterior margin gives the opercular boundary, not a separate disc.
for label,s in [('L',-1),('R',1)]:
 outline=[(-51,29),(-44,32),(-38,29),(-36,22),(-40,12),(-47,11),(-53,17)]
 y0=sum(a for a,b in outline)/len(outline);z0=sum(b for a,b in outline)/len(outline)
 verts=[(s*(flank(y,z)+.22),y,z) for y,z in outline]+[(s*(flank(y,z)-.8),y,z) for y,z in outline]
 verts.extend([(s*(flank(y0,z0)+.25),y0,z0),(s*(flank(y0,z0)-.8),y0,z0)]);n=len(outline);faces=[]
 for j in range(n):faces.extend([(2*n,j,(j+1)%n),(2*n+1,n+(j+1)%n,n+j),(j,n+j,n+(j+1)%n,(j+1)%n)])
 name=label+'-subtle-opercular-cheek';add(name,verts,faces,'head');connect(name,body.name,'opercular volume embedded into head')
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
 y=-65;z=28;x=flank(y,z)
 rim=ellipsoid(label+'-dorsolateral-eye-rim',(s*x,y,z),(1.1,2.3,2),'head');connect(rim,body.name,'eye rim embedded dorsolaterally')
 eye=ellipsoid(label+'-modest-nonemissive-eye',(s*(x+.65),y-.05,z+.12),(.65,1.45,1.35),'eye');connect(eye,rim,'small eye intersects fleshy rim')
mouth=ellipsoid('closed-snout-seam',(0,-79.5,21.3),(2.7,.65,.35),'dorsal',12,4);connect(mouth,body.name,'closed mouth embedded in snout')
# A fin is one closed connected volume with variable thickness along each ray.
# Paired fin intermediate rails define a short fleshy lobe, no detached rod/foot.
def fin(name,roots,tips,normal,identity,lobe=None):
 n=len(roots);normal=Vector(normal).normalized();ts=[0,.25,.48,.72,1];verts=[];thickness=[1.45,1.55,1.05,.46,.25] if lobe else [.75,.6,.43,.32,.22]
 for sign in [-1,1]:
  for i,(r,e) in enumerate(zip(roots,tips)):
   r,e=Vector(r),Vector(e)
   for k,t in enumerate(ts):
    if lobe:
     mid=Vector(lobe[i]);q=r.lerp(mid,t/.48) if t<=.48 else mid.lerp(e,(t-.48)/.52)
    else:q=r.lerp(e,t)
    # Small continuous ray relief, not literal exposed bones.
    ridge=.055 if i%2==0 and k>=3 else 0
    q+=normal*sign*(thickness[k]+ridge);verts.append(tuple(q))
 M=n*len(ts);faces=[];idx=[]
 for side in [0,1]:
  off=side*M
  for i in range(n-1):
   for k in range(4):faces.append((off+i*5+k,off+(i+1)*5+k,off+(i+1)*5+k+1,off+i*5+k+1));idx.append(1 if lobe and k<2 else (2 if i%3==0 else 0))
 perimeter=[i*5 for i in range(n)]+[(n-1)*5+k for k in range(1,5)]+[i*5+4 for i in range(n-2,-1,-1)]+[3,2,1]
 for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]):faces.append((a,b,M+b,M+a));idx.append(0)
 o=add(name,verts,faces,['fin','body','head'],idx);o['fin_identity']=identity;o['closed_thin_solid']=True;o['fleshy_lobe']=bool(lobe);fins.append(name)
 connect(name,body.name,'fin root closed volume physically embedded into body; distal membrane continuous')
 fin_records.append({'name':name,'identity':identity,'root_rail_mm':roots,'lobe_rail_mm':lobe,'distal_margin_mm':tips,'closed_volume':True,'half_thickness_mm':thickness,'fleshy_lobe':bool(lobe),'ray_count_stylized_not_literal':True})
# Separated narrow-based dorsal fins, both posteriorly extended, modest height.
ys=[-15,-13,-11,-9,-7,-5];roots=[(0,y,profile(y)[2]-.8) for y in ys]
tips=[(0,y,z) for y,z in [(-12,42),(-7,47),(-1,47),(5,44),(10,40),(9,37)]]
fin('02-first-dorsal',roots,tips,(1,0,0),'dorsal-1')
ys=[24,25.5,27,28.5,30,31.5];roots=[(0,y,profile(y)[2]-.7) for y in ys]
tips=[(0,y,z) for y,z in [(25,35),(29,41),(35,42),(40,39),(44,35),(42,31)]]
fin('03-second-dorsal',roots,tips,(1,0,0),'dorsal-2')
ys=[24,25.5,27,28.5,30,31.5];roots=[(0,y,profile(y)[1]+.7) for y in ys]
tips=[(0,y,z) for y,z in [(25,9),(29,3),(35,2),(40,5),(44,9),(42,13)]]
fin('04-anal',roots,tips,(1,0,0),'anal')
roots=[(0,51.5,18.8+i*.82) for i in range(9)]
tips=[(0,y,z) for y,z in [(68,5),(73,8),(76,13),(77,18),(80,22),(77,26),(75,31),(72,36),(66,39)]]
fin('05-single-integrated-caudal',roots,tips,(1,0,0),'caudal-integrated-upper-lower-axial')
for label,s in [('L',-1),('R',1)]:
 # Broad base immediately behind gill region, lobes sweep rearward waterborne.
 yz=[(-39,19.5),(-38,18.2),(-37,16.9),(-36,15.6),(-35,14.3),(-34,13)]
 roots=[(s*(flank(y,z)-1),y,z) for y,z in yz]
 lobe=[(s*x,y,z) for x,y,z in [(16,-34,17),(17,-32,15.8),(17.7,-30,14.6),(17.9,-28,13.4),(17.5,-26,12.2),(16.8,-25,11.5)]]
 tips=[(s*x,y,z) for x,y,z in [(21,-33,16),(26,-27,14),(29,-19,11.5),(28,-14,9),(25,-12,7.5),(21,-16,8)]]
 fin(label+'-pectoral-fleshy-fin',roots,tips,(s*.25,-.05,.97),'pectoral-'+label,lobe)
 yz=[(4,13),(5.2,12.6),(6.4,12.2),(7.6,11.8),(8.8,11.4),(10,11)]
 roots=[(s*(flank(y,z)-.6),y,z) for y,z in yz]
 lobe=[(s*x,y,z) for x,y,z in [(10.2,10,9.5),(11,12,8.7),(11.4,14,8),(11.5,16,7.3),(11.2,18,6.8),(10.7,19,6.3)]]
 tips=[(s*x,y,z) for x,y,z in [(13,13,8),(17,18,6),(20,24,4.5),(19.5,29,4),(17,31,4.2),(13.5,27,5)]]
 fin(label+'-pelvic-fleshy-fin',roots,tips,(s*.22,0,.98),'pelvic-'+label,lobe)
# Actual triangle surface contacts/contained vertices, not mere AABB touch.
bpy.context.view_layer.update()
def bvh(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],epsilon=0)
cache={n:bvh(o) for n,o in parts.items()}
def inside(p,tree):
 d=Vector((1,.137,.219)).normalized();pos=p.copy();count=0
 for _ in range(80):
  hit,_,_,_=tree.ray_cast(pos,d,1)
  if hit is None:break
  count+=1;pos=hit+d*1e-9
 return count%2==1
for link in links:
 a,b=link['child'],link['parent'];hits=len(cache[a].overlap(cache[b]));contained=sum(inside(parts[a].matrix_world@v.co,cache[b]) for v in parts[a].data.vertices)
 link.update({'boundary_intersection_pairs':hits,'child_vertices_inside_parent':contained,'status':'PASS' if hits or contained else 'FAIL'})
failed=[x for x in links if x['status']!='PASS'];assert len(fins)==8
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'Source mesh BVH surface intersection and ray-parity contained vertices','count':len(links),'failed':failed,'checks':links,'fin_count':len(fins),'fins':fin_records,'nonadjacent_intersections':'Not exhaustive; physically separate median margins verified through exact views.'},indent=2))
if failed:raise RuntimeError('Disconnected anatomy: '+repr(failed))
offset=ac.ground_asset(coll,center_xy=True)
for o in coll.all_objects:
 if o.type=='MESH':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
root['species']='Eusthenopteron foordi';root['eight_fins']=fins;root['individual_scope']='small-bodied artistic nominal 0.16m';root['reconstruction_notes']=C['reconstruction_notes'];root['representation']='living-reconstruction'
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=ac.export_asset(C['asset_id'],{'en':'Eusthenopteron foordi — small-bodied individual','zh':'真掌鳍鱼 Eusthenopteron foordi（小型个体）'},'fish',coll,metadata={'revision':C['revision'],'representation':'living-reconstruction','description':{'en':'Original small-bodied Eusthenopteron foordi aquatic reconstruction with fleshy paired fins, two dorsal fins, one anal fin and a single integrated tail fin.','zh':'原创小型真掌鳍鱼水生复原：肉质偶鳍、两枚背鳍、一枚臀鳍与一体尾鳍。'},'reconstruction_notes':C['reconstruction_notes'],'origin_note':'Lowest swimming surface at Z0; horizontal bounds centered, no terrestrial support claim.','generator':'scripts/build_eusthenopteron.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.16,'anatomy':{'fins':8,'paired_pectoral':2,'paired_pelvic':2,'dorsal':2,'anal':1,'caudal':1,'fine_connected_scale_cells':cells},'individual_scope':'small-bodied, not adult giant'},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'export_meshes':len(parts),'fin_count':len(fins),'fine_scale_cells':cells,'datum_offset_m':offset,'glb_sha256':record['sha256']['glb'],'default_area_epsilon_m2':1e-10},indent=2))
print('BUILD_COMPLETE',record['sha256']['glb'])
