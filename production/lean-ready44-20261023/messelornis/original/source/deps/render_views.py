# SPDX-License-Identifier: MIT
"""Four consistent orthographic images from fresh exact-GLB import. No GPU claim."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--samples',type=int,default=48);ap.add_argument('--resolution',type=int,default=512);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
    if list(a.out.iterdir()):raise RuntimeError('Refuse to overwrite previous render evidence')
    h=sha(a.glb);c=setup_scene('messelornis-export-view');root=bpy.data.objects[c['asset_root']];before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));imported=[o for o in bpy.data.objects if o not in before]
    for o in imported:link_object(o,c,parent=False)
    for o in imported:
        if o.parent not in imported:m=o.matrix_world.copy();o.parent=root;o.matrix_world=m
    bpy.context.view_layer.update();points=_vertices_world(c);lo,hi=_bounds(points);target=Vector([(lo[i]+hi[i])/2 for i in range(3)]);radius=max((p-target).length for p in points);scale=2*radius*1.10
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=a.samples;sc.cycles.use_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=2
    sc.render.resolution_x=sc.render.resolution_y=a.resolution;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False;sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;n=world.node_tree.nodes;l=world.node_tree.links;env=n['Background'];env.inputs['Color'].default_value=(.75,.75,.75,1);env.inputs['Strength'].default_value=.35
    bg=n.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1;lp=n.new('ShaderNodeLightPath');mix=n.new('ShaderNodeMixShader');l.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);l.new(env.outputs[0],mix.inputs[1]);l.new(bg.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n['World Output'].inputs['Surface']);sc.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*radius**2;d.shape='DISK';d.size=size*radius;o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=target+Vector(direction)*radius;_look_at(o,target);lights.append({'name':name,'direction':direction,'energy':d.energy,'size':d.size})
    d=bpy.data.cameras.new('view-camera');cam=bpy.data.objects.new('view-camera',d);sc.collection.objects.link(cam);sc.camera=cam;d.type='ORTHO';d.ortho_scale=scale;d.clip_start=.0001;d.clip_end=10
    if a.clay:bpy.context.view_layer.material_override=make_material('diagnostic-clay','#929292')
    dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'denoising':False,'render_threads':2,'camera_type':'ORTHO','ortho_scale_m':scale,'target_blender_m':list(target),'camera_directions':dirs,'lighting':lights,'background_srgb':'#E8E4DC','transparent':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'clay_override':a.clay,'source_glb_sha256':h,'renderer_sha256':sha(__file__),'asset_common_sha256':sha(Path(__file__).with_name('asset_common.py')),'web_presentation_contract':False};save(a.out/'render-config.json',config);frames=[]
    for name,direction in dirs.items():
        cam.location=target+Vector(direction).normalized()*radius*6;_look_at(cam,target);sc.render.filepath=str(a.out/(name+'.png'));bpy.ops.render.render(write_still=True);frames.append({'path':name+'.png','sha256':sha(a.out/(name+'.png')),'glb_sha256':h,'width':a.resolution,'height':a.resolution,'camera_direction_blender':direction})
    assert sha(a.glb)==h
    save(a.out/'render-manifest.json',{'glb_sha256':h,'config_sha256':sha(a.out/'render-config.json'),'source_unchanged':True,'method':'Clean Blender scene, fresh import of the exact exported GLB.','frames':frames,'scope':'Shape and color pixels from CPU renderer only, not WebGL or GPU or composed-scene proof.'})
if __name__=='__main__':main()
