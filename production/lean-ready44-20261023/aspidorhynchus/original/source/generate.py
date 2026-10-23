# SPDX-License-Identifier: MIT
"""Deterministic original Aspidorhynchus acutirostris, whole living fish.
Run using Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
No images, downloads, external geometry or undeclared build dependencies.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb

P = json.loads((HERE / 'params.json').read_text())
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=HERE.parent)
args = parser.parse_args(argv)
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'qa/evidence').mkdir(parents=True, exist_ok=True)

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(p, data):
    Path(p).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

col = setup_scene('aspidorhynchus', P['seed'])
root = bpy.data.objects[col['asset_root']]
root['authoring_forward'] = '+X'
root['mount'] = P['origin']
root['taxon'] = P['species']
root['primary_specimen'] = P['primary_specimen']
root['scale_status'] = 'Representative species-scale reconstruction, not measured WDC CSG255 size'
mats = {k: make_material(k, v, roughness=0.78 if k != 'dark' else 0.65) for k,v in P['palette'].items()}

# The head and projecting upper premaxilla are continuous with the torso.
# Each profile is x, half-width, lower surface Z, upper surface Z, all metres.
body_profile = [
 (-.350,.006,-.010,.010),(-.325,.009,-.013,.014),(-.295,.013,-.017,.020),
 (-.265,.017,-.023,.026),(-.230,.020,-.028,.032),(-.190,.024,-.033,.037),
 (-.145,.027,-.038,.041),(-.100,.030,-.043,.045),(-.050,.032,-.047,.048),
 (.000,.0325,-.050,.050),(.050,.0323,-.050,.050),(.100,.0315,-.048,.049),
 (.150,.030,-.044,.047),(.190,.028,-.038,.043),(.210,.026,-.032,.038),
 (.235,.023,-.022,.032),(.255,.020,-.014,.027),(.275,.016,-.006,.020),
 (.295,.012,-.000,.015),(.320,.008,.003,.012),(.350,.005,.004,.010),
 (.380,.0034,.005,.0089),(.410,.0019,.0057,.0078),(.438,.00065,.0062,.0070)]
# Subdivision retains hand-defined station silhouette. Mild alternating side facets
# suggest broad ganoid scale rows, not applied armor or copied fossil surface.
def sample_profile(x):
    for a,b in zip(body_profile,body_profile[1:]):
        if a[0] <= x <= b[0]:
            t=(x-a[0])/(b[0]-a[0]); return tuple(a[j]*(1-t)+b[j]*t for j in range(1,4))
    return body_profile[0][1:] if x<body_profile[0][0] else body_profile[-1][1:]

stations=[]
for i,(a,b) in enumerate(zip(body_profile,body_profile[1:])):
    stations.append(a)
    if a[0]<.20:
        stations.append(tuple((a[j]+b[j])/2 for j in range(4)))
stations.append(body_profile[-1])
N=24
verts=[]
for i,(x,w,lo,hi) in enumerate(stations):
    for j in range(N):
        theta=2*math.pi*j/N
        # Mild rhombic shaping only on trunk flank. Ends stay exactly on profile.
        stagger = .0015 * (1 if j%2 else -1) if -.29<x<.18 else 0
        z=(lo+hi)/2+(hi-lo)/2*math.sin(theta)
        y=w*math.cos(theta)
        verts.append((x+stagger,y,z))
faces=[]; mids=[]
for i in range(len(stations)-1):
    for j in range(N):
        faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
        height=math.sin(2*math.pi*(j+.5)/N)
        mids.append(0 if height>.52 else 2 if height<-.54 else 1)
faces.append(tuple(reversed(range(N))));mids.append(1)
tip=len(verts); verts.append((.450,0,.0066))
for j in range(N):
    faces.append(((len(stations)-1)*N+j,(len(stations)-1)*N+(j+1)%N,tip));mids.append(1)
body=mesh_object('Body-head-and-upper-rostrum',verts,faces,[mats['dorsal'],mats['flank'],mats['ventral']],col)
for poly,mi in zip(body.data.polygons,mids):poly.material_index=mi
body['anatomy']='Continuous upper premaxillary rostrum; no detached horn'

# Short, slim lower jaw. Tip at +0.370 vs upper +0.450: 0.080 m overhang.
def loft(name,sections,n,material):
    vs=[];fs=[]
    for x,y,z,ry,rz in sections:
        for j in range(n):
            t=2*math.pi*j/n;vs.append((x,y+ry*math.cos(t),z+rz*math.sin(t)))
    for i in range(len(sections)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.append(tuple(reversed(range(n))));fs.append(tuple((len(sections)-1)*n+j for j in range(n)))
    return mesh_object(name,vs,fs,material,col)
loft('Short-lower-jaw',[(.205,0,-.027,.018,.009),(.235,0,-.025,.018,.006),(.265,0,-.017,.014,.0045),(.295,0,-.0095,.009,.0035),(.325,0,-.0038,.005,.0027),(.350,0,-.0015,.0027,.0018),(.367,0,-.0005,.0010,.0008),(.370,0,-.0003,.0002,.00025)],12,mats['ventral'])

# Editable bilateral eye surrounds and dark eyes, constructed as ellipsoid lofts.
def ellipsoid_component(center,radius,n=16,rings=7):
    c=Vector(center);rx,ry,rz=radius; vs=[tuple(c+Vector((0,0,-rz)))];fs=[]
    for i in range(1,rings):
        phi=-math.pi/2+math.pi*i/rings
        for j in range(n):
            a=2*math.pi*j/n;vs.append(tuple(c+Vector((rx*math.cos(phi)*math.cos(a),ry*math.cos(phi)*math.sin(a),rz*math.sin(phi)))))
    vs.append(tuple(c+Vector((0,0,rz))));top=len(vs)-1
    for j in range(n):fs.append((0,1+(j+1)%n,1+j))
    for i in range(rings-2):
        for j in range(n):
            a=1+i*n+j;b=1+i*n+(j+1)%n;fs.append((a,b,b+n,a+n))
    for j in range(n):fs.append((1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n,top))
    return vs,fs

def combine(name,components,material):
    v=[];f=[]
    for vs,fs in components:
        off=len(v);v.extend(vs);f.extend(tuple(off+i for i in face) for face in fs)
    return mesh_object(name,v,f,material,col)
combine('Paired-orbital-rims',[ellipsoid_component((.260,s*.0178,.013),(.0105,.0027,.010)) for s in (-1,1)],mats['silver'])
combine('Paired-eyes',[ellipsoid_component((.261,s*.0201,.013),(.0076,.0018,.0076)) for s in (-1,1)],mats['dark'])

# Shallow curved gill-cover relief, not an exposed slit or disarticulated plate.
def tube(points,radius,sides=5):
    vs=[];fs=[]
    for i,p in enumerate(points):
        p=Vector(p);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        t.normalize();axis=Vector((1,0,0))
        if abs(t.dot(axis))>.9:axis=Vector((0,0,1))
        u=t.cross(axis).normalized();v=t.cross(u).normalized()
        for j in range(sides):vs.append(tuple(p+radius*(math.cos(j*2*math.pi/sides)*u+math.sin(j*2*math.pi/sides)*v)))
    for i in range(len(points)-1):
        for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    fs.append(tuple(reversed(range(sides))));fs.append(tuple((len(points)-1)*sides+j for j in range(sides)))
    return vs,fs
op=[]
for s in (-1,1):
    pts=[]
    for k in range(11):
        z=-.030+.064*k/10;x=.207-.009*math.cos((z-.002)/.034*math.pi/2)
        w,lo,hi=sample_profile(x);ym=w*math.sqrt(max(0,1-((z-(lo+hi)/2)/((hi-lo)/2))**2))+.0006
        pts.append((x,s*ym,z))
    op.append(tube(pts,.00065,5))
combine('Opercular-relief-lines',op,mats['dorsal'])

# Closed thin fins with shallow radial folds; both faces have deliberate outward normals.
# Contours/spread are inferred and are not a claim of preserved soft-tissue outlines.
fin_components=[]
def fin(outline,normal,thickness,center_override=None):
    normal=Vector(normal).normalized();center=Vector(center_override) if center_override else sum((Vector(p) for p in outline),Vector())/len(outline)
    vs=[];fs=[];n=len(outline)
    # More central thickness, narrow perimeter: a solid, not a double-sided plane.
    for sign in (-1,1):
        for p in outline:vs.append(tuple(Vector(p)+sign*normal*thickness*.20))
        vs.append(tuple(center+sign*normal*thickness))
    for j in range(n):
        k=(j+1)%n;fs.extend([(n,j,k),(2*n+1,n+1+k,n+1+j),(j,n+1+j,n+1+k,k)])
    fin_components.append((vs,fs))

# Posterior opposed median fins; dorsal is a modest ray-supported fan, not a shark fin.
fin([(-.190,0,.030),(-.222,0,.060),(-.244,0,.068),(-.270,0,.056),(-.284,0,.039),(-.292,0,.019),(-.245,0,.025)],(0,1,0),.0018)
fin([(-.196,0,-.029),(-.230,0,-.057),(-.251,0,-.064),(-.276,0,-.051),(-.289,0,-.033),(-.293,0,-.017),(-.246,0,-.024)],(0,1,0),.0016)
# Paired pectoral and pelvic fins, conservative inferred spread.
for s in (-1,1):
    fin([(.191,s*.020,-.023),(.170,s*.046,-.029),(.128,s*.067,-.039),(.097,s*.073,-.044),(.112,s*.045,-.043),(.157,s*.017,-.030)],(0,s*.36,.93),.0018)
    fin([(-.094,s*.012,-.033),(-.111,s*.036,-.041),(-.153,s*.048,-.053),(-.163,s*.041,-.055),(-.140,s*.010,-.032)],(0,s*.40,.92),.0013)
# Forked, vertically oriented caudal fin; longitudinal extent 0.10 m.
fin([(-.344,0,.009),(-.374,0,.035),(-.414,0,.061),(-.450,0,.065),(-.428,0,.033),(-.399,0,0),(-.428,0,-.033),(-.450,0,-.065),(-.414,0,-.061),(-.374,0,-.035),(-.344,0,-.009)],(0,1,0),.0024,(-.370,0,0))
fins=combine('Paired-and-median-fins',fin_components,mats['fin'])
fins['reconstruction']='Fin spread, thickness and margins inferred; 2 pectoral, 2 pelvic, 1 dorsal, 1 anal, vertical forked caudal'

# Thin low-relief ray lines are bundled semantically, not one node per ray.
rays=[]
for side in (-1,1):
    for end in [(-.223,.059),(-.244,.066),(-.266,.055),(-.279,.040)]:
        rays.append(tube([(-.228,side*.0021,.029),((-.228+end[0])/2,side*.0023,(.029+end[1])/2),(end[0],side*.00065,end[1])],.00038,4))
    for end in [(-.231,-.056),(-.251,-.062),(-.274,-.050)]:
        rays.append(tube([(-.235,side*.0019,-.027),((-.235+end[0])/2,side*.0021,(-.027+end[1])/2),(end[0],side*.0006,end[1])],.00035,4))
    for z in [-.057,-.044,-.028,.028,.044,.057]:
        endx=-.414-abs(z)*.43
        rays.append(tube([(-.352,side*.0022,z*.12),(-.389,side*.0025,z*.55),(endx,side*.0007,z)],.00036,4))
combine('Restrained-fin-ray-relief',rays,mats['silver'])

bpy.context.view_layer.update()
source = audit_source(col, 24000)
if source['errors']:raise RuntimeError(source['errors'])
# Save a clean source before importing or adding any preview stage.
bpy.context.scene['asset_license']='CC-BY-4.0'
bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene['scale_note']=root['scale_status']
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.context.preferences.filepaths.save_version=0
# Portable source-state paths are initialized before the first deliverable save.
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type == 'FILE_BROWSER' and space.params:
                space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,
 export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
 export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Missing exporter flags: '+str(set(options)-available))
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**options)
glb=audit_glb(OUT/'model.glb',24000,6,16)
if glb['errors']:raise RuntimeError(glb['errors'])
b=source['bounds_blender_m'];g=glb['bounds_m'];mn=[b['min'][0],b['min'][2],-b['max'][1]];mx=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(g[k][i]-expected[i]) for k,expected in [('min',mn),('max',mx)] for i in range(3))
assert delta<.0001 and source['triangles']==glb['scene_triangles']
assert (OUT/'model.glb').stat().st_size<=2500000
import io_scene_gltf2
report={'asset_id':'aspidorhynchus','revision':'r001','status':'PASS_TECHNICAL_SCOPE_ONLY',
 'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,
 'blender_version':bpy.app.version_string,'gltf_exporter_version':'.'.join(map(str,io_scene_gltf2.bl_info['version'])),
 'export_options':options,'seed':P['seed'],'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),
 'artifact_sha256':{'model.glb':digest(OUT/'model.glb'),'model.blend':digest(OUT/'model.blend')},
 'anatomical_landmarks_m':{'upper_tip_x':.450,'lower_tip_x':.370,'posterior_head_x':.200,'caudal_base_x':-.350,'caudal_extreme_x':-.450,
 'upper_projection_m':.080,'projection_to_headlength_ratio':.32,'standard_length_m':.800,'inferred_total_length_m':.900,'inferred_body_width_m':.065,'inferred_body_depth_m':.100},
 'limits':['Not a measurement of WDC CSG255','Body width, fin edges/spread, soft tissue and palette inferred','No independent visual or scientific approval','No browser GPU or populated scene test'],
 'source_warning_review':['Swimming model has declared mid-body mounting point; lowest-Z warning is expected.'],
 'source_closure':'Bundled source and deps plus Blender standard runtime; no external data required'}
# The audit path is unnecessary private execution detail; preserve only asset-relative name.
for key in ('path','file'):
    if key in report['glb']:report['glb'][key]='model.glb'
write(OUT/'qa/evidence/generator-check.json',report)
print('BUILD COMPLETE',glb['sha256'],glb['scene_triangles'])
