#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Four bounded canonical images. Clean import of an exact GLB, not source geometry.
Gray mode is cheap authoring evidence, final mode is hash-bound Cycles CPU evidence.
"""
import argparse,hashlib,json,math,sys,time
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_look_at,_vertices_world,_bounds

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    a=argparse.ArgumentParser(); a.add_argument('glb',type=Path);a.add_argument('--out',type=Path,required=True);a.add_argument('--gray',action='store_true');a.add_argument('--resolution',type=int,default=640);a.add_argument('--samples',type=int,default=48)
    args=a.parse_args(sys.argv[sys.argv.index('--')+1:]); args.out.mkdir(parents=True,exist_ok=True)
    h=sha(args.glb); C=setup_scene('evidence-stage'); before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(args.glb.resolve()))
    for o in set(bpy.data.objects)-before:link_object(o,C,parent=False)
    points=_vertices_world(C);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);radius=max((p-center).length for p in points)
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=args.samples;sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=sc.render.resolution_y=args.resolution;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-light');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;sc.world=world
    lights=[]
    for name,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),200,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power*radius**2;d.shape='DISK';d.size=size*radius;o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center);lights.append({'name':name,'direction':direction,'power':d.energy,'size':d.size})
    camdata=bpy.data.cameras.new('evidence-camera');cam=bpy.data.objects.new('evidence-camera',camdata);sc.collection.objects.link(cam);sc.camera=cam;camdata.type='ORTHO';camdata.ortho_scale=2*radius*1.1;camdata.clip_start=.01;camdata.clip_end=100
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if args.gray:
        sc.cycles.samples=8;sc.render.resolution_x=sc.render.resolution_y=360
        clay=make_material('diagnostic-clay','#919191',roughness=.9);bpy.context.view_layer.material_override=clay
        directions={k:directions[k] for k in ['front','side','perspective']}
    config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'source_glb_sha256':h,'renderer_sha256':sha(__file__),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'camera':'ORTHOGRAPHIC','target_blender_m':list(center),'ortho_scale':camdata.ortho_scale,'directions':directions,'resolution':[sc.render.resolution_x,sc.render.resolution_y],'samples':sc.cycles.samples,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'transparent':True,'world_strength':.45,'lights':lights,'kind':'gray-authoring-diagnostic' if args.gray else 'exact-GLB-final-views','website_compatible':False}
    (args.out/'render-config.json').write_text(json.dumps(config,indent=2)+'\n'); frames=[]
    for name,direction in directions.items():
        cam.location=center+Vector(direction).normalized()*radius*7;_look_at(cam,center);sc.render.filepath=str((args.out/(name+'.png')).resolve());start=time.monotonic();bpy.ops.render.render(write_still=True)
        frames.append({'view':name,'path':name+'.png','sha256':sha(args.out/(name+'.png')),'seconds':round(time.monotonic()-start,3),'camera_position_blender_m':list(cam.location),'direction':list(direction)})
    assert sha(args.glb)==h
    (args.out/'render-manifest.json').write_text(json.dumps({'source_glb_sha256':h,'config_sha256':sha(args.out/'render-config.json'),'frames':frames,'scope':config['kind'],'source_unchanged':True,'visual_acceptance':'PENDING_INDEPENDENT_REVIEW'},indent=2)+'\n')
if __name__=='__main__':main()
