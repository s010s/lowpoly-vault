# SPDX-License-Identifier: MIT
"""Original parametric Birkenia elegans, reference-led rather than traced geometry.
Coordinates authored numerically in millimeters then converted to meters.
blender -b -t 2 --factory-startup --python build_birkenia.py -- --config config.json --output-dir PATH [--gray]
"""
import bpy,bmesh,json,math,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent));import asset_common as ac
P=argparse.ArgumentParser();P.add_argument('--config',type=Path,required=True);P.add_argument('--output-dir',type=Path,required=True);P.add_argument('--gray',action='store_true')
A=P.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
coll=ac.setup_scene('birkenia',C['seed']);root=bpy.data.objects[coll['asset_root']];S=C['model_space_mm_to_m'];parts={};connections=[]
mats={k:ac.make_material('birkenia-'+k,'#929292' if A.gray else v,double_sided=False) for k,v in C['palette'].items()}
def add(name,v,f,mat):
 o=ac.mesh_object(name,[[a*S for a in p] for p in v],f,[mats[k] for k in mat] if isinstance(mat,list) else mats[mat],coll);parts[name]=o
 g=o.vertex_groups.new(name=name);g.add(list(range(len(v))),1,'REPLACE');return o

def link(a,b,why):connections.append({'child':a.name,'parent':b.name,'anatomical_relation':why})
def solid(name,poly,thickness,mat):
 n=len(poly);v=[(-thickness/2,y,z) for y,z in poly]+[(thickness/2,y,z) for y,z in poly]
 f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,n+(j+1)%n,n+j) for j in range(n)]
 return add(name,v,f,mat)
# Whole trunk and caudal axial extension, with smooth profile changes in editable ring topology.
# Maximum torso depth21mm, width9mm. Distal body bends DOWN into the long lower caudal lobe.
sections=[(-40,.30,11.8,12.7),(-39,1.0,9.8,14.3),(-37,2.1,7.4,16.8),(-34,3.0,4.9,19.0),(-30,3.75,3.0,21.0),(-25,4.3,2.0,22.2),(-19,4.5,1.5,22.5),(-12,4.4,1.8,22.2),(-5,4.05,2.9,21.0),(2,3.6,4.3,19.4),(9,2.9,6.2,17.8),(16,2.0,8.0,15.9),(22,1.05,9.6,14.3),(26,.65,8.8,12.4),(30,.43,6.9,9.9),(34,.27,4.9,7.4),(38,.17,3.0,4.8),(40,.11,2.1,2.9)]
def profile(y):
 for i in range(len(sections)-1):
  a,b=sections[i:i+2]
  if a[0]<=y<=b[0]:
   t=(y-a[0])/(b[0]-a[0]);return [a[j]*(1-t)+b[j]*t for j in range(1,4)]
 return list(sections[0 if y<sections[0][0] else -1][1:])
# Each armor row is an integrated shallow raised fold, not detached scale beads.
# Four samples per oblique row retain broad deliberate facets. Dorsal and ventral rows reverse near ridge.
rings=[-40,-39.4,-38.6,-37.5,-36.3,-35.1,-33.8,-32.4,-31,-29.5,-28]
for i in range(28):
 for f in [0,.18,.30,.88]:rings.append(-26.5+i*1.75+f*1.75)
rings+= [23,24.5,26,28,30,32,34,36,38,40];rings=sorted(set(rings))
n=C['body_ring_sides'];v=[]
for k,y0 in enumerate(rings):
 for j in range(n):
  a=j*2*math.pi/n;ca=math.cos(a);sa=math.sin(a)
  envelope=max(0,min(1,(y0+33)/7,(26-y0)/6))
  # Opposed upper/lower oblique rows meet around the mid-flank, a restrained herringbone organization.
  shift=(2.2*abs(ca)-.5)*envelope if abs(sa)>.25 else 1.2*envelope
  y=y0+shift;w,lo,hi=profile(y);phase=((y0+26.5)/1.75)%1
  relief=(.12 if .15<phase<.3 else .055 if .3<=phase<.8 else 0)*envelope
  if A.gray:relief=0
  v.append(((w+relief)*sa,y,(hi+lo)/2+((hi-lo)/2+relief)*ca))
f=[tuple(reversed(range(n)))]
for k in range(len(rings)-1):
 for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
