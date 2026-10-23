# SPDX-License-Identifier: MIT
"""Original Palaeophonus living reconstruction, based on the frozen reference brief.
Blender 4.3.2: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Millimeter design coordinates are converted to meters when meshes are created.
The generator uses only its packaged helpers, params and Blender runtime.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);out=ap.parse_args(a).out;out.mkdir(parents=True,exist_ok=True)
col=setup_scene(P['asset_id'],P['seed']);root=bpy.data.objects[col['asset_root']]
root['taxon']='Palaeophonus nuncius';root['representation']='living-reconstruction'
root['scale_basis']='62 mm published specimen length; part dimensions, depth, pose and color inferred.'
root['scope']='NRM PAL Ar0032235 proportions, completed using the FIRST Palaeophonus reconstruction in Dunlop and Garwood 2024 Figure 9.'
root['anatomy_limits']='No reconstructed respiratory organs; ventral anatomy simplified; ecology unresolved.'
root['origin']='Identity root at center of the walking contact footprint, floor z=0, head -Y.'
colors={'carapace':'#79583B','plates':'#936C46','chelae':'#88603F','ridges':'#AF895A','joint':'#584735','eyes':'#24241F'}
mats={k:make_material('Palaeophonus-'+k,v,roughness=.83 if k!='eyes' else .5) for k,v in colors.items()}
sem=[]
def mesh(name,v,f,mat,kind):
 o=mesh_object(name,[tuple(x*.001 for x in p) for p in v],f,mats[mat],col)
 o['semantic_part']=kind;o['anatomical_status']='Regularized living interpretation, not direct preservation of every part'
 sem.append({'name':name,'category':kind,'vertices':len(v),'polygons':len(f),'material':mat})
 return o

def tube(name,points,radii,mat,kind,sides=10,flatten=1):
 v=[];f=[]
 for i,p in enumerate(points):
  tangent=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])).normalized()
  ref=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((0,1,0))
  u=tangent.cross(ref).normalized(); w=tangent.cross(u).normalized()
  for j in range(sides):
   q=Vector(p)+radii[i]*(u*math.cos(j*math.tau/sides)+w*math.sin(j*math.tau/sides)*flatten);v.append(tuple(q))
  if i:
   for j in range(sides):f.append(((i-1)*sides+j,(i-1)*sides+(j+1)%sides,i*sides+(j+1)%sides,i*sides+j))
 f.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))])
 return mesh(name,v,f,mat,kind)

def oval(name,c,r,mat,kind,n=14,rings=8):
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

def loft_y(name,sections,mat,kind,n=16,power=1):
 # Each section is y, center_x, center_z, half_width, half_height.
 v=[];f=[]
 for i,(y,x,z,w,h) in enumerate(sections):
  for j in range(n):
   a=math.tau*j/n; ca=math.cos(a);sa=math.sin(a)
   v.append((x+w*math.copysign(abs(ca)**power,ca),y,z+h*math.copysign(abs(sa)**power,sa)))
  if i:
   for j in range(n):f.append(((i-1)*n+j,(i-1)*n+(j+1)%n,i*n+(j+1)%n,i*n+j))
 f.extend([tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))])
 return mesh(name,v,f,mat,kind)

# Broad subrectangular prosoma, with rounded lateral shoulders and a restrained median furrow.
loft_y('Carapace-subrectangular',[(-5.5,0,3.45,3.45,1.1),(-5.15,0,3.5,4.1,1.65),(-3.7,0,3.6,4.5,1.9),(.9,0,3.5,4.4,1.85),(3.15,0,3.4,4.15,1.45),(3.5,0,3.35,3.8,1.15)],'carapace','carapace',20,.66)
# Fine, short raised axial panels give the dorsal shield structure without invented armor.
for s,label in ((-1,'L'),(1,'R')):
 loft_y('Carapace-low-lobe-'+label,[(-4.5,s*1.6,4.95,1.15,.32),(-3,s*1.85,5.25,1.5,.30),(.7,s*1.9,5.14,1.45,.25),(2.3,s*1.7,4.85,1.15,.14)],'plates','carapace-dorsal-lobe',12,.75)
 oval('Median-eye-'+label,(s*.44,-3.35,5.51),(.24,.31,.18),'eyes','median-eye-region-inferred',12,6)
 # Conservative small chelicerae, not an extra antennal pair.
 loft_y('Chelicera-base-'+label,[(-5.0,s*.95,3.7,.62,.65),(-6.2,s*.95,3.8,.80,.7),(-7.35,s*.83,3.8,.60,.5)],'plates','chelicera',12,.85)
 tube('Chelicera-fixed-finger-'+label,[(s*1.25,-7,3.9),(s*1.34,-8,3.9),(s*.96,-8.6,3.86)],[.26,.19,.035],'ridges','cheliceral-finger',8)
 tube('Chelicera-movable-finger-'+label,[(s*.53,-7,3.9),(s*.48,-7.85,3.95),(s*.76,-8.4,3.92)],[.24,.17,.035],'chelae','cheliceral-finger',8)

# Seven broad mesosoma tergites: gradual posterior narrowing, with dark flexible joins.
lengths=[2.5,2.8,3.3,3.8,4.2,4.5,4.9];assert abs(sum(lengths)-26)<1e-8
widths=[4.28,4.65,4.95,5.1,5.0,4.55,3.65]
loft_y('Mesosoma-simplified-continuous-venter',[(3.1,0,2.65,3.9,.9),(6.8,0,2.7,4.25,1),(12,0,2.8,4.7,1.05),(19,0,2.75,4.7,1.05),(25,0,2.7,3.9,.95),(29.5,0,2.75,2.0,.8)],'joint','simplified-venter',16,.78)
y=3.5
for i,(L,w) in enumerate(zip(lengths,widths),1):
 z=3.35-.045*i; h=1.6-.025*i; endw=w if i<7 else 2.15
 secs=[(y+.12,0,z,w*.88,h*.72),(y+.46,0,z,w,h),(y+L-.5,0,z,endw,h*.92),(y+L-.12,0,z,endw*.90,h*.72)]
 ob=loft_y('Mesosoma-tergite-%02d'%i,secs,'plates','mesosoma-tergite',20,.69);ob['segment_index']=i
 # A narrow flush rear bevel, no detached decorative stripes.
 pts=[]
 for j in range(11):
  a=math.pi*j/10;pts.append((endw*.92*math.cos(a),y+L-.25,z+h*.80*math.sin(a)))
 tube('Tergite-%02d-posterior-lip'%i,pts,[.10]*11,'ridges','tergite-lip',6)
 y+=L

# Four short robust digitigrade pairs. Podomeres are compact and roughly subequal;
# tips taper directly to points, without long modern-scorpion articulated feet.
leg_routes=[[(3.4,-3.1,2.6),(5.4,-3.2,3.1),(7.35,-3.4,3.0),(8.9,-3.6,1.9),(10.3,-3.8,.11)],
 [(3.8,-.75,2.6),(6.4,-.7,3.2),(9.1,-.45,3.1),(11.8,-.25,1.95),(14.0,-.2,.11)],
 [(3.8,1.5,2.55),(6.1,2.4,3.2),(8.9,3.75,3.15),(11.65,5.1,2.0),(14.0,6.9,.11)],
 [(3.7,3.4,2.5),(5.5,5.0,3.25),(7.9,7.55,3.15),(10.4,10.1,2.05),(12.6,13.0,.11)]]
for s,label in ((-1,'L'),(1,'R')):
 for i,route in enumerate(leg_routes,1):
  pts=[Vector((s*x,y,z)) for x,y,z in route]
  for j in range(4):
   start,end=pts[j],pts[j+1];v=end-start;A=start+v*.035;B=end-v*.035
   thick=[.79,.73,.59,.43][j]*(.88+.055*i)
   if j==3:
    tube(f'Leg-{i}-{label}-pointed-terminal',[tuple(A),tuple(A+v*.40),tuple(B)],[thick,.28,.055],'chelae','pointed-walking-terminal',9)
   else:
    tube(f'Leg-{i}-{label}-podomere-{j+1}',[tuple(A),tuple(A+v*.18),tuple(B-v*.15),tuple(B)],[thick*.78,thick,thick*.88,thick*.68],'chelae','walking-podomere',10)
   if j:
    oval(f'Leg-{i}-{label}-joint-{j}',tuple(start),(thick*.74,thick*.74,thick*.74),'joint','walking-joint',10,6)

# Very stout pedipalp palms and compact transverse arms, distinct from long-clawed Pulmonoscorpius.
for s,label in ((-1,'L'),(1,'R')):
 arm=[(s*3.15,-4.45,3.7),(s*6.0,-6.75,4.05),(s*10.5,-7.0,4.15),(s*13.65,-9.1,4.35)]
 for j in range(3):
  A=Vector(arm[j]);B=Vector(arm[j+1]);v=B-A;thick=[1.28,1.48,1.35][j]
  tube(f'Pedipalp-{label}-arm-{j+1}',[tuple(A),tuple(A+v*.18),tuple(A+v*.78),tuple(B)],[thick*.7,thick,thick*.93,thick*.68],'chelae','pedipalp-arm',12,.90)
  if j:oval(f'Pedipalp-{label}-joint-{j}',tuple(A),(.96,.96,.85),'joint','pedipalp-joint',12,6)
 loft_y('Expanded-chela-palm-'+label,[(-9.1,s*13.65,4.35,1.0,.9),(-10.2,s*14.8,4.5,2.0,1.55),(-12.0,s*15.2,4.55,2.6,1.85),(-13.7,s*15.1,4.5,2.25,1.65),(-14.65,s*15.05,4.45,1.5,1.05)],'chelae','expanded-chela-palm',16,.85)
 tube('Chela-fixed-curved-finger-'+label,[(s*17.0,-13.1,4.5),(s*17.35,-15.0,4.5),(s*17.15,-17.15,4.45),(s*16.55,-19.0,4.35),(s*15.9,-20.4,4.3)],[.98,.84,.56,.30,.055],'chelae','chela-fixed-finger',12,.85)
 tube('Chela-opposing-finger-'+label,[(s*13.45,-13.25,4.45),(s*13.5,-15.0,4.45),(s*14.1,-17.0,4.43),(s*14.8,-18.6,4.35),(s*15.3,-19.55,4.3)],[.92,.72,.48,.25,.055],'ridges','chela-movable-finger',12,.82)
 # A restrained palm crest follows the swollen chela, not a copied fossil crack.
 tube('Chela-palm-crest-'+label,[(s*15.6,-10.3,5.65),(s*15.8,-11.9,6.36),(s*15.65,-13.5,5.95)],[.09,.10,.065],'ridges','palm-crest',6)

# Five segmented robust metasomal rings, with a modest lateral and dorsal bend.
# The five centerline lengths total 21 mm, plus 6 mm telson/sting = 27 mm.
current=Vector((0,29.5,2.9)); tail_lengths=[4.0,4.0,4.2,4.3,4.5];tail_nodes=[tuple(current)]
for i,(L,dx,dz) in enumerate(zip(tail_lengths,[.1,.35,.65,.85,.75],[.05,.18,.4,.7,.85]),1):
 d=Vector((dx,math.sqrt(L*L-dx*dx-dz*dz),dz));end=current+d
 r=1.9-i*.075;axis=d.normalized()
 tube('Metasoma-segment-%02d'%i,[tuple(current+axis*.10),tuple(current+axis*.42),tuple(end-axis*.42),tuple(end-axis*.10)],[r*.80,r,r*.91,r*.72],'carapace','metasoma-segment',14,.86)
 # Closed joint core fills an anatomical articulation, not a single unsegmented tube.
 if i>1:oval('Metasoma-articulation-%02d'%i,tuple(current),(r*.70,r*.72,r*.62),'joint','metasoma-articulation',12,6)
 # Paired low longitudinal carinae follow the exact segment, with no unsupported spines.
 side=Vector((1,0,0));up=Vector((0,0,1))
 for sign,letter in ((-1,'L'),(1,'R')):
  off=side*(sign*r*.52)+up*(r*.68)
  tube(f'Metasoma-{i}-low-carina-{letter}',[tuple(current+axis*.52+off),tuple(end-axis*.52+off)],[.075,.075],'ridges','metasoma-low-carina',6)
 current=end;tail_nodes.append(tuple(end))
# Small telson bulb with curved aculeus; no tightly elevated threat loop.
d=Vector((.12,.97,.20)).normalized();bulb_end=current+d*2.3
pts=[tuple(current),tuple(current+d*.65),tuple(current+d*1.5),tuple(bulb_end)]
tube('Telson-bulb',pts,[.85,1.12,1.03,.57],'plates','telson',14,.92)
# Aculeus is 3.7 mm in centerline, curving gently down toward its tip.
q=bulb_end;sting=[tuple(q)]
for direction,L in [((.10,1,.06),1.2),((.06,1,-.25),1.2),((.02,.85,-.53),1.3)]:q=q+Vector(direction).normalized()*L;sting.append(tuple(q))
tube('Curved-pointed-aculeus',sting,[.48,.33,.17,.060],'ridges','sting',10)

# Place the root at the footprint center, not the whole body bounding-box center.
foot_y=(-3.8+13.0)/2
lowest=min(v.co.z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
for obj in col.objects:
 if obj.type=='MESH':
  for v in obj.data.vertices:v.co.y-=foot_y*.001;v.co.z-=lowest
bpy.context.view_layer.update();src=audit_source(col,40000)
assert not src['errors'],src['errors']
# Save editable semantic source first, with no cameras, lights, text blocks, images or external assets.
bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
 for area in screen.areas:
  for sp in area.spaces:
   if sp.type=='FILE_BROWSER' and sp.params:sp.params.directory=b'//'+b' '*1020;sp.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),check_existing=False)
# Export a material-batched copy only. The blend retains all semantic parts separately.
exp=bpy.data.collections.new('EXPORT_BATCHED');bpy.context.scene.collection.children.link(exp)
exp_root=bpy.data.objects.new('palaeophonus-export-root',None);exp.objects.link(exp_root)
for key,mat in mats.items():
 v=[];f=[]
 for obj in col.objects:
  if obj.type!='MESH' or obj.data.materials[0]!=mat:continue
  off=len(v);v.extend(tuple(obj.matrix_world@q.co) for q in obj.data.vertices);f.extend(tuple(off+i for i in poly.vertices) for poly in obj.data.polygons)
 m=bpy.data.meshes.new('Palaeophonus-'+key+'-batched');m.from_pydata(v,[],f);m.update();m.materials.append(mat)
 ob=bpy.data.objects.new('Palaeophonus-'+key,m);exp.objects.link(ob);ob.parent=exp_root
bpy.ops.object.select_all(action='DESELECT')
for o in exp.objects:o.select_set(True)
bpy.context.view_layer.objects.active=exp_root
opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
assert not set(opts)-{x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
g=audit_glb(out/'model.glb',40000,6,8);g['file']='model.glb';assert not g['errors'],g['errors'];assert g['bytes']<=8388608
b=src['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(g['bounds_m'][k][i]-t[i]) for k,t in [('min',emin),('max',emax)] for i in range(3));assert delta<1e-7;assert g['scene_triangles']==src['triangles']
report={'status':'PASS','source':src,'glb':g,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'export_options':opts,'palette_srgb':colors,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'seed':P['seed'],'semantic_parts':sem,'anatomy_counts':{'walking_leg_pairs':4,'pedipalp_pairs':1,'chelicera_pairs':1,'mesosoma_tergites':7,'metasoma_segments':5,'telson':1,'sting':1},'design_centerline_mm':{'carapace':9,'mesosoma':sum(lengths),'metasoma':sum(tail_lengths),'telson_and_sting':6,'total':62},'ground_shift_m':-lowest,'footprint_center_y_shift_m':-foot_y*.001,'scope':'Source integrity and static standalone GLB audit only, not independent visual, browser GPU, populated scene or user acceptance.'}
(out/'build-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print('BUILD COMPLETE',g['sha256'],g['scene_triangles'])
