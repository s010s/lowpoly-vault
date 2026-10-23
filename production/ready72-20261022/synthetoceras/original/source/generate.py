# SPDX-License-Identifier: MIT
"""Deterministic Synthetoceras whole-animal reconstruction. Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python generate.py -- --output-dir OUTPUT
Source helpers are bundled; no network, textures, or other candidate dependencies.
"""
import argparse, hashlib, json, math, os, shutil, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',required=True); ap.add_argument('--clay',action='store_true')
a=ap.parse_args(args); OUT=Path(a.output_dir).resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=ac.setup_scene(P['asset_id'],seed=P['seed'])
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
M={n:ac.make_material(n,c,roughness=0.86 if n!='eye' else 0.30) for n,c in P['palette'].items()}

def loft(name, nodes, material, sides=12, triangulate=False):
    # nodes: x,y,z, transverse radius, sagittal radius. Local transverse basis
    # is kept in X for sagittal paths, avoiding arbitrary twist.
    vs=[]; fs=[]
    for j,node in enumerate(nodes):
        p=Vector(node[:3]); before=Vector(nodes[max(0,j-1)][:3]); after=Vector(nodes[min(len(nodes)-1,j+1)][:3]); tangent=(after-before).normalized()
        u=Vector((1,0,0)); u=(u-tangent*u.dot(tangent)).normalized()
        if u.length<.1: u=Vector((0,1,0)); u=(u-tangent*u.dot(tangent)).normalized()
        v=tangent.cross(u).normalized()
        for k in range(sides):
            th=2*math.pi*k/sides
            vs.append(tuple(p+u*(math.cos(th)*node[3])+v*(math.sin(th)*node[4])))
    for j in range(len(nodes)-1):
        for k in range(sides):
            aa=j*sides+k; bb=j*sides+(k+1)%sides; cc=(j+1)*sides+(k+1)%sides; dd=(j+1)*sides+k
            if triangulate and (j+k)%2: fs.extend([(aa,bb,dd),(bb,cc,dd)])
            else: fs.append((aa,bb,cc,dd))
    vs.append(tuple(nodes[0][:3])); start=len(vs)-1
    vs.append(tuple(nodes[-1][:3])); end=len(vs)-1
    for k in range(sides): fs.append((start,(k+1)%sides,k)); fs.append((end,(len(nodes)-1)*sides+k,(len(nodes)-1)*sides+(k+1)%sides))
    return ac.mesh_object(name,vs,fs,M[material],C)

def unify(name, objects, voxel, ratio, mat):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]; bpy.ops.object.join(); ob=objects[0]; ob.name=name
    mod=ob.modifiers.new('Anatomical continuous surface','REMESH'); mod.mode='VOXEL'; mod.voxel_size=voxel; mod.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=mod.name)
    sm=ob.modifiers.new('Gentle contour blend','SMOOTH'); sm.factor=.55; sm.iterations=3; bpy.ops.object.modifier_apply(modifier=sm.name)
    dec=ob.modifiers.new('Deliberate low-poly surface','DECIMATE'); dec.ratio=ratio; dec.use_collapse_triangulate=True
    bpy.ops.object.modifier_apply(modifier=dec.name)
    ob.data.materials.clear(); ob.data.materials.append(M[mat]); ob.data.shade_flat(); return ob

