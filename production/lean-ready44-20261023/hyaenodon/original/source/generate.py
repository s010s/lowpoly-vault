# SPDX-License-Identifier: MIT
"""Original deterministic Hyaenodon horridus reconstruction. Run in Blender.

Build: blender -b -t 2 --python source/generate.py -- --output . --mode build
Views: blender -b -t 2 --python source/generate.py -- --output . --mode render
The model is an estimate, not a scan or a single-specimen reconstruction.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys, tempfile
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--output',default='.');ap.add_argument('--mode',choices=['build','gray','render'],default='build');A=ap.parse_args(ARGS)
OUT=Path(A.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,d): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def build():
    col=ac.setup_scene('hyaenodon',P['seed'])
    mats=[ac.make_material(k,v,0.88 if k not in ['ivory','dark'] else 0.64) for k,v in P['palette'].items()]
    # Material order: coat, dorsal, ventral, dark, ivory, mucosa.
    store={}
    def add(name,verts,faces,mi=0,face_mats=None):
        entry=store.setdefault(name,[[],[],[]]);o=len(entry[0]);entry[0].extend(verts);entry[1].extend([tuple(i+o for i in f) for f in faces]);entry[2].extend(face_mats if face_mats is not None else [mi]*len(faces))
    def loft(name,rings,sides=12,mi=0,zoning=False):
        # Each ring is (y, center_z, lateral_radius, vertical_radius, center_x).
        vv=[]
        for y,z,rx,rz,x in rings:
            for j in range(sides):
                a=2*math.pi*j/sides;vv.append((x+rx*math.cos(a),y,z+rz*math.sin(a)))
        ff=[tuple(range(sides-1,-1,-1))];fm=[mi]
        for k in range(len(rings)-1):
            for j in range(sides):
                ff.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
                h=math.sin(2*math.pi*(j+0.5)/sides)
                fm.append(1 if zoning and h>0.65 else 2 if zoning and h < -0.4 else mi)
        ff.append(tuple((len(rings)-1)*sides+j for j in range(sides)));fm.append(mi)
        add(name,vv,ff,mi,fm)
    def tube(name,centers,radii,sides=10,mi=0):
        vv=[]
        for i,(c,rr) in enumerate(zip(centers,radii)):
            c=Vector(c);t=(Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(0,i-1)])).normalized()
            u=t.cross(Vector((0,0,1)))
            if u.length<0.1:u=t.cross(Vector((0,1,0)))
            u.normalize();v=t.cross(u).normalized();r1,r2=rr if isinstance(rr,(list,tuple)) else (rr,rr)
            for j in range(sides):
                a=2*math.pi*j/sides;vv.append(tuple(c+u*r1*math.cos(a)+v*r2*math.sin(a)))
        ff=[tuple(range(sides-1,-1,-1))]
        for k in range(len(centers)-1):
            for j in range(sides):ff.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
        ff.append(tuple((len(centers)-1)*sides+j for j in range(sides)))
        add(name,vv,ff,mi)
    def ellipsoid(name,c,r,mi=0,segments=12,rows=6):
        # Deliberate low-resolution profile with single poles; no zero-area caps.
        vv=[(c[0],c[1],c[2]+r[2])]
        for i in range(1,rows):
            a=math.pi*i/rows
            for j in range(segments):
                b=2*math.pi*j/segments;vv.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
        vv.append((c[0],c[1],c[2]-r[2]));end=len(vv)-1;ff=[]
        for j in range(segments):ff.append((0,1+j,1+(j+1)%segments))
        for i in range(rows-2):
            for j in range(segments):ff.append((1+i*segments+j,1+(i+1)*segments+j,1+(i+1)*segments+(j+1)%segments,1+i*segments+(j+1)%segments))
        for j in range(segments):ff.append((1+(rows-2)*segments+j,end,1+(rows-2)*segments+(j+1)%segments))
        add(name,vv,ff,mi)
    # A low elongated trunk; back is near-level rather than modern-hyena slope.
    loft('Torso',[(.34,.405,.035,.045,0),(.30,.422,.078,.092,0),(.23,.425,.099,.105,0),(.12,.441,.090,.089,0),(.02,.424,.105,.106,0),(-.10,.408,.120,.126,0),(-.23,.420,.115,.115,0),(-.32,.440,.097,.093,0),(-.39,.463,.071,.075,0)],16,0,True)
    loft('Neck', [(-.31,.450,.088,.089,0),(-.39,.490,.075,.091,0),(-.46,.529,.063,.084,0),(-.515,.554,.058,.067,0)],14,0,True)
    # Long low skull with deep rear cheek, gradually narrowed muzzle, blunt nose.
    loft('Upper_skull', [(-.495,.586,.051,.068,0),(-.53,.590,.076,.074,0),(-.565,.583,.072,.061,0),(-.594,.576,.064,.051,0),(-.620,.560,.051,.033,0),(-.655,.558,.041,.030,0),(-.710,.551,.033,.025,0),(-.741,.546,.029,.023,0)],14,0,True)
    # Slightly dropped lower jaw turns around a documented hinge, not a yawning snarl.
    hinge=Vector((0,-.505,.540));ang=math.radians(P['jaw_opening_degrees'])
    def drop(v):
        x,y,z=v;dy=y-hinge.y;dz=z-hinge.z
        return (x,hinge.y+dy*math.cos(ang)-dz*math.sin(ang),hinge.z+dy*math.sin(ang)+dz*math.cos(ang))
    jawrings=[(-.506,.518,.054,.037,0),(-.550,.511,.052,.024,0),(-.60,.514,.043,.014,0),(-.665,.519,.031,.011,0),(-.722,.522,.024,.009,0),(-.74,.525,.021,.007,0)]
    loft('Mandible',jawrings,12,2,False)
    store['Mandible'][0]=[drop(v) for v in store['Mandible'][0]]
    # Thin closed inner palate and jaw lining back the oral opening; no fake black billboards.
    loft('Palate', [(-.53,.529,.047,.004,0),(-.59,.529,.045,.004,0),(-.65,.530,.031,.004,0),(-.71,.529,.024,.004,0),(-.739,.526,.020,.003,0)],10,3)
    loft('Lower_oral_lining',[(-.54,.533,.043,.003,0),(-.60,.530,.036,.003,0),(-.67,.531,.027,.003,0),(-.729,.533,.019,.002,0)],10,5)
    store['Lower_oral_lining'][0]=[drop(v) for v in store['Lower_oral_lining'][0]]
    ellipsoid('Nose',(0,-.743,.550),(.028,.013,.018),3,12,5)
    # Eyes and modest ear pinnae are explicitly inferred soft tissues.
    for s in (-1,1):
        ellipsoid('Orbital_brows',(s*.059,-.596,.610),(.016,.020,.012),1,10,4)
        ellipsoid('Eyes',(s*.066,-.598,.604),(.008,.012,.009),3,12,6)
        # Rounded triangular pinna with a thick closed rim.
        verts=[(s*.039,-.504,.615),(s*.077,-.506,.617),(s*.081,-.507,.647),(s*.067,-.509,.675),(s*.052,-.510,.672),(s*.041,-.508,.643),
               (s*.040,-.489,.617),(s*.075,-.490,.620),(s*.077,-.494,.645),(s*.066,-.498,.672),(s*.053,-.499,.670),(s*.043,-.494,.641)]
        faces=[tuple(range(6)),tuple(range(11,5,-1))]+[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)]
        add('Ears',verts,faces,0,[1,0]+[0]*6)
        add('Ear_inner',[(s*.049,-.511,.631),(s*.070,-.511,.632),(s*.071,-.512,.646),(s*.063,-.513,.661),(s*.055,-.513,.657),(s*.050,-.512,.643),
                         (s*.049,-.509,.631),(s*.070,-.509,.632),(s*.071,-.510,.646),(s*.063,-.511,.661),(s*.055,-.511,.657),(s*.050,-.510,.643)],faces,5)
    # Labio-lingually narrow, serried multi-cusped cheek blades, not huge sabres.
    def blade(name,x,y,z,L,W,H,invert=False,lower=False):
        sign=-1 if not invert else 1
        outline=[(-L/2,0),(-L*.30,H*.48),(0,H),(L*.26,H*.54),(L/2,H*.15)]
        vv=[]
        for dx in (-W/2,W/2):
            vv.extend([(x+dx,y+dy,z+sign*h) for dy,h in outline])
        ff=[tuple(range(4,-1,-1)),tuple(range(5,10))]+[(j,(j+1)%5,(j+1)%5+5,j+5) for j in range(5)]
        if lower:vv=[drop(v) for v in vv]
        add(name,vv,ff,4)
    for s in (-1,1):
        for i,(y,x,le,he) in enumerate([(-.557,.048,.020,.020),(-.579,.045,.021,.023),(-.602,.041,.021,.021),(-.625,.036,.020,.018),(-.648,.031,.018,.015),(-.669,.026,.015,.011)]):
            blade('Upper_cheek_teeth',s*x,y,.533,le,.007,he)
            blade('Lower_cheek_teeth',s*(x-.004),y-.005,.532,le*.88,.006,he*.70,True,True)
        tube('Upper_canines',[(s*.0201,-.697,.533),(s*.0208,-.697,.520),(s*.022,-.694,.504),(s*.023,-.690,.499)],[(.006,.0075),(.0055,.006),(.0028,.0035),(.0008,.001)],8,4)
        vs=[(s*.021,-.714,.533),(s*.022,-.715,.545),(s*.022,-.712,.552)]
        tube('Lower_canines',[drop(v) for v in vs],[(.004,.0055),(.0028,.0035),(.0007,.0008)],8,4)
        for x in (.006,.014):
            blade('Incisors',s*x,-.733,.531,.009,.005,.008)
            blade('Incisors',s*x,-.735,.533,.008,.0045,.006,True,True)
    # Four short substantial limbs. Hind stifle points forward, hock backward.
    for s in (-1,1):
        foff=0 if s>0 else .045
        fcent=[(s*.072,-.270+foff,.438),(s*.093,-.260+foff,.378),(s*.103,-.225+foff,.282),(s*.104,-.282+foff,.175),(s*.104,-.308+foff,.082),(s*.104,-.327+foff,.046)]
        tube('Forelimb_R' if s>0 else 'Forelimb_L',fcent,[(.052,.060),(.047,.054),(.036,.037),(.026,.027),(.022,.025),(.027,.026)],12,0)
        ellipsoid('Elbow_forms',(s*.108,-.225+foff,.284),(.033,.038,.035),0,10,5)
        hoff=.015 if s>0 else -.045
        hcent=[(s*.083,.235+hoff,.425),(s*.109,.175+hoff,.341),(s*.111,.124+hoff,.268),(s*.107,.234+hoff,.174),(s*.106,.286+hoff,.118),(s*.105,.235+hoff,.045)]
        tube('Hindlimb_R' if s>0 else 'Hindlimb_L',hcent,[(.070,.077),(.056,.061),(.040,.046),(.026,.029),(.024,.023),(.023,.026)],12,0)
        # Flattened six-sided rings at soles give real floor contact, not floating balls.
        for which,ybase in [('front',-.352+foff),('hind',.210+hoff)]:
            xbase=s*.105
            loft('Feet',[(ybase+.042,.034,.026,.024,xbase),(ybase+.012,.027,.037,.027,xbase),(ybase-.024,.020,.036,.020,xbase),(ybase-.044,.017,.027,.017,xbase)],12,0)
            for dx in (-.022,-.0075,.0075,.022):
                # Toe pads and little non-retractile claws, no modern canine breed detail.
                ellipsoid('Toes',(xbase+dx,ybase-.036,.018),(.009,.025,.018),0,8,4)
                tube('Claws',[(xbase+dx,ybase-.054,.014),(xbase+dx,ybase-.063,.010),(xbase+dx,ybase-.069,.006)],[(.0035,.004),(.0025,.003),(.0008,.0008)],6,3)
    # Muscular base and continuous long low taper, with mild lateral bend at tip.
    tailcent=[(0,.300,.444),(0,.368,.418),(.012,.438,.367),(.026,.511,.309),(.047,.586,.263),(.070,.660,.232),(.091,.724,.210),(.106,.767,.199),(.112,.790,.195)]
    length=sum((Vector(tailcent[i+1])-Vector(tailcent[i])).length for i in range(len(tailcent)-1))
    base=Vector(tailcent[0]);tailcent=[tuple(base+(Vector(c)-base)*(P['tail_path_length_estimate_m']/length)) for c in tailcent]
    tube('Long_tail',tailcent,[(.041,.044),(.037,.040),(.030,.032),(.023,.027),(.019,.021),(.014,.016),(.010,.011),(.0055,.0065),(.0015,.002)],12,0)
    contacts=[v for n in ('Feet','Toes','Claws') for v in store[n][0] if v[2]<0.00001]
    origin_shift=[-(min(v[i] for v in contacts)+max(v[i] for v in contacts))/2 for i in (0,1)]+[0]
    for name,(vv,ff,fm) in store.items():
        vv=[tuple(v[i]+origin_shift[i] for i in range(3)) for v in vv]
        used=sorted(set(fm));obj=ac.mesh_object(name,vv,ff,[mats[i] for i in used],col)
        for poly,idx in zip(obj.data.polygons,fm):poly.material_index=used.index(idx)
        obj['anatomy_component']=name
    bpy.context.scene['reconstruction_status']='Living size and soft tissues estimated; not a complete measured specimen.'
    bpy.context.scene['specimen_measurement_separation']='Fig.8 caption 0.25m skull; SDSM493 and SDSM3017 canine measurements are separate specimens.'
    # The footprint origin is centered between four support limbs, not the tail bbox.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
    for image in list(bpy.data.images):
        if not image.users: bpy.data.images.remove(image)
    bpy.context.scene.render.filepath='//renders/'
    source=ac.audit_source(col,16000)
    with tempfile.TemporaryDirectory(prefix='build-',dir=OUT) as temp:
        record=ac.export_asset('hyaenodon',{'en':'Hyaenodon horridus','zh':'恐鬣齿兽'},'mammals',col,output_root=temp,render=False,diagnostics=False,max_triangles=16000,max_materials=6,max_primitives=48,metadata={'generator':'source/generate.py'})
        product=Path(temp)/'hyaenodon'
        shutil.copy2(product/'hyaenodon.glb',OUT/'model.glb');shutil.copy2(product/'hyaenodon.blend',OUT/'model.blend')
        raw=json.loads((product/'qa.json').read_text())
    raw['glb']['file']='model.glb'
    raw['artifact']={'path':'model.glb','sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend')}
    raw['source_generator_sha256']=sha(HERE/'generate.py');raw['parameters_sha256']=sha(HERE/'params.json')
    raw['runtime']={'blender':bpy.app.version_string,'gltf_exporter':'4.3.47','threads':2,'seed':P['seed'],'export_options':record['export_options']}
    raw['scope']='Source geometry, exact static GLB and source-export bounds only. Not independent, GPU or populated-scene acceptance.'
    raw['dimensions_and_scale']={'glb_bounds_m':record['bounds_glb_m'],'estimated_shoulder_height_m':P['shoulder_height_estimate_m'],'skull_length_target_m':P['skull_length_m'],'estimated_head_body_length_m':P['head_body_length_estimate_m'],'tail_centerline_m':sum((Vector(tailcent[i+1])-Vector(tailcent[i])).length for i in range(len(tailcent)-1)),'root_origin':'Center of floor-contact footprint; identity transform','origin_shift_m':origin_shift,'skull_reference':'Unnumbered Fig.8 25cm caption. Not assigned to either SDSM tooth-measurement specimen.'}
    put(OUT/'qa/evidence/technical.json',raw)
    print('BUILD_COMPLETE',json.dumps({'sha256':raw['artifact']['sha256'],'triangles':raw['glb']['scene_triangles'],'bytes':raw['glb']['bytes']}))

def render(gray=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.cycles.samples=8 if gray else P['render']['samples_final'];scene.cycles.use_denoising=False
    resolution=384 if gray else P['render']['resolution_final'];scene.render.resolution_x=resolution;scene.render.resolution_y=resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    objects=[o for o in scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
    low=Vector([min(v[i] for v in points) for i in range(3)]);high=Vector([max(v[i] for v in points) for i in range(3)]);center=(low+high)/2;span=max(high-low)
    world=bpy.data.worlds.new('Neutral_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;ac._look_at(obj,center)
    camdata=bpy.data.cameras.new('QA_camera');cam=bpy.data.objects.new('QA_camera',camdata);scene.collection.objects.link(cam);camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=span*30;scene.camera=cam
    if gray: scene.view_layers[0].material_override=ac.make_material('QA_clay','#929292',.88)
    output=OUT/'private/gray' if gray else OUT/'views';output.mkdir(parents=True,exist_ok=True);receipt={'artifact_sha256':sha(OUT/'model.glb'),'source':'Clean import of delivered model.glb','render_engine':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':[resolution,resolution],'samples':scene.cycles.samples,'threads':2,'color':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'transparent':True,'lights':'Canonical helper two-area neutral key/fill, no baked lighting.','views':[]}
    for view,direction in P['render']['directions'].items():
        cam.location=center+Vector(direction).normalized()*span*4;ac._look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();pp=[inv@v for v in points]
        bounds=[[min(v[i] for v in pp),max(v[i] for v in pp)] for i in range(2)];shift=Vector([(b[0]+b[1])/2 for b in bounds]+[0]);cam.location+=cam.matrix_world.to_3x3()@shift;camdata.ortho_scale=max(b[1]-b[0] for b in bounds)*1.15
        scene.render.filepath=str(output/(view+'.png'));bpy.ops.render.render(write_still=True)
        receipt['views'].append({'name':view,'path':('private/gray/' if gray else 'views/')+view+'.png','sha256':sha(output/(view+'.png')),'camera_direction':direction,'camera_location_m':list(cam.location),'orthographic_scale_m':camdata.ortho_scale})
    if not gray:shutil.copy2(output/'perspective.png',OUT/'preview.png')
    put((OUT/'private/gray/render-receipt.json') if gray else (OUT/'qa/evidence/render-receipt.json'),receipt)

if A.mode=='build':build()
else:render(A.mode=='gray')
