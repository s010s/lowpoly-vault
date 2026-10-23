# SPDX-License-Identifier: MIT
"""Original low-frilled Leptoceratops whole-body reconstruction, Blender 4.3.2.
Usage: blender -b --factory-startup -t 2 -P source/generate.py -- --out OUTPUT --mode build
Modes: build, gray (source-only diagnostics), render (clean exact-GLB import), verify.
Only adjacent params.json and the declared vendored helpers are needed.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _vertices_world, _bounds, _look_at, srgb_to_linear
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mode',choices=['build','gray','render','verify'],default='build')
A=p.parse_args(sys.argv[sys.argv.index('--')+1:]);OUT=Path(A.out).resolve();OUT.mkdir(parents=True,exist_ok=True)
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
parts={}
def add(name,vertices,faces,materials):
    parts[name]=(vertices,faces,[materials]*len(faces) if isinstance(materials,int) else materials)
def loft(name,rings,n=12,mat=0,shade=False):
    # Longitudinal rings: y, center z, width radius, height radius, center x.
    v=[];f=[];m=[]
    for y,z,rx,rz,x in rings:
        for k in range(n):
            a=k*2*math.pi/n;v.append((x+rx*math.cos(a),y,z+rz*math.sin(a)))
    f.append(tuple(reversed(range(n))));m.append(mat)
    for j in range(len(rings)-1):
        for k in range(n):
            f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
            h=math.sin((k+.5)*2*math.pi/n);m.append(1 if shade and h>.68 else 2 if shade and h<-.65 else mat)
    f.append(tuple((len(rings)-1)*n+k for k in range(n)));m.append(mat);add(name,v,f,m)
def tube(name,points,radii,n=10,mat=0,ratio=1):
    vs=[];rows=[];pts=[Vector(x) for x in points]
    for j,(pt,r) in enumerate(zip(pts,radii)):
        if r==0:rows.append([len(vs)]);vs.append(tuple(pt));continue
        d=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized();u=Vector((1,0,0));u=u-d*u.dot(d)
        if u.length<.01:u=d.cross(Vector((0,0,1)))
        u.normalize();v=d.cross(u).normalized();row=[]
        for k in range(n):
            a=k*2*math.pi/n;row.append(len(vs));vs.append(tuple(pt+u*r*math.cos(a)+v*r*ratio*math.sin(a)))
        rows.append(row)
    fs=[]
    if len(rows[0])>1:fs.append(tuple(reversed(rows[0])))
    for a,b in zip(rows,rows[1:]):
        if len(a)==1:fs.extend((a[0],b[(k+1)%n],b[k]) for k in range(n))
        elif len(b)==1:fs.extend((a[k],a[(k+1)%n],b[0]) for k in range(n))
        else:fs.extend((a[k],a[(k+1)%n],b[(k+1)%n],b[k]) for k in range(n))
    if len(rows[-1])>1:fs.append(tuple(rows[-1]))
    add(name,vs,fs,mat)
def oval(name,c,r,mat,n=10,stacks=5):
    vs=[(c[0],c[1],c[2]-r[2])];fs=[]
    for j in range(1,stacks):
        t=-math.pi/2+math.pi*j/stacks
        for k in range(n):
            a=k*2*math.pi/n;vs.append((c[0]+r[0]*math.cos(t)*math.cos(a),c[1]+r[1]*math.cos(t)*math.sin(a),c[2]+r[2]*math.sin(t)))
    top=len(vs);vs.append((c[0],c[1],c[2]+r[2]))
    for k in range(n):fs.append((0,1+(k+1)%n,1+k))
    for j in range(stacks-2):
        for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;fs.append((a,b,b+n,a+n))
    for k in range(n):fs.append((top,1+(stacks-2)*n+k,1+(stacks-2)*n+(k+1)%n))
    add(name,vs,fs,mat)
def foot(name,x,y,width,length):
    # Six-sided transverse sections with completely flat, shared Z=0 soles.
    vs=[]
    for yy,w,h in [(y-length*.62,width*.67,.058),(y-length*.28,width,.083),(y+length*.35,width*.82,.105),(y+length*.56,width*.45,.11)]:
        vs.extend([(x+w,yy,.025),(x+w*.7,yy,h),(x-w*.7,yy,h),(x-w,yy,.025),(x-w*.8,yy,0),(x+w*.8,yy,0)])
    fs=[tuple(reversed(range(6)))]
    for j in range(3):
        for k in range(6):fs.append((j*6+k,j*6+(k+1)%6,(j+1)*6+(k+1)%6,(j+1)*6+k))
    fs.append(tuple(18+k for k in range(6)));add(name,vs,fs,0)
def create():
    C=setup_scene(P['asset_id'],P['seed']);mats=[make_material(k,v,.88) for k,v in P['palette_hex'].items()]
    loft('ribcage',[(y,z,rx,rz,0) for y,z,rx,rz in [(-.56,.59,.15,.19),(-.40,.63,.23,.265),(-.15,.65,.29,.30),(.12,.66,.31,.32),(.36,.68,.285,.31),(.55,.67,.20,.25),(.66,.65,.13,.18)]],14,shade=True)
    loft('short_neck',[(-.79,.70,.145,.18,0),(-.66,.68,.18,.22,0),(-.48,.65,.19,.24,0),(-.36,.63,.20,.24,0)],12,shade=True)
    loft('complete_tail',[(.53,.66,.16,.19,0),(.75,.64,.15,.17,.012),(1.0,.59,.12,.135,.025),(1.25,.54,.083,.097,.035),(1.48,.50,.046,.055,.032),(1.68,.47,.018,.025,.016),(1.78,.455,.002,.003,0)],12,shade=True)
    for s in (-1,1):
        # Short forelimbs and powerfully muscled, longer hindlimbs in a neutral stance.
        tube('forelimb_'+str(s),[(s*.19,-.40,.65),(s*.245,-.39,.47),(s*.26,-.31,.29),(s*.255,-.41,.12),(s*.255,-.43,.065)],[.13,.10,.066,.055,.070],10)
        tube('hindlimb_'+str(s),[(s*.17,.43,.69),(s*.245,.39,.51),(s*.28,.30,.39),(s*.28,.52,.23),(s*.275,.43,.09)],[.185,.15,.115,.073,.067],12,ratio=1.12)
        for label,x,y,w,l in [('fore',s*.255,-.45,.093,.19),('hind',s*.275,.38,.115,.235)]:
            foot(label+'_foot_'+str(s),x,y,w,l)
            for j in (-1,0,1):
                oval(label+'_nail_'+str(s)+'_'+str(j),(x+j*w*.51,y-l*.56,.028),(w*.22,l*.17,.021),3,8,4)
    # Deep compact head: arched dorsal cranium slopes strongly down to a parrot-like beak.
    loft('deep_hornless_skull',[(y,z,rx,rz,0) for y,z,rx,rz in [(-1.18,.67,.055,.10),(-1.09,.73,.12,.15),(-.97,.77,.175,.20),(-.83,.78,.215,.225),(-.68,.76,.22,.22),(-.58,.73,.18,.18)]],14,shade=True)
    # Deep angular dentary, not a small mammalian chin. Closed mouth is a soft-tissue choice.
    loft('deep_lower_jaw',[(-1.18,.555,.045,.045,0),(-1.08,.55,.09,.083,0),(-.96,.54,.145,.11,0),(-.82,.55,.19,.125,0),(-.69,.59,.19,.14,0),(-.61,.63,.155,.12,0)],12,2)
    loft('hooked_upper_beak',[(-1.26,.545,.012,.018,0),(-1.235,.60,.043,.065,0),(-1.19,.665,.075,.100,0),(-1.13,.695,.093,.108,0),(-1.075,.69,.103,.085,0)],10,3)
    loft('lower_beak',[(-1.22,.525,.018,.025,0),(-1.17,.515,.048,.043,0),(-1.075,.535,.085,.052,0)],10,3)
    # The frill is a short low posterior shelf, continuous with the skull roof.
    # A closed shallow loft stays close to the head instead of an upright shield.
    loft('short_low_frill',[(-.82,.89,.155,.075,0),(-.72,.91,.215,.065,0),(-.61,.935,.252,.052,0),(-.50,.945,.245,.035,0),(-.455,.94,.185,.018,0)],14,5)
    for s in (-1,1):
        oval('jugal_cheek_'+str(s),(s*.205,-.69,.645),(.065,.13,.10),0,10,5)
        # Eyes remain lateral; raised eyelid rims are not brow horns.
        oval('eye_rim_'+str(s),(s*.202,-.845,.835),(.044,.066,.055),1,12,5)
        oval('eye_'+str(s),(s*.236,-.851,.836),(.020,.039,.032),4,12,6)
        oval('nostril_'+str(s),(s*.128,-1.068,.765),(.010,.022,.013),4,8,4)
        tube('closed_mouth_'+str(s),[(s*.072,-1.172,.586),(s*.123,-1.06,.608),(s*.17,-.95,.625),(s*.201,-.82,.648),(s*.213,-.73,.655)],[.003,.004,.004,.004,.002],6,4)
    # Merge data, retaining named semantic vertex groups and closed anatomical solids.
    vs=[];fs=[];mi=[];groups=[]
    for name,(v,f,m) in parts.items():
        off=len(vs);vs.extend(v);fs.extend(tuple(i+off for i in face) for face in f);mi.extend(m);groups.append((name,list(range(off,len(vs)))))
    lowy=min(v[1] for v in vs);highy=max(v[1] for v in vs);scale=P['total_length_target_m']/(highy-lowy)
    # Footprint origin lies midway between the fore and hind contacts, never bbox-centered.
    cy=(-.45+.38)/2;vs=[(x*scale,(y-cy)*scale,z*scale) for x,y,z in vs]
    ob=mesh_object('editable_anatomy',vs,fs,mats,C)
    for poly,index in zip(ob.data.polygons,mi):poly.material_index=index
    for name,indices in groups:ob.vertex_groups.new(name=name).add(indices,1,'REPLACE')
    ob['construction']='Closed anatomical solids with intentionally buried muscle and joint overlaps; vertex groups retain editable parts.'
    ob['scientific_scope']='Artistic living reconstruction; museum fossil contexts separate. Short low frill and deep hornless skull.'
    ob['scale_basis']='3 m NHM genus estimate, not a measurement of a photographed individual.'
    return C

def render(C,out,gray=False):
    out.mkdir(parents=True,exist_ok=True);pts=_vertices_world(C);lo,hi=_bounds(pts);center=Vector([(a+b)/2 for a,b in zip(lo,hi)]);span=max(b-a for a,b in zip(lo,hi))
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=8 if gray else 32;sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=sc.render.resolution_y=384 if gray else 800;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    stage=bpy.data.collections.new('_RENDER_ONLY');sc.collection.children.link(stage)
    world=bpy.data.worlds.new('neutral_studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.42;sc.world=world
    nd=world.node_tree.nodes;cam_bg=nd.new('ShaderNodeBackground');cam_bg.inputs['Color'].default_value=tuple(srgb_to_linear(x/255) for x in (235,232,225))+(1,);cam_bg.inputs['Strength'].default_value=1
    lp=nd.new('ShaderNodeLightPath');mix=nd.new('ShaderNodeMixShader');ln=world.node_tree.links;ln.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);ln.new(nd['Background'].outputs[0],mix.inputs[1]);ln.new(cam_bg.outputs[0],mix.inputs[2]);ln.new(mix.outputs[0],nd['World Output'].inputs['Surface'])
    for name,pos,energy,size in [('key',(-3,-4,6),420,4),('fill',(4,-1,3),180,5),('rim',(-1,4,5),230,3)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span**2/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);stage.objects.link(o);o.location=center+Vector(pos)*span/2;_look_at(o,center)
    mesh_object('ground',[(-30,-30,-.002),(30,-30,-.002),(30,30,-.002),(-30,30,-.002)],[(0,1,2,3)],make_material('floor','#EBE8E1',1),stage)
    d=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',d);stage.objects.link(cam);d.type='ORTHO';d.clip_start=.01;d.clip_end=100;sc.camera=cam
    if gray:bpy.context.view_layer.material_override=make_material('gray_diagnostic','#A0A0A0',.9)
    spec={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};views={}
    for name,direction in spec.items():
        if gray and name=='top':continue
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@pt for pt in pts]
        xmin,xmax=min(pt.x for pt in proj),max(pt.x for pt in proj);ymin,ymax=min(pt.y for pt in proj),max(pt.y for pt in proj)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));d.ortho_scale=max(xmax-xmin,ymax-ymin)*1.18
        sc.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        views[name]={'path':('private/gray/' if gray else 'views/')+name+'.png','direction_blender':list(direction),'camera_location_blender_m':list(cam.location),'orthographic_scale_m':d.ortho_scale,'sha256':sha(out/(name+'.png'))}
    return {'source':'authoring source gray diagnostic' if gray else 'clean import of exact model.glb','glb_sha256':None if gray else sha(OUT/'model.glb'),'generator_sha256':sha(HERE/'generate.py'),'blender':bpy.app.version_string,'engine':'Cycles CPU','resolution':[384,384] if gray else [800,800],'samples':8 if gray else 32,'threads':2,'views':views,'color_management':'Standard / None / exposure 0 / gamma 1','background':'neutral studio #EBE8E1','preview_reuses':'perspective exact bytes' if not gray else None}

def imported():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    C=bpy.data.collections.new('ACTUAL_GLB');bpy.context.scene.collection.children.link(C)
    for ob in list(bpy.context.scene.objects):
        for c in list(ob.users_collection):c.objects.unlink(ob)
        C.objects.link(ob)
    return C
if A.mode in ('build','gray'):
    C=create()
    if A.mode=='gray':write(OUT/'render-record.json',render(C,OUT,True))
    else:
        source=audit_source(C,P['geometry_policy']['max_triangles']);write(OUT/'source-audit.json',source)
        if source['errors']:raise RuntimeError(source['errors'])
        bpy.context.preferences.filepaths.save_version=0
        # Remove inherited machine-specific UI destinations before source serialization.
        for scene in bpy.data.scenes:scene.render.filepath='//'
        for screen in bpy.data.screens:
            for area in screen.areas:
                for space in area.spaces:
                    if space.type=='FILE_BROWSER' and space.params:
                        space.params.directory=b'.'*1023;space.params.directory=b'//';space.params.filename=''
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),relative_remap=True)
        bpy.ops.object.select_all(action='DESELECT')
        for ob in C.all_objects:ob.select_set(True)
        bpy.context.view_layer.objects.active=bpy.data.objects[P['asset_id']]
        options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
        available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
        if set(options)-available:raise RuntimeError('Unsupported exporter options: '+str(set(options)-available))
        bpy.ops.export_scene.gltf(**options)
        q=audit_glb(OUT/'model.glb',P['geometry_policy']['max_triangles'],P['geometry_policy']['max_materials'],P['geometry_policy']['max_primitives']);q['file']='model.glb';write(OUT/'glb-audit.json',q)
        if q['errors'] or q['bytes']>P['geometry_policy']['max_glb_bytes']:raise RuntimeError(q)
        write(OUT/'build-record.json',{'blender':bpy.app.version_string,'seed':P['seed'],'params_sha256':sha(HERE/'params.json'),'generator_sha256':sha(HERE/'generate.py'),'export_options':{k:v for k,v in options.items() if k!='filepath'},'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'triangles':source['triangles'],'material_count':len(source['materials']),'editable_semantic_parts':list(parts),'surface':'original texture-free palette; no embedded reference imagery'})
elif A.mode=='render':
    C=imported();record=render(C,OUT/'views');shutil.copy2(OUT/'views/perspective.png',OUT/'preview.png');write(OUT/'qa/evidence/actual-glb-previews.json',record)
else:
    C=imported();pts=_vertices_world(C);lo,hi=_bounds(pts);count=0
    for ob in C.objects:
        if ob.type=='MESH':ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles)
    glb=sha(OUT/'model.glb');bpy.ops.wm.open_mainfile(filepath=str(OUT/'model.blend'))
    export=bpy.data.collections.get('EXPORT');source=audit_source(export,P['geometry_policy']['max_triangles']) if export else {'errors':['Missing EXPORT']}
    unexpected=[ob.name for ob in bpy.context.scene.objects if ob.type in ('CAMERA','LIGHT') or 'RENDER_ONLY' in ob.name]
    write(OUT/'qa/evidence/roundtrip.json',{'glb_sha256':glb,'blender':bpy.app.version_string,'imported_triangles':count,'imported_bounds_blender_m':{'min':lo,'max':hi},'source_reopen_audit':source,'source_cameras_lights':unexpected,'linked_libraries':[x.name for x in bpy.data.libraries],'external_images':[x.name for x in bpy.data.images if x.filepath and not x.packed_file],'status':'PASS' if not source['errors'] and not unexpected else 'FAIL','scope':'Blender clean import and source reopen; not GPU or interactive runtime'})
