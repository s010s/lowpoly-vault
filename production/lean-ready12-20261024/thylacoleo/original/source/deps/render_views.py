# SPDX-License-Identifier: MIT
"""Render only the declared exact-export views, using canonical palette and lighting helpers."""
import argparse,hashlib,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at
A=argparse.ArgumentParser();A.add_argument('glb',type=Path);A.add_argument('--output',type=Path,required=True);A.add_argument('--gray',action='store_true');A.add_argument('--samples',type=int,default=48);A.add_argument('--views',default='front,side,top,perspective')
a=A.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=sha(a.glb)
col=setup_scene('export-view');root=bpy.data.objects[col['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb));obs=[o for o in bpy.data.objects if o not in before]
for o in obs:link_object(o,col,parent=False)
pts=_vertices_world(col);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)])
span=max(hi[i]-lo[i] for i in range(3));scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*span**2/4;d.shape='DISK';d.size=size*span/2
 o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
d=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30
if a.gray:bpy.context.view_layer.material_override=make_material('Gray_check','#929292',.85)
frames=[]
directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
for name in a.views.split(','):
 direction=Vector(directions[name]).normalized();cam.location=center+direction*span*3;_look_at(cam,center);bpy.context.view_layer.update()
 inv=cam.matrix_world.inverted();p2=[inv@p for p in pts];xs=[p.x for p in p2];ys=[p.y for p in p2]
 d.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.18
 # Center each canonical projection to its projected bounds without changing direction.
 right=cam.matrix_world.to_quaternion()@Vector((1,0,0));up=cam.matrix_world.to_quaternion()@Vector((0,1,0))
 shift=right*((max(xs)+min(xs))/2)+up*((max(ys)+min(ys))/2);cam.location+=shift
 target=center+shift
 path=a.output/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
 frames.append({'view':name,'path':name+'.png','sha256':sha(path),'direction_blender':list(directions[name]),'target_blender_m':list(target),'orthographic_scale_m':d.ortho_scale,'width':512,'height':512})
assert sha(a.glb)==h
r={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','source_glb_sha256':h,'renderer':'Blender 4.3.2 Cycles CPU','renderer_sha256':sha(Path(__file__)),'canonical_helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'transparent':True,'samples':a.samples,'threads':2,'gray_override':a.gray,'frames':frames,'source_unchanged':True,'gpu_claim':'NOT_TESTED'}
(a.output/'render-report.json').write_text(json.dumps(r,indent=2)+'\n')
