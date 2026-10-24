# SPDX-License-Identifier: MIT
"""Original female reconstruction. Units are meters; helper dependencies are relative.
Run in Blender with -- --output DIRECTORY --render none|gray|final.
Output is resolved before save; the editable scene excludes preview helpers.
"""
from pathlib import Path
import argparse, hashlib, json, math, random, sys
import bpy
from mathutils import Vector
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def mm(v): return Vector(v)*.001

def axial_loft(name,profiles,sides,material,col):
    # Original varying sections: y, lateral radius, lower z, upper z, in mm.
    verts=[]; faces=[]
    for y,rx,lo,hi in profiles:
        for j in range(sides):
            a=2*math.pi*j/sides
            verts.append(tuple(mm((rx*math.cos(a),y,(lo+hi)/2+(hi-lo)/2*math.sin(a)))))
    for k in range(len(profiles)-1):
        for j in range(sides):
            a=k*sides+j; b=k*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    for idx,profile in ((0,profiles[0]),(len(profiles)-1,profiles[-1])):
        y,rx,lo,hi=profile; c=len(verts); verts.append(tuple(mm((0,y,(lo+hi)/2))))
        for j in range(sides): faces.append((c,idx*sides+j,idx*sides+(j+1)%sides))
    return mesh_object(name,verts,faces,material,col)

