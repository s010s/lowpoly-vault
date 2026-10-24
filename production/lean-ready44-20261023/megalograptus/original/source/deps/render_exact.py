# SPDX-License-Identifier: MIT
"""Four hash-bound diagnostic views from a clean import of the actual GLB.
Uses project color conversion and camera utilities; this is Cycles CPU, not GPU evidence.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear
p=argparse.ArgumentParser();p.add_argument('--glb',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);a.out.mkdir(parents=True,exist_ok=True)
col=setup_scene('megalograptus-review');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb));imported=[o for o in bpy.data.objects if o not in before]
for o in imported:link_object(o,col,parent=False)
if a.clay:
 mat=make_material('Diagnostic-clay','#929999',roughness=.9)
 for o in imported:
  if o.type=='MESH':
   o.data.materials.clear();o.data.materials.append(mat)
   for face in o.data.polygons:face.material_index=0
points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral-world');world.use_nodes=True;nodes=world.node_tree.nodes;links=world.node_tree.links
nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);nodes['Background'].inputs['Strength'].default_value=.45
bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(nodes['Background'].outputs[0],mix.inputs[1]);links.new(bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface']);s.world=world
cd=bpy.data.cameras.new('Review-camera');cam=bpy.data.objects.new('Review-camera',cd);s.collection.objects.link(cam);cd.type='ORTHO';cd.clip_start=.00001;cd.clip_end=span*30;s.camera=cam
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};records=[]
for name,direction in views.items():
 cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();q=[inv@v for v in points]
 x0=min(v.x for v in q);x1=max(v.x for v in q);y0=min(v.y for v in q);y1=max(v.y for v in q)
 cam.location+=cam.matrix_world.to_3x3()@Vector(((x0+x1)/2,(y0+y1)/2,0));cd.ortho_scale=max(x1-x0,y1-y0)*1.14
 s.render.filepath=str(a.out/(name+'.png'));bpy.ops.render.render(write_still=True)
 records.append({'view':name,'camera_direction_blender':direction,'camera_position_blender_m':list(cam.location),'orthographic_scale_m':cd.ortho_scale,'png_sha256':hashlib.sha256((a.out/(name+'.png')).read_bytes()).hexdigest()})
(a.out/'render-receipt.json').write_text(json.dumps({'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','glb_sha256':hashlib.sha256(a.glb.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'import':'clean Blender glTF import','engine':'Cycles CPU','blender_version':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'clay':a.clay,'view_transform':'Standard','look':'None','background_srgb':'#E8E4DC','views':records,'gpu':'UNKNOWN','scene':'UNKNOWN'},indent=2)+'\n')
