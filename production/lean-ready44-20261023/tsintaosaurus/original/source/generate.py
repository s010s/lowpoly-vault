# SPDX-License-Identifier: MIT
"""Original parameterized Tsintaosaurus, expanded 2020 crest interpretation.
The fossil-derived outline is interpreted, never a scan. Run with Blender 4.3.2.
Only package-relative code and configuration are read.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args(args)
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
col=setup_scene(P['asset_id'],P['seed'])
root=bpy.data.objects[col['asset_root']]
root['scientific_scope']='Living reconstruction. Crest missing regions and soft tissue inferred; 12 m genus estimate, not a measured individual.'
M={k:make_material(k,v,roughness=0.84) for k,v in P['palette'].items()}
class Mesh:
 def __init__(self,name,materials): self.name=name; self.ms=materials; self.v=[]; self.f=[]; self.mi=[]; self.groups=[]
 def add(self,name,verts,faces,matids=None):
  n=len(self.v); self.v+=verts;self.f += [tuple(i+n for i in f) for f in faces];self.mi += matids or [0]*len(faces);self.groups.append((name,n,len(self.v)))
 def finish(self):
  ob=mesh_object(self.name,self.v,self.f,[M[x] for x in self.ms],col)
  for p,i in zip(ob.data.polygons,self.mi):p.material_index=i
  for name,start,end in self.groups:ob.vertex_groups.new(name=name).add(list(range(start,end)),1,'REPLACE')
  return ob

def loft_y(target,name,rings,n=16,color=False):
 # rings: y, center Z, half width, vertical half height; capped continuous profile.
 v=[];f=[];ids=[]
 for y,z,rx,rz in rings:
  for j in range(n):
   t=2*math.pi*j/n;v.append((rx*math.cos(t),y,z+rz*math.sin(t)))
 f.append(tuple(reversed(range(n))));ids.append(0)
 for i in range(len(rings)-1):
  for j in range(n):
   f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
   t=2*math.pi*(j+.5)/n;ids.append((1 if math.sin(t)>.70 else 2 if math.sin(t)<-.65 else 0) if color else 0)
 f.append(tuple((len(rings)-1)*n+j for j in range(n)));ids.append(0)
 target.add(name,v,f,ids)

def tube(target,name,centers,radii,n=12):
 v=[];f=[]
 for i,c in enumerate(centers):
  c=Vector(c);t=Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(i-1,0)]);t.normalize()
  u=Vector((1,0,0));u=(u-t*u.dot(t)).normalized();w=t.cross(u).normalized()
  rx,ry=radii[i]
  for j in range(n):
   ang=2*math.pi*j/n;v.append(tuple(c+u*(rx*math.cos(ang))+w*(ry*math.sin(ang))))
 f.append(tuple(reversed(range(n))))
 for i in range(len(centers)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 f.append(tuple((len(centers)-1)*n+j for j in range(n)))
 target.add(name,v,f)

def ellipsoid(target,name,c,r,n=12,k=6):
 v=[(c[0],c[1],c[2]+r[2])];f=[]
 for i in range(1,k):
  ph=math.pi*i/k
  for j in range(n):
   th=2*math.pi*j/n;v.append((c[0]+r[0]*math.sin(ph)*math.cos(th),c[1]+r[1]*math.sin(ph)*math.sin(th),c[2]+r[2]*math.cos(ph)))
 v.append((c[0],c[1],c[2]-r[2]));end=len(v)-1
 for j in range(n):f.append((0,1+j,1+(j+1)%n))
 for i in range(k-2):
  for j in range(n):f.append((1+i*n+j,1+(i+1)*n+j,1+(i+1)*n+(j+1)%n,1+i*n+(j+1)%n))
 for j in range(n):f.append((end,1+(k-2)*n+(j+1)%n,1+(k-2)*n+j))
 target.add(name,v,f)

# Deliberate linked profiles establish the long tail, deep abdomen and rising neck.
body=Mesh('01_trunk_neck_tail',['skin','dorsal','underside'])
loft_y(body,'continuous axial profile',[
 (-3.12,3.38,.23,.28),(-2.86,3.40,.30,.39),(-2.59,3.27,.37,.48),
 (-2.27,3.03,.46,.58),(-1.96,2.74,.61,.74),(-1.52,2.50,.76,.91),
 (-.90,2.44,.94,1.03),(-.10,2.49,1.02,1.10),(.65,2.51,.99,1.07),
 (1.20,2.48,.85,.94),(1.78,2.37,.68,.73),(2.30,2.20,.51,.53),
 (2.95,1.98,.40,.40),(3.7,1.73,.31,.29),(4.55,1.47,.23,.21),
 (5.35,1.25,.17,.15),(6.15,1.06,.105,.10),(6.9,.92,.061,.055),(7.55,.83,.015,.016)],20,True)
body.finish()
head=Mesh('02_head_cheeks',['skin'])
loft_y(head,'elongated duckbill skull',[(-4.40,3.15,.31,.14),(-4.22,3.20,.32,.20),(-3.99,3.31,.25,.25),(-3.73,3.40,.25,.29),(-3.48,3.50,.31,.34),(-3.22,3.54,.34,.38),(-2.98,3.53,.29,.35),(-2.80,3.48,.20,.24)],16)
head.finish()
bill=Mesh('03_broad_beak',['horn'])
loft_y(bill,'keratinous duckbill',[(-4.45,3.13,.27,.09),(-4.40,3.14,.34,.13),(-4.23,3.17,.34,.14),(-4.08,3.20,.27,.12)],16)
bill.finish()

# Cross-sectional rings follow Fig4's broad summit and rostral inclination.
# Each station provides the front and rear border in sagittal view and transverse half width.
# A solid exterior mesh is used; no claim that the entire crest interior is solid.
crest=Mesh('04_expanded_cranial_crest',['crest'])
stations=[(3.26,-4.27,-3.02,.155),(3.55,-3.98,-2.99,.19),(3.82,-3.78,-3.04,.17),
 (4.12,-3.73,-3.15,.14),(4.42,-3.81,-3.22,.13),(4.72,-4.00,-3.27,.13),
 (5.00,-4.16,-3.28,.15),(5.24,-4.18,-3.31,.16),(5.42,-4.07,-3.42,.15),
 (5.50,-3.90,-3.61,.085)]
v=[];f=[];n=12
for z,front,rear,width in stations:
 cy=(front+rear)/2;ry=(rear-front)/2
 for j in range(n):
  t=2*math.pi*j/n;v.append((width*math.cos(t),cy+ry*math.sin(t),z))
f.append(tuple(reversed(range(n))))
for i in range(len(stations)-1):
 for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
f.append(tuple((len(stations)-1)*n+j for j in range(n)))
crest.add('lobate thin transverse crest',v,f);crest.finish()

fore=Mesh('05_forelimbs',['skin']);hind=Mesh('06_hindlimbs',['skin'])
for s in (-1,1):
 d=.10 if s==1 else -.10
 tube(fore,'left forelimb' if s<0 else 'right forelimb',[(s*.55,-1.75,2.57),(s*.66,-1.58,2.15),(s*.67,-1.30,1.60),(s*.62,-1.48,1.02),(s*.61,-1.60,.38)],[(.26,.32),(.25,.27),(.20,.22),(.15,.17),(.15,.16)],12)
 tube(hind,'left hindlimb' if s<0 else 'right hindlimb',[(s*.64,.88,2.63),(s*.87,.91,2.29),(s*1.00,.52+d,1.63),(s*.98,.80+d,1.15),(s*.93,1.20+d,.55),(s*.92,1.03+d,.26)],[(.45,.50),(.45,.50),(.35,.36),(.23,.23),(.15,.17),(.17,.18)],14)
fore.finish();hind.finish()
feet=Mesh('07_functional_feet',['horn'])
for s in (-1,1):
 d=.10 if s==1 else -.10
 # Compact forefoot columns, not splayed grasping or pronated palms.
 tube(feet,'compact supported forefoot',[(s*.61,-1.60,.45),(s*.61,-1.65,.25),(s*.61,-1.71,.07)],[(.16,.17),(.18,.20),(.18,.22)],12)
 # Three weight-bearing toes remain close; longitudinal seams are a stylization.
 ellipsoid(feet,'hindfoot pad',(s*.92,.93+d,.22),(.27,.40,.22),12,6)
 for k in (-1,0,1):
  ellipsoid(feet,'hind toe', (s*.92+k*.17,.65+d- (.05 if k==0 else 0),.13),(.105,.29,.13),10,6)
for i,(x,y,z) in enumerate(feet.v):
 if y < -.9 and z < .15: feet.v[i]=(x,y,0.0)
feet.finish()
features=Mesh('08_eyes_nares_mouth',['eye'])
for s in (-1,1):
 ellipsoid(features,'eye',(s*.307,-3.22,3.69),(.040,.082,.067),12,6)
 ellipsoid(features,'nostril',(s*.26,-4.02,3.37),(.022,.07,.035),10,6)
 # Tiny flush closed oral seam on each side, not an open floating jaw strip.
 tube(features,'mouth seam',[(s*.309,-4.37,3.105),(s*.325,-4.22,3.125),(s*.267,-3.96,3.16),(s*.277,-3.66,3.19)],[(.010,.012)]*4,6)
features.finish()
# All authored coordinates use meters. Root origin stays at floor footprint center.
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
scene['generator_seed']=P['seed'];scene['taxon']='Tsintaosaurus spinorhinus';scene['representation']='living-reconstruction'
source=audit_source(col,6500)
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in col.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Exporter flags unavailable')
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
glb=audit_glb(out/'model.glb',6500,6,12)
glb['file']='model.glb'
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
err=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
assert not glb['errors'] and glb['scene_triangles']==source['triangles'] and err<1e-4 and glb['bytes']<=2000000
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'status':'PASS','scope':'Source geometry, static embedded GLB audit and axis-aware source/export equivalence only. Not visual, factual, GPU or independent approval.','asset_id':P['asset_id'],'revision':P['revision'],'blender':bpy.app.version_string,'generator_sha256':sha(Path(__file__)),'params_sha256':sha(HERE/'params.json'),'source':source,'glb':glb,'source_export_bounds_error_m':err,'export_options':options,'three_consumer_version':P['three_version'],'source_only_scene':{'cameras':sum(o.type=='CAMERA' for o in scene.objects),'lights':sum(o.type=='LIGHT' for o in scene.objects)},'scale_note':'Overall length 12 m is a genus estimate, not a measured individual; crest scale and soft tissue are interpreted.'}
(out/'technical.json').write_text(json.dumps(report,indent=2)+'\n')
print('BUILD_OK',glb['sha256'],glb['scene_triangles'],glb['bytes'])
