# SPDX-License-Identifier: MIT
"""Original Platybelodon grangeri living reconstruction, adult male r001.

Run with Blender --background --threads 2 --python source/generate.py --
--output-dir . . The adjacent params.json and deps directory are the only
non-runtime dependencies. No reference images or external geometry are loaded.
"""
import sys, json, math, hashlib, argparse
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb, read_glb, semantic_digest

P = json.loads((HERE/'params.json').read_text())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,j): Path(p).write_text(json.dumps(j,indent=2,sort_keys=True,allow_nan=False)+'\n')

# Cubic profile interpolation: contours are authored stations, not primitives.
def curve(points, per=3):
    out=[]
    for i in range(len(points)-1):
        a,b,c,d=points[max(0,i-1)],points[i],points[i+1],points[min(len(points)-1,i+2)]
        for k in range(per):
            t=k/per
            out.append(tuple(.5*((2*b[j])+(-a[j]+c[j])*t+(2*a[j]-5*b[j]+4*c[j]-d[j])*t*t+(-a[j]+3*b[j]-3*c[j]+d[j])*t*t*t) for j in range(len(b))))
    return out+[points[-1]]

def rings_mesh(name,rings,mat,close=True):
    n=len(rings[0]); v=[tuple(p) for row in rings for p in row]; f=[]
    for i in range(len(rings)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;c=(i+1)*n+(j+1)%n;d=(i+1)*n+j
            # Quads preserve deliberately broad surface planes after triangulation.
            f.append((a,b,c,d))
    if close:
        f += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))]
    return mesh_object(name,v,f,mat,C)

def length_loft(name, stations, mat, n=28, per=2, exponent=.9):
    rings=[]
    for y,w,bot,top in curve(stations,per):
        z=(bot+top)/2; rz=(top-bot)/2
        ring=[]
        for j in range(n):
            t=2*math.pi*j/n;c=math.cos(t);s=math.sin(t)
            ring.append((w*math.copysign(abs(c)**exponent,c),y,z+rz*math.copysign(abs(s)**exponent,s)))
        rings.append(ring)
    return rings_mesh(name,rings,mat)

def sweep(name, controls,mat,n=14,per=3,flatten=1):
    rows=curve(controls,per); rings=[]
    for i,row in enumerate(rows):
        center=Vector(row[:3]);r=row[3]
        tangent=(Vector(rows[min(i+1,len(rows)-1)][:3])-Vector(rows[max(i-1,0)][:3])).normalized()
        seed=Vector((1,0,0))
        if abs(tangent.dot(seed))>.92:seed=Vector((0,1,0))
        u=(seed-tangent*seed.dot(tangent)).normalized();v=tangent.cross(u).normalized()
        rings.append([center+r*(math.cos(2*math.pi*j/n)*u+flatten*math.sin(2*math.pi*j/n)*v) for j in range(n)])
    return rings_mesh(name,rings,mat)

def leg(name,x,cy,front=True):
    # Wide proximal limb disappears inside shoulder/hip, then knee, carpus,
    # broad heel and flat weight-bearing sole. No ball-joint primitives.
    profile=[(0,.235,.255,-.035),(.055,.25,.275,-.05),(.16,.245,.26,-.045),(.30,.197,.205,0),(.48,.178,.179,.02),(.67,.189,.19,.02),(.89,.205,.218,-.015),(1.09,.25,.26,-.025),(1.30,.30,.31,-.005),(1.50,.32,.34,.02),(1.70,.26,.30,.04),(1.80,.16,.18,.04)]
    if not front:profile=[(z,rx*(1.03 if z>.8 else .94),ry,dy+(.11*math.sin(z*2) if z>.3 else 0)) for z,rx,ry,dy in profile]
    rings=[]
    for z,rx,ry,dy in curve(profile,2):
        xc=x*(1-.26*max(0,min(1,(z-1.0)/.65)))
        rings.append([(xc+rx*math.cos(2*math.pi*j/16),cy+dy+ry*math.sin(2*math.pi*j/16),max(0,z)) for j in range(16)])
    return rings_mesh(name,rings,M['skin'])

