# SPDX-License-Identifier: MIT
"""Render four canonical proof views from an independently imported final GLB.
Lighting and color conversion reuse the pinned asset_common helper.
"""
from pathlib import Path
import sys,math,json,hashlib,argparse,time
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb
ap=argparse.ArgumentParser();ap.add_argument('--glb',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--resolution',type=int,default=768);ap.add_argument('--samples',type=int,default=48);ap.add_argument('--clay',action='store_true')
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
glbsha=sha(a.glb);audit=audit_glb(a.glb,6500,6,12);assert not audit['errors']
col=setup_scene('exact-glb-view');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
new=[o for o in bpy.data.objects if o not in before]
for ob in new:link_object(ob,col,parent=False)
points=_vertices_world(col);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)])
span=max(high[i]-low[i] for i in range(3));scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
 ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
cd=bpy.data.cameras.new('proof-camera');cam=bpy.data.objects.new('proof-camera',cd);scene.collection.objects.link(cam);scene.camera=cam;cd.type='ORTHO';cd.clip_start=.01;cd.clip_end=span*30
if a.clay:bpy.context.view_layer.material_override=make_material('clay','#929292')
# One locked orthographic scale for all views, including the narrow frontal crest.
# Geometry is not rotated or rescaled between views.
cd.ortho_scale=span*1.10
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
config={'schema':1,'source_glb_sha256':glbsha,'renderer':'Blender Cycles CPU','blender':bpy.app.version_string,'threads':2,'samples':a.samples,'resolution':[a.resolution,a.resolution],'transparent':True,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'denoising':False,'camera':{'type':'ORTHO','scale_m':cd.ortho_scale,'target_blender_m':list(center),'directions':views,'fixed_across_views':True},'lights':{'key':[-3,-4,6,450,4],'fill':[4,-1,3,150,5],'world_strength':.3,'scale_basis_m':span},'clay':a.clay,'renderer_sha256':sha(Path(__file__)),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'glb_imported_in_fresh_factory_scene':True,'imported_bounds_blender_m':{'min':low,'max':high},'gpu':'UNKNOWN','scene':'UNKNOWN'}
(out/'render-config.json').write_text(json.dumps(config,indent=2)+'\n');frames=[]
for name,d in views.items():
 cam.location=center+Vector(d).normalized()*span*2.4;_look_at(cam,center);scene.render.filepath=str(out/(name+'.png'))
 start=time.monotonic();bpy.ops.render.render(write_still=True)
 frames.append({'view':name,'path':'views/'+name+'.png','sha256':sha(out/(name+'.png')),'source_glb_sha256':glbsha,'camera_direction_blender':d,'wall_seconds':round(time.monotonic()-start,4)})
assert sha(a.glb)==glbsha
(out/'views-manifest.json').write_text(json.dumps({'source_glb_sha256':glbsha,'render_config_sha256':sha(out/'render-config.json'),'frames':frames,'claim':'Exact-GLB Blender CPU image evidence only. No GPU, scene or independent acceptance.'},indent=2)+'\n')
