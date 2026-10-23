# SPDX-License-Identifier: MIT
"""Original Pyrotherium romeroi reconstruction; Blender 4.3.2.
Skull-derived diagnostic six-incisor arrangement; body and soft tissues inferred.
This short-proboscis concept is not preserved anatomy. No fossil images embedded.
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
parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('pyrotherium',P['seed']); ROOT=bpy.data.objects[COL['asset_root']]
M={n:make_material(n,c,roughness=.84 if n!='eye' else .3) for n,c in P['palette'].items()}
FORMS=[]
def loft_y(name,sections,mat=None,n=24):
    verts=[];faces=[]
    for y,z,wx,hz in sections:
        for j in range(n):
            a=2*math.pi*j/n; verts.append((wx*math.cos(a),y,z+hz*math.sin(a)))
    for i in range(len(sections)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.extend([tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))])
    return mesh_object(name,verts,faces,mat or M['skin'],COL)
def loft_z(name,sections,mat=None,n=20):
    verts=[];faces=[]
    for z,x,y,wx,dy in sections:
        for j in range(n):
            a=2*math.pi*j/n;verts.append((x+wx*math.cos(a),y+dy*math.sin(a),z))
    for i in range(len(sections)-1):
        for j in range(n):faces.append((i*n+j,(i+1)*n+j,(i+1)*n+(j+1)%n,i*n+(j+1)%n))
    faces.extend([tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))])
    return mesh_object(name,verts,faces,mat or M['skin'],COL)
def tube(name,points,mat,n=14):
    # Parallel-transport-like stable frames; each point is x,y,z,radius.
    verts=[];faces=[]
    for i,p in enumerate(points):
        c=Vector(p[:3]); t=Vector(points[min(i+1,len(points)-1)][:3])-Vector(points[max(i-1,0)][:3]);t.normalize()
        u=t.cross(Vector((1,0,0))).normalized();v=t.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n; q=c+p[3]*(u*math.cos(a)+v*math.sin(a));verts.append(tuple(q))
    for i in range(len(points)-1):
        for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))])
    return mesh_object(name,verts,faces,mat,COL)
def ellipsoid(name,center,scale,mat,segments=16,rings=10):
    cx,cy,cz=center;sx,sy,sz=scale;verts=[(cx,cy,cz-sz)];faces=[]
    for i in range(1,rings):
        v=-math.pi/2+math.pi*i/rings
        for j in range(segments):
            a=2*math.pi*j/segments;verts.append((cx+sx*math.cos(v)*math.cos(a),cy+sy*math.cos(v)*math.sin(a),cz+sz*math.sin(v)))
    top=len(verts);verts.append((cx,cy,cz+sz))
    for j in range(segments):faces.append((0,1+(j+1)%segments,1+j))
    for i in range(rings-2):
        off=1+i*segments
        for j in range(segments):faces.append((off+j,off+(j+1)%segments,off+segments+(j+1)%segments,off+segments+j))
    off=1+(rings-2)*segments
    for j in range(segments):faces.append((off+j,off+(j+1)%segments,top))
    return mesh_object(name,verts,faces,mat,COL)
# Deep elongated barrel, modest shoulder crown, low abdomen and broad rump.
FORMS.append(loft_y('Deep_barrel_profile',[
 (-.88,1.03,.12,.18),(-.73,1.05,.33,.36),(-.52,1.00,.46,.46),(-.22,.98,.54,.48),
 (.18,.97,.56,.47),(.57,1.00,.53,.45),(.89,1.02,.46,.40),(1.14,1.02,.32,.33),(1.27,1.03,.10,.18)]))
FORMS.append(loft_y('Powerful_neck',[
 (-1.13,1.18,.17,.24),(-.96,1.15,.25,.29),(-.78,1.12,.31,.31),(-.57,1.09,.33,.31)]))
# The head narrows strongly anteriorly; cranium is elongate, not elephant-like globular.
FORMS.append(loft_y('Long_narrow_cranium',[
 (-1.67,1.075,.103,.09),(-1.57,1.10,.135,.14),(-1.45,1.16,.154,.17),
 (-1.29,1.23,.186,.225),(-1.12,1.29,.207,.24),(-.96,1.30,.20,.22),(-.85,1.29,.14,.16)],n=26))
FORMS.append(loft_y('Heavy_procumbent_mandible',[
 (-1.67,.87,.095,.055),(-1.57,.87,.14,.09),(-1.42,.90,.176,.12),(-1.24,.96,.20,.15),(-1.05,1.05,.18,.17),(-.95,1.12,.11,.12)]))
for s,label in [(-1,'L'),(1,'R')]:
    FORMS.append(ellipsoid('Zygomatic_cheek_'+label,(s*.17,-1.17,1.12),(.10,.18,.16),M['skin']))
    FORMS.append(loft_z('Stout_forelimb_'+label,[
      (.04,s*.38,-.57,.145,.18),(.17,s*.38,-.53,.13,.14),(.38,s*.38,-.48,.115,.125),
      (.64,s*.39,-.41,.15,.17),(.89,s*.35,-.47,.205,.22),(1.14,s*.28,-.49,.20,.21),(1.34,s*.20,-.47,.13,.14)]))
    FORMS.append(loft_z('Stout_hindlimb_'+label,[
      (.04,s*.38,.91,.15,.19),(.18,s*.38,.97,.13,.15),(.40,s*.39,1.0,.12,.13),
      (.66,s*.39,.84,.17,.18),(.90,s*.35,.74,.23,.24),(1.14,s*.28,.77,.21,.23),(1.30,s*.17,.80,.13,.15)]))
    for leg,y in [('Fore',-.57),('Hind',.91)]:
        FORMS.append(loft_z(leg+'_broad_plantigrade_mass_'+label,[
          (0,s*.38,y-.035,.157,.205),(.035,s*.38,y-.045,.17,.22),(.105,s*.38,y-.025,.164,.19),(.19,s*.38,y+.03,.13,.14)]))
# Editable semantic pre-union forms are retained separately, never exported.
SC=bpy.data.collections.new('SOURCE_FORMS');bpy.context.scene.collection.children.link(SC)
for ob in FORMS:
    cp=ob.copy();cp.data=ob.data.copy();cp.name='EDIT_'+ob.name;cp.parent=None;SC.objects.link(cp);cp.hide_render=True;cp.hide_set(True)
SC.hide_render=True;SC.hide_viewport=True
bpy.ops.object.select_all(action='DESELECT')
for ob in FORMS:ob.select_set(True)
bpy.context.view_layer.objects.active=FORMS[0];bpy.ops.object.join();body=FORMS[0];body.name='Unified_original_body_skin'
r=body.modifiers.new('Skin_union','REMESH');r.mode='VOXEL';r.voxel_size=P['voxel_size_m'];r.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=r.name)
r=body.modifiers.new('Restrained_relaxation','SMOOTH');r.factor=.45;r.iterations=3;bpy.ops.object.modifier_apply(modifier=r.name)
body.data.calc_loop_triangles();d=body.modifiers.new('Refined_lowpoly_facets','DECIMATE');d.ratio=min(1,P['body_triangle_target']/len(body.data.loop_triangles));d.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=d.name)
minimum=min(v.co.z for v in body.data.vertices)
for v in body.data.vertices:v.co.z=max(0.,v.co.z-minimum)
body.data.materials.clear();body.data.materials.append(M['skin']);body.data.materials.append(M['under'])
for poly in body.data.polygons:
    c=poly.center
    if -.48<c.y<.95 and c.z<.67:poly.material_index=1
body['anatomical_status']='Original whole-body estimate; no articulated complete skeleton used'
body['ground_shift_m']=-minimum
# Short proboscis is an explicitly uncertain soft-tissue choice above the tusk arcade.
trunk=tube('Short_proboscis_concept',[(0,-1.36,1.41,.115),(0,-1.48,1.40,.103),(0,-1.59,1.35,.088),(0,-1.67,1.27,.073),(0,-1.70,1.20,.066)],M['nose'],18)
trunk['claim']='Soft-tissue length unpreserved; alternative to Billet large-trunk inference'
# Six separate incisor meshes. Beveled non-needle tips are original reconstructions.
for s,label in [(-1,'L'),(1,'R')]:
    tube('Upper_I1_'+label,[(s*.068,-1.61,1.047,.038),(s*.074,-1.72,1.012,.036),(s*.079,-1.83,.977,.029),(s*.082,-1.91,.955,.016)],M['ivory'],10)
    tube('Upper_I2_'+label,[(s*.150,-1.50,1.072,.043),(s*.171,-1.62,1.035,.040),(s*.187,-1.73,.996,.031),(s*.194,-1.82,.971,.018)],M['ivory'],10)
    tube('Lower_I1_'+label,[(s*.110,-1.60,.826,.036),(s*.119,-1.72,.853,.033),(s*.131,-1.82,.888,.026),(s*.140,-1.91,.921,.014)],M['ivory'],10)
    ellipsoid('Small_inferred_ear_'+label,(s*.224,-.949,1.43),(.085,.046,.108),M['skin'],16,10)
    ellipsoid('Ear_concha_'+label,(s*.235,-.987,1.439),(.052,.014,.068),M['ear'],14,8)
    ellipsoid('Eye_rim_'+label,(s*.185,-1.315,1.332),(.029,.034,.028),M['nose'],14,8)
    ellipsoid('Dark_eye_'+label,(s*.205,-1.329,1.336),(.017,.021,.019),M['eye'],14,8)
    ellipsoid('Nostril_'+label,(s*.026,-1.754,1.211),(.014,.011,.012),M['eye'],10,6)
# Tail and discreet lip line; no false reconstructed digit-count or toenail claim.
tube('Inferred_moderate_tail',[(0,1.20,1.10,.072),(.025,1.37,.97,.051),(.06,1.51,.80,.034),(.09,1.58,.70,.018),(.10,1.60,.68,.006)],M['skin'],12)
loft_y('Mouth_seam',[(-1.65,.956,.10,.007),(-1.53,.958,.145,.008),(-1.39,.99,.167,.007),(-1.25,1.035,.195,.004)],M['nose'],20)
for ob in COL.all_objects:
    if ob.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    for poly in ob.data.polygons:poly.use_smooth=False
bpy.context.view_layer.update();source=audit_source(COL,16000)
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.scene['source_generator']='source/generate.py'
bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
# Store portable authoring defaults rather than environment-specific UI paths.
bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'
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
b=source['bounds_blender_m'];exp={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-exp[k][i]) for k in ('min','max') for i in range(3))
if delta>1e-4 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source/export mismatch')
glb['file']='model.glb'
record={'asset_id':'pyrotherium','revision':'r001','blender':bpy.app.version_string,'seed':P['seed'],
 'glb_sha256':glb['sha256'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,
 'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},
 'source_forms_excluded':len(SC.objects),'threads':2,'incisor_meshes':6,
 'notes':['Original construction lofts retained outside EXPORT.','Short proboscis, body, ears and tail are explicitly conjectural.','No digit-count claim; broad supporting foot masses only.']}
(OUT/'build-report.json').write_text(json.dumps(record,indent=2)+'\n')
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
