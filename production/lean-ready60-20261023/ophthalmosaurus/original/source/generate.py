# SPDX-License-Identifier: MIT
"""Original Ophthalmosaurus reconstruction. Run with Blender --background --python.
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
ap.add_argument('--view-names',default='front,side,top,perspective')
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
 (-1.66,.020,.035,.032,-.015),(-1.53,.037,.061,.057,-.004),(-1.38,.065,.100,.094,.005),
 (-1.20,.104,.153,.144,.013),(-1.00,.151,.218,.209,.014),(-.78,.204,.292,.278,.009),
 (-.55,.251,.364,.344,.004),(-.30,.282,.415,.395,.000),(-.06,.298,.445,.428,.000),
 (.18,.300,.450,.430,.000),(.40,.293,.442,.413,.003),(.60,.273,.411,.372,.007),
 (.78,.245,.367,.322,.013),(.94,.212,.319,.274,.022),(1.08,.181,.275,.230,.030),
 (1.20,.159,.240,.198,.036),(1.32,.142,.217,.174,.040),(1.43,.128,.197,.153,.041),
 (1.53,.110,.175,.130,.039),(1.63,.071,.092,.073,.026),(1.74,.052,.048,.042,.015),
 (1.86,.041,.036,.032,.010),(1.98,.030,.027,.024,.006),(2.09,.024,.024,.021,.004),
 (2.18,.012,.012,.011,.001),(2.25,.0015,.002,.002,.000)]

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

def body_surface_y(x,z,sign):
    w,up,down,z0=body_properties(x)
    return sign*w*math.sqrt(max(.001,1-((z-z0)/(up if z>=z0 else down))**2))

def seated_eye(label,sign,col,mat):
    # A thin conformal lens, not a protruding eyeball or an exposed bony ring.
    cx,cz=1.483,.110; rx,rz=.078,.072; n=32; rings=5
    v=[]; f=[]
    for level in [0,1]:
        v.append((cx,body_surface_y(cx,cz,sign)+sign*(.008 if level==0 else -.006),cz))
        for k in range(1,rings+1):
            r=k/rings
            for j in range(n):
                a=2*math.pi*j/n; x=cx+rx*r*math.cos(a); z=cz+rz*r*math.sin(a)
                y=body_surface_y(x,z,sign)+sign*((.002+.006*(1-r*r)) if level==0 else -.006)
                v.append((x,y,z))
    step=1+rings*n
    for off in [0,step]:
        for j in range(n):f.append((off,off+1+j,off+1+(j+1)%n))
        for k in range(rings-1):
            for j in range(n):f.append((off+1+k*n+j,off+1+(k+1)*n+j,off+1+(k+1)*n+(j+1)%n,off+1+k*n+(j+1)%n))
    for j in range(n):f.append((1+(rings-1)*n+j,1+(rings-1)*n+(j+1)%n,step+1+(rings-1)*n+(j+1)%n,step+1+(rings-1)*n+j))
    o=surface('Flesh_seated_eye_'+label,v,f,mat,col)
    for p in o.data.polygons:p.use_smooth=True
    return o

def build():
    col=setup_scene(P['asset_id'],P['seed']); root=bpy.data.objects[P['asset_id']]
    root['authoring_forward']='+X'; root['mount']='Swimming axial centre'; root['taxon']='Ophthalmosaurus icenicus'
    root['length_basis']='Nominal 4.5 m composite estimate; not a single measured individual'
    root['teeth']='Numerous small teeth are concealed by the closed jaws; not edentulous'
    root['orbit_basis']='R3013 orbit / jaw = 0.28; model orbital region 0.294 / 1.05 m; eye opening smaller'
    mats={k:make_material(k,c,.78 if k!='detail' else .42) for k,c in P['palette'].items()}
    body=create_body(col,[mats['dorsum'],mats['flank'],mats['belly']])
    lens_loft('Single_inferred_swept_dorsal_fin',[(.365,-.080,.82,.065),(.440,-.090,.69,.060),(.535,-.130,.52,.046),(.645,-.198,.34,.032),(.745,-.260,.17,.018),(.815,-.305,.055,.008),(.835,-.317,.010,.003)],col,mats['dorsum'])
    for sign,label in [(-1,'near'),(1,'far')]:
        lens_loft('Broad_foreflipper_'+label,[(sign*.203,.890,.278,.070,-.170),(sign*.290,.876,.290,.061,-.192),(sign*.410,.842,.281,.050,-.219),(sign*.540,.802,.251,.038,-.248),(sign*.660,.758,.198,.027,-.274),(sign*.755,.718,.113,.016,-.291),(sign*.806,.700,.025,.005,-.300)],col,mats['dorsum'],'y',16)
        lens_loft('Reduced_hindflipper_'+label,[(sign*.090,-1.080,.150,.043,-.068),(sign*.155,-1.096,.149,.035,-.090),(sign*.230,-1.128,.130,.026,-.115),(sign*.304,-1.168,.095,.017,-.137),(sign*.362,-1.198,.047,.009,-.155),(sign*.378,-1.205,.012,.004,-.160)],col,mats['dorsum'],'y',12)
    upper=lens_loft('Upper_inferred_caudal_membrane',[(.000,-1.640,.360,.060),(.110,-1.704,.293,.050),(.230,-1.798,.233,.039),(.350,-1.906,.165,.027),(.460,-2.010,.091,.014),(.545,-2.087,.026,.006),(.560,-2.102,.008,.003)],col,mats['dorsum'],n=16)
    lower=lens_loft('Downturned_axial_lower_caudal_lobe',[(.005,-1.640,.350,.060),(-.105,-1.713,.286,.049),(-.225,-1.842,.216,.037),(-.345,-1.982,.147,.025),(-.455,-2.115,.080,.014),(-.525,-2.218,.025,.006),(-.540,-2.245,.010,.003)],col,mats['dorsum'],n=16)
    bpy.ops.object.select_all(action='DESELECT'); upper.select_set(True); lower.select_set(True); bpy.context.view_layer.objects.active=lower; bpy.ops.object.join(); lower.name='Vertical_lunate_caudal_fin'
    details=[]
    for sign,label in [(-1,'near'),(1,'far')]:
        seated_eye(label,sign,col,mats['detail'])
        x=1.730;z=.060;y=body_surface_y(x,z,sign)+sign*.001
        details.append(ellipsoid('Nostril_'+label,(x,y,z),(.015,.004,.008),col,mats['detail'],16,6))
        points=[]
        for i in range(37):
            x=1.20+(2.245-1.20)*i/36; w,up,down,z0=body_properties(x); z=z0-.020*(1-i/36)
            y=body_surface_y(x,z,sign)+sign*.0007
            points.append((x,y,z))
        details.append(tube_path('Closed_fine_jaw_seam_'+label,points,.0020,col,mats['detail']))
    bpy.ops.object.select_all(action='DESELECT')
    for o in details:o.select_set(True)
    bpy.context.view_layer.objects.active=details[0]; bpy.ops.object.join(); details[0].name='Fine_jaw_seams_and_nostrils'
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
    measured=[]
    for obj in col.all_objects:
        if obj.type!='MESH':continue
        verts=[obj.matrix_world@v.co for v in obj.data.vertices];lo,hi=_bounds(verts)
        bm=bmesh.new();bm.from_mesh(obj.data);volume=bm.calc_volume(signed=True);bm.free()
        measured.append({'name':obj.name,'bounds_blender_m':{'min':list(lo),'max':list(hi),'size':[hi[i]-lo[i] for i in range(3)]},'signed_volume_m3':volume,'positive_transform_determinant':obj.matrix_world.determinant()>0})
    record['parts_measured']=measured
    record['palette_srgb_hex']=P['palette']
    record['origin']=P['origin']
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
        if name not in A.view_names.split(','):continue
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
