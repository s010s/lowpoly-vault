#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Thylacoleo reconstruction. Run inside Blender with -- --output DIR.
All build inputs are local to this source folder. No reference pixels are used.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
A=argparse.ArgumentParser(); A.add_argument('--output',type=Path,required=True)
a=A.parse_args(sys.argv[sys.argv.index('--')+1:])
OUT=a.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('thylacoleo',P['seed'])
M={k:make_material(k,v['hex'],v['roughness']) for k,v in P['palette_srgb'].items()}
SKIN=[]

def loft(name,sections,n=16,material='coat',skin=True):
    """Tailored cross-section skin. Each section is center, lateral, dorsal, ventral radii."""
    verts=[]; previous_vertical=None
    for j,(xyz,rx,up,down) in enumerate(sections):
        c=Vector(xyz)
        tangent=Vector(sections[min(j+1,len(sections)-1)][0])-Vector(sections[max(j-1,0)][0])
        tangent.normalize()
        lat=Vector((1,0,0)); lat=(lat-lat.dot(tangent)*tangent).normalized()
        vertical=tangent.cross(lat).normalized()
        if previous_vertical is None:
            if vertical.z<0: vertical=-vertical
        elif vertical.dot(previous_vertical)<0: vertical=-vertical
        previous_vertical=vertical.copy()
        for k in range(n):
            q=2*math.pi*k/n; z=math.sin(q)
            verts.append(tuple(c+lat*rx*math.cos(q)+vertical*(up if z>=0 else down)*z))
    faces=[]
    for j in range(len(sections)-1):
        for k in range(n):
            kn=(k+1)%n
            faces.append((j*n+k,j*n+kn,(j+1)*n+kn,(j+1)*n+k))
    faces += [tuple(reversed(range(n))),tuple((len(sections)-1)*n+k for k in range(n))]
    ob=mesh_object(name,verts,faces,M[material],COL)
    if skin: SKIN.append(ob)
    return ob

def tube(name,points,radii,depths=None,n=12,material='coat',skin=True):
    depths=depths or radii
    return loft(name,[(p,r,d,d) for p,r,d in zip(points,radii,depths)],n,material,skin)

def union_skin():
    bpy.ops.object.select_all(action='DESELECT')
    for ob in SKIN: ob.select_set(True)
    bpy.context.view_layer.objects.active=SKIN[0]
    bpy.ops.object.join(); ob=bpy.context.object; ob.name='Continuous_anatomical_skin'
    rem=ob.modifiers.new('Integrated_branch_topology','REMESH'); rem.mode='VOXEL'; rem.voxel_size=.007
    rem.use_smooth_shade=False; bpy.ops.object.modifier_apply(modifier=rem.name)
    sm=ob.modifiers.new('Restrained_transition_relaxation','SMOOTH'); sm.factor=.65; sm.iterations=5
    bpy.ops.object.modifier_apply(modifier=sm.name)
    dec=ob.modifiers.new('Anatomical_plane_budget','DECIMATE'); dec.ratio=min(1,7900/(len(ob.data.polygons)*2))
    dec.use_collapse_triangulate=True; bpy.ops.object.modifier_apply(modifier=dec.name)
    ob.data.materials.clear()
    for k in ('coat','dorsal','belly','muzzle'): ob.data.materials.append(M[k])
    for f in ob.data.polygons:
        c=f.center; f.use_smooth=False
        if c.z>.66 and c.y>-.54: f.material_index=1
        elif -.38<c.y<.34 and .32<c.z<.46 and abs(c.x)<.125 and f.normal.z<-.12: f.material_index=2
        elif c.y<-.65 and c.z<.655: f.material_index=3
        else: f.material_index=0
    # Ground only the foot contact region without translating the placement root.
    for v in ob.data.vertices:
        if v.co.z<.027: v.co.z=0
    bm=bmesh.new(); bm.from_mesh(ob.data)
    # The organic surface is one connected skin. Remove numerical micro-islands inside the union.
    groups=[]; unseen=set(bm.verts)
    while unseen:
        q=[unseen.pop()]; group=[]
        while q:
            v=q.pop();group.append(v)
            for e in v.link_edges:
                other=e.other_vert(v)
                if other in unseen: unseen.remove(other);q.append(other)
        groups.append(group)
    keep=max(groups,key=len)
    bmesh.ops.delete(bm,geom=[v for g in groups if g is not keep for v in g],context='VERTS')
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001); bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00001); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(ob.data); bm.free()
    ob.data.update()
    return ob

# Trunk, neck and head each start from explicitly authored anatomical sections.
loft('Trunk_sections',[
 ((0,-.43,.565),.083,.105,.100),((0,-.36,.557),.143,.163,.169),
 ((0,-.27,.548),.185,.202,.204),((0,-.16,.546),.198,.204,.205),
 ((0,-.02,.546),.194,.196,.191),((0,.13,.548),.173,.176,.156),
 ((0,.26,.541),.161,.161,.160),((0,.37,.515),.170,.155,.171),
 ((0,.46,.493),.121,.115,.125),((0,.53,.487),.076,.069,.073)],24)