f.append(tuple((len(rings)-1)*n+j for j in range(n)))
body=add('01-integrated-oblique-armor-body-and-lower-axial-tail',v,f,['dorsal','flank','ventral','web'])
for i,p in enumerate(body.data.polygons):
 if i==0 or i==len(body.data.polygons)-1:p.material_index=1;continue
 k,j=divmod(i-1,n);ca=math.cos((j+.5)*2*math.pi/n);y=rings[k];phase=((y+26.5)/1.75)%1
 p.material_index=0 if ca>.78 else 2 if ca<-.78 else 1
 # Quiet pale raised scale edge; not every facet alternates into a checkerboard.
 if not A.gray and -27<y<21 and .13<phase<.27 and -.8<ca<.8:p.material_index=3
# Caudal fin asymmetric outline. Axial tapered body runs along the long lower lobe.
tail=solid('02-hypocercal-caudal-fin',[(21,14.0),(24,15.1),(27.3,19.5),(30.8,22.2),(32.8,22.5),(33.1,21.2),(31.8,17.0),(29.9,13.1),(31.7,10.9),(35.5,7.6),(40,3.0),(39.9,2.1),(37.5,1.8),(32.4,3.9),(28.0,6.4),(24.4,9.3),(21,10.1)],.65,'web');link(tail,body,'finite caudal web surrounding the downward axial continuation, longer lower lobe')
anal=solid('03-short-unpaired-anal-fin',[(7.6,6.3),(10.5,5.2),(14.4,4.0),(17.9,4.8),(19,6.7),(18.1,8.9),(13.2,9.7),(8.2,8.0)],.6,'web');link(anal,body,'short median anal fin rooted into lower posterior trunk, not paired pelvic fans')
# Double-headed low dorsal element: two opposed projections; not a webbed ray-bearing fin.
ridge_specs=[(-12,3.0,5.2),(-5.7,2.25,4.5),(0.0,1.8,4.0),(5.0,1.45,3.7),(9.5,1.15,3.1),(13.4,.85,2.8)]
for idx,(y,h,length) in enumerate(ridge_specs):
 top=profile(y)[2]
 if idx==0:poly=[(y-length/2,top-.45),(y-length/2+.6,top+h*.6),(y-length/2-.5,top+h),(y-.5,top+h*.88),(y+.25,top+h*.35),(y+length/2+1.1,top+h*.75),(y+length/2+.5,top+h*.2),(y+1.0,top-.5)]
 else:poly=[(y-length/2,top-.45),(y-length/2+.4,top+h*.72),(y+.3,top+h),(y+length/2+.5,top+h*.6),(y+.8,top+.2),(y+length/2,top-.65)]
 o=solid('04-dorsal-ridge-'+('double-headed' if idx==0 else str(idx+1)),poly,.65,'ridge');link(o,body,'low isolated enlarged dorsal ridge scale, deeply embedded root; stylized count')
# Parametric elliptical surface locating attached organs without axis-aligned bbox claims.
def side_x(y,z):
 w,lo,hi=profile(y);t=max(-.98,min(.98,(z-(hi+lo)/2)/((hi-lo)/2)))
 a=math.acos(t);q=a/(2*math.pi/n);j=int(q);f=q-j
 return w*(math.sin(j*2*math.pi/n)*(1-f)+math.sin((j+1)*2*math.pi/n)*f)
def oval(v,f,c,rx,ry,rz,n=12):
 # Closed bipyramid lens: poles finite and broad enough for default tiny-triangle threshold.
 base=len(v);x,y,z=c;v.extend([(x-rx,y,z),(x+rx,y,z)])
 for j in range(n):a=j*2*math.pi/n;v.append((x,y+ry*math.cos(a),z+rz*math.sin(a)))
 for j in range(n):f.extend([(base,base+2+(j+1)%n,base+2+j),(base+1,base+2+j,base+2+(j+1)%n)])
for s,label in [(-1,'L'),(1,'R')]:
 y=-35.6;z=14.2;x=s*(side_x(y,z)-.08);ev=[];ef=[];oval(ev,ef,(x,y,z),.45,1.65,1.6,16)
 o=add('05-'+label+'-embedded-lateral-eye',ev,ef,'eye');link(o,body,'shallow lens broadly embedded in compact head, no stalk')
 gv=[];gf=[]
 for k in range(8):
  y=-31.3+k*.92;z=10.0-k*.62;x=s*(side_x(y,z)-.035)
  oval(gv,gf,(x,y,z),.22,.28,.38,10)
 o=add('06-'+label+'-eight-oblique-branchial-marks',gv,gf,'eye');link(o,body,'eight small closed superficial branchial marks, not drilled holes or an operculum')
 # Close-to-body small postbranchial plate, no long paired fin membrane.
 y=-23.0;z=4.9;x=s*(side_x(y,z)-.12);pv=[];pf=[];oval(pv,pf,(x,y,z),.32,1.4,.65,10)
 o=add('07-'+label+'-small-postbranchial-plate',pv,pf,'ridge');link(o,body,'small ventrolateral plate region remains close to trunk; distal soft fin extent not asserted')
