#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Belotelson magister reconstruction. Run with Blender background mode.
Only this package's source directory and Blender are needed to rebuild the asset.
Dimensions are authored in mm below and converted once to meters. Population
means are not measurements of the photographed MPM counterpart specimen.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

argsv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=HERE.parent)
args=ap.parse_args(argsv); out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True)
p=json.loads((HERE/'params.json').read_text())
col=setup_scene('belotelson',p['seed']); root=bpy.data.objects[col['asset_root']]
root['representation']='living-reconstruction'; root['scientific_scope']='Species-level population-anchored interpretation, not a specimen replica'
root['mount']='Virtual mounting plane at the lowest appendage; swimming pose is inferred'
root['anatomy']='8 thoracopod pairs; 6 pleonal somites; 5 pleopod pairs; pointed blade-like uropods'
palette=p['palette']; mats={k:make_material(k,v,roughness=0.85 if k!='eye' else 0.45) for k,v in palette.items()}
buckets={k:{'v':[],'f':[],'parts':[]} for k in mats}; semantic=[]

def add(name,verts,faces,mat):
    b=buckets[mat]; offset=len(b['v']); b['v'].extend(verts); b['f'].extend(tuple(offset+i for i in face) for face in faces)
    b['parts'].append((name,offset,len(verts))); semantic.append({'name':name,'material':mat,'vertices':len(verts),'polygons':len(faces)})

def tube(name,points,radii,mat,sides=8):
    pts=[Vector(v) for v in points]; verts=[]; faces=[]
    for j,c in enumerate(pts):
        t=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized()
        ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((1,0,0)); u=t.cross(ref).normalized(); v=t.cross(u).normalized()
        for k in range(sides):
            a=2*math.pi*k/sides; verts.append(tuple(c+radii[j]*(math.cos(a)*u+math.sin(a)*v)))
    for j in range(len(pts)-1):
        for k in range(sides): faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    faces.extend([tuple(reversed(range(sides))),tuple((len(pts)-1)*sides+k for k in range(sides))]); add(name,verts,faces,mat)

def ellipsoid(name,center,scale,mat,rings=6,sides=12):
    c=Vector(center); verts=[tuple(c+Vector((0,0,scale[2])))]; faces=[]
    for j in range(1,rings):
        th=math.pi*j/rings
        for k in range(sides):
            a=2*math.pi*k/sides; verts.append(tuple(c+Vector((scale[0]*math.sin(th)*math.cos(a),scale[1]*math.sin(th)*math.sin(a),scale[2]*math.cos(th)))))
    end=len(verts); verts.append(tuple(c-Vector((0,0,scale[2]))))
    for k in range(sides): faces.append((0,1+k,1+(k+1)%sides))
    for j in range(rings-2):
        for k in range(sides):
            a=1+j*sides+k; b=1+j*sides+(k+1)%sides; faces.append((a,a+sides,b+sides,b))
    for k in range(sides): faces.append((end,1+(rings-2)*sides+(k+1)%sides,1+(rings-2)*sides+k))
    add(name,verts,faces,mat)

def loft(name,centers,widths,heights,mat,sides=12):
    pts=[Vector(v) for v in centers]; verts=[]; faces=[]
    for j,c in enumerate(pts):
        t=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized(); u=Vector((1,0,0)); v=u.cross(t).normalized()
        for k in range(sides):
            a=2*math.pi*k/sides; verts.append(tuple(c+u*(math.cos(a)*widths[j])+v*(math.sin(a)*heights[j])))
    for j in range(len(pts)-1):
        for k in range(sides): faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    faces.extend([tuple(reversed(range(sides))),tuple((len(pts)-1)*sides+k for k in range(sides))]); add(name,verts,faces,mat)

def plate(name,outline,thickness,mat):
    # A closed thin convex/rimmed anatomical plate, thickness in lateral X.
    verts=[(x+s*thickness/2,y,z) for s in (-1,1) for x,y,z in outline]; n=len(outline)
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    add(name,verts,faces,mat)

