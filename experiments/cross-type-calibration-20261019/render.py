# SPDX-License-Identifier: MIT
"""Frozen actual GLBs, matched camera/light/meter scale before/after."""
import bpy,sys,math,json,hashlib,shutil
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;ROOT=H.parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import make_material
sources={'conglomerate-outcrop':ROOT/'assets/additions/conglomerate-outcrop/small-life-round08-20261018/conglomerate-outcrop.glb','horsetail-cluster':ROOT/'assets/prehistoric/plants/horsetail-cluster/horsetail-cluster.glb'}
records=[]
for slug,old in sources.items():
 height=.22 if slug.startswith('conglomerate') else .75;fit=1.08 if slug.startswith('conglomerate') else 1.95;target=Vector((0,0,height))
 for version,path in [('before',old),('candidate',H/'candidates'/slug/(slug+'.glb'))]:
  bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;bpy.ops.import_scene.gltf(filepath=str(path));models=[o for o in s.objects if o.type=='MESH'];materials={o.name:list(o.data.materials) for o in models}
  s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
  s.world=bpy.data.worlds.new('neutral-studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.42,.42,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.5
  bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));bpy.context.object.data.materials.append(make_material('neutral-ground','#BBBAB5',.95))
  for name,loc,power,size in [('key',(-3,-4,5),190,4),('fill',(4,-2,3),90,4),('back',(0,3,4),80,3)]:
   d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
  d=bpy.data.cameras.new('matched-pair-camera');cam=bpy.data.objects.new('camera',d);s.collection.objects.link(cam);s.camera=cam;clay=make_material('clay','#989B99',.9)
  views=[('hero',35,25),('reversehero',215,25),('front',0,8),('side',90,15),('top',0,80),('clay',215 if slug.startswith('conglomerate') else 35,25),('scene-240',35,20)]
  out=H/'evidence'/slug;out.mkdir(parents=True,exist_ok=True)
  for view,az,el in views:
   for o in models:
    for i,m in enumerate(materials[o.name]):o.data.materials[i]=clay if view=='clay' else m
   s.render.resolution_x=s.render.resolution_y=640;s.render.resolution_percentage=100;d.type='ORTHO';d.ortho_scale=fit
   a=math.radians(az);e=math.radians(el);cam.location=target+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*5
   if view=='scene-240':
    s.render.resolution_x=s.render.resolution_y=240;d.type='PERSP';d.lens=50;cam.location=(1.1,-3.0,1.35)
   cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();file=out/(version+'-'+view+'.png');s.render.filepath=str(file);bpy.ops.render.render(write_still=True)
   if version=='candidate' and view=='hero':shutil.copyfile(file,H/'candidates'/slug/'preview-hero.png')
   records.append({'asset_id':slug,'version':version,'view':view,'file':str(file.relative_to(H)),'glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'camera_m':list(cam.location),'target_m':list(target),'projection':d.type,'ortho_scale':fit if d.type=='ORTHO' else None,'lens_mm':50 if d.type=='PERSP' else None,'resolution':s.render.resolution_x,'samples':32,'engine':'Cycles CPU','view_transform':'Standard','exposure':0,'scale':'original meters, no normalization, no burial'})
(H/'render-manifest.json').write_text(json.dumps(records,indent=2))
