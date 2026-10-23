# SPDX-License-Identifier: MIT
"""Exact delivered GLB renderer, using canonical material/color and light conventions.
All arguments and output hashes are recorded. No source scene dependency.
"""
import bpy,sys,json,math,hashlib,argparse
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));import asset_common as ac
p=argparse.ArgumentParser();p.add_argument('--glb',required=True);p.add_argument('--output',required=True);p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48);p.add_argument('--clay',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(a.output);out.mkdir(parents=True,exist_ok=True);src=Path(a.glb)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(src))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
lo,hi=ac._bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3));scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=a.resolution;scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;ac._look_at(o,center)
camd=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',camd);scene.collection.objects.link(cam);camd.type='ORTHO';camd.ortho_scale=span*1.4;camd.clip_start=span/1000;camd.clip_end=span*30;scene.camera=cam
if a.clay:
 clay=ac.make_material('diagnostic-grey','#999999',roughness=.85)
 for o in meshes:
  o.data.materials.clear();o.data.materials.append(clay)
  for poly in o.data.polygons:poly.material_index=0
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
meta={'source_glb_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','samples':a.samples,'resolution':a.resolution,'clay':a.clay,'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'camera_type':'ORTHO','ortho_scale':camd.ortho_scale,'target_m':list(center),'views':{}}
for name,direction in views.items():
 cam.location=center+Vector(direction).normalized()*span*4;ac._look_at(cam,center);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 meta['views'][name]={'path':name+'.png','direction':direction,'sha256':hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest()}
(out/'render-manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
