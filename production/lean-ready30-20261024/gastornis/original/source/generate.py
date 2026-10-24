#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic, original Diatryma gigantea reconstruction. Run in Blender.

Usage: blender --background --threads 2 --python source/generate.py -- --output .
References are consulted, never embedded. All bundled dependencies are relative.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import shutil
import sys
import bpy
from mathutils import Vector

SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE / 'deps'))
import asset_common as common

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='.')
opt = parser.parse_args(args)
OUT = Path(opt.output).resolve()
OUT.mkdir(parents=True, exist_ok=True)
P = json.loads((SOURCE / 'params.json').read_text())
C = common.setup_scene(P['asset_id'], P['seed'])
bpy.context.scene.render.threads_mode = 'FIXED'
bpy.context.scene.render.threads = 2
M = {k: common.make_material(k, v, roughness=.86 if k != 'eye_nail' else .76)
     for k, v in P['palette_srgb'].items()}


def combine(items):
    verts, faces = [], []
    for v, f in items:
        offset = len(verts)
        verts.extend(v)
        faces.extend(tuple(i + offset for i in face) for face in f)
    return verts, faces


def closed_rings(rings):
    """Closed ordered section mesh, with noncollapsed end caps."""
    n = len(rings[0])
    verts = [v for ring in rings for v in ring]
    faces = []
    for j in range(len(rings) - 1):
        for i in range(n):
            k = (i + 1) % n
            faces.append((j*n+i, j*n+k, (j+1)*n+k, (j+1)*n+i))
    faces.extend([tuple(reversed(range(n))), tuple((len(rings)-1)*n+i for i in range(n))])
    return verts, faces


def make(name, data, material, smooth=False):
    obj = common.mesh_object(name, *data, material, C)
    if smooth:
        for f in obj.data.polygons:
            f.use_smooth = True
    return obj


def zloft(stations, n=28, shift=0):
    # z, y center, lateral radius, fore-aft radius, lateral center
    rings = []
    for j, (z, y, rx, ry, x) in enumerate(stations):
        ring=[]
        for i in range(n):
            a=2*math.pi*(i+shift)/n
            ring.append((x+rx*math.cos(a), y+ry*math.sin(a), z))
        rings.append(ring)
    return closed_rings(rings)


def tube(stations, n=12):
    """Anatomical sweep: (x,y,z,lateral_radius,other_radius)."""
    rings=[]
    for j, p in enumerate(stations):
        center=Vector(p[:3])
        prev=Vector(stations[max(j-1,0)][:3])
        nex=Vector(stations[min(j+1,len(stations)-1)][:3])
        axis=(nex-prev).normalized()
        u=Vector((1,0,0))
        if abs(axis.dot(u))>.85: u=Vector((0,1,0))
        u=(u-axis*axis.dot(u)).normalized()
        v=axis.cross(u).normalized()
        rings.append([tuple(center+u*(p[3]*math.cos(2*math.pi*i/n))+v*(p[4]*math.sin(2*math.pi*i/n))) for i in range(n)])
    return closed_rings(rings)


def ellipsoid(c, r, n=16, sections=8):
    rings=[]
    for j in range(sections+1):
        a=math.pi*(.025+.95*j/sections)
        rings.append([(c[0]+r[0]*math.sin(a)*math.cos(2*math.pi*i/n),
                       c[1]+r[1]*math.sin(a)*math.sin(2*math.pi*i/n),
                       c[2]+r[2]*math.cos(a)) for i in range(n)])
    return closed_rings(rings)

