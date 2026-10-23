# SPDX-License-Identifier: MIT
"""Four-axis review renders imported from the exact standalone GLB.
This Blender CPU renderer is evidence generation, not Three.js GPU acceptance.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
argv=sys.argv[sys.argv.index('--')+1:]
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=512);p.add_argument('--samples',type=int,default=32)
a=p.parse_args(argv);a.output_dir.mkdir(parents=True,exist_ok=True)
h=sha(a.glb);C=setup_scene('morganucodon-render',664);root=bpy.data.objects[C['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb));added=[o for o in bpy.data.objects if o not in before]
for o in added:link_object(o,C,parent=False)
for o in added:
 if o.parent not in added:
  world=o.matrix_world.copy();o.parent=root;o.matrix_world=world
bpy.context.view_layer.update();pts=_vertices_world(C);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);r=max((p-center).length for p in pts)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=a.samples;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=sc.render.resolution_y=a.resolution;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False
sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
world=bpy.data.worlds.new('studio-world');world.use_nodes=True;bg=world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
camera_bg=world.node_tree.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(bg.outputs[0],mix.inputs[1]);world.node_tree.links.new(camera_bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']);sc.world=world
for name,d,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*(2*r)**2/4;data.shape='DISK';data.size=size*r;ob=bpy.data.objects.new(name,data);sc.collection.objects.link(ob);ob.location=center+Vector(d)*r;_look_at(ob,center)
cam_data=bpy.data.cameras.new('review-camera');cam=bpy.data.objects.new('review-camera',cam_data);sc.collection.objects.link(cam);cam_data.type='ORTHO';cam_data.clip_start=.0001;cam_data.clip_end=r*50;sc.camera=cam
if a.clay:sc.view_layers[0].material_override=make_material('clay-review','#929292')
frames=[]
for name,d in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
 direction=Vector(d).normalized();cam.location=center+direction*r*6;_look_at(cam,center)
 if name=='top':cam.rotation_euler.rotate_axis('Z',math.pi)
 bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@v for v in pts];width=max(v.x for v in proj)-min(v.x for v in proj);height=max(v.y for v in proj)-min(v.y for v in proj)
 cam_data.ortho_scale=max(width,height)*1.18
 dest=a.output_dir/(name+'.png');sc.render.filepath=str(dest);bpy.ops.render.render(write_still=True)
 frames.append({'view':name,'path':name+'.png','sha256':sha(dest),'camera_direction_blender':list(d),'ortho_scale_m':cam_data.ortho_scale,'width':a.resolution,'height':a.resolution})
assert sha(a.glb)==h
report={'status':'RENDERED_PENDING_VISUAL_REVIEW','source_glb_sha256':h,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'samples':a.samples,'clay':a.clay,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background':'#E8E4DC','bounds_blender_m':{'min':lo,'max':hi},'framing':'Each orthographic diagnostic fits all actual GLB vertices with 18 percent margin; front is not a substitute perspective.','renderer_sha256':sha(__file__),'frames':frames,'gpu_rendering':'UNKNOWN','scene_performance':'UNKNOWN'}
(a.output_dir/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
