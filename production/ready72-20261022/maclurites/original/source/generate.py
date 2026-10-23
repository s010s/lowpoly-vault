# SPDX-License-Identifier: MIT
"""Original Maclurites fossil-shell interpretation, deterministic Blender 4.3.2.
Run: blender -b -t 2 --python source/generate.py -- --out OUTPUT
Render exact export: add --render --clay (for private draft) or --render only.
The only generator imports outside Blender/Python stdlib are declared local deps.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse, shutil
import bpy, bmesh
from mathutils import Vector
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import asset_common as ac
from qa_glb import audit_glb
TAU=math.tau

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save_json(p,x):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def wrap(a): return (a+math.pi)%TAU-math.pi

def make_shell(p, coll):
    n=p['angular_segments']; nr=p['radial_segments']; R=.055
    vertices=[(0.,0.,.0252)]; faces=[]; roles=[]
    def boundary(a):
        # Heavier expanding outer sector faces -Y. Erosion is coherent, not random spikes.
        terminal=math.exp(-(wrap(a+1.35)/.46)**2)
        notch=math.exp(-(wrap(a+.57)/.13)**2)
        return R*(1+.065*math.cos(a+1.5)+.042*math.cos(2*a+.4)+.015*math.sin(5*a+.2)+.009*math.sin(11*a+1.4)+.0045*math.sin(23*a+.3)+.060*terminal-.095*notch)
    def height(r,a,rho):
        phase=p['spiral_turn_coefficient']*(r/R)**p['spiral_radial_exponent']-a/TAU+.17
        sine=math.sin(math.pi*phase)
        groove=math.exp(-(sine/.24)**2)
        # A continuous low fossil surface, with real descending helical sutures.
        roll=abs(sine)**.55
        core=min(1,r/.0045)
        h=(.0200+.0080*roll+.0008*rho)*core+.024*(1-core)
        h-=p['suture_depth_m']*.38*groove*min(1,r/.003)
        h-=.0085*rho**6
        h+=.0010*math.sin(5*a+10*rho)*rho + .00035*math.sin(13*a-16*rho)*rho
        h+=.00014*math.sin(36*rho+3*a)*math.sin(17*a+8*rho)*min(1,r/.006)
        # Broad terminal fracture is shallow/filled, never a restored open tube.
        sector=math.exp(-(wrap(a+1.4)/.34)**2)*max(0,(rho-.64)/.36)
        h-=.0011*sector*(.7+.3*math.sin(14*rho+2*a))
        return h
    for j in range(1,nr+1):
        rho=j/nr
        for i in range(n):
            a=TAU*i/n
            r=boundary(a)*rho
            vertices.append((r*math.cos(a),r*math.sin(a),height(r,a,rho)))
    for i in range(n): faces.append((0,1+i,1+(i+1)%n)); roles.append('top')
    for j in range(nr-1):
        for i in range(n):
            a=1+j*n+i; b=1+j*n+(i+1)%n; c=b+n; d=a+n
            # Alternate diagonals for less rigid concentric tessellation.
            if (i+j)%2: faces.extend([(a,b,d),(b,c,d)])
            else: faces.extend([(a,b,c),(a,c,d)])
            roles.extend(['top','top'])
    # Deliberate low convex wall and a nearly planar basal face.
    prev=[1+(nr-1)*n+i for i in range(n)]
    for band,(factor,ratio,zbase) in enumerate([(1.010,.76,0),(.993,.43,0),(.962,.16,0),(.920,0,.00055),(.87,0,0)]):
        curr=[]
        for i in range(n):
            a=TAU*i/n; r=boundary(a)*factor
            edge_z=height(boundary(a),a,1)
            z=edge_z*ratio+zbase
            if band<3: z+=.00032*math.sin(19*a+.8)*math.sin(math.pi*ratio)
            curr.append(len(vertices)); vertices.append((r*math.cos(a),r*math.sin(a),z))
        for i in range(n):
            k=(i+1)%n
            faces.extend([(prev[i],curr[i],curr[k]),(prev[i],curr[k],prev[k])]); roles.extend(['wall','wall'])
        prev=curr
    bc=len(vertices); vertices.append((0,0,0))
    for i in range(n): faces.append((prev[i],bc,prev[(i+1)%n])); roles.append('bottom')
    # Root stays identity; footprint center is bbox center with basal plane at 0.
    lows=[min(v[k] for v in vertices) for k in range(3)]
    highs=[max(v[k] for v in vertices) for k in range(3)]
    scale=p['diameter']/max(highs[0]-lows[0],highs[1]-lows[1]); zscale=p['height']/highs[2]
    cx=(lows[0]+highs[0])/2; cy=(lows[1]+highs[1])/2
    vertices=[((x-cx)*scale,(y-cy)*scale,z*zscale) for x,y,z in vertices]
    materials=[ac.make_material(name,color,roughness=.94) for name,color in p['palette']]
    obj=ac.mesh_object('weathered_spiral_shell',vertices,faces,materials,coll)
    for poly,role in zip(obj.data.polygons,roles):
        pts=[vertices[k] for k in poly.vertices]; x,y,z=[sum(v[k] for v in pts)/len(pts) for k in range(3)]
        r=math.hypot(x+cx*scale,y+cy*scale)/scale; a=math.atan2(y+cy*scale,x+cx*scale)
        phase=p['spiral_turn_coefficient']*(r/R)**p['spiral_radial_exponent']-a/TAU+.17
        groove=math.exp(-(math.sin(math.pi*phase)/.24)**2)
        patch=.7*math.sin(x*128+y*87+.5)+.45*math.sin(x*258-y*173)+.25*math.sin(x*455+y*340)
        if role=='bottom': idx=3
        elif role=='wall': idx=4 if patch>.1 else 1 if patch>-.35 else 3
        elif groove>.63 and r>.004: idx=2
        elif patch>.62: idx=1
        elif patch<-.6: idx=3
        else: idx=0
        poly.material_index=idx
        poly.use_smooth=(role=='top')
    obj['interpretation']='Original solid fossil shell; underside and terminal preservation simplified, not specimen scan.'
    obj['topology']='Single closed positive-volume heightfield shell with helical sutural depressions and rounded irregular perimeter.'
    obj['scale_basis']='Approximate published diameter 0.11 m; working height 0.03 m is inferred.'
    return obj

def mesh_check(obj):
    bm=bmesh.new(); bm.from_mesh(obj.data)
    volume=bm.calc_volume(signed=True)
    edges_bad=sum(not e.is_manifold for e in bm.edges)
    euler=len(bm.verts)-len(bm.edges)+len(bm.faces)
    remaining=set(bm.verts); comps=0
    while remaining:
        comps+=1; stack=[remaining.pop()]
        while stack:
            for edge in stack.pop().link_edges:
                for v in edge.verts:
                    if v in remaining: remaining.remove(v); stack.append(v)
    result={'status':'pass' if edges_bad==0 and euler==2 and comps==1 and volume>0 else 'fail',
        'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'nonmanifold_edges':edges_bad,
        'euler_characteristic':euler,'connected_components':comps,'signed_volume_m3':volume,
        'minimum_z_m':min(v.co.z for v in bm.verts),
        'base_ring_planar':all(abs(v.co.z)<1e-9 for v in list(bm.verts)[-129:]),
        'self_intersection_scope':'Top is a single-valued polar heightfield; bottom is planar; wall levels monotonically descend with positive noncrossing radial loops. No overlapping assembled whorl tubes. Not a general arbitrary-mesh intersection certifier.'}
    bm.free(); return result

def export_and_check(p,out,coll,obj):
    out.mkdir(parents=True,exist_ok=True); evidence=out/'qa/evidence'; evidence.mkdir(parents=True,exist_ok=True)
    source=ac.audit_source(coll,p['geometry_policy']['max_triangles'])
    geom=mesh_check(obj)
    if source['errors'] or geom['status']!='pass': raise RuntimeError({'source':source,'geometry':geom})
    bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in coll.all_objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['maclurites']
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,
        export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,
        export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,
        export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
        export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    missing=set(options)-{v.identifier for v in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if missing: raise RuntimeError('Missing exporter options '+str(missing))
    bpy.ops.export_scene.gltf(**options)
    gp=p['geometry_policy']; glb=audit_glb(out/'model.glb',gp['max_triangles'],gp['max_materials'],gp['max_primitives'])
    if glb['errors'] or glb['bytes']>gp['max_glb_bytes']: raise RuntimeError(glb)
    b=source['bounds_blender_m']; emin=[b['min'][0],b['min'][2],-b['max'][1]]; emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    assert delta<1e-7 and source['triangles']==glb['scene_triangles']
    for rec in (source,geom): rec['glb_sha256']=digest(out/'model.glb')
    save_json(evidence/'source.json',source); save_json(evidence/'geometry.json',geom); save_json(evidence/'glb.json',glb)
    save_json(evidence/'build.json',{'asset_id':p['asset_id'],'revision':p['revision'],'blender':bpy.app.version_string,
        'generator_sha256':digest(SOURCE/'generate.py'),'params_sha256':digest(SOURCE/'params.json'),
        'brief_sha256':digest(SOURCE.parent/'brief.json'),'reference_sha256':digest(SOURCE.parent/'references.json'),
        'seed':p['seed'],'profile':'original palette-only static closed shell','source_export_bounds_max_error_m':delta,
        'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),
        'export_options':{k:v for k,v in options.items() if k!='filepath'},'consuming_threejs_version':'0.180.0',
        'runtime_gpu':'NOT_RUN','runtime_scene':'NOT_RUN','independent_review':'PENDING',
        'dimensions_blender_m':b['size'],'warnings_reviewed':['Intentional mixed normals: smooth upper whorl faces retain modeled sutural relief, flat outer fracture wall and basal faces retain low-poly weathered edges. No blanket double-sided material.']})

def render_exact(path,out,clay,resolution,samples):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=samples
    scene.cycles.use_denoising=False; scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.render.resolution_x=resolution; scene.render.resolution_y=resolution; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=False; scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
    scene.view_settings.exposure=0; scene.view_settings.gamma=1
    meshes=[o for o in scene.objects if o.type=='MESH']; points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    lo=[min(v[k] for v in points) for k in range(3)]; hi=[max(v[k] for v in points) for k in range(3)]
    center=Vector([(lo[k]+hi[k])/2 for k in range(3)]); span=max(hi[k]-lo[k] for k in range(3))
    world=bpy.data.worlds.new('neutral_world'); world.use_nodes=True; scene.world=world
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
    camera_bg=world.node_tree.nodes.new('ShaderNodeBackground'); camera_bg.inputs['Color'].default_value=tuple(ac.srgb_to_linear(v/255) for v in (232,228,220))+(1,)
    lightpath=world.node_tree.nodes.new('ShaderNodeLightPath'); mix=world.node_tree.nodes.new('ShaderNodeMixShader')
    world.node_tree.links.new(lightpath.outputs['Is Camera Ray'],mix.inputs[0]); world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],mix.inputs[1]); world.node_tree.links.new(camera_bg.outputs[0],mix.inputs[2]); world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs[0])
    if clay:
        m=ac.make_material('gray_clay','#9B9B9B',roughness=.9)
        for ob in meshes:
            ob.data.materials.clear(); ob.data.materials.append(m)
            for poly in ob.data.polygons: poly.material_index=0
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        dat=bpy.data.lights.new(name,'AREA'); dat.energy=energy*span*span/4; dat.shape='DISK'; dat.size=size*span/2
        ob=bpy.data.objects.new(name,dat); scene.collection.objects.link(ob); ob.location=center+Vector(direction)*span/2; ac._look_at(ob,center)
    camdat=bpy.data.cameras.new('camera'); cam=bpy.data.objects.new('camera',camdat); scene.collection.objects.link(cam); scene.camera=cam
    camdat.type='ORTHO'; camdat.ortho_scale=span*1.25; camdat.clip_start=.001; camdat.clip_end=10
    target=Vector((center.x,center.y,center.z)); out.mkdir(parents=True,exist_ok=True)
    records=[]
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=target+Vector(direction).normalized()*span*4; ac._look_at(cam,target)
        scene.render.filepath=str(out/(name+'.png')); bpy.ops.render.render(write_still=True)
        records.append({'view':name,'direction_blender':direction,'target_blender_m':list(target),'orthographic_scale_m':camdat.ortho_scale,'sha256':digest(out/(name+'.png'))})
    save_json(out/'render-record.json',{'glb_sha256':digest(path),'source':'clean import of exact GLB','clay_override':clay,
        'engine':'Cycles CPU','threads':2,'resolution':[resolution,resolution],'samples':samples,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,
        'camera_fit':'Fixed 1.25 times maximum model span, common center and scale across all four views',
        'background_srgb':'#E8E4DC','lighting':'Canonical asset_common key/fill recipe; no exported stage','views':records})

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('--render',action='store_true'); ap.add_argument('--clay',action='store_true'); ap.add_argument('--render-only',action='store_true'); ap.add_argument('--resolution',type=int,default=768); ap.add_argument('--samples',type=int,default=20)
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=Path(args.out).resolve(); p=json.loads((SOURCE/'params.json').read_text()); brief=json.loads((SOURCE.parent/'brief.json').read_text()); p['geometry_policy']=brief['geometry_policy']
    if not args.render_only:
        coll=ac.setup_scene(p['asset_id'],p['seed']); obj=make_shell(p,coll); export_and_check(p,out,coll,obj)
    if args.render:
        target=out/'private/gray' if args.clay else out/'views'; render_exact(out/'model.glb',target,args.clay,args.resolution,args.samples)
        if not args.clay:
            shutil.copyfile(out/'views/perspective.png',out/'preview.png'); shutil.move(str(out/'views/render-record.json'),str(out/'qa/evidence/render-record.json'))
