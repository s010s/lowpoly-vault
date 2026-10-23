#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Eryon cuvieri: original conservative whole-animal reconstruction.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
Only Blender, Python stdlib, params.json, and declared local deps are required.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
args=argparse.ArgumentParser()
args.add_argument('--output',type=Path,required=True)
args.add_argument('--params',type=Path,default=HERE/'params.json')
args.add_argument('--clay',action='store_true')
a=args.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output.mkdir(parents=True,exist_ok=True)
p=json.loads(a.params.read_text())
c=setup_scene(p['asset_id'],p['seed'])
root=bpy.data.objects[c['asset_root']]
root['taxon']='Eryon cuvieri Desmarest, 1817'
root['specimen_anchor']='MNHN.F.A32407; Charbonnier et al. 2012, Fig. 1'
root['interpretation']='Living restoration; thickness, pose and colour inferred; not a scan'
root['mount']='Grounded walking stance; foot tips at Blender Z=0; origin at carapace centre projection'
root['carapace_length_m']=p['carapace_length']
root['uropodal_exopod_length_m']=p['uropodal_exopod_length']
palette=p['palette_srgb']
mats={k:make_material(k,'#929292' if a.clay else v,roughness=.82 if k!='eye' else .46) for k,v in palette.items()}
parts=[]
# All modeling coordinates below are millimeters, explicitly converted to meters.
def mesh(name,verts,faces,mat,semantic=None):
    o=mesh_object(name,[(x*.001,y*.001,z*.001) for x,y,z in verts],faces,mats[mat],c)
    o['anatomical_part']=semantic or name
    parts.append(o)
    return o

def tube(name,path,radii,mat='limb',sides=8,flat=.82):
    # Deliberate polyhedral swept segments, capped and independent at anatomical joints.
    pts=[Vector(v) for v in path]; vs=[]; fs=[]
    for i,pt in enumerate(pts):
        direction=pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]
        direction.normalize(); ref=Vector((0,0,1))
        if abs(direction.dot(ref))>.95: ref=Vector((1,0,0))
        u=direction.cross(ref).normalized(); v=direction.cross(u).normalized()
        for j in range(sides):
            ang=2*math.pi*j/sides
            vv=pt+radii[i]*(math.cos(ang)*u+flat*math.sin(ang)*v)
            vs.append(tuple(vv))
    fs.append(tuple(reversed(range(sides))))
    for i in range(len(pts)-1):
        for j in range(sides): fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    fs.append(tuple(range((len(pts)-1)*sides,len(pts)*sides)))
    return mesh(name,vs,fs,mat)

def lens(name,outline,zbottom,ztop,mat='shell',dome=.8):
    # Closed low-poly lamina: exact outline rim, inset dorsal rings and flattened underside.
    n=len(outline); cx=sum(x for x,y in outline)/n; cy=sum(y for x,y in outline)/n
    specs=[(.96,zbottom),(1,zbottom+(ztop-zbottom)*.2),(.92,zbottom+(ztop-zbottom)*.58),(.65,zbottom+(ztop-zbottom)*.9),(.25,ztop)]
    vs=[]; fs=[]
    for scale,z in specs:
        for x,y in outline:
            if name.startswith('Carapace__') and scale in (.92,.65,.25):
                # Notches affect the peripheral rim, not deep grooves across the entire shield.
                u=(x-cx)/28.5; v=(y-cy)/25.25; norm=math.hypot(u,v)
                inner={.92:.74,.65:.43,.25:.16}[scale]
                vs.append((cx+28.5*u/norm*inner,cy+25.25*v/norm*inner,z))
            else: vs.append((cx+(x-cx)*scale,cy+(y-cy)*scale,z))
    fs.append(tuple(reversed(range(n))))
    for j in range(len(specs)-1):
        for i in range(n): fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    fs.append(tuple(range((len(specs)-1)*n,len(specs)*n)))
    return mesh(name,vs,fs,mat)

# A broad subcircular dorsal shield with two real incisions on EACH side.
right=[(0,-25.25),(7,-24.5),(13.7,-22),(19.4,-18.7),(24.4,-14.8),(25.8,-11.8),(20.1,-9.4),(26.9,-7.3),(28.5,-1.8),(27.7,4.6),(21.8,7.5),(26.1,10.1),(24.6,15.2),(20.2,20.1),(13.1,23.9),(6.1,25),(0,25.25)]
outline=right+[(-x,y) for x,y in right[-2:0:-1]]
shell=lens('Carapace__two_incisions_each_side',outline,7.0,19.0)
shell['length_m']=.0505; shell['width_m']=.057; shell['depth_m']=.012
# Subtle margin contrast follows the same outline without bridging the incisions.
for side in (-1,1):
    for j,(i0,i1) in enumerate(((1,5),(7,9),(11,15))):
        path=[(side*right[i][0]*.99,right[i][1]*.99,9.0) for i in range(i0,i1+1)]
        tube(f'Carapace_margin_{side}_{j}',path,[.42]*len(path),'margin',6,.65)
