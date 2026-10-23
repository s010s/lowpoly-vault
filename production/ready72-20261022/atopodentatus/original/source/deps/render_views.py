# SPDX-License-Identifier: MIT
"""Original four-view exact-GLB adapter, canonical asset_common lighting/color utilities."""
import argparse,hashlib,json,math,sys,time
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=1024);p.add_argument('--samples',type=int,default=32)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sha=hashfile(a.glb);col=setup_scene('export-preview');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb));imported=[o for o in bpy.data.objects if o not in before]
for o in imported:link_object(o,col,parent=False)
pts=_vertices_world(col);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
world=bpy.data.worlds.new('studio');world.use_nodes=True;nodes=world.node_tree.nodes
nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);nodes['Background'].inputs['Strength'].default_value=.3
bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(nodes['Background'].outputs[0],mix.inputs[1]);world.node_tree.links.new(bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],nodes['World Output'].inputs[0]);s.world=world
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
 ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
camd=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',camd);s.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=span*30;s.camera=cam
if a.gray:bpy.context.view_layer.material_override=make_material('gray-diagnostic','#97978C',roughness=.9)
frames=[]
for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
 direction=Vector(direction).normalized();cam.location=center+direction*span*4;_look_at(cam,center);bpy.context.view_layer.update()
 inv=cam.matrix_world.inverted();projected=[inv@pt for pt in pts];width=max(pt.x for pt in projected)-min(pt.x for pt in projected);height=max(pt.y for pt in projected)-min(pt.y for pt in projected)
 camd.ortho_scale=max(width,height)*1.13
 # Projected midpoint framing keeps a small non-symmetric tail tip in frame.
 offset=Vector(((max(pt.x for pt in projected)+min(pt.x for pt in projected))/2,(max(pt.y for pt in projected)+min(pt.y for pt in projected))/2,0));cam.location+=cam.rotation_euler.to_matrix()@offset
 path=a.out/(name+'.png');s.render.filepath=str(path);start=time.monotonic();bpy.ops.render.render(write_still=True)
 frames.append({'view':name,'direction_blender':list(direction),'camera_position':list(cam.location),'ortho_scale_m':camd.ortho_scale,'sha256':hashfile(path),'path':name+'.png','seconds':round(time.monotonic()-start,3)})
assert hashfile(a.glb)==sha
(a.out/'render-manifest.json').write_text(json.dumps({'source_glb_sha256':sha,'exact_export_import':True,'renderer':'Blender Cycles CPU','blender':bpy.app.version_string,'gray':a.gray,'samples':a.samples,'resolution':a.resolution,'threads':2,'background':'#E8E4DC','view_transform':'Standard','look':'None','exposure':0,'gamma':1,'source_unchanged':True,'generator_sha256':hashfile(Path(__file__)),'frames':frames},indent=2)+'\n')
