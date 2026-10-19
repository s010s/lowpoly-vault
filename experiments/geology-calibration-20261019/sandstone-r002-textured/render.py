# SPDX-License-Identifier: MIT
"""Three-version exact GLB comparison. No production or source asset writes."""
import bpy,sys,math,json,hashlib,shutil
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;E=H.parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT/'scripts'));from asset_common import make_material
sources={'production':ROOT/'assets/additions/cross-bedded-sandstone/small-life-round11-20261018/cross-bedded-sandstone.glb','previous':E/'cross-bedded-sandstone/cross-bedded-sandstone.glb','new':H/'cross-bedded-sandstone/cross-bedded-sandstone.glb'}
records=[]
for version,path in sources.items():
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;bpy.ops.import_scene.gltf(filepath=str(path));meshes=[o for o in s.objects if o.type=='MESH'];original={o.name:list(o.data.materials) for o in meshes}
 s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=False
 s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
 s.world=bpy.data.worlds.new('neutral-soft-studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.42,.42,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.5
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));floor=bpy.context.object;floor.data.materials.append(make_material('same-neutral-ground','#BBBAB5',.95))
 target=Vector((0,0,.26))
 for name,loc,power,size in [('key',(-3,-4,5),190,4),('fill',(4,-2,3),90,4),('back',(0,3,4),80,3)]:
  d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
 d=bpy.data.cameras.new('fixed-three-version-camera');cam=bpy.data.objects.new('camera',d);s.collection.objects.link(cam);s.camera=cam
 clay=make_material('diagnostic-clay','#979B9A',.9)
 out=H/'views';out.mkdir(exist_ok=True)
 for view,az,el in [('bedding-side',0,8),('right-side',90,12),('hero',35,25),('clay',35,25),('scene-240',25,18)]:
  for o in meshes:
   for i,m in enumerate(original[o.name]):o.data.materials[i]=clay if view=='clay' else m
  if view=='scene-240':
   d.type='PERSP';d.lens=50;cam.location=(1.05,-2.55,1.2);s.render.resolution_x=s.render.resolution_y=240
  else:
   d.type='ORTHO';d.ortho_scale=1.12;a=math.radians(az);e=math.radians(el);cam.location=target+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*4;s.render.resolution_x=s.render.resolution_y=640
  s.render.resolution_percentage=100;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();file=out/(version+'-'+view+'.png');s.render.filepath=str(file);bpy.ops.render.render(write_still=True)
  if version=='new' and view=='hero':shutil.copyfile(file,H/'cross-bedded-sandstone/preview-hero.png')
  records.append({'version':version,'view':view,'file':str(file.relative_to(H)),'source_glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'camera_m':list(cam.location),'target_m':list(target),'projection':d.type,'ortho_scale':d.ortho_scale if d.type=='ORTHO' else None,'lens_mm':d.lens if d.type=='PERSP' else None,'physical_scale':'unchanged 1:1 meters; no normalization or burial','resolution':s.render.resolution_x,'samples':64,'engine':'Cycles CPU','view_transform':'Standard','exposure':0})
(H/'render-manifest.json').write_text(json.dumps(records,indent=2))
