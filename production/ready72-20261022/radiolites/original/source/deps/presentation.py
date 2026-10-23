# SPDX-License-Identifier: MIT
"""Small-scale four-view adapter derived from asset_common preview preset.
Keeps canonical linear colors, Standard display, key/fill and CPU renderer.
Permits 45 mm framing and exact (+X,-Y,+Z) oblique camera.
"""
from pathlib import Path
import bpy
from mathutils import Vector
from asset_common import _vertices_world,_bounds,_look_at,make_material,srgb_to_linear

def render_views(collection,output_dir,resolution=768,samples=20,clay=False):
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True);scene=bpy.context.scene
    points=_vertices_world(collection);low,high=_bounds(points);center=Vector([(a+b)/2 for a,b in zip(low,high)]);span=max(high[i]-low[i] for i in range(3))
    stage=bpy.data.collections.new('_PRESENTATION_ONLY');scene.collection.children.link(stage)
    world=bpy.data.worlds.new('_neutral_world');world.use_nodes=True;scene.world=world;nodes=world.node_tree.nodes;links=world.node_tree.links
    bg=nodes.get('Background');bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    cb=nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1
    lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(cb.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes.get('World Output').inputs['Surface'])
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=resolution;scene.render.resolution_y=resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        obj=bpy.data.objects.new(name,data);stage.objects.link(obj);obj.location=center+Vector(direction)*span/2;_look_at(obj,center)
    mesh=bpy.data.meshes.new('floor');s=span*20;z=low[2]-.00015;mesh.from_pydata([(-s,-s,z),(s,-s,z),(s,s,z),(-s,s,z)],[],[(0,1,2,3)])
    floor=bpy.data.objects.new('floor',mesh);stage.objects.link(floor);mesh.materials.append(make_material('floor-neutral','#E8E4DC',roughness=1))
    data=bpy.data.cameras.new('four-view-camera');camera=bpy.data.objects.new('four-view-camera',data);stage.objects.link(camera);scene.camera=camera;data.type='ORTHO';data.clip_start=span/1000;data.clip_end=span*50
    if clay:bpy.context.view_layer.material_override=make_material('gray-check','#9C9C9C',roughness=.9)
    outputs=[]
    for name,direction in {'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}.items():
        camera.location=center+Vector(direction).normalized()*span*4;_look_at(camera,center);bpy.context.view_layer.update();inv=camera.matrix_world.inverted();pp=[inv@p for p in points]
        xmin,xmax=min(p.x for p in pp),max(p.x for p in pp);ymin,ymax=min(p.y for p in pp),max(p.y for p in pp)
        camera.location+=camera.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));data.ortho_scale=max(xmax-xmin,ymax-ymin)*1.24
        scene.render.filepath=str(output_dir/(name+'.png'));bpy.ops.render.render(write_still=True);outputs.append(Path(scene.render.filepath))
    bpy.context.view_layer.material_override=None
    return outputs
