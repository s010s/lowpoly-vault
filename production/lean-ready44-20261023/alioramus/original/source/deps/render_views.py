#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Render the delivered GLB from an empty Blender scene, never the source blend.
Neutral common-helper lighting. Canonical orthographic views, plus a (1,-1,1) oblique.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys,time
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--resolution',type=int,default=1024);p.add_argument('--samples',type=int,default=32);p.add_argument('--clay',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output_dir.mkdir(parents=True,exist_ok=True)
digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sha=digest(a.glb);col=setup_scene('exact-glb-view');root=bpy.data.objects[col['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
obs=[o for o in bpy.data.objects if o not in before]
for o in obs:link_object(o,col,parent=False)
for o in obs:
 if o.parent not in obs:
  mat=o.matrix_world.copy();o.parent=root;o.matrix_world=mat
bpy.context.view_layer.update();points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3));scale=span*1.12
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
w=bpy.data.worlds.new('neutral-studio');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;s.world=w
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center);lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
camdata=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',camdata);s.collection.objects.link(cam);s.camera=cam;camdata.type='ORTHO';camdata.ortho_scale=scale;camdata.clip_start=.001;camdata.clip_end=100
if a.clay:bpy.context.view_layer.material_override=make_material('clay','#929292',roughness=.85)
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'source_glb_sha256':sha,'renderer_sha256':digest(__file__),'helper_sha256':digest(Path(__file__).with_name('asset_common.py')),'resolution':[a.resolution,a.resolution],'samples':a.samples,'denoising':False,'threads':2,'background':'transparent','color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'world_strength':.3,'lights':lights,'camera_type':'ORTHOGRAPHIC','camera_target_blender_m':list(center),'orthographic_scale_m':scale,'directions':views,'clay_override':a.clay,'source_bounds_blender_m':{'min':lo,'max':hi}}
(a.output_dir/'render-config.json').write_text(json.dumps(config,indent=2)+'\n');frames=[]
for name,direction in views.items():
 cam.location=center+Vector(direction).normalized()*span*3;_look_at(cam,center);s.render.filepath=str((a.output_dir/(name+'.png')).resolve());start=time.monotonic();bpy.ops.render.render(write_still=True);f=a.output_dir/(name+'.png');frames.append({'view':name,'path':f.name,'sha256':digest(f),'bytes':f.stat().st_size,'camera_direction':direction,'wall_seconds':round(time.monotonic()-start,3)})
if digest(a.glb)!=sha:raise RuntimeError('GLB changed during rendering')
r={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','source':'clean import of exact delivered GLB','source_glb_sha256':sha,'config_sha256':digest(a.output_dir/'render-config.json'),'frames':frames,'preview_reuses':'perspective.png','gpu':'UNKNOWN','scene':'UNKNOWN'}
(a.output_dir/'render-manifest.json').write_text(json.dumps(r,indent=2)+'\n')
