# SPDX-License-Identifier: MIT
"""Minimal neutral studio render of the scene, with literal declared axes."""
from pathlib import Path
import hashlib,json,math
import bpy
from mathutils import Vector
from asset_common import make_material,_look_at,_vertices_world,_bounds

def render_views(collection, output, grey=False, resolution=768, samples=48, views=None):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    points=_vertices_world(collection); low,high=_bounds(points)
    center=Vector([(low[i]+high[i])/2 for i in range(3)])
    span=max(high[i]-low[i] for i in range(3))
    scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=samples
    scene.cycles.use_denoising=False; scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.render.resolution_x=resolution;scene.render.resolution_y=resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('studio-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.75,0.75,0.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4;scene.world=world
    preview=bpy.data.collections.new('PREVIEW_ONLY');scene.collection.children.link(preview)
    for name,d,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        ld=bpy.data.lights.new(name,'AREA');ld.energy=energy*span*span/4;ld.shape='DISK';ld.size=size*span/2
        ob=bpy.data.objects.new(name,ld);preview.objects.link(ob);ob.location=center+Vector(d)*span/2;_look_at(ob,center)
    cd=bpy.data.cameras.new('inspection-camera');camera=bpy.data.objects.new('inspection-camera',cd);preview.objects.link(camera);scene.camera=camera
    cd.type='ORTHO';cd.clip_start=.001;cd.clip_end=span*30
    if grey:
        grey_mat=make_material('inspection-clay','#8F9394',.88)
        # Actual material override for all mesh regions, including eyes.
        for obj in collection.all_objects:
            if obj.type=='MESH':
                obj.data.materials.clear();obj.data.materials.append(grey_mat)
                for p in obj.data.polygons:p.material_index=0
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    record={'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','samples':samples,'resolution':[resolution,resolution],'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'output_color_space':'sRGB','gpu_rendering':False,'views':{}}
    for name in views or directions:
        direction=Vector(directions[name]).normalized();camera.location=center+direction*span*4;_look_at(camera,center);bpy.context.view_layer.update()
        inverse=camera.matrix_world.inverted();proj=[inverse@p for p in points]
        width=max(p.x for p in proj)-min(p.x for p in proj);height=max(p.y for p in proj)-min(p.y for p in proj)
        shift=Vector(((max(p.x for p in proj)+min(p.x for p in proj))/2,(max(p.y for p in proj)+min(p.y for p in proj))/2,0))
        camera.location+=camera.matrix_world.to_3x3()@shift;cd.ortho_scale=max(width,height,.05)*1.14
        dest=output/(name+'.png');scene.render.filepath=str(dest);bpy.ops.render.render(write_still=True)
        record['views'][name]={'direction':directions[name],'camera_position_m':list(camera.location),'ortho_scale_m':cd.ortho_scale,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
    return record
