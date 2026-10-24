#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Palaeoniscum living reconstruction.
Run with Blender background mode, two threads, and -- --output-dir OUTPUT.
Only this source tree and the Blender bundled runtime are required.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

HERE=Path(__file__).resolve().parent
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=HERE.parent);p.add_argument('--params',type=Path,default=HERE/'params.json');p.add_argument('--gray',action='store_true');a=p.parse_args(argv)
P=json.loads(a.params.read_text());out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
C=setup_scene(P['asset_id'],P['seed']);root=bpy.data.objects[C['asset_root']]
root['representation']='living-reconstruction';root['mounting_origin']='body center';root['scientific_limits']=P['reconstruction_notes']
mats={k:make_material(k,'#8A8F8A' if a.gray else color,roughness=.82) for k,color in P['palette'].items()}
body_sections=P['body_profile_y_rx_rz_centerz']

def radii(y):
 for i in range(len(body_sections)-1):
  v,w=body_sections[i:i+2]
  if v[0]<=y<=w[0]:
   t=(y-v[0])/(w[0]-v[0]);return tuple(v[j]*(1-t)+w[j]*t for j in [1,2,3])
 return tuple((body_sections[0] if y<body_sections[0][0] else body_sections[-1])[j] for j in [1,2,3])
def surface(y,theta,side=1,relief=0):
 rx,rz,cz=radii(y);return (side*(rx+relief)*math.cos(theta),y,cz+(rz+relief)*math.sin(theta))
def make(name,v,f,material):return mesh_object(name,v,f,material,C)

# Deliberate ring loft: pointed head, long trunk, narrow peduncle, upper caudal axis.
n=P['body_rings'];verts=[];faces=[]
for y,rx,rz,cz in body_sections:
 for j in range(n):
  t=2*math.pi*j/n;verts.append((rx*math.cos(t),y,cz+rz*math.sin(t)))
for i in range(len(body_sections)-1):
 for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
faces.extend([tuple(reversed(range(n))),tuple((len(body_sections)-1)*n+j for j in range(n))])
body=make('Continuous scaled body and upper caudal axis',verts,faces,[mats['body'],mats['dorsal'],mats['ventral']])
for f in body.data.polygons:
 z=f.center.z;y=f.center.y;rx,rz,cz=radii(y);rel=(z-cz)/rz
 f.material_index=1 if rel>.55 else 2 if rel<-.55 else 0

# Low-relief closed rhomboids are merged into two editable flank meshes.
if not a.gray:
 for side in [-1,1]:
  vv=[];ff=[];indices=[]
  for col in range(P['scale_columns']):
   yc=-.052+col*.00485
   for row in range(P['scale_rows_each_flank']):
    theta=(row-4)*.245
    y=yc+(row%2)*.0022
    if y>.065:continue
    # Oblique axial shift produces visible continuous diagonal ganoid bands.
    corners=[(y-.0030,theta-.018),(y-.0008,theta+.151),(y+.0030,theta+.018),(y+.0008,theta-.151)]
    b=len(vv)
    for yy,tt in corners:vv.append(surface(yy,tt,side,.00011))
    for yy,tt in corners:vv.append(surface(yy,tt,side,-.00032))
    vv.append(surface(y-.0003,theta,side,P['scale_relief_m']))
    ff.extend([(b+j,b+(j+1)%4,b+8) for j in range(4)])
    ff.append(tuple(b+4+j for j in reversed(range(4))))
    ff.extend([(b+j,b+4+j,b+4+(j+1)%4,b+(j+1)%4) for j in range(4)])
    indices.extend([0 if (col+row)%4 else 1]*9)
  # Smaller rhomboids continue on the long upper caudal axis.
  for col in range(9):
   y=.068+col*.0043
   for row in range(5):
    theta=(row-2)*.39;dy=.0024*(1-col*.035)
    corners=[(y-dy,theta-.02),(y-dy*.24,theta+.23),(y+dy,theta+.02),(y+dy*.24,theta-.23)]
    b=len(vv)
    for yy,tt in corners:vv.append(surface(yy,tt,side,.00006))
    for yy,tt in corners:vv.append(surface(yy,tt,side,-.00015))
    vv.append(surface(y,theta,side,.00018))
    ff.extend([(b+j,b+(j+1)%4,b+8) for j in range(4)])
    ff.append(tuple(b+4+j for j in reversed(range(4))))
    ff.extend([(b+j,b+4+j,b+4+(j+1)%4,b+(j+1)%4) for j in range(4)])
    indices.extend([0 if (col+row)%4 else 1]*9)
  o=make(('Right' if side>0 else 'Left')+' merged rhomboid scale bands',vv,ff,[mats['scale_light'],mats['scale_alt']])
  for f,idx in zip(o.data.polygons,indices):f.material_index=idx

