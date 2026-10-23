# SPDX-License-Identifier: MIT
"""Euphoberia: deterministic, palette-only genus-level reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
Use --render clay for four low-cost diagnostic views or --render final for
four clean-import exact-GLB evidence views. No external data or images used.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse, shutil
import bpy
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
import asset_common as ac
from qa_glb import audit_glb, read_glb, semantic_digest

P = json.loads((HERE / 'params.json').read_text())
PALETTE = [('chitin', '#75503A'), ('metazonal_crests', '#A67C50'),
           ('spines', '#342D28'), ('legs', '#9C7857'), ('face', '#8D6946'), ('eyes', '#28271F')]
BAGS = {}
SEMANTICS = []

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def bag(name): return BAGS.setdefault(name, {'verts':[], 'faces':[], 'groups':[]})
def add(name, verts, faces, label):
    b=bag(name); n=len(b['verts']); b['verts'].extend(verts)
    b['faces'].extend(tuple(n+i for i in f) for f in faces)
    b['groups'].append((label, n, len(verts)))

def tube(name, points, radii, label, sides=6, tip=False):
    points=[Vector(p) for p in points]; verts=[]; faces=[]
    count=len(points)-1 if tip else len(points)
    for i in range(count):
        tangent=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
        normal=tangent.cross(Vector((0,1,0)))
        if normal.length<0.1: normal=tangent.cross(Vector((1,0,0)))
        normal.normalize(); binormal=tangent.cross(normal).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides
            verts.append(tuple(points[i]+radii[i]*(math.cos(a)*normal+math.sin(a)*binormal)))
    faces.append(tuple(reversed(range(sides))))
    for i in range(count-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    if tip:
        apex=len(verts); verts.append(tuple(points[-1]))
        for j in range(sides): faces.append(((count-1)*sides+j,(count-1)*sides+(j+1)%sides,apex))
    else: faces.append(tuple((count-1)*sides+j for j in range(sides)))
    add(name,verts,faces,label)

def center(y):
    # Gentle curvature, not a broad pose that would erase the long cylindrical form.
    return 0.0018*math.sin((y+0.0485)/0.097*math.pi*1.55)-0.00055

def section(y,rx,rz,z=0.0045,n=16):
    return [(center(y)+rx*math.cos(j*2*math.pi/n),y,z+rz*math.sin(j*2*math.pi/n)) for j in range(n)]

def ring(name, profiles,label,n=16):
    verts=[]; faces=[]
    for y,rx,rz,z in profiles: verts.extend(section(y,rx,rz,z,n))
    faces.append(tuple(reversed(range(n))))
    for i in range(len(profiles)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.append(tuple((len(profiles)-1)*n+j for j in range(n)))
    add(name,verts,faces,label)

def build():
    coll=ac.setup_scene('euphoberia',P['seed'])
    mats={name:ac.make_material(name,col,roughness=0.88) for name,col in PALETTE}
    pitch=0.094/36; start=-0.0470
    # 36 historical raised rings, including the conservative anterior transition.
    # Head and terminal region are additional, simplified extremities.
    for i in range(36):
        num=i+1; y=start+(i+0.5)*pitch
        taper=1-0.13*(max(0,(i-30)/5)**1.5)
        if i==0: taper=0.88
        rx=0.003*taper; rz=0.00275*taper
        profiles=[(y+u*pitch,rx*r,rz*r,0.0045) for u,r in [(-.53,.83),(-.37,.94),(-.05,1.0),(.25,1.0),(.44,.92),(.53,.80)]]
        ring('chitin',profiles,f'ring_{num:02d}_body')
        # Raised metazonal collar remains cylindrical; no flattened lateral armour.
        crest=[(y+u*pitch,rx*r,rz*r,0.0045) for u,r in [(.04,1.007),(.13,1.025),(.31,1.025),(.40,1.005)]]
        ring('metazonal_crests',crest,f'ring_{num:02d}_metazonum')
        pairs=0 if i==0 else 1 if i<4 else 2
        for pair in range(pairs):
            ly=y+((-0.24 if pair==0 else 0.22)*pitch if pairs==2 else 0)
            # Small, alternating walking phase. Each articulated leg has five spans.
            phase=math.sin(i*.83+pair*math.pi)*0.00028
            for sign in [-1,1]:
                x=center(ly); swing=phase*sign
                pts=[(x+sign*0.00165,ly,0.00275),
                     (x+sign*0.0026,ly+swing*.3,0.0029),
                     (x+sign*0.00375,ly+swing*.55,0.0025),
                     (x+sign*0.00475,ly+swing*.8,0.00165),
                     (x+sign*0.00545,ly+swing,0.00055),
                     (x+sign*0.00595,ly+swing-0.00025,0.00011)]
                tube('legs',pts,[.00021,.00020,.00018,.00015,.00012,.00010],f'ring_{num:02d}_pair_{pair+1}_{"L" if sign<0 else "R"}',6)
        if i>0:
            strength=(0.70 if i<4 else 1)*taper
            for sign in [-1,1]:
                # Lateral row: long, posteriorly inclined primary with short anterior branch.
                root=Vector((center(y)+sign*rx*.94,y+pitch*.20,.0045+rz*.13))
                direction=Vector((sign*.91,.22,.34)).normalized()
                length=P['lateral_spine_length_inferred']*strength
                pts=[root,root+direction*length*.40,root+direction*length*.73,root+direction*length]
                tube('spines',pts,[.00031*strength,.00024*strength,.00014*strength,0],f'ring_{num:02d}_lateral_{sign}',6,True)
                fork=pts[1]
                fdir=Vector((sign*.30,-.85,.43)).normalized()
                fl=P['secondary_spine_branch_inferred']*strength
                tube('spines',[fork,fork+fdir*fl*.58,fork+fdir*fl],[.00019*strength,.00011*strength,0],f'ring_{num:02d}_lateral_branch_{sign}',6,True)
                # Subdorsal row is distinct in height and attachment, forming four rows total.
                root=Vector((center(y)+sign*rx*.53,y+pitch*.20,.0045+rz*.84))
                direction=Vector((sign*.40,.20,.89)).normalized()
                length=P['subdorsal_spine_length_inferred']*strength
                tube('spines',[root,root+direction*length*.45,root+direction*length*.76,root+direction*length],[.00029*strength,.00022*strength,.00012*strength,0],f'ring_{num:02d}_subdorsal_{sign}',6,True)
        SEMANTICS.append({'ring':num,'leg_pairs':pairs,'spine_rows':0 if i==0 else 4,'branched_lateral_spines':0 if i==0 else 2})
    # Semicircular, conservative head without predatory mouthparts.
    ring('face',[(-.0508,.00030,.00045,.0040),(-.0505,.00150,.00165,.0041),(-.0496,.00250,.00235,.0043),(-.0482,.00275,.00250,.0044),(-.04685,.00240,.00230,.0045)],'head',16)
    ring('chitin',[(.0467,.00250,.00225,.0045),(.0480,.00235,.00215,.0045),(.0492,.00185,.00170,.0044),(.0500,.0011,.00105,.0043),(.0508,.00025,.0003,.0042)],'terminal_region',16)
    for sign in [-1,1]:
        y=-.0495; x=center(y)
        # Five gently bent antennal spans, intentionally simplified and inferred.
        pts=[(x+sign*.0016,y-.0005,.0044),(x+sign*.0023,y-.0015,.0041),(x+sign*.0030,y-.0026,.0038),(x+sign*.00345,y-.0037,.0035),(x+sign*.00355,y-.0045,.0033)]
        tube('face',pts,[.00024,.00022,.00018,.00014,.00011],f'antenna_{sign}',6)
        # Small dark points only; not an inferred ommatidial arrangement.
        eye=(x+sign*.0022,-.04965,.0051)
        tube('eyes',[(eye[0]-sign*.00020,eye[1],eye[2]),(eye[0]+sign*.00016,eye[1],eye[2])],[.00024,.00021],f'eye_spot_{sign}',8)
    for name, b in BAGS.items():
        obj=ac.mesh_object(name,b['verts'],b['faces'],mats[name],coll)
        for label,start,count in b['groups']:
            vg=obj.vertex_groups.new(name=label); vg.add(list(range(start,start+count)),1,'REPLACE')
    # Locate origin at the center of the actual walking-foot contact footprint.
    feet=[v.co for v in bpy.data.objects['legs'].data.vertices if v.co.z < 0.00035]
    xy=[(min(v[i] for v in feet)+max(v[i] for v in feet))/2 for i in (0,1)]
    for obj in coll.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices: v.co.x-=xy[0]; v.co.y-=xy[1]
    offset=ac.ground_asset(coll,center_xy=False)
    offset[0]-=xy[0]; offset[1]-=xy[1]
    root=bpy.data.objects['euphoberia']
    root['representation']='living-reconstruction'
    root['reconstruction_scope']='brownii measured body; armigera comparative spine restoration'
    root['historical_body_length_m']=P['body_length']
    root['historical_rings']=36
    root['body_length_excludes_antennae']=True
    return coll,offset

def render_exact(glb,out,clay=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    coll=bpy.data.collections.new('EXACT_GLB'); bpy.context.scene.collection.children.link(coll)
    objects=list(bpy.context.scene.objects)
    for o in objects:
        for old in list(o.users_collection): old.objects.unlink(o)
        coll.objects.link(o)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=8 if clay else 32
    scene.cycles.use_denoising=False; scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'; scene.view_settings.exposure=0; scene.view_settings.gamma=1
    res=512 if clay else 1024; scene.render.resolution_x=res; scene.render.resolution_y=res; scene.render.resolution_percentage=100
    world=bpy.data.worlds.new('studio'); world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.40; scene.world=world
    points=ac._vertices_world(coll); lo,hi=ac._bounds(points); target=Vector([(lo[i]+hi[i])/2 for i in range(3)])
    span=max(hi[i]-lo[i] for i in range(3))
    for label,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),190,5)]:
        d=bpy.data.lights.new(label,'AREA'); d.energy=power*span*span/4; d.shape='DISK'; d.size=size*span/2
        o=bpy.data.objects.new(label,d); scene.collection.objects.link(o); o.location=target+Vector(direction)*span/2; ac._look_at(o,target)
    if clay: bpy.context.view_layer.material_override=ac.make_material('diagnostic_clay','#969696')
    d=bpy.data.cameras.new('orthographic_evidence'); camera=bpy.data.objects.new('orthographic_evidence',d)
    scene.collection.objects.link(camera); d.type='ORTHO'; d.clip_start=.0001; d.clip_end=span*30; scene.camera=camera
    out.mkdir(parents=True,exist_ok=True); evidence=[]
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    for label, direction in views.items():
        camera.location=target+Vector(direction).normalized()*span*4; ac._look_at(camera,target); bpy.context.view_layer.update()
        inverse=camera.matrix_world.inverted(); projected=[inverse@v for v in points]
        width=max(p.x for p in projected)-min(p.x for p in projected); height=max(p.y for p in projected)-min(p.y for p in projected)
        shift=Vector(((max(p.x for p in projected)+min(p.x for p in projected))/2,(max(p.y for p in projected)+min(p.y for p in projected))/2,0))
        camera.location+=camera.matrix_world.to_3x3()@shift; d.ortho_scale=max(width,height)*1.15
        scene.render.filepath=str(out/(label+'.png')); bpy.ops.render.render(write_still=True)
        evidence.append({'view':label,'path':('private/clay/' if clay else 'views/')+label+'.png','sha256':sha(out/(label+'.png')),'camera_direction':direction,'camera_position_m':list(camera.location),'ortho_scale_m':d.ortho_scale})
    return {'source':'clean import of exact delivered GLB','glb_sha256':sha(glb),'renderer':'Blender 4.3.2 Cycles CPU','GPU':False,'samples':scene.cycles.samples,'resolution':[res,res],'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'views':evidence}

def main():
    args=argparse.ArgumentParser(); args.add_argument('--output',default='.'); args.add_argument('--render',choices=['none','clay','final'],default='none'); args.add_argument('--render-only',action='store_true')
    a=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=Path(a.output).resolve(); out.mkdir(parents=True,exist_ok=True)
    if not a.render_only:
        coll,offset=build()
        src=ac.audit_source(coll,40000)
        if src['errors']: raise RuntimeError(json.dumps(src))
        bpy.context.scene['source_generator']='source/generate.py'
        bpy.context.preferences.filepaths.save_version=0
        bpy.context.scene.render.filepath='//renders/'
        # Make saved UI directories relative, not workstation-specific.
        for screen in bpy.data.screens:
            for area in screen.areas:
                for space in area.spaces:
                    if space.type=='FILE_BROWSER' and space.params:
                        space.params.directory=b'//'
        bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
        bpy.ops.object.select_all(action='DESELECT')
        for obj in coll.all_objects: obj.select_set(True)
        bpy.context.view_layer.objects.active=bpy.data.objects['euphoberia']
        options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
        available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
        assert not(set(options)-available)
        bpy.ops.export_scene.gltf(**options)
        glb=audit_glb(out/'model.glb',40000,6,8); glb['file']='model.glb'
        if glb['errors']: raise RuntimeError(json.dumps(glb))
        doc,binary,raw=read_glb(out/'model.glb')
        srcmin=src['bounds_blender_m']['min']; srcmax=src['bounds_blender_m']['max']
        expected={'min':[srcmin[0],srcmin[2],-srcmax[1]],'max':[srcmax[0],srcmax[2],-srcmin[1]]}
        actual=glb['bounds_m']
        delta=max(abs(expected[k][i]-actual[k][i]) for k in ['min','max'] for i in range(3))
        assert delta<1e-6 and src['triangles']==glb['scene_triangles']
        write(out/'qa/evidence/technical.json',{'status':'PASS','scope':'source geometry; static GLB audit; axis-transformed bounds; counts; budgets; not official format or GPU','blender':'4.3.2','generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'source':src,'glb':glb,'source_export_bounds_max_error_m':delta,'semantic_digest':semantic_digest(doc,binary),'export_options':{k:v for k,v in options.items() if k!='filepath'},'ground_shift_m':offset,'palette_srgb':dict(PALETTE),'source_editability':'Six semantic material meshes; named per-ring, spine and paired-leg vertex groups; no stage objects.'})
        write(out/'qa/evidence/anatomy.json',{'glb_sha256':sha(out/'model.glb'),'body_length_without_antennae_m':.1016,'body_width_approx_m':.006,'trunk_ring_guide':36,'ordinary_diplosegments':32,'anterior_single_pair_rings':[2,3,4],'apodous_collum_ring':1,'total_leg_pairs':sum(x['leg_pairs'] for x in SEMANTICS),'legs':2*sum(x['leg_pairs'] for x in SEMANTICS),'spine_rows':4,'lateral_forks':70,'spine_count_total':140,'rings':SEMANTICS,'overlap_policy':'Closed anatomical components deliberately overlap at ring joints, leg sockets and spine roots. No external scene geometry.','scientific_limits':'Only brownii body scale and ring guide are anchored; long branching spines use same-genus armigera comparison; head, antennae, pose and color remain inferred.'})
    if a.render!='none':
        clay=a.render=='clay'; dest=out/'private/clay' if clay else out/'views'
        evidence=render_exact(out/'model.glb',dest,clay)
        write(out/('private/clay/render.json' if clay else 'qa/evidence/render.json'),evidence)
        if not clay: shutil.copyfile(dest/'perspective.png',out/'preview.png')

if __name__=='__main__': main()
