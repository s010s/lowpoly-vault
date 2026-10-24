# SPDX-License-Identifier: MIT
"""Original Tylosaurus proriger reconstruction. Run with Blender --background --python.
Use -- --output DIR --mode build|gray|views. All model dependencies are local.
"""
from pathlib import Path
import argparse, sys, json, math, hashlib, shutil
import bpy, bmesh
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _vertices_world, _bounds, _look_at
from qa_glb import audit_glb
P = json.loads((HERE / 'params.json').read_text())
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument('--output', default=str(HERE.parent)); ap.add_argument('--mode', choices=['build','gray','views'], default='build')
A = ap.parse_args(args); OUT = Path(A.output).resolve(); OUT.mkdir(parents=True, exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, obj): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(obj, indent=2) + '\n')

def surface(name, verts, faces, mats, collection, indices=None):
    o = mesh_object(name, verts, faces, mats, collection)
    if indices:
        for face, index in zip(o.data.polygons, indices): face.material_index = index
    return o

def lens_loft(name, stations, col, mat, axis='z', n=12):
    # Stations: axis position, fore-aft centre, chord, thickness, optional vertical centre.
    v=[]; f=[]
    for pos,c,ch,th,*zz in stations:
        for j in range(n):
            a=2*math.pi*j/n
            if axis=='z': v.append((c+ch*.5*math.cos(a),th*.5*math.sin(a),pos))
            else: v.append((c+ch*.5*math.cos(a),pos,(zz[0] if zz else 0)+th*.5*math.sin(a)))
    for k in range(len(stations)-1):
        for j in range(n): f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    f += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]
    return surface(name,v,f,mat,col)

def ellipsoid(name, center, radii, col, mat, n=16, rings=8):
    v=[(center[0],center[1],center[2]+radii[2])]; f=[]
    for k in range(1,rings):
        a=math.pi*k/rings
        for j in range(n):
            b=2*math.pi*j/n
            v.append((center[0]+radii[0]*math.sin(a)*math.cos(b),center[1]+radii[1]*math.sin(a)*math.sin(b),center[2]+radii[2]*math.cos(a)))
    v.append((center[0],center[1],center[2]-radii[2])); end=len(v)-1
    for j in range(n): f.append((0,1+j,1+(j+1)%n))
    for k in range(rings-2):
        for j in range(n): f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
    for j in range(n): f.append((end,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
    return surface(name,v,f,mat,col)

def tube_path(name, points, radius, col, mat):
    v=[]; f=[]; n=6
    for i,p in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        tangent.normalize(); up=Vector((0,0,1)); across=tangent.cross(up).normalized(); vertical=across.cross(tangent).normalized()
        for j in range(n):
            a=2*math.pi*j/n; v.append(tuple(Vector(p)+radius*(math.cos(a)*across+math.sin(a)*vertical)))
    for k in range(len(points)-1):
        for j in range(n): f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    f += [tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]
    return surface(name,v,f,mat,col)

# Axial profiles are original fleshed estimates informed by the frozen specimen brief.
def axial_loft(name, stations, col, mats):
    n=P['radial_segments'];v=[];f=[];mi=[]
    for x,w,up,down,z0 in stations:
        for j in range(n):
            a=2*math.pi*j/n;s=math.sin(a)
            v.append((x,w*math.cos(a),z0+(up if s>=0 else down)*s))
    for k in range(len(stations)-1):
        for j in range(n):
            f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
            s=math.sin(2*math.pi*(j+.5)/n)
            mi.append((0 if s>.30 else 2 if s<-.46 else 1) if len(mats)==3 else (0 if s>-.2 else 1) if len(mats)==2 else 0)
    f += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))];mi += [0,0]
    return surface(name,v,f,mats,col,mi)

