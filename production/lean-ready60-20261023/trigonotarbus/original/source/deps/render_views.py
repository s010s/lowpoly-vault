# SPDX-License-Identifier: MIT
"""Exact-export CPU preview adapter. Lighting follows canonical asset_common.
Display-only scale compensates for millimeter specimens; model bytes stay SI.
"""
from pathlib import Path
import argparse, json, hashlib, math, sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import make_material, srgb_to_linear, _look_at, _bounds
ap=argparse.ArgumentParser();ap.add_argument('--asset',required=True);ap.add_argument('--output',required=True);ap.add_argument('--gray',action='store_true');ap.add_argument('--resolution',type=int,default=768);ap.add_argument('--samples',type=int,default=32)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]); asset=Path(a.asset);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
if asset.suffix=='.glb': bpy.ops.import_scene.gltf(filepath=str(asset))
else: bpy.ops.wm.open_mainfile(filepath=str(asset))
scene=bpy.context.scene;objects=[o for o in scene.objects if o.type=='MESH'];roots=[o for o in scene.objects if o.parent is None]
for o in roots:o.scale*=1000
bpy.context.view_layer.update()
if a.gray:
    gray=make_material('_diagnostic_gray','#929292',roughness=.85)
    for o in objects:
        for i in range(len(o.data.materials)):o.data.materials[i]=gray
points=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
low,high=_bounds(points); center=Vector([(x+y)/2 for x,y in zip(low,high)]);span=max(y-x for x,y in zip(low,high))
world=bpy.data.worlds.new('_preview_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
camera_bg=world.node_tree.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],mix.inputs[1]);world.node_tree.links.new(camera_bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],next(n for n in world.node_tree.nodes if n.type=='OUTPUT_WORLD').inputs['Surface']);scene.world=world
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=a.resolution;scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
camera_data=bpy.data.cameras.new('_preview_camera');camera=bpy.data.objects.new('_preview_camera',camera_data);scene.collection.objects.link(camera);camera_data.type='ORTHO';camera_data.clip_start=span/1000;camera_data.clip_end=span*30;scene.camera=camera
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    data=bpy.data.lights.new('_preview_'+name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;o=bpy.data.objects.new('_preview_'+name,data);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
fm=bpy.data.meshes.new('_preview_floor');ext=span*20;fm.from_pydata([(-ext,-ext,-.002),(ext,-ext,-.002),(ext,ext,-.002),(-ext,ext,-.002)],[],[(0,1,2,3)]);floor=bpy.data.objects.new('_preview_floor',fm);scene.collection.objects.link(floor);fm.materials.append(make_material('_floor','#E8E4DC',roughness=1))
records=[]
for label,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
    camera.location=center+Vector(direction).normalized()*span*4;_look_at(camera,center);bpy.context.view_layer.update();inverse=camera.matrix_world.inverted();projected=[inverse@p for p in points];xmin,xmax=min(p.x for p in projected),max(p.x for p in projected);ymin,ymax=min(p.y for p in projected),max(p.y for p in projected);camera.location+=camera.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));camera_data.ortho_scale=max(xmax-xmin,ymax-ymin)*1.2
    target=out/(label+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True);records.append({'file':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'camera_direction_authoring':direction,'orthographic':True})
(out/'render-receipt.json').write_text(json.dumps({'input_file':asset.name,'input_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'input_kind':'actual_GL B'.replace(' ', '') if asset.suffix=='.glb' else 'source_gray','engine':'Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'resolution':[a.resolution,a.resolution],'samples':a.samples,'display_only_scale':1000,'colors':'Standard/None/exposure 0/gamma 1','lighting':'canonical studio area key 450 and fill 150, scaled by bounding span squared','background':'neutral #E8E4DC','views':records,'gpu_rendered':False},indent=2)+'\n')