def tube_arrays(points,radii,sides=8):
    pts=[Vector(p) for p in points]; verts=[]; faces=[]
    for i,p in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        guide=Vector((0,0,1)) if abs(tangent.z)<.94 else Vector((0,1,0))
        u=tangent.cross(guide).normalized(); v=tangent.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides
            verts.append(tuple((p+radii[i]*(u*math.cos(a)+v*math.sin(a)))*.001))
    for i in range(len(pts)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    faces.append(tuple(range(sides-1,-1,-1)))
    faces.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
    return verts,faces

def tube(name,points,radii,mat,col,sides=8):
    verts,faces=tube_arrays(points,radii,sides)
    return mesh_object(name,verts,faces,mat,col)

def add_needle(verts,faces,start,end,radius):
    start,end=Vector(start),Vector(end); d=(end-start).normalized()
    guide=Vector((0,0,1)) if abs(d.z)<.95 else Vector((0,1,0))
    u=d.cross(guide).normalized(); v=d.cross(u).normalized(); n=len(verts); sides=5
    for j in range(sides):
        a=2*math.pi*j/sides
        verts.append(tuple((start+radius*(u*math.cos(a)+v*math.sin(a)))*.001))
    verts.append(tuple(end*.001))
    for j in range(sides): faces.append((n+j,n+(j+1)%sides,n+sides))
    faces.append(tuple(n+j for j in range(sides-1,-1,-1)))

def articulated(name,landmarks,base_radii,mat,jointmat,col):
    points=[]; radii=[]; markers=[]
    for k in range(len(landmarks)-1):
        a,b=Vector(landmarks[k]),Vector(landmarks[k+1])
        for t in (0,.12,.48,.88):
            points.append(a.lerp(b,t)); radii.append(base_radii[k]*(.84 if t==0 else 1 if t<.5 else .83))
            markers.append(k if t==0 else -1)
    points.append(Vector(landmarks[-1])); radii.append(base_radii[-1]); markers.append(-1)
    verts,faces=tube_arrays(points,radii,8)
    ob=mesh_object(name,verts,faces,[mat,jointmat],col)
    for p in ob.data.polygons:
        ring=p.index//8
        if ring<len(markers) and markers[ring]>=0: p.material_index=1
    return ob

def build(params):
    col=setup_scene(params['asset_id'],params['seed']); root=bpy.data.objects[params['asset_id']]
    root['representation']='living-reconstruction'; root['sex']='adult female'; root['specimen_basis']='CNU-ARA-NN2010008'
    root['scientific_limits']='Depth, colors, eyes and pose inferred; distal IV reconstructed; fine plumose microstructure omitted.'
    mats={k:make_material(k,c,roughness=.87 if k=='setae' else .82) for k,c in params['palette_srgb'].items()}
    axial_loft('carapace',[
      (-9.655,.62,6.0,6.65),(-9.32,1.22,5.65,7.35),(-8.6,1.85,5.1,7.95),(-7.7,2.6,4.75,8.3),
      (-6.5,3.17,4.65,8.35),(-5.2,3.415,4.68,8.17),(-3.8,3.30,4.76,7.95),(-2.5,2.85,4.95,7.65),
      (-1.35,1.9,5.2,7.28),(-.65,1.18,5.5,6.98),(-.345,.56,5.85,6.68)],18,mats['carapace'],col)
    axial_loft('abdomen',[
      (.32,.48,5.7,6.7),(.8,1.85,4.55,7.9),(1.8,3.2,3.5,8.95),(3.4,4.25,2.96,9.65),
      (5.1,4.75,2.8,9.8),(7.1,4.6,2.83,9.55),(9.2,4.1,3.0,9.12),(11.1,3.35,3.4,8.65),
      (12.7,2.55,3.95,8.12),(14,1.7,4.63,7.5),(15,.8,5.31,6.84),(15.68,.18,5.9,6.25)],20,mats['abdomen'],col)
    tube('narrow-pedicel',[(0,-.8,6.25),(0,-.1,6.25),(0,.8,6.25)],[.64,.53,.64],mats['joints'],col,10)
    axial_loft('ventral-sternum',[(-7.8,.6,4.8,5),(-6.5,1.5,4.48,4.96),(-4.8,1.65,4.45,4.95),(-3,1.1,4.7,5),(-2.3,.4,4.95,5.1)],12,mats['underside'],col)
    lengths=[(14.57,3.75,15.39,16.92,4.62),(11.42,3.25,9.56,11.49,3.21),(6.89,2.1,4.95,5.24,2.29),(9.83,2.56,6.3,8,2.6)]
    # Neutral artistic stance. Segment lengths constrained, yaw/depth inferred.
    attach=[(2.15,-7.6,6.15),(2.9,-5.8,6.1),(2.8,-3.8,6),(2.25,-2,6.05)]
    yaws=[-52,-12,25,57]
    rises=[(10.8,11.1,6.9,.67,.07),(10,10.25,5.5,.55,.07),(8.65,8.45,4.6,.5,.07),(9.8,9.9,5.2,.54,.07)]
    offsets=[(-5,0,3,0,-3),(-8,1,4,1,-2),(-5,0,3,0,-2),(-5,0,5,0,-2)]
    metrics=[]
    for sign,label in ((1,'R'),(-1,'L')):
        for k,seg in enumerate(lengths):
            c=Vector(attach[k]); direction=Vector((math.cos(math.radians(yaws[k])),math.sin(math.radians(yaws[k])),0))
            a=c+direction*1.25; points=[c,a]; current=a
            for j,length in enumerate(seg):
                z=rises[k][j]; dz=z-current.z; horizontal=math.sqrt(length*length-dz*dz)
                yaw=math.radians(yaws[k]+offsets[k][j])
                current=current+Vector((horizontal*math.cos(yaw),horizontal*math.sin(yaw),dz)); points.append(current)
            points=[Vector((p.x*sign,p.y,p.z)) for p in points]
            scale=[1,.93,.8,.89][k]; radii=[.48*scale,.39*scale,.36*scale,.265*scale,.165*scale,.108*scale,.07]
            articulated(f'walking-leg-{k+1}-{label}',points,radii,mats['limbs'],mats['joints'],col)
            verts=[]; faces=[]; rng=random.Random(params['seed']+k*113+(0 if sign==1 else 701))
            # Sparse distal tibial gaiters on ALL pairs; subordinate femur/metatarsus setae.
            for segment,count,t0,t1,size in ((3,22,.5,.98,1.25),(4,9,.52,.92,.8),(1,8,.45,.94,.55)):
                p,q=points[segment],points[segment+1]; tangent=(q-p).normalized()
                u=tangent.cross(Vector((0,0,1))).normalized(); v=tangent.cross(u).normalized()
                for h in range(count):
                    t=t0+(t1-t0)*(h+.25)/count; a=h*2.399963+rng.uniform(-.16,.16)
                    radial=u*math.cos(a)+v*math.sin(a); center=p.lerp(q,t)
                    start=center+radial*radii[segment]*.85*.7
                    length=size*(.72+.38*rng.random())*(.8 if k==2 else 1)
                    end=start+(radial*.95+tangent*.30).normalized()*length
                    add_needle(verts,faces,start,end,.042 if segment==3 else .035)
            mesh_object(f'sparse-setae-{k+1}-{label}',verts,faces,mats['setae'],col)
            metrics.append({'name':f'walking-leg-{k+1}-{label}','pair':k+1,'landmarks_m':[list(p*.001) for p in points],
              'femur_to_tarsus_lengths_mm':[(points[j+2]-points[j+1]).length for j in range(5)],'femur_to_tarsus_total_mm':sum(seg),
              'distal_tibial_gaiter_needles':22,'posterior_missing_segments_inferred':k==3})
    for sign,label in ((1,'R'),(-1,'L')):
        palp=[(sign*1.25,-8.65,5.85),(sign*2.3,-10.4,5.30),(sign*2.8,-11.55,4.75),(sign*2.3,-12.5,4.4),(sign*1.95,-13,4.4)]
        articulated('short-female-palp-'+label,palp,[.31,.28,.23,.16,.12],mats['limbs'],mats['joints'],col)
        tube('chelicera-'+label,[(sign*.61,-8.8,5.65),(sign*.71,-9.7,4.9),(sign*.5,-10.15,4.4)],[.37,.32,.17],mats['joints'],col)
    # Place the identity root at the center of the intended eight-foot footprint.
    foot_y=[x['landmarks_m'][-1][1] for x in metrics]
    shift_y=-(min(foot_y)+max(foot_y))/2
    for ob in col.all_objects:
        if ob.type=='MESH':
            for vertex in ob.data.vertices: vertex.co.y+=shift_y
    for record in metrics:
        for point in record['landmarks_m']: point[1]+=shift_y
    root['footprint_center_shift_y_m']=shift_y
    bpy.context.view_layer.update()
    return col,metrics

EXPORT_OPTIONS=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,
    export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,
    export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,
    export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)