def join_parts(parts, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();parts[0].name=name
    return parts[0]

def cone_tooth(name,root,tip,r,col,mat):
    v=[];f=[];n=8
    # Gently recurved crowns, not large sabers or crushing bulbs.
    for t,rad in [(0,r),(.45,r*.72),(.82,r*.32)]:
        c=Vector(root).lerp(Vector(tip),t);c.x+=.003*math.sin(t*math.pi)
        for j in range(n):
            a=2*math.pi*j/n;v.append((c.x+rad*math.cos(a),c.y+rad*math.sin(a),c.z))
    v.append(tip);tipindex=len(v)-1
    f.append(tuple(reversed(range(n))))
    for k in range(2):
        for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    for j in range(n):f.append((2*n+j,2*n+(j+1)%n,tipindex))
    return surface(name,v,f,mat,col)

def profile_at(stations,x):
    for a,b in zip(stations,stations[1:]):
        if a[0]<=x<=b[0]:
            t=(x-a[0])/(b[0]-a[0]);return [a[k]*(1-t)+b[k]*t for k in range(1,5)]
    raise ValueError('Out of profile')

def jaw_transform(v):
    pivot=Vector(P['jaw_pivot']);q=Vector(v)-pivot;a=math.radians(P['jaw_open_degrees'])
    return (pivot.x+q.x*math.cos(a)+q.z*math.sin(a),pivot.y+q.y,pivot.z-q.x*math.sin(a)+q.z*math.cos(a))

def build():
    col=setup_scene(P['asset_id'],P['seed']);root=bpy.data.objects[P['asset_id']]
    root['authoring_forward']='+X';root['mount']=P['mount'];root['taxon']=P['taxon']
    root['nominal_total_length_m']=P['estimated_total_length_m'];root['scale_basis']='Approximate published USNM8898 estimate, not direct photograph measurement'
    root['inference']='Body volumes, paddle outlines, complete fin outline and coloration inferred; multi-specimen reconstruction'
    mats={k:make_material(k,c,.78 if k not in ('detail','teeth') else .45) for k,c in P['palette'].items()}
    tail=[row[:] for row in P['tail_stations']]
    length=sum(math.hypot(b[0]-a[0],b[4]-a[4]) for a,b in zip(tail,tail[1:]))
    factor=P['inferred_targets']['tail_axis_length']/length
    for row in tail:row[0]*=factor;row[4]*=factor
    root['tail_axis_length_m']=sum(math.hypot(b[0]-a[0],b[4]-a[4]) for a,b in zip(tail,tail[1:]))
    axial_loft('Robust_trunk_and_compressed_tail',list(reversed(tail[1:]))+P['trunk_stations'],col,[mats['dorsum'],mats['flank'],mats['belly']])
    head=axial_loft('Long_upper_skull_with_blunt_edentulous_rostrum',P['head_stations'],col,[mats['dorsum'],mats['flank']])
    head['rostral_gate']='Foremost 0.10 m upper tip intentionally has no teeth. Rounded projection, not a horn.'
    jaw=axial_loft('Open_lower_jaw_with_tooth_free_symphyseal_tip',P['jaw_stations'],col,[mats['flank'],mats['belly']])
    for v in jaw.data.vertices:v.co=jaw_transform(v.co)
    jaw['gape_degrees']=P['jaw_open_degrees']
    for sign,label in [(-1,'near'),(1,'far')]:
        lens_loft('Forepaddle_'+label,[(sign*.29,2.63,.40,.135,-.20),(sign*.47,2.60,.43,.12,-.29),(sign*.68,2.49,.43,.095,-.39),(sign*.90,2.34,.37,.068,-.46),(sign*1.10,2.21,.25,.043,-.49),(sign*1.235,2.16,.075,.015,-.485)],col,mats['dorsum'],'y',20)
        lens_loft('Hindpaddle_'+label,[(sign*.255,.17,.35,.115,-.16),(sign*.43,.10,.38,.10,-.23),(sign*.62,-.02,.37,.077,-.31),(sign*.81,-.17,.30,.055,-.36),(sign*.98,-.28,.19,.032,-.385),(sign*1.085,-.31,.06,.012,-.38)],col,mats['dorsum'],'y',20)
    fin=lens_loft('Restrained_vertical_hypocercal_fin',[(-.785,-4.35,.035,.012),(-.70,-4.28,.16,.035),(-.52,-4.13,.34,.065),(-.30,-3.93,.51,.095),(-.12,-3.77,.54,.105),(.03,-3.71,.47,.093),(.19,-3.84,.38,.069),(.36,-3.96,.28,.043),(.50,-4.04,.17,.025),(.59,-4.075,.04,.01)],col,mats['dorsum'],'z',20)
    fin['uncertainty']='Ventrally bent caudal support and restrained upper lobe inferred from related mosasaurs, not directly preserved Tylosaurus soft tissue.'
    details=[]
    for sign,label in [(-1,'near'),(1,'far')]:
        x=3.55;w,up,down,z0=profile_at(P['head_stations'],x);z=.157;y=sign*(w*math.sqrt(1-((z-z0)/up)**2)+.001)
        eye=ellipsoid('Eye_'+label,(x,y,z),(.041,.012,.038),col,mats['detail'],20,10)
        for face in eye.data.polygons:face.use_smooth=True
        details.append(eye)
        x=3.89;w,up,down,z0=profile_at(P['head_stations'],x);z=.155;y=sign*(w*math.sqrt(1-((z-z0)/up)**2)+.002)
        details.append(ellipsoid('Fleshy_nostril_'+label,(x,y,z),(.020,.006,.010),col,mats['detail'],12,6))
    join_parts(details,'Eyes_and_nostrils')
    axial_loft('Recessed_mouth_interior',[[3.38,.13,.065,.06,-.05],[3.52,.15,.052,.055,-.063],[3.70,.127,.041,.048,-.085],[3.92,.101,.031,.037,-.111],[4.15,.07,.021,.027,-.139],[4.32,.035,.013,.016,-.157],[4.37,.012,.006,.007,-.165]],col,[mats['mouth']])
    teeth=[]; upper_teeth=[]; lower_unposed_max=[]
    for sign,label in [(-1,'near'),(1,'far')]:
        for i in range(P['simplified_teeth_per_jaw_side']):
            x=3.52+i*(.83/11);w,up,down,z0=profile_at(P['head_stations'],x)
            z=z0-down*.64;y=sign*w*.79;h=.057*(.78+.22*math.sin(i/11*math.pi));r=.014*(.9+.1*math.sin(i/11*math.pi))
            upper=cone_tooth('Upper_'+label+'_'+str(i),(x,y,z+.004),(x-.012,y,z-h),r,col,mats['teeth']);teeth.append(upper);upper_teeth.append(upper)
            x=3.54+i*(.78/11);w,up,down,z0=profile_at(P['jaw_stations'],x);z=z0+up*.62;y=sign*w*.79
            tooth=cone_tooth('Lower_'+label+'_'+str(i),(x,y,z-.004),(x-.012,y,z+h*.88),r*.92,col,mats['teeth'])
            lower_unposed_max.append(max(v.co.x for v in tooth.data.vertices))
            for v in tooth.data.vertices:v.co=jaw_transform(v.co)
            teeth.append(tooth)
    root['upper_tooth_free_gap_m']=max(v.co.x for v in head.data.vertices)-max(v.co.x for o in upper_teeth for v in o.data.vertices)
    root['lower_unposed_tooth_free_gap_m']=P['jaw_stations'][-1][0]-max(lower_unposed_max)
    assert root['upper_tooth_free_gap_m'] >= .10 and root['lower_unposed_tooth_free_gap_m'] >= .05
    dentition=join_parts(teeth,'Forty_eight_simplified_marginal_teeth')
    dentition['rendering_choice']='Twelve visible crowns per jaw side, not a claimed dental formula.'
    dentition['upper_anterior_tooth_limit_m']=4.364
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    return col

EXPORT_OPTIONS=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)