# Deep, laterally compressed, smooth carapace with a small anterior eye sinus.
L=p['carapace_length_population_mean']*1000; front=-L/2; back=L/2; zc=13.2
stations=[(front,2.10,3.85),(-7.35,2.75,4.35),(-4.8,3.35,4.50),(0,3.50,4.50),(5.0,3.22,4.35),(back,2.80,4.0)]
verts=[]; faces=[]; sides=16
for j,(y,w,h) in enumerate(stations):
    for k in range(sides):
        a=2*math.pi*k/sides; sn=math.sin(a); x=math.cos(a)*w
        yy=y+(1.2*math.exp(-((sn-.24)/.31)**2) if j==0 else 0)
        verts.append((x,yy,zc+sn*h))
for j in range(len(stations)-1):
    for k in range(sides): faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
faces.extend([tuple(reversed(range(sides))),tuple((len(stations)-1)*sides+k for k in range(sides))]); add('carapace_eye_notched',verts,faces,'shell')
# A restrained dorsal tone strip is geometry-coincident only along its boundary.
# Rostrum measured from the anterior carapace anchor, exactly 9.84 mm.
R=p['rostrum_length_population_mean']*1000
loft('short_narrow_rostrum',[(0,front+.25,16.45),(0,front-2,16.68),(0,front-6.8,16.48),(0,front-R,16.38)],[.78,.50,.24,.055],[.65,.33,.16,.055],'dorsal',8)
# Mouth is a simple non-diagnostic ventral plate, not another maxilliped pair.
ellipsoid('ventral_mouth_region',(0,front+.9,10.0),(1.1,.9,.45),'joint',4,8)
for sign,label in [(-1,'left'),(1,'right')]:
    tube(label+'_eye_stalk',[(sign*1.45,front+.5,14.2),(sign*2.35,front-.45,14.7)],[.34,.27],'joint')
    ellipsoid(label+'_stalked_eye',(sign*2.58,front-.65,14.88),(.70,.62,.66),'eye',6,12)
    # Two anterior antennal systems with articulated peduncles and thin flagella.
    tube(label+'_antennule',[(sign*.95,front-.3,13.5),(sign*1.3,front-2.0,13.4),(sign*2.3,front-4.2,13.65),(sign*3.9,front-7.2,14.1),(sign*5.5,front-10.4,14.55)],[.28,.24,.15,.10,.065],'antenna')
    tube(label+'_antenna',[(sign*1.65,front+.25,11.45),(sign*2.3,front-2.2,11.35),(sign*3.4,front-4.4,10.2),(sign*4.5,front-7.5,8.3),(sign*5.0,front-10.2,5.9),(sign*5.1,front-12.3,3.0),(sign*4.8,front-13.7,.65)],[.36,.30,.23,.17,.13,.10,.065],'antenna')
    # Eight uniramous thoracopods, with long merus and propodus and stout carpus.
    for i in range(8):
        y=-6.65+i*1.88; reach=3.7+1.25*math.sin(i*math.pi/7); spread=3.0+.18*i
        pts=[(sign*1.8,y,9.65),(sign*2.65,y-.5,8.8),(sign*spread,y-reach,6.2),(sign*(spread+.22),y-reach-.4,5.25),(sign*(spread+.65),y-reach-.25,1.75),(sign*(spread+.8),y-reach+.5,.75)]
        tube(f'{label}_thoracopod_{i+1:02d}',pts,[.37,.45,.40,.42,.25,.075],'joint',8)
        # Long middle segment is warmer, allowing joints to read without fake armor.
        tube(f'{label}_merus_{i+1:02d}',[pts[1],pts[2]],[.452,.402],'shell',8)
        tube(f'{label}_propodus_{i+1:02d}',[pts[3],pts[4]],[.422,.252],'shell',8)