# One authored, uninterrupted primary surface from belly to crown. Cross sections
# carry the deep torso, thick curved neck, jaw support and large cranial profile.
body_sections=[
(.650,.075,.090,.120,0),(.690,.072,.166,.230,0),(.740,.067,.226,.303,0),
(.800,.060,.278,.363,.003),(.870,.047,.317,.412,.005),(.945,.025,.339,.448,.007),
(1.020,.008,.350,.465,.008),(1.095,-.010,.344,.460,.007),(1.165,-.031,.321,.430,.005),
(1.230,-.061,.290,.388,.003),(1.290,-.105,.252,.327,0),(1.345,-.155,.210,.275,0),
(1.395,-.217,.177,.223,-.003),(1.445,-.274,.151,.181,-.004),
(1.495,-.319,.134,.152,-.004),(1.545,-.348,.124,.133,-.003),
(1.595,-.362,.121,.124,-.002),(1.645,-.364,.123,.124,0),
(1.690,-.366,.128,.132,0),(1.730,-.380,.136,.144,0),
(1.770,-.407,.145,.158,0),(1.810,-.432,.148,.178,0),
(1.850,-.446,.147,.184,0),(1.890,-.445,.137,.179,0),
(1.925,-.433,.119,.162,0),(1.955,-.420,.092,.133,0),
(1.980,-.408,.058,.090,0),(1.994,-.400,.025,.043,0),(2.000,-.398,.006,.010,0)]
body=make('continuous-plumage-body-neck-head', zloft(body_sections,32),
          [M['plumage_main'],M['neck_head'],M['plumage_light']])
for poly in body.data.polygons:
    z=poly.center.z
    # Mesh centers are updated after construction. Broad material areas follow
    # anatomy, not random polygon noise; the head and neck have gentler normals.
    points=[body.data.vertices[i].co for i in poly.vertices]
    z=sum(p.z for p in points)/len(points)
    y=sum(p.y for p in points)/len(points)
    x=sum(p.x for p in points)/len(points)
    poly.material_index = 1 if z>1.39 else (2 if y<-.25 and z<1.22 and abs(x)<.23 else 0)
    poly.use_smooth = z>1.37

# Paired feathered thighs connect the torso to the true angular lower-limb chain.
for s, label, advance in [(-1,'left',.035),(1,'right',-.035)]:
    thigh=make(label+'-feathered-thigh',tube([
        (s*.216,.028+advance,1.050,.113,.137),
        (s*.229,-.015+advance,.965,.122,.140),
        (s*.229,-.038+advance,.870,.112,.125),
        (s*.214,-.030+advance,.780,.091,.099),
        (s*.198,.002+advance,.710,.068,.073),
        (s*.189,.027+advance,.676,.049,.057)],16),M['plumage_main'])
    leg=make(label+'-tibiotarsus-hock-tarsometatarsus',tube([
        (s*.190,.025+advance,.740,.052,.056),
        (s*.187,.050+advance,.657,.049,.048),
        (s*.180,.077+advance,.555,.044,.043),
        (s*.174,.102+advance,.440,.040,.039),
        (s*.172,.116+advance,.370,.047,.048),
        (s*.172,.107+advance,.332,.047,.050),
        (s*.171,.083+advance,.296,.036,.035),
        (s*.170,.050+advance,.220,.030,.032),
        (s*.170,.013+advance,.140,.031,.032),
        (s*.170,-.014+advance,.088,.050,.036),
        (s*.170,-.025+advance,.062,.052,.029)],14),M['legs_toes'])
    toes=[]; nails=[]
    # Three broad plantigrade digits and a much smaller posterior hallux.
    for side,length,spread in [(-1,.235,-.106),(0,.295,.006),(1,.224,.108)]:
        x0=s*.170+side*.030; y0=-.025+advance
        x1=s*.170+spread; endy=y0-length
        points=[(x0,y0,.063,.027,.025),
                (x0+spread*.22,y0-length*.24,.051,.029,.026),
                (x0+(x1-x0)*.66,y0-length*.58,.035,.025,.025),
                (x1,endy+.033,.026,.018,.023),
                (x1,endy,.021,.011,.019)]
        toes.append(tube(points,12))
        nails.append(tube([(x1,endy+.010,.026,.012,.012),
                           (x1,endy-.014,.020,.011,.012),
                           (x1,endy-.030,.014,.006,.008),
                           (x1,endy-.035,.012,.0025,.0035)],10))
    toes.append(tube([(s*.166,.003+advance,.083,.024,.022),
                      (s*.153,.047+advance,.061,.020,.018),
                      (s*.145,.095+advance,.034,.015,.017),
                      (s*.140,.119+advance,.023,.009,.013)],12))
    nails.append(tube([(s*.142,.110+advance,.025,.010,.010),
                       (s*.137,.134+advance,.018,.007,.009),
                       (s*.135,.142+advance,.015,.002,.003)],10))
    make(label+'-three-forward-toes-and-small-hallux',combine(toes),M['legs_toes'])
    make(label+'-restrained-rounded-nails',combine(nails),M['eye_nail'],True)

