# SPDX-License-Identifier: MIT
"""Four canonical exact-GLB images using the project's neutral Cycles CPU rig."""
import argparse, hashlib,json,math,sys,time
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--gray',action='store_true');ap.add_argument('--resolution',type=int,default=768);ap.add_argument('--samples',type=int,default=48);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    a.output.mkdir(parents=True,exist_ok=True);source_hash=digest(a.glb)
    col=setup_scene('exact-glb-view');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));imported=[o for o in bpy.data.objects if o not in before]
    for o in imported:link_object(o,col,parent=False)
    pts=_vertices_world(col);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);r=max((p-center).length for p in pts)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral_studio');world.use_nodes=True;nodes=world.node_tree.nodes;links=world.node_tree.links;bg=nodes.get('Background');bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    cam_bg=nodes.new('ShaderNodeBackground');cam_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cam_bg.inputs['Strength'].default_value=1
    lightpath=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lightpath.outputs['Is Camera Ray'],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(cam_bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes.get('World Output').inputs['Surface']);scene.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*(2*r)**2/4;data.shape='DISK';data.size=size*r;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(direction)*r;_look_at(o,center);lights.append({'direction':direction,'power':data.energy,'size':data.size})
    data=bpy.data.cameras.new('Canonical_camera');cam=bpy.data.objects.new('Canonical_camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO';data.ortho_scale=2*r*1.12;data.clip_start=.0001;data.clip_end=r*40
    if a.gray:bpy.context.view_layer.material_override=make_material('Gray_self_check','#929292',roughness=.85)
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};frames=[]
    for name,d in views.items():
        cam.location=center+Vector(d).normalized()*r*6;_look_at(cam,center);path=a.output/(name+'.png');scene.render.filepath=str(path);start=time.monotonic();bpy.ops.render.render(write_still=True);frames.append({'view':name,'camera_direction_blender':d,'path':path.name,'sha256':digest(path),'seconds':round(time.monotonic()-start,3)})
    if digest(a.glb)!=source_hash:raise RuntimeError('GLB changed during render')
    report={'source_glb_sha256':source_hash,'source_unchanged':True,'actual_glb_import':True,'gray_override':a.gray,'source_blend_render':False,'blender':bpy.app.version_string,'engine':'Cycles CPU','resolution':a.resolution,'samples':a.samples,'threads':2,'denoising':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'camera':{'type':'ORTHO','target':list(center),'scale':data.ortho_scale},'lights':lights,'background_srgb':'#E8E4DC','bounds_blender_m':{'min':lo,'max':hi},'views':frames,'visual_acceptance':'not automatically established','renderer_sha256':digest(__file__)}
    (a.output/'render-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('FOUR_EXACT_GLB_VIEWS_COMPLETE '+source_hash)
if __name__=='__main__':main()