# Six separate pleonal somites; continuous arc with small narrow articulation seams.
lengths=[3.6,3.5,3.5,3.4,3.3,3.7]; angles=[0,8,18,32,46,58]
start=Vector((0,back-.12,zc)); segments=[]
for i,(length,ang) in enumerate(zip(lengths,angles)):
    a=math.radians(ang); t=Vector((0,math.cos(a),-math.sin(a))); n=Vector((0,math.sin(a),math.cos(a)))
    w=2.82-i*.20; h=3.75-i*.23; center=start+t*length*.5
    if i>0:
        loft(f'articular_membrane_{i:02d}',[start-t*.4,start,start+t*.4],[w*.89,w*.96,w*.89],[h*.88,h*.96,h*.88],'joint',12)
    centers=[start+t*.08,center,start+t*(length-.1)]
    loft(f'pleonal_somite_{i+1:02d}',centers,[w*.94,w,w*.91],[h*.98,h,h*.90],'shell' if i%2==0 else 'dorsal',12)
    for sign,label in [(-1,'left'),(1,'right')]:
        # Deep pointed pleura, anterior excavations expressed as a concave leading rim.
        local=[(.18,-.05),(.48,-h*.7),(length*.58,-h*1.38),(length*.9,-h*.88),(length-.12,h*.2),(length*.28,h*.35)]
        outline=[tuple(start+t*u+n*v+Vector((sign*w*.87,0,0))) for u,v in local]
        plate(f'{label}_pleuron_{i+1:02d}',outline,.46,'shell' if i%2==0 else 'dorsal')
        if i<5:
            attach=start+t*length*.55-n*(h*.68)+Vector((sign*w*.56,0,0))
            stem=attach+Vector((sign*.35,-.05,-1.1))
            tube(f'{label}_pleopod_peduncle_{i+1:02d}',[tuple(attach),tuple(stem)],[.28,.23],'joint',6)
            # Simplified paired swimming flaps are interpretive, not fossil soft-tissue claims.
            path=[stem,stem+Vector((sign*.18,.25,-1.0)),stem+Vector((sign*.24,.7,-3.4)),stem+Vector((sign*.23,.9,-3.85))]
            loft(f'{label}_pleopod_flap_{i+1:02d}',[tuple(q) for q in path],[.28,.48,.31,.09],[.18,.19,.14,.08],'ventral',8)
    segments.append({'index':i+1,'center_mm':list(center),'axis':list(t),'length_mm':length})
    start=start+t*length
# Tail fan follows the distal body tangent. Outer rami are long narrow blades.
a=math.radians(63); t=Vector((0,math.cos(a),-math.sin(a))); n=Vector((0,math.sin(a),math.cos(a)))
base=start; tail_origin=list(base)
def tailpoint(x,u,z=0):return tuple(base+Vector((x,0,0))+t*u+n*z)
def tailblade(name,sections,mat):
    verts=[]; faces=[]; sides=8
    # Small living-pose ramus splay makes independent blades readable in side view.
    branch_angle=55 if 'outer_blade' in name else 72 if 'inner_spined' in name else 63
    ba=math.radians(branch_angle); bt=Vector((0,math.cos(ba),-math.sin(ba))); bn=Vector((0,math.sin(ba),math.cos(ba)))
    for x,u,w,h in sections:
        c=base+Vector((x,0,0))+bt*u;
        for k in range(sides):
            aa=2*math.pi*k/sides; verts.append(tuple(c+Vector((math.cos(aa)*w,0,0))+bn*(math.sin(aa)*h)))
    for j in range(len(sections)-1):
        for k in range(sides): faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    faces.extend([tuple(reversed(range(sides))),tuple((len(sections)-1)*sides+k for k in range(sides))]); add(name,verts,faces,mat)
