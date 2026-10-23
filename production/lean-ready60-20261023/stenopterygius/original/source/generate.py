# SPDX-License-Identifier: MIT
"""Original Stenopterygius reconstruction. Run with Blender --background --python.
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

# X, half width, upper height, lower height, axial Z.
BODY = [
 (-.835,.014,.022,.020,-.005),(-.76,.021,.031,.028,.005),(-.66,.034,.047,.042,.018),
 (-.55,.050,.069,.059,.023),(-.43,.071,.098,.082,.020),(-.30,.094,.130,.111,.015),
 (-.16,.115,.153,.142,.006),(-.02,.127,.168,.166,.000),(.12,.130,.171,.169,.000),
 (.26,.126,.169,.164,.005),(.39,.117,.160,.151,.012),(.49,.104,.148,.127,.018),
 (.58,.090,.129,.108,.021),(.65,.080,.110,.088,.025),(.71,.073,.087,.070,.029),
 (.77,.066,.070,.056,.028),(.83,.055,.052,.043,.024),(.89,.044,.037,.030,.019),
 (.95,.033,.024,.021,.014),(1.01,.024,.017,.015,.009),(1.07,.015,.011,.010,.005),
 (1.12,.007,.0055,.005,.002),(1.15,.0015,.0018,.0018,.000)]

def body_properties(x):
    for a,b in zip(BODY,BODY[1:]):
        if a[0] <= x <= b[0]:
            t=(x-a[0])/(b[0]-a[0]); return [a[k]*(1-t)+b[k]*t for k in range(1,5)]
    raise ValueError('Position outside body')

def create_body(col, mats):
    n=P['radial_segments']; v=[]; f=[]; mi=[]
    for x,w,up,down,z0 in BODY:
        for j in range(n):
            ang=2*math.pi*j/n; s=math.sin(ang)
            v.append((x,w*math.cos(ang),z0+(up if s>=0 else down)*s))
    for k in range(len(BODY)-1):
        for j in range(n):
            f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
            s=math.sin(2*math.pi*(j+.5)/n)
            mi.append(0 if s>.36 else 2 if s<-.52 else 1)
    f += [tuple(reversed(range(n))),tuple((len(BODY)-1)*n+j for j in range(n))]; mi += [1,1]
    return surface('Continuous_fusiform_body_and_matching_jaws',v,f,mats,col,mi)

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

def build():
    col=setup_scene(P['asset_id'],P['seed']); root=bpy.data.objects[P['asset_id']]
    root['authoring_forward']='+X'; root['mount']='Swimming axial centre'; root['taxon']='Stenopterygius quadriscissus'
    root['length_basis']='Approximate 2.3 m; not precision measurement'
    mats={k:make_material(k,c,.76 if k!='detail' else .4) for k,c in P['palette'].items()}
    body=create_body(col,[mats['dorsum'],mats['flank'],mats['belly']])
    lens_loft('Single_swept_dorsal_fin',[(.115,-.040,.46,.039),(.17,-.035,.40,.036),(.23,-.053,.29,.027),(.30,-.086,.18,.016),(.365,-.102,.068,.008),(.395,-.114,.009,.003)],col,mats['dorsum'])
    for sign,label in [(-1,'near'),(1,'far')]:
        lens_loft('Narrow_foreflipper_'+label,[(sign*.083,.520,.114,.034,-.055),(sign*.136,.499,.113,.031,-.075),(sign*.200,.468,.106,.024,-.103),(sign*.267,.433,.086,.017,-.130),(sign*.325,.406,.058,.011,-.150),(sign*.354,.399,.015,.004,-.156)],col,mats['dorsum'],'y')
        lens_loft('Small_hindflipper_'+label,[(sign*.043,-.40,.074,.024,-.026),(sign*.088,-.421,.077,.019,-.047),(sign*.137,-.448,.058,.013,-.065),(sign*.180,-.469,.033,.007,-.079),(sign*.196,-.475,.007,.003,-.082)],col,mats['dorsum'],'y')
    upper=lens_loft('Upper_caudal_membrane',[(.000,-.876,.232,.037),(.065,-.927,.168,.028),(.14,-.975,.133,.021),(.215,-1.024,.090,.014),(.278,-1.060,.040,.007),(.305,-1.077,.007,.003)],col,mats['dorsum'])
    lower=lens_loft('Lower_caudal_lobe',[(.005,-.877,.224,.037),(-.055,-.919,.170,.028),(-.12,-.984,.120,.021),(-.19,-1.054,.078,.014),(-.255,-1.112,.037,.007),(-.285,-1.145,.010,.003)],col,mats['dorsum'])
    # Combine caudal lobes into one editable semantic mesh, retaining disconnected closed shells.
    bpy.ops.object.select_all(action='DESELECT'); upper.select_set(True); lower.select_set(True); bpy.context.view_layer.objects.active=lower; bpy.ops.object.join(); lower.name='Vertical_lunate_caudal_fin'
    details=[]
    for sign,label in [(-1,'near'),(1,'far')]:
        x=.786; w,up,down,z0=body_properties(x); z=.052; y=sign*(w*math.sqrt(1-((z-z0)/up)**2)+.001)
        eye=ellipsoid('Eye_'+label,(x,y,z),(.023,.008,.0225),col,mats['detail'])
        for p in eye.data.polygons: p.use_smooth=True
        x=.930; w,up,down,z0=body_properties(x); z=.029; y=sign*(w*math.sqrt(1-((z-z0)/up)**2)+.0005)
        details.append(ellipsoid('Nostril_'+label,(x,y,z),(.006,.002,.003),col,mats['detail'],12,6))
        points=[]
        for i in range(26):
            x=.672+(1.144-.672)*i/25; w,up,down,z0=body_properties(x); z=z0-.006*(1-i/25)
            y=sign*(w*math.sqrt(max(0,1-((z-z0)/down)**2))+.0004)
            points.append((x,y,z))
        details.append(tube_path('Closed_jaw_seam_'+label,points,.00135,col,mats['detail']))
    bpy.ops.object.select_all(action='DESELECT')
    for o in details:o.select_set(True)
    bpy.context.view_layer.objects.active=details[0]; bpy.ops.object.join(); details[0].name='Fine_jaw_seams_and_nostrils'
    # Semantic parts have identity scales and root; small buried overlaps are intentional attachments.
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
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
    record={'status':'PASS','source':qa,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'warning_review':{'mount':'Negative Z is intended for a swimming reconstruction with an axial mount.','smooth_normals':'Only the small eye surfaces are smooth; the body and fins are deliberate low-poly facets.','attachments':'Solid closed fin bases and eye/seam details intentionally overlap the body at anatomical roots.'},'claim_scope':'Source geometry and static GLB inspection only; not independent factual review or GPU rendering.'}
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
