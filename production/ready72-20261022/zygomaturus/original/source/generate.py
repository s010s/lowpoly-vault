# SPDX-License-Identifier: MIT
"""Original Zygomaturus trilobus living reconstruction, deterministic Blender 4.3.2.
Semantic construction meshes are retained outside EXPORT in the editable blend.
No reference images are embedded, no file outside this source tree is read.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, link_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
A=argparse.ArgumentParser(); A.add_argument('--output-dir',type=Path,required=True)
args=A.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('zygomaturus',P['seed'])
ROOT=bpy.data.objects[COL['asset_root']]
M={n:make_material(n,c,roughness=.86 if n!='eye' else .32) for n,c in P['palette'].items()}
FORMS=[]
def loft_y(name,sections,material=None,n=20):
    # sections: y, center_z, halfwidth_x, halfheight_z; original anatomy profiles.
    verts=[]; faces=[]
    for y,z,wx,hz in sections:
        for j in range(n):
            a=2*math.pi*j/n
            verts.append((wx*math.cos(a),y,z+hz*math.sin(a)))
    for i in range(len(sections)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces += [tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]
    obj=mesh_object(name,verts,faces,material or M['coat'],COL); return obj

def loft_z(name,sections,n=16,material=None):
    # z, center_x, center_y, halfwidth_x, halfdepth_y. Supports bent limbs.
    verts=[]; faces=[]
    for z,x,y,wx,dy in sections:
        for j in range(n):
            a=2*math.pi*j/n; verts.append((x+wx*math.cos(a),y+dy*math.sin(a),z))
    for i in range(len(sections)-1):
        for j in range(n): faces.append((i*n+j,(i+1)*n+j,(i+1)*n+(j+1)%n,i*n+(j+1)%n))
    faces += [tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]
    return mesh_object(name,verts,faces,material or M['coat'],COL)

def ellipsoid(name,center,scale,mat,segments=16,rings=10):
    cx,cy,cz=center; sx,sy,sz=scale; verts=[(cx,cy,cz-sz)]; faces=[]
    for i in range(1,rings):
        v=-math.pi/2+math.pi*i/rings
        for j in range(segments):
            a=2*math.pi*j/segments
            verts.append((cx+sx*math.cos(v)*math.cos(a),cy+sy*math.cos(v)*math.sin(a),cz+sz*math.sin(v)))
    top=len(verts); verts.append((cx,cy,cz+sz))
    for j in range(segments): faces.append((0,1+(j+1)%segments,1+j))
    for i in range(rings-2):
        off=1+i*segments
        for j in range(segments): faces.append((off+j,off+(j+1)%segments,off+segments+(j+1)%segments,off+segments+j))
    off=1+(rings-2)*segments
    for j in range(segments): faces.append((off+j,off+(j+1)%segments,top))
    return mesh_object(name,verts,faces,mat,COL)

# Torso: arched spine, shoulder crown, pendulous abdomen, tapered croup.
FORMS.append(loft_y('Torso_profile',[
 (-.73,.74,.10,.17),(-.62,.72,.25,.27),(-.45,.69,.34,.31),
 (-.20,.66,.385,.33),(.12,.65,.390,.33),(.39,.66,.35,.30),
 (.61,.67,.28,.27),(.78,.65,.15,.21),(.82,.65,.035,.10)]))
FORMS.append(loft_y('Neck_slope',[
 (-.98,.74,.12,.15),(-.82,.76,.19,.22),(-.66,.77,.24,.23),(-.48,.75,.24,.22)],n=20))
# Short deep cranium; broad zygomatic mass distinct from narrower muzzle.
FORMS.append(loft_y('Cranium_profile',[
 (-1.30,.655,.09,.07),(-1.25,.675,.125,.11),(-1.16,.70,.135,.155),
 (-1.07,.735,.17,.195),(-.96,.755,.205,.205),(-.85,.77,.18,.17),(-.77,.78,.10,.10)],n=24))
FORMS.append(loft_y('Mandible_profile',[
 (-1.28,.583,.085,.035),(-1.20,.572,.115,.061),(-1.08,.580,.145,.082),
 (-.95,.61,.17,.105),(-.83,.67,.12,.10)],n=20))
for s,label in [(-1,'L'),(1,'R')]:
    # Expanded cheek regions are geometry, not painted patterns.
    FORMS.append(ellipsoid('Expanded_cheek_'+label,(s*.172,-.992,.672),(.102,.145,.151),M['coat'],20,12))
    # Broad limb roots blend into shoulder and pelvis, but joints retain direction.
    FORMS.append(loft_z('Forelimb_'+label,[
      (.045,s*.274,-.525,.091,.112),(.115,s*.278,-.49,.083,.083),
      (.29,s*.278,-.465,.075,.077),(.41,s*.281,-.405,.097,.103),
      (.60,s*.26,-.445,.123,.141),(.73,s*.237,-.45,.139,.159),(.86,s*.20,-.45,.10,.13),(.94,s*.13,-.45,.05,.08)],n=18))
    FORMS.append(loft_z('Hindlimb_'+label,[
      (.045,s*.270,.49,.095,.112),(.12,s*.270,.55,.077,.086),
      (.24,s*.273,.59,.073,.075),(.38,s*.279,.44,.105,.103),
      (.57,s*.266,.43,.146,.158),(.72,s*.232,.47,.147,.188),(.85,s*.19,.47,.10,.14),(.92,s*.12,.47,.05,.08)],n=18))
    for leg,y in [('Fore',-.525),('Hind',.49)]:
        FORMS.append(loft_z(leg+'_plantigrade_foot_'+label,[
            (0,s*.274,y-.025,.084,.116),(.035,s*.274,y-.039,.102,.133),
            (.08,s*.274,y-.015,.094,.115),(.125,s*.274,y+.025,.067,.070)],n=16))

# Preserve construction parts for anatomical editing, outside exported collection.
SC=bpy.data.collections.new('SOURCE_FORMS'); bpy.context.scene.collection.children.link(SC)
for ob in FORMS:
    cp=ob.copy(); cp.data=ob.data.copy(); cp.name='EDIT_'+ob.name; cp.parent=None
    SC.objects.link(cp); cp.hide_render=True; cp.hide_set(True)
SC.hide_render=True; SC.hide_viewport=True
# Unified watertight skin from the explicit lofts: no hidden spheres in delivery.
bpy.ops.object.select_all(action='DESELECT')
for ob in FORMS: ob.select_set(True)
bpy.context.view_layer.objects.active=FORMS[0]; bpy.ops.object.join(); body=FORMS[0]; body.name='Unified_anatomical_skin'
r=body.modifiers.new('Skin_union','REMESH'); r.mode='VOXEL'; r.voxel_size=P['voxel_size_m']; r.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=r.name)
smooth=body.modifiers.new('Conservative_surface_relaxation','SMOOTH'); smooth.factor=.5; smooth.iterations=3
bpy.ops.object.modifier_apply(modifier=smooth.name)
body.data.calc_loop_triangles(); d=body.modifiers.new('Deliberate_lowpoly_facets','DECIMATE')
d.ratio=min(1,P['body_triangle_target']/len(body.data.loop_triangles)); d.use_collapse_triangulate=True
bpy.ops.object.modifier_apply(modifier=d.name)
# Ground feet consistently, without normalizing overall size.
minimum=min(v.co.z for v in body.data.vertices)
for v in body.data.vertices: v.co.z=max(0.,v.co.z-minimum)
body.data.materials.clear(); body.data.materials.append(M['coat'])
body['construction']='Original anatomical lofts, voxel union, decimation; source forms retained separately'
body['ground_shift_m']=-minimum
# Small external details, all closed original meshes.
tail=loft_y('Short_plain_tail',[(.75,.61,.056,.058),(.84,.56,.044,.047),(.91,.50,.030,.034),(.98,.46,.012,.017),(.997,.455,.004,.005)],n=12)
for s,label in [(-1,'L'),(1,'R')]:
    # Rounded, conservative ears. No horns or tusks.
    ellipsoid('Rounded_ear_'+label,(s*.165,-.845,.935),(.047,.031,.050),M['coat'],16,10)
    ellipsoid('Ear_concha_'+label,(s*.165,-.871,.940),(.031,.012,.033),M['inner_ear'],14,8)
    # Eyes sit high and anterior to the expanded cheek; tiny catchlight not geometry.
    ellipsoid('Eye_rim_'+label,(s*.150,-1.096,.813),(.026,.029,.024),M['muzzle'],14,8)
    ellipsoid('Eye_'+label,(s*.169,-1.111,.815),(.015,.016,.015),M['eye'],14,8)
    # Nostrils shallow bilateral patches on a modest nasal pad, no protruding tube.
    ellipsoid('Nostril_'+label,(s*.059,-1.308,.694),(.020,.009,.011),M['eye'],12,8)
    # Two enlarged but short front incisors; not canines or long tusks.
    inc=loft_z('Incisor_'+label,[(.576,s*.025,-1.299,.015,.012),(.592,s*.025,-1.307,.016,.012),(.612,s*.025,-1.296,.017,.013)],n=8,material=M['ivory'])
    # Compact rounded toes with small keratin caps, not split ungulate hooves.
    for leg,y in [('Fore',-.525),('Hind',.49)]:
        caps=[]
        for k,off in enumerate([-.066,-.022,.022,.066]):
            c=ellipsoid(leg+'_nail_'+label+str(k),(s*.274+off,y-.144,.037),(.017,.029,.017),M['nail'],10,6)
            caps.append(c)
        bpy.ops.object.select_all(action='DESELECT')
        for c in caps: c.select_set(True)
        bpy.context.view_layer.objects.active=caps[0]; bpy.ops.object.join(); caps[0].name=leg+'_small_nails_'+label
# A small dark nose and narrow lip establish the short muzzle, not an elongated snout.
loft_y('Nasal_pad',[(-1.316,.682,.092,.034),(-1.297,.689,.106,.045),(-1.270,.701,.096,.042)],M['muzzle'],20)
loft_y('Mouth_line',[(-1.311,.610,.082,.006),(-1.27,.604,.112,.007),(-1.215,.604,.119,.006)],M['muzzle'],18)
# Recalculate normals, preserve intentional flat shading and identity root.
for obj in COL.all_objects:
    if obj.type!='MESH': continue
    bm=bmesh.new(); bm.from_mesh(obj.data); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(obj.data); bm.free()
    for poly in obj.data.polygons: poly.use_smooth=False
bpy.context.view_layer.update()
source=audit_source(COL,16000)
if source['errors']: raise RuntimeError(source['errors'])
# Exact public filenames established here, not inferred by later packaging.
bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene['source_generator']='source/generate.py'; bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects: ob.select_set(True)
bpy.context.view_layer.objects.active=ROOT
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
 export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
 export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available: raise RuntimeError('Unsupported export options')
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',16000,6,48)
if glb['errors']: raise RuntimeError(glb['errors'])
if glb['bytes']>2200000: raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m']; exp={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-exp[k][i]) for k in ('min','max') for i in range(3))
if delta>1e-4 or glb['scene_triangles']!=source['triangles']: raise RuntimeError('Source/export mismatch')
record={'asset_id':'zygomaturus','revision':'r001','blender':bpy.app.version_string,'seed':P['seed'],
 'glb_sha256':glb['sha256'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),
 'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,
 'export_options':{k:v for k,v in options.items() if k!='filepath'},
 'source_forms_excluded':len(SC.objects),'threads':2,'notes':['Construction forms retained outside EXPORT; no textures or reference images embedded.','Anatomical reconstruction, not a measured whole fossil.']}
(OUT/'build-report.json').write_text(json.dumps(record,indent=2)+'\n')
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
