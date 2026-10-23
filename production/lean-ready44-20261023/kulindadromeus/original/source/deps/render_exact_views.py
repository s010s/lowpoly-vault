#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Clean-import exact delivered GLB views, canonical axes and fixed framing.
Uses the pinned common helper's scene/material/color and camera utilities.
This records Cycles CPU evidence only, never target-runtime GPU acceptance.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,_vertices_world,_bounds,_look_at,srgb_to_linear

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def main():
    pa=argparse.ArgumentParser();pa.add_argument('glb',type=Path);pa.add_argument('--out',type=Path,required=True);pa.add_argument('--resolution',type=int,default=768);pa.add_argument('--samples',type=int,default=48);a=pa.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.out;out.mkdir(parents=True,exist_ok=True)
    ghash=sha(a.glb);c=setup_scene('kulindadromeus-exact-view');root=bpy.data.objects[c['asset_root']];before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));objs=[o for o in bpy.data.objects if o not in before]
    for o in objs:link_object(o,c,parent=False)
    for o in objs:
        if o.parent not in objs:o.parent=root
    bpy.context.view_layer.update();ps=_vertices_world(c);lo,hi=_bounds(ps);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);radius=max((p-center).length for p in ps);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral_studio');world.use_nodes=True;nt=world.node_tree;bg=nt.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3;cb=nt.nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(x/255) for x in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1;lp=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(bg.outputs[0],mix.inputs[1]);nt.links.new(cb.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes['World Output'].inputs['Surface']);s.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*radius**2;data.shape='DISK';data.size=size*radius;ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=center+Vector(direction)*radius;_look_at(ob,center);lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
    data=bpy.data.cameras.new('Exact_glb_camera');cam=bpy.data.objects.new('Exact_glb_camera',data);s.collection.objects.link(cam);s.camera=cam;data.type='ORTHO';data.ortho_scale=radius*2.22;data.clip_start=.0001;data.clip_end=radius*40
    dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    config={'source_glb_sha256':ghash,'renderer_sha256':sha(__file__),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,'background_srgb':'#E8E4DC','transparent':False,'denoising':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'camera_type':'ORTHO','orthographic_scale':data.ortho_scale,'target_blender_m':list(center),'fixed_framing':True,'directions_blender':dirs,'lights':lights,'gpu_claim':'UNKNOWN'};write(out/'render-config.json',config);frames=[]
    for name,d in dirs.items():
        cam.location=center+Vector(d).normalized()*radius*6;_look_at(cam,center);s.render.filepath=str((out/(name+'.png')).resolve());t=time.monotonic();bpy.ops.render.render(write_still=True);frames.append({'view':name,'path':'views/'+name+'.png','sha256':sha(out/(name+'.png')),'direction_blender':d,'seconds':round(time.monotonic()-t,3)})
    assert sha(a.glb)==ghash
    write(out/'render-manifest.json',{'kind':'exact-GLB-four-views','source_glb_sha256':ghash,'render_config_sha256':sha(out/'render-config.json'),'source_unchanged':True,'frames':frames,'preview_reuses':'views/perspective.png','independent_visual_review':'PENDING','gpu':'UNKNOWN'})
if __name__=='__main__':main()
