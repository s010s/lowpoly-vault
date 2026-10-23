# SPDX-License-Identifier: MIT
"""Four actual-GLB orthographic views. CPU rendering does not establish GPU support."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def main():
    argv=sys.argv[sys.argv.index('--')+1:]
    ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--samples',type=int,default=48);ap.add_argument('--resolution',type=int,default=512);a=ap.parse_args(argv)
    a.out.mkdir(parents=True,exist_ok=True)
    if list(a.out.iterdir()):raise RuntimeError('Output must be empty')
    glb_hash=sha(a.glb);c=setup_scene('vegavis-view');root=bpy.data.objects[c['asset_root']]
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    imported=[o for o in bpy.data.objects if o not in before]
    for o in imported:link_object(o,c,parent=False)
    for o in imported:
        if o.parent not in imported:
            m=o.matrix_world.copy();o.parent=root;o.matrix_world=m
    bpy.context.view_layer.update();points=_vertices_world(c);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)])
    radius=max((p-center).length for p in points);scale=2*radius*1.10
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True
    nodes=world.node_tree.nodes;links=world.node_tree.links
    env=nodes['Background'];env.inputs['Color'].default_value=(.75,.75,.75,1);env.inputs['Strength'].default_value=.35
    bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(x/255) for x in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
    lightpath=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lightpath.outputs['Is Camera Ray'],mix.inputs[0]);links.new(env.outputs[0],mix.inputs[1]);links.new(bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface']);scene.world=world
    lighting=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*radius**2;d.shape='DISK';d.size=size*radius
        o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center)
        lighting.append({'name':name,'direction':direction,'energy':d.energy,'size':d.size})
    d=bpy.data.cameras.new('camera');o=bpy.data.objects.new('camera',d);scene.collection.objects.link(o);d.type='ORTHO';d.ortho_scale=scale;d.clip_start=.0001;d.clip_end=10;scene.camera=o
    if a.clay:bpy.context.view_layer.material_override=make_material('diagnostic-clay','#929292')
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'denoising':False,'render_threads':2,'camera_type':'ORTHO','ortho_scale_m':scale,'target_blender_m':list(center),'camera_directions':directions,'lighting':lighting,'background_srgb':'#E8E4DC','transparent':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'clay_override':a.clay,'source_glb_sha256':glb_hash,'renderer_sha256':sha(__file__),'asset_common_sha256':sha(Path(__file__).with_name('asset_common.py')),'web_presentation_contract':False}
    write(a.out/'render-config.json',config);frames=[]
    for name,direction in directions.items():
        o.location=center+Vector(direction).normalized()*radius*6;_look_at(o,center)
        scene.render.filepath=str(a.out/(name+'.png'));bpy.ops.render.render(write_still=True)
        frames.append({'path':name+'.png','sha256':sha(a.out/(name+'.png')),'glb_sha256':glb_hash,'width':a.resolution,'height':a.resolution,'camera_direction_blender':direction})
    assert sha(a.glb)==glb_hash
    write(a.out/'render-manifest.json',{'glb_sha256':glb_hash,'config_sha256':sha(a.out/'render-config.json'),'source_unchanged':True,'method':'Fresh clean Blender import of exact exported GLB; no source-scene geometry used.','frames':frames,'scope':'Four shape/color images only. CPU rendering is not GPU, WebGL or composed-scene evidence.'})
if __name__=='__main__':main()
