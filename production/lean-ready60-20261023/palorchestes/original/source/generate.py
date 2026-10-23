# SPDX-License-Identifier: MIT
"""Original Palorchestes living reconstruction; Blender 4.3.2, meters, -Y forward.
Separate fossil elements inform this deliberately estimated whole animal.
No reference image or outside file is read. Editable loft forms remain in source.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
OUT=args.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene(P['asset_id'],P['seed']);ROOT=bpy.data.objects[COL['asset_root']]
M={k:make_material(k,v,roughness=.88 if k!='eye' else .32) for k,v in P['palette_srgb'].items()}
FORMS=[]
def loft(name,sections,axis='Y',n=20,mat=None):
    # Y: longitudinal station, height, half-width, half-depth. Z: height,x,y,rx,ry.
    verts=[];faces=[]
    for sec in sections:
        for j in range(n):
            a=2*math.pi*j/n
            if axis=='Y':
                y,z,w,h=sec;verts.append((w*math.cos(a),y,z+h*math.sin(a)))
            else:
                z,x,y,w,d=sec;verts.append((x+w*math.cos(a),y+d*math.sin(a),z))
    for i in range(len(sections)-1):
        for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.extend([tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))])
    return mesh_object(name,verts,faces,mat or M['body'],COL)
def oval(name,center,scale,mat,segments=16,rings=10):
    x,y,z=center;rx,ry,rz=scale;v=[(x,y,z-rz)];f=[]
    for i in range(1,rings):
        b=-math.pi/2+math.pi*i/rings
        for j in range(segments):
            a=2*math.pi*j/segments;v.append((x+rx*math.cos(b)*math.cos(a),y+ry*math.cos(b)*math.sin(a),z+rz*math.sin(b)))
    tip=len(v);v.append((x,y,z+rz))
    for j in range(segments):f.append((0,1+(j+1)%segments,1+j))
    for i in range(rings-2):
        o=1+i*segments
        for j in range(segments):f.append((o+j,o+(j+1)%segments,o+segments+(j+1)%segments,o+segments+j))
    o=1+(rings-2)*segments
    for j in range(segments):f.append((o+j,o+(j+1)%segments,tip))
    return mesh_object(name,v,f,mat,COL)
# Long barrel, pronounced shoulder, ventral sag and narrowing croup.
FORMS.append(loft('Long_barrel',[
 (-.78,.98,.12,.19),(-.66,.98,.27,.30),(-.50,.93,.36,.42),
 (-.22,.88,.43,.43),(.12,.86,.455,.42),(.44,.87,.43,.405),
 (.72,.90,.365,.37),(.92,.91,.25,.28),(1.025,.91,.055,.12)],n=24))
FORMS.append(loft('Strong_sloping_neck',[
 (-1.09,1.105,.115,.18),(-.98,1.08,.19,.24),(-.83,1.03,.24,.29),(-.61,1.00,.29,.31)],n=22))
# Elongate narrow face with high caudal nasal region, NOT a tapir/elephant tube.
FORMS.append(loft('Elongate_cranium',[
 (-1.465,1.025,.068,.065),(-1.40,1.055,.095,.10),(-1.29,1.095,.115,.13),
 (-1.16,1.145,.14,.175),(-1.025,1.17,.16,.185),(-.925,1.16,.13,.16),(-.87,1.14,.065,.09)],n=24))
FORMS.append(loft('Elongate_lower_jaw',[
 (-1.465,.964,.058,.025),(-1.38,.955,.085,.043),(-1.23,.955,.105,.065),
 (-1.08,.974,.14,.09),(-.96,1.025,.125,.12)],n=20))
for sign,label in [(-1,'L'),(1,'R')]:
    # Upper arm goes caudolaterally; elbow is abducted and forearm returns forward.
    FORMS.append(loft('Bent_abducted_forelimb_'+label,[
      (.075,sign*.495,-.605,.083,.10),(.18,sign*.50,-.57,.087,.095),
      (.36,sign*.54,-.465,.085,.095),(.53,sign*.585,-.31,.10,.11),
      (.665,sign*.59,-.205,.135,.13),(.78,sign*.53,-.27,.155,.16),
      (.95,sign*.40,-.425,.175,.18),(1.10,sign*.30,-.49,.17,.20),(1.19,sign*.23,-.49,.115,.14)],'Z',20))
    FORMS.append(loft('Hindlimb_'+label,[
      (.055,sign*.33,.735,.082,.11),(.16,sign*.33,.79,.08,.085),
      (.35,sign*.34,.845,.085,.09),(.51,sign*.355,.68,.115,.13),
      (.69,sign*.345,.57,.16,.17),(.87,sign*.31,.65,.19,.225),
      (1.06,sign*.245,.70,.15,.18),(1.18,sign*.17,.69,.075,.11)],'Z',20))
    for leg,x,y in [('Fore',.495,-.63),('Hind',.33,.72)]:
        FORMS.append(loft(leg+'_support_palm_'+label,[
          (0,sign*x,y,.087,.14),(.035,sign*x,y-.015,.102,.155),(.08,sign*x,y,.097,.14),(.14,sign*x,y+.045,.070,.085)],'Z',16))
        # Three separated simplified toe bases; no claim of complete recovered digit count.
        for i,dx in enumerate([-.064,0,.064]):
            FORMS.append(oval(leg+'_digit_base_'+label+str(i),(sign*x+dx,y-.128,.068),(.028,.065,.045),M['body'],12,8))
# A moderate tapering tail, an explicitly original soft-tissue estimate.
FORMS.append(loft('Moderate_tapering_tail',[(.94,.92,.085,.085),(1.08,.855,.07,.07),(1.23,.75,.05,.055),(1.37,.665,.031,.04),(1.49,.62,.009,.014),(1.515,.617,.003,.005)],n=14))
SC=bpy.data.collections.new('SOURCE_FORMS');bpy.context.scene.collection.children.link(SC)
for obj in FORMS:
    cp=obj.copy();cp.data=obj.data.copy();cp.name='EDIT_'+obj.name;cp.parent=None
    SC.objects.link(cp);cp.hide_render=True;cp.hide_set(True)
SC.hide_render=True;SC.hide_viewport=True
bpy.ops.object.select_all(action='DESELECT')
for obj in FORMS:obj.select_set(True)
bpy.context.view_layer.objects.active=FORMS[0];bpy.ops.object.join();body=FORMS[0];body.name='Unified_loft_skin'
r=body.modifiers.new('Watertight_anatomical_union','REMESH');r.mode='VOXEL';r.voxel_size=P['voxel_size_m'];r.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=r.name)
s=body.modifiers.new('Conservative_relaxation','SMOOTH');s.factor=.42;s.iterations=3;bpy.ops.object.modifier_apply(modifier=s.name)
body.data.calc_loop_triangles();d=body.modifiers.new('Lowpoly_surface','DECIMATE');d.ratio=min(1,P['body_triangle_target']/len(body.data.loop_triangles));d.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=d.name)
low=min(v.co.z for v in body.data.vertices)
for v in body.data.vertices:v.co.z=max(0.,v.co.z-low)
body.data.materials.clear();body.data.materials.append(M['body']);body.data.materials.append(M['under'])
# Quiet underside color break follows surface location, not an applied picture.
for poly in body.data.polygons:
    c=sum((body.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices)
    if -.65<c.y<.85 and c.z<.62 and abs(c.x)<.35:poly.material_index=1
body['construction']='Original lofts, union, conservative relaxation and decimation; editable forms retained'
# Thin closed blade profiles, with deep sagittal crescent and a pointed keratin edge.
def claw(name,x,y,scale=1):
    profile=[(0,.125),(-.030,.128),(-.060,.103),(-.080,.063),(-.095,.022),(-.076,.035),(-.051,.071),(-.026,.086),(0,.080)]
    v=[]
    for side in [-1,1]:
        for i,(dy,z) in enumerate(profile):
            w=.009 if i not in (3,4,5) else (.004 if i!=4 else .0015)
            v.append((x+side*w*scale,y+dy*scale,.015+(z-.015)*scale))
    n=len(profile);f=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    for j in range(n):f.append((j,(j+1)%n,(j+1)%n+n,j+n))
    return mesh_object(name,v,f,M['claw'],COL)
for sign,label in [(-1,'L'),(1,'R')]:
    oval('Small_rounded_ear_'+label,(sign*.153,-.902,1.326),(.054,.039,.072),M['body'],16,10)
    oval('Ear_concha_'+label,(sign*.155,-.935,1.331),(.034,.013,.047),M['inner'],14,8)
    oval('Eye_rim_'+label,(sign*.142,-1.123,1.225),(.027,.035,.025),M['nose'],14,8)
    oval('Small_eye_'+label,(sign*.161,-1.138,1.228),(.014,.018,.015),M['eye'],14,8)
    oval('Retracted_nostril_'+label,(sign*.061,-1.425,1.115),(.017,.010,.011),M['eye'],12,8)
    for leg,x,y,fac in [('Fore',.495,-.773,1.),('Hind',.33,.576,.48)]:
        claws=[]
        for i,dx in enumerate([-.064,0,.064]):claws.append(claw(leg+'_blade_'+label+str(i),sign*x+dx,y+(0 if i==1 else .008),fac*(1 if i==1 else .90)))
        bpy.ops.object.select_all(action='DESELECT')
        for ob in claws:ob.select_set(True)
        bpy.context.view_layer.objects.active=claws[0];bpy.ops.object.join();claws[0].name=leg+'_separated_claw_blades_'+label
# Small dark distal lip is only 35 mm long and does not become a pendant trunk.
loft('Mobile_upper_lip',[(-1.505,1.015,.043,.027),(-1.492,1.035,.069,.046),(-1.46,1.063,.083,.053),(-1.426,1.084,.086,.047)],n=20,mat=M['nose'])
loft('Narrow_mouth_line',[(-1.493,.979,.047,.004),(-1.445,.976,.079,.005),(-1.355,.980,.095,.004),(-1.29,.986,.097,.003)],n=18,mat=M['nose'])
for obj in COL.all_objects:
    if obj.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()
    for poly in obj.data.polygons:poly.use_smooth=False
bpy.context.view_layer.update();source=audit_source(COL,16000)
if source['errors']:raise RuntimeError(source['errors'])
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
scene['asset_license']='CC-BY-4.0';scene['asset_author']='Leon Made This / s010s';scene['source_generator']='source/generate.py'
bpy.context.preferences.filepaths.save_version=0
scene.render.filepath='//preview.png'
# Portable startup editor state; no local file-browser directory in the source.
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'
                space.params.filename='model.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=ROOT
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
 export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
 export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available:raise RuntimeError('Unsupported exporter options')
bpy.ops.export_scene.gltf(**opts);glb=audit_glb(OUT/'model.glb',16000,6,48)
if glb['errors'] or glb['bytes']>2200000:raise RuntimeError(glb['errors'] or 'GLB byte budget exceeded')
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
if delta>1e-4 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source/export mismatch')
record={'asset_id':P['asset_id'],'revision':P['revision'],'seed':P['seed'],'blender':bpy.app.version_string,
 'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),
 'glb_sha256':glb['sha256'],'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,
 'export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_forms_excluded':len(SC.objects),'threads':2,
 'notes':['Whole-body proportions and soft tissue are estimates, not a complete skeleton.','Three simplified visible claw-bearing digits are not a claim of complete manual anatomy.']}
# Public reports contain portable names only; logs may retain local provenance privately.
record['glb']['file']='model.glb'
(OUT/'build-report.json').write_text(json.dumps(record,indent=2)+'\n')
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
