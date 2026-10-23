#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Metamynodon living reconstruction. Run with Blender 4.3.2.

Example: blender --background --threads 2 --python source/generate.py -- --output .
The generator uses only params.json and the declared adjacent deps directory.
Source proportions are a generalized artistic composite, not a scanned specimen.
"""
import argparse, hashlib, json, math, os, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
C=setup_scene(P['asset_id'],P['seed'])
M={k:make_material(k,v,roughness=0.88) for k,v in P['palette_srgb'].items()}

def loft_y(name, rings, material, n=20):
    # Rings: y, center-z, half-width, half-height. End caps are explicit.
    vertices=[]
    for y,z,rx,rz in rings:
        for i in range(n):
            a=2*math.pi*i/n
            vertices.append((rx*math.cos(a),y,z+rz*math.sin(a)))
    faces=[]
    for j in range(len(rings)-1):
        for i in range(n): faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    faces.extend([tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))])
    return mesh_object(name,vertices,faces,material,C)

def tube(name, rings, material, n=12):
    # ring center xyz and lateral radii, section planes follow the path.
    vertices=[]
    for j,(co,rx,ry) in enumerate(rings):
        tangent=Vector(rings[min(j+1,len(rings)-1)][0])-Vector(rings[max(j-1,0)][0]);tangent.normalize()
        ref=Vector((1,0,0)) if abs(tangent.x)<0.9 else Vector((0,1,0))
        u=(ref-tangent*ref.dot(tangent)).normalized();v=tangent.cross(u).normalized()
        for i in range(n):
            a=2*math.pi*i/n;vertices.append(tuple(Vector(co)+u*rx*math.cos(a)+v*ry*math.sin(a)))
    faces=[tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))]
    for j in range(len(rings)-1):
        for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    return mesh_object(name,vertices,faces,material,C)

def ellipsoid(name, center, scale, material, n=12, rings=6):
    vs=[(center[0],center[1],center[2]-scale[2])]
    for j in range(1,rings):
        lat=-math.pi/2+math.pi*j/rings
        for i in range(n):
            a=2*math.pi*i/n
            vs.append((center[0]+scale[0]*math.cos(lat)*math.cos(a),center[1]+scale[1]*math.cos(lat)*math.sin(a),center[2]+scale[2]*math.sin(lat)))
    vs.append((center[0],center[1],center[2]+scale[2]));fs=[]
    for i in range(n):fs.append((0,1+(i+1)%n,1+i));fs.append((len(vs)-1,1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n))
    for j in range(rings-2):
        for i in range(n):fs.append((1+j*n+i,1+j*n+(i+1)%n,1+(j+1)*n+(i+1)%n,1+(j+1)*n+i))
    return mesh_object(name,vs,fs,material,C)

def merge_skin(parts):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.object.join();o=parts[0];o.name='Integrated_body_neck_head_limbs_tail'
    rem=o.modifiers.new('Anatomical union','REMESH');rem.mode='VOXEL';rem.voxel_size=P['skin_voxel_m'];rem.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=rem.name)
    sm=o.modifiers.new('Transition relaxation','SMOOTH');sm.factor=0.72;sm.iterations=3
    bpy.ops.object.modifier_apply(modifier=sm.name)
    de=o.modifiers.new('Deliberate low-poly skin','DECIMATE');de.ratio=P['skin_decimate_ratio'];de.use_collapse_triangulate=True
    bpy.ops.object.modifier_apply(modifier=de.name)
    o.data.shade_flat()
    return o

parts=[]
parts.append(loft_y('Long deep barrel torso',[
 (-.94,1.00,.20,.27),(-.77,.96,.40,.39),(-.50,.94,.53,.43),(-.14,.93,.58,.46),(.29,.94,.58,.45),(.67,.96,.51,.40),(.98,.94,.37,.33),(1.10,.92,.13,.23)],M['body'],24))
parts.append(loft_y('Substantial sloping neck',[
 (-.55,1.08,.34,.29),(-.81,1.14,.32,.30),(-1.02,1.25,.27,.27),(-1.25,1.32,.24,.24),(-1.40,1.33,.21,.22)],M['body'],20))
parts.append(loft_y('Broad zygomatic short-face skull envelope',[
 (-1.23,1.38,.14,.18),(-1.35,1.40,.23,.21),(-1.48,1.37,.28,.23),(-1.61,1.35,.26,.21),(-1.74,1.32,.19,.17),(-1.87,1.28,.195,.135),(-1.94,1.26,.165,.10)],M['body'],20))
# Each limb has muscular proximal mass, stout midshaft and a broad foot pad.
leg_layout=[('Fore_L',-.40,-.67,4),('Fore_R',.40,-.57,4),('Hind_L',-.40,.78,3),('Hind_R',.40,.86,3)]
for name,x,y,count in leg_layout:
    fore=name.startswith('Fore')
    parts.append(tube(name+' short stout limb',[
        ((x*.82,y,1.04),.215,.24),((x,y+(.02 if fore else -.02),.78),.19,.20),
        ((x,y+(.03 if fore else .09),.53),.135,.14),((x,y,.30),.115,.12),((x,y-.035,.135),.16,.17),((x,y-.045,.08),.17,.18)],M['body'],16))
parts.append(tube('Tapered tail',[
    ((0,1.01,1.12),.095,.095),((.02,1.20,1.06),.079,.073),((.04,1.37,.91),.057,.053),((.06,1.52,.75),.035,.033),((.065,1.58,.59),.012,.013)],M['body'],12))
body=merge_skin(parts)
# Shallow dark opening is bounded by modeled thick lips and a substantial jaw.
loft_y('Lower jaw thick lip',[
 (-1.34,1.19,.13,.10),(-1.48,1.11,.21,.10),(-1.64,1.08,.22,.085),(-1.82,1.075,.18,.075),(-1.94,1.09,.125,.045)],M['under'],16)
loft_y('Narrow mouth opening',[
 (-1.47,1.175,.16,.026),(-1.63,1.158,.213,.025),(-1.82,1.157,.175,.027),(-1.935,1.155,.13,.023)],M['detail'],16)
for s,label in [(-1,'L'),(1,'R')]:
    # High-set lateral orbits, not protruding hippopotamus stalks.
    ellipsoid('High eye '+label,(s*.223,-1.655,1.469),(.034,.038,.031),M['detail'],12,6)
    ellipsoid('Small nostril '+label,(s*.133,-1.905,1.319),(.037,.022,.019),M['detail'],12,6)
    tube('Small rounded ear '+label,[
        ((s*.19,-1.30,1.52),.048,.045),((s*.248,-1.29,1.59),.065,.035),((s*.256,-1.28,1.635),.047,.025),((s*.248,-1.28,1.65),.022,.018)],M['body'],10)
    ellipsoid('Ear inset '+label,(s*.250,-1.319,1.601),(.036,.008,.033),M['under'],10,6)
    tube('Upper enlarged canine '+label,[
        ((s*.172,-1.803,1.216),.031,.033),((s*.181,-1.814,1.156),.026,.025),((s*.183,-1.837,1.099),.017,.017),((s*.173,-1.856,1.074),.003,.004)],M['ivory'],10)
    tube('Lower canine '+label,[
        ((s*.140,-1.901,1.092),.023,.026),((s*.151,-1.918,1.130),.019,.020),((s*.153,-1.922,1.165),.010,.010),((s*.145,-1.917,1.181),.0025,.003)],M['ivory'],10)

# Four fully weightbearing foredigits and three hinddigits; tips are individually separated.
for name,x,y,count in leg_layout:
    spacing=.102 if count==4 else .108
    for i in range(count):
        dx=(i-(count-1)/2)*spacing
        # The marginal foretoe is smaller but reaches the ground: not a dewclaw.
        lateral=abs(dx);w=(.047 if count==4 else .052)*(0.88 if i in (0,count-1) else 1)
        front=y-.255+(.022 if i in (0,count-1) else 0)
        mid_y=front+.079
        vs=[]
        profile=[(-.7,-1),(.7,-1),(1,-.6),(1,.7),(.65,1),(-.65,1),(-1,.7),(-1,-.6)]
        for z,sc,ys in [(0,.90,0),(.045,1,0),(.112,.78,.025)]:
            for a,b in profile:vs.append((x+dx+a*w*sc,mid_y+b*.083*sc+ys,z))
        fs=[tuple(range(7,-1,-1)),tuple(16+i for i in range(8))]
        for j in range(2):
            for k in range(8):fs.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k))
        ob=mesh_object(f'{name}_weightbearing_toe_{i+1}',vs,fs,M['hoof'],C)
        ob['functional_digit']=i+1;ob['limb']=name;ob['ground_contact_m']=0.0


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,data):Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def finish(output):
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    os.chdir(output)
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene['representation']='living-reconstruction';scene['scientific_limit']='Composite restoration: measured 555 mm skull reference; 3 m living body estimate.'
    root=bpy.data.objects[C['asset_root']];root['bony_skull_reference_m']=.555
    root['fore_toes_each']=4;root['hind_toes_each']=3;root['horns']=0
    source=audit_source(C,16000)
    if source['errors']:raise RuntimeError(source['errors'])
    if len(source['materials'])>6:raise RuntimeError('Material budget')
    bpy.context.preferences.filepaths.save_version=0
    scene.render.filepath='//'
    # The delivered source contains no workstation browser location or output path.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//';space.params.filename='model.blend'
    for image in bpy.data.images:
        if image.source=='FILE':image.filepath=''
    for text in bpy.data.texts:text.filepath=''
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in C.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(filepath='model.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
        export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
        export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
        export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing required exporter options')
    bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb('model.glb',16000,6,48)
    if glb['errors'] or glb['bytes']>2200000:raise RuntimeError(glb)
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(expected[k][i]-glb['bounds_m'][k][i]) for k in ['min','max'] for i in range(3))
    if delta>.0001 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export mismatch')
    toes={name:sorted(ob['functional_digit'] for ob in C.all_objects if ob.get('limb')==name) for name,_,_,_ in leg_layout}
    report={'status':'PASS','scope':'Source geometry and static exact-GLB technical checks only','source':source,'glb':glb,'source_export_max_bounds_delta_m':delta,
      'digit_inventory':toes,'ground_contact':'All 14 modeled hoof meshes have vertices at z=0; no suspended marginal foredigit.',
      'runtime':{'blender':bpy.app.version_string,'python':sys.version.split()[0],'threads':2,'seed':P['seed']},
      'source_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),
      'blend_sha256':digest('model.blend'),'export_options':{k:v for k,v in opts.items() if k!='filepath'},
      'surface_policy':'Faceted closed meshes. Intentional anatomical overlap at mouth, eyes, ear insets and separate hoof meshes. Not a printable boolean union.'}
    dump('qa/evidence/technical.json',report)
    print('BUILD_OK',glb['sha256'],glb['scene_triangles'])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='.')
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    finish(args.output)
