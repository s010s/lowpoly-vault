#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic Alioramus altai living reconstruction. Run inside Blender.
Usage: blender -b -t 2 --python source/generate.py -- --output-dir .
Only bpy, Python standard libraries, params.json and declared relative helpers are needed.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P = json.loads((HERE/'params.json').read_text())
args = argparse.ArgumentParser()
args.add_argument('--output-dir', type=Path, default=Path('.'))
a = args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out = a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
collection = setup_scene(P['asset_id'], seed=P['seed'])
root = bpy.data.objects[collection['asset_root']]
root['specimen_basis']='Alioramus altai, IGM 100/1844; nine-year-old juvenile'
root['reconstruction_limits']='Forelimbs and missing bones restored; 6 m is an estimate; colours and external soft tissues inferred.'
mats=[make_material(k,v,roughness=.86) for k,v in P['palette'].items()]
parts=[]
def mesh(name,verts,faces,indices=None):
    ob=mesh_object(name,verts,faces,mats,collection)
    if indices:
        for f,i in zip(ob.data.polygons,indices): f.material_index=i
    parts.append(ob);return ob

def axial(name,stations,n=12,colors=True):
    # Stations: lateral X, longitudinal Y, vertical Z, half-width, half-depth.
    verts=[]
    for x,y,z,w,h in stations:
        verts.extend([(x+w*math.cos(2*math.pi*j/n),y,z+h*math.sin(2*math.pi*j/n)) for j in range(n)])
    faces=[tuple(range(n-1,-1,-1))];mi=[0]
    for i in range(len(stations)-1):
        for j in range(n):
            faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
            mid=math.sin(2*math.pi*(j+.5)/n)
            mi.append(1 if colors and mid<-.52 else 0)
    faces.append(tuple((len(stations)-1)*n+j for j in range(n)));mi.append(0)
    return mesh(name,verts,faces,mi)

def tube(name,points,radii,n=8,mat=0):
    pts=list(map(Vector,points));v=[]
    for i,(p,r) in enumerate(zip(pts,radii)):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        ref=Vector((1,0,0)) if abs(tangent.x)<.8 else Vector((0,1,0))
        u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
        rx,ry=r if isinstance(r,(tuple,list)) else (r,r)
        v.extend([tuple(p+u*(rx*math.cos(2*math.pi*j/n))+w*(ry*math.sin(2*math.pi*j/n))) for j in range(n)])
    f=[tuple(range(n-1,-1,-1))]
    for i in range(len(pts)-1):
        for j in range(n): f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.append(tuple((len(pts)-1)*n+j for j in range(n)))
    return mesh(name,v,f,[mat]*len(f))