# Weak ridges only, no invented high carinae.
for side in (-1,1):
    tube(f'Weak_branchial_ridge_{side}',[(side*5,1,18.65),(side*7,7,18.4),(side*6,14,17.8)],[.30,.38,.18],'shell',6,.55)
# Underlying segmented abdomen, visibly exposed beyond the shield.
tube('Abdomen_flexible_ventral_axis',[(0,22,8.2),(0,31,7.8),(0,45,6.5),(0,60,5.0)],[8.5,8.0,6.8,4.5],'ventral',12,.46)
for idx,(y,w) in enumerate(zip((28,34,40,46,52,58),(22.5,21.5,20,18.5,16.5,14.0)),1):
    length=5.35 if idx<6 else 5.5
    # Curved tergite with tapering pleural side corners, not disconnected beads.
    outline_seg=[(-.40*w,y-length/2),(.40*w,y-length/2),(.50*w,y-.2),(.47*w,y+length*.36),(.30*w,y+length*.51),(-.30*w,y+length*.51),(-.47*w,y+length*.36),(-.50*w,y-.2)]
    top=14.1-(idx-1)*.90; bottom=5.7-(idx-1)*.3
    o=lens(f'Abdominal_segment_{idx:02d}',outline_seg,bottom,top,'shell')
    o['segment_index']=idx
    tube(f'Tergite_posterior_edge_{idx:02d}',[(-w*.36,y+length*.37,top-1.5),(0,y+length*.42,top-.2),(w*.36,y+length*.37,top-1.5)],[.25,.3,.25],'margin',6,.55)
# Telson and paired biramous uropods: petaloid outer exopods, no transverse diaeresis.
lens('Tail_telson', [(-3.4,59.6),(3.4,59.6),(3.5,63.6),(2.0,68.7),(0,69.75),(-2.0,68.7),(-3.5,63.6)],3.0,6.5,'margin')
for side in (-1,1):
    base=Vector((side*4.4,59.4,0))
    for kind,direction,L,W,z in [('exopod',(side*.80,.60,0),9.7,4.8,5.1),('endopod',(side*.38,.925,0),9.4,3.8,5.6)]:
        d=Vector(direction).normalized(); u=Vector((d.y,-d.x,0)); points=[]
        # Petal widens distally then rounds to a narrow tip.
        for t,w in [(0,-.18),(.25,-.42),(.62,-.52),(.88,-.38),(1,0),(.88,.38),(.62,.52),(.25,.42),(0,.18)]:
            q=base+d*(t*L)+u*(w*W); points.append((q.x,q.y))
        o=lens(f'Uropod_{kind}_{"L" if side<0 else "R"}',points,2.8,z,'margin')
        o['lobe_length_m']=L*.001; o['diaeresis']=False
        tube(f'Uropod_longitudinal_rib_{kind}_{side}',[(base.x+d.x*1,base.y+d.y*1,z-.4),(base.x+d.x*7,base.y+d.y*7,z-.3)],[.23,.13],'shell',6,.5)
# Five pairs, successively shorter; only P1-4 carry a true two-digit chela.
# P1 path is deliberately long/slender rather than the obsolete 'short pincers' interpretation.
legdata=[
 (1,[(11,-10,9),(29,-7,7.2),(39,-19,4.9),(36,-34,3.1)],1.65,15.7),
 (2,[(14,-2,8),(32,0,6),(43,-5,3.0)],1.1,8.7),
 (3,[(14,6,7.5),(32,12,5.6),(41,13,2.3)],.98,7.7),
 (4,[(12,13,7),(28,22,4.7),(34,26,1.6)],.87,6.7),
 (5,[(10,19,6.5),(23,30,3.2),(27,37,1.1),(27.5,40,.20)],.65,0)]
for side in (-1,1):
    s='L' if side<0 else 'R'
    for idx,points,radius,clawlength in legdata:
        path=[(side*x,y,z) for x,y,z in points]
        for j in range(len(path)-1):
            a0=Vector(path[j]); b0=Vector(path[j+1]); mid=a0.lerp(b0,.48)
            fac=1-j*.17
            o=tube(f'P{idx}_{s}_limb_segment{j+1}',[a0,mid,b0],[radius*fac*.83,radius*fac,radius*fac*.70],'limb',8,.78)
            o['leg_pair']=idx; o['side']=s; o['chelate']=idx<=4
        wrist=Vector(path[-1])
        if idx<=4:
            # Conservative open chela, elongated propodus and two tapering distinct fingers.
            directions={1:(side*-.08,-1,-.075),2:(side*.48,-.88,-.16),3:(side*.92,-.39,-.20),4:(side*.84,.54,-.18)}
            d=Vector(directions[idx]).normalized(); u=Vector((-d.y,d.x,0)).normalized()
            palm_length=clawlength*.40; fingers=clawlength*.60
            palmend=wrist+d*palm_length
            rr=radius*(.94 if idx==1 else .77)
            tube(f'P{idx}_{s}_chela_propodus',[wrist,wrist.lerp(palmend,.55),palmend],[rr*.70,rr,rr*.8],'limb',8,.67)
            gap=(1.4 if idx==1 else .8)
            for digit in (-1,1):
                start=palmend+u*digit*rr*.58
                mid=palmend+d*fingers*.58+u*digit*gap
                end=palmend+d*fingers+u*digit*.27
                # Keep ground contact only on lowest tip, without sending fingers through floor.
                start.z=max(start.z,.5); mid.z=max(mid.z,.4); end.z=max(end.z,.16)
                o=tube(f'P{idx}_{s}_chela_{"fixed" if digit<0 else "movable"}',[start,mid,end],[rr*.43,rr*.31,.13],'margin',7,.75)
                o['digit']='fixed' if digit<0 else 'movable';o['leg_pair']=idx;o['side']=s