# Original deep, laterally compressed, blunt beak. Each y section is an oval
# following separately authored culmen and tomial/basal profiles, not a cone.
def bill(sections, n=20, dome=None):
    rings=[]
    for y, width, top, bottom in sections:
        mid=(top+bottom)/2; rz=(top-bottom)/2
        if dome is None:
            rings.append([(width*math.cos(2*math.pi*i/n),y,mid+rz*math.sin(2*math.pi*i/n)) for i in range(n)])
        else:
            rings.append([(width*math.cos(math.pi*i/(n-1)),y,
                bottom+(top-bottom)*math.sin(math.pi*i/(n-1)) if dome=='upper' else
                top-(top-bottom)*math.sin(math.pi*i/(n-1))) for i in range(n)])
    return closed_rings(rings)
upper=[(-.532,.074,1.951,1.770),(-.558,.082,1.967,1.768),
       (-.588,.083,1.969,1.765),(-.622,.081,1.966,1.763),
       (-.656,.077,1.957,1.760),(-.690,.070,1.941,1.757),
       (-.722,.061,1.920,1.755),(-.752,.051,1.893,1.752),
       (-.778,.040,1.863,1.749),(-.799,.029,1.832,1.747),
       (-.813,.020,1.803,1.745),(-.820,.012,1.778,1.746),
       (-.822,.006,1.761,1.749)]
lower=[(-.538,.073,1.765,1.674),(-.572,.078,1.762,1.668),
       (-.607,.077,1.760,1.670),(-.642,.073,1.758,1.676),
       (-.678,.065,1.756,1.687),(-.711,.056,1.753,1.700),
       (-.744,.045,1.750,1.714),(-.774,.033,1.747,1.728),
       (-.798,.021,1.745,1.738),(-.815,.009,1.744,1.741)]
make('deep-rounded-culmen-upper-beak',bill(upper,dome='upper'),M['beak'],True)
make('closed-narrow-symphysis-lower-beak',bill(lower,dome='lower'),M['beak'],True)
seam=[(y,w*.985, bot+.001, bot-.0045) for y,w,top,bot in upper[1:-2]]
make('subtle-closed-tomial-seam',bill(seam,12),M['eye_nail'],True)

# Embedded small eyes, restrained orbital feather rims and tiny nares.
rims=[]; eyes=[]; nares=[]
for s in (-1,1):
    rims.append(ellipsoid((s*.132,-.470,1.881),(.017,.034,.030),20,8))
    eyes.append(ellipsoid((s*.145,-.478,1.884),(.007,.018,.017),20,8))
    nares.append(ellipsoid((s*.080,-.614,1.908),(.0026,.012,.0050),12,6))
make('paired-subtle-orbital-feather-rims',combine(rims),M['plumage_shadow'],True)
make('paired-inset-eyes',combine(eyes),M['eye_nail'],True)
make('paired-small-nares',combine(nares),M['plumage_shadow'],True)

# Tiny tucked wings: broad shoulder blending into a short trailing teardrop.
# Feather scallops are quiet contour turns, never spikes or flight-feather fans.
for s,label in [(-1,'left'),(1,'right')]:
    wing_sections=[
        (.030,1.218,.261,.008,.025),(.067,1.204,.285,.018,.053),
        (.114,1.177,.305,.026,.073),(.162,1.144,.315,.028,.078),
        (.208,1.110,.309,.025,.071),(.247,1.081,.294,.021,.055),
        (.279,1.055,.277,.016,.040),(.301,1.038,.251,.006,.013)]
    rings=[]
    for y,z,x,rx,rz in wing_sections:
        rings.append([(s*(x+rx*math.cos(2*math.pi*i/16)),y,z+rz*math.sin(2*math.pi*i/16)) for i in range(16)])
    wing=make(label+'-tiny-tucked-wing',closed_rings(rings),[M['plumage_shadow'],M['plumage_main']])
    for f in wing.data.polygons:
        f.material_index=1 if sum(wing.data.vertices[i].co.z for i in f.vertices)/len(f.vertices)>1.17 else 0