# Shoulder, ribcage and rump use distinct profiles rather than scaled spheres.
flesh=[]
flesh.append(loft('ribcage',[(0,-.48,.86,.07,.12),(0,-.41,.87,.16,.22),(0,-.29,.86,.205,.255),(0,-.08,.83,.23,.255),(0,.15,.82,.24,.24),(0,.38,.84,.215,.23),(0,.55,.85,.17,.20),(0,.64,.85,.055,.11)],'coat',16))
flesh.append(loft('neck',[(0,-.34,.84,.16,.17),(0,-.43,1.00,.145,.155),(0,-.48,1.14,.115,.135),(0,-.57,1.27,.087,.105),(0,-.64,1.36,.073,.085)],'coat',14))
flesh.append(loft('elongated-cranium',[(0,-.605,1.36,.047,.063),(0,-.665,1.365,.087,.097),(0,-.73,1.35,.081,.086),(0,-.81,1.325,.061,.064),(0,-.90,1.30,.051,.053),(0,-.975,1.285,.057,.044),(0,-1.015,1.286,.045,.031)],'coat',14))
# Four continuous limbs, with distinct fore-knee and hind hock angular breaks.
legdefs=[]
for side in (-1,1):
    # Small stance asymmetry keeps both hoof pairs readable in side projection.
    x=side*.153; off=.035 if side==1 else -.035
    nodes=[(x,-.32,.87,.108,.11),(side*.167,-.35+off,.69,.070,.075),(side*.166,-.32+off,.49,.043,.046),(side*.171,-.35+off,.38,.031,.034),(side*.173,-.36+off,.18,.027,.030),(side*.174,-.385+off,.08,.038,.040)]
    flesh.append(loft(('right' if side==1 else 'left')+'-foreleg',nodes,'coat',10)); legdefs.append((side*.174,-.395+off,'fore'))
    nodes=[(side*.155,.45,.86,.12,.15),(side*.177,.36+off,.68,.083,.105),(side*.18,.43+off,.51,.047,.064),(side*.183,.56+off,.37,.036,.044),(side*.183,.52+off,.22,.027,.032),(side*.183,.485+off,.08,.037,.040)]
    flesh.append(loft(('right' if side==1 else 'left')+'-hindleg',nodes,'coat',10)); legdefs.append((side*.183,.475+off,'hind'))
# Continuous original construction surfaces preserved before union for editing.
construction=bpy.data.collections.new('CONSTRUCTION_EDITABLE'); bpy.context.scene.collection.children.link(construction)
for ob in flesh:
    cp=ob.copy(); cp.data=ob.data.copy(); cp.name='design-'+ob.name; construction.objects.link(cp); cp.hide_render=True; cp.hide_viewport=True; cp.hide_set(True); cp.parent=None
body=unify('connected-body-neck-head-four-limbs',flesh,P['body_voxel_m'],P['body_decimate'],'coat')
body.data.materials.append(M['underside']); body.data.materials.append(M['dorsal'])
for poly in body.data.polygons:
    c=poly.center
    if (-.29<c.y<.40 and .54<c.z<.665 and abs(c.x)<.14) or (-.61<c.y<-.39 and .90<c.z<1.24 and abs(c.x)<.055 and poly.normal.y<-.25): poly.material_index=1
    elif (-.28<c.y<.54 and c.z>1.015) or c.z<.32:poly.material_index=2
# Four split hoof contacts: two separate, closed low-poly toes per foot.
def toe(name,x,y):
    rings=[(x,y,.0,.021,.052),(x,y,.026,.025,.053),(x,y+.012,.070,.021,.033),(x,y+.015,.085,.013,.022)]
    # Vertical rings use sagittal radius along Y.
    return loft(name,rings,'horn-hoof',8)
for i,(x,y,kind) in enumerate(legdefs):
    toe(kind+str(i)+'-inner-toe',x-.024,y); toe(kind+str(i)+'-outer-toe',x+.024,y)
# Short tail follows rump, not a long antelope flag.
loft('short-tail',[(0,.585,.93,.052,.054),(0,.69,.93,.043,.043),(0,.765,.88,.033,.035),(0,.80,.81,.019,.024),(0,.798,.785,.004,.005)],'dorsal',10)
# One long anterior nasal shaft. The fork appears only distally.
nh=[]
nh.append(loft('nasal-single-midline-shaft',[(0,-.936,1.325,.041,.044),(0,-.993,1.41,.035,.035),(0,-1.09,1.53,.029,.030),(0,-1.167,1.64,.026,.027),(0,-1.162,1.705,.029,.028)],'horn-hoof',12))
for s in (-1,1):
    nh.append(loft('nasal-distal-branch-'+str(s),[(0,-1.164,1.67,.025,.026),(s*.050,-1.160,1.73,.025,.026),(s*.11,-1.146,1.80,.020,.020),(s*.16,-1.118,1.855,.011,.012),(s*.175,-1.093,1.88,.0025,.003)],'horn-hoof',10))
