# SPDX-License-Identifier: MIT
"""Original Pachyornis elephantopus, deterministic palette-only low-poly reconstruction.
Blender 4.3.2. Run: blender -b -t 2 --python source/generate.py -- --output DIR
Source dependencies are copied, hash-pinned in dependencies.json, and local only.
"""
from pathlib import Path
import argparse, hashlib, json, math, random, sys, shutil
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, ground_asset, _look_at, _vertices_world, _bounds
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
A=argparse.ArgumentParser(); A.add_argument('--output',default=str(HERE.parent)); A.add_argument('--gray',action='store_true'); A.add_argument('--render-final',action='store_true')
args=A.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(args.output).resolve(); OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,indent=2)+'\n')

# Each loft is closed, intentionally faceted, with semantic editable parts.
def tube(name,centers,radii,mat,n=12,phase=0):
    cs=[Vector(c) for c in centers]; verts=[]
    for i,c in enumerate(cs):
        tangent=(cs[min(i+1,len(cs)-1)]-cs[max(0,i-1)]).normalized()
        side=Vector((1,0,0)); side=(side-tangent*side.dot(tangent)).normalized()
        ortho=tangent.cross(side).normalized()
        rx,rz=radii[i] if isinstance(radii[i],(tuple,list)) else (radii[i],radii[i])
        for j in range(n):
            a=2*math.pi*j/n+phase
            verts.append(tuple(c+side*(rx*math.cos(a))+ortho*(rz*math.sin(a))))
    faces=[tuple(range(n-1,-1,-1))]
    for i in range(len(cs)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.append(tuple((len(cs)-1)*n+j for j in range(n)))
    return mesh_object(name,verts,faces,mat,C)

def ellipsoid(name,center,r,mat,n=12,rings=7):
    c=Vector(center); verts=[tuple(c+Vector((0,0,-r[2])))]; faces=[]
    for i in range(1,rings):
        ph=-math.pi/2+math.pi*i/rings
        for j in range(n):
            a=2*math.pi*j/n
            verts.append(tuple(c+Vector((r[0]*math.cos(ph)*math.cos(a),r[1]*math.cos(ph)*math.sin(a),r[2]*math.sin(ph)))))
    top=len(verts); verts.append(tuple(c+Vector((0,0,r[2]))))
    for j in range(n): faces.append((0,1+(j+1)%n,1+j))
    for i in range(rings-2):
        for j in range(n): faces.append((1+i*n+j,1+i*n+(j+1)%n,1+(i+1)*n+(j+1)%n,1+(i+1)*n+j))
    base=1+(rings-2)*n
    for j in range(n): faces.append((base+j,base+(j+1)%n,top))
    return mesh_object(name,verts,faces,mat,C)

def build():
    global C, MAT
    C=setup_scene('pachyornis',seed=P['seed']); rng=random.Random(P['seed'])
    MAT={k:make_material(k,v,roughness=0.88 if k!='eye' else .42) for k,v in P['palette_srgb'].items()}
    # Rear rump to deep breast; no wing or wing-like appendage geometry exists.
    sections=[(.56,.66,.018,.035),(.51,.70,.12,.15),(.40,.73,.245,.235),(.25,.735,.31,.265),(.08,.73,.335,.275),(-.10,.71,.33,.275),(-.25,.69,.285,.255),(-.37,.685,.22,.205),(-.46,.71,.15,.145),(-.50,.74,.05,.07)]
    centers=[(0,y,z) for y,z,rx,rz in sections]
    body=tube('broad-wingless-feathered-trunk',centers,[(rx,rz) for y,z,rx,rz in sections],[MAT['body'],MAT['under']],n=24,phase=math.pi/24)
    for poly in body.data.polygons:
        if poly.center.z < .57: poly.material_index=1
    # Thick, forward-carried neck with a relaxed S, lower neck embedded in breast.
    neckc=[(0,-.39,.68),(0,-.49,.74),(0,-.565,.81),(0,-.61,.90),(0,-.635,.99),(0,-.68,1.055),(0,-.75,1.082),(0,-.79,1.083)]
    neck=tube('forward-curving-feathered-neck',neckc,[(.143,.145),(.132,.13),(.113,.115),(.087,.09),(.066,.073),(.056,.061),(.049,.051),(.040,.045)],[MAT['body'],MAT['under']],n=16)
    for poly in neck.data.polygons:
        if poly.center.y<-.6 and poly.normal.y<-.2: poly.material_index=1
    head=tube('small-rounded-moa-head',[(0,-.735,1.093),(0,-.765,1.106),(0,-.81,1.111),(0,-.851,1.102),(0,-.877,1.087)],[(.025,.037),(.047,.044),(.056,.039),(.045,.034),(.027,.024)],[MAT['body'],MAT['under']],n=16)
    for poly in head.data.polygons:
        if poly.center.z<1.092: poly.material_index=1
    tube('stout-decurved-bill',[(0,-.859,1.089),(0,-.89,1.092),(0,-.93,1.084),(0,-.965,1.071),(0,-.982,1.057)],[(.029,.027),(.032,.024),(.024,.018),(.013,.010),(.0015,.0015)],MAT['bill'],n=12)
    for s,label in [(1,'right'),(-1,'left')]:
        ellipsoid(label+'-small-dark-eye',(s*.0515,-.82,1.117),(.006,.009,.008),MAT['eye'],n=12,rings=6)
        # Exact bone centerline lengths, independent from soft contour.
        hip=Vector((s*.185,.10,.79)); knee=hip+Vector((0,-.24,-math.sqrt(P['femur_m']**2-.24**2)))
        ankle=knee+Vector((0,.22,-math.sqrt(P['tibiotarsus_m']**2-.22**2)))
        foot=ankle+Vector((0,-.115,-math.sqrt(P['tarsometatarsus_m']**2-.115**2)))
        tube(label+'-feathered-thigh',[hip,knee*.6+hip*.4,knee],[.13,.135,.098],[MAT['body'],MAT['under']],n=14)
        # One continuous soft-tissue skin across the hock avoids overlapping endcaps.
        # The exact knee/ankle/foot centerline still retains measured segment lengths.
        legc=[knee,knee.lerp(ankle,.35),knee.lerp(ankle,.7),ankle,ankle.lerp(foot,.2),ankle.lerp(foot,.65),foot]
        tube(label+'-stout-leg-with-short-tarsus',legc,[.082,.067,.045,.056,.048,.040,.047],MAT['legs'],n=12)
        # Three forward digits with separately readable toe channels and claws.
        for idx,(dx,dy) in enumerate([(-.105,-.156),(0,-.214),(.106,-.163)],1):
            toe0=foot+Vector((dx*.15,-.012,-.015))
            tip=foot+Vector((dx,dy,-.034))
            toe1=toe0.lerp(tip,.36)+Vector((0,0,.007)); toe2=toe0.lerp(tip,.76)
            tube(f'{label}-forward-toe-{idx}',[toe0,toe1,toe2,tip],[(.027,.022),(.028,.020),(.020,.016),(.012,.011)],MAT['legs'],n=8)
            end=tip+Vector((dx*.18,-.037,-.007))
            tube(f'{label}-forward-claw-{idx}',[tip-Vector((0,.006,0)),tip.lerp(end,.55)+Vector((0,0,.006)),end],[(.014,.012),(.010,.008),(.0014,.0014)],MAT['bill'],n=8)
        hind=foot+Vector((-s*.035,.105,-.032))
        tube(label+'-small-rear-hallux',[foot+Vector((-s*.025,.01,-.015)),foot.lerp(hind,.6),hind],[(.022,.019),(.019,.016),(.010,.009)],MAT['legs'],n=8)
        tube(label+'-rear-claw',[hind,hind+Vector((-s*.004,.020,-.003)),hind+Vector((-s*.005,.032,-.006))],[(.011,.010),(.007,.006),(.0013,.0013)],MAT['bill'],n=8)
    # Small closed feather wedges aligned rearward over dorsal/side trunk.
    # They are contour accents, not feather planes, not anatomy-bearing wings.
    fv=[]; ff=[]; fm=[]
    for k in range(176):
        y=rng.uniform(-.35,.46); a=rng.uniform(-.1,math.pi+0.1)
        if k%3==0: a=rng.uniform(0,2*math.pi)
        # Interpolate section to remain anchored to actual loft surface.
        pair=next((i for i in range(len(sections)-1) if sections[i][0]>=y>=sections[i+1][0]),len(sections)-2)
        q=(sections[pair][0]-y)/(sections[pair][0]-sections[pair+1][0])
        sec=[sections[pair][j]*(1-q)+sections[pair+1][j]*q for j in range(4)]
        _,z,rx,rz=sec; pos=Vector((rx*math.cos(a)*.989,y,z+rz*math.sin(a)*.989))
        normal=Vector((math.cos(a)/rx,0,math.sin(a)/rz)).normalized(); lateral=Vector((0,1,0)).cross(normal).normalized()
        width=rng.uniform(.013,.025); length=rng.uniform(.045,.075); thick=rng.uniform(.006,.013)
        rear=Vector((0,1,-.10)).normalized(); start=pos-rear*length*.38; end=pos+rear*length*.62
        verts=[start-lateral*width/2,start+lateral*width/2,end,pos+normal*thick,pos-normal*.006]
        b=len(fv); fv.extend(tuple(v) for v in verts)
        faces=[(0,1,3),(1,2,3),(2,0,3),(1,0,4),(2,1,4),(0,2,4)]
        ff.extend(tuple(b+x for x in f) for f in faces); fm.extend([1 if k%5==0 else 0]*6)
    feathers=mesh_object('restrained-rearward-shag-contour',fv,ff,[MAT['body'],MAT['plume']],C)
    for i,p in enumerate(feathers.data.polygons): p.material_index=fm[i]
    # Deliberate shallow scute bands on front of each short tarsus.
    sv=[]; sf=[]
    for s in [-1,1]:
        hip=Vector((s*.185,.10,.79)); knee=hip+Vector((0,-.24,-math.sqrt(P['femur_m']**2-.24**2))); ankle=knee+Vector((0,.22,-math.sqrt(P['tibiotarsus_m']**2-.22**2))); foot=ankle+Vector((0,-.115,-math.sqrt(P['tarsometatarsus_m']**2-.115**2)))
        for i in range(8):
            t=.20+i*.082; c=ankle.lerp(foot,t); width=.039-(.006*t); y=c.y-.041; z=c.z
            b=len(sv); sv.extend([(c.x-width,y,z-.006),(c.x+width,y,z-.006),(c.x+width,y,z+.006),(c.x-width,y,z+.006),(c.x-width,y+.007,z-.006),(c.x+width,y+.007,z-.006),(c.x+width,y+.007,z+.006),(c.x-width,y+.007,z+.006)])
            sf.extend(tuple(b+j for j in f) for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)])
    mesh_object('subtle-tarsal-scutes',sv,sf,MAT['bill'],C)
    shift=ground_asset(C,center_xy=False)
    # Place the center of floor-contact footprint at the identity root.
    foot_points=[v.co for ob in C.all_objects if ob.type=='MESH' and any(k in ob.name for k in ('forward-toe','forward-claw','rear-hallux','rear-claw')) for v in ob.data.vertices]
    footprint_y_shift=-(min(v.y for v in foot_points)+max(v.y for v in foot_points))/2
    for obj in C.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices: v.co.y+=footprint_y_shift
    bpy.context.view_layer.update()
    return C,shift


