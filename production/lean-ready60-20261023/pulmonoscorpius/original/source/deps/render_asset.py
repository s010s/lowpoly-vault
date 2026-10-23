# SPDX-License-Identifier: MIT
"""Four-view exact-export evidence. Reference CPU rendering, not a GPU test."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear

def main():
    a=sys.argv[sys.argv.index('--')+1:]; p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=32);args=p.parse_args(a)
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    col=setup_scene('preview-import'); original=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(args.glb)); imported=[o for o in bpy.data.objects if o not in original]
    for o in imported:link_object(o,col,parent=False)
    meshes=[o for o in imported if o.type=='MESH']
    if args.gray:
        clay=make_material('clay-check','#95938F',roughness=.9)
        for o in meshes:
            for i in range(len(o.data.materials)):o.data.materials[i]=clay
    points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);radius=max((v-center).length for v in points)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=args.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=args.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True
    bg=world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    cbg=world.node_tree.nodes.new('ShaderNodeBackground');cbg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cbg.inputs['Strength'].default_value=1
    lp=world.node_tree.nodes.new('ShaderNodeLightPath');mx=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mx.inputs[0]);world.node_tree.links.new(bg.outputs[0],mx.inputs[1]);world.node_tree.links.new(cbg.outputs[0],mx.inputs[2]);world.node_tree.links.new(mx.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']);scene.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*radius*radius;d.shape='DISK';d.size=size*radius;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center);lights.append({'direction':direction,'energy':d.energy,'size':d.size})
    camera_data=bpy.data.cameras.new('inspection');camera=bpy.data.objects.new('inspection',camera_data);scene.collection.objects.link(camera);scene.camera=camera;camera_data.type='ORTHO';camera_data.clip_start=.0001;camera_data.clip_end=radius*30
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if args.gray:directions={v:directions[v] for v in ['side','top','perspective']}
    receipt={'glb_sha256':hashlib.sha256(args.glb.read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'blender':'4.3.2','engine':'Cycles CPU','gpu_rendering_claim':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'threads':2,'samples':args.samples,'resolution':[args.resolution,args.resolution],'gray':args.gray,'lights':lights,'background_srgb':'#E8E4DC','source':'Clean import of model.glb, not saved source scene.','views':[]}
    for name,direction in directions.items():
        camera.location=center+Vector(direction).normalized()*radius*6;_look_at(camera,center);bpy.context.view_layer.update()
        inv=camera.matrix_world.inverted(); projected=[inv@v for v in points];w=max(v.x for v in projected)-min(v.x for v in projected);h=max(v.y for v in projected)-min(v.y for v in projected)
        camera_data.ortho_scale=2*max(max(abs(v.x),abs(v.y)) for v in projected)*1.14
        path=out/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        receipt['views'].append({'view':name,'camera_direction':direction,'target_m':list(center),'ortho_scale':camera_data.ortho_scale,'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (out/'render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