def join_objects(name,objects):
    if not objects:return
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.join();o=bpy.context.object;o.name=name;o.data.name=name+'-mesh'
    return o

def ear(side):
    # Hand-drawn fan outline, rounded edge thickness and recessed inner bowl.
    outline=[(-1.29,2.12),(-1.12,2.15),(-.99,2.08),(-.95,1.95),(-.98,1.80),(-1.08,1.66),(-1.20,1.65),(-1.32,1.74),(-1.37,1.88),(-1.36,2.02)]
    center=Vector((side*.485,-1.19,1.91)); v=[]
    # Concentric front rings curve toward head at the root.
    for scale,xx in [(1,.55),(.83,.61),(.49,.635),(.13,.63)]:
        for y,z in outline:
            v.append((side*(xx+(.035 if y> -1.1 else -.03)),center.y+(y-center.y)*scale,center.z+(z-center.z)*scale))
    for y,z in outline:v.append((side*.505,y,z))
    n=len(outline);f=[];materials=[]
    for i in range(3):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j));materials.append(0 if i==0 else 1)
    f.append(tuple(3*n+j for j in range(n)));materials.append(1)
    for j in range(n):f.append((j,4*n+j,4*n+(j+1)%n,(j+1)%n));materials.append(0)
    f.append(tuple(4*n+j for j in range(n)));materials.append(0)
    o=mesh_object('ear-right' if side>0 else 'ear-left',v,f,[M['skin'],M['ear_inner']],C)
    for p,mi in zip(o.data.polygons,materials):p.material_index=mi
    return o

def blade(side):
    # Each blade is an independent closed shallow cutting tusk. An open median
    # seam persists along the full exposed edge; neither blade is a cone.
    sections=[(-2.60,.016,.205,1.015,.055),(-2.73,.009,.244,1.003,.052),(-2.89,.008,.270,.997,.046),(-3.06,.008,.279,1.007,.034),(-3.20,.009,.270,1.034,.012)]
    rings=[]
    for y,inner,outer,z,th in curve(sections,2):
        width=outer-inner
        # Cross-section follows shallow concave upper face, convex lower face,
        # and bevelled lateral/medial edges; ring sweeps along the mandible.
        xz=[(inner,z+.012),(inner+.1*width,z+.024),(inner+.45*width,z+.012),(outer-.1*width,z+.028),(outer,z+.018),(outer-.012,z-th),(inner+.15*width,z-th-.006),(inner,z-th*.65)]
        rings.append([(side*x,y,zz) for x,zz in xz])
    return rings_mesh('lower-tusk-right' if side>0 else 'lower-tusk-left',rings,M['ivory'])

def cheek_surface_x(y,z,side):
    """Intersect the real authored cheek along X, not an estimated head radius."""
    body=bpy.data.objects['body-cranium-rostrum']
    bpy.context.view_layer.update()
    ok,point,normal,index=body.ray_cast(Vector((side*2,y,z)),Vector((-side,0,0)))
    if not ok:raise RuntimeError('Eye or brow lies outside the cheek profile')
    return abs(point.x)

