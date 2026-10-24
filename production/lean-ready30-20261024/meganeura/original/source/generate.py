# SPDX-License-Identifier: MIT
"""Deterministic original Meganeura monyi reconstruction. No image or external mesh input.
Run in Blender: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output .
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source, ground_asset
from qa_glb import audit_glb
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE.parent);p.add_argument('--params',type=Path,default=BASE/'params.json');p.add_argument('--gray',action='store_true');a=p.parse_args(argv)
P=json.loads(a.params.read_text());OUT=a.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('meganeura',P['seed']);M={k:make_material('meganeura-'+k,'#99978F' if a.gray else v,roughness=.78 if k!='eyes' else .58) for k,v in P['palette'].items()}
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mat=0):
  n=len(self.v);self.v.extend(v);self.f.extend(tuple(n+i for i in q) for q in f);self.mi.extend([mat]*len(f))
 def object(self,name,mats):
  o=mesh_object(name,self.v,self.f,mats,C)
  for f,i in zip(o.data.polygons,self.mi):f.material_index=i
  return o
 def tube(self,points,radii,sides=6,mat=0):
  # Closed original profiled polyline, not a Blender primitive.
  pts=[Vector(q) for q in points];v=[]
  for i,(q,r) in enumerate(zip(pts,radii)):
   d=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();aux=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0));u=d.cross(aux).normalized();w=d.cross(u).normalized()
   v += [tuple(q+r*(math.cos(j*2*math.pi/sides)*u+math.sin(j*2*math.pi/sides)*w)) for j in range(sides)]
  f=[tuple(range(sides-1,-1,-1))]
  for i in range(len(pts)-1):
   for j in range(sides):k=i*sides+j;l=i*sides+(j+1)%sides;f.append((k,l,l+sides,k+sides))
  f.append(tuple((len(pts)-1)*sides+j for j in range(sides)));self.add(v,f,mat)
 def loft(self,rings,sides=12,mat=0):
  # Each ring is y, center_z, half_width, half_height.
  v=[(math.sin(j*2*math.pi/sides)*rx,y,z+math.cos(j*2*math.pi/sides)*rz) for y,z,rx,rz in rings for j in range(sides)]
  f=[tuple(range(sides-1,-1,-1))]
  for i in range(len(rings)-1):
   for j in range(sides):f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
  f.append(tuple((len(rings)-1)*sides+j for j in range(sides)));self.add(v,f,mat)

def ellipsoid(name,center,scale,mat):
 x,y,z=center;rx,ry,rz=scale;g=Mesh();rings=[]
 for t in [-.96,-.78,-.4,0,.4,.78,.96]:rings.append((y+t*ry,z,rx*math.sqrt(1-t*t),rz*math.sqrt(1-t*t)))
 g.loft(rings,12);g.v=[(vx+x,vy,vz) for vx,vy,vz in g.v];return g.object(name,mat)
# Thoracic flight block: three compact organic sections, not a pinched wasp waist.
g=Mesh();g.loft([(-.042,.052,.007,.009),(-.033,.056,.019,.016),(-.015,.059,.024,.021),(.006,.058,.024,.022),(.025,.055,.019,.018),(.040,.052,.014,.013)],12)
o=g.object('thorax-flight-musculature',[M['cuticle'],M['dorsal']]);
for f in o.data.polygons:
 if f.center.z>.065:f.material_index=1
# Long continuous 10-segment abdomen with modest intersegment constrictions.
g=Mesh();rings=[]
for i in range(10):
 y=.034+i*.0275;rx=.0145*(1-.075*i);rz=.011*(1-.065*i);z=.052-.0019*i
 rings.extend([(y,z,rx*.90,rz*.92),(y+.005,z+.0004,rx,rz),(y+.023,z-.001,rx*.91,rz*.94)])
rings += [(.315,.032,.0031,.0033),(.322,.031,.0019,.0022)]
g.loft(rings,10);o=g.object('abdomen-ten-segments',[M['cuticle'],M['dorsal'],M['seams']])
for f in o.data.polygons:
 cy=f.center.y
 if int(max(0,cy-.034)/.0275)%2==0 and f.center.z>.044:f.material_index=1
 if (cy-.034)% .0275<.004:f.material_index=2
# Rounded head, lateral eyes, small paired mandibles. All are explicitly inferred.
ellipsoid('head-rounded-predatory', (0,-.053,.053),(.019,.018,.016),M['dorsal'])
for s,label in [(-1,'left'),(1,'right')]:
 ellipsoid('eye-'+label,(s*.015,-.056,.060),(.010,.013,.0115),M['eyes'])
 g=Mesh();g.tube([(s*.010,-.065,.047),(s*.008,-.075,.043),(s*.0025,-.077,.046)],[.004,.003,.001],6);g.object('mandible-'+label,M['mouth'])
g=Mesh()
for s in [-1,1]:g.tube([(s*.007,-.061,.065),(s*.009,-.073,.070),(s*.010,-.082,.069)],[.0012,.0008,.00035],5)
g.object('short-antennae',M['cuticle'])
# Three true leg pairs. Femur, tibia, tarsus and restrained prey-spine cues share a semantic mesh.
for i,(y,dy,spread) in enumerate([(-.029,-.035,.047),(-.005,.009,.063),(.020,.057,.075)]):
 for s,label in [(-1,'left'),(1,'right')]:
  p0=(s*.015,y,.049);p1=(s*(spread*.66),y+dy*.3,.029);p2=(s*spread,y+dy*.72,.010);p3=(s*(spread-.006),y+dy,.0023)
  g=Mesh();g.tube([p0,p1,p2,p3],[.0037,.003,.002,.0014],7)
  # terminal toes rest near the contact plane, not adhesive suction pads
  g.tube([p3,(p3[0]+s*.004,p3[1]-.004,.0013)],[.0014,.0007],5)
  for t in [.35,.66]:
   q=Vector(p1).lerp(Vector(p2),t);e=q+Vector((-s*.005,-.003,.0008));g.tube([q,e],[.0012,.00035],5)
  g.object('leg-'+str(i+1)+'-'+label,M['cuticle'])
# Paired small terminal appendages, no scorpion sting.
g=Mesh()
for s in [-1,1]:g.tube([(s*.0017,.319,.032),(s*.003,.328,.031),(s*.0025,.333,.031)],[.0013,.0009,.00035],5)
g.object('terminal-cerci',M['cuticle'])
# Broad-based four wings. Span stations carry leading/trailing edge offsets.
FORE=[(.017,-.026,.004),(.040,-.043,.016),(.085,-.063,.020),(.145,-.079,.013),(.210,-.087,-.001),(.270,-.085,-.016),(.318,-.074,-.030),(.342,-.060,-.037),(.350,-.047,-.044)]
HIND=[(.018,.014,.041),(.043,.018,.071),(.088,.026,.101),(.150,.037,.124),(.218,.048,.137),(.277,.059,.135),(.318,.074,.122),(.338,.088,.108),(.343,.098,.101)]
def wingpoint(stations,x,t,s,zadd=0):
 for a,b in zip(stations,stations[1:]):
  if a[0]-1e-9<=x<=b[0]+1e-9:
   f=(x-a[0])/(b[0]-a[0]);lead=a[1]*(1-f)+b[1]*f;trail=a[2]*(1-f)+b[2]*f
   return (s*x,lead*(1-t)+trail*t,.073+.016*(x/.35)+.0018*math.sin(t*math.pi)+zadd)
 raise ValueError('wing coordinate outside outline')
for pair,stations in [('forewing',FORE),('hindwing',HIND)]:
 for s,label in [(-1,'left'),(1,'right')]:
  g=Mesh();vs=[];ts=[0,.23,.48,.73,1]
  for dz in [P['membrane_thickness_m']/2,-P['membrane_thickness_m']/2]:
   for x,_,_ in stations:
    for t in ts:vs.append(wingpoint(stations,x,t,s,dz))
  n=len(stations);k=len(ts);N=n*k;fs=[]
  for row in range(n-1):
   for col in range(k-1):
    q=row*k+col;fs += [(q,q+k,q+k+1,q+1),(q+N,q+1+N,q+k+1+N,q+k+N)]
  edge=[i*k for i in range(n)]+[(n-1)*k+j for j in range(1,k)]+[i*k+k-1 for i in range(n-2,-1,-1)]+list(range(k-2,0,-1))
  fs += [(a,b,b+N,a+N) for a,b in zip(edge,edge[1:]+edge[:1])];g.add(vs,fs);g.object(pair+'-membrane-'+label,M['membrane'])
  if not a.gray:
   vein=Mesh()
   # Five longitudinal traces including the margins; fine branching/cross-link cues are simplified.
   for t in [0,.23,.48,.73,1]:
    pts=[wingpoint(stations,x,t,s,.00065) for x,_,_ in stations]
    r=[P['main_vein_radius_m']*(1-.40*i/(n-1)) for i in range(n)];vein.tube(pts,r,5)
   for i,x in enumerate([.058,.088,.122,.158,.195,.231,.266,.300,.324]):
    for j,(t0,t1) in enumerate(zip(ts,ts[1:])):
     end=min(x+.010+(.003 if (i+j)%2 else 0),stations[-1][0]-.002)
     pts=[wingpoint(stations,x,t0,s,.00065),wingpoint(stations,end,t1,s,.00065)]
     vein.tube(pts,[P['cross_vein_radius_m']]*2,5)
   # Distal forks express branching without asserting an exact taxonomic vein map.
   for t in [.23,.48,.73]:
    vein.tube([wingpoint(stations,.218,t,s,.0007),wingpoint(stations,.278,t+.085,s,.0007),wingpoint(stations,.325,t+.13,s,.0007)],[.0004,.0003,.00023],5)
   vein.object(pair+'-simplified-veins-'+label,M['veins'])
ground_asset(C,False)
for o in C.objects:
 if o.type=='MESH':o['anatomical_part']=o.name
root=bpy.data.objects['meganeura'];root['taxon']='Meganeura monyi';root['representation']='living-reconstruction';root['inferred_anatomy']='Head, mouthparts, abdomen completion, limb proportions, membranes, color and posture';root['reference_specimen']='MNHN-F-R51142';root['venation']='original sparse interpretation, not an exact taxonomic map'
source=audit_source(C,18000)
if source['errors']:raise RuntimeError(str(source['errors']))
bpy.context.preferences.filepaths.save_version=0
# Keep editable data self-contained and remove file-browser defaults before saving.
bpy.context.scene.render.filepath='//preview'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:
    space.params.directory=b''
    space.params.filename=''
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),relative_remap=True)
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={q.identifier for q in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Missing export options')
bpy.ops.export_scene.gltf(**options)
exported=audit_glb(OUT/'model.glb',18000,8,36)
if exported['errors']:raise RuntimeError(str(exported['errors']))
report={'status':'pass','scope':'source geometry and static GLB only; not independent review or browser GPU','blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256(a.params.read_bytes()).hexdigest(),'source':source,'glb':exported,'export_options':{k:v for k,v in options.items() if k!='filepath'},'gray':a.gray}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'triangles':exported['scene_triangles'],'glb_sha256':exported['sha256'],'bytes':exported['bytes']}))
