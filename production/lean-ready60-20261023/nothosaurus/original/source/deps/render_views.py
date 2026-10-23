# SPDX-License-Identifier: MIT
"""Four-camera exact-GLB inspection, Cycles CPU. No GPU-performance claim."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at
p=argparse.ArgumentParser();p.add_argument('glb');p.add_argument('--output',required=True);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=1024);p.add_argument('--samples',type=int,default=40)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.glb);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
sourcehash=h(src);col=setup_scene('inspection');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(src))
for o in list(bpy.data.objects):
    if o not in before:link_object(o,col,parent=False)
bpy.context.view_layer.update();points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(x+y)/2 for x,y in zip(lo,hi)]);radius=max((p-center).length for p in points)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False
s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=a.resolution;s.render.resolution_y=a.resolution;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
world=bpy.data.worlds.new('Inspection_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs[1].default_value=.4;s.world=world
lighting=[]
for name,direc,energy,size in [('key',(-3,-4,6),600,4),('fill',(4,-1,3),230,5),('rim',(0,4,3),330,3)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy*radius*radius;data.shape='DISK';data.size=size*radius;o=bpy.data.objects.new(name,data);s.collection.objects.link(o);o.location=center+Vector(direc)*radius;_look_at(o,center);lighting.append({'name':name,'direction':direc,'energy':data.energy,'size':data.size})
camdata=bpy.data.cameras.new('Inspection_camera');cam=bpy.data.objects.new('Inspection_camera',camdata);s.collection.objects.link(cam);s.camera=cam;camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=100
if a.clay:s.view_layers[0].material_override=make_material('Inspection_gray','#A2A2A2')
frames=[]
for name,d in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
    cam.location=center+Vector(d).normalized()*radius*6;_look_at(cam,center);bpy.context.view_layer.update()
    inv=cam.matrix_world.inverted();q=[inv@v for v in points];xs=[v.x for v in q];ys=[v.y for v in q]
    camdata.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.12
    mid=(max(xs)+min(xs))/2,(max(ys)+min(ys))/2
    cam.location+=cam.matrix_world.to_3x3()@Vector((mid[0],mid[1],0))
    s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    frames.append({'path':name+'.png','sha256':h(out/(name+'.png')),'camera_direction_blender':d,'camera_location_blender_m':list(cam.location),'ortho_scale':camdata.ortho_scale,'resolution':[a.resolution,a.resolution]})
assert h(src)==sourcehash
report={'status':'RENDERED_PENDING_VISUAL_REVIEW','source_glb_sha256':sourcehash,'actual_clean_glb_import':True,'engine':'Cycles CPU','blender_version':bpy.app.version_string,'gpu':'UNKNOWN','samples':a.samples,'render_threads':2,'denoising':False,'clay_override':a.clay,'transparent':True,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'lighting':lighting,'renderer_sha256':h(__file__),'frames':frames,'framing':'Orthographic per-view projected geometry fit; full complete asset at every view. Not a fixed website renderer contract.'}
(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('RENDER_COMPLETE',sourcehash)
