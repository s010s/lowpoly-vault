# SPDX-License-Identifier: MIT
"""Exact-GLB four-view renderer. Temporary imported scene only; source untouched."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',default=1024,type=int);p.add_argument('--samples',default=32,type=int);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
col=setup_scene('darwinius-preview');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
for ob in set(bpy.data.objects)-before:link_object(ob,col,parent=False)
pts=_vertices_world(col);low,high=_bounds(pts);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False;scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('_preview_world');world.use_nodes=True;scene.world=world
nodes=world.node_tree.nodes;links=world.node_tree.links;bg=nodes.get('Background');bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
cb=nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath');mx=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mx.inputs[0]);links.new(bg.outputs[0],mx.inputs[1]);links.new(cb.outputs[0],mx.inputs[2]);links.new(mx.outputs[0],nodes.get('World Output').inputs['Surface'])
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
camdata=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.type='ORTHO';camdata.clip_start=.0001;camdata.clip_end=span*30
if a.gray:scene.view_layers[0].material_override=make_material('gray','#969696',.9)
frames={};dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
if a.gray:dirs={k:dirs[k] for k in ['top','side','perspective']}
for name,direction in dirs.items():
 cam.location=center+Vector(direction).normalized()*span*3;_look_at(cam,center)
 if name=='top':cam.rotation_euler.z+=math.pi
 # Projected geometry framing, with no cutoffs. Canonical edge views stay honest.
 R=cam.rotation_euler.to_matrix().transposed();pr=[R@(v-center) for v in pts];w=max(v.x for v in pr)-min(v.x for v in pr);hh=max(v.y for v in pr)-min(v.y for v in pr);camdata.ortho_scale=max(w,hh)*1.14
 scene.render.filepath=str(a.output/(name+'.png'));bpy.ops.render.render(write_still=True)
 frames[name]={'path':name+'.png','sha256':h(a.output/(name+'.png')),'camera_direction_blender':list(direction),'camera_target':list(center),'ortho_scale':camdata.ortho_scale,'roll_degrees':180 if name=='top' else 0}
record={'status':'RENDERED','claim_scope':'Fresh Blender import of exact GLB; not Three.js GPU or independent visual approval','glb_sha256':h(a.glb),'renderer_sha256':h(__file__),'blender_version':bpy.app.version_string,'engine':'CYCLES CPU','threads':2,'samples':a.samples,'resolution':a.resolution,'gray_override':a.gray,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'lights':[['key',[-3,-4,6],450,4],['fill',[4,-1,3],150,5]],'world_strength':.3,'background_srgb':'#E8E4DC','frames':frames,'bounds_blender_m':{'min':low,'max':high}}
(a.output/'render-evidence.json').write_text(json.dumps(record,indent=2)+'\n')