# All fins are closed thin solids, never alpha cards or two-sided sheets.
def fin(name,pts,normal,thick=.00055):
 normal=Vector(normal).normalized();base=[Vector(p) for p in pts];v=[tuple(p+normal*thick/2) for p in base]+[tuple(p-normal*thick/2) for p in base];n=len(base)
 triangles=tessellate_polygon([base]);idx=lambda v: v if isinstance(v,int) else min(range(n),key=lambda j:(base[j]-v).length)
 f=[tuple(idx(x) for x in tri) for tri in triangles]+[tuple(n+idx(x) for x in reversed(tri)) for tri in triangles]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return make(name,v,f,mats['fin'])
def median(name,yz):return fin(name,[(0,y,z) for y,z in yz],(1,0,0))
median('Heterocercal caudal web',[(.052,.004),(.066,.013),(.089,.024),(.110,.029),(.104,.016),(.087,-.001),(.095,-.014),(.082,-.024),(.071,-.018),(.059,-.003)])
median('Posterior dorsal fin',[(.007,.017),(.015,.027),(.026,.039),(.038,.029),(.045,.013),(.036,.012)])
median('Anal fin',[(.030,-.011),(.041,-.028),(.052,-.029),(.061,-.008),(.052,-.005)])
for side in [-1,1]:
 fin(('Right' if side>0 else 'Left')+' pectoral fin',[(side*.010,-.052,-.004),(side*.021,-.039,-.011),(side*.028,-.017,-.015),(side*.019,-.023,-.007),(side*.010,-.033,-.004)],(side*.45,.10,1),.00065)
 fin(('Right' if side>0 else 'Left')+' pelvic fin',[(side*.007,.005,-.015),(side*.017,.019,-.025),(side*.019,.034,-.027),(side*.010,.027,-.016)],(side*.5,0,1),.00055)

# Fin rays use one merged mesh. Their endpoints stay inside the web margins.
rv=[];rf=[]
def rod(start,end,r=.00017):
 A=Vector(start);B=Vector(end);d=(B-A).normalized();u=d.cross(Vector((0,0,1)))
 if u.length<.01:u=d.cross(Vector((1,0,0)))
 u.normalize();v=d.cross(u).normalized();i=len(rv)
 for t,rr in [(A,r),(B,r*.52)]:
  for j in range(4):rv.append(tuple(t+(u*math.cos(j*math.pi/2)+v*math.sin(j*math.pi/2))*rr))
 rf.extend([(i+j,i+(j+1)%4,i+4+(j+1)%4,i+4+j) for j in range(4)]);rf.extend([(i+3,i+2,i+1,i),(i+4,i+5,i+6,i+7)])
