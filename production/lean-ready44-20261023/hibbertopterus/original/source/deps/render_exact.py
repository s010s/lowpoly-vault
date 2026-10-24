# SPDX-License-Identifier: MIT
"""Canonical soft-studio preset adapted to the frozen four camera directions."""
import bpy
from mathutils import Vector
import asset_common as common

def render(collection,out,grey=False):
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    points=common._vertices_world(collection); low,high=common._bounds(points)
    center=Vector([(low[i]+high[i])/2 for i in range(3)])
    span=max(high[i]-low[i] for i in range(3))
    preview=bpy.data.collections.new('_PREVIEW_ONLY'); scene.collection.children.link(preview)
    world=bpy.data.worlds.new('_preview_world'); world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
    scene.world=world; scene.render.engine='CYCLES'; scene.cycles.device='CPU'
    scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.cycles.samples=8 if grey else 32; scene.cycles.use_denoising=False
    scene.render.resolution_x=scene.render.resolution_y=320 if grey else 640
    scene.render.resolution_percentage=100; scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
    scene.view_settings.exposure=0; scene.view_settings.gamma=1
    camera_data=bpy.data.cameras.new('_preview_camera'); camera_data.type='ORTHO'
    camera_data.clip_start=.0001; camera_data.clip_end=10
    camera=bpy.data.objects.new('_preview_camera',camera_data); preview.objects.link(camera); scene.camera=camera
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new('_preview_'+name,'AREA'); d.energy=energy*span*span/4
        d.shape='DISK'; d.size=size*span/2
        o=bpy.data.objects.new('_preview_'+name,d); preview.objects.link(o)
        o.location=center+Vector(direction)*span/2; common._look_at(o,center)
    if grey:
        clay=common.make_material('_clay','#929292',.85)
        bpy.context.view_layer.material_override=clay
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    for name,direction in directions.items():
        camera.location=center+Vector(direction).normalized()*span*4; common._look_at(camera,center)
        bpy.context.view_layer.update(); inv=camera.matrix_world.inverted(); pp=[inv@p for p in points]
        xmin,xmax=min(p.x for p in pp),max(p.x for p in pp)
        ymin,ymax=min(p.y for p in pp),max(p.y for p in pp)
        camera.location+=camera.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0))
        camera_data.ortho_scale=max(xmax-xmin,ymax-ymin)*1.22
        scene.render.filepath=str(out/(name+'.png')); bpy.ops.render.render(write_still=True)