def render_views(collection,folder,gray=False):
    folder.mkdir(parents=True,exist_ok=True); sc=bpy.context.scene
    sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=12 if gray else 48; sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED'; sc.render.threads=2
    sc.render.resolution_x=sc.render.resolution_y=384 if gray else 768; sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'; sc.render.film_transparent=False
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='None'; sc.view_settings.exposure=0; sc.view_settings.gamma=1
    pts=_vertices_world(collection); lo,hi=_bounds(pts); center=Vector([(lo[i]+hi[i])/2 for i in range(3)]); span=max(hi[i]-lo[i] for i in range(3))
    world=bpy.data.worlds.new('neutral-studio'); world.use_nodes=True; world.node_tree.nodes['Background'].inputs['Color'].default_value=(.72,.72,.72,1); world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25; sc.world=world
    cd=bpy.data.cameras.new('presentation-camera'); cam=bpy.data.objects.new('presentation-camera',cd); sc.collection.objects.link(cam); sc.camera=cam; cd.type='ORTHO'; cd.clip_end=100
    for name,loc,energy,size in [('key',(-3,-4,6),220,4),('fill',(4,-1,3),80,5),('rim',(1,4,5),140,3)]:
        ld=bpy.data.lights.new(name,'AREA'); ld.energy=energy; ld.size=size; ob=bpy.data.objects.new(name,ld); sc.collection.objects.link(ob); ob.location=center+Vector(loc)*span/2; _look_at(ob,center)
    # Studio plane and all lights stay outside the imported EXPORT collection.
    fl=bpy.data.meshes.new('studio-floor-mesh'); fl.from_pydata([(-50,-50,-.003),(50,-50,-.003),(50,50,-.003),(-50,50,-.003)],[],[(0,1,2,3)])
    fo=bpy.data.objects.new('studio-floor',fl); sc.collection.objects.link(fo); fl.materials.append(make_material('studio-neutral','#E8E4DC',roughness=1))
    if gray:
        clay=make_material('gray-study-only','#9A9996')
        for ob in collection.all_objects:
            if ob.type=='MESH':
                ob.data.materials.clear(); ob.data.materials.append(clay)
                for p in ob.data.polygons:p.material_index=0
    records={}
    for label,d in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(d).normalized()*span*4; _look_at(cam,center); bpy.context.view_layer.update(); inv=cam.matrix_world.inverted(); pp=[inv@p for p in pts]
        mn=[min(p[i] for p in pp) for i in range(2)]; mx=[max(p[i] for p in pp) for i in range(2)]
        cam.location+=cam.matrix_world.to_3x3()@Vector(((mn[0]+mx[0])/2,(mn[1]+mx[1])/2,0)); cd.ortho_scale=max(mx[i]-mn[i] for i in range(2))*1.20
        bpy.context.view_layer.update()
        dest=folder/(label+'.png'); sc.render.filepath=str(dest); bpy.ops.render.render(write_still=True)
        records[label]={'path':dest.name,'sha256':sha(dest),'camera_direction':d,'camera_projection':'orthographic','ortho_scale_m':cd.ortho_scale,'camera_location_m':list(cam.location)}
    return {'status':'rendered_not_independently_reviewed','source':'source-scene-gray' if gray else 'clean-import-of-exact-delivered-GLB','renderer':'Blender '+bpy.app.version_string+' Cycles CPU','threads':2,'samples':sc.cycles.samples,'resolution':sc.render.resolution_x,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'views':records}

