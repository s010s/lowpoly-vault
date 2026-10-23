# SPDX-License-Identifier: MIT
"""Original Astrapotherium magnum reconstruction. Blender 4.3.2.
Reference-driven standing interpretation, not the pose of the recumbent mount.
Fleshy nose/lip, ears, pad outlines, tail and skin color are inferred.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=a.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('astrapotherium',P['seed']);ROOT=bpy.data.objects[COL['asset_root']]
M={n:make_material(n,c,roughness=.86 if n!='eye' else .32) for n,c in P['palette'].items()}
FORMS=[]
def loft_y(name,sections,material=None,n=24):
    verts=[];faces=[]
    for y,z,w,h in sections:
        for j in range(n):
            t=2*math.pi*j/n;verts.append((w*math.cos(t),y,z+h*math.sin(t)))
    for i in range(len(sections)-1):
        for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces += [tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]
    return mesh_object(name,verts,faces,material or M['skin'],COL)
def loft_z(name,sections,material=None,n=20):
    verts=[];faces=[]
    for z,x,y,w,d in sections:
        for j in range(n):
            t=2*math.pi*j/n;verts.append((x+w*math.cos(t),y+d*math.sin(t),z))
    for i in range(len(sections)-1):
        for j in range(n):faces.append((i*n+j,(i+1)*n+j,(i+1)*n+(j+1)%n,i*n+(j+1)%n))
    faces += [tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]
    return mesh_object(name,verts,faces,material or M['skin'],COL)
def tube(name,points,material,n=12,section_y=1.):
    verts=[];faces=[]
    for i,p in enumerate(points):
        center=Vector(p[:3]); tangent=Vector(points[min(i+1,len(points)-1)][:3])-Vector(points[max(i-1,0)][:3]);tangent.normalize()
        axis=Vector((1,0,0)) if abs(tangent.x)<.8 else Vector((0,1,0))
        u=tangent.cross(axis).normalized();v=tangent.cross(u).normalized()
        for j in range(n):
            t=2*math.pi*j/n;q=center+p[3]*(u*math.cos(t)*section_y+v*math.sin(t));verts.append(tuple(q))
    for i in range(len(points)-1):
        for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces += [tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]
    ob=mesh_object(name,verts,faces,material,COL)
    ob['centerline_length_m']=sum((Vector(points[i][:3])-Vector(points[i-1][:3])).length for i in range(1,len(points)))
    return ob
def ellipsoid(name,c,s,material,n=16,r=10):
    verts=[(c[0],c[1],c[2]-s[2])];faces=[]
    for i in range(1,r):
        v=-math.pi/2+math.pi*i/r
        for j in range(n):
            t=2*math.pi*j/n;verts.append((c[0]+s[0]*math.cos(v)*math.cos(t),c[1]+s[1]*math.cos(v)*math.sin(t),c[2]+s[2]*math.sin(v)))
    top=len(verts);verts.append((c[0],c[1],c[2]+s[2]))
    for j in range(n):faces.append((0,1+(j+1)%n,1+j))
    for i in range(r-2):
        k=1+i*n
        for j in range(n):faces.append((k+j,k+(j+1)%n,k+n+(j+1)%n,k+n+j))
    k=1+(r-2)*n
    for j in range(n):faces.append((k+j,k+(j+1)%n,top))
    return mesh_object(name,verts,faces,material,COL)
# The narrow, deep anterior rib cage precedes a long, lower lumbar region.
FORMS.append(loft_y('Elongated_deep_chest_and_lighter_rump',[
 (-.71,1.075,.13,.15),(-.60,1.055,.28,.28),(-.43,1.035,.345,.335),(-.20,1.02,.385,.34),
 (.12,.99,.40,.335),(.45,.985,.385,.31),(.73,1.00,.34,.275),(.97,1.015,.29,.24),(1.15,1.04,.19,.18),(1.19,1.05,.07,.10)]))
FORMS.append(loft_y('Moderately_long_neck',[
 (-1.10,1.23,.14,.19),(-.94,1.20,.195,.22),(-.76,1.16,.245,.25),(-.56,1.11,.275,.27)]))
# Raised posterior cranium and an anterior gap occupied by inferred fleshy upper lip.
FORMS.append(loft_y('Massive_long_cranium',[
 (-1.57,1.165,.10,.095),(-1.49,1.225,.15,.13),(-1.38,1.32,.18,.17),(-1.23,1.385,.205,.205),
 (-1.08,1.39,.205,.225),(-.96,1.35,.17,.20),(-.89,1.30,.10,.13)],n=26))
FORMS.append(loft_y('Deep_elongate_mandible',[
 (-1.60,1.005,.10,.055),(-1.52,1.00,.145,.085),(-1.38,1.035,.18,.11),(-1.22,1.075,.195,.14),(-1.08,1.13,.18,.16),(-.98,1.20,.12,.13)]))
for sign,label in [(-1,'L'),(1,'R')]:
    FORMS.append(ellipsoid('Cheek_arch_'+label,(sign*.173,-1.17,1.22),(.08,.17,.16),M['skin']))
    # Forelimbs deliberately longer and stronger than the recumbent mount appears.
    FORMS.append(loft_z('Strong_forelimb_'+label,[
      (.045,sign*.29,-.50,.11,.145),(.18,sign*.29,-.49,.10,.115),(.39,sign*.285,-.455,.095,.105),
      (.66,sign*.28,-.385,.125,.14),(.90,sign*.265,-.45,.17,.185),(1.12,sign*.21,-.45,.18,.20),(1.31,sign*.13,-.42,.105,.115)]))
    FORMS.append(loft_z('Slender_hindlimb_'+label,[
      (.045,sign*.265,.90,.09,.13),(.18,sign*.265,.95,.085,.10),(.40,sign*.265,1.00,.072,.087),
      (.59,sign*.27,.86,.09,.115),(.80,sign*.245,.75,.13,.15),(1.04,sign*.195,.83,.15,.17),(1.20,sign*.12,.88,.095,.11)]))
    for leg,y,x,w,d in [('Fore',-.52,.29,.13,.17),('Hind',.90,.265,.108,.165)]:
        FORMS.append(loft_z(leg+'_inferred_support_pad_'+label,[
          (0,sign*x,y-.015,w*.93,d*.92),(.035,sign*x,y-.025,w,d),(.10,sign*x,y-.005,w*.96,d*.90),(.18,sign*x,y+.025,w*.73,d*.63)]))
# Editable source forms are separate from the portable surface export.
SC=bpy.data.collections.new('SOURCE_FORMS');bpy.context.scene.collection.children.link(SC)
for ob in FORMS:
    cp=ob.copy();cp.data=ob.data.copy();cp.name='EDIT_'+ob.name;cp.parent=None;SC.objects.link(cp);cp.hide_render=True;cp.hide_set(True)
SC.hide_render=True;SC.hide_viewport=True
bpy.ops.object.select_all(action='DESELECT')
for ob in FORMS:ob.select_set(True)
bpy.context.view_layer.objects.active=FORMS[0];bpy.ops.object.join();body=FORMS[0];body.name='Continuous_original_body_surface'
mod=body.modifiers.new('Union_profile_forms','REMESH');mod.mode='VOXEL';mod.voxel_size=P['voxel_size_m'];mod.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=body.modifiers.new('Soften_only_form_transitions','SMOOTH');mod.factor=.40;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
body.data.calc_loop_triangles();mod=body.modifiers.new('Deliberate_lowpoly_surface','DECIMATE');mod.ratio=min(1,P['body_triangle_target']/len(body.data.loop_triangles));mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
# Ground the four pads and preserve the measured standing shoulder reference.
minimum=min(v.co.z for v in body.data.vertices)
for v in body.data.vertices:v.co.z=max(0,v.co.z-minimum)
shoulder=max(v.co.z for v in body.data.vertices if -.54<v.co.y<-.31 and abs(v.co.x)<.16)
scale=P['shoulder_model_m']/shoulder
for v in body.data.vertices:v.co.z*=scale
body.data.materials.clear();body.data.materials.append(M['skin']);body.data.materials.append(M['belly'])
for f in body.data.polygons:
    c=f.center
    if -.30<c.y<.79 and c.z<.76:f.material_index=1
body['anatomy']='Deep narrow chest; elongated trunk; standing strong forelimbs and lighter hindquarters.'
body['reference_shoulder_m']=P['shoulder_model_m'];body['vertical_adjustment']=scale
# Short pouchy prehensile upper lip. It does not form a dangling elephant trunk.
nose=tube('Inferred_short_mobile_nose_lip',[(0,-1.425,1.385,.112),(0,-1.52,1.355,.117),(0,-1.605,1.285,.108),(0,-1.656,1.205,.082),(0,-1.66,1.16,.049)],M['nose_pad'],18,section_y=.72)
nose['soft_tissue_status']='Inferred short fleshy nose and mobile upper lip; no preserved soft-tissue measurement.'
# Four canines, not incisors. Upper exposed lengths and lower lengths are estimates.
for sign,label in [(-1,'L'),(1,'R')]:
    up=tube('Upper_canine_'+label,[(sign*.164,-1.445,1.195,.043),(sign*.187,-1.47,1.12,.041),(sign*.211,-1.508,1.035,.033),(sign*.221,-1.543,.97,.021),(sign*.218,-1.57,.945,.007)],M['ivory'],9,section_y=.86)
    up['tooth']='Upper canine, not incisor; exposed size reconstructed'
    lo=tube('Lower_canine_'+label,[(sign*.108,-1.545,.996,.030),(sign*.119,-1.61,1.005,.027),(sign*.135,-1.675,1.035,.020),(sign*.148,-1.711,1.074,.006)],M['ivory'],10)
    lo['tooth']='Lower canine; shorter opposing pair, exposed size reconstructed'
    # Moderate ears, eyes on lateral upper face and restrained nostril marks.
    ellipsoid('Inferred_ear_'+label,(sign*.224,-.974,1.477),(.072,.046,.105),M['skin'],16,10)
    ellipsoid('Ear_concha_'+label,(sign*.235,-1.012,1.483),(.045,.014,.070),M['inner_ear'],14,8)
    ellipsoid('Eye_rim_'+label,(sign*.199,-1.255,1.434),(.031,.037,.030),M['nose_pad'],14,8)
    ellipsoid('Dark_eye_'+label,(sign*.220,-1.270,1.438),(.016,.022,.019),M['eye'],14,8)
    ellipsoid('Nostril_'+label,(sign*.035,-1.672,1.233),(.017,.013,.012),M['eye'],12,8)
# The mouth is a closed thin seam, not a gaping cavity; roots remain embedded.
loft_y('Closed_mouth_seam',[(-1.59,1.092,.103,.004),(-1.48,1.115,.154,.005),(-1.34,1.15,.184,.004),(-1.22,1.19,.194,.003)],M['nose_pad'],20)
# Modest tapered tail, freely inferred, kept distinct from the fossil body length.
tail_path=[(0,1.12,1.12,.052),(.02,1.28,1.065,.042),(.04,1.43,.965,.030),(.055,1.54,.84,.020),(.06,1.565,.735,.006)]
tail_origin=Vector(tail_path[0][:3]);tail_length=sum((Vector(tail_path[i][:3])-Vector(tail_path[i-1][:3])).length for i in range(1,len(tail_path)))
tail_path=[(*tuple(tail_origin+(Vector(p[:3])-tail_origin)*(P['tail_model_m']/tail_length)),p[3]) for p in tail_path]
tail=tube('Inferred_tail',tail_path,M['skin'],12)
tail['status']='Soft-tissue estimate, excluded from reported nose-to-pelvis dimension'
# Implied foredigit fronts are shallow pad lobes, not five oversized claws.
for sign,label in [(-1,'L'),(1,'R')]:
    for i in range(5):
        x=sign*.29+(i-2)*.043
        ellipsoid('Fore_pad_digit_'+label+'_'+str(i+1),(x,-.656+.015*abs(i-2),.058),(.025,.026,.033),M['nose_pad'],10,6)
for ob in COL.all_objects:
    if ob.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    for f in ob.data.polygons:f.use_smooth=False
bpy.context.view_layer.update();source=audit_source(COL,16000)
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.scene['source_generator']='source/generate.py'
bpy.context.scene['reference_nose_to_pelvis_m']=2.88
bpy.context.scene['nose_to_pelvis_note']='Specimen measurement is not tail-inclusive total length; body landmarks are estimates.'
bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=ROOT
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
 export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
 export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Unsupported exporter options')
bpy.ops.export_scene.gltf(**options);glb=audit_glb(OUT/'model.glb',16000,6,48)
if glb['errors'] or glb['bytes']>2200000:raise RuntimeError(glb)
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
if delta>1e-4 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source/export mismatch')
glb['file']='model.glb'
record={'asset_id':'astrapotherium','revision':'r001','blender':bpy.app.version_string,'seed':P['seed'],
 'glb_sha256':glb['sha256'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,
 'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},
 'source_forms_excluded':len(SC.objects),'threads':2,'upper_canine_meshes':2,'lower_canine_meshes':2,
 'scale_landmarks':{'shoulder_m':P['shoulder_model_m'],'nose_tip_y_estimate':-1.69,'pelvis_posterior_y_estimate':1.19,'nose_to_pelvis_m':2.88,'tail_centerline_m':tail['centerline_length_m'],'tail_excluded_from_body_reference':True},
 'notes':['Original profile forms retained outside EXPORT.','Standing pose does not copy the lying mount.','Fleshy nose/lip, pads, ears, tail and color are inferred.','Forefoot digit lobes are conservative surface interpretation, not fossil soft anatomy.']}
(OUT/'build-report.json').write_text(json.dumps(record,indent=2)+'\n')
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