def details():
    eyes=[];lids=[];nails=[]
    for s in [-1,1]:
        # A restrained almond cap follows the actual faceted cheek. Its back
        # pole penetrates the skin; the cap projects only nine millimetres.
        cy,cz=-1.81,1.965
        v=[(s*(cheek_surface_x(cy,cz,s)+.009),cy,cz)]
        for j in range(12):
            a=2*math.pi*j/12;y=cy+.049*math.cos(a);z=cz+.026*math.sin(a)
            v.append((s*(cheek_surface_x(y,z,s)+.0008),y,z))
        v.append((s*(cheek_surface_x(cy,cz,s)-.018),cy,cz));f=[]
        for j in range(12):f.extend([(0,1+j,1+(j+1) % 12),(13,1+(j+1) % 12,1+j)])
        eyes.append(mesh_object('eye',v,f,M['eye'],C))
        # Sweep a small brow in the YZ plane, then wrap every vertex onto the
        # cheek. A six-millimetre inset gives the entire ridge a rooted base.
        brow=sweep('brow',[(0,-1.862,1.965,.012),(0,-1.83,1.992,.018),(0,-1.785,1.992,.016),(0,-1.757,1.968,.008)],M['skin_shadow'],n=8,per=2)
        for vert in brow.data.vertices:
            yy,zz=vert.co.y,vert.co.z
            vert.co.x=s*(cheek_surface_x(yy,zz,s)+vert.co.x-.006)
        bm=bmesh.new();bm.from_mesh(brow.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(brow.data);bm.free();brow.data.update()
        lids.append(brow)
    for x,y in FOOT_CENTERS:
        # Three small rounded nail plates per visible front of each foot.
        for dx in [-.125,0,.125]:
            cy=y-.263+abs(dx)*.17;cx=x+dx
            rings=[]
            for z,rx,ry in [(.025,.043,.015),(.043,.055,.023),(.105,.048,.024),(.14,.027,.015)]:
                rings.append([(cx+rx*math.cos(2*math.pi*j/8),cy+ry*math.sin(2*math.pi*j/8),z) for j in range(8)])
            nails.append(rings_mesh('nail',rings,M['nails']))
    join_objects('eyes-pair',eyes);join_objects('brow-pair',lids);join_objects('nails-four-feet',nails)

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE.parent);a=ap.parse_args(argv)
OUT=a.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True);(OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
C=setup_scene('platybelodon',P['seed']);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
M={k:make_material(k,v,P['roughness'].get(k,.88)) for k,v in P['palette_srgb'].items()}
# Top/belly profiles integrate pelvis, barrel, shoulder, nape, cheek and rostrum.
body=[(1.46,.06,1.65,1.80),(1.38,.28,1.38,2.03),(1.16,.49,1.12,2.17),(.84,.60,.99,2.22),(.45,.65,.94,2.25),(0,.67,.925,2.27),(-.42,.65,.96,2.30),(-.78,.60,1.02,2.31),(-1.06,.50,1.18,2.28),(-1.27,.395,1.38,2.25),(-1.48,.36,1.44,2.22),(-1.68,.34,1.43,2.15),(-1.88,.29,1.47,2.04),(-2.07,.225,1.53,1.92),(-2.20,.14,1.58,1.80),(-2.24,.065,1.63,1.73)]
length_loft('body-cranium-rostrum',body,M['skin'],n=32,per=2)
FOOT_CENTERS=[(-.44,-.93),(.44,-.77),(-.43,.81),(.43,.89)]
for i,(x,y) in enumerate(FOOT_CENTERS):leg(('fore' if i<2 else 'hind')+('-left' if x<0 else '-right'),x,y,i<2)
for s in [-1,1]:ear(s)
# Deep posterior mandible becomes a constricted long waist and a shallow dish.
length_loft('mandible-waist-and-platform',[(-1.40,.235,1.26,1.62),(-1.55,.292,1.18,1.57),(-1.76,.270,1.12,1.44),(-1.99,.205,1.045,1.25),(-2.16,.157,1.005,1.12),(-2.32,.141,.977,1.075),(-2.48,.180,.950,1.055),(-2.64,.231,.941,1.052),(-2.78,.261,.952,1.052)],M['skin'],n=20,per=3,exponent=.72)
for s in [-1,1]:
    blade(s)
    sweep('upper-tusk-right' if s>0 else 'upper-tusk-left',[(s*.173,-2.05,1.65,.083),(s*.205,-2.22,1.54,.078),(s*.239,-2.43,1.39,.065),(s*.267,-2.64,1.25,.048),(s*.282,-2.82,1.165,.026),(s*.285,-2.91,1.145,.0035)],M['ivory'],n=14,per=3)
# Gently lifted, right-offset flexible trunk, separate from all four tusks.
sweep('flexible-trunk',[(0,-1.86,1.84,.180),(.008,-2.08,1.84,.188),(.024,-2.25,1.78,.179),(.045,-2.41,1.64,.161),(.10,-2.58,1.48,.137),(.19,-2.79,1.43,.111),(.29,-2.94,1.52,.088),(.345,-2.96,1.71,.068),(.350,-2.89,1.88,.053),(.335,-2.81,1.95,.045)],M['skin'],n=16,per=4)
sweep('tail',[(0,1.37,1.84,.067),(.025,1.55,1.62,.055),(.055,1.65,1.35,.043),(.10,1.71,1.09,.030),(.13,1.69,.91,.020)],M['skin_shadow'],n=10,per=4)
sweep('tail-tuft',[(.12,1.69,.98,.025),(.14,1.68,.89,.055),(.15,1.65,.77,.018)],M['skin_shadow'],n=10,per=3)
# Keep tail one semantic part while retaining editable disconnected tuft geometry.
join_objects('tail-and-tuft',[bpy.data.objects['tail'],bpy.data.objects['tail-tuft']])
details()
# Public source scene records only portable identifiers and biological caveats.
scene['generator']='source/generate.py';scene['parameters']='source/params.json';scene['revision']='r001';scene['representation']='living-reconstruction'
scene['scientific_limits']='Head informed by HMV0940; soft anatomy, palette, pose and body scale are artistic.'
source=audit_source(C,max_triangles=P['geometry_targets']['hard_max_triangles'])
if source['errors']:raise RuntimeError(repr(source['errors']))
bpy.context.preferences.filepaths.save_version=0
# Reset factory file-browser and render-output history before saving portable DNA.
scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'.'*1023
                space.params.directory=b'//'
# The output argument is runtime-only, never an authored resource dependency.
import os
os.chdir(OUT)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),relative_remap=True)
bpy.ops.object.select_all(action='DESELECT')
for obj in C.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['platybelodon']
options=dict(filepath='model.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Unsupported explicit exporter options')
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(Path('model.glb'),max_triangles=12000,max_materials=7,max_primitives=24)
if glb['errors']:raise RuntimeError(repr(glb['errors']))
assert glb['bytes']<=2097152
assert source['triangles']==glb['scene_triangles']
b=source['bounds_blender_m'];expected_min=[b['min'][0],b['min'][2],-b['max'][1]];expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
assert delta<.0001
# Face normals and each closed semantic component were inspected numerically.
volumes=[]
for obj in C.all_objects:
    if obj.type=='MESH':
        bm=bmesh.new();bm.from_mesh(obj.data);volumes.append({'name':obj.name,'signed_volume_m3':bm.calc_volume(signed=True)});bm.free()