# Small closed mouth mark, inset at blunt front; no teeth or hinged lower jaw.
v=[(-.48,-39.1,11.7),(.48,-39.1,11.7),(.48,-39.75,11.7),(-.48,-39.75,11.7),(-.48,-39.1,12.0),(.48,-39.1,12.0),(.48,-39.75,12.0),(-.48,-39.75,12.0)]
f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
mouth=add('08-small-closed-jawless-mouth',v,f,'eye');link(mouth,body,'closed tiny mouth notation embedded across rounded snout; no jaw articulation')
# Actual intersecting triangles or interior child vertex; never infer connection from overlapping AABBs.
bpy.context.view_layer.update();trees={name:BVHTree.FromPolygons([o.matrix_world@p.co for p in o.data.vertices],[list(p.vertices) for p in o.data.polygons],all_triangles=False,epsilon=0) for name,o in parts.items()}
def inside(point,tree):
 direction=Vector((1,.137,.219)).normalized();p=point.copy();hits=0
 for _ in range(60):
  hit,normal,face,d=tree.ray_cast(p,direction,1)
  if hit is None:break
  hits+=1;p=hit+direction*1e-9
 return hits%2==1
for q in connections:
 a,b=q['child'],q['parent'];count=len(trees[a].overlap(trees[b]));contained=any(inside(parts[a].matrix_world@v.co,trees[b]) for v in parts[a].data.vertices)
 q.update(boundary_intersection_pairs=count,child_vertex_inside_parent=contained,status='PASS' if count or contained else 'FAIL')
failed=[q for q in connections if q['status']!='PASS'];assert not failed,failed
# Ground means documented unsupported-swim display datum only, not a habitat assertion.
offset=ac.ground_asset(coll,center_xy=True)
for o in coll.all_objects:
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
root['representation']='living-reconstruction';root['scientific_limits']=C['reconstruction_notes'];root['lower_lobe_axial_extension']=True;root['branchial_marks_per_side']=8
root['source']='Blom Maerss Miller2002 Fig5D,11,14';bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
report={'status':'PASS','method':'zero-epsilon BVH actual triangle intersections or ray-parity containment','checks':connections,'failed':failed,'branchial_marks_per_side':8,'paired_large_fin_fans':0,'double_headed_dorsal_scale':True,'stylized_ridge_elements':6,'finite_fin_thickness_mm':.65,'anal_thickness_mm':.6,'body_sections_mm':sections,'lower_axial_tip_yz_mm':[40,2.5],'upper_fin_tip_yz_mm':[32.8,22.5],'nominal_length_mm':80,'datum_shift_m':offset,'reconstruction_limits':C['reconstruction_notes'],'nonadjacent_self_intersections':'Not exhaustive; anatomical embedding recorded, no global boolean fusion claim.'}
(OUT/'anatomical-connections.json').write_text(json.dumps(report,indent=2))
record=ac.export_asset('birkenia',{'en':'Birkenia elegans','zh':'比尔肯鱼 Birkenia elegans'},'fish',coll,metadata={'revision':'r001','representation':'living-reconstruction','description':{'en':'Original80mm jawless anaspid with integrated oblique armor, double-headed ridge scale and longer LOWER caudal lobe.','zh':'原创80毫米无颌鱼：连体斜列甲鳞、双头背脊鳞与延长的下尾叶。'},'reconstruction_notes':C['reconstruction_notes'],'origin_note':'Unsupported neutral swim, lowest surfaceZ0 and XYbounds center display datum.','generator':'scripts/build_birkenia.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'total_length_m':.08},output_root=OUT,render=False,diagnostics=False,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'anatomical_objects':len(parts),'anatomical_links':len(connections),'glb_sha256':record['sha256']['glb']},indent=2))
print('BUILD_COMPLETE',record['sha256']['glb'])
