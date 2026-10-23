# SPDX-License-Identifier: MIT
"""Exact-export four canonical review views, deliberately CPU-only evidence."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear
p=argparse.ArgumentParser();p.add_argument('--glb',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=32)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);a.out.mkdir(parents=True,exist_ok=True)
h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest();gh=h(a.glb)
col=setup_scene('eurypterus-exact-review');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb));imported=[o for o in bpy.data.objects if o not in before]
for ob in imported:link_object(ob,col,parent=False)
if a.clay:
 mat=make_material('Diagnostic-gray','#969696',roughness=.85)
 for ob in imported:
  if ob.type=='MESH':
   ob.data.materials.clear();ob.data.materials.append(mat)
   for poly in ob.data.polygons:poly.material_index=0
points=_vertices_world(col);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3));scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Review-neutral-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.32
bg=world.node_tree.nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(x/255) for x in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],mix.inputs[1]);world.node_tree.links.new(bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']);scene.world=world
cd=bpy.data.cameras.new('Canonical-camera');cam=bpy.data.objects.new('Canonical-camera',cd);scene.collection.objects.link(cam);cd.type='ORTHO';cd.clip_start=.00001;cd.clip_end=10;scene.camera=cam
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;ob=bpy.data.objects.new(name,d);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center);lights.append({'name':name,'direction':direction,'energy':d.energy,'size_m':d.size})
records=[]
for name,dr in {'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}.items():
 cam.location=center+Vector(dr).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();qs=[inv@v for v in points]
 width=max(v.x for v in qs)-min(v.x for v in qs);height=max(v.y for v in qs)-min(v.y for v in qs);cd.ortho_scale=max(width,height)*1.14
 offset=cam.matrix_world.to_3x3()@Vector(((max(v.x for v in qs)+min(v.x for v in qs))/2,(max(v.y for v in qs)+min(v.y for v in qs))/2,0));target=center+offset;cam.location+=offset;_look_at(cam,target);bpy.context.view_layer.update()
 scene.render.filepath=str(a.out/(name+'.png'));bpy.ops.render.render(write_still=True)
 records.append({'view':name,'camera_direction_blender':dr,'camera_location_m':list(cam.location),'camera_target_m':list(target),'orthographic_scale_m':cd.ortho_scale,'sha256':h(a.out/(name+'.png'))})
assert h(a.glb)==gh
(a.out/'render-receipt.json').write_text(json.dumps({'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','glb_sha256':gh,'script_sha256':h(__file__),'helper_sha256':h(Path(__file__).with_name('asset_common.py')),'source':'Clean Blender import of the exact delivered GLB','engine':'Cycles CPU','blender_version':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,'clay':a.clay,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'background_srgb':'#E8E4DC','lights':lights,'bounds_blender_m':{'min':low,'max':high},'views':records,'gpu':'UNKNOWN','scene':'UNKNOWN'},indent=2)+'\n')
