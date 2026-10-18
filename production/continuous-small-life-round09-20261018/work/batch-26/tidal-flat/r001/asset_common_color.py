# SPDX-License-Identifier: MIT
"""Reproducible Blender 4.3+ helpers for original low-poly museum assets.

Import from a generator running inside Blender. All paths are cloud workspace
paths. Preview helpers never enter the EXPORT collection or emitted GLB.
"""
from pathlib import Path
import hashlib
import json
import math
import random
import sys

import bpy
import bmesh
from mathutils import Vector

SCRIPTS_DIR = next(p for p in Path(__file__).resolve().parents if (p/'scripts/qa_glb.py').exists())/'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0,str(SCRIPTS_DIR))
from qa_glb import audit_glb

REPO_ROOT = SCRIPTS_DIR.parent
LICENSE = 'CC-BY-4.0'
AUTHOR = 'Leon Made This / s010s'


def setup_scene(slug, seed=0):
    """Reset an asset-generation scene; return its dedicated EXPORT collection."""
    if not slug or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slug):
        raise ValueError('slug must contain lowercase letters, digits, and hyphens')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    random.seed(seed)
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC'
    scene.unit_settings.scale_length=1.0
    scene['asset_slug']=slug
    scene['generator_seed']=seed
    collection=bpy.data.collections.new('EXPORT')
    scene.collection.children.link(collection)
    root=bpy.data.objects.new(slug,None)
    collection.objects.link(root)
    root['asset_id']=slug
    root['license']=LICENSE
    root['author']=AUTHOR
    root['units']='meters'
    root['authoring_forward']='-Y'
    collection['asset_root']=root.name
    return collection


def srgb_to_linear(value):
    return value/12.92 if value<=0.04045 else ((value+0.055)/1.055)**2.4


def make_material(name, color, roughness=0.85, metallic=0.0, double_sided=False):
    """color is '#RRGGBB' or an sRGB 3/4-tuple in [0,1]; alpha remains opaque."""
    if isinstance(color,str):
        color=color.lstrip('#')
        if len(color)!=6: raise ValueError('Expected six-digit sRGB hex color')
        rgb=[int(color[i:i+2],16)/255 for i in (0,2,4)]
    else:
        rgb=list(color[:3])
    if len(rgb)!=3 or any(not 0<=c<=1 for c in rgb): raise ValueError('Invalid sRGB color')
    rgba=tuple(srgb_to_linear(c) for c in rgb)+(1.,)
    material=bpy.data.materials.new(name)
    material.use_nodes=True
    nodes=material.node_tree.nodes
    nodes.clear()
    shader=nodes.new('ShaderNodeBsdfPrincipled')
    shader.inputs['Base Color'].default_value=rgba
    shader.inputs['Roughness'].default_value=roughness
    shader.inputs['Metallic'].default_value=metallic
    shader.inputs['Alpha'].default_value=1.
    output=nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(shader.outputs['BSDF'],output.inputs['Surface'])
    material.diffuse_color=rgba
    material.roughness=roughness
    material.metallic=metallic
    material.use_backface_culling=not double_sided
    material['palette_srgb']='#'+''.join(f'{round(c*255):02X}' for c in rgb)
    return material


def link_object(obj, collection, parent=True):
    """Move an object into EXPORT; preserve its current world transform."""
    world=obj.matrix_world.copy()
    for old in list(obj.users_collection): old.objects.unlink(obj)
    collection.objects.link(obj)
    if parent:
        root=bpy.data.objects.get(collection.get('asset_root',''))
        if root and obj!=root:
            obj.parent=root
            obj.matrix_world=world
    return obj


def mesh_object(name, vertices, faces, material, collection, *, recalculate_normals=True):
    """Create a flat-shaded mesh with explicit topology and root parenting."""
    mesh=bpy.data.meshes.new(name+'-mesh')
    mesh.from_pydata(vertices,[],faces,shade_flat=True)
    mesh.update()
    if mesh.validate(verbose=True):
        raise ValueError(name+': invalid topology was repaired; fix the generator instead')
    if recalculate_normals:
        bm=bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    obj=bpy.data.objects.new(name,mesh)
    collection.objects.link(obj)
    root=bpy.data.objects.get(collection.get('asset_root',''))
    if root: obj.parent=root
    if material is not None:
        if isinstance(material,(list,tuple)):
            for m in material: mesh.materials.append(m)
        else: mesh.materials.append(material)
    return obj


