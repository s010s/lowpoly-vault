# SPDX-License-Identifier: MIT
"""Four exact-export diagnostic views. This is not a browser or GPU check."""
import argparse, hashlib, json, math, sys, time
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene, link_object, make_material, srgb_to_linear, _vertices_world, _bounds, _look_at
from qa_glb import audit_glb
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--resolution',type=int,default=512);p.add_argument('--samples',type=int,default=32);p.add_argument('--clay',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output_dir.mkdir(parents=True,exist_ok=True)
if any(a.output_dir.iterdir()):raise RuntimeError('Use fresh output directory')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
source_hash=sha(a.glb);audit=audit_glb(a.glb,16000,6,48)
if audit['errors']:raise RuntimeError(audit['errors'])
COL=setup_scene('holmesina-view');ROOT=bpy.data.objects[COL['asset_root']];before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));obs=[o for o in bpy.data.objects if o not in before]
for o in obs:link_object(o,COL,parent=False)
for o in obs:
    if o.parent not in obs:
        m=o.matrix_world.copy();o.parent=ROOT;o.matrix_world=m
bpy.context.view_layer.update();points=_vertices_world(COL);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);radius=max((v-center).length for v in points);scale=2*radius*1.09
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral_world');world.use_nodes=True;scene.world=world
ns=world.node_tree.nodes;ls=world.node_tree.links;ns['Background'].inputs['Color'].default_value=(.75,.75,.75,1);ns['Background'].inputs['Strength'].default_value=.3
cam_bg=ns.new('ShaderNodeBackground');cam_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cam_bg.inputs['Strength'].default_value=1
path=ns.new('ShaderNodeLightPath');mix=ns.new('ShaderNodeMixShader');ls.new(path.outputs['Is Camera Ray'],mix.inputs[0]);ls.new(ns['Background'].outputs[0],mix.inputs[1]);ls.new(cam_bg.outputs[0],mix.inputs[2]);ls.new(mix.outputs[0],ns['World Output'].inputs['Surface'])
lights=[]
for name,vec,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=energy*(2*radius)**2/4;d.shape='DISK';d.size=size*radius;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(vec)*radius;_look_at(o,center);lights.append({'name':name,'direction':vec,'energy':d.energy,'size':d.size})
c=bpy.data.cameras.new('Canonical_camera');c.type='ORTHO';c.ortho_scale=scale;c.clip_start=.001;c.clip_end=radius*40;camera=bpy.data.objects.new('Canonical_camera',c);scene.collection.objects.link(camera);scene.camera=camera
if a.clay:scene.view_layers[0].material_override=make_material('Clay','#969696')
dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'renderer_sha256':sha(__file__),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'audit_helper_sha256':sha(Path(__file__).with_name('qa_glb.py')),'glb_sha256':source_hash,'resolution':a.resolution,'samples':a.samples,'threads':2,'clay':a.clay,'camera_type':'ORTHO','ortho_scale':scale,'target_blender_m':list(center),'directions':dirs,'background':'#E8E4DC','color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'lights':lights,'source_bounds_blender_m':{'min':list(low),'max':list(high)}}
(a.output_dir/'render-config.json').write_text(json.dumps(config,indent=2)+'\n');frames=[]
for name,direction in dirs.items():
    camera.location=center+Vector(direction).normalized()*radius*6;_look_at(camera,center)
    if name=='top':camera.rotation_euler=(0,0,0)
    scene.render.filepath=str((a.output_dir/(name+'.png')).resolve());start=time.monotonic();bpy.ops.render.render(write_still=True);fp=a.output_dir/(name+'.png')
    frames.append({'view':name,'path':name+'.png','sha256':sha(fp),'bytes':fp.stat().st_size,'width':a.resolution,'height':a.resolution,'camera_direction_blender':list(direction),'wall_seconds':round(time.monotonic()-start,3)})
if sha(a.glb)!=source_hash:raise RuntimeError('GLB changed')
manifest={'source_glb_sha256':source_hash,'config_path':'render-config.json','config_sha256':sha(a.output_dir/'render-config.json'),'frames':frames,'source_unchanged':True,'visual_review':'PENDING','gpu':'UNKNOWN'}
(a.output_dir/'render-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('RENDER_COMPLETE',source_hash)
