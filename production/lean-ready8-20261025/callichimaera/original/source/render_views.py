# SPDX-License-Identifier: MIT
"""Four exact GLB canonical views. CPU evidence, not GPU/scene acceptance."""
import sys,json,math,hashlib,argparse,time
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'deps'))
from asset_common import make_material,srgb_to_linear
ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--resolution',type=int,default=768);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--clay',action='store_true');ap.add_argument('--views',default='front,side,top,perspective');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
before=sha(a.glb);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
objs=[o for o in bpy.context.scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in objs for v in o.data.vertices]
lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)]);center=(lo+hi)/2;span=max(hi-lo)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=a.resolution;scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.30;scene.world=world
def aim(o,target):o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;aim(o,center)
camd=bpy.data.cameras.new('canonical-camera');cam=bpy.data.objects.new('canonical-camera',camd);scene.collection.objects.link(cam);scene.camera=cam;camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=span*30
if a.clay:bpy.context.view_layer.material_override=make_material('diagnostic-clay','#929292',roughness=.85)
rows=[]
for name in a.views.split(','):
 direction=Vector({'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1),'ventral':(1,-1,-.8)}[name]);cam.location=center+direction.normalized()*span*4;aim(cam,center);bpy.context.view_layer.update()
 inv=cam.matrix_world.inverted();cp=[inv@v for v in points];w=max(p.x for p in cp)-min(p.x for p in cp);h=max(p.y for p in cp)-min(p.y for p in cp);camd.ortho_scale=max(w,h)*1.16
 # Center projected bounds without changing geometry or canonical camera direction.
 shiftx=(max(p.x for p in cp)+min(p.x for p in cp))/2;shifty=(max(p.y for p in cp)+min(p.y for p in cp))/2
 cam.location+=cam.matrix_world.to_3x3()@Vector((shiftx,shifty,0));bpy.context.view_layer.update()
 path=a.output/(name+'.png');scene.render.filepath=str(path.resolve());start=time.monotonic();bpy.ops.render.render(write_still=True)
 rows.append({'view':name,'file':name+'.png','sha256':sha(path),'bytes':path.stat().st_size,'camera_direction_blender':list(direction),'camera_location_m':list(cam.location),'orthographic_scale_m':camd.ortho_scale,'resolution':[a.resolution,a.resolution],'samples':a.samples,'elapsed_seconds':round(time.monotonic()-start,3)})
assert sha(a.glb)==before
(a.output/'render-manifest.json').write_text(json.dumps({'glb_sha256':before,'source':'clean import of exact GLB','blender_version':bpy.app.version_string,'renderer':'Cycles CPU','threads':2,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'transparent':True,'clay':a.clay,'geometry_bounds_blender_m':{'min':list(lo),'max':list(hi)},'lights':{'key':[-3,-4,6],'fill':[4,-1,3],'world_strength':.3},'views':rows,'gpu':'UNKNOWN','scene':'UNKNOWN'},indent=2)+'\n')
