# SPDX-License-Identifier: MIT
"""Original adult Massospondylus reconstruction. Run with Blender 4.3.2.
Usage: blender -b -t 2 --python source/generate.py -- --output . --mode build
Modes clay and views import model.glb fresh and never save preview scenes.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source, _look_at, _vertices_world, _bounds
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')

def loft(rows,n=12,axis='y',phase=0):
    # Rows: centre x,y,z and two semiaxes perpendicular to local centreline.
    verts=[];faces=[]
    for i,r in enumerate(rows):
        c=Vector(r[:3]); prev=Vector(rows[max(0,i-1)][:3]); nex=Vector(rows[min(len(rows)-1,i+1)][:3]); t=(nex-prev).normalized()
        ref=Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0))
        u=(ref-t*ref.dot(t)).normalized(); v=t.cross(u).normalized()
        for k in range(n):
            a=phase+2*math.pi*k/n
            verts.append(tuple(c+u*(r[3]*math.cos(a))+v*(r[4]*math.sin(a))))
    faces.append(tuple(reversed(range(n))))
    for i in range(len(rows)-1):
        for k in range(n): faces.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
    faces.append(tuple((len(rows)-1)*n+k for k in range(n)))
    return verts,faces

def combine(items):
    vv=[];ff=[]
    for v,f in items:
        off=len(vv);vv+=v;ff.extend(tuple(x+off for x in a) for a in f)
    return vv,ff

def ellipsoid(c,r,n=10):
    rows=[]
    for a in [-1.48,-1.05,-.5,0,.5,1.05,1.48]:
        rows.append((c[0],c[1]+r[1]*math.sin(a),c[2],r[0]*math.cos(a),r[2]*math.cos(a)))
    return loft(rows,n)

def build(out):
    col=setup_scene('massospondylus',P['seed'])
    mats={k:make_material(k,v,roughness=.87) for k,v in P['palette_hex'].items()}
    # One uninterrupted axial body: slender neck to ribcage, pelvis and elevated tail.
    rows=[(0,-1.68,1.64,.048,.061),(0,-1.57,1.59,.057,.066),(0,-1.45,1.52,.064,.070),
      (0,-1.31,1.43,.070,.075),(0,-1.16,1.34,.076,.083),(0,-1.01,1.25,.084,.098),
      (0,-.86,1.18,.102,.125),(0,-.70,1.13,.143,.183),(0,-.55,1.08,.191,.244),
      (0,-.38,1.05,.239,.295),(0,-.20,1.06,.277,.330),(0,0,1.075,.287,.336),
      (0,.18,1.10,.271,.312),(0,.34,1.115,.230,.255),(0,.49,1.12,.175,.196),
      (0,.65,1.12,.140,.154),(0,.83,1.13,.112,.122),(0,1.02,1.145,.087,.093),
      (0,1.22,1.16,.064,.070),(0,1.43,1.17,.045,.050),(0,1.62,1.165,.029,.033),
      (0,1.80,1.14,.016,.021),(0,1.96,1.11,.009,.012),(0,2.09,1.085,.0025,.003)]
    v,f=loft(rows,16);body=mesh_object('axial-body-neck-tail',v,f,[mats['skin'],mats['dorsal'],mats['ventral']],col)
    for poly in body.data.polygons:
        z=sum(body.data.vertices[k].co.z for k in poly.vertices)/len(poly.vertices)
        y=sum(body.data.vertices[k].co.y for k in poly.vertices)/len(poly.vertices)
        nearest=min(rows,key=lambda r:abs(r[1]-y)); rel=(z-nearest[2])/max(nearest[4],.001)
        poly.material_index=1 if rel>.65 else 2 if rel<-.57 else 0
    # Small short, deep posterior cranium with a blunt narrow muzzle, not a hatchling head.
    skull=[(0,-1.91,1.657,.032,.042),(0,-1.88,1.665,.053,.052),(0,-1.81,1.680,.066,.067),
      (0,-1.74,1.690,.077,.079),(0,-1.68,1.688,.069,.076),(0,-1.625,1.665,.043,.052)]
    v,f=loft(skull,12,phase=math.pi/12);head=mesh_object('small-boxlike-skull',v,f,[mats['skin'],mats['ventral']],col)
    for poly in head.data.polygons:
        poly.material_index=int(sum(head.data.vertices[k].co.z for k in poly.vertices)/len(poly.vertices)<1.635)
    claws=[];facial=[]
    for s,side in [(1,'left'),(-1,'right')]:
        # Longer hindlimb: powerful upper leg, bent knee, back-sloping shank, raised heel.
        leg=[(s*.175,.19,1.11,.115,.166),(s*.225,.10,.99,.151,.187),
          (s*.255,-.015,.81,.131,.164),(s*.267,-.10,.66,.087,.101),
          (s*.272,-.01,.51,.066,.083),(s*.275,.105,.31,.047,.056),
          (s*.278,.13,.17,.040,.045),(s*.280,.045,.073,.044,.046)]
        pieces=[loft(leg,12)]
        # Three long forward toes plus a modest raised inner hallux.
        for j in [-1,0,1]:
            x=s*(.280+j*.064);end=-.19 if j==0 else -.14
            toe=[(s*.280,.045,.070,.037,.032),(x,-.035,.046,.031,.032),
                 (x+s*j*.014,end+.035,.033,.025,.030),(x+s*j*.021,end,.031,.013,.025)]
            pieces.append(loft(toe,8))
            claws.append(loft([(x+s*j*.021,end+.012,.038,.018,.019),(x+s*j*.023,end-.033,.027,.012,.013),(x+s*j*.025,end-.060,.018,.0018,.002)],8))
        pieces.append(loft([(s*.253,.10,.122,.018,.023),(s*.217,.166,.072,.015,.019),(s*.204,.193,.067,.004,.008)],8))
        v,f=combine(pieces);mesh_object(side+'-hindlimb-and-foot',v,f,mats['skin'],col)
        # Forelimbs are short, reach forward, and hang with inward palms, never columnar.
        arm=[(s*.149,-.55,1.084,.070,.082),(s*.200,-.575,.986,.071,.077),
          (s*.233,-.565,.885,.052,.056),(s*.239,-.605,.797,.035,.040),
          (s*.236,-.689,.742,.027,.032),(s*.231,-.746,.710,.030,.037)]
        hand=[(s*.231,-.742,.717,.029,.036),(s*.234,-.785,.677,.034,.041),(s*.234,-.800,.638,.031,.029)]
        pieces=[loft(arm,10),loft(hand,8)]
        # Three developed and two reduced digits; medial thumb claw emphasized modestly.
        for j in range(5):
            yy=-.811+j*.018; zz=.658-(.018 if j in [1,2] else 0); length=[.070,.083,.076,.045,.031][j]
            xx=s*(.231+.007*j)
            points=[(xx,yy,zz,.012 if j<3 else .008,.013),(xx-s*.012,yy-.009,zz-length*.65,.010 if j<3 else .006,.010),(xx-s*.033,yy-.002,zz-length,.004,.005)]
            pieces.append(loft(points,7))
            if j<3:
                c=points[-1];claws.append(loft([(*c[:3],.008,.009),(c[0]-s*(.035 if j==0 else .017),c[1]-.003,c[2]-.012,.005,.006),(c[0]-s*(.047 if j==0 else .023),c[1]+.008,c[2]-.024,.0015,.0015)],7))
        v,f=combine(pieces);mesh_object(side+'-short-forelimb-inward-hand',v,f,mats['skin'],col)
        facial.append(ellipsoid((s*.0718,-1.732,1.713),(.0125,.021,.019),10))
        # Closed mouth seam: thin dark strip at cheek, no invented beak or exposed big teeth.
        facial.append(loft([(s*.033,-1.906,1.638,.0018,.0023),(s*.055,-1.861,1.638,.0020,.0020),(s*.065,-1.805,1.637,.0021,.0020),(s*.070,-1.748,1.642,.0018,.002)],6))
        facial.append(ellipsoid((s*.048,-1.873,1.688),(.003,.008,.004),8))
    v,f=combine(claws);mesh_object('keratin-digit-tips',v,f,mats['horn'],col)
    v,f=combine(facial);mesh_object('paired-eyes-nostrils-mouth-seams',v,f,mats['dark'],col)
    # Shift all mesh vertices to establish exact lowest foot contact and footprint-centred root.
    # Toe claws currently contact below soft toes; this is deliberate, with both feet grounded.
    points=_vertices_world(col);floor=min(p.z for p in points)
    for obj in col.all_objects:
        if obj.type=='MESH':
            for vert in obj.data.vertices: vert.co.z-=floor;vert.co.y+=.025
    bpy.context.view_layer.update()
    root=bpy.data.objects['massospondylus'];root['reconstruction']='Adult whole animal; missing neotype hindlimbs/tail inferred. Color and soft tissue artistic.'
    source=audit_source(col,6500)
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing exporter settings')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    glb=audit_glb(out/'model.glb',6500,6,12)
    glb['file']='model.glb'
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][key][i]-expected[key][i]) for key in expected for i in range(3))
    if glb['errors'] or delta>1e-4 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Export mismatch: '+str(glb['errors']))
    if glb['bytes']>2000000:raise RuntimeError('Frozen byte budget exceeded')
    write(out/'qa/evidence/technical.json',{'status':'PASS','glb_sha256':digest(out/'model.glb'),'source':source,'glb':glb,'source_export_bounds_max_error_m':delta,'runtime':{'blender':bpy.app.version_string,'exporter':'4.3.47','three_target':'0.180.0'},'export_options':opts,'origin':'Floor-contact centre between hind feet. Blender +Z up and -Y head; glTF +Y up and +Z head.','scale_note':'Nominal four-metre species-level display length, not an individual measured total.','warning_review':'Separate overlapping solid anatomical parts are intentional. Source facets are flat, each component closed. No rig or texture dependency.','gpu':'UNKNOWN','scene':'UNKNOWN'})

def render(out,clay=False):
    glb=out/'model.glb'; sha=digest(glb)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    scene=bpy.context.scene;objs=[o for o in scene.objects if o.type=='MESH']
    points=[o.matrix_world@v.co for o in objs for v in o.data.vertices]
    lo,hi=_bounds(points);center=Vector([(a+b)/2 for a,b in zip(lo,hi)]);span=max(b-a for a,b in zip(lo,hi))
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False
    scene.cycles.samples=10 if clay else P['render']['samples']
    resolution=384 if clay else P['render']['resolution']
    scene.render.resolution_x=scene.render.resolution_y=resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;_look_at(obj,center)
    camdata=bpy.data.cameras.new('inspection-camera');cam=bpy.data.objects.new('inspection-camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.clip_start=.01;camdata.clip_end=100
    if clay:
        m=make_material('clay','#959595');bpy.context.view_layer.material_override=m
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if clay:views={k:views[k] for k in ['side','front','perspective']}
    target=out/'private/clay' if clay else out/'views';target.mkdir(parents=True,exist_ok=True)
    evidence=[]
    for name,direction in views.items():
        direction=Vector(direction).normalized();camdata.type='PERSP' if name=='perspective' else 'ORTHO';camdata.lens=50
        cam.location=center+direction*span*2.25;_look_at(cam,center);bpy.context.view_layer.update()
        inv=cam.matrix_world.inverted();projected=[inv@v for v in points];width=max(v.x for v in projected)-min(v.x for v in projected);height=max(v.y for v in projected)-min(v.y for v in projected)
        shift=Vector(((max(v.x for v in projected)+min(v.x for v in projected))/2,(max(v.y for v in projected)+min(v.y for v in projected))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift
        camdata.ortho_scale=max(width,height)*1.18
        if name=='perspective':
            # Fit all eight bbox corners with perspective depth rather than crop/resize.
            target_center=center+cam.matrix_world.to_3x3()@shift
            basis=cam.rotation_euler.to_matrix().transposed()
            local=[basis@(v-target_center) for v in points]
            tangent=math.tan(camdata.angle_x/2)
            desired=max(max(abs(v.x)/tangent+v.z,abs(v.y)/tangent+v.z) for v in local)*1.18
            cam.location=target_center+direction*desired
            _look_at(cam,target_center)
            bpy.context.view_layer.update()
        scene.render.filepath=str(target/(name+'.png'));bpy.ops.render.render(write_still=True)
        evidence.append({'path':('private/clay/' if clay else 'views/')+name+'.png','sha256':digest(scene.render.filepath),'camera_direction_blender':list(direction),'camera_position_blender_m':list(cam.location),'camera_type':camdata.type,'resolution':[resolution,resolution],'source':'Fresh import of exact model.glb'})
    if not clay:
        import shutil
        shutil.copyfile(target/'perspective.png',out/'preview.png')
        write(out/'qa/evidence/views.json',{'status':'RENDERED_PENDING_INDEPENDENT_REVIEW','glb_sha256':sha,'generator_sha256':digest(__file__),'renderer':'Blender Cycles CPU','settings':P['render'],'images':evidence,'preview':'Byte-identical reuse of views/perspective.png. No website-render contract claimed.','gpu_evidence':False})

args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=Path('.'));a.add_argument('--mode',choices=['build','clay','views'],default='build');opt=a.parse_args(args);out=opt.output.resolve();out.mkdir(parents=True,exist_ok=True)
if opt.mode=='build':build(out)
else:render(out,opt.mode=='clay')
