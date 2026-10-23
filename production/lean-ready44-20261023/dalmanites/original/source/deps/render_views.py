# SPDX-License-Identifier: MIT
"""Render a clean import of the exact GLB, with hash-bound fixed-view evidence."""
import bpy, sys, json, math, hashlib, argparse
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene, link_object, make_material, srgb_to_linear, _vertices_world, _bounds, _look_at

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    a=argparse.ArgumentParser();a.add_argument('glb',type=Path);a.add_argument('--output',type=Path,required=True);a.add_argument('--resolution',type=int,default=768);a.add_argument('--samples',type=int,default=48);a.add_argument('--clay',action='store_true');a.add_argument('--views',default='front,side,top,perspective');args=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    args.output.mkdir(parents=True,exist_ok=True);assert not any(args.output.iterdir())
    c=setup_scene('dalmanites-preview');root=bpy.data.objects[c['asset_root']]
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(args.glb.resolve()));imported=[o for o in bpy.data.objects if o not in before]
    for o in imported:link_object(o,c,parent=False)
    for o in imported:
        if o.parent not in imported:
            m=o.matrix_world.copy();o.parent=root;o.matrix_world=m
    bpy.context.view_layer.update();points=_vertices_world(c);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);radius=max((p-center).length for p in points);scale=radius*2*1.12
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=args.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=scene.render.resolution_y=args.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    w=bpy.data.worlds.new('neutral_world');w.use_nodes=True;scene.world=w;nodes=w.node_tree.nodes;links=w.node_tree.links;bg=nodes.get('Background');bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    camera_bg=nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
    lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(camera_bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes.get('World Output').inputs['Surface'])
    lights=[]
    for name,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power*(2*radius)**2/4;d.shape='DISK';d.size=size*radius;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center);lights.append({'name':name,'direction':direction,'energy':d.energy,'size_m':d.size})
    d=bpy.data.cameras.new('evidence_camera');o=bpy.data.objects.new('evidence_camera',d);scene.collection.objects.link(o);d.type='ORTHO';d.ortho_scale=scale;d.clip_start=.00001;d.clip_end=10;scene.camera=o
    if args.clay:scene.view_layers[0].material_override=make_material('clay','#929292')
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1),'bottom':(0,0,-1)}
    cfg={'glb_sha256':digest(args.glb),'renderer_sha256':digest(__file__),'helper_sha256':digest(Path(__file__).with_name('asset_common.py')),'engine':'Blender Cycles CPU','version':bpy.app.version_string,'resolution':[args.resolution,args.resolution],'samples':args.samples,'threads':2,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background':'#E8E4DC','transparent':False,'camera_type':'ORTHO','fixed_target_m':list(center),'fixed_orthographic_scale_m':scale,'lights':lights,'source_bounds_blender_m':{'min':low,'max':high},'clay_override':args.clay,'frames':[]}
    for view in args.views.split(','):
        direction=Vector(directions[view]).normalized();o.location=center+direction*radius*6;_look_at(o,center);target=args.output/(view+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True)
        cfg['frames'].append({'view':view,'camera_direction_blender':directions[view],'file':view+'.png','sha256':digest(target)})
    (args.output/'render-manifest.json').write_text(json.dumps(cfg,indent=2)+'\n')
if __name__=='__main__':main()
