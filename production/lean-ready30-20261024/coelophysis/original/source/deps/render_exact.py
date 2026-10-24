# SPDX-License-Identifier: MIT
"""Render exactly the supplied GLB, without modifying it or its source blend."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import make_material,_look_at,srgb_to_linear
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    glb=a.glb.resolve();out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True);before=sha(glb)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb));scene=bpy.context.scene
    meshes=[o for o in scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    lo=Vector([min(v[i] for v in points) for i in range(3)]);hi=Vector([max(v[i] for v in points) for i in range(3)]);center=(lo+hi)*.5;span=max(hi-lo)
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=a.resolution;scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral studio illumination');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center);lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
    cd=bpy.data.cameras.new('Evidence camera');camera=bpy.data.objects.new('Evidence camera',cd);scene.collection.objects.link(camera);cd.type='ORTHO';cd.clip_start=.001;cd.clip_end=span*30;scene.camera=camera
    if a.gray: scene.view_layers[0].material_override=make_material('Gray inspection','#929292')
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if a.gray: directions.pop('top')
    records=[]
    for name,direction in directions.items():
        camera.location=center+Vector(direction).normalized()*span*4;_look_at(camera,center);bpy.context.view_layer.update();inverse=camera.matrix_world.inverted();pr=[inverse@v for v in points]
        xmin,xmax=min(v.x for v in pr),max(v.x for v in pr);ymin,ymax=min(v.y for v in pr),max(v.y for v in pr);camera.location+=camera.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));cd.ortho_scale=max(xmax-xmin,ymax-ymin)*1.17
        path=out/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);records.append({'view':name,'camera_direction_blender':direction,'orthographic_scale':cd.ortho_scale,'image':name+'.png','sha256':sha(path)})
    assert before==sha(glb)
    result={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','glb_sha256':before,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'renderer_source_sha256':sha(__file__),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'resolution':a.resolution,'samples':a.samples,'threads':2,'gray_override':a.gray,'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'world_strength':.3,'lights':lights,'bounds_blender_m':{'min':list(lo),'max':list(hi)},'views':records,'gpu_claim':'UNKNOWN'}
    (out/'render-evidence.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__': main()
