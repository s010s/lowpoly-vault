# SPDX-License-Identifier: MIT
"""Original, deterministic Coelodonta reconstruction. Run in Blender 4.3.2.

Usage: blender --background --factory-startup --threads 2 --python generate.py -- --output OUTPUT
Only declared sibling dependencies and params.json are required. The exact GLB
is static, texture-free and meter-scaled. Geometry is an artistic reconstruction,
not a scan. The construction collection preserves editable semantic loft inputs.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse, os
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb
P=json.loads((BASE/'params.json').read_text())
for module_name in ('asset_common','qa_glb'):
    assert Path(sys.modules[module_name].__file__).resolve().parent==(BASE/'deps').resolve(), 'Undeclared local helper origin'

A=argparse.ArgumentParser(); A.add_argument('--output',type=Path,required=True)
a=A.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
os.chdir(out)
collection=setup_scene('coelodonta',P['seed']); root=bpy.data.objects['coelodonta']
scene=bpy.context.scene; scene.render.threads_mode='FIXED'; scene.render.threads=2
scene.render.filepath='//renders/'
M={k:make_material(k,v,roughness=.91 if k not in ('eyes_nostrils','keratin') else .80) for k,v in P['palette'].items()}
body_inputs=[]

def loft_y(name,rings,sides=24,material=None,fur=False):
    # Rings: longitudinal y, center z, lateral half-width, vertical half-height.
    vs=[]; fs=[]
    for j,(y,z,rx,rz) in enumerate(rings):
        for k in range(sides):
            angle=2*math.pi*k/sides
            # A few long coat lobes, not stochastic hair geometry.
            ripple=1
            if fur and 0<j<len(rings)-1:
                ripple+=.014*math.cos(5*angle+1.25*j)+.008*math.cos(3*angle-.8*j)
            vs.append((rx*math.cos(angle)*ripple,y,z+rz*math.sin(angle)*ripple))
    for j in range(len(rings)-1):
        for k in range(sides): fs.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    fs.append(tuple(reversed(range(sides)))); fs.append(tuple((len(rings)-1)*sides+k for k in range(sides)))
    return mesh_object(name,vs,fs,material or M['wool'],collection)

def sweep_z(name,rings,sides=16,material=None):
    # Vertical elliptical profile rings: x, y, z, transverse radius, fore-aft radius.
    vs=[]; fs=[]
    for x,y,z,rx,ry in rings:
        for k in range(sides):
            t=2*math.pi*k/sides;vs.append((x+rx*math.cos(t),y+ry*math.sin(t),z))
    for j in range(len(rings)-1):
        for k in range(sides):fs.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    fs.extend([tuple(reversed(range(sides))),tuple((len(rings)-1)*sides+k for k in range(sides))])
    return mesh_object(name,vs,fs,material or M['wool'],collection)

def ellipsoid(name,center,radii,mat,sides=16,levels=8):
    vs=[(center[0],center[1],center[2]-radii[2])]; fs=[]
    for j in range(1,levels):
        phi=-math.pi/2+math.pi*j/levels
        for k in range(sides):
            t=2*math.pi*k/sides
            vs.append((center[0]+radii[0]*math.cos(phi)*math.cos(t),center[1]+radii[1]*math.cos(phi)*math.sin(t),center[2]+radii[2]*math.sin(phi)))
    vs.append((center[0],center[1],center[2]+radii[2])); top=len(vs)-1
    for k in range(sides):fs.append((0,1+(k+1)%sides,1+k))
    for j in range(levels-2):
        for k in range(sides):fs.append((1+j*sides+k,1+j*sides+(k+1)%sides,1+(j+1)*sides+(k+1)%sides,1+(j+1)*sides+k))
    for k in range(sides):fs.append((top,1+(levels-2)*sides+k,1+(levels-2)*sides+(k+1)%sides))
    return mesh_object(name,vs,fs,mat,collection)

# A long barrel, massive shoulders and descending dorsal line. All visible
# soft-body transitions are one unioned surface, not covered primitive caps.
body_inputs.append(loft_y('Editable-trunk-profile',[
 (-1.08,.97,.16,.25),(-.99,1.02,.28,.35),(-.86,1.055,.38,.425),
 (-.66,1.055,.47,.495),(-.44,1.025,.51,.50),(-.16,1.00,.54,.49),
 (.15,.98,.54,.465),(.43,.985,.535,.445),(.71,.99,.51,.435),
 (.96,1.015,.48,.415),(1.15,1.025,.415,.36),(1.31,1.03,.30,.285),
 (1.41,1.03,.14,.18),(1.45,1.03,.025,.06)],fur=True))
body_inputs.append(loft_y('Editable-low-head-neck-profile',[
 (-2.05,.505,.135,.075),(-2.025,.51,.20,.115),(-1.96,.545,.235,.155),
 (-1.84,.595,.249,.203),(-1.69,.66,.257,.235),(-1.52,.73,.282,.26),
 (-1.36,.805,.305,.28),(-1.19,.865,.286,.305),(-1.05,.95,.30,.36),
 (-.90,1.0,.33,.39),(-.76,1.02,.29,.32)],fur=True))
feet=[]
for side,x in [('right',.395),('left',-.395)]:
    s=1 if x>0 else -1
    for where,y in [('front',-.94 if s>0 else -.68),('hind',.99 if s>0 else .73)]:
        front=where=='front'; foot_y=y-.04
        rings=[
          (s*.25,y+(0 if front else -.03),1.25,.14,.20),
          (s*.30,y,1.08,.20,.24 if front else .25),
          (s*.355,y+(.025 if front else -.06),.88,.195,.22),
          (s*.40,y+(.065 if front else -.105),.68,.17,.18),
          (s*.43,y+(.055 if front else .015),.49,.151,.162),
          (s*.435,y+(.015 if front else .08),.33,.145,.15),
          (s*.44,foot_y+.045,.185,.175,.18),
          (s*.44,foot_y+.015,.115,.188,.20),
          (s*.44,foot_y,.066,.18,.19)]
        body_inputs.append(sweep_z('Editable-'+side+'-'+where+'-limb',rings,sides=20))
        feet.append((side,where,s*.44,foot_y))
# The brow is integrated into the cheek mass, so the eyes will sit beneath it.
for s in (-1,1):
    body_inputs.append(ellipsoid('Editable-orbital-brow', (s*.263,-1.34,.952),(.060,.094,.045),M['wool'],16,6))
# Keep editable original lofts outside EXPORT. No renderer stage enters source.
construction=bpy.data.collections.new('CONSTRUCTION');scene.collection.children.link(construction)
for obj in body_inputs:
    copy=obj.copy();copy.data=obj.data.copy();construction.objects.link(copy);copy.parent=None
    copy.name=obj.name+'-control';copy.hide_render=True;copy.hide_set(True)
construction.hide_render=True;construction.hide_viewport=True
bpy.ops.object.select_all(action='DESELECT')
for obj in body_inputs:obj.select_set(True)
bpy.context.view_layer.objects.active=body_inputs[0];bpy.ops.object.join()
body=bpy.context.object;body.name='Continuous-woolly-body'
rem=body.modifiers.new('Integrated-profile-union','REMESH');rem.mode='VOXEL';rem.voxel_size=P['construction']['body_voxel_m'];rem.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=rem.name)
sm=body.modifiers.new('Soft-tissue-transition','SMOOTH');sm.factor=.62;sm.iterations=P['construction']['surface_smooth_iterations'];bpy.ops.object.modifier_apply(modifier=sm.name)
body.data.calc_loop_triangles();before=len(body.data.loop_triangles)
dec=body.modifiers.new('Purposeful-surface-budget','DECIMATE');dec.ratio=min(1,P['construction']['body_surface_triangles']/before);bpy.ops.object.modifier_apply(modifier=dec.name)
# Sparse shallow coat edge undulations are integrated into the skin surface.
for vertex in body.data.vertices:
    x,y,z=vertex.co
    if -.6<y<1.0 and z<.65 and abs(x)<.34:
        vertex.co.z-=.018*max(0,math.sin(y*24+.8))**4*max(0,1-abs(x)/.34)
    if -.90<y<.70 and z>1.31 and abs(x)<.21:
        vertex.co.z+=.013*max(0,math.sin(y*26))**4*(1-abs(x)/.21)
body.data.update()
body.data.materials.clear()
for k in ['wool','dorsal_wool','undercoat']:body.data.materials.append(M[k])
for poly in body.data.polygons:
    co=poly.center
    # Restrained natural dorsal/undercoat regions share the same surface.
    upper=1.335+.045*math.sin(2.4*co.y)
    if (co.x/.32)**2+((co.y+.10)/1.18)**2<1.0 and co.z>1.31:poly.material_index=1
    elif (co.y<-1.76 and co.z<.57) or (co.y>-.8 and co.z<.66 and abs(co.x)<.38):poly.material_index=2
    else:poly.material_index=0
    poly.use_smooth=False

# Two individually editable horns, all their basal rings buried in head volume.
# The nasal root is 0.45 m fore-aft by 0.30 m transverse (ratio 1.5),
# not a flattened razor base. The distal shaft progressively compresses.
horn=sweep_z('Nasal-horn-broad-oval-root',[
 (0,-1.780,.80,.150,.225),(0,-1.790,.89,.153,.225),
 (0,-1.82,1.00,.140,.203),(0,-1.885,1.10,.119,.176),
 (0,-1.90,1.20,.098,.149),(0,-1.899,1.30,.077,.125),
 (0,-1.88,1.40,.058,.105),(0,-1.85,1.49,.042,.083),
 (0,-1.81,1.57,.030,.060),(0,-1.755,1.64,.020,.039),
 (0,-1.69,1.70,.011,.021),(0,-1.62,1.75,.0025,.0035)],sides=24,material=M['keratin'])
# Carry the curved skin attachment into progressively flatter rising rings.
# This avoids both a floating horizontal rim and an inverted basal fold.
bpy.context.view_layer.update()
for k in range(24):
    v=horn.data.vertices[k]
    hit,loc,norm,index=body.ray_cast(Vector((v.co.x,v.co.y,2.5)),Vector((0,0,-1)))
    if not hit:raise RuntimeError('Nasal horn root exceeds supporting head '+str(tuple(v.co)))
    delta=loc.z-.80
    for ring,weight in enumerate((1.,.85,.60,.35,.15)):
        q=horn.data.vertices[ring*24+k]
        q.co.z+=delta*weight-(.035 if ring==0 else 0)
bm=bmesh.new();bm.from_mesh(horn.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(horn.data);bm.free();horn.data.update()
second=sweep_z('Frontal-horn',[
 (0,-1.37,1.005,.115,.150),(0,-1.37,1.06,.114,.142),
 (0,-1.365,1.12,.089,.112),(0,-1.35,1.19,.063,.081),
 (0,-1.32,1.255,.034,.047),(0,-1.28,1.30,.005,.007)],sides=20,material=M['keratin'])
# Ears are small closed pointed pinnae, rather than spheres or oversized sails.
for s in (-1,1):
    e=sweep_z(('Right' if s>0 else 'Left')+'-compact-ear',[
      (s*.225,-1.135,1.07,.060,.055),(s*.265,-1.115,1.14,.071,.055),
      (s*.293,-1.09,1.22,.062,.043),(s*.32,-1.055,1.29,.039,.029),
      (s*.336,-1.028,1.325,.006,.007)],sides=12,material=[M['wool'],M['undercoat']])
    for p in e.data.polygons:
        if p.normal.y<-.4 and p.center.z>1.15:p.material_index=1
# Three anatomically placed short nail/hoof units per foot. The central toe is
# broader and projects farther, and all twelve soles share the Z=0 ground.
for side,where,x,y in feet:
    for t,offset in enumerate((-.118,0,.118)):
        mid=t==1; w=.063 if mid else .050
        cy=y-(.109 if mid else .076)
        toe=sweep_z(side+'-'+where+'-toe-'+str(t+1),[
          (x+offset,cy,.0,w*.88,.092 if mid else .078),
          (x+offset,cy-.006,.025,w,.102 if mid else .086),
          (x+offset,cy,.095,w*.97,.098 if mid else .082),
          (x+offset*.94,cy+.018,.145,w*.78,.076 if mid else .064)],sides=10,material=M['hooves'])
# Short, thick-based tail following rump; intentionally not a long whip.
tail=loft_y('Short-tapered-tail',[
 (1.34,1.12,.087,.079),(1.43,1.095,.083,.073),(1.51,1.04,.070,.066),
 (1.56,.96,.052,.057),(1.58,.88,.041,.047),(1.59,.80,.028,.035),
 (1.60,.765,.010,.015)],sides=14,material=M['wool'])
# Embedded dark lateral lenses: locate the actual post-union skin using rays.
# Their center is recessed and only a shallow lens extends beyond the surface.
bpy.context.view_layer.update()
face_points=[]
for s in (-1,1):
    for label,y,z,ry,rz in [('Eye',-1.35,.902,.029,.021),('Nostril',-1.963,.595,.034,.024)]:
        hit,loc,norm,index=body.ray_cast(Vector((s*2,y,z)),Vector((-s,0,0)))
        if not hit:raise RuntimeError('Cannot place embedded '+label)
        center=loc+Vector((-s*.007,0,0))
        eye=ellipsoid(('Right' if s>0 else 'Left')+'-'+label,center,(.012,ry,rz),M['eyes_nostrils'],16,8)
        face_points.append({'part':eye.name,'surface_m':list(loc),'center_m':list(center),'max_protrusion_m':.005})
    # An extremely shallow closed-mouth line, fitted against the cheek.
    vs=[]; fs=[]
    for j,(y,z) in enumerate([(-2.023,.486),(-1.99,.474),(-1.93,.465),(-1.86,.473),(-1.80,.49)]):
        hit,loc,norm,index=body.ray_cast(Vector((s*2,y,z)),Vector((-s,0,0)))
        if not hit:raise RuntimeError('Mouth surface missing')
        for dz in (-.005,.005):vs.append((loc.x+s*.0015,y,z+dz))
    for j in range(4):fs.append((2*j,2*j+1,2*j+3,2*j+2))
    mouth=mesh_object(('Right' if s>0 else 'Left')+'-closed-mouth-line',vs,fs,M['eyes_nostrils'],collection)
    sol=mouth.modifiers.new('Inset-thickness','SOLIDIFY');sol.thickness=.004;sol.offset=-1
    bpy.context.view_layer.objects.active=mouth;bpy.ops.object.modifier_apply(modifier=sol.name)
# Exact minimum ground comes from hoof soles; keep the canonical identity root.
scene['reconstruction_scope']='Original living reconstruction, not exact individual specimen'
scene['generator']='source/generate.py'; scene['scientific_limits']='See brief.json'
source=audit_source(collection,16000)
if source['errors']:raise RuntimeError(str(source['errors']))
# Runtime RNA probe is recorded before writing the delivery.
opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
 export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',
 export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,
 export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,
 export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available:raise RuntimeError('Missing exporter options '+str(set(opts)-available))
import io_scene_gltf2
exporter_version='.'.join(map(str,io_scene_gltf2.bl_info['version']))
# Clear transient file-browser directory buffers before saving a public source.
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'.'*1023
                space.params.directory=b'//'
                space.params.filename='model.blend'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in collection.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath='model.glb',**opts)
glb=audit_glb(Path('model.glb'),16000,6,48)
if glb['errors']:raise RuntimeError(str(glb['errors']))
b=source['bounds_blender_m']; expmin=[b['min'][0],b['min'][2],-b['max'][1]]; expmax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][k][i]-v[i]) for k,v in [('min',expmin),('max',expmax)] for i in range(3))
assert delta<.0001 and source['triangles']==glb['scene_triangles']
assert glb['bytes']<=2200000
report={'schema_version':1,'subject':{'asset_id':'coelodonta','revision':'r001','glb_sha256':glb['sha256']},
 'runtime':{'blender':bpy.app.version_string,'gltf_exporter':exporter_version,'python':sys.version.split()[0],'threads':2},
 'export_options':opts,'rna_required_options_present':True,'source':source,'glb':glb,
 'source_export_bound_max_error_m':delta,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'params_sha256':hashlib.sha256((BASE/'params.json').read_bytes()).hexdigest(),
 'local_dependency_origins':[{'module':name,'path':'source/deps/'+Path(sys.modules[name].__file__).name,'sha256':hashlib.sha256(Path(sys.modules[name].__file__).read_bytes()).hexdigest()} for name in ('asset_common','qa_glb')],
 'anatomical_measurements':{'body_nose_to_rump_m':max(v.co.y for v in body.data.vertices)-min(v.co.y for v in body.data.vertices),'withers_height_m':max(v.co.z for v in body.data.vertices if -.95<v.co.y<-.2),'nasal_horn_base_transverse_m':.30,'nasal_horn_base_fore_aft_m':.45,'nasal_horn_base_ratio':1.5,'scope':'Reconstruction geometry measurements, not exact specimen measurements.'},
 'ground_contacts':{'toe_count':12,'feet':4,'sole_z_m':0.0},'face_placements':face_points,
 'construction_notes':'Controlled torso/head/limb lofts form one remeshed soft-tissue surface. Horns, pinnae, toes and tail remain semantic editable parts. No untouched sphere/cylinder assembly.',
 'runtime_limits':'Source/export evidence only. No Three.js GPU or populated scene claim.'}
(out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'BUILT','triangles':glb['scene_triangles'],'primitives':glb['scene_primitives_estimated_base_draw_calls'],'glb_bytes':glb['bytes'],'semantic_sha256':glb['semantic_sha256']}))