def emit(col):
    qa=audit_source(col,P['max_triangles'])
    if qa['errors']:raise RuntimeError(str(qa['errors']))
    bpy.context.scene['asset_author']='Leon Made This / s010s'; bpy.context.scene['asset_license']='CC-BY-4.0'
    bpy.context.preferences.filepaths.save_version=0
    # Remove inherited file-browser directory hints from the editable deliverable.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type == 'FILE_BROWSER' and space.params:
                    space.params.directory = b'//'
    bpy.context.scene.render.filepath = '//'
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[P['asset_id']]
    if set(EXPORT_OPTIONS)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}:raise RuntimeError('Exporter flags unavailable')
    bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**EXPORT_OPTIONS)
    glb=audit_glb(OUT/'model.glb',P['max_triangles'],P['max_materials'],P['max_primitives'])
    glb['file']='model.glb'
    if glb['errors'] or glb['bytes']>P['max_glb_bytes']:raise RuntimeError(str(glb['errors']))
    b=qa['bounds_blender_m']; expected_min=[b['min'][0],b['min'][2],-b['max'][1]]; expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
    assert delta<.0001 and qa['triangles']==glb['scene_triangles']
    record={'status':'PASS','source':qa,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'warning_review':{'mount':'Negative Z is intended for a swimming reconstruction with an axial mount.','smooth_normals':'Eye surfaces are smooth; the body and paddles are deliberate low-poly facets.','attachments':'Solid closed fin bases and eye/seam details intentionally overlap the body at anatomical roots.'},'claim_scope':'Source geometry and static GLB inspection only; not independent factual review or GPU rendering.'}
    write(OUT/'qa/evidence/source-glb.json',record)
    return col