def _vertices_world(collection):
    bpy.context.view_layer.update()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    points=[]
    for obj in collection.all_objects:
        if obj.type!='MESH': continue
        evaluated=obj.evaluated_get(depsgraph)
        mesh=evaluated.to_mesh()
        try: points.extend(evaluated.matrix_world@v.co for v in mesh.vertices)
        finally: evaluated.to_mesh_clear()
    if not points: raise ValueError('EXPORT collection has no mesh vertices')
    return points


def _bounds(points):
    return ([min(v[i] for v in points) for i in range(3)],
            [max(v[i] for v in points) for i in range(3)])


def ground_asset(collection, center_xy=False):
    """Shift top-level asset parts to floor Z=0; optional bbox centering in XY.

    Does not move the identity root. Do not use bbox centering when an intentional
    footprint/mount pivot is already established.
    """
    low,high=_bounds(_vertices_world(collection))
    offset=Vector((-(low[0]+high[0])/2 if center_xy else 0,
                   -(low[1]+high[1])/2 if center_xy else 0,-low[2]))
    root=bpy.data.objects.get(collection.get('asset_root',''))
    objects=set(collection.all_objects)
    for obj in objects:
        if obj==root: continue
        if obj.parent==root or obj.parent not in objects:
            world=obj.matrix_world.copy()
            world.translation+=offset
            obj.matrix_world=world
    bpy.context.view_layer.update()
    return list(offset)


def audit_source(collection,max_triangles=12000):
    errors,warnings=[],[]
    scene=bpy.context.scene
    if abs(scene.unit_settings.scale_length-1)>1e-8: errors.append('Scene unit scale must be 1 meter')
    root=bpy.data.objects.get(collection.get('asset_root',''))
    if root is None: errors.append('Missing asset root')
    elif any(abs(root.matrix_world[r][c]-(1. if r==c else 0.))>1e-6 for r in range(4) for c in range(4)):
        errors.append('Asset root must have identity world transform')
    depsgraph=bpy.context.evaluated_depsgraph_get()
    triangles=0; parts=[]; material_names=set()
    for obj in collection.all_objects:
        if obj.type not in {'MESH','EMPTY'}:
            errors.append(obj.name+': non-mesh export object '+obj.type); continue
        if obj.instance_type!='NONE': errors.append(obj.name+': unresolved object instance')
        if obj.type!='MESH': continue
        if obj.hide_render: errors.append(obj.name+': mesh hidden from rendering')
        if obj.matrix_world.to_3x3().determinant()<=0: errors.append(obj.name+': nonpositive transform determinant')
        if any(abs(s-1)>1e-5 for s in obj.scale): warnings.append(obj.name+': object scale not applied')
        if any(m.type=='NODES' for m in obj.modifiers): warnings.append(obj.name+': Geometry Nodes requires realized-instance review')
        evaluated=obj.evaluated_get(depsgraph)
        mesh=evaluated.to_mesh()
        try:
            mesh.calc_loop_triangles()
            count=len(mesh.loop_triangles)
            triangles+=count
            if not count: errors.append(obj.name+': no triangles')
            if any(not math.isfinite(x) for v in mesh.vertices for x in v.co): errors.append(obj.name+': non-finite vertex')
            degenerates=sum(1 for t in mesh.loop_triangles if t.area<1e-10)
            if degenerates: errors.append(f'{obj.name}: {degenerates} degenerate triangles')
            if any(p.use_smooth for p in mesh.polygons): warnings.append(obj.name+': smooth faces require intentional-style review')
            if not mesh.materials or any(m is None for m in mesh.materials): errors.append(obj.name+': missing material')
            material_names.update(m.name for m in mesh.materials if m)
            bm=bmesh.new(); bm.from_mesh(mesh)
            boundary=sum(e.is_boundary for e in bm.edges)
            nonmanifold=sum(not e.is_manifold and not e.is_boundary for e in bm.edges)
            bm.free()
            if boundary: warnings.append(f'{obj.name}: {boundary} boundary edges; review intentional openings')
            if nonmanifold: warnings.append(f'{obj.name}: {nonmanifold} non-manifold edges; review topology')
            parts.append({'name':obj.name,'vertices':len(mesh.vertices),'triangles':count,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold})
        finally: evaluated.to_mesh_clear()
    if triangles>max_triangles: errors.append(f'Triangle budget exceeded: {triangles} > {max_triangles}')
    low,high=_bounds(_vertices_world(collection))
    if abs(low[2])>0.002: warnings.append(f'Lowest Blender Z is {low[2]:.6f} m; verify mount/ground contract')
    return {'status':'fail' if errors else 'pass_with_warnings' if warnings else 'pass',
            'errors':errors,'warnings':warnings,'triangles':triangles,'materials':sorted(material_names),
            'bounds_blender_m':{'min':low,'max':high,'size':[high[i]-low[i] for i in range(3)]},'parts':parts}


