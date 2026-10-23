#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Four exact-export orthographic views, independent of authoring scene.
Uses local canonical asset_common color, normals, bounds and camera utilities.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=1024);p.add_argument('--samples',type=int,default=64)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
assert not any(a.out.iterdir()),'Use a fresh output directory'
C=setup_scene('macropoma-exact-export-render');old=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
for ob in bpy.data.objects:
 if ob not in old:link_object(ob,C,parent=False)
pts=_vertices_world(C);low,high=_bounds(pts);center=Vector([(low[i]+high[i])/2 for i in range(3)]);radius=max((p-center).length for p in pts)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral_studio');world.use_nodes=True;n=world.node_tree.nodes;links=world.node_tree.links
n['Background'].inputs['Color'].default_value=(.75,.75,.75,1);n['Background'].inputs['Strength'].default_value=.32
background=n.new('ShaderNodeBackground');background.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,);background.inputs['Strength'].default_value=1
lp=n.new('ShaderNodeLightPath');mix=n.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(n['Background'].outputs[0],mix.inputs[1]);links.new(background.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],n['World Output'].inputs['Surface']);scene.world=world
lights=[]
for name,direction,energy,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*(2*radius)**2/4;data.shape='DISK';data.size=size*radius;ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*radius;_look_at(ob,center);lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
camdata=bpy.data.cameras.new('Exact_GLB_camera');cam=bpy.data.objects.new('Exact_GLB_camera',camdata);scene.collection.objects.link(cam);camdata.type='ORTHO';camdata.clip_start=.0001;camdata.clip_end=10;scene.camera=cam
if a.clay:bpy.context.view_layer.material_override=make_material('Gray diagnostic','#929292',roughness=.87)
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
record={'artifact_glb_sha256':sha(a.glb),'source':'Clean import of delivered GLB; source blend never opened.','renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':a.resolution,'samples':a.samples,'threads':2,'clay':a.clay,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'bounds_blender':{'min':list(low),'max':list(high)},'lighting':lights,'world_strength':.32,'background_srgb':'#E8E4DC','renderer_sha256':sha(__file__),'views':{}}
for name,direction in views.items():
 vec=Vector(direction).normalized();cam.location=center+vec*radius*6;_look_at(cam,center)
 # Canonical directions, all view bounds fitted analytically with generous safe margin.
 bpy.context.view_layer.update();inv=cam.matrix_world.inverted(); projected=[inv@p for p in pts];sx=max(v.x for v in projected)-min(v.x for v in projected);sy=max(v.y for v in projected)-min(v.y for v in projected);camdata.ortho_scale=max(sx,sy)*1.17
 scene.render.filepath=str(a.out/(name+'.png'));bpy.ops.render.render(write_still=True)
 record['views'][name]={'camera_direction':direction,'orthographic_scale':camdata.ortho_scale,'sha256':sha(a.out/(name+'.png')),'path':name+'.png'}
(a.out/'render-evidence.json').write_text(json.dumps(record,indent=2)+'\n')
