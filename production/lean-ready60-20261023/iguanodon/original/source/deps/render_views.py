#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Four actual-GLB views with canonical CPU preview lights and explicit axes.
Blender arguments after --: --root DIR --mode clay|final.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--mode',choices=['clay','final'],required=True)
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);root=args.root.resolve();glb=root/'model.glb';digest=sha(glb)
    params=json.loads((root/'source/params.json').read_text());resolution=384 if args.mode=='clay' else params['render']['resolution'];samples=8 if args.mode=='clay' else params['render']['samples']
    out=root/'private/clay' if args.mode=='clay' else root/'views';out.mkdir(parents=True,exist_ok=True)
    col=setup_scene('iguanodon-preview');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(glb));objects=[o for o in bpy.data.objects if o not in before]
    for o in objects:link_object(o,col,parent=False)
    pts=_vertices_world(col);low,high=_bounds(pts);center=Vector([(a+b)/2 for a,b in zip(low,high)]);span=max(b-a for a,b in zip(low,high))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-preview-world');world.use_nodes=True;scene.world=world
    bg=world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    camera_bg=world.node_tree.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
    lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');links=world.node_tree.links
    links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(camera_bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface'])
    lighting=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
        lighting.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
    camera_data=bpy.data.cameras.new('preview-camera');camera=bpy.data.objects.new('preview-camera',camera_data);scene.collection.objects.link(camera);scene.camera=camera;camera_data.type='ORTHO';camera_data.clip_start=.001;camera_data.clip_end=span*30
    if args.mode=='clay':
        clay=make_material('neutral-clay','#929292',roughness=.85);bpy.context.view_layer.material_override=clay
    report={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','glb_sha256':digest,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'gpu_used':False,'resolution':[resolution,resolution],'samples':samples,'denoising':False,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'background_srgb':'#E8E4DC','transparent':False,'lights':lighting,'renderer_sha256':sha(Path(__file__)),'canonical_helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'imported_bounds_blender_m':{'min':low,'max':high},'views':{},'website_contract_claim':False}
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        direction=Vector(direction).normalized();camera.location=center+direction*span*4;_look_at(camera,center);bpy.context.view_layer.update();inverse=camera.matrix_world.inverted();projected=[inverse@p for p in pts]
        xmin=min(p.x for p in projected);xmax=max(p.x for p in projected);ymin=min(p.y for p in projected);ymax=max(p.y for p in projected)
        camera.location+=camera.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));camera_data.ortho_scale=max(xmax-xmin,ymax-ymin)*1.16
        path=out/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        report['views'][name]={'path':('private/clay/' if args.mode=='clay' else 'views/')+name+'.png','sha256':sha(path),'direction_blender':list(direction),'camera_type':'ORTHO','ortho_scale':camera_data.ortho_scale,'camera_location_blender_m':list(camera.location)}
    if args.mode=='final':
        (root/'preview.png').write_bytes((out/'perspective.png').read_bytes());report['preview_reuses_perspective']=True
    assert sha(glb)==digest
    report_path=(root/'private/clay/render.json') if args.mode=='clay' else (root/'qa/evidence/actual-glb-views.json')
    report_path.write_text(json.dumps(report,indent=2)+'\n');print('FOUR_VIEWS_DONE',args.mode,digest)
if __name__=='__main__':main()
