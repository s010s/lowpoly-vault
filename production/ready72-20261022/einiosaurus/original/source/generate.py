# SPDX-License-Identifier: MIT
"""Original adult Einiosaurus reconstruction. Blender 4.3.2; no external assets.
Usage: blender -b --factory-startup -t 2 -P source/generate.py -- --out DIR --mode build
Modes: gray (source clay diagnostic only), build (source + GLB), render (clean GLB import).
All configuration is in adjacent params.json; helper imports are vendored in deps/.
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
A=argparse.ArgumentParser(); A.add_argument('--out',required=True); A.add_argument('--mode',choices=['gray','build','render'],default='build')
args=A.parse_args(sys.argv[sys.argv.index('--')+1:]); OUT=Path(args.out).resolve(); OUT.mkdir(parents=True,exist_ok=True)
def write(path,obj): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
C=None; M=[]; buckets={}; semantics={}
def add(name,verts,faces,mi):
    """Accumulate closed anatomical solids; semantic vertex groups preserve editing."""
    if isinstance(mi,int): mis=[mi]*len(faces)
    else: mis=mi
    for mat in sorted(set(mis)):
        selected=[f for f,m in zip(faces,mis) if m==mat]
        # Keep a whole manifold anatomical part together, material indices per face.
    buckets[name]=(verts,faces,mis)
def loft(name,rings,n=12,mat=0,shade=False):
    # y, center_z, lateral radius, vertical radius, lateral center
    verts=[]
    foot='_foot_' in name
    if foot: n=6
    for y,z,rx,rz,x in rings:
        if foot:
            verts.extend([(x+rx,y,z),(x+.6*rx,y,z+rz),(x-.6*rx,y,z+rz),(x-rx,y,z),(x-.85*rx,y,0),(x+.85*rx,y,0)])
        else:
            for k in range(n):
                t=2*math.pi*k/n; verts.append((x+rx*math.cos(t),y,z+rz*math.sin(t)))
    faces=[tuple(reversed(range(n)))]; mids=[mat]
    for j in range(len(rings)-1):
        for k in range(n):
            faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
            q=math.sin(2*math.pi*(k+.5)/n)
            mids.append(1 if shade and q>.61 else 2 if shade and q<-.68 else mat)
    faces.append(tuple((len(rings)-1)*n+k for k in range(n)));mids.append(mat)
    add(name,verts,faces,mids)
def tube(name,points,radii,n=9,mat=3,ratio=1):
    vs=[]; rows=[]
    pts=[Vector(p) for p in points]
    for j,(pt,r) in enumerate(zip(pts,radii)):
        if r==0: rows.append([len(vs)]); vs.append(tuple(pt)); continue
        d=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized()
        u=Vector((1,0,0)); u=(u-d*u.dot(d)).normalized()
        if u.length<.1: u=d.cross(Vector((0,0,1))).normalized()
        v=d.cross(u).normalized(); row=[]
        for k in range(n):
            t=k*2*math.pi/n; row.append(len(vs)); vs.append(tuple(pt+u*r*math.cos(t)+v*r*ratio*math.sin(t)))
        rows.append(row)
    fs=[]
    if len(rows[0])>1:fs.append(tuple(reversed(rows[0])))
    for a,b in zip(rows,rows[1:]):
        if len(a)==1:
            fs.extend((a[0],b[(k+1)%n],b[k]) for k in range(n))
        elif len(b)==1:fs.extend((a[k],a[(k+1)%n],b[0]) for k in range(n))
        else:fs.extend((a[k],a[(k+1)%n],b[(k+1)%n],b[k]) for k in range(n))
    if len(rows[-1])>1:fs.append(tuple(rows[-1]))
    add(name,vs,fs,mat)
def ellipsoid(name,center,radii,mat,n=10,stacks=5):
    vs=[(center[0],center[1],center[2]-radii[2])]; fs=[]
    for j in range(1,stacks):
        t=-math.pi/2+math.pi*j/stacks
        for k in range(n):
            a=2*math.pi*k/n
            vs.append((center[0]+radii[0]*math.cos(t)*math.cos(a),center[1]+radii[1]*math.cos(t)*math.sin(a),center[2]+radii[2]*math.sin(t)))
    top=len(vs); vs.append((center[0],center[1],center[2]+radii[2]))
    for k in range(n):fs.append((0,1+(k+1)%n,1+k))
    for j in range(stacks-2):
        for k in range(n): a=1+j*n+k;b=1+j*n+(k+1)%n;fs.append((a,b,b+n,a+n))
    for k in range(n):fs.append((top,1+(stacks-2)*n+k,1+(stacks-2)*n+(k+1)%n))
    add(name,vs,fs,mat)
def create():
    global C,M
    C=setup_scene(P['asset_id'],P['seed']);M=[make_material(k,v,.88) for k,v in P['palette_hex'].items()]
    # Deliberate longitudinal lofts: a deep ribcage, muscular shoulders, tapered pelvis.
    loft('torso',[(y,z,rx,rz,0) for y,z,rx,rz in [(-1.0,1.3,.34,.49),(-.78,1.4,.53,.63),(-.4,1.45,.69,.73),(.15,1.42,.77,.79),(.66,1.4,.74,.76),(1.03,1.35,.57,.65),(1.36,1.24,.31,.45)]],14,shade=True)
    loft('neck',[(-1.73,1.31,.27,.31,0),(-1.5,1.35,.40,.45,0),(-1.1,1.39,.47,.50,0),(-.76,1.38,.45,.49,0)],12,shade=True)
    loft('tail',[(1.12,1.3,.31,.39,0),(1.55,1.22,.27,.31,.02),(2.0,1.07,.18,.22,.08),(2.45,.91,.10,.135,.13),(2.84,.78,.045,.065,.17),(3.18,.72,.004,.006,.2)],10,shade=True)
    # Four weight-bearing limbs have bent knees/hocks, broad spread feet and toes.
    for side in (-1,1):
        x=side*.54
        tube('forelimb_'+str(side),[(x,-.64,1.42),(side*.64,-.68,1.0),(side*.70,-.45,.65),(side*.68,-.70,.25),(side*.68,-.78,.13)],[.27,.235,.17,.145,.19],10,0,1.05)
        tube('hindlimb_'+str(side),[(side*.49,.89,1.35),(side*.65,.94,.94),(side*.68,1.09,.62),(side*.68,.87,.27),(side*.68,.82,.13)],[.37,.28,.19,.15,.20],10,0,1.10)
        for label,y in [('fore',-.81),('hind',.79)]:
            # Horizontal low foot profile, flat sole at Z=0.
            loft(label+'_foot_'+str(side),[(y-.27,.10,.14,.10,side*.68),(y-.16,.12,.235,.12,side*.68),(y+.13,.13,.21,.13,side*.68),(y+.23,.15,.14,.14,side*.68)],10,0)
            for j in (-1,0,1):
                ellipsoid(label+'_nail_'+str(side)+'_'+str(j),(side*.68+j*.108,y-.225,.075),(.057,.085,.05),3,8,4)
    # Broad cheeks taper into a narrow rhamphotheca, not a rhinoceros mammalian muzzle.
    loft('skull',[(y,z,rx,rz,0) for y,z,rx,rz in [(-2.52,1.23,.13,.13),(-2.36,1.35,.23,.23),(-2.13,1.45,.31,.28),(-1.88,1.48,.40,.34),(-1.65,1.46,.43,.37),(-1.39,1.42,.34,.31)]],12,shade=True)
    loft('lower_jaw',[(-2.51,1.135,.10,.09,0),(-2.27,1.15,.21,.13,0),(-1.98,1.19,.29,.17,0),(-1.64,1.22,.38,.19,0)],10,2)
    loft('beak',[(-2.69,1.16,.025,.025,0),(-2.61,1.25,.11,.13,0),(-2.45,1.30,.16,.17,0),(-2.36,1.28,.16,.14,0)],10,3)
    for s in (-1,1):
        ellipsoid('jugal_cheek_'+str(s),(s*.40,-1.7,1.23),(.13,.25,.18),0,9,5)
        ellipsoid('eye_socket_'+str(s),(s*.355,-1.99,1.66),(.095,.135,.11),1,10,5)
        ellipsoid('eye_'+str(s),(s*.424,-2.005,1.68),(.047,.067,.055),5,10,6)
        # Round adult low supraorbital bosses, no long brow horns.
        ellipsoid('supraorbital_boss_'+str(s),(s*.34,-1.99,1.79),(.14,.17,.09),0,10,5)
        ellipsoid('nostril_'+str(s),(s*.255,-2.30,1.43),(.018,.053,.031),5,8,4)
        tube('mouth_line_'+str(s),[(s*.13,-2.53,1.174),(s*.22,-2.31,1.21),(s*.30,-2.07,1.27),(s*.35,-1.89,1.28)],[.008,.011,.011,.003],5,5)
    tube('adult_forward_downcurved_nasal_horn',[(0,-2.10,1.53),(0,-2.08,1.91),(0,-2.18,2.14),(0,-2.39,2.22),(0,-2.59,2.10),(0,-2.73,1.89),(0,-2.76,1.74)],[.205,.195,.16,.126,.086,.045,0],12,3,1.05)
    # Closed soft-tissue-covered neck shield, without fossil fenestra/breakage holes.
    outline=[(0,0),(.37,.08),(.67,.29),(.78,.56),(.72,.82),(.53,1.04),(.25,1.09),(0,1.04),(-.25,1.09),(-.53,1.04),(-.72,.82),(-.78,.56),(-.67,.29),(-.37,.08)]
    vs=[]; n=len(outline)
    def pt(x,h,d):return (x,-1.43+.63*h+d,1.36+h)
    for d in (-.055,.055):
        vs.append(pt(0,.56,d-.055 if d<0 else d))
        vs.extend(pt(x*.57,.56+(h-.56)*.57,d-.035 if d<0 else d) for x,h in outline)
        vs.extend(pt(x,h,d) for x,h in outline)
    layer=1+2*n;fs=[];mi=[]
    for side in range(2):
        off=side*layer
        for j in range(n):
            k=(j+1)%n
            fs.append((off,off+1+j,off+1+k));mi.append(4 if side==0 else 0)
            fs.append((off+1+j,off+1+n+j,off+1+n+k,off+1+k));mi.append(0 if side else 4)
    for j in range(n):k=(j+1)%n;fs.append((1+n+j,1+n+k,layer+1+n+k,layer+1+n+j));mi.append(0)
    add('frill_shield',vs,fs,mi)
    # P3 pair is long and nearly straight; all other marginal processes low.
    for s in (-1,1):
        tube('dominant_P3_'+str(s),[(s*.50,-.84,2.31),(s*.54,-.61,2.49),(s*.60,-.29,2.72),(s*.65,.04,2.96)],[.135,.11,.064,0],10,3,.95)
        for j,(x,h,dx,dh) in enumerate([(.74,.45,.09,.01),(.77,.64,.10,.05),(.68,.86,.09,.08),(.28,1.075,.00,.10)]):
            a=pt(s*x,h,0);b=pt(s*(x+dx),h+dh,0)
            tube('minor_frill_process_'+str(s)+'_'+str(j),[a,b],[.065,0],7,3)
    # A compact dorsal colour band is actual polygon material, not a texture dependency.
    # Assemble into one editable mesh with semantic vertex groups, six material primitives.
    vs=[];fs=[];mis=[];groups=[]
    for name,(v,f,m) in buckets.items():
        off=len(vs);vs.extend(v);fs.extend(tuple(i+off for i in face) for face in f);mis.extend(m);groups.append((name,list(range(off,len(vs)))))
    miny=min(v[1] for v in vs);maxy=max(v[1] for v in vs); scale=P['total_length_target_m']/(maxy-miny)
    # Ground and center intended fore/hind footprint, not the tail-extending bounds.
    minz=min(v[2] for v in vs); foot_y_center=-.03
    vs=[(x*scale,(y-foot_y_center)*scale,(z-minz)*scale) for x,y,z in vs]
    ob=mesh_object('anatomy_editable_semantic_parts',vs,fs,M,C)
    for poly,mat in zip(ob.data.polygons,mis):poly.material_index=mat
    for name,ix in groups:ob.vertex_groups.new(name=name).add(ix,1,'REPLACE')
    ob['editable_parts']='Each anatomical solid is retained as a named vertex group; intentional buried overlaps at muscles/joints.'
    ob['adult_basis']='Wilson & Scannella 2021 Fig8B; McDonald2011 Fig7A/E; life reconstruction.'
    ob['scale_estimate']='NHM genus-level 6m reconstruction; not a measured complete holotype.'
    return C

def render(collection,out,gray=False):
    out.mkdir(parents=True,exist_ok=True)
    pts=_vertices_world(collection);lo,hi=_bounds(pts);center=Vector([(a+b)/2 for a,b in zip(lo,hi)]);span=max(b-a for a,b in zip(lo,hi))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8 if gray else 32;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=400 if gray else 900;scene.render.resolution_y=400 if gray else 900;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    stage=bpy.data.collections.new('_TEMPORARY_RENDER_STAGE');scene.collection.children.link(stage)
    w=bpy.data.worlds.new('neutral_studio');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.42;scene.world=w
    # Camera-visible background and ground share the same neutral colour.
    nodes=w.node_tree.nodes;cam_bg=nodes.new('ShaderNodeBackground');cam_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (235,232,225))+(1,);cam_bg.inputs['Strength'].default_value=1
    lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');w.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);w.node_tree.links.new(nodes['Background'].outputs[0],mix.inputs[1]);w.node_tree.links.new(cam_bg.outputs[0],mix.inputs[2]);w.node_tree.links.new(mix.outputs[0],nodes['World Output'].inputs['Surface'])
    for name,loc,energy,size in [('key',(-3,-4,6),420,4),('fill',(4,-1,3),180,5),('rim',(-1,4,5),230,3)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);stage.objects.link(o);o.location=center+Vector(loc)*span/2;_look_at(o,center)
    mesh_object('_floor',[(-30,-30,-.002),(30,-30,-.002),(30,30,-.002),(-30,30,-.002)],[(0,1,2,3)],make_material('neutral_floor','#EBE8E1',1),stage)
    camd=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',camd);stage.objects.link(cam);camd.type='ORTHO';camd.clip_start=.01;camd.clip_end=100;scene.camera=cam
    if gray:
        clay=make_material('gray_source_only','#A0A0A0',.9);bpy.context.view_layer.material_override=clay
    specs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    meta={}
    for name,d in specs.items():
        if gray and name=='top':continue
        cam.location=center+Vector(d).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();ip=cam.matrix_world.inverted();proj=[ip@p for p in pts]
        xmin,xmax=min(p.x for p in proj),max(p.x for p in proj);ymin,ymax=min(p.y for p in proj),max(p.y for p in proj)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));camd.ortho_scale=max(xmax-xmin,ymax-ymin)*1.18
        scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        meta[name]={'direction_blender':list(d),'orthographic_scale_m':camd.ortho_scale,'sha256':sha(out/(name+'.png'))}
    write(out/'render-record.json',{'source':'authoring gray diagnostic' if gray else 'clean import of exact model.glb','glb_sha256':None if gray else sha(OUT/'model.glb'),'blender':bpy.app.version_string,'engine':'Cycles CPU','resolution':400 if gray else 900,'samples':8 if gray else 32,'views':meta,'color_management':'Standard / None / exposure 0 / gamma 1'})

if args.mode in ('gray','build'):
    C=create()
    if args.mode=='gray':render(C,OUT,True)
    else:
        source=audit_source(C,P['geometry_policy']['max_triangles']);write(OUT/'source-audit.json',source)
        if source['errors']:raise RuntimeError(source['errors'])
        bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
        bpy.ops.object.select_all(action='DESELECT')
        for ob in C.all_objects:ob.select_set(True)
        bpy.context.view_layer.objects.active=bpy.data.objects[P['asset_id']]
        options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
        available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
        if set(options)-available:raise RuntimeError('Unsupported exporter options')
        bpy.ops.export_scene.gltf(**options)
        q=audit_glb(OUT/'model.glb',P['geometry_policy']['max_triangles'],P['geometry_policy']['max_materials'],P['geometry_policy']['max_primitives']);write(OUT/'glb-audit.json',q)
        if q['errors'] or q['bytes']>P['geometry_policy']['max_glb_bytes']:raise RuntimeError(q)
        write(OUT/'build-record.json',{'blender':bpy.app.version_string,'seed':P['seed'],'params_sha256':sha(HERE/'params.json'),'generator_sha256':sha(HERE/'generate.py'),'export_options':{k:v for k,v in options.items() if k!='filepath'},'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'intentional_construction':'Closed anatomical solids retain buried overlaps; no raw reference image or external resource.','triangles':source['triangles'],'materials':len(source['materials'])})
else:
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    C=bpy.data.collections.new('ACTUAL_GLB');bpy.context.scene.collection.children.link(C)
    for ob in list(bpy.context.scene.objects):
        for co in list(ob.users_collection):co.objects.unlink(ob)
        C.objects.link(ob)
    render(C,OUT/'views',False);shutil.copy2(OUT/'views'/'perspective.png',OUT/'preview.png')