def render_exact(glb,output,gray):
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=str(glb.resolve()))
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'
    scene.cycles.samples=8 if gray else 48; scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=400 if gray else 900
    scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True; scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
    scene.view_settings.exposure=0; scene.view_settings.gamma=1
    points=[o.matrix_world@v.co for o in scene.objects if o.type=='MESH' for v in o.data.vertices]
    low=Vector([min(p[i] for p in points) for i in range(3)]); high=Vector([max(p[i] for p in points) for i in range(3)])
    center=(low+high)/2; span=max(high-low)
    world=bpy.data.worlds.new('neutral-preview-world'); world.use_nodes=True; scene.world=world
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1); world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
    if gray: bpy.context.view_layer.material_override=make_material('gray-check','#A5A5A5',roughness=.9)
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA'); data.energy=energy*span*span/4; data.shape='DISK'; data.size=size*span/2
        light=bpy.data.objects.new(name,data); scene.collection.objects.link(light); light.location=center+Vector(direction)*span/2
        light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
    camdata=bpy.data.cameras.new('inspection-camera'); camera=bpy.data.objects.new('inspection-camera',camdata)
    scene.collection.objects.link(camera); scene.camera=camera; camdata.type='ORTHO'; camdata.clip_start=.0001; camdata.clip_end=10
    record={'source_glb_sha256':sha(glb),'engine':'Cycles CPU','gpu_claim':False,'samples':scene.cycles.samples,
      'resolution':[scene.render.resolution_x]*2,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},
      'transparent':True,'gray_override':gray,'views':[]}
    for name,xyz in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        camera.location=center+Vector(xyz).normalized()*span*4
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler(); bpy.context.view_layer.update()
        inv=camera.matrix_world.inverted(); pp=[inv@p for p in points]
        width=max(p.x for p in pp)-min(p.x for p in pp); height=max(p.y for p in pp)-min(p.y for p in pp)
        shift=Vector(((max(p.x for p in pp)+min(p.x for p in pp))/2,(max(p.y for p in pp)+min(p.y for p in pp))/2,0))
        camera.location+=camera.matrix_world.to_3x3()@shift; camdata.ortho_scale=max(width,height)*1.16
        path=output/(name+'.png'); scene.render.filepath=str(path.resolve()); bpy.ops.render.render(write_still=True)
        record['views'].append({'name':name,'path':path.name,'sha256':sha(path),'camera_direction':list(xyz),
          'camera_location_m':list(camera.location),'orthographic_scale_m':camdata.ortho_scale})
    write(output/'views.json',record)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='output'); parser.add_argument('--render',choices=['none','gray','final'],default='none')
    parser.add_argument('--render-existing',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=Path(args.output).resolve(); out.mkdir(parents=True,exist_ok=True)
    if not args.render_existing:
        params=json.loads((SOURCE/'params.json').read_text()); col,metrics=build(params)
        source=audit_source(col,14000); write(out/'source-audit.json',source)
        if source['errors']: raise RuntimeError('; '.join(source['errors']))
        bpy.context.scene['generator']='source/generate.py'; bpy.context.scene['parameter_sha256']=sha(SOURCE/'params.json')
        # Portable editor state. Clear stale string-buffer content before assigning relative paths.
        bpy.context.scene.render.filepath='//renders/'
        for screen in bpy.data.screens:
            for area in screen.areas:
                for space in area.spaces:
                    if space.type=='FILE_BROWSER' and space.params:
                        space.params.directory=b'.'*1023
                        space.params.directory=b'//'
                        space.params.filename=''
        bpy.context.preferences.filepaths.save_version=0
        bpy.ops.wm.save_as_mainfile(filepath=str((out/'model.blend').resolve()))
        bpy.ops.object.select_all(action='DESELECT')
        for ob in col.all_objects: ob.select_set(True)
        bpy.context.view_layer.objects.active=bpy.data.objects['mongolarachne']
        available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}; missing=set(EXPORT_OPTIONS)-available
        if missing: raise RuntimeError('Missing exporter options: '+', '.join(sorted(missing)))
        bpy.ops.export_scene.gltf(filepath=str((out/'model.glb').resolve()),**EXPORT_OPTIONS)
        glb=audit_glb(out/'model.glb',14000,6,72,ground_tolerance=.0001)
        glb['file']='model.glb'
        write(out/'glb-audit.json',glb)
        if glb['errors']: raise RuntimeError('; '.join(glb['errors']))
        if (out/'model.glb').stat().st_size>2500000: raise RuntimeError('GLB byte budget exceeded')
        b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
        delta=max(abs(expected[k][i]-glb['bounds_m'][k][i]) for k in expected for i in range(3))
        assert delta<1e-7 and glb['scene_triangles']==source['triangles']
        import io_scene_gltf2
        write(out/'build.json',{'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],
          'exporter_version':list(io_scene_gltf2.bl_info['version']),'seed':params['seed'],'generator_sha256':sha(SOURCE/'generate.py'),
          'params_sha256':sha(SOURCE/'params.json'),'export_options':EXPORT_OPTIONS,'glb_sha256':sha(out/'model.glb'),
          'semantic_digest':glb.get('semantic_sha256'),'bounds_roundtrip_max_error_m':delta,'leg_metrics':metrics,
          'scale_scope':'Published fossil lengths; living depth, stance and missing IV distal segments interpretive.'})
    if args.render!='none':
        views=out/('gray' if args.render=='gray' else 'views'); views.mkdir(parents=True,exist_ok=True)
        render_exact(out/'model.glb',views,args.render=='gray')
if __name__=='__main__': main()
