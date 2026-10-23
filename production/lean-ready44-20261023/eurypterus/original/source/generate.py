# SPDX-License-Identifier: MIT
"""Original Eurypterus remipes living reconstruction, deterministic Blender 4.3.2.
Use: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Design millimeters become meters at mesh creation. No reference pixels are embedded.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);out=a.out;out.mkdir(parents=True,exist_ok=True)
col=setup_scene(P['asset_id'],P['seed']);root=bpy.data.objects[col['asset_root']]
root['taxon']='Eurypterus remipes';root['representation']='living-reconstruction'
root['scale_basis']='MGM1758X author estimate about 200 mm if straight; component proportions are estimates.'
root['reference_limits']='Ventral MGM1758X main anchor; same-species MGM5868X dorsal shape only, not its 150 mm scale. Plate 1D excluded.'
root['origin']='Identity root under carapace-trunk junction at the lowermost mounting plane; swimming/crawling-neutral pose, no habitat claim.'
root['uncertainty']='Thickness, pose, missing limb tips and living color are inferred; simplified venter, no exposed bookgill fins.'
colors={'shield':'#6F6850','plates':'#918260','limbs':'#89775B','rim':'#B39D71','flex':'#4D4C40','eyes':'#252D2B'}
mats={k:make_material('Eurypterus-'+k,v,roughness=.83 if k!='eyes' else .44) for k,v in colors.items()}
sem=[]
def mesh(name,v,f,mat,kind):
 ob=mesh_object(name,[tuple(x*.001 for x in q) for q in v],f,mats[mat],col);ob['semantic_part']=kind
 sem.append({'name':name,'category':kind,'vertices':len(v),'polygons':len(f),'material':mat});return ob

def tube(name,points,radii,mat,kind,sides=10,flatten=1):
 v=[];f=[]
 for i,p in enumerate(points):
  t=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])).normalized()
  ref=Vector((0,0,1)) if abs(t.z)<.92 else Vector((0,1,0));u=t.cross(ref).normalized();w=t.cross(u).normalized()
  for j in range(sides):
   q=Vector(p)+radii[i]*(u*math.cos(j*math.tau/sides)+w*math.sin(j*math.tau/sides)*flatten);v.append(tuple(q))
  if i:
   for j in range(sides):f.append(((i-1)*sides+j,(i-1)*sides+(j+1)%sides,i*sides+(j+1)%sides,i*sides+j))
 f.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))]);return mesh(name,v,f,mat,kind)

def loft(name,sections,mat,kind,n=20,power=.82):
 v=[];f=[]
 for i,(y,x,z,w,h) in enumerate(sections):
  for j in range(n):
   ang=math.tau*j/n;c=math.cos(ang);s=math.sin(ang)
   v.append((x+w*math.copysign(abs(c)**power,c),y,z+h*math.copysign(abs(s)**power,s)))
  if i:
   for j in range(n):f.append(((i-1)*n+j,(i-1)*n+(j+1)%n,i*n+(j+1)%n,i*n+j))
 f.extend([tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))]);return mesh(name,v,f,mat,kind)

def oval(name,c,r,mat,kind,n=12,rings=6):
 v=[(c[0],c[1],c[2]-r[2])];f=[]
 for k in range(1,rings):
  a=math.pi*k/rings
  for j in range(n):
   b=math.tau*j/n;v.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]-r[2]*math.cos(a)))
 v.append((c[0],c[1],c[2]+r[2]));last=len(v)-1
 for j in range(n):f.append((0,1+(j+1)%n,1+j))
 for k in range(rings-2):
  for j in range(n):
   i=1+k*n+j;q=1+k*n+(j+1)%n;f.append((i,q,q+n,i+n))
 for j in range(n):f.append((last,last-n+j,last-n+(j+1)%n))
 return mesh(name,v,f,mat,kind)

# Deliberately lofted, rounded-front subtrapezoidal prosoma. Local lateral narrowing
# outside the eye regions represents the remipes embayment without borrowing Plate 1D.
head=[(-33,0,8.0,2.5,.8),(-32.5,0,8.3,7.5,1.7),(-31.5,0,8.6,12,2.5),(-29.5,0,8.8,16.6,3.2),(-26,0,9.0,20.5,4.0),(-22.5,0,9.0,20.3,4.2),(-18,0,9.0,18.6,4.4),(-13,0,8.9,20.1,4.5),(-7,0,8.6,21.5,4.2),(-1,0,8.2,21.2,3.5),(0,0,8.1,20.2,2.7)]
loft('Carapace-remipes-embayed-margin',head,'shield','carapace',28,.82)
# Continuous shallow marginal rim, not fossil cracks or oversized ornament.
for s,lab in [(-1,'L'),(1,'R')]:
 tube('Carapace-margin-'+lab,[(s*w*.995,y,z+.45) for y,x,z,w,h in head],[.32]*len(head),'rim','carapace-margin',6,.75)
 # Kidney-shaped raised lateral compound-eye region with a concave inner side.
 outline=[(-1.3,-3.7),(.8,-4.2),(2.0,-3.4),(2.45,-1.9),(2.5,.2),(1.9,2.8),(.5,4.1),(-1.2,3.5),(-1.85,2.2),(-1.5,.4),(-.8,-.8),(-1.5,-2.1)]
 cx=s*12.7;cy=-23.6;z=12.4;v=[];N=len(outline)
 for scale,dz in [(1,-.35),(1,.1),(.70,.65)]:
  v.extend((cx+s*x*scale,cy+y*scale,z+dz) for x,y in outline)
 f=[tuple(range(N-1,-1,-1))]
 for k in range(2):
  for j in range(N):f.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
 f.append(tuple(2*N+j for j in range(N)))
 mesh('Lateral-kidney-eye-'+lab,v,f,'eyes','lateral-eye')
 oval('Median-ocellus-'+lab,(s*.75,-20.8,13.55),(.38,.5,.26),'eyes','median-ocellus',10,6)
 # Small chelicerae, tucked under the rounded front. Never giant pterygotid claws.
 loft('Chelicera-small-base-'+lab,[(-30.7,s*2.9,6.3,1.15,.85),(-33.2,s*2.9,6.25,1.5,1.1),(-35.2,s*2.7,6.2,1.0,.7)],'limbs','chelicera',12,.85)
 tube('Chelicera-fixed-finger-'+lab,[(s*3.45,-34.7,6.2),(s*3.55,-36.5,6.2),(s*2.9,-37.2,6.2)],[.45,.31,.09],'rim','chelicera-fixed-finger',8)
 tube('Chelicera-moving-finger-'+lab,[(s*1.95,-34.7,6.2),(s*1.8,-36.0,6.2),(s*2.4,-36.8,6.2)],[.40,.27,.09],'limbs','chelicera-moving-finger',8)

# Twelve serial trunk tergites, six broad anterior and six progressively narrower
# posterior. Flexible venter occupies joints without masquerading as extra segments.
preL=[6,7,8.5,9.5,10,11];postL=[10,10.5,11,11,11,11.5];assert sum(preL)==52 and sum(postL)==65
width=[21.0,22.4,23.7,24.0,22.4,19.4,16.7,14.5,12.6,10.7,8.6,6.2]
loft('Trunk-flexible-venter',[(0,0,7.7,19.4,2.4),(14,0,7.6,21.4,2.6),(31,0,7.4,22.0,2.6),(52,0,7.0,16.3,2.3),(75,0,6.6,12.2,1.9),(98,0,6.0,7.6,1.5),(117,0,5.7,3.2,1.1)],'flex','trunk-venter',20,.82)
y=0
for i,(L,w) in enumerate(zip(preL+postL,width),1):
 z=8.1-.14*i;h=5.25-.21*i;wstart=width[i-2] if i>1 else 20.2;wend=w if i<12 else 4.6
 secs=[(y+.15,0,z,wstart*.96,h*.73),(y+min(1.4,L*.20),0,z,wstart+(wend-wstart)*.18,h),(y+L-.9,0,z,wstart+(wend-wstart)*.89,h*.90),(y+L-.15,0,z,wend*.98,h*.65)]
 ob=loft('Trunk-tergite-%02d'%i,secs,'plates' if i<=6 else 'shield','trunk-tergite',24,.74);ob['segment_index']=i;ob['trunk_region']='preabdomen' if i<=6 else 'postabdomen'
 # Posterior low arch picks up light but stays attached to each plate.
 pts=[]
 for j in range(13):
  ang=math.pi*j/12;pts.append((wend*.96*math.cos(ang),y+L-.55,z+h*.77*math.sin(ang)))
 tube('Tergite-%02d-rear-bevel'%i,pts,[.23 if i<7 else .18]*13,'rim','tergite-bevel',6,.80)
 y+=L
assert y==117
# Straight slender telson, flattened to a shallow keel, not a scorpion sting.
loft('Straight-slender-telson',[(117,0,6.3,3.45,1.65),(120,0,6.3,3.2,1.7),(128,0,6.2,2.45,1.45),(143,0,5.95,1.55,1.0),(156,0,5.7,.78,.58),(166.9,0,5.5,.10,.13),(167,0,5.5,.08,.11)],'limbs','telson',12,.85)
# Subtle distal marginal teeth support the published remipes serration observation.
for s,lab in [(-1,'L'),(1,'R')]:
 for i,(yy,ww) in enumerate([(144,1.5),(147,1.30),(150,1.12),(153,.93),(156,.78),(159,.59)]):
  tube('Telson-marginal-serration-'+lab+'-'+str(i+1),[(s*(ww-.10),yy,5.93-.02*(yy-144)),(s*(ww+.38),yy+.33,5.93-.02*(yy-144))],[.19,.085],'rim','telson-serration',6,.65)

# All five appendage pairs attach to the prosoma. Four walking pairs II-V form a
# forward/lateral fan. Pair V is longer, more slender, with no extra comb spines.
routes=[[(8.5,-25.0,5.5),(18,-29,6),(25.5,-34,5.8),(31.5,-39,3.8),(34.0,-44,1.5)],
 [(11.5,-19,5.4),(22.0,-22,6.5),(32.0,-25,6.0),(40.5,-27,3.9),(44,-30,1.5)],
 [(15,-11.7,5.3),(26,-11.5,6.4),(36.5,-10.4,5.8),(46,-11.1,3.7),(51,-15.5,1.5)],
 [(16.8,-4.8,5.1),(28,-.2,6.1),(41,2,5.6),(53,1.2,3.7),(62,-.7,1.5)]]
for s,lab in [(-1,'L'),(1,'R')]:
 for i,route in enumerate(routes,2):
  points=[Vector((s*x,y,z)) for x,y,z in route]
  for j in range(4):
   A=points[j];B=points[j+1];d=B-A;thick=[1.65,1.6,1.25,.85][j]*(1 if i<5 else .78)
   rr=[thick*.73,thick,thick*.82,thick*.52] if j<3 else [thick*.82,thick*.90,thick*.42,.13]
   tube(f'Walking-{i}-{lab}-podomere-{j+1}',[tuple(A+d*.02),tuple(A+d*.19),tuple(A+d*.79),tuple(B-d*.02)],rr,'limbs','walking-podomere' if j<3 else 'walking-terminal',10,.70)
   if j:oval(f'Walking-{i}-{lab}-joint-{j}',tuple(A),(thick*.66,thick*.66,thick*.50),'flex','walking-joint',10,6)
   if i<5 and j in [1,2]:
    # Restrained paired ventrolateral spines, no exaggerated pincers.
    v=d.normalized();side=Vector((-v.y,v.x,0)).normalized()
    for sign in [-1,1]:
     base=A+d*.68+side*sign*thick*.65;tip=base+side*sign*(1.8 if j==1 else 1.4)+v*.50+Vector((0,0,-.6))
     tube(f'Walking-{i}-{lab}-{j}-spine-{sign}',[tuple(base),tuple(tip)],[.35,.095],'rim','walking-spine',7,.85)
 # Sixth appendage is swimming pair: articulated proximal stalk and broad oval blade.
 paddlestalk=[Vector((s*x,y,z)) for x,y,z in [(15,-.5,5.5),(23,5.0,5.3),(31,9.5,5.3),(37,14.0,5.5),(40.5,20,5.6)]]
 for j in range(4):
  A=paddlestalk[j];B=paddlestalk[j+1];d=B-A;r=[2.3,2.0,2.1,2.5][j]
  tube(f'Swimming-VI-{lab}-stalk-{j+1}',[tuple(A),tuple(A+d*.20),tuple(A+d*.83),tuple(B)],[r*.72,r,r,r*.72],'limbs','paddle-stalk',12,.42)
  if j:oval(f'Swimming-VI-{lab}-joint-{j}',tuple(A),(r*.68,r*.68,r*.31),'flex','paddle-joint',10,6)
 # Broad paddle podomere VIII has a rounded unequal outline and narrow stalk neck.
 paddle=[(19,s*40.0,5.7,2.0,.64),(21,s*42.5,5.7,4.1,.90),(25,s*45.5,5.7,7.3,1.1),(30,s*47.8,5.7,8.2,1.08),(35,s*48.4,5.7,7.2,.96),(39,s*47.7,5.7,4.8,.7),(41,s*46.3,5.7,2.0,.40),(41.7,s*45.6,5.7,.35,.18)]
 ob=loft('Swimming-VI-'+lab+'-oval-paddle',paddle,'plates','swimming-paddle',20,.90);ob['appendage_pair']=6
 # One low rim following the leading edge, not a detached blade.
 tube('Swimming-paddle-leading-rim-'+lab,[(s*(abs(x)+w*.92),yy,z+.1) for yy,x,z,w,h in paddle],[.22]*len(paddle),'rim','paddle-rim',6,.65)

# Conservative visible venter: metastoma and opercular plate, plus a modest median
# Type A appendage. The female interpretation is not presented as proven sex.
loft('Ventral-metastoma',[(-23,0,4.7,1.1,.45),(-20,0,4.5,2.1,.68),(-15,0,4.4,2.4,.78),(-10,0,4.5,1.8,.65)],'rim','metastoma',12,.85)
loft('Ventral-operculum',[(1,0,4.4,14.2,.8),(3,0,4.15,16.8,1.15),(7,0,4.15,16.2,1.0),(9.5,0,4.4,13.6,.6)],'limbs','operculum',18,.80)
loft('Type-A-median-appendage',[(2.8,0,2.9,.7,.35),(6,0,2.8,.80,.40),(11,0,2.8,.66,.30),(15.2,0,2.9,.18,.18)],'rim','type-A-appendage',10,.85)
# A lowermost mounting plane, without implying that the whole body rests on ground.
lowest=min(v.co.z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
for ob in col.objects:
 if ob.type=='MESH':
  for v in ob.data.vertices:v.co.z-=lowest
bpy.context.view_layer.update();src=audit_source(col,40000);assert not src['errors'],src['errors']
bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
 for area in screen.areas:
  for sp in area.spaces:
   if sp.type=='FILE_BROWSER' and sp.params:sp.params.directory=b'//'+b' '*1020;sp.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),check_existing=False)
# Batch only a temporary export copy by material; editable semantic parts remain in blend.
exp=bpy.data.collections.new('EXPORT_BATCHED');bpy.context.scene.collection.children.link(exp);er=bpy.data.objects.new('eurypterus-export-root',None);exp.objects.link(er)
for key,mat in mats.items():
 v=[];f=[]
 for ob in col.objects:
  if ob.type!='MESH' or ob.data.materials[0]!=mat:continue
  off=len(v);v.extend(tuple(ob.matrix_world@q.co) for q in ob.data.vertices);f.extend(tuple(off+i for i in poly.vertices) for poly in ob.data.polygons)
 me=bpy.data.meshes.new('Eurypterus-'+key+'-batched');me.from_pydata(v,[],f);me.update();me.materials.append(mat);ob=bpy.data.objects.new('Eurypterus-'+key,me);exp.objects.link(ob);ob.parent=er
bpy.ops.object.select_all(action='DESELECT')
for ob in exp.objects:ob.select_set(True)
bpy.context.view_layer.objects.active=er
opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
assert not set(opts)-{x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties};bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
g=audit_glb(out/'model.glb',40000,6,8);g['file']='model.glb';assert not g['errors'],g['errors'];assert not g['warnings'],g['warnings'];assert g['bytes']<=8388608
b=src['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(g['bounds_m'][k][i]-t[i]) for k,t in [('min',emin),('max',emax)] for i in range(3));assert delta<1e-7;assert g['scene_triangles']==src['triangles']
report={'status':'PASS','source':src,'glb':g,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'export_options':opts,'palette_srgb':colors,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'seed':P['seed'],'semantic_parts':sem,'anatomy_counts':{'walking_pairs_II_V':4,'paddle_pair_VI':1,'small_chelicera_pair_I':1,'trunk_tergites':12,'preabdominal_segments':6,'postabdominal_segments':6,'straight_telson':1,'lateral_eyes':2,'median_ocelli':2},'design_body_centerline_mm':{'carapace':33,'preabdomen':sum(preL),'postabdomen':sum(postL),'telson':50,'total':200},'lowest_mounting_plane_shift_m':-lowest,'scope':'Source and uncompressed static GLB technical integrity only. Not independent visual/factual acceptance, GPU, populated scene, user or deployment evidence.'}
(out/'build-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n');print('BUILD COMPLETE',g['sha256'],g['scene_triangles'])
