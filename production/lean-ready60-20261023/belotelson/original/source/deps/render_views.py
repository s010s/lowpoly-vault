# SPDX-License-Identifier: MIT
"""Minimal exact-export four-view renderer; no website-image contract is claimed."""
from pathlib import Path
import sys,argparse,json,hashlib,math
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear
ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--resolution',type=int,default=640);ap.add_argument('--samples',type=int,default=48)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();before_hash=sha(a.glb)
col=setup_scene('exact-export-render');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb))
for obj in set(bpy.data.objects)-before:link_object(obj,col,parent=False)
points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3));radius=max((v-center).length for v in points)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=not a.clay
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
world=bpy.data.worlds.new('neutral_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.7,.7,.7,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;s.world=world
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5),('rim',(1,4,4),190,3)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy*(2*radius)**2/4;data.shape='DISK';data.size=size*radius;obj=bpy.data.objects.new(name,data);s.collection.objects.link(obj);obj.location=center+Vector(direction)*radius;_look_at(obj,center);lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
cd=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',cd);s.collection.objects.link(cam);cd.type='ORTHO';cd.ortho_scale=span*1.14;cd.clip_start=.00001;cd.clip_end=10;s.camera=cam
if a.clay:bpy.context.view_layer.material_override=make_material('clay','#909090')
views={'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)} if a.clay else {'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
frames=[]
for name,d in views.items():
    cam.location=center+Vector(d).normalized()*radius*6;_look_at(cam,center);s.render.filepath=str(a.out/(name+'.png'));bpy.ops.render.render(write_still=True);frames.append({'view':name,'direction_blender':list(d),'path':name+'.png','sha256':sha(a.out/(name+'.png'))})
assert sha(a.glb)==before_hash
report={'source':'clean-import-of-final-GLB','source_glb_sha256':before_hash,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'renderer_sha256':sha(__file__),'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,'transparent':not a.clay,'clay':a.clay,'camera_type':'ORTHO','ortho_scale':cd.ortho_scale,'target_blender_m':list(center),'directions':views,'lights':lights,'view_transform':'Standard','look':'None','source_unchanged':True,'frames':frames,'claim':'CPU exact-export structural evidence; not browser GPU, scene performance or website contract evidence.'}
(a.out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