loft('Neck_sections',[
 ((0,-.32,.568),.123,.140,.138),((0,-.43,.584),.114,.132,.135),
 ((0,-.50,.602),.107,.103,.113),((0,-.565,.603),.090,.085,.094)],20)
loft('Broad_short_cranium',[
 ((0,-.475,.606),.080,.081,.092),((0,-.52,.617),.110,.105,.119),
 ((0,-.575,.615),.126,.112,.124),((0,-.625,.605),.125,.106,.126),
 ((0,-.673,.591),.115,.092,.104),((0,-.716,.584),.093,.067,.080),
 ((0,-.757,.578),.071,.047,.059),((0,-.782,.582),.051,.035,.038)],24)
# Ears remain restrained inferred short-coat features, not large feline triangles.
for s in (-1,1):
    tube('Rounded_ear_'+str(s),[(s*.086,-.525,.681),(s*.112,-.518,.718),(s*.115,-.524,.742),(s*.106,-.535,.748)],
         [.041,.038,.026,.010],[.027,.026,.020,.008],n=12)
# Strong, unbroken tail base and a steadily thinning distal curve.
tube('Muscular_tapering_tail',[(0,.43,.505),(0,.53,.493),(.007,.64,.458),(.016,.76,.409),(.026,.87,.345),(.038,.98,.282),(.045,1.066,.258),(.047,1.086,.260)],
     [.086,.080,.068,.052,.037,.023,.010,.002],n=16)
# All roots penetrate the trunk internally before voxel union; no raised limb caps.
for s in (-1,1):
    d=-.0175 if s==1 else .0175
    tube('Forelimb_'+str(s),[(s*.068,-.28,.600),(s*.125,-.254,.519),(s*.177,-.181,.409),(s*.182,-.190,.350),(s*.190,-.244+d,.235),(s*.194,-.292+d,.120),(s*.196,-.312+d,.060)],
         [.099,.086,.067,.067,.061,.041,.043],[.112,.108,.069,.073,.066,.040,.032],n=16)
    loft('Forepalm_'+str(s),[((s*.196,-.285+d,.052),.041,.034,.028),((s*.196,-.329+d,.045),.057,.035,.030),((s*.196,-.360+d,.038),.051,.026,.020)],16)
    for k in range(4):
        x=s*(.157+.027*k); end=-.404+d+(abs(k-1.5)*.009)
        tube('Forefinger_'+str(s)+'_'+str(k),[(x,-.339+d,.040),(x,-.369+d,.037),(x,end,.031)],
             [.019,.017,.011],[.020,.018,.012],n=10)
    # Anatomical digit I is medial on BOTH paws.
    tube('Medial_forethumb_'+str(s),[(s*.151,-.307+d,.064),(s*.127,-.326+d,.068),(s*.112,-.345+d,.066)],
         [.026,.023,.017],[.026,.023,.016],n=12)
    h=.0125 if s==1 else -.0125
    tube('Hindlimb_'+str(s),[(s*.116,.350,.529),(s*.158,.333,.466),(s*.193,.226,.340),(s*.197,.223,.286),(s*.200,.314+h,.169),(s*.200,.390+h,.079),(s*.200,.391+h,.045)],
         [.104,.099,.071,.057,.039,.031,.033],[.108,.101,.073,.059,.038,.031,.021],n=16)
    loft('Plantigrade_heel_and_pes_'+str(s),[((s*.200,.415+h,.038),.029,.024,.018),((s*.200,.366+h,.038),.038,.026,.024),((s*.200,.312+h,.036),.048,.025,.022),((s*.204,.275+h,.030),.046,.022,.018)],16)
    # II and III are deliberately paired more closely than IV and V.
    for k,(xoff,yl) in enumerate(((.167,.223),(.184,.215),(.211,.211),(.239,.224))):
        tube('Hind_digit_'+str(s)+'_'+str(k+2),[(s*xoff,.295+h,.032),(s*xoff,.256+h,.028),(s*xoff,yl+h,.024)],
             [.014,.012,.0085],[.014,.011,.008],n=10)
    tube('Inferred_blunt_hallux_'+str(s),[(s*.166,.326+h,.035),(s*.141,.300+h,.030),(s*.132,.277+h,.028)],
         [.019,.016,.010],[.016,.013,.009],n=10)
CORE=union_skin()
# Solid tapered claws, gathered later into one semantic mesh per anatomical group.
CLAWS=[]
for s in (-1,1):
    d=-.0175 if s==1 else .0175
    for k in range(4):
        x=s*(.157+.027*k); end=-.404+d+abs(k-1.5)*.009
        CLAWS.append(tube('Forefinger_claw_'+str(s)+'_'+str(k),[(x,end+.006,.034),(x,end-.010,.030),(x,end-.020,.017)],
             [.0075,.005,.0008],[.007,.006,.0007],n=8,material='claw',skin=False))
    CLAWS.append(tube('Enlarged_medial_thumb_claw_'+str(s),[(s*.112,-.341+d,.069),(s*.105,-.359+d,.073),(s*.098,-.381+d,.060),(s*.098,-.399+d,.038),(s*.105,-.405+d,.018)],
         [.015,.013,.010,.006,.0009],[.014,.013,.011,.006,.0008],n=10,material='claw',skin=False))
    h=.0125 if s==1 else -.0125
    for k,(xoff,yl) in enumerate(((.167,.223),(.184,.215),(.211,.211),(.239,.224))):
        CLAWS.append(tube('Hind_claw_'+str(s)+'_'+str(k+2),[(s*xoff,yl+h+.004,.026),(s*xoff,yl+h-.009,.023),(s*xoff,yl+h-.016,.014)],
             [.005,.004,.0007],[.005,.004,.0006],n=8,material='claw',skin=False))