# Small anterior eye peduncles and two paired antenna/antennule systems.
for side in (-1,1):
    s='L' if side<0 else 'R'
    tube(f'Eyestalk_{s}',[(side*6,-22,12),(side*8.7,-26,12)],[.85,.75],'limb',8)
    # Faceted little eye lobe, subdued rather than cartoon spheres.
    x=side*8.7;y=-26;z=12
    lens(f'Eye_{s}',[(x-1.0,y-.9),(x+.7,y-1),(x+1,y+.65),(x-.8,y+.9)],z-.7,z+.8,'eye')
    tube(f'Antenna_base_{s}',[(side*4,-23.5,11.8),(side*5.2,-27.5,10.8)],[.65,.4],'limb',7)
    tube(f'Antenna_filament_{s}',[(side*5.2,-27.5,10.8),(side*9,-33,10),(side*15,-38.5,8.4)],[.34,.24,.10],'margin',6)
    tube(f'Antennule_base_{s}',[(side*1.7,-23.5,12),(side*2.8,-28,11.3)],[.50,.31],'limb',7)
    tube(f'Antennule_filament_{s}',[(side*2.8,-28,11.3),(side*3,-33,10),(side*1.4,-36,9.3)],[.27,.18,.08],'margin',6)
# Move all geometry so the anatomical foot contact minimum is exactly zero.
minz=min((o.matrix_world@v.co).z for o in parts for v in o.data.vertices)
for o in parts:
    for v in o.data.vertices: v.co.z-=minz
bpy.context.view_layer.update()
source=audit_source(c,40000)
if source['errors']: raise RuntimeError('Source QA errors: '+repr(source['errors']))
bpy.context.scene['generator_sha256']=sha(__file__)
bpy.context.scene['parameter_sha256']=sha(a.params)
bpy.context.scene['profile']='static-palette-v2; source semantic parts retained; export material-batched'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'model.blend'))
# Bake a material-batched export copy; never save this over editable semantic parts.
semantic=[{'name':o.name,'vertices':len(o.data.vertices),'material':o.data.materials[0].name,'properties':dict(o.items())} for o in parts]
for material in mats.values():
    objects=[o for o in c.all_objects if o.type=='MESH' and o.data.materials[0]==material]
    if not objects: continue
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    if len(objects)>1: bpy.ops.object.join()
    merged=bpy.context.view_layer.objects.active
    merged.name='Eryon_'+material.name
    merged['export_group']='Material batch; semantic component editing retained in model.blend'
    # Avoid misleading singular part metadata inherited from active object.
    for key in list(merged.keys()):
        if key!='export_group': del merged[key]
bpy.ops.object.select_all(action='DESELECT')
for o in c.all_objects: o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(a.output/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available: raise RuntimeError('Missing exporter options '+str(set(options)-available))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(a.output/'model.glb',40000,6,8)
if glb['errors']: raise RuntimeError('GLB QA errors: '+repr(glb['errors']))
if glb['scene_triangles']!=source['triangles']: raise RuntimeError('Source/export triangle mismatch')
sb=source['bounds_blender_m']; gb=glb['bounds_m']
expected={'min':[sb['min'][0],sb['min'][2],-sb['max'][1]],'max':[sb['max'][0],sb['max'][2],-sb['min'][1]]}
bounds_error=max(abs(expected[k][i]-gb[k][i]) for k in ('min','max') for i in range(3))
if bounds_error>1e-6: raise RuntimeError('Source/export bounds mismatch')
report={'status':'PASS','source_export_bounds_max_abs_error_m':bounds_error,'source':source,'glb':glb,'glb_sha256':sha(a.output/'model.glb'),'blend_sha256':sha(a.output/'model.blend'),'generator_sha256':sha(__file__),'params_sha256':sha(a.params),'blender_version':bpy.app.version_string,'exporter_options':{k:v for k,v in options.items() if k!='filepath'},'semantic_parts':semantic,'source_to_export':'Material batching only; triangle count equal; bounds checked by build audit','mode':'grey-anatomy-check' if a.clay else 'candidate','limitations':'Maker technical evidence, not independent review, GPU test, populated scene or release approval.'}
write(a.output/'build-report.json',report)
print('ERYON_BUILD_OK',json.dumps({'triangles':glb['scene_triangles'],'sha256':report['glb_sha256'],'warnings':glb['warnings']}))