def import_exact():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    col=bpy.data.collections.new('EXACT_GLB'); bpy.context.scene.collection.children.link(col)
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH':
            for c in list(o.users_collection):c.objects.unlink(o)
            col.objects.link(o)
    return col

def render(col, destination, gray=False):
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=8 if gray else P['preview']['samples']; scene.cycles.use_denoising=False; scene.cycles.seed=P['seed']
    scene.render.threads_mode='FIXED';scene.render.threads=2
    size=448 if gray else P['preview']['resolution']; scene.render.resolution_x=size;scene.render.resolution_y=size;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=not gray
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral_studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4;scene.world=world
    if gray:scene.view_layers[0].material_override=make_material('Clay','#A6A6A6')
    points=_vertices_world(col); low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
    for name,direction,energy,size_factor in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size_factor*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
    d=bpy.data.cameras.new('Evidence_camera');cam=bpy.data.objects.new('Evidence_camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    rows=[];destination.mkdir(parents=True,exist_ok=True)
    for name,direction in views.items():
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points]
        width=max(p.x for p in proj)-min(p.x for p in proj);height=max(p.y for p in proj)-min(p.y for p in proj)
        shift=Vector(((max(p.x for p in proj)+min(p.x for p in proj))/2,(max(p.y for p in proj)+min(p.y for p in proj))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift
        d.ortho_scale=max(width,height)*1.18;scene.render.filepath=str(destination/(name+'.png'));bpy.ops.render.render(write_still=True)
        rows.append({'path':('private/gray/' if gray else 'views/')+name+'.png','sha256':sha(destination/(name+'.png')),'direction_blender':direction,'camera_position':list(cam.location),'orthographic_scale':d.ortho_scale,'width':size,'height':size})
    if not gray:
        shutil.copyfile(destination/'perspective.png',OUT/'preview.png')
        write(OUT/'qa/evidence/views.json',{'glb_sha256':sha(OUT/'model.glb'),'input':'Clean import of the actual delivered GLB, not source geometry','engine':'Cycles CPU','gpu_status':'UNKNOWN','samples':scene.cycles.samples,'transparent':True,'view_transform':'Standard','look':'None','views':rows,'preview_sha256':sha(OUT/'preview.png'),'preview_reuses':'views/perspective.png','render_source_sha256':sha(HERE/'generate.py')})

if A.mode=='build':emit(build())
elif A.mode=='gray':render(build(),OUT/'private/gray',True)
else:render(import_exact(),OUT/'views')