def patch(name,s,y,z,ry,rz,mat):
    """Inset anatomical patch ray-fitted to the continuous surface, not a floating sphere."""
    vertices=[]; count=20
    for k in range(count):
        t=2*math.pi*k/count; yy=y+ry*math.cos(t); zz=z+rz*math.sin(t)
        hit,p,n,idx=CORE.ray_cast(Vector((s*.4,yy,zz)),Vector((-s,0,0)))
        if not hit: raise RuntimeError('Missing face attachment '+name)
        vertices.append((p.x+s*.0014,yy,zz))
    hit,p,n,idx=CORE.ray_cast(Vector((s*.4,y,z)),Vector((-s,0,0)))
    vertices.append((p.x+s*.0045,y,z)); vertices.append((p.x-s*.004,y,z))
    faces=[(k,(k+1)%count,count) for k in range(count)]+[((k+1)%count,k,count+1) for k in range(count)]
    return mesh_object(name,vertices,faces,M[mat],COL)
for s in (-1,1):
    patch('Inset_eye_'+str(s),s,-.657,.652,.018,.010,'dark')
    # Thin mouth crease follows the actual broad muzzle surface.
    patch('Closed_mouth_line_'+str(s),s,-.725,.540,.046,.0025,'dark')
# Nose: broad, low relief and flattened, with a gently lobed front outline.
loft('Broad_nasal_pad',[((0,-.770,.586),.045,.020,.018),((0,-.787,.584),.046,.021,.020),((0,-.796,.583),.034,.016,.014)],12,'dark',False)
# Preserve editability with named separate anatomical claw objects, but merge small claws per limb at export source.
for s in (-1,1):
    for prefix in ('Forefinger_claw_','Hind_claw_'):
        obs=[o for o in list(COL.all_objects) if o.name.startswith(prefix+str(s)+'_')]
        bpy.ops.object.select_all(action='DESELECT')
        for o in obs:o.select_set(True)
        bpy.context.view_layer.objects.active=obs[0]; bpy.ops.object.join(); bpy.context.object.name=prefix+str(s)+'group'
for ob in list(COL.all_objects):
    if ob.type!='MESH': continue
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
bpy.context.view_layer.update()
source=audit_source(COL,P['budgets']['max_triangles'])
if source['errors']: raise RuntimeError(source['errors'])
bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene['reconstruction']='Thylacoleo carnifex; living reconstruction, uncertain soft tissues and pedal hallux tip.'
bpy.context.preferences.filepaths.save_version=0
# Neutralize factory file-browser and output-location buffers before serialization.
for scene in bpy.data.scenes:
    scene.render.filepath='_'*1023
    scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'_'*1023
                space.params.directory=b'//'

bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),compress=True)
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects: ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[COL['asset_root']]
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available: raise RuntimeError('Missing exporter options')
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**options)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if glb['errors']: raise RuntimeError(glb['errors'])
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
print('ROUNDTRIP',delta,source['triangles'],glb['scene_triangles'],source['bounds_blender_m'],glb['bounds_m'],flush=True)
assert delta<.0001 and source['triangles']==glb['scene_triangles']
assert glb['bytes']<=P['budgets']['max_glb_bytes']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Paths in public evidence are package-relative only.
glb.pop('path',None); glb['file']='model.glb'
record={'status':'PASS','scope':'Source geometry and static export only; not independent visual, browser GPU, scene, user or publication approval.','blender_version':bpy.app.version_string,'gltf_exporter_version':'4.3.47','threejs_consumer_version':'0.180.0','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':options,'inputs':{'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json')},'artifact_sha256':{'model.glb':sha(OUT/'model.glb'),'model.blend':sha(OUT/'model.blend')},'design_measurements':{'head_body_m':1.28,'tail_centerline_m':.68,'shoulder_m':.75,'head_width_m':.252,'head_length_m':.30},'dependency_closure':{'asset_common':'source/deps/asset_common.py','qa_glb':'source/deps/qa_glb.py','other_nonstandard_dependencies':['Blender bpy','Blender bmesh','Blender mathutils']},'topology_note':'Tailored loft skins and anatomical limb branches fused into one closed skin; separate ray-fitted inset facial patches and solid claws. No reference pixels or mesh traced.'}
(OUT/'build-report.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'BUILT','triangles':glb['scene_triangles'],'bytes':glb['bytes'],'semantic_sha256':glb['semantic_sha256']}))