tailblade('central_telson_abrupt_distal_taper',[(0,0,1.05,.40),(0,2,.85,.34),(0,5.2,.53,.25),(0,5.6,.21,.15),(0,7,.065,.065)],'dorsal')
for sign,label in [(-1,'left'),(1,'right')]:
    tailblade(label+'_outer_blade_uropod',[(sign*1.35,.1,.55,.30),(sign*1.8,2,.69,.28),(sign*2.8,5.6,.49,.21),(sign*4.15,9,.065,.065)],'shell')
    tailblade(label+'_inner_spined_uropod',[(sign*.78,.2,.43,.27),(sign*1.10,1.7,.56,.25),(sign*1.35,3.1,.38,.21),(sign*1.8,6,.065,.065)],'ventral')
    tailblade(label+'_telson_furcal_projection',[(sign*.5,5.15,.16,.13),(sign*.78,5.8,.13,.10),(sign*1.05,6.5,.055,.055)],'dorsal')

# Six portable material groups, with editable named anatomical vertex groups.
min_z=min(v[2] for b in buckets.values() for v in b['v']); shift=-min_z
for key,b in buckets.items():
    if not b['v']: continue
    verts=[(x*.001,y*.001,(z+shift)*.001) for x,y,z in b['v']]
    obj=mesh_object('anatomy_'+key,verts,b['f'],mats[key],col)
    obj['semantic_parts']=[part[0] for part in b['parts']]
    for name,offset,count in b['parts']:
        vg=obj.vertex_groups.new(name=name); vg.add(list(range(offset,offset+count)),1.0,'REPLACE')
root['mount_shift_m']=shift*.001
bpy.context.view_layer.update()
source=audit_source(col,p['budget']['max_triangles'])
if source['errors']: raise RuntimeError('Source audit failed: '+repr(source['errors']))
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'
                space.params.filename=''
# Do not pack provenance photographs or hidden external resources.
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={v.identifier for v in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available:raise RuntimeError('Missing required exporter options')
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(out/'model.glb',p['budget']['max_triangles'],p['budget']['max_materials'],p['budget']['max_primitives']); glb['file']='model.glb'
if glb['errors']: raise RuntimeError('GLB audit failed: '+repr(glb['errors']))
bb=source['bounds_blender_m']; emin=[bb['min'][0],bb['min'][2],-bb['max'][1]]; emax=[bb['max'][0],bb['max'][2],-bb['min'][1]]
delta=max(abs(glb['bounds_m'][k][i]-e[i]) for k,e in [('min',emin),('max',emax)] for i in range(3))
assert delta<1e-6 and glb['scene_triangles']==source['triangles']
assert glb['bytes']<=p['budget']['max_glb_bytes']
evidence=out/'qa'/'evidence'; evidence.mkdir(parents=True,exist_ok=True)
report={'asset_id':'belotelson','revision':'r001','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'export_options':{k:v for k,v in opts.items() if k!='filepath'},'anatomy':{'thoracic_walking_pairs':8,'abdominal_somites':6,'pleopod_pairs':5,'antennal_system_pairs':2,'carapace_length_anchor_mm':L,'rostrum_length_anchor_mm':R,'pleon_centerline_mm':sum(lengths),'outer_uropod_axial_length_mm':9,'inner_uropod_axial_length_mm':6,'outer_inner_ratio':1.5,'carapace_width_inferred_mm':7,'semantic_parts':semantic,'somites':segments,'tail_origin_unshifted_mm':tail_origin,'mount_shift_m':shift*.001},'limits':['Population means, not single-specimen measurements.','Living width, soft appendages, pigmentation and pose are inferred.','Separate anatomical solids intentionally meet or overlap at joints; no Boolean-printability claim.','CPU Blender evidence is not Three.js GPU rendering.']}
(evidence/'source-export.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'BUILT','glb_sha256':glb['sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes'],'materials':glb.get('materials'),'primitives':glb.get('scene_primitives')}))