if args.render_final:
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    C=bpy.data.collections.new('EXACT_GLB_IMPORT'); bpy.context.scene.collection.children.link(C)
    for ob in list(bpy.context.scene.objects):
        for co in list(ob.users_collection): co.objects.unlink(ob)
        C.objects.link(ob)
    rec=render_views(C,OUT/'views'); rec['glb_sha256']=sha(OUT/'model.glb'); shutil.copyfile(OUT/'views/perspective.png',OUT/'preview.png'); rec['preview_reuses']='views/perspective.png'; rec['preview_sha256']=sha(OUT/'preview.png'); write(OUT/'qa/evidence/exact-glb-views.json',rec)
else:
    C,shift=build(); source=audit_source(C,P['budgets']['max_triangles']); assert not source['errors'],source['errors']
    bpy.context.preferences.filepaths.save_version=0; bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in C.all_objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['pachyornis']
    opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}; assert not set(opts)-available
    bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives']); assert not glb['errors'],glb['errors']; glb['file']='model.glb'
    b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}; delta=max(abs(glb['bounds_m'][s][i]-expected[s][i]) for s in expected for i in range(3)); assert delta<.0001
    assert glb['scene_triangles']==source['triangles']; assert (OUT/'model.glb').stat().st_size<=P['budgets']['max_glb_bytes']
    write(OUT/'qa/evidence/build.json',{'status':'PASS','blender_version':bpy.app.version_string,'seed':P['seed'],'source':source,'glb':glb,'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'source_generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'bounds_roundtrip_max_error_m':delta,'ground_shift_m':shift,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'scope':'Maker source and exported static geometry checks only; no independent visual or GPU acceptance.'})
    if args.gray: write(OUT/'private/gray/gray-record.json',render_views(C,OUT/'private/gray',gray=True))
print('PACHYORNIS_STAGE_COMPLETE',OUT)
