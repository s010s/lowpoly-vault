# SPDX-License-Identifier: MIT
"""Four fixed-direction neutral views of a clean GLB import, no source geometry."""
import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector
from asset_common import make_material, _vertices_world, _bounds, _look_at, srgb_to_linear

def render_four(glb_path, output_dir, resolution=768, samples=24, clay=False):
    glb_path=Path(glb_path); output_dir=Path(output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb_path))
    asset_objects=list(bpy.context.scene.objects)
    c=bpy.data.collections.new('IMPORTED_ASSET'); bpy.context.scene.collection.children.link(c)
    for obj in asset_objects:
        for old in list(obj.users_collection): old.objects.unlink(obj)
        c.objects.link(obj)
    scene=bpy.context.scene
    points=_vertices_world(c); low,high=_bounds(points)
    center=Vector([(a+b)/2 for a,b in zip(low,high)]); span=max(high[i]-low[i] for i in range(3))
    p=bpy.data.collections.new('PRESENTATION_ONLY'); scene.collection.children.link(p)
    world=bpy.data.worlds.new('Neutral world'); world.use_nodes=True
    bg=world.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(.75,.75,.75,1); bg.inputs['Strength'].default_value=.3
    cb=world.node_tree.nodes.new('ShaderNodeBackground'); cb.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,); cb.inputs['Strength'].default_value=1
    lp=world.node_tree.nodes.new('ShaderNodeLightPath'); mix=world.node_tree.nodes.new('ShaderNodeMixShader')
    world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]); world.node_tree.links.new(bg.outputs[0],mix.inputs[1]); world.node_tree.links.new(cb.outputs[0],mix.inputs[2]); world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']); scene.world=world
    scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=samples; scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=resolution; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'; scene.view_settings.exposure=0; scene.view_settings.gamma=1
    camdata=bpy.data.cameras.new('Evidence camera'); cam=bpy.data.objects.new('Evidence camera',camdata); p.objects.link(cam); camdata.type='ORTHO'; camdata.clip_start=.001; camdata.clip_end=span*30; scene.camera=cam
    # One locked ortho scale across all four views, deliberately not per-view autofitted.
    camdata.ortho_scale=span*1.28
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        light=bpy.data.lights.new(name,'AREA'); light.energy=energy*span*span/4; light.shape='DISK'; light.size=size*span/2
        obj=bpy.data.objects.new(name,light); p.objects.link(obj); obj.location=center+Vector(direction)*span/2; _look_at(obj,center)
    mesh=bpy.data.meshes.new('Studio floor'); extent=span*20
    mesh.from_pydata([(-extent,-extent,low[2]-.0006),(extent,-extent,low[2]-.0006),(extent,extent,low[2]-.0006),(-extent,extent,low[2]-.0006)],[],[(0,1,2,3)])
    floor=bpy.data.objects.new('Studio floor',mesh); p.objects.link(floor); mesh.materials.append(make_material('Studio background','#E8E4DC',1))
    if clay:
        mat=make_material('Gray form check','#999C9B',.9)
        for obj in c.objects:
            if obj.type=='MESH':
                obj.data.materials.clear(); obj.data.materials.append(mat)
                for poly in obj.data.polygons: poly.material_index=0
    result={'status':'rendered_not_independently_reviewed','source_glb_sha256':hashlib.sha256(glb_path.read_bytes()).hexdigest(),'clean_import':True,'engine':'Cycles CPU','threads':2,'samples':samples,'resolution':[resolution,resolution],'background_srgb':'#E8E4DC','view_transform':'Standard','look':'None','orthographic_scale_m':camdata.ortho_scale,'clay':clay,'views':{}}
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4; _look_at(cam,center)
        scene.render.filepath=str(output_dir/(name+'.png')); bpy.ops.render.render(write_still=True)
        result['views'][name]={'camera_direction_blender':direction,'camera_location_m':list(cam.location),'target_m':list(center),'sha256':hashlib.sha256((output_dir/(name+'.png')).read_bytes()).hexdigest()}
    return result
