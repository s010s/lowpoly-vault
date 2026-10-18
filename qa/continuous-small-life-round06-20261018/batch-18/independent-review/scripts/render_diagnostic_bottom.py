import bpy,sys,json
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
glb=Path(args[0]);out=Path(args[1]);out.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb))
pts=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH':pts.extend([o.matrix_world@v.co for v in o.data.vertices])
if not pts:raise RuntimeError('no mesh')
lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(lo+hi)/2;size=hi-lo;radius=max(size.length/2,.001)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=1024;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False;scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('review-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.72,0.72,0.72,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.15;scene.world=world
for name,offset,factor in [('key',Vector((-1,-.5,-1)),.07),('fill',Vector((1,.4,-.7)),.025)]:
 data=bpy.data.lights.new('review-'+name,'AREA');data.energy=450*(2*radius)**2/4*factor;data.shape='DISK';data.size=radius*4;obj=bpy.data.objects.new('review-'+name,data);scene.collection.objects.link(obj);obj.location=center+offset*radius;obj.rotation_euler=(center-obj.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('review-camera');camera=bpy.data.objects.new('review-camera',data);scene.collection.objects.link(camera);camera.location=center+Vector((0,0,-radius*6));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=max(size.x,size.y)*1.15;data.clip_start=.0001;data.clip_end=radius*20;scene.camera=camera
scene.render.filepath=str(out);bpy.ops.render.render(write_still=True);print(json.dumps({'glb':str(glb),'bounds_blender_m':{'min':list(lo),'max':list(hi)},'size_m':list(size),'camera':'targeted underside orthographic','samples':24,'resolution':[1024,1024]}))
