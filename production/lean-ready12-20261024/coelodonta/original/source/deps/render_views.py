# SPDX-License-Identifier: MIT
"""Render the exact supplied GLB, not the authoring scene. CPU, two threads."""
from pathlib import Path
import sys,json,math,hashlib,argparse
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear
A=argparse.ArgumentParser();A.add_argument('glb',type=Path);A.add_argument('--out',type=Path,required=True);A.add_argument('--gray',action='store_true');A.add_argument('--resolution',type=int,default=640);A.add_argument('--samples',type=int,default=48)
a=A.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
subject=h(a.glb)
c=setup_scene('exact-export-view');root=bpy.data.objects[c['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
objects=[o for o in bpy.data.objects if o not in before]
for o in objects:link_object(o,c,parent=False)
for o in objects:
 if o.parent not in objects:
  m=o.matrix_world.copy();o.parent=root;o.matrix_world=m
bpy.context.view_layer.update();points=_vertices_world(c);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)])
radius=max((v-center).length for v in points)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False
s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.36
nodes=world.node_tree.nodes;links=world.node_tree.links
bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(nodes['Background'].outputs[0],mix.inputs[1]);links.new(bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface']);s.world=world
lighting=[]
for name,d,e,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=e*radius*radius;data.shape='DISK';data.size=size*radius;o=bpy.data.objects.new(name,data);s.collection.objects.link(o);o.location=center+Vector(d)*radius;_look_at(o,center);lighting.append({'name':name,'direction':d,'energy':data.energy,'size':data.size})
data=bpy.data.cameras.new('Evidence-camera');cam=bpy.data.objects.new('Evidence-camera',data);s.collection.objects.link(cam);data.type='ORTHO';data.clip_start=.001;data.clip_end=100;s.camera=cam
if a.gray:bpy.context.view_layer.material_override=make_material('Gray-inspection','#969696')
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
if a.gray:views={k:views[k] for k in ['front','side','perspective']}
frames=[]
for name,d in views.items():
 direction=Vector(d).normalized();cam.location=center+direction*radius*6;_look_at(cam,center)
 # Stable common enclosing field, four directions exactly as frozen in brief.
 data.ortho_scale=2*radius*1.10
 s.render.filepath=str((a.out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
 frames.append({'name':name,'path':name+'.png','sha256':h(a.out/(name+'.png')),'camera_direction_blender':d,'camera_type':'ORTHO','ortho_scale_m':data.ortho_scale,'target_blender_m':list(center)})
assert h(a.glb)==subject
report={'schema_version':1,'source_glb_sha256':subject,'source_unchanged':True,'exact_glb_import':True,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'renderer_script_sha256':h(Path(__file__)),'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,'denoising':False,'gray_override':a.gray,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'lighting':lighting,'background_srgb':'#E8E4DC','bounds_blender_m':{'min':low,'max':high},'frames':frames,'scope':'Exact-export structural evidence, not Three.js GPU, populated scene, independent acceptance or publication.'}
(a.out/'render-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
