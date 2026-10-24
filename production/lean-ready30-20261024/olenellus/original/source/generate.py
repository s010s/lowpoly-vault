# SPDX-License-Identifier: MIT
"""Deterministic original Olenellus living reconstruction and exact-GLB views.

Run inside Blender: --python source/generate.py -- --output .
Diagnostic/final rendering: --render-glb model.glb --render-dir views [--clay]
All project dependencies are declared, package-relative and copied locally.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
import bpy
from mathutils import Vector
from asset_common import (setup_scene, make_material, mesh_object, ground_asset,
                          audit_source, _look_at, _vertices_world, _bounds)
from qa_glb_scale_aware import audit_glb


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def join_geometries(name, pieces, material, collection):
    verts, faces = [], []
    for vv, ff in pieces:
        n = len(verts)
        verts.extend(vv)
        faces.extend(tuple(n + i for i in face) for face in ff)
    return mesh_object(name, verts, faces, material, collection)


def tube(points, radii, sides=8, flatten=1.0):
    """Closed polygonal sweep with stable local cross sections and end caps."""
    verts, faces = [], []
    for i, (point, radius) in enumerate(zip(points, radii)):
        p = Vector(point)
        tangent = Vector(points[min(i + 1, len(points)-1)]) - Vector(points[max(0, i-1)])
        tangent.normalize()
        reference = Vector((0, 0, 1)) if abs(tangent.z) < 0.9 else Vector((1, 0, 0))
        u = tangent.cross(reference).normalized()
        v = tangent.cross(u).normalized()
        for j in range(sides):
            a = 2*math.pi*j/sides
            verts.append(tuple(p + u*(radius*math.cos(a)) + v*(radius*flatten*math.sin(a))))
    for i in range(len(points)-1):
        for j in range(sides):
            a, b = i*sides+j, i*sides+(j+1)%sides
            faces.append((a, b, b+sides, a+sides))
    faces += [tuple(reversed(range(sides))), tuple((len(points)-1)*sides+j for j in range(sides))]
    return verts, faces


def longitudinal_loft(name, rows, material, collection, sides=12):
    """Rows: y, half-width, center-z, vertical radius; closed at both ends."""
    verts, faces = [], []
    for y, w, z, h in rows:
        for j in range(sides):
            a = 2*math.pi*j/sides
            verts.append((w*math.cos(a), y, z+h*math.sin(a)))
    for i in range(len(rows)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    faces += [tuple(reversed(range(sides))), tuple((len(rows)-1)*sides+j for j in range(sides))]
    return mesh_object(name,verts,faces,material,collection)


def build(params, output):
    c=setup_scene(params['asset_id'],params['seed'])
    mats={k:make_material('Olenellus-'+k,v,roughness=0.86) for k,v in params['palette'].items()}
    outline=[]
    for i in range(25):
        a=math.pi-i*math.pi/24
        outline.append((25*math.cos(a),-6-24*math.sin(a)))
    outline.extend([(19,-4.6),(13,-5.5),(7,-7.2),(0,-8.0),(-7,-7.2),(-13,-5.5),(-19,-4.6)])
    n=len(outline); verts=[]
    for r,z in [(1,4.5),(.91,6.2),(.64,9.0),(.30,10.1)]:
        verts.extend((x*r,-15+(y+15)*r,z) for x,y in outline)
    verts.append((0,-15,10.5)); center=len(verts)-1
    faces=[]; regions=[]
    for k in range(3):
        for i in range(n):
            faces.append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i));regions.append(1 if k==0 else 0)
    for i in range(n):
        faces.append((3*n+i,3*n+(i+1)%n,center));regions.append(0)
    bottom=len(verts);verts.extend((x,y,3.1) for x,y in outline)
    for i in range(n):
        faces.append((i,bottom+i,bottom+(i+1)%n,(i+1)%n));regions.append(0)
    faces.append(tuple(bottom+i for i in reversed(range(n))));regions.append(0)
    obj=mesh_object('Crescent-cephalon',verts,faces,[mats['cuticle'],mats['border']],c)
    for p,reg in zip(obj.data.polygons,regions):p.material_index=reg
    obj['anatomical_basis']='Dorsal P12142 outline; raised thickness inferred.'
    longitudinal_loft('Lobate-central-glabella',[
        (-26,1.9,7.0,1.0),(-23.8,4.4,9.0,2.8),(-21,5.2,10.1,3.0),
        (-18.5,4.1,10.4,2.8),(-16.8,4.5,10.5,2.9),(-14.4,3.9,10.2,2.8),
        (-12.5,4.1,9.8,2.8),(-10.6,3.5,9.3,2.3),(-8,3.4,8.5,1.7),(-6.2,3.1,7.2,1.1)],mats['axial'],c)
    for s,label in [(-1,'left'),(1,'right')]:
        join_geometries('Long-genal-spine-'+label,[tube([
            (s*23.0,-7,4.8),(s*25.6,-2,4.5),(s*26.0,5,3.8),
            (s*24.6,13,3.0),(s*22.2,21.5,2.2)], [2.1,1.7,1.15,.62,.11],8,.75)],mats['cuticle'],c)
        join_geometries('Crescent-eye-ridge-'+label,[tube([
            (s*7.2,-23,9.0),(s*9.9,-20,10.2),(s*10.6,-16.5,10.1),
            (s*9.3,-13,9.5),(s*7.2,-10.8,8.9)],[.32,.74,.83,.72,.28],8,.65)],mats['eyes'],c)
        join_geometries('Inferred-antenna-'+label,[tube([
            (s*3.8,-23,3.1),(s*4.7,-28,3.0),(s*6.2,-32.7,3.5),
            (s*9.0,-36.4,3.8),(s*12.3,-38.0,3.4)],[.72,.58,.43,.29,.11],7)],mats['underside'],c)
    leg_pieces={-1:[],1:[]}; branch_pieces={-1:[],1:[]}
    for y,w in [(-20,12),(-14,15),(-8,16)]:
        for s in [-1,1]:
            leg_pieces[s].append(tube([(s*2,y,2.7),(s*5,y+.1,2.1),
                (s*w*.73,y+1.2,1.9),(s*w,y+2.6,.38)],[.69,.66,.48,.13],6,.75))
            branch_pieces[s].append(tube([(s*2.2,y+.2,2.3),(s*5.2,y-1.1,2.4),
                (s*w*.87,y-.3,2.0)],[.42,.65,.11],6,.30))
    N=params['main_segments']
    for i in range(N):
        t=i/(N-1); y=-5.7+2.55*i
        width=17.3*(1-.73*t**1.2); axis=4.4*(1-.59*t)
        ring_depth=2.08*(1-.16*t); height=8.5-3.1*t
        xs=[-1,-.85,-.62,-axis/width,-.7*axis/width,0,.7*axis/width,axis/width,.62,.85,1]
        verts=[]
        for u in xs:
            x=u*width; au=abs(u)
            sweep=3.0*au**2.1*(1-.25*t)
            if au<axis/width: z=height+1.0*(1-(au/(axis/width))**2)
            else: z=height-2.5-1.1*(au-axis/width)/(1-axis/width)
            depth=ring_depth*(1-.79*au**2.4)
            verts.extend([(x,y+sweep-depth/2,z-.35),(x,y+sweep,z+.40),
                          (x,y+sweep+depth/2,z-.35),(x,y+sweep+depth/2,z-1.25),
                          (x,y+sweep-depth/2,z-1.25)])
        faces=[]; tags=[]
        for k in range(len(xs)-1):
            for j in range(5):faces.append((k*5+j,k*5+(j+1)%5,(k+1)*5+(j+1)%5,(k+1)*5+j));tags.append(1 if abs((xs[k]+xs[k+1])/2)<axis/width else 0)
        faces.extend([tuple(reversed(range(5))),tuple((len(xs)-1)*5+j for j in range(5))]);tags.extend([0,0])
        ob=mesh_object(f'Articulated-thorax-{i+1:02d}',verts,faces,[mats['cuticle'],mats['axial']],c)
        for poly,tag in zip(ob.data.polygons,tags):poly.material_index=tag
        for s in [-1,1]:
            legspan=width*.87
            leg_pieces[s].append(tube([(s*1.5,y,2.7),(s*min(4,legspan*.46),y+.1,2.1),
                (s*legspan*.68,y+1.2,1.9),(s*legspan,y+2.6,.38)], [.69,.66,.48,.13],6,.75))
            branch_pieces[s].append(tube([(s*1.6,y+.2,2.3),(s*min(5.2,legspan*.64),y-1.1,2.4),
                (s*legspan*.87,y-.3,2.0)], [.42,.65,.11],6,.30))
    for s,label in [(-1,'left'),(1,'right')]:
        a=join_geometries('Inferred-walking-limbs-'+label,leg_pieces[s],mats['underside'],c)
        a['anatomical_basis']='Generic inferred soft underside; not diagnostic fossil evidence.'
        join_geometries('Inferred-short-limb-branches-'+label,branch_pieces[s],mats['underside'],c)
    longitudinal_loft('Inferred-intersegment-body',[(-24,3.0,2.8,1),(-21,8.0,2.8,1),
        (-10,13.3,3.2,1.1),(0,13.4,3.2,1.1),(12,9.8,2.7,1),
        (25,4.5,2.2,.8),(29,2.3,2.3,.5)],mats['underside'],c)
    longitudinal_loft('Small-terminal-shield',[(27.7,2.8,4.2,1.1),(30,2.3,3.8,.9),(32.0,.8,3.1,.5)],mats['cuticle'],c)
    join_geometries('Single-posterior-axial-spine',[tube([(0,28,4.5),(0,33.5,4.0),
        (0,39,3.2),(0,43,2.4)],[1.5,1.0,.46,.10],8,.7)],mats['axial'],c)
    bpy.context.view_layer.update()
    low,high=_bounds(_vertices_world(c));scale=params['length_m']/(high[1]-low[1])
    for ob in c.objects:
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co=Vector((v.co.x,v.co.y-6.325,v.co.z))*scale
    ground_asset(c,center_xy=False)
    source=audit_source(c,max_triangles=16000)
    if source['errors']:raise RuntimeError(source['errors'])
    output.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene['scientific_limits']=params['inference']
    scene.render.filepath='//renders/'
    # Factory workspaces can retain machine-specific file-browser directories.
    # Clear them in the authored scene before saving, not in a packaged binary.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//' + b' '*1000
                    space.params.directory=b'//'
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'model.blend'),relative_remap=True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in c.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[c['asset_root']]
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
        export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',
        export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,
        export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,
        export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Exporter RNA changed')
    bpy.ops.export_scene.gltf(filepath=str(output/'model.glb'),**options)
    glb=audit_glb(output/'model.glb',16000,8,100);glb['file']='model.glb'
    if glb['errors']:raise RuntimeError(glb['errors'])
    if glb['bytes']>3000000:raise RuntimeError('Frozen byte budget exceeded')
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(expected[k][i]-glb['bounds_m'][k][i]) for k in expected for i in range(3))
    if delta>1e-6 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export mismatch')
    save(output/'qa/evidence/build-technical.json',{'status':'PASS','source':source,'glb':glb,
        'bounds_roundtrip_max_error_m':delta,'export_options':options,'blender_version':bpy.app.version_string,
        'blender_python':sys.version.split()[0],'generator_sha256':sha(__file__),
        'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(output/'model.blend'),
        'scope':'Source mesh/topology, static GLB audit and axis-aware bounds; not independent visual review, GPU or scene QA.'})


def render(glb, output, resolution, samples, clay):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    objs=[o for o in bpy.data.objects if o.type=='MESH']
    bpy.context.view_layer.update()
    points=[o.matrix_world@v.co for o in objs for v in o.data.vertices]
    low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)])
    span=max(high[i]-low[i] for i in range(3))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU'
    scene.cycles.samples=samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Studio');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;scene.world=world
    for name,direction,energy in [('key',(-3,-4,6),450),('fill',(4,-1,3),180)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=span*2
        obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj)
        obj.location=center+Vector(direction)*span/2;_look_at(obj,center)
    data=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',data)
    scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO'
    data.clip_start=.00001;data.clip_end=10
    if clay:scene.view_layers[0].material_override=make_material('Diagnostic-clay','#999999',roughness=.9)
    output.mkdir(parents=True,exist_ok=True);frames=[]
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    for view,direction in directions.items():
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center)
        bpy.context.view_layer.update();inv=cam.matrix_world.inverted();projections=[inv@v for v in points]
        width=max(v.x for v in projections)-min(v.x for v in projections)
        height=max(v.y for v in projections)-min(v.y for v in projections)
        shift=Vector(((max(v.x for v in projections)+min(v.x for v in projections))/2,
                      (max(v.y for v in projections)+min(v.y for v in projections))/2,0))
        cam.location+=cam.matrix_world.to_3x3()@shift;data.ortho_scale=max(width,height)*1.18
        scene.render.filepath=str(output/(view+'.png'));bpy.ops.render.render(write_still=True)
        frames.append({'view':view,'file':view+'.png','sha256':sha(output/(view+'.png')),
            'direction':direction,'orthographic_scale_m':data.ortho_scale})
    save(output/'render-receipt.json',{'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED',
        'glb_sha256':sha(glb),'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,
        'generator_sha256':sha(__file__),'exact_clean_import':True,'resolution':[resolution,resolution],
        'samples':samples,'threads':2,'clay_override':clay,'transparent':True,
        'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'frames':frames,
        'scope':'Four actual-GLB Blender views; does not establish browser GPU or populated-scene rendering.'})


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE.parent)
    ap.add_argument('--render-glb',type=Path);ap.add_argument('--render-dir',type=Path)
    ap.add_argument('--resolution',type=int,default=512);ap.add_argument('--samples',type=int,default=16)
    ap.add_argument('--clay',action='store_true')
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.render_glb:
        render(args.render_glb.resolve(),args.render_dir.resolve(),args.resolution,args.samples,args.clay)
    else:build(json.loads((HERE/'params.json').read_text()),args.output.resolve())


if __name__=='__main__':main()