if not a.gray:
 for x in [-.0004,.0004]:
  for end in [(.019,.028),(.025,.036),(.031,.034),(.036,.029),(.040,.023)]:rod((x,.028,.015),(x,*end))
  for end in [(.042,-.025),(.048,-.027),(.053,-.023),(.057,-.015)]:rod((x,.043,-.009),(x,*end))
  for end in [(.102,.023),(.101,.017),(.095,.010),(.089,.003),(.090,-.013),(.083,-.021),(.076,-.017)]:rod((x,.063,.004),(x,*end))
 for side in [-1,1]:
  for end in [(side*.023,-.026,-.013),(side*.019,-.029,-.009),(side*.016,-.033,-.007)]:rod((side*.012,-.047,-.0045),end)
  for end in [(side*.016,.027,-.024),(side*.014,.023,-.021)]:rod((side*.008,.009,-.015),end)
 make('Merged fin-ray relief',rv,rf,mats['ray'])

# Flattened semantic opercular plates and restrained eyes, not oversized mascot eyes.
for side in [-1,1]:
 y=-.054;theta=.03
 points=[(-.066,.008),(-.059,.013),(-.050,.011),(-.046,-.002),(-.052,-.013),(-.061,-.009)]
 vv=[(side*(radii(yy)[0]*math.sqrt(max(.1,1-((zz-radii(yy)[2])/radii(yy)[1])**2))+.0002),yy,zz) for yy,zz in points]
 fin(('Right' if side>0 else 'Left')+' opercular plate',vv,(side,0,0),.0005).data.materials[0]=mats['body']
 def eye_part(name,rx,ry,rz,mat):
  center=Vector((side*.0084,-.071,.0061));v=[];f=[];N=12
  # Two ring levels plus pole caps, fully closed ellipsoid.
  v.append(tuple(center+Vector((side*rx,0,0))))
  for level in [.42,-.42]:
   rr=math.sqrt(1-level*level)
   for j in range(N):t=2*math.pi*j/N;v.append(tuple(center+Vector((side*rx*level,ry*rr*math.cos(t),rz*rr*math.sin(t)))))
  v.append(tuple(center+Vector((-side*rx,0,0))));end=len(v)-1
  for j in range(N):f.append((0,1+j,1+(j+1)%N));f.append((1+j,1+N+j,1+N+(j+1)%N,1+(j+1)%N));f.append((end,1+N+(j+1)%N,1+N+j))
  return make(name,v,f,mat)
 eye_part(('Right' if side>0 else 'Left')+' eye',.0016,.0026,.0025,mats['eye'])
# Mouth is a discrete narrow dark strip on the pointed rostrum.
fin('Short jaw line',[(-.003,-.086,-.0011),(0,-.0902,-.0013),(.003,-.086,-.0011),(.0028,-.0846,-.0018),(-.0028,-.0846,-.0018)],(0,0,1),.00035).data.materials[0]=mats['eye']

bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
source=audit_source(C,P['geometry_policy']['max_triangles'])
if source['errors']:raise RuntimeError(str(source['errors']))
# The editable file contains only original model geometry and its identity root.
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params is not None:
    space.params.directory=b'//'
bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
os.chdir(out);bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),relative_remap=True)
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath='model.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Missing required exporter flags: '+str(missing))
bpy.ops.export_scene.gltf(**options)
g=audit_glb('model.glb',P['geometry_policy']['max_triangles'],P['geometry_policy']['max_materials'],P['geometry_policy']['max_primitives'])
if g['errors']:raise RuntimeError(str(g['errors']))
if g['bytes']>P['geometry_policy']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]};delta=max(abs(g['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
if source['triangles']!=g['scene_triangles'] or delta>1e-4:raise RuntimeError('Source/export geometry mismatch')
h=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
report={'status':'PASS','scope':'Source geometry, static GLB audit and axis-converted bounds only','asset_id':P['asset_id'],'revision':P['revision'],'gray_model':a.gray,'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','generator_sha256':h(Path(__file__)),'params_sha256':h(a.params),'source':source,'glb':g,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_blend_sha256':h(out/'model.blend'),'glb_sha256':h(out/'model.glb')}
(out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','triangles':g['scene_triangles'],'bytes':g['bytes'],'glb_sha256':h(out/'model.glb')}))