# A short, tapered feather wedge, with a gentle three-lobed distal edge.
rings=[]
for y,z,rx,rz in [(.355,1.160,.182,.101),(.426,1.153,.169,.092),
                   (.498,1.129,.139,.077),(.563,1.098,.109,.061),
                   (.620,1.062,.077,.044),(.666,1.034,.035,.024),
                   (.680,1.023,.010,.010)]:
    rings.append([(rx*math.cos(2*math.pi*i/20),y,z+rz*math.sin(2*math.pi*i/20)) for i in range(20)])
make('short-restrained-tail-wedge',closed_rings(rings),M['plumage_shadow'])

# Preserve the numerical floor origin: toe sections are authored to contact Z=0.
shift=common.ground_asset(C,center_xy=False)
root=bpy.data.objects[P['asset_id']]
root['scientific_subject']='Diatryma gigantea'
root['taxonomy_note']='Historical Gastornis catalog usage; Diatryma distinction follows Mayr et al. (2024).'
root['reconstruction_limits']='Artistic plumage, color, soft tissue and pose; approximate two-metre taxon scale.'
root['representation']='living-reconstruction'

# Probe required exporter flags in the running Blender before calling the pinned
# canonical export helper. Helper outputs are retained as private build evidence.
required=['export_format','use_selection','export_yup','export_apply','export_normals',
          'export_texcoords','export_tangents','export_materials','export_vertex_color',
          'export_animations','export_skins','export_morph','export_cameras','export_lights',
          'export_extras','export_gpu_instances','export_gn_mesh',
          'export_draco_mesh_compression_enable','export_use_gltfpack']
rna={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
assert set(required)<=rna, 'Required exporter RNA options unavailable'
import io_scene_gltf2
# Remove default UI/render machine-local locations before source serialization.
bpy.context.scene.render.filepath='//render/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params is not None:
                space.params.directory=b'//'
                space.params.filename=''
export_dir=OUT/'private'/'build'
record=common.export_asset(P['asset_id'],{'en':'Gastornis (Diatryma gigantea)','zh':'加斯顿鸟（Diatryma gigantea）'},
    'animals',C,metadata={'generator':'source/generate.py','description':{'en':'Original quiet-standing Diatryma gigantea living reconstruction under historical Gastornis catalog usage.','zh':'历史Gastornis目录用法下，安静站立的Diatryma gigantea原创生命复原。'}},
    output_root=export_dir,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=32)
built=export_dir/P['asset_id']
shutil.copyfile(built/(P['asset_id']+'.glb'),OUT/'model.glb')
shutil.copyfile(built/(P['asset_id']+'.blend'),OUT/'model.blend')
evidence=OUT/'qa'/'evidence'; evidence.mkdir(parents=True,exist_ok=True)
qa=json.loads((built/'qa.json').read_text())
qa['glb']['file']='model.glb'  # public evidence names the delivered relative member
(evidence/'source-export-audit.json').write_text(json.dumps(qa,indent=2)+'\n')
pin={'blender':bpy.app.version_string,'exporter':getattr(io_scene_gltf2,'bl_info',{}).get('version'),
     'seed':P['seed'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'params_sha256':hashlib.sha256((SOURCE/'params.json').read_bytes()).hexdigest(),
     'required_rna_options_present':required,'export_options':record['export_options'],
     'ground_shift_m':shift,'rendering_in_generator':False,'geometry_source':'original custom section meshes',
     'threejs_consumer_version':'0.180.0','threejs_gpu_test':'NOT_RUN',
     'source_blend_has_presentation_objects':False,
     'source_files':['source/generate.py','source/params.json','source/dependencies.json']}
(evidence/'build-runtime.json').write_text(json.dumps(pin,indent=2)+'\n')
print('BUILD_COMPLETE',json.dumps({'triangles':record['triangles'],'glb_bytes':record['glb_bytes'],'dimensions':record['dimensions'],'glb_sha256':record['sha256']['glb']}))
