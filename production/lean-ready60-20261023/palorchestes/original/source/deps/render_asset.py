# SPDX-License-Identifier: MIT
"""Four actual-GLB views with pinned axes, stable framing and canonical helper lighting."""
from pathlib import Path
import argparse,hashlib,json,math,sys,time
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',type=Path,required=True)
p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=512);p.add_argument('--samples',type=int,default=24)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output_dir.mkdir(parents=True,exist_ok=True)
sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
col=setup_scene('exact-export-preview');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
for ob in set(bpy.data.objects)-before:link_object(ob,col,parent=False)
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
points=_vertices_world(col);low,high=_bounds(points);center=Vector([(x+y)/2 for x,y in zip(low,high)])
radius=max((v-center).length for v in points);scale=radius*2.16
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral_studio');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
cb=world.node_tree.nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader')
world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],mix.inputs[1]);world.node_tree.links.new(cb.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']);scene.world=world
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*radius*radius;data.shape='DISK';data.size=size*radius
 ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*radius;_look_at(ob,center)
 lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
camd=bpy.data.cameras.new('Orthographic_review');cam=bpy.data.objects.new('Orthographic_review',camd);scene.collection.objects.link(cam);scene.camera=cam
camd.type='ORTHO';camd.ortho_scale=scale;camd.clip_start=.001;camd.clip_end=100
if a.clay:
 clay=make_material('Review_clay','#929292')
 for ob in col.all_objects:
  if ob.type=='MESH':
   ob.data.materials.clear();ob.data.materials.append(clay)
   for face in ob.data.polygons:face.material_index=0
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,'transparent':False,'background':'#E8E4DC','color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'camera':{'type':'ORTHO','target_blender_m':list(center),'scale':scale,'directions':views,'fixed_orbit_framing':True},'lights':lights,'world_strength':.3,'clay_override':a.clay,'renderer_sha256':sha(__file__),'asset_common_sha256':sha(Path(__file__).with_name('asset_common.py')),'source_glb_sha256':sha(a.glb)}
(a.output_dir/'render-config.json').write_text(json.dumps(config,indent=2)+'\n');frames=[];start=time.time()
for name,direction in views.items():
 cam.location=center+Vector(direction).normalized()*radius*6;_look_at(cam,center)
 scene.render.filepath=str((a.output_dir/(name+'.png')).resolve());t=time.time();bpy.ops.render.render(write_still=True)
 path=a.output_dir/(name+'.png');frames.append({'view':name,'path':name+'.png','sha256':sha(path),'bytes':path.stat().st_size,'width':a.resolution,'height':a.resolution,'camera_direction_blender':direction,'wall_seconds':round(time.time()-t,4)})
report={'kind':'exact-export-four-views','source_glb_sha256':sha(a.glb),'config_sha256':sha(a.output_dir/'render-config.json'),'source_bounds_blender_m':{'min':low,'max':high},'frames':frames,'visual_review':'PENDING','gpu_render':'UNKNOWN','wall_seconds':round(time.time()-start,4)}
(a.output_dir/'views.json').write_text(json.dumps(report,indent=2)+'\n')
print('VIEWS_COMPLETE',report['source_glb_sha256'])
