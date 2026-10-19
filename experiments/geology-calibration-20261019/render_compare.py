# SPDX-License-Identifier: MIT
"""Renders exact before/after GLBs using fixed per-pair cameras, scale and lights."""
import bpy,sys,json,math,hashlib,shutil
from pathlib import Path
from mathutils import Vector, Matrix
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import make_material
baseline={'cross-bedded-sandstone':'assets/additions/cross-bedded-sandstone/small-life-round11-20261018/cross-bedded-sandstone.glb','hydrothermal-chimney':'assets/additions/hydrothermal-chimney/small-life-round09-20261018/hydrothermal-chimney.glb'}
manifest=[]
for slug,old in baseline.items():
 # Shared target/ortho scale per pair derived from union; no per-image normalization.
 scale=1.12 if slug=='cross-bedded-sandstone' else 1.22
 target=Vector((0,0,.25 if slug=='cross-bedded-sandstone' else .43))
 for version,path in [('before',ROOT/old),('after',HERE/slug/(slug+'.glb'))]:
  bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
  bpy.ops.import_scene.gltf(filepath=str(path));meshes=[o for o in sc.objects if o.type=='MESH']
  sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.use_denoising=False
  sc.render.resolution_x=640;sc.render.resolution_y=640;sc.render.resolution_percentage=100
  sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
  sc.world=bpy.data.worlds.new('neutral-studio');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.32,.32,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.3
  bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));floor=bpy.context.object;floor.name='presentation-floor';floor.data.materials.append(make_material('neutral-floor','#D4D2CD',.92))
  for name,loc,power,size in [('key',(-2,-3,4),380,3),('fill',(3,-1,2),160,3),('back',(0,3,4),250,2.5)]:
   d=bpy.data.lights.new(name,'AREA');d.energy=power*.45;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
  d=bpy.data.cameras.new('fixed-pair-camera');cam=bpy.data.objects.new('camera',d);sc.collection.objects.link(cam);sc.camera=cam;d.type='ORTHO';d.ortho_scale=scale
  clay=make_material('clay-neutral','#999C9C',.9);original={o.name:[m for m in o.data.materials] for o in meshes}
  out=HERE/slug/'views';out.mkdir(exist_ok=True)
  plan=[('thumbnail-scene-240',35,25)] if '--scene-only' in sys.argv else [('hero',35,25),('front',0,7),('back',180,18),('clay',35,25),('top',0,80),('side',90,15),('reversehero',215,25),('thumbnail-240',35,25)]
  for name,az,el in plan:
   for o in meshes:
    for i,m in enumerate(original[o.name]):o.data.materials[i]=clay if name=='clay' else m
   a=math.radians(az);e=math.radians(el);cam.location=target+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*4;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
   # Small staging scene is genuine 240px render, with two smaller support rocks.
   extras=[]
   if name.startswith('thumbnail'):
    sc.render.resolution_x=sc.render.resolution_y=240;d.ortho_scale=scale*1.15
    if name=='thumbnail-scene-240':
     d.ortho_scale=scale*2.3
     for sign in [-1,1]:
      for src in meshes:
       obj=src.copy();obj.data=src.data;sc.collection.objects.link(obj);obj.parent=None
       obj.matrix_world=Matrix.Translation((sign*.60,.24,0)) @ Matrix.Rotation(sign*.65,4,'Z') @ Matrix.Scale(.65,4) @ src.matrix_world
       extras.append(obj)
    # Neutral floor gives contact/scale context without exporting scenery.
   else:sc.render.resolution_x=sc.render.resolution_y=640;d.ortho_scale=scale
   file=out/(version+'-'+name+'.png');sc.render.filepath=str(file);bpy.ops.render.render(write_still=True)
   if version=='after' and name=='hero':shutil.copyfile(file,HERE/slug/'preview-hero.png')
   manifest.append({'slug':slug,'version':version,'view':name,'file':str(file.relative_to(HERE)),'source_glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'camera_location':list(cam.location),'target':list(target),'ortho_scale':d.ortho_scale,'azimuth':az,'elevation':el,'resolution':sc.render.resolution_x,'engine':'Cycles CPU','samples':32,'view_transform':'Standard','exposure':0})
(HERE/('scene-render-manifest.json' if '--scene-only' in sys.argv else 'render-manifest.json')).write_text(json.dumps(manifest,indent=2))