def ellipsoid(name,center,scale,mat,n=10,rings=5):
    # Nonzero polar rings and flat polar caps avoid degenerate pole quads.
    v=[]
    for i in range(rings):
        phi=-math.pi/2+.12+(math.pi-.24)*i/(rings-1)
        for j in range(n):
            t=2*math.pi*j/n
            v.append((center[0]+scale[0]*math.cos(phi)*math.cos(t),center[1]+scale[1]*math.cos(phi)*math.sin(t),center[2]+scale[2]*math.sin(phi)))
    f=[tuple(range(n-1,-1,-1))]
    for i in range(rings-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.append(tuple((rings-1)*n+j for j in range(n)))
    return mesh(name,v,f,[mat]*len(f))

# One continuous loft gives cervical, thoracic, pelvic and caudal silhouette.
axial('cervical-trunk-and-tapered-tail',P['body_stations'],16)
# Whole skull: filled flesh-covered face, no skeletal fenestra holes.
# Each profile = y, halfwidth, ventral, dorsal, additional midline bump relief.
v=[]; profiles=P['skull_profiles'];n=16
for y,w,lo,hi,bump in profiles:
    for j in range(n):
        t=2*math.pi*j/n;s=math.sin(t)
        v.append((w*math.cos(t),y,lo+(hi-lo)*(s+1)/2+bump*max(0,s)**12))
f=[tuple(range(n-1,-1,-1))];mi=[0]
for i in range(len(profiles)-1):
    for j in range(n):
        f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        # Skin-coloured low relief, not three giant differently coloured horns.
        mi.append(2 if profiles[i][4]>.01 and j in [3,4] else 0)
f.append(tuple((len(profiles)-1)*n+j for j in range(n)));mi.append(0)
mesh('elongate-shallow-cranium-three-integrated-nasal-rugosities',v,f,mi)
axial('slender-mandible',[(0,-2.54,1.805,.048,.026),(0,-2.44,1.793,.079,.032),(0,-2.24,1.785,.094,.034),(0,-1.99,1.802,.113,.043),(0,-1.77,1.832,.134,.066),(0,-1.58,1.882,.14,.10)],12)
# Continuous dark mouth seam under the upper lip; it is not an open skull window.
axial('mouth-gap',[(0,-2.52,1.832,.048,.009),(0,-2.37,1.838,.085,.015),(0,-2.13,1.855,.106,.019),(0,-1.91,1.88,.125,.019),(0,-1.71,1.922,.138,.012)],10,False)
for face in parts[-1].data.polygons: face.material_index=3
for side in [-1,1]:
    tag='left' if side<0 else 'right'
    ellipsoid(tag+'-eye-socket',(side*.151,-1.715,2.058),(.026,.056,.045),3)
    ellipsoid(tag+'-amber-eye',(side*.174,-1.725,2.06),(.013,.029,.029),4,n=10,rings=5)
    ellipsoid(tag+'-pupil',(side*.184,-1.730,2.062),(.006,.012,.021),3,n=8,rings=4)
    # Lateral jugal horn is distinct from the ventral cornual process.
    tube(tag+'-lateral-jugal-horn',[(side*.132,-1.63,1.94),(side*.217,-1.62,1.97),(side*.29,-1.605,1.99)],[.058,.035,.002],n=7,mat=2)
    tube(tag+'-low-lacrimal-ornament',[(side*.135,-1.765,2.094),(side*.15,-1.748,2.154),(side*.16,-1.73,2.173)],[.044,.024,.002],n=7,mat=0)
    ellipsoid(tag+'-nostril',(side*.072,-2.405,1.949),(.005,.031,.016),3,n=8,rings=4)
    # Small exposed tooth tips, a display choice, not a complete dental census.
    for j in range(12):
        t=j/11;y=-2.43+.62*t;w=.078+.052*t;z=1.847+.055*t
        tube(tag+'-maxillary-tooth-%02d'%j,[(side*w,y,z),(side*(w*.98),y-.004,z-.030-.008*math.sin(math.pi*t))],[.009,.0012],n=5,mat=5)
    # Long gracile hindlimbs with the two feet slightly staggered for leg separation.
    off=0.10 if side>0 else -.10
    hip=(side*.265,.18,1.55);knee=(side*.36,-.23+off,.96);ankle=(side*.345,.22+off,.49);base=(side*.345,.035+off,.115)
    tube(tag+'-thigh',[hip,(side*.32,.02+off,1.34),knee],[(.22,.205),(.198,.18),(.108,.10)],n=12)
    tube(tag+'-shank',[knee,(side*.35,-.04+off,.79),ankle],[.105,.099,.058],n=10)
    tube(tag+'-metatarsus',[ankle,(side*.345,.18+off,.28),base],[.059,.047,.062],n=8)
    for j in [-1,0,1]:
        x=side*.345+j*.064;end=(x+j*.055,-.27+off-(.05 if j==0 else 0),.039)
        tube(tag+'-pedal-digit-'+str(j),[(side*.345+j*.018,.035+off,.10),(x,-.13+off,.057),end],[.043,.033,.021],n=7)
        tube(tag+'-pedal-claw-'+str(j),[end,(end[0]+j*.012,end[1]-.082,end[2]-.017),(end[0]+j*.015,end[1]-.12,.005)],[.023,.014,.0015],n=6,mat=3)
    tube(tag+'-raised-hallux',[(side*.32,.095+off,.17),(side*.28,.19+off,.12)],[.023,.003],n=6,mat=3)
    # Short inferred arms. Hands lie in sagittal planes, palms face inward.
    shoulder=(side*.215,-.72,1.58);elbow=(side*.27,-.73,1.30);wrist=(side*.275,-.93,1.27)
    tube(tag+'-inferred-upper-arm',[shoulder,(side*.255,-.71,1.44),elbow],[.079,.064,.043],n=8)
    tube(tag+'-inferred-forearm',[elbow,wrist],[.044,.03],n=8)
    for j in [0,1]:
        start=(side*.278,-.93,1.285-j*.045);mid=(side*.278,-1.025,1.27-j*.044);end=(side*.28,-1.065,1.228-j*.038)
        tube(tag+'-inferred-manual-digit-'+str(j),[start,mid,end],[.018,.014,.002],n=6,mat=3)

# Ground the lowest toe/claw surface, then center the paired pedal footprint.
footpoints=[v.co.copy() for ob in parts if '-pedal-' in ob.name for v in ob.data.vertices]
allpoints=[v.co.copy() for ob in parts for v in ob.data.vertices]
shift=Vector((-(min(v.x for v in footpoints)+max(v.x for v in footpoints))/2,-(min(v.y for v in footpoints)+max(v.y for v in footpoints))/2,-min(v.z for v in allpoints)))
for ob in parts:
    for v in ob.data.vertices:v.co+=shift
bpy.context.view_layer.update()
# Stable origin at the horizontal center of the intended footprint. Root stays identity.
source=audit_source(collection,P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene['asset_license']='CC-BY-4.0'
bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene['generator_revision']=P['revision']
# Clear default UI path buffers before creating the portable source, including stale bytes.
for scene in bpy.data.scenes:
    scene.render.filepath='.'*1023
    scene.render.filepath='//renders/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'.'*1023
                space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
# Consolidate the static export only. Editable semantic source parts remain in .blend.
verts=[];faces=[];indices=[]
for ob in parts:
    offset=len(verts);verts.extend([tuple(ob.matrix_world@v.co) for v in ob.data.vertices])
    for p in ob.data.polygons:faces.append(tuple(offset+i for i in p.vertices));indices.append(p.material_index)
for ob in parts:bpy.data.objects.remove(ob,do_unlink=True)
mesh('static-export-surface',verts,faces,indices)
bpy.ops.object.select_all(action='DESELECT')
for ob in collection.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available:raise RuntimeError('Unsupported exporter options')
bpy.ops.export_scene.gltf(**opts)
audit=audit_glb(out/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if audit['errors']:raise RuntimeError(audit['errors'])
audit['file']='model.glb'
lo=source['bounds_blender_m']['min'];hi=source['bounds_blender_m']['max']
expected={'min':[lo[0],lo[2],-hi[1]],'max':[hi[0],hi[2],-lo[1]]}
delta=max(abs(expected[s][i]-audit['bounds_m'][s][i]) for s in ['min','max'] for i in range(3))
if delta>1e-4 or source['triangles']!=audit['scene_triangles']:raise RuntimeError('Source/export metrics mismatch')
if audit['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
report={'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':audit,'source_export_bounds_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'semantic_source_parts':len(parts)-1,'skin_colour_and_pose':'artistic reconstruction; no fossil skin or colour claimed','runtime_gpu':'UNKNOWN','populated_scene':'UNKNOWN'}
(out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('ALI0RAMUS_BUILD_COMPLETE',audit['sha256'],audit['scene_triangles'],audit['bytes'])
