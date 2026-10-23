#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exact delivered GLB renders, isolated import, scale-aware official studio rig.
The imported model is never modified, re-exported, or resaved.
"""
from pathlib import Path
import argparse, hashlib,json,math,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,_look_at,_vertices_world,_bounds,srgb_to_linear
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=640);p.add_argument('--samples',type=int,default=40)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
col=setup_scene('conus-exact-import');root=bpy.data.objects[col['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
new=[o for o in bpy.data.objects if o not in before]
for o in new:link_object(o,col,parent=False)
for o in new:
 if o.parent not in new:
  world=o.matrix_world.copy();o.parent=root;o.matrix_world=world
bpy.context.view_layer.update();points=_vertices_world(col);low,high=_bounds(points)
center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('temporary-neutral-world');world.use_nodes=True
bg=world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
camera_bg=world.node_tree.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(bg.outputs[0],mix.inputs[1]);world.node_tree.links.new(camera_bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']);scene.world=world
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new('temporary-'+name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
 obj=bpy.data.objects.new('temporary-'+name,data);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;_look_at(obj,center);lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
camdat=bpy.data.cameras.new('temporary-camera');camera=bpy.data.objects.new('temporary-camera',camdat);scene.collection.objects.link(camera);camdat.type='ORTHO';camdat.clip_start=.00001;camdat.clip_end=span*30;scene.camera=camera
if a.gray:
 clay=make_material('temporary-neutral-gray','#929292',.85);bpy.context.view_layer.material_override=clay
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
rows=[]
for name,direction in views.items():
 camera.location=center+Vector(direction).normalized()*span*4;_look_at(camera,center);bpy.context.view_layer.update();inv=camera.matrix_world.inverted();projected=[inv@pt for pt in points];xmin=min(p.x for p in projected);xmax=max(p.x for p in projected);ymin=min(p.y for p in projected);ymax=max(p.y for p in projected)
 camera.location+=camera.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));camdat.ortho_scale=max(xmax-xmin,ymax-ymin)*1.23
 target=a.out/(name+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True)
 rows.append({'view':name,'direction_blender':direction,'camera_location_m':list(camera.location),'ortho_scale_m':camdat.ortho_scale,'sha256':sha(target),'filename':target.name})
report={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','source':'clean import of exact delivered GLB','glb_sha256':sha(a.glb),'blender_version':bpy.app.version_string,'render_engine':'Cycles CPU','threads':2,'samples':a.samples,'resolution':a.resolution,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'background_srgb':'#E8E4DC','lights':lights,'gray_override':a.gray,'source_bounds_blender_m':{'min':low,'max':high},'views':rows,'geometry_unchanged':True}
(a.out/'render-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
