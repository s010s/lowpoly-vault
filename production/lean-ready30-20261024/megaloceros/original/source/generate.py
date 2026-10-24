# SPDX-License-Identifier: MIT
"""Original Megaloceros giganteus, r001. Run in Blender with -- --output DIR.
The generated animal is an interpretive living reconstruction, not a specimen scan.
All geometry is authored in meters, +Z up and -Y forward, from editable profiles.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb, read_glb, accessor_values

args=argparse.ArgumentParser();args.add_argument('--output',type=Path,default=HERE.parent);args.add_argument('--gray',action='store_true')
A=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=A.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text())
C=setup_scene('megaloceros',seed=P['seed']);ROOT=bpy.data.objects[C['asset_root']]
ROOT['representation']='living-reconstruction';ROOT['revision']='r001'
M={n:make_material(n,'#929292' if A.gray else c,roughness=.84 if n!='eye' else .65) for n,c in P['palette'].items()}
BODY=M['body-warm-taupe'];BACK=M['dorsal-neck'];BELLY=M['ventral-soft-tan'];BONE=M['antler-bone'];DARK=M['hooves-muzzle'];EYE=M['eye'];INNER=M['ear-inner']

def mesh(name,verts,faces,mats,shade=False):
 o=mesh_object(name,verts,faces,mats,C)
 for f in o.data.polygons:f.use_smooth=shade
 return o

def loft(name,rings,sides,materials,material_fn=None):
 """Each ring: center, lateral radius, meridian radius, meridian vector."""
 # Additional rings follow a cubic profile, resolving shoulder, cheek and
 # joint transitions rather than adding uniform subdivisions to flat planes.
 if len(rings)>3:
  expanded=[]
  raw=[list(c)+[rx,rm]+list(mer) for c,rx,rm,mer in rings]
  for j in range(len(raw)-1):
   p0=raw[max(0,j-1)];p1=raw[j];p2=raw[j+1];p3=raw[min(j+2,len(raw)-1)]
   for t in [0,1/3,2/3]:
    v=[.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t) for a,b,c,d in zip(p0,p1,p2,p3)]
    expanded.append((v[:3],v[3],v[4],v[5:]))
  expanded.append(rings[-1]);rings=expanded
 vs=[]
 for center,rx,rm,mer in rings:
  center=Vector(center);mer=Vector(mer).normalized()
  for k in range(sides):
   a=2*math.pi*k/sides
   vs.append(tuple(center+Vector((rx*math.cos(a),0,0))+mer*(rm*math.sin(a))))
 fs=[]
 for j in range(len(rings)-1):
  for k in range(sides):fs.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
 fs.extend([tuple(range(sides-1,-1,-1)),tuple((len(rings)-1)*sides+k for k in range(sides))])
 o=mesh(name,vs,fs,materials)
 if material_fn:
  for poly in o.data.polygons:
   poly.material_index=material_fn(poly.center,poly.normal)
 return o

def sweep(name,points,radii,sides=10,mat=None):
 """Parallel-frame tapered closed branch, including bent anatomical joints."""
 vs=[];p=[Vector(q) for q in points]
 for j,c in enumerate(p):
  t=(p[min(j+1,len(p)-1)]-p[max(0,j-1)]).normalized()
  ref=Vector((0,1,0)) if abs(t.y)<.9 else Vector((0,0,1))
  u=t.cross(ref).normalized();v=t.cross(u).normalized()
  r=radii[j] if isinstance(radii[j],tuple) else (radii[j],radii[j])
  for k in range(sides):
   a=2*math.pi*k/sides;vs.append(tuple(c+u*r[0]*math.cos(a)+v*r[1]*math.sin(a)))
 fs=[tuple(range(sides-1,-1,-1))]
 for j in range(len(p)-1):
  for k in range(sides):fs.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
 fs.append(tuple((len(p)-1)*sides+k for k in range(sides)))
 return mesh(name,vs,fs,mat or BODY)

# One continuous torso/shoulder/neck skin with quiet shaped planes.
body_specs=[
 (1.12,1.44,.12,.22,(0,0,1)),(1.00,1.45,.26,.32,(0,0,1)),
 (.82,1.48,.32,.32,(0,0,1)),(.56,1.46,.30,.30,(0,0,1)),
 (.28,1.43,.325,.35,(0,0,1)),(-.05,1.43,.365,.43,(0,0,1)),
 (-.35,1.46,.38,.46,(0,0,1)),(-.60,1.47,.355,.48,(0,0,1)),
 (-.79,1.49,.315,.46,(0,-.12,1)),(-.92,1.64,.28,.375,(0,.35,1)),
 (-1.03,1.83,.245,.33,(0,.65,1)),(-1.12,2.02,.213,.28,(0,.75,1)),
 (-1.23,2.20,.18,.23,(0,.7,1)),(-1.31,2.28,.142,.17,(0,.55,1))]
rings=[((0,y,z),rx,rm,m) for y,z,rx,rm,m in body_specs]
def body_region(c,n):
 if (c.y>-.90 and n.z>.70) or (c.y<=-.90 and n.y>.68):return 1
 if c.z<1.16 and c.y>-.85:return 2
 return 0
body=loft('continuous-trunk-withers-neck',rings,20,[BODY,BACK,BELLY],body_region)
# Slim elongated skull, brow, cheek and lower jaw, not a broad moose nose.
head_specs=[(-1.12,2.29,.105,.125),(-1.21,2.35,.16,.165),(-1.37,2.34,.165,.165),(-1.49,2.29,.145,.135),(-1.61,2.22,.111,.108),(-1.76,2.165,.087,.077),(-1.87,2.14,.075,.062),(-1.93,2.14,.066,.052)]
head=loft('narrow-cervid-head',[((0,y,z),w,h,(0,0,1)) for y,z,w,h in head_specs],16,[BODY,BELLY],lambda c,n:1 if c.z<2.20 and c.y> -1.78 else 0)
loft('small-dark-muzzle',[((0,-1.875,2.14),.076,.063,(0,0,1)),((0,-1.933,2.141),.07,.054,(0,0,1)),((0,-1.956,2.142),.056,.040,(0,0,1))],12,DARK)
# Four custom anatomical limb profiles; fore-aft offsets reveal far limbs.
feet=[]
for s,label in [(-1,'left'),(1,'right')]:
 fy=-.73 + (.11 if s<0 else -.08)
 front=[((s*.20,-.64,1.68),.115,.16),((s*.28,-.59,1.35),.135,.145),((s*.285,-.55,1.15),.105,.105),((s*.28,fy+.06,.92),.073,.075),((s*.28,fy,.65),.068,.072),((s*.278,fy+.025,.54),.052,.057),((s*.278,fy+.035,.27),.041,.047),((s*.278,fy,.14),.051,.058)]
 loft(label+'-foreleg',[ (c,w,d,(0,1,0)) for c,w,d in front],16,BODY)
 feet.append((s*.278,fy-.035,label+'-fore'))
 hy=.81 + (.11 if s<0 else -.07)
 hind=[((s*.16,.82,1.69),.12,.14),((s*.25,.79,1.45),.17,.20),((s*.28,.75,1.32),.16,.17),((s*.30,.53,1.08),.107,.13),((s*.30,.67,.91),.081,.105),((s*.30,hy+.12,.65),.073,.083),((s*.298,hy+.09,.55),.049,.057),((s*.298,hy+.045,.29),.041,.049),((s*.298,hy,.14),.051,.061)]
 loft(label+'-hindleg',[ (c,w,d,(0,1,0)) for c,w,d in hind],16,BODY)
 feet.append((s*.298,hy-.04,label+'-hind'))
# Each hoof is a pair of tapered toe volumes separated by a visible cleft.
for x,y,label in feet:
 vs=[];fs=[]
 for s in [-1,1]:
  cx=x+s*.038
  for z,w,l,dy in [(0,.031,.102,-.015),(.047,.037,.108,-.018),(.12,.031,.070,.012),(.175,.022,.046,.029)]:
   for a in [( -1,-.65),(-.65,-1),(.65,-1),(1,-.65),(1,.65),(.65,1),(-.65,1),(-1,.65)]:vs.append((cx+w*a[0],y+dy+l*a[1],z))
  off=len(vs)-32;fs.append(tuple(off+k for k in reversed(range(8))))
  for j in range(3):
   for k in range(8):fs.append((off+j*8+k,off+j*8+(k+1)% 8,off+(j+1)*8+(k+1)% 8,off+(j+1)*8+k))
  fs.append(tuple(off+24+k for k in range(8)))
 mesh(label+'-cloven-hoof',vs,fs,DARK)
# Tail: short, downward taper, with a lighter underside.
tail=sweep('small-tail',[(0,1.05,1.58),(0,1.20,1.52),(0,1.32,1.38),(0,1.34,1.30)],[.085,.07,.045,.012],10,[BODY,BELLY])
for poly in tail.data.polygons:poly.material_index=1 if poly.center.z<1.4 else 0
# Ears use a leaf outline and finite curved faces, not ellipsoid primitives.
for s,label in [(-1,'left'),(1,'right')]:
 outline=[(.13,-1.13,2.35),(.23,-1.12,2.45),(.42,-1.08,2.50),(.54,-1.03,2.48),(.46,-1.08,2.36),(.30,-1.17,2.31),(.18,-1.18,2.31)]
 vs=[(s*x,y,z) for x,y,z in outline]+[(s*x,y+.035,z-.012) for x,y,z in outline]
 vs.extend([(s*.315,-1.155,2.402),(s*.315,-1.105,2.396)])
 n=len(outline);fs=[]
 for i in range(n):fs.extend([(14,i,(i+1)%n),(15,n+(i+1)%n,n+i),(i,n+i,n+(i+1)%n,(i+1)%n)])
 o=mesh(label+'-leaf-ear',vs,fs,[BODY,INNER])
 for j,f in enumerate(o.data.polygons):f.material_index=1 if j% 3==0 else 0
 # Eyes: small closed lens integrated into lateral brow.
 center=Vector((s*.153,-1.405,2.365));vs=[]
 for dx,ry,rz in [(0,.044,.032),(.014,.031,.024),(.019,.010,.009)]:
  for k in range(12):
   a=2*math.pi*k/12;vs.append(tuple(center+Vector((s*dx,ry*math.cos(a),rz*math.sin(a)))))
 fs=[tuple(range(11,-1,-1))]
 for j in range(2):
  for k in range(12):fs.append((j*12+k,j*12+(k+1)% 12,(j+1)*12+(k+1)% 12,(j+1)*12+k))
 fs.append(tuple(24+k for k in range(12)))
 mesh(label+'-eye',vs,fs,EYE,shade=True)

# A curved low beam and separated brow tine below each continuous distal palm.
outline=[(.48,2.59),(.56,2.73),(.63,2.86),(.64,3.035),(.70,3.17),(.76,3.24),(.75,3.055),(.79,2.955),(.88,3.01),(.98,3.20),(1.05,3.31),(1.065,3.13),(1.04,3.035),(1.17,3.075),(1.36,3.23),(1.46,3.27),(1.37,3.09),(1.23,2.97),(1.38,2.985),(1.56,3.07),(1.625,3.08),(1.55,2.94),(1.39,2.84),(1.22,2.815),(1.42,2.78),(1.56,2.80),(1.51,2.71),(1.27,2.67),(1.08,2.65),(.88,2.61),(.69,2.55),(.52,2.55)]
# Round broad joins and concave notches while retaining unequal pointed tips.
rounded=[]
for i,p in enumerate(outline):
 prev=outline[(i-1)%len(outline)];nxt=outline[(i+1)%len(outline)]
 tip=i in {5,10,15,20,25}
 f=.04 if tip else .20
 a=tuple(p[k]+f*(prev[k]-p[k]) for k in [0,1]);b=tuple(p[k]+f*(nxt[k]-p[k]) for k in [0,1])
 rounded.extend([a,tuple(.25*a[k]+.5*p[k]+.25*b[k] for k in [0,1]),b])
scale=1.625/max(p[0] for p in rounded)
outline=[(x*scale,z) for x,z in rounded]
for s,label in [(-1,'left'),(1,'right')]:
 sweep(label+'-pedicle-curved-beam',[(s*.115,-1.19,2.445),(s*.16,-1.16,2.53),(s*.27,-1.10,2.60),(s*.42,-1.01,2.62),(s*.57,-.91,2.65),(s*.72,-.79,2.69)],[.065,.070,.067,.067,.077,.10],12,BONE)
 sweep(label+'-separate-brow-tine',[(s*.235,-1.105,2.575),(s*.30,-1.22,2.605),(s*.36,-1.37,2.68),(s*.39,-1.44,2.78),(s*.395,-1.455,2.81)],[.052,.042,.030,.013,.0028],10,BONE)
 # Triangulate planar outline, add one internal centroid per triangle, then
 # map both surfaces into a shallow compound bend with tapered edge thickness.
 planar=[Vector((x,z,0)) for x,z in outline]
 tris=tessellate_polygon([planar]);uv=[(v.x,v.y) for v in planar];index={(round(v.x,7),round(v.y,7)):i for i,v in enumerate(planar)}
 base=[]
 for t in tris:
  ids=[v if isinstance(v,int) else index[(round(v.x,7),round(v.y,7))] for v in t]
  cx=sum(uv[i][0] for i in ids)/3;cz=sum(uv[i][1] for i in ids)/3;k=len(uv);uv.append((cx,cz))
  base.extend([(ids[0],ids[1],k),(ids[1],ids[2],k),(ids[2],ids[0],k)])
 def curved(x,z):return -.94+.30*(x-.5)+.035*math.sin((z-2.6)*4)+.045*(x-.95)**2
 vs=[]
 for front in [-1,1]:
  for i,(x,z) in enumerate(uv):
   asym=0 if s==1 else .018*math.sin(x*7)*(z-2.55)
   tip_distance=min(math.hypot(x-tx,z-tz) for tx,tz in [(.76,3.24),(1.05,3.31),(1.46,3.27),(1.625,3.08),(1.56,2.80)])
   thick=.012+.043*min(1,tip_distance/.13)
   vs.append((s*x,curved(x,z)+front*thick/2,z+asym))
 n=len(uv);fs=[]
 for t in base:fs.extend([t,tuple(n+i for i in reversed(t))])
 for i in range(len(outline)):j=(i+1)%len(outline);fs.append((i,n+i,n+j,j))
 antler=mesh(label+'-curved-palmated-antler',vs,fs,BONE)
 for i,p in enumerate(antler.data.polygons):p.use_smooth=i<2*len(base)

# Refine the skull's length to a cervid muzzle, rather than a long equid-like nose.
for o in C.all_objects:
 if o.type=='MESH' and o.name in ['narrow-cervid-head','small-dark-muzzle','left-eye','right-eye']:
  for v in o.data.vertices:
   if v.co.y < -1.37:v.co.y=-1.37+(v.co.y+1.37)*.66
  o.data.update()
# Center of the four contacts is the root placement origin.
contact_center=[sum(f[i] for f in feet)/len(feet) for i in [0,1]]
for o in C.all_objects:
 if o.type=='MESH':
  for v in o.data.vertices:v.co.x-=contact_center[0];v.co.y-=contact_center[1]
bpy.context.view_layer.update()
source=audit_source(C,max_triangles=P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.context.scene.render.filepath='//render.png'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=ROOT
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Missing required exporter settings')
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**options)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
glb['file']='model.glb'
if glb['errors']:raise RuntimeError(glb['errors'])
b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][k][i]-e[i]) for k,e in [('min',emin),('max',emax)] for i in range(3))
if delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export mismatch')
if (OUT/'model.glb').stat().st_size>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB bytes over ceiling')
# Normalized semantic digest covers actual decoded geometry, indices and PBR.
doc,binary,_=read_glb(OUT/'model.glb')
semantic={'materials':doc.get('materials',[]),'meshes':[],'nodes':doc.get('nodes',[])}
for me in doc.get('meshes',[]):
 ps=[]
 for pr in me['primitives']:
  ps.append({'material':pr.get('material'),'attributes':{k:accessor_values(doc,binary,v) for k,v in sorted(pr['attributes'].items())},'indices':accessor_values(doc,binary,pr['indices'])})
 semantic['meshes'].append({'name':me.get('name'),'primitives':ps})
sh=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
evidence={'schema':'maker-source-export-v1','status':'PASS','gray':A.gray,'glb_sha256':sh(OUT/'model.glb'),'blend_sha256':sh(OUT/'model.blend'),'generator_sha256':sh(Path(__file__)),'params_sha256':sh(HERE/'params.json'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'semantic_sha256':hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'export_options':options,'origin_footprint_translation_m':contact_center,'measurements':{'shoulder_height_m':max(v.co.z for v in body.data.vertices if -.75<v.co.y<-.4),'antler_span_m':glb['bounds_m']['size'][0],'nose_to_tail_length_m':glb['bounds_m']['size'][2],'palm_main_thickness_m':.055,'palm_tip_thickness_min_m':.012,'palm_closed_volumetric':True},'warnings_review':{'smooth_eye_faces':'Small closed eye lenses and the broad front/back antler palm surfaces use smooth normals. Antler rims, body and other parts are faceted.','anatomical_overlaps':'Shoulder and hip roots, head-neck and antler beam-palm use small intentional anatomical overlaps; independent image review remains required.'},'boundaries':'Maker technical check only. Independent visual/factual QA, GPU and scene gates not established.'}
(OUT/'build-report.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'status':'BUILT','glb_sha256':evidence['glb_sha256'],'triangles':glb['scene_triangles'],'primitives':glb['scene_primitives_estimated_base_draw_calls'],'bytes':glb['bytes']}))
