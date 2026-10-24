# SPDX-License-Identifier: MIT
"""Original Ilingoceros reconstruction. Run with Blender and -- --output OUTPUT.
Only sibling parameters and declared relative dependencies are required.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE / 'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True)
args = p.parse_args(argv)
out = args.output.resolve(); out.mkdir(parents=True, exist_ok=True)
config = json.loads((SOURCE / 'params.json').read_text())
collection = setup_scene(config['asset_id'], config['seed'])
root = bpy.data.objects[collection['asset_root']]
root['representation'] = 'living-reconstruction'
root['anatomy_note'] = 'Composite inferred body and keratin tips; separate fragment evidence, not a complete fossil individual.'
materials = {k: make_material(k, '#' + v, roughness=0.88) for k,v in config['palette_srgb'].items()}
coat, belly = materials['coat'], materials['underside']

# One explicit surface for the rump, torso, rising neck, head and all four limbs.
# The limb-root holes are replaced by shared-vertex branch loops, not overlapped spheres.
# Stations: longitudinal center Y, center Z, lateral radius, sagittal radius,
# sagittal ring basis Y/Z. The latter follows the bent spine deliberately.
stations = [
 (.575,.795,.035,.082,0,1),(.55,.80,.105,.145,0,1),
 (.50,.805,.15,.19,0,1),(.43,.80,.17,.205,0,1),(.36,.79,.175,.21,0,1),
 (.27,.80,.151,.172,0,1),(.14,.795,.161,.185,0,1),(0,.795,.165,.20,0,1),
 (-.14,.80,.16,.20,0,1),(-.28,.805,.164,.21,0,1),(-.35,.81,.165,.205,0,1),
 (-.42,.825,.15,.19,.1,.995),(-.485,.87,.125,.167,.32,.947),
 (-.53,.95,.102,.145,.57,.822),(-.565,1.035,.086,.135,.70,.714),
 (-.602,1.115,.076,.118,.70,.714),(-.645,1.195,.073,.10,.55,.835),
 (-.68,1.265,.078,.087,.38,.925),(-.715,1.312,.087,.082,0,1),
 (-.77,1.302,.087,.082,-.2,.98),(-.83,1.275,.067,.070,-.25,.968),
 (-.90,1.244,.051,.055,-.25,.968),(-.965,1.221,.043,.043,-.14,.990),
 (-1.003,1.217,.037,.035,0,1)]
N = 20
vertices=[]; faces=[]; face_material=[]
for y,z,rx,rz,vy,vz in stations:
    for j in range(N):
        a=2*math.pi*j/N
        vertices.append((rx*math.cos(a),y+rz*math.sin(a)*vy,z+rz*math.sin(a)*vz))
# Four 2x2 patches on the lower lateral torso become stitched upper limbs.
patches=[{'start':2,'j':17,'s':1,'kind':'hind','stagger':.055},
         {'start':2,'j':11,'s':-1,'kind':'hind','stagger':-.055},
         {'start':9,'j':17,'s':1,'kind':'fore','stagger':-.045},
         {'start':9,'j':11,'s':-1,'kind':'fore','stagger':.045}]
def f(indices, material=0): faces.append(tuple(indices)); face_material.append(material)
for i in range(len(stations)-1):
    for j in range(N):
        if any(q['start']<=i<q['start']+2 and q['j']<=j<q['j']+2 for q in patches): continue
        f((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j), 1 if 11<=j<=17 and i<12 else 0)
f(tuple(reversed(range(N))))
f(tuple((len(stations)-1)*N+j for j in range(N)))
foot_centers=[]
for q in patches:
    i,j,s,st=q['start'],q['j'],q['s'],q['stagger']
    boundary=[i*N+j,(i+1)*N+j,(i+2)*N+j,(i+2)*N+j+1,(i+2)*N+j+2,(i+1)*N+j+2,i*N+j+2,i*N+j+1]
    cx=sum(vertices[v][0] for v in boundary)/8; cy=sum(vertices[v][1] for v in boundary)/8
    # Preserve the root's continuous angular ordering while opening the lower limb.
    angles=[math.atan2((vertices[v][1]-cy)/.07,(vertices[v][0]-cx)/.035) for v in boundary]
    if q['kind']=='fore':
        points=[(.147,-.35,.635,.052,.062),(.158,-.325,.56,.038,.041),(.17,-.325,.50,.032,.034),
                (.17,-.36,.43,.025,.027),(.173,-.395,.32,.021,.023),(.174,-.422,.22,.018,.020),
                (.174,-.433,.155,.021,.023),(.174,-.445,.105,.020,.025),(.174,-.457,.070,.022,.027)]
    else:
        points=[(.158,.38,.64,.061,.070),(.17,.29,.575,.058,.057),(.174,.30,.52,.043,.044),
                (.176,.365,.445,.032,.035),(.18,.445,.37,.025,.029),(.18,.46,.325,.021,.025),
                (.18,.439,.235,.018,.022),(.18,.421,.150,.019,.023),(.18,.410,.095,.021,.025),(.18,.402,.070,.022,.027)]
    previous=boundary
    for x,y,z,rx,ry in points:
        current=[]
        for a in angles:
            current.append(len(vertices)); vertices.append((s*x+rx*math.cos(a),y+st+ry*math.sin(a),z))
        for k in range(8): f((previous[k],previous[(k+1)%8],current[(k+1)%8],current[k]))
        previous=current
    f(tuple(reversed(previous)))
    x,y,z,rx,ry=points[-1]; foot_centers.append((s*x,y+st))
body=mesh_object('Body_neck_head_and_stitched_limbs',vertices,faces,[coat,belly],collection)
for poly,mat in zip(body.data.polygons,face_material): poly.material_index=mat
body['topology_note']='Connected torso, neck, head and four legs; explicit eight-vertex stitched limb roots.'

# General hand-authored elliptical loft for small anatomical solids.
def loft(name, rings, material, count=12):
    vs=[]; fs=[]
    for c,u,v,ru,rv in rings:
        c,u,v=Vector(c),Vector(u),Vector(v)
        for k in range(count):
            a=2*math.pi*k/count; vs.append(tuple(c+u*ru*math.cos(a)+v*rv*math.sin(a)))
    for i in range(len(rings)-1):
        for k in range(count): fs.append((i*count+k,i*count+(k+1)%count,(i+1)*count+(k+1)%count,(i+1)*count+k))
    fs.extend([tuple(reversed(range(count))),tuple((len(rings)-1)*count+k for k in range(count))])
    return mesh_object(name,vs,fs,material,collection)

# Solid, nearly straight horn shafts with broad paired ridges rotated in each ring.
# Each terminal fork is part of the same manifold surface, with a shared internal divider.
for side,label in [(1,'R'),(-1,'L')]:
    vs=[]; fs=[]; count=24; rings=43
    direction=Vector((side*.10,.16,.98)).normalized()
    u=Vector((1,0,-direction.x/direction.z)).normalized(); v=direction.cross(u).normalized()
    base=Vector((side*.069,-.702,1.365)); length=.55
    for i in range(rings):
        t=i/(rings-1); center=base+direction*length*t
        phase=side*2*math.pi*1.4*t + .15
        radius=.0275*(1-.38*t)
        for k in range(count):
            a=2*math.pi*k/count
            r=radius*(1+.21*math.cos(2*(a-phase))+.055*math.cos(a-phase))
            vs.append(tuple(center+(u*math.cos(a)+v*math.sin(a))*r))
    fs.append(tuple(reversed(range(count))))
    for i in range(rings-1):
        for k in range(count): fs.append((i*count+k,i*count+(k+1)%count,(i+1)*count+(k+1)%count,(i+1)*count+k))
    start=(rings-1)*count; center=base+direction*length
    # Diameter is across the forward/back axis, so the two inferred tips split laterally.
    low=start+18; high=start+6
    mid=[]
    for t in [.75,.5,.25]: mid.append(len(vs)); vs.append(tuple(Vector(vs[low]).lerp(Vector(vs[high]),t)))
    arcs=[[start+(k%count) for k in range(18,31)]+mid,
          [start+k for k in range(6,19)]+list(reversed(mid))]
    for branch,arc in zip([1,-1],arcs):
        previous=arc; c0=sum((Vector(vs[idx]) for idx in arc),Vector())/len(arc)
        aa=[math.atan2((Vector(vs[idx])-c0).dot(v),(Vector(vs[idx])-c0).dot(u)) for idx in arc]
        for advance,spread,rad in [(.018,.012,.0095),(.038,.019,.0062),(.055,.026,.0032)]:
            c=center+direction*advance+u*branch*spread
            current=[]
            for a in aa: current.append(len(vs)); vs.append(tuple(c+(u*math.cos(a)+v*math.sin(a))*rad))
            for k in range(len(arc)): fs.append((previous[k],previous[(k+1)%len(arc)],current[(k+1)%len(arc)],current[k]))
            previous=current
        tip=len(vs); vs.append(tuple(center+direction*.066+u*branch*.029))
        for k in range(len(arc)): fs.append((previous[k],previous[(k+1)%len(arc)],tip))
    horn=mesh_object('Solid_twisted_horn_'+label,vs,fs,materials['horn'],collection)
    horn['evidence']='Broad torsion: I. alexandrae No.11880 and No.11886. Complete sheath, pairing and small terminal fork are inferred.'

# Ears are thick lens-shaped forms, lateral/posterior to the horn bases.
for s,label in [(1,'R'),(-1,'L')]:
    rings=[]
    for x,y,z,ry,rz in [(.08,-.663,1.308,.018,.025),(.13,-.638,1.335,.026,.047),(.19,-.611,1.367,.026,.050),(.24,-.587,1.389,.018,.034),(.27,-.574,1.403,.002,.003)]:
        rings.append(((s*x,y,z),(0,-1,0),(0,0,1),ry,rz))
    ear=loft('Ear_'+label,rings,[coat,materials['inner_ear']],count=12)
    for poly in ear.data.polygons:
        if poly.center.y < -.62: pass
        # Material per forward-facing middle panel, not a separate floating decal.
        if poly.normal.y<-.4: poly.material_index=1
    eye_rings=[]
    for x,ry,rz in [(.080,.010,.011),(.089,.016,.017),(.096,.013,.014),(.099,.004,.005)]:
        eye_rings.append(((s*x,-.782,1.316),(0,1,0),(0,0,1),ry,rz))
    loft('Eye_'+label,eye_rings,materials['eye'],count=12)

# Muzzle cap and fine lip are original geometry, with no asserted fossil markings.
loft('Nose', [((0,y,1.216),(1,0,0),(0,0,1),rx,rz) for y,rx,rz in [(-.993,.037,.032),(-1.011,.040,.030),(-1.022,.032,.024)]],materials['hoof_nose'],12)
for s,label in [(1,'R'),(-1,'L')]:
    loft('Mouth_line_'+label,[((s*x,y,z),(1,0,0),(0,0,1),.0018,.0024) for x,y,z in [(.047,-.917,1.210),(.041,-.966,1.199),(.031,-1.011,1.202)]],materials['hoof_nose'],6)

# Eight separately editable hoof toes; a real gap continues through each cloven front.
for idx,(x,y) in enumerate(foot_centers):
    for toe in [-1,1]:
        cx=x+toe*.016
        outline=[(-.010,-.039),(.010,-.039),(.014,-.026),(.014,.021),(.009,.030),(-.009,.030),(-.014,.021),(-.014,-.026)]
        vs=[]
        for z,scale,dy in [(0,1,0),(.012,1.04,0),(.052,.90,.006),(.075,.65,.010)]:
            for dx,yy in outline: vs.append((cx+dx*scale,y+yy*scale+dy,z))
        fs=[tuple(reversed(range(8)))]
        for j in range(3):
            for k in range(8): fs.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k))
        fs.append(tuple(24+k for k in range(8)))
        mesh_object('Hoof_%d_%s'%(idx,'outer' if toe>0 else 'inner'),vs,fs,materials['hoof_nose'],collection)

# Short, hanging tail, not an elongated deer or bovid tassel.
loft('Short_tail',[((0,y,z),(1,0,0),(0,-.7,.7),rx,rz) for y,z,rx,rz in [(.54,.86,.035,.035),(.594,.84,.029,.03),(.625,.795,.022,.026),(.635,.75,.010,.015),(.632,.73,.002,.003)]],coat,12)

# Center the actual four-hoof contact footprint while retaining the identity root.
contacts=[v.co.copy() for obj in collection.all_objects if obj.type=='MESH' and obj.name.startswith('Hoof_') for v in obj.data.vertices if abs(v.co.z)<1e-7]
shift=Vector((-(min(v.x for v in contacts)+max(v.x for v in contacts))/2,-(min(v.y for v in contacts)+max(v.y for v in contacts))/2,0))
for obj in collection.all_objects:
    if obj.type=='MESH':
        for vertex in obj.data.vertices: vertex.co+=shift
bpy.context.view_layer.update()
# Pin provenance with portable relative strings only.
scene=bpy.context.scene
scene['generator']='source/generate.py'; scene['parameter_file']='source/params.json'
scene['asset_license']='CC-BY-4.0'; scene['asset_author']='Leon Made This / s010s'
scene['scientific_scope']='Horn-core centered composite reconstruction; body, coat and keratin tips inferred.'
budget=config['budget']; source=audit_source(collection,budget['max_triangles'])
if source['errors']: raise RuntimeError(str(source['errors']))
bpy.context.preferences.filepaths.save_version=0
scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str((out/'model.blend').resolve()),relative_remap=True)
bpy.ops.object.select_all(action='DESELECT')
for obj in collection.all_objects: obj.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,
 export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
 export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={prop.identifier for prop in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available: raise RuntimeError('Missing exporter flags: '+repr(set(options)-available))
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
qa=audit_glb(out/'model.glb',budget['max_triangles'],budget['max_materials'],budget['max_primitives']); qa['file']='model.glb'
if qa['errors']: raise RuntimeError(str(qa['errors']))
if qa['bytes']>budget['max_glb_bytes']: raise RuntimeError('GLB bytes exceed frozen budget')
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(qa['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
if delta>1e-4 or source['triangles']!=qa['scene_triangles']: raise RuntimeError('Source/export geometry mismatch')
write(out/'qa/evidence/source-geometry.json',source)
write(out/'qa/evidence/glb-geometry.json',qa)
write(out/'qa/evidence/build.json',{'asset_id':config['asset_id'],'revision':config['revision'],'blender':bpy.app.version_string,
 'exporter':'4.3.47','viewer_pin':'three@0.180.0','viewer_test':'NOT_RUN','seed':config['seed'],
 'generator_sha256':digest(SOURCE/'generate.py'),'params_sha256':digest(SOURCE/'params.json'),
 'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),
 'export_options':options,'source_to_glb_max_bounds_error_m':delta,'source_to_glb_triangle_match':True,
 'geometry_profile':'Palette-only opaque static mesh; positive transforms; no textures, rig or animation.',
 'scope':'Local technical source/export checks only. No independent QA, browser GPU, populated-scene, user or deployment claim.'})
print('BUILD_COMPLETE',source['triangles'],qa['bytes'],digest(out/'model.glb'))
