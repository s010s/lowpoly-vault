# SPDX-License-Identifier: MIT
"""Deterministic Ouranosaurus living reconstruction, metres; head -Y, up +Z.
Run with Blender background mode, --python generate.py -- --output-dir OUTPUT.
The default output is this portable bundle root. No reference image is embedded.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
PARAMS=json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE.parent);args=ap.parse_args(argv)
OUT=args.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True);(OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
COL=setup_scene('ouranosaurus',PARAMS['seed'])
MATS={name:make_material(name,colour,roughness=0.87) for name,colour in PARAMS['palette_srgb'].items()}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,v):(OUT/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
class Part:
 def __init__(self,name,materials):self.name=name;self.materials=materials;self.v=[];self.f=[];self.mi=[];self.groups=[]
 def add(self,verts,faces,material=0,label=None):
  start=len(self.v);self.v+=verts;self.f += [tuple(start+i for i in f) for f in faces];self.mi += material if isinstance(material,list) else [material]*len(faces)
  if label:self.groups.append((label,list(range(start,len(self.v)))))
 def finish(self):
  ob=mesh_object(self.name,self.v,self.f,[MATS[x] for x in self.materials],COL)
  for p,i in zip(ob.data.polygons,self.mi):p.material_index=i
  for label,ids in self.groups:ob.vertex_groups.new(name=label).add(ids,1.,'REPLACE')
  ob['construction']='Deliberate closed lofts; overlapping anatomical attachments are intentional, not a printable union.'
  return ob

def loft_y(part,rings,n=16,label='loft',material=0,ventral=False):
 verts=[];faces=[];mats=[]
 for y,z,rx,rz in rings:
  for j in range(n):
   a=2*math.pi*j/n;verts.append((rx*math.cos(a),y,z+rz*math.sin(a)))
 for i in range(len(rings)-1):
  for j in range(n):
   faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
   mats.append(1 if ventral and math.sin(2*math.pi*(j+.5)/n)<-.62 else material)
 faces += [tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+j for j in range(n))];mats += [material,material]
 part.add(verts,faces,mats,label)

def path_loft(part,path,n=10,material=0,label='segment'):
 verts=[];faces=[]
 for i,(xyz,rx,ry) in enumerate(path):
  p=Vector(xyz);t=Vector(path[min(i+1,len(path)-1)][0])-Vector(path[max(i-1,0)][0]);t.normalize();u=Vector((1,0,0));v=t.cross(u).normalized()
  for j in range(n):
   a=2*math.pi*j/n;verts.append(tuple(p+u*rx*math.cos(a)+v*ry*math.sin(a)))
 for i in range(len(path)-1):
  for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 faces += [tuple(range(n-1,-1,-1)),tuple((len(path)-1)*n+j for j in range(n))]
 part.add(verts,faces,material,label)

def ellipsoid(part,center,radius,n=10,rings=6,material=0,label='detail'):
 verts=[(center[0],center[1],center[2]-radius[2])];faces=[]
 for k in range(1,rings):
  lat=-math.pi/2+math.pi*k/rings
  for j in range(n):
   a=2*math.pi*j/n;verts.append((center[0]+radius[0]*math.cos(lat)*math.cos(a),center[1]+radius[1]*math.cos(lat)*math.sin(a),center[2]+radius[2]*math.sin(lat)))
 top=len(verts);verts.append((center[0],center[1],center[2]+radius[2]))
 for j in range(n):faces.append((0,1+(j+1)%n,1+j))
 for k in range(rings-2):
  for j in range(n):faces.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
 for j in range(n):faces.append((top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n))
 part.add(verts,faces,material,label)

body=Part('neck-trunk-long-tail',['skin','ventral'])
loft_y(body,[(-1.82,2.04,.17,.20),(-1.58,2.03,.23,.26),(-1.30,1.94,.28,.31),(-1.00,1.77,.38,.44),(-.65,1.58,.51,.60),(-.15,1.49,.61,.65),(.40,1.48,.60,.64),(.85,1.49,.52,.58),(1.20,1.53,.39,.43),(1.55,1.57,.29,.29),(1.95,1.55,.22,.23),(2.45,1.49,.15,.16),(2.95,1.42,.105,.12),(3.45,1.32,.065,.075),(3.95,1.19,.031,.04),(4.40,1.08,.003,.005)],16,'continuous neck torso and restored tail tip',ventral=True)
body.finish()

head=Part('low-elongated-beaked-head',['skin'])
loft_y(head,[(-2.47,2.075,.185,.09),(-2.32,2.09,.205,.115),(-2.12,2.13,.205,.13),(-1.92,2.18,.235,.19),(-1.73,2.19,.22,.215),(-1.60,2.15,.16,.16)],12,'long low skull')
for sign in (-1,1):ellipsoid(head,(sign*.108,-2.02,2.255),(.080,.18,.070),10,5,label='modest nasal swelling')
head.finish()
bill=Part('broad-closed-keratin-bill',['keratin'])
loft_y(bill,[(-2.60,2.055,.16,.050),(-2.57,2.065,.205,.068),(-2.43,2.075,.214,.080),(-2.34,2.08,.192,.078)],12,'broad terminal beak')
bill.finish()

sail=Part('continuous-covered-dorsal-sail',['sail','sail_edge'])
# Explicit high dorsal dome, shallow saddle and lower proximal-tail rise.
profiles=[(-1.22,2.09,2.19,.20),(-1.05,2.10,2.53,.24),(-.77,2.10,2.87,.27),(-.40,2.04,3.10,.28),(0.0,2.00,3.18,.29),(.42,2.00,3.10,.28),(.80,1.98,2.87,.25),(1.13,1.89,2.73,.20),(1.43,1.78,2.77,.16),(1.72,1.72,2.59,.13),(2.02,1.65,2.25,.10),(2.29,1.57,1.93,.075),(2.52,1.50,1.65,.045)]
levels=[0,.34,.72,.92,1.0];v=[];f=[];mi=[]
# Section is a closed thick lens, not an exposed bone sheet or isolated fin.
section=[(1,t) for t in levels]+[(-1,t) for t in reversed(levels)]
for y,base,top,width in profiles:
 for sign,t in section:
  w=width*(1-t)**1.35+.012
  v.append((sign*w,y,base+(top-base)*t))
k=len(section)
for i in range(len(profiles)-1):
 for j in range(k):
  f.append((i*k+j,i*k+(j+1)%k,(i+1)*k+(j+1)%k,(i+1)*k+j));mi.append(1 if min(section[j][1],section[(j+1)%k][1])>=.92 else 0)
f += [tuple(range(k-1,-1,-1)),tuple((len(profiles)-1)*k+j for j in range(k))];mi += [0,0]
sail.add(v,f,mi,'covered high sail and lower posterior rise');sail.finish()

for limb in ('fore','hind'):
 part=Part('paired-'+limb+'limbs',['skin','keratin'])
 for s in (-1,1):
  if limb=='fore':
   path=[((s*.40,-.68,1.55),.19,.21),((s*.50,-.69,1.19),.15,.16),((s*.51,-.84,.79),.115,.13),((s*.49,-.77,.41),.085,.095),((s*.49,-.83,.16),.09,.08)]
   footy=-.91;footx=s*.49;toe_r=.053;toe_len=.16;toe_space=.070
  else:
   path=[((s*.40,.75,1.58),.30,.33),((s*.55,.54,1.24),.27,.29),((s*.61,.29,.87),.18,.21),((s*.60,.59,.48),.11,.12),((s*.58,.83,.16),.13,.105)]
   footy=.67;footx=s*.58;toe_r=.075;toe_len=.30;toe_space=.100
  path_loft(part,path,12,0,('left ' if s<0 else 'right ')+limb+' limb')
  # Broad weight-bearing digits, all three ground at Z=0, not theropod talons.
  for j in (-1,0,1):
   x=footx+j*toe_space;extend=toe_len*(1.0 if j==0 else .86)
   path_loft(part,[((x,footy+.11,.11),toe_r,.10),((x,footy-.01,.085),toe_r*1.02,.085),((x,footy-extend,.055),toe_r*.84,.055)],8,0,'digit '+str(j))
   path_loft(part,[((x,footy-extend+.015,.055),toe_r*.86,.055),((x,footy-extend-.055,.045),toe_r*.70,.045)],8,1,'short blunt hoof')
 part.v=[(x,y,0.0 if z<.045 else z) for x,y,z in part.v]
 part.finish()

detail=Part('paired-eyes-nostrils-and-mouth-seam',['details'])
for s in (-1,1):
 ellipsoid(detail,(s*.230,-1.835,2.265),(.021,.057,.043),12,6,label='eye')
 ellipsoid(detail,(s*.193,-2.285,2.135),(.012,.027,.015),10,5,label='nostril')
 # Thin closed neutral mouth seam. No tooth rows, gap or predatory grin.
 path_loft(detail,[((s*.205,-2.43,2.047),.005,.008),((s*.208,-2.20,2.037),.005,.008),((s*.207,-1.995,2.052),.005,.008)],6,0,'closed beak mouth seam')
detail.finish()
# Recenter contact footprint, not the long-tailed bounding box.
contacts=[v.co for o in COL.all_objects if o.type=='MESH' for v in o.data.vertices if v.co.z<.00001]
origin_y=(min(v.y for v in contacts)+max(v.y for v in contacts))/2
for ob in COL.all_objects:
 if ob.type=='MESH':
  for v in ob.data.vertices:v.co.y-=origin_y
bpy.context.scene['scale_note']='Seven metres is an artistic conventional estimate; not a measured complete adult.'
bpy.context.scene['reconstruction_limits']='MSNVE3714 is restored and immature with missing tail tip and restored mounted skull. Tissue outline, colour and pose inferred.'
bpy.context.scene.render.filepath='//'
bpy.context.preferences.filepaths.save_version=0
# Remove factory UI navigation history before saving a portable source file.
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:
    space.params.directory=b'.'*1023
    space.params.directory=b'//'
    space.params.filename='.'*255
    space.params.filename='model.blend'
source=audit_source(COL,6500)
if source['errors']:raise RuntimeError(source['errors'])
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[COL['asset_root']]
opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available:raise RuntimeError('Exporter options unavailable')
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**opts)
glb=audit_glb(OUT/'model.glb',6500,6,12)
# Publish a portable artifact identifier, never a machine-local report path.
glb['file']='model.glb'
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>2000000:raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][key][i]-expected[key][i]) for key in expected for i in range(3))
assert delta<.0001 and source['triangles']==glb['scene_triangles']
assert abs(b['size'][1]-7.)<.0001
report={'status':'PASS','scope':'Source mesh, export, budgets and source-to-GLB axes/bounds only; not independent visual or GPU acceptance.','glb_sha256':sha(OUT/'model.glb'),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':'.'.join(map(str,__import__('io_scene_gltf2').bl_info['version'])),'export_options':opts,'source':source,'glb':glb,'source_glb_bounds_delta_m':delta,'contact_origin_shift_y_m':origin_y,'separate_mesh_policy':'Editable semantic parts retained. Lofted parts are individually closed; intentional anatomical overlaps, not a boolean union.','warnings_review':[]}
write('qa/evidence/source-export.json',report)
print('BUILD_OK',glb['sha256'],glb['scene_triangles'],glb['bytes'])