write(OUT/'qa/evidence/source-geometry.json',{'status':'PASS','glb_sha256':sha(OUT/'model.glb'),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'source':source,'signed_part_volumes':volumes,'source_export_bounds_max_error_m':delta,'feet_contact_z_m':[0,0,0,0],'foot_contact_centers_blender_m':[[x,y,0] for x,y in FOOT_CENTERS],'footprint_center_blender_m':[0,0,0],'warning_review':'All source faces intentionally faceted; closed positive-volume parts. Semantic anatomical parts overlap at their attachment roots; no watertight union is claimed.'})
write(OUT/'qa/evidence/glb-audit.json',glb)
write(OUT/'qa/evidence/build.json',{'status':'BUILT_NOT_INDEPENDENTLY_ACCEPTED','asset_id':'platybelodon','revision':'r001','seed':P['seed'],'blender_version':bpy.app.version_string,'blender_build_hash':bpy.app.build_hash.decode(),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'export_options':{k:v for k,v in options.items() if k!='filepath'},'exporter_options_probed':True,'target_threejs_version':'0.180.0','threejs_gpu':'UNKNOWN','populated_scene':'UNKNOWN','semantic_digest':glb.get('semantic_sha256'),'privacy_note':'No source image, external mesh, texture, animation or private task locator is embedded.'})
print('CANDIDATE_BUILT',glb['scene_triangles'],glb['scene_primitives_estimated_base_draw_calls'],glb['bytes'],sha(OUT/'model.glb'))