def _look_at(obj,target):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()


def render_previews(collection, output_dir, views=('hero','reversehero','front','side','rear'), resolution=1024, samples=32, transparent=False):
    """Render consistent previews with Cycles CPU. Does not save scene changes."""
    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    points=_vertices_world(collection)
    low,high=_bounds(points)
    center=Vector([(low[i]+high[i])/2 for i in range(3)])
    span=max(max(high[i]-low[i] for i in range(3)),0.1)
    preview=bpy.data.collections.new('_PREVIEW_ONLY')
    scene.collection.children.link(preview)
    original_camera=scene.camera
    original_world=scene.world
    original_engine=scene.render.engine
    old_hidden={o:o.hide_render for o in scene.objects if o not in set(collection.all_objects)}
    for obj in old_hidden: obj.hide_render=True
    world=bpy.data.worlds.new('_preview_world')
    world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.75,0.75,0.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.3
    # Camera-visible studio background is independent of illumination intensity.
    # Otherwise horizontal orthographic views show a darker world than the floor.
    camera_background=world.node_tree.nodes.new('ShaderNodeBackground')
    camera_background.name='_preview_camera_background'
    camera_background.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,)
    camera_background.inputs['Strength'].default_value=1
    light_path=world.node_tree.nodes.new('ShaderNodeLightPath')
    background_mix=world.node_tree.nodes.new('ShaderNodeMixShader')
    world.node_tree.links.new(light_path.outputs['Is Camera Ray'],background_mix.inputs[0])
    world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],background_mix.inputs[1])
    world.node_tree.links.new(camera_background.outputs[0],background_mix.inputs[2])
    world_output=next(n for n in world.node_tree.nodes if n.type=='OUTPUT_WORLD')
    world.node_tree.links.new(background_mix.outputs[0],world_output.inputs['Surface'])
    scene.world=world
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=samples
    # This cloud Blender 4.3.2 build has no OpenImageDenoise support.
    scene.cycles.use_denoising=False
    scene.render.resolution_x=resolution
    scene.render.resolution_y=resolution
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=transparent
    scene.view_settings.view_transform='Standard'
    scene.view_settings.look='None'
    scene.view_settings.exposure=0
    scene.view_settings.gamma=1
    camera_data=bpy.data.cameras.new('_preview_camera')
    camera=bpy.data.objects.new('_preview_camera',camera_data)
    preview.objects.link(camera)
    camera_data.type='ORTHO'
    camera_data.clip_start=max(0.001,span/1000)
    camera_data.clip_end=span*30
    scene.camera=camera
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new('_preview_'+name,'AREA')
        data.energy=energy*span*span/4
        data.shape='DISK'
        data.size=size*span/2
        obj=bpy.data.objects.new('_preview_'+name,data)
        preview.objects.link(obj)
        obj.location=center+Vector(direction)*span/2
        _look_at(obj,center)
    # An opaque neutral studio plane is deliberately outside EXPORT.
    if not transparent:
        floor_mesh=bpy.data.meshes.new('_preview_floor')
        extent=span*20
        floor_mesh.from_pydata([(-extent,-extent,low[2]-0.002),(extent,-extent,low[2]-0.002),(extent,extent,low[2]-0.002),(-extent,extent,low[2]-0.002)],[],[(0,1,2,3)])
        floor=bpy.data.objects.new('_preview_floor',floor_mesh)
        preview.objects.link(floor)
        floor_mesh.materials.append(make_material('_preview_floor','#E8E4DC',roughness=1))
    directions={'hero':Vector((0.574,-0.819,0.466)), 'reversehero':Vector((-0.574,0.819,0.466)), 'front':Vector((0,-1,0)), 'side':Vector((1,0,0)),
                'rear':Vector((0,1,0)), 'top':Vector((0,0,1))}
    for label in ('silhouette','clay','clay-alt','wireframe'):
        directions[label]=directions['hero']
    clay=make_material('_preview_clay','#929292',roughness=0.85)
    black=bpy.data.materials.new('_preview_silhouette')
    black.use_nodes=True
    black.node_tree.nodes.clear()
    emission=black.node_tree.nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value=(0,0,0,1)
    emission.inputs['Strength'].default_value=1
    output=black.node_tree.nodes.new('ShaderNodeOutputMaterial')
    black.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
    wire=make_material('_preview_wire','#B5B5B5',roughness=0.85)
    wire_node=wire.node_tree.nodes.new('ShaderNodeWireframe')
    wire_node.use_pixel_size=True
    wire_node.inputs['Size'].default_value=0.8
    mix=wire.node_tree.nodes.new('ShaderNodeMixRGB')
    mix.inputs[1].default_value=tuple(srgb_to_linear(0.71) for _ in range(3))+(1,)
    mix.inputs[2].default_value=(0.015,0.015,0.015,1)
    wire.node_tree.links.new(wire_node.outputs['Fac'],mix.inputs[0])
    bsdf=next(n for n in wire.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    wire.node_tree.links.new(mix.outputs[0],bsdf.inputs['Base Color'])
    original_override=bpy.context.view_layer.material_override
    key=bpy.data.objects.get('_preview_key')
    key_location=key.location.copy()
    wire_copies=[]
    wire_hidden={}
    files=[]
    try:
        for view in views:
            is_silhouette=view=='silhouette'
            scene.render.resolution_x=128 if is_silhouette else resolution
            scene.render.resolution_y=128 if is_silhouette else resolution
            scene.render.film_transparent=False if is_silhouette else transparent
            background=world.node_tree.nodes['Background']
            background.inputs['Color'].default_value=(1,1,1,1) if is_silhouette else (0.75,0.75,0.75,1)
            background.inputs['Strength'].default_value=1 if is_silhouette else 0.3
            camera_background.inputs['Color'].default_value=(1,1,1,1) if is_silhouette else tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,)
            floor=bpy.data.objects.get('_preview_floor')
            if floor: floor.hide_render=is_silhouette
            bpy.context.view_layer.material_override=black if is_silhouette else clay if view.startswith('clay') else wire if view=='wireframe' else original_override
            key.location=center+Vector((3,4,6))*span/2 if view=='clay-alt' else key_location
            _look_at(key,center)
            if view=='wireframe':
                # Snapshot all evaluated data before creating any new datablocks.
                # Scene edits can invalidate depsgraph-owned RNA meshes in Blender 4.3.
                depsgraph=bpy.context.evaluated_depsgraph_get()
                snapshots=[]
                for obj in list(collection.all_objects):
                    if obj.type!='MESH': continue
                    evaluated=obj.evaluated_get(depsgraph)
                    evaluated_mesh=evaluated.to_mesh()
                    try:
                        evaluated_mesh.calc_loop_triangles()
                        snapshots.append((obj, [tuple(v.co) for v in evaluated_mesh.vertices],
                            [tuple(t.vertices) for t in evaluated_mesh.loop_triangles],
                            evaluated.matrix_world.copy()))
                    finally: evaluated.to_mesh_clear()
                for obj,vertices,triangles,matrix in snapshots:
                    triangle_mesh=bpy.data.meshes.new('_preview_triangles_'+obj.name)
                    triangle_mesh.from_pydata(vertices,[],triangles)
                    triangle_mesh.shade_flat()
                    triangle_mesh.materials.append(wire)
                    triangle_obj=bpy.data.objects.new('_preview_triangles_'+obj.name,triangle_mesh)
                    preview.objects.link(triangle_obj)
                    triangle_obj.matrix_world=matrix
                    wire_copies.append(triangle_obj)
                    wire_hidden[obj]=obj.hide_render
                    obj.hide_render=True
            if view not in directions: raise ValueError('Unknown preview view: '+view)
            direction=directions[view].normalized()
            camera.location=center+direction*span*4
            _look_at(camera,center)
            bpy.context.view_layer.update()
            inverse=camera.matrix_world.inverted()
            projected=[inverse@p for p in points]
            width=max(p.x for p in projected)-min(p.x for p in projected)
            height=max(p.y for p in projected)-min(p.y for p in projected)
            # Center on projected geometry, not merely its world-axis box.
            shift=Vector(((max(p.x for p in projected)+min(p.x for p in projected))/2,
                          (max(p.y for p in projected)+min(p.y for p in projected))/2,0))
            camera.location+=camera.matrix_world.to_3x3()@shift
            camera_data.ortho_scale=max(width,height,0.05)*1.25
            scene.render.filepath=str(output_dir/f'preview-{view}.png')
            bpy.ops.render.render(write_still=True)
            files.append(scene.render.filepath)
            for obj,state in wire_hidden.items(): obj.hide_render=state
            wire_hidden.clear()
            for obj in wire_copies: bpy.data.objects.remove(obj,do_unlink=True)
            wire_copies.clear()
    finally:
        for obj,state in wire_hidden.items(): obj.hide_render=state
        for obj in wire_copies: bpy.data.objects.remove(obj,do_unlink=True)
        bpy.context.view_layer.material_override=original_override
        scene.camera=original_camera
        scene.world=original_world
        scene.render.engine=original_engine
        for obj,state in old_hidden.items(): obj.hide_render=state
        for obj in list(preview.objects): bpy.data.objects.remove(obj,do_unlink=True)
        bpy.data.collections.remove(preview)
        bpy.data.worlds.remove(world)
        for material in (clay,black,wire): bpy.data.materials.remove(material)
    return files


