# SPDX-License-Identifier: MIT
"""Original deterministic Megalograptus ohioensis composite living reconstruction.
Blender 4.3.2: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
No fossil image, external mesh or texture is incorporated. All dimensions are meters.
The 0.75 m axial body estimate is not the preserved extent of UC 24119A.
Appendage III distal coxa and hypertrophied spine endpoints/angles are inferred.
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
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);out=a.out;out.mkdir(parents=True,exist_ok=True)
col=setup_scene('megalograptus',P['seed']);root=bpy.data.objects[col['asset_root']]
root['taxon']='Megalograptus ohioensis';root['representation']='Composite living reconstruction'
root['scale_note']='Brief maps the published about-0.75 m complete-animal estimate to an illustrative axial head-to-telson span. UC 24119A is partial.'
root['uncertainty']='Depth, color, posture, distal coxa III and long-spine endpoints/angles are inferred.'
root['mount']='Identity mounting origin on sagittal plane near anterior/posterior trunk transition. Z=0 is a baseline below this swimming reconstruction, not claimed ground contact.'
colors={'dorsal':'#59685B','edge':'#9D9675','limb':'#7B8167','ventral':'#707C68','joint':'#4B594A','eye':'#202E29'}
mats={k:make_material('Megalograptus-'+k,v,roughness=.86 if k!='eye' else .42) for k,v in colors.items()}
parts=[]
def mesh(name,verts,faces,mat='dorsal',category=None):
 o=mesh_object(name,verts,faces,mats[mat],col);o['semantic_part']=category or name
 parts.append({'name':name,'category':category or name,'material':mat,'vertices':len(verts),'polygons':len(faces)})
 return o

def tube(name,points,radii,mat='limb',sides=10,category=None,flatten=1):
 vv=[];ff=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]);tangent.normalize()
  ref=Vector((0,0,1)) if abs(tangent.z)<.95 else Vector((0,1,0));u=tangent.cross(ref).normalized();v=tangent.cross(u).normalized()
  for j in range(sides):
   angle=j*math.tau/sides;vv.append(tuple(Vector(p)+radii[i]*(math.cos(angle)*u+math.sin(angle)*v*flatten)))
  if i:
   for j in range(sides):ff.append(((i-1)*sides+j,(i-1)*sides+(j+1)%sides,i*sides+(j+1)%sides,i*sides+j))
 ff += [tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))]
 return mesh(name,vv,ff,mat,category)

def ellipsoid(name,c,r,mat='joint',n=12,rings=6,category=None):
 vv=[(c[0],c[1],c[2]-r[2])];ff=[]
 for k in range(1,rings):
  a=math.pi*k/rings
  for j in range(n):
   b=math.tau*j/n;vv.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]-r[2]*math.cos(a)))
 vv.append((c[0],c[1],c[2]+r[2]));last=len(vv)-1
 for j in range(n):ff.append((0,1+(j+1)%n,1+j))
 for k in range(rings-2):
  for j in range(n):
   p=1+k*n+j;q=1+k*n+(j+1)%n;ff.append((p,q,q+n,p+n))
 for j in range(n):ff.append((last,last-n+j,last-n+(j+1)%n))
 return mesh(name,vv,ff,mat,category)

def loft(name,stations,mat='dorsal',category=None,n=24):
 # y, half-width, center-z, half-height. Faceted oval cross-sections.
 vv=[];ff=[]
 for y,w,z,h in stations:
  for j in range(n):
   t=j*math.tau/n;zz=z+h*math.sin(t)
   if zz<z-h*.62:zz=z-h*.62
   vv.append((w*math.cos(t),y,zz))
 for k in range(len(stations)-1):
  for j in range(n):ff.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 ff += [tuple(range(n-1,-1,-1)),tuple((len(stations)-1)*n+j for j in range(n))]
 return mesh(name,vv,ff,mat,category)

def blade(name,outline,z,thickness,mat,category):
 # Closed tapered lenticular plate, a small interior ring preserves its intentional outline.
 n=len(outline);cx=sum(x for x,y in outline)/n;cy=sum(y for x,y in outline)/n
 vv=[(x,y,z) for x,y in outline]
 vv.extend((cx+(x-cx)*.79,cy+(y-cy)*.79,z+thickness) for x,y in outline)
 vv.extend((cx+(x-cx)*.79,cy+(y-cy)*.79,z-thickness*.45) for x,y in outline)
 ff=[]
 for j in range(n):
  k=(j+1)%n;ff.extend([(j,k,n+k,n+j),(j,2*n+j,2*n+k,k)])
 ff.extend([tuple(n+j for j in range(n)),tuple(3*n-1-j for j in range(n))])
 return mesh(name,vv,ff,mat,category)

def mirror(points,s):return [(s*x,y,z) for x,y,z in points]
def spike(name,base,tip,r=.0028,mat='edge',category='raptorial-spine'):
 b=Vector(base);t=Vector(tip);m=b.lerp(t,.48);m.z+=.001
 return tube(name,[b,m,t],[r,r*.54,.00025],mat,8,category)

# Compact headshield, clearly separate from the broad segmented mesosoma.
outline=[(0,-.375),(.027,-.374),(.050,-.362),(.065,-.343),(.070,-.321),(.067,-.293),(.057,-.275),(0,-.277),(-.057,-.275),(-.067,-.293),(-.070,-.321),(-.065,-.343),(-.050,-.362),(-.027,-.374)]
n=len(outline);vv=[(0,-.326,.068)];ff=[]
for scale,z in ((.28,.067),(.59,.062),(.84,.052),(1,.037)):
 vv.extend((x*scale,-.326+(y+.326)*scale,z) for x,y in outline)
for j in range(n):ff.append((0,1+j,1+(j+1)%n))
for k in range(3):
 p=1+k*n;q=p+n
 for j in range(n):ff.append((p+j,q+j,q+(j+1)%n,p+(j+1)%n))
vbottom=len(vv);vv.append((0,-.327,.023))
for j in range(n):ff.append((1+3*n+j,vbottom,1+3*n+(j+1)%n))
mesh('Compact-rounded-headshield',vv,ff,'dorsal','carapace')
# Fine perimeter lip, no ornamental armor or false horns.
tube('Headshield-perimeter-lip',[(x*.992,y,.038) for x,y in outline]+[(outline[0][0]*.992,outline[0][1],.038)],[.00125]*(n+1),'edge',8,'carapace-rim')
for s,label in ((-1,'L'),(1,'R')):
 ellipsoid('Compound-eye-'+label,(s*.042,-.347,.058),(.0077,.0125,.0044),'eye',14,7,'compound-eye')
 ellipsoid('Median-ocellus-'+label,(s*.0025,-.337,.068),(.0017,.0022,.0011),'eye',10,5,'ocellus')
# Conservative ventral cover plate and gnathobasic bases, not external giant chelicerae.
ellipsoid('Ventral-metastoma',(0,-.306,.020),(.017,.034,.004),'ventral',16,7,'metastoma')
for s,label in ((-1,'L'),(1,'R')):
 for i in range(5):
  ellipsoid(f'Gnathobasic-base-{i+2}-{label}',(s*(.022+i*.003),-.350+i*.017,.024),(.012,.010,.006),'ventral',10,6,'gnathobasic-base')
 # I small chelicerae with tiny opposed terminal digits.
 tube('I-chelicera-'+label,mirror([(.011,-.361,.026),(.013,-.383,.028),(.011,-.394,.029)],s),[.0043,.0034,.0019],'limb',9,'appendage-I')
 for q in (-1,1):
  spike(f'I-terminal-digit-{label}-{q}',(s*(.011+q*.0015),-.390,.029),(s*(.011+q*.003),-.401,.030),.0012,'edge','cheliceral-digit')
 # II shorter spinose limbs frame a narrow central opening.
 pp=[(.030,-.354,.032),(.044,-.382,.040),(.056,-.416,.046),(.052,-.450,.051),(.040,-.471,.055)]
 tube('II-short-spinose-pedipalp-'+label,mirror(pp,s),[.009,.008,.006,.004,.0012],'limb',12,'appendage-II')
 for i in range(7):
  f=i/6;x=.051+.004*math.sin(f*math.pi);y=-.388-.069*f;z=.043+.010*f
  spike(f'II-inward-spine-{label}-{i+1}',(s*x,y,z),(s*(x-.014+.005*f),y-.010,z+.004),.0018*(1-.4*f),'edge','pedipalp-spine')
 # III enlarged raptorial system, with a conservative restored basal coxa.
 basal=[(.048,-.338,.031),(.088,-.357,.042),(.133,-.384,.054),(.172,-.419,.065)]
 tube('III-restored-coxa-and-proximal-podomeres-'+label,mirror(basal,s),[.016,.021,.019,.014],'limb',14,'appendage-III-base')
 # Slight swellings identify articulation rather than a single uniform tentacle.
 for j,p in enumerate(basal[1:]):ellipsoid(f'III-proximal-joint-{label}-{j+1}',(s*p[0],p[1],p[2]),(.014,.012,.010),'joint',12,6,'appendage-III-joint')
 distal=[(.170,-.415,.065),(.196,-.449,.075),(.213,-.488,.083),(.218,-.527,.089),(.209,-.563,.094),(.190,-.590,.098),(.167,-.602,.099)]
 tube('III-curved-distal-basket-arm-'+label,mirror(distal,s),[.0137,.012,.010,.008,.0058,.0035,.0008],'limb',14,'appendage-III-distal')
 # Two hypertrophied podomere-4 spines per side. Their length and angles are inferred.
 for j,(bx,by,bz,tx,ty,tz) in enumerate(((.165,-.411,.064,.088,-.516,.070),(.170,-.416,.071,.106,-.529,.083))):
  ob=spike(f'III-inferred-long-podomere4-spine-{label}-{j+1}',(s*bx,by,bz),(s*tx,ty,tz),.0047 if j==0 else .0037,'edge','hypertrophied-III-spine')
  ob['scientific_limit']='Complete length, endpoint and angle unknown. Conservative illustrative restoration, not a fossil measurement.'
 # Opposing paired basket teeth shorten toward the distal tip; negative space remains open.
 for i in range(10):
  f=i/9;y=-.444-.138*f;x=.195+.022*math.sin(f*math.pi)-.003*f;z=.075+.022*f
  length=.040*(1-.54*f)
  for j,dz in enumerate((-.003,.003)):
   spike(f'III-basket-spine-{label}-{i+1:02}-{j+1}',(s*x,y,z+dz),(s*(x-length),y-.014+f*.006,z+dz+.003),.0026*(1-.45*f),'edge','paired-basket-spine')
 # IV and V only: two modest walking leg pairs, separate from the swimming VI.
 for pair,y,dy in ((4,-.310,-.012),(5,-.283,-.015)):
  pp=[(.051,y,.027),(.097,y+.004,.027),(.142,y+dy,.023),(.177,y+dy+.005,.015),(.198,y+dy+.018,.010)]
  tube(f'{pair}-walking-leg-'+label,mirror(pp,s),[.007,.0065,.0046,.0028,.0006],'limb',10,'appendage-'+('IV' if pair==4 else 'V'))
  if pair==4:
   for i in range(7):
    f=i/6;x=.092+.078*f;yy=y+dy*f
    spike(f'IV-small-leg-spine-{label}-{i+1}',(s*x,yy,.026-f*.008),(s*(x+.003),yy-.012+f*.003,.025-f*.008),.0014,'edge','walking-spine')
 # VI has an articulated stalk and broad distal swimming paddle.
 pp=[(.054,-.277,.025),(.103,-.268,.023),(.149,-.251,.024),(.181,-.232,.025)]
 tube('VI-swimming-stalk-'+label,mirror(pp,s),[.010,.011,.010,.008],'limb',12,'appendage-VI-stalk',flatten=.70)
 ellipsoid('VI-paddle-joint-'+label,(s*.179,-.232,.025),(.012,.010,.006),'joint',12,6,'paddle-joint')
 poly=[(.171,-.239),(.187,-.250),(.208,-.242),(.229,-.223),(.247,-.194),(.250,-.178),(.227,-.189),(.207,-.207),(.187,-.217),(.176,-.224)]
 blade('VI-broad-swimming-paddle-'+label,[(s*x,y) for x,y in poly],.025,.0045,'dorsal','appendage-VI-paddle')
 tube('VI-paddle-articulated-midline-'+label,mirror([(.182,-.235,.029),(.206,-.221,.030),(.228,-.200,.029)],s),[.0012,.0013,.0007],'edge',7,'paddle-ridge')

# Seven broad anterior opisthosomal segments; continuous low axis hides artificial gaps.
loft('Continuous-ventral-mesosoma',[(-.280,.055,.034,.013),(-.23,.077,.034,.016),(-.16,.074,.033,.016),(-.09,.057,.031,.014),(-.028,.034,.029,.012)],'ventral','ventral-axis')
L=.24/7
widths=[.065,.079,.082,.079,.071,.059,.043]
for i,w in enumerate(widths):
 y=-.275+i*L;z=.040-i*.0014;h=.025-i*.0014
 stations=[(y-.002,w*.90,z,h*.88),(y+.007,w,z,h),(y+L*.78,w*.98,z-.001,h*.94),(y+L+.001,w*.89,z-.002,h*.80)]
 loft(f'Opisthosomal-segment-{i+1:02}-mesosoma',stations,'dorsal','mesosoma-segment')
 # A narrow trailing shelf, integrated overlapping plate lip, not a separate armored ring.
 yy=y+L*.84;pts=[]
 for j in range(17):
  angle=math.pi*j/16;pts.append((w*.96*math.cos(angle),yy,z-.001+h*.92*math.sin(angle)))
 tube(f'Mesosoma-{i+1:02}-trailing-lip',pts,[.0011]*len(pts),'edge',6,'segment-margin')
# Four narrow posterior segments and a fifth, broadened pretelson: total 12.
start=-.035;length=.0625
for i in range(4):
 y=start+i*length;w=[.034,.030,.027,.025][i];z=.028-i*.001;h=.017-i*.0006
 loft(f'Opisthosomal-segment-{i+8:02}-metasoma',[(y-.002,w*.96,z,h*.93),(y+.012,w,z,h),(y+length*.84,w*.92,z-.001,h*.92),(y+length+.002,w*.89,z-.001,h*.84)],'limb','metasoma-segment')
 pts=[(w*.92*math.cos(math.pi*j/14),y+length*.91,z-.001+h*.91*math.sin(math.pi*j/14)) for j in range(15)]
 tube(f'Metasoma-{i+8:02}-trailing-lip',pts,[.0009]*len(pts),'edge',6,'segment-margin')
loft('Opisthosomal-segment-12-broad-pretelson',[(.213,.023,.024,.015),(.235,.035,.024,.017),(.260,.040,.022,.015),(.276,.031,.020,.011)],'dorsal','pretelson')
# Three separate terminal forms: central telson and paired curved sickle-like cercal blades.
tube('Central-straight-telson',[(0,.268,.022),(0,.295,.022),(0,.335,.021),(0,.375,.020)],[.006,.0047,.0027,.00035],'edge',10,'telson',flatten=.8)
for s,label in ((-1,'L'),(1,'R')):
 poly=[(.016,.273),(.034,.285),(.044,.307),(.046,.329),(.038,.350),(.024,.366),(.009,.375),(.017,.352),(.018,.336),(.013,.323),(.007,.309),(.008,.289)]
 blade('Curved-sickle-cercal-blade-'+label,[(s*x,y) for x,y in poly],.020,.005,'limb','cercal-blade')
 # Shallow dorsal keel, stops before the pointed free tip.
 tube('Cercal-blade-keel-'+label,mirror([(.020,.282,.025),(.032,.309,.027),(.032,.333,.026),(.024,.353,.023)],s),[.0010,.0015,.0012,.0005],'edge',7,'cercal-keel')

# Keep identity root and preserve conservative swimming-body thickness.
bpy.context.view_layer.update();source=audit_source(col,40000)
if source['errors']:raise RuntimeError(json.dumps(source['errors']))
bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:
    space.params.directory=b'//' + b' '*1020;space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),check_existing=False)
# Batched export copy reduces draw primitives without destroying source semantics.
exp=bpy.data.collections.new('EXPORT_BATCHED');bpy.context.scene.collection.children.link(exp)
rr=bpy.data.objects.new('megalograptus-export-root',None);exp.objects.link(rr)
for k,mat in mats.items():
 vv=[];ff=[]
 for o in col.objects:
  if o.type!='MESH' or o.data.materials[0]!=mat:continue
  off=len(vv);vv.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices);ff.extend(tuple(off+i for i in p.vertices) for p in o.data.polygons)
 if not vv:continue
 m=bpy.data.meshes.new('Megalograptus-'+k+'-batched');m.from_pydata(vv,[],ff);m.update();m.materials.append(mat)
 o=bpy.data.objects.new('Megalograptus-'+k,m);exp.objects.link(o);o.parent=rr
bpy.ops.object.select_all(action='DESELECT')
for o in exp.objects:o.select_set(True)
bpy.context.view_layer.objects.active=rr
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=False,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
assert not set(options)-{x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
glb=audit_glb(out/'model.glb',40000,6,8);glb['file']='model.glb'
assert not glb['errors'],glb['errors'];assert glb['bytes']<=8388608
b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-target[i]) for side,target in [('min',emin),('max',emax)] for i in range(3));assert delta<1e-7;assert glb['scene_triangles']==source['triangles']
report={'status':'PASS','scope':'Maker source geometry, standalone GLB and source/export bounds only; no independent acceptance or GPU claim.','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'export_options':options,'palette_srgb':colors,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'seed':P['seed'],'semantic_parts':parts,'anatomy_counts':{'headshield':1,'appendage_pairs_I_to_VI':6,'walking_pairs_IV_V':2,'swimming_paddle_pair_VI':1,'hypertrophied_appendage_pair_III':1,'hypertrophied_spines_per_III_limb':2,'mesosoma_segments':7,'metasoma_segments_including_pretelson':5,'central_telson':1,'cercal_blades':2},'axial_body_estimate_m':.75,'limits':'Published complete-animal estimate is about 0.75 m, not preserved UC24119A length. Per the frozen brief this is mapped to illustrative axial head-to-telson span; limb-inclusive bounds are longer, not an independent fossil measurement. Depth, segmentation proportions, spine endpoint geometry and living color are interpretive.'}
(out/'build-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('BUILD COMPLETE',glb['sha256'],glb['scene_triangles'])
