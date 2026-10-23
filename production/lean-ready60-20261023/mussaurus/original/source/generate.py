# SPDX-License-Identifier: MIT
"""Original adult Mussaurus living reconstruction. Blender 4.3.2, metres.
Run: blender -b -t 2 --python source/generate.py -- --output . --mode build
Modes clay/views reimport the exact exported GLB. Reference images are not loaded.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _vertices_world, _bounds, _look_at
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def tube(rows,n=12,phase=0):
    """Closed hand-shaped elliptical sections, transported around their centreline."""
    verts=[];faces=[]
    for i,r in enumerate(rows):
        c=Vector(r[:3]);t=(Vector(rows[min(i+1,len(rows)-1)][:3])-Vector(rows[max(i-1,0)][:3])).normalized()
        ref=Vector((1,0,0)) if abs(t.x)<.88 else Vector((0,1,0))
        u=(ref-t*ref.dot(t)).normalized();v=t.cross(u).normalized()
        for j in range(n):
            a=phase+2*math.pi*j/n;verts.append(tuple(c+u*r[3]*math.cos(a)+v*r[4]*math.sin(a)))
    faces.append(tuple(reversed(range(n))))
    for i in range(len(rows)-1):
        for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.append(tuple((len(rows)-1)*n+j for j in range(n)))
    return verts,faces

def joined(parts):
    verts=[];faces=[]
    for vv,ff in parts:
        o=len(verts);verts.extend(vv);faces.extend(tuple(v+o for v in f) for f in ff)
    return verts,faces

def oval(c,r,n=10):
    return tube([(c[0],c[1]+r[1]*math.sin(a),c[2],r[0]*math.cos(a),r[2]*math.cos(a)) for a in [-1.48,-1.05,-.52,0,.52,1.05,1.48]],n)

def build(out):
    col=setup_scene('mussaurus',P['seed']);root=bpy.data.objects['mussaurus']
    mats={k:make_material(k,v,roughness=.86) for k,v in P['palette_hex'].items()}
    # Continuous axial envelope, from the high conservative neck to the deep trunk,
    # broad sacral region and substantial tail musculature. All sections are authored.
    rows=[(0,-1.65,2.48,.088,.102),(0,-1.63,2.36,.094,.109),
      (0,-1.62,2.20,.101,.112),(0,-1.60,2.03,.114,.123),
      (0,-1.55,1.86,.142,.155),(0,-1.44,1.69,.176,.212),
      (0,-1.27,1.55,.228,.290),(0,-1.08,1.44,.314,.377),
      (0,-.86,1.37,.405,.465),(0,-.60,1.34,.463,.536),
      (0,-.32,1.35,.485,.565),(0,-.04,1.38,.478,.546),
      (0,.20,1.415,.431,.479),(0,.43,1.425,.368,.420),
      (0,.66,1.405,.315,.369),(0,.90,1.375,.277,.325),
      (0,1.15,1.335,.236,.281),(0,1.42,1.28,.195,.235),
      (0,1.70,1.205,.155,.194),(0,1.99,1.115,.117,.153),
      (0,2.28,1.025,.083,.112),(0,2.58,.935,.056,.079),
      (0,2.87,.852,.035,.050),(0,3.13,.783,.020,.030),
      (0,3.34,.726,.010,.017),(0,3.49,.688,.0025,.004)]
    vv,ff=tube(rows,16);body=mesh_object('deep-trunk-neck-and-muscular-tail',vv,ff,[mats['skin'],mats['dorsal'],mats['ventral']],col)
    # Body colour boundaries follow section coordinates, not arbitrary world height.
    n=16
    for poly in body.data.polygons:
        k=(poly.index-1)%n;a=2*math.pi*(k+.5)/n
        poly.material_index=1 if math.sin(a)<-.70 else 2 if math.sin(a)>.58 else 0
    # Small inferred adult skull: no claim of preserved adult cranial morphology.
    skull=[(0,-2.01,2.509,.040,.048),(0,-1.965,2.527,.070,.062),
      (0,-1.875,2.551,.094,.083),(0,-1.785,2.565,.107,.102),
      (0,-1.700,2.554,.096,.099),(0,-1.635,2.513,.063,.065)]
    vv,ff=tube(skull,12,math.pi/12);head=mesh_object('inferred-small-adult-head',vv,ff,[mats['skin'],mats['ventral']],col)
    for f in head.data.polygons:f.material_index=int(sum(head.data.vertices[i].co.z for i in f.vertices)/len(f.vertices)<2.50)
    claws=[];face=[];femur_axes=[]
    for s,label in [(1,'left'),(-1,'right')]:
        # Hip/knee centres follow a 0.726 m axis, an independent published scale anchor.
        hip=(s*.36,.25,1.38);knee=(s*.45,-.10,1.38-math.sqrt(P['femur_anchor_m']**2-.35**2-.09**2))
        femur_axes.append({'side':label,'hip_m':hip,'knee_m':knee,'length_m':(Vector(hip)-Vector(knee)).length})
        legs=[(s*.31,.28,1.43,.169,.236),(s*.40,.18,1.27,.238,.294),
          (s*.447,.045,1.06,.229,.272),(knee[0],knee[1],knee[2],.133,.154),
          (s*.464,-.025,.635,.104,.133),(s*.48,.135,.421,.076,.093),
          (s*.485,.235,.241,.058,.067),(s*.485,.186,.123,.060,.068),
          (s*.486,.075,.061,.071,.047)]
        pieces=[tube(legs,14)]
        # Tridactyl weight-bearing pad, tapering toe segments and a reduced hallux.
        for j in [-1,0,1]:
            x=s*(.486+j*.095);tip=-.245 if j==0 else -.192
            pieces.append(tube([(s*.486,.080,.071,.050,.042),(x,-.035,.050,.045,.039),
              (x+s*j*.022,tip+.060,.042,.035,.034),(x+s*j*.027,tip,.038,.018,.028)],8))
            claws.append(tube([(x+s*j*.027,tip+.008,.046,.022,.024),(x+s*j*.032,tip-.045,.031,.013,.015),(x+s*j*.035,tip-.074,.022,.002,.0025)],8))
        pieces.append(tube([(s*.431,.163,.151,.025,.030),(s*.371,.196,.094,.021,.023),(s*.348,.233,.085,.009,.012)],8))
        vv,ff=joined(pieces);mesh_object(label+'-powerful-hindlimb-and-foot',vv,ff,mats['skin'],col)
        # Small free arm hangs from the shoulder; elbow is rearward of the wrist.
        # Hands are blade-like in sagittal orientation, with their palms facing medially.
        arms=[(s*.263,-1.040,1.485,.089,.117),(s*.332,-.986,1.345,.091,.108),
          (s*.382,-.918,1.185,.072,.083),(s*.389,-.970,1.065,.052,.065),
          (s*.379,-1.075,.956,.039,.047),(s*.369,-1.150,.911,.035,.049)]
        palms=[(s*.369,-1.146,.918,.031,.052),(s*.367,-1.184,.855,.035,.064),(s*.361,-1.198,.808,.027,.052)]
        pieces=[tube(arms,10),tube(palms,10)]
        for j in range(5):
            y=-1.244+j*.028;z=.830;L=[.087,.115,.104,.065,.042][j];r=.016 if j<3 else .010
            pts=[(s*.359,y,z,r,r*1.1),(s*.350,y-.011,z-L*.58,r*.82,r*.8),(s*.323,y+.003,z-L,r*.40,r*.4)]
            pieces.append(tube(pts,8))
            if j<3:
                x,y,z=pts[-1][:3];bend=.053 if j==0 else .030
                claws.append(tube([(x,y,z,.012,.013),(x-s*bend*.7,y-.007,z-.021,.008,.008),(x-s*bend,y+.012,z-.028,.002,.002)],8))
        vv,ff=joined(pieces);mesh_object(label+'-short-free-arm-inward-hand',vv,ff,mats['skin'],col)
        face.append(oval((s*.102,-1.774,2.587),(.014,.027,.025),12))
        face.append(oval((s*.064,-1.960,2.550),(.004,.009,.005),8))
        face.append(tube([(s*.041,-2.006,2.489,.0025,.0025),(s*.072,-1.950,2.487,.0025,.0025),
          (s*.091,-1.871,2.486,.0024,.0024),(s*.101,-1.793,2.493,.0020,.0025)],6))
    vv,ff=joined(claws);mesh_object('restrained-keratin-digit-tips',vv,ff,mats['keratin'],col)
    vv,ff=joined(face);mesh_object('paired-eyes-nares-and-closed-mouth',vv,ff,mats['face'],col)
    # Ground the toes and centre the root under the bilateral hind-foot contact region.
    floor=min(v.z for v in _vertices_world(col));foot_y=.015
    for obj in col.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices:v.co.z-=floor;v.co.y-=foot_y
    root['reconstruction']='Adult composite reconstruction, not a single complete fossil. Missing adult skull and tail portions inferred from published restoration; colour and soft tissues artistic.'
    root['reference']='Otero et al. 2019, Scientific Reports 9:7614, Figure 1d'
    root['nominal_length_m']=5.5;root['femur_anchor_m']=.726
    bpy.context.view_layer.update();source=audit_source(col,6500)
    if source['errors']:raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    assert not set(opts)-available
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    glb=audit_glb(out/'model.glb',6500,6,12);glb['file']='model.glb'
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][key][i]-expected[key][i]) for key in expected for i in range(3))
    assert not glb['errors'] and glb['scene_triangles']==source['triangles'] and delta<1e-5 and glb['bytes']<=2000000
    write(out/'qa/evidence/technical.json',{'status':'PASS','glb_sha256':sha(out/'model.glb'),'source':source,'glb':glb,'source_export_bounds_max_error_m':delta,'runtime':{'blender':bpy.app.version_string,'exporter':'4.3.47','three_target':'0.180.0'},'export_options':opts,'origin':'Floor contact, centred between hind feet; +Z up/-Y head in Blender and +Y up/+Z head in glTF.','scale_note':'Approximately 5.5 m straight-line display length, not a measured complete individual. Published 0.726 m femur is a proportion anchor; articulated pose is inferred.','femur_axes':femur_axes,'design_sections_m':{'trunk_width':.970,'trunk_depth':1.130,'tail_base_depth_at_y_0_66':.738,'neck_min_width':.176,'head_length':.375},'warning_review':'Closed editable anatomical components overlap at attachments. The entire axial envelope is continuous. Intentional flat facets; no texture, rig, or external dependency.','gpu':'UNKNOWN','scene':'UNKNOWN'})

def render(out,clay=False):
    model=out/'model.glb';model_sha=sha(model)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(model))
    scene=bpy.context.scene;points=[obj.matrix_world@v.co for obj in scene.objects if obj.type=='MESH' for v in obj.data.vertices]
    low,high=_bounds(points);center=Vector([(a+b)/2 for a,b in zip(low,high)]);span=max(b-a for a,b in zip(low,high))
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False;scene.cycles.samples=8 if clay else P['render']['samples']
    res=384 if clay else P['render']['resolution'];scene.render.resolution_x=scene.render.resolution_y=res;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.34;scene.world=world
    for name,d,energy in [('key',(-3,-4,6),420),('fill',(4,-1,3),160)]:
        light=bpy.data.lights.new(name,'AREA');light.energy=energy*span*span/4;light.shape='DISK';light.size=span*2
        obj=bpy.data.objects.new(name,light);scene.collection.objects.link(obj);obj.location=center+Vector(d)*span/2;_look_at(obj,center)
    data=bpy.data.cameras.new('exact-export-inspection-camera');cam=bpy.data.objects.new('exact-export-inspection-camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.clip_start=.01;data.clip_end=100
    if clay:scene.view_layers[0].material_override=make_material('inspection-clay','#9A9A9A')
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if clay:directions={k:directions[k] for k in ['side','front','perspective']}
    target=out/('private/clay' if clay else 'views');target.mkdir(parents=True,exist_ok=True);records=[]
    for name,d in directions.items():
        direction=Vector(d).normalized();data.type='PERSP' if name=='perspective' else 'ORTHO';data.lens=50
        cam.location=center+direction*span*2.4;_look_at(cam,center);bpy.context.view_layer.update()
        inv=cam.matrix_world.inverted();q=[inv@v for v in points]
        minx,maxx=min(v.x for v in q),max(v.x for v in q);miny,maxy=min(v.y for v in q),max(v.y for v in q)
        shift=cam.matrix_world.to_3x3()@Vector(((minx+maxx)/2,(miny+maxy)/2,0));target_center=center+shift;cam.location+=shift
        data.ortho_scale=max(maxx-minx,maxy-miny)*1.17
        if name=='perspective':
            basis=cam.rotation_euler.to_matrix().transposed();q=[basis@(v-target_center) for v in points];t=math.tan(data.angle_x/2)
            dist=max(max(abs(v.x)/t+v.z,abs(v.y)/t+v.z) for v in q)*1.17;cam.location=target_center+direction*dist;_look_at(cam,target_center)
        scene.render.filepath=str(target/(name+'.png'));bpy.ops.render.render(write_still=True)
        records.append({'path':('private/clay/' if clay else 'views/')+name+'.png','sha256':sha(scene.render.filepath),'camera_direction_blender':list(direction),'camera_position_blender_m':list(cam.location),'camera_type':data.type,'resolution':[res,res],'source':'Fresh import of exact model.glb'})
    if not clay:
        shutil.copyfile(target/'perspective.png',out/'preview.png')
        write(out/'qa/evidence/views.json',{'status':'RENDERED_PENDING_INDEPENDENT_REVIEW','glb_sha256':model_sha,'generator_sha256':sha(__file__),'renderer':'Blender Cycles CPU','settings':P['render'],'images':records,'preview':'Byte-identical reuse of views/perspective.png. No website renderer contract claimed.','gpu_evidence':False})

parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('.'));parser.add_argument('--mode',choices=['build','clay','views'],default='build')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);out=args.output.resolve();out.mkdir(exist_ok=True,parents=True)
if args.mode=='build':build(out)
else:render(out,args.mode=='clay')
