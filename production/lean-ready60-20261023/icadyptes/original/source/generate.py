# SPDX-License-Identifier: MIT
"""Original deterministic Icadyptes salasi reconstruction, model-task-v2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
No external files are read except this source, adjacent params and declared deps.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
S=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def write(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=S.parent);a=p.parse_args(argv)
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
P=json.loads((S/'params.json').read_text());C=setup_scene(P['asset_id'],P['seed'])
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
M={k:make_material('icadyptes-'+k,v,roughness=0.84 if k!='eye' else 0.3) for k,v in P['palette_srgb'].items()}

# z, lateral radius, AP radius, center Y, angular light-ventrum halfwidth.
# Single continuous loft from inferred lower trunk through preserved-neck region.
rings=[(.145,.073,.072,.025,72),(.21,.118,.122,.025,83),(.31,.155,.172,.025,83),
 (.44,.192,.211,.025,82),(.59,.215,.236,.018,80),(.74,.218,.238,.005,78),
 (.89,.202,.216,-.012,75),(1.02,.174,.184,-.035,72),(1.12,.137,.147,-.061,68),
 (1.205,.099,.113,-.091,61),(1.28,.079,.091,-.125,55),(1.34,.072,.076,-.155,48),
 (1.39,.063,.065,-.177,42),(1.425,.054,.058,-.187,32),(1.46,.052,.051,-.19,0),
 (1.486,.038,.040,-.19,0),(1.499,.019,.023,-.189,0)]
N=28;V=[];F=[];mi=[]
for z,rx,ry,cy,w in rings:
 for j in range(N):
  q=j if j<=N/2 else N-j
  boundary=math.radians(max(w,25))
  t=(q/6*boundary if q<=6 else boundary+(math.pi-boundary)*(q-6)/(N/2-6))
  if j>N/2:t=-t
  V.append((rx*math.sin(t),cy-ry*math.cos(t),z))
for k in range(len(rings)-1):
 for j in range(N):
  F.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
  ang=min((j+.5)*360/N,360-(j+.5)*360/N)
  mi.append(int(k<=12 and (j<6 or j>=N-6)))
V.extend([(0,.025,.13),(0,-.189,1.5)])
for j in range(N):F.append((len(V)-2,(j+1)%N,j));mi.append(0)
for j in range(N):F.append((len(V)-1,(len(rings)-1)*N+j,(len(rings)-1)*N+(j+1)%N));mi.append(0)
body=mesh_object('continuous-trunk-neck-cranium',V,F,[M['back'],M['belly']],C)
for poly,idx in zip(body.data.polygons,mi):poly.material_index=idx
body['interpretation']='Trunk and plumage inferred; robust neck and narrow skull guided by MUSM897.'

# Dorsoventrally flattened spear-like bill, no teeth or invented crest.
# Caudal cranial margin Y=-.14, bill root=-.24, tip=-.48: length .34, bill .24.
def bill(name,lower=False):
 sections=[(-.229,.028,1.446,.014),(-.25,.026,1.446,.012),(-.302,.019,1.444,.009),(-.37,.013,1.441,.0068),(-.438,.0067,1.437,.0043),(-.477,.0017,1.433,.0014)]
 v=[];f=[]
 for y,w,z,h in sections:
  # Four-point roof and four lower points keep a precise straight cutting edge.
  z0=z-(.00015 if lower else 0)
  top=z0 if lower else z0+h
  bottom=z0-h*.66 if lower else z0+.00065
  v.extend([(-w,y,z0+.0008 if not lower else top),(-w*.55,y,top),(w*.55,y,top),(w,y,z0+.0008 if not lower else top),(w*.7,y,bottom),(-w*.7,y,bottom)])
 for k in range(len(sections)-1):
  for j in range(6):f.append((k*6+j,k*6+(j+1)%6,(k+1)*6+(j+1)%6,(k+1)*6+j))
 f.append(tuple(reversed(range(6))));f.append(tuple((len(sections)-1)*6+j for j in range(6)))
 ob=mesh_object(name,v,f,M['bill'],C);ob['bone_scale_note']='Outer keratin sheath artistic; bill length 0.24m, 70.6% of 0.34m skull approximation.'
 return ob
bill('spear-upper-bill');bill('slender-lower-mandible',True)

# Small low-poly eyes on each side of narrow cranium, not prominent cartoon globes.
def ellipsoid(name,c,r,mat,segments=12,rings_n=6):
 v=[(c[0],c[1],c[2]-r[2])];f=[]
 for k in range(1,rings_n):
  phi=-math.pi/2+math.pi*k/rings_n
  for j in range(segments):
   t=2*math.pi*j/segments;v.append((c[0]+r[0]*math.cos(phi)*math.cos(t),c[1]+r[1]*math.cos(phi)*math.sin(t),c[2]+r[2]*math.sin(phi)))
 v.append((c[0],c[1],c[2]+r[2]))
 for j in range(segments):f.append((0,1+(j+1)%segments,1+j))
 for k in range(rings_n-2):
  for j in range(segments):f.append((1+k*segments+j,1+k*segments+(j+1)%segments,1+(k+1)*segments+(j+1)%segments,1+(k+1)*segments+j))
 for j in range(segments):f.append((len(v)-1,1+(rings_n-2)*segments+j,1+(rings_n-2)*segments+(j+1)%segments))
 return mesh_object(name,v,f,mat,C)
for sign,label in [(1,'left'),(-1,'right')]:
 ellipsoid(label+'-eye',(sign*.0484,-.210,1.459),(.006,.0083,.0075),M['eye'])
 # Powerful paddle with genuinely thick root, broad chord, no flying feathers.
 sec=[(.165,-.015,1.095,.047,.026),(.205,.005,1.055,.082,.025),(.25,.018,.93,.082,.020),(.293,.029,.805,.062,.015),(.327,.057,.691,.041,.010),(.341,.082,.625,.016,.005)]
 v=[];f=[];ids=[];n=10
 for x,y,z,chord,thick in sec:
  for j in range(n):
   t=2*math.pi*j/n;v.append((sign*(x+thick*math.sin(t)),y-chord*math.cos(t),z))
 for k in range(len(sec)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));ids.append(0)
 v.extend([(sign*sec[0][0],sec[0][1],sec[0][2]+.018),(sign*.343,.09,.607)])
 for j in range(n):f.append((len(v)-2,(j+1)%n,j));ids.append(0)
 for j in range(n):f.append((len(v)-1,(len(sec)-1)*n+j,(len(sec)-1)*n+(j+1)%n));ids.append(0)
 wing=mesh_object(label+'-powerful-flipper',v,f,M['back'],C)
 wing['humerus_length_model_m']=.18;wing['humerus_midshaft_width_model_m']=.0396
 wing['bone_landmarks_note']='Skeletal humerus ratio0.22 is distinct from inferred outer flipper chord, not claimed measured from soft mesh.'
 # Two separated short shanks; pelvis, hindlimbs and feet are comparative.
 ellipsoid(label+'-short-shank',(sign*.091,-.012,.118),(.044,.055,.095),M['back'],segments=12,rings_n=6)
 # Closed webbed foot, modest three toe lobes. Footprint centered Y=0 overall.
 points=[(-.032,.073),(.035,.068),(.056,-.018),(.067,-.079),(.058,-.129),(.039,-.138),(.021,-.107),(.010,-.151),(-.008,-.157),(-.025,-.113),(-.045,-.143),(-.063,-.134),(-.060,-.080),(-.043,-.008)]
 v=[];f=[]
 for top in [False,True]:
  for x,y in points:v.append((sign*.091+sign*x,y,.0 if not top else .019+max(0,y+.05)*.12))
 n=len(points);v.extend([(sign*.091,-.035,.0),(sign*.091,-.035,.029)])
 for j in range(n):
  f.append((2*n,j,(j+1)%n));f.append((2*n+1,n+(j+1)%n,n+j));f.append((j,n+j,n+(j+1)%n,(j+1)%n))
 mesh_object(label+'-webbed-foot',v,f,M['foot'],C)

# Short stiff tail at low rear, original closed loft rather than feather fingers.
sec=[(.17,.255,.088,.050),(.26,.19,.073,.038),(.34,.135,.045,.022),(.39,.115,.009,.008)]
v=[];f=[];n=10
for y,z,rx,rz in sec:
 for j in range(n):
  t=2*math.pi*j/n;v.append((rx*math.sin(t),y,z+rz*math.cos(t)))
for k in range(len(sec)-1):
 for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
f.append(tuple(reversed(range(n))));f.append(tuple((len(sec)-1)*n+j for j in range(n)))
mesh_object('short-tapered-tail',v,f,M['back'],C)

source=audit_source(C,P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
# Editable semantic parts only. No presentation camera, lighting or floor saved.
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(opts)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Exporter options unavailable: '+repr(missing))
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(out/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][s][i]-v[i]) for s,v in [('min',lo),('max',hi)] for i in range(3))
assert delta<.0001 and source['triangles']==glb['scene_triangles']
write(out/'qa/evidence/technical.json',{'status':'PASS','claim_scope':'Source geometry, static embedded GLB audit and source/export correspondence only','blender_version':bpy.app.version_string,'generator_sha256':sha(Path(__file__)),'params_sha256':sha(S/'params.json'),'glb_sha256':sha(out/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'reconstruction_calibration':{'standing_height_m':1.5,'skull_length_m':.34,'bill_length_m':.24,'bill_fraction_skull':.24/.34,'humerus_length_m':.18,'humerus_midshaft_width_m':.18*.22,'humerus_ratio':.22,'note':'Fig2 ruler approximate skull and humerus; height comparison inference. No internal skeleton exported.'},'gpu':'NOT_RUN','scene':'NOT_RUN'})
print('ICADYPTES_BUILD_OK '+glb['sha256'])
