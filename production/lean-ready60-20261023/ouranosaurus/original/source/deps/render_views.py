# SPDX-License-Identifier: MIT
"""Four portable exact-GLB CPU evidence views; optional three-view clay check."""
from pathlib import Path
import argparse,hashlib,json,math,sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear
ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--output-dir',required=True,type=Path);ap.add_argument('--clay',action='store_true');ap.add_argument('--resolution',type=int,default=768);ap.add_argument('--samples',type=int,default=64)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output_dir;out.mkdir(exist_ok=True,parents=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
col=setup_scene('ouranosaurus-render');root=bpy.data.objects[col['asset_root']];before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
imported=[o for o in bpy.data.objects if o not in before]
for o in imported:link_object(o,col,parent=False)
for o in imported:
 if o.parent not in imported:
  mat=o.matrix_world.copy();o.parent=root;o.matrix_world=mat
points=_vertices_world(col);low,high=_bounds(points);target=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
camera_bg=world.node_tree.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],mix.inputs[1]);world.node_tree.links.new(camera_bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']);scene.world=world
light_config=[]
for name,dr,en,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=en*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=target+Vector(dr)*span/2;_look_at(o,target);light_config.append({'name':name,'direction':dr,'energy':d.energy,'size':d.size})
camdata=bpy.data.cameras.new('qa-camera');cam=bpy.data.objects.new('qa-camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=span*40
clay=make_material('neutral-clay','#929292')
if a.clay:scene.view_layers[0].material_override=clay
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
if a.clay:views={k:views[k] for k in ['front','side','perspective']}
result=[]
for name,dr in views.items():
 cam.location=target+Vector(dr).normalized()*span*3;_look_at(cam,target)
 # Fit exact projected vertices with a documented stable margin, no cropped tail.
 bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points];width=max(p.x for p in proj)-min(p.x for p in proj);height=max(p.y for p in proj)-min(p.y for p in proj);camdata.ortho_scale=max(width,height)*1.16
 scene.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
 result.append({'path':name+'.png','sha256':sha(out/(name+'.png')),'camera_direction':dr,'camera_location':list(cam.location),'target':list(target),'orthographic_scale':camdata.ortho_scale,'width':a.resolution,'height':a.resolution})
report={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','source':'clean import of the delivered model.glb','glb_sha256':sha(a.glb),'renderer_sha256':sha(__file__),'engine':'Cycles CPU','blender_version':bpy.app.version_string,'samples':a.samples,'denoising':False,'threads':2,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'background_srgb':'#E8E4DC','transparent':False,'clay_override':a.clay,'lighting':light_config,'views':result,'gpu_status':'UNKNOWN','website_renderer_equivalence':'NOT_CLAIMED'}
(out/'render-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
