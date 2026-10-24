# SPDX-License-Identifier: MIT
"""Reproduce orthographic evidence from a clean import of model.glb, never the source scene."""
from pathlib import Path
import argparse,hashlib,json,math,sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from asset_common import make_material,_look_at,_vertices_world,_bounds,srgb_to_linear

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',required=True);ap.add_argument('--output',required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--resolution',type=int,default=1024);ap.add_argument('--samples',type=int,default=40);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);model=Path(a.model).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(model));scene=bpy.context.scene
    imported=list(scene.objects);col=bpy.data.collections.new('IMPORTED_EXACT_GLB');scene.collection.children.link(col)
    for o in imported:
        for c in list(o.users_collection):c.objects.unlink(o)
        col.objects.link(o)
    points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3));scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('evidence-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
    camdata=bpy.data.cameras.new('evidence-camera');cam=bpy.data.objects.new('evidence-camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=30*span
    if a.clay:bpy.context.view_layer.material_override=make_material('evidence-clay','#929292',.85)
    views={};directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    for name,di in directions.items():
        cam.location=center+Vector(di).normalized()*span*4;_look_at(cam,center)
        if name=='top':cam.rotation_euler[2]+=math.pi
        bpy.context.view_layer.update();iv=cam.matrix_world.inverted();ps=[iv@p for p in points];xmin,xmax=min(p.x for p in ps),max(p.x for p in ps);ymin,ymax=min(p.y for p in ps),max(p.y for p in ps)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));camdata.ortho_scale=max(xmax-xmin,ymax-ymin)*1.16
        scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        views[name]={'direction':list(di),'location_m':list(cam.location),'rotation_euler_rad':list(cam.rotation_euler),'orthographic_scale_m':camdata.ortho_scale,'sha256':hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest()}
    config={'engine':'Cycles CPU','blender':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'clay_override':a.clay,'key':{'direction':[-3,-4,6],'energy_scaled':450,'size_scaled':4},'fill':{'direction':[4,-1,3],'energy_scaled':150,'size_scaled':5},'world_strength':.3,'framing':'Full exact-export geometry with 16 percent margin; canonical axes.','views':views}
    receipt={'status':'COMPLETE','scope':'Exact GLB Blender evidence, not GPU/Three.js verification.','glb_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'configuration':config,'configuration_sha256':hashlib.sha256(json.dumps(config,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
    (out/'render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
