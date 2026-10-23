#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Hash-bound exact GLB rendering; four declared views, no asset changes."""
import argparse,hashlib,json,math,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
D={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
p=argparse.ArgumentParser(); p.add_argument('glb',type=Path); p.add_argument('--out',type=Path,required=True);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48);p.add_argument('--views',default='front,side,top,perspective');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a.out.mkdir(parents=True,exist_ok=True)
h=sha(a.glb); c=setup_scene('mixosaurus-render'); root=bpy.data.objects[c['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb)); new=set(bpy.data.objects)-before
for o in new: link_object(o,c,parent=False)
for o in new:
 if o.parent not in new:
  w=o.matrix_world.copy();o.parent=root;o.matrix_world=w
bpy.context.view_layer.update(); pts=_vertices_world(c); low,high=_bounds(pts); center=Vector([(low[i]+high[i])/2 for i in range(3)]);radius=max((x-center).length for x in pts)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
world=bpy.data.worlds.new('neutral_world');world.use_nodes=True; nodes=world.node_tree.nodes;links=world.node_tree.links;bg=nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
cb=nodes.new('ShaderNodeBackground');cb.inputs[0].default_value=tuple(srgb_to_linear(x/255) for x in (232,228,220))+(1,);cb.inputs[1].default_value=1;lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(cb.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs[0]);s.world=world
lights=[]
for name,di,en,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=en*(2*radius)**2/4;data.shape='DISK';data.size=size*radius;o=bpy.data.objects.new(name,data);s.collection.objects.link(o);o.location=center+Vector(di)*radius;_look_at(o,center);lights.append({'name':name,'direction':di,'energy':data.energy,'size':data.size})
d=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',d);s.collection.objects.link(cam);s.camera=cam;d.type='ORTHO';d.clip_start=.0001;d.clip_end=20
if a.clay:bpy.context.view_layer.material_override=make_material('clay','#929292',roughness=.85)
frames=[]
for view in a.views.split(','):
 direction=Vector(D[view]).normalized();cam.location=center+direction*radius*6;_look_at(cam,center);bpy.context.view_layer.update()
 inv=cam.matrix_world.inverted();proj=[inv@x for x in pts];wh=[max(x[i] for x in proj)-min(x[i] for x in proj) for i in [0,1]];d.ortho_scale=max(wh)*1.17
 path=a.out/(view+'.png');s.render.filepath=str(path);start=time.monotonic();bpy.ops.render.render(write_still=True)
 frames.append({'view':view,'path':path.name,'sha256':sha(path),'camera_direction':D[view],'camera_target':list(center),'orthographic_scale':d.ortho_scale,'width':a.resolution,'height':a.resolution,'seconds':round(time.monotonic()-start,3)})
assert sha(a.glb)==h
report={'kind':'exact-GLB clean import render','glb_sha256':h,'source_unchanged':True,'renderer_sha256':sha(__file__),'blender_version':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'samples':a.samples,'resolution':a.resolution,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background_srgb':'#E8E4DC','lights':lights,'clay':a.clay,'frames':frames,'scope':'Evidence rendering only; not independent visual or runtime approval'}
(a.out/'render-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'RENDERED','glb_sha256':h,'frames':len(frames)}))