def render_diagnostics(collection,output_dir,resolution=1024,samples=32):
    """128px unlit silhouette plus neutral clay, alternate-light clay and triangulated wireframe."""
    return render_previews(collection,output_dir,('silhouette','clay','clay-alt','wireframe'),resolution,samples)


def export_asset(slug, title, category, collection, metadata=None, output_root=None, render=True,
                 views=('hero','reversehero','front','side','rear'), max_triangles=12000, max_materials=8,
                 max_primitives=24, resolution=1024, samples=32, collection_id='prehistoric', diagnostics=True):
    """Save editable blend, export GLB, audit it, and render previews.

    title may be {'en':..., 'zh':...}. metadata may supply bilingual description,
    provenance, generator, tags, sources, reconstruction notes and reviewed warnings.
    output_root defaults to repository/assets/<collection_id>/<category> and receives a slug subfolder.
    """
    metadata=dict(metadata or {})
    if not category or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in category):
        raise ValueError('Invalid category')
    if not collection_id or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in collection_id):
        raise ValueError('Invalid collection_id')
    output_dir=Path(output_root or REPO_ROOT/'assets'/collection_id/category)/slug
    output_dir.mkdir(parents=True,exist_ok=True)
    source=audit_source(collection,max_triangles)
    qa={'source':source,'glb':None,'khronos_validator':{'status':'not_run'},
        'threejs_runtime':{'status':'not_run'},'visual_review':{'status':'pending'}}
    if source['errors']:
        (output_dir/'qa.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
        raise RuntimeError('Source QA failed: '+'; '.join(source['errors']))
    # Save before the temporary preview stage exists.
    bpy.context.scene['asset_license']=LICENSE
    bpy.context.scene['asset_author']=AUTHOR
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(output_dir/f'{slug}.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.all_objects: obj.select_set(True)
    root=bpy.data.objects.get(collection.get('asset_root',''))
    bpy.context.view_layer.objects.active=root
    options=dict(filepath=str(output_dir/f'{slug}.glb'),export_format='GLB',use_selection=True,
        export_yup=True,export_apply=True,export_normals=True,export_texcoords=bool(metadata.pop('export_texcoords',False)),
        export_tangents=False,export_materials='EXPORT',export_vertex_color='ACTIVE',
        export_animations=False,export_skins=False,export_morph=False,export_cameras=False,
        export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,
        export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    missing=set(options)-available
    if missing: raise RuntimeError('Blender exporter lacks required flags: '+', '.join(sorted(missing)))
    bpy.ops.export_scene.gltf(**options)
    glb=audit_glb(output_dir/f'{slug}.glb',max_triangles,max_materials,max_primitives)
    qa['glb']=glb
    # Axis-aware source-to-export bounds comparison catches scaling/selection errors.
    b=source['bounds_blender_m']
    expected_min=[b['min'][0],b['min'][2],-b['max'][1]]
    expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
    if 'bounds_m' in glb:
        delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
        qa['bounds_roundtrip_max_error_m']=delta
        if delta>0.0001: glb['errors'].append(f'Source/GLB bounds differ by {delta:.6f} m')
    if glb.get('scene_triangles')!=source['triangles']: glb['errors'].append('Source/GLB scene triangle counts differ')
    if glb['errors']:
        glb['status']='fail'
        (output_dir/'qa.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
        raise RuntimeError('GLB QA failed: '+'; '.join(glb['errors']))
    names=title if isinstance(title,dict) else {'en':title,'zh':metadata.pop('name_zh',title)}
    description=metadata.pop('description',{'en':'Original low-poly museum asset.','zh':'原创低多边形博物馆资产。'})
    if isinstance(description,str): description={'en':description,'zh':metadata.pop('description_zh',description)}
    try: relative=output_dir.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError: relative=output_dir.resolve().as_posix()
    dimensions=glb['bounds_m']['size']
    record={**metadata,'id':slug,'name':names,'category':category,'description':description,
        'glb':f'{relative}/{slug}.glb','blend':f'{relative}/{slug}.blend',
        'preview':f'{relative}/preview-hero.png','triangles':glb['scene_triangles'],'dimensions':dimensions,
        'license':LICENSE,'author':AUTHOR,'schema_version':1,'collection':collection_id,
        'units':'meters','axes':{'glb_up':'+Y','glb_forward':'+Z','blender_up':'+Z','blender_forward':'-Y'},
        'origin':'ground-center (or documented mounting point)',
        'blender_version':bpy.app.version_string,'blender_unit_scale':bpy.context.scene.unit_settings.scale_length,
        'blender_dimensions_m':b['size'],'bounds_glb_m':glb['bounds_m'],
        'generator_seed':bpy.context.scene.get('generator_seed',0),
        'export_options':{k:v for k,v in options.items() if k!='filepath'},
        'materials':[{'name':name,'srgb':bpy.data.materials[name].get('palette_srgb')} for name in source['materials']],
        'glb_bytes':glb['bytes'],'sha256':{'glb':glb['sha256'],'blend':hashlib.sha256((output_dir/f'{slug}.blend').read_bytes()).hexdigest()}}
    (output_dir/'metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    (output_dir/'qa.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
    if render:
        preview_files=render_previews(collection,output_dir,tuple(dict.fromkeys(('hero','reversehero')+tuple(views))),resolution,samples)
        if diagnostics:
            preview_files+=render_diagnostics(collection,output_dir,resolution=resolution,samples=samples)
        qa['previews']={'status':'rendered_not_visually_reviewed','files':[Path(p).name for p in preview_files],
            'engine':'Cycles CPU','resolution':resolution,'samples':samples,'view_transform':'Standard','look':'None','background_srgb':'#E8E4DC'}
        (output_dir/'qa.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
    return record