nasal=unify('single-nasal-shaft-with-terminal-Y-fork',nh,P['horn_voxel_m'],P['horn_decimate'],'horn-hoof')
nasal['anatomy']='One midline rostral root; bifurcation only near distal end; no extra tines.'
for s in (-1,1):
    loft(('right' if s==1 else 'left')+'-postorbital-horn',[(s*.062,-.664,1.435,.033,.036),(s*.125,-.642,1.463,.029,.031),(s*.201,-.627,1.49,.026,.028),(s*.244,-.597,1.55,.023,.024),(s*.246,-.574,1.62,.019,.020),(s*.220,-.556,1.684,.014,.016),(s*.178,-.549,1.727,.008,.009),(s*.155,-.551,1.744,.002,.003)],'horn-hoof',10)
# Small lateral ears behind the horn bases. Front and back are closed, not cards.
def ear(s):
    coords=[(s*.060,-.583,1.400),(s*.117,-.560,1.444),(s*.241,-.514,1.528),(s*.238,-.548,1.463),(s*.161,-.586,1.397),(s*.089,-.599,1.382),(s*.158,-.554,1.444),(s*.153,-.584,1.443)]
    faces=[(0,1,6),(1,2,6),(2,3,6),(3,4,6),(4,5,6),(5,0,6),(1,0,7),(2,1,7),(3,2,7),(4,3,7),(5,4,7),(0,5,7)]
    ob=ac.mesh_object(('right' if s==1 else 'left')+'-ear',coords,faces,[M['coat'],M['underside']],C)
    for p in ob.data.polygons:p.material_index=1 if p.index<6 else 0
for s in (-1,1):ear(s)
# Alert lateral eyes, discreet muzzle and nostrils. No human-like eyelids.
for s in (-1,1):
    loft(('right' if s==1 else 'left')+'-eye',[(s*.071,-.724,1.378,.006,.009),(s*.084,-.724,1.378,.014,.016),(s*.087,-.724,1.378,.003,.004)],'eye',10)
loft('soft-nasal-pad',[(0,-.997,1.287,.043,.028),(0,-1.020,1.285,.048,.027),(0,-1.028,1.285,.033,.019)],'horn-hoof',12)
# Anatomical mouth line in relief, restrained and closed, each side.
for s in (-1,1):
    loft(('right' if s==1 else 'left')+'-mouth',[(s*.044,-.989,1.265,.002,.002),(s*.053,-.953,1.261,.0022,.0022),(s*.052,-.910,1.263,.001,.001)],'horn-hoof',6)
# Source contract, clean authoring file, explicit portable export flags.
bpy.context.view_layer.update()
source=ac.audit_source(C,max_triangles=P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene['description']='Original complete Synthetoceras reconstruction. Coat and body proportions are artistic; diagnostic horn topology follows FAM33407.'
bpy.context.scene['blender_version_pinned']='4.3.2'; bpy.context.scene['seed']=P['seed']
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in C.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
flags=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
assert not set(flags)-available
bpy.ops.export_scene.gltf(**flags)
q=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(q['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
assert not q['errors'] and delta<1e-4 and q['scene_triangles']==source['triangles'] and q['bytes']<=P['budgets']['max_glb_bytes'],q
report={'status':'PASS','source':source,'glb':q,'bounds_delta_m':delta,'runtime':{'blender':bpy.app.version_string,'threads':2,'gltf_exporter':'4.3.47'},'export_options':{k:v for k,v in flags.items() if k!='filepath'},'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'gpu':'NOT_RUN','independent_review':'NOT_RUN'}
(OUT/'build-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
if a.clay:
    for ob in C.all_objects:
        if ob.type=='MESH':
            ob.data.materials.clear(); ob.data.materials.append(ac.make_material('_gray_'+ob.name,'#96958F'))
    ac.render_previews(C,OUT/'gray',views=('front','side','hero'),resolution=512,samples=8)
print('SYNTHETOCERAS_BUILD_OK',q['sha256'],q['scene_triangles'],q['bytes'])
