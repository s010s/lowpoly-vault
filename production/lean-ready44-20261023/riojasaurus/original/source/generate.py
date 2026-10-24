# SPDX-License-Identifier: MIT
"""Original Riojasaurus whole-animal reconstruction, Blender 4.3.2.
Run: blender -b -t 2 --python source/generate.py -- --output . --mode build
The clay and views modes freshly import the exact emitted model.glb.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,_look_at,_vertices_world,_bounds
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,obj):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def tube(rows,n=12,phase=0):
    """Closed flat-faceted profile loft, with locally perpendicular sections."""
    vertices=[];faces=[]
    for i,r in enumerate(rows):
        c=Vector(r[:3]);t=(Vector(rows[min(i+1,len(rows)-1)][:3])-Vector(rows[max(i-1,0)][:3])).normalized()
        ref=Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0))
        u=(ref-t*ref.dot(t)).normalized();v=t.cross(u)
        for k in range(n):
            a=phase+2*math.pi*k/n
            vertices.append(tuple(c+u*r[3]*math.cos(a)+v*r[4]*math.sin(a)))
    faces.append(tuple(reversed(range(n))))
    for i in range(len(rows)-1):
        for k in range(n):faces.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
    faces.append(tuple((len(rows)-1)*n+k for k in range(n)))
    return vertices,faces

def merge(items):
    vertices=[];faces=[]
    for vv,ff in items:
        off=len(vertices);vertices.extend(vv);faces.extend(tuple(off+j for j in f) for f in ff)
    return vertices,faces

def oval(c,r,n=10):
    rows=[(c[0],c[1]+r[1]*math.sin(a),c[2],r[0]*math.cos(a),r[2]*math.cos(a)) for a in [-1.48,-1.02,-.51,0,.51,1.02,1.48]]
    return tube(rows,n)

def build(out):
    col=setup_scene('riojasaurus',P['seed'])
    mats={k:make_material('riojasaurus-'+k,v,roughness=.88) for k,v in P['palette_hex'].items()}
    # A strong continuous axial volume. Broad, deep trunk is structurally distinct
    # from gracile bipedal sauropodomorph silhouettes. Tail has its full taper.
    axial=[(0,-1.94,1.355,.060,.068),(0,-1.82,1.355,.070,.077),
      (0,-1.66,1.320,.079,.085),(0,-1.49,1.270,.086,.093),
      (0,-1.31,1.215,.098,.109),(0,-1.13,1.155,.121,.136),
      (0,-.96,1.105,.160,.185),(0,-.80,1.065,.220,.258),
      (0,-.63,1.035,.299,.345),(0,-.44,1.025,.370,.408),
      (0,-.22,1.035,.418,.443),(0,0,1.055,.430,.450),
      (0,.22,1.080,.409,.427),(0,.42,1.110,.345,.360),
      (0,.60,1.135,.266,.278),(0,.77,1.140,.212,.215),
      (0,.96,1.145,.171,.172),(0,1.16,1.145,.141,.137),
      (0,1.37,1.140,.113,.109),(0,1.59,1.125,.088,.085),
      (0,1.82,1.105,.066,.064),(0,2.05,1.080,.047,.046),
      (0,2.28,1.050,.031,.032),(0,2.49,1.015,.019,.022),
      (0,2.69,.975,.010,.014),(0,2.86,.940,.005,.007),
      (0,2.965,.915,.0016,.002)]
    vv,ff=tube(axial,18)
    body=mesh_object('continuous-neck-deep-trunk-full-tail',vv,ff,[mats['skin'],mats['dorsal'],mats['ventral']],col)
    for poly in body.data.polygons:
        mid=sum((body.data.vertices[j].co for j in poly.vertices),Vector())/len(poly.vertices)
        row=min(axial,key=lambda r:abs(r[1]-mid.y));rel=(mid.z-row[2])/row[4]
        poly.material_index=1 if rel>.69 else 2 if rel<-.57 else 0
    # Long, gently descending snout, compact posterior cranium. This is living
    # soft tissue informed by a cast, not a copy of fossil openings.
    skull=[(0,-2.235,1.333,.043,.041),(0,-2.207,1.342,.062,.050),
      (0,-2.14,1.362,.073,.061),(0,-2.055,1.392,.085,.078),
      (0,-1.980,1.410,.098,.092),(0,-1.915,1.400,.090,.087),
      (0,-1.865,1.373,.057,.057)]
    vv,ff=tube(skull,14,math.pi/14)
    head=mesh_object('small-elongate-sloping-head',vv,ff,[mats['skin'],mats['ventral']],col)
    for poly in head.data.polygons:
        mid=sum((head.data.vertices[j].co for j in poly.vertices),Vector())/len(poly.vertices)
        row=min(skull,key=lambda r:abs(r[1]-mid.y))
        poly.material_index=int((mid.z-row[2])/row[4]<-.35)
    claws=[];features=[]
    for s,side in [(1,'left'),(-1,'right')]:
        # Hind femur is robust and gently forward, shank back to a weight-bearing
        # metatarsal segment. Hip-to-foot lateral displacement remains modest.
        hind=[(s*.255,.39,1.105,.149,.180),(s*.327,.33,.965,.188,.219),
          (s*.390,.215,.795,.173,.185),(s*.421,.160,.635,.112,.121),
          (s*.432,.230,.477,.083,.096),(s*.441,.330,.308,.063,.075),
          (s*.445,.355,.160,.056,.063),(s*.445,.295,.084,.061,.060)]
        pieces=[tube(hind,14)]
        # Three principal forward toes and a smaller medial digit. Their pads
        # touch the same floor; claws remain short rather than raptor-like.
        for j in [-1,0,1]:
            x=s*(.445+j*.067);end=.070 if j==0 else .108
            toe=[(s*.445,.306,.083,.046,.042),(x,.226,.053,.040,.043),
                 (x+s*j*.012,end+.035,.041,.032,.040),(x+s*j*.016,end,.040,.021,.037)]
            pieces.append(tube(toe,8))
            claws.append(tube([(x+s*j*.016,end+.013,.048,.020,.020),
              (x+s*j*.020,end-.029,.035,.013,.015),(x+s*j*.024,end-.057,.021,.002,.003)],8))
        pieces.append(tube([(s*.403,.320,.128,.024,.026),(s*.357,.359,.075,.022,.023),(s*.340,.375,.057,.009,.012)],8))
        vv,ff=merge(pieces);mesh_object(side+'-robust-hindlimb-pes',vv,ff,mats['skin'],col)
        # Forelimbs are shorter but strongly supporting. Elbows are slightly
        # lateral, not horizontal; palms are oblique/inward rather than flat.
        arm=[(s*.235,-.638,1.045,.109,.135),(s*.309,-.645,.930,.130,.149),
          (s*.363,-.610,.779,.112,.123),(s*.407,-.563,.625,.090,.099),
          (s*.416,-.595,.463,.070,.082),(s*.420,-.640,.292,.053,.064),
          (s*.419,-.660,.155,.047,.055),(s*.421,-.670,.088,.052,.054)]
        pieces=[tube(arm,12)]
        # An artistic supported manus, not an assertion of exact digit posture.
        # Digit axes angle medially. Three prominent, two reduced digits.
        for j in range(5):
            xx=s*(.421+(j-2)*.032);yy=-.674+(j-2)*.014
            length=[.077,.112,.115,.083,.055][j]
            pts=[(xx,yy,.095,.021,.027),(xx-s*.014,yy-length*.55,.057,.020,.027),
                 (xx-s*.024,yy-length,.034,.014,.029)]
            pieces.append(tube(pts,8))
            if j<3:
                tip=pts[-1];claws.append(tube([(tip[0],tip[1]+.006,.047,.013,.015),
                  (tip[0]-s*.010,tip[1]-.023,.033,.009,.011),
                  (tip[0]-s*.018,tip[1]-.037,.022,.002,.003)],7))
        vv,ff=merge(pieces);mesh_object(side+'-supporting-forelimb-oblique-manus',vv,ff,mats['skin'],col)
        # Small lateral eyes, quiet closed mouth and nostrils. No invented horns,
        # osteoderms, spikes, crest, fur or exposed toothed snarl.
        features.append(oval((s*.090,-1.965,1.435),(.011,.018,.015),10))
        features.append(oval((s*.056,-2.196,1.365),(.0035,.008,.004),8))
        features.append(tube([(s*.037,-2.233,1.316,.0017,.0017),
          (s*.060,-2.191,1.318,.0018,.0018),(s*.071,-2.128,1.321,.0018,.0018),
          (s*.081,-2.055,1.327,.0018,.0018),(s*.088,-1.989,1.334,.0015,.0015)],6))
    vv,ff=merge(claws);mesh_object('short-keratin-digit-tips',vv,ff,mats['keratin'],col)
    vv,ff=merge(features);mesh_object('paired-eyes-nostrils-closed-mouth',vv,ff,mats['facial'],col)
    # Preserve proportional real-world metre scale. Set longitudinal envelope
    # to the cited 5.2 m display estimate and floor contact at zero.
    pts=_vertices_world(col);low,high=_bounds(pts);scale=5.2/(high[1]-low[1]);floor=low[2]
    for obj in col.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices:
                v.co.x*=scale;v.co.y=(v.co.y+.22)*scale;v.co.z=(v.co.z-floor)*scale
    # Fore and hind pads share a true supporting plane; small loft-frame
    # differences must not leave the front pair floating above the floor.
    for side in ['left','right']:
        fore=bpy.data.objects[side+'-supporting-forelimb-oblique-manus']
        delta=min(v.co.z for v in fore.data.vertices)
        for v in fore.data.vertices:v.co.z-=delta
        tips=bpy.data.objects['short-keratin-digit-tips']
        for v in tips.data.vertices:
            if v.co.y<0 and ((v.co.x>0)==(side=='left')):v.co.z-=delta
    bpy.context.view_layer.update()
    root=bpy.data.objects['riojasaurus']
    root['reconstruction']='Whole-animal reconstruction; mounts include restoration. Cast association and accession unknown. Skin, width, pose and color inferred.'
    source=audit_source(col,6500)
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for sp in area.spaces:
                if sp.type=='FILE_BROWSER' and sp.params:sp.params.directory=b'//';sp.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,
      export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
      export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
      export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing required exporter option')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    glb=audit_glb(out/'model.glb',6500,6,12);glb['file']='model.glb'
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
    if glb['errors'] or delta>1e-4 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Invalid export '+str(glb['errors']))
    if glb['bytes']>2000000:raise RuntimeError('Byte budget exceeded')
    write(out/'qa/evidence/technical.json',{'status':'PASS','glb_sha256':sha(out/'model.glb'),'source':source,'glb':glb,
      'source_export_bounds_max_error_m':delta,'runtime':{'blender':bpy.app.version_string,'exporter':'4.3.47','three_target':'0.180.0'},
      'export_options':opts,'origin':'Ground contact centre between fore and hind support pairs. Head -Y, tail +Y, up +Z.',
      'scale':'5.2 m longitudinal display estimate from NHM, not a measured individual. Posture and soft tissues reconstructed.',
      'warnings_review':'Closed overlapping anatomical solids are deliberate. Flat faceting throughout, no procedural shader, rig or external texture.',
      'gpu':'UNKNOWN','scene':'UNKNOWN'})

def render(out,clay=False):
    glb=out/'model.glb';glbhash=sha(glb)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb))
    scene=bpy.context.scene;objects=[o for o in scene.objects if o.type=='MESH']
    points=[o.matrix_world@v.co for o in objects for v in o.data.vertices];lo,hi=_bounds(points)
    center=Vector([(a+b)/2 for a,b in zip(lo,hi)]);span=max(b-a for a,b in zip(lo,hi))
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False
    scene.cycles.samples=8 if clay else P['render']['samples'];res=384 if clay else P['render']['resolution']
    scene.render.resolution_x=scene.render.resolution_y=res;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;_look_at(obj,center)
    data=bpy.data.cameras.new('inspection-camera');cam=bpy.data.objects.new('inspection-camera',data);scene.collection.objects.link(cam);scene.camera=cam
    data.clip_start=.01;data.clip_end=100;data.lens=50
    if clay:bpy.context.view_layer.material_override=make_material('gray-selfcheck','#969696')
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    target=out/'private/clay' if clay else out/'views';target.mkdir(parents=True,exist_ok=True);records=[]
    for name,direction in views.items():
        direction=Vector(direction).normalized();data.type='PERSP' if name=='perspective' else 'ORTHO'
        cam.location=center+direction*span*2.25;_look_at(cam,center);bpy.context.view_layer.update()
        projected=[cam.matrix_world.inverted()@p for p in points]
        width=max(p.x for p in projected)-min(p.x for p in projected);height=max(p.y for p in projected)-min(p.y for p in projected)
        shift=Vector(((max(p.x for p in projected)+min(p.x for p in projected))/2,(max(p.y for p in projected)+min(p.y for p in projected))/2,0))
        cam.location+=cam.matrix_world.to_3x3()@shift;data.ortho_scale=max(width,height)*1.18
        if name=='perspective':
            target_center=center+cam.matrix_world.to_3x3()@shift;basis=cam.rotation_euler.to_matrix().transposed();local=[basis@(p-target_center) for p in points]
            tangent=math.tan(data.angle_x/2);distance=max(max(abs(p.x)/tangent+p.z,abs(p.y)/tangent+p.z) for p in local)*1.18
            cam.location=target_center+direction*distance;_look_at(cam,target_center);bpy.context.view_layer.update()
        scene.render.filepath=str(target/(name+'.png'));bpy.ops.render.render(write_still=True)
        records.append({'path':('private/clay/' if clay else 'views/')+name+'.png','sha256':sha(scene.render.filepath),
          'camera_direction_blender':list(direction),'camera_position_blender_m':list(cam.location),'camera_type':data.type,
          'resolution':[res,res],'source':'Fresh import of exact model.glb'})
    if not clay:
        import shutil
        shutil.copyfile(target/'perspective.png',out/'preview.png')
        write(out/'qa/evidence/views.json',{'status':'RENDERED_PENDING_INDEPENDENT_REVIEW','glb_sha256':glbhash,
          'generator_sha256':sha(__file__),'renderer':'Blender Cycles CPU','settings':P['render'],'images':records,
          'preview':'Byte-identical reuse of perspective.png; no website render contract claimed.','gpu_evidence':False})

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=Path('.'));a.add_argument('--mode',choices=['build','clay','views'],default='build')
opt=a.parse_args(argv);out=opt.output.resolve();out.mkdir(parents=True,exist_ok=True)
if opt.mode=='build':build(out)
else:render(out,opt.mode=='clay')
