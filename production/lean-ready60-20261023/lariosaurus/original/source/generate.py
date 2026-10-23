# SPDX-License-Identifier: MIT
"""Original Lariosaurus valceresii MCSN 8713 reconstruction, metres.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out PATH
Optional --render gray or final produces fresh imports of the exact GLB.
No external runtime files beyond the declared local source/deps and params.json.
"""
from pathlib import Path
import argparse, hashlib, json, math, random, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, ground_asset, audit_source, link_object, _vertices_world, _bounds, _look_at, srgb_to_linear
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
argsv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=HERE.parent); ap.add_argument('--render',choices=['gray','final']); ap.add_argument('--render-only',action='store_true'); A=ap.parse_args(argsv); OUT=A.out.resolve(); OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def sample_path(keys, steps=3):
    # Interpolating Catmull-Rom spline with endpoints fixed.
    result=[]
    for i in range(len(keys)-1):
        p0=keys[max(0,i-1)];p1=keys[i];p2=keys[i+1];p3=keys[min(len(keys)-1,i+2)]
        for j in range(steps):
            t=j/steps
            result.append(tuple(0.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t) for a,b,c,d in zip(p0,p1,p2,p3)))
    result.append(tuple(keys[-1]));return result

def loft_x(name,keys,collection,mat):
    # Keys: x, lateral centre, vertical centre, halfwidth, halfdepth.
    ks=sample_path(keys,3);n=24;vs=[];fs=[]
    for x,y,z,w,h in ks:
        for j in range(n):
            q=2*math.pi*j/n
            vs.append((x,y+max(w,.0006)*math.cos(q),z+max(h,.0006)*math.sin(q)))
    for i in range(len(ks)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.append(tuple(reversed(range(n))));fs.append(tuple((len(ks)-1)*n+j for j in range(n)))
    return mesh_object(name,vs,fs,mat,collection)

def limb(name,keys,sgn,collection,mat):
    ks=sample_path(keys,4);n=20;vs=[];fs=[]
    for i,(x,y,z,w,h) in enumerate(ks):
        a=ks[max(i-1,0)];b=ks[min(i+1,len(ks)-1)];t=Vector((b[0]-a[0],b[1]-a[1],0)).normalized();v=Vector((-t.y,t.x,0))
        for j in range(n):
            q=2*math.pi*j/n;pt=Vector((x,y,z))+v*w*math.cos(q)+Vector((0,0,h*math.sin(q)))
            vs.append((pt.x,sgn*pt.y,pt.z))
    for i in range(len(ks)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.append(tuple(reversed(range(n))));fs.append(tuple((len(ks)-1)*n+j for j in range(n)))
    return mesh_object(name,vs,fs,mat,collection)

def webfoot(name,center,direction,sgn,scale,collection,mat):
    # Five rounded distal caps joined by true continuous shallow interdigital webs.
    # All outline points are original, not traced from a published reconstruction.
    lengths=[.026,.034,.038,.034,.027];rad=.0034
    outline=[(-.009,-.009),(.005,-.023)]
    for i,L in enumerate(lengths):
        v=(i-2)*.009
        if i: outline.append((min(lengths[i-1],L)-.0085,v-.0045))
        for j in range(7):
            q=math.pi-j*math.pi/6
            outline.append((L-rad+rad*math.sin(q),v+rad*math.cos(q)))
    outline +=[(.005,.023),(-.009,.009)]
    cen=Vector((.013,0));n=len(outline);vs=[];fs=[]
    # Convex-in-z layered fan allows thin but volumetric web edges and round tips.
    layers=[(.0,-.0038),(.56,-.0035),(.91,-.0022),(1,0),(.91,.0022),(.56,.0035),(.0,.0038)]
    d=Vector(direction).normalized();v=Vector((-d.y,d.x,0));org=Vector(center)
    for k,(r,z) in enumerate(layers):
        if r==0:
            pt=org+d*cen.x*scale+Vector((0,0,z*scale));vs.append((pt.x,sgn*pt.y,pt.z));continue
        for u,w in outline:
            p=cen+(Vector((u,w))-cen)*r;pt=org+d*p.x*scale+v*p.y*scale+Vector((0,0,z*scale));vs.append((pt.x,sgn*pt.y,pt.z))
    # Five rings between the two poles.
    for j in range(n):fs.append((0,1+(j+1)%n,1+j))
    for ring in range(4):
        a=1+ring*n;b=a+n
        for j in range(n):fs.append((a+j,a+(j+1)%n,b+(j+1)%n,b+j))
    pole=len(vs)-1;a=1+4*n
    for j in range(n):fs.append((a+j,a+(j+1)%n,pole))
    ob=mesh_object(name,vs,fs,mat,collection);ob['digit_count']=5;ob['claws']=False;return ob

def ellipsoid(name,center,radii,mat,collection):
    vs=[];fs=[];n=16;lat=8
    vs.append((center[0],center[1],center[2]-radii[2]))
    for k in range(1,lat):
        a=-math.pi/2+math.pi*k/lat
        for j in range(n):
            q=2*math.pi*j/n;vs.append((center[0]+radii[0]*math.cos(a)*math.cos(q),center[1]+radii[1]*math.cos(a)*math.sin(q),center[2]+radii[2]*math.sin(a)))
    vs.append((center[0],center[1],center[2]+radii[2]));last=len(vs)-1
    for j in range(n):fs.append((0,1+(j+1)%n,1+j))
    for k in range(lat-2):
        for j in range(n):fs.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
    for j in range(n):fs.append((1+(lat-2)*n+j,1+(lat-2)*n+(j+1)%n,last))
    ob=mesh_object(name,vs,fs,mat,collection)
    for p in ob.data.polygons:p.use_smooth=True
    return ob

def tube(name,pts,r,mat,collection):
    vs=[];fs=[];n=8
    for i,p in enumerate(pts):
        t=(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(i-1,0)])).normalized();v=t.cross(Vector((0,0,1))).normalized();w=t.cross(v)
        for j in range(n):
            q=2*math.pi*j/n;vs.append(tuple(Vector(p)+r*(v*math.cos(q)+w*math.sin(q))))
    for i in range(len(pts)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs += [tuple(reversed(range(n))),tuple((len(pts)-1)*n+j for j in range(n))]
    return mesh_object(name,vs,fs,mat,collection)

def build():
    c=setup_scene('lariosaurus',P['seed']);root=bpy.data.objects[c['asset_root']];root['authoring_forward']='+X';root['specimen']='Lariosaurus valceresii MCSN 8713';root['reconstruction']='Original bounded living reconstruction; not a fossil scan';root['nominal_length_m']=.82
    mats=[make_material('Dorsal olive','#667168'),make_material('Quiet tonal facets','#738073'),make_material('Ventral grey olive','#ADB19D'),make_material('Web grey green','#85917D'),make_material('Eyes and closed mouth','#202A26',roughness=.48),make_material('Restrained iris','#B3AC75',roughness=.55)]
    # Trunk 290 mm, neck 160 mm, skull 75.5 mm, tail 294.5 mm: chosen specimen only.
    keys=[(-.4695,.016,.038,.0007,.0007),(-.450,.019,.037,.0022,.0025),(-.415,.021,.036,.0045,.005),(-.370,.020,.036,.008,.008),(-.325,.015,.036,.012,.0105),(-.275,.008,.037,.018,.013),(-.225,.002,.038,.025,.016),(-.175,0,.039,.034,.021),(-.135,0,.040,.042,.025),(-.090,0,.041,.048,.027),(-.025,0,.042,.050,.028),(.040,0,.042,.047,.027),(.085,0,.042,.038,.024),(.115,0,.043,.026,.020),(.145,0,.044,.019,.016),(.180,0,.044,.014,.013),(.220,0,.044,.012,.0115),(.255,0,.044,.011,.011),(.275,0,.044,.012,.011),(.290,0,.044,.015,.011),(.307,0,.044,.0145,.0105),(.320,0,.043,.012,.0085),(.334,0,.042,.0078,.0066),(.343,0,.042,.00665,.005),(.3505,0,.042,.0024,.003)]
    body=loft_x('Axial body neck head and tapered tail',keys,c,mats[0]);parts=[body]
    for sgn,side in [(1,'left'),(-1,'right')]:
        fore=[(.084,.027,.041,.030,.021),(.079,.050,.038,.030,.019),(.065,.080,.031,.022,.014),(.047,.101,.025,.013,.008),(.035,.111,.023,.009,.005)]
        hind=[(-.127,.028,.039,.023,.018),(-.132,.054,.036,.020,.015),(-.143,.083,.030,.015,.010),(-.160,.105,.024,.010,.006),(-.168,.112,.022,.008,.0045)]
        parts.append(limb(side+' robust forelimb and axillary tissue',fore,sgn,c,mats[0]));parts.append(webfoot(side+' five finger webbed manus',(.035,.111,.023),(-.92,.39,0),sgn,1,c,mats[0]))
        parts.append(limb(side+' fleshy hindlimb',hind,sgn,c,mats[0]));parts.append(webfoot(side+' five toe webbed pes',(-.168,.112,.022),(-.94,.34,0),sgn,.94,c,mats[0]))
    # Keep all original semantic loft construction editable in the native blend.
    construction=bpy.data.collections.new('CONSTRUCTION hidden editable lofts');bpy.context.scene.collection.children.link(construction)
    for ob in parts:
        cp=ob.copy();cp.data=ob.data.copy();cp.name='input '+ob.name;cp.parent=None;construction.objects.link(cp);cp.hide_render=True;cp.hide_set(True)
    construction.hide_render=True
    bpy.ops.object.select_all(action='DESELECT')
    for ob in parts:ob.select_set(True)
    bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body.name='Continuous skin with four five digit webbed limbs'
    body.data.remesh_voxel_size=P['voxel_m'];body.data.use_remesh_preserve_volume=True;bpy.ops.object.voxel_remesh()
    smooth=body.modifiers.new('Soft tissue relaxation','SMOOTH');smooth.factor=.28;smooth.iterations=3;bpy.ops.object.modifier_apply(modifier=smooth.name)
    body.data.calc_loop_triangles();rawtris=len(body.data.loop_triangles)
    dec=body.modifiers.new('Silhouette preserving low polygon reduction','DECIMATE');dec.ratio=min(1,P['target_skin_triangles']/rawtris);dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
    bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,dist=1e-7,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
    # Exact overall span is 820 mm, not the 900/980 mm individuals in the table.
    lo=min(v.co.x for v in body.data.vertices);hi=max(v.co.x for v in body.data.vertices)
    for v in body.data.vertices:v.co.x=-.4695+(v.co.x-lo)*.82/(hi-lo)
    body.data.materials.clear()
    for m in mats[:4]:body.data.materials.append(m)
    body.data.update()
    for p in body.data.polygons:
        q=p.center;n=p.normal
        if n.z<-.40:p.material_index=2
        elif abs(q.y)>.101:p.material_index=3
        elif n.z>.15 and math.sin(q.x*303+q.y*179)*math.cos(q.y*221-q.x*51)>.48:p.material_index=1
        else:p.material_index=0
        p.use_smooth=False
    # Closed mouth and living-tissue eyes, not exposed temporal fenestrae.
    for sgn,side in [(1,'left'),(-1,'right')]:
        ellipsoid(side+' eye',(.315,sgn*.0114,.048),(.0036,.0025,.0026),mats[4],c)
        ellipsoid(side+' iris',(.3157,sgn*.01315,.0488),(.00155,.00072,.00155),mats[5],c)
        ellipsoid(side+' pupil',(.3160,sgn*.0137,.0489),(.00075,.00045,.00095),mats[4],c)
        ellipsoid(side+' nostril',(.341,sgn*.0047,.0455),(.001,.00055,.00048),mats[4],c)
        pts=[(.289,sgn*.0136,.0395),(.303,sgn*.0140,.0389),(.317,sgn*.0118,.0383),(.331,sgn*.0083,.0386),(.343,sgn*.0055,.039),(.349,sgn*.0025,.040)]
        tube(side+' closed mouth seam',pts,.00036,mats[4],c)
    # Group facial accents by material to keep low draw-call counts, while inputs stay named above.
    for material,label in [(mats[4],'Eyes pupils nostrils and closed mouth'),(mats[5],'Paired iris accents')]:
        obs=[ob for ob in c.objects if ob.type=='MESH' and ob!=body and ob.data.materials[0]==material]
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();obs[0].name=label
    shift=ground_asset(c,center_xy=False)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    audit=audit_source(c,max_triangles=P['max_triangles']);assert not audit['errors'],audit['errors']
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in c.all_objects:ob.select_set(True)
    opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    rna=bpy.ops.export_scene.gltf.get_rna_type().properties;assert all(k in rna for k in opts),'Exporter option unavailable';bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb(OUT/'model.glb',max_triangles=P['max_triangles'],max_materials=6,max_primitives=16);assert not glb['errors'],glb['errors'];assert (OUT/'model.glb').stat().st_size<2500000
    put(OUT/'qa/evidence/source-audit.json',audit);glb['file']='model.glb';put(OUT/'qa/evidence/glb-audit.json',glb)
    put(OUT/'qa/evidence/build.json',{'status':'PASS','scope':'Maker source and static export checks only','blender':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'seed':P['seed'],'raw_remesh_triangles':rawtris,'skin_target_triangles':P['target_skin_triangles'],'ground_translation_m':shift,'export_settings':{k:v for k,v in opts.items() if k!='filepath'},'orientation':'Blender +X snout +Z dorsal; glTF +X snout +Y dorsal','palette':[m.get('palette_srgb') for m in mats],'construction':'Original axial loft and eight custom limb/foot lofts unified by voxel remesh; hidden editable inputs retained, no third-party mesh','body_dimensions':audit['bounds_blender_m'],'facial_accents':'Closed mouth, paired living eyes, no temporal holes or claws','runtime_gpu':'NOT_RUN','populated_scene':'NOT_RUN'})
    print('BUILD_COMPLETE',glb['sha256'],flush=True)

def render(mode):
    source=OUT/'model.glb';bound=sha(source)
    c=setup_scene('lariosaurus-render');root=bpy.data.objects[c['asset_root']];before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(source));imported=[ob for ob in bpy.data.objects if ob not in before]
    for ob in imported:link_object(ob,c,parent=False)
    for ob in imported:
        if ob.parent not in imported:matrix=ob.matrix_world.copy();ob.parent=root;ob.matrix_world=matrix
    bpy.context.view_layer.update();points=_vertices_world(c);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=12 if mode=='gray' else 64;sc.cycles.use_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=2
    sc.render.resolution_x=sc.render.resolution_y=640 if mode=='gray' else 1400;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False;sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True;bg=world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    cb=world.node_tree.nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1
    lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(bg.outputs[0],mix.inputs[1]);world.node_tree.links.new(cb.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs[0]);sc.world=world
    for name,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=power*span*span/4;data.shape='DISK';data.size=size*span/2;ob=bpy.data.objects.new(name,data);sc.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
    camd=bpy.data.cameras.new('Inspection camera');cam=bpy.data.objects.new('Inspection camera',camd);sc.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=10;sc.camera=cam
    if mode=='gray':bpy.context.view_layer.material_override=make_material('Inspection clay','#8C938C')
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};records=[];dest=OUT/'private/gray' if mode=='gray' else OUT/'views';dest.mkdir(parents=True,exist_ok=True)
    for name,direction in views.items():
        cam.location=center+Vector(direction).normalized()*span*3;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points];bounds=[min(p.x for p in proj),max(p.x for p in proj),min(p.y for p in proj),max(p.y for p in proj)];cam.location+=cam.matrix_world.to_3x3()@Vector(((bounds[0]+bounds[1])/2,(bounds[2]+bounds[3])/2,0));camd.ortho_scale=max(bounds[1]-bounds[0],bounds[3]-bounds[2]) * 1.16
        path=dest/(name+'.png');sc.render.filepath=str(path);bpy.ops.render.render(write_still=True);records.append({'view':name,'camera_direction_blender':direction,'path':str(path.relative_to(OUT)),'sha256':sha(path),'orthographic_scale':camd.ortho_scale})
    assert sha(source)==bound
    if mode=='final':(OUT/'preview.png').write_bytes((dest/'perspective.png').read_bytes())
    evidence={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','glb_sha256':bound,'source':'Clean factory scene imported actual delivered model.glb','blender':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'samples':sc.cycles.samples,'resolution':sc.render.resolution_x,'material_override':'gray' if mode=='gray' else None,'tone_mapping':'Standard, None, exposure 0, gamma 1','background':'#E8E4DC','views':records,'preview_reuses_perspective':mode=='final','generator_sha256':sha(__file__)}
    put((OUT/'private/gray/render-evidence.json') if mode=='gray' else (OUT/'qa/evidence/exact-glb-views.json'),evidence)
if not A.render_only:build()
if A.render:render(A.render)
