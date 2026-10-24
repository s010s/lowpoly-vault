# SPDX-License-Identifier: MIT
"""Original Daeodon shoshonensis living reconstruction, not a specimen scan.
Build: blender -b -t 2 --python source/generate.py -- --output . --mode build
Views: blender -b -t 2 --python source/generate.py -- --output . --mode render
CM1594 is the skeletal form anchor; soft tissues and whole-body size are estimates.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys, tempfile
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
P=json.loads((HERE/'params.json').read_text())
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--output',default='.');ap.add_argument('--mode',choices=['build','gray','render'],default='build');A=ap.parse_args(ARGS)
OUT=Path(A.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,d): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def build():
    col=ac.setup_scene('daeodon',P['seed'])
    mats=[ac.make_material(k,v,.88 if k not in ('ivory','dark') else .65) for k,v in P['palette'].items()]
    store={}
    def add(name,vv,ff,mi=0,fm=None):
        e=store.setdefault(name,[[],[],[]]);o=len(e[0]);e[0].extend(vv);e[1].extend([tuple(i+o for i in f) for f in ff]);e[2].extend(fm if fm is not None else [mi]*len(ff))
    def loft(name,rings,sides=16,mi=0,zoning=False):
        # Explicit cross-section profiles, along body axis; never a scaled sphere.
        vv=[]
        for y,z,rx,rz,x in rings:
            for j in range(sides):
                a=2*math.pi*j/sides;vv.append((x+rx*math.cos(a),y,z+rz*math.sin(a)))
        ff=[tuple(range(sides-1,-1,-1))];fm=[mi]
        for k in range(len(rings)-1):
            for j in range(sides):
                ff.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
                h=math.sin(2*math.pi*(j+.5)/sides)
                fm.append(1 if zoning and h>.7 else 2 if zoning and h<-.6 else mi)
        ff.append(tuple((len(rings)-1)*sides+j for j in range(sides)));fm.append(mi);add(name,vv,ff,mi,fm)
    def tube(name,centers,radii,sides=12,mi=0):
        vv=[]
        for i,(c,rr) in enumerate(zip(centers,radii)):
            c=Vector(c);t=(Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(0,i-1)])).normalized()
            u=Vector((1,0,0))-t*t.x
            if u.length<.1:u=Vector((0,1,0))-t*t.y
            u.normalize();v=t.cross(u).normalized();r1,r2=rr if isinstance(rr,(list,tuple)) else (rr,rr)
            for j in range(sides):
                a=2*math.pi*j/sides;vv.append(tuple(c+u*r1*math.cos(a)+v*r2*math.sin(a)))
        ff=[tuple(range(sides-1,-1,-1))]
        for k in range(len(centers)-1):
            for j in range(sides):ff.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
        ff.append(tuple((len(centers)-1)*sides+j for j in range(sides)));add(name,vv,ff,mi)
    def ellipsoid(name,c,r,mi=0,segments=12,rows=6):
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
    # Narrow deep chest, tucked flank, high withers, restrained hips. Not a pig barrel.
    loft('Torso',[(1.17,1.40,.055,.085,0),(1.08,1.40,.18,.21,0),(.91,1.41,.245,.26,0),(.67,1.39,.25,.28,0),(.42,1.34,.235,.30,0),(.13,1.31,.27,.35,0),(-.12,1.32,.29,.39,0),(-.37,1.37,.275,.42,0),(-.53,1.45,.235,.35,0),(-.64,1.49,.17,.25,0)],16,0,True)
    loft('Neck', [(-.49,1.53,.20,.27,0),(-.64,1.61,.19,.29,0),(-.77,1.70,.18,.27,0),(-.87,1.74,.17,.23,0),(-.94,1.71,.16,.19,0)],16,0,True)
    # Posterior cranial roof is high. The long face remains deep to its broad blunt end.
    loft('Deep_skull',[(-.82,1.80,.125,.19,0),(-.91,1.82,.185,.245,0),(-1.01,1.79,.205,.245,0),(-1.13,1.72,.185,.22,0),(-1.27,1.64,.17,.18,0),(-1.45,1.615,.164,.175,0),(-1.63,1.58,.165,.16,0),(-1.72,1.56,.145,.145,0)],16,0,True)
    # Broad paired lateral zygomatic flanges, positioned behind and below the eyes.
    # They are cheek expansions, not enormous anterior mandibular knobs.
    for s in (-1,1):
        loft('Lateral_cheek_flanges',[(-.89,1.68,.050,.125,s*.16),(-.96,1.64,.115,.16,s*.215),(-1.04,1.59,.115,.15,s*.215),(-1.14,1.55,.082,.095,s*.21),(-1.22,1.54,.028,.045,s*.172)],12,0,True)
    hinge=Vector((0,-.91,1.48));ang=math.radians(P['mouth_open_degrees'])
    def drop(v):
        x,y,z=v;dy=y-hinge.y;dz=z-hinge.z
        return (x,hinge.y+dy*math.cos(ang)-dz*math.sin(ang),hinge.z+dy*math.sin(ang)+dz*math.cos(ang))
    loft('Mandible',[(-.91,1.46,.135,.14,0),(-1.04,1.39,.15,.115,0),(-1.20,1.35,.125,.075,0),(-1.39,1.35,.118,.057,0),(-1.59,1.36,.117,.052,0),(-1.69,1.37,.105,.043,0)],14,2)
    store['Mandible'][0]=[drop(v) for v in store['Mandible'][0]]
    ellipsoid('Small_chin_tubercle',(0,-1.61,1.309),(.041,.043,.023),2,10,4)
    store['Small_chin_tubercle'][0]=[drop(v) for v in store['Small_chin_tubercle'][0]]
    loft('Oral_surfaces',[(-1.02,1.465,.13,.009,0),(-1.20,1.46,.13,.009,0),(-1.40,1.446,.13,.008,0),(-1.61,1.425,.12,.007,0),(-1.70,1.415,.10,.005,0)],12,5)
    loft('Jaw_lining',[(-1.05,1.45,.12,.006,0),(-1.25,1.412,.108,.006,0),(-1.47,1.412,.10,.005,0),(-1.66,1.414,.09,.004,0)],12,5)
    store['Jaw_lining'][0]=[drop(v) for v in store['Jaw_lining'][0]]
    # Slightly convex terminal muzzle, not a circular domestic-pig snout disk.
    loft('Nasal_pad',[(-1.684,1.565,.144,.13,0),(-1.731,1.560,.139,.115,0),(-1.749,1.559,.104,.085,0)],12,1)
    for s in (-1,1):
        ellipsoid('Nostrils',(s*.103,-1.735,1.598),(.028,.014,.019),3,10,5)
        ellipsoid('Orbital_rims',(s*.184,-1.115,1.817),(.038,.054,.040),1,12,5)
        ellipsoid('Eyes',(s*.209,-1.121,1.818),(.015,.031,.022),3,12,5)
        # Modest rounded pinnae. No historic sculpture's exaggerated ears or expression.
        vv=[(s*.12,-.86,1.932),(s*.21,-.848,1.93),(s*.252,-.832,1.994),(s*.236,-.815,2.045),(s*.18,-.825,2.052),(s*.135,-.844,1.995),
            (s*.12,-.82,1.932),(s*.207,-.805,1.93),(s*.245,-.801,1.992),(s*.23,-.795,2.04),(s*.18,-.796,2.048),(s*.135,-.81,1.995)]
        ff=[tuple(range(6)),tuple(range(11,5,-1))]+[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)]
        add('Ears',vv,ff,0,[1,0]+[0]*6)
    # Small conical/bunodont cheek crowns, with clearly readable but non-curling canines.
    # P3 and M1 crown envelope dimensions reproduce Table 2 CM1594 values.
    # Other teeth and complete dental arrangement are stylized, not a dental replica.
    for s in (-1,1):
        for y,x,L,W,H in [(-1.075,.136,.0429,.0448,.039),(-1.132,.134,.0372,.0386,.043),(-1.188,.128,.0435,.0332,.047),(-1.246,.12,.040,.028,.052),(-1.303,.115,.035,.024,.045),(-1.352,.111,.030,.020,.038)]:
            z=1.454-(abs(y)-1.1)*.075
            tube('Upper_cheek_teeth',[(s*x,y,z+.007),(s*x,y,z-.025),(s*x,y-.004,z-H)],[(W/2,L/2),(W*.36,L*.38),(.002,.002)],8,4)
            tube('Lower_cheek_teeth',[drop((s*(x-.009),y-.017,1.416)),drop((s*(x-.009),y-.017,1.447)),drop((s*(x-.009),y-.014,1.462))],[(W*.40,L*.43),(W*.24,L*.24),(.002,.002)],8,4)
        tube('Canines',[(s*.119,-1.46,1.444),(s*.126,-1.464,1.390),(s*.132,-1.454,1.318),(s*.133,-1.435,1.279)],[(.029,.032),(.025,.028),(.015,.016),(.002,.003)],10,4)
        tube('Canines',[drop((s*.102,-1.525,1.416)),drop((s*.112,-1.536,1.469)),drop((s*.116,-1.522,1.503))],[(.020,.023),(.014,.016),(.002,.002)],10,4)
        for x in (.027,.073):
            tube('Incisors',[(s*x,-1.672,1.423),(s*x,-1.679,1.386),(s*x,-1.678,1.380)],[(.018,.018),(.014,.014),(.004,.009)],8,4)
            tube('Incisors',[drop((s*x*.9,-1.659,1.414)),drop((s*x*.9,-1.661,1.443))],[(.015,.015),(.009,.011)],8,4)
    # Long, weight-bearing limbs, with elbow/stifle/hock transitions and no spindly stilts.
    for s in (-1,1):
        tube('Forelimbs',[(s*.205,-.43,1.51),(s*.24,-.405,1.25),(s*.245,-.34,.98),(s*.244,-.43,.73),(s*.242,-.49,.36),(s*.243,-.515,.15)],[(.115,.19),(.10,.15),(.075,.095),(.062,.070),(.048,.054),(.062,.068)],12,0)
        tube('Hindlimbs',[(s*.17,.85,1.45),(s*.215,.77,1.20),(s*.245,.56,.90),(s*.255,.87,.55),(s*.256,.91,.38),(s*.257,.865,.15)],[(.13,.21),(.125,.18),(.080,.105),(.057,.066),(.047,.052),(.059,.068)],12,0)
        for which,y,x in [('fore',-.535,s*.243),('hind',.85,s*.257)]:
            # Paired central digits (III/IV), flat sole at z=0 and separated toe tips.
            for off in (-.051,.051):
                cx=x+off
                vv=[(cx-.044,y-.105,0),(cx+.044,y-.105,0),(cx+.047,y+.065,0),(cx-.047,y+.065,0),
                    (cx-.038,y-.084,.113),(cx+.038,y-.084,.113),(cx+.040,y+.060,.145),(cx-.040,y+.060,.145)]
                ff=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
                add('Paired_hooves',vv,ff,3)
    # Narrow shortish tail, broad root then tapered, not a domestic-pig curl.
    tail=[(0,1.10,1.49),(0,1.21,1.43),(.015,1.29,1.34),(.03,1.33,1.23),(.04,1.35,1.13)]
    length=sum((Vector(tail[i+1])-Vector(tail[i])).length for i in range(len(tail)-1));base=Vector(tail[0]);tail=[tuple(base+(Vector(c)-base)*(P['tail_m']/length)) for c in tail]
    tube('Tail',tail,[(.050,.055),(.039,.042),(.027,.030),(.018,.02),(.006,.007)],12,0)
    contacts=[v for v in store['Paired_hooves'][0] if v[2]==0]
    origin_shift=[-(min(v[i] for v in contacts)+max(v[i] for v in contacts))/2 for i in (0,1)]+[0]
    for name,(vv,ff,fm) in store.items():
        vv=[tuple(v[i]+origin_shift[i] for i in range(3)) for v in vv];used=sorted(set(fm));obj=ac.mesh_object(name,vv,ff,[mats[i] for i in used],col)
        for poly,idx in zip(obj.data.polygons,fm):poly.material_index=used.index(idx)
        obj['anatomy_component']=name
    bpy.context.scene['reconstruction_status']='CM1594 skeletal form anchor. Whole-body dimensions and all soft tissues estimated, not a specimen scan.'
    bpy.context.scene['measurement_separation']='Lucas et al.1998 Table2 CM1594 P3/M1 cheektooth measurements are separate from whole-body estimates and museum approximate six-foot shoulder.'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
    for img in list(bpy.data.images):
        if not img.users:bpy.data.images.remove(img)
    bpy.context.scene.render.filepath='//renders/'
    with tempfile.TemporaryDirectory(prefix='build-',dir=OUT) as temp:
        record=ac.export_asset('daeodon',{'en':'Daeodon shoshonensis','zh':'凶齿兽'},'mammals',col,output_root=temp,render=False,diagnostics=False,max_triangles=16000,max_materials=6,max_primitives=48,metadata={'generator':'source/generate.py'})
        product=Path(temp)/'daeodon';shutil.copy2(product/'daeodon.glb',OUT/'model.glb');shutil.copy2(product/'daeodon.blend',OUT/'model.blend');raw=json.loads((product/'qa.json').read_text())
    raw['glb']['file']='model.glb';raw['artifact']={'path':'model.glb','sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend')};raw['source_generator_sha256']=sha(HERE/'generate.py');raw['parameters_sha256']=sha(HERE/'params.json')
    raw['runtime']={'blender':bpy.app.version_string,'gltf_exporter':'4.3.47','threads':2,'seed':P['seed'],'export_options':record['export_options']}
    raw['scope']='Source geometry, exact static GLB and source-export bounds. Not independent review, GPU or populated-scene acceptance.'
    raw['dimensions_and_scale']={'glb_bounds_m':record['bounds_glb_m'],'estimated_shoulder_height_m':1.80,'estimated_skull_length_m':.90,'estimated_head_body_length_m':3.0,'estimated_cheek_width_m':.66,'estimated_torso_width_m':.58,'tail_centerline_m':sum((Vector(tail[i+1])-Vector(tail[i])).length for i in range(len(tail)-1)),'root_origin':'Center of four-hoof floor-contact footprint; identity transform','origin_shift_m':origin_shift,'anatomical_note':'Lateral cheek expansions are wide; anterior chin tubercle is small, not the huge tubercle of adult Archaeotherium.'}
    put(OUT/'qa/evidence/technical.json',raw);print('BUILD_COMPLETE',json.dumps({'sha256':raw['artifact']['sha256'],'triangles':raw['glb']['scene_triangles'],'bytes':raw['glb']['bytes']}))

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
    output=OUT/'private/gray' if gray else OUT/'views';output.mkdir(parents=True,exist_ok=True);receipt={'artifact_sha256':sha(OUT/'model.glb'),'source':'Clean import of delivered model.glb','render_engine':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':[resolution,resolution],'samples':scene.cycles.samples,'threads':2,'color':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'transparent':True,'lights':'Two-area neutral key/fill, no baked lighting.','views':[]}
    for view,direction in P['render']['directions'].items():
        cam.location=center+Vector(direction).normalized()*span*4;ac._look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();pp=[inv@v for v in points]
        bounds=[[min(v[i] for v in pp),max(v[i] for v in pp)] for i in range(2)];shift=Vector([(b[0]+b[1])/2 for b in bounds]+[0]);cam.location+=cam.matrix_world.to_3x3()@shift;camdata.ortho_scale=max(b[1]-b[0] for b in bounds)*1.15
        scene.render.filepath=str(output/(view+'.png'));bpy.ops.render.render(write_still=True)
        receipt['views'].append({'name':view,'path':('private/gray/' if gray else 'views/')+view+'.png','sha256':sha(output/(view+'.png')),'camera_direction':direction,'camera_location_m':list(cam.location),'orthographic_scale_m':camdata.ortho_scale})
    if not gray:shutil.copy2(output/'perspective.png',OUT/'preview.png')
    put((OUT/'private/gray/render-receipt.json') if gray else (OUT/'qa/evidence/render-receipt.json'),receipt)

if A.mode=='build':build()
else:render(A.mode=='gray')
