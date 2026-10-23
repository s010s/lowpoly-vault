# SPDX-License-Identifier: MIT
"""Original Cymbospondylus petrinus, composite living reconstruction.
Run Blender in factory background mode with this file, then -- --out OUTPUT.
All geometry is deterministic; required helpers and parameters are adjacent.
The 11.5 m restored length is an estimate, not a complete measured specimen.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _bounds, _vertices_world, _look_at
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--out',default=str(HERE.parent));parser.add_argument('--mode',choices=['build','gray','views'],default='build');parser.add_argument('--view-names',default='front,side,top,perspective')
A=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(A.out).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')

# x, lateral center, vertical center, transverse radius, vertical radius.
# Skull base is x=4.61; neck ends 4.31; restored trunk ends -0.49.
AXIAL=[
(5.75,0,.061,.027,.026),(5.69,0,.062,.048,.038),(5.54,0,.066,.062,.050),
(5.36,0,.071,.074,.060),(5.18,0,.078,.088,.072),(5.03,0,.091,.108,.088),
(4.89,0,.077,.132,.089),(4.76,0,.066,.152,.105),(4.61,0,.040,.160,.130),
(4.46,0,.039,.184,.205),(4.31,0,.015,.215,.255),(4.10,0,0,.265,.324),
(3.88,0,-.010,.324,.397),(3.63,0,-.025,.378,.456),(3.37,0,-.033,.417,.502),
(3.08,0,-.036,.448,.529),(2.77,0,-.039,.467,.535),(2.43,0,-.038,.470,.535),
(2.08,0,-.032,.468,.531),(1.73,0,-.025,.455,.513),(1.38,0,-.018,.435,.487),
(1.03,0,-.009,.411,.460),(.68,0,0,.382,.428),(.34,0,.006,.349,.396),
(0,0,.012,.318,.364),(-.25,0,.018,.291,.334),(-.49,0,.020,.266,.308),
(-.78,.005,.018,.241,.283),(-1.10,.013,.014,.216,.258),(-1.43,.025,.009,.193,.236),
(-1.77,.039,.004,.171,.216),(-2.12,.055,0,.150,.196),(-2.48,.073,-.006,.129,.177),
(-2.85,.092,-.013,.108,.158),(-3.21,.110,-.018,.088,.144),(-3.55,.126,-.023,.070,.136),
(-3.88,.137,-.025,.055,.139),(-4.18,.142,-.024,.044,.155),(-4.46,.141,-.020,.035,.176),
(-4.72,.135,-.014,.027,.190),(-4.96,.123,-.007,.021,.182),(-5.18,.109,.002,.016,.152),
(-5.38,.093,.011,.011,.112),(-5.55,.079,.019,.007,.070),(-5.68,.068,.023,.0037,.031),
(-5.75,.063,.025,.0016,.004)]

def axial_mesh(col,mats):
    n=16;v=[];f=[];mi=[]
    for x,y,z,ry,rz in AXIAL:
        for j in range(n):
            a=2*math.pi*j/n;v.append((x,y+ry*math.cos(a),z+rz*math.sin(a)))
    for i in range(len(AXIAL)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;c=(i+1)*n+(j+1)%n;d=(i+1)*n+j
            # Broad deliberate panels; alternating diagonal avoids one repeated seam.
            if (i+j)%2:f.extend([(a,b,d),(b,c,d)])
            else:f.extend([(a,b,c),(a,c,d)])
            s=math.sin(2*math.pi*(j+.5)/n);idx=0 if s>.50 else 2 if s<-.35 else 1;mi.extend([idx,idx])
    f.extend([tuple(reversed(range(n))),tuple((len(AXIAL)-1)*n+j for j in range(n))]);mi.extend([1,1])
    o=mesh_object('Axial_body_small_skull_long_trunk_low_tail',v,f,mats,col)
    for p,i in zip(o.data.polygons,mi):p.material_index=i
    o['skull_base_x_m']=4.61;o['tail_start_x_m']=-.49;o['preserved_specimen_length_m']=6.66;o['restored_total_length_m']=11.5;o['tail_tip']='Inferred shallow terminal expansion; no deep crescent fork.'

def loft(name,rings,col,mat,axis='x',n=12):
    # Each ring supplies center x/y/z and radii in its plane.
    v=[];f=[]
    for x,y,z,r1,r2 in rings:
        for j in range(n):
            a=2*math.pi*j/n
            v.append((x,y+r1*math.cos(a),z+r2*math.sin(a)) if axis=='x' else (x+r1*math.cos(a),y,z+r2*math.sin(a)))
    for i in range(len(rings)-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))])
    return mesh_object(name,v,f,mat,col)

def add_ellipsoid(v,f,center,radii,n=12,m=6):
    base=len(v);v.append((center[0],center[1],center[2]+radii[2]))
    for i in range(1,m):
        t=math.pi*i/m
        for j in range(n):
            a=2*math.pi*j/n;v.append((center[0]+radii[0]*math.sin(t)*math.cos(a),center[1]+radii[1]*math.sin(t)*math.sin(a),center[2]+radii[2]*math.cos(t)))
    bottom=len(v);v.append((center[0],center[1],center[2]-radii[2]))
    for j in range(n):f.append((base,base+1+j,base+1+(j+1)%n))
    for i in range(m-2):
        for j in range(n):f.append((base+1+i*n+j,base+1+(i+1)*n+j,base+1+(i+1)*n+(j+1)%n,base+1+i*n+(j+1)%n))
    for j in range(n):f.append((bottom,base+1+(m-2)*n+(j+1)%n,base+1+(m-2)*n+j))

def details(col,m):
    v=[];f=[]
    for s in [-1,1]:
        add_ellipsoid(v,f,(4.865,s*.129,.108),(.037,.014,.032))
        add_ellipsoid(v,f,(5.08,s*.083,.132),(.024,.010,.010),10,4)
    o=mesh_object('Small_paired_eyes_and_nares',v,f,m['detail'],col)
    for p in o.data.polygons:p.use_smooth=True
    # Modest marginal teeth, never oversized fangs. Closed solids joined only in data.
    v=[];f=[]
    for s in [-1,1]:
        for i in range(17):
            x=4.99+i*.041;w=.105-(x-4.99)*.084
            h=.013+(1-i/19)*.007
            for upper in [True,False]:
                cx=x+(0 if upper else .018);z=.008 if upper else -.035
                b=len(v);rad=.0047
                for j in range(6):
                    a=2*math.pi*j/6;v.append((cx+rad*math.cos(a),s*w+rad*math.sin(a),z))
                v.append((cx+.002,s*w,z-h if upper else z+h));f.append(tuple(b+j for j in range(6)))
                for j in range(6):f.append((b+j,b+(j+1)%6,b+6))
    mesh_object('Modest_conical_marginal_teeth',v,f,m['tooth'],col)

def build():
    c=setup_scene(P['asset_id'],P['seed']);root=bpy.data.objects[P['asset_id']];root['authoring_forward']='+X';root['mount']=P['origin'];root['reconstruction']='C. petrinus; UCMP9950 axial evidence, separate UCMP9947 tail, missing terminal tail restored.'
    m={k:make_material(k,col,.82 if k!='detail' else .38)for k,col in P['palette'].items()}
    axial_mesh(c,[m['dorsum'],m['flank'],m['belly']])
    jaw=loft('Slender_lower_jaw',[(4.58,0,-.069,.136,.075),(4.76,0,-.078,.136,.062),(4.94,0,-.076,.112,.049),(5.14,0,-.071,.090,.043),(5.35,0,-.064,.074,.037),(5.54,0,-.057,.060,.031),(5.70,0,-.049,.044,.024),(5.744,0,-.043,.022,.018)],c,m['belly'])
    loft('Narrow_oral_seam',[(4.83,0,-.014,.112,.013),(5.03,0,-.013,.104,.019),(5.25,0,-.010,.084,.016),(5.48,0,-.010,.064,.015),(5.70,0,-.012,.038,.009)],c,m['oral'])
    for s,label in [(-1,'near'),(1,'far')]:
        fore=[(3.71,s*.305,-.235,.129,.100),(3.70,s*.44,-.252,.150,.083),(3.66,s*.60,-.276,.145,.066),(3.60,s*.76,-.301,.126,.050),(3.52,s*.90,-.326,.101,.035),(3.43,s*1.015,-.348,.073,.023),(3.35,s*1.09,-.363,.038,.012),(3.315,s*1.115,-.368,.009,.003)]
        o=loft('Inferred_forepaddle_'+label,fore,c,m['dorsum'],'y');o['distal_outline']='Conservative inferred rounded membrane, not directly preserved.'
        hind=[(-.10,s*.229,-.155,.106,.073),(-.12,s*.34,-.171,.125,.061),(-.17,s*.47,-.193,.120,.049),(-.23,s*.59,-.219,.104,.037),(-.31,s*.70,-.245,.082,.026),(-.39,s*.79,-.265,.055,.017),(-.46,s*.85,-.279,.028,.009),(-.49,s*.87,-.284,.007,.0025)]
        o=loft('Inferred_hindpaddle_'+label,hind,c,m['dorsum'],'y');o['distal_outline']='Conservative inferred rounded membrane, not directly preserved.'
    details(c,m)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    return c

EXPORT_OPTIONS=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
def emit(col):
    qa=audit_source(col,P['max_triangles'])
    if qa['errors']:raise RuntimeError(str(qa['errors']))
    bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
    bpy.context.scene.render.filepath='//';bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[P['asset_id']]
    if set(EXPORT_OPTIONS)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}:raise RuntimeError('Exporter flags unavailable')
    bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**EXPORT_OPTIONS)
    glb=audit_glb(OUT/'model.glb',P['max_triangles'],P['max_materials'],P['max_primitives']);glb['file']='model.glb'
    if glb['errors'] or glb['bytes']>P['max_glb_bytes']:raise RuntimeError(str(glb['errors']))
    b=qa['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][side][i]-exp[i])for side,exp in [('min',lo),('max',hi)]for i in range(3));assert delta<.0001 and qa['triangles']==glb['scene_triangles']
    parts=[]
    for o in col.all_objects:
        if o.type!='MESH':continue
        lo,hi=_bounds([o.matrix_world@v.co for v in o.data.vertices]);bm=bmesh.new();bm.from_mesh(o.data);vol=bm.calc_volume(signed=True);bm.free()
        parts.append({'name':o.name,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i]for i in range(3)]},'signed_volume_m3':vol,'positive_transform_determinant':o.matrix_world.determinant()>0})
    write(OUT/'qa/evidence/source-glb.json',{'status':'PASS','source':qa,'glb':glb,'parts_measured':parts,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'palette_srgb_hex':P['palette'],'origin':P['origin'],'warning_review':{'mount':'Negative Z is intentional for a swimming animal with an axial mount.','smooth_normals':'Only eyes and nares are smooth; other surfaces are deliberate facets.','attachments':'Solid closed paddles overlap their muscular axial roots; eyes and oral details overlap deliberately.'},'claim_scope':'Source and static GLB geometry only, not independent visual/factual acceptance or GPU rendering.'})
    return col

def import_exact():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    c=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(c)
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH':
            for old in list(o.users_collection):old.objects.unlink(o)
            c.objects.link(o)
    return c

def render(col,destination,gray=False):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=8 if gray else P['preview']['samples'];sc.cycles.use_denoising=False;sc.cycles.seed=P['seed'];sc.render.threads_mode='FIXED';sc.render.threads=2
    size=448 if gray else P['preview']['resolution'];sc.render.resolution_x=size;sc.render.resolution_y=size;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=not gray
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    w=bpy.data.worlds.new('Neutral_studio');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.4;sc.world=w
    if gray:sc.view_layers[0].material_override=make_material('Clay','#A6A6A6')
    points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i]for i in range(3))
    for name,direction,energy,siz in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=siz*span/2;o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
    d=bpy.data.cameras.new('Evidence_camera');cam=bpy.data.objects.new('Evidence_camera',d);sc.collection.objects.link(cam);sc.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30
    rows=[];destination.mkdir(parents=True,exist_ok=True)
    for name,direction in {'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}.items():
        if name not in A.view_names.split(','):continue
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points];width=max(p.x for p in proj)-min(p.x for p in proj);height=max(p.y for p in proj)-min(p.y for p in proj)
        shift=Vector(((max(p.x for p in proj)+min(p.x for p in proj))/2,(max(p.y for p in proj)+min(p.y for p in proj))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift;d.ortho_scale=max(width,height)*1.18
        sc.render.filepath=str(destination/(name+'.png'));bpy.ops.render.render(write_still=True)
        rows.append({'path':('private/gray/'if gray else'views/')+name+'.png','sha256':sha(destination/(name+'.png')),'direction_blender':direction,'camera_position':list(cam.location),'orthographic_scale':d.ortho_scale,'width':size,'height':size})
    if not gray:
        shutil.copyfile(destination/'perspective.png',OUT/'preview.png');write(OUT/'qa/evidence/views.json',{'glb_sha256':sha(OUT/'model.glb'),'input':'Clean import of exact delivered GLB, not source geometry','engine':'Cycles CPU','gpu_status':'UNKNOWN','samples':sc.cycles.samples,'transparent':True,'view_transform':'Standard','look':'None','views':rows,'preview_sha256':sha(OUT/'preview.png'),'preview_reuses':'views/perspective.png','render_source_sha256':sha(HERE/'generate.py')})
if A.mode=='build':emit(build())
elif A.mode=='gray':render(build(),OUT/'private/gray',True)
else:render(import_exact(),OUT/'views')
