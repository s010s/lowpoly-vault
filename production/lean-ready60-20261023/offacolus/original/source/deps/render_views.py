# SPDX-License-Identifier: MIT
"""Scale-aware original render driver for 7 mm asset, with canonical helper lighting/color.
Reads the exact emitted GLB. Never writes source model.blend or model.glb.
"""
import argparse,json,hashlib,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',required=True,type=Path);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=40);p.add_argument('--views',default='front,side,top,perspective,ventral');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output_dir.mkdir(parents=True,exist_ok=True);glbhash=sha(a.glb)
C=setup_scene('offacolus-preview');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));imported=set(bpy.data.objects)-before
for obj in imported:link_object(obj,C,parent=False)
points=_vertices_world(C);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);radius=max((v-center).length for v in points)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True;scene.world=world;nd=world.node_tree.nodes;lk=world.node_tree.links
bg=nd['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.40
cb=nd.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in(232,228,220))+(1,);cb.inputs['Strength'].default_value=1
lp=nd.new('ShaderNodeLightPath');mix=nd.new('ShaderNodeMixShader');lk.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);lk.new(bg.outputs[0],mix.inputs[1]);lk.new(cb.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],nd['World Output'].inputs[0])
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5),('rim',(0,4,4),200,3)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*radius**2;d.shape='DISK';d.size=size*radius;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);lights.append((o,direction))
d=bpy.data.cameras.new('Exact GLB orthographic');cam=bpy.data.objects.new('Exact GLB orthographic',d);scene.collection.objects.link(cam);d.type='ORTHO';d.clip_start=radius/1000;d.clip_end=radius*40;scene.camera=cam
if a.clay:bpy.context.view_layer.material_override=make_material('Diagnostic clay','#93938B',roughness=.9)
dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1),'ventral':(0,0,-1)}
frames=[]
for view in a.views.split(','):
 direction=Vector(dirs[view]).normalized();cam.location=center+direction*radius*6;_look_at(cam,center)
 bpy.context.view_layer.update();rot=cam.rotation_euler.to_matrix();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0))
 ranges=[]
 for axis in(right,up):r=[(v-center).dot(axis) for v in points];ranges.append(max(r)-min(r))
 d.ortho_scale=max(ranges)*1.16
 for o,ld in lights:o.location=center+Vector((ld[0],ld[1],-ld[2] if view=='ventral' else ld[2]))*radius;_look_at(o,center)
 target=a.output_dir/(view+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True)
 frames.append({'view':view,'path':target.name,'sha256':sha(target),'camera_direction_blender':dirs[view],'ortho_scale_m':d.ortho_scale,'resolution':a.resolution,'samples':a.samples,'ventral_light_inversion':view=='ventral'})
assert sha(a.glb)==glbhash
(a.output_dir/'render-evidence.json').write_text(json.dumps({'source':'exact clean GLB import','glb_sha256':glbhash,'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','render_driver_sha256':sha(__file__),'clay':a.clay,'frames':frames,'threads':2,'view_transform':'Standard','look':'None','gamma':1,'exposure':0,'background':'#E8E4DC','bounds_blender_m':{'min':low,'max':high},'notes':'Per-view projected-bounds framing. Geometry remains in exact real-world metres. Ventral lights mirrored below to reveal anatomy. No source-scene or research image used as final preview.'},indent=2)+'\n')
print('RENDER_COMPLETE',glbhash)
